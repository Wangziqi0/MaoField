#!/usr/bin/env python3
"""Phase B Exp 1 — O3 analysis: kinematic self-similarity under block averaging.

Per O3 math review (REVIEW_PHASE_B_EXP1_math_O3.md interpretation C):
  - Three runs dt_inner ∈ {0.01, 0.1, 1.0} with t_sim=50 fixed
  - Compute two structure functions per run:
      S₂^{|ψ|²}(r) = ⟨(|ψ|²(x+r) − |ψ|²(x))²⟩
      C_ψ(r)       = Re⟨ψ*(x+r)·ψ(x)⟩        (two-point phase coherence)
  - Primary judgment: scaling collapse + log-log Pearson > 0.9
  - Secondary (Win original): Pearson corr between raw S₂(r) pairs > 0.7

LANGUAGE: kinematic self-similarity under block averaging, NOT RG fixed point.
"""
import json
import numpy as np
from pathlib import Path
from scipy.fft import fftn, ifftn

G = 32
N = G * G * G
DAY2 = Path("results/phase_b_exp1/day2")
RUNS = [
    ("dt001", "exp", "exp"),             # t_sim=50, dt=0.01, 5000 steps
    ("dt01",  "exp_dt0.1", "exp"),       # t_sim=50, dt=0.1,  500 steps
    ("dt10",  "exp_dt1.0", "exp"),       # t_sim=50, dt=1.0,  50 steps
]


def load_states(dir_name, mode_bin):
    path = DAY2 / dir_name / f"states_{mode_bin}.bin"
    meta = json.loads((DAY2 / dir_name / f"meta_{mode_bin}.json").read_text())
    n_docs = meta["n_docs"]
    data = np.fromfile(path, dtype=np.float32).reshape(n_docs, 2, N)
    fields = [(data[d, 0].reshape(G,G,G), data[d, 1].reshape(G,G,G)) for d in range(n_docs)]
    return fields, meta


def radial_pair_function_via_fft(f):
    """Given scalar field f on periodic G³ lattice, compute radially-binned
    two-point correlation C(r) = ⟨f(x)·f(x+r)⟩ − ⟨f⟩² via FFT Wiener-Khinchin.
    Returns (r_centers, C_r).
    """
    f_mean = f.mean()
    df = f - f_mean
    F = fftn(df)
    P = (F * np.conj(F)).real
    # Inverse FFT: 3D correlation
    C3d = ifftn(P).real / N  # autocorr at each lattice offset
    # radial binning
    ix, iy, iz = np.indices(f.shape)
    # minimum-image distance magnitudes for each lattice offset
    def mic(n, size):
        return np.where(n > size//2, n - size, n)
    dx = mic(ix, G); dy = mic(iy, G); dz = mic(iz, G)
    R = np.sqrt(dx*dx + dy*dy + dz*dz)
    n_bins = G // 2
    bin_edges = np.arange(n_bins + 1).astype(float)  # r bins: [0,1),[1,2),...,[G/2-1,G/2)
    C_r = np.zeros(n_bins)
    counts = np.zeros(n_bins)
    for i in range(n_bins):
        mask = (R >= bin_edges[i]) & (R < bin_edges[i+1])
        if mask.sum() > 0:
            C_r[i] = C3d[mask].mean()
            counts[i] = mask.sum()
    r_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    return r_centers, C_r


def structure_function_S2(f):
    """S₂(r) = ⟨(f(x+r) − f(x))²⟩ = 2·(⟨f²⟩ − C(r))"""
    r, C_r = radial_pair_function_via_fft(f)
    f2 = (f**2).mean()
    f_mean_sq = f.mean()**2
    # note C_r above is for df = f - ⟨f⟩, so C_df(r) = ⟨f(x+r)f(x)⟩ − ⟨f⟩²
    # thus S₂(r) = 2·(⟨f²⟩ − ⟨f⟩² − C_df(r)) + 0 = 2·(Var(f) − C_df(r))
    var_f = f2 - f_mean_sq
    S2 = 2.0 * (var_f - C_r)
    return r, S2, var_f


def phase_two_point(a, b):
    """C_ψ(r) = Re⟨ψ*(x+r)·ψ(x)⟩ = ⟨a(x+r)a(x)⟩ + ⟨b(x+r)b(x)⟩"""
    # equivalently: Σ real parts of both a, b autocorr (non-mean-subtracted)
    A = fftn(a); B = fftn(b)
    PA = (A * np.conj(A)).real; PB = (B * np.conj(B)).real
    CA = ifftn(PA).real / N; CB = ifftn(PB).real / N
    C3d = CA + CB
    ix, iy, iz = np.indices((G,G,G))
    def mic(n, size): return np.where(n > size//2, n - size, n)
    dx = mic(ix, G); dy = mic(iy, G); dz = mic(iz, G)
    R = np.sqrt(dx*dx + dy*dy + dz*dz)
    n_bins = G // 2
    bin_edges = np.arange(n_bins + 1).astype(float)
    Cr = np.zeros(n_bins); counts = np.zeros(n_bins)
    for i in range(n_bins):
        mask = (R >= bin_edges[i]) & (R < bin_edges[i+1])
        if mask.sum() > 0:
            Cr[i] = C3d[mask].mean()
    r = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    return r, Cr


def average_over_docs(fields, func_one):
    """Apply func_one to each (a, b) and average the returned arrays."""
    results = [func_one(a, b) for (a, b) in fields]
    # each result is (r, array) or ((r, array, var))
    # all have same r grid
    r = results[0][0]
    # stack arrays (skip last elt if it's var)
    arrays = np.stack([np.asarray(res[1]) for res in results])
    return r, arrays.mean(axis=0), arrays.std(axis=0)


def log_log_pearson(x, y, rmin=1.0, rmax=8.0):
    """Log-log Pearson correlation between x (r) and y (structure function) in [rmin, rmax]."""
    mask = (x >= rmin) & (x <= rmax) & (y > 0)
    if mask.sum() < 3:
        return float('nan')
    lx = np.log(x[mask]); ly = np.log(y[mask])
    cc = np.corrcoef(lx, ly)[0, 1]
    return float(cc)


def scaling_collapse_exponent(x, y, rmin=1.0, rmax=8.0):
    """Fit y ~ A · x^η in log-log, return (A, η, residual)."""
    mask = (x >= rmin) & (x <= rmax) & (y > 0)
    if mask.sum() < 3:
        return float('nan'), float('nan'), float('nan')
    lx = np.log(x[mask]); ly = np.log(y[mask])
    coef = np.polyfit(lx, ly, 1)
    eta = coef[0]; logA = coef[1]
    pred = coef[0]*lx + coef[1]
    resid = float(np.std(ly - pred))
    return float(np.exp(logA)), float(eta), resid


def main():
    print("=" * 96)
    print("Phase B Exp 1 — O3 Analysis: kinematic self-similarity (NOT RG fixed point)")
    print("=" * 96)
    print("Interpretation C (per math review): t_sim=50 fixed, dt_inner ∈ {0.01, 0.1, 1.0}")
    print()

    # amp² structure function (spatially: how rough is |ψ|² field)
    def S2_amp(a, b):
        m2 = a*a + b*b
        r, S2, var = structure_function_S2(m2)
        return r, S2

    # phase two-point (how coherent is ψ across lattice)
    def Cpsi(a, b):
        r, C = phase_two_point(a, b)
        return r, C

    per_run = {}
    for tag, dir_name, mode in RUNS:
        fields, meta = load_states(dir_name, mode)
        r_s2, S2_mean, S2_std = average_over_docs(fields, S2_amp)
        r_cp, Cp_mean, Cp_std = average_over_docs(fields, Cpsi)
        per_run[tag] = {
            "dt_inner": meta["dt_inner"],
            "n_docs": meta["n_docs"],
            "r": r_s2.tolist(),
            "S2_mean": S2_mean.tolist(),
            "C_psi_mean": Cp_mean.tolist(),
        }
        eta_S2 = scaling_collapse_exponent(r_s2, S2_mean, rmin=1.0, rmax=8.0)
        eta_Cp = scaling_collapse_exponent(r_cp, np.abs(Cp_mean - Cp_mean[-1]) + 1e-20, rmin=1.0, rmax=8.0)
        print(f"  {tag} (dt={meta['dt_inner']}): S₂^|ψ|²(r) scaling η={eta_S2[1]:.3f}  residual={eta_S2[2]:.3f}")
        print(f"           C_ψ-tail scaling    η={eta_Cp[1]:.3f}  residual={eta_Cp[2]:.3f}")
        per_run[tag]["S2_scaling_eta"] = eta_S2[1]
        per_run[tag]["Cpsi_tail_scaling_eta"] = eta_Cp[1]

    print()
    print("### Pairwise Pearson between structure functions (primary: log-log > 0.9; secondary Win: raw > 0.7)")
    tags = list(per_run.keys())
    pair_results = {}
    for i in range(len(tags)):
        for j in range(i+1, len(tags)):
            ti, tj = tags[i], tags[j]
            r = np.array(per_run[ti]["r"])
            yi = np.array(per_run[ti]["S2_mean"])
            yj = np.array(per_run[tj]["S2_mean"])
            raw_pearson = float(np.corrcoef(yi, yj)[0,1])
            # log-log in 1..8 range
            mask = (r >= 1.0) & (r <= 8.0) & (yi > 0) & (yj > 0)
            loglog = float(np.corrcoef(np.log(yi[mask]), np.log(yj[mask]))[0,1])
            key = f"{ti}_vs_{tj}"
            pair_results[key] = {"raw_pearson": raw_pearson, "loglog_pearson": loglog}
            print(f"  {ti} ↔ {tj}:  raw_Pearson={raw_pearson:.4f}  loglog_Pearson(r∈[1,8])={loglog:.4f}")

    # scaling collapse verdict: if η's agree across scales (|Δη|/η̄ < 15%) → kinematic self-similar
    eta_values = [per_run[t]["S2_scaling_eta"] for t in tags]
    eta_mean = np.mean(eta_values)
    eta_spread = (max(eta_values) - min(eta_values)) / (abs(eta_mean) + 1e-20)
    print()
    print(f"### Scaling collapse (η across 3 dt_inner):")
    for t, e in zip(tags, eta_values):
        print(f"  {t}: η_{{S₂^|ψ|²}}(r) = {e:.3f}")
    print(f"  mean η = {eta_mean:.3f}  |Δη|/η̄ = {eta_spread:.3f}  (Pass primary if < 0.15)")
    primary_pass = eta_spread < 0.15
    secondary_pass = all(v["raw_pearson"] > 0.7 for v in pair_results.values())
    loglog_pass = all(v["loglog_pearson"] > 0.9 for v in pair_results.values())
    print()
    print(f"### O3 Verdict:")
    print(f"  Primary (scaling collapse |Δη|/η̄ < 15%):   {'PASS' if primary_pass else 'FAIL'}")
    print(f"  Log-log Pearson > 0.9 all pairs:           {'PASS' if loglog_pass else 'FAIL'}")
    print(f"  Secondary (Win raw Pearson > 0.7 all pairs): {'PASS' if secondary_pass else 'FAIL'}")
    combined = primary_pass and loglog_pass
    print(f"  Combined O3 (primary + log-log): {'PASS' if combined else 'FAIL'}  (per math-review principled 判据)")

    out = {
        "interpretation": "C (fix t_sim=50, vary dt_inner)",
        "runs": per_run,
        "pair_pearsons": pair_results,
        "verdict": {
            "scaling_collapse_eta_mean": eta_mean,
            "scaling_collapse_eta_spread": eta_spread,
            "primary_pass": primary_pass,
            "loglog_pass": loglog_pass,
            "secondary_pass": secondary_pass,
            "combined": combined,
        },
    }
    Path("results/phase_b_exp1/day2/o3_analysis.json").write_text(json.dumps(out, indent=2, default=lambda o: bool(o) if hasattr(o, '__bool__') else str(o)))
    print("\nwrote results/phase_b_exp1/day2/o3_analysis.json")


if __name__ == "__main__":
    main()
