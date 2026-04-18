#!/usr/bin/env python3
"""Block IV Dim 4: attractor count k* via k-means silhouette on 100-doc final
states (a, b) for IV-A (byte source) and IV-B (BGE source).
Representation: phase_cos_sin (matches block3_cluster.py best representation).
"""
import json, numpy as np, sys, csv
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

OUT = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4")
G = 32; N = G**3


def load_states(states_bin, n):
    raw = np.fromfile(states_bin, dtype=np.float32).reshape(n, 2, N)
    return raw[:, 0, :], raw[:, 1, :]  # a, b


def best_k(a, b, k_min=2, k_max=20):
    """Try multiple representations; return (best_rep, best_k, best_sil, full_table)."""
    amp = np.sqrt(a**2 + b**2)
    phase = np.arctan2(b, a)
    reps = {
        "raw_ab": np.concatenate([a, b], axis=1),
        "amplitude": amp,
        "phase_cos_sin": np.concatenate([np.cos(phase), np.sin(phase)], axis=1),
    }
    table = []
    best = ("", 0, -1.0)
    for name, X in reps.items():
        Xn = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)
        for k in range(k_min, k_max+1):
            km = KMeans(n_clusters=k, n_init=10, random_state=20260412).fit(Xn)
            if len(set(km.labels_)) < 2:
                sil = -1.0
            else:
                sil = float(silhouette_score(Xn, km.labels_))
            table.append((name, k, sil))
            if sil > best[2]: best = (name, k, sil)
    return best, table


def main():
    rows = []
    summary = {}
    for group, sb in [("IV-A", OUT/"dim4_IV-A_states.bin"), ("IV-B", OUT/"dim4_IV-B_states.bin")]:
        meta = json.load(open(str(sb).replace("_states.bin","_meta.json")))
        n = meta["n_docs"]
        print(f"\n=== {group} ({n} docs) ===")
        a, b = load_states(sb, n)
        best, table = best_k(a, b)
        print(f"  best: rep={best[0]} k*={best[1]} silhouette={best[2]:.4f}")
        summary[group] = {"n_docs": n, "best_rep": best[0], "k_star": best[1], "silhouette": best[2]}
        for rep, k, sil in table:
            rows.append({"group": group, "representation": rep, "k": k, "silhouette": f"{sil:.4f}"})
    # Save scan
    with open(OUT/"dim4_attractor_scan.csv","w",newline="") as f:
        w = csv.DictWriter(f, fieldnames=["group","representation","k","silhouette"])
        w.writeheader()
        for r in rows: w.writerow(r)
    # Summary
    with open(OUT/"dim4_attractor_k.csv","w",newline="") as f:
        w = csv.DictWriter(f, fieldnames=["group","n_docs","best_representation","k_star","silhouette"])
        w.writeheader()
        for g, s in summary.items():
            w.writerow({"group": g, "n_docs": s["n_docs"], "best_representation": s["best_rep"],
                        "k_star": s["k_star"], "silhouette": f"{s['silhouette']:.4f}"})
    json.dump(summary, open(OUT/"dim4_attractor_k.json","w"), indent=2)
    print("\nSummary:", json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
