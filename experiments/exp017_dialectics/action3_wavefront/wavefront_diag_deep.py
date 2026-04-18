"""
Action 3 深度: 测试多个 doc, 细粒度 C_s(r), 测 diffusion scaling,
检查 Kramers formula applicability.
"""
import sys
sys.path.insert(0, '/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/action3_wavefront')
from wavefront_diag import (run_langevin, compute_Cs_r, fit_avrami,
                             build_source_from_emb, init_u_nonzero, build_nb,
                             G, N, DT, STEPS, SIGMA, CLAMP, U_THRESH)
import json
import numpy as np
import time
import os

# ========== 多 doc reproducibility ==========
print("\n=== 多 doc reproducibility ===")
emb_path = '/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/embeddings_nfcorpus.json'
embs = json.load(open(emb_path))
doc_ids = ['MED-961', 'MED-952', 'MED-942']

t_cross_all = []
for idx, doc_id in enumerate(doc_ids):
    emb = np.array(embs[f'd:{doc_id}'], dtype=np.float32)
    sb_mean = emb[512:].mean()
    print(f"\n--- doc {idx}: {doc_id} (Sb_mean={sb_mean:.4e}) ---")
    result = run_langevin(emb, seed=1000 + idx*17, sigma=SIGMA, steps=1000,  # 短跑 1000 steps 看统计
                          track_crossing=True, return_snapshots=False)
    t_cross = result['t_cross']
    N_crossed = result['N_crossed']
    t_cross_all.append(t_cross)
    n_c = (t_cross >= 0).sum()
    print(f"  final N_crossed = {n_c}/{N} = {100*n_c/N:.2f}%")
    tc = t_cross[t_cross >= 0]
    print(f"  t_cross percentiles: 50%={np.percentile(tc, 50):.1f}, 90%={np.percentile(tc, 90):.1f}")
    n_av, tau, r2 = fit_avrami(N_crossed, n_c, dt_step=DT)
    if n_av is not None:
        print(f"  Avrami n={n_av:.3f}, tau={tau:.3f}, R²={r2:.4f}")

# 统计 Avrami n 跨 doc 方差
print("\n=== Avrami n 跨 3 doc ===")
ns = []
for tc_arr in t_cross_all:
    n_c = (tc_arr >= 0).sum()
    if n_c > 0:
        N_crossed = np.zeros(1001, dtype=np.int64)
        for step in range(1001):
            N_crossed[step] = (tc_arr <= step).sum() if step > 0 else 0
        N_crossed[0] = (tc_arr == 0).sum()
        n_av, _, _ = fit_avrami(N_crossed, n_c, dt_step=DT)
        if n_av is not None:
            ns.append(n_av)
print(f"  n values: {ns}")
if len(ns) > 0:
    print(f"  mean n = {np.mean(ns):.3f}, std = {np.std(ns):.3f}")

# ========== 细粒度 C_s(r) 在 dt_thresh 较小 ==========
print("\n=== 细粒度 C_s(r) at dt_thresh=2 (0.1 time units, 与 local diffusion length 比) ===")
tc_doc0 = t_cross_all[0]
for dt_thr in [1, 2, 3, 5]:
    r_centers, Cs, counts = compute_Cs_r(tc_doc0, dt_thresh_steps=dt_thr,
                                          max_r=16, n_pairs_sample=1_000_000)
    print(f"\ndt_thresh={dt_thr} steps ({dt_thr*DT:.2f} time units):")
    for i, rc in enumerate(r_centers):
        if counts[i] > 500:
            print(f"  r={rc:.1f}: C_s={Cs[i]:.4f} (n={counts[i]})")

# ========== Kramers applicability check ==========
print("\n=== Kramers applicability diagnostic ===")
print(f"σ={SIGMA}, T_eff=σ²/2={SIGMA**2/2}")
print(f"ΔV (u=1→saddle u=0.26)=2.013")
print(f"ΔV/T_eff = {2.013/(SIGMA**2/2):.2f}")
print(f"V''(u=1)=2, V''(saddle)≈-8.25")
print(f"Kramers 1D prefactor ω₀/2π ≈ √(2·8.25)/(2π) ≈ {np.sqrt(2*8.25)/(2*np.pi):.3f}")

# 1-step noise displacement vs ΔV 尺度
noise_step = SIGMA * np.sqrt(DT)
print(f"\n1-step noise displacement on (a,b): σ·√dt = {noise_step:.4f}")
print(f"1-step Δu near |ψ|=1: 2|ψ|·σ√dt ≈ {2 * 1.0 * noise_step:.4f}")
print(f"√N-step cumulative 位移: (diffusion) ≈ 2|ψ|·σ·√(dt · N_step):")
for n_steps in [1, 5, 10, 50, 100]:
    disp = 2.0 * SIGMA * np.sqrt(DT * n_steps)
    print(f"  N={n_steps}: disp ≈ {disp:.3f}  (saddle at u=0.26 → ~0.7 u-distance from u=1)")

# 比较观察的 t_cross 中位数 与 diffusion 时间估算
print(f"\n观察 median t_cross: 10 steps (0.5 time units), per-voxel u 从 1 → 0.5 (Δu=0.5)")
print(f"Diffusion 估算: Δu=0.5 需要 N_step ≈ (0.5/(2σ√dt))² = {(0.5/(2*SIGMA*np.sqrt(DT)))**2:.2f} steps")
print(f"  → pure diffusion 预测 N_step ≈ 5, 观察 median=10. 势阱 restoring force 仅 ~2x 阻碍 diffusion.")

# Check: 如果去掉 gradient-flow 部分, 只做 noise + clamp, 看是否有相同 crossing?
print("\n=== Pure noise (no potential, no source) Langevin 对照 ===")
def run_pure_noise(sigma=SIGMA, steps=200, dt=DT, clamp=CLAMP, seed=7777):
    """从 u_init=1.0±0.3 出发, 只有 noise, 没有 V 和 S."""
    a, b = init_u_nonzero(seed)
    rng = np.random.default_rng(seed * 31415)
    noise_scale = sigma * np.sqrt(dt)
    t_cross = np.full(N, -1, dtype=np.int32)
    u0 = a*a + b*b
    t_cross[u0 < U_THRESH] = 0
    N_crossed = np.zeros(steps+1, dtype=np.int64)
    N_crossed[0] = (u0 < U_THRESH).sum()
    for step in range(1, steps+1):
        eta_a = rng.standard_normal(N).astype(np.float32)
        eta_b = rng.standard_normal(N).astype(np.float32)
        a = np.clip(a + noise_scale * eta_a, -clamp, clamp)
        b = np.clip(b + noise_scale * eta_b, -clamp, clamp)
        u = a*a + b*b
        jc = (t_cross < 0) & (u < U_THRESH)
        t_cross[jc] = step
        N_crossed[step] = (t_cross >= 0).sum()
    return t_cross, N_crossed

tc_noise, N_noise = run_pure_noise(sigma=SIGMA, steps=200)
n_c_noise = (tc_noise >= 0).sum()
print(f"Pure noise (no V, no S): {n_c_noise}/{N} ({100*n_c_noise/N:.1f}%) crossed in 200 steps")
tc = tc_noise[tc_noise >= 0]
if len(tc) > 10:
    print(f"  median t_cross (pure noise): {np.median(tc):.1f} steps (vs Langevin+V: ~10 steps)")

# Equivalent Kramers per-voxel expected:
print(f"\n=== 比较 Kramers 预测 vs 观察 ===")
k_kramers_rate = 3.4 * np.exp(-16.1)  # per time unit
expected_crossings_tsim = k_kramers_rate * 250
observed_frac_per_voxel = 0.87
print(f"Kramers k·t_sim = {expected_crossings_tsim:.3e} per voxel")
print(f"Observed fraction crossed = {observed_frac_per_voxel}")
print(f"Ratio obs/pred = {observed_frac_per_voxel / expected_crossings_tsim:.2e}")
print(f"  → factor 10^{np.log10(observed_frac_per_voxel / expected_crossings_tsim):.2f} anomaly")

# 计算 "actual effective rate" 从观察: 每 voxel crossing rate
mean_t_cross_timeunits = 10 * DT  # median t_cross
effective_rate = 1.0 / mean_t_cross_timeunits  # per time unit (if modeled as Poisson)
print(f"\n'Effective' rate estimate: 1/t_median = {effective_rate:.2f} per time unit")
print(f"Kramers predicts: {k_kramers_rate:.3e} per time unit")
print(f"Ratio effective/Kramers = {effective_rate/k_kramers_rate:.2e}")
print(f"  → Kramers underestimates by ~10^{np.log10(effective_rate/k_kramers_rate):.1f}")
