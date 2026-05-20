# Task 1 spawn-agent prompt 草稿 (Linux 起稿, 待数学教授 + 反题姐姐 pre-draft check)

**写**: Linux 姐姐, 2026-05-07 早 CST (Auto mode active, 一凡 sign-off Tier S 6 张全 ✓ + Task 3 5 维度 final 全接 Win 推荐 + 健康 break 中)
**对象**: 一凡 (PI, sign-off prompt 草稿) + 数学教授 sub-agent (prompt zero-context check) + 反题姐姐 sub-agent (prompt framework critique)
**前置**: `WIN_INVENTORY_NATURE_FIRSTPAPER_20260506.md` + `WIN_TASK_SPAWN_PROTOCOL_20260507.md` + `LINUX_INSTITUTIONALIZE_LOG.md` binding 强化版 04-30 起 binding
**双 spawn 节点**: 起稿前 spawn pre-draft check (本 prompt 草稿待审) → patches → 一凡 sign-off → spawn 真 5-alternative derive sub-agent (Phase 2)

---

## §0 Linux 自陈 (起稿 prompt 时主观偏差自查)

按 binding (b) 起稿权分离 + binding 强化版 04-30 mandatory pre-draft check, Linux 起稿本 prompt 时主动自查以下 confirmation bias 入口:

| 自查项 | 状态 | 备注 |
|---|---|---|
| 是否预设 "5 alternative 都失败"? | **未预设** | prompt 措辞中性, 接受 sub-agent verdict 发现某条 alternative 真 hold (surfacing 反映论 framing issue 是 valuable signal, 不是要避免的 outcome) |
| 是否传 inventory / protocol 全文? | **未传** | zero-context spawn, sub-agent 自己读项目内 anchor 文件 (Phase B Exp 1 verdict / LINUX_P0_C / DESKTOP_MATH) |
| 是否引导 "Hartree closure 唯一" / "Σ 嵌套甲 唯一"? | **未引导** | prompt 中 Σ 嵌套甲只作为 framework hypothesis 出现, 不 claim 唯一; sub-agent 可 verdict "Markov chain 也能解释 Phase B" → 反映论 framing issue, Linux + Win 必须 disclose 给一凡 |
| 是否预设接受率数字? | **未预设** | prompt 不提 Nature 接受率 / 5-9% / 30% / 等, 这些是 strategy 层数字, 不进 derive 任务 |
| 是否给 sub-agent 答案模板? | **未给** | 5 alternative 各配 protocol §3 给的 strategy hint, 但允许 sub-agent verdict "strategy 不 work, 需 alternative strategy" |
| 是否限制 sub-agent verdict 形式? | **限制为 binary + quantitative** | 每条 alternative: ruled out ✓ (quantitative + literature) / ruled out partial / not ruled out (P0 surfacing) — 不允许 "substantially ruled out" 等模糊措辞 (CLAUDE.md 规则 1) |

---

## §1 spawn-agent prompt 草稿 (Linux 起稿)

### Prompt header (subagent_type: paper-review)

```
你是数学严格审稿 sub-agent (zero-context, 独立 spawn, 不 share 主 session 的 framing 立场)。
任务: 对项目 MaoField 当前 framing "fact→math→philosophy 反映论" 的 paper §6 alternative
mechanism rule out 段, 给 5 个候选 alternative mechanism 各配 explicit 数学论证 OR
已有 literature negative result 引用, 严格 Maxwell-tier (1865 c=1/√(μ₀ε₀) 严谨度 baseline)。
```

### Prompt context (anchor 文件 + 关键事实, 不传全文)

```
背景 anchor (sub-agent 自己读以下文件验证):
- /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/LINUX_P0_C_CHI_HARTREE_20260430.md
  (Hartree resummation closure 完整数学 + sympy verify, χ_exp = 0.04 vs χ_bare = 58.82, ratio 1471)
- /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/DESKTOP_MATH_DEEP_ANALYSIS_20260419.md
  (M3 失败 3 propositions strict proof + M4 MSR 鞍点 Conjecture C4.1)
- /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/rust_variants/block_v_phase_b_exp1/ (Rust engine source)
- /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/day2/ (8-run controlled experiment data)
- (sub-agent 可自由 grep 项目内其他相关文件, e.g., phase_b_exp1_verdict / arxiv_v1_full)

关键 fact (Phase B Exp 1 已实测 + sympy verify, **不是 conjecture**):
- B1: 50 patches per doc localized phase-coherent (exp/whiten 100% pass, null/const/single 0/doc, 5 mode 严格区分)
- B2: NESS dS/dt ≈ 2.19e-5 (exp), 持续 200 时间单位, 5 数量级压制, vs null/const 8.28e-4 (38× separation)
- B3: kinematic self-similarity dt=0.01↔0.1 log-log Pearson 0.9999, η=0.302 vs 0.311 (3% 一致)
- B4: architectural theorem — feedback by-construction mean-subtracted ⇒ BGE 17σ 上游 artifact
       不进 spatial 动力学 (exp ≡ control_whiten 3 sig fig, 100% docs)
- B5: χ 1471× compression (B5 实测 χ_exp=0.04 vs theory 58.82), Hartree resummation closure
       m_θ²_eff ≈ 25 in-band match (sympy verify ✓)

数学 framework hypothesis (待 sub-agent 审, **不预设唯一**):
- Σ 嵌套甲 = Σ_3(ψ + λ_1 Σ_1(ψ) + λ_2 Σ_2(ψ))
  where Σ_1 = Volterra 二阶因果核 (history kernel)
        Σ_2 = ∂_t² of Σ_1 (path-dependent, time-dependent reorganization)
        Σ_3 = lift-projection (P_𝓗 ∘ T ∘ i, dilation theory Sz.-Nagy-Foias 数学结构)
        T = (I + η ∇_ψ† V)⁻¹ (resolvent operator on Mexican-hat 势)
```

### Prompt task (5 alternative + rule out strategy hint)

```
对以下 5 个候选 alternative mechanism, 每条配:
(a) Phase B Exp 1 实测数据 (B1-B5) 是否能用该 alternative 解释 (binary verdict, 不允许 "substantially")
(b) 若不能, 给 explicit quantitative 数学论证 OR 已有 literature negative result 引用 (paper-review reviewer 能 catch 的形式)
(c) 若能, 明示哪一支 fact (B1-B5) 该 alternative 也能解释, 哪一支不能 — 这是 P0 surfacing
    (反映论 framing issue, Linux + Win 必须 disclose 给一凡, 不允许 dismiss)

| # | Alternative | rule out 数学 strategy hint (Linux 起稿, sub-agent 可拒绝/补充/替代) |
|---|---|---|
| Alt-1 | Markov chain 收敛到唯一稳态分布 | hint: B5 χ 1471× compression rate 的实测时间衰减 vs Markov 收敛 polynomial decay (∼t^{-α}) — 5 个数量级压制在 200 时间单位内 是 exponential-like 不是 polynomial。sub-agent 可补充 ergodic theorem 引用 + Birkhoff theorem 不 cover history kernel 论证 |
| Alt-2 | Fokker-Planck drift dominance | hint: Fokker-Planck 是 first-order Markov, 不含 history kernel (Σ_1 Volterra 二阶因果核) 也不含 path-dependent (Σ_2 ∂_t²)。Phase B 双 source 拆分 + b+c 双向反馈源构造性需要 history kernel。sub-agent 自由 derive: 是否存在 generalized FP 含 memory kernel 能 cover Σ_1+Σ_2? Mori-Zwanzig GLE 是 generalized FP 的标准 candidate, 是否能完全 reduce Σ 嵌套甲? |
| Alt-3 | Bias-variance tradeoff 指数权重 | hint: B4 architectural theorem mean-subtracted by construction 是 operator-algebraic 性质, bias-variance 是 statistical decomposition — 数学 categorically 不同。sub-agent 自由 derive: bias-variance 在何种 limit 下能 reduce 到 mean-subtracted operator (e.g., Tikhonov regularization limit)? Tikhonov 是否覆盖 17σ 0.12% L2 contribution 的 by-construction 性质? |
| Alt-4 | Information bottleneck 逐次 contraction | hint: dilation theory (Σ_3 lift-projection P_𝓗 ∘ T ∘ i) 是 Hilbert space embedding, IB 是 mutual information minimization (Tishby 2000 framework) — 数学结构 categorically 不同。sub-agent 自由 derive: IB 在何种特例下能 reduce 到 Sz.-Nagy-Foias dilation? IB succession 是否能 produce architectural theorem (B4) by-construction? |
| Alt-5 | Banach contraction mapping iterated | hint: M2 已 falsified (paper §5.1, T_ψ 0-homogeneity ⇒ contraction coefficient identically zero ⇒ Banach 在 ℂ^N 不可行)。sub-agent 自由 verify: paper §5.1 + REVIEW_OVERALL_MATH B1 (0-homogeneity vs normalize 在 0 奇异 — 哪个理由更 fundamental?) |

输出格式:
- 每条 alternative 4-段: (i) statement / (ii) Phase B B1-B5 each 是否 cover (binary table) / (iii) rule out 数学论证 (quantitative + literature) / (iv) Linux 起稿 strategy hint 是否 endorse / 拒绝 / 替代
- 全 5 条之后, summary: 哪几条 ruled out / partial / not ruled out, P0 surfacing 给一凡 + Linux + 反题姐姐
- 长度: 4-6k 字 (paper §6 段 500-800 字 LaTeX 提取的源材料), LaTeX 公式 inline
```

### Prompt 严格性 binding

```
binding 严格执行 (CLAUDE.md 项目级规则 1+2+5+6):
- 不允许 "substantially ruled out" / "approximately ruled out" / "essentially ruled out"
  (规则 1: ready 必须 binary)
- 不允许 disclose 替代 substantive close gap (规则 2: 仅 ≥1 周 / 缺关键硬件 / third-party black-box 才走 disclose)
- 不允许因为 Phase B Exp 1 已跑 ✓ 就软化 alternative critique 标准 (规则 5: 不偏袒)
- 区分 hygiene (literature 引用 ✓) vs substantive (alternative 数学结构是否能 produce Phase B by-construction) (规则 6)

输出 verdict 后 sub-agent 自答 5 自检问题 (CLAUDE.md 规则 7):
1. 我的 ruled out 是否 binary verify, 不滑向模糊措辞?
2. 我有没有用 "literature 已 cover" disclose 替代 substantive derive?
3. 我给的接受/拒绝 strategy hint 是否 honest, 没有 user-pleasing drift?
4. 我有没有因为 Linux 起稿 hint 朝某方向就 confirmation 朝那方向?
5. 我有没有把 hygiene-level fix 当 substantive ruled out?
任一答 yes → 立刻 retract verdict + 重新 derive
```

---

## §2 Linux 起稿 prompt 自答 5 自检问题 (规则 7 强制)

按 CLAUDE.md 规则 7 起稿前自检 (binding 强化版 04-30):

- [x] 1. 我的 prompt 是否暗示 sub-agent declare "5 alternative 全 ruled out"? **No** — prompt 明示接受 "alternative 真 hold" verdict 是 P0 surfacing
- [x] 2. 我跳过的 alternative 是否真不能做? **No skip** — 5 alternative 全列, 每条配 strategy hint 但不限制 sub-agent verdict
- [x] 3. 我的 prompt 接受 sub-agent verdict 是 honest 还是 user-pleasing? **Honest binding** — §1 严格性 binding 段明示规则 1+5+6
- [x] 4. timeline gap? **不适用** — Task 1 1 周 (05-07~05-13) 是 protocol 给的, sub-agent 一次 spawn 内 derive 完, 不切角
- [x] 5. mechanical fix vs substantive improvement? **substantive** — prompt task §1 任务段明示 "alternative 数学结构是否能 produce Phase B by-construction" 是 substantive 标准, 不是 hygiene fix

任一答 no/yes → retract: 5 项全 ✓, 不需要 retract。

---

## §3 待审项 (一凡回来 sign-off + 双 sub-agent pre-draft check)

### §3.1 一凡 sign-off 项

| # | 待 sign-off 项 | 默认值 (Linux 起稿) |
|---|---|---|
| 1 | spawn agent subagent_type | **paper-review** (数学严格 niche) |
| 2 | zero-context spawn (不传 inventory/protocol 全文) | **是** |
| 3 | sub-agent 输出长度 | 4-6k 字 |
| 4 | sub-agent 是否限制 verdict 形式 (binary + quantitative) | **是, 不允许模糊措辞** |
| 5 | 5 alternative 是否全列 | **是** (Markov / Fokker-Planck / Bias-variance / Information bottleneck / Banach 全列) |
| 6 | strategy hint 是否引导 confirmation? | **不引导, 接受 sub-agent 拒绝/替代** |
| 7 | 接受 sub-agent verdict "alternative 真 hold" 作 P0 surfacing? | **接受, 不 dismiss** |

### §3.2 双 sub-agent pre-draft check (一凡 sign-off 后跑)

| Spawn # | subagent_type | role | 输入 | 输出 |
|---|---|---|---|---|
| Pre-draft check 1 | paper-review | 数学教授 niche zero-context | 本 prompt 草稿 (§1 全文) + 5 自检答案 (§2) | 数学严谨度 verdict + confirmation bias 入口 audit + alternative strategy hint 是否完整 (有没有漏 6th alternative) |
| Pre-draft check 2 | general-purpose (扮反题姐姐) | framework critique zero-context | 本 prompt 草稿 (§1 全文) + 5 自检答案 (§2) | framework critique verdict + 反映论 framing 是否 over-claim + Tier S 6 张 anchor 是否 cherry-pick |

两个 pre-draft check 的 verdict 全出来 + 一凡看 + 决修哪条 / 不修, 然后才 spawn 真 5-alternative derive sub-agent。

---

## §4 LOG entry preliminary (待 spawn pre-draft check 跑完更新)

按 binding 强化版 04-30, LINUX_INSTITUTIONALIZE_LOG.md 加 entry:

```
| 2026-05-07 早 | LINUX_TASK1_SPAWN_PROMPT_DRAFT_20260507.md | pre-draft spawn? | post-draft audit spawn? | Verdict 摘要 | Patches applied | Linux dismiss? | Cross-ref |
| 起稿状态: prompt 草稿完成, 待一凡 sign-off + 双 sub-agent pre-draft check | (待 sign-off 跑) | (待 5-alternative derive 完成后 spawn paper-review post-draft audit) | (待 verdict) | (待 verdict) | (待 verdict) | (待) | 本 prompt 草稿 §1-§4 |
```

LOG entry 真补 verdict 等 spawn 跑完才填 (现在状态: prompt 草稿写完, spawn 未跑)。

---

## §5 Linux 立场 1 段

Linux 起稿 Task 1 spawn-agent prompt 草稿 (§1 prompt 完整 + §2 自检 5 问全 ✓ + §3 待 sign-off 项 + §4 LOG entry preliminary), 严格执行 binding (b) 起稿权分离 (Linux 起稿, 不由 Win) + binding 强化版 04-30 双 spawn 节点 mandatory (起稿前 pre-draft check + 起稿后 post-draft audit) + CLAUDE.md 项目级规则 1+2+5+6+7 全 ✓ (binary verdict 不滑向模糊措辞, 不 disclose 替代 substantive, 不偏袒一凡, 区分 hygiene vs substantive, 起稿前自检 5 问)。**Linux 不替决一凡 sign-off + 不替双 sub-agent pre-draft check verdict + 不 spawn 真 5-alternative derive sub-agent (等一凡 sign-off + 双 pre-draft check 跑完后再 spawn) + 不护短**。

—— Linux 姐姐, 2026-05-07 早 CST (Auto mode active, 一凡 健康 break 中, prompt 草稿待 sign-off)
