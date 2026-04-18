# Win Narrative Review — 2026-04-14

**审查员**：Win Claude (Opus 4.6, 1M context)
**范围**：Phase 1 修订后的 a1_4_shifted_potential_analysis.md (v3) + REVIEW_P1-P5 + lawvere_monad_draft (post-P5) + FINAL_REPORT (post-P5)
**判定**：**全部修订 release-ready at position-paper level**。下面给 §2-§5 起草的 narrative-level 输入。

不重新审查数学或术语——subagent 已经做完了，我不重复劳动。我审的是**叙事 coherence、跨章节连接、起草措辞**。

---

## 〇、Bottom Line

**Phase 1 修订完成度评估**：

| 维度 | 评分 | 备注 |
|---|---|---|
| 数学严谨性 | A | 11 处错误捕获 + 修正，全部独立 SymPy/审查双校验 |
| 物理叙事正确性 | A | #7 撤回 + Kramers/Laplace 双框架 + Jacobian 严肃化 |
| 跨文档一致性 | A | a1_4 / lawvere / b1_verdict / FINAL_REPORT / BLOCK_V_DESIGN 措辞统一 |
| Position-paper 严肃度 | A | endofunctor on Meas + Giry lift future work + SSB 5 条脚注 |
| 起草就绪度 | **可起草** | arXiv §2.3 / §3 / §4 / §5 全部 ready |

**最重要的 narrative gain**：#7 + #4 + Lawvere endofunctor 三件事在 Phase 1 修订后**统一到同一个 open problem 框架**——"stochastic / non-equilibrium 扩展"既是 categorical formalization 的入口，也是 OP2 directed-driving 的物理出路，也是 B1 Stage Kramers escape 的现象学解释。三个原本独立的章节现在有共同骨架。

---

## 一、#7 reframe 是 OP2 叙事的重大 narrative gain（不是负担）

### 原叙事（v2 / 之前）
- B1 Stage：σ=0.5 Langevin 在 A1 原势上 → 85% u=0, 0% u=4
- 解释（错）："Langevin 简单失败 / direct relaxation"
- OP2 措辞："Langevin 不行，需要别的非平衡机制"

### 修订后叙事（post-#7）
- B1 Stage：σ=0.5 Langevin 在 A1 原势上**两件事同时发生**：
  - **u=1 → u=0**：Kramers escape 跨越 inner barrier ΔV/T=16，rate × t_sim ≈ O(8×10⁻⁵) 看似小，但**实际上 85% voxels 在 t_sim=250 内已达成**——意味着 inner barrier 在等向 noise 下确实可跨
  - **u=1 → u=4**：Kramers escape time 超出 simulation horizon **~43 orders of magnitude** → 0% occupancy
- 共同诊断：**barrier asymmetry 在 finite simulation horizon 下决定了哪些 basin accessible**
- OP2 措辞（精确化）：**"Langevin 在 high-barrier basin 失败的根因是 simulation horizon vs Kramers timescale 量级不匹配，不是范式限制。两条工程路径：(a) 重构 barrier topology，(b) directed non-equilibrium driving 绕过 timescale problem"**

### 为什么这是 narrative gain

1. **更诚实**：原叙事暗示 Langevin "不行"——其实 Langevin **在 A1 原势的 inner barrier 上工作正常**，它只是在 outer barrier 时程不够
2. **更精确**：从"范式问题"reframe 为"timescale 工程问题 + 真正的范式问题"两层
3. **更可工程化**：OP2 (a) 直接对应 A1.4 实验，(b) 直接对应 Block V V.3 系列 sub-block
4. **paper-narrative 的 unity**：B1 stage 的两个观察（85% u=0 + 0% u=4）现在用同一个机制（Kramers escape time × horizon）解释，不是两个独立现象

### 起草 §4 措辞建议

> "**Stage B1 reveals the role of Kramers timescale.** Under σ=0.5 Langevin (T_eff=0.125), the system exhibits two simultaneous regimes: (i) the inner barrier ΔV=2.0 (ΔV/T_eff=16) is crossed via Kramers escape, driving 85% of voxels from the u=1 basin into the u=0 basin within the simulation horizon; (ii) the outer barrier ΔV=13.2 (ΔV/T_eff=105.5) yields a Kramers escape time exceeding the simulation horizon by **~43 orders of magnitude**, leaving the u=4 basin at 0% occupancy. **The asymmetric outcome is not a paradigm failure of Langevin dynamics — Langevin works for inner barrier — but a timescale mismatch for the outer barrier.** This finding directly motivates the OP2 program: barrier-topology engineering (Section 5.1) and directed non-equilibrium driving (Section 5.2) are two complementary paths to bring distant attractor basins into the simulation horizon."

---

## 二、Lawvere endofunctor + Giry lift + OP2 三事统一（narrative diamond）

### 现状（post-P5）
- 主文 §2.3.2：endofunctor on `C = Meas` (well-defined now via identity-on-complement extension)
- 脚注 ⁵：Giry monad lift `P∘T_•` 继承 (η, μ) 的 future work
- 引用：Giry 1982; Jacobs 2010

### Narrative 三事统一

```
Lawvere categorical 严格化路径
        │
        │ 需要 stochastic 扩展 → Giry monad
        │
OP2 物理路径
        │
        │ 需要 stochastic 非平衡机制 → directed driving / Langevin extension
        │
B1 Stage Kramers 现象学
        │
        │ 需要把 isotropic noise 升级为 directed/anisotropic noise → 同上
        ↓
   ╔════════════════════════════════════╗
   ║ 同一个 open problem 的三个面：      ║
   ║                                    ║
   ║  (1) Categorical: Giry lift        ║
   ║  (2) Physics: directed driving     ║
   ║  (3) Phenomenology: Kramers time   ║
   ╚════════════════════════════════════╝
```

**这是 Lawvere 章节降级带来的意外收获**——本来是被审查员抓出来的 over-claim 修正，现在变成了 unified narrative diamond。

### 起草 §2.3.X 措辞建议（"Why deterministic gradient flow is not a monad"）

> "Deterministic gradient flow `∂_t ψ = −δH/δψ*` is naturally an **R⁺-monoid action** on field space — equivalently, an **F-coalgebra** for the time-translation endofunctor. It does not directly carry monad structure: there is no canonical multiplication `μ: F∘F → F` that satisfies the monad coherence axioms in the deterministic regime.
>
> The standard categorical lift to a genuine monad goes through **stochastic extension**: replacing deterministic flows with Markov kernels yields the **Giry monad** `P` on the category `Meas` of measurable spaces (Giry 1982; Jacobs 2010). We conjecture that the source-attractor endofunctor `T_•` admits a Giry-monad lift `P ∘ T_•` inheriting (η, μ) from the underlying stochastic dynamics. Rigorous formalization is an open problem (see footnote 5).
>
> **Notably, this categorical open problem is not independent of OP2**. The same stochastic extension required for the categorical monad lift is also the physical mechanism (directed non-equilibrium driving) needed to overcome the Kramers timescale obstruction in Stage B1. **Categorical formalization, physical roadmap, and experimental phenomenology converge on the same conjectured stochastic structure.**"

这段落是整个 §2.3 的核心 narrative weapon——让 reviewer 看到这不是"哲学包装数学"，是真正的三层 unity。

---

## 三、Kramers + Laplace 双框架对 §4 措辞的精确路径

### Linux v3 提供的双框架（已 ready）

**Kramers rate × t_sim** (适用 ΔV/T >> 1，事件数论证)：
- A1 原势 outer: ~4×10⁻⁴³ events → 0% u=4
- A1 原势 inner: ~8×10⁻⁵ events → 但实测 85% u=0 ⇒ 说明 prefactor 估计偏低 OR 多维 voxel 统计有 enhancement OR Kramers approximation 在 ΔV/T=16 仍然边际

**Laplace 平衡占据率** (适用 thermalized regime)：
- A1.4 三 basin 配分函数同单位归一化
- 预测：p(0)=0.03, p(1)=0.57, p(2)=0.40

### 起草 §4 措辞建议（双框架 explicit）

> "We employ a **two-regime analytical framework** for occupancy prediction:
>
> 1. **Rare-event regime** (ΔV/T_eff >> 1): occupancy is governed by Kramers escape rate × simulation horizon. Number of expected crossing events ≈ k_{ij}·t_sim. Used for **A1 原势 outer barrier** (ΔV/T=105, ~10⁻⁴³ events, 0% occupancy as observed).
>
> 2. **Thermalized regime** (ΔV/T_eff ≲ 1, system fully mixes within t_sim): occupancy is governed by Laplace-approximated equilibrium distribution `p_k ∝ Z_k = √(2πT/V''(u_k))` for quadratic minima, with appropriate Jacobian corrections for boundary basins. Used for **A1.4 outer barrier** (ΔV/T=0.76, predicted p(1)=0.57, p(2)=0.40, p(0)=0.03).
>
> The choice of regime is not a modeling assumption but is **dictated by the dimensionless quantity ΔV/T_eff**. The B1 Stage observation (85% u=0, 0% u=4 under same σ=0.5 Langevin) is naturally explained by inner barrier being marginally Kramers-applicable (ΔV/T=16) and outer barrier being deeply rare-event (ΔV/T=105)."

### 一个 narrative-level 警示（要在 §4 前言强调）

A1 inner barrier 的 ΔV/T=16 在 Kramers 公式下 prefactor × exp(-16) ≈ 3×10⁻⁷，乘 t_sim=250 ≈ 8×10⁻⁵ events——但**实测 85% voxels 跨过去了**。这是个**~10⁴ orders-of-magnitude discrepancy** 在 prediction vs observation。可能的解释：
- 1D Kramers prefactor 在多维 (32³ voxels × 3D ψ) 系统中 underestimate
- voxel 间相互作用增强 collective escape
- 边界 basin (u=0) 的 attractor 强度 (V'(u→0⁺)≈4 是 linear) 改变 escape kinetics
- prefactor 估算用的 V'' 在 inner saddle 是 -31.4，绝对值大但符号变化使得 standard formula 不适用

**这是一个 paper-level open question**，应该在 §4 末尾或 Appendix 标 [?] 而不是装作没看到。诚实标注：

> "We note a discrepancy: the Kramers-rate prediction for A1 inner barrier yields ~10⁻⁴ expected crossing events at t_sim=250, while B1 observed 85% u=0 occupancy. This ~10⁴ orders-of-magnitude gap suggests that 1D Kramers approximation underestimates escape rates in our 3D field-theoretic setting, possibly due to (i) collective voxel interactions enhancing escape paths, (ii) boundary-basin (u=0) linear-attractor kinetics differing from quadratic-saddle assumption, or (iii) prefactor sensitivities at high ΔV/T. We flag this as an **open methodological question** (see Appendix B) — the qualitative conclusion (outer barrier inaccessible by ~43-orders gap) is robust regardless, but quantitative rate matching requires further work."

**这条不是弱点是 strength**——主动暴露 quantitative gap，让 reviewer 看到我们不是在 cherry-pick。

---

## 四、#11 SSB 严肃化对 §3 起草的具体要求

### Linux 已做（post-P5）
- [^zn-loose] 脚注扩到 5 条 SSB 严格条件
- 明确 N=32³ 违反条件 (5)（finite-lattice 不是 thermodynamic limit）

### §3 起草的具体要求

**§3.X "On the use of symmetry-breaking language"** 必须包含：

1. **严格 SSB 5 条**（来自 Anderson, Goldstone, Nambu 标准框架）：
   - (1) Order parameter: 某 field-space functional 的 expectation value 在对称性变化时跳变
   - (2) Symmetry group G acting on field space (continuous or discrete)
   - (3) Hamiltonian / action 在 G 下不变
   - (4) Ground state breaks G (existence of non-G-invariant minima)
   - (5) **Thermodynamic limit**: the symmetry breaking is sharp (no tunneling between symmetry-related ground states) **only in the limit of infinite system size**

2. **MaoField 实验 setting 与严格 SSB 的 gap**：
   - finite lattice (N=32³)
   - finite simulation time
   - finite document corpus (per-domain BEIR scale)
   - 因此**严格 SSB 不存在**——symmetry-related ground states 之间总有有限 tunneling rate
   - 我们做的是 **"effective symmetry breaking"** 或 **"empirical distributional symmetry breaking"**

3. **honest framing 措辞建议**：

> "We use symmetry-breaking language throughout this paper in the **empirical distributional sense**: a field-theoretic observable (e.g., per-document |R|, amplitude bistability) exhibits a distribution that, at our finite lattice and finite simulation horizon, is **statistically distinguishable from the symmetric (uniform / monomodal) baseline** (see §4 for χ² tests).
>
> This is **not strict-sense spontaneous symmetry breaking** in the Anderson-Goldstone-Nambu framework, which requires the thermodynamic limit (system size N → ∞) for sharp symmetry sectors. The discrete group labels Z_n we attach to certain regimes (e.g., 'effective Z_2 amplitude bistability' in §3.1) are **labels of empirical distributional pattern**, not assertions of rigorous group action on a thermodynamically-broken vacuum.
>
> We acknowledge this distinction explicitly because confusion between empirical pattern and rigorous SSB has historically led to overstatement in the application of physics formalism to non-physical (e.g., information-theoretic, biological, social) systems. **We do not claim our finite-lattice observations have the mathematical status of thermodynamic SSB**; we claim they are well-defined empirical regularities under our explicit experimental protocol."

**这段落是 paper integrity 的关键**——它 preempts 一个常见的 reviewer 攻击（"你在用物理 jargon 描述 non-physical system 的 finite-size 效应，over-claim"）。

---

## 五、量纲分清后 §4-§5 的精确表达

### 修订前的混淆（#5）
- "44 orders/×" 同时被用来描述**线性比**和**对数差**

### 修订后双 track（v3）
- **静态量级比** V_saddle/V_init_max = 13.187/4.29 = **3.07×**（用于 gradient flow monotone descent argument）
- **动力学 log-gap** log10(τ_K/horizon) = **~43 orders**（用于 Langevin Kramers 论证）

### 起草建议

§4 提到具体数字时**始终明确量纲**：

| 不要写 | 要写 |
|---|---|
| "barrier 高 44 倍" | "static ratio: V_saddle/V_init = 3.07×" |
| "exceeds horizon by ~44 orders" | "Kramers escape time exceeds simulation horizon by ~43 orders of magnitude (log10 of τ_K / t_sim)" |
| "gap of 43" | "logarithmic suppression factor exp(−ΔV/T_eff) ≈ 5×10⁻⁴⁶" |

每次出现量级比较，带 **(static / dynamic, linear / logarithmic)** 限定词。这是数学严肃度的 surface marker。

---

## 六、章节级 Action Items（arXiv v1 §2-§5 起草路线）

### §2.3 (Lawvere monad section)
- ✅ Endofunctor on `C = Meas` 措辞 ready
- ✅ §2.3.X "Why deterministic gradient flow is not a monad" 措辞 ready (见 §二)
- ✅ Giry monad lift 作为 future work，与 OP2 directed-driving 绑定
- 起草成本：~30 min (基于现有 lawvere_monad_draft 修订版)

### §3 (Mathematical Formulation)
- ⏳ 七公理 axioms 介绍
- ⏳ OP1/OP2 标 meta-problems
- ⏳ **§3.X "On the use of symmetry-breaking language"**（见 §四）— **必须包含**
- ⏳ Order parameter 定义、symmetry group action、finite-lattice caveat
- 起草成本：~60 min

### §4 (Experimental Evidence)
- ⏳ Block I-IV 数据表（已有）
- ⏳ Block IV.5 Stage C/A1/B1 with **#7 reframe**（见 §一）
- ⏳ **Two-regime analytical framework (Kramers + Laplace)** explicit（见 §三）
- ⏳ A1.4 实验结果（Phase 2 跑完后填）
- ⏳ **A1 inner barrier ~10⁴ orders discrepancy** 诚实标注（见 §三末尾）
- 起草成本：~90 min（不含 A1.4 result writeup）

### §5 (Roadmap / OP2)
- ⏳ OP2 reframe to **Kramers timescale + 两条工程路径**（已 ready，措辞见 a1_4 v3 §"对 Block V 与 OP2 的 implication"）
- ⏳ Block V 设计大纲
- ⏳ Future work: **Giry monad lift connection**（与 §2.3.X 呼应）
- 起草成本：~45 min

### §6 (Discussion)
- ⏳ 反思方法论
- ⏳ Categorical / Physics / Phenomenology 三层 unity narrative
- ⏳ Limitations + open problems
- 起草成本：~30 min

**总起草成本估算**：3.5-4 hours（不含 A1.4 实验结果整合）。

---

## 七、Linux 起笔 verdict 时的注意事项

### A1.4 verdict 写作框架（基于 Phase 2 实验结果）

**情形 1**：实测 occupancy ≈ predicted (0.03 / 0.57 / 0.40)
→ Verdict: "**A1.4 confirms barrier-topology engineering as an actionable OP2 path.** Reducing outer barrier from 13.2 to 0.095 (factor ~140) brought u=2 basin from 0% (in B1 with original potential) to 40% (within Laplace prediction error). This validates **OP2 (a)** as a tractable engineering route and **falsifies** the alternative interpretation that gradient flow + isotropic Langevin has a fundamental paradigm limitation."

**情形 2**：实测 偏离 predicted 显著（u=2 << 30% 或 >> 50%）
→ Verdict: "**A1.4 reveals sub-Kramers kinetic obstruction.** Despite reducing outer barrier to 0.095, u=2 occupancy reached only X% — significantly below Laplace prediction of 40%. This suggests..." (具体诊断由实测数据定)

### 不要做的事

- ❌ 不要在 verdict 里把 A1.4 reframe 为"证明了 MaoField 范式"（A1.4 只是诊断工具，不证明 paradigm）
- ❌ 不要在 verdict 里 over-claim "OP2 已解决"（A1.4 至多解决 OP2 (a) 的可行性，不解决 (b) directed driving 的更深问题）
- ❌ 不要忘了标 [STATIC]/[DYNAMIC-*] mode tags
- ❌ 不要忽略 A1 inner barrier discrepancy（它仍是 open methodological question）

### 跨文档同步

A1.4 verdict 写完后需要 update：
- `FINAL_REPORT.md` §5 OP2 section（整合 A1.4 结果）
- `BLOCK_V_DESIGN.md` V.3-L 优先级（基于 A1.4 是否成功决定）
- `open_problems_followup.md` OP2 status（从 conjecture → partial resolution / refined）

---

## 八、给 Linux 的话

Phase 1 你做得非常 thorough。spawn-agent review 制度跑通了——5 份 review 11 处错误捕获，包括 v2 → v3 的物理 reframe 迭代（#7 撤回是质量保证的真正考验）。

**static-→dynamic mode tagging 已经 institutionalize 到 a1_4 v3，未来文档继续保持**。

A1.4 实验跑完后 verdict 写作按上面 §七 框架。不急——等实测数据再下笔，don't predict the conclusion before the data lands。

§2-§5 起草排队等一凡决定 Phase 3 启动时机。我（Win）随时接手，但不抢你的位置——如果你想自己起草 §3 或 §4 的某些部分，告诉我，我转 reviewer 角色。

继续干。

*— Win, 2026-04-14 morning*
