#!/usr/bin/env python3
"""A2 诊断: rho/theta field 统计 + variance 对比 Gaussian equipartition 预测.

目的: 理解为何 S_rho fit 给 m_rho^2 ≈ 0.1, 远小于 V''_radial = 4.

Gaussian equipartition 预测 (若 eta 是 unit white noise, T=1, D=0.1):
  <|d_rho|^2(k)> = T / (D k^2 + m_rho^2)
  在 steady state, rho variance = (1/V) sum_k T/(D k^2 + m^2)
  但 Phase B Exp 1 是 deterministic (no noise), steady state 不由 T 决定.
  因此 A 不等于 T, 而由 driving strength 决定.

关键: m^2 的相对大小是可靠的 inverse-correlation-length; 绝对值受 A 影响但 A 独立 fit.
Spectral relation: S(k) = A/(D k^2 + m^2) → m^2 = D k_cross^2 where S(k_cross) = A/(2m^2).
即 k_cross = 1/correlation length × sqrt(D).

诊断: 先看 rho field 的 mean, std, dist; 看是否已经 steady state (可由 Phase B appendix dS/dt~10^-6 推断).
"""
import json
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.fft import fftn, fftfreq

G = 32
N = G * G * G
D_PDE = 0.1
v = 1.0

DATA = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/phase_b_exp1/day2/exp")
OUT = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/ACTION2_figures")
OUT.mkdir(exist_ok=True, parents=True)

meta = json.loads((DATA / "meta_exp.json").read_text())
n_docs = meta["n_docs"]
data = np.fromfile(DATA / "states_exp.bin", dtype=np.float32).reshape(n_docs, 2, N)

print("="*78)
print("诊断: rho, theta fields 统计")
print("="*78)
print()

# Per doc stats
rho_means = []
rho_stds = []
psi_abs_means = []
theta_stds = []  # circular std
for d in range(n_docs):
    a = data[d, 0].reshape(G, G, G).astype(np.float64)
    b = data[d, 1].reshape(G, G, G).astype(np.float64)
    psi = a + 1j * b
    rho = np.abs(psi)
    theta = np.angle(psi)
    rho_means.append(rho.mean())
    rho_stds.append(rho.std())
    psi_abs_means.append(psi.mean().real)  # real part of mean psi, 表 order parameter
    # circular std via complex mean
    mean_c = np.cos(theta).mean()
    mean_s = np.sin(theta).mean()
    R_order = np.sqrt(mean_c**2 + mean_s**2)  # circular concentration
    theta_stds.append(np.sqrt(-2 * np.log(R_order)) if R_order > 0 else np.pi)

rho_means = np.array(rho_means)
rho_stds = np.array(rho_stds)
theta_stds = np.array(theta_stds)

print(f"rho field (|psi|):")
print(f"  <rho>_x per doc: mean over docs = {rho_means.mean():.4f}, std = {rho_means.std():.4f}")
print(f"  std(rho)_x per doc: mean over docs = {rho_stds.mean():.4f}, std = {rho_stds.std():.4f}")
print(f"  (预期 if at v=1 with small fluctuation: <rho>≈1, std << 1)")
print(f"  (实际 Mexican-hat 最小 at |psi|=v=1, 但 rho 不必 = 1, 可 = 0 if 在原点附近)")
print()
print(f"theta field (angle psi):")
print(f"  circular std per doc: mean = {theta_stds.mean():.4f}, std = {theta_stds.std():.4f}")
print(f"  (0 = 完全 aligned, π/sqrt(3)≈1.81 = uniform)")
print()

# 看一个 doc 的分布
d0 = 0
a0 = data[d0, 0].reshape(G, G, G).astype(np.float64)
b0 = data[d0, 1].reshape(G, G, G).astype(np.float64)
psi0 = a0 + 1j * b0
rho0 = np.abs(psi0)
theta0 = np.angle(psi0)

print(f"doc 0 详情:")
print(f"  rho: min={rho0.min():.4f}, max={rho0.max():.4f}, mean={rho0.mean():.4f}, std={rho0.std():.4f}")
print(f"  rho histogram分位: 5%={np.percentile(rho0, 5):.3f}, 50%={np.percentile(rho0, 50):.3f}, 95%={np.percentile(rho0, 95):.3f}")
print(f"  |psi|^2: min={(rho0**2).min():.4f}, mean={(rho0**2).mean():.4f}, max={(rho0**2).max():.4f}")
print(f"  ψ real 部分: mean={a0.mean():.4e}, std={a0.std():.4f}")
print(f"  ψ imag 部分: mean={b0.mean():.4e}, std={b0.std():.4f}")
print()

# --- 诊断: 分离 radial vs angular via projection onto <psi> direction ---
# 若 <psi> 非零 (U(1) 破缺), 则 radial = psi · exp(-i arg <psi>) 的 real part
# angular = psi · exp(-i arg <psi>) 的 imag part
psi_mean = psi0.mean()
print(f"  <psi>_x = {psi_mean:.4e}, |<psi>|={abs(psi_mean):.4f}, arg<psi>={np.angle(psi_mean):.4f}")
psi_rot = psi0 * np.exp(-1j * np.angle(psi_mean))  # rotate so <psi> is on real axis
delta_radial = psi_rot.real - psi_rot.real.mean()
delta_angular = psi_rot.imag - psi_rot.imag.mean()
print(f"  δ_radial (ψ在 <ψ>方向): std={delta_radial.std():.4f}")
print(f"  δ_angular (ψ在 <ψ>⊥方向): std={delta_angular.std():.4f}")
print(f"  angular / radial variance ratio: {delta_angular.var()/delta_radial.var():.2f}")
print()

# --- 用新方式算 S_theta, S_radial ---
# 对所有 docs 重跑, 但这次 delta_angular 用 projection on <psi>⊥ 方向
# 与 analyze_O1.py 的 (cos θ - <cos θ>, sin θ - <sin θ>) 不同. 但小 fluctuation 下
# 等价 (两者差别在 rho 的变化).
print("重算 S_theta 用 orthogonal projection (应 equivalent 到 rho·δθ 小 fluct limit):")

def radial_bin(power_3d, G):
    kx = fftfreq(G, d=1.0) * 2*np.pi
    KX, KY, KZ = np.meshgrid(kx, kx, kx, indexing='ij')
    K = np.sqrt(KX**2 + KY**2 + KZ**2)
    dk = 2*np.pi / G
    n_bins = G // 2
    edges = np.arange(n_bins + 1) * dk
    S = np.zeros(n_bins); counts = np.zeros(n_bins)
    for i in range(n_bins):
        m = (K >= edges[i]) & (K < edges[i+1])
        if m.sum() > 0:
            S[i] = power_3d[m].mean(); counts[i] = m.sum()
    return 0.5*(edges[:-1]+edges[1:]), S, counts

S_rad_accum = None
S_ang_accum = None
for d in range(n_docs):
    a = data[d, 0].reshape(G, G, G).astype(np.float64)
    b = data[d, 1].reshape(G, G, G).astype(np.float64)
    psi = a + 1j * b
    pm = psi.mean()
    psi_rot = psi * np.exp(-1j * np.angle(pm))
    dr = psi_rot.real - psi_rot.real.mean()
    da = psi_rot.imag - psi_rot.imag.mean()
    P_r = np.abs(fftn(dr))**2
    P_a = np.abs(fftn(da))**2
    kc, S_r, _ = radial_bin(P_r, G)
    _, S_a, _ = radial_bin(P_a, G)
    if S_rad_accum is None:
        S_rad_accum = S_r; S_ang_accum = S_a; k_c = kc
    else:
        S_rad_accum += S_r; S_ang_accum += S_a
S_rad = S_rad_accum / n_docs
S_ang = S_ang_accum / n_docs

print(f"\nk_center     S_radial(k)        S_angular(k)     ratio_ang/rad")
for i in range(min(10, len(k_c))):
    ratio = S_ang[i]/S_rad[i] if S_rad[i] > 0 else np.nan
    print(f"  {k_c[i]:.4f}   {S_rad[i]:.4e}   {S_ang[i]:.4e}   {ratio:.2f}")
print()

# fit both
from scipy.optimize import curve_fit
def model(k, A, m2):
    return A / (D_PDE * k**2 + m2)

for label, S_k in [("radial (on-axis)", S_rad), ("angular (off-axis)", S_ang)]:
    for k_max in [4, 6, 8]:
        k_fit = k_c[1:k_max+1]; S_fit = S_k[1:k_max+1]
        try:
            popt, pcov = curve_fit(model, k_fit, S_fit,
                                   p0=[S_fit[0]*(D_PDE*k_fit[0]**2+0.1), 0.1],
                                   bounds=([0,0],[np.inf,np.inf]))
            A, m2 = popt
            S_pred = model(k_fit, *popt)
            r2 = 1 - ((S_fit-S_pred)**2).sum() / ((S_fit-S_fit.mean())**2).sum()
            print(f"  [{label}, k_max={k_max}] m²={m2:.5f}, A={A:.3e}, R²={r2:.4f}")
        except Exception as e:
            print(f"  [{label}, k_max={k_max}] fit failed: {e}")
print()

# --- 诊断: 在不同 doc 上 m^2 是否稳定 ---
print("-"*78)
print("per-doc m_theta^2 distribution (用 analyze_O1 的 tangent-plane 法, k_max=6)")
print("-"*78)
m2_thetas = []
m2_rhos = []
for d in range(n_docs):
    a = data[d, 0].reshape(G, G, G).astype(np.float64)
    b = data[d, 1].reshape(G, G, G).astype(np.float64)
    psi = a + 1j*b
    rho = np.abs(psi); theta = np.angle(psi)
    dc = np.cos(theta) - np.cos(theta).mean()
    ds = np.sin(theta) - np.sin(theta).mean()
    dr = rho - rho.mean()
    P_th = np.abs(fftn(dc))**2 + np.abs(fftn(ds))**2
    P_rh = np.abs(fftn(dr))**2
    _, S_th, _ = radial_bin(P_th, G)
    _, S_rh, _ = radial_bin(P_rh, G)
    try:
        popt, _ = curve_fit(model, k_c[1:7], S_th[1:7],
                           p0=[S_th[1]*(D_PDE*k_c[1]**2+0.1), 0.1],
                           bounds=([0,0],[np.inf,np.inf]))
        m2_thetas.append(popt[1])
    except: m2_thetas.append(np.nan)
    try:
        popt, _ = curve_fit(model, k_c[1:7], S_rh[1:7],
                           p0=[S_rh[1]*(D_PDE*k_c[1]**2+0.1), 0.1],
                           bounds=([0,0],[np.inf,np.inf]))
        m2_rhos.append(popt[1])
    except: m2_rhos.append(np.nan)

m2_thetas = np.array(m2_thetas)
m2_rhos = np.array(m2_rhos)
print(f"m_theta^2 per doc:  mean={np.nanmean(m2_thetas):.5f}, median={np.nanmedian(m2_thetas):.5f}")
print(f"                    std={np.nanstd(m2_thetas):.5f}, min={np.nanmin(m2_thetas):.5f}, max={np.nanmax(m2_thetas):.5f}")
print(f"                    5%={np.nanpercentile(m2_thetas,5):.5f}, 95%={np.nanpercentile(m2_thetas,95):.5f}")
print()
print(f"m_rho^2 per doc:    mean={np.nanmean(m2_rhos):.5f}, median={np.nanmedian(m2_rhos):.5f}")
print(f"                    std={np.nanstd(m2_rhos):.5f}, min={np.nanmin(m2_rhos):.5f}, max={np.nanmax(m2_rhos):.5f}")
print(f"                    5%={np.nanpercentile(m2_rhos,5):.5f}, 95%={np.nanpercentile(m2_rhos,95):.5f}")

# --- plot ---
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].hist(rho_means, bins=20, color='tab:orange', alpha=0.7)
axes[0].axvline(v, color='red', linestyle='--', label=f'v={v}')
axes[0].set_xlabel("<rho>_x per doc")
axes[0].set_title(f"<rho> distribution (v=1 expected)")
axes[0].legend()
axes[1].hist(m2_thetas[~np.isnan(m2_thetas)], bins=20, color='tab:blue', alpha=0.7)
axes[1].set_xlabel("m_theta^2 per doc")
axes[1].set_title(f"m_theta^2 dist, median={np.nanmedian(m2_thetas):.3f}")
axes[2].hist(m2_rhos[~np.isnan(m2_rhos)], bins=20, color='tab:green', alpha=0.7)
axes[2].axvline(4.0, color='red', linestyle='--', label='V"=4 expected')
axes[2].set_xlabel("m_rho^2 per doc")
axes[2].set_title(f"m_rho^2 dist, median={np.nanmedian(m2_rhos):.3f}")
axes[2].legend()
plt.tight_layout()
plt.savefig(OUT / "diagnose.png", dpi=120)
plt.close()
print(f"\nsaved: {OUT / 'diagnose.png'}")
