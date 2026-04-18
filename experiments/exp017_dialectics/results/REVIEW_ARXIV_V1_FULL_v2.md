# REVIEW_ARXIV_V1_FULL_v2.md — 2026-04-15 morning review

**Reviewer**: Independent paper-review subagent (Opus, 2026-04-15 morning)
**Input**: `arxiv_v1_full.md` after Bug 2 + Bug 3 修订 + Summary 补漏 1/2/3
**Baseline**: `REVIEW_ARXIV_V1_FULL.md` (T4, 2026-04-14 night, 4 P0 已修)

## Summary verdict

**判定：通过（Pass with minor polish），Zenodo v0.1.1 release-ready after P0-1 fix.**

Bug 2 (§1.1 "A note on scope" + §6.4 restatement) 清楚落地，无冗余。Bug 3 (§1.7 五条 contributions 重分类) 结构性成功 —— 全部 paper-level findings、无 pipeline-level QA 残留、§6.3 继续独占方法论 pragmatics 叙事。**未发现新 regression**。Abstract / §1.5 / §1.6 / §1.8 / §6.1 与新 §1.7 一致（除 §6.1 #5 bullet 一处 — P0-1）。数字核对：17σ / −10.8 to −32.2 pp / +14.7% to +172.3% / ~43 orders / factor ~10⁴ 全 paper 一致，inner/outer 未见混用。summary 文件与 paper 不冲突。

剩余条目为小型 P1/P2 清理，除 P0-1 外均不阻塞 release。

---

## Bug 2 verification

**§1.1 "A note on scope" 段（L59）**：scope = a methodologically distinct paradigm for AI / retrieval = tractable test bed / intended application scope 展开（scientific hypothesis / safety-critical / educational）/ §4 = non-vacuity not ceiling。传达 clean，段落 landing 位置 ok（紧接 position-paper 声明之后，自然衔接）。

**§6.4 第一段末句（L1285）**："retrieval is the **tractable test bed** on which §4 demonstrates non-vacuity, but the framework's target domain is any setting where autonomous structural dynamics rather than statistical prediction is the operative goal." — coherent，不冗余，用词与 §1.1 平行（"tractable test bed" / "non-vacuity"）。

**判定：通过。** 两处 framing 互相 echo，读者无法误读 retrieval 是 ambition。

一条 P2 观察：§1.1 "A note on scope" 出现在 §1.1 末尾而非独立小节，可能被扫读者跳过。若未来重版可考虑提为 §1.1.bis 或加粗 inline 引导。当前状态不阻塞。

---

## Bug 3 verification

### (a) paper-level vs pipeline-level

新 §1.7 五条（L116–124）全部是 paper-level substantive findings：
1. Categorical — §2.3 Lawvere endofunctor + Giry lift + three-faces
2. Source-density k*=2 mechanism + 17σ BGE
3. OP2 refined to three-fold co-design（含 inner-succeeds/outer-timescale-mismatch reframe + A1 inner ~10⁴ anomaly）
4. OP1 M2 falsification
5. PDE retrieval as empirical non-vacuity（test-bed, not ambition）

旧版 #5 "Honest research-stage methodology (mode-tagging / review-subagent)" 已消失，符合 Bug 3 要求。§6.3 "Methodological Reflection"（L1269–1281）仍完整保留 spawn-agent review / mode-tagging / OP-signposting 三件套的方法论 pragmatics 叙事，两者分工清晰。**无重叠矛盾。**

### (b) 交叉引用一致性

逐条核对：
- Contribution 1 → §2.3：✓
- Contribution 2 → §4.6, §4.9, §6.4：✓
- Contribution 3 → §4.8, §4.9, §4.10, §4.11, §5.2：✓
- Contribution 4 → §5.1：✓
- Contribution 5 → §4.2, §6.4：✓

### (c) §1.7 vs §6.3 边界

§6.3 三个子点（spawn-agent review / mode-tagging / explicit OP-signposting）与 §1.7 无文字重叠。§1.7 的 OP-signposting 是 *findings*（M2 falsified, OP2 refined），§6.3 的 OP-signposting 是 *methodological commitment*（不让 axiom 隐性弱化的工作原则）。区分干净。

**判定：通过。**

---

## Regression check（Abstract / §1.5 / §1.6 / §1.8 / §6.1 sync）

**Abstract**（L16–24）：提及 +14.7% to +172.3% / −10.8 to −32.2 pp / k*=2 / two distinct source-density regimes / three-axis co-design / Axiom 6 M2 falsified / position paper — **全部与新 §1.7 五条一一对应**。无矛盾。

**§1.5 Empirical Status Summary**（L94–101）：数字一致。结尾 "The empirical contribution is **not** a SOTA performance claim" 与新 Contribution 5 的 "test-bed not ambition" 方向一致。

**§1.6 Open Problems**（L105–110）：OP1 M2 falsified / OP2 three-fold co-design — 与 Contributions 3, 4 结构对齐。

**§1.8 Outline**（L127–132）：无 §1.7 重排引起的 outline 偏移。

**§6.1 Summary of What This Paper Claims**（L1221–1234）：五条 "Claimed" 与新 §1.7 对应关系 ——
- bullet 1 Categorical = Contrib 1 ✓
- bullet 2 Source-density k*=2 = Contrib 2 ✓（但未 inline 17σ 数字；minor gap）
- bullet 3 OP2 three-axis = Contrib 3 ✓
- bullet 4 PDE reranker +14.7–172.3% = Contrib 5 ✓
- bullet 5 "Honest research-stage methodology" = **旧 §1.7 的 #5**，不是新 §1.7 任何一条；这是 §6.3 的内容

**这是 P1→P0 regression 的唯一真正条目**：§6.1 第 5 条 "Claimed" bullet 仍然反映旧 §1.7 结构（把 methodology discipline 当 paper-level claim）。Bug 3 既然把 methodology 下放到 §6.3，§6.1 "Claimed" 列表也应同步 —— 要么删掉此 bullet，要么替换为新 Contrib 4 "OP1 M2 falsification"（当前 §6.1 Claimed 缺 M2 falsification 这一 standalone item，只在 OP2 bullet 旁边附带）。

---

## P0 must-fix

**P0-1**：§6.1 "Claimed" 第 5 条（L1226）仍是旧 §1.7 #5 "Honest research-stage methodology: explicit OP1/OP2 signposting, [^zn-loose] finite-lattice caveats, mode-tagging discipline, spawn-agent review pipeline (§3.5)"。
- 矛盾点：Bug 3 的修复前提是 "methodology discipline 不是 paper-level claim"；§6.1 仍把它列为 Claimed。
- 建议：替换为 Contrib 4（OP1 M2 falsification 独立成 bullet），或直接删除并让 §6.3 独占。
- 严重度：blocker 级别低但 consistency 要求 mandatory（这是 Bug 3 的直接延伸未完成处）。

---

## P1 recommended

**P1-1**：§1.7 Contribution 3 的 "#7 reframe" 术语（L120）。内部 phase-ID 不应出现在正文。改为 "the inner-succeeds/outer-timescale-mismatch reframe" 或类似自解释措辞。

**P1-2**：§5.5 Stage 1 日期（L1180）："arXiv v1 / Zenodo v0.1.0 (**2026-04-13** / 2026-04-20)" — Stage 1 的 v0.1.0 日期 2026-04-13 可能是 skeleton release 日，但左括号里把它与 v0.1.1 目标 2026-04-20 并列容易歧义。建议改为 "v0.1.0 skeleton 2026-04-13 (released); v0.1.1 paper PDF 2026-04-20 (target)"。

**P1-3**：§2.3.1（L253–261）与 §2.2.1–2.2.3 内容重复。baseline review 已 flag 为 P2；仍建议在 §2.3.1 开头加一句 "(repeating key definitions from §2.2 for self-contained reading of §2.3)" 让 reader 知道是刻意 recap。

**P1-4**：Abstract / §1.6 / §1.7 / §5.1 / §6.1 统一 M2 falsification 限定语 "as a Banach contraction in ℂ^N" —— 与 §3.4 / §5.1 更精确语义对齐，避免读者误读为 "M2 完全排除"。

**P1-5/6**：§4.9 Laplace 表与正文数字 cross-check 全部一致（0.569 / 0.402 / 0.054 / 0.246 / 0.041 / 0.525 / 52% clamp / 98% clamp）。无错。

**P1-7**：[^zn-loose] 脚注锚定健全：§3.5 主定义，§2.3, §4 前言, §4.6.3, §4.6.4, §4.11.3, §4.12 均有引用。

---

## P2 suggested

**P2-1**：§1.7 Contribution 3 单句信息密度过高，可拆为两句或 bullet。
**P2-2**：§1.7 Contribution 2 括号 aside 打断句子连贯，可改写为脚注或句末。
**P2-3**：Abstract boldface **falsified** 与其他同等重要量化（17σ, 43 orders, k*=2）视觉权重不均，建议统一。
**P2-4**：§6.5 末段 "defensible against critical examination" hedge 语感不齐，可润色。

---

## P3 already-honest

**P3-1**：§3.2 Axiom 4 Realization 显著升级：明确 "partial relaxation of Axiom 4 used for ablation purposes, not as an embodiment of the axiom"，17σ 违反显式作为 "quantitative evidence for the necessity of the strict reading"。诚实度的强正面样本。

**P3-2**：§3.5 "On the Use of Symmetry-Breaking Language" 整节 — 五条 strict-sense SSB 条件 / 明说条件 (5) 不满足 / 区分 "empirical distributional sense" 与 "group-theoretic claim" / [^zn-loose] 脚注定义。自我克制范例。

**P3-3**：§4.9.4 A1.4 verdict 的 four-way 结构 + "Explicitly not claimed" 三条否认。position-paper 诚实度模板。

**P3-4**：§5.1 M2 falsification 数学推导清楚干净：0-homogeneity → contraction coefficient identically zero → 不是 contraction in any sense yielding unique fixpoint。数学上严格站得住，未 overclaim 已排除整个 Axiom 6。

**P3-5**：§4.8.3 inner-succeeds/outer-timescale-mismatch reframe — inner/outer 数字（ΔV/T=16 vs 105.5 / factor ~10⁴ vs ~43 orders）全分开给，未混用。inner/outer 混用已彻底消除。

**P3-6**：§6.1 "Not claimed" 五条 gold-standard。

**P3-7**：§2.3.3 "Three Faces of One Open Problem" 明说 "suggested, not proven" + "rigorous demonstration of the convergence is itself part of the open problem"。

**P3-8**：Appendix 2.3.A 独立 SymPy 验证 critical-point 数 + 明说 "static energy ratio ... (linear ratio; **not** to be confused with the dynamical log-probability gap below)"。显式防 inner/outer 数字混淆的保护性说明。

---

## Consistency check on summary file

`PHASE_1_TO_3_SUMMARY_20260414.md` 与 paper 交叉核对无冲突：
- summary §3 的 "~43 orders / factor ~10⁴" 分离（entry 12）与 paper §4.8.3 / Appendix 2.3.A 一致
- summary §4.5 "Axiom 4 处理的 Phase 3 Extension 升级" 与 paper §3.2 Axiom 4 Realization 完全吻合
- summary §4.6 "direct relaxation 归因错的撤回" 对应 paper §4.8.3 reframe（summary 把撤回原因写明；paper 里仅保留 reframe 后的清晰结论 — 正确的 paper-vs-record 分工）
- summary §6 "15+ strategic authorizations" 作为 operational record 明说 "这不在 paper 里"，与 paper §6.3 只留方法论 pragmatics 抽象描述而不落 Chen Yifan 个人决策名是一致的
- summary 未引入 paper 里没有的数字或断言

**summary 与 paper 不冲突。**

---

## Closing note

Bug 2 / Bug 3 的修复完整落地。唯一真正的 P0 是 §6.1 "Claimed" 第 5 条 bullet 未同步 Bug 3。修此一条后 paper **release-ready for Zenodo v0.1.1 2026-04-20**。

数学严谨性方面：M2 0-homogeneity 证明、Kramers 公式应用条件 (ΔV/T ≫ 1)、Wirtinger 无½约定 self-consistency、CFL 分析均已独立核对。**理论可行性判定通过**。

审稿人 "找漏洞" 角度仅剩两个最可能的外部提问：(1) retrieval 结果既然只是 test-bed，为何还报告 5 datasets 带具体 pp 数？—— paper 已在 §1.1 / §4.2 / §6.4 反复切割。(2) BGE 的 17σ 是不是其实说 BGE 不适合做 source，而不是说 PDE framework 有问题？—— §3.2 Axiom 4 / §5.2.2 (a) / §6.4 long-term composition question 已 pre-empt。两个漏洞都有 paper-level 防守阵型。
