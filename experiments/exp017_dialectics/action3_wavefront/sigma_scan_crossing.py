"""
Action 3 最终 diagnostic: σ-scan of crossing statistics for 单 doc
看 t_cross 如何随 σ 变化, 区分 Kramers (exp-like dependence) vs
diffusion-dominated (power-law / quadratic dependence).
"""
import sys, os, time, json
sys.path.insert(0, '/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/action3_wavefront')
from wavefront_diag import (run_langevin, fit_avrami,
                             G, N, DT, STEPS, CLAMP, U_THRESH)
import numpy as np

emb_path = '/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/embeddings_nfcorpus.json'
embs = json.load(open(emb_path))
emb = np.array(embs['d:MED-961'], dtype=np.float32)

print("=== σ-scan of crossing rate (test Kramers exp dependence) ===")
print("Kramers: rate ∝ exp(-ΔV/T_eff) = exp(-2·ΔV/σ²) → log(rate) ∝ -1/σ²")
print("Diffusion: rate ∝ σ² / Δu² (linear in σ²)")
print()

results = {}
for sigma in [0.1, 0.2, 0.3, 0.5, 0.7]:
    t0 = time.time()
    res = run_langevin(emb, seed=1000, sigma=sigma, steps=200,
                       track_crossing=True, return_snapshots=False)
    t_cross = res['t_cross']
    n_c = (t_cross >= 0).sum()
    T_eff = sigma**2 / 2
    dV_over_T = 2.013 / T_eff if T_eff > 0 else float('inf')
    kramers_rate = 3.4 * np.exp(-dV_over_T)  # per time unit
    expected_k = kramers_rate * 200 * DT  # crossings per voxel in 200 steps

    tc = t_cross[t_cross >= 0]
    median_t_steps = np.median(tc) if len(tc) > 0 else -1
    actual_rate = 1.0 / (median_t_steps * DT) if median_t_steps > 0 else -1

    print(f"σ={sigma:.2f}: T_eff={T_eff:.4f}, ΔV/T={dV_over_T:.2f}")
    print(f"  Kramers predicts rate={kramers_rate:.3e}/time, k·200dt={expected_k:.3e}/voxel")
    print(f"  Observed: {n_c}/{N}={100*n_c/N:.1f}% crossed in 200 steps")
    print(f"    median t_cross={median_t_steps}, actual rate={actual_rate:.3f}/time")
    if expected_k > 0 and actual_rate > 0:
        print(f"    ratio actual/kramers = {actual_rate/kramers_rate:.2e}")
    print(f"  Elapsed {time.time()-t0:.1f}s")
    results[sigma] = dict(
        T_eff=T_eff, dV_over_T=dV_over_T, kramers_rate=kramers_rate,
        n_crossed=int(n_c), median_t_steps=float(median_t_steps),
        actual_rate=float(actual_rate) if actual_rate > 0 else -1
    )

# 分析 scaling
print("\n=== Scaling analysis ===")
print("If Kramers: log(rate) = -ΔV/T_eff + const → plot log(rate) vs 1/σ² → slope=-2·ΔV")
print("If diffusion: rate = 4σ²/d² → plot rate vs σ² → linear")
print()
sigmas = sorted(results.keys())
print("σ       | 1/σ²     | log10(actual_rate) | σ² (diffusion)  | actual_rate")
print("-" * 85)
for s in sigmas:
    r = results[s]['actual_rate']
    if r > 0:
        print(f"{s:.2f}    | {1/s**2:7.3f}  | {np.log10(r):7.3f}            | {s**2:8.4f}        | {r:.4f}")

# Fit actual_rate vs σ²
sigmas_arr = np.array([s for s in sigmas if results[s]['actual_rate'] > 0])
rates = np.array([results[s]['actual_rate'] for s in sigmas_arr])
x_kr = 1.0 / sigmas_arr**2
y_log = np.log(rates)
# Kramers fit: log(rate) ≈ -ΔV * 2 * (1/σ²) + log(prefactor)
A_kr = np.vstack([x_kr, np.ones_like(x_kr)]).T
coef_kr, *_ = np.linalg.lstsq(A_kr, y_log, rcond=None)
slope_kr = coef_kr[0]
predicted_dV = -slope_kr / 2  # slope = -2·ΔV → ΔV = -slope/2
# Diffusion fit: rate ≈ C·σ² → rate/σ² = const
x_diff = sigmas_arr**2
# linear fit: rate = a·σ²
a_diff = (rates * x_diff).sum() / (x_diff**2).sum()
# residuals
pred_kr = np.exp(A_kr @ coef_kr)
pred_diff = a_diff * x_diff
rss_kr = ((rates - pred_kr)**2).sum()
rss_diff = ((rates - pred_diff)**2).sum()
ss_tot = ((rates - rates.mean())**2).sum()
print(f"\nKramers fit: log(rate) = {slope_kr:.3f}/σ² + {coef_kr[1]:.3f}")
print(f"  Implied ΔV = {predicted_dV:.3f} (true ΔV=2.013) — Kramers match if this ≈ 2.013")
print(f"  R² (Kramers) = {1 - rss_kr/ss_tot:.4f}")
print(f"Diffusion fit: rate = {a_diff:.3f}·σ²")
print(f"  R² (diffusion linear in σ²) = {1 - rss_diff/ss_tot:.4f}")

# Summary
print("\n=== Verdict ===")
if abs(predicted_dV - 2.013) < 0.5:
    print("→ Kramers-like scaling (log rate linear in 1/σ²)")
else:
    print("→ NOT Kramers scaling — implied ΔV far from true ΔV")

# save
np.savez_compressed('/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/action3_wavefront/sigma_scan.npz',
                    sigmas=sigmas_arr, rates=rates, results=results)
