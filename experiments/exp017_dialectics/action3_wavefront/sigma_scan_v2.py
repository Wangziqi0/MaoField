"""
σ-scan 更 robust: 用 "time to 50% crossing" 作为 rate 代理.
"""
import sys, os, time, json
sys.path.insert(0, '/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/action3_wavefront')
from wavefront_diag import (run_langevin, G, N, DT, STEPS, CLAMP, U_THRESH)
import numpy as np

emb_path = '/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/embeddings_nfcorpus.json'
embs = json.load(open(emb_path))
emb = np.array(embs['d:MED-961'], dtype=np.float32)

# 测 σ ∈ {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7}, each 长 500 steps
results = {}
for sigma in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
    t0 = time.time()
    res = run_langevin(emb, seed=1000, sigma=sigma, steps=500,
                       track_crossing=True, return_snapshots=False)
    N_crossed = res['N_crossed']
    # 找 t_50, t_85
    frac = N_crossed / N
    t_50 = np.argmax(frac >= 0.50) if (frac >= 0.50).any() else -1
    t_85 = np.argmax(frac >= 0.85) if (frac >= 0.85).any() else -1
    final_frac = frac[-1]
    T_eff = sigma**2 / 2
    dV_over_T = 2.013 / T_eff
    kramers_k = 3.4 * np.exp(-dV_over_T)
    kramers_t_half_1 = np.log(2) / kramers_k if kramers_k > 0 else float('inf')

    print(f"σ={sigma:.2f}: T={T_eff:.4f}, ΔV/T={dV_over_T:.2f}, final_frac={final_frac:.3f}")
    print(f"  t_50 = {t_50} steps ({t_50*DT:.2f} time units)")
    print(f"  t_85 = {t_85} steps ({t_85*DT:.2f} time units)")
    print(f"  Kramers t_half_1 (time for 50% of 1 voxel to cross) = {kramers_t_half_1:.3e} time units")
    if t_50 > 0:
        print(f"  Kramers/observed t_50 ratio = {kramers_t_half_1 / (t_50*DT):.3e}")
    results[sigma] = dict(t_50=int(t_50), t_85=int(t_85), final_frac=float(final_frac),
                          T_eff=float(T_eff), dV_over_T=float(dV_over_T),
                          kramers_t_half=float(kramers_t_half_1))
    print(f"  Elapsed {time.time()-t0:.1f}s")

# scaling: log(1/t_50) vs 1/σ²
print("\n=== σ² → 1/t_50 scaling ===")
print("Kramers: 1/t ∝ exp(-ΔV/T) = exp(-2ΔV/σ²) → log(1/t) linear in -1/σ²")
print("Diffusion: 1/t ∝ σ² (linear in σ²) [naive random walk]")
print("Over-damped from u=1: need Δu=0.5, diffusion D_u ≈ 4σ² (for ψ=1), so t_diff ≈ Δu²/(4σ²)")

sigmas = sorted(results.keys())
print(f"\n{'σ':6s} {'1/σ²':>8s} {'σ²':>8s} {'t_50':>8s} {'1/t_50':>12s} {'log10(1/t_50)':>14s}")
for s in sigmas:
    t_50 = results[s]['t_50']
    if t_50 > 0:
        print(f"{s:.2f}   {1/s**2:>8.3f} {s**2:>8.4f} {t_50*DT:>8.3f} {1/(t_50*DT):>12.4f} {np.log10(1/(t_50*DT)):>14.3f}")

# Fit 1/t_50 ∝ σ^p
sigmas_arr = np.array([s for s in sigmas if results[s]['t_50'] > 0 and results[s]['final_frac'] > 0.5])
t_50_arr = np.array([results[s]['t_50'] * DT for s in sigmas_arr])
log_rate = -np.log(t_50_arr)
log_sigma = np.log(sigmas_arr)

# Power law: 1/t = C·σ^p → log(1/t) = p·log(σ) + const
A = np.vstack([log_sigma, np.ones_like(log_sigma)]).T
coef, *_ = np.linalg.lstsq(A, log_rate, rcond=None)
power = coef[0]
print(f"\nPower law fit: 1/t_50 ∝ σ^{power:.2f}")
print(f"  Pure diffusion prediction: p=2 (since D_u ∝ σ²)")

# Kramers fit: log(1/t) = -2ΔV/σ² + const
A_kr = np.vstack([-1/sigmas_arr**2, np.ones_like(sigmas_arr)]).T
coef_kr, *_ = np.linalg.lstsq(A_kr, log_rate, rcond=None)
slope_kr = coef_kr[0]  # = 2ΔV if Kramers
predicted_dV = slope_kr / 2
pred_kr = A_kr @ coef_kr
rss_kr = ((log_rate - pred_kr)**2).sum()
ss_tot = ((log_rate - log_rate.mean())**2).sum()
print(f"\nKramers fit: log(1/t_50) = {slope_kr:.3f}/σ² + {coef_kr[1]:.3f}")
print(f"  Implied ΔV = slope/2 = {predicted_dV:.3f} (true ΔV=2.013)")
print(f"  R² (Kramers) = {1 - rss_kr/ss_tot:.4f}")

pred_power = A @ coef
rss_power = ((log_rate - pred_power)**2).sum()
print(f"Power-law R² = {1 - rss_power/ss_tot:.4f}")

# save
np.savez_compressed('/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/action3_wavefront/sigma_scan_v2.npz',
                    sigmas=sigmas_arr, t_50=t_50_arr, results_list=[results[s] for s in sigmas])
