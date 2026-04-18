"""
MaoField Experiment 012: Dialectical Query Expansion
=====================================================

实践→认识→再实践：
1. 原始 query cosine 粗筛 top-10（第一次实践）
2. 从 top-10 文档中提取"query 没说的" token（认识）
3. 扩展 query 点云（新认识）
4. 用扩展后的 query 做 PQ-Chamfer（再实践）

token_new = token_original + expansion_tokens_from_practice
"""

import sqlite3
import numpy as np
import json
import time
import os
import shutil
from collections import defaultdict

DATA_DIR = "/home/amd/HEZIMENG/legal-assistant/beir_data/nfcorpus"
EXP_DIR = "/home/amd/HEZIMENG/MaoField/experiments"


def load_clouds(db_path):
    db = sqlite3.connect(db_path)
    rows = db.execute("SELECT file_id, vector FROM chunks ORDER BY file_id, id").fetchall()
    db.close()
    clouds = {}
    for fid, blob in rows:
        vec = np.frombuffer(blob, dtype=np.float32).copy()
        clouds.setdefault(fid, []).append(vec)
    for fid in clouds:
        clouds[fid] = np.stack(clouds[fid])
    return clouds


def load_sentence_clouds(db_path):
    """Load sentence-level clouds for centroid cosine coarse filter"""
    db = sqlite3.connect(db_path)
    rows = db.execute("SELECT file_id, vector FROM chunks ORDER BY file_id").fetchall()
    db.close()
    clouds = {}
    for fid, blob in rows:
        vec = np.frombuffer(blob, dtype=np.float32)
        clouds.setdefault(fid, []).append(vec)
    for fid in clouds:
        clouds[fid] = np.stack(clouds[fid])
    return clouds


def cosine_topk(query_centroid, doc_centroids, doc_fids, k):
    """Cosine similarity top-k retrieval"""
    q_norm = query_centroid / (np.linalg.norm(query_centroid) + 1e-10)
    sims = []
    for fid in doc_fids:
        d = doc_centroids[fid]
        d_norm = d / (np.linalg.norm(d) + 1e-10)
        sims.append((fid, float(np.dot(q_norm, d_norm))))
    sims.sort(key=lambda x: x[1], reverse=True)
    return [fid for fid, _ in sims[:k]]


def find_implicit_tokens(query_tokens, top_doc_tokens, n_expand):
    """
    Find tokens in top docs that are "implicit" — relevant to the topic
    but NOT covered by the query.

    implicit_score = distance_to_query - distance_to_top_center
    High score = far from query but close to what relevant docs discuss
    """
    # Query centroid and top-docs centroid
    q_cent = query_tokens.mean(axis=0)
    top_cent = top_doc_tokens.mean(axis=0)

    # Normalize for cosine
    q_cent_n = q_cent / (np.linalg.norm(q_cent) + 1e-10)
    top_cent_n = top_cent / (np.linalg.norm(top_cent) + 1e-10)

    # For each token in top docs, compute implicit score
    scores = []
    for i in range(len(top_doc_tokens)):
        t = top_doc_tokens[i]
        t_n = t / (np.linalg.norm(t) + 1e-10)

        # Distance to query (min distance to any query token)
        min_q_sim = max(
            float(np.dot(t_n, qt / (np.linalg.norm(qt) + 1e-10)))
            for qt in query_tokens
        )

        # Similarity to top-docs center
        top_sim = float(np.dot(t_n, top_cent_n))

        # Implicit = close to top center but far from query
        implicit_score = top_sim - min_q_sim

        scores.append((i, implicit_score, t))

    # Sort by implicit score descending
    scores.sort(key=lambda x: x[1], reverse=True)

    # Return top-n expansion tokens
    return np.stack([s[2] for s in scores[:n_expand]])


def find_contrast_tokens(query_tokens, top_doc_tokens, bottom_doc_tokens, n_expand):
    """
    Find tokens that appear in top docs but NOT in bottom docs.
    These discriminate relevant from irrelevant.
    """
    # Bottom docs centroid
    bot_cent = bottom_doc_tokens.mean(axis=0)
    bot_cent_n = bot_cent / (np.linalg.norm(bot_cent) + 1e-10)

    top_cent = top_doc_tokens.mean(axis=0)
    top_cent_n = top_cent / (np.linalg.norm(top_cent) + 1e-10)

    scores = []
    for i in range(len(top_doc_tokens)):
        t = top_doc_tokens[i]
        t_n = t / (np.linalg.norm(t) + 1e-10)

        top_sim = float(np.dot(t_n, top_cent_n))
        bot_sim = float(np.dot(t_n, bot_cent_n))

        # Contrast = close to top but far from bottom
        contrast_score = top_sim - bot_sim

        scores.append((i, contrast_score, t))

    scores.sort(key=lambda x: x[1], reverse=True)
    return np.stack([s[2] for s in scores[:n_expand]])


def save_expanded_queries(original_db, output_db, expanded_clouds):
    """Save expanded query clouds — may have more tokens than original"""
    # Create fresh database
    if os.path.exists(output_db):
        os.remove(output_db)

    db = sqlite3.connect(output_db)
    db.execute("""CREATE TABLE chunks (
        id INTEGER PRIMARY KEY,
        file_id INTEGER NOT NULL,
        chunk_text TEXT,
        vector BLOB
    )""")

    row_id = 0
    for fid in sorted(expanded_clouds.keys()):
        tokens = expanded_clouds[fid]
        for i in range(tokens.shape[0]):
            blob = tokens[i].astype(np.float32).tobytes()
            db.execute("INSERT INTO chunks (id, file_id, chunk_text, vector) VALUES (?,?,?,?)",
                       (row_id, fid, f"token_{i}", blob))
            row_id += 1

    db.commit()
    db.close()


def main():
    print("=" * 60)
    print("MaoField Exp012: Dialectical Query Expansion")
    print("实践→认识→再实践")
    print("=" * 60)
    t0 = time.time()

    # Load data
    print("\nLoading token clouds...")
    doc_clouds = load_clouds(os.path.join(DATA_DIR, "token_clouds.sqlite"))
    query_clouds = load_clouds(os.path.join(DATA_DIR, "query_token_clouds.sqlite"))
    print(f"  {len(doc_clouds)} docs, {len(query_clouds)} queries")

    # Doc centroids for cosine coarse filter
    print("Computing doc centroids...")
    doc_centroids = {}
    for fid, cloud in doc_clouds.items():
        doc_centroids[fid] = cloud.mean(axis=0)
    doc_fids = sorted(doc_clouds.keys())

    # ID maps
    doc_map = {}
    with open(os.path.join(DATA_DIR, "corpus.jsonl")) as f:
        for idx, line in enumerate(f):
            doc_map[idx + 1] = json.loads(line).get("_id", str(idx))
    doc_rmap = {v: k for k, v in doc_map.items()}

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

    # Variants
    variants = [
        {"name": "expand-5", "n_expand": 5, "method": "implicit", "iterations": 1},
        {"name": "expand-10", "n_expand": 10, "method": "implicit", "iterations": 1},
        {"name": "expand-20", "n_expand": 20, "method": "implicit", "iterations": 1},
        {"name": "expand-10-iter2", "n_expand": 10, "method": "implicit", "iterations": 2},
        {"name": "expand-10-contrast", "n_expand": 10, "method": "contrast", "iterations": 1},
    ]

    for var in variants:
        print(f"\n{'='*60}")
        print(f"Variant: {var['name']}")
        print(f"{'='*60}")

        expanded_clouds = {}
        stats = []

        for qfid, q_tokens in query_clouds.items():
            qsid = query_map.get(qfid)
            if qsid is None or qsid not in qrels:
                # Non-eval query: keep original
                expanded_clouds[qfid] = q_tokens
                continue

            current_tokens = q_tokens.copy()

            for iteration in range(var["iterations"]):
                # Step 1: Coarse retrieve top-10 using current query centroid
                q_cent = current_tokens.mean(axis=0)
                top_fids = cosine_topk(q_cent, doc_centroids, doc_fids, k=10)

                # Collect top-10 doc tokens
                top_tokens_list = []
                for fid in top_fids:
                    top_tokens_list.append(doc_clouds[fid])
                top_doc_tokens = np.vstack(top_tokens_list)

                # Step 2: Find expansion tokens
                if var["method"] == "implicit":
                    expansion = find_implicit_tokens(
                        current_tokens, top_doc_tokens, var["n_expand"])
                elif var["method"] == "contrast":
                    # Also get bottom-10
                    bottom_fids = cosine_topk(q_cent, doc_centroids, doc_fids, k=len(doc_fids))
                    bottom_fids = bottom_fids[-10:]
                    bot_tokens = np.vstack([doc_clouds[fid] for fid in bottom_fids])
                    expansion = find_contrast_tokens(
                        current_tokens, top_doc_tokens, bot_tokens, var["n_expand"])

                # Step 3: Expand query
                current_tokens = np.vstack([current_tokens, expansion])

            expanded_clouds[qfid] = current_tokens

            orig_n = q_tokens.shape[0]
            new_n = current_tokens.shape[0]
            stats.append({"fid": qfid, "orig_tokens": orig_n, "new_tokens": new_n})

        eval_stats = [s for s in stats if s["new_tokens"] > s["orig_tokens"]]
        if eval_stats:
            avg_new = np.mean([s["new_tokens"] for s in eval_stats])
            print(f"  Expanded {len(eval_stats)} queries: avg {avg_new:.1f} tokens (from ~6)")

        # Save
        output_db = os.path.join(EXP_DIR, f"expanded_query_{var['name']}.sqlite")
        save_expanded_queries(
            os.path.join(DATA_DIR, "query_token_clouds.sqlite"),
            output_db, expanded_clouds)
        print(f"  Saved: {output_db}")

    print(f"\n\nAll variants saved. Total: {time.time()-t0:.1f}s")
    print("Run: RAYON_NUM_THREADS=70 node exp012_bench.js")


if __name__ == "__main__":
    main()
