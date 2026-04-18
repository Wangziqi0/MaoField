#!/usr/bin/env python3
"""A2 Part 3 — combine Part 1 spectrum + Part 2 m_theta^2 → M3 verdict.

结合:
- Part 1: ||F_H||_op = 0.9525 (实际 eigenvalue, 比 ℓ^1 bound 1.118 紧)
- Part 2: m_theta^2 实测 = 0.017 (median per-doc), m_rho^2 = 0.09 (median)

Verdict: 因为 m_theta^2 ≪ ||F_H||_op (几乎两个量级), 且 m_rho^2 也远小于 V''_rad=4 的预期,
实测 effective mass spectrum 都不够覆盖 ||F_H||_op.

最严格的 verdict:
  λ_min((L-F)_H on V_0) = min(D k_min^2 + m_rho^2, D k_min^2 + m_theta^2) - ||F_H||_op
                       = min(0.00384 + 0.09, 0.00384 + 0.017) - 0.9525
                       = 0.021 - 0.9525  (theta mode wins)
                       ≈ -0.93  (FAIL, negative by 0.93)
"""
import json
import numpy as np
from pathlib import Path

F_H_op = 0.9525  # from Part 1
m_theta_sq = 0.01654  # median from Part 2 per-doc fit, tangent-plane method
m_theta_sq_lo = 0.00846  # 5th percentile (conservative for M3 救援)
m_theta_sq_hi = 0.02634  # 95th percentile
m_rho_sq = 0.09181  # median
m_rho_sq_lo = 0.03701
m_rho_sq_hi = 0.20742

D = 0.1
Dk2_min = D * 2 * (1 - np.cos(2*np.pi/32))  # ≈ 0.00384

print("="*78)
print("A2 M3 Verdict: combine Part 1 spectrum + Part 2 m_theta extraction")
print("="*78)
print()
print(f"Part 1: ||F_H||_op (Hermitian part) = {F_H_op:.4f}")
print(f"Part 1: 临界 m_θ² (M3 PASS 需): > {F_H_op - Dk2_min:.4f}")
print()
print(f"Part 2: m_theta^2 median = {m_theta_sq:.5f}  (90% CI: [{m_theta_sq_lo:.5f}, {m_theta_sq_hi:.5f}])")
print(f"Part 2: m_rho^2   median = {m_rho_sq:.5f}  (90% CI: [{m_rho_sq_lo:.5f}, {m_rho_sq_hi:.5f}])")
print()

# λ_min((L-F)_H) = min(m_theta_sq, m_rho_sq) + Dk2_min - F_H_op
L_min_measured = Dk2_min + min(m_theta_sq, m_rho_sq)
LmF_H_min = L_min_measured - F_H_op
print(f"λ_min(L on V_0) 实测 = Dk²_min + min(m_θ², m_ρ²) = {L_min_measured:.4f}")
print(f"λ_min((L-F)_H on V_0) = {L_min_measured:.4f} - {F_H_op:.4f} = {LmF_H_min:+.4f}")
print()

if LmF_H_min > 0:
    verdict = "PASS"
elif abs(LmF_H_min) < 0.01:
    verdict = "MARGINAL"
else:
    verdict = "FAIL"

print(f"=> M3 verdict: **{verdict}**")
print()

# 甚至 95th percentile upper bound 也 fail:
L_min_95 = Dk2_min + min(m_theta_sq_hi, m_rho_sq_hi)
print(f"用 95%ile upper bound (最 favor M3): L_min_95 = {L_min_95:.4f}, "
      f"λ_min((L-F)_H) = {L_min_95 - F_H_op:+.4f}  → still {'PASS' if L_min_95 > F_H_op else 'FAIL'}")
print()

# Falsification test: is m_theta^2 < 1.2 (pre-committed threshold)?
print(f"Pre-committed falsification test (A5 反题姐姐, A1 §7 [?]5):")
print(f"  若 m_θ² < 1.2 → M3 falsified.")
print(f"  实测 m_θ² = {m_theta_sq:.4f} (两个量级 < 1.2)")
print(f"  → M3 **FALSIFIED** 按 pre-commit 标准.")
print()

summary = {
    "F_H_op_from_eigvals": F_H_op,
    "m_theta_sq_critical_for_pass": float(F_H_op - Dk2_min),
    "m_theta_sq_measured_median": m_theta_sq,
    "m_theta_sq_CI90": [m_theta_sq_lo, m_theta_sq_hi],
    "m_rho_sq_measured_median": m_rho_sq,
    "m_rho_sq_CI90": [m_rho_sq_lo, m_rho_sq_hi],
    "lambda_min_LmFH": float(LmF_H_min),
    "verdict": verdict,
    "pre_commit_test": {
        "threshold": 1.2,
        "measured": m_theta_sq,
        "result": "FALSIFIED" if m_theta_sq < 1.2 else "NOT_FALSIFIED",
    },
}
out_path = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/ACTION2_figures/final_verdict.json")
out_path.write_text(json.dumps(summary, indent=2))
print(f"saved: {out_path}")
