#!/usr/bin/env python3
"""Block IV Dim 3: adversarial robustness on SciFact 200-query subset.

Steps:
1. Load SciFact top-20 input, take first 200 queries.
2. For each query, replace ~30% of WordNet-substitutable words.
3. Build perturbed input json + perturbed BGE embeddings for IV-B.
4. Run IV-A (variant_A binary), IV-B (block4 binary), IV-C (cosine over BGE),
   IV-D (byte cosine) on the perturbed set.
5. Compute drop = original_nDCG10 - perturbed_nDCG10 per group.
"""
import json, math, time, sys, os, random, subprocess, functools
import numpy as np
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
print = functools.partial(print, flush=True)

random.seed(20260412)

EXP17 = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics")
INPUTS = EXP17 / "inputs_block1_top20"
OUT = EXP17 / "results/block4"
LOG = EXP17 / "logs/block4"

TARGET_FRAC = 0.30  # per spec: 30% content words
SUBSET_N = 200
DS = "scifact"
URL = "http://192.168.31.22:8080/v1/embeddings"

# WordNet
import nltk
try:
    from nltk.corpus import wordnet as wn
    from nltk import pos_tag, word_tokenize
    wn.synsets("dog")
except LookupError:
    nltk.download("wordnet", quiet=True)
    nltk.download("punkt", quiet=True)
    nltk.download("averaged_perceptron_tagger", quiet=True)
    nltk.download("omw-1.4", quiet=True)
    from nltk.corpus import wordnet as wn
    from nltk import pos_tag, word_tokenize

WN_POS = {"NN":"n","NNS":"n","NNP":"n","NNPS":"n",
          "VB":"v","VBD":"v","VBG":"v","VBN":"v","VBP":"v","VBZ":"v",
          "JJ":"a","JJR":"a","JJS":"a","RB":"r","RBR":"r","RBS":"r"}


def get_synonyms(word, pos):
    wnpos = WN_POS.get(pos)
    if not wnpos: return []
    out = []
    for syn in wn.synsets(word, pos=wnpos):
        for lem in syn.lemmas():
            name = lem.name().replace("_", " ")
            if name.lower() != word.lower() and " " not in name and name.isalpha():
                out.append(name)
    return list(dict.fromkeys(out))


def perturb(text, frac=0.3):
    toks = word_tokenize(text); tagged = pos_tag(toks)
    candidates = [(i,w,p) for i,(w,p) in enumerate(tagged)
                  if p in WN_POS and w.isalpha() and len(w)>=3]
    candidates.sort(key=lambda x: -len(x[1]))
    n_target = max(1, int(len(candidates) * frac))
    out = list(toks); replaced = 0
    for i, w, p in candidates:
        if replaced >= n_target: break
        syns = get_synonyms(w, p)
        if syns:
            out[i] = random.choice(syns[:3]); replaced += 1
    return " ".join(out), replaced


def ndcg_at_k(order, qrels, k=10):
    dcg = 0.0
    for i, d in enumerate(order[:k]):
        rel = qrels.get(d, 0)
        if rel > 0: dcg += (2 ** rel - 1) / math.log2(i + 2)
    rels = sorted([v for v in qrels.values() if v > 0], reverse=True)
    ideal = sum((2 ** r - 1) / math.log2(i + 2) for i, r in enumerate(rels[:k]))
    return dcg / ideal if ideal > 0 else 0.0


def byte_vec(text):
    b = text.encode("utf-8", errors="ignore")
    if not b: return np.zeros(256, dtype=np.float32)
    arr = np.frombuffer(b, dtype=np.uint8)
    v = np.bincount(arr, minlength=256).astype(np.float32)
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def embed_one(text):
    try:
        r = requests.post(URL, json={"input":[text], "model":"bge-m3"}, timeout=60)
        r.raise_for_status()
        e = np.asarray(r.json()["data"][0]["embedding"], dtype=np.float32)
        n = np.linalg.norm(e); return e/n if n>0 else e
    except Exception: return None


def main():
    t0 = time.time()
    full = json.load(open(INPUTS / f"{DS}_top20_input.json"))
    subset = full[:SUBSET_N]
    print(f"[dim3] subset={len(subset)} queries from {DS}")

    # Step 1: perturb queries
    perturbed = []
    for q in subset:
        p_txt, n_rep = perturb(q["query"], TARGET_FRAC)
        qq = dict(q); qq["query"] = p_txt
        perturbed.append(qq)
    print(f"[dim3] perturbed {len(perturbed)} queries (avg replacements logged)")

    # Save perturbed input
    pert_in = OUT / "dim3_scifact_perturbed_input.json"
    json.dump(perturbed, open(pert_in, "w"))

    # Step 2: BGE embed perturbed queries (docs unchanged, reuse existing emb)
    print("[dim3] embedding perturbed queries...")
    z_orig = np.load(OUT / f"embeddings_{DS}.npz", allow_pickle=True)
    ids_arr = z_orig["ids"]; vecs_arr = z_orig["vecs"]
    id2idx = {str(ids_arr[k]): k for k in range(len(ids_arr))}

    # Determine which doc IDs are needed (only those in the 200-q subset)
    needed_doc_ids = set()
    for qq in perturbed:
        for c in qq["candidates"]:
            needed_doc_ids.add(c["doc_id"])
    print(f"[dim3] needed docs: {len(needed_doc_ids)}")

    new_qvecs = {}
    with ThreadPoolExecutor(max_workers=16) as ex:
        futs = {ex.submit(embed_one, qq["query"][:500]): qq["query_id"] for qq in perturbed}
        for fut in as_completed(futs):
            qid = futs[fut]
            v = fut.result()
            if v is None:
                idx = id2idx.get(f"q:{qid}")
                v = vecs_arr[idx] if idx is not None else np.zeros(1024, dtype=np.float32)
            new_qvecs[f"q:{qid}"] = v
    print(f"[dim3] embedded {len(new_qvecs)} perturbed queries")

    # Build small embedding json with only perturbed queries + needed docs (~4400 entries)
    import orjson
    small_emb = {}
    for qkey, v in new_qvecs.items():
        small_emb[qkey] = v.astype(np.float32).tolist()
    for did in needed_doc_ids:
        idx = id2idx.get(f"d:{did}")
        if idx is not None:
            small_emb[f"d:{did}"] = vecs_arr[idx].astype(np.float32).tolist()
    pert_emb_json = OUT / "dim3_scifact_perturbed_embeddings.json"
    with open(pert_emb_json, "wb") as f:
        f.write(orjson.dumps(small_emb))
    print(f"[dim3] wrote {len(small_emb)} embedding entries -> {pert_emb_json}")
    # also build id2v for IV-C python (only what we need)
    id2v = {k: np.asarray(v, dtype=np.float32) for k, v in small_emb.items()}
    del small_emb

    # Step 3: run IV-A (variant_A)
    print("[dim3] running IV-A (variant_A) on perturbed...")
    a_out = OUT / "dim3_IV-A_perturbed_out.json"
    if not a_out.exists():
        VBIN = "/home/amd/HEZIMENG/MaoField/experiments/exp016_diagnostic/rust_variants/variant_A/target/release/variant_a_solver"
        with open(LOG/"dim3_IV-A.log","w") as logf:
            subprocess.run([VBIN, str(pert_in), str(a_out)], stdout=logf, stderr=logf, check=True)
    print(f"[dim3] IV-A done -> {a_out}")

    # Step 4: run IV-B (block4 binary)
    print("[dim3] running IV-B (block4) on perturbed...")
    b_out = OUT / "dim3_IV-B_perturbed_out.json"
    if not b_out.exists():
        BBIN = "/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/rust_variants/block4_idealist/target/release/block4_idealist_solver"
        with open(LOG/"dim3_IV-B.log","w") as logf:
            subprocess.run([BBIN, str(pert_in), str(pert_emb_json), str(b_out)],
                           stdout=logf, stderr=logf, check=True)
    print(f"[dim3] IV-B done -> {b_out}")

    # Step 5: IV-C and IV-D (Python)
    print("[dim3] running IV-C and IV-D on perturbed...")
    iv_c_rows = []; iv_d_rows = []
    for qq in perturbed:
        qid = qq["query_id"]
        # IV-C
        qkey = f"q:{qid}"
        qv = new_qvecs[qkey]
        scored_c = []
        for c in qq["candidates"]:
            dv = id2v.get(f"d:{c['doc_id']}")
            if dv is None: continue
            scored_c.append((c["doc_id"], float(np.dot(qv, dv))))
        scored_c.sort(key=lambda x: -x[1])
        order_c = [d for d,_ in scored_c]
        iv_c_rows.append({"query_id": qid, "order": order_c, "qrels": qq["qrels"]})
        # IV-D
        qv_b = byte_vec(qq["query"][:500])
        scored_d = [(c["doc_id"], float(np.dot(qv_b, byte_vec(c["text"][:500])))) for c in qq["candidates"]]
        scored_d.sort(key=lambda x: -x[1])
        order_d = [d for d,_ in scored_d]
        iv_d_rows.append({"query_id": qid, "order": order_d, "qrels": qq["qrels"]})

    # Compute perturbed nDCG@10 per group
    iv_a_data = json.load(open(a_out))
    iv_b_data = json.load(open(b_out))
    pert_ndcg = {}
    pert_ndcg["IV-A"] = float(np.mean([ndcg_at_k(p["mao_order"], p["qrels"]) for p in iv_a_data["per_query"]]))
    pert_ndcg["IV-B"] = float(np.mean([ndcg_at_k(p["mao_order"], p["qrels"]) for p in iv_b_data["per_query"]]))
    pert_ndcg["IV-C"] = float(np.mean([ndcg_at_k(r["order"], r["qrels"]) for r in iv_c_rows]))
    pert_ndcg["IV-D"] = float(np.mean([ndcg_at_k(r["order"], r["qrels"]) for r in iv_d_rows]))

    # Original nDCG@10 on the same 200 query subset
    subset_ids = {qq["query_id"] for qq in subset}
    orig_ndcg = {}
    # IV-A original
    iv_a_orig_path = OUT / f"IV-A_{DS}_out.json"
    if not iv_a_orig_path.exists():
        # fiqa special case n/a here (DS=scifact)
        raise RuntimeError(f"Need {iv_a_orig_path}")
    orig_a = json.load(open(iv_a_orig_path))
    orig_ndcg["IV-A"] = float(np.mean([ndcg_at_k(p["mao_order"], p["qrels"]) for p in orig_a["per_query"] if p["query_id"] in subset_ids]))
    iv_b_orig_path = OUT / f"IV-B_{DS}_out.json"
    orig_b = json.load(open(iv_b_orig_path))
    orig_ndcg["IV-B"] = float(np.mean([ndcg_at_k(p["mao_order"], p["qrels"]) for p in orig_b["per_query"] if p["query_id"] in subset_ids]))
    orig_c = json.load(open(OUT / f"IV-C_{DS}.json"))
    orig_ndcg["IV-C"] = float(np.mean([ndcg_at_k(p["rerank_order"], p["qrels"]) for p in orig_c["per_query"] if p["query_id"] in subset_ids]))
    orig_d = json.load(open(OUT / f"IV-D_{DS}.json"))
    orig_ndcg["IV-D"] = float(np.mean([ndcg_at_k(p["rerank_order"], p["qrels"]) for p in orig_d["per_query"] if p["query_id"] in subset_ids]))

    # Drop = orig - pert (positive = degradation)
    out = {"dataset": DS, "subset_n": SUBSET_N, "frac": TARGET_FRAC,
           "orig_ndcg10": orig_ndcg, "pert_ndcg10": pert_ndcg,
           "drop_ndcg10": {g: orig_ndcg[g] - pert_ndcg[g] for g in ["IV-A","IV-B","IV-C","IV-D"]}}
    with open(OUT / "dim3_robustness.json", "w") as f: json.dump(out, f, indent=2)
    # CSV
    import csv
    with open(OUT / "dim3_robustness.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["group", "orig_nDCG10", "pert_nDCG10", "drop_nDCG10"])
        for g in ["IV-A","IV-B","IV-C","IV-D"]:
            w.writerow([g, f"{orig_ndcg[g]:.4f}", f"{pert_ndcg[g]:.4f}", f"{out['drop_ndcg10'][g]:.4f}"])
    print(f"[dim3] DONE in {time.time()-t0:.1f}s")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
