"""Block IV.5 Stage A1: multi-well potential diagnostic.
Analyses:
  1. amplitude histogram (expect 3 peaks at |psi|=0,1,2)
  2. phase uniformity (global+per-doc |R|, antipodal distance)
  3. k-means k=2..5 on raw_ab / amplitude / phase_cos_sin
Outputs under results/block4_5/:
  a1_amp_hist.png, a1_phase_diag.png, a1_cluster_k_search.csv, a1_verdict.md
"""
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

RESULTS = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results")
OUT = RESULTS / "block4_5"
OUT.mkdir(exist_ok=True)

G = 32; N = G**3

meta = json.load(open(OUT.parent/"block4_5"/"a1_meta.json"))
n = meta["n_docs"]
raw = np.fromfile(OUT/"a1_states.bin", dtype=np.float32).reshape(n, 2, N)
a, b = raw[:, 0, :], raw[:, 1, :]
amp = np.sqrt(a**2 + b**2)  # (n, N)
phase = np.arctan2(b, a)
u = amp**2

print(f"Loaded {n} docs  dt={meta['dt']} steps={meta['evolve_steps']} potential={meta['potential']}")
print(f"  amp range [{amp.min():.4f}, {amp.max():.4f}]  mean={amp.mean():.4f}")
print(f"  u range   [{u.min():.4f}, {u.max():.4f}]  mean={u.mean():.4f}")

# ---- 1. amplitude histogram ----
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
h, edges, _ = axes[0].hist(amp.ravel(), bins=100, range=(0, 2.5), color='teal', alpha=0.85)
axes[0].axvline(0.0, color='red', ls='--', alpha=0.6, label='|psi|=0 well')
axes[0].axvline(1.0, color='orange', ls='--', alpha=0.6, label='|psi|=1 well')
axes[0].axvline(2.0, color='purple', ls='--', alpha=0.6, label='|psi|=2 well')
axes[0].set_xlabel("|psi|"); axes[0].set_ylabel("voxel count")
axes[0].set_title(f"A1 amplitude histogram ({n*N:,} voxels)")
axes[0].legend()

# u distribution (clearer for well identification)
axes[1].hist(u.ravel(), bins=100, range=(0, 6.0), color='crimson', alpha=0.85)
for u_w, c in zip([0.0, 1.0, 4.0], ['red','orange','purple']):
    axes[1].axvline(u_w, color=c, ls='--', alpha=0.6, label=f'u={u_w}')
axes[1].set_xlabel("u = |psi|^2"); axes[1].set_ylabel("voxel count")
axes[1].set_title("A1 u-squared distribution")
axes[1].legend()
plt.tight_layout()
plt.savefig(OUT/"a1_amp_hist.png", dpi=120)
plt.close()
print(f"saved {OUT/'a1_amp_hist.png'}")

# Find peaks (simple local max in smoothed histogram)
centers = 0.5*(edges[1:]+edges[:-1])
from scipy.ndimage import gaussian_filter1d
h_smooth = gaussian_filter1d(h, sigma=1.5)
peaks = []
for i in range(1, len(h_smooth)-1):
    if h_smooth[i] > h_smooth[i-1] and h_smooth[i] > h_smooth[i+1] and h_smooth[i] > h_smooth.max()*0.02:
        peaks.append((centers[i], float(h_smooth[i])))
print(f"amplitude peaks (pos, height): {peaks}")

# occupancy per well (bucket by nearest u-well)
u_flat = u.ravel()
d0 = np.abs(u_flat - 0.0)
d1 = np.abs(u_flat - 1.0)
d4 = np.abs(u_flat - 4.0)
stacked = np.stack([d0, d1, d4], axis=1)
nearest = stacked.argmin(axis=1)
occ = [float((nearest==i).mean()) for i in range(3)]
print(f"well occupancy (u=0, u=1, u=4): {occ}")

# ---- 2. phase diagnostic ----
def uniformity_stats(phi):
    R = np.abs(np.mean(np.exp(1j*phi)))
    h_, _ = np.histogram(phi, bins=72, range=(-np.pi, np.pi))
    exp = len(phi) / 72
    chi2 = np.sum((h_ - exp)**2 / exp)
    return float(R), float(chi2/72)

R_glob, chi2_glob = uniformity_stats(phase.ravel())
R_perdoc = np.array([uniformity_stats(phase[i])[0] for i in range(n)])
mean_phase = np.angle(np.mean(np.exp(1j*phase), axis=1))
pts = np.column_stack([np.cos(mean_phase), np.sin(mean_phase)])
km2 = KMeans(n_clusters=2, n_init=10, random_state=20260412).fit(pts)
centers_phi = np.angle(km2.cluster_centers_[:,0] + 1j*km2.cluster_centers_[:,1])
def ang_dist(a_, b_):
    d = abs(a_-b_); return min(d, 2*np.pi-d)
antipodal = float(np.degrees(ang_dist(centers_phi[0], centers_phi[1])))

print(f"\n--- phase uniformity ---")
print(f"global |R|={R_glob:.4f}  chi2/n={chi2_glob:.2f}")
print(f"per-doc |R| mean={R_perdoc.mean():.4f} +- {R_perdoc.std():.4f}")
print(f"kmeans-2 antipodal distance: {antipodal:.1f} deg")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].hist(phase.ravel(), bins=72, density=True, color='coral', alpha=0.85)
axes[0].axhline(y=1/(2*np.pi), color='red', ls='--', label=f'uniform {1/(2*np.pi):.4f}')
axes[0].set_title(f"A1: phase distribution\n|R|_glob={R_glob:.3f}")
axes[0].set_xlabel("phase phi"); axes[0].legend()
axes[1].hist(mean_phase, bins=30, color='teal', alpha=0.85)
axes[1].set_title(f"A1: per-doc mean phase\nmean |R|={R_perdoc.mean():.3f}, antipodal={antipodal:.0f} deg")
axes[1].set_xlabel("mean phi per doc")
plt.tight_layout()
plt.savefig(OUT/"a1_phase_diag.png", dpi=120)
plt.close()
print(f"saved {OUT/'a1_phase_diag.png'}")

# ---- 3. k-means scan on 3 representations ----
# Build per-doc feature vectors
feat_raw_ab = np.concatenate([a, b], axis=1)  # (n, 2N)
feat_amp = amp  # (n, N)
feat_phase_cs = np.concatenate([np.cos(phase), np.sin(phase)], axis=1)  # (n, 2N)

rows = []
for name, X in [("raw_ab", feat_raw_ab), ("amplitude", feat_amp), ("phase_cos_sin", feat_phase_cs)]:
    for k in [2,3,4,5]:
        km = KMeans(n_clusters=k, n_init=10, random_state=20260412).fit(X)
        lab = km.labels_
        if len(set(lab)) < 2:
            sil = float('nan')
        else:
            # subsample for silhouette speed
            idx = np.arange(len(X))
            sil = float(silhouette_score(X, lab))
        inertia = float(km.inertia_)
        rows.append({"repr": name, "k": k, "silhouette": sil, "inertia": inertia})
        print(f"  {name} k={k}: sil={sil:.4f}  inertia={inertia:.3e}")

# Write CSV
import csv
with open(OUT/"a1_cluster_k_search.csv","w",newline='') as f:
    w = csv.DictWriter(f, fieldnames=["repr","k","silhouette","inertia"])
    w.writeheader()
    for r in rows: w.writerow(r)
print(f"saved {OUT/'a1_cluster_k_search.csv'}")

# Best k per repr
best = {}
for name in ["raw_ab","amplitude","phase_cos_sin"]:
    sub = [r for r in rows if r["repr"]==name]
    sub_sorted = sorted(sub, key=lambda r: (-r["silhouette"] if not np.isnan(r["silhouette"]) else 1e9))
    best[name] = sub_sorted[0]

print("\n--- best k* per repr ---")
for name, r in best.items():
    print(f"  {name}: k*={r['k']}  sil={r['silhouette']:.4f}")

# ---- Verdict (data-only, no philosophy) ----
verdict = {
    "config": {
        "dt": meta["dt"], "steps": meta["evolve_steps"], "clamp": meta["clamp_hi"],
        "potential": meta["potential"], "init": meta["init"], "n_docs": n,
    },
    "amplitude": {
        "range": [float(amp.min()), float(amp.max())],
        "mean": float(amp.mean()),
        "u_range": [float(u.min()), float(u.max())],
        "u_mean": float(u.mean()),
        "peaks_pos_height": peaks,
        "well_occupancy_u0_u1_u4": occ,
    },
    "phase": {
        "global_R": R_glob, "chi2_per_bin": chi2_glob,
        "per_doc_R_mean": float(R_perdoc.mean()),
        "per_doc_R_std": float(R_perdoc.std()),
        "kmeans2_antipodal_deg": antipodal,
        "kmeans2_centers_deg": np.degrees(centers_phi).tolist(),
    },
    "kmeans_k_search": rows,
    "best_k_per_repr": {k: {"k_star": v["k"], "silhouette": v["silhouette"]} for k,v in best.items()},
}
with open(OUT/"a1_verdict.json","w") as f:
    json.dump(verdict, f, indent=2)

# Markdown summary
with open(OUT/"a1_verdict.md","w") as f:
    f.write("# Block IV.5 Stage A1: Multi-well Amplitude Potential\n\n")
    f.write(f"## Config\nDT={meta['dt']}  steps={meta['evolve_steps']}  clamp={meta['clamp_hi']}  n_docs={n}\n\n")
    f.write(f"Potential: `{meta['potential']}`\n\n")
    f.write(f"Init: `{meta['init']}`\n\n")
    f.write("## Stability\n")
    f.write(f"- u_max (field) = {meta.get('u_max_all', 'n/a')}\n")
    f.write(f"- u_mean (field) = {meta.get('u_mean_all', 'n/a')}\n")
    f.write(f"- n_nan = {meta.get('n_nan', 'n/a')}\n\n")
    f.write("## Amplitude distribution\n")
    f.write(f"- |psi| range: [{amp.min():.4f}, {amp.max():.4f}]  mean {amp.mean():.4f}\n")
    f.write(f"- u=|psi|^2 range: [{u.min():.4f}, {u.max():.4f}]  mean {u.mean():.4f}\n")
    f.write(f"- peaks (pos,height): {peaks}\n")
    f.write(f"- well occupancy fraction [u=0, u=1, u=4]: {[round(x,4) for x in occ]}\n\n")
    f.write("## Phase diagnostic\n")
    f.write(f"| metric | value |\n|---|---|\n")
    f.write(f"| global \\|R\\| | {R_glob:.4f} |\n")
    f.write(f"| chi2 / 72 | {chi2_glob:.2f} |\n")
    f.write(f"| per-doc \\|R\\| mean | {R_perdoc.mean():.4f} +- {R_perdoc.std():.4f} |\n")
    f.write(f"| kmeans-2 antipodal | {antipodal:.1f} deg |\n\n")
    f.write("## k-means k=2..5\n\n")
    f.write("| repr | k | silhouette | inertia |\n|---|---|---|---|\n")
    for r in rows:
        f.write(f"| {r['repr']} | {r['k']} | {r['silhouette']:.4f} | {r['inertia']:.3e} |\n")
    f.write("\n### Best k* per representation\n\n")
    for name, r in best.items():
        f.write(f"- {name}: k*={r['k']}  silhouette={r['silhouette']:.4f}\n")
    f.write("\n## Data rules (no philosophy)\n")
    f.write("- k*>=3 AND |R| < 0.3 -> multi-well clusters resolved by kmeans, phase stays uniform\n")
    f.write("- k*=2 AND |R| < 0.3 -> multi-well may exist in amplitude space but kmeans doesn't split; need manifold-aware eval\n")
    f.write("- |R| >= 0.3 -> phase uniformity broken by multi-well (counter-example)\n")
print(f"\nwrote {OUT/'a1_verdict.md'}")
