"""
MaoField Experiment 001: Subspace Variance Analysis
====================================================
基础设施实验：验证 PQ 子空间方差能否区分"显式"和"隐含"语义。

原理：
- 4096d embedding 切分为 64 个 64d 子空间
- 每个文档的点云(~356 tokens)在每个子空间有不同的方差
- 高方差子空间 = tokens 在此维度表达丰富 = "说了的"（显式）
- 低方差子空间 = tokens 在此维度聚集 = "没说的"（隐含）
- 子空间方差的分布模式 = 文档的"矛盾结构"

输出：
1. 每个文档的 64 维方差向量
2. 全局子空间活跃度排名
3. 显式/隐含子空间的统计分析
4. query vs doc 的子空间活跃度对比
"""

import sqlite3
import numpy as np
import json
import time
import os

DATA_DIR = "/home/amd/HEZIMENG/legal-assistant/beir_data/nfcorpus"
OUT_DIR = "/home/amd/HEZIMENG/MaoField/experiments"

N_SUBSPACES = 64
SUB_DIM = 64  # 4096 / 64

def load_clouds(db_path, limit=None):
    """Load token clouds from sqlite, return {file_id: np.array(n_tokens, 4096)}"""
    db = sqlite3.connect(db_path)
    cur = db.cursor()

    if limit:
        rows = cur.execute(
            "SELECT file_id, vector FROM chunks ORDER BY file_id LIMIT ?", (limit,)
        ).fetchall()
    else:
        rows = cur.execute("SELECT file_id, vector FROM chunks ORDER BY file_id").fetchall()
    db.close()

    clouds = {}
    for file_id, blob in rows:
        vec = np.frombuffer(blob, dtype=np.float32)
        if file_id not in clouds:
            clouds[file_id] = []
        clouds[file_id].append(vec)

    # Convert to numpy arrays
    for fid in clouds:
        clouds[fid] = np.stack(clouds[fid])

    return clouds


def compute_subspace_variance(cloud):
    """
    For a single document cloud (n_tokens, 4096):
    Split into 64 subspaces of 64d each.
    Compute variance of tokens in each subspace.
    Returns: (64,) variance vector
    """
    n_tokens = cloud.shape[0]
    if n_tokens < 2:
        return np.zeros(N_SUBSPACES)

    # Reshape to (n_tokens, 64, 64)
    reshaped = cloud.reshape(n_tokens, N_SUBSPACES, SUB_DIM)

    # Variance per subspace: mean of per-dimension variance across tokens
    # Shape: (64, 64) -> mean over dim -> (64,)
    var_per_sub = np.var(reshaped, axis=0).mean(axis=1)

    return var_per_sub


def compute_subspace_coverage(cloud, threshold_ratio=0.1):
    """
    For each subspace, compute what fraction of the 64d hypercube is "covered" by tokens.
    Low coverage = "空洞" (void) = implicit/unsaid.

    Method: compute the volume of the bounding box of tokens in each subspace,
    relative to the full range.
    """
    n_tokens = cloud.shape[0]
    if n_tokens < 2:
        return np.zeros(N_SUBSPACES)

    reshaped = cloud.reshape(n_tokens, N_SUBSPACES, SUB_DIM)

    # For each subspace: range of each dimension
    ranges = np.ptp(reshaped, axis=0)  # (64, 64) - peak-to-peak range

    # Mean range per subspace (normalized by global std to be comparable)
    mean_range = ranges.mean(axis=1)  # (64,)

    return mean_range


def compute_subspace_entropy(cloud, n_bins=8):
    """
    For each subspace, discretize token positions and compute entropy.
    High entropy = tokens spread uniformly = explicit/active
    Low entropy = tokens clustered = implicit/compressed
    """
    n_tokens = cloud.shape[0]
    if n_tokens < 3:
        return np.zeros(N_SUBSPACES)

    reshaped = cloud.reshape(n_tokens, N_SUBSPACES, SUB_DIM)

    entropies = np.zeros(N_SUBSPACES)
    for s in range(N_SUBSPACES):
        sub_data = reshaped[:, s, :]  # (n_tokens, 64)
        # Project to 1D via first PC for simplicity
        centered = sub_data - sub_data.mean(axis=0)
        if np.allclose(centered, 0):
            continue
        # Use variance along each dim, sum top-k
        dim_var = np.var(sub_data, axis=0)
        top_dim = np.argmax(dim_var)
        vals = sub_data[:, top_dim]

        # Histogram entropy
        hist, _ = np.histogram(vals, bins=n_bins)
        hist = hist / hist.sum()
        hist = hist[hist > 0]
        entropies[s] = -np.sum(hist * np.log2(hist))

    return entropies


def analyze_tension(var_vector):
    """
    Compute "tension" = disparity between subspace variances.
    High tension = some subspaces very active, others very quiet = strong contradiction structure.
    """
    if var_vector.sum() == 0:
        return 0.0
    normalized = var_vector / var_vector.sum()
    # Gini coefficient as tension measure
    sorted_v = np.sort(normalized)
    n = len(sorted_v)
    index = np.arange(1, n + 1)
    gini = (2 * np.sum(index * sorted_v) / (n * np.sum(sorted_v))) - (n + 1) / n
    return gini


def main():
    print("=" * 60)
    print("MaoField Exp001: Subspace Variance Analysis")
    print("=" * 60)

    # --- Load document clouds ---
    t0 = time.time()
    print("\n[1/6] Loading document token clouds...")
    doc_clouds = load_clouds(os.path.join(DATA_DIR, "token_clouds.sqlite"))
    print(f"  Loaded {len(doc_clouds)} documents, {sum(c.shape[0] for c in doc_clouds.values())} total tokens")
    print(f"  Time: {time.time()-t0:.1f}s")

    # --- Load query clouds ---
    t1 = time.time()
    print("\n[2/6] Loading query token clouds...")
    query_clouds = load_clouds(os.path.join(DATA_DIR, "query_token_clouds.sqlite"))
    print(f"  Loaded {len(query_clouds)} queries, {sum(c.shape[0] for c in query_clouds.values())} total tokens")
    print(f"  Time: {time.time()-t1:.1f}s")

    # --- Compute subspace variance for all docs ---
    t2 = time.time()
    print("\n[3/6] Computing subspace variance for documents...")
    doc_variances = {}
    doc_coverages = {}
    doc_entropies = {}
    doc_tensions = {}

    for fid, cloud in doc_clouds.items():
        var_vec = compute_subspace_variance(cloud)
        doc_variances[fid] = var_vec
        doc_coverages[fid] = compute_subspace_coverage(cloud)
        doc_entropies[fid] = compute_subspace_entropy(cloud)
        doc_tensions[fid] = analyze_tension(var_vec)

    print(f"  Time: {time.time()-t2:.1f}s")

    # --- Compute subspace variance for all queries ---
    t3 = time.time()
    print("\n[4/6] Computing subspace variance for queries...")
    query_variances = {}
    query_tensions = {}

    for fid, cloud in query_clouds.items():
        var_vec = compute_subspace_variance(cloud)
        query_variances[fid] = var_vec
        query_tensions[fid] = analyze_tension(var_vec)

    print(f"  Time: {time.time()-t3:.1f}s")

    # --- Global analysis ---
    print("\n[5/6] Analyzing subspace patterns...")

    # Stack all doc variances
    all_doc_var = np.stack(list(doc_variances.values()))  # (2473, 64)
    all_query_var = np.stack(list(query_variances.values()))  # (3237, 64)

    # Global subspace activity ranking
    global_activity = all_doc_var.mean(axis=0)  # (64,)
    ranked_subspaces = np.argsort(global_activity)[::-1]

    print(f"\n  === Global Subspace Activity (docs) ===")
    print(f"  Most active 5:  {ranked_subspaces[:5].tolist()}")
    print(f"  Least active 5: {ranked_subspaces[-5:].tolist()}")
    print(f"  Activity range: {global_activity.min():.6f} ~ {global_activity.max():.6f}")
    print(f"  Activity ratio (max/min): {global_activity.max()/global_activity.min():.1f}x")

    # Explicit vs implicit split
    median_activity = np.median(global_activity)
    explicit_subs = np.where(global_activity >= median_activity)[0]
    implicit_subs = np.where(global_activity < median_activity)[0]

    print(f"\n  === Explicit vs Implicit Split (by median) ===")
    print(f"  Explicit subspaces (top 32): {sorted(explicit_subs.tolist())}")
    print(f"  Implicit subspaces (bot 32): {sorted(implicit_subs.tolist())}")
    print(f"  Explicit mean variance: {global_activity[explicit_subs].mean():.6f}")
    print(f"  Implicit mean variance: {global_activity[implicit_subs].mean():.6f}")
    print(f"  Ratio: {global_activity[explicit_subs].mean() / global_activity[implicit_subs].mean():.2f}x")

    # Query vs doc comparison
    query_activity = all_query_var.mean(axis=0)
    correlation = np.corrcoef(global_activity, query_activity)[0, 1]

    print(f"\n  === Query vs Doc Subspace Activity ===")
    print(f"  Correlation: {correlation:.4f}")
    print(f"  Doc activity range:   {global_activity.min():.6f} ~ {global_activity.max():.6f}")
    print(f"  Query activity range: {query_activity.min():.6f} ~ {query_activity.max():.6f}")

    # Where do queries and docs DISAGREE most?
    # Normalize both to [0,1] for comparison
    doc_norm = (global_activity - global_activity.min()) / (global_activity.max() - global_activity.min())
    query_norm = (query_activity - query_activity.min()) / (query_activity.max() - query_activity.min())
    disagreement = np.abs(doc_norm - query_norm)
    top_disagree = np.argsort(disagreement)[::-1][:10]

    print(f"\n  === Top 10 Disagreement Subspaces (query active but doc quiet, or vice versa) ===")
    for idx, s in enumerate(top_disagree):
        print(f"  #{idx+1} Sub {s}: doc={doc_norm[s]:.3f} query={query_norm[s]:.3f} gap={disagreement[s]:.3f}")

    # Tension analysis
    all_tensions = list(doc_tensions.values())
    query_all_tensions = list(query_tensions.values())

    print(f"\n  === Tension (Gini of subspace variance) ===")
    print(f"  Doc tension:   mean={np.mean(all_tensions):.4f}, std={np.std(all_tensions):.4f}")
    print(f"  Query tension: mean={np.mean(query_all_tensions):.4f}, std={np.std(query_all_tensions):.4f}")
    print(f"  (Higher tension = stronger contradiction structure)")

    # Coverage / void analysis
    all_doc_cov = np.stack(list(doc_coverages.values()))
    global_coverage = all_doc_cov.mean(axis=0)
    low_cov_subs = np.argsort(global_coverage)[:10]

    print(f"\n  === Coverage / Void Analysis (docs) ===")
    print(f"  Lowest coverage subspaces (most 'void'): {low_cov_subs.tolist()}")
    print(f"  Coverage range: {global_coverage.min():.6f} ~ {global_coverage.max():.6f}")

    # Entropy analysis
    all_doc_ent = np.stack(list(doc_entropies.values()))
    global_entropy = all_doc_ent.mean(axis=0)

    print(f"\n  === Entropy Analysis (docs) ===")
    print(f"  Entropy range: {global_entropy.min():.4f} ~ {global_entropy.max():.4f}")
    print(f"  Low entropy subs (clustered/implicit): {np.argsort(global_entropy)[:5].tolist()}")
    print(f"  High entropy subs (spread/explicit):   {np.argsort(global_entropy)[-5:][::-1].tolist()}")

    # Cross-validate: do variance, coverage, entropy agree on which subs are "implicit"?
    var_rank = np.argsort(global_activity)  # low to high
    cov_rank = np.argsort(global_coverage)
    ent_rank = np.argsort(global_entropy)

    # Top 16 "implicit" by each metric
    var_implicit = set(var_rank[:16].tolist())
    cov_implicit = set(cov_rank[:16].tolist())
    ent_implicit = set(ent_rank[:16].tolist())

    print(f"\n  === Cross-validation: Top 16 'Implicit' Subspaces ===")
    print(f"  By variance:  {sorted(var_implicit)}")
    print(f"  By coverage:  {sorted(cov_implicit)}")
    print(f"  By entropy:   {sorted(ent_implicit)}")
    print(f"  Var ∩ Cov:    {sorted(var_implicit & cov_implicit)} ({len(var_implicit & cov_implicit)}/16)")
    print(f"  Var ∩ Ent:    {sorted(var_implicit & ent_implicit)} ({len(var_implicit & ent_implicit)}/16)")
    print(f"  All three:    {sorted(var_implicit & cov_implicit & ent_implicit)} ({len(var_implicit & cov_implicit & ent_implicit)}/16)")

    # --- Save results ---
    print("\n[6/6] Saving results...")

    results = {
        "meta": {
            "dataset": "NFCorpus",
            "n_docs": len(doc_clouds),
            "n_queries": len(query_clouds),
            "n_subspaces": N_SUBSPACES,
            "sub_dim": SUB_DIM,
            "date": "2026-04-08"
        },
        "global_subspace_activity": {
            "doc_mean_variance": global_activity.tolist(),
            "query_mean_variance": query_activity.tolist(),
            "doc_query_correlation": float(correlation),
            "most_active_5": ranked_subspaces[:5].tolist(),
            "least_active_5": ranked_subspaces[-5:].tolist(),
            "activity_ratio": float(global_activity.max() / global_activity.min())
        },
        "explicit_implicit_split": {
            "explicit_subspaces": sorted(explicit_subs.tolist()),
            "implicit_subspaces": sorted(implicit_subs.tolist()),
            "explicit_mean_var": float(global_activity[explicit_subs].mean()),
            "implicit_mean_var": float(global_activity[implicit_subs].mean()),
            "ratio": float(global_activity[explicit_subs].mean() / global_activity[implicit_subs].mean())
        },
        "tension": {
            "doc_mean": float(np.mean(all_tensions)),
            "doc_std": float(np.std(all_tensions)),
            "query_mean": float(np.mean(query_all_tensions)),
            "query_std": float(np.std(query_all_tensions))
        },
        "cross_validation": {
            "var_implicit_16": sorted(var_implicit),
            "cov_implicit_16": sorted(cov_implicit),
            "ent_implicit_16": sorted(ent_implicit),
            "var_cov_overlap": len(var_implicit & cov_implicit),
            "var_ent_overlap": len(var_implicit & ent_implicit),
            "all_three_overlap": len(var_implicit & cov_implicit & ent_implicit),
            "consensus_implicit": sorted(var_implicit & cov_implicit & ent_implicit)
        },
        "disagreement_subspaces": [
            {"sub": int(s), "doc_norm": float(doc_norm[s]), "query_norm": float(query_norm[s]), "gap": float(disagreement[s])}
            for s in top_disagree
        ]
    }

    out_path = os.path.join(OUT_DIR, "exp001_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Saved to {out_path}")

    # Save per-doc variance matrix for later use
    var_matrix = np.stack([doc_variances[fid] for fid in sorted(doc_variances.keys())])
    np.save(os.path.join(OUT_DIR, "doc_subspace_variances.npy"), var_matrix)

    fid_list = sorted(doc_variances.keys())
    with open(os.path.join(OUT_DIR, "doc_file_ids.json"), "w") as f:
        json.dump(fid_list, f)

    print(f"  Saved variance matrix ({var_matrix.shape}) and file_id list")

    print(f"\n{'='*60}")
    print(f"Total time: {time.time()-t0:.1f}s")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
