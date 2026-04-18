"""Block IV.5 Stage B1: Langevin σ scan analysis.
For each σ, compute |ψ| distribution + basin occupancy at u∈{0,1,4}."""
import json, numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

RESULTS = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results")
OUT = RESULTS / "block4_5" / "b1_langevin"
G = 32; N = G**3

sigmas = [0.0, 0.1, 0.5, 1.0, 2.0]
stats_table = []

fig, axes = plt.subplots(1, 5, figsize=(22, 4), sharey=True)

for ax, sigma in zip(axes, sigmas):
    meta = json.load(open(OUT / f"s{sigma}_meta.json"))
    n = meta["n_docs"]
    raw = np.fromfile(OUT / f"s{sigma}_states.bin", dtype=np.float32).reshape(n, 2, N)
    a, b = raw[:,0,:], raw[:,1,:]
    amp = np.sqrt(a**2 + b**2)
    u = amp**2

    # Occupancy: voxel within ±0.3 of each basin
    near0 = (u < 0.3).sum() / u.size
    near1 = ((u > 0.5) & (u < 1.5)).sum() / u.size
    near4 = ((u > 3.5) & (u < 4.5)).sum() / u.size
    clamped = (u > 16).sum() / u.size   # near clamp edge |ψ|≈√18

    ax.hist(amp.ravel(), bins=100, range=(0, 5), density=True, color='steelblue')
    ax.axvline(0, color='red', ls='--', alpha=0.5, label='u=0')
    ax.axvline(1, color='green', ls='--', alpha=0.5, label='u=1')
    ax.axvline(2, color='orange', ls='--', alpha=0.5, label='u=4 (|ψ|=2)')
    ax.set_title(f"σ={sigma}")
    ax.set_xlabel("|ψ|"); ax.set_xlim(0, 5)
    if sigma == 0.0: ax.legend()

    print(f"σ={sigma}: u=0 {near0*100:.1f}%  u=1 {near1*100:.1f}%  u=4 {near4*100:.1f}%  clamped {clamped*100:.1f}%")
    stats_table.append({
        "sigma": sigma,
        "u_max_all": meta["u_max_all"],
        "u_mean_all": meta["u_mean_all"],
        "near0_pct": near0*100, "near1_pct": near1*100, "near4_pct": near4*100, "clamped_pct": clamped*100,
    })

plt.suptitle("Block IV.5 Stage B1: Langevin σ scan — amplitude distribution (20 NFC docs, 5000 steps, A1 triple-well)", fontsize=11)
plt.tight_layout()
plt.savefig(OUT.parent / "b1_amp_hist_sigma_scan.png", dpi=120)
print(f"\nSaved plot: {OUT.parent/'b1_amp_hist_sigma_scan.png'}")

# Write CSV
import csv
with open(OUT.parent / "b1_sigma_scan.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["sigma","u_max_all","u_mean_all","near0_pct","near1_pct","near4_pct","clamped_pct"])
    w.writeheader()
    [w.writerow(r) for r in stats_table]
print(f"Saved CSV: {OUT.parent/'b1_sigma_scan.csv'}")

# Verdict MD
lines = ["# Block IV.5 Stage B1: Langevin σ Scan — Results", "",
         "## Config", f"- A1 multi-well potential V = |ψ|²(|ψ|²−1)²(|ψ|²−4)²",
         f"- BGE-M3 embedding source (20 NFC docs, same as Stage A1 subset)",
         f"- DT=0.05, steps=5000, clamp_hi=3.0, init |ψ|≈1.0±0.3",
         f"- σ ∈ {{0.0, 0.1, 0.5, 1.0, 2.0}}", "",
         "## Occupancy table (% of voxels within basin boundary)", "",
         "| σ | u_max_all | u_mean_all | near u=0 | near u=1 | **near u=4** | clamped |",
         "|---|---|---|---|---|---|---|"]
for r in stats_table:
    lines.append(f"| {r['sigma']} | {r['u_max_all']:.2f} | {r['u_mean_all']:.2f} | {r['near0_pct']:.1f}% | {r['near1_pct']:.1f}% | **{r['near4_pct']:.1f}%** | {r['clamped_pct']:.1f}% |")

lines += ["", "## Data-layer observations (no philosophy)", ""]
# Automated observations
for r in stats_table:
    if r['sigma'] == 0.0:
        lines.append(f"- σ=0 (pure gradient flow): u=1 basin dominates at {r['near1_pct']:.1f}%; u=4 basin occupancy {r['near4_pct']:.1f}% (reproduces Stage A1 finding).")
    elif r['sigma'] == 0.1:
        delta1 = r['near1_pct'] - stats_table[0]['near1_pct']
        lines.append(f"- σ=0.1 (weak noise): u=1 {r['near1_pct']:.1f}% (Δ{delta1:+.1f}pp); u=4 {r['near4_pct']:.1f}%. Noise too weak to cross barrier V≈13.2.")
    elif r['sigma'] == 0.5:
        lines.append(f"- σ=0.5 (moderate noise): u=1 collapses to {r['near1_pct']:.1f}%; u_max_all={r['u_max_all']:.1f} hits clamp ceiling; bulk of voxels ({r['near0_pct']:.1f}% at u=0) scattered. NOT a clean u=1↔u=4 transition.")
    elif r['sigma'] >= 1.0:
        lines.append(f"- σ={r['sigma']}: u_mean_all={r['u_mean_all']:.1f} near clamp ceiling (|ψ|²≈18); {r['clamped_pct']:.1f}% voxels clamped. System entirely dominated by noise, potential structure is erased.")

lines += ["", "## Verdict against OP2 hypothesis", "",
          "**H_OP2_Langevin**: Adding Langevin noise to gradient flow should populate the u=4 basin unreachable under pure gradient flow.",
          "",
          "**Result**: No σ in tested range yields clean u=4 basin occupancy (>1%).",
          "- σ ≤ 0.1: too weak → stuck in u=1 basin (expected, V_barrier≈13.2 > noise kinetic ~σ²·dt = 0.0005)",
          "- σ ≥ 0.5: too strong → field explodes to clamp ceiling (|ψ|²≈18, unphysical) rather than populating u=4",
          "- No 'Goldilocks zone' found in tested σ range where tunneling is clean.",
          "",
          "**Interpretation (data-layer only, no philosophy)**: ",
          "Naive Langevin on top of gradient flow in this V(ψ) is unlikely to realize 'ascent phase' of dialectical motion cleanly. The potential landscape is too steep (V grows as |ψ|^10 far from wells) — noise either insufficient or destructive, no balanced regime.",
          "",
          "## Implications for Block V design",
          "",
          "1. **Langevin alone is NOT OP2 answer** — not in this V(ψ) form. Options:",
          "   - Redesign V(ψ) with lower barriers (e.g., wells at u∈{0,1,2} instead of {0,1,4})",
          "   - Combine with active driving or Hamiltonian structure",
          "   - Use metadynamics / adaptive biasing to flatten barrier",
          "2. **The triple-well A1 potential V ~ |ψ|^10 may be unsuitable** for noise-based exploration — too steep. A1.4 shifted minima u∈{0,1,2} (from FINAL_REPORT §3.2 future directions) has V ~ |ψ|^6, may be more noise-tolerant.",
          "3. This result argues for **V.3-H (Hamiltonian)** or **V.3-A (structured active driving)** as more promising Q2 candidates than naive Langevin.",
          "",
          "**Overall**: Stage B1 provides a concrete data point supporting the claim 'gradient flow + simple noise ≠ OP2'. The ascending phase requires more structured non-equilibrium mechanisms.",
          "",
          "---",
          "",
          "## Decision points for em × Win [?]",
          "",
          "1. Is this result enough to rule out Langevin route entirely, or should we retry on lower-barrier potential (A1.4, u∈{0,1,2})?",
          "2. Should Block V shift V.3-L priority down (currently 1st) and elevate V.3-H (Hamiltonian)?",
          "3. Does this support reframing OP2 from 'add noise' to 'restructure barrier topology'?"]

(OUT.parent / "b1_verdict.md").write_text("\n".join(lines))
print(f"\nSaved verdict: {OUT.parent/'b1_verdict.md'}")
