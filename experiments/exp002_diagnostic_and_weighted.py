"""
MaoField Experiment 002: Diagnostic Analysis + Weighted Chamfer
================================================================

实验 A（诊断）：
  显式子空间 vs 隐含子空间，哪个更能区分相关/不相关文档？
  如果隐含子空间区分度更强 → "没说的比说的更有信息量"

实验 B（检索改进）：
  给子空间不同权重做 Chamfer：
  方案1: 按方差加权（显式优先）
  方案2: 按方差反向加权（隐含优先）
  方案3: 按 query-doc 分歧加权（矛盾信号）
  对照: 均匀权重（现有 PQ-Chamfer）
"""

import sqlite3
import numpy as np
import json
import time
import os
from collections import defaultdict

DATA_DIR = "/home/amd/HEZIMENG/legal-assistant/beir_data/nfcorpus"
EXP_DIR = "/home/amd/HEZIMENG/MaoField/experiments"

N_SUBSPACES = 64
SUB_DIM = 64


# ── data loading ──

def load_clouds(db_path):
    db = sqlite3.connect(db_path)
    rows = db.execute("SELECT file_id, vector FROM chunks ORDER BY file_id").fetchall()
    db.close()
    clouds = {}
    for fid, blob in rows:
        vec = np.frombuffer(blob, dtype=np.float32)
        if fid not in clouds:
            clouds[fid] = []
        clouds[fid].append(vec)
    for fid in clouds:
        clouds[fid] = np.stack(clouds[fid])
    return clouds


def load_qrels(data_dir):
    """Load BEIR qrels: {query_id: {doc_id: relevance}}"""
    qrels = defaultdict(dict)
    qrels_path = os.path.join(data_dir, "qrels", "test.tsv")
    if not os.path.exists(qrels_path):
        # Try corpus.jsonl for id mapping
        qrels_path = os.path.join(data_dir, "qrels_test.tsv")
    if not os.path.exists(qrels_path):
        # Search for it
        for root, dirs, files in os.walk(data_dir):
            for f in files:
                if 'qrel' in f.lower() and f.endswith('.tsv'):
                    qrels_path = os.path.join(root, f)
                    break
    with open(qrels_path) as f:
        header = True
        for line in f:
            if header:
                header = False
                continue
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                qid, did, rel = parts[0], parts[1], int(parts[2])
                if rel > 0:
                    qrels[qid][did] = rel
    return qrels


def load_id_maps(data_dir):
    """Build mapping: file_id (int) <-> string id"""
    # corpus
    doc_map = {}  # file_id -> string_id
    doc_rmap = {}  # string_id -> file_id
    with open(os.path.join(data_dir, "corpus.jsonl")) as f:
        for idx, line in enumerate(f):
            obj = json.loads(line)
            sid = obj.get("_id", str(idx))
            fid = idx + 1  # file_id in sqlite starts at 1
            doc_map[fid] = sid
            doc_rmap[sid] = fid

    # queries
    query_map = {}
    query_rmap = {}
    queries_path = os.path.join(data_dir, "queries.jsonl")
    if os.path.exists(queries_path):
        with open(queries_path) as f:
            for idx, line in enumerate(f):
                obj = json.loads(line)
                sid = obj.get("_id", str(idx))
                fid = idx + 1
                query_map[fid] = sid
                query_rmap[sid] = fid

    return doc_map, doc_rmap, query_map, query_rmap


# ── subspace distance functions ──

def subspace_cosine_distances(query_cloud, doc_cloud, subspace_idx):
    """
    Compute mean pairwise cosine distance between query and doc tokens
    in a specific subspace.
    Returns: mean cosine distance (lower = more similar)
    """
    s = subspace_idx
    q_sub = query_cloud[:, s*SUB_DIM:(s+1)*SUB_DIM]  # (nq, 64)
    d_sub = doc_cloud[:, s*SUB_DIM:(s+1)*SUB_DIM]     # (nd, 64)

    # Normalize
    q_norm = q_sub / (np.linalg.norm(q_sub, axis=1, keepdims=True) + 1e-10)
    d_norm = d_sub / (np.linalg.norm(d_sub, axis=1, keepdims=True) + 1e-10)

    # Cosine similarity matrix
    sim = q_norm @ d_norm.T  # (nq, nd)

    # Chamfer-style: for each query token, max similarity to any doc token
    q2d = sim.max(axis=1).mean()  # mean of max-per-query-token
    d2q = sim.max(axis=0).mean()  # mean of max-per-doc-token

    return (q2d + d2q) / 2


def weighted_chamfer(query_cloud, doc_cloud, weights):
    """
    Weighted Chamfer across 64 subspaces.
    weights: (64,) array of subspace weights (will be normalized)
    Returns: weighted similarity score
    """
    w = weights / weights.sum()
    score = 0.0
    for s in range(N_SUBSPACES):
        sub_score = subspace_cosine_distances(query_cloud, doc_cloud, s)
        score += w[s] * sub_score
    return score


def uniform_chamfer(query_cloud, doc_cloud):
    """Standard uniform-weight Chamfer across subspaces"""
    return weighted_chamfer(query_cloud, doc_cloud, np.ones(N_SUBSPACES))


# ── Experiment A: Diagnostic ──

def experiment_a(query_clouds, doc_clouds, qrels, doc_map, query_map,
                 exp001_results):
    print("\n" + "=" * 60)
    print("EXPERIMENT A: Diagnostic — Explicit vs Implicit Discriminability")
    print("=" * 60)

    # Get explicit/implicit split from exp001
    explicit_subs = exp001_results["explicit_implicit_split"]["explicit_subspaces"]
    implicit_subs = exp001_results["explicit_implicit_split"]["implicit_subspaces"]

    # For each query, compute subspace distances to relevant and random irrelevant docs
    n_queries_tested = 0
    explicit_rel_dists = []
    explicit_irr_dists = []
    implicit_rel_dists = []
    implicit_irr_dists = []

    all_doc_fids = list(doc_clouds.keys())
    rng = np.random.RandomState(42)

    t0 = time.time()
    for qfid, q_cloud in query_clouds.items():
        qsid = query_map.get(qfid)
        if qsid is None or qsid not in qrels:
            continue

        # Relevant doc file_ids
        rel_sids = list(qrels[qsid].keys())
        rel_fids = [fid for fid in all_doc_fids
                     if doc_map.get(fid) in qrels[qsid]]

        if len(rel_fids) == 0:
            continue

        # Sample irrelevant docs (same count as relevant, max 10)
        n_sample = min(len(rel_fids), 10)
        rel_fids_sample = rel_fids[:n_sample]

        irr_candidates = [fid for fid in all_doc_fids if doc_map.get(fid) not in qrels[qsid]]
        irr_fids_sample = rng.choice(irr_candidates, size=n_sample, replace=False).tolist()

        # Compute per-subspace distances
        for fid in rel_fids_sample:
            for s in explicit_subs:
                d = subspace_cosine_distances(q_cloud, doc_clouds[fid], s)
                explicit_rel_dists.append(d)
            for s in implicit_subs:
                d = subspace_cosine_distances(q_cloud, doc_clouds[fid], s)
                implicit_rel_dists.append(d)

        for fid in irr_fids_sample:
            for s in explicit_subs:
                d = subspace_cosine_distances(q_cloud, doc_clouds[fid], s)
                explicit_irr_dists.append(d)
            for s in implicit_subs:
                d = subspace_cosine_distances(q_cloud, doc_clouds[fid], s)
                implicit_irr_dists.append(d)

        n_queries_tested += 1
        if n_queries_tested % 50 == 0:
            elapsed = time.time() - t0
            print(f"  Processed {n_queries_tested} queries... ({elapsed:.1f}s)")

        if n_queries_tested >= 323:
            break

    elapsed = time.time() - t0
    print(f"  Done: {n_queries_tested} queries, {elapsed:.1f}s")

    # Analyze
    exp_rel = np.mean(explicit_rel_dists)
    exp_irr = np.mean(explicit_irr_dists)
    imp_rel = np.mean(implicit_rel_dists)
    imp_irr = np.mean(implicit_irr_dists)

    exp_gap = exp_rel - exp_irr
    imp_gap = imp_rel - imp_irr

    print(f"\n  === Results ===")
    print(f"  Explicit subspaces (top-32 variance):")
    print(f"    Relevant docs mean sim:   {exp_rel:.6f}")
    print(f"    Irrelevant docs mean sim: {exp_irr:.6f}")
    print(f"    Gap (rel - irr):          {exp_gap:.6f}")
    print(f"    Discriminability:         {exp_gap / (exp_irr + 1e-10):.4f} ({exp_gap/exp_irr*100:.2f}%)")

    print(f"\n  Implicit subspaces (bottom-32 variance):")
    print(f"    Relevant docs mean sim:   {imp_rel:.6f}")
    print(f"    Irrelevant docs mean sim: {imp_irr:.6f}")
    print(f"    Gap (rel - irr):          {imp_gap:.6f}")
    print(f"    Discriminability:         {imp_gap / (imp_irr + 1e-10):.4f} ({imp_gap/imp_irr*100:.2f}%)")

    print(f"\n  >>> Implicit / Explicit discriminability ratio: {imp_gap/exp_gap:.3f}")
    if imp_gap > exp_gap:
        print(f"  >>> IMPLICIT SUBSPACES ARE MORE DISCRIMINATIVE <<<")
    else:
        print(f"  >>> Explicit subspaces are more discriminative")

    results_a = {
        "n_queries": n_queries_tested,
        "explicit": {
            "relevant_mean_sim": float(exp_rel),
            "irrelevant_mean_sim": float(exp_irr),
            "gap": float(exp_gap),
            "discriminability_pct": float(exp_gap / exp_irr * 100)
        },
        "implicit": {
            "relevant_mean_sim": float(imp_rel),
            "irrelevant_mean_sim": float(imp_irr),
            "gap": float(imp_gap),
            "discriminability_pct": float(imp_gap / imp_irr * 100)
        },
        "implicit_over_explicit_ratio": float(imp_gap / exp_gap) if exp_gap != 0 else None
    }

    return results_a


# ── Experiment B: Weighted Chamfer Retrieval ──

def compute_ndcg(ranked_doc_ids, qrels_dict, k=10):
    """Compute NDCG@k"""
    dcg = 0.0
    for i, did in enumerate(ranked_doc_ids[:k]):
        rel = qrels_dict.get(did, 0)
        dcg += rel / np.log2(i + 2)

    # Ideal
    ideal_rels = sorted(qrels_dict.values(), reverse=True)[:k]
    idcg = sum(r / np.log2(i + 2) for i, r in enumerate(ideal_rels))

    return dcg / idcg if idcg > 0 else 0.0


def experiment_b(query_clouds, doc_clouds, qrels, doc_map, query_map,
                 exp001_results):
    print("\n" + "=" * 60)
    print("EXPERIMENT B: Weighted Chamfer Retrieval")
    print("=" * 60)

    # Load subspace info
    doc_var = np.array(exp001_results["global_subspace_activity"]["doc_mean_variance"])
    query_var = np.array(exp001_results["global_subspace_activity"]["query_mean_variance"])

    # Weight schemes
    # 1. Variance-weighted (explicit priority)
    w_variance = doc_var.copy()

    # 2. Inverse-variance (implicit priority)
    w_inverse = 1.0 / (doc_var + 1e-6)

    # 3. Disagreement-weighted (contradiction signal)
    doc_norm = (doc_var - doc_var.min()) / (doc_var.max() - doc_var.min() + 1e-10)
    query_norm = (query_var - query_var.min()) / (query_var.max() - query_var.min() + 1e-10)
    w_disagree = np.abs(doc_norm - query_norm) + 0.1  # +0.1 floor

    # 4. Uniform (baseline)
    w_uniform = np.ones(N_SUBSPACES)

    schemes = {
        "uniform": w_uniform,
        "variance": w_variance,
        "inverse_variance": w_inverse,
        "disagreement": w_disagree
    }

    # Pre-compute top-200 candidates per query using centroid cosine (fast)
    print("\n  Pre-computing centroid cosine candidates (top-200)...")
    t0 = time.time()

    doc_centroids = {}
    for fid, cloud in doc_clouds.items():
        doc_centroids[fid] = cloud.mean(axis=0)

    query_centroids = {}
    for fid, cloud in query_clouds.items():
        query_centroids[fid] = cloud.mean(axis=0)

    # Build doc centroid matrix
    doc_fids = sorted(doc_clouds.keys())
    doc_cent_matrix = np.stack([doc_centroids[fid] for fid in doc_fids])  # (2473, 4096)
    doc_cent_norms = doc_cent_matrix / (np.linalg.norm(doc_cent_matrix, axis=1, keepdims=True) + 1e-10)

    candidates = {}  # qfid -> list of doc fids (top 200)
    for qfid in query_clouds:
        qsid = query_map.get(qfid)
        if qsid is None or qsid not in qrels:
            continue
        q_cent = query_centroids[qfid]
        q_norm = q_cent / (np.linalg.norm(q_cent) + 1e-10)
        sims = doc_cent_norms @ q_norm
        top200_idx = np.argsort(sims)[::-1][:200]
        candidates[qfid] = [doc_fids[i] for i in top200_idx]

    print(f"  {len(candidates)} queries with candidates, {time.time()-t0:.1f}s")

    # Run weighted Chamfer for each scheme
    results_b = {}

    for scheme_name, weights in schemes.items():
        t1 = time.time()
        print(f"\n  --- Scheme: {scheme_name} ---")

        ndcg_scores = []
        n_done = 0

        for qfid, cand_fids in candidates.items():
            qsid = query_map.get(qfid)
            q_cloud = query_clouds[qfid]

            # Score candidates
            scores = []
            for dfid in cand_fids:
                s = weighted_chamfer(q_cloud, doc_clouds[dfid], weights)
                scores.append((doc_map[dfid], s))

            # Rank by score descending
            scores.sort(key=lambda x: x[1], reverse=True)
            ranked_ids = [x[0] for x in scores]

            # NDCG@10
            ndcg = compute_ndcg(ranked_ids, qrels[qsid], k=10)
            ndcg_scores.append(ndcg)

            n_done += 1
            if n_done % 50 == 0:
                print(f"    {n_done}/{len(candidates)} queries... mean NDCG@10={np.mean(ndcg_scores):.4f}")

        mean_ndcg = np.mean(ndcg_scores)
        elapsed = time.time() - t1
        print(f"    Final: NDCG@10 = {mean_ndcg:.4f} ({n_done} queries, {elapsed:.1f}s)")

        results_b[scheme_name] = {
            "ndcg_at_10": float(mean_ndcg),
            "n_queries": n_done,
            "time_s": float(elapsed)
        }

    # Summary
    print(f"\n  === Summary ===")
    baseline_ndcg = results_b["uniform"]["ndcg_at_10"]
    for name, res in sorted(results_b.items(), key=lambda x: x[1]["ndcg_at_10"], reverse=True):
        delta = (res["ndcg_at_10"] - baseline_ndcg) / baseline_ndcg * 100
        marker = " (baseline)" if name == "uniform" else f" ({delta:+.2f}%)"
        print(f"  {name:20s}: NDCG@10 = {res['ndcg_at_10']:.4f}{marker}")

    return results_b


# ── Main ──

def main():
    print("=" * 60)
    print("MaoField Exp002: Diagnostic + Weighted Chamfer")
    print("=" * 60)

    # Load exp001 results
    with open(os.path.join(EXP_DIR, "exp001_results.json")) as f:
        exp001 = json.load(f)

    # Load data
    t0 = time.time()
    print("\nLoading data...")
    doc_clouds = load_clouds(os.path.join(DATA_DIR, "token_clouds.sqlite"))
    query_clouds = load_clouds(os.path.join(DATA_DIR, "query_token_clouds.sqlite"))
    print(f"  Loaded {len(doc_clouds)} docs, {len(query_clouds)} queries ({time.time()-t0:.1f}s)")

    # Load qrels and id maps
    doc_map, doc_rmap, query_map, query_rmap = load_id_maps(DATA_DIR)
    qrels = load_qrels(DATA_DIR)
    print(f"  Loaded qrels: {len(qrels)} queries with relevance judgments")

    # Experiment A
    results_a = experiment_a(query_clouds, doc_clouds, qrels, doc_map, query_map, exp001)

    # Experiment B
    results_b = experiment_b(query_clouds, doc_clouds, qrels, doc_map, query_map, exp001)

    # Save all results
    all_results = {
        "meta": {
            "dataset": "NFCorpus",
            "date": "2026-04-08",
            "total_time_s": float(time.time() - t0)
        },
        "experiment_a_diagnostic": results_a,
        "experiment_b_weighted_chamfer": results_b
    }

    out_path = os.path.join(EXP_DIR, "exp002_results.json")
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved to {out_path}")
    print(f"Total time: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
