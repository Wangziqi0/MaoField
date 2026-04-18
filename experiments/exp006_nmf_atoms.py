"""
MaoField Experiment 006: NMF Semantic Atom Discovery
=====================================================

实验 1: 寻找自然原子数 k（重建误差拐点）
实验 2: 原子的语义解释（top token 分析）
实验 5: 原子间矛盾关系（cosine 矩阵）

三种 NMF 处理方式：
  方案1: V - V.min()（平移到非负）
  方案2: np.maximum(V, 0)（截断负值）
  方案3: 正负分离——V_pos 和 V_neg 分别做 NMF（对立统一）
"""

import sqlite3
import numpy as np
import json
import time
import os
from sklearn.decomposition import NMF

DATA_DIR = "/home/amd/HEZIMENG/legal-assistant/beir_data/nfcorpus"
EXP_DIR = "/home/amd/HEZIMENG/MaoField/experiments"

N_SAMPLE = 100000  # 抽样 token 数
K_VALUES = [2, 3, 4, 8, 16, 32, 64, 128, 256]
RANDOM_STATE = 42


def load_token_sample(db_path, n_sample, rng):
    """Load a random sample of token vectors"""
    db = sqlite3.connect(db_path)
    total = db.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    print(f"  Total tokens in DB: {total}")

    # Sample indices
    indices = rng.choice(total, size=min(n_sample, total), replace=False)
    indices.sort()

    # Also load chunk_text for semantic analysis
    # Load in batches for efficiency
    vectors = []
    texts = []
    file_ids = []

    # Load all at once (faster for sqlite)
    rows = db.execute("SELECT id, file_id, chunk_text, vector FROM chunks").fetchall()
    db.close()

    idx_set = set(indices.tolist())
    for row_id, fid, text, blob in rows:
        if row_id in idx_set:
            vec = np.frombuffer(blob, dtype=np.float32).copy()
            vectors.append(vec)
            texts.append(text or f"token_{row_id}")
            file_ids.append(fid)

    V = np.stack(vectors)
    print(f"  Sampled {V.shape[0]} tokens, dim={V.shape[1]}")
    return V, texts, file_ids


def gini_coefficient(arr):
    """Compute Gini coefficient of an array"""
    arr = np.abs(arr)
    if arr.sum() == 0:
        return 0.0
    sorted_arr = np.sort(arr)
    n = len(sorted_arr)
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * sorted_arr) / (n * np.sum(sorted_arr))) - (n + 1) / n


def run_nmf(V, k, max_iter=500):
    """Run NMF and return model, W, H, and metrics"""
    model = NMF(n_components=k, max_iter=max_iter, random_state=RANDOM_STATE,
                init='nndsvda', solver='mu', beta_loss='frobenius')
    W = model.fit_transform(V)
    H = model.components_
    recon_err = model.reconstruction_err_
    rel_err = recon_err / np.linalg.norm(V, 'fro')

    # Sparsity of W columns (Gini per atom)
    sparsities = [gini_coefficient(W[:, i]) for i in range(k)]

    return model, W, H, recon_err, rel_err, sparsities


# ── Experiment 1: Find natural k ──

def experiment_1(V_shift, V_pos, V_neg):
    print("\n" + "=" * 60)
    print("EXPERIMENT 1: Finding Natural Atom Count k")
    print("=" * 60)

    results = {}

    for scheme_name, V_input in [("shift", V_shift), ("pos_only", V_pos), ("neg_only", V_neg)]:
        print(f"\n  --- Scheme: {scheme_name} (shape={V_input.shape}) ---")
        scheme_results = []

        for k in K_VALUES:
            t0 = time.time()
            print(f"    k={k}...", end=" ", flush=True)

            try:
                _, W, H, recon_err, rel_err, sparsities = run_nmf(V_input, k)
                elapsed = time.time() - t0

                result = {
                    "k": k,
                    "reconstruction_error": float(recon_err),
                    "relative_error": float(rel_err),
                    "mean_sparsity": float(np.mean(sparsities)),
                    "time_s": float(elapsed)
                }
                scheme_results.append(result)
                print(f"rel_err={rel_err:.4f} sparsity={np.mean(sparsities):.4f} ({elapsed:.1f}s)")
            except Exception as e:
                print(f"FAILED: {e}")
                scheme_results.append({"k": k, "error": str(e)})

        results[scheme_name] = scheme_results

    # Print summary
    print("\n  === Summary ===")
    for scheme in ["shift", "pos_only", "neg_only"]:
        print(f"\n  {scheme}:")
        print(f"    {'k':>4s}  {'rel_err':>8s}  {'sparsity':>8s}  {'Δ_err':>8s}")
        prev_err = None
        for r in results[scheme]:
            if "error" in r:
                continue
            delta = f"{r['relative_error'] - prev_err:.4f}" if prev_err else "—"
            print(f"    {r['k']:4d}  {r['relative_error']:8.4f}  {r['mean_sparsity']:8.4f}  {delta:>8s}")
            prev_err = r['relative_error']

    return results


# ── Experiment 2: Atom semantic interpretation ──

def experiment_2(V_input, texts, k, scheme_name):
    print(f"\n{'=' * 60}")
    print(f"EXPERIMENT 2: Atom Semantics (k={k}, {scheme_name})")
    print("=" * 60)

    _, W, H, _, _, _ = run_nmf(V_input, k)

    atom_semantics = []
    for i in range(k):
        # Top 20 tokens by activation for this atom
        top_idx = np.argsort(W[:, i])[::-1][:20]
        top_tokens = [(texts[idx], float(W[idx, i])) for idx in top_idx]

        print(f"\n  Atom {i}:")
        for token, weight in top_tokens[:10]:
            print(f"    {weight:.4f}  {token}")

        atom_semantics.append({
            "atom_id": i,
            "top_tokens": [{"token": t, "weight": w} for t, w in top_tokens]
        })

    return atom_semantics


# ── Experiment 5: Atom contradiction matrix ──

def experiment_5(V_input, k, scheme_name):
    print(f"\n{'=' * 60}")
    print(f"EXPERIMENT 5: Atom Contradiction Matrix (k={k}, {scheme_name})")
    print("=" * 60)

    _, W, H, _, _, _ = run_nmf(V_input, k)

    # H: (k, 4096) — each row is an atom basis vector
    # Compute cosine similarity between atom pairs
    H_norm = H / (np.linalg.norm(H, axis=1, keepdims=True) + 1e-10)
    cos_matrix = H_norm @ H_norm.T  # (k, k)

    print(f"\n  Atom cosine similarity matrix ({k}x{k}):")
    print(f"  Min cosine: {cos_matrix[np.triu_indices(k, 1)].min():.4f}")
    print(f"  Max cosine: {cos_matrix[np.triu_indices(k, 1)].max():.4f}")
    print(f"  Mean cosine: {cos_matrix[np.triu_indices(k, 1)].mean():.4f}")

    # Find opposing atom pairs (cosine < 0)
    opposing = []
    for i in range(k):
        for j in range(i + 1, k):
            if cos_matrix[i, j] < 0:
                opposing.append((i, j, float(cos_matrix[i, j])))

    print(f"\n  Opposing atom pairs (cosine < 0): {len(opposing)}")
    for i, j, c in sorted(opposing, key=lambda x: x[2])[:10]:
        print(f"    Atom {i} vs Atom {j}: cosine = {c:.4f}")

    # For pos/neg split: cross-polarity analysis
    return {
        "cosine_matrix": cos_matrix.tolist(),
        "min_cosine": float(cos_matrix[np.triu_indices(k, 1)].min()),
        "max_cosine": float(cos_matrix[np.triu_indices(k, 1)].max()),
        "mean_cosine": float(cos_matrix[np.triu_indices(k, 1)].mean()),
        "n_opposing_pairs": len(opposing),
        "opposing_pairs": [(int(i), int(j), float(c)) for i, j, c in opposing]
    }


# ── Experiment 5b: Cross-polarity analysis (pos atoms vs neg atoms) ──

def experiment_5b(V_pos, V_neg, k):
    print(f"\n{'=' * 60}")
    print(f"EXPERIMENT 5b: Cross-Polarity (Pos vs Neg atoms, k={k})")
    print("=" * 60)

    _, _, H_pos, _, _, _ = run_nmf(V_pos, k)
    _, _, H_neg, _, _, _ = run_nmf(V_neg, k)

    # Cosine between positive atoms and negative atoms
    H_pos_norm = H_pos / (np.linalg.norm(H_pos, axis=1, keepdims=True) + 1e-10)
    H_neg_norm = H_neg / (np.linalg.norm(H_neg, axis=1, keepdims=True) + 1e-10)
    cross_cos = H_pos_norm @ H_neg_norm.T  # (k, k)

    print(f"\n  Cross-polarity cosine (pos_atom × neg_atom):")
    print(f"  Min: {cross_cos.min():.4f}")
    print(f"  Max: {cross_cos.max():.4f}")
    print(f"  Mean: {cross_cos.mean():.4f}")

    # Find most opposed pos-neg pairs
    print(f"\n  Most opposed pos-neg atom pairs:")
    flat_idx = np.argsort(cross_cos.flatten())
    for rank in range(min(10, len(flat_idx))):
        idx = flat_idx[rank]
        pi, ni = idx // k, idx % k
        print(f"    Pos-Atom {pi} vs Neg-Atom {ni}: cosine = {cross_cos[pi, ni]:.4f}")

    # Find most aligned pos-neg pairs (should be interesting too)
    print(f"\n  Most aligned pos-neg atom pairs:")
    for rank in range(min(5, len(flat_idx))):
        idx = flat_idx[-(rank + 1)]
        pi, ni = idx // k, idx % k
        print(f"    Pos-Atom {pi} vs Neg-Atom {ni}: cosine = {cross_cos[pi, ni]:.4f}")

    return {
        "cross_cosine_matrix": cross_cos.tolist(),
        "min": float(cross_cos.min()),
        "max": float(cross_cos.max()),
        "mean": float(cross_cos.mean())
    }


def main():
    print("=" * 60)
    print("MaoField Exp006: NMF Semantic Atom Discovery")
    print("=" * 60)

    rng = np.random.RandomState(RANDOM_STATE)

    # Load data
    t0 = time.time()
    print("\nLoading token sample...")
    V_raw, texts, file_ids = load_token_sample(
        os.path.join(DATA_DIR, "token_clouds.sqlite"), N_SAMPLE, rng
    )
    print(f"  Load time: {time.time()-t0:.1f}s")

    # Check value range
    print(f"\n  Value range: [{V_raw.min():.4f}, {V_raw.max():.4f}]")
    print(f"  % negative: {(V_raw < 0).mean()*100:.1f}%")
    print(f"  % zero: {(V_raw == 0).mean()*100:.1f}%")

    # Prepare three variants
    print("\nPreparing NMF input variants...")

    # Scheme 1: shift to non-negative
    V_shift = V_raw - V_raw.min()
    print(f"  shift: [{V_shift.min():.4f}, {V_shift.max():.4f}]")

    # Scheme 2: positive part only
    V_pos = np.maximum(V_raw, 0)
    print(f"  pos:   [{V_pos.min():.4f}, {V_pos.max():.4f}], nnz={np.count_nonzero(V_pos)}/{V_pos.size}")

    # Scheme 3: negative part (flipped to positive)
    V_neg = np.maximum(-V_raw, 0)
    print(f"  neg:   [{V_neg.min():.4f}, {V_neg.max():.4f}], nnz={np.count_nonzero(V_neg)}/{V_neg.size}")

    # ── Experiment 1 ──
    exp1_results = experiment_1(V_shift, V_pos, V_neg)

    # ── Find best k (elbow detection via second derivative) ──
    # Use pos_only scheme for experiments 2 and 5
    pos_results = [r for r in exp1_results["pos_only"] if "error" not in r]
    if len(pos_results) >= 3:
        errs = [r["relative_error"] for r in pos_results]
        ks = [r["k"] for r in pos_results]
        # Second derivative (finite differences on log scale)
        log_k = np.log2(ks)
        d1 = np.diff(errs) / np.diff(log_k)
        d2 = np.diff(d1) / np.diff(log_k[:-1])
        # Elbow = where second derivative is most positive (rate of improvement slows most)
        elbow_idx = np.argmax(d2) + 1  # +1 because diff shifts index
        best_k = ks[elbow_idx]
        print(f"\n  Detected elbow at k={best_k}")
    else:
        best_k = 16
        print(f"\n  Using default k={best_k}")

    # ── Experiment 2 ──
    exp2_pos = experiment_2(V_pos, texts, best_k, "pos_only")
    exp2_neg = experiment_2(V_neg, texts, best_k, "neg_only")

    # ── Experiment 5 ──
    exp5_pos = experiment_5(V_pos, best_k, "pos_only")
    exp5_neg = experiment_5(V_neg, best_k, "neg_only")

    # ── Experiment 5b: Cross-polarity ──
    exp5b = experiment_5b(V_pos, V_neg, best_k)

    # Save all results
    all_results = {
        "meta": {
            "dataset": "NFCorpus",
            "n_sample": V_raw.shape[0],
            "dim": V_raw.shape[1],
            "pct_negative": float((V_raw < 0).mean() * 100),
            "best_k": best_k,
            "date": "2026-04-08"
        },
        "exp1_atom_count": exp1_results,
        "exp2_atom_semantics": {
            "pos_atoms": exp2_pos,
            "neg_atoms": exp2_neg
        },
        "exp5_contradiction_matrix": {
            "pos": exp5_pos,
            "neg": exp5_neg,
            "cross_polarity": exp5b
        }
    }

    out_path = os.path.join(EXP_DIR, "exp006_results.json")
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\n\nSaved to {out_path}")
    print(f"Total time: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
