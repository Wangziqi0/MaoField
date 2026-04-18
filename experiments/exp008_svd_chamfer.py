"""
MaoField Experiment 008: SVD + PQ-Chamfer Fusion
=================================================

预计算 SVD 投影矩阵，然后三个方案：
A: 16维 SVD Chamfer + PQ-Chamfer 融合
B: 同侧率信号 + PQ-Chamfer
C: SVD 奇异值作为 64 子空间权重

全部在 Python 端完成（调用已有 token clouds 数据），
因为需要 SVD 投影操作，Rust 引擎不方便加。
用 centroid cosine 粗筛 top-200，精排用各方案。
"""

import sqlite3
import numpy as np
import json
import time
import os
from collections import defaultdict
from scipy.sparse.linalg import svds

DATA_DIR = "/home/amd/HEZIMENG/legal-assistant/beir_data/nfcorpus"
EXP_DIR = "/home/amd/HEZIMENG/MaoField/experiments"

N_SVD_MODES = 16  # From exp007: 50% variance at k=8, best retrieval at k=16


def load_clouds(db_path):
    db = sqlite3.connect(db_path)
    rows = db.execute("SELECT file_id, vector FROM chunks ORDER BY file_id").fetchall()
    db.close()
    clouds = {}
    for fid, blob in rows:
        vec = np.frombuffer(blob, dtype=np.float32).copy()
        clouds.setdefault(fid, []).append(vec)
    for fid in clouds:
        clouds[fid] = np.stack(clouds[fid])
    return clouds


def pq_chamfer_subspace(q_cloud, d_cloud, sub_start, sub_dim):
    """PQ-Chamfer in a single subspace slice"""
    q = q_cloud[:, sub_start:sub_start+sub_dim]
    d = d_cloud[:, sub_start:sub_start+sub_dim]
    # Normalize
    q_n = q / (np.linalg.norm(q, axis=1, keepdims=True) + 1e-10)
    d_n = d / (np.linalg.norm(d, axis=1, keepdims=True) + 1e-10)
    sim = q_n @ d_n.T
    # Chamfer: mean of max-per-row + mean of max-per-col (similarity, not distance)
    qd = sim.max(axis=1).mean()
    dq = sim.max(axis=0).mean()
    return (qd + dq) / 2


def full_pq_chamfer(q_cloud, d_cloud):
    """Full 64-subspace PQ-Chamfer (cosine-based, similarity)"""
    total = 0.0
    for s in range(64):
        total += pq_chamfer_subspace(q_cloud, d_cloud, s * 64, 64)
    return total / 64


def svd_chamfer(q_proj, d_proj):
    """Chamfer in SVD mode space (already projected)"""
    # q_proj: (nq, k), d_proj: (nd, k)
    q_n = q_proj / (np.linalg.norm(q_proj, axis=1, keepdims=True) + 1e-10)
    d_n = d_proj / (np.linalg.norm(d_proj, axis=1, keepdims=True) + 1e-10)
    sim = q_n @ d_n.T
    qd = sim.max(axis=1).mean()
    dq = sim.max(axis=0).mean()
    return (qd + dq) / 2


def same_side_rate(q_proj, d_proj):
    """For each SVD mode, fraction of query-doc token pairs on same side (both pos or both neg)"""
    n_modes = q_proj.shape[1]
    rates = []
    for m in range(n_modes):
        q_signs = np.sign(q_proj[:, m])  # (nq,)
        d_signs = np.sign(d_proj[:, m])  # (nd,)
        # For each query token, check if its nearest doc token is same side
        # Simplified: fraction of all pairs that agree
        agree = (q_signs[:, None] * d_signs[None, :] > 0).mean()
        rates.append(agree)
    return np.mean(rates)


def compute_ndcg(ranked_ids, qrel, k=10):
    dcg = 0
    for i, did in enumerate(ranked_ids[:k]):
        rel = qrel.get(did, 0)
        dcg += (2**rel - 1) / np.log2(i + 2)
    ideal = sorted(qrel.values(), reverse=True)[:k]
    idcg = sum((2**r - 1) / np.log2(i + 2) for i, r in enumerate(ideal))
    return dcg / idcg if idcg > 0 else 0


def main():
    print("=" * 60)
    print("MaoField Exp008: SVD + PQ-Chamfer Fusion")
    print("=" * 60)
    t0 = time.time()

    # ── Load data ──
    print("\nLoading data...")
    doc_clouds = load_clouds(os.path.join(DATA_DIR, "token_clouds.sqlite"))
    query_clouds = load_clouds(os.path.join(DATA_DIR, "query_token_clouds.sqlite"))
    print(f"  {len(doc_clouds)} docs, {len(query_clouds)} queries")

    # ID maps
    doc_map = {}
    with open(os.path.join(DATA_DIR, "corpus.jsonl")) as f:
        for idx, line in enumerate(f):
            doc_map[idx + 1] = json.loads(line).get("_id", str(idx))
    query_map = {}
    with open(os.path.join(DATA_DIR, "queries.jsonl")) as f:
        for idx, line in enumerate(f):
            query_map[idx] = json.loads(line).get("_id", str(idx))

    qrels = defaultdict(dict)
    with open(os.path.join(DATA_DIR, "qrels", "test.tsv")) as f:
        next(f)
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 3 and int(parts[2]) > 0:
                qrels[parts[0]][parts[1]] = int(parts[2])

    # ── SVD on sampled tokens ──
    print("\nComputing SVD...")
    rng = np.random.RandomState(42)
    all_tokens = []
    for cloud in doc_clouds.values():
        all_tokens.append(cloud)
    all_tokens = np.vstack(all_tokens)
    # Sample 100K
    idx = rng.choice(len(all_tokens), size=100000, replace=False)
    V_sample = all_tokens[idx]
    V_mean = V_sample.mean(axis=0)
    V_centered = V_sample - V_mean

    U, S, Vt = svds(V_centered.astype(np.float64), k=N_SVD_MODES)
    sort_idx = np.argsort(S)[::-1]
    S = S[sort_idx]
    Vt = Vt[sort_idx, :]
    print(f"  SVD done: top S = {S[:5].tolist()}")

    # Projection matrix
    proj = Vt.astype(np.float32)  # (16, 4096)

    # ── Precompute projections for all docs and queries ──
    print("Projecting all tokens to SVD space...")
    doc_proj = {}
    for fid, cloud in doc_clouds.items():
        centered = cloud - V_mean
        doc_proj[fid] = centered @ proj.T  # (n_tokens, 16)

    query_proj = {}
    for fid, cloud in query_clouds.items():
        centered = cloud - V_mean
        query_proj[fid] = centered @ proj.T

    # ── Centroid cosine coarse filter (top 200) ──
    print("Precomputing centroid cosine candidates...")
    doc_centroids = {}
    for fid, cloud in doc_clouds.items():
        c = cloud.mean(axis=0)
        doc_centroids[fid] = c / (np.linalg.norm(c) + 1e-10)

    doc_fids = sorted(doc_clouds.keys())
    doc_cent_matrix = np.stack([doc_centroids[fid] for fid in doc_fids])

    candidates = {}
    for qfid, cloud in query_clouds.items():
        qsid = query_map.get(qfid)
        if qsid is None or qsid not in qrels:
            continue
        q_cent = cloud.mean(axis=0)
        q_norm = q_cent / (np.linalg.norm(q_cent) + 1e-10)
        sims = doc_cent_matrix @ q_norm
        top200 = np.argsort(sims)[::-1][:200]
        candidates[qfid] = [doc_fids[i] for i in top200]

    print(f"  {len(candidates)} queries with candidates")

    # ── SVD singular values → 64 subspace weights (方案 C) ──
    # Map 16 SVD modes to 64 PQ subspaces
    # Each SVD mode spans all 4096 dims; project SVD mode vectors onto PQ subspaces
    # to get per-subspace contribution of each mode
    svd_sub_weights = np.ones(64)
    for m in range(N_SVD_MODES):
        mode_vec = Vt[m, :]  # (4096,)
        for s in range(64):
            # Energy of this mode in this subspace
            sub_vec = mode_vec[s*64:(s+1)*64]
            svd_sub_weights[s] += S[m] * np.dot(sub_vec, sub_vec)

    # ── Run all schemes ──
    schemes = [
        "baseline_pq_chamfer",
        "A_svd_chamfer_fusion",
        "B_same_side_rate",
        "C_svd_weighted_pq",
        "AB_fusion",
    ]

    results = {s: [] for s in schemes}

    print(f"\nRunning {len(candidates)} queries × 200 candidates × 5 schemes...")
    t_run = time.time()

    for qi, (qfid, cand_fids) in enumerate(candidates.items()):
        qsid = query_map[qfid]
        q_cloud = doc_clouds.get(qfid) or query_clouds[qfid]
        q_cloud_orig = query_clouds[qfid]
        q_proj_tokens = query_proj[qfid]

        scores = {s: [] for s in schemes}

        for dfid in cand_fids:
            d_cloud = doc_clouds[dfid]
            d_proj_tokens = doc_proj[dfid]
            dsid = doc_map[dfid]

            # Baseline: full PQ-Chamfer
            pq_score = full_pq_chamfer(q_cloud_orig, d_cloud)

            # A: SVD Chamfer in 16d
            svd_score = svd_chamfer(q_proj_tokens, d_proj_tokens)

            # B: Same-side rate
            ssr = same_side_rate(q_proj_tokens, d_proj_tokens)

            # C: SVD-weighted PQ-Chamfer
            weighted_score = 0.0
            for s in range(64):
                sub_score = pq_chamfer_subspace(q_cloud_orig, d_cloud, s * 64, 64)
                weighted_score += svd_sub_weights[s] * sub_score
            weighted_score /= svd_sub_weights.sum()

            scores["baseline_pq_chamfer"].append((dsid, pq_score))
            scores["A_svd_chamfer_fusion"].append((dsid, 0.7 * pq_score + 0.3 * svd_score))
            scores["B_same_side_rate"].append((dsid, 0.7 * pq_score + 0.3 * ssr))
            scores["C_svd_weighted_pq"].append((dsid, weighted_score))
            scores["AB_fusion"].append((dsid, 0.5 * pq_score + 0.25 * svd_score + 0.25 * ssr))

        # Compute NDCG for each scheme
        for scheme in schemes:
            ranked = [x[0] for x in sorted(scores[scheme], key=lambda x: x[1], reverse=True)]
            ndcg = compute_ndcg(ranked, qrels[qsid], k=10)
            results[scheme].append(ndcg)

        if (qi + 1) % 20 == 0:
            elapsed = time.time() - t_run
            baseline_ndcg = np.mean(results["baseline_pq_chamfer"])
            print(f"  {qi+1}/{len(candidates)} ({elapsed:.0f}s) baseline={baseline_ndcg:.4f}")

    # ── Summary ──
    print(f"\n{'='*60}")
    print("  MaoField Exp008 — SVD + PQ-Chamfer Fusion")
    print(f"{'-'*60}")

    baseline_mean = np.mean(results["baseline_pq_chamfer"])
    summary = {}
    for scheme in schemes:
        mean = np.mean(results[scheme])
        delta = (mean - baseline_mean) / baseline_mean * 100
        marker = "(baseline)" if scheme == "baseline_pq_chamfer" else f"{delta:+.2f}%"
        print(f"  {scheme:28s} {mean:.4f}  {marker}")
        summary[scheme] = {"ndcg_at_10": float(mean), "n_queries": len(results[scheme])}

    print(f"{'='*60}")

    # Save
    out_path = os.path.join(EXP_DIR, "exp008_results.json")
    with open(out_path, "w") as f:
        json.dump({
            "meta": {"dataset": "nfcorpus", "n_svd_modes": N_SVD_MODES, "date": "2026-04-08"},
            "svd_singular_values": S.tolist(),
            "svd_subspace_weights": svd_sub_weights.tolist(),
            "results": summary
        }, f, indent=2)
    print(f"\nSaved: {out_path}")
    print(f"Total: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
