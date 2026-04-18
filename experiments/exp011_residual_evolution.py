"""
MaoField Experiment 011: Residual Query Evolution
==================================================

token_new = token_original + β × evolution_residual
         = 原有认识        + 实践带来的新认识

不抛弃原始 4096d 信息，只加 SVD 演化的修正量。

步骤：
1. query tokens → SVD k维
2. 力场演化 → evolved_svd
3. 计算残差：residual_svd = evolved_svd - original_svd
4. 投影回 4096d：residual_4096 = residual_svd @ Vt
5. token_new = token_original + β × residual_4096
6. 存为新 sqlite → Rust PQ-Chamfer 评估
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
    db = sqlite3.connect(db_path)
    rows = db.execute("SELECT vector FROM chunks").fetchall()
    db.close()
    return np.stack([np.frombuffer(b, dtype=np.float32).copy() for (b,) in rows])


def load_query_clouds(db_path):
    db = sqlite3.connect(db_path)
    rows = db.execute("SELECT file_id, chunk_text, vector FROM chunks ORDER BY file_id, id").fetchall()
    db.close()
    clouds = {}
    for fid, text, blob in rows:
        vec = np.frombuffer(blob, dtype=np.float32).copy()
        clouds.setdefault(fid, []).append(vec)
    for fid in clouds:
        clouds[fid] = np.stack(clouds[fid])
    return clouds


def compute_svd(V_all, k):
    rng = np.random.RandomState(RANDOM_STATE)
    idx = rng.choice(len(V_all), size=min(100000, len(V_all)), replace=False)
    V_sample = V_all[idx]
    V_mean = V_sample.mean(axis=0)
    V_centered = (V_sample - V_mean).astype(np.float64)
    U, S, Vt = svds(V_centered, k=k)
    sort_idx = np.argsort(S)[::-1]
    return S[sort_idx].astype(np.float32), Vt[sort_idx, :].astype(np.float32), V_mean.astype(np.float32)


def evolve_query(query_svd, S, dt, n_steps, epsilon=1e-6, damping=0.95):
    tokens = query_svd.copy()
    n = tokens.shape[0]
    if n <= 1:
        return tokens

    S_norm = S / S[0]

    for step in range(n_steps):
        forces = np.zeros_like(tokens)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                diff = tokens[j] - tokens[i]
                distance = np.linalg.norm(diff) + epsilon
                sign_agree = np.sign(tokens[i]) * np.sign(tokens[j])
                force_per_mode = sign_agree * S_norm / (distance + epsilon)
                forces[i] += -force_per_mode * (diff / (distance + epsilon))

        tokens = tokens + forces * dt
        tokens *= damping

        norms = np.linalg.norm(tokens, axis=1, keepdims=True)
        norms[norms < epsilon] = 1.0
        tokens = tokens / norms
        tokens = tokens * np.linalg.norm(query_svd, axis=1, keepdims=True).mean()

    return tokens


def save_evolved_queries(original_db, output_db, evolved_clouds):
    shutil.copy2(original_db, output_db)
    db = sqlite3.connect(output_db)
    for fid, evolved_tokens in evolved_clouds.items():
        rows = db.execute("SELECT id FROM chunks WHERE file_id=? ORDER BY id", (fid,)).fetchall()
        for i, (row_id,) in enumerate(rows):
            if i < len(evolved_tokens):
                blob = evolved_tokens[i].astype(np.float32).tobytes()
                db.execute("UPDATE chunks SET vector=? WHERE id=?", (blob, row_id))
    db.commit()
    db.close()


def main():
    print("=" * 60)
    print("MaoField Exp011: Residual Query Evolution")
    print("token_new = token_original + β × evolution_residual")
    print("=" * 60)
    t0 = time.time()

    print("\nLoading data...")
    V_all = load_all_doc_tokens(os.path.join(DATA_DIR, "token_clouds.sqlite"))
    query_clouds = load_query_clouds(os.path.join(DATA_DIR, "query_token_clouds.sqlite"))
    print(f"  {V_all.shape[0]} doc tokens, {len(query_clouds)} queries")

    # SVD
    k = 16
    print(f"\nComputing SVD (k={k})...")
    S, Vt, V_mean = compute_svd(V_all, k)
    print(f"  Top S: {S[:5].tolist()}")

    # Evolve all queries once (k=16, 50 steps)
    print("\nEvolving queries in SVD space...")
    t_ev = time.time()

    original_svd = {}
    evolved_svd = {}
    residual_svd = {}

    for fid, cloud in query_clouds.items():
        centered = cloud - V_mean
        q_svd = centered @ Vt.T  # (n_tokens, k)
        original_svd[fid] = q_svd

        e_svd = evolve_query(q_svd, S, dt=0.01, n_steps=50)
        evolved_svd[fid] = e_svd
        residual_svd[fid] = e_svd - q_svd  # The "new knowledge from practice"

    print(f"  Evolution done ({time.time()-t_ev:.1f}s)")

    # Compute residual stats
    all_residual_norms = []
    all_original_norms = []
    for fid in residual_svd:
        r_norm = np.linalg.norm(residual_svd[fid], axis=1).mean()
        o_norm = np.linalg.norm(original_svd[fid], axis=1).mean()
        all_residual_norms.append(r_norm)
        all_original_norms.append(o_norm)

    print(f"  Residual norm: mean={np.mean(all_residual_norms):.4f}")
    print(f"  Original norm: mean={np.mean(all_original_norms):.4f}")
    print(f"  Ratio: {np.mean(all_residual_norms)/np.mean(all_original_norms):.4f}")

    # Generate variants for different β values
    betas = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0]

    for beta in betas:
        name = f"residual_b{str(beta).replace('.','')}"
        print(f"\n--- β={beta} ({name}) ---")

        evolved_4096 = {}
        shifts = []

        for fid, cloud in query_clouds.items():
            # residual in SVD space → project back to 4096d
            res_4096 = residual_svd[fid] @ Vt  # (n_tokens, 4096)

            # Apply residual correction
            new_tokens = cloud + beta * res_4096
            evolved_4096[fid] = new_tokens

            # Stats
            shift = np.linalg.norm(new_tokens - cloud, axis=1).mean()
            cos = np.sum(new_tokens * cloud, axis=1) / (
                np.linalg.norm(new_tokens, axis=1) * np.linalg.norm(cloud, axis=1) + 1e-10)
            shifts.append({"shift": float(shift), "cos": float(cos.mean())})

        mean_shift = np.mean([s["shift"] for s in shifts])
        mean_cos = np.mean([s["cos"] for s in shifts])
        print(f"  Mean shift: {mean_shift:.4f}")
        print(f"  Mean cosine: {mean_cos:.6f}")

        # Save
        output_db = os.path.join(EXP_DIR, f"evolved_query_{name}.sqlite")
        save_evolved_queries(
            os.path.join(DATA_DIR, "query_token_clouds.sqlite"),
            output_db, evolved_4096)
        print(f"  Saved: {output_db}")

    print(f"\n\nAll variants saved. Total: {time.time()-t0:.1f}s")
    print("Run: RAYON_NUM_THREADS=70 node exp011_bench.js")


if __name__ == "__main__":
    main()
