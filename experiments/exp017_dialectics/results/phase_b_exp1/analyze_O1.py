#!/usr/bin/env python3
"""Phase B Exp 1 — O1 analysis: localized coherent structures + Goldstone indicator.

Per O1 math review (REVIEW_PHASE_B_EXP1_math_O1.md):
  Algorithm A: phase-coherence connected components
  Algorithm B: polar-decomp structure factors S_ρ(k), S_θ(k)
  Pass iff (A: N_struct≥3 with r_g<8) AND (B: R=S_θ/S_ρ > 5 at low k AND α_θ > 1.0)
"""
import json
import numpy as np
from pathlib import Path
from scipy import ndimage
from scipy.fft import fftn, fftfreq

G = 32
N = G * G * G
DAY2 = Path("results/phase_b_exp1/day2")
MODES = ["exp", "null", "control_const", "control_whiten", "control_single"]


def load_state(mode):
    """Read states_{mode}.bin → list of (a, b) arrays per doc."""
    path = DAY2 / mode / f"states_{mode}.bin"
    meta = json.loads((DAY2 / mode / f"meta_{mode}.json").read_text())
    n_docs = meta["n_docs"]
    data = np.fromfile(path, dtype=np.float32)
    assert data.size == n_docs * 2 * N
    data = data.reshape(n_docs, 2, N)
    fields = []
    for d in range(n_docs):
        a = data[d, 0].reshape(G, G, G)
        b = data[d, 1].reshape(G, G, G)
        fields.append((a, b))
    return fields, meta["doc_ids"]


# ==========================================================================
# Algorithm A: connected-component labeling on phase coherence
# ==========================================================================
def local_phase_coherence(a, b):
    """C(x) = |(1/27) Σ_{y∈N(x)} exp(i·θ(y))|, θ = atan2(b, a)
       Uses a 3x3x3 box filter on (cos θ, sin θ), periodic BC.
    """
    # theta
    ca = a / np.sqrt(a*a + b*b + 1e-20)  # cos θ
    sa = b / np.sqrt(a*a + b*b + 1e-20)  # sin θ
    kernel = np.ones((3,3,3), dtype=np.float32) / 27.0
    # periodic BC via scipy.ndimage.convolve(mode='wrap')
    ca_bar = ndimage.convolve(ca, kernel, mode='wrap')
    sa_bar = ndimage.convolve(sa, kernel, mode='wrap')
    return np.sqrt(ca_bar*ca_bar + sa_bar*sa_bar)


def count_localized_structures(a, b, r_g_max=8.0, min_size=3):
    C = local_phase_coherence(a, b)
    T = C.mean() + 1.0 * C.std()
    mask = C > T
    labels, n_lab = ndimage.label(mask, structure=np.ones((3,3,3)))
    n_struct_valid = 0
    sizes = []
    r_gs = []
    for lbl in range(1, n_lab + 1):
        idx = np.argwhere(labels == lbl)
        if idx.shape[0] < min_size:
            continue
        # gyration radius in periodic box: use minimum-image convention via
        # complex phase for coordinates (avoids PBC wrap issues)
        com_coords = []
        for dim in range(3):
            angles = idx[:, dim] * (2*np.pi / G)
            mean_c = np.cos(angles).mean()
            mean_s = np.sin(angles).mean()
            com_angle = np.arctan2(mean_s, mean_c)
            com_coords.append(com_angle)
        # distances from com with PBC
        dists_sq = np.zeros(idx.shape[0])
        for dim in range(3):
            ang = idx[:, dim] * (2*np.pi / G)
            diff = np.arctan2(np.sin(ang - com_coords[dim]), np.cos(ang - com_coords[dim]))
            # convert back to voxel units
            dists_sq += (diff * G / (2*np.pi))**2
        r_g = np.sqrt(dists_sq.mean())
        sizes.append(idx.shape[0])
        r_gs.append(r_g)
        if r_g < r_g_max:
            n_struct_valid += 1
    return {
        "n_struct_valid": n_struct_valid,
        "n_components_all": n_lab,
        "threshold_C": float(T),
        "C_mean": float(C.mean()),
        "C_std": float(C.std()),
        "component_sizes": sizes,
        "component_rgs": [float(r) for r in r_gs],
    }


# ==========================================================================
# Algorithm B: polar decomposition + radial structure factors
# ==========================================================================
def goldstone_indicator(a, b):
    """Returns S_θ(k), S_ρ(k) radial-binned + low-k ratio + α slopes."""
    psi = a + 1j * b
    rho = np.abs(psi)
    theta = np.angle(psi)
    # Project onto tangent at ⟨ψ⟩: use cos θ, sin θ minus means
    cos_th = np.cos(theta)
    sin_th = np.sin(theta)
    d_rho = rho - rho.mean()
    d_c = cos_th - cos_th.mean()
    d_s = sin_th - sin_th.mean()
    # 3D FFT (no normalization; we only care about ratios)
    R = fftn(d_rho)
    C = fftn(d_c)
    S = fftn(d_s)
    P_rho = np.abs(R)**2
    P_theta = np.abs(C)**2 + np.abs(S)**2
    # Radial binning
    kx = fftfreq(G, d=1.0) * 2*np.pi
    ky = fftfreq(G, d=1.0) * 2*np.pi
    kz = fftfreq(G, d=1.0) * 2*np.pi
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing='ij')
    K = np.sqrt(KX*KX + KY*KY + KZ*KZ)
    # bins: 0, 2π/32, 2·2π/32, ..., up to π
    dk = 2*np.pi / G
    n_bins = G // 2
    bin_edges = np.arange(n_bins + 1) * dk
    S_rho_k = np.zeros(n_bins)
    S_theta_k = np.zeros(n_bins)
    counts = np.zeros(n_bins)
    for i in range(n_bins):
        mask = (K >= bin_edges[i]) & (K < bin_edges[i+1])
        if mask.sum() > 0:
            S_rho_k[i] = P_rho[mask].mean()
            S_theta_k[i] = P_theta[mask].mean()
            counts[i] = mask.sum()
    k_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    # low-k ratio (skip k=0 bin which contains DC only)
    # k_min index is 1 (first non-zero bin)
    k_idx_low = slice(1, 5)
    # ratio at k_min
    R_at_kmin = S_theta_k[1] / (S_rho_k[1] + 1e-20)
    # log-log slopes on low-k
    logk = np.log(k_centers[k_idx_low] + 1e-20)
    with np.errstate(invalid='ignore'):
        alpha_rho = -np.polyfit(logk, np.log(S_rho_k[k_idx_low] + 1e-20), 1)[0]
        alpha_theta = -np.polyfit(logk, np.log(S_theta_k[k_idx_low] + 1e-20), 1)[0]
    return {
        "k_centers": k_centers.tolist(),
        "S_rho_k": S_rho_k.tolist(),
        "S_theta_k": S_theta_k.tolist(),
        "R_at_kmin": float(R_at_kmin),
        "alpha_rho_lowk": float(alpha_rho),
        "alpha_theta_lowk": float(alpha_theta),
    }


def main():
    print("=" * 96)
    print("Phase B Exp 1 — Day 2 O1 Analysis (localized structures + Goldstone indicator)")
    print("=" * 96)
    print()
    all_results = {}
    for mode in MODES:
        fields, doc_ids = load_state(mode)
        # aggregate over docs
        n_structs = []
        R_ratios = []
        alpha_ths = []
        alpha_rhos = []
        per_doc_records = []
        for (a, b), did in zip(fields, doc_ids):
            A = count_localized_structures(a, b)
            B = goldstone_indicator(a, b)
            n_structs.append(A["n_struct_valid"])
            R_ratios.append(B["R_at_kmin"])
            alpha_ths.append(B["alpha_theta_lowk"])
            alpha_rhos.append(B["alpha_rho_lowk"])
            per_doc_records.append({"doc_id": did, "A": A, "B_ratio_kmin": B["R_at_kmin"],
                                    "B_alpha_theta": B["alpha_theta_lowk"],
                                    "B_alpha_rho": B["alpha_rho_lowk"]})
        ns = np.array(n_structs, dtype=float)
        R = np.array(R_ratios, dtype=float)
        ath = np.array(alpha_ths, dtype=float)
        arh = np.array(alpha_rhos, dtype=float)
        # Pass evaluations per doc
        pass_A = ns >= 3
        pass_B = (R > 5.0) & (ath > 1.0)
        pass_O1 = pass_A & pass_B

        print(f"### Mode: {mode}  ({len(ns)} docs)")
        print(f"  Algorithm A (phase-coherence components):")
        print(f"    n_struct_valid  mean={ns.mean():.2f}  median={np.median(ns):.1f}  max={ns.max():.0f}")
        print(f"    frac docs with N_struct≥3 (Pass A): {pass_A.mean()*100:.1f}%")
        print(f"  Algorithm B (Goldstone indicator):")
        print(f"    R = S_θ(k_min)/S_ρ(k_min):  mean={R.mean():.2f}  median={np.median(R):.2f}")
        print(f"    α_θ (low-k slope):          mean={ath.mean():.2f}")
        print(f"    α_ρ (low-k slope):          mean={arh.mean():.2f}")
        print(f"    Δα = α_θ − α_ρ:             mean={(ath-arh).mean():.2f}")
        print(f"    frac docs with Pass B (R>5 & α_θ>1.0): {pass_B.mean()*100:.1f}%")
        print(f"  ==> Combined O1 Pass frac: {pass_O1.mean()*100:.1f}%")
        print()
        all_results[mode] = {
            "n_docs": int(len(ns)),
            "A_stats": {"mean_n_struct": float(ns.mean()), "frac_pass_A": float(pass_A.mean())},
            "B_stats": {"mean_R_kmin": float(R.mean()), "mean_alpha_theta": float(ath.mean()),
                        "mean_alpha_rho": float(arh.mean()), "frac_pass_B": float(pass_B.mean())},
            "combined_pass_frac": float(pass_O1.mean()),
            "per_doc": per_doc_records[:5],  # first 5 only to keep file size sane
        }
    Path("results/phase_b_exp1/day2/o1_analysis.json").write_text(json.dumps(all_results, indent=2))
    print("wrote results/phase_b_exp1/day2/o1_analysis.json")


if __name__ == "__main__":
    main()
