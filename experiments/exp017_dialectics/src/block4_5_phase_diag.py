"""Block IV.5 Stage C: phase distribution diagnostic.
Question: Is k*=2 from a hidden phase-locking mechanism?
If phase φ = atan2(b,a) clusters at discrete values → hidden Z_n lock.
If phase is uniform on (-π,π] → no lock, Z_2 comes from elsewhere (Allen-Cahn term or boundary)."""
import numpy as np
import json, os
from pathlib import Path
import matplotlib.pyplot as plt

RESULTS = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results")
OUT = RESULTS / "block4_5"
OUT.mkdir(exist_ok=True)

G = 32; N = G**3

# Load Block III states (IV-A equivalent, byte source)
meta = json.load(open(RESULTS/"block3_meta.json"))
n = meta["n_docs"]
raw = np.fromfile(RESULTS/"block3_states.bin", dtype=np.float32).reshape(n, 2, N)
a_A, b_A = raw[:, 0, :], raw[:, 1, :]
phase_A = np.arctan2(b_A, a_A)  # (n, N) in (-π, π]
amp_A = np.sqrt(a_A**2 + b_A**2)

# Load IV-B states (BGE source)
B_meta_p = RESULTS/"block4"/"dim4_IV-B_meta.json"
B_bin = RESULTS/"block4"/"dim4_IV-B_states.bin"
B_meta = json.load(open(B_meta_p))
nB = B_meta["n_docs"]
rawB = np.fromfile(B_bin, dtype=np.float32).reshape(nB, 2, N)
a_B, b_B = rawB[:, 0, :], rawB[:, 1, :]
phase_B = np.arctan2(b_B, a_B)
amp_B = np.sqrt(a_B**2 + b_B**2)

print(f"IV-A (byte) states: {n} docs, amp range [{amp_A.min():.4f}, {amp_A.max():.4f}], mean |ψ|={amp_A.mean():.4f}")
print(f"IV-B (BGE)  states: {nB} docs, amp range [{amp_B.min():.4f}, {amp_B.max():.4f}], mean |ψ|={amp_B.mean():.4f}")

# ---- Diagnostic 1: global phase histogram (all voxels, all docs) ----
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# IV-A
axes[0,0].hist(phase_A.ravel(), bins=72, density=True, color='steelblue', alpha=0.8)
axes[0,0].axhline(y=1/(2*np.pi), color='red', linestyle='--', label=f'uniform {1/(2*np.pi):.4f}')
axes[0,0].set_title(f"IV-A (byte source): phase distribution\n{n*N:,} voxels")
axes[0,0].set_xlabel("phase φ"); axes[0,0].set_ylabel("density"); axes[0,0].legend()

# IV-B
axes[0,1].hist(phase_B.ravel(), bins=72, density=True, color='coral', alpha=0.8)
axes[0,1].axhline(y=1/(2*np.pi), color='red', linestyle='--', label=f'uniform {1/(2*np.pi):.4f}')
axes[0,1].set_title(f"IV-B (BGE source): phase distribution\n{nB*N:,} voxels")
axes[0,1].set_xlabel("phase φ"); axes[0,1].set_ylabel("density"); axes[0,1].legend()

# Per-doc mean phase (does each doc settle to a specific phase?)
mean_phase_A = np.angle(np.mean(np.exp(1j*phase_A), axis=1))  # circular mean per doc
mean_phase_B = np.angle(np.mean(np.exp(1j*phase_B), axis=1))
axes[1,0].hist(mean_phase_A, bins=30, color='steelblue', alpha=0.8)
axes[1,0].set_title(f"IV-A: circular-mean phase per doc ({n} docs)")
axes[1,0].set_xlabel("mean φ_doc"); axes[1,0].set_ylabel("count")

axes[1,1].hist(mean_phase_B, bins=30, color='coral', alpha=0.8)
axes[1,1].set_title(f"IV-B: circular-mean phase per doc ({nB} docs)")
axes[1,1].set_xlabel("mean φ_doc"); axes[1,1].set_ylabel("count")

plt.tight_layout()
plt.savefig(OUT/"stageC_phase_diag.png", dpi=120)
print(f"saved {OUT/'stageC_phase_diag.png'}")

# ---- Quantitative uniformity test ----
# Kuiper test variant: max deviation from uniform CDF
def uniformity_stats(phi):
    """Return (mean |R|, bin-χ² / n_bins, skew-based asymmetry)."""
    # Circular mean magnitude |R| in [0, 1]: 1 = fully phase-locked, 0 = uniform
    R = np.abs(np.mean(np.exp(1j*phi)))
    # 72-bin histogram χ² against uniform
    h, _ = np.histogram(phi, bins=72, range=(-np.pi, np.pi))
    exp = len(phi) / 72
    chi2 = np.sum((h - exp)**2 / exp)
    return float(R), float(chi2/72)

# Global
R_A, chi2_A = uniformity_stats(phase_A.ravel())
R_B, chi2_B = uniformity_stats(phase_B.ravel())
# Per-doc
R_perdoc_A = [uniformity_stats(phase_A[i])[0] for i in range(n)]
R_perdoc_B = [uniformity_stats(phase_B[i])[0] for i in range(nB)]

print(f"\n--- Global phase uniformity ---")
print(f"IV-A: |R|_global={R_A:.4f}  χ²/n={chi2_A:.2f}")
print(f"IV-B: |R|_global={R_B:.4f}  χ²/n={chi2_B:.2f}")
print(f"  (|R|=1 → fully locked, |R|≈0 → uniform; χ²/n ≈ 1 under uniform null)")

print(f"\n--- Per-doc phase locking ---")
print(f"IV-A: mean |R|_perdoc = {np.mean(R_perdoc_A):.4f} ± {np.std(R_perdoc_A):.4f}")
print(f"IV-B: mean |R|_perdoc = {np.mean(R_perdoc_B):.4f} ± {np.std(R_perdoc_B):.4f}")

# ---- Per-doc mean phase: bimodal? ----
# If k*=2 comes from phase locking to 0 vs π, mean_phase should cluster at {0, π}
from sklearn.cluster import KMeans
pts_A = np.column_stack([np.cos(mean_phase_A), np.sin(mean_phase_A)])
pts_B = np.column_stack([np.cos(mean_phase_B), np.sin(mean_phase_B)])
# Try k=2 on (cos,sin) representation
km_A = KMeans(n_clusters=2, n_init=10, random_state=20260413).fit(pts_A)
km_B = KMeans(n_clusters=2, n_init=10, random_state=20260413).fit(pts_B)
centers_A_phase = np.angle(km_A.cluster_centers_[:,0] + 1j*km_A.cluster_centers_[:,1])
centers_B_phase = np.angle(km_B.cluster_centers_[:,0] + 1j*km_B.cluster_centers_[:,1])

print(f"\n--- k=2 on mean_phase (cos,sin) representation ---")
print(f"IV-A cluster centers (φ): {np.degrees(centers_A_phase).round(1)} deg")
print(f"IV-B cluster centers (φ): {np.degrees(centers_B_phase).round(1)} deg")
print(f"  (if centers are ~180° apart → phase-locked to antipodal → supports 'Z_2 from phase locking')")
print(f"  (if centers are not antipodal → k*=2 is not from phase locking)")

# Angular distance between centers
def ang_dist(a, b):
    d = abs(a-b); return min(d, 2*np.pi - d)
d_A = ang_dist(centers_A_phase[0], centers_A_phase[1])
d_B = ang_dist(centers_B_phase[0], centers_B_phase[1])
print(f"  IV-A antipodal distance: {np.degrees(d_A):.1f}° (π=180° is strict antipodal)")
print(f"  IV-B antipodal distance: {np.degrees(d_B):.1f}°")

# ---- Save results ----
results = {
    "dataset_A": "NFCorpus (byte source, IV-A)",
    "dataset_B": "NFCorpus (BGE source, IV-B)",
    "global": {
        "IV-A": {"R": R_A, "chi2_per_bin": chi2_A},
        "IV-B": {"R": R_B, "chi2_per_bin": chi2_B},
    },
    "per_doc_R_mean": {
        "IV-A": float(np.mean(R_perdoc_A)),
        "IV-B": float(np.mean(R_perdoc_B)),
    },
    "kmeans2_mean_phase_centers_deg": {
        "IV-A": np.degrees(centers_A_phase).tolist(),
        "IV-B": np.degrees(centers_B_phase).tolist(),
        "antipodal_dist_deg": {"IV-A": float(np.degrees(d_A)), "IV-B": float(np.degrees(d_B))},
    },
    "interpretation_rules": {
        "R_close_to_0": "uniform phase, no locking",
        "R_close_to_1": "strong phase lock (Z_1 lock)",
        "antipodal_180": "Z_2 lock (two opposite phases) → k*=2 IS from phase locking",
        "antipodal_not_180": "k*=2 is NOT from phase locking; Z_2 origin lies in amplitude domain",
    },
}
with open(OUT/"stageC_phase_diag.json","w") as f:
    json.dump(results, f, indent=2)

# ---- Verdict ----
print("\n=== STAGE C VERDICT ===")
verdict_lines = []
# Rule: if per-doc |R| < 0.3 and antipodal is far from 180, phase is NOT the Z_2 source
if np.mean(R_perdoc_A) < 0.3 and abs(np.degrees(d_A) - 180) > 30:
    verdict_A = "IV-A: per-doc phase is NEARLY UNIFORM (no strong lock). k*=2 is NOT from phase locking."
elif np.mean(R_perdoc_A) > 0.5 and abs(np.degrees(d_A) - 180) < 30:
    verdict_A = "IV-A: per-doc phase has STRONG Z_2 LOCK (~antipodal). k*=2 IS from phase locking."
else:
    verdict_A = f"IV-A: ambiguous (|R|={np.mean(R_perdoc_A):.3f}, antipodal={np.degrees(d_A):.0f}°). Need deeper test."
verdict_lines.append(verdict_A)

if np.mean(R_perdoc_B) < 0.3 and abs(np.degrees(d_B) - 180) > 30:
    verdict_B = "IV-B: per-doc phase is NEARLY UNIFORM. k*=2 is NOT from phase locking."
elif np.mean(R_perdoc_B) > 0.5 and abs(np.degrees(d_B) - 180) < 30:
    verdict_B = "IV-B: per-doc phase has STRONG Z_2 LOCK. k*=2 IS from phase locking."
else:
    verdict_B = f"IV-B: ambiguous (|R|={np.mean(R_perdoc_B):.3f}, antipodal={np.degrees(d_B):.0f}°)."
verdict_lines.append(verdict_B)

for v in verdict_lines: print(v)

with open(OUT/"stageC_verdict.md","w") as f:
    f.write("# Block IV.5 Stage C: Phase Distribution Diagnostic\n\n")
    f.write("## Question\nIs k*=2 from a hidden phase-locking mechanism (Z_2 via phase antipodes)?\n\n")
    f.write("## Method\nAnalyze phase φ = atan2(b,a) for IV-A (byte) and IV-B (BGE) final states.\n\n")
    f.write("## Metrics\n- `|R|`: circular mean resultant length (0=uniform, 1=locked)\n")
    f.write("- `χ²/n_bins`: goodness-of-fit against uniform\n")
    f.write("- k=2 centers on (cos,sin) of per-doc mean phase: ~180° apart = Z_2 phase lock\n\n")
    f.write(f"## Numbers\n\n")
    f.write(f"| group | global |R| | χ²/72 | per-doc |R| mean | kmeans-2 center dist |\n")
    f.write(f"|---|---|---|---|---|\n")
    f.write(f"| IV-A (byte) | {R_A:.4f} | {chi2_A:.2f} | {np.mean(R_perdoc_A):.4f} | {np.degrees(d_A):.1f}° |\n")
    f.write(f"| IV-B (BGE)  | {R_B:.4f} | {chi2_B:.2f} | {np.mean(R_perdoc_B):.4f} | {np.degrees(d_B):.1f}° |\n\n")
    f.write("## Verdict\n\n")
    for v in verdict_lines: f.write(f"- {v}\n")
    f.write("\n## Next Step\n\n")
    any_locked = any("IS from phase" in v for v in verdict_lines)
    if any_locked:
        f.write("Stage A (Allen-Cahn Z_2 symmetry) test is **skippable** — we already know phase locking is the mechanism.\n")
    else:
        f.write("Proceed to **Stage A**: add external field `+h·Re(ψ)` to Allen-Cahn, test if Z_2 breaks and k* changes.\n")

print(f"\nWrote {OUT/'stageC_verdict.md'}")
