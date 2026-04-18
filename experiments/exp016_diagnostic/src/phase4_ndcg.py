#!/usr/bin/env python3
"""phase 4 batch A: compute nDCG@10 and P@10 for 4 scorers on NFCorpus+SciFact.

Scorers:
  - BM25: original candidate order
  - S1: byte frequency cosine
  - S4: 3-gram Jaccard
  - MaoField: mao_order from exp015 rust output
"""
import csv
import json
import math
import re
from pathlib import Path

import numpy as np

OUT = Path("/home/amd/HEZIMENG/MaoField/experiments/exp016_diagnostic/results/phase4")
RES = Path("/home/amd/HEZIMENG/MaoField/experiments/exp016_diagnostic/results")

TOKEN_RE = re.compile(r"\w+", re.UNICODE)


def byte_vec(text: str) -> np.ndarray:
    b = text.encode("utf-8", errors="ignore")
    if not b:
        return np.zeros(256, dtype=np.float32)
    arr = np.frombuffer(b, dtype=np.uint8)
    v = np.bincount(arr, minlength=256).astype(np.float32)
    n = np.linalg.norm(v)
    if n > 0:
        v /= n
    return v


def ngram_set(text: str, n: int):
    if len(text) < n:
        return {text} if text else set()
    return {text[i:i + n] for i in range(len(text) - n + 1)}


def jaccard(a, b):
    if not a and not b:
        return 0.0
    u = len(a | b)
    return len(a & b) / u if u else 0.0


def ndcg_at_k(order, qrels, k=10):
    dcg = 0.0
    for i, d in enumerate(order[:k]):
        rel = qrels.get(d, 0)
        if rel > 0:
            dcg += (2 ** rel - 1) / math.log2(i + 2)
    rels = sorted([v for v in qrels.values() if v > 0], reverse=True)
    ideal = 0.0
    for i, r in enumerate(rels[:k]):
        ideal += (2 ** r - 1) / math.log2(i + 2)
    return dcg / ideal if ideal > 0 else 0.0


def p_at_k(order, qrels, k=10):
    hits = sum(1 for d in order[:k] if qrels.get(d, 0) > 0)
    return hits / k


def score_dataset(name: str):
    inp = json.load(open(OUT / f"{name}_stage1_input.json"))
    mao = json.load(open(OUT / f"{name}_stage1_out.json"))

    # index mao per_query by query_id
    mao_map = {pq["query_id"]: pq for pq in mao["per_query"]}

    ndcg = {"bm25": [], "s1": [], "s4": [], "maofield": []}
    prec = {"bm25": [], "s1": [], "s4": [], "maofield": []}

    for item in inp:
        qid = item["query_id"]
        q_text = item["query"]
        cands = item["candidates"]
        qrels = item["qrels"]

        # BM25: original order
        bm25_order = [c["doc_id"] for c in cands]

        # S1
        qv = byte_vec(q_text)
        s1_scores = []
        for c in cands:
            dv = byte_vec(c["text"])
            s1_scores.append(float(np.dot(qv, dv)))
        s1_order = [c["doc_id"] for _, c in sorted(zip(s1_scores, cands),
                                                     key=lambda x: -x[0])]

        # S4
        q3 = ngram_set(q_text, 3)
        s4_scores = [jaccard(q3, ngram_set(c["text"], 3)) for c in cands]
        s4_order = [c["doc_id"] for _, c in sorted(zip(s4_scores, cands),
                                                     key=lambda x: -x[0])]

        # MaoField
        mao_order = mao_map[qid]["mao_order"] if qid in mao_map else bm25_order

        ndcg["bm25"].append(ndcg_at_k(bm25_order, qrels))
        ndcg["s1"].append(ndcg_at_k(s1_order, qrels))
        ndcg["s4"].append(ndcg_at_k(s4_order, qrels))
        ndcg["maofield"].append(ndcg_at_k(mao_order, qrels))
        prec["bm25"].append(p_at_k(bm25_order, qrels))
        prec["s1"].append(p_at_k(s1_order, qrels))
        prec["s4"].append(p_at_k(s4_order, qrels))
        prec["maofield"].append(p_at_k(mao_order, qrels))

    out = {
        "dataset": name,
        "n_queries": len(inp),
        "bm25_ndcg10": float(np.mean(ndcg["bm25"])),
        "s1_ndcg10": float(np.mean(ndcg["s1"])),
        "s4_ndcg10": float(np.mean(ndcg["s4"])),
        "maofield_ndcg10": float(np.mean(ndcg["maofield"])),
        "bm25_p10": float(np.mean(prec["bm25"])),
        "s1_p10": float(np.mean(prec["s1"])),
        "s4_p10": float(np.mean(prec["s4"])),
        "maofield_p10": float(np.mean(prec["maofield"])),
    }
    return out


def main():
    rows = []
    for name in ["nfcorpus", "scifact"]:
        r = score_dataset(name)
        print(r)
        rows.append(r)

    csv_path = RES / "ndcg_comparison_batchA.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"Wrote {csv_path}")

    # markdown
    md = []
    md.append("# Phase 4 Batch A: 四 scorer nDCG@10 对比\n")
    md.append("统一候选池 = BM25 top-100，四 scorer 均在该 100 内重排。\n")
    md.append("| dataset | n_q | BM25 nDCG@10 | S1 (byte-cos) | S4 (3gram-jac) | MaoField |")
    md.append("|---|---:|---:|---:|---:|---:|")
    for r in rows:
        md.append(f"| {r['dataset']} | {r['n_queries']} | {r['bm25_ndcg10']:.4f} | "
                  f"{r['s1_ndcg10']:.4f} | {r['s4_ndcg10']:.4f} | {r['maofield_ndcg10']:.4f} |")
    md.append("\n## P@10\n")
    md.append("| dataset | BM25 | S1 | S4 | MaoField |")
    md.append("|---|---:|---:|---:|---:|")
    for r in rows:
        md.append(f"| {r['dataset']} | {r['bm25_p10']:.4f} | {r['s1_p10']:.4f} | "
                  f"{r['s4_p10']:.4f} | {r['maofield_p10']:.4f} |")

    md.append("\n## 三个诊断问题\n")
    for r in rows:
        dname = r["dataset"]
        d_mao_s1 = (r["maofield_ndcg10"] - r["s1_ndcg10"]) * 100
        d_mao_bm25 = (r["maofield_ndcg10"] - r["bm25_ndcg10"]) * 100
        d_s4_bm25 = (r["s4_ndcg10"] - r["bm25_ndcg10"]) * 100
        md.append(f"- **{dname}**:")
        md.append(f"  - MaoField vs S1: {d_mao_s1:+.2f} pp")
        md.append(f"  - MaoField vs BM25: {d_mao_bm25:+.2f} pp")
        md.append(f"  - S4 vs BM25: {d_s4_bm25:+.2f} pp")

    md_path = OUT / "batchA_summary.md"
    md_path.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
