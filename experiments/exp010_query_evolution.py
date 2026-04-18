"""
MaoField Experiment 010: Query Evolution in SVD Force Field
============================================================

实验 A: query token 在 SVD 力场中自演化，投影回 4096d，
用现有 Rust PQ-Chamfer 评估。

核心思想：token 不是静态向量，是运动中的粒子。
力场由 token 间的矛盾关系决定（同号排斥、异号吸引），
不需要训练。

步骤：
1. query tokens → SVD k维空间
2. 力场演化 N 步
3. 投影回 4096d
4. 存为新的 query_token_clouds.sqlite
5. 用 Rust 引擎做 PQ-Chamfer
"""

import sqlite3
import numpy as np
import json
import time
import os
import shutil
from scipy.sparse.linalg import svds

DATA_DIR = "/home/amd/HEZIMENG/legal-assistant/beir_data/nfcorpus"
EXP_DIR = "/home/amd/HEZIMENG/MaoField/experiments"
RANDOM_STATE = 42


def load_all_doc_tokens(db_path):
    """Load all doc tokens for SVD training"""
    db = sqlite3.connect(db_path)
    rows = db.execute("SELECT vector FROM chunks").fetchall()
    db.close()
    vectors = [np.frombuffer(blob, dtype=np.float32).copy() for (blob,) in rows]
    return np.stack(vectors)


def load_query_clouds(db_path):
    """Load query token clouds: {file_id: np.array(n_tokens, 4096)}"""
    db = sqlite3.connect(db_path)
    rows = db.execute("SELECT file_id, chunk_text, vector FROM chunks ORDER BY file_id, id").fetchall()
    db.close()
    clouds = {}
    texts = {}
    for fid, text, blob in rows:
        vec = np.frombuffer(blob, dtype=np.float32).copy()
        clouds.setdefault(fid, []).append(vec)
        texts.setdefault(fid, []).append(text)
    for fid in clouds:
        clouds[fid] = np.stack(clouds[fid])
    return clouds, texts


def compute_svd(V_all, k):
    """Compute SVD on sampled tokens"""
    rng = np.random.RandomState(RANDOM_STATE)
    n = len(V_all)
    idx = rng.choice(n, size=min(100000, n), replace=False)
    V_sample = V_all[idx]
    V_mean = V_sample.mean(axis=0)
    V_centered = (V_sample - V_mean).astype(np.float64)

    U, S, Vt = svds(V_centered, k=k)
    sort_idx = np.argsort(S)[::-1]
    S = S[sort_idx].astype(np.float32)
    Vt = Vt[sort_idx, :].astype(np.float32)

    return S, Vt, V_mean.astype(np.float32)


def evolve_query(query_svd, S, dt, n_steps, epsilon=1e-6, damping=0.95):
    """
    Evolve query tokens in SVD force field.

    Force between token i and j in mode m:
      sign_agreement = sign(token_i[m]) * sign(token_j[m])
      F[m] = sign_agreement * S[m] / (distance + eps)
      同号 → 排斥（正力），异号 → 吸引（负力）

    After each step, normalize to unit sphere to keep cosine meaningful.
    """
    tokens = query_svd.copy()  # (n_tokens, k)
    n = tokens.shape[0]
    k = tokens.shape[1]

    if n <= 1:
        return tokens  # Can't evolve single token

    # Normalize S for force scaling
    S_norm = S / S[0]  # Main contradiction = weight 1.0

    for step in range(n_steps):
        forces = np.zeros_like(tokens)

        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                diff = tokens[j] - tokens[i]
                distance = np.linalg.norm(diff) + epsilon

                # Per-mode force
                sign_agree = np.sign(tokens[i]) * np.sign(tokens[j])  # (k,)
                # 同号=+1 → 排斥, 异号=-1 → 吸引
                force_per_mode = sign_agree * S_norm / (distance + epsilon)

                # Force direction: along the difference vector per mode
                # Repulsion: push away (opposite to diff), Attraction: pull closer (along diff)
                # sign_agree > 0 → repel → force pushes i AWAY from j → subtract diff
                # sign_agree < 0 → attract → force pulls i TOWARD j → add diff
                # So: force on i from j = -sign_agree * S_norm * (diff/distance) / distance
                forces[i] += -force_per_mode * (diff / (distance + epsilon))

        # Update with damping
        tokens = tokens + forces * dt
        tokens *= damping  # Prevent divergence

        # Normalize each token to unit sphere in SVD space
        norms = np.linalg.norm(tokens, axis=1, keepdims=True)
        norms[norms < epsilon] = 1.0
        tokens = tokens / norms

        # Re-scale to original magnitude (preserve energy)
        tokens = tokens * np.linalg.norm(query_svd, axis=1, keepdims=True).mean()

    return tokens


def save_evolved_query_clouds(original_db, output_db, evolved_clouds):
    """Save evolved query token clouds to a new sqlite database"""
    shutil.copy2(original_db, output_db)
    db = sqlite3.connect(output_db)

    for fid, evolved_tokens in evolved_clouds.items():
        # Get original row ids for this file_id
        rows = db.execute(
            "SELECT id FROM chunks WHERE file_id=? ORDER BY id", (fid,)
        ).fetchall()

        for i, (row_id,) in enumerate(rows):
            if i < len(evolved_tokens):
                blob = evolved_tokens[i].astype(np.float32).tobytes()
                db.execute("UPDATE chunks SET vector=? WHERE id=?", (blob, row_id))

    db.commit()
    db.close()


def main():
    print("=" * 60)
    print("MaoField Exp010: Query Evolution in SVD Force Field")
    print("=" * 60)
    t0 = time.time()

    # Load data
    print("\nLoading doc tokens for SVD...")
    V_all = load_all_doc_tokens(os.path.join(DATA_DIR, "token_clouds.sqlite"))
    print(f"  {V_all.shape[0]} tokens")

    print("Loading query clouds...")
    query_clouds, query_texts = load_query_clouds(
        os.path.join(DATA_DIR, "query_token_clouds.sqlite"))
    print(f"  {len(query_clouds)} queries")

    # Experiment variants
    variants = [
        {"name": "evolve-16-50", "k": 16, "steps": 50, "dt": 0.01},
        {"name": "evolve-8-50", "k": 8, "steps": 50, "dt": 0.01},
        {"name": "evolve-32-50", "k": 32, "steps": 50, "dt": 0.01},
        {"name": "evolve-16-100", "k": 16, "steps": 100, "dt": 0.01},
        {"name": "evolve-16-10", "k": 16, "steps": 10, "dt": 0.01},
        {"name": "evolve-16-50-dt05", "k": 16, "steps": 50, "dt": 0.05},
    ]

    for var in variants:
        print(f"\n{'='*60}")
        print(f"Variant: {var['name']} (k={var['k']}, steps={var['steps']}, dt={var['dt']})")
        print(f"{'='*60}")

        # Compute SVD
        print("  Computing SVD...")
        S, Vt, V_mean = compute_svd(V_all, var['k'])
        print(f"  Top S: {S[:5].tolist()}")

        # Project query tokens to SVD space
        print("  Projecting and evolving queries...")
        evolved_clouds_4096 = {}
        evolution_stats = []

        for fid, cloud in query_clouds.items():
            # Project to SVD space
            centered = cloud - V_mean  # (n_tokens, 4096)
            query_svd = centered @ Vt.T  # (n_tokens, k)

            # Evolve
            evolved_svd = evolve_query(
                query_svd, S, dt=var['dt'], n_steps=var['steps']
            )

            # Project back to 4096d
            evolved_4096 = evolved_svd @ Vt + V_mean  # (n_tokens, 4096)
            evolved_clouds_4096[fid] = evolved_4096

            # Stats: how much did tokens move?
            original_centroid = cloud.mean(axis=0)
            evolved_centroid = evolved_4096.mean(axis=0)
            centroid_shift = np.linalg.norm(evolved_centroid - original_centroid)
            cos_shift = np.dot(original_centroid, evolved_centroid) / (
                np.linalg.norm(original_centroid) * np.linalg.norm(evolved_centroid) + 1e-10)

            evolution_stats.append({
                "file_id": fid,
                "n_tokens": cloud.shape[0],
                "centroid_shift": float(centroid_shift),
                "centroid_cosine": float(cos_shift)
            })

        # Print evolution stats
        shifts = [s["centroid_shift"] for s in evolution_stats]
        cosines = [s["centroid_cosine"] for s in evolution_stats]
        print(f"  Centroid shift: mean={np.mean(shifts):.4f}, max={np.max(shifts):.4f}")
        print(f"  Centroid cosine: mean={np.mean(cosines):.6f}, min={np.min(cosines):.6f}")

        # Save evolved query clouds
        output_db = os.path.join(EXP_DIR, f"evolved_query_{var['name']}.sqlite")
        print(f"  Saving evolved queries to {output_db}...")
        save_evolved_query_clouds(
            os.path.join(DATA_DIR, "query_token_clouds.sqlite"),
            output_db,
            evolved_clouds_4096
        )
        print(f"  Saved.")

        # Save stats
        stats_path = os.path.join(EXP_DIR, f"exp010_stats_{var['name']}.json")
        with open(stats_path, "w") as f:
            json.dump({
                "variant": var,
                "svd_singular_values": S.tolist(),
                "evolution_stats_summary": {
                    "mean_centroid_shift": float(np.mean(shifts)),
                    "max_centroid_shift": float(np.max(shifts)),
                    "mean_centroid_cosine": float(np.mean(cosines)),
                    "min_centroid_cosine": float(np.min(cosines))
                }
            }, f, indent=2)

    print(f"\n\nAll variants saved. Total time: {time.time()-t0:.1f}s")
    print("\nNext: run JS benchmark with each evolved query sqlite to get real NDCG.")


if __name__ == "__main__":
    main()
