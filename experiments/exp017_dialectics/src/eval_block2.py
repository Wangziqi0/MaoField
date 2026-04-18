"""Evaluate Block II coupled runs. For each (dataset, pool, g, scorer) compute nDCG@10, P@10."""
import json, os, math, csv, glob

BASE = "/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics"
RES_DIR = os.path.join(BASE, "results", "block2")

G_VALUES = [0.0, 0.01, 0.05, 0.1, 0.3, 1.0]
POOLS = [6, 20]
DATASETS = ["nfcorpus", "scifact"]
SCORERS = ["F1", "F2", "F3"]

def dcg(order, qrels, k):
    s = 0.0
    for i, d in enumerate(order[:k]):
        rel = qrels.get(d, 0)
        try:
            rel = int(rel)
        except Exception:
            rel = 0
        if rel > 0:
            s += (2**rel - 1) / math.log2(i + 2)
    return s

def ndcg(order, qrels, k):
    d = dcg(order, qrels, k)
    rels = sorted([int(v) for v in qrels.values() if (isinstance(v, (int, float, str)) and int(v) > 0)], reverse=True) if qrels else []
    ideal = sum((2**r - 1) / math.log2(i + 2) for i, r in enumerate(rels[:k]))
    return d / ideal if ideal > 0 else 0.0

def p_at_k(order, qrels, k):
    hits = sum(1 for d in order[:k] if int(qrels.get(d, 0) or 0) > 0)
    return hits / k

def score_order(cands, scorer):
    """Return doc_ids sorted best-first under given scorer."""
    if scorer == "F1":
        # energy diff ascending (small = match)
        return [c["doc_id"] for c in sorted(cands, key=lambda c: c["f1_energy_diff"])]
    elif scorer == "F2":
        # phase lock descending (large = match)
        return [c["doc_id"] for c in sorted(cands, key=lambda c: -c["f2_phase_lock"])]
    elif scorer == "F3":
        # lock step ascending (small = match)
        return [c["doc_id"] for c in sorted(cands, key=lambda c: c["f3_lock_step"])]

def g_tag(g):
    return f"{g:.2f}".replace('.', 'p')

rows = []
# also track BM25 baseline per dataset-pool
bm25_rows = {}

for ds in DATASETS:
    for pool in POOLS:
        for g in G_VALUES:
            path = os.path.join(RES_DIR, f"{ds}_top{pool}_g{g_tag(g)}.json")
            if not os.path.exists(path):
                print("MISSING:", path); continue
            with open(path) as f:
                data = json.load(f)
            runtime = data["runtime_s"]
            pqs = data["per_query"]
            n = len(pqs)
            # BM25 baseline (once per ds,pool)
            if (ds, pool) not in bm25_rows:
                bm25_ndcg = sum(ndcg(q["bm25_order"], q["qrels"], 10) for q in pqs) / n
                bm25_p10 = sum(p_at_k(q["bm25_order"], q["qrels"], 10) for q in pqs) / n
                bm25_rows[(ds, pool)] = (bm25_ndcg, bm25_p10)

            for scorer in SCORERS:
                ndcgs = []
                p10s = []
                for q in pqs:
                    order = score_order(q["candidates"], scorer)
                    ndcgs.append(ndcg(order, q["qrels"], 10))
                    p10s.append(p_at_k(order, q["qrels"], 10))
                ndcg10 = sum(ndcgs) / n
                p10 = sum(p10s) / n
                rows.append({
                    "dataset": ds, "pool_size": pool, "g": g, "scorer": scorer,
                    "n_queries": n, "ndcg10": round(ndcg10, 4),
                    "p10": round(p10, 4), "runtime_s": round(runtime, 1),
                })

# Write CSV
csv_path = os.path.join(BASE, "results", "block2_scan.csv")
with open(csv_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["dataset", "pool_size", "g", "scorer", "n_queries", "ndcg10", "p10", "runtime_s"])
    w.writeheader()
    for r in rows:
        w.writerow(r)
print("Wrote", csv_path)

# Print BM25 baselines
print("\nBM25 baselines:")
for (ds, pool), (nd, pp) in bm25_rows.items():
    print(f"  {ds} top{pool}: BM25 nDCG@10={nd:.4f}  P@10={pp:.4f}")

# Print table
print("\nnDCG@10 by (dataset, pool, scorer, g):")
for ds in DATASETS:
    for pool in POOLS:
        print(f"\n{ds} top-{pool} (BM25={bm25_rows[(ds,pool)][0]:.4f})")
        header = "scorer | " + " | ".join(f"g={g}" for g in G_VALUES)
        print(header)
        for scorer in SCORERS:
            vals = []
            for g in G_VALUES:
                r = next((r for r in rows if r["dataset"]==ds and r["pool_size"]==pool and r["scorer"]==scorer and abs(r["g"]-g)<1e-9), None)
                vals.append(f"{r['ndcg10']:.4f}" if r else "  NA  ")
            print(f"{scorer:6} | " + " | ".join(vals))

# Find g_c per (dataset, pool, scorer)
findings = []
for ds in DATASETS:
    for pool in POOLS:
        for scorer in SCORERS:
            sub = [r for r in rows if r["dataset"]==ds and r["pool_size"]==pool and r["scorer"]==scorer]
            if not sub: continue
            best = max(sub, key=lambda r: r["ndcg10"])
            baseline_row = next(r for r in sub if abs(r["g"])<1e-9)
            findings.append({
                "dataset": ds, "pool": pool, "scorer": scorer,
                "g_c": best["g"], "ndcg_best": best["ndcg10"],
                "ndcg_g0": baseline_row["ndcg10"],
                "bm25_ndcg": round(bm25_rows[(ds, pool)][0], 4),
                "delta_vs_g0": round(best["ndcg10"] - baseline_row["ndcg10"], 4),
                "gain_pct_vs_g0": round(100*(best["ndcg10"]-baseline_row["ndcg10"])/max(baseline_row["ndcg10"],1e-9), 2),
            })

# H1 check (NFCorpus top-20 best vs 0.2026 * 1.2 = 0.243)
print("\n--- g_c findings ---")
for f in findings:
    print(f)

md_path = os.path.join(BASE, "results", "block2_gc_findings.md")
with open(md_path, "w") as fp:
    fp.write("# Block II g_c Findings\n\n")
    fp.write("| dataset | pool | scorer | g_c | nDCG_best | nDCG@g=0 | BM25 nDCG | delta | gain% vs g0 |\n")
    fp.write("|---|---|---|---|---|---|---|---|---|\n")
    for f in findings:
        fp.write(f"| {f['dataset']} | top-{f['pool']} | {f['scorer']} | {f['g_c']} | {f['ndcg_best']} | {f['ndcg_g0']} | {f['bm25_ndcg']} | {f['delta_vs_g0']} | {f['gain_pct_vs_g0']}% |\n")
    # H1 check
    fp.write("\n## H1 check (NFCorpus top-20 best F* vs exp016 E variant 0.2026)\n\n")
    nfc20 = [f for f in findings if f["dataset"]=="nfcorpus" and f["pool"]==20]
    best_nfc20 = max(nfc20, key=lambda r: r["ndcg_best"])
    fp.write(f"- Best across F1/F2/F3 at NFC top-20: scorer={best_nfc20['scorer']} g_c={best_nfc20['g_c']} nDCG={best_nfc20['ndcg_best']}\n")
    fp.write(f"- E-variant baseline (exp016): 0.2026; 1.2x threshold = 0.243\n")
    if best_nfc20["ndcg_best"] >= 0.243:
        fp.write(f"- H1 VERDICT: **成立** (>= 0.243)\n")
    elif best_nfc20["ndcg_best"] > 0.2026:
        fp.write(f"- H1 VERDICT: **弱成立** (> 0.2026 but < 0.243)\n")
    else:
        fp.write(f"- H1 VERDICT: **证伪** (<= 0.2026)\n")
print("Wrote", md_path)
