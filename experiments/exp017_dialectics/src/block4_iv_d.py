#!/usr/bin/env python3
"""IV-D Materialist static: rerank top-20 by cosine of UTF-8 byte-frequency
vectors (256-dim) — same scoring family as block1 S1, but on the top-20 pool
to keep the IV-A/B/C/D candidate set identical."""
import json, math, time, sys
import numpy as np
from pathlib import Path

EXP17 = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics")
INPUTS = EXP17 / "inputs_block1_top20"
OUT = EXP17 / "results/block4"

DATASETS = ["nfcorpus", "scifact", "fiqa"]


def byte_vec(text):
    b = text.encode("utf-8", errors="ignore")
    if not b:
        return np.zeros(256, dtype=np.float32)
    arr = np.frombuffer(b, dtype=np.uint8)
    v = np.bincount(arr, minlength=256).astype(np.float32)
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def ndcg_at_k(order, qrels, k=10):
    dcg = 0.0
    for i, d in enumerate(order[:k]):
        rel = qrels.get(d, 0)
        if rel > 0: dcg += (2 ** rel - 1) / math.log2(i + 2)
    rels = sorted([v for v in qrels.values() if v > 0], reverse=True)
    ideal = sum((2 ** r - 1) / math.log2(i + 2) for i, r in enumerate(rels[:k]))
    return dcg / ideal if ideal > 0 else 0.0


def p_at_k(order, qrels, k=10):
    return sum(1 for d in order[:k] if qrels.get(d, 0) > 0) / k


def mrr_at_k(order, qrels, k=10):
    for i, d in enumerate(order[:k]):
        if qrels.get(d, 0) > 0: return 1.0 / (i + 1)
    return 0.0


def run_one(ds):
    qs = json.load(open(INPUTS / f"{ds}_top20_input.json"))
    per_query = []
    t0 = time.time()
    for q in qs:
        qv = byte_vec(q["query"][:500])
        scored = []
        bm_order = []
        for c in q["candidates"]:
            bm_order.append(c["doc_id"])
            dv = byte_vec(c["text"][:500])
            scored.append((c["doc_id"], float(np.dot(qv, dv))))
        scored.sort(key=lambda x: -x[1])
        order = [d for d, _ in scored]
        per_query.append({
            "query_id": q["query_id"], "query": q["query"],
            "bm25_order": bm_order, "rerank_order": order,
            "qrels": q["qrels"],
        })
    el = time.time() - t0
    nd = [ndcg_at_k(p["rerank_order"], p["qrels"]) for p in per_query]
    p10 = [p_at_k(p["rerank_order"], p["qrels"]) for p in per_query]
    mrr = [mrr_at_k(p["rerank_order"], p["qrels"]) for p in per_query]
    summary = {
        "dataset": ds,
        "n_queries": len(per_query),
        "ndcg10": float(np.mean(nd)) if nd else 0.0,
        "p10": float(np.mean(p10)) if p10 else 0.0,
        "mrr10": float(np.mean(mrr)) if mrr else 0.0,
        "runtime_s": el,
        "per_query": per_query,
    }
    with open(OUT / f"IV-D_{ds}.json", "w") as f:
        json.dump(summary, f)
    print(f"[IV-D/{ds}] n={len(per_query)} nDCG10={summary['ndcg10']:.4f} P10={summary['p10']:.4f} MRR10={summary['mrr10']:.4f} ({el:.2f}s)")


if __name__ == "__main__":
    sel = sys.argv[1:] or DATASETS
    for ds in sel: run_one(ds)
