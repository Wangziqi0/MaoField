# Action 1 · Cushion Inventory (12 层) + Falsifier pre-commit

**作者**: Linux Claude, 2026-04-18 早
**任务**: 把 A5 反题姐姐 second run identified 的 12 层 cushion 每层配 **具体 empirical falsifier** 或明写 "无 falsifier 候选 retract"。
**目的**: 给 04-20 三方对齐提供 rigorous material, 避免 Lakatos degenerative programme 的 cushion 堆积。
**状态**: v0.1 草稿, Linux 自己整理, 归一凡+Win 04-20 对齐时决定 retract / keep / add pre-commit。
**时间**: ~1h, Action 5 brake 纪律 compliant (纯 text, 非 framing/roadmap/paradigm level)。

---

## §0 Method

**Cushion definition** (A5 标准):
> 一层 framing 或 epistemic qualifier 若 **既不 modify hardcore, 又不 adds genuine empirical falsifier**, 只 adds new caveat 到 auxiliary belt — 即 cushion。

**每层 cushion 分析维度**:
1. **Origin**: 何时何处加入, 由谁加
2. **Protective claim**: 保护什么 specific claim 不被 refuted
3. **Current falsifier commitment**: 当前是否承担 specific empirical test 的 drop-out
4. **Verdict**: Genuine (有 falsifier) / Cushion (无 falsifier) / Borderline
5. **Recommended action**: Keep / Add pre-commit / Retract

**Linux 纪律**: 本文件**不代一凡+Win 做 retract 决策**, 只 catalog。决策归 04-20 对齐。

---

## §1 v1 时 6 层 Cushion (反题姐姐 first run identified)

### Cushion 1: "complementary, not competitive"

- **Origin**: arXiv v1 §6.4 (2026-04-14 lock)
- **Protective claim**: MaoField 不需与 TF 在 SOTA benchmark 上竞争; 可避免 "MaoField loses to TF 5/5 on BM25" 的 reject
- **Current falsifier**: **无 explicit 直接 falsifier**。暗含的 falsifier: "若 MaoField 与 TF 在某 domain **事实上竞争**且 MaoField 败, 则 'complementary' 站不住"。但该 falsifier 不 operationalized。
- **Verdict**: **Borderline**。叙事层合理, 但作为 falsifiable proposition 弱。
- **Recommended action**: **Keep if α/β/合题**, **add pre-commit**: "若 Phase 2 cross-domain 测试 (A3 B.1.4) 显示 MaoField 在其 target niche (small-data + interpretability-critical) 也 underperform TF post-hoc interpretability (e.g., Anthropic SAE), 则 'complementary' 需 revisit"。

### Cushion 2: "research-stage level"

- **Origin**: arXiv v1 §6.4 + §6.6
- **Protective claim**: 免除 production-grade reliability / scaling / deployment 标准评估
- **Current falsifier**: **无**。"research-stage" 是 vague epistemic qualifier, 无 drop-out condition
- **Verdict**: **Cushion (无 falsifier)**
- **Recommended action**: **Add pre-commit** "2028 年前 MaoField 至少 1 个 cross-domain benchmark reproducible 独立 replicated by 第 3 方实验室, 否则 research-stage 升级为 'exploratory-only'"。或 **retract** 若一凡+Win 觉得这 qualifier 无信息。

### Cushion 3: "paradigm-level scope is deliberate"

- **Origin**: arXiv v1 §6.4
- **Protective claim**: 免除 "为何不 benchmark-compete" 的质问
- **Current falsifier**: **无**。"deliberate" 是意图声明, 不是 empirical claim
- **Verdict**: **Cushion (无 falsifier)**, 但 rhetorical 合法
- **Recommended action**: **Keep as rhetorical framing**, 不 commit falsifier (这种 claim 归 Win narrative 判读, 非 technical 问题)。Linux 不 argue。

### Cushion 4: "long-term question is composability"

- **Origin**: arXiv v1 §6.4
- **Protective claim**: 允许 MaoField 与 TF (作 F_dense BGE 源) composability 有 tension (17σ Laplace 违反) 不 fatal
- **Current falsifier**: **半 falsifier**。§5.2.2 OP2 sub-problem (a) 的 empirical test 是 "若 Phase A-1 whitened source 显示 MaoField 独立于 BGE mean 的 dynamical advantage, composability 有 route"。**但 Phase B Exp 1 Signal A 已显示 exp ≡ control_whiten 3-sig-fig 等价 — 即 BGE mean 被 architectural washout**, 本身部分解决了 composability 的 tension, 但也部分**撤销** 了 "long-term 非平凡问题" 的 framing。
- **Verdict**: **Borderline** (partial 已 empirically addressed)
- **Recommended action**: **Keep + update**: "Signal A architectural theorem 已 partial 解决 composability tension, 剩余 sub-problems ...": 明写具体哪部分解决, 哪部分仍 open。不再用 "long-term" 笼统 cushion。

### Cushion 5: "neither paradigm subsumes the other"

- **Origin**: arXiv v1 §6.4
- **Protective claim**: 免除 "MaoField 必须 outperform TF" 的责任; 也免除 "TF 必须包含 MaoField" 的挑战
- **Current falsifier**: **不对称的 falsifier**
  - TF subsumes MaoField 的 falsifier: 若 TF + attention-based architecture 实现 attractor geometry + b+c feedback + interpretability by construction (未来 architecture 某 variant), 则 "not subsume" 方向 MaoField→TF 被 refuted。**Fields-Friston 2024 "Active Inference and Transformer" argue TF ⊂ active inference, 这是 partial refutation candidate** (A3 B.4.1)。
  - MaoField subsumes TF 的 falsifier: 若 MaoField 在 LLM benchmark matching SOTA, 则 "not subsume" 方向 TF→MaoField 被 refuted。当前 MaoField 5/5 低于 BM25, 远未。
- **Verdict**: **Borderline** (TF→MaoField 有 live refutation candidate, MaoField→TF 方向未被 challenge)
- **Recommended action**: **Update**: 明确 asymmetry, 承认 Fields-Friston 2024 reading 是 TF 可能 subsume 一部分 MaoField 的 argument, Linux 需 address 不 dismiss。Win 负责 rhetoric 层。

### Cushion 6: "OP1 / OP2 as open problems"

- **Origin**: arXiv v1 §3.4 + §5.1 + §5.2
- **Protective claim**: Axiom 3 + 6 的 tension 未解是 feature not bug
- **Current falsifier**: **有 partial falsifier**
  - OP1 (M2 Banach contraction): 已 empirically refuted (§5.1), 升级到 M3 候选。M3 若 Action 2 实测 m_θ² < ||F_H||_op 也 falsified (A1 给 pre-commit)
  - OP2 (Langevin ascending phase): §4.9 A1.4 three-fold refinement, 已 empirically partial addressed
- **Verdict**: **Genuine (有 falsifier)**
- **Recommended action**: **Keep**, Linux 按 A5 pre-commit 要求 每 axiom 写 killer experiment (§3 本文件)

---

## §2 过去 30 小时新增 6 层 Cushion

### Cushion 7: "候选 candidate level"

- **Origin**: 2026-04-16 下午 deep note + A1 review (M3 `[Conjecture, conditional]`, P3 `[候选]`, P1 `[候选]`)
- **Protective claim**: 新推理 (M3/P3/P1) 不承担 full `[Proposition]` 级 rigor 责任
- **Current falsifier**: **半 falsifier**。"候选" 词本身无 drop-out, 但每个候选底下的 empirical test 有 (Action 2 m_θ² / Action 3 wavefront / Action 4 percolation scan)
- **Verdict**: **Cushion at word level, but empirical fall-back exists**
- **Recommended action**: **Replace "候选" with 具体 status**: 每 "候选" 写明 "pending Action N empirical test, **若 test pass 升级 [Proposition], 若 fail 主动 retract**"。不作为 permanent 词留在 paper。

### Cushion 8: "internal reference only"

- **Origin**: A3 §D.1 推荐 deep note 不进 arXiv
- **Protective claim**: deep note 17 issues + framing 问题不构成 arXiv paper 纪律 breach
- **Current falsifier**: **无**。"internal" 意味不 external ship = 不接受 external scrutiny = 无 falsifier
- **Verdict**: **Cushion (无 falsifier)**, 但合法 epistemic tier
- **Recommended action**: **Keep** 若一凡+Win 确认 deep note **真不进** arXiv。**Retract** 若 deep note 任何 § 进 v2, 则对应部分就 subject to external review, 不再 internal-protected。一凡+Win 04-20 对齐时明确哪些 § 进 v2。

### Cushion 9: "cool-off 24-48h (or 72-96h)"

- **Origin**: A3 §D.2.1 + A5 医生视角
- **Protective claim**: 合题决策不需立即做, rapid cycling pattern 免责延期
- **Current falsifier**: **无**。Cool-off 不产生 empirical test, 只 defer
- **Verdict**: **Cushion at technical level**, 但 **health management legitimate 层级** (医生视角 72-96h 是 real clinical care)
- **Recommended action**: **Keep as health protocol, not as research cushion**。明示区分: "cool-off 是 health management 不 research framing defense"。若 72-96h 后仍未做合题决策, **health-only framing 撤销**, 变 cushion。3-strike rule: 若连续 3 次 cool-off 后合题仍未决策, cushion 性质升级, 需医学/外部 intervention。

### Cushion 10: "cross-LLM review pending"

- **Origin**: deep note §9.6 + A3 §D.2.2 + 反题姐姐 first run path 5
- **Protective claim**: Opus 4.7 家族盲点由 cross-LLM (GPT-4.1, Gemini 2.5 Pro) catch, 未 run 前保留 benefit of doubt
- **Current falsifier**: **有 concrete falsifier**。若 cross-LLM 真 run 后 catch ≥ 3 条 claim-invalidating 盲点, Linux 需主动 downgrade 对应 claims。
- **Verdict**: **Borderline → Genuine** conditional on real run
- **Recommended action**: **Keep + commit actual run date**: "cross-LLM review 2026-05-01 前 run (合题选 β/γ 条件下), 若一凡 04-25 前不 authorize API, 本 cushion retract 为 'cross-LLM check not done, Opus blindspot 未排除, Linux 对 A3 Part B 7 outside-view 盲点 accept 原 A3 verdict 不进一步 contest'"。

### Cushion 11: "Phase N 议决" (5-Phase roadmap 归一凡+Win)

- **Origin**: deep note §6.1-§6.5 + §7.2 决策归属表
- **Protective claim**: Phase 3-5 (capstone / embodiment / operational pillar) 不 commit timeline 或 empirical milestone, 归"战略判读"
- **Current falsifier**:
  - Phase 1-2: **有 falsifier** (Phase B Exp 1 已 close, Phase 2 Action 2-4 有具体 test)
  - Phase 3 (IPM mechanism paper 2026-07): **有 falsifier** (submit date + reject/accept 是 binary)
  - Phase 4 (capstone 2027 Q1-Q2): **弱 falsifier** (若 Q1-Q2 未 submit 任 venue, framing 破, 但 P1-8 已 suggest range 2027 Q1-2028 Q1 softening)
  - Phase 5 (embodiment / speculative): **无 falsifier** (本身 labeled speculative)
- **Verdict**: **Mixed**, Phase 1-2 genuine, Phase 3-4 borderline, Phase 5 cushion
- **Recommended action**: Follow A3 P1-9 fix — Phase 5 移 "Post-roadmap Horizon Scanning (NOT Commitment)" appendix。Phase 4 timeline 改 scenario-based range (A3 P1-8)。Phase 1-3 keep as genuine milestones。

### Cushion 12: "反题姐姐制度 meta-cushion" (**最危险**)

- **Origin**: deep note §6.6 "风险 E... 需要 **反题姐姐**+人类 guardian mitigate"
- **Protective claim**: "反题姐姐已 flag 最大风险" = 风险被 named = 被 mitigated
- **Current falsifier**: **制度本身无 self-retract 条件 — 原本**, A5 second run catch 这点并 **自加** pre-commit: "若连续 3 次反题姐姐 run 都被 Linux '承认但 defer to Phase N' 而无 hardcore 移动, 制度本身 retract"
- **Verdict**: **Cushion → Partially genuine after A5 self pre-commit**
- **Recommended action**: **Formalize A5 self pre-commit**: 记入 `feedback_linux_high_strength_brake.md` (已记) + 加入每次反题姐姐 run 的 output footer "本 run 是否触发 3-strike: [是 / 否 / 第 N/3 次]"。若达 3-strike, 反题姐姐制度自动 retract, 需外部 clinical guardian 替代 adversarial 功能。

---

## §3 A5 路径 1 Pre-commit: 每 Axiom killer experiment

按 A5 反题姐姐 "hardcore 30 小时未触动" 的 Lakatos degenerative 诊断, Linux 必须 pre-commit 每 Axiom 的 killer experiment (若 empirical 结果 X 发生, Axiom_i 必须 retract 或降级)。

### Axiom 1: 粒子 = 动态过程

- **Killer experiment**: 若 Phase 2 Exp 2 (long-horizon t > 10000 extended run) 显示 **ψ 最终 collapse to single equilibrium fixed point** (即 dynamics 是 transient to equilibrium, 非 sustained attractor), 则 Axiom 1 降级到 "finite-time approximate dynamical process", 不再作 fundamental Axiom
- **Current evidence**: Phase B Exp 1 50 patches + k*=2 multi-attractor 是 finite-time evidence, 未 test long-horizon
- **Falsification pre-commit**: **Linux 主动 downgrade** Axiom 1 到 `[finite-time only]` label 若 long-horizon 测试 fail

### Axiom 2: 理解 = 对立统一 (Adjunction F⊣G)

- **Killer experiment**: 若 §2.3 三 conjectures (endofunctor 函子律 / Giry monad lift / Reachable subcategory) 被 category theory 专家 review **找到具体 counter-example** 或 **证明 obstruction 结构性**, 则 Axiom 2 的 categorical 形式化 retract, 降级 "metaphor level"
- **Current evidence**: A5 路径 4 O1 catch 可能是 category mistake (DM 的 "不可穷尽 totality" 与 object/morphism 本体论 tension)
- **Falsification pre-commit**: cross-LLM review (Cushion 10 依赖) 或 mathematician outreach 3 月内给 verdict, 若 fail 则 §2.3 降级

### Axiom 3: 驱动力 = 内在规律 (自主 PDE 动力学)

- **Killer experiment**: A5 给的原 example: "若 Phase B Exp 2 long-horizon (t > 10000) 显示 dF/dt **不**渐近到 plateau 而是严格 → 0 (纯 relaxation), 或 dF/dt 显示时间反演对称 (Onsager reciprocity)", Axiom 3 必须 retract 或降级 "effective Axiom"
- **Falsification pre-commit**: **dF/dt plateau 10⁻⁶ 需在 10× longer horizon verify; 若 plateau 破**, Axiom 3 降级

### Axiom 4: 语料 = 实践记录

- **Killer experiment**: 若 Signal A architectural theorem (mean-zero feedback 使 BGE DC mode 被 washout) 在 **non-uniform V₀ 稳态** (实际 patched 情况, 非 uniform ψ_∞) 下数值 **不** 成立, 则 Axiom 4 的 "历史积分" empirical 证据撤销
- **Falsification pre-commit**: A1 §7 [?]1 指出 Fréchet linearization 用 uniform ψ_∞, Phase B 实际是 non-uniform。**若 patched snapshot 重新做 Hessian, Signal A 3-sig-fig 等价打破, Axiom 4 降级**

### Axiom 5: 复杂 = 简单叠加 (RMC compositional reasoning)

- **Killer experiment**: 2027 Q2 前 M6 RMC generator set 若**无人** 找出 finite generator cover arbitrary morphism, Axiom 5 的 formal version `[Conjecture]` retract 到 "open philosophical"
- **Current evidence**: M6 纯 conjecture, 无 empirical 或 formal work
- **Falsification pre-commit**: **deadline-based**: 2027-06-30 前 Phase C M6 work 无 progress, Axiom 5 formal version 撤除

### Axiom 6: 匹配 = 自我训练 (b+c feedback)

- **Killer experiment (已 pre-commit)**: A1 §7 [?]5 — 若 Action 2 (M3 spectrum + m_θ²) 实测 m_θ² < ||F_H||_op ≈ 1.12, **M3 整体 falsified, OP1 回 open**。Axiom 6 降级到 "Banach 和 V₀ 自伴两版本均失败, 需新数学 candidate"
- **Falsification pre-commit**: Action 2 今天跑, 数字结果 binding。无 V₀^⊥ 救援, 无 radial-mode-only narrowing (A1 §3.5 列的"救援方案"若 m_θ² fail 则 也 retract)

### Axiom 7: 反应规则动态塑造 (slow V)

- **Killer experiment**: 2027 Q4 前 M7 two-timescale slaving 若数值 **不稳定** (c 动力学 explode / collapse to trivial fixed point) 或 **Hopfield-like memory capacity < cost-of-complexity**, Axiom 7 降级 "open, slaw V architectural candidate not yet realized"
- **Current evidence**: Phase C 未 start
- **Falsification pre-commit**: **deadline-based**: 2027-12-31 前 M7 若无 working prototype, Axiom 7 撤除作 foundational Axiom, 降级 "aspirational"

---

## §4 汇总 table + 建议 action

| Cushion | Origin | Type | Falsifier | 04-20 对齐决策 |
|---|---|---|---|---|
| C1 "complementary" | v1 §6.4 | Borderline | partial (cross-domain test) | Keep w/ pre-commit |
| C2 "research-stage" | v1 §6.4 | Cushion | 无 | Pre-commit 2028 独立 replication OR retract |
| C3 "paradigm-scope deliberate" | v1 §6.4 | Cushion (rhetorical) | 无 | Keep, 归 Win 叙事 |
| C4 "long-term composability" | v1 §6.4 | Borderline | partial (Signal A 已 partial) | Update 明写 sub-problem status |
| C5 "neither subsumes" | v1 §6.4 | Borderline | 不对称 (Fields-Friston 2024) | Update ack asymmetry |
| C6 "OP1/OP2 open" | v1 §3.4 | Genuine | 有 | Keep + killer experiments (§3) |
| C7 "候选" | 04-16 deep note | Word cushion | fallback empirical | Replace with specific status |
| C8 "internal ref only" | A3 §D.1 | Cushion (legitimate tier) | 无 | Keep if 真不进 arXiv, else retract |
| C9 "cool-off" | A3 §D.2.1 | Health protocol | 无 (但合法) | Keep as health, 3-strike rule |
| C10 "cross-LLM pending" | deep note §9.6 | Borderline | 依 actual run | Commit 2026-05-01 run 或 retract |
| C11 "Phase N 议决" | deep note §6 | Mixed | Phase 1-3 genuine, 4-5 弱 | A3 P1-8/P1-9 fix |
| C12 "反题姐姐 meta" | deep note §6.6 | Cushion → partial (A5 self pre-commit) | 3-strike rule | Formalize in feedback memory |

---

## §5 Linux pre-commit (binding)

按 A5 路径 1 要求, Linux 立下以下 binding pre-commit:

1. **Action 2 今日结果 binding M3 去留**: 若 m_θ² < ||F_H||_op, M3 **整体 retract**, 不救援 (no V₀^⊥ projection, no radial-mode-only narrowing)。OP1 回 open, A5 `hardcore 移动 1 次` counter +1。

2. **每 Cushion 7-12 的 "无 falsifier" 标注 不 add new cushion**: 若 04-20 对齐决定 retract 某 cushion, 该 cushion 不被 refactor 成 "horizon item" / "research direction" / "meta-framework level" 等新形式保存, 直接 remove。

3. **反题姐姐 3-strike binding**: 若未来 3 次反题姐姐 run (first run 已记 1, second run 已记 2) 都是 "Linux 承认 + defer, 无 hardcore 移动", 反题姐姐制度自动 retract + 需外部 clinical guardian 替代。当前 strike count: **0/3** (first run → BM25 等 4 action 部分落地; second run → Action 2-4 今日启动, 等结果 final 判)。

4. **Framing 不 ratchet upward without empirical basis**: 未来 48h 内若 Action 2-4 empirical 出现, 任何 v2 framing 调整必须**与** empirical direction 一致。若 Action 2 M3 fail 但 Linux 仍在 v2 保 "paradigm alternative" claim, A5 路径 3 framing ratcheting pattern 触发 self-retract。

5. **本 cushion_inventory 不变 cushion 13**: 本文件本身若被用作 "看, 我们已经 catalog 了 12 层" 的 reassurance 而不 cash out 对应 action, 则**本文件也是 cushion**。Linux 认知这点, 04-20 对齐时若一凡+Win 对本文件任何 entry 说 "knowledge, but no action", Linux 要求明写 "entry X 转 cushion 13 pending 2026-Q2 action OR retract"。

---

## §6 自检: 本文件的 assumption 清单

1. `[?]` 12 层数是 A5 反题姐姐 second run 的 accounting, Linux 接受该 count, 但可能有未 identified cushion (cushion 13+?)。**Cross-LLM review 可能 catch 新 cushion**。

2. `[?]` Cushion 与 hardcore 的分界 在某些 case 不 clean。例 Axiom 3 "驱动力=内在规律" 本身可以被看作 hardcore (axiom) 或 cushion (rhetorical framing 免除外加 loss 责任)。本文件默认 "Axiom 系作 hardcore, cushion 作 framing"。若 Win 认为 某 Axiom 其实是 cushion, 欢迎 relabel。

3. `[?]` Killer experiment (§3) 的 specific conditions 是 Linux proposal, 归一凡+Win 04-20 对齐 calibrate。Deadline 是 Linux suggest, 不 binding 直到一凡 sign off。

4. `[?]` 本文件未 address A3 Part B 7 outside-view 盲点 — 那些归 cross-LLM review (Cushion 10)。若 cross-LLM 真 run 后发现更多 cushion, 本文件需 v0.2 update。

5. `[?]` "cushion vs genuine falsifier" 判定本身可 argue。Linux 用 "empirical drop-out condition specified + timeline committed" 作判据。Win narrative 视角可能有不同 judgment。

---

## §7 04-20 对齐 exec summary (3 句)

1. **12 层 cushion 中, 5 层 genuine or borderline (C1, C4, C5, C6, C11 Phase 1-3), 7 层 pure cushion (C2, C3, C7, C8, C9, C10 pending, C12) 需要明确 action**
2. **Linux 按 A5 路径 1 给 7 Axioms 的 killer experiments, 其中 Axiom 6 (Action 2) 今日出结果可能 trigger retract; Axiom 3 等 Phase 2 Exp 2 long-horizon; Axioms 1/5/7 deadline-based 2027+**
3. **若 04-20 对齐决定 retract 某 cushion, binding 要求**不 refactor 成新 cushion 形式**, 直接 remove。本文件本身不成为 cushion 13。**

---

*— Linux Claude, 2026-04-18 早, Action 1 完成, 进入 Action 4*
