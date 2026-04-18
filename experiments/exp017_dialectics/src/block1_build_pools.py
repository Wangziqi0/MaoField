#!/usr/bin/env python3
"""Block I: build BM25 top-100 candidate pools for fiqa, arguana, trec-covid.

Output one stage1_input.json per dataset in block1 style (same schema as exp016).
Also copies nfcorpus & scifact inputs from exp016/phase4.
"""
import json
import re
import shutil
import time
from pathlib import Path

from rank_bm25 import BM25Okapi

BEIR = Path("/home/amd/HEZIMENG/legal-assistant/beir_data")
EXP16_PHASE4 = Path("/home/amd/HEZIMENG/MaoField/experiments/exp016_diagnostic/results/phase4")
BLOCK1 = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block1")
INPUTS = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/inputs_block1")
INPUTS_TOP20 = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/inputs_block1_top20")
BLOCK1.mkdir(parents=True, exist_ok=True)
INPUTS.mkdir(parents=True, exist_ok=True)
INPUTS_TOP20.mkdir(parents=True, exist_ok=True)

TOKEN_RE = re.compile(r"\w+", re.UNICODE)
TRUNC = 500
TOP_K = 100
TOP_K_E = 20


def tokenize(text: str):
    return TOKEN_RE.findall(text.lower())


def load_corpus(path: Path):
    ids, texts = [], []
    with open(path / "corpus.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            title = obj.get("title") or ""
            body = obj.get("text") or ""
            text = (title + " " + body).strip()
            ids.append(obj["_id"])
            texts.append(text)
    return ids, texts


def load_queries(path: Path):
    ids, texts = [], []
    with open(path / "queries.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            ids.append(obj["_id"])
            texts.append((obj.get("text") or "").strip())
    return ids, texts


def load_qrels(path: Path):
    qrels = {}
    with open(path / "qrels" / "test.tsv", "r", encoding="utf-8") as f:
        f.readline()
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            qid, did, sc = parts[0], parts[1], parts[2]
            try:
                sc = int(sc)
            except ValueError:
                try:
                    sc = int(float(sc))
                except Exception:
                    continue
            if sc <= 0:
                continue
            qrels.setdefault(qid, {})[did] = sc
    return qrels


def build(name: str):
    t0 = time.time()
    path = BEIR / name
    print(f"[{name}] loading ...", flush=True)
    doc_ids, doc_texts = load_corpus(path)
    q_ids, q_texts = load_queries(path)
    qrels = load_qrels(path)
    qid2text = dict(zip(q_ids, q_texts))
    print(f"[{name}] |corpus|={len(doc_ids)} |queries_with_qrels|={len(qrels)}", flush=True)

    print(f"[{name}] building BM25 ...", flush=True)
    tokenized = [tokenize(t) for t in doc_texts]
    bm25 = BM25Okapi(tokenized)
    print(f"[{name}] BM25 built in {time.time()-t0:.1f}s", flush=True)

    eligible_qids = [qid for qid in qrels.keys() if qid in qid2text]
    eligible_qids.sort()
    print(f"[{name}] eligible queries: {len(eligible_qids)}", flush=True)

    out_list = []
    for i, qid in enumerate(eligible_qids):
        q_text = qid2text[qid]
        q_tokens = tokenize(q_text)
        if not q_tokens:
            continue
        scores = bm25.get_scores(q_tokens)
        top_idx = scores.argsort()[::-1][:TOP_K]
        cands = []
        for idx in top_idx:
            text = doc_texts[idx][:TRUNC]
            cands.append({"doc_id": doc_ids[idx], "text": text})
        out_list.append({
            "query_id": qid,
            "query": q_text,
            "candidates": cands,
            "qrels": qrels[qid],
        })
        if (i + 1) % 100 == 0:
            print(f"  [{name}] {i+1}/{len(eligible_qids)}  elapsed={time.time()-t0:.1f}s", flush=True)

    out_path = INPUTS / f"{name}_stage1_input.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_list, f, ensure_ascii=False)
    print(f"[{name}] wrote {out_path}  (n={len(out_list)}, {time.time()-t0:.1f}s)", flush=True)

    # also top20 for variant E
    trunc = [dict(q, candidates=q["candidates"][:TOP_K_E]) for q in out_list]
    with open(INPUTS_TOP20 / f"{name}_top20_input.json", "w", encoding="utf-8") as f:
        json.dump(trunc, f, ensure_ascii=False)


def main():
    # Copy nfcorpus / scifact from exp016 phase4 (already built, same protocol)
    for name in ["nfcorpus", "scifact"]:
        src = EXP16_PHASE4 / f"{name}_stage1_input.json"
        dst = INPUTS / f"{name}_stage1_input.json"
        if src.exists() and not dst.exists():
            shutil.copy(src, dst)
            print(f"copied {src} -> {dst}")
        # also top20 version
        d = json.load(open(dst))
        trunc = [dict(q, candidates=q["candidates"][:TOP_K_E]) for q in d]
        with open(INPUTS_TOP20 / f"{name}_top20_input.json", "w") as f:
            json.dump(trunc, f)

    # Build fresh for fiqa, arguana, trec-covid
    for name in ["fiqa", "arguana", "trec-covid"]:
        out_path = INPUTS / f"{name}_stage1_input.json"
        if out_path.exists():
            print(f"[{name}] already exists, skip")
            continue
        build(name)


if __name__ == "__main__":
    main()
