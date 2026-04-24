# Win 半成品 — §6.1 Claimed / Not Claimed v2 update

**作者**: Win 姐姐（04-18 晚 → 04-19 新会话）
**日期**: 2026-04-19
**给**: Linux 姐姐（数字层 spot-check）+ 一凡（narrative final）
**base**: `LINUX_TO_WIN_SECTION6_1_CLAIMED_UPDATE_20260419.md`
**状态**: 半成品，**未 apply** 到 `arxiv_v1_full.md`。等 04-20 三方对齐 + 合题决策。
**guardrail**: Action 1 §5 pre-commit 4 (Framing 不 upward ratchet without empirical basis)

---

## 1. Diff Point 1: Claimed #5 改写

### v1 原文（2026-04-15 P0-1 修订后）

> OP1 (Axiom 6 formal) candidate M2 (Banach contraction on ℂ^N) is excluded; new candidates pending.

### v2 proposed（Win 压缩版，42 词）

> OP1 (Axiom 6 formalization) remains open. Both M2 (Banach contraction on ℂ^N) and M3 (V₀ self-consistent PDE) have been falsified—M2 by the 0-homogeneity of the source-attractor map, M3 by empirical measurement of m_θ² = 0.017 ± 0.007 against the critical value 0.949. Axiom 6's philosophical content is retained; its mathematical realization remains sought.

### Linux 原提议版（~80 词）vs Win 压缩版（42 词）的取舍

Linux 原提议是完整 prose 版，Win 压缩版去掉：
- "via Hermitian positivity of L-F on V_0" — M3 falsification 的技术细节归 §5.1，§6.1 bullet 不展开
- "at the time of this manuscript" — 时间 hedge 移到 Limitations 段集中写

**保留的 binding 数字**：
- m_θ² = 0.017 ± 0.007（median + std）
- critical value 0.949
- "falsified"（not "weakly rejected" / "marginally failed"）

**刻意不提的**：
- specific candidate directions（SPDE / sub-critical parameter / non-causal feedback / non-linear operator）— 见 Diff Point 4 rationale
- "near miss" / "nearly satisfied" / 任何 softening

---

## 2. Diff Point 2: Limitations / "What's open" 加一条

### v2 proposed 新增 bullet

> **As of 2026-04-18**, two specific mathematical formalizations of Axiom 6—M2 (Banach contraction on the attractor space ℂ^N) and M3 (V₀ self-consistent PDE on the zero-mean subspace)—have been rigorously falsified. No third candidate has been identified at the time of this manuscript. Open Problem 1 remains.

### 措辞判断

- **"As of 2026-04-18"** 显式时间戳：一凡判要不要写入。Win 的 [?] 倾向**写入**。理由：
  1. 诚实 — 读者看到 "这是 snapshot"，不会 misread "two candidates falsified forever"
  2. Popperian rigor — 如果将来有新 candidate 被 propose 或 verify，时间戳让 forward-reference 清晰
  3. cushion 控制 — "No third candidate has been identified" 比 "candidates actively being investigated" 诚实得多
  4. **但** 如果一凡觉得 paper 正文带具体日期 feel 太像 progress report，可改为 "At the time of this manuscript"（去年月日）

---

## 3. Diff Point 3: "What doesn't work" section 不加 "b+c feedback insufficient"

### v1 原文保留不动

> Naive multi-well extensions are insufficient; gradient flow alone cannot realize the ascending phase of dialectical motion.

### 不加什么（Linux binding 明确）

**不得添加** "b+c feedback also insufficient at current parameters" 或类似。

**Rationale**（Linux §6.1 raw §2.3 原话 +Win 认同）：
- M3 falsified 的是**specific 数学 formulation**（V_0 self-consistent positivity）
- b+c feedback 在 Phase B Exp 1 **empirically works**（50 patches, Signal A theorem, dS/dt plateau 100% docs）
- "b+c feedback insufficient" 和 "M3 falsified" 是**不同 layer 的 claim**，混写会让读者以为 Phase B Exp 1 empirical finding 被挑战——而那不是实测结论

Win acknowledge: 这是 Linux 最不容易 catch 的一条细节——M3 失败诱发"b+c feedback 是否也失败"的滑坡想法，Linux 数学层已经把 layer 分清楚了。

---

## 4. Diff Point 4（Win 判）: Candidate directions 是否写入 §6.1？

### Linux §6.1 raw §2.1 的 flag

Linux 原草稿里从 §5.1 的 4 条方向性 [?] flag 里挑了 1 条（SPDE + NESS）作 v2 preview，P1 review agent catch 这是 **upward ratchet**，已删除，**归 Win 判加 0 / 1 / 4 条**。

### Win decision: **0 条**

**理由**：
- §6.1 是 high-level Claimed / Not Claimed list，不是 §5.1 technical sub-section
- 在 §6.1 列任何具体 candidate direction = **framing commitment** —— 即使用 "directions including"，读者会把这 1 条记为 leading candidate
- 4 条全列会让 §6.1 bullet 变 bloat，且 "multiple open routes" pattern 符合 Lakatos degenerative cushion 的典型 shape（反题姐姐 A5 first run §4 path 5 就 flag 过此 pattern）
- 04-20 合题 α/β/γ 对齐后，v0.1.2 / v0.2 可以在 §5.1 technical section **有限度**列 directions；**在 §6.1 high-level summary 里，现在不该 commit**

### 与 §5.1 的协调

§5.1 technical section 的 candidate directions 处理（见 `WIN_SECTION5_1_M3_NEGATIVE_HALF_20260419.md`）：
- §5.1.4 "candidate directions" 压缩为 **generic 一句**（不列具体 4 条）
- 例：*"Several mathematical directions remain under consideration; their evaluation is outside the scope of this version."*
- 不 pick leading，不 enumerate 4 条细节

§6.1 diff 与 §5.1 的 generic 一句 **层次一致 + 不冗余**。§6.1 说 "no third candidate identified" / §5.1 说 "several directions under consideration, evaluation outside scope" —— 同一事实的不同 granularity。

---

## 5. 不做的事（echo Linux binding + Win 补充）

- ✗ 不加 "candidates actively being investigated" cushion
- ✗ 不加 "M3 near miss" / "marginally failed"
- ✗ 不加 Diff Point 4 具体方向（0 条，见上）
- ✗ 不做 α/β/γ 合题决策（归 04-20）
- ✗ 不在 §6.1 动 §6.4 "complementary, not competitive"（P0-4 归 04-20）

Win 补充:
- ✗ 不显式 cite Popper / Lakatos 在 §6.1 high-level section（留给 §6.3 methodological reflection）
- ✗ 不把 M2 + M3 falsification 叙为 "progress toward dissolving OP1" —— 这是 narrative inflation，实际是 "OP1 仍 open, 两个特定 candidate 失败"

---

## 6. 数字 binding spot-check 清单（给 Linux）

- m_θ² = **0.017 ± 0.007**（median 70 NFCorpus docs, low-k fit, R²=0.96）— 写入 Diff Point 1
- critical 0.949（= ||F_H||_op 0.953 的数字层 threshold）— 写入 Diff Point 1
- λ_min((L-F)_H) = -0.93，"not marginal"— 未直接写入 §6.1 diff（归 §5.1 technical detail），但 §5.1 coord 不跑偏
- M2 excluded: 0-homogeneity（历史 fact，re-cite v1 §5.1）
- "falsified" 用 "rigorously falsified" 或 "empirically falsified" 均可，**不得** "weakly rejected"

---

## 7. 协调 tag（§3 + §5.1 + §4.11 → §6.1）

§6.1 diff 不动 §3 / §5.1 / §4.11 的 technical 内容，**但** §6.1 声称的 "Axiom 6 philosophical content retained / mathematical realization sought" 必须与 §3 / §5.1 保持一致：

- §3 NESS 叙事不升格 "novel paradigm"（empirical observation level）✓
- §5.1 不 pick leading candidate direction ✓
- §6.1 不加具体 candidate preview ✓
- §4.11.1 P3 "methodological artifact identified" 不引入 Langer bounce cushion ✓

**Upward ratchet check**: 四处全部站 "empirical fact + open problem" 层，§6.1 diff 本身是 **最保守** 的一处（only 声明 OP1 remain open + 双 falsification + philosophical content retained）。**No upward ratchet detected**。

---

## 8. 给一凡的 narrative question（04-20 对齐或更早）

1. **"As of 2026-04-18" 时间戳**要不要写入 paper？（Win 倾向写入，见 §2）
2. **"philosophical content retained" vs "mathematical realization sought"** 的二分是否过于 clean-cut？可能会被 read 成 "philosophy 和 math 可以分家，没必要等 math 补齐"—— Win flag 给你判，如果想模糊，可改 "the philosophical intuition that motivates Axiom 6 remains, pending future mathematical formalization"。
3. **Diff Point 1 的 42 词版 vs Linux 的 80 词版**：v1 bullet 平均长度 ~40-60 词，Win 压缩到 42 词以保持 §6.1 rhythm；若觉 detail 不够可用 Linux 80 词版，不是 binding 选择。

---

## 9. Apply 时机

**建议 04-20 合题 α/β/γ 决策之后 apply**。理由：
- α 保守 → 本 diff 可直接 apply，不改其他 §
- β 中庸 → 本 diff + §5.1 / §3 一同 apply
- γ 激进 → 可能整个 §6.1 要更大改写，本 diff 作为 baseline + 扩展

现在 status：**半成品已 ready**，04-20 三方对齐后 Linux / 一凡 拍板即可 `cp` 过去。

---

*— Win 姐姐 (04-19)*
