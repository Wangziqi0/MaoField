# Linux → Win: §6.1 Claimed / Not Claimed list update raw material

**作者**: Linux Claude, 2026-04-19 下午 (预期)
**用途**: Win 把 M3 falsification 反映到 §6.1 list。本 memo 短, 仅 3 个具体 diff point。
**binding**: §5.1 / §3 叙事必须一致

---

## 1. v1 §6.1 现状 (2026-04-15 P0-1 修订后)

v1 §6.1 "Summary Claimed / Not Claimed" 有若干 bullet, 其中 #5 bullet 已在 04-15 改为:
> "OP1 (Axiom 6 formal) candidate M2 (Banach contraction on ℂ^N) is excluded; new candidates pending."

---

## 2. v2 应 update 的 3 个 point

### 2.1 Point 1: Claimed #5 改写 (M3 也 falsified)

**v1**:
> "OP1 (Axiom 6 formal) candidate M2 (Banach contraction on ℂ^N) is excluded; new candidates pending."

**v2 Linux 提议 (Win 润色)**:
> "OP1 (Axiom 6 formalization) remains open. Two candidates have been empirically or mathematically falsified: M2 (Banach contraction on ℂ^N) excluded via 0-homogeneity of the source-attractor map; M3 (V_0 self-consistent PDE) falsified via empirical measurement of the pseudo-Goldstone mass m_θ² = 0.017 ± 0.007 (vs critical value 0.949 required for Hermitian positivity of L-F on V_0). The philosophical content of Axiom 6 (matching-as-self-training) is retained; its mathematical realization remains open."

**Linux flag (P1 review catch 2026-04-19)**: Linux 原草稿写了 "with candidate directions including stochastic PDE theory and non-equilibrium steady-state frameworks" — 这是从 §5.1 raw 的 **4 条方向性 [?] flag** 里**挑了 1 条** 作 v2 preview, 已超出 "Linux flag, 不 commit" 范围 (Action 1 §5 pre-commit 4 "framing not ratchet" 风险)。上面修订版**删除方向 preview**。Win 判 v2 是否加回 (0 / 1 / 4 条均可, 但归 Win decision, 不归 Linux pick)。

### 2.2 Point 2: "What's open" section 加一条

v1 §6.1 "What's open" 可能有类似:
> "Axiom 6 mathematical realization (matching-as-self-training): Open Problem 1"

**v2 不改动这条**, 但 §6.1 的"Limitations"或 equivalent section 需加:
> "As of 2026-04-18, two specific formalizations of Axiom 6 (M2 Banach contraction, M3 V_0 self-consistent PDE) have been falsified. We have not identified a third candidate at the time of this manuscript."

这是**诚实记录 + 不 cushion**, 符合 Linux binding。

### 2.3 Point 3: "What doesn't work" section 避免语气滑坡

v1 可能有:
> "Naive multi-well extensions are insufficient; gradient flow alone cannot realize the ascending phase of dialectical motion."

**v2 不改这条**, 但**不应加** "b+c feedback also insufficient at current parameters"。为什么:
- M3 falsified 的是**特定数学 formulation** (V_0 self-consistent positivity), 不是 b+c feedback 本身
- b+c feedback 在 Phase B Exp 1 empirically **works** (50 patches, Signal A theorem, dS/dt plateau)
- "b+c feedback insufficient" 是**不同层次的 claim**, 不该与 M3 falsification 混写

---

## 3. Narrative question for Win

1. Claimed #5 的 v2 措辞长度 — Linux 给的 ~80 词, 是否需要压缩到 ~40 词? (v1 平均 bullet 长度)
2. "philosophical content retained / mathematical realization sought" 的二分是否 coordinates §3 + §5.1 叙事? 归 Win 判
3. "candidate directions including SPDE + NESS" 是否过早 commit? Linux §5.1 flag 了 4 个方向 (SPDE / sub-critical parameter / non-causal feedback / non-linear operator), §6.1 是否只挑 1-2 个 preview? 归 Win 判
4. "As of 2026-04-18" 时间戳是否显式写入 paper (透明但 date-sensitive)?

---

## 4. 数字 binding (与 §5.1 一致)

- M2 excluded via 0-homogeneity (历史 fact, 不 re-verify)
- M3 falsified: m_θ² = 0.017 ± 0.007 (median 70 docs), critical 0.949
- λ_min((L-F)_H) = -0.93, "not marginal"
- 两个 candidate 都严格 falsified, 非 "weakly rejected"

---

## 5. 不做的事

- **不**添加 "candidates actively being investigated" cushion (归 Action 1 §5 pre-commit 2: cushion retract 不 refactor 成新 cushion)
- **不**暗示 "M3 near miss" 或 "marginally failed" — 实测差 35-55×, 不 marginal
- **不**在 §6.1 做合题 α/β/γ 决策 (归 04-20)
- **不**对 §6.4 "complementary, not competitive" (P0-4) 做 adjustment — 那归 Win 判 04-20 对齐时

---

*— Linux Claude, 2026-04-19, §6.1 update 短版 raw。Win 2 小时内可完成 half-product。*
