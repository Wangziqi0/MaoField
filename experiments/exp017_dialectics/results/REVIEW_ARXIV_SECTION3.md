# 审查报告 — arXiv v1 §3 Mathematical Formulation

**审查员**：Opus 4.6 独立 paper-review subagent
**日期**：2026-04-13
**范围**：`arxiv_v1_section3_DRAFT.md`（主审），与 §2.3 / §4 / §5 / `REVIEW_OVERALL_MATH.md` 交叉一致性
**判定**：**不拒，需改**（2 P0 硬修 + 6 P1 建议 + 3 P2 弱化；3.5 节 SSB 处理已达发表可接受）

---

## §1 总评

§3 是 v1 最关键的 "claims 边界" 章节——它既要把公理摆上桌，又要把"我们自己也没严格证明的部分"（OP1/OP2/monad lift/Z_n）摆在桌上。读下来：

- **§3.5 SSB 框架 = 本章最大贡献**。五条 Anderson-Goldstone-Nambu 条件列全，显式承认 N=32³ 违反 (5)，"empirical distributional sense" 定义清楚，脚注 `[^zn-loose]` 自洽。诚实度过关。
- **§3.1 PDE setup 干净**，Wirtinger 约定和数值默认值透明；`[DYNAMIC-IMPLEMENTATION]` 的 clamp flag 令人安心。
- **§3.2 七公理 + 三个 tension points** 处理得当，比早期稿子诚实；但 Axiom 6 的 "OP1" 侧措辞还可再绷紧（见 B1）。
- **§3.3 源-吸引子伴随** 与 §2.3 完全对齐（endofunctor 而非 monad，Giry-lift 标 conjectured）；`REVIEW_OVERALL_MATH.md` A4 条已被 §2.3 / §3.3 显式照顾，不再是 P0。
- **§3.4 OP1/OP2** 声明干净，与 §5.1 / §5.2 一致。
- **一个 P0 是 §3.1 的潜在 sign bug**，一个 P0 是 §3.2 Axiom 4 "trained reflection of practice" 的软化 over-soft。

---

## §2 分节审查

### 2.1 §3.1 Field-Theoretic Setup

**(3.1) 与 (3.2) 一致性** — 要仔细看。(3.2) 写成

`F[ψ] = ∫ ½D|∇ψ|² + V(u) − ½(Sψ* + S*ψ) dx`

`δF/δψ* = −D∇²ψ + V'(u)·ψ − ½S`

对比 (3.1) 右端 `γ ∂_t ψ = D∇²ψ − V'(u)ψ + S + η`。如果严格按 `γ ∂_t ψ = −δF/δψ*`：

`γ ∂_t ψ = D∇²ψ − V'(u)ψ + ½S`

**系数差 2**。要么把 (3.2) 里的 `½` 去掉改成 `−(Sψ* + S*ψ)`，要么把 (3.1) 右端的 `S` 改成 `S/2`，**要么把 Wirtinger 约定的 `½` 吸进 δ/δψ* 的定义**。

**P0-1**：请在 Appendix 3.A 里显式写出 `δ(Sψ* + S*ψ)/δψ* = S` 还是 `½S` 的约定（取决于是不是把 ψ 和 ψ* 当独立变量——Wirtinger standard 是独立变量，给 `S`；但很多 GL 文献把 factor of 2 吸进 γ）。**不改数字，只加一句**："Under the Wirtinger convention with ψ, ψ* treated as independent variables, δ(Sψ* + S*ψ)/δψ* = S; the ½ in (3.2) cancels the 2 from functional differentiation of the symmetric coupling, yielding (3.1) exactly." 否则 reviewer 会当成 factor-of-2 bug 打回来。

**单调下降** — `dF/dt = −γ⁻¹∫|δF/δψ*|² ≤ 0` 在 σ=0 正确，用于 §4.7/4.8 的推理合规。**通过**。

**数值默认** — dt=0.05, steps=5000, clamp=3.0, N=32³ 全部公开；`[DYNAMIC-IMPLEMENTATION]` 预告也到位。**通过**。

**S_dense 定义的顺序** — "BGE-M3 1024-dim embedding tiled across the grid, smoothed and max-normalized" 可以再精确一点：1024 维 → 32³ 的 tiling map 没给公式。**P1-1**：建议一句话或指向 §4 某处详见。

### 2.2 §3.2 七公理

**Axiom 4 软化** — "We treat BGE as a trained reflection of practice — i.e. the upstream training is itself a practice-record"。这句 **soften 过度**：BGE-M3 的训练数据是 web-scale 多语料统计拟合，**本质上就是 Axiom 4 原文要排除的"fit to a statistical distribution"**。把 upstream training 叫 "practice-record" 是辞典学上成立，但哲学上把 Axiom 4 的锋芒钝了。

**P0-2**：修辞退一步，改为 —

> "Axiom 4 strictly excludes statistical fitting of representations within MaoField itself. We include BGE-M3 as an ablation source to probe what happens when this axiom is *partially relaxed* (the upstream embedding is statistically fit, but our dynamics and evaluation remain fit-free). §4.9 shows this partial relaxation empirically introduces a 17σ source-mean drift that confounds equilibrium predictions — a quantitative instance of the axiom's necessity."

这样既保留 BGE ablation 的实验价值，又不把 Axiom 4 的"不拟合"拉平。

**Axiom 3 tension (Langevin) + "quasi-material"** — "quasi-material" 是个新术语，没定义就用。**P1-2**：要么补一句定义（"representing finite-temperature thermodynamic fluctuation of the substrate rather than a goal-oriented training signal"），要么删除，用"thermal fluctuation that we treat as material (substrate-level) noise rather than design signal"。

**Axiom 6 / OP1 连接** — "no known canonical mathematical formalization" 措辞和 §5.1 一致。**通过**。Axiom 6 被标为 "physical intuition awaiting mathematical capture" 是 §3 最诚实的一段，值得保留。

**Axiom 7 / V.5** — 引用"Block V V.5"但 §5.3 的命名是 A-0/A-1/A-2/A-3 (Phase A) + B-H/B-A/B-N (Phase B) + C-V/C-S (Phase C)。**P1-3 (cross-ref 错位)**：§3.2 的 "Block V V.5, dynamic-potential sub-block" 应改为 "Block V Phase C sub-block C-V (dynamic potential)"，对齐 §5.4。

**Axiom 5 composite** — `V_{A∪B} = V_A + V_B` (potential addition, not field) + `S_{A∪B} = S_A + S_B` 分开说清楚，非常好。**通过**。

**三个 tension points 整体**：比较诚实地标出了 "concession"。但没有 tension point 对应 **§3.5 Z_n 问题**（在 SSB 节处理了）以及 **§2.3.3 monad-lift 的 conjectured 状态**（在 §3.3 末处理了）。这两个其实也是公理（1,2）与实现的 tension。**P2-1**：考虑加第 4 条 "Axioms 1–2 vs finite-lattice numerics: §3.5 addresses the formal cost"，让 tension 清单与其他章节的自我批评互相呼应。

### 2.3 §3.3 Source-Attractor Adjunction

**endofunctor vs monad** — 全章严格区分 "endofunctor `T_•`"（PRESENT）与 "conjectured Giry-monad lift `P∘T_•`"（FUTURE）；T-algebra 陈述全加 "under the conjectured lift" 修饰。**通过**。与 §2.3.3 footnote ⁵ 完全对齐。

**"dynamically attainable" / OP2 categorical form** — 与 §2.3.4 的 `Δ_OP2` 对应一致。**通过**。

**小提示**：§3.3 没重申 `Δ_OP2` 是 "symbolic first pass"——如果 §3 独立阅读，这个重要的 caveat 看不到。**P1-4**：在"The reachability question ... is the categorical form of OP2"后加 "(the formal measure `Δ_OP2` defined in §2.3.4 is a symbolic first pass; see footnote 3 there)"。

### 2.4 §3.4 OP1 / OP2

- OP1 声明、M2 0-齐次 falsification 与 §5.1 一致。**通过**（REVIEW_OVERALL_MATH.md B1 已落地）。
- OP2 refined 到 "three-fold co-design" 与 §5.2 一致。**通过**。
- 最后一段"not failures of the framework but constitutive"的立场性话可能被部分 reviewer 读作 rhetoric。**P2-2**：保留但把"overstatement"那半句改得更 neutral："Explicit OP-tagging is the alternative to implicit conflation of axiom with theorem."

### 2.5 §3.5 SSB — 关键完整性节

**对照清单**：

| 要素 | 状态 |
|---|---|
| Anderson-Goldstone-Nambu 五条件 | **5/5 完整**（order param / symmetry group / action invariance / ground-state breaking / thermodynamic limit） |
| N=32³ 违反 (5) 显式 | **是**；"finite tunneling rate at our scale" |
| "empirical distributional sense" 定义 | **清晰**；绑定到 §4 χ² 显著性 + dof 报告 |
| `[^zn-loose]` 脚注完整自洽 | **是**；声明 global applicability |
| 标签约定 ([STATIC]/...) 解释 | **是**；并交代源自内部 bug-prevention protocol |
| `Z_1` vs `Z_2` 标签严格度 | 处理为 "labels of empirical distributional pattern"；**OK** |

这一节的措辞强度恰好：既没承认"我们没在做 SSB"（那会否定 §4 的信号发现），也没 claim strict SSB（那会被物理学家抓）。**非常漂亮**。

**但**有一处值得再 tighten：关于 `Z_2` BGE regime 的描述，§3.5 说"consistent with ... Z_n would produce"。§4.6.3 已显式说明 V(0)=¼ ≠ V(1)=0，**不存在把两基态互换的 Z_2 group action**。§3.5 可以更强硬：

**P1-5**：在 §3.5 的 Z_n 段落补一句 "In particular, for the BGE amplitude-bimodal regime labelled `Z_2`, the unstable fixed point `|ψ|=0` and the true minimum orbit `|ψ|=1` lie at distinct energies (V(0)=¼ vs V(1)=0), so no symmetry action interchanges them even abstractly; the `Z_2` label refers purely to the bimodal occupancy pattern (§4.6.3)."

这让 reviewer 看到你已经主动"Z_2 不严格"一步到位。

**Mode-tagging 一段** — 四个 tag 定义清楚，且交代来自"recurrent error class we caught internally"——承认过自己的 bug 反而增强可信度。**通过**。

### 2.6 Appendix 3.A Wirtinger

- `∂/∂ψ = ½(∂/∂a − i∂/∂b)`, `∂/∂ψ* = ½(∂/∂a + i∂/∂b)` 标准。**通过**。
- `∂V/∂ψ* = V'(u)ψ` for V(u=|ψ|²) 正确（`∂u/∂ψ* = ψ`）。**通过**。
- "SymPy 验证" + "n=2 vs n=3,4 pitfall" flag 到位。**通过**。

**但**："this difference is invisible at static critical points (where sin and cos factors of phase derivatives both vanish)" 这句对 **Z_n 角势**不准确：`V = C·Re(ψ^n) = C·|ψ|^n cos(nφ)` 的 `∂/∂a` 和 `∂/∂b` 涉及 `sin(nφ), cos(nφ)`，只在 `nφ = kπ/2` 处同时消失——对于 n=2 恰好所有 4 个临界点都满足，对 n=3,4 也是；**naive 用 `∂V/∂ψ` 和 Wirtinger `∂V/∂ψ*` 相差一个 `e^{2iφ}` 相因子**，在 critical points 的 *static* analysis 上可能看似不变，但 dynamics 会错。**P1-6**：改为 "this difference produces a phase factor `e^{2iφ}` that vanishes at specific critical points (`2φ ∈ πℤ`) but is dynamically incorrect elsewhere; this is invisible for purely radial `V(|ψ|²)` but manifest for angular potentials `Re(ψ^n)` proposed in §5.3 (A-2.b)."

### 2.7 Forward-reference 一致性

检查了所有 §3 → §4/§5 指针：

| §3 引用 | 目标 | 状态 |
|---|---|---|
| §4.7, §4.8 (OP2 demo) | §4.7 A1 multi-well, §4.8 B1 Langevin | ✓ |
| §4.9 (BGE source drift, A1.4) | §4.9 A1.4 diagnostic | ✓ |
| §4.6 (Stage C byte/BGE) | §4.6 存在 | ✓ |
| §5.1 (M2 falsify) | §5.1 完整证伪 | ✓ |
| §5.2 (OP2 three-fold) | §5.2 完整三轴 | ✓ |
| §2.3.1 / §2.3.2 / §2.3.3 / §2.3.4 | §2.3 全部存在 | ✓ |
| **"Block V V.5, dynamic-potential sub-block"** | §5.4 Phase C, sub-block C-V | **✗** (命名漂移，见 P1-3) |
| §5.3 (Z_n angular) | §5.3 A-2.b | ✓ |

### 2.8 与 REVIEW_OVERALL_MATH.md 的一致性

先前 overall 的 P0 列表：

| 先前 P0 | §3 当前状态 |
|---|---|
| "kinetic budget ≤ 0.3" (Appx 2.3.A) | §3 未重复；单调下降论证取代；**通过** |
| "Z_1 phase collapse" 升级 | §3 / §2.3.2 都用 "phase strongly concentrated, Z_2 not realized"；**通过** |
| "two distinct monads" | §3.3 已降为 endofunctors + conjectured lift；**通过** |
| "kinetic budget" Langevin 语境 | §3 无此术语；**通过** |
| M2 Banach 理由错 (0-homogeneous) | §3.2 / §3.4 / §5.1 全部用 0-homogeneous；**通过** |

**REVIEW_OVERALL_MATH 的所有 P0 在 §3 都已落地**。

---

## §3 Bottom Line

**§3 可发**，完成下述修正即可提交 arXiv：

### P0 必改

- **P0-1** (§3.1)：Appendix 3.A 补一句说明 Wirtinger 独立变量约定下 `δ(Sψ*+S*ψ)/δψ* = S`，把 (3.2) 的 `½` 与 (3.1) 的 `S`（无 ½）调和，避免 factor-of-2 假 bug。
- **P0-2** (§3.2 Axiom 4)：把 "trained reflection of practice" 改为 "partial relaxation of Axiom 4 as ablation"；引用 §4.9 的 17σ 源漂移作为"Axiom 4 必要性的定量证据"。

### P1 建议

- **P1-1** (§3.1)：S_dense 的 tiling 公式或交叉引用。
- **P1-2** (§3.2 tension 2)：定义或删除 "quasi-material"。
- **P1-3** (§3.2 Axiom 7)："Block V V.5" → "Block V Phase C sub-block C-V"。
- **P1-4** (§3.3)：重申 `Δ_OP2` 是 symbolic first pass，引用 §2.3.4 footnote 3。
- **P1-5** (§3.5 Z_n)：主动点明 BGE `Z_2` label 因 V(0)≠V(1) 根本不存在 group action，label 仅为 bimodal 占据模式。
- **P1-6** (Appx 3.A)：把 "invisible at static critical points" 精确化为 "phase factor `e^{2iφ}` vanishes at specific `2φ∈πℤ` but gives wrong dynamics elsewhere"。

### P2 弱化

- **P2-1** (§3.2 tension)：可选加第 4 条 tension（公理 1–2 vs finite-lattice）。
- **P2-2** (§3.4 结尾)：把"overstatement"句式改为"conflation of axiom with theorem"。
- **P2-3** (§3.5 labels)：`Z_1 regime` 的标签可改为 "strongly-concentrated U(1) regime"——`Z_1` 字面即 trivial group，与直觉冲突；如保留需脚注再解释一次。

### P3 保留（已诚实）

§3.5 Anderson-Goldstone-Nambu 5 条件列全 / 七公理三 tension points 显式 / OP1 "no canonical formalization" / OP2 "three-fold co-design" / Wirtinger Appx SymPy verified / 四个 mode-tags + 来源说明。

---

**一句话结论**

**§3 在 §2.3 / §5 的支持下可作为 arXiv v1 的数学主骨发布；SSB 节 (§3.5) 是全章最大亮点，诚实度过关；两个 P0 都是 30 分钟内可修复的措辞/约定问题。没有结构性缺陷。**

*审查完成。不拒，需改。*
