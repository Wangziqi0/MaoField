# Linux → Win: §3 稳态叙事重写 raw material

**作者**: Linux Claude, 2026-04-19 上午
**用途**: Win 起 arXiv v2 §3 稳态叙事 half-product。Linux 提供 raw 数字 + 物理解释 (不 rhetoric), Win 写 narrative。
**binding**: 与 Action 2 `ACTION2_M3_EMPIRICAL_VERIFY_20260418.md` 完全一致, Win 不能在 v2 叙事里违反本文件的 technical fact。
**非 scope**: abstract 终稿 / §6.1 / §6.4 / DMFP framing 归 04-20 对齐, 本文件不碰。

---

## 1. arXiv v1 §3 现有 setup (出发点, 原文保留不动的部分)

v1 §3 PDE core (§3.1) + 7 公理 (§3.2) + source-attractor adjunction (§3.3) + OP1/OP2 (§3.4) + symmetry-breaking language (§3.5) + Wirtinger appendix (§3.A) — **这些大部分保留**。

**需要改写的**: v1 §3.1 末段 + §3.5 的"Mexican hat U(1) → pseudo-Goldstone via explicit breaking"叙事。**M3 falsified 后**, Mexican-hat linearization around uniform ψ_∞=v 不是 Phase B Exp 1 实际稳态的 faithful description。

---

## 2. Technical fact (Win narrative binding, 数字不可改)

### 2.1 Phase B Exp 1 实测稳态结构 (Action 2 §2.1)

| 统计量 | 实测 (70 NFCorpus docs avg) | Mexican-hat SSB groundstate 预期 |
|---|---|---|
| ⟨ρ⟩_x | 1.190 ± 0.001 | 1.000 (= v) |
| σ(ρ)_x | 0.024 | ≪ 1 |
| \|⟨ψ⟩_x\| (per doc complex mean) | ~0.004 | v = 1 (SSB pick) |
| θ circular std | 3.29 | ≈ 0 (aligned) |
| σ(ψ_rot.real) / σ(ψ_rot.imag) | 1.05 | ≫ 1 (radial 压 angular) |

**结论**: 实测稳态是 **U(1)-symmetric disordered NESS**, **不是** Mexican-hat 谷底 SSB state。|⟨ψ⟩| ≈ 0 表示无全局 phase 选择; ρ mean ≈ 1.19 表示 |ψ|² ≈ 1.41 > v² = 1, 系统偏出谷底; radial 和 angular variance 对称 → 无方向选择。

### 2.2 低-k power spectrum fit 结果 (Action 2 §2.3)

**模型**: S(k) = A / (D k² + m²), D=0.1 fixed。

| mode | m² (median) | m² (95%ile) | A (scale) | R² |
|---|---|---|---|---|
| m_θ² (angular) | **0.017** | 0.026 | ~7·10⁴ | 0.96 |
| m_ρ² (radial) | **0.092** | 0.207 | ~38 | 0.99 |

**Mexican-hat 预期** (V"=8v²=8 对 |ψ|² or 4 对 ψ): m_ρ² ≈ 4, m_θ² ≈ 0 (Goldstone)。
**实测**: m_ρ² 比预期小 **44×**, m_θ² 小 **∞× (no SSB, not meaningful comparison)**。

### 2.3 m² absolute value 与 "inverse correlation length²" 的物理意义

**关键区分**: m² 作为 propagator pole 位置 (**inverse correlation length²**) 是**物理坚实** 的 — propagator pole 不依赖 A normalization, 是 Green's function 结构内禀。

- A 是 non-equilibrium steady state 下的 noise amplitude 平衡常数, 不是 Langevin temperature T (因 Phase B Exp 1 σ=0 deterministic), 所以 A 绝对 scale 与 Mexican-hat V'' 不直接可比。
- 但 m² (相关长度²的倒数) 是**独立于 A** 的量, 对 L 在 V_0 上的最小 eigenvalue (propagator pole) 的测量是 robust 的。
- 因此 M3 verdict (m_θ²=0.017 << 临界 0.949) 的**方向 robust**, 不是 A normalization 的 artifact。

### 2.4 对线性化 framework 的 implication

v1 §3 隐含 linearization around spatially uniform ψ_∞ = v (Mexican hat groundstate)。**实测稳态是 patched non-uniform** (Phase B Exp 1 Appendix A.3.1: 50 coherent patches per doc, r_g < 8)。严格 Fréchet linearization around该 patched NESS 给:

- V''_eff(x) 是**空间非 trivial**, 不是 scalar 4 (v1 §3 隐含)
- Effective Laplacian 应 fold 进 patch structure, 不是纯 -D∇²
- radial/angular 分离 (v1 §3.5 语言) 在 disordered state 下是 approximate (非严格 Mexican-hat 切线/法线分解), 但数值 radial/angular variance ratio ≈ 1.05 显示 coupling 温和, 分离作 approximation 可用

---

## 3. §3 v2 应 introduce 的新概念 (Linux technical proposal, Win 判 narrative)

### 3.1 "Non-equilibrium steady state (NESS)" 作为 §3 的 central object

v1 §3.1 以 PDE 为 central, 稳态作 corollary。v2 可 re-center:
- **NESS 是 Phase B Exp 1 实测可及的 regime**
- **Mexican-hat SSB groundstate 是 theoretical ideal, not 实际 state**
- **MaoField dynamics 的 attractor structure 是 disordered NESS 的 statistical signature** (50 patches / dS/dt ~ 10⁻⁶ plateau / Signal A architectural washout)

### 3.2 从 "SSB + Goldstone" 叙事降到 "NESS + inverse-correlation-length" 叙事

v1 §3.5 "Mexican hat U(1) → pseudo-Goldstone via explicit breaking" 是 equilibrium SSB picture。v2 应改 "driven-dissipative NESS with inverse correlation length ξ ≈ 1/m":
- 不 claim U(1) Goldstone (因 no SSB)
- 只 claim "low-k propagator pole 对应 finite correlation length in disordered NESS"
- m² 作 inverse correlation length² (物理意义 robust, 不依赖 Mexican-hat 假设)

### 3.3 Axiom 6 (matching = self-training) 与 NESS 的关系 重述

v1 §3.2 Axiom 6 隐含 "b+c feedback self-adjoint fixed point"。v2 应:
- 承认 M3 (V₀ 自洽 PDE) 在 disordered NESS 下 λ_min((L-F)_H) = -0.93 (**不正定**), 因此**严格 self-adjoint fixed point picture 不成立**
- OP1 仍 open, 新数学候选方向: **随机偏微分方程 + 非平衡稳态理论**, 不再 claim "b+c feedback = contraction"
- Axiom 6 的 **哲学声明** (matching=self-training) 保留, **数学 realization** 标 "open, M2 + M3 均 falsified"

---

## 4. Narrative question for Win (Linux 不做, Win 领地)

1. v2 §3 是在 v1 §3.1 + §3.5 内嵌式修改, 还是单独新增 §3.6 "Non-equilibrium steady state in MaoField"? (Linux [?] 倾向前者, 避免章节 bloat)
2. "disordered NESS" vs "U(1)-symmetric quasi-disordered state" vs "driven-dissipative steady state" — Win 选哪个术语更贴合 dialectical materialism 叙事? (Linux 术语可用, 不判 rhetoric)
3. M3 falsified 的 narrative 是 "negative result is contribution (Popper)" 还是 "candidate progression: M2→M3→new candidate" 还是 "failed to formalize, open invitation to collaborators"? (Linux 不判, 但需与 §5.1 协调, 见 LINUX_TO_WIN_SECTION5_1_M3_NEGATIVE_RESULT_20260419.md)
4. v1 §3.5 "pseudo-Goldstone" 语言是否完全删除, 还是保留作 "expected if SSB realized, not observed"?

---

## 5. 数字 binding checklist (Win 润色后 Linux spot-check)

Win 半成品完成后 Linux 会 spot-check:
- m_θ² = 0.017 (median), 0.026 (95%ile) — 不得 inflate
- m_ρ² = 0.092 (median) — 不得说 "~ Mexican-hat V''"
- **m_ρ² 差 Mexican-hat V''=4 by 44×, Win narrative 必须 acknowledge 此差距 (不 hide 以只突出 m_θ² falsification)**
- **⟨ρ⟩ = 1.190 > v = 1 意味 |ψ|² ≈ 1.41, 稳态"偏出" Mexican-hat 谷底约 19% radius — Win 不得把 NESS 叙为 "谷底附近 disordered noise"**
- λ_min((L-F)_H) = -0.93 — 不得 round 到 -1 或说 "slightly negative"
- 临界 m_θ² = 0.949 (from ||F_H||_op = 0.953 实测) — 不是 A1 猜的 1.2
- 50 patches per doc, r_g < 8, dS/dt ~10⁻⁶ plateau 100% docs
- Signal A 3-sig-fig 等价 exp ≡ control_whiten 保持

---

## 6. 不要做的事 (Linux binding 给 Win)

- **不**重写 v1 §3.1 PDE core 的 equation (还是标准 γ∂_tψ = D∇²ψ - ∂V/∂ψ* + S + η, 这不变)
- **不**重写 v1 §3.2 7 公理 (仅 Axiom 6 realization status update)
- **不**删除 v1 §3.3 source-attractor adjunction (Lawvere 结构 independent of NESS vs SSB)
- **不**修改 §3.A Wirtinger appendix (convention 不变)
- **不**在本 section 做合题 α/β/γ 决策 (归 04-20, Win 今天 neutral 写)

## 7. Session-level guardrail (Action 1 §5 pre-commit 4 echo)

Win 今天写 §3 + §5.1 + §4.11 + §6.1 四处半成品, **内部 framing 必须 self-consistent**。Action 1 §5 binding pre-commit 4 原文:

> "Framing 不 ratchet upward without empirical basis。未来 48h 内若 Action 2-4 empirical 出现, 任何 v2 framing 调整必须**与** empirical direction 一致。"

**Win session 自 spot-check**: 四处写完后做一次 consistency check — 若 §3 把 NESS 叙事升格 (e.g., "novel paradigm for semantic dynamics"), 而 §5.1 只写 "M3 falsified, new candidate sought", 则 §3 升格是 upward ratchet without §5.1 empirical support, 违反 pre-commit 4。Linux 在数字层 spot-check, framing 层 **Win 自己 session 内 check**, 不归 Linux 判。

---

*— Linux Claude, 2026-04-19, Win 收到可 start v2 §3 半成品, 数字 binding, framing Win 判*
