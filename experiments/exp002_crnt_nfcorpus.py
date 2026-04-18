"""
MaoField Experiment 002: CRNT on NFCorpus
==========================================
From toy to real data.

Core idea:
- SVD modes = "species" (not hand-defined, discovered from data)
- Each SVD mode has positive and negative directions = a pair of opposing species
- Token projections onto SVD modes = "concentrations"
- CRNT dynamics: opposing species react, system evolves to equilibrium
- Equilibrium state = document score

Species definition:
  For each SVD mode m (m=0..k-1):
    X_{2m}   = positive projection (tokens projected onto +direction)
    X_{2m+1} = negative projection (tokens projected onto -direction)
  Total: 2k species

Reactions (for each mode m):
    R_fwd: X_{2m} + X_{2m+1} -> C_m   (opposition -> synthesis, rate k_fwd)
    R_rev: C_m -> X_{2m} + X_{2m+1}    (reverse, rate k_rev)
  This models dialectical unity: opposing aspects combine into a synthesis.

Scoring:
  For (query, doc) pair:
    1. Project query tokens onto SVD modes -> query concentrations
    2. Project doc tokens onto SVD modes -> doc concentrations
    3. Combine into initial state x0
    4. Run CRNT to equilibrium
    5. Score = f(equilibrium state) -- how "resolved" the contradictions are

Baseline: PQ-Chamfer NDCG@10 on NFCorpus

Deploy on: Linux server 192.168.31.36
Data: /home/amd/HEZIMENG/legal-assistant/beir_data/nfcorpus/
"""

import sqlite3
import numpy as np
import json
import time
import os
from collections import defaultdict

DATA_DIR = "/home/amd/HEZIMENG/legal-assistant/beir_data/nfcorpus"
EXP_DIR = "/home/amd/HEZIMENG/MaoField/experiments"

K_MODES = 8       # number of SVD modes (= 8 pairs of species = 16 species total)
N_SAMPLE = 50000  # tokens for SVD
N_STEPS = 200     # CRNT evolution steps
DT = 0.01
K_FWD = 0.5       # forward reaction rate (opposition -> synthesis)
K_REV = 0.05      # reverse reaction rate
TOP_N = 100       # candidates from cosine prescore


def load_doc_tokens(db_path, doc_ids=None):
    """Load token clouds for specific documents. Returns {file_id: np.array(n_tokens, 4096)}"""
    db = sqlite3.connect(db_path)
    docs = {}
    if doc_ids is not None:
        placeholders = ','.join('?' * len(doc_ids))
        rows = db.execute(
            f"SELECT file_id, vector FROM chunks WHERE file_id IN ({placeholders}) ORDER BY file_id, id",
            doc_ids
        ).fetchall()
    else:
        rows = db.execute("SELECT file_id, vector FROM chunks ORDER BY file_id, id").fetchall()
    db.close()

    for fid, blob in rows:
        vec = np.frombuffer(blob, dtype=np.float32).copy()
        if fid not in docs:
            docs[fid] = []
        docs[fid].append(vec)

    return {fid: np.stack(vecs) for fid, vecs in docs.items()}


def load_query_tokens(db_path, query_ids=None):
    """Load query token clouds. Returns {file_id: np.array(n_tokens, 4096)}"""
    return load_doc_tokens(db_path, query_ids)


def load_centroids(db_path):
    """Load sentence-level centroids from clouds.sqlite"""
    db = sqlite3.connect(db_path)
    rows = db.execute("SELECT file_id, vector FROM chunks ORDER BY file_id").fetchall()
    db.close()
    centroids = {}
    for fid, blob in rows:
        centroids[fid] = np.frombuffer(blob, dtype=np.float32).copy()
    return centroids


def load_qrels():
    qrels = defaultdict(dict)
    qrels_path = os.path.join(DATA_DIR, "qrels", "test.tsv")
    with open(qrels_path) as f:
        next(f)  # skip header
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                qid, did, rel = parts[0], parts[1], int(parts[2])
                if rel > 0:
                    qrels[qid][did] = rel
    return qrels


def compute_svd(db_path, n_sample, k):
    """Sample tokens, compute truncated SVD -> (Vh, singular_values)"""
    print(f"Computing SVD with k={k} from {n_sample} sampled tokens...")
    db = sqlite3.connect(db_path)
    total = db.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    rng = np.random.default_rng(42)
    indices = set(rng.choice(total, size=min(n_sample, total), replace=False).tolist())

    vectors = []
    for row_id, blob in db.execute("SELECT id, vector FROM chunks"):
        if row_id in indices:
            vectors.append(np.frombuffer(blob, dtype=np.float32).copy())
    db.close()

    V = np.stack(vectors)
    print(f"  Matrix shape: {V.shape}")

    # Center
    mean = V.mean(axis=0)
    V_centered = V - mean

    # Truncated SVD via randomized method
    from scipy.sparse.linalg import svds
    U, s, Vh = svds(V_centered, k=k)

    # Sort by descending singular value
    order = np.argsort(-s)
    s = s[order]
    Vh = Vh[order]

    print(f"  Singular values: {s}")
    print(f"  Variance explained: {(s**2).sum() / (np.linalg.norm(V_centered)**2) * 100:.1f}%")

    return Vh, s, mean


def tokens_to_concentrations(tokens, Vh):
    """
    Project tokens onto SVD modes -> concentrations for 2k species.
    For mode m:
      positive projection -> species 2m
      negative projection -> species 2m+1
    """
    k = Vh.shape[0]
    projections = tokens @ Vh.T  # (n_tokens, k)

    # Aggregate: mean projection per mode
    mean_proj = projections.mean(axis=0)  # (k,)

    concentrations = np.zeros(2 * k)
    for m in range(k):
        concentrations[2*m]   = max(mean_proj[m], 0)    # positive part
        concentrations[2*m+1] = max(-mean_proj[m], 0)    # negative part

    return concentrations


def crnt_evolve(x_query, x_doc, k, n_steps=N_STEPS, dt=DT, k_fwd=K_FWD, k_rev=K_REV):
    """
    Run CRNT dynamics for a (query, doc) pair.

    Initial state: combined concentrations from query and doc.
    Reactions per mode m:
      X_{2m} + X_{2m+1} -> Cm   (rate k_fwd * x[2m] * x[2m+1])
      Cm -> X_{2m} + X_{2m+1}   (rate k_rev * cm)

    Returns: final energy (lower = better match = more resolved contradictions)
    """
    n_species = 2 * k
    # Initial: blend query and doc concentrations
    x = x_query + x_doc  # combined activation
    synthesis = np.zeros(k)  # Cm for each mode

    for step in range(n_steps):
        x = np.maximum(x, 0)
        synthesis = np.maximum(synthesis, 0)

        for m in range(k):
            # Forward: opposition -> synthesis
            rate_fwd = k_fwd * x[2*m] * x[2*m+1]
            # Reverse: synthesis -> opposition
            rate_rev = k_rev * synthesis[m]

            # Update
            dx = (-rate_fwd + rate_rev) * dt
            x[2*m]   += dx
            x[2*m+1] += dx
            synthesis[m] += (rate_fwd - rate_rev) * dt

    # Score: total synthesis achieved (higher = contradictions more resolved = better match)
    # Intuition: if query and doc are compatible, their opposing aspects combine easily
    score = synthesis.sum()

    # Also compute remaining contradiction (unresolved opposition)
    remaining_opposition = sum(x[2*m] * x[2*m+1] for m in range(k))

    # Final score: synthesis - remaining opposition
    return score - 0.1 * remaining_opposition


def cosine_prescore(query_centroid, doc_centroids, top_n):
    """Cosine similarity pre-screening"""
    qnorm = query_centroid / (np.linalg.norm(query_centroid) + 1e-10)
    scores = {}
    for did, dvec in doc_centroids.items():
        dnorm = dvec / (np.linalg.norm(dvec) + 1e-10)
        scores[did] = float(np.dot(qnorm, dnorm))
    sorted_docs = sorted(scores.items(), key=lambda x: -x[1])
    return [did for did, _ in sorted_docs[:top_n]]


def ndcg_at_k(ranking, qrels_dict, k=10):
    """Compute NDCG@k"""
    dcg = 0.0
    for i, did in enumerate(ranking[:k]):
        rel = qrels_dict.get(str(did), 0)
        dcg += rel / np.log2(i + 2)

    # Ideal DCG
    ideal_rels = sorted(qrels_dict.values(), reverse=True)[:k]
    idcg = sum(r / np.log2(i + 2) for i, r in enumerate(ideal_rels))

    return dcg / idcg if idcg > 0 else 0.0


def main():
    print("=" * 60)
    print("MaoField Exp002: CRNT on NFCorpus")
    print("=" * 60)

    # Step 1: Load data
    print("\n[1] Loading centroids for pre-screening...")
    centroids = load_centroids(os.path.join(DATA_DIR, "clouds.sqlite"))
    print(f"  Loaded {len(centroids)} document centroids")

    # Map string IDs to int IDs
    # In BEIR, doc IDs might be strings. Let's check the qrels.
    qrels = load_qrels()
    print(f"  Loaded qrels: {len(qrels)} queries with relevance judgments")

    # Step 2: Compute SVD from doc tokens
    print(f"\n[2] Computing SVD (k={K_MODES})...")
    token_db = os.path.join(DATA_DIR, "token_clouds.sqlite")
    Vh, sing_vals, mean_vec = compute_svd(token_db, N_SAMPLE, K_MODES)

    # Step 3: Evaluate
    print(f"\n[3] Running CRNT scoring on queries...")
    query_db = os.path.join(DATA_DIR, "query_token_clouds.sqlite")

    # Load all query tokens
    query_tokens_all = load_query_tokens(query_db)
    print(f"  Loaded token clouds for {len(query_tokens_all)} queries")

    # Get query IDs that have qrels
    query_ids_with_qrels = []
    qid_to_fid = {}  # map string qrel ID to file_id

    # We need to figure out the mapping between file_id and qrel query_id
    # Load query texts to map
    qdb = sqlite3.connect(query_db)
    # Get unique file_ids
    fids = [r[0] for r in qdb.execute("SELECT DISTINCT file_id FROM chunks ORDER BY file_id").fetchall()]
    qdb.close()

    # In BEIR NFCorpus, query IDs in qrels are like "PLAIN-xxx"
    # file_ids in our DB are integers 0, 1, 2, ...
    # We need a mapping file. Let's check if there's a queries.jsonl
    queries_file = os.path.join(DATA_DIR, "queries.jsonl")
    query_id_map = {}  # file_id -> qrel_id
    if os.path.exists(queries_file):
        with open(queries_file) as f:
            for idx, line in enumerate(f):
                obj = json.loads(line)
                qid = obj.get("_id", str(idx))
                query_id_map[idx] = qid
    else:
        # Fallback: try integer mapping
        for fid in fids:
            query_id_map[fid] = str(fid)

    # Similarly for docs
    corpus_file = os.path.join(DATA_DIR, "corpus.jsonl")
    doc_id_map = {}  # file_id -> corpus_id (string)
    if os.path.exists(corpus_file):
        with open(corpus_file) as f:
            for idx, line in enumerate(f):
                obj = json.loads(line)
                did = obj.get("_id", str(idx))
                doc_id_map[idx] = did
    else:
        cdb = sqlite3.connect(os.path.join(DATA_DIR, "clouds.sqlite"))
        for fid, in cdb.execute("SELECT DISTINCT file_id FROM chunks ORDER BY file_id"):
            doc_id_map[fid] = str(fid)
        cdb.close()

    # Reverse map: corpus_id -> file_id
    corpus_id_to_fid = {v: k for k, v in doc_id_map.items()}

    # Filter queries that have qrels
    valid_queries = []
    for fid, qid in query_id_map.items():
        if qid in qrels and fid in query_tokens_all:
            valid_queries.append((fid, qid))

    print(f"  Valid queries (have qrels + tokens): {len(valid_queries)}")

    if len(valid_queries) == 0:
        print("  WARNING: No valid queries found. Trying integer ID mapping...")
        for fid in fids:
            qid = str(fid)
            if qid in qrels and fid in query_tokens_all:
                valid_queries.append((fid, qid))
        print(f"  Valid queries (integer mapping): {len(valid_queries)}")

    if len(valid_queries) == 0:
        print("  ERROR: Cannot map query IDs. Exiting.")
        return

    # Limit for initial test
    max_queries = min(50, len(valid_queries))
    valid_queries = valid_queries[:max_queries]
    print(f"  Running on {max_queries} queries (first batch)")

    # Pre-compute doc tokens for top-N candidates (lazy load)
    doc_token_cache = {}

    ndcg_cosine_list = []
    ndcg_crnt_list = []

    t0 = time.time()
    for qi, (fid, qid) in enumerate(valid_queries):
        # Query tokens
        q_tokens = query_tokens_all[fid] - mean_vec  # center
        q_conc = tokens_to_concentrations(q_tokens, Vh)

        # Cosine pre-screen
        q_centroid = centroids.get(fid) or q_tokens.mean(axis=0)
        # Actually query centroids might be in a different DB. Use mean of tokens.
        q_centroid = query_tokens_all[fid].mean(axis=0)
        top_doc_fids = cosine_prescore(q_centroid, centroids, TOP_N)

        # Load doc tokens for candidates (lazy)
        missing = [d for d in top_doc_fids if d not in doc_token_cache]
        if missing:
            new_docs = load_doc_tokens(token_db, missing)
            doc_token_cache.update(new_docs)

        # Score each candidate with CRNT
        crnt_scores = {}
        for dfid in top_doc_fids:
            if dfid not in doc_token_cache:
                continue
            d_tokens = doc_token_cache[dfid] - mean_vec
            d_conc = tokens_to_concentrations(d_tokens, Vh)
            score = crnt_evolve(q_conc.copy(), d_conc.copy(), K_MODES)
            did_str = doc_id_map.get(dfid, str(dfid))
            crnt_scores[did_str] = score

        # Cosine ranking (for baseline)
        cosine_scores = {}
        for dfid in top_doc_fids:
            did_str = doc_id_map.get(dfid, str(dfid))
            dvec = centroids.get(dfid)
            if dvec is not None:
                cosine_scores[did_str] = float(
                    np.dot(q_centroid, dvec) / (np.linalg.norm(q_centroid) * np.linalg.norm(dvec) + 1e-10)
                )

        # Rank
        cosine_ranking = [did for did, _ in sorted(cosine_scores.items(), key=lambda x: -x[1])]
        crnt_ranking = [did for did, _ in sorted(crnt_scores.items(), key=lambda x: -x[1])]

        # NDCG@10
        qrels_dict = qrels[qid]
        ndcg_cos = ndcg_at_k(cosine_ranking, qrels_dict, k=10)
        ndcg_crnt = ndcg_at_k(crnt_ranking, qrels_dict, k=10)

        ndcg_cosine_list.append(ndcg_cos)
        ndcg_crnt_list.append(ndcg_crnt)

        if (qi + 1) % 10 == 0 or qi == 0:
            elapsed = time.time() - t0
            print(f"  [{qi+1}/{max_queries}] cosine={np.mean(ndcg_cosine_list):.4f} "
                  f"crnt={np.mean(ndcg_crnt_list):.4f} "
                  f"({elapsed:.1f}s)")

    # Final results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    mean_cos = np.mean(ndcg_cosine_list)
    mean_crnt = np.mean(ndcg_crnt_list)
    delta = (mean_crnt - mean_cos) / mean_cos * 100
    print(f"  Cosine baseline NDCG@10:  {mean_cos:.4f}")
    print(f"  CRNT NDCG@10:             {mean_crnt:.4f}")
    print(f"  Delta:                    {delta:+.2f}%")
    print(f"  Queries evaluated:        {len(ndcg_cosine_list)}")
    print(f"  SVD modes (k):            {K_MODES}")
    print(f"  CRNT steps:               {N_STEPS}")
    print(f"  k_fwd={K_FWD}, k_rev={K_REV}, dt={DT}")

    # Save results
    results = {
        "experiment": "exp002_crnt_nfcorpus",
        "cosine_ndcg10": mean_cos,
        "crnt_ndcg10": mean_crnt,
        "delta_pct": delta,
        "n_queries": len(ndcg_cosine_list),
        "k_modes": K_MODES,
        "n_steps": N_STEPS,
        "k_fwd": K_FWD,
        "k_rev": K_REV,
        "per_query": [
            {"qid": qid, "cosine": c, "crnt": r}
            for (_, qid), c, r in zip(valid_queries, ndcg_cosine_list, ndcg_crnt_list)
        ]
    }
    out_path = os.path.join(EXP_DIR, "exp002_results.json")
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n  Saved to {out_path}")


if __name__ == "__main__":
    main()
