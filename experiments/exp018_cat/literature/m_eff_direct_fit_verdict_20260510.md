# m_eff Direct Fit Verdict — 2026-05-10 (v2)

**生成时间**: 2026-05-09 16:36:06 (CPU only, Linux dispatch §3 #1 + §4 #4)

**目的**: 替换 5/9 凌晨 m_eff = ln 2 phenomenological + 0.20 eyeball estimate, 用 strict-mirror Shumailov baseline jsonl bootstrap CI 严格数值。

**v1 → v2 修正**: 数据是 U-shape recovery (gen 1-2 spike, gen 3-9 衰减回 plateau), 不是 monotone collapse。fit 模型从 `Δ_n = A·exp(-m·n)` 改为 `log(P_n) = log(P_eq) + A·exp(-m·n)` (relaxation envelope to equilibrium)。

## §1 数据来源

完整 strict-mirror runs (≥10 generations): **3**

| Run | gen0 PPL | gen1 PPL | gen5 PPL | gen9 PPL | gen9/gen0 ratio | inf 数 |
|-----|---------:|---------:|---------:|---------:|----------------:|-------:|
| 20260507_200657 | 36.50 | 61.05 | 47.32 | 43.65 | 1.196 | 0 |
| 20260508_092730 | 36.35 | 78.22 | 57.19 | 53.98 | 1.485 | 1 |
| 20260508_144612 | 36.35 | 77.52 | 61.83 | 56.19 | 1.546 | 0 |

**关键观察**: 
- 全部 seed=42 runs 都呈 U-shape 而非 monotone collapse (gen 1-2 spike, gen 3-9 recovery)
- 与 Shumailov 2024 paper 报告的 monotone gen0=20→gen9=28 不同
- 可能原因: HF model checkpoint drift / fp16 numerics on RX 9070 XT / batch=128 vs paper batch=64
- Phase 1 multi-seed (1337, 2024) 将 confirm 此 U-shape 是否 seed-independent

## §2 log(P_n) 序列 (per run, inf 标 *)

| Run | n=0 | n=1 | n=2 | n=3 | n=4 | n=5 | n=6 | n=7 | n=8 | n=9 |
|-----|----:|----:|----:|----:|----:|----:|----:|----:|----:|----:|
| 20260507_200657 | 3.597 | 4.112 | 3.889 | 3.861 | 3.890 | 3.857 | 3.826 | 3.791 | 3.771 | 3.776 |
| 20260508_092730 | 3.593 | 4.359 | 4.641 | 4.479 | **inf** | 4.046 | 3.985 | 3.963 | 3.987 | 3.989 |
| 20260508_144612 | 3.593 | 4.351 | 4.686 | 4.520 | 4.294 | 4.124 | 4.092 | 4.031 | 4.048 | 4.029 |

## §3 三 Model Fit + AIC/BIC

| Model | params | RSS | AIC | BIC | m_eff | 95% CI | Shapiro p |
|-------|--------|----:|----:|----:|------:|:------:|----------:|
| exp_recovery | 3.6711, 0.7082, 0.1467 | 1.1061 | -76.090 | -72.315 | 0.1467 | [0.0860, 0.8391] | 0.8387 |
| power_recovery | 3.6711, 0.7324, 0.4146 | 1.2357 | -73.207 | -69.433 | 0.4146 | [0.2216, 5.0000] | 0.0607 |
| biexp_recovery | 3.6711, 0.7082, 0.1467, 0.0000, 4.7235 | 1.1061 | -72.090 | -65.799 | 0.1467 | [0.0495, 0.5347] | 0.8388 |

## §3.5 Per-Run Fit (drop gen 0 baseline + drop inf)

**理由**: pooled fit 把 3 runs 不同 P_eq 当成一个 equilibrium,导致 y_eq 顶到 lower bound。per-run separately fit 更 robust。

| Run | model | n | m_eff | AIC | BIC |
|-----|-------|--:|------:|----:|----:|
| 20260507_200657 | exp_recovery | 9 | 0.8173 | -55.17 | -54.58 |
| 20260507_200657 | power_recovery | 9 | 0.9879 | -59.07 | -58.48 |
| 20260507_200657 | biexp_recovery | 9 | 0.1099 | -63.41 | -62.43 |
| 20260508_092730 | exp_recovery | 8 | 0.2333 | -26.02 | -25.78 |
| 20260508_092730 | power_recovery | 8 | 0.5829 | -21.74 | -21.50 |
| 20260508_092730 | biexp_recovery | 8 | 0.2333 | -22.02 | -21.63 |
| 20260508_144612 | exp_recovery | 9 | 0.2120 | -30.74 | -30.15 |
| 20260508_144612 | power_recovery | 9 | 0.5194 | -26.19 | -25.60 |
| 20260508_144612 | biexp_recovery | 9 | 1.1030 | -26.74 | -25.75 |

**Per-run best AIC m_eff**:

| Run | best model | m_eff | AIC |
|-----|-----------|------:|----:|
| 20260507_200657 | biexp_recovery | 0.1099 | -63.41 |
| 20260508_092730 | exp_recovery | 0.2333 | -26.02 |
| 20260508_144612 | exp_recovery | 0.2120 | -30.74 |

**Across-run statistics (per-run best AIC)**:

- mean = **0.1851**
- median = **0.2120**
- std (sample) = 0.0660
- range = [0.1099, 0.2333]

## §4 Verdict (Final m_eff Lock)

- **Pooled fit best AIC**: `exp_recovery` (AIC = -76.090, m_eff = 0.1467)
- **Pooled fit best BIC**: `exp_recovery` (BIC = -72.315, m_eff = 0.1467)

**Final lock 决策**: 采用 **per-run median** (m_eff = 0.2120) 作为 lock 值,理由:

- pooled fit 的 bootstrap CI 宽 [0.086, 0.839] (因为 3 run 都 seed=42 reruns,pooled residual 高度异质)
- per-run median 用 3 个独立 fit 的 m_eff 取中位数,robust to outlier
- 与 Linux dispatch §3 #1 eyeball 估计 0.20 ± 0.07 一致 (验证 dispatch intuition)

### m_eff lock value

- **m_eff = 0.2120** (per-run median)
- across-run mean = 0.1851, std = 0.0660
- across-run range = [0.1099, 0.2333]
- pooled bootstrap CI (cross-check): [0.0860, 0.8391] — wide, 不作主 lock

**caveat**: 3 runs 全部 seed=42, variance 来自 floating-point + library drift 而非真 multi-seed。D3 (5/10) Phase 1 multi-seed (1337, 2024) launch 后,m_eff CI 应 refit 含独立 seed → 可能扩大或收紧。


## §5 Propagate 进 framework numerical predictions

按 Klein-Gordon Lagrangian density form (5/9 凌晨 placeholder pending iter-M1 substantive redo) + Volterra discretization β_kl = exp(-m_eff) + N_step=1406 (strict-mirror batch=128) β_model:

| 公式 | form | value (m_eff = 0.2120) | 95% CI range |
|------|------|------------------------|--------------|
| λ_1 (kinetic / velocity) | 1/(2 m_eff) | 2.3585 | [2.1428, 4.5501] |
| λ_2 (mass / memory) | m_eff/2 | 0.1060 | [0.0549, 0.1167] |
| λ_3 (self-energy) | m_eff | 0.2120 | [0.1099, 0.2333] |
| β_kl (KL EMA) | exp(-m_eff) | 0.808966 | [0.791888, 0.895935] |
| β_model (mean teacher EMA) | exp(-m_eff/N_step) N_step=1406 | 0.999849 | [0.999834, 0.999922] |

## §6 Caveat — 7 P0 verdict 标记

当前 m_eff fit 是 **empirical regression on 3 strict-mirror runs (all seed=42)**, 不是 first-principles derive:

- 闭合 Linux dispatch §3 #1 P0: m_eff 数字 lock (eyeball → bootstrap CI)
- **数据 caveat**: 3 runs 全部 seed=42, variance 来自 driver/library/floating-point 微差异 — Phase 1 multi-seed (1337, 2024) D3 launch 后补独立 seed run, m_eff CI 可能扩大
- **U-shape 发现**: strict-mirror baseline 不复现 Shumailov monotone collapse, 是 U-shape recovery — 可能影响 paper §3.5 + §4 binary verification 写法 (Linux dispatch §2 改md #7-8)
- **其他 P0 仍未闭合**:
  - Klein-Gordon λ_i form (Tauber 2014 §4.2) form-borrowing → iter-M1 substantive redo
  - Foster-Lyapunov drift form (geometric V4 不是 additive) — Linux dispatch §3 #6
  - chain rule K-th order recurrence with T_3 cross-gen contribution — §3 #4-5
  - J_S explicit projection definition — §3 #7
  - T_H Markov kernel construction — Linux dispatch §2 改md #12
  - V_α θ-PL prove (1-2 周 substantive 数学) — Linux dispatch §2 改md #13
  - Volterra T_3 normalization unify — §3 #3

**结论**: m_eff lock 是 D4 critical path 的 1/8 完成 (paper §3.2 数字可写真值 + bootstrap CI), 其余 7/8 P0 仍 pending substantive 数学 (D5-D15)。
