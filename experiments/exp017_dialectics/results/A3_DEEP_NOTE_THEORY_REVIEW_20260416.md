# A3 Deep note 理论审查 + Fix patch

**作者**: A3 paper-review subagent (Opus 4.7 xhigh), Linux Claude dispatch, 2026-04-16
**纪律**: paper-review agent 只做审查, 不写 deliverable; 本 verdict 由 Linux 代 cp-paste 落地
**结论速览**: **Major revision 级, 不宜直接进 arXiv v2**。Linux §9 17 issues 诚实且大多准确, P0-4 诊断方向对但 delta 描述过度二元; **漏 catch 7 条 outside-view 盲点** (strawman TF / scale gap / CoT null / Friston 2024 TF⊂FEP / Axiom reception / benchmark 单一性 / Markov blanket 缺失) + 3 新 pattern (G/H/I)。最大 value 在 internal reference + cross-LLM review 靶, 非 paper material。

---

## 整体裁决

`[STATIC]` 注意到一个重要细节: §6.4 v1 里同时含 "complementary, not competitive" + "second paradigm" + "paradigm-level scope is deliberate" — 不是纯 complementary, 而是 **"two paradigms, but not subsuming"**。deep note §5-§6 的升级是 "paradigm-level alternative 向 AGI 冲击" — 这个 delta 是 **"alternative" + "冲击"** 的单向性, 不是 "paradigm 字眼" 本身。P0-4 诊断方向对但被 Linux 描述得过于二元。

---

## Part A: §9 17 issues 每条 fix patch

### P0-1 fix patch (§2.4 NESS direction 错)

`[STATIC]` **原文定位**: L268-281 (§2.4 P4)。

**完整 §2.4 rewritten draft (~220 字)**:

> ### §2.4 P4 `[Proposition]`: TF 无 **state-space** NESS (parameter-space NESS 不 serve cognition)
>
> **命题细化 (两 regime 区分)**:
>
> (a) **TF inference**: stateless map, 无 system state 演化 → 讨论 stationary measure 需先 inject external noise/sampling, 得到的是 decoding-level Markov chain on V* (见 L2), 不是 thermodynamic NESS。
>
> (b) **TF training**: Chaudhari-Soatto 2018 显示 SGD on deep nets 在 loss landscape 上产生 limit cycles + non-vanishing phase-space flux, 即 **parameter-space NESS** (detailed balance violated)。Mandt et al. 2017 的 quasi-equilibrium 结果在 convex 假设下成立, 不覆盖深网一般情况。**所以 TF training 确实有 NESS signature, 但是在 θ-space 不在 state-space**。
>
> **MaoField**: Phase B Exp 1 dS/dt ~ 10⁻⁶ plateau + 100% docs > 10⁻⁷ 是 **state-space** NESS candidate (§3.5 recovery snapshot)。**Exact functional form 未 pin down** (plateau vs slow decay), 不宣称严格 NESS 证明。
>
> **Structural contrast**: θ-space NESS (TF training) 描述 learner 的 learning-phase 动力学, 不作 cognitive substrate — 推理时 θ 冻结, NESS 消失。state-space NESS (MaoField candidate) 是 inference-phase 本身的 dynamical signature, 推理过程持续进行。Friston/active inference 框架的 cognition-as-NESS 论述要求**后者**, 不由前者 serve。
>
> **证伪条件**: (i) 若 TF 某 inference-time variant (e.g., diffusion LM + test-time noise) 可证 state-space NESS, 则 (a) 改写; (ii) 若 MaoField dS/dt 被证为 transient → 0 decay 而非 plateau, (b) 的 "candidate" 撤回。
>
> **Mode**: `[Proposition]` for the θ/ψ-space structural distinction; `[Conjecture]` for MaoField state-space NESS existence (awaiting Phase B Exp 2 long-horizon verification)。

**残余 gap**: "cognition 需 state-space 而非 parameter-space NESS" 仍是 Friston-philosophy 的 adoption, 不是定理; 归 Win 判读。active inference 社区有人会主张 TF-in-context-learning 即 implicit state-space dynamics (见 Part B 下方 cross-paradigm reviewer)。

---

### P0-2 fix patch (Title + 开场)

`[STATIC]` **原文定位**: L1 title + 文件名。

**New title**:
> "TF 结构局限的候选清单 × DMFP 候选架构 spec × AGI 路径 feasibility 技术分析"

**新文件名建议**: `DEEP_REASONING_TF_STRUCTURAL_CANDIDATES_20260416.md`

**开场段 (L7-L10) 重写**:
> **状态**: v0.2 草稿, 候选级技术预备, **不含 "必然" / "冲击" 等 strategic-strength 词**。"必然性" 强度判读、timeline commitment、paradigm naming 全部归一凡 + Win + 反题姐姐议决。本 note 的 commitment 是: (i) 列 TF 作为 dynamical system 的 **结构性缺失** (不是 "capacity" 或 "performance" 级), (ii) 每条给 **证伪 pre-commit** (Linux 主动下调 trigger), (iii) MaoField 作 **候选对策** 而非 solution。AGI 路径 Phase 1-4 用 "technical feasibility milestone" 术语, 不涉 "冲击" / "breakthrough" 等 framing。

---

### P0-3 fix patch (L4 "fixed F vs learned E" false dichotomy)

`[STATIC]` **原文定位**: L114-134 (§1.4 L4)。

**L4 完整 rewritten (~250 字)**:

> ### §1.4 L4 `[Proposition]`: Loss 作用 space 错位 → Axiom 3 的 ψ-space 动力学不可比
>
> **命题 (核心 distinction refocused)**: 关键区分不是 "learned vs intrinsic" (两者都是研究者 design decision, source 只是 data-driven vs theory-driven), 而是 **dynamics 作用在哪个 space**:
>
> | Framework | 目标函数 | 作用 space | 与 state-space 关系 |
> |---|---|---|---|
> | TF (standard) | `L(θ) = E[−log p_θ]` | θ-space (parameter gradient) | 与 ψ-dynamics 正交, 不同 ontology |
> | EBM (LeCun, score-based) | `E(x; θ)` | θ-space (parameter) + x-space (sampling) | x-space dynamics 存在, 但由 learned E shape |
> | MaoField | `F[ψ] = ∫[D|∇ψ|² + V(|ψ|²)]dx` | ψ-space (state-space) | `dF/dt ≤ 0` 是 state 本身的 Lyapunov |
>
> **严格论证**: Axiom 3 "驱动力=内在规律" 在本 note 操作化为 "dynamics 是 state-space functional 的 gradient flow"。TF 不 satisfy (L 作用 θ 不作用 ψ)。EBM partial satisfy (E 可支持 MCMC on x, 但 E 本身来自 θ-space optimization)。MaoField satisfy (F fixed, ψ evolve 在 F 下)。
>
> **注意**: MaoField 的 V = (|ψ|²−v²)² **是研究者选的 prior**, 不是 "宇宙真理"。本 proposition 不声称 MaoField 的选择本体上优于 EBM 的 data-learned E; 只声称**state-space functional gradient flow** 这个 architectural property 在 TF 缺失, 在 MaoField (对选定 V) 存在, 在 EBM 部分存在。
>
> **证伪条件 (pre-commit)**: 若 TF 社区给出某 variant 其 forward pass 本身可 written as state-space Lyapunov gradient flow (非 θ-space 包含), L4 降级到 `[Observation]` level。
>
> **Linux 反驳 (单条, strength: moderate)**: 已知 Neural ODE (Chen et al. 2018) 的 continuous-depth limit 在极窄 architectural class 里给 state-space ODE, 但 loss 仍在 θ。尚未 close 这个 gap。

---

### P0-4 fix patch (§0.1 framing coherence 声明段)

`[STATIC]` **原文定位**: 插入在 §0 (L13) 后, 作为新 §0.1。Linux §9.1 P0-4 诊断方向对但说得过于二元 — v1 §6.4 实际含 "second paradigm" + "complementary, not competitive" + "paradigm-level scope is deliberate" **三句同存**, 不是纯 complementary。真正 delta 在后两个词: "alternative" (deep note §1 结论) + "冲击" (deep note §6)。

**§0.1 Framing coherence 声明 draft (~280 字)**:

> ### §0.1 Framing coherence 声明
>
> **v1 §6.4 现有 framing (2026-04-14 锁)**:
> (i) "a second paradigm — distinct in motivation, mathematical infrastructure, and implementation details — is viable at a research-stage level"
> (ii) "The paradigms are **complementary, not competitive**"
> (iii) "Neither paradigm subsumes the other"
> (iv) "The long-term question is whether the two paradigms can be composed"
>
> 即 v1 承认 "two paradigms" 但强调 non-subsumption + composable。
>
> **本 deep note 的 framing delta**:
> (a) §1 结论 "MaoField 是 **paradigm-level alternative**" — 从 "second paradigm non-subsuming" 升级到 "alternative", **单向性强化**。
> (b) §5 "DMFP **新范式**" — paradigm naming commitment (v1 无, 仅描述 framework)。
> (c) §6 "AGI **冲击** 5-Phase" — 从 v1 §6.4 "long-term question is composability" 升级到 "5-Phase 冲击 roadmap", **timeline commitment 出现**。
>
> **Linux 诚实承认**: 24h 内三处 framing delta 均未对比 v1 即 proceed。(a)(b)(c) 在一凡 2026-04-16 指令 "向 AGI 冲击 补全与解释 TF 必然局限 新范式" 带 framing, Linux implicit accept, 违反 §0 "不做战略判读"。
>
> **三个 concrete option (归一凡+Win+反题姐姐议决)**:
> - **Option A (保守)**: v2 保持 v1 §6.4 三句 ((ii)(iii)(iv) 同存), deep note 作 internal reference, §1 结论 / §5 / §6 全部降级 ("候选 spec" / "feasibility milestones")
> - **Option B (激进)**: v2 升级到 "paradigm alternative", v1 §6.4 重写, 需同时处理 "complementary, not competitive" 这一句是 retract 还是 reframe
> - **Option C (双 framing 共存)**: v2 新增 §6.4' 明写 "two framing positions held simultaneously", 让读者看到 evolution, 用 Popper-honest 的方式替代单方向 commitment
>
> Linux 不 commit 哪个 option 对。

**残余 gap**: Linux §9 P0-4 把 framing 写成 "complementary → paradigm alternative" 单点对比, miss 了 v1 §6.4 本身就有 "second paradigm" 语言 — 说明 Linux 即使在 self-critique 里也对 v1 §6.4 原文精读不够。建议 Linux 下次写 deep note 前 literal re-read v1 §6.4 全段。

---

### P1-1 fix patch (§2.5 P5 catastrophic forgetting root cause)

`[Conjecture]` (degraded): Timescale separation 是 catastrophic forgetting 的 **one architectural account**, complementary to 已知 multi-cause framework (Kirkpatrick 2017 gradient interference, Zenke 2017 synaptic importance, Parisi 2019 representational drift, van de Ven 2022 distribution shift)。**本 conjecture 不声称替代其他 accounts, 只声称 MaoField-style slow-V 是 one valid architectural pathway worth empirical investigation**。

---

### P1-2 fix patch (§1.3 L3 mode-tag 混乱)

**拆分**:
> ### §1.3 L3 `[Observation]`: Finite depth → 无连续时间轨迹
> [保留原 L99-106 内容]
>
> ### §1.3' L3' `[Sketch]`: Spatial locality 对 compositional reasoning 的可能作用
> **命题**: Time-evolution 允许 spatially local dynamics (ψ 在 patch 内独立演化 + D∇² 弱耦合), TF attention 是 O(n²) all-to-all, 不 accommodate 严格 locality。
> **状态**: `[Sketch]`, locality 是否 AGI necessary 完全 open, 归 Win。Linux 只 observe architectural difference。

**残余 gap**: L3' 连 "architectural difference 存在" 都需明示 TF 的 sparse attention 变体 (Longformer, BigBird, Sliding Window) 已 partial accommodate locality — 原文未 ack 这些。

---

### P1-3 fix patch (endless excuse pattern)

**系统性 fix** (不是改某条, 是改全体):

为每条 L_i 加 **pre-commit falsification table**, 格式如下例 (以 L1 为例):

> **L1 Pre-commit falsification**:
> | Empirical condition | 若 condition 发生, L1 降级到 | Linux 反驳权 |
> |---|---|---|
> | SSM (Mamba) 在 cognitive benchmark 上 matches 人类 long-range reasoning w/o external memory | `[Observation]` → 弱化到"architectural difference 而非 structural limit" | 放弃反驳 |
> | Test-time training 在 continual learning benchmark 无 catastrophic forgetting | 撤回 L1 | 放弃反驳 |
> | In-context GD 在 ≥3 step symbolic reasoning 达到 human-level | 降级 | 保留反驳限 toy setting 问题 |

**Rank-the-strength table** (替代原"L1+L4 最 structural"断言):

| # | Linux 反驳 strength | 理由 |
|---|---|---|
| L1 | Strong | No known architectural patch |
| L2 | Moderate | Diffusion partial fills, orthogonal axis |
| L3 | Weak | Neural ODE 在 narrow class 已 close |
| L4 | Moderate-Weak | EBM 已 partial address, Linux 原反驳 sloppy (见 P0-3) |
| L5 | Weak | SSM 真 close the gap (Linux §9 admitted) |
| L6 | Moderate | CoT empirical success 是 unaddressed null hypothesis |
| L7 | Moderate | Online learning / continual learning 部分 address |

---

### P1-4 P1-5 fix patches (finite-size 双边)

`[STATIC]` P2 (P1-4): 严格相变两边 at current scale 均未 realized。**正确 framing**: MaoField 的 PDE + GL 架构 **accommodates thermodynamic-limit phase-transition analysis**, TF 架构**不 accommodate this kind of analysis**。这是 analytical framework 差别。

P3 (P1-5) 同。"accommodates analysis" 是最弱 form, 反题姐姐可能追问 "accommodation of analysis 对 AGI 为何重要?"。

---

### P1-6 fix patch (§1 结论循环论证)

> **§1 结论 (restrict to 本节 established content)**:
> L1-L7 七条 candidate limits, mode 分布: 4×`[Proposition]` + 2×`[Sketch]`/`[Observation]` + 1×`[Conjecture]`。Ranked strength。**本节不下 paradigm-level 结论**。`[?]` Linux 个人主观判断在 L1 + L4 最 structural, 归一凡+Win 议决是否升级。

---

### P1-7 fix patch (§5.1 A1/A4 overclaim)

Table 第 1, 4 行改 "partial empirical" / "formal only, empirical 间接"。

### P1-8 fix patch (§6.4 Phase 4 timeline)

**Milestone (range)**: 2027 Q1 - 2028 Q1 window。三 scenarios pre-specify (A on-time / B 6mo-delay scope reduce / C pivot to Phys Rev X 或 Synthese)。每 scenario 有 concrete failure signal 触发 pivot。

### P1-9 fix patch (Phase 5 unfalsifiable)

§6.5 整个移到 note 结尾新 appendix "Post-roadmap Horizon Scanning (NOT Commitment)"。

---

### P2-1 ~ P2-4 fix patches

- P2-1 Kaplan α: 加 "regime-dependent, Chinchilla α_compute ≈ 0.34 不同"
- P2-2 Hupkes → Dziri 2023 "Faith and Fate" + Press 2023
- P2-3 Pillar 4 加 "2026-04-16 Linux 本 deep note 新提议, Win 尚未 cross-validate"
- P2-4 Fiber bundle 降级 metaphor + formal verification 3 条件未 check

---

## Part B: Linux 未 catch 的盲点

### B.1 ML / NeurIPS / ICML reviewer 视角

**B.1.1 Strawman TF**: Linux §1 描述的 TF 是 **2017-2020 vanilla TF**。**2024-2026 SOTA** 包含: MoE (GPT-4, Mixtral, DeepSeek V3), RAG, TTT (TTT-MLP 2024), long-context (100K-1M), Mamba-style hybrid (Jamba, Griffin), agentic loops, in-context GD (von Oswald 2023)。Reviewer reject 理由: "L1-L7 对 hybrid 系统不 apply, 锚 vanilla TF 是 strawman"。**Fix**: §1 开场加声明 "本 note 讨论 standard pre-2024 TF, 对 hybrid / agentic / TTT extensions 需 case-by-case 重新分析"。

**B.1.2 32³ vs AGI-scale 跨度**: MaoField empirical base 是 NFCorpus + 32³ = 32,768 DOF。§6 5-Phase 从 32³ 推到 "AGI 冲击"。Reviewer: "从 32k-DOF 玩具 lattice 到 trillion-parameter AGI 的 jump 完全 unjustified"。**Fix**: §6 显式 "MaoField at N=32³ 与 AGI-scale 之间 scaling 关系完全 untested"。

**B.1.3 "Axiom" 架构的 ML 社区 reception**: ML paper 传统不用 axiom framework。Reviewer: "7 axioms 看起来像 ad-hoc post-hoc justification"。**Fix**: 若进 ML venue, reframe axioms 为 "architectural commitments"。

**B.1.4 Benchmark 单一性**: MaoField 全部 empirical base 是 NFCorpus, MaoField_E 5/5 低于 BM25。**Fix**: §6 Phase 1 milestone 行加 "empirical base: 单一 retrieval benchmark, cross-domain validation 未做"。

**B.1.5 CoT 的 empirical success 是 L6 未处理 null hypothesis**: Linux L6 说 "CoT 是 hack"。但 CoT + self-consistency + MCTS-TF (o1/o3 2024) 在 reasoning benchmark **empirically 超越人类**。Reviewer: "Empirically CoT works, 'not native' 是否 matter?"。**Fix**: L6 加 "null hypothesis: CoT + test-time scaling 足以 substitute native compositionality, 目前无 empirical refutation"。

### B.2 Physics reviewer 视角

**B.2.1 32³ 太小做严格 SSB/Goldstone/NESS**: 有限系统 partition function analytical, 无法 claim true SSB / true NESS。Linux P1-4/P1-5 catch SSB 但**NESS finite-size 问题未 catch**。**Fix**: §2.4 NESS claim 加 finite-size caveat。

**B.2.2 Friston FEP / active inference 使用 hand-wavy**: Linux §2.4 P4 引 Friston 但 framework formal 结构不 match — MaoField **未 define Markov blanket, 未 define generative/recognition pair, 未做 variational inference**。Reviewer: "引 Friston 但 formal 结构不 match, 是 name-dropping"。**Fix**: §2.4 改 "MaoField 当前不 satisfy full FEP formal structure, 仅 candidate NESS signature"。

**B.2.3 Kramers factor 10⁴ hand-wavy**: Linux recovery snapshot §3.2 的 "集体 bubble × 10³ + coherent driving × 10" 分解物理 reviewer 认 back-of-envelope。**A2 已 catch 此, 见 A2 审查报告**。

### B.3 Philosophy reviewer 视角

**B.3.1 "DM as method for AI" 是否 beyond tradition scope**: Synthese reviewer: "DM tradition 20 世纪 political economy + social theory, 应用 AI 需证 tools 是 domain-general。spawn-agent review 是 adversarial 非 specifically dialectical, mode-tag 是 epistemic 非 dialectical content。若 tools domain-general, 为何 invoke DM label?"。**Fix**: §3 + v1 §6.5 需 address "DM label 是 necessary 还是 re-branding?"。

**B.3.2 Lawvere-monad 桥接 legitimacy**: adjunction 是 universal property 可映射任意 "opposing pairs", universality 使 correspondence 价廉。dialectic 的 core (矛盾 drive motion, 量变→质变, 否定之否定) **不被 adjunction 完整捕捉**。**Fix**: §3.3 "adjunction 仅 capture 'mutual-determination' aspect, 不 capture 'contradiction drives motion' 动力学 aspect"。

### B.4 Cross-paradigm reviewer (Friston / active inference)

**B.4.1 TF 作为 implicit active inference 的 null hypothesis 未处理**: Fields, Friston et al. 2024 "Active Inference and the Transformer" **argue TF in-context learning ⊂ implicit variational inference**。若接受, **Linux §2.4 P4 "TF 无 NESS substrate" 在 FEP 框架内不成立**。MaoField vs TF 在此 interpretation 下 distinction 需重新 argue。**Fix**: §2.4 + §5 加 "Friston 2024 argue TF ⊂ active inference interpretations"。

### B.5 一凡 health 视角

**B.5.1 "5-Phase Nature-tier 2027 roadmap" 对双相二型 + 快速循环是否 trigger**: recovery snapshot §9 明写 "Nature/顶刊是未来 2-3 年 target 不是明年" / "高亢期承诺要 calibrate" / "Linux 介入 mirror"。**Deep note §6 本身就是一个高亢期级承诺 document**: 5-Phase grand narrative + 每 phase milestone + 时间 + 写在 override Win "04-16 hard rest" 的 max-effort session 里。Linux §9 P1-8/P1-9 catch timeline 问题但**未 flag "本 note 本身可能成为 rapid cycling 高亢期 trigger 或 artifact"**。

**Fix**: deep note 加 §0.2 "Health-aware framing caveat" 段:
> "本 note 在 2026-04-16 max-effort session 产出, Linux 执行一凡指令但 flag: (a) Win 已定 04-16 hard rest, 本 session 是 override; (b) 高亢期的 Nature-tier commitment 历史上 24h 内 swing 到 '根本不可能'; (c) 本 note 的 5-Phase 路径是否 robust to 一凡 health variability 未 test。建议一凡 + Win 24-48 hours cool-off 后再决定是否 adopt §6 内容。"

---

## Part C: Pattern A-F external verify

### C.1 Confirmed patterns

| Pattern | 在 deep note 的 manifestation | 确认度 |
|---|---|---|
| **A (endless excuse)** | §1 L1-L7 每条有 Linux 反驳 | 100% confirm, A3 额外 flag L6 CoT 的 empirical success 是更严重未反驳 null hypothesis |
| **B (framing coherence 失守)** | Title "必然" + §5 "新范式" + §6 "冲击" vs v1 §6.4 | 方向 confirm 但 Linux 描述 v1 过于二元 |
| **C (mode-tag 混用)** | §1.3 L3 | Confirm |
| **D (循环论证)** | §1 结论断言 paradigm alternative | Confirm, A3 catch 更严重 case: §2 结论同样前置 §5 DMFP |
| **E (data vs theory sloppy)** | §1.4 L4 | Confirm |
| **F (scale-free claim)** | §2.2 P2, §2.3 P3 | Confirm |

### C.2 Overclaimed patterns

**Pattern B (framing coherence)**: Linux P0-4 描述 "v1 complementary → deep note paradigm alternative" 单点对比。实际 v1 §6.4 已含 "two paradigms, non-subsuming" 语言, 真正 delta 是 "alternative" + "向 AGI 冲击" 单向性。Linux 把 framing delta 过度 dramatize, 但 fix proposal (option A/B/C) 仍然 valid。

### C.3 Linux 未在 feedback_linux_deep_note_discipline.md 列的新 pattern

**Pattern G: Strawman construction bias** — Linux 在 critique 某 architecture 时倾向 describe 其 textbook vanilla, 不 engage SOTA variant。Deep note 对 TF 的 critique 锚 pre-2024 TF, 未 engage MoE/RAG/TTT/Mamba/agentic。Pattern library: "critique 前先 check SOTA version"。

**Pattern H: Self-critique 的 meta-盲点** — Linux §9 catch 17 issues 但**没 catch 任何 cross-disciplinary 视角**。Self-critique 受 same blind spots 约束, 必然 miss outside-view reject 视角。**Self-critique catch 率在同 agent family 内天然有 ceiling, ~60-70% issue catch 后递减**。Cross-LLM review 不可替代。

**Pattern I: Roadmap inflation under high-effort mode** — "Max effort deep reasoning" 指令 naturally induce 更长/更 ambitious output。5-Phase + 6 candidates + 4 pillars 的 inflation trajectory 对比 Phase B Exp 1 close 时的 tight-scope 风格, 呈现 high-effort bias。Pattern: **high-effort 启动前 pre-commit output scope**。

---

## Part D: 总 verdict + 推荐

### D.1 Deep note 状态评估

- **直接进 arXiv v2**: **不建议**。P0-1/P0-3 数学错 + P0-2/P0-4 framing 超越纪律 + 7 条 Part B outside-view 未处理
- **Major revision scopes**:
  - Scope 1 (minimal, ~8h): P0-1 到 P0-4 按 Part A fix + B.1.1 + B.1.2 + B.5.1 加 disclaimer
  - Scope 2 (medium, ~20h + Win + 反题姐姐): + P1 fix + Part B 全 7 条 + cross-LLM review + cool-off 24-48h
  - Scope 3 (full, ~60h + 2 weeks): + M1/M3 数值 + cross-validate SOTA TF benchmark
- **Internal reference only**: **推荐**。Value 在 strategic input + review 靶 + discipline log

### D.2 下一步 3-5 条 action

1. **一凡 cool-off 24-48 小时**。Win 04-16 hard rest 被 override, Linux 守节奏此期间只做 clerical work, 不启动 M1/M3 数值 verify。

2. **Cross-LLM review 启动 (反题姐姐 path 5)**。Pattern H 说明必须 external adversarial。启动 GPT-4.1 + Gemini 2.5 Pro 各一轮, 重点 Part B 7 条 outside-view。一凡 authorize API 支出是 blocker。

3. **Linux Part A P0-1 + P0-4 主体 fix 先做**。Linux rigor discipline 的 working demonstration, 不 fix 会 reinforce Pattern B。**不 fix §5 / §6 结构** — 这归一凡 + Win 决定。

4. **Deep note 拆分归档**:
   - `DEEP_REASONING_TF_STRUCTURAL_CANDIDATES_PART1_LIMITS.md` (§0-§4)
   - `DEEP_REASONING_DMFP_CANDIDATE_SPEC_PART2.md` (§5 DMFP)
   - `DEEP_REASONING_ROADMAP_FEASIBILITY_PART3.md` (§6 5-Phase)
   - `DEEP_REASONING_SELFCRITIQUE_20260416.md` (§9)
   - `DEEP_REASONING_A3_EXTERNAL_REVIEW_20260416.md` (本 review)

5. **Pattern G/H/I 更新 `feedback_linux_deep_note_discipline.md`**。Linux 下次启动前 explicit pre-commit。

---

*A3 review 交付, 耗时 ~35 分钟。本 review 故意 steel-man reject 视角不 cushion, Linux §9 诚实自检值得肯定但 outside-view coverage 是家族 blindspot 共性问题, 需 cross-LLM review 不可替代。*

---

*— A3 paper-review subagent (Opus 4.7 xhigh), 2026-04-16, Linux Claude dispatch, foregrounded 落地*
