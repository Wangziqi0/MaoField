#!/usr/bin/env python3
"""A2 Part 2 — extract pseudo-Goldstone mass m_theta^2 from Phase B Exp 1 exp mode.

Data: /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/phase_b_exp1/day2/exp/states_exp.bin
  layout per doc: [a f32 × 32768][b f32 × 32768], psi = a + i*b, 70 docs

Polar decomposition: psi(x) = rho(x) e^{i theta(x)}
  delta_theta(x) = theta(x) - <theta>_x  (但注意 circular mean)
  S_theta(k) from 3D FFT radial binning

Low-k fit model (equipartition + Gaussian field, overdamped稳态):
  S_theta(k) = T / (D k^2 + m_theta^2)

若 Goldstone 严格 massless → S_theta(k) ∝ 1/k^2 divergent at k→0
若 pseudo-Goldstone → saturates at T/m_theta^2

Sanity check: S_rho(k) 应给 m_radial^2 ~ 4 (Mexican hat curvature)

注意: theta 是 circular variable, 减去 <theta>_x 要用 circular mean 或
  改用 (cos theta, sin theta) 的 tangent space projection (与 analyze_O1.py 一致).
这里采用 analyze_O1.py 的方式: delta_c = cos θ - <cos θ>, delta_s = sin θ - <sin θ>,
S_theta(k) := |FFT(delta_c)|^2 + |FFT(delta_s)|^2.
这是 U(1) tangent plane 的 angular fluctuation power; 在小 fluctuation limit
等价于 |FFT(delta_theta)|^2 (至 rho^2 因子 — 但 rho 在 Mexican hat 基本均匀 ≈ 1).
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.fft import fftn, fftfreq
from scipy.optimize import curve_fit

G = 32
N = G * G * G
D_PDE = 0.1   # 与 engine 参数一致

DATA_DIR = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/phase_b_exp1/day2/exp")
OUT = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/ACTION2_figures")
OUT.mkdir(parents=True, exist_ok=True)

print("="*78)
print("A2 M3 V_0 empirical verify — Part 2: m_theta^2 from Exp 1 data")
print("="*78)
print()

# --- Load data ---
meta = json.loads((DATA_DIR / "meta_exp.json").read_text())
n_docs = meta["n_docs"]
data = np.fromfile(DATA_DIR / "states_exp.bin", dtype=np.float32)
assert data.size == n_docs * 2 * N, f"expected {n_docs*2*N}, got {data.size}"
data = data.reshape(n_docs, 2, N)
print(f"loaded {n_docs} docs, grid {G}^3 = {N} voxels")
print(f"meta: mode={meta['mode']}, t_sim={meta['n_inner_steps']*meta['dt_inner']:.1f}, "
      f"multi_scale={meta['multi_scale']}, params α={meta['params']['alpha']}, β={meta['params']['beta']}")
print()

# --- Radial bin setup ---
def radial_bin(power_3d, G):
    kx = fftfreq(G, d=1.0) * 2*np.pi
    KX, KY, KZ = np.meshgrid(kx, kx, kx, indexing='ij')
    K = np.sqrt(KX**2 + KY**2 + KZ**2)
    dk = 2*np.pi / G
    n_bins = G // 2
    edges = np.arange(n_bins + 1) * dk
    S = np.zeros(n_bins)
    counts = np.zeros(n_bins)
    for i in range(n_bins):
        mask = (K >= edges[i]) & (K < edges[i+1])
        if mask.sum() > 0:
            S[i] = power_3d[mask].mean()
            counts[i] = mask.sum()
    centers = 0.5 * (edges[:-1] + edges[1:])
    return centers, S, counts

# --- Polar decomposition + spectra per doc, then average ---
S_theta_accum = None
S_rho_accum = None
n_valid = 0
for d in range(n_docs):
    a = data[d, 0].reshape(G, G, G).astype(np.float64)
    b = data[d, 1].reshape(G, G, G).astype(np.float64)
    psi = a + 1j * b
    rho = np.abs(psi)
    theta = np.angle(psi)
    # angular fluctuation via tangent space (cos θ, sin θ mean-subtracted)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    d_c = cos_t - cos_t.mean()
    d_s = sin_t - sin_t.mean()
    d_rho = rho - rho.mean()
    # 3D FFT
    Fc = fftn(d_c)
    Fs = fftn(d_s)
    Fr = fftn(d_rho)
    P_theta = np.abs(Fc)**2 + np.abs(Fs)**2
    P_rho   = np.abs(Fr)**2
    # radial bin
    k_c, S_th, cnt = radial_bin(P_theta, G)
    _, S_rh, _ = radial_bin(P_rho, G)
    if S_theta_accum is None:
        S_theta_accum = S_th
        S_rho_accum = S_rh
        k_centers = k_c
        counts = cnt
    else:
        S_theta_accum += S_th
        S_rho_accum += S_rh
    n_valid += 1

S_theta = S_theta_accum / n_valid
S_rho = S_rho_accum / n_valid
print(f"averaged over {n_valid} docs")
print()
print(f"k_centers = {np.array2string(k_centers, precision=4, max_line_width=120)}")
print()

# S_theta[0] 是 DC bin (k=0), 已被 mean-subtract 掉, should be ≈ 0
print(f"S_theta[k=0] (DC bin) = {S_theta[0]:.6e}  (应 ≈ 0, 因 mean-subtracted)")
print(f"S_rho[k=0]   (DC bin) = {S_rho[0]:.6e}  (应 ≈ 0, 因 mean-subtracted)")
print()
print("bin#  k_center       S_theta(k)         S_rho(k)          count")
for i in range(min(10, len(k_centers))):
    print(f"  {i:2d}   {k_centers[i]:.5f}   {S_theta[i]:.5e}   {S_rho[i]:.5e}   {int(counts[i]):4d}")
print()

# --- Low-k fit to S(k) = A / (D k^2 + m^2) ---
# 等价于 1/S(k) = (D/A) k^2 + (m^2/A)
# linear fit on 1/S vs k^2 → slope = D/A, intercept = m^2/A
# → m^2 = D * intercept / slope

def fit_mass(S_k, k_centers, k_fit_max_idx, D_val, label):
    # skip k=0 bin (DC)
    k_fit = k_centers[1:k_fit_max_idx+1]
    S_fit = S_k[1:k_fit_max_idx+1]
    # nonlinear fit S(k) = A/(D k^2 + m^2)
    def model(k, A, m2):
        return A / (D_val * k**2 + m2)
    try:
        # initial guess: A ~ S_fit[0] * (D k0^2 + 1), m2 ~ D k_min^2
        A0 = S_fit[0] * (D_val * k_fit[0]**2 + 0.1)
        p0 = [A0, 0.1]
        popt, pcov = curve_fit(model, k_fit, S_fit, p0=p0,
                               bounds=([0, 0], [np.inf, np.inf]))
        A_fit, m2_fit = popt
        S_pred = model(k_fit, *popt)
        ss_res = np.sum((S_fit - S_pred)**2)
        ss_tot = np.sum((S_fit - S_fit.mean())**2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
        # chi^2 per dof
        chi2 = ss_res / (len(k_fit) - 2)
        # perr
        perr = np.sqrt(np.diag(pcov)) if pcov is not None else [np.nan, np.nan]
        print(f"  [{label}] nonlinear fit S(k) = A/(D k² + m²), low-k bins 1..{k_fit_max_idx}")
        print(f"    A = {A_fit:.5e} ± {perr[0]:.3e}")
        print(f"    m² = {m2_fit:.5f} ± {perr[1]:.5f}")
        print(f"    R² = {r2:.5f}, chi²/dof = {chi2:.3e}")
    except Exception as e:
        print(f"  [{label}] fit failed: {e}")
        return None, None, None
    # Also report linear fit 1/S vs k^2 as sanity
    x = k_fit**2
    y = 1.0 / S_fit
    slope, intercept = np.polyfit(x, y, 1)
    if slope > 0:
        m2_lin = D_val * intercept / slope
        A_lin = D_val / slope
        print(f"    linear sanity: 1/S = ({slope:.4e}) k² + ({intercept:.4e})")
        print(f"    → A_lin = {A_lin:.4e}, m²_lin = {m2_lin:.5f}")
    return A_fit, m2_fit, r2

# --- S_theta fit ---
print("-"*78)
print("S_theta(k) low-k fit")
print("-"*78)
A_th_4, m2_th_4, r2_th_4 = fit_mass(S_theta, k_centers, k_fit_max_idx=4, D_val=D_PDE, label="S_theta, k_max=4")
print()
A_th_6, m2_th_6, r2_th_6 = fit_mass(S_theta, k_centers, k_fit_max_idx=6, D_val=D_PDE, label="S_theta, k_max=6")
print()
A_th_8, m2_th_8, r2_th_8 = fit_mass(S_theta, k_centers, k_fit_max_idx=8, D_val=D_PDE, label="S_theta, k_max=8")
print()

# --- S_rho fit (sanity check, expect m^2 ~ 4) ---
print("-"*78)
print("S_rho(k) low-k fit (sanity check, expected m² ~ 4)")
print("-"*78)
A_rh_4, m2_rh_4, r2_rh_4 = fit_mass(S_rho, k_centers, k_fit_max_idx=4, D_val=D_PDE, label="S_rho, k_max=4")
print()
A_rh_6, m2_rh_6, r2_rh_6 = fit_mass(S_rho, k_centers, k_fit_max_idx=6, D_val=D_PDE, label="S_rho, k_max=6")
print()
A_rh_8, m2_rh_8, r2_rh_8 = fit_mass(S_rho, k_centers, k_fit_max_idx=8, D_val=D_PDE, label="S_rho, k_max=8")
print()

# --- Plot S_theta, S_rho vs k ---
fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))

ax = axes[0]
ax.loglog(k_centers[1:], S_theta[1:], 'o-', color='tab:blue', label='S_θ(k)', markersize=6)
ax.loglog(k_centers[1:], S_rho[1:], 's-', color='tab:orange', label='S_ρ(k)', markersize=6)
ax.set_xlabel("k")
ax.set_ylabel("S(k)")
ax.set_title("Angular / radial spectrum (Exp 1, 70 docs avg)")
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[1]
k_fit = k_centers[1:9]
S_th_fit = S_theta[1:9]
ax.plot(k_fit**2, 1.0/S_th_fit, 'o-', color='tab:blue', label='1/S_θ')
ax.plot(k_fit**2, 1.0/S_rho[1:9], 's-', color='tab:orange', label='1/S_ρ')
# fit lines
if m2_th_6 is not None:
    x = np.linspace(0, (k_fit.max())**2, 50)
    y_th = (D_PDE/A_th_6) * x + m2_th_6/A_th_6
    ax.plot(x, y_th, '--', color='tab:blue', alpha=0.7,
            label=f'fit: m²_θ={m2_th_6:.3f}')
if m2_rh_6 is not None:
    x = np.linspace(0, (k_fit.max())**2, 50)
    y_rh = (D_PDE/A_rh_6) * x + m2_rh_6/A_rh_6
    ax.plot(x, y_rh, '--', color='tab:orange', alpha=0.7,
            label=f'fit: m²_ρ={m2_rh_6:.3f}')
ax.set_xlabel("k²")
ax.set_ylabel("1/S(k)")
ax.set_title("Linearized fit: 1/S = (D/A) k² + m²/A")
ax.legend()
ax.grid(True, alpha=0.3)

ax = axes[2]
# direct S vs k with fit curves
if m2_th_6 is not None:
    ax.semilogy(k_fit, S_th_fit, 'o', color='tab:blue', markersize=8)
    k_fine = np.linspace(k_fit.min()*0.5, k_fit.max()*1.2, 100)
    ax.semilogy(k_fine, A_th_6/(D_PDE*k_fine**2 + m2_th_6), '-', color='tab:blue',
                label=f'S_θ fit m²={m2_th_6:.3f}')
if m2_rh_6 is not None:
    ax.semilogy(k_fit, S_rho[1:9], 's', color='tab:orange', markersize=8)
    ax.semilogy(k_fine, A_rh_6/(D_PDE*k_fine**2 + m2_rh_6), '-', color='tab:orange',
                label=f'S_ρ fit m²={m2_rh_6:.3f}')
ax.set_xlabel("k")
ax.set_ylabel("S(k) [log]")
ax.set_title("Low-k fit quality")
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUT / "mtheta_spectrum.png", dpi=120)
plt.close()
print(f"saved: {OUT / 'mtheta_spectrum.png'}")
print()

# --- Summary ---
print("="*78)
print("Summary:")
print(f"  m_theta^2 fits (k_max varies):")
print(f"    k_max=4: m_θ² = {m2_th_4:.5f}  (R²={r2_th_4:.4f})")
print(f"    k_max=6: m_θ² = {m2_th_6:.5f}  (R²={r2_th_6:.4f})")
print(f"    k_max=8: m_θ² = {m2_th_8:.5f}  (R²={r2_th_8:.4f})")
print(f"  m_rho^2 fits (sanity, expect ~4):")
print(f"    k_max=4: m_ρ² = {m2_rh_4:.5f}  (R²={r2_rh_4:.4f})")
print(f"    k_max=6: m_ρ² = {m2_rh_6:.5f}  (R²={r2_rh_6:.4f})")
print(f"    k_max=8: m_ρ² = {m2_rh_8:.5f}  (R²={r2_rh_8:.4f})")
print("="*78)

# --- save json ---
summary = {
    "n_docs": int(n_valid),
    "k_centers": k_centers.tolist(),
    "S_theta_avg": S_theta.tolist(),
    "S_rho_avg": S_rho.tolist(),
    "fits": {
        "m_theta_sq": {"k_max_4": float(m2_th_4) if m2_th_4 else None,
                       "k_max_6": float(m2_th_6) if m2_th_6 else None,
                       "k_max_8": float(m2_th_8) if m2_th_8 else None,
                       "R2": {"k_max_4": float(r2_th_4) if r2_th_4 else None,
                              "k_max_6": float(r2_th_6) if r2_th_6 else None,
                              "k_max_8": float(r2_th_8) if r2_th_8 else None}},
        "m_rho_sq": {"k_max_4": float(m2_rh_4) if m2_rh_4 else None,
                     "k_max_6": float(m2_rh_6) if m2_rh_6 else None,
                     "k_max_8": float(m2_rh_8) if m2_rh_8 else None,
                     "R2": {"k_max_4": float(r2_rh_4) if r2_rh_4 else None,
                            "k_max_6": float(r2_rh_6) if r2_rh_6 else None,
                            "k_max_8": float(r2_rh_8) if r2_rh_8 else None}},
    },
}
(OUT / "mtheta_extract_summary.json").write_text(json.dumps(summary, indent=2))
print(f"saved: {OUT / 'mtheta_extract_summary.json'}")
