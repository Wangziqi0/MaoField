# Win 半成品 — §3 稳态叙事 Mexican-hat SSB → U(1)-symmetric disordered NESS v2

**作者**: Win 姐姐（04-18 晚 → 04-19 新会话）
**日期**: 2026-04-19
**给**: Linux 姐姐（数字 + 两条 acknowledgment spot-check）+ 一凡（narrative final）
**base**: `LINUX_TO_WIN_SECTION3_NESS_RAW_20260419.md` + `ACTION2_M3_EMPIRICAL_VERIFY_20260418.md`
**状态**: 半成品，**未 apply** 到 `arxiv_v1_full.md`。**最大工程**，请 Linux + 一凡仔细 review。
**guardrail**: Action 1 §5 pre-commit 4 (Framing 不 upward ratchet without empirical basis) — **本 half 最容易踩红线的一份**

---

## 1. 改动范围总览

### 不碰（Linux binding §6）

- §3.1 PDE core equation: γ∂_tψ = D∇²ψ − ∂V/∂ψ* + S + η — 不改
- §3.2 7 axioms statements — 不改（仅 Axiom 6 **realization status** 的 annotation 由 §5.1 处理）
- §3.3 source-attractor adjunction — 不改（Lawvere adjoint 结构 independent of NESS vs SSB）
- §3.A Wirtinger appendix — 不改

### 要改写（Linux raw §1 明示）

- **§3.1 末段** ("symmetry-breaking setup" 引入)
- **§3.5 整个 subsection** ("Mexican hat U(1) → pseudo-Goldstone via explicit breaking" 叙事)

### 可能微调（Win judgment）

- §3.4 OP2 描述末段 — 只改 "Mexican-hat groundstate" phrase，保留 OP2 数学内容

**Win judgment on structural 选择** (Linux narrative question 1):
**内嵌式修改**（不新增 §3.6）。理由：
- 避免章节 bloat（NESS 是 §3 现有 setup 的重述，不是新概念引入）
- 新增 §3.6 会让读者以为 "NESS is a new framework on top of §3.1-§3.5"——那就是 framing upward ratchet（§3.6 "Non-equilibrium steady state in MaoField" 的 title 本身就带 paradigm claim 暗示）
- 内嵌式（§3.1 末段 + §3.5 改写）保持 §3 skeleton 不变，只更新 empirical-level 描述

---

## 2. §3.1 末段 proposed text

### v1 原文（sketch, Win 没 Linux source of truth 原文, 语气 approximation）

> The PDE in (3.1) is expected to admit a family of stationary solutions ψ_∞(x) parameterized by the source field S₀(x). Under mild coupling and double-well V(ψ) with broken U(1) symmetry near the source's preferred direction, these stationary solutions realize a Mexican-hat-type symmetry breaking: radial mode gapped at V″(v) = 4, angular (pseudo-Goldstone) mode softened by the explicit U(1)-breaking tilt of S₀. Section 3.5 develops this picture.

### v2 proposed text

> The PDE in (3.1) admits a family of stationary solutions ψ_∞(x) parameterized by the source field S₀(x). The empirical character of these stationary states—documented in §4 and most directly in Phase B Experiment 1 (§4.7, Appendix A.3)—is more naturally described as a **driven-dissipative non-equilibrium steady state (NESS)** than as the equilibrium symmetry-breaking picture that the double-well V(ψ) nominally suggests. Section 3.5 reconstructs this picture empirically, contrasting the Mexican-hat spontaneous-symmetry-breaking (SSB) expectation against the observed U(1)-symmetric, spatially patched, disordered stationary-state structure. Key quantities that anchor the empirical picture (inverse correlation length, radial-mode mass, angular-mode mass, radial-mode displacement from the Mexican-hat valley) are introduced there.

### Win narrative judgments 注记

1. **Term choice**: "U(1)-symmetric disordered NESS" first spelled out here, abbreviated later
   - Why not "quasi-disordered": "quasi" 是 cushion 前缀，Linux binding §6 避免任何 softening
   - Why not just "NESS": 缺 U(1)-symmetry 信息
   - Why not "driven-dissipative steady state": 缺 disordered（读者会默认 ordered NESS）
2. **"more naturally described as... than as... equilibrium symmetry-breaking picture that... nominally suggests"** — 对 v1 Mexican-hat framing 诚实 retract ("nominally suggests" 承认 v1 是 nominal expectation, not empirically realized)，不 self-flagellate
3. **"reconstructs this picture empirically"** — 信号 §3.5 是**以 empirical observation 重建 theoretical description**，不是 "propose new theoretical framework"（avoids paradigm upward ratchet）

---

## 3. §3.5 整个 subsection proposed text

### v2 proposed text

> **§3.5 Stationary-state structure: empirical reconstruction**
>
> `[DYNAMIC-EQUILIBRIUM → DYNAMIC-NESS]` *(mode tag transition: v1 described the stationary state as near-equilibrium SSB ground state; v2 describes it as a driven-dissipative non-equilibrium steady state anchored by Phase B Experiment 1 measurements.)*
>
> The double-well potential V(ψ) = |ψ|²(|ψ|² − 1)² in (3.1), taken in isolation, admits a circle of degenerate minima at |ψ| = 1 and nominally predicts Mexican-hat spontaneous symmetry breaking (SSB): a stationary state that picks a preferred U(1) phase, with a gapped radial mode at effective curvature V″(v) = 4 and a massless angular Goldstone mode softened to a small finite mass only by the explicit U(1)-breaking tilt of the source term S₀(x).
>
> The stationary states observed in Phase B Experiment 1 (50 coherent patches per document, r_g < 8, dS/dt plateau at ~10⁻⁶ across 100% of documents) depart from this picture in three quantitative respects.
>
> **(i) No global phase selection.** The per-document complex mean |⟨ψ⟩_x| is ~0.004, three orders of magnitude below the SSB-expected value v = 1. The angular distribution has circular standard deviation 3.29, consistent with a uniform distribution over [0, 2π). The stationary state is **U(1)-symmetric**: the expected symmetry breaking has not occurred.
>
> **(ii) Radial-mode softening far below Mexican-hat expectation.** The low-k propagator-pole fit S_ρ(k) = A/(Dk² + m_ρ²) (D = 0.1 fixed, k_max = 6, R² = 0.99, 70 NFCorpus documents) yields m_ρ² = **0.092** (median). The Mexican-hat prediction V″(v) = 4 (in the same convention where V = |ψ|²(|ψ|² − 1)²/... ; see below) is a factor of **44× larger**. We do not claim a small correction; the observed radial-mode stiffness is **far softer** than the SSB ground-state expectation.
>
> **(iii) Radial displacement away from the Mexican-hat valley.** The radial field statistics give ⟨ρ⟩_x = **1.190 ± 0.001** with σ(ρ)_x = 0.024, corresponding to a mean |ψ|² ≈ 1.416 — the stationary state sits at **~19% larger radius than the Mexican-hat valley v = 1**. The state is not a small fluctuation around the SSB minimum; it is displaced.
>
> Additionally, the radial-to-angular variance ratio σ(ψ_rot.real)/σ(ψ_rot.imag) = 1.05 indicates near-isotropic fluctuations in field space, inconsistent with the strong radial-gapped / angular-soft anisotropy that Mexican-hat SSB would produce.
>
> **Reconstruction.** Together, (i)-(iii) and the isotropy observation characterize the stationary state as a **driven-dissipative non-equilibrium steady state with unbroken U(1) symmetry, supported by spatially patched coherent structure at r_g < 8, and displaced in radial average from the Mexican-hat valley**. The Mexican-hat SSB picture provides a theoretical contrast against which the empirical state is measured; it does not describe the observed dynamics.
>
> **Mass scales and correlation length.** Although the stationary state is not an SSB ground state, the propagator-pole fits yield well-defined masses that carry physical meaning as **inverse correlation lengths** of field fluctuations in the NESS: ξ_ρ = 1/√m_ρ² ≈ 3.3 lattice units for radial fluctuations; ξ_θ = 1/√m_θ² ≈ 7.7 lattice units for angular fluctuations (m_θ² = 0.017 ± 0.007, measured in Action 2). These length scales are robust to the noise-amplitude normalization A (which in a driven-dissipative NESS lacks the equilibrium fluctuation-dissipation identification with temperature): the propagator-pole position is an intrinsic structural quantity, while A carries the driving-strength dependence. The finite ξ_θ — in particular — signals that what a Mexican-hat picture would predict as a massless Goldstone mode is instead a **finite-correlation-length angular fluctuation** in the NESS, a quantitative departure from the equilibrium SSB expectation rather than a rescaling of it.
>
> **Linearization caveat.** The rigorous Fréchet linearization of the PDE around ψ_∞(x) takes place around a **spatially non-uniform, patched** configuration rather than around the uniform Mexican-hat groundstate ψ_∞ = v assumed in v1. The effective curvature V″_eff(x) is consequently **spatially non-trivial**, not the scalar 4 that uniform linearization would give. The radial-to-angular separation used in §3.5 and in the linearized operator analyses of §5.1 and Appendix A1 holds approximately — the observed variance ratio 1.05 indicates only mild coupling between the two — but is an approximation to, rather than a rigorous decomposition of, the full spatially non-uniform stationary state. Section 5.1 addresses the implications of this non-uniformity for the Axiom 6 formalization programme.
>
> **Remark on the philosophical content.** The stationary state's departure from Mexican-hat SSB does not bear on the philosophical content of Axioms 1–7 (§3.2): those axioms specify structural requirements on the source-attractor map and its fixed-point content, not on whether the specific PDE (3.1) realizes those requirements via SSB or via disordered NESS. What the empirical stationary-state structure does constrain is the class of candidate **mathematical** formalizations of Axiom 6 that proceed by linearizing around a Mexican-hat groundstate; see §5.1 for the falsification of M3 on this basis and for the resulting status of Open Problem 1.

### Win narrative judgments 注记

1. **2 条 acknowledgment 强制要求**（Linux raw §5 binding）:
   - **"factor of 44× larger"** ← m_ρ² = 0.092 vs Mexican-hat V″=4, 显式 acknowledge, 不 hide, 不 round to "order of magnitude smaller"
   - **"~19% larger radius than the Mexican-hat valley v = 1"** ← ⟨ρ⟩ = 1.190 偏离谷底，显式承认**不是谷底附近 noise** ✓

   两条 binding 都写入，不 soften。

2. **"We do not claim a small correction... far softer than the SSB ground-state expectation"** — 显式 preempt "是不是 M_ρ² 只是 quantitative correction" 的 reading

3. **Mode tag**: `[DYNAMIC-EQUILIBRIUM]` → `[DYNAMIC-NESS]` — 新 tag value 在 v1 `feedback_mode_tags.md` 里没有，Linux 姐姐 spot-check 确认 tag 值。若 feedback_mode_tags.md 只有 `[DYNAMIC-EQUILIBRIUM / -RARE-EVENT / -IMPLEMENTATION]`，可改为 **`[DYNAMIC-IMPLEMENTATION]`** (因为 NESS 是 specific dynamics implementation) 或新建 `[DYNAMIC-NESS]`（归 Linux 判）

4. **"reconstruction"** 作 §3.5 subsection 子标题 — 信号 "empirical reconstruction of what v1 nominally predicted"，不是 "new theoretical framework introduced"。**不 upward ratchet** 核心机制

5. **"inverse correlation length" 取代 "Goldstone mass"** — Linux raw §3.2 明确：*"m² 作 inverse correlation length² (物理意义 robust, 不依赖 Mexican-hat 假设)"*. Win prose 直接引此物理 grounding, 读者不会以为 m_θ² 仍然是 "near-massless Goldstone"

6. **"finite-correlation-length angular fluctuation" phrasing**: 不说 "pseudo-Goldstone" （因为 Goldstone 不存在 — no SSB），但显式 cross-link 到 Mexican-hat picture 的 massless-Goldstone 期望，让读者看见**对应关系 + empirical mismatch**。Linux raw §4 question 4: "pseudo-Goldstone 语言是否完全删除?" — Win decision: **删除 "pseudo-Goldstone" phrasing itself, 但保留 Mexican-hat / Goldstone 概念作为对比框架**

7. **Linearization caveat 段**: coordinate §5.1 的 "linearization around uniform ψ_∞=v" 假设，诚实 acknowledge §5.1 M3 分析用的 uniform linearization 是 approximation。这段也让 §5.1 "λ_min = −0.93 on V_0" 的判定更 defensible (approximation 但 direction robust, 不是 Mexican-hat ambiguity artifact)

8. **"Remark on philosophical content"** 末段: coordinate §5.1.4 + §6.1 Diff Point 1 "philosophical content retained / mathematical realization sought" twin. 在 §3 内部**显式声明**：stationary-state empirical 结构不动 philosophical Axioms, 只 constrain mathematical realization 候选. 这是**三处 coordination 最关键 anchor**

9. **"spatially patched coherent structure at r_g < 8"** — 显式 incorporate Phase B Exp 1 Appendix A.3.1 的 50 patches finding, 让 §3.5 的 "disordered NESS" 描述不与 "50 coherent patches" 矛盾 (NESS 可以 at field level disordered 同时 at real-space level patched — 这是重要 nuance)

10. **Upward ratchet check**: 
    - §3.5 内 **没有** 任何 "novel paradigm" / "new framework" / "this opens a new class of..." 等 claim
    - §3.5 的 framing 是 "empirical reconstruction of the stationary state structure that v1 nominally predicted via SSB but is in fact NESS"
    - "Mass scales and correlation length" 段虽然把 NESS + propagator pole 写得比较 rich，但**全部挂在 empirical measurement** (Action 2 §2.3)，不 claim NESS theory 是"for this system, the right theory"
    - 任何读者会读出的 implicit "new direction" 都落在 **§5.1.4 候选方向 generic list**（我们没 commit leading candidate），不在 §3.5 内部
    - ✓ no upward ratchet

---

## 4. §3.4 OP2 描述末段微调

### 仅改 1 个 phrase

v1 §3.4 OP2 描述末段（Win 从 Linux raw 推 v1 原文 approximation）含:
> "...the gradient-flow descent from generic initial conditions cannot realize the full dialectical motion to the Mexican-hat groundstate..."

v2 改为:
> "...the gradient-flow descent from generic initial conditions cannot realize the full dialectical ascent across the barrier separating the initial regime from the distant attractor basin at |ψ|² ≈ 4 (cf. Appendix §4.A1 barrier height 13.2 ≫ initial kinetic energy 1)..."

**不 mention "Mexican-hat groundstate"** (因为观察到的 stationary state 不是 groundstate), 但 OP2 的数学内容 (barrier 13.2 >> 1, gradient flow 不够) 保留不变 ✓

**Note**: 本 phrase 仅是 Win 推测 v1 有此 phrase. 若 v1 §3.4 OP2 末段实际没有 "Mexican-hat groundstate" phrase, 本 §3.4 微调跳过. Linux spot-check 查 v1 `arxiv_v1_full.md` §3.4 原文验证.

---

## 5. 不做的事（Linux binding + Win 补充）

- ✗ **不**重写 §3.1 PDE core equation
- ✗ **不**重写 §3.2 7 公理
- ✗ **不**删除 §3.3 source-attractor adjunction
- ✗ **不**修改 §3.A Wirtinger appendix
- ✗ **不**在 §3 做 α/β/γ 合题决策
- ✗ **不**把 NESS 升格为 "novel paradigm for semantic dynamics" / "new framework for dialectical computation"
- ✗ **不** pick leading candidate direction for Axiom 6 re-formalization（归 §5.1.4 generic list）

**Win 补充**：
- ✗ **不** cite Friston 2000s variational posterior 类比（Linux forward 给一凡时用过，Linux raw §2 明示 "Win 姐姐的 take: 类比是 Linux 的, 姐姐先不用"）
- ✗ **不**在 §3 显式 name Popperian / Lakatosian methodology（归 §5.1.4 + §6.3）
- ✗ **不**把 m_ρ² = 0.092 叙为 "consistent with a weakly coupled near-Gaussian NESS" 等过度 interpret —— 数字是数字，interpretation 留给未来 study

---

## 6. 数字 binding + 两条 acknowledgment 强制要求 spot-check 清单（给 Linux）

### 核心数字 binding

| 数字 | Linux binding | Win prose | ✓ |
|---|---|---|---|
| ⟨ρ⟩_x | **1.190 ± 0.001** | "⟨ρ⟩_x = 1.190 ± 0.001" | ✓ |
| σ(ρ)_x | **0.024** | "σ(ρ)_x = 0.024" | ✓ |
| \|⟨ψ⟩_x\| | **~0.004** | "~0.004, three orders of magnitude below the SSB-expected value v = 1" | ✓ |
| θ circular std | **3.29** | "circular standard deviation 3.29, consistent with a uniform distribution over [0, 2π)" | ✓ |
| radial/angular variance ratio | **1.05** | "σ(ψ_rot.real)/σ(ψ_rot.imag) = 1.05" | ✓ |
| m_ρ² (median) | **0.092** | "m_ρ² = 0.092 (median)" | ✓ |
| m_ρ² (95%ile) | 0.207 | (not used in §3 prose, 归 §5.1 if needed) | — |
| m_θ² (median) | **0.017** | "m_θ² = 0.017 ± 0.007" (prose 中 cross-ref to Action 2 / §5.1) | ✓ |
| 50 patches, r_g < 8, dS/dt ~10⁻⁶ plateau 100% docs | 保留 | "50 coherent patches per document, r_g < 8, dS/dt plateau at ~10⁻⁶ across 100% of documents" | ✓ |
| Correlation length ξ_ρ, ξ_θ | computed from 1/√m² | "ξ_ρ = 1/√m_ρ² ≈ 3.3 lattice units... ξ_θ ≈ 7.7 lattice units" | ✓ |

### Two Acknowledgment 强制要求（Linux raw §5 double-star binding）

1. **m_ρ² 差 Mexican-hat V″ = 4 by 44×**
   - Win prose 原话: *"a factor of **44× larger**"* + *"We do not claim a small correction; the observed radial-mode stiffness is **far softer** than the SSB ground-state expectation."*
   - ✓ acknowledge 强度足够, 不 hide 不 soften

2. **⟨ρ⟩ = 1.190 > v = 1 意味偏出谷底 ~19% radius, 不是 "谷底附近 disordered noise"**
   - Win prose 原话: *"⟨ρ⟩_x = 1.190 ± 0.001... corresponding to a mean |ψ|² ≈ 1.416 — the stationary state sits at **~19% larger radius than the Mexican-hat valley v = 1**. The state is not a small fluctuation around the SSB minimum; it is displaced."*
   - ✓ acknowledge 强度足够, 显式声明 "not a small fluctuation around the SSB minimum; it is displaced"

**0 处 hide, 0 处 round to "roughly", 0 处 "谷底附近"-style softening**。

---

## 7. 协调 check（§4.11 + §5.1 + §6.1 → §3）

- **§4.11.1 P3**: §3 不涉及 Kramers / inner-outer barrier, 完全正交 ✓
- **§5.1 M3 falsification**: 
   - §3.5 "Mass scales and correlation length" 段使用 m_θ² = 0.017 和 §5.1 binding 数字一致 ✓
   - §3.5 "Linearization caveat" 段显式 acknowledge §5.1 linearization 是 approximation around patched state, 不 undermine §5.1 M3 falsification (approximation direction robust, Linux raw §2.3 已 established 这点 — m² as inverse correlation length² 物理 robust 不依赖 Mexican-hat)
   - §3.5 "Remark on philosophical content" 显式与 §5.1.4 / §6.1 Diff Point 1 twin "philosophical content retained / mathematical realization sought" 协调 ✓
- **§6.1 Claimed / Not Claimed**: §3 不直接 touch §6.1 bullets, 但 §3.5 "NESS as empirical observation" 语气与 §6.1 "mathematical realization sought" 语气 phrasing-level 一致 ✓

**Upward ratchet self-check**（**最重要**）:

| 潜在 upward ratchet 诱惑 | §3.5 Win prose 实际处理 | 结果 |
|---|---|---|
| "NESS as novel paradigm" | 不提 "paradigm" 词; 用 "empirical reconstruction" | ✓ 避免 |
| "SPDE theory leading candidate" | 不 mention SPDE at all in §3 | ✓ 避免 |
| "Friston variational posterior analog" | 不 cite Friston | ✓ 避免 |
| "dialectical dynamics revealed to be..." | 用 "driven-dissipative NESS... anchored by measurements" | ✓ empirical level |
| "gradient flow fundamentally insufficient" | 不 扩展 OP2 status; 只 update §3.4 phrase | ✓ 不扩 claim |
| "Mexican-hat SSB ruled out" | 用 "does not describe the observed dynamics" + "is measured against it as contrast" | ✓ empirical only |

**Result**: §3.5 prose 站 empirical level, §5.1 站 falsification + open, §6.1 站 high-level summary + no candidate preview, §4.11.1 站 methodological resolution. **四处 framing-level 全部 bounded, no upward ratchet** ✓

---

## 8. Apply 时机

**建议**:
- **α 保守路径**：直接 apply。α 要求 §3 revise 以反映 M3 falsified + U3 finding，§3.5 v2 half 正是 α 语气（"empirical reconstruction, philosophical content retained, mathematical realization sought"）
- **β 中庸路径**：直接 apply + 可能在 §3.5 末段（"Remark on philosophical content" 之后）加一句 Phase A 候选 conditional experiment (e.g., "Phase A-0 sub-critical parameter scan planned")—但这进入 β 专属 territory, 本 half 不写入
- **γ 激进路径**：可 apply + γ 可能要求 §3.5 显式 upgrade NESS 为 "the primary dynamical regime of dialectical semantic computation"——**但这违反 Action 1 §5 pre-commit 4**, 要 γ 定下后由一凡 + Linux 姐姐共同授权 Win 另出 diff (Win **不 unilateral** 做此 upgrade)

本 half 写的 core prose **α/β 两种路径直接可用**；γ 路径需要 case-by-case authorization。

---

## 9. 给一凡的 narrative question（04-20 对齐或更早）

1. **"driven-dissipative NESS with unbroken U(1) symmetry, supported by spatially patched coherent structure at r_g < 8, and displaced in radial average from the Mexican-hat valley"** — 这是 §3.5 核心定性句。对你有几种可能 reading：
   - (a) **empirical-level description** (Win intended) — "这就是实测到的样子，不 commit 任何 theoretical interpretation"
   - (b) **quasi-paradigm framing** — "NESS 是 MaoField 的 nature" 信号
   - 你判：(a) 语气 OK 还是要 dial back 更保守？如选 (b)，本 half 需要 rewrite（归 γ territory，本 half 不做）

2. **"Remark on philosophical content" 段的二分**——这段 explicit 声明 "philosophical Axioms 1-7 unchanged, mathematical realization constrained"。如果觉得这段把哲学和数学分家分得太干净，可改软化版（见 §6.1 half narrative question 2）

3. **"Mexican-hat valley" 措辞** — 全 §3.5 用 "Mexican-hat valley" / "Mexican-hat SSB picture" / "Mexican-hat groundstate" 三种 phrasing。一凡判：统一到哪一个？Win 倾向保持这三个 phrasing（不 mechanical unified），因为 context 不同（valley = 位置 / SSB picture = 理论预期 / groundstate = v1 linearization 假设）

4. **"reconstruction" 作 subsection 子标题**——你觉得这词够 neutral 吗？备选: "empirical structure" / "observed structure" / "stationary-state measurements"。Win 倾向 "reconstruction"（active verb, 不 passive "observed"）

5. **最大 risk question**: §3.5 这 ~900 词的 prose 如果单独读（不读 §5.1 / §6.1），会不会读成 "MaoField 现在有了一个新 framework (NESS)"? Win 自检 ✗（不会，因 prose 全站 empirical level），但 Linux 数学层 spot-check + 你叙事层 spot-check 请判一次

---

## 10. Linux 姐姐 spot-check 请求

除了 §6 数字 + 两条 acknowledgment checklist 以外：

1. **mode tag value**: `[DYNAMIC-NESS]` 是否在 `feedback_mode_tags.md` 的合法 tag set 里？若没有请建议使用 `[DYNAMIC-IMPLEMENTATION]` 或其他已 established tag

2. **linearization caveat 段 (§3.5) 与 A1 Proposition A1.1 的一致性**: §3.5 "Linearization caveat" 声称 "uniform linearization is approximation to the spatially non-uniform stationary state"; A1 §3.5 的 uniform linearization 处理是否 consistent with 这个 acknowledgment (即 A1 是否 explicitly  标出这一 assumption)?

3. **ξ_ρ ≈ 3.3 lattice units, ξ_θ ≈ 7.7 lattice units** 的数字算正确吗？(1/√0.092 ≈ 3.30, 1/√0.017 ≈ 7.67) ✓ Win 已 verify, 但请 Linux 再 check

4. **§3.4 OP2 末段微调是否需要**——Linux 需 check v1 `arxiv_v1_full.md` §3.4 原文是否确实含 "Mexican-hat groundstate" phrase。若无，§3.4 本 micro-diff 跳过

---

*— Win 姐姐 (04-19)，§3 最大工程 half 完成*
