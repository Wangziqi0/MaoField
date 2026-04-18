#!/usr/bin/env python3
"""Block IV evaluation: build the 4-group x 3-dataset x 5-dimension matrix.

Inputs (must already exist):
  results/block4/IV-A_{ds}_out.json   (variant_A FUSION=0 byte-source PDE)
    - Special case: fiqa reuses block1/fiqa_maofield_E_out.json
  results/block4/IV-B_{ds}_out.json   (BGE-source GL FUSION=0 PDE)
  results/block4/IV-C_{ds}.json       (BGE cosine static)
  results/block4/IV-D_{ds}.json       (byte-freq cosine static)
"""
import json, math, csv, sys
import numpy as np
from pathlib import Path

EXP17 = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics")
OUT = EXP17 / "results/block4"
BLOCK1 = EXP17 / "results/block1"

DATASETS = ["nfcorpus", "scifact", "fiqa"]
GROUPS = ["IV-A", "IV-B", "IV-C", "IV-D"]


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


def load_group(group, ds):
    """Return list of dict with keys: query_id, query, order, qrels."""
    if group == "IV-A":
        if ds == "fiqa":
            p = BLOCK1 / "fiqa_maofield_E_out.json"
        else:
            p = OUT / f"IV-A_{ds}_out.json"
        d = json.load(open(p))
        return [
            {"query_id": q["query_id"], "query": q["query"],
             "order": q["mao_order"], "qrels": q["qrels"]}
            for q in d["per_query"]
        ]
    if group == "IV-B":
        p = OUT / f"IV-B_{ds}_out.json"
        d = json.load(open(p))
        return [
            {"query_id": q["query_id"], "query": q["query"],
             "order": q["mao_order"], "qrels": q["qrels"]}
            for q in d["per_query"]
        ]
    if group == "IV-C":
        d = json.load(open(OUT / f"IV-C_{ds}.json"))
        return [
            {"query_id": q["query_id"], "query": q["query"],
             "order": q["rerank_order"], "qrels": q["qrels"]}
            for q in d["per_query"]
        ]
    if group == "IV-D":
        d = json.load(open(OUT / f"IV-D_{ds}.json"))
        return [
            {"query_id": q["query_id"], "query": q["query"],
             "order": q["rerank_order"], "qrels": q["qrels"]}
            for q in d["per_query"]
        ]
    raise ValueError(group)


def metric(rows, fn):
    if not rows: return 0.0
    return float(np.mean([fn(r["order"], r["qrels"]) for r in rows]))


def dim1_overall():
    """4 groups x 3 datasets nDCG@10."""
    table = {}  # (ds, group) -> ndcg
    n_table = {}  # (ds, group) -> n
    for ds in DATASETS:
        for g in GROUPS:
            try:
                rows = load_group(g, ds)
            except FileNotFoundError as e:
                print(f"  WARN: {g}/{ds} missing: {e}")
                table[(ds, g)] = float("nan"); n_table[(ds, g)] = 0; continue
            table[(ds, g)] = metric(rows, ndcg_at_k)
            n_table[(ds, g)] = len(rows)
    return table, n_table


def dim2_longtail():
    """Subset queries with <5 words. Compute nDCG@10."""
    table = {}; subset_n = {}
    for ds in DATASETS:
        # Use IV-A's queries (any group's queries should be ~same)
        try:
            ref = load_group("IV-A", ds)
        except FileNotFoundError:
            ref = load_group("IV-B", ds)
        short_ids = {r["query_id"] for r in ref if len(r["query"].split()) < 5}
        subset_n[ds] = len(short_ids)
        for g in GROUPS:
            try:
                rows = load_group(g, ds)
            except FileNotFoundError:
                table[(ds, g)] = float("nan"); continue
            sub = [r for r in rows if r["query_id"] in short_ids]
            table[(ds, g)] = metric(sub, ndcg_at_k)
    return table, subset_n


def write_matrix(dim1, dim2, dim2_n, dim3=None, dim4=None, dim5=None):
    rows = []
    # dim1
    for ds in DATASETS:
        rows.append({
            "dimension": "总体nDCG10", "dataset": ds,
            **{f"{g}": f"{dim1.get((ds,g), float('nan')):.4f}" for g in GROUPS}
        })
    # dim2
    for ds in DATASETS:
        rows.append({
            "dimension": f"长尾nDCG10(n={dim2_n.get(ds,0)})", "dataset": ds,
            **{f"{g}": f"{dim2.get((ds,g), float('nan')):.4f}" for g in GROUPS}
        })
    # dim3 (only scifact)
    if dim3:
        for ds in DATASETS:
            if ds in dim3:
                rows.append({
                    "dimension": "鲁棒性drop_nDCG10(扰动-原)", "dataset": ds,
                    **{f"{g}": f"{dim3[ds].get(g, float('nan')):.4f}" for g in GROUPS}
                })
    # dim4
    if dim4:
        rows.append({
            "dimension": "attractor_k* (kmeans silhouette)", "dataset": "nfcorpus_doc100",
            "IV-A": str(dim4.get("IV-A", "NA")), "IV-B": str(dim4.get("IV-B", "NA")),
            "IV-C": "NA", "IV-D": "NA"
        })
    if dim5:
        for ds, vals in dim5.items():
            rows.append({"dimension": "crosslingual_AUC", "dataset": ds,
                         **{g: f"{vals.get(g, float('nan')):.4f}" for g in GROUPS}})
    out_csv = OUT / "block4_matrix.csv"
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["dimension", "dataset"] + GROUPS)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"Wrote {out_csv}")
    return rows


def main():
    print("=== Dim 1: overall nDCG@10 ===")
    d1, d1n = dim1_overall()
    for ds in DATASETS:
        print(f"  {ds}: " + ", ".join(f"{g}={d1[(ds,g)]:.4f}(n={d1n[(ds,g)]})" for g in GROUPS))
    print("=== Dim 2: longtail (<5 word query) nDCG@10 ===")
    d2, d2n = dim2_longtail()
    for ds in DATASETS:
        print(f"  {ds}: subset={d2n[ds]} " + ", ".join(f"{g}={d2[(ds,g)]:.4f}" for g in GROUPS))
    # dim3 robustness
    dim3 = None
    p3 = OUT/"dim3_robustness.json"
    if p3.exists():
        d3raw = json.load(open(p3))
        dim3 = {d3raw["dataset"]: d3raw["drop_ndcg10"]}
        print(f"=== Dim 3: robustness drop on {d3raw['dataset']} subset={d3raw['subset_n']} ===")
        for g in GROUPS:
            print(f"  {g}: orig={d3raw['orig_ndcg10'][g]:.4f} pert={d3raw['pert_ndcg10'][g]:.4f} drop={d3raw['drop_ndcg10'][g]:+.4f}")
    # dim4
    dim4 = None
    p4 = OUT/"dim4_attractor_k.json"
    if p4.exists():
        d4raw = json.load(open(p4))
        dim4 = {g: d4raw[g]["k_star"] for g in d4raw}
        print(f"=== Dim 4: attractor k* (nfcorpus 100 docs) ===")
        for g, v in dim4.items(): print(f"  {g}: k*={d4raw[g]['k_star']} sil={d4raw[g]['silhouette']:.4f} rep={d4raw[g]['best_rep']}")
    write_matrix(d1, d2, d2n, dim3, dim4)


if __name__ == "__main__":
    main()
