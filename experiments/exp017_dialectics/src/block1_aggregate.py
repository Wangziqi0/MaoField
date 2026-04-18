#!/usr/bin/env python3
"""Block I aggregate: compute nDCG@10 / P@10 / MRR@10 for all scorer x dataset
rank files in results/block1 + MaoField_baseline + MaoField_E from exp016 & block2.

Outputs:
  results/block1_baselines.csv    (columns: dataset, scorer, n_queries,
                                             ndcg10, p10, mrr10, runtime_s)
  results/block1_summary.md       (5 x 6 nDCG@10 markdown table + observations)
"""
import csv
import json
import math
from pathlib import Path

import numpy as np

EXP17 = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics")
INPUTS = EXP17 / "inputs_block1"
BLOCK1 = EXP17 / "results/block1"
EXP16_P4 = Path("/home/amd/HEZIMENG/MaoField/experiments/exp016_diagnostic/results/phase4")
EXP16_P6 = Path("/home/amd/HEZIMENG/MaoField/experiments/exp016_diagnostic/results/phase6_ablation")

DATASETS = ["nfcorpus", "scifact", "fiqa", "arguana", "trec-covid"]
SCORERS = ["bm25", "s1", "s4", "bge", "maofield_baseline", "maofield_E"]


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


def mrr_at_k(order, qrels, k=10):
    for i, d in enumerate(order[:k]):
        if qrels.get(d, 0) > 0:
            return 1.0 / (i + 1)
    return 0.0


def load_input(ds):
    p = INPUTS / f"{ds}_stage1_input.json"
    if not p.exists():
        return None
    return json.load(open(p))


def get_mao_ranks(ds, variant):
    """variant in {'baseline','E'}.

    For nfcorpus/scifact we reuse exp016 outputs.
    For fiqa/arguana/trec-covid expect outputs in block1/{ds}_maofield_{variant}_out.json.
    """
    if variant == "baseline":
        if ds in ("nfcorpus", "scifact"):
            p = EXP16_P4 / f"{ds}_stage1_out.json"
        else:
            p = BLOCK1 / f"{ds}_maofield_baseline_out.json"
    elif variant == "E":
        if ds in ("nfcorpus", "scifact"):
            p = EXP16_P6 / f"variant_E_{ds}_out.json"
        else:
            p = BLOCK1 / f"{ds}_maofield_E_out.json"
    else:
        return None
    if not p.exists():
        return None
    d = json.load(open(p))
    ranks = {pq["query_id"]: pq["mao_order"] for pq in d["per_query"]}
    runtime = d.get("total_time_s", 0.0)
    return ranks, runtime


def score_ranks_file(path, qrels_by_qid):
    d = json.load(open(path))
    ndcgs, p10s, mrrs = [], [], []
    for r in d["ranks"]:
        qid = r["query_id"]
        qrels = qrels_by_qid.get(qid, {})
        if not qrels:
            continue
        order = r["order"]
        ndcgs.append(ndcg_at_k(order, qrels))
        p10s.append(p_at_k(order, qrels))
        mrrs.append(mrr_at_k(order, qrels))
    return {
        "n_queries": len(ndcgs),
        "ndcg10": float(np.mean(ndcgs)) if ndcgs else 0.0,
        "p10": float(np.mean(p10s)) if p10s else 0.0,
        "mrr10": float(np.mean(mrrs)) if mrrs else 0.0,
        "runtime_s": d.get("runtime_s", 0.0),
    }


def score_mao_ranks(rank_map, runtime, qrels_by_qid, qid_list):
    ndcgs, p10s, mrrs = [], [], []
    for qid in qid_list:
        if qid not in rank_map:
            continue
        order = rank_map[qid]
        qrels = qrels_by_qid.get(qid, {})
        if not qrels:
            continue
        ndcgs.append(ndcg_at_k(order, qrels))
        p10s.append(p_at_k(order, qrels))
        mrrs.append(mrr_at_k(order, qrels))
    return {
        "n_queries": len(ndcgs),
        "ndcg10": float(np.mean(ndcgs)) if ndcgs else 0.0,
        "p10": float(np.mean(p10s)) if p10s else 0.0,
        "mrr10": float(np.mean(mrrs)) if mrrs else 0.0,
        "runtime_s": runtime,
    }


def main():
    rows = []
    for ds in DATASETS:
        data = load_input(ds)
        if data is None:
            print(f"[{ds}] no stage1_input yet, skip")
            continue
        qrels_by_qid = {it["query_id"]: it["qrels"] for it in data}
        qid_list = [it["query_id"] for it in data]

        for scorer in ["bm25", "s1", "s4", "bge"]:
            p = BLOCK1 / f"{ds}_{scorer}_ranks.json"
            if not p.exists():
                print(f"[{ds}/{scorer}] MISSING")
                continue
            m = score_ranks_file(p, qrels_by_qid)
            m.update({"dataset": ds, "scorer": scorer})
            rows.append(m)

        for variant_key, variant in [("maofield_baseline", "baseline"),
                                     ("maofield_E", "E")]:
            got = get_mao_ranks(ds, variant)
            if got is None:
                print(f"[{ds}/{variant_key}] MISSING")
                continue
            rank_map, runtime = got
            m = score_mao_ranks(rank_map, runtime, qrels_by_qid, qid_list)
            m.update({"dataset": ds, "scorer": variant_key})
            rows.append(m)

    # CSV
    csv_path = EXP17 / "results/block1_baselines.csv"
    fields = ["dataset", "scorer", "n_queries", "ndcg10", "p10", "mrr10", "runtime_s"]
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})
    print(f"wrote {csv_path}  ({len(rows)} rows)")

    # Build 5 x 6 ndcg table
    idx = {(r["dataset"], r["scorer"]): r for r in rows}
    md = []
    md.append("# Block I baseline table  (5 datasets x 6 scorers)\n")
    md.append("Pool = BM25 top-100 per query. All scorers rerank within this pool.\n")
    md.append("Metric below: **nDCG@10** (mean over queries with non-empty qrels).\n")
    header = "| dataset | " + " | ".join(SCORERS) + " |"
    sep = "|---|" + "|".join(["---:"] * len(SCORERS)) + "|"
    md.append(header)
    md.append(sep)
    for ds in DATASETS:
        cells = [ds]
        for sc in SCORERS:
            r = idx.get((ds, sc))
            cells.append(f"{r['ndcg10']:.4f}" if r else "-")
        md.append("| " + " | ".join(cells) + " |")

    md.append("\n## P@10\n")
    md.append(header); md.append(sep)
    for ds in DATASETS:
        cells = [ds]
        for sc in SCORERS:
            r = idx.get((ds, sc))
            cells.append(f"{r['p10']:.4f}" if r else "-")
        md.append("| " + " | ".join(cells) + " |")

    md.append("\n## MRR@10\n")
    md.append(header); md.append(sep)
    for ds in DATASETS:
        cells = [ds]
        for sc in SCORERS:
            r = idx.get((ds, sc))
            cells.append(f"{r['mrr10']:.4f}" if r else "-")
        md.append("| " + " | ".join(cells) + " |")

    # Observations: MaoField-E vs S1, vs BGE
    md.append("\n## Core observations\n")
    for ds in DATASETS:
        s1 = idx.get((ds, "s1"))
        bge = idx.get((ds, "bge"))
        mE = idx.get((ds, "maofield_E"))
        mB = idx.get((ds, "maofield_baseline"))
        parts = [f"- **{ds}**:"]
        if mE and s1 and s1["ndcg10"] > 0:
            d = (mE["ndcg10"] - s1["ndcg10"]) / s1["ndcg10"] * 100
            parts.append(f"MaoField-E vs S1 = {d:+.1f}%")
        if mE and bge:
            d = (mE["ndcg10"] - bge["ndcg10"]) * 100
            parts.append(f"MaoField-E - BGE = {d:+.2f} pp")
        if mB and mE:
            d = (mE["ndcg10"] - mB["ndcg10"]) * 100
            parts.append(f"E - baseline = {d:+.2f} pp")
        md.append("  ".join(parts))

    md_path = EXP17 / "results/block1_summary.md"
    md_path.write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {md_path}")


if __name__ == "__main__":
    main()
