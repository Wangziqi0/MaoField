"""
MaoField Exp007b: SVD Mode Space Retrieval (only exp3)
Uses the SVD from exp007 to do centroid-based retrieval in mode space.
"""

import sqlite3
import numpy as np
import json
import time
import os
from collections import defaultdict

DATA_DIR = "/home/amd/HEZIMENG/legal-assistant/beir_data/nfcorpus"
EXP_DIR = "/home/amd/HEZIMENG/MaoField/experiments"


def main():
    print("=== Exp007b: SVD Retrieval ===\n")
    t0 = time.time()

    # Load token sample for SVD
    print("Loading token sample for SVD...")
    rng = np.random.RandomState(42)
    db = sqlite3.connect(os.path.join(DATA_DIR, "token_clouds.sqlite"))
    total = db.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    indices = set(rng.choice(total, size=100000, replace=False).tolist())
    rows = db.execute("SELECT id, vector FROM chunks").fetchall()
    db.close()
    vectors = [np.frombuffer(blob, dtype=np.float32).copy() for rid, blob in rows if rid in indices]
    V_raw = np.stack(vectors)
    print(f"  {V_raw.shape[0]} tokens")

    # SVD
    print("Running SVD...")
    V_centered = V_raw - V_raw.mean(axis=0)
    from scipy.sparse.linalg import svds
    U, S, Vt = svds(V_centered.astype(np.float64), k=256)
    idx = np.argsort(S)[::-1]
    S = S[idx]; Vt = Vt[idx, :]
    print(f"  SVD done, top S: {S[0]:.1f}")

    # Load full clouds
    print("Loading full doc clouds...")
    db = sqlite3.connect(os.path.join(DATA_DIR, "token_clouds.sqlite"))
    rows = db.execute("SELECT file_id, vector FROM chunks ORDER BY file_id").fetchall()
    db.close()
    doc_clouds = {}
    for fid, blob in rows:
        vec = np.frombuffer(blob, dtype=np.float32)
        doc_clouds.setdefault(fid, []).append(vec)
    for fid in doc_clouds:
        doc_clouds[fid] = np.stack(doc_clouds[fid])

    print("Loading full query clouds...")
    db = sqlite3.connect(os.path.join(DATA_DIR, "query_token_clouds.sqlite"))
    rows = db.execute("SELECT file_id, vector FROM chunks ORDER BY file_id").fetchall()
    db.close()
    query_clouds = {}
    for fid, blob in rows:
        vec = np.frombuffer(blob, dtype=np.float32)
        query_clouds.setdefault(fid, []).append(vec)
    for fid in query_clouds:
        query_clouds[fid] = np.stack(query_clouds[fid])

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

    # Global mean
    all_centroids = np.stack([c.mean(axis=0) for c in doc_clouds.values()])
    V_mean = all_centroids.mean(axis=0)

    # Also compute 4096d cosine baseline
    print("\nRunning cosine baseline (4096d)...")
    doc_cent_norm = {}
    for fid, cloud in doc_clouds.items():
        c = cloud.mean(axis=0)
        doc_cent_norm[fid] = c / (np.linalg.norm(c) + 1e-10)

    ndcg_cos = []
    for qfid, cloud in query_clouds.items():
        qsid = query_map.get(qfid)
        if qsid is None or qsid not in qrels:
            continue
        q = cloud.mean(axis=0)
        q_n = q / (np.linalg.norm(q) + 1e-10)
        scores = [(doc_map[dfid], float(np.dot(q_n, d_n))) for dfid, d_n in doc_cent_norm.items()]
        scores.sort(key=lambda x: x[1], reverse=True)
        ranked = [s[0] for s in scores[:10]]
        dcg = sum((2**qrels[qsid].get(ranked[i], 0) - 1) / np.log2(i + 2) for i in range(len(ranked)))
        ideal = sorted(qrels[qsid].values(), reverse=True)[:10]
        idcg = sum((2**r - 1) / np.log2(i + 2) for i, r in enumerate(ideal))
        ndcg_cos.append(dcg / idcg if idcg > 0 else 0)
    print(f"  Cosine 4096d: NDCG@10 = {np.mean(ndcg_cos):.4f} ({len(ndcg_cos)} queries)")

    # SVD mode space retrieval
    results = {"cosine_4096d": {"ndcg_at_10": float(np.mean(ndcg_cos)), "n_queries": len(ndcg_cos)}}

    for n_modes in [2, 4, 8, 16, 32, 64, 128, 256]:
        proj = Vt[:n_modes, :]

        doc_proj = {}
        for fid, cloud in doc_clouds.items():
            c = cloud.mean(axis=0) - V_mean
            doc_proj[fid] = proj @ c

        query_proj = {}
        for fid, cloud in query_clouds.items():
            c = cloud.mean(axis=0) - V_mean
            query_proj[fid] = proj @ c

        ndcg_scores = []
        for qfid, q_vec in query_proj.items():
            qsid = query_map.get(qfid)
            if qsid is None or qsid not in qrels:
                continue
            q_n = q_vec / (np.linalg.norm(q_vec) + 1e-10)
            scores = []
            for dfid, d_vec in doc_proj.items():
                d_n = d_vec / (np.linalg.norm(d_vec) + 1e-10)
                scores.append((doc_map[dfid], float(np.dot(q_n, d_n))))
            scores.sort(key=lambda x: x[1], reverse=True)
            ranked = [s[0] for s in scores[:10]]
            dcg = sum((2**qrels[qsid].get(ranked[i], 0) - 1) / np.log2(i + 2) for i in range(len(ranked)))
            ideal = sorted(qrels[qsid].values(), reverse=True)[:10]
            idcg = sum((2**r - 1) / np.log2(i + 2) for i, r in enumerate(ideal))
            ndcg_scores.append(dcg / idcg if idcg > 0 else 0)

        mean_ndcg = np.mean(ndcg_scores)
        delta = (mean_ndcg - np.mean(ndcg_cos)) / np.mean(ndcg_cos) * 100
        print(f"  SVD k={n_modes:4d}: NDCG@10 = {mean_ndcg:.4f} ({delta:+.2f}% vs cosine)")
        results[f"svd_{n_modes}"] = {"ndcg_at_10": float(mean_ndcg), "n_queries": len(ndcg_scores)}

    # Summary
    print(f"\n{'='*50}")
    baseline = results["cosine_4096d"]["ndcg_at_10"]
    for name, res in sorted(results.items(), key=lambda x: x[1]["ndcg_at_10"], reverse=True):
        delta = f"{(res['ndcg_at_10'] - baseline) / baseline * 100:+.2f}%" if name != "cosine_4096d" else "(baseline)"
        print(f"  {name:16s} {res['ndcg_at_10']:.4f}  {delta}")

    out_path = os.path.join(EXP_DIR, "exp007b_retrieval_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {out_path}")
    print(f"Total: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
