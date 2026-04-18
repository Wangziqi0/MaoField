# Action 2 M3 V₀ 自洽方程 empirical 数值 verify

**作者**: A2 algo-verify subagent (Opus 4.7 xhigh), Linux Claude dispatch, 2026-04-18
**任务**: rigorous 数值 verify A1 §3.2 spectrum 预测 + 从 Phase B Exp 1 数据提 pseudo-Goldstone mass m_θ² → M3 verdict
**结论速览**: **M3 FALSIFIED**. 实测 m_θ² = 0.017 (median), 远小于临界值 0.95 (从 ||F_H||_op 实测 eigenvalue 导出, 比 A1 猜的 1.2 threshold 略松但量级一致)。λ_min((L-F)_H on V_0) ≈ -0.93, 负定一个量级。按 A1 §7 [?]5 pre-committed 标准 (m_θ² < 1.2 → falsify) **触发**。OP1 回 open, Axiom 6 realization 失败。**Linux 主动下调**, 不救援。

---

## 1. Part 1 spectrum verify 结果

Python script: `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/scripts/A2_spectrum_verify.py`
Raw output 与 summary: `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/ACTION2_figures/spectrum_summary.json`
Histogram: `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/ACTION2_figures/spectrum_verify.png`

### 1.1 Python script run output (raw numbers)

```
参数: G=32, D=0.1, v=1.0, α=0.1, β=0.05, λ=0.05, dt_outer=1.0, N_hist=100

||w||_1 = 20.366011
  (解析: (1-e^(-λ N dt)) / (1-e^(-λ dt)) * dt = 20.366011)  [与 A1 预测 20.366 一致]

||F||_op ≤ alpha + beta * ||w||_1 = 1.118301   [与 A1 预测 1.118 一致]

Dk^2 min (on V_0) = 0.003843  (k_min=2π/32, D*2*(1-cos))
Dk^2 max (on V_0) = 1.2  (k_max 方向, 6D cubic lattice pessimistic)
```

### 1.2 K_H PSD 判 + 数值

**A1 §3.2 的 "不确定" 处 resolved**:

```
K_H (100×100 causal Toeplitz Hermitian part) 谱:
  λ_max(K_H) = 17.050555
  λ_min(K_H) = 0.512500
  K_H is PSD?  YES
  K_H 负 eigenvalue 个数: 0 / 100
```

**解释**: causal exponential 卷积的 Hermitian part 对应 **two-sided symmetric exponential smoothing kernel** κ̃(τ) = (1/2)e^(-λ|τ|), truncated。此 kernel **正 definite in Fourier**: FT 给 Lorentzian-like positive spectrum λ/(λ² + ω²), 始终 > 0。所以 K_H 严格 PSD, λ_min = 0.5125 (= dt_outer/2 ≈ K_mat 对角值) 对应最高频时间 mode (无 history coupling)。

**意义**: F_H = α I + β K_H 的谱**全部 positive**, 不会对 L-F 的 Hermitian part positivity 贡献负 direction — Hermitian part analysis framework (A1 Proposition A1.2) 是 well-defined 的。

### 1.3 F_H 谱 + ||F_H||_op 数值

```
F_H = α I + β K_H 谱:
  λ_max(F_H) = 0.952528
  λ_min(F_H) = 0.125625
  ||F_H||_op = max(|λ_max|, |λ_min|) = 0.952528
```

**紧于 A1 的 ℓ¹ bound**: A1 预估 ||F_H||_op ≤ 1.118 用 ||K_H|| ≤ ||w||_1 = 20.366。实际 λ_max(K_H) = 17.05, 比 20.37 小 16%。因此真实 ||F_H||_op = 0.953 (比 A1 猜的 threshold 1.2 降到 0.95)。临界 m_θ² (M3 PASS 最低要求) 相应降到 **0.949** (i.e., m_θ² + Dk²_min > ||F_H||_op → m_θ² > 0.949)。

### 1.4 λ_min((L-F)_H) for m_θ² ∈ {0, 0.5, 1.2, 2.0}

Tensor product formula: λ_min((L-F)_H on V_0 ⊗ L²_time) = λ_min(L on V_0) - λ_max(F_H)

| m_θ² | L_radial_min | L_angular_min | λ_min(L on V_0) | λ_min((L-F)_H) | M3 状态 |
|---|---|---|---|---|---|
| 0.00 | 4.0038 | 0.0038 | 0.0038 | **-0.9487** | FAIL |
| 0.50 | 4.0038 | 0.5038 | 0.5038 | **-0.4487** | FAIL |
| 1.20 | 4.0038 | 1.2038 | 1.2038 | **+0.2513** | PASS |
| 2.00 | 4.0038 | 2.0038 | 2.0038 | **+1.0513** | PASS |

**临界**: m_θ² > 0.949 → M3 PASS, 否则 FAIL。

---

## 2. Part 2 m_θ² extraction from Phase B Exp 1

Python scripts: `A2_mtheta_extract.py`, `A2_diagnose.py`
Output json: `mtheta_extract_summary.json`
Figures: `mtheta_spectrum.png`, `diagnose.png`

### 2.1 数据 load + polar decomposition

**数据**: `phase_b_exp1/day2/exp/states_exp.bin`, 70 NFCorpus docs, 32³ complex lattice, per doc 2×32768 f32 (real/imag), t_sim = 50。meta 参数与 Appendix §A.2 一致。

**polar decomposition**: ψ(x) = ρ(x) e^{iθ(x)}, 复用 `analyze_O1.py` 的 tangent-plane 法:
- δc(x) = cos θ(x) - ⟨cos θ⟩_x
- δs(x) = sin θ(x) - ⟨sin θ⟩_x
- δρ(x) = ρ(x) - ⟨ρ⟩_x
- P_θ(k) = |FFT(δc)|² + |FFT(δs)|²
- P_ρ(k) = |FFT(δρ)|²
- S_θ(k), S_ρ(k) 径向 bin 后 3D→1D

**Sanity check 发现关键 anomaly**:

| 统计量 | 实测 | 预期 (Mexican-hat groundstate) |
|---|---|---|
| ⟨ρ⟩_x (mean over docs) | 1.190 ± 0.001 | 1.000 (= v) |
| σ(ρ)_x (mean over docs) | 0.024 | ≪ 1 |
| ⟨ψ⟩_x (complex mean, per doc) | magnitude ≈ 0.004 | v = 1 (SSB pick) |
| θ circular std | 3.29 (≈ π/√3 = 1.81 对 uniform) | ≈ 0 (aligned) |
| σ(ψ_rotated.real) / σ(ψ_rotated.imag) | **1.05** (symmetric) | ≫ 1 (radial fluct 压 angular) |

**解读**: 系统处于 **U(1)-symmetric disordered steady state**, 不是 Mexican-hat 谷底的 SSB state。|⟨ψ⟩| ≈ 0 说明没有全局 phase 选择; ρ mean ≈ 1.19 说明 |ψ|² ≈ 1.41 > v², 系统偏出谷底; radial 和 angular variance 完全对称。**A1 §7 [?]1 的 flag 精确命中**: around uniform v 的 linearization 假设完全不适用。

**Implication for 理论 framing**:
- Mexican hat 的 "radial mass 4, angular Goldstone 0" 结构**失效**, 因为没有 SSB。
- 我们测得的 S_θ(k), S_ρ(k) 更像 **disordered phase (高温/强噪声) susceptibility**, effective mass 由 full non-perturbative dynamics 决定, 不由 V''|_v 决定。
- 但仍然可以通过 low-k asymptotic fit 读 "effective inverse correlation length squared" = m² — 这是物理上最直接 relevant to M3 positivity 的量。

### 2.2 S_θ(k) 径向谱

低 k 谱样本 (averaged 70 docs):

| bin | k_center | S_θ(k) | S_ρ(k) | count |
|---|---|---|---|---|
| 0 | 0.098 | ~0 (DC, mean-subtracted) | ~0 | 1 |
| 1 | 0.295 | 2.70e+06 | 3.71e+02 | 26 |
| 2 | 0.491 | 2.03e+06 | 3.38e+02 | 66 |
| 3 | 0.687 | 1.15e+06 | 2.86e+02 | 158 |
| 4 | 0.884 | 6.29e+05 | 2.29e+02 | 234 |
| 5 | 1.080 | 3.13e+05 | 1.79e+02 | 410 |
| 6 | 1.276 | 1.64e+05 | 1.34e+02 | 470 |

**两个观察**:
- S_θ 在 low-k 大约两万倍于 S_ρ — 符合 "angular mode 更软" 的直觉, 但 (见 sanity) 不是因为 SSB Goldstone, 而是因为 U(1)-symmetric disordered fluctuation 中 angular "direction" 的 BGE 源振幅本身就大。
- 两者都**不 divergent at k→0**, 说明 massive; 进一步 quantitatively fit。

### 2.3 Low-k fit 结果: m_θ² 数值 + 拟合质量

**模型**: S(k) = A / (D k² + m²), D=0.1 固定。

**aggregated avg fit (70 docs 平均后 fit)**:

| fit window | m_θ² | A | R² |
|---|---|---|---|
| k_max=4 | 0.02042 ± 0.00714 | 8.06e+04 | 0.965 |
| k_max=6 | 0.01631 ± 0.00588 | 7.00e+04 | 0.959 |
| k_max=8 | 0.01485 ± 0.00509 | 6.62e+04 | 0.959 |

| fit window | m_ρ² | A | R² |
|---|---|---|---|
| k_max=4 | 0.10718 ± 0.01014 | 4.36e+01 | 0.991 |
| k_max=6 | 0.09005 ± 0.00926 | 3.77e+01 | 0.987 |
| k_max=8 | 0.07726 ± 0.01066 | 3.34e+01 | 0.976 |

**per-doc fit (k_max=6, 统计 70 docs 分布)**:

| mode | median | mean | std | 5%ile | 95%ile |
|---|---|---|---|---|---|
| m_θ² | 0.01654 | 0.01743 | 0.00694 | 0.00846 | 0.02634 |
| m_ρ² | 0.09181 | 0.10431 | 0.05107 | 0.03701 | 0.20742 |

**稳定性**: m_θ² 在不同 k_max 下 ~0.015-0.020, 拟合 R² ≈ 0.96, 相对 consistent。分布 95%ile 的上界 0.026, 仍远小于临界 0.949。

### 2.4 Sanity check S_ρ(k) 拟合 radial mass — **与理论不符**

**预期**: m_ρ² ≈ 4 (Mexican-hat V''_radial = 8v² = 8 对 |ψ|² 或 4 对 ψ linearization, 见 A1 §3.1)。
**实测**: m_ρ² = 0.09 ≈ 1/44 × 预期值。

**两种可能解释**:

1. **(方法论)** fit 给的 m² 绝对值受 A normalization 影响。在 equipartition Langevin 下 A = T (temperature), 但 Phase B Exp 1 是 deterministic (无 thermal noise), A 由 driving + feedback 能量平衡决定, 不固定。因此 m² 的 "**比值**" (m_θ²/m_ρ² ≈ 0.18) 与 "**absolute comparison to V''**" 不直接可比。

2. **(物理)** 系统 far from Mexican-hat minimum (|⟨ψ⟩| ≈ 0, ρ ≈ 1.19 ≠ v). 在 disordered state 下 effective radial mass 由 non-perturbative susceptibility 决定, 可以远小于 V''|_v=1 的 4。

**但对 M3 verdict 的 implication**: m² 作为 "**inverse correlation length squared**" 的物理意义是**坚实的** (propagator pole, independent of A)。M3 positivity 要求 L 在 low-k 给的最小 eigenvalue > ||F_H||_op; low-k eigenvalue 本质就是 Dk²_min + m². 所以实测 m² 直接可用, 与 A1 的 "m_θ² vs ||F||_op 比较" framing 一致。

**另一个 framework-level 问题**: Part 1 假设 L = -D∇² + V''_eff linearized around uniform steady state ψ_∞ = v。实测显示**稳态不是** uniform v, 而是 patched disordered state (Appendix A.3.1 说 50 coherent patches per doc, r_g < 8)。严格 Fréchet linearization around该 patched state 会给**空间非 trivial 的 V''_eff(x)**, 不是 scalar 4。Part 1 的 scalar V''=4 是 simplification。**但**: low-k propagator pole 实测 m² 仍然是 effective L 在 V_0 的最小 eigenvalue proxy (Green's function 的 pole), 所以 verdict 方向 robust — 只是 "L_min on V_0" 的 Mexican-hat 表达式不严格成立, 应直接用实测 m²。

---

## 3. M3 verdict

### 3.1 λ_min((L-F)_H on V_0 with measured m_θ²) 数值

```
||F_H||_op (实测 eigenvalue) = 0.9525
临界 m_θ² = 0.9487
Dk²_min = 0.00384

λ_min(L on V_0) = Dk²_min + min(m_θ², m_ρ²)
                = 0.00384 + min(0.017, 0.092)
                = 0.00384 + 0.017 = 0.020

λ_min((L-F)_H on V_0) = 0.020 - 0.9525 = -0.9321
```

**即使用 95th percentile 最 favor M3**: m_θ²_hi = 0.026, λ_min((L-F)_H) = 0.030 - 0.953 = **-0.922**。依然负。

### 3.2 verdict: **falsified**

**M3 FALSIFIED**。理由:

1. λ_min((L-F)_H) = **-0.93**, 不 marginal (差 -0.93, 约 ||F_H||_op 的 97%); 这不是 numerical precision 问题。
2. 即使用 95%ile upper bound 的 m_θ², verdict 不变。
3. **pre-committed falsification test (A5 反题姐姐 + A1 §7 [?]5)**: 若 m_θ² < 1.2 → falsify。实测 m_θ² = 0.017, 小于 1.2 **两个量级**。Trigger **触发**, **必须 honor**。

**Linux 纪律 compliance**: 不试 V_0^⊥ projection 加强 (A1 §3.5 option 1), 不试 partial M3 radial-only (option 3)。Honest failure > cushioned success。

---

## 4. 对 arXiv v2 implication

1. **M3 section 完全撤回**。v1 只有 "outlook" 级 mention, 未作 claim; v2 中 M3 不应以 [Proposition] 或 [Conjecture, conditional] 存在。
2. **§5.1 M2 证伪段保持**。
3. **OP1 (Axiom 6 formalization) 回 "open, unresolved"**。之前 M2 → M3 的 "candidate progression" narrative 需要替换为 "探索 M2, M3 两条 route 均失败; OP1 仍然 open; 新的 candidate 需重起"。
4. **新增 "negative result" 报告**: M3 falsification 本身是 contribution (Popperian):
   - A1 给出 rigorous mathematical framing (Hermitian part, 非自伴, Goldstone 软模)
   - A2 empirical verify 从 Phase B Exp 1 数据提 m_θ² = 0.017 << threshold 0.95
   - 结论: b+c feedback 架构 ||F_H||_op ≈ 0.95 过强, 把 V_0 子空间上最软 mode 推成不稳定
   - 物理意义: Axiom 6 "matching = self-training" 在 current α=0.1, β=0.05 参数下**超过** critical strength — 可能 suggests 需要 **parameter scan 找 stability boundary** (这是 Phase B 后续 experiments 的 natural motivation)
5. **Block V 优先级提升**: 潜在的 remedy (M3 救援, 不在本 action scope) 在于 reduce feedback strength 或找 sub-critical α, β。这与 Phase B §A.9 "parameter robustness" 一致。

### Alternate framing (honest, 不 save M3)

Negative result 的 positive vein: **实验揭示 current parameter 超临界**, M3 的 rigorous form 不能 close 因为系统实际处于**不稳定 sub-regime** in (α, β) space。**这不是 M3 数学框架的失败**, 而是 specific parameter 的 feedback-strength 选择失败 — 把稳态推出了 "L-F 正定" 的区间。发现这一点本身就是有价值的 empirical finding, 并提供 Phase B 后续 follow-up 的 quantitative target: 需要 α, β 小到 ||F_H||_op < m_θ²_measured ≈ 0.017。

**但**: 此 alternate framing 不 save 当前 M3 claim; 它只是给出下一步方向的 hint。当前 claim 严格 falsified。

---

## 5. 剩余 open problems

1. **稳态结构**: 实测稳态是 U(1)-symmetric disordered state (⟨ψ⟩ ≈ 0), 不是 Mexican-hat SSB minimum。linearization around该 state 的 rigorous theory 需要 replace A1 framework。具体: V''_eff(x) 是空间非 trivial, 以及 effective Laplacian 应 fold 进 patch structure (50 patches, r_g<8)。这个 "linearization around non-uniform patched NESS" 可能要用 large-N / replica / Wilsonian effective action, 不在 scope。

2. **m² 绝对值 sanity**: S_ρ 实测 m_ρ² = 0.09 远小于 Mexican-hat V'' = 4。本 action 用 "m² = low-k propagator pole" 的物理意义做 verdict 是 robust 的 (不依赖 A normalization), 但 framework 与 A1 的 "linearize around uniform v" 有 gap。若要 reconcile, 需要独立 Phase C task: 在 non-uniform patched state 上做 Fréchet linearization, 实测 V''_eff(x) 谱。

3. **non-equilibrium steady state 的 Gaussian ansatz**: low-k fit 假设 Gaussian field + equipartition。deterministic driven system 是否 satisfy 仍然 open; R² ≈ 0.96-0.99 说 fit 质量很高, ansatz 不算 wildly off。

4. **history decay + time-space tensor product**: Part 1 用 L⊗I_t - α I - β K 的 tensor product spectrum formula, 对 infinite-time L² 严格。实际 MaoField 是 N_hist=100 finite window + causal only, edge effect 未分析 (A1 §7 [?]4)。但因为实测 ||F_H||_op = 0.953 (用实 K_mat eigenvalue), 这个数值已经 captures finite-window 的 effective operator norm, 不是 idealized。

5. **OP1 的 future candidate**: M3 失败后 OP1 重新 open。可能方向: (a) 完全放弃 "b+c feedback linear operator" framing, 改用 variational 或 fixed-point principle; (b) 弱化 α, β 找 sub-critical 参数; (c) 换一类 feedback 结构 (非 causal memory)。这是 one-yifan level 决策, 不 agent 内部给。

---

## 6. 自检: assumption 清单

1. [?] Part 1 的 tensor product spectrum formula (λ_min(A_H) = λ_min(L) - λ_max(F_H)) 假设 L 和 F_H 在可分离 space/time 空间上 **可交换 tensor**。严格讲, F 只作用于 time, L 只作用于 space; 可交换成立。但 multi-scale integrator 的三时间尺度混合可能 break 这个干净分离 (A1 §7 [?]6 也 flag 了)。本 analysis 假设 Δt=1 (outer tick) 是 effective time unit, 单 scale。

2. [?] low-k fit model S(k) = A/(Dk² + m²) 假设 Gaussian field + Langevin equipartition 或 overdamped linear response。实测 R² = 0.96-0.99 说 fit 质量可以, 但 Phase B Exp 1 是 deterministic driven, 不严格 Langevin。m² 的 physical interpretation 为 inverse correlation length² 坚实, absolute scale 与 V'' 对应不直接。

3. [?] m_θ² 和 m_ρ² 分离假设 polar decomposition 的 angular/radial mode 独立 propagate。对 Mexican hat SSB state 成立 (tangent/normal 分开), 对 disordered state (本实验实际 state) **解耦 approximate**, 可能有 mixing。**实测** radial vs angular variance ratio ≈ 1.05 (doc 0), 说明两者 variance **对称**, 解耦假设大致 OK 但非严格。

4. [?] 稳态判定: t_sim = 50, dS/dt ~ 10⁻⁵ (Appendix §A.3.2)。这是 quasi-steady, 不严格 steady。但 snapshot 已经 5 量级远离 transient, 对 spectrum 分析 adequate (A1 §3.1 框架也只要求稳态 snapshot)。

5. [?] 70 docs 是 NFCorpus 抽样, 每 doc 一个 distinct BGE embedding 作 S_0。per-doc m_θ² 分布 spread (std/mean ≈ 40%) 说明 S_0 strength 影响很大。但 **95%ile 上界仍 0.026**, 距离临界 0.949 还差 35×。所以 verdict 对 document-level variation robust。

6. [?] 本 analysis 默认 ||F_H||_op 可以直接比 λ_min(L), 但这是 tensor product + Hermitian part 的 worst-case bound。实际 A = L⊗I - F 的 Hermitian part eigenvalue 还可以用 L 和 -F_H 的 interleaving (Weyl inequality), 给更紧的 bound。但 worst-case bound 给 verdict 方向不变 (因差距量级 -0.93, 不是 marginal 差距), 不影响 verdict。

7. [?] Pre-commit test "m_θ² < 1.2 → falsify" 来自 A1 §7 [?]5 的猜数 (1.2 = F_op_bound + ε marginal estimate)。真实临界从 Part 1 算出是 **0.949** (用 F_H eigenvalue), 比 1.2 松。用 0.949 threshold, verdict 仍然 FAIL (实测 0.017 < 0.949 by 55×)。所以 falsification 对 threshold 选择 robust — 不是 test 过严。

---

## 7. 一凡 04-20 对齐用 exec summary (3 句)

**M3 严格 falsified**: 从 Phase B Exp 1 数据实测 pseudo-Goldstone mass m_θ² = 0.017 (median, 70 docs), 远小于 M3 正定性临界 0.95 (从 ||F_H||_op 实测 eigenvalue 导出)。λ_min((L-F)_H on V_0) = **-0.93**, 负定接近 ||F_H||_op 整数量级, 不是 marginal。**结论: OP1 回 open, M3 从 A1 给的 [Conjecture, conditional] 现在 **[Falsified]**; arXiv v2 不应以任何形式 claim M3, 下一步方向要么 parameter scan 找 sub-critical (α, β), 要么完全换 Axiom 6 formalization 框架。**

---

## 附: 可复现 commands

```bash
source /home/amd/HEZIMENG/legal-assistant/.venv/bin/activate

# Part 1: spectrum verify
python /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/scripts/A2_spectrum_verify.py

# Part 2: m_theta extraction
python /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/scripts/A2_mtheta_extract.py

# Part 2 diagnose (additional sanity checks)
python /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/scripts/A2_diagnose.py

# Part 3: final verdict
python /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/scripts/A2_final_verdict.py
```

outputs:
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/ACTION2_figures/spectrum_summary.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/ACTION2_figures/spectrum_verify.png`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/ACTION2_figures/mtheta_extract_summary.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/ACTION2_figures/mtheta_spectrum.png`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/ACTION2_figures/diagnose.png`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/ACTION2_figures/final_verdict.json`

---

*— A2 algo-verify subagent (Opus 4.7 xhigh), 2026-04-18, Linux Claude dispatch, Action 2 交付*
