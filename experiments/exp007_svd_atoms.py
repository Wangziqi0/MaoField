"""
MaoField Experiment 007: SVD Semantic Mode Discovery
=====================================================

SVD 替代 NMF：天然允许负值，找正交/对立方向。
每个奇异向量有正方向和负方向 = 对立统一。
奇异值从大到小 = 主要矛盾到次要矛盾。

实验 1: 奇异值分布——有没有拐点（自然的模式数）
实验 2: 每个模式的正/负方向对应什么 token（语义解释）
实验 5: 模式间的对立关系
实验 3: 模式空间中做检索
实验 4: 模式权重的信息熵
"""

import sqlite3
import numpy as np
import json
import time
import os
from collections import defaultdict

DATA_DIR = "/home/amd/HEZIMENG/legal-assistant/beir_data/nfcorpus"
EXP_DIR = "/home/amd/HEZIMENG/MaoField/experiments"

N_SAMPLE = 100000
RANDOM_STATE = 42


def load_token_sample_with_text(db_path, corpus_path, n_sample, rng):
    """Load token sample and map back to original text"""
    db = sqlite3.connect(db_path)
    total = db.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    print(f"  Total tokens in DB: {total}")

    indices = set(rng.choice(total, size=min(n_sample, total), replace=False).tolist())

    # Load corpus text for document-level context
    doc_texts = {}
    with open(corpus_path) as f:
        for idx, line in enumerate(f):
            obj = json.loads(line)
            doc_texts[idx + 1] = obj.get("title", "") + " " + obj.get("text", "")

    rows = db.execute("SELECT id, file_id, chunk_text, vector FROM chunks").fetchall()
    db.close()

    vectors = []
    token_infos = []  # (file_id, token_position, doc_text_snippet)

    for row_id, fid, text, blob in rows:
        if row_id in indices:
            vec = np.frombuffer(blob, dtype=np.float32).copy()
            vectors.append(vec)

            # Extract token position from chunk_text
            pos = text if text else f"token_{row_id}"
            # Get a snippet from the document
            doc_text = doc_texts.get(fid, "")
            token_infos.append({
                "id": row_id,
                "file_id": fid,
                "position": pos,
                "doc_snippet": doc_text[:200]
            })

    V = np.stack(vectors)
    print(f"  Sampled {V.shape[0]} tokens, dim={V.shape[1]}")
    return V, token_infos


def load_qrels():
    qrels = defaultdict(dict)
    with open(os.path.join(DATA_DIR, "qrels", "test.tsv")) as f:
        next(f)  # header
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                qid, did, rel = parts[0], parts[1], int(parts[2])
                if rel > 0:
                    qrels[qid][did] = rel
    return qrels


# ── Experiment 1: Singular value distribution ──

def experiment_1(V):
    print("\n" + "=" * 60)
    print("EXPERIMENT 1: Singular Value Distribution")
    print("=" * 60)

    # Center the data (important for SVD to find variance directions)
    V_centered = V - V.mean(axis=0)

    t0 = time.time()
    print("  Running truncated SVD (k=256)...")
    # Full SVD on 100K×4096 is expensive, use truncated
    from scipy.sparse.linalg import svds
    # svds returns smallest, so we ask for 256 and reverse
    U, S, Vt = svds(V_centered.astype(np.float64), k=256)

    # Sort by decreasing singular value
    idx = np.argsort(S)[::-1]
    S = S[idx]
    U = U[:, idx]
    Vt = Vt[idx, :]

    elapsed = time.time() - t0
    print(f"  SVD done ({elapsed:.1f}s)")

    # Singular value analysis
    total_var = np.sum(S ** 2)
    cumulative = np.cumsum(S ** 2) / total_var

    print(f"\n  === Singular Value Analysis ===")
    print(f"  Top 10 singular values: {S[:10].tolist()}")
    print(f"  S[0]/S[1] ratio: {S[0]/S[1]:.2f}")
    print(f"  S[0]/S[255] ratio: {S[0]/S[255]:.2f}")

    # Variance explained
    milestones = [0.5, 0.8, 0.9, 0.95, 0.99]
    for m in milestones:
        k_needed = np.searchsorted(cumulative, m) + 1
        print(f"  {m*100:.0f}% variance: k={k_needed}")

    # Elbow detection via ratio of consecutive singular values
    ratios = S[:-1] / S[1:]
    elbow_candidates = np.argsort(ratios)[::-1][:5]
    print(f"\n  Largest singular value drops at k: {(elbow_candidates + 1).tolist()}")
    print(f"  Drop ratios: {[f'{ratios[i]:.3f}' for i in elbow_candidates]}")

    # Second derivative for elbow
    log_s = np.log(S + 1e-10)
    d2 = np.diff(log_s, 2)
    elbow_d2 = np.argmax(d2) + 1
    print(f"  Elbow by 2nd derivative of log(S): k={elbow_d2}")

    results = {
        "singular_values": S.tolist(),
        "cumulative_variance": cumulative.tolist(),
        "variance_milestones": {f"{m*100:.0f}pct": int(np.searchsorted(cumulative, m) + 1) for m in milestones},
        "elbow_by_ratio": (elbow_candidates + 1).tolist(),
        "elbow_by_d2": int(elbow_d2),
        "s0_s1_ratio": float(S[0] / S[1]),
        "time_s": elapsed
    }

    return U, S, Vt, results


# ── Experiment 2: Mode semantic interpretation ──

def experiment_2(U, S, Vt, token_infos, n_modes=16):
    print(f"\n{'=' * 60}")
    print(f"EXPERIMENT 2: Mode Semantics (top {n_modes} modes)")
    print("=" * 60)

    mode_semantics = []

    for m in range(n_modes):
        # U[:, m] are the token loadings on mode m
        loadings = U[:, m]

        # Top tokens in POSITIVE direction
        pos_idx = np.argsort(loadings)[::-1][:15]
        # Top tokens in NEGATIVE direction
        neg_idx = np.argsort(loadings)[:15]

        pos_tokens = [(token_infos[i]["position"], token_infos[i]["doc_snippet"][:80],
                       float(loadings[i])) for i in pos_idx]
        neg_tokens = [(token_infos[i]["position"], token_infos[i]["doc_snippet"][:80],
                       float(loadings[i])) for i in neg_idx]

        print(f"\n  Mode {m} (σ={S[m]:.2f}):")
        print(f"    POSITIVE direction (正极):")
        for pos, doc, w in pos_tokens[:5]:
            print(f"      {w:+.4f}  [{pos}] {doc}")
        print(f"    NEGATIVE direction (负极):")
        for pos, doc, w in neg_tokens[:5]:
            print(f"      {w:+.4f}  [{pos}] {doc}")

        # Check: are positive and negative from DIFFERENT documents?
        pos_docs = set(token_infos[i]["file_id"] for i in pos_idx[:10])
        neg_docs = set(token_infos[i]["file_id"] for i in neg_idx[:10])
        overlap = pos_docs & neg_docs
        print(f"    Doc overlap (pos∩neg): {len(overlap)}/{min(len(pos_docs),len(neg_docs))}")

        mode_semantics.append({
            "mode": m,
            "singular_value": float(S[m]),
            "pos_tokens": [{"pos": p, "doc": d, "loading": w} for p, d, w in pos_tokens],
            "neg_tokens": [{"pos": p, "doc": d, "loading": w} for p, d, w in neg_tokens],
            "doc_overlap": len(overlap)
        })

    return mode_semantics


# ── Experiment 5: Opposition structure in SVD modes ──

def experiment_5(U, S, Vt, n_modes=32):
    print(f"\n{'=' * 60}")
    print(f"EXPERIMENT 5: Opposition Structure in SVD Modes")
    print("=" * 60)

    # Vt rows are mode directions in 4096d space
    # SVD modes are orthogonal by construction, so cosine between modes ≈ 0
    # The real question: within each mode, how strong is the pos/neg split?

    opposition_metrics = []

    for m in range(n_modes):
        loadings = U[:, m]

        # Split tokens into positive and negative groups
        pos_mask = loadings > 0
        neg_mask = loadings < 0
        n_pos = pos_mask.sum()
        n_neg = neg_mask.sum()

        # How balanced is the split?
        balance = min(n_pos, n_neg) / max(n_pos, n_neg) if max(n_pos, n_neg) > 0 else 0

        # How strong is the opposition? (gap between pos mean and neg mean)
        pos_mean = loadings[pos_mask].mean() if n_pos > 0 else 0
        neg_mean = loadings[neg_mask].mean() if n_neg > 0 else 0
        opposition_strength = pos_mean - neg_mean

        # Bimodality: is the loading distribution bimodal?
        # Simple test: distance between pos centroid and neg centroid in original space
        # vs average within-group distance

        opposition_metrics.append({
            "mode": m,
            "singular_value": float(S[m]),
            "n_positive": int(n_pos),
            "n_negative": int(n_neg),
            "balance": float(balance),
            "pos_mean_loading": float(pos_mean),
            "neg_mean_loading": float(neg_mean),
            "opposition_strength": float(opposition_strength)
        })

        if m < 8:
            print(f"\n  Mode {m} (σ={S[m]:.2f}):")
            print(f"    Pos: {n_pos} tokens, mean={pos_mean:.4f}")
            print(f"    Neg: {n_neg} tokens, mean={neg_mean:.4f}")
            print(f"    Balance: {balance:.4f}")
            print(f"    Opposition strength: {opposition_strength:.4f}")

    # Cross-mode analysis: do positive tokens in mode A tend to be negative in mode B?
    print(f"\n  === Cross-mode opposition ===")
    cross_corr = np.corrcoef(U[:, :n_modes].T)  # (n_modes, n_modes)
    # By SVD construction, cross_corr should be identity (orthogonal)
    off_diag = cross_corr[np.triu_indices(n_modes, 1)]
    print(f"  Off-diagonal correlations: mean={off_diag.mean():.6f} max={off_diag.max():.6f}")
    print(f"  (Should be ~0 by SVD orthogonality)")

    return opposition_metrics


# ── Experiment 3: Retrieval in mode space ──

def experiment_3(V_all_docs, V_all_queries, S, Vt, doc_ids, query_ids, qrels, n_modes_list):
    print(f"\n{'=' * 60}")
    print(f"EXPERIMENT 3: Retrieval in SVD Mode Space")
    print("=" * 60)

    # Project all docs and queries into mode space
    # Compute global mean from all doc token centroids
    all_centroids = np.stack([cloud.mean(axis=0) for cloud in V_all_docs.values()])
    V_mean = all_centroids.mean(axis=0)

    results = {}

    for n_modes in n_modes_list:
        # Projection matrix: top n_modes right singular vectors
        proj = Vt[:n_modes, :]  # (n_modes, 4096)

        # For each query and doc, project centroids
        # (simplified: use document centroid, not full Chamfer)
        doc_proj = {}
        for fid, cloud in V_all_docs.items():
            centroid = cloud.mean(axis=0) - V_mean
            doc_proj[fid] = proj @ centroid  # (n_modes,)

        query_proj = {}
        for fid, cloud in V_all_queries.items():
            centroid = cloud.mean(axis=0) - V_mean
            query_proj[fid] = proj @ centroid  # (n_modes,)

        # Cosine similarity in mode space
        ndcg_scores = []
        for qfid, q_vec in query_proj.items():
            qsid = query_ids.get(qfid)
            if qsid is None or qsid not in qrels:
                continue

            q_norm = q_vec / (np.linalg.norm(q_vec) + 1e-10)
            scores = []
            for dfid, d_vec in doc_proj.items():
                d_norm = d_vec / (np.linalg.norm(d_vec) + 1e-10)
                sim = np.dot(q_norm, d_norm)
                scores.append((doc_ids[dfid], sim))

            scores.sort(key=lambda x: x[1], reverse=True)
            ranked = [s[0] for s in scores[:10]]

            # NDCG@10
            dcg = 0
            for i, did in enumerate(ranked):
                rel = qrels[qsid].get(did, 0)
                dcg += (2**rel - 1) / np.log2(i + 2)
            ideal = sorted(qrels[qsid].values(), reverse=True)[:10]
            idcg = sum((2**r - 1) / np.log2(i + 2) for i, r in enumerate(ideal))
            ndcg = dcg / idcg if idcg > 0 else 0
            ndcg_scores.append(ndcg)

        mean_ndcg = np.mean(ndcg_scores) if ndcg_scores else 0
        print(f"  k={n_modes:4d} modes: NDCG@10 = {mean_ndcg:.4f} ({len(ndcg_scores)} queries)")
        results[n_modes] = {"ndcg_at_10": float(mean_ndcg), "n_queries": len(ndcg_scores)}

    return results


# ── Experiment 4: Information entropy of mode weights ──

def experiment_4(U, S, n_modes_list):
    print(f"\n{'=' * 60}")
    print(f"EXPERIMENT 4: Information Entropy of Mode Weights")
    print("=" * 60)

    results = {}

    for n_modes in n_modes_list:
        # For each token, its weight distribution across modes
        W = np.abs(U[:, :n_modes]) * S[:n_modes]  # weighted loadings

        # Normalize per token to get probability distribution
        W_sum = W.sum(axis=1, keepdims=True)
        W_sum[W_sum == 0] = 1
        P = W / W_sum

        # Entropy per token
        log_P = np.log2(P + 1e-15)
        entropies = -np.sum(P * log_P, axis=1)

        mean_ent = entropies.mean()
        max_ent = np.log2(n_modes)  # max possible entropy

        print(f"  k={n_modes:4d}: mean entropy={mean_ent:.4f} bits, max possible={max_ent:.4f}, ratio={mean_ent/max_ent:.4f}")

        results[n_modes] = {
            "mean_entropy": float(mean_ent),
            "std_entropy": float(entropies.std()),
            "max_possible": float(max_ent),
            "normalized_entropy": float(mean_ent / max_ent)
        }

    return results


def main():
    print("=" * 60)
    print("MaoField Exp007: SVD Semantic Mode Discovery")
    print("=" * 60)

    rng = np.random.RandomState(RANDOM_STATE)
    t0 = time.time()

    # Load data
    print("\nLoading token sample with text...")
    V_raw, token_infos = load_token_sample_with_text(
        os.path.join(DATA_DIR, "token_clouds.sqlite"),
        os.path.join(DATA_DIR, "corpus.jsonl"),
        N_SAMPLE, rng
    )

    # ── Experiment 1: SVD ──
    U, S, Vt, exp1 = experiment_1(V_raw)

    # ── Experiment 2: Mode semantics ──
    exp2 = experiment_2(U, S, Vt, token_infos, n_modes=16)

    # ── Experiment 5: Opposition structure ──
    exp5 = experiment_5(U, S, Vt, n_modes=32)

    # ── Experiment 4: Entropy ──
    exp4 = experiment_4(U, S, [2, 4, 8, 16, 32, 64, 128, 256])

    # ── Experiment 3: Retrieval in mode space ──
    # Need full doc/query clouds for this
    print("\n  Loading full clouds for retrieval experiment...")
    t_load = time.time()

    db = sqlite3.connect(os.path.join(DATA_DIR, "token_clouds.sqlite"))
    rows = db.execute("SELECT file_id, vector FROM chunks ORDER BY file_id").fetchall()
    db.close()
    doc_clouds = {}
    for fid, blob in rows:
        vec = np.frombuffer(blob, dtype=np.float32)
        if fid not in doc_clouds:
            doc_clouds[fid] = []
        doc_clouds[fid].append(vec)
    for fid in doc_clouds:
        doc_clouds[fid] = np.stack(doc_clouds[fid])

    db = sqlite3.connect(os.path.join(DATA_DIR, "query_token_clouds.sqlite"))
    rows = db.execute("SELECT file_id, vector FROM chunks ORDER BY file_id").fetchall()
    db.close()
    query_clouds = {}
    for fid, blob in rows:
        vec = np.frombuffer(blob, dtype=np.float32)
        if fid not in query_clouds:
            query_clouds[fid] = []
        query_clouds[fid].append(vec)
    for fid in query_clouds:
        query_clouds[fid] = np.stack(query_clouds[fid])

    # Load ID maps
    doc_map = {}
    with open(os.path.join(DATA_DIR, "corpus.jsonl")) as f:
        for idx, line in enumerate(f):
            obj = json.loads(line)
            doc_map[idx + 1] = obj.get("_id", str(idx))

    query_map = {}
    with open(os.path.join(DATA_DIR, "queries.jsonl")) as f:
        for idx, line in enumerate(f):
            obj = json.loads(line)
            query_map[idx] = obj.get("_id", str(idx))

    qrels = load_qrels()
    print(f"  Loaded ({time.time()-t_load:.1f}s)")

    exp3 = experiment_3(
        doc_clouds, query_clouds, S, Vt, doc_map, query_map, qrels,
        n_modes_list=[2, 4, 8, 16, 32, 64, 128, 256]
    )

    # Save
    all_results = {
        "meta": {
            "dataset": "NFCorpus",
            "n_sample": V_raw.shape[0],
            "dim": V_raw.shape[1],
            "date": "2026-04-08"
        },
        "exp1_singular_values": exp1,
        "exp2_mode_semantics": exp2,
        "exp3_retrieval": exp3,
        "exp4_entropy": exp4,
        "exp5_opposition": exp5
    }

    out_path = os.path.join(EXP_DIR, "exp007_results.json")
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\n\nSaved to {out_path}")
    print(f"Total time: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
