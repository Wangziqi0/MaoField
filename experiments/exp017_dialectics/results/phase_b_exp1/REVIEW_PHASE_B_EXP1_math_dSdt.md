# REVIEW_PHASE_B_EXP1_math_dSdt.md — 2026-04-15

Reviewer: math-review subagent (independent). Scope: Seifert-style dS/dt
in `engine.rs::entropy_production_rate` (Phase B Exp 1, block_v).

## Summary verdict

**存疑 (conditional pass)**. Linux 公式 dS/dt := ⟨|∂_t ψ|²⟩ 作为
"deterministic dissipation power" 在数学上 **well-defined 且非负**，
对 γ=1 isothermal 情形与 Seifert (2005) 的 medium EP rate 差一个
温度常数 β=1/T (Exp 1 设 T=1 故数值一致)。但作为洞见 2-3
("开放耗散 dS/dt > 0 sustained") 的 Pass/Fail 判据只在
**S(x,t) 非平凡时变** 条件下有意义；若反馈使 (ψ, S) 共同收敛到
不动点，dS/dt → 0 是梯度流的数学必然，不能证伪洞见。Verdict
书写建议把 Pass 阈值明确为 "late-window ⟨dS/dt⟩ 相对 early-window
不衰减到 < ε_fp"，并要求同时报告 `source_l2(t)` 判定 S 是否时变。

## Derivation audit

### 1. Seifert framework 适用

对 overdamped Langevin  γ ∂_t x = F(x,t) + η,  ⟨η(t)η(t')⟩ = 2γT δ(t−t')，
Seifert (2005, PRL 95 040602) 定义 medium entropy production rate

  σ_med(t) = ⟨ F ∘ ẋ ⟩ / T        (Stratonovich)

其中 ẋ = γ⁻¹(F+η)。在 deterministic limit η→0：ẋ = F/γ，故

  σ_med = ⟨F · F/γ⟩ / T = ⟨F²⟩ / (γT) = (γ/T) · ⟨ẋ²⟩.

Linux 计算 ⟨|RHS|²⟩ 其中 RHS = ∂_t ψ（γ 已吸收进 EOM，即 γ=1）：

  dS/dt_Linux = ⟨|∂_t ψ|²⟩ = ⟨F²⟩ = (γT) · σ_med = T · σ_med   (γ=1).

**(a) 等价性**: γ=T=1 下 dS/dt_Linux ≡ σ_med（Seifert medium EP）
的数值。正确。
**(b) EP vs dissipation power**: 严格讲 ⟨F·ẋ⟩ 是 **dissipated power** P_diss，
`σ_med = P_diss/T`。量纲：[σ_med] = k_B/s, [P_diss] = J/s。两者差 1/T。
Linux 注释说 "dS/dt" 但实际量是 P_diss (γ=1 下)；isothermal T=1 单位选取
二者同数值，但 "entropy production" 的命名应标注 "in units of k_B T"。
**(c) 复场分解**: 写 ψ = a + ib, 视 (a,b) ∈ ℝ² 为实自由度。
Wirtinger 导数 ∂V/∂ψ* = (|ψ|²−v²)ψ 对应 F_a = −∂V/∂a = −2(|ψ|²−v²)a,
F_b = −2(|ψ|²−v²)b (含扩散项同理)。故

  |∂_t ψ|² = (∂_t a)² + (∂_t b)²  ✓

此即 Linux 的 `ra² + rb²`。复场 EP 的这种 real-representation 是
标准做法 (see Aron et al. 2016, J. Stat. Mech. on MSRJD for complex fields)，
**正确**。

### 2. Gradient flow 无噪声下 dS/dt → 0 的必然性

纯梯度流 (S=0) ∂_t ψ = −δF/δψ* 下 dF/dt = −⟨|∂_t ψ|²⟩ ≤ 0，
Lyapunov 函数论保证 ψ → 临界点，dS/dt → 0。**这是定理，不是洞见 2-3
被证伪**。

Exp 1 有 S(x,t) 含 b+c 反馈。关键判据：
- 若反馈 map Φ: ψ ↦ S 连续且其 fixed-point set 非空，且能量 F̃[ψ] =
  F[ψ] − ⟨ψ,S[ψ]⟩ 仍 bounded below（Lax–Milgram 类条件），则
  augmented gradient flow 仍收敛 → dS/dt → 0。
- 若反馈引入 **non-variational** 分量（S 不能写作某 F̃ 的变分梯度），
  系统可存在极限环或奇异吸引子，此时 sustained dS/dt > 0 成立。
  数学上需验证 curl_ψ S ≠ 0（即 δS_a/δb ≠ δS_b/δa）。

**建议**: verdict 应要求检验 `source_l2(t)` 和 `curl(S)` 是否在 late
window 非零；否则 dS/dt > 0 的 "sustained" 判据无物理意义。

### 3. Sign convention

Linux 返回 Σ(ra²+rb²)/N ≥ 0 by construction。与 Seifert σ_med ≥ 0
(second law, ensemble average) 符号一致。**正确**。注：instantaneous
σ_med 可为负（单轨迹 fluctuation theorem），但此处为空间平均
(等价 ensemble average in ergodic assumption)，始终 ≥ 0。

### 4. Complex field EP decomposition

见 §1(c)。补充: 若追求 U(1)-symmetric formulation,
可写 σ = 2 Re⟨(∂_t ψ)* (∂_t ψ)⟩ = 2⟨|∂_t ψ|²⟩，差一个 factor 2
（Wirtinger 约定）。Linux 用 (∂_t a)²+(∂_t b)² = |∂_t ψ|² 未带 factor 2,
内部一致即可，不影响 monotonicity 判据。若与文献绝对值对比需注明约定。

## Taskbook §2 公式 vs Linux 实现 对比

Taskbook: `dS/dt = ∫ (∇V·∇ψ)² / γ dx + noise term`.

**(a) physical sense**: 存疑。若 ∇V 为 **空间梯度** ∇_x V(ψ(x))，
则 ∇_x V = (∂V/∂ψ)∇ψ + (∂V/∂ψ*)∇ψ*，与 ∇ψ 同阶，`(∇V·∇ψ)²` 是
四阶梯度量，量纲不对 (见 b)。若 ∇V 为 **变分导数** δV/δψ，则
∇V 与 ∇ψ 不同空间的对象，点积无定义。两种解读都 **non-standard**。
**(b) 量纲**: Seifert 标准 σ 量纲 [F²/γ] = [energy²/length²·time/mass]
(对 particle Langevin)。对 field theory, ⟨|∂_t ψ|²⟩ 量纲
[ψ]²/[t]² × volume⁻¹。Taskbook 公式 (∇V ∇ψ)²/γ 量纲
[V]²[ψ]²/[L]⁴/γ，与 ⟨|RHS|²⟩ 在 γ,D=1 且 V ~ ψ² 时 **仅在 potential-dominated
regime 巧合**，一般不等。
**(c) 若 ∇V = ∂V/∂ψ**: 则 `(∂V/∂ψ)·∇ψ = ∇_x V` (chain rule)，公式退化为
`⟨|∇_x V|²⟩/γ`。这对应 **纯势能梯度流 without diffusion** 的耗散率，
丢失 Laplacian 和 source 贡献，**不完整**。
**(d) noise term**: 无噪声 Exp 1 该项为 0，ok。

**结论**: Taskbook §2 公式存在符号歧义，三种解读无一与 Seifert 标准
|∂_t ψ|² 完全等价。**建议以 Linux 实现 (Seifert standard) 为准**，
taskbook 公式作为近似或特例注解。这与一凡定夺一致。

## Blocking / non-blocking 分类

| Issue | Severity | Blocking? |
|---|---|---|
| γ=T=1 单位未显式声明 | low | no |
| "entropy production" 命名 vs P_diss | low | no (注释加说明即可) |
| S(x,t) 时变性未强制验证 | **medium** | **yes for verdict logic** |
| Taskbook §2 公式歧义 | medium | no (以 Linux 为准) |
| Factor-2 Wirtinger 约定 | low | no |
| curl(S) ≠ 0 作为 non-variational 判据未测 | medium | no (nice-to-have) |

## Recommendations to verdict

1. 在 verdict 明确声明 "dS/dt 按 Seifert-standard σ_med (γ=T=1 units)
   即 ⟨|∂_t ψ|²⟩" — 避免与 taskbook §2 公式混淆。
2. 洞见 2-3 Pass 条件修订为 **双阈值**:
   (i) late-window mean(dS/dt) > ε_pass,
   (ii) source_l2(t) in late window 非 constant (time-variation > ε_S),
   否则系统只是 relaxation, dS/dt → 0 是定理必然。
3. 报告 dS/dt(t) **曲线**（不仅均值），check monotone decay vs oscillation。
   Oscillating 才是真正 non-equilibrium steady state。
4. 可选 (P1): 测 ⟨F_a·∂_b S_a − F_b·∂_a S_b⟩ 作 non-variational indicator。

## References

- U. Seifert, PRL 95, 040602 (2005) — medium entropy production rate for
  overdamped Langevin.
- U. Seifert, Rep. Prog. Phys. 75, 126001 (2012) — review, complex
  order-parameter extensions.
- L. Peliti & S. Pigolotti, *Stochastic Thermodynamics: An Introduction*
  (Princeton, 2021) — chap. 4 on deterministic limit, EP vs dissipation
  power distinction.
- C. Aron, G. Biroli, L. Cugliandolo, J. Stat. Mech. (2016) P053207 —
  MSRJD / real-representation for complex fields.
- J.-L. Barrat & L. Berthier — gradient flow Lyapunov convergence (classical).
