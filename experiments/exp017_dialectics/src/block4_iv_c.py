#!/usr/bin/env python3
"""IV-C Idealist static: rerank top-20 candidates by cosine(q_emb, d_emb)
using cached BGE-M3 embeddings.

Output: results/block4/IV-C_{ds}.json  with per_query rerank order + nDCG@10
"""
import json, math, time, sys
import numpy as np
from pathlib import Path

EXP17 = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics")
INPUTS = EXP17 / "inputs_block1_top20"
OUT = EXP17 / "results/block4"

DATASETS = ["nfcorpus", "scifact", "fiqa"]


def ndcg_at_k(order, qrels, k=10):
    dcg = 0.0
    for i, d in enumerate(order[:k]):
        rel = qrels.get(d, 0)
        if rel > 0:
            dcg += (2 ** rel - 1) / math.log2(i + 2)
    rels = sorted([v for v in qrels.values() if v > 0], reverse=True)
    ideal = sum((2 ** r - 1) / math.log2(i + 2) for i, r in enumerate(rels[:k]))
    return dcg / ideal if ideal > 0 else 0.0


def p_at_k(order, qrels, k=10):
    return sum(1 for d in order[:k] if qrels.get(d, 0) > 0) / k


def mrr_at_k(order, qrels, k=10):
    for i, d in enumerate(order[:k]):
        if qrels.get(d, 0) > 0:
            return 1.0 / (i + 1)
    return 0.0


def run_one(ds):
    z = np.load(OUT / f"embeddings_{ds}.npz", allow_pickle=True)
    ids = list(z["ids"]); vecs = z["vecs"]
    id2v = {i: vecs[k] for k, i in enumerate(ids)}

    qs = json.load(open(INPUTS / f"{ds}_top20_input.json"))
    per_query = []
    skipped = 0
    t0 = time.time()
    for q in qs:
        qkey = f"q:{q['query_id']}"
        if qkey not in id2v:
            skipped += 1; continue
        qv = id2v[qkey]
        scored = []
        bm_order = []
        for c in q["candidates"]:
            dkey = f"d:{c['doc_id']}"
            bm_order.append(c["doc_id"])
            if dkey not in id2v:
                continue
            sc = float(np.dot(qv, id2v[dkey]))  # already L2 normalized -> cosine
            scored.append((c["doc_id"], sc))
        scored.sort(key=lambda x: -x[1])
        order = [d for d, _ in scored]
        per_query.append({
            "query_id": q["query_id"], "query": q["query"],
            "bm25_order": bm_order, "rerank_order": order,
            "qrels": q["qrels"],
        })
    el = time.time() - t0
    # metrics
    nd = [ndcg_at_k(p["rerank_order"], p["qrels"]) for p in per_query]
    p10 = [p_at_k(p["rerank_order"], p["qrels"]) for p in per_query]
    mrr = [mrr_at_k(p["rerank_order"], p["qrels"]) for p in per_query]
    summary = {
        "dataset": ds,
        "n_queries": len(per_query),
        "skipped": skipped,
        "ndcg10": float(np.mean(nd)) if nd else 0.0,
        "p10": float(np.mean(p10)) if p10 else 0.0,
        "mrr10": float(np.mean(mrr)) if mrr else 0.0,
        "runtime_s": el,
        "per_query": per_query,
    }
    with open(OUT / f"IV-C_{ds}.json", "w") as f:
        json.dump(summary, f)
    print(f"[IV-C/{ds}] n={len(per_query)} skip={skipped} nDCG10={summary['ndcg10']:.4f} P10={summary['p10']:.4f} MRR10={summary['mrr10']:.4f} ({el:.2f}s)")
    return summary


if __name__ == "__main__":
    sel = sys.argv[1:] or DATASETS
    for ds in sel:
        run_one(ds)
