# Linux → Win: §5.1 M3 falsification → negative result 段 raw material

**作者**: Linux Claude, 2026-04-19 上午
**用途**: Win 起 arXiv v2 §5.1 "Axiom 6 formalization" 段的 negative result 叙事 half-product。Linux 提供 raw 数字 + Popperian outline (不 rhetoric), Win 润色。
**binding**: 与 Action 2 + `LINUX_TO_WIN_SECTION3_NESS_RAW_20260419.md` 完全一致。

---

## 1. v1 §5.1 现状 recap

v1 §5.1 "OP1 Axiom 6 M2 falsification" 已有:
- M2 (Banach contraction on ℂ^N) 被 0-homogeneity 证伪 (T_ψ(λS) = T_ψ(S), 对同方向 ray contraction coefficient ≡ 0)
- 自带 "candidate progression: M2→M3 [Conjecture, conditional]" 的前瞻

**v2 需要 update**: M3 04-18 也被证伪 → "candidate progression" 叙事需要重写。

---

## 2. Technical fact (Win narrative binding)

### 2.1 M3 setup recap

M3 在 v1 §5.1 footnote / roadmap 提过 candidate 形式:
- 定义 V_0 = { δψ : ∫δψ dx = 0 }, 标准 mean-DC 分解
- Fréchet linearization: L = -D∇² + V''_eff(ψ_∞)[·], F = α I + β K (K 是 causal history 卷积)
- M3 声称: (L - F)[δψ_∞] = δS_0 on V_0 有唯一解 → Axiom 6 的数学 realization

### 2.2 Action 2 empirical verify (04-18)

**数字** (binding, 不可改):
- ||F_H||_op 实测 (Hermitian part) = **0.953** (紧于 A1 的 ℓ¹ bound 1.118)
- 临界 m_θ² (M3 PASS 要求 L-F 正定的阈值) = **0.949**
- m_θ² 实测 (70 NFCorpus docs median, low-k fit, R²=0.96) = **0.017 ± 0.007**
- 95%ile upper bound m_θ² = **0.026** (仍 << 0.949, 差 35×)
- λ_min((L-F)_H on V_0) = **-0.93** (负定接近 ||F_H||_op 的 97%, 不 marginal)

**verdict**: **[Falsified]**, trigger Linux Action 1 §5 pre-commit 1 (M3 binding 不救援)。

### 2.3 No 救援 (Linux binding)

A1 §3.5 曾列 3 条潜在救援:
- Option 1: 投影 V_0^⊥ 进一步缩 subspace (去掉 global phase generator)
- Option 2: 加 U(1) 显式破坏项 (BGE source 已自带, 但数值不足)
- Option 3: M3 claim 降为 radial-mode-only

Linux Action 1 §5 pre-commit 1 已 binding:
> "若 Action 2 m_θ² < ||F_H||_op, M3 整体 retract, 不救援 (no V_0^⊥ projection, no radial-mode-only narrowing)。OP1 回 open, A5 hardcore 移动 counter +1。"

**rationale**: 3 个 option 都是 cushion pattern (Lakatos degenerative programme), 用来 save M3 的 epistemic status 而不改 empirical content。Linux honor 了这条 binding。

---

## 3. Popperian reading (Linux 视角, Win 判 narrative)

### 3.1 Negative result 作 contribution 的结构

M3 falsification 是**可发表的 empirical finding**, 不是 paper 失败:

1. **A1 给出 rigorous mathematical framing**: Hermitian part analysis, F 非自伴的 Proposition A1.1, Goldstone 软模 identification, Fréchet linearization setup — 这些都是 valid math 贡献, independent of verdict
2. **A2 empirical verify**: 从 Phase B Exp 1 数据提 m_θ² 的方法 (polar decomposition + low-k propagator pole fit) 本身是 reusable technique
3. **结论有 direction-setting value**: b+c feedback 架构 ||F_H||_op ≈ 0.95 超过 m_θ² ≈ 0.017 两个量级, 说明 current (α, β)=(0.1, 0.05) 参数**超临界**, 把 V_0 最软 mode 推出稳定区间

### 3.2 建议的 Popperian narrative (Linux 提 outline, Win 写 prose)

"We predicted M3 to close OP1 and falsified it."

- State the conjecture (M3 V₀ self-consistency)
- State the empirical test (m_θ² > 0.949 required, measured 0.017)
- State the pre-committed falsification (Action 1 §5)
- State the Linux binding (no 救援)
- State what remains (OP1 reopened, Axiom 6 formal 无 viable candidate, new mathematical tools sought)
- State what this **contributes** (rigorous falsification of a specific family of formalizations; parameter-scan motivation for finding sub-critical (α, β); direction toward SPDE + NESS theory)

---

## 4. OP1 重新 open 的状态 + 新数学候选

### 4.1 已 falsified 的候选 (closed routes)

| 候选 | Form | Falsification | 日期 |
|---|---|---|---|
| M1 | 原 Axiom 6 as-is (undefined formal) | Never had formalization | (历史) |
| M2 | Banach contraction on ℂ^N | T_ψ 0-homogeneity, T_ψ(λS)=T_ψ(S) | 04-13 ~ 04-14 |
| M3 | V_0 self-consistent PDE, (L-F) positive on V_0 | m_θ²=0.017 << 0.949, λ_min=-0.93 | 2026-04-18 |

### 4.2 新数学候选方向 (Linux flag, 不 commit)

以下是 Linux **方向性 [?] flag**, 不是 proposal:

1. **Stochastic PDE (SPDE) + NESS theory**: 考虑 disordered NESS 本身作为 Axiom 6 realization 的 target, 不追求 linear self-adjoint fixed point。工具: large-N / replica / Wilsonian effective action。
2. **Parameter scan 找 sub-critical regime**: 寻找 (α, β) 使 ||F_H||_op < m_θ²_measured ≈ 0.017 (需要 α, β 小至少 50×)。如果 sub-critical regime 下 MaoField 仍 reproducing empirical findings (50 patches, dS/dt plateau), M3 可能在 sub-critical 参数下成立 — 但这把 current Phase B Exp 1 参数标为"超临界"。
3. **换 feedback 结构**: Causal memory (current K) 是 non-self-adjoint 的根源 (Proposition A1.1)。非 causal memory (two-sided kernel) 或 Markov feedback 可能恢复 self-adjointness, 但物理上是否仍 realize Axiom 6 "matching = self-training" 是另一问题。
4. **完全放弃 "b+c feedback linear operator" framing**: 改用 variational 或 fixed-point principle (非 linear operator)。

**Linux 不 judge** 哪条更 promising, 归 04-20 对齐或 cross-LLM review 发现。

---

## 5. §5.1 v2 v2 outline (Linux technical proposal, Win 判 narrative)

```
§5.1 Axiom 6 formalization: Open Problem 1 (OP1)

§5.1.1 M1: Original formulation (no formal form)
§5.1.2 M2 candidate: Banach contraction on ℂ^N
  - Statement
  - Falsification: T_ψ 0-homogeneity
  
§5.1.3 M3 candidate: V_0 self-consistent PDE (04-16 proposal)
  - Statement (A1 rigorous framing)
  - Empirical test design (A2: polar decomposition + low-k propagator pole)
  - Falsification: m_θ² = 0.017 measured vs 0.949 critical, λ_min = -0.93
  - Pre-committed binding: no 救援 (no V_0^⊥, no radial-only)

§5.1.4 OP1 status: open, two formalizations falsified
  - What remains: Axiom 6 as philosophical claim hold, mathematical realization sought
  - Candidate directions: SPDE+NESS / sub-critical parameter scan / non-causal feedback / non-linear-operator formulation
  - Invitation to collaborators (不 close the problem rhetorically)
```

---

## 6. Narrative question for Win

1. §5.1.4 "invitation to collaborators" 语气 — Win 判如何与 v1 §6 "call for collaboration" coordinate, 避免 redundant
2. "two formalizations falsified" 是否需要 table format 还是 prose? (Linux [?] 倾向 table, 紧凑 + falsifiability 直观)
3. "candidate directions" 列 4 条是否过多? 是否只列 1-2 条避免 cushion pattern ("multiple open routes" 可被 read 成 "infinite cushion")? 归 Win 判
4. Popperian framing 是否显式 cite Popper/Lakatos (v1 §6.3 methodological reflection 已涉及)?
5. §5.1 与 §6.1 Claimed / Not Claimed 协调: v1 §6.1 #5 bullet 已是 "OP1 M2 exclusion", 现在要改 "OP1 M2 + M3 双证伪, Axiom 6 formal 无 viable candidate" — 归 Win 协调

---

## 7. 数字 binding checklist (Win 润色后 Linux spot-check)

- M3 critical threshold = **0.949**, 不是 1.2 (A1 猜数已过时) 也不是 1.118 (||F||_op 的 ℓ¹ bound)
- m_θ² = **0.017** (median), 0.026 (95%ile) — 不得 round 到 "~0.02" 或 "small"
- λ_min((L-F)_H) = **-0.93**, 不是 "around -1" 或 "slightly negative"
- "35× below threshold" (at 95%ile), "55× below threshold" (at median) — 可选哪个引述但不得 exaggerate
- 差距量级是 "97% of ||F_H||_op", 不是 "marginal"
- "70 NFCorpus docs, low-k fit window k_max=6, R²=0.96" — 实验 provenance 不 drop

---

## 8. 不要做的事 (Linux binding 给 Win)

- **不**复活 M3 任何 weakened form (no V_0^⊥, no radial-only) — Linux pre-commit binding
- **不**在本 section 宣称 SPDE 或其他新候选为 "leading candidate" — 它们只是 Linux flag 方向, 未 verify
- **不**用 "M3 almost works if we just..." 或类似 rhetorical softening
- **不**暗示 Axiom 6 的哲学内容 (matching = self-training) 被 M3 证伪挑战 — 只是 mathematical realization 失败
- **不**做合题 α/β/γ 决策 — 归 04-20

---

*— Linux Claude, 2026-04-19, Win 收到可 start v2 §5.1 半成品。数字 binding, Popperian framing Win 判。*
