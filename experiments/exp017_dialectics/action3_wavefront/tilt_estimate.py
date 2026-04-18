"""
Action 3 路线 C: BGE DC tilt 量级估

⟨S_b⟩ = -1.48e-3 (17σ from 0) 作 constant tilt, 算是否单独可解释 factor 10⁴.
"""
import numpy as np
import json

# ====== Inputs ======
S_b_mean = 1.48e-3  # |⟨S_b⟩|
S_a_mean_typical = 5e-5  # 参考 (Sa 近 0, 不贡献 tilt)

# Langevin parameters
sigma = 0.5
gamma = 1.0
T_eff = sigma**2 / (2 * gamma)  # = 0.125
dt = 0.05

# Potential landscape (A1: V = u(u-1)²(u-4)², wells at u=0,1,4; saddles at u=0.2597, 2.7036)
V_u0 = 0.0
V_saddle_inner = 2.013   # 即 V(u=0.2597)
V_u1 = 0.0
V_saddle_outer = 13.187  # V(u=2.7036)
V_u4 = 0.0

u_well_1 = 1.0
u_saddle_inner = 0.2597
u_well_0 = 0.0
d_inner_barrier_u = u_well_1 - u_saddle_inner  # = 0.7403 (in u=|ψ|² space)
d_inner_barrier_psi = 1.0 - np.sqrt(u_saddle_inner)  # = 1.0 - 0.5096 = 0.4904 (in |ψ| space)

delta_V_inner = V_saddle_inner - V_u1  # = 2.013

print("=== Action 3 路线 C: BGE DC tilt 量级估 ===\n")
print("## 2.1 数字 input")
print(f"|⟨S_b⟩| = {S_b_mean:.3e}   (17σ from 0, p<10⁻²⁵)")
print(f"σ = {sigma}, T_eff = σ²/(2γ) = {T_eff}")
print(f"ΔV (inner barrier, u=1 → u=0 via saddle u=0.26) = {delta_V_inner}")
print(f"u-distance from u=1 well to u=0.2597 saddle = {d_inner_barrier_u:.4f}")
print(f"|ψ|-distance from |ψ|=1 to |ψ|=0.51 (saddle) = {d_inner_barrier_psi:.4f}")
print(f"ΔV/T_eff = {delta_V_inner/T_eff:.2f}")
print(f"Kramers rate: k = 3.4·exp(-16.1) = {3.4*np.exp(-16.1):.3e}/time")
print(f"Kramers per-voxel: k·t_sim = {3.4*np.exp(-16.1)*250:.3e}")

# ====== Part 2.2: Force projection ======
print("\n## 2.2 Force projection onto inner-barrier reaction coordinate")
print()
print("方程 (overdamped Langevin on complex ψ):")
print("  γ·dψ/dt = D·∇²ψ − F(u)·ψ + S + η, S = S_a + i·S_b")
print()
print("Reaction coordinate for u=1 → u=0: u = |ψ|² = a² + b².")
print("沿 u 方向的力 (from source S):")
print("  (du/dt)_from_S = 2a·S_a + 2b·S_b")
print()
print("在 u=1 well 处, ⟨|ψ|²⟩=1, 假设各向同性 ⟨a⟩≈1/√2, ⟨b⟩≈1/√2 (非物理假设, 实际 a/b 各 near 1/√2).")
print("|ψ| ~ 1 → 典型 |a|, |b| ~ 0.7.")
print()
# Source mean values 在 voxel 上:
# Sb 每 voxel 值平均 ≈ -1.48e-3 × normalization.
# 注意: build_source 做了 max-normalization, 所以 sb 每 voxel 值 ~ O(1) 但 mean ~ -1.48e-3 × 放大因子.
# 实际上让我从 embedding 重建精确 tilt.
print("Loading actual embeddings to compute |S_b| per-voxel after smoothing + normalize...")
emb_path = '/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/embeddings_nfcorpus.json'
embs = json.load(open(emb_path))

# Compute per-voxel Sb mean
G = 32
N = G*G*G
def build_nb_roll():
    idx = np.arange(N).reshape(G, G, G)
    xm = np.roll(idx, 1, axis=2).ravel(); xp = np.roll(idx, -1, axis=2).ravel()
    ym = np.roll(idx, 1, axis=1).ravel(); yp = np.roll(idx, -1, axis=1).ravel()
    zm = np.roll(idx, 1, axis=0).ravel(); zp = np.roll(idx, -1, axis=0).ravel()
    return xm, xp, ym, yp, zm, zp
nb = build_nb_roll()

def tile_and_smooth(emb_half):
    """Match Rust: sa[k] = emb[k%512], then smooth 3x in each axis, then max-normalize."""
    s = emb_half[np.arange(N) % 512].astype(np.float32).copy()
    xm, xp, ym, yp, zm, zp = nb
    for _ in range(3):
        buf = (s[xm] + s + s[xp]) / 3.0; s = buf.copy()
        buf = (s[ym] + s + s[yp]) / 3.0; s = buf.copy()
        buf = (s[zm] + s + s[zp]) / 3.0; s = buf.copy()
    mx = np.abs(s).max()
    if mx > 0: s = s / mx
    return s

sb_means_per_voxel = []
sa_means_per_voxel = []
for doc_id in ['MED-961', 'MED-952', 'MED-942', 'MED-941', 'MED-917']:
    emb = np.array(embs[f'd:{doc_id}'], dtype=np.float32)
    sb_field = tile_and_smooth(emb[512:])
    sa_field = tile_and_smooth(emb[:512])
    sb_means_per_voxel.append(sb_field.mean())
    sa_means_per_voxel.append(sa_field.mean())
    print(f"  {doc_id}: post-normalize ⟨S_b⟩_voxel={sb_field.mean():.4e}, "
          f"|S_b|_max={np.abs(sb_field).max():.3f}, std_S_b={sb_field.std():.3f}")

sb_post_mean = np.mean(sb_means_per_voxel)
print(f"\nPost-normalize ⟨S_b⟩ per voxel (avg over 5 docs) = {sb_post_mean:.4e}")
print(f"Post-normalize ⟨S_a⟩ per voxel (avg over 5 docs) = {np.mean(sa_means_per_voxel):.4e}")

# F_tilt = 2b · ⟨S_b⟩  (沿 u 方向的 deterministic tilt from non-zero mean source)
# 在 u=1 well, b ~ 0.7 (假设 init |psi|=1 各向同分布在 (a,b))
# 实际 init_u_nonzero 是 a=1.0±0.3, b=0.3·rand，所以 |b| ~ 0.3, |a| ~ 1.0
# 在 langevin 过程中 b grows from noise 到 ~sigma·√dt*√t_sim ~ 3.5 at t=250.
# 但在 crossing 发生 (step ~10, t~0.5) 时, b growth negligible (~σ·√(t)=0.35).
# 所以 b 在 crossing 时 typical |b| ~ 0.3 (init spread).
print("\n### Tilt projection onto u-axis:")
a_typ = 1.0   # init: a~1.0±0.3
b_typ = 0.3   # init: b~0-0.3 (evolve to ~0.35 at crossing time)
print(f"typical a = {a_typ}, typical |b| = {b_typ}")

# u-axis gradient from S: du/dt|_S = 2a·⟨S_a⟩ + 2b·⟨S_b⟩
dudt_from_Sb_tilt = 2 * b_typ * sb_post_mean
dudt_from_Sa_tilt = 2 * a_typ * np.mean(sa_means_per_voxel)
print(f"⟨du/dt⟩_from_Sb_DC = 2·|b|·⟨S_b⟩ = {dudt_from_Sb_tilt:.4e}")
print(f"⟨du/dt⟩_from_Sa_DC = 2·|a|·⟨S_a⟩ = {dudt_from_Sa_tilt:.4e}")
print(f"(Sb 是 dominant DC, Sa 近 0)")

# Note: 上面用 b_typ=0.3 可能高估实际贡献 (b 早期太小).
# 让我看 a_typ, b_typ 的正负: 实际分布 a 正负平衡 (a=1.0±0.3 → 都 positive),
# b 正负对称 (-0.3 到 0.3, mean ~0).
# 但 per-voxel 只保留 sign; ensemble 上 2b·⟨Sb⟩ 对每 voxel 随机正负.
# 只有 b 有和 Sb 的相关性时 tilt 才 accumulate — 但 b 和 Sb 相关?
# 实际上, gradient flow 会 drive ψ 对齐到 S: -F(u)·ψ + S = 0 解 ψ ∝ S/F(u).
# 所以 local b 会渐渐与 local Sb 对齐: sign(b) = sign(Sb) after relaxation.
# 一旦 b~Sb方向, 2b·⟨Sb⟩ = 2·|b|·⟨|Sb|⟩ · sign_factor

# 关键: 计算 tilt force magnitude when b has aligned with Sb
# ⟨|S_b|⟩ per voxel (absolute mean):
for doc_id in ['MED-961']:
    emb = np.array(embs[f'd:{doc_id}'], dtype=np.float32)
    sb_field = tile_and_smooth(emb[512:])
    print(f"\n{doc_id} after normalize:")
    print(f"  mean(S_b) = {sb_field.mean():.4e}")
    print(f"  mean(|S_b|) = {np.abs(sb_field).mean():.4f}")
    print(f"  std(S_b) = {sb_field.std():.4f}")
    print(f"  max|S_b| = {np.abs(sb_field).max():.4f}")

# 更 careful 的 tilt estimate:
# 情况 I: "Coherent" tilt (b 和 Sb 对齐后): F_tilt = 2·|b|·|Sb|, 但这是 per-voxel full deterministic force, 不是 "DC mean"
# 情况 II: "DC mean" tilt (ensemble 平均): F_tilt = 2·|b|·⟨Sb⟩_mean ~ 2·0.3·(-1.48e-3) = -8.9e-4
#          这是 independent of whether b aligns — 因为 ⟨Sb⟩ 是 spatial mean, 作用于全 field
# A2 路线 C 要求的是 情况 II: constant DC tilt.

F_tilt_dc = 2.0 * b_typ * np.abs(sb_post_mean)
print(f"\n### Tilt force 情况 II (DC 恒定 tilt, 2·|b|·|⟨Sb⟩|):")
print(f"F_tilt = {F_tilt_dc:.4e} per (u-space unit time)")

# 在 u-方向上, 势能差 ΔV=2.013, barrier 距离 d=0.7403 (in u).
# 但 source 进入方程是 dψ/dt ← S/γ, 所以 F_tilt 是 u-位置 time derivative in terms of u-distance.
# 更 rigorous: tilt 对 u-势能的贡献为:
#   dV_eff/du = dV/du - F_tilt (沿 u 方向的等效力)
# 能量降低 (tilt): Δ(V_eff) = - F_tilt_energy × d_barrier
# F_tilt_energy in energy/u units:
# 从 equation of motion: γ du/dt = -dV/du + (2a·Sa + 2b·Sb) 的 projected term
# 所以 effective potential tilt in u:  V_tilt(u) = -(2a·Sa + 2b·Sb) · u (近似 const a, b, S)
# 在 well vs saddle: |Δu|=0.74
# 在 typical (a,b)=(1, 0.3): effective tilt height = |F_tilt| · Δu = F_tilt_dc · 0.74

delta_V_tilt_energy = F_tilt_dc * d_inner_barrier_u
print(f"\n### Effective barrier reduction from tilt (情况 II):")
print(f"Δ(V_eff) = F_tilt · d_barrier = {F_tilt_dc:.4e} × {d_inner_barrier_u:.4f} = {delta_V_tilt_energy:.4e}")

# 但注意: 这个 "力 × 距离" 的 积分 in actual barrier crossing 是动力学的, 不是势能.
# source 项 Sb 直接进 ψ-motion equation, 不是 via potential derivative.
# 严格处理: 给定 const Sb > 0 tilt (在 b 方向), 势能在 b 方向倾斜为 V_eff(a,b) = V(|ψ|²) - Sb·b
# 在 u=a²+b² reaction coord 下, u_saddle_inner 从 0.2597 移位?
# 解 dV_eff/db = -F(u)·2b - Sb = 0 → 2b·F(u) = -Sb → saddle 沿 b 小的偏移.
# 对于 Sb 小 perturbation, saddle height shift: ΔV ≈ -Sb · Δb, Δb ~ 0.1 (估).
# 这非常小.
print()
print("### 严格处理 (Sb 如何改变 saddle structure):")
print("V_eff(a,b) = V(|ψ|²) - a·Sa - b·Sb")
print("Saddle (inner) 原 at u_s=0.2597. 假设 b 方向 tilt:")
print("  b_saddle shift: ΔV_saddle_height = -Sb·b_saddle ≈ 1.48e-3 · 0.5 ≈ 7.4e-4")
print("  Δ(ΔV) = 7.4e-4 (negligible vs ΔV=2.013)")
print()

# ====== Boltzmann ratio ======
print("## 2.3 Boltzmann ratio ")
# ratio = exp(-ΔV_eff/T_eff) / exp(-ΔV/T_eff) = exp(Δ(ΔV)/T_eff)
# 情况 II (F_tilt · d_barrier):
exponent_ii = delta_V_tilt_energy / T_eff
ratio_ii = np.exp(exponent_ii)
print(f"情况 II (F·d_barrier / T_eff):")
print(f"  exponent = {delta_V_tilt_energy:.3e} / {T_eff} = {exponent_ii:.4f}")
print(f"  ratio = exp({exponent_ii:.4f}) = {ratio_ii:.4f}")

# 情况 I (coherent: 2|b|·|Sb|_local, per voxel full force):
F_tilt_coherent = 2.0 * b_typ * 0.08  # 用 mean(|Sb|)=0.08
delta_V_tilt_coherent = F_tilt_coherent * d_inner_barrier_u
ratio_coherent = np.exp(delta_V_tilt_coherent / T_eff)
print(f"\n情况 I (coherent 沿 local |Sb|~0.08 计算, 假设 b aligned):")
print(f"  F_tilt = 2·0.3·0.08 = {F_tilt_coherent:.4f}")
print(f"  exponent = F_tilt · d / T_eff = {delta_V_tilt_coherent/T_eff:.4f}")
print(f"  ratio = {ratio_coherent:.3f}")

print("\n## 2.4 Can tilt alone explain 10⁴?")
print(f"  情况 II (DC): ratio = {ratio_ii:.4f}, 远不到 10⁴")
print(f"  情况 I (aligned coherent): ratio = {ratio_coherent:.3f}, 仍 ≪ 10⁴")
print()
# 要 10⁴ 需 exponent = ln(10⁴) = 9.21
# 要 F·d/T = 9.21 → F·d = 9.21 · 0.125 = 1.15
# 要 F = 1.55 (with d=0.74) -- 这 > 1 的 force 在 u-motion 方程里 per step 就 overshoot.
print(f"要 ratio=10⁴ 需要 F·d = ln(10⁴)·T_eff = {np.log(1e4) * T_eff:.3f}")
print(f"  以 d={d_inner_barrier_u:.3f} u-space, 需 F ≈ {np.log(1e4)*T_eff/d_inner_barrier_u:.3f}")
print(f"  DC ⟨Sb⟩ × 2b = {2*b_typ*S_b_mean:.3e} << 1.55 - 差 10³ 倍")
print()
print(">>> 结论 (路线 C): BGE DC tilt 单独 **完全无法** 解释 10⁴")
print(">>> factor 来源 ~ exp(0.007) ≈ 1.007 (negligible ~ 1% 调整)")

print("\n## 对比 Kramers vs 实际 scenario")
print("Kramers formula 的前提: ΔV/T ≫ 1 且 relaxation << escape time.")
print(f"T_eff=0.125, ΔV=2.013, ΔV/T=16.1")
print("但在这个 T 下, Langevin 单步位移 σ√dt=0.112, 10 步累积扩散 Δu~0.5.")
print("Crossing 时间 (~0.5 time unit) << Kramers inverse rate (10⁷ time units).")
print("系统 thermalize 到 bimodal distribution 而非 rare-event escape.")
print("→ Kramers formula NOT APPLICABLE in this regime (diffusion-dominated, not activation-dominated)")
