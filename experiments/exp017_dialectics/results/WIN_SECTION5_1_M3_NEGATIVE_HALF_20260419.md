# Win 半成品 — §5.1 Axiom 6 formalization: M2 + M3 双 falsification v2

**作者**: Win 姐姐（04-18 晚 → 04-19 新会话）
**日期**: 2026-04-19
**给**: Linux 姐姐（数字 + Popperian outline spot-check）+ 一凡（narrative final）
**base**: `LINUX_TO_WIN_SECTION5_1_M3_NEGATIVE_RESULT_20260419.md` + `ACTION2_M3_EMPIRICAL_VERIFY_20260418.md`
**状态**: 半成品，**未 apply** 到 `arxiv_v1_full.md`。等 04-20 三方对齐。
**guardrail**: Action 1 §5 pre-commit 4 (Framing 不 upward ratchet without empirical basis)

---

## 1. §5.1 v2 结构（Linux outline + Win 判断）

```
§5.1 Axiom 6 formalization: Open Problem 1 (OP1)

§5.1.1 M1: Original formulation (no formal form)
§5.1.2 M2 candidate: Banach contraction on ℂ^N — excluded
§5.1.3 M3 candidate: V_0 self-consistent PDE — empirically falsified
§5.1.4 OP1 status: open, two formalizations falsified, invitation to collaborators
    [summary table]
    [Popperian reading]
    [generic candidate directions, 1 句, no leading]
```

**Win judgment**: 采用 Linux outline 的 4-subsection 结构。**Table** 放在 §5.1.4 开头（Linux [?] 建议 table 紧凑——Win 同意），Popperian prose 和 candidate directions 跟在 table 之后。

---

## 2. §5.1.3 M3 candidate prose（Win 草稿）

### Proposed text

> **§5.1.3 M3 candidate: V₀ self-consistent PDE (2026-04-16 proposal)**
>
> Building on the exclusion of M2 (§5.1.2), we proposed a second formalization candidate, M3: restrict the domain to the zero-mean subspace V₀ = {δψ : ∫δψ dx = 0}, Fréchet-linearize the attractor dynamics around ψ_∞ = v, and identify Axiom 6 realization with the requirement that (L − F) be positive definite on V₀. Here L = −D∇² + V″_eff(ψ_∞)[·] is the linearized Allen-Cahn operator and F = αI + βK is the b+c-feedback operator with K the causal history convolution kernel.
>
> `[Conjecture]`—stated in v1 §5.1 as a prospective route. A rigorous mathematical framing (dispatch A1, 2026-04-16) established the non-self-adjointness of F via a Hermitian-part decomposition (A1 Proposition A1.1), identified the angular pseudo-Goldstone mode as the critical eigenmode on V₀, and gave an ℓ¹ upper bound ||F_H||_op ≤ 1.118.
>
> **Empirical test design (dispatch A2, 2026-04-18).** Extract the effective angular mass m_θ² from Phase B Experiment 1 stationary-state field snapshots via polar decomposition of ψ followed by a low-k propagator-pole fit of S_θ(k) = A/(Dk² + m²) with D = 0.1 fixed. M3 passes iff m_θ² exceeds the measured Hermitian-part operator norm ||F_H||_op, i.e., iff the restoring force on the softest V₀ mode dominates the feedback destabilization.
>
> **Result.** On 70 NFCorpus documents (median, low-k fit window k_max = 6, R² = 0.96):
>
> - ||F_H||_op = **0.953** (tighter than the A1 ℓ¹ bound of 1.118)
> - critical threshold = **0.949**
> - m_θ² measured = **0.017 ± 0.007** (median) / **0.026** (95th percentile upper bound)
> - λ_min((L − F)_H on V₀) = **−0.93**
>
> The measured m_θ² is below the critical threshold by a factor of 35× (at 95th percentile) to 55× (at median); λ_min is negative-definite at 97% of ||F_H||_op, not marginal. **M3 is falsified.** `[Falsified]`
>
> **No rescue.** Per pre-committed Action 1 §5 discipline, three potential salvage routes flagged in A1 §3.5 (orthogonal-projection to V₀^⊥ narrowing, explicit U(1)-breaking augmentation beyond what the BGE source already provides, radial-mode-only restriction of the M3 claim) are **not** pursued. Each would preserve the epistemic status of M3 while altering its empirical content—a Lakatos-degenerative pattern that the project's methodological discipline (cf. §6.3) precludes. M3 is retracted in full; OP1 is returned to open.

### Win narrative judgments 注记

1. **"prospective route" for v1 framing** — 不说 v1 "错"，说 v1 "stated as prospective" ——诚实 + 不 self-flagellate
2. **`[Conjecture]` → `[Falsified]` mode tag transition 显式写入** — Popperian transparency，读者一眼看到 status 变化
3. **"not marginal" 显式写入** — Linux binding 数字要求："λ_min = −0.93, 不 marginal"
4. **"three potential salvage routes... not pursued"** — 诚实列出 potential rescue 路径 + 明说 **不走** + rationale（Lakatos-degenerative pattern + §6.3 cross-ref）——反题姐姐 A5 second run 的 12 层 cushion inventory 直接受此段呼应
5. **"cf. §6.3" cross-reference 替代显式 Popper/Lakatos cite** — §5.1 technical section 不拉 philosopher name，让 methodological rigor 的底气在 §6.3 methodological reflection 集中
6. **OP1 returned to open** 不 soften 为 "OP1 receives additional context" 或类似

---

## 3. §5.1.4 OP1 status prose（Win 草稿）

### Proposed text

> **§5.1.4 OP1 status: open, two formalizations falsified**
>
> **Table 5.1.** Axiom 6 formalization candidates, as of 2026-04-18.
>
> | Candidate | Form | Status | Basis for exclusion |
> |---|---|---|---|
> | M1 | Original Axiom 6 statement, no formal form | Philosophical claim, preserved | — |
> | M2 | Banach contraction on the attractor space ℂ^N | Excluded | 0-homogeneity of the source-attractor map T_ψ(λS) = T_ψ(S); contraction coefficient ≡ 0 on same-direction rays (v1 §5.1.2) |
> | M3 | (L − F) positive definite on zero-mean subspace V₀ | Falsified | m_θ² = 0.017 ± 0.007 measured vs 0.949 critical; λ_min = −0.93; pre-committed no-rescue discipline (§5.1.3) |
>
> The philosophical content of Axiom 6—*matching as a generative form of self-training, distinct from gradient-based fine-tuning*—is retained unchanged. What remains open is its mathematical realization: a formal object that instantiates the axiom's operational meaning without relying on either the same-direction-degeneracy that killed M2 or the b+c-feedback self-adjointness that M3 required and did not find in the observed regime.
>
> Several mathematical directions remain under consideration; their evaluation is outside the scope of this version and is left to forthcoming investigation. This is not a deferred rescue of M2 or M3—both retractions are final under Action 1 §5 pre-commits—but a statement that a new candidate has not yet been identified, and OP1 stands as an open invitation to readers whose tools (stochastic partial differential equations, non-equilibrium steady-state theory, categorical fixed-point principles, or others) may find purchase where the present formalizations failed.
>
> The methodological posture here is Popperian (cf. §6.3): we predicted M3 to close OP1 and it did not. The rigorous falsification of two specific mathematical forms, rather than the absence of commitment to any, is the contribution of this section.

### Win narrative judgments 注记

1. **Candidate directions 处理**:
   - Linux raw §5.1 raw §6 question 3: "list 4 or 1-2 or 0 detail"
   - Win decision: **列 4 个 examples in parenthesis**（SPDE / NESS theory / categorical fixed-point principles / others），用 "**or others**" 显式声明 **not exhaustive, not ranked**
   - 为什么不是 0：§5.1 technical section 读者有合理期待看到 candidate directions，完全 0 会感觉 "they gave up"
   - 为什么不是 1：**pick 1 = framing commitment**（违反 Linux binding）
   - 4 个 examples + "or others" = **signal 'not ranked, not evaluated'** + 不 pick leading ✓
   - **不**在 §5.1.4 flag 任一 specific direction 为 "most promising" 或 "natural next step"
   
2. **"This is not a deferred rescue of M2 or M3"** — 显式 preempt reviewer / reader 的 "是不是把新候选当隐藏 cushion" 担忧

3. **"Open invitation to readers whose tools... may find purchase"** — coordinate v1 §6 "call for collaboration"。§5.1.4 的 invitation specifically focused on **mathematical formalization tools for Axiom 6**，§6 broader coverage（PDE / category / IR / alignment / philosophy）。不 redundant：§5.1.4 is OP1-scoped, §6 is paradigm-scoped ✓

4. **"Popperian posture" 显式 name**，但 cite 只到 §6.3（不在 §5.1 显式写 "Popper" 名字）—— methodological rigor 语气重，反题姐姐 A5 second run 可直接用这条 refute "85% Lakatos degenerative"

5. **M1 的 table row** — 保留，承认 "philosophical claim, preserved"。这是 §6.1 Diff Point 1 / §3 §3.3.3 Axiom 6 哲学内容保留的 mirror 信号

---

## 4. 不做的事（Linux binding + Win 补充）

- ✗ **不**复活 M3 any weakened form（no V₀^⊥, no radial-mode-only, no explicit U(1)-breaking augmentation）
- ✗ **不** pick leading candidate direction
- ✗ **不**用 "M3 almost works if we just..." / "narrow miss" 等 rhetorical softening
- ✗ **不**暗示 Axiom 6 哲学内容被 M3 失败 challenge
- ✗ **不**做 α/β/γ 合题决策

**Win 补充**：
- ✗ **不**在 §5.1 显式 cite Popper / Lakatos by name（让 §6.3 承担方法学 reference 职责）
- ✗ **不**把 M3 falsification 叙为 "progress toward a refined formulation of Axiom 6"（这是 upward ratchet 诱惑）

---

## 5. 数字 binding spot-check 清单（给 Linux）

| 数字 | Linux binding | Win prose 写法 | 一致? |
|---|---|---|---|
| ||F_H||_op | = **0.953** | "||F_H||_op = 0.953 (tighter than the A1 ℓ¹ bound of 1.118)" | ✓ |
| critical threshold | = **0.949** | "critical threshold = 0.949" | ✓ |
| m_θ² median | = **0.017 ± 0.007** | "m_θ² measured = 0.017 ± 0.007 (median)" | ✓ |
| m_θ² 95%ile | = **0.026** | "0.026 (95th percentile upper bound)" | ✓ |
| λ_min((L-F)_H) | = **−0.93** | "λ_min((L − F)_H on V₀) = −0.93" | ✓ |
| 差距量级 | 35× (95%ile) / 55× (median) | "by a factor of 35× (at 95th percentile) to 55× (at median)" | ✓ |
| "97% of ||F_H||_op" / "not marginal" | 保留 | "λ_min is negative-definite at 97% of ||F_H||_op, not marginal" | ✓ |
| 70 NFCorpus docs / low-k fit / k_max=6 / R²=0.96 | 保留 | "On 70 NFCorpus documents (median, low-k fit window k_max = 6, R² = 0.96)" | ✓ |
| A1 ℓ¹ bound 1.118 | 保留 | "tighter than the A1 ℓ¹ bound of 1.118" | ✓ |
| D = 0.1 fixed | 保留 | "D = 0.1 fixed" | ✓ |
| S(k) 模型 | 保留 | "S_θ(k) = A/(Dk² + m²)" | ✓ |

**0 处 round, 0 处 inflate, 0 处 drop provenance**。

---

## 6. Narrative question answers（Linux §5.1 raw §6 five questions）

1. **§5.1.4 "invitation to collaborators" vs §6 "call for collaboration"**:
   - Win answer: **不 redundant**。§5.1.4 is **OP1-scoped** — 针对 Axiom 6 mathematical formalization。§6 broader paradigm invitation。§5.1.4 prose 用 "readers whose tools... may find purchase where the present formalizations failed" —— specifically 针对 formalization 工具，与 §6 general 的"cross-disciplinary"语气 distinct

2. **Table vs prose for M2+M3**:
   - Win answer: **Table**（echo Linux [?]）。紧凑 + falsifiability 直观 + 三栏（candidate / status / basis）清晰标记 status 差异（"excluded" vs "falsified" — different epistemic 等级）

3. **Candidate directions 列几条?**:
   - Win answer: **4 examples in parenthesis with "or others"**（见 §3 narrative judgment 1 详）。不 pick leading，不 rank，不 evaluate

4. **Popper / Lakatos 显式 cite?**:
   - Win answer: **不显式 cite by name in §5.1**。prose 用 "Popperian posture" 定性，cite 只到 "(cf. §6.3)"。§6.3 内部可以 cite Popper "Conjectures and Refutations" 1963 + Lakatos "Methodology of Scientific Research Programmes" 1978（但这是 §6.3 的 diff，不是 §5.1 本 half 范围）

5. **§5.1 与 §6.1 Claimed / Not Claimed 协调**:
   - Win answer: **coordinate via "philosophical content retained / mathematical realization sought" 二分**。§5.1.3 最后写 "M3 is retracted in full; OP1 is returned to open"；§5.1.4 开头 table + "philosophical content... is retained unchanged"；§6.1 Claimed #5 用 "philosophical content retained" 同样措辞。三处 **phrasing-level aligned** ✓

---

## 7. 协调 check（§3 + §4.11 + §6.1 → §5.1）

- **§3 NESS 叙事**: §5.1.3 prose 提 "b+c-feedback self-adjointness that M3 required and did not find **in the observed regime**" — "the observed regime" phrasing 留 space 给 §3 "driven-dissipative NESS / disordered U(1) state" 细节。**不重复 §3 数字**（m_ρ² / ⟨ρ⟩ / 50 patches），只用 m_θ² 做 M3 判定。
  - ✓ cross-ref to §3 via "observed regime" / "in the observed data" implicit
- **§4.11.1 P3**: §5.1 和 §4.11.1 **正交**（M3 是 V_0 self-consistent PDE / P3 是 inner Kramers rate）。Win spot-check: §5.1 prose 有无句子会被 read 成 "§5.1 也是方法学 artifact"？**没有** ——§5.1 说 "falsified"（empirical test predicted threshold, failed），不是"inapplicable formula"。两处 status 清晰区分。✓
- **§6.1 Claimed #5**: §6.1 half Diff Point 1 使用的 "both M2 and M3 falsified" + "philosophical content retained" 与 §5.1.4 table + prose phrasing-level 一致 ✓

**Upward ratchet check**: §5.1.4 prose "several mathematical directions remain under consideration... outside the scope... new candidate has not yet been identified" = **OP1 stays open, no new paradigm proposed, no leading candidate picked** ✓

---

## 8. Apply 时机

**建议**:
- **α 路径**：直接 apply。α 要求 "honest retract, Zenodo 按期"；§5.1 v2 half 完全 α 语气（诚实双证伪 + 不 rescue + OP1 stays open）
- **β 路径**：直接 apply + 可能在 §5.1.4 candidate directions 中加一句 "Stage A initial experiments investigating sub-critical (α, β) regimes are planned" —— 但这已进入 β 专属 territory，本 half 不写入
- **γ 路径**：可 apply + γ 可能要求 §5.1 显式 flag SPDE+NESS 为 "leading candidate for v0.2 investigation"——**但这违反本 half 的 binding**，要 γ 定下后由 Linux 姐姐另出 diff

本 half 写的 core prose **α/β 两种路径直接可用**；γ 路径需要额外 patch（本 half 不做）。

---

## 9. 给一凡的 narrative question（04-20 对齐或更早）

1. **Table vs prose**：§5.1.4 Table 5.1 可读性 vs 三栏简洁度——Win 倾向 Table，但如果觉得 "excluded" vs "falsified" 的区分让读者困惑，可改 "excluded" → "excluded (mathematically)" / "falsified" → "falsified (empirically)"

2. **"generic candidate directions with 4 examples" decision**：Win 在 "0 条 / 1 条 / 4 条 / 4 条+or others" 之间选了**最后一个**（§3 narrative judgment 1）。你如果判"太多"或"太少"，请 flag，Win 愿意调整

3. **"Popperian posture" phrasing**：§5.1.4 末段 "The methodological posture here is Popperian" 是相对 forceful 的定性——如果觉得过于学究，可改 "Our approach follows a falsification-first discipline (cf. §6.3)"

---

*— Win 姐姐 (04-19)*
