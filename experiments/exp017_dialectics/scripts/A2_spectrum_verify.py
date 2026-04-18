#!/usr/bin/env python3
"""A2 M3 V₀ spectrum verify — Hermitian part of (L-F) on 32³ × N_hist, V₀ subspace.

Part 1 of Action 2 (Linux dispatch 2026-04-18).

按 A1 §3.2 template, 计算:
  - ||w||_1 (预期 ≈ 20.366)
  - ||F||_op bound (预期 ≈ 1.118)
  - causal Toeplitz K_H 谱 (是否 PSD 不 ensure)
  - F_H = alpha I + beta K_H 谱
  - (L-F)_H 谱 on V_0 for m_theta^2 ∈ {0.0, 0.5, 1.2, 2.0}

关键修正 (A1 §2): F 非自伴, 需用 Hermitian part F_H = (F + F*)/2.
关键修正 (A1 §3.1): L 在 V_0 上含 pseudo-Goldstone 软模 Dk^2 + m_theta^2.

Tensor product 理解:
  线性化算子 A := L ⊗ I_t - alpha I - beta K 作用于 L^2(V_0) ⊗ L^2([0,T]).
  A_H = L ⊗ I_t - alpha I - beta K_H.
  A 的空间-时间 spectrum 是 {λ_L + λ_t : λ_L ∈ σ(L on V_0), λ_t ∈ σ(-alpha I - beta K_H)}.
  最小 eigenvalue of A_H = λ_min(L on V_0) + λ_min(-alpha - beta K_H)
                       = λ_min(L on V_0) - alpha - beta * λ_max(K_H).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/ACTION2_figures")
OUT.mkdir(parents=True, exist_ok=True)

# --- 参数 (Phase B Exp 1 meta_exp.json) ---
G = 32
D = 0.1
v = 1.0
alpha = 0.1
beta = 0.05
lam = 0.05
dt_outer = 1.0
N_hist = 100

print("="*78)
print("A2 M3 V_0 spectrum verify — Part 1")
print("="*78)
print()
print(f"参数: G={G}, D={D}, v={v}, α={alpha}, β={beta}, λ={lam}, dt_outer={dt_outer}, N_hist={N_hist}")
print()

# --- w weights and ||w||_1 ---
w = np.exp(-lam * np.arange(N_hist) * dt_outer) * dt_outer
w_l1 = w.sum()
print(f"||w||_1 = sum_k e^(-λ k dt) dt = {w_l1:.6f}")
print(f"  (解析: (1-e^(-λ N dt)) / (1-e^(-λ dt)) * dt = "
      f"{(1-np.exp(-lam*N_hist*dt_outer))/(1-np.exp(-lam*dt_outer))*dt_outer:.6f})")
print()

# --- F op bound (causal Toeplitz ℓ^1 upper bound) ---
F_op_bound = alpha + beta * w_l1
print(f"||F||_op ≤ alpha + beta * ||w||_1 = {F_op_bound:.6f}")
print()

# --- 空间 Laplacian eigenvalues on 32^3 periodic lattice ---
def lap_eigs_3d(G):
    ks = np.arange(G)
    cos_k = np.cos(2*np.pi*ks/G)
    ex, ey, ez = np.meshgrid(2*(1-cos_k), 2*(1-cos_k), 2*(1-cos_k), indexing='ij')
    return (ex + ey + ez).flatten()

lap = lap_eigs_3d(G)       # ≥ 0, min nonzero = 2(1-cos(2π/32)) ≈ 0.01924
Dk2 = D * lap
# 剔除 k=0 (mean-subtracted V_0)
Dk2_V0 = Dk2.copy()
Dk2_V0[0] = np.inf
print(f"Dk^2 min (on V_0) = {Dk2_V0[Dk2_V0<np.inf].min():.6f}  (k_min=2π/32, D*2*(1-cos))")
print(f"Dk^2 max = {Dk2_V0.max():.6f}")
print()

# --- Build causal Toeplitz K (N_hist × N_hist) ---
K_mat = np.zeros((N_hist, N_hist))
for i in range(N_hist):
    for j in range(i+1):
        K_mat[i, j] = w[i-j]
K_H = 0.5 * (K_mat + K_mat.T)

eigs_KH = np.linalg.eigvalsh(K_H)
print(f"K_H (N_hist × N_hist = {N_hist}×{N_hist}) 谱:")
print(f"  λ_max(K_H) = {eigs_KH.max():.6f}")
print(f"  λ_min(K_H) = {eigs_KH.min():.6f}")
print(f"  K_H is PSD?  {'YES' if eigs_KH.min() >= -1e-10 else 'NO'}")
print(f"  K_H 负 eigenvalue 个数: {(eigs_KH < -1e-10).sum()} / {N_hist}")
print(f"  K_H 谱范围: [{eigs_KH.min():.4f}, {eigs_KH.max():.4f}]")
print()

F_H_max = alpha + beta * eigs_KH.max()
F_H_min = alpha + beta * eigs_KH.min()
print(f"F_H = α I + β K_H 谱:")
print(f"  λ_max(F_H) = {F_H_max:.6f}")
print(f"  λ_min(F_H) = {F_H_min:.6f}")
print(f"  ||F_H||_op = max(|λ_max|, |λ_min|) = {max(abs(F_H_max), abs(F_H_min)):.6f}")
print()

# --- (L-F)_H on V_0 for m_theta^2 options ---
# A_H tensor product: eigs(A_H) = {λ_L + (-F_H eig) : ...}
# λ_min(A_H) = λ_min(L on V_0) - λ_max(F_H)
# 最坏情况 (λ_max(F_H) 最大 + L 最小)
# Note: L 包含 radial (Dk^2 + 4) 和 angular (Dk^2 + m_theta^2) 两个 mode
L_radial = Dk2_V0 + 4.0
# angular 的 DC mode 也被投影掉 (V_0)
# 但 angular 非 DC mode 有 Dk^2 + m_theta^2 mass

m_theta_sq_options = [0.0, 0.5, 1.2, 2.0]
verdicts = {}
print("-"*78)
print(f"m_theta^2       L_radial_min    L_angular_min   λ_min(L on V_0)  λ_min((L-F)_H)  M3")
print("-"*78)
for m2 in m_theta_sq_options:
    L_angular = Dk2_V0 + m2  # V_0 投影掉 DC, 所以 min over k≠0
    L_rad_min = L_radial[L_radial < np.inf].min()
    L_ang_min = L_angular[L_angular < np.inf].min()
    L_min = min(L_rad_min, L_ang_min)
    # λ_min((L-F)_H on V_0 ⊗ time) = L_min - λ_max(F_H) (worst case, tensor product)
    LmF_min = L_min - F_H_max
    verdict = "PASS" if LmF_min > 0 else ("MARGINAL" if abs(LmF_min) < 0.01 else "FAIL")
    verdicts[m2] = (L_min, LmF_min, verdict)
    print(f"  {m2:.2f}         {L_rad_min:.6f}      {L_ang_min:.6f}      "
          f"{L_min:.6f}        {LmF_min:+.6f}       {verdict}")
print("-"*78)
print()

# --- histogram ---
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# K_H 谱
axes[0].hist(eigs_KH, bins=40, color='steelblue', edgecolor='k')
axes[0].axvline(0, color='red', linestyle='--', label='0')
axes[0].set_xlabel("eigenvalue")
axes[0].set_ylabel("count")
axes[0].set_title(f"K_H spectrum ({N_hist}×{N_hist})\nmin={eigs_KH.min():.3f} max={eigs_KH.max():.3f}")
axes[0].legend()

# L on V_0 (radial vs angular; plot for m_theta^2 = 1.2 as illustrative)
m2_plot = 1.2
L_angular_plot = Dk2_V0[Dk2_V0 < np.inf] + m2_plot
L_radial_plot = Dk2_V0[Dk2_V0 < np.inf] + 4.0
axes[1].hist(L_radial_plot, bins=40, alpha=0.5, label=f"radial (mass=4)", color='tab:orange')
axes[1].hist(L_angular_plot, bins=40, alpha=0.5, label=f"angular (m²={m2_plot})", color='tab:blue')
axes[1].axvline(F_H_max, color='red', linestyle='--', label=f"λ_max(F_H)={F_H_max:.3f}")
axes[1].set_xlabel("eigenvalue of L on V_0")
axes[1].set_ylabel("count")
axes[1].set_title(f"L spectrum (V_0, m_θ²={m2_plot})")
axes[1].legend()

# (L-F)_H worst case eigenvalue as function of m_theta^2
m2_scan = np.linspace(0, 3, 100)
LmF_min_scan = []
for m2 in m2_scan:
    L_ang_min = (Dk2_V0[Dk2_V0 < np.inf] + m2).min()
    L_rad_min = (Dk2_V0[Dk2_V0 < np.inf] + 4.0).min()
    L_min = min(L_rad_min, L_ang_min)
    LmF_min_scan.append(L_min - F_H_max)
LmF_min_scan = np.array(LmF_min_scan)
axes[2].plot(m2_scan, LmF_min_scan, '-', color='darkgreen', linewidth=2)
axes[2].axhline(0, color='red', linestyle='--')
axes[2].axvline(F_H_max, color='blue', linestyle=':', label=f'F_H_max={F_H_max:.3f}')
axes[2].fill_between(m2_scan, LmF_min_scan, 0, where=(LmF_min_scan > 0),
                     alpha=0.3, color='green', label='M3 PASS region')
axes[2].fill_between(m2_scan, LmF_min_scan, 0, where=(LmF_min_scan <= 0),
                     alpha=0.3, color='red', label='M3 FAIL region')
axes[2].set_xlabel("m_θ²")
axes[2].set_ylabel("λ_min((L-F)_H)")
axes[2].set_title("M3 verdict vs pseudo-Goldstone mass")
axes[2].legend()

plt.tight_layout()
plt.savefig(OUT / "spectrum_verify.png", dpi=120)
plt.close()
print(f"saved histogram: {OUT / 'spectrum_verify.png'}")
print()

# --- find critical m_theta^2 (threshold) ---
# λ_min((L-F)_H) > 0 要求 L_min > F_H_max
# L_min = min(Dk^2 + 4, Dk^2_min + m_theta^2) = min(4.00385, 0.00385 + m_theta^2)
# 要 0.00385 + m_theta^2 > F_H_max → m_theta^2 > F_H_max - 0.00385
Dk2_min = (Dk2_V0[Dk2_V0 < np.inf]).min()
m2_critical = F_H_max - Dk2_min
print(f"临界 m_θ²: m_θ² > {m2_critical:.6f} → M3 PASS")
print(f"(等价: 需要 angular mass + Dk²_min > ||F_H||_op ≈ {F_H_max:.4f})")
print()

# --- save summary json ---
import json
summary = {
    "w_l1": float(w_l1),
    "F_op_bound": float(F_op_bound),
    "K_H_lambda_max": float(eigs_KH.max()),
    "K_H_lambda_min": float(eigs_KH.min()),
    "K_H_PSD": bool(eigs_KH.min() >= -1e-10),
    "F_H_lambda_max": float(F_H_max),
    "F_H_lambda_min": float(F_H_min),
    "F_H_op": float(max(abs(F_H_max), abs(F_H_min))),
    "Dk2_min_V0": float(Dk2_min),
    "m_theta2_critical_for_M3_pass": float(m2_critical),
    "verdicts": {f"{k}": {"L_min": float(v[0]), "LmF_min": float(v[1]), "verdict": v[2]}
                 for k, v in verdicts.items()},
}
(OUT / "spectrum_summary.json").write_text(json.dumps(summary, indent=2))
print(f"saved summary: {OUT / 'spectrum_summary.json'}")
