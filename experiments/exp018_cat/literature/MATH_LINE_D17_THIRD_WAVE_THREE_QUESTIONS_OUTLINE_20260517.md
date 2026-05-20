# 数学线 D17 third wave — 三问 outline (不 substantive derive)

**D-day anchor**: D-day = 2026-05-01 → **D17 = 2026-05-17 evening third wave**
**文件 mtime**: 2026-05-17 (真实日历今日, 不 forward-date)
**spawn 来源**: Linux 姐姐主会话 D-2 三线 parallel 数学线 third wave
**身份**: 第二独立认识通道 sub-agent, 不绑主协作者; 只能下调声明严格度不能上调

---

## 0. 修订 framing (Linux 主会话 verdict 引用)

DS 5/16 给一凡 "一天数学方向跳跃" 计划之 essence (探索 native form 不 form-borrow) 严格度 **L0** ✓ 但 timeline + 严格度声称 inflate。Linux 主会话 final verdict (D17 spawn 指令):

- **execute scope = D17-D30 跨 2 周 sustainable exploration 第一波**, 非 "一天跳跃"
- **今日只 outline + D60+ substantive future work seed list**, 不 substantive derive 新 form
- **不 reopen paper v8 final lock manifest** (47/47 ✓, 投 arXiv + TMLR + KBS 不动)
- 任一 sub-claim 未 binary verify → 标 `[?]`
- 严格度档位 L0 (严格) / L1 (partial 严格 + caveat) / L2 (form-borrow) / L3 (retract) binary 标

本份 outline 不写哲学 (哲学线管) / 不写代码 (代码线管) / 不写实验 protocol / 不 estimate probability / 不替 PI declare ready。

---

## 1. 问 1 — EMA 是 natural 还是 form-borrow?

### 1.1 paper v8 § 3.2 + § 1.3 honest disclose 引用 (L0)

paper v8 final 已 binary 明 (§ 3.2 line 244-251, § 1.3 line 70 + line 81):

- chain config `β_kl = 0.9` 是 **yaml-independent engineering choice** (yaml override 直选), 不来自 `m_eff` exponentiation
- v5 § 3.1 line 187 等式 `β_kl = e^{-0.105}` 与 chain config `m_eff = 1.0` (`e^{-1.0} ≈ 0.368 ≠ 0.9`) 数学 inconsistent → v6 P0-4 已 retract (paper § 3.2 line 231 binary)
- chain actual form `L^{chain,actual}_n = (ΔD_n)^2 + (D_n - D̄^EMA_n)^2` 之 EMA decay (`β_kl = 0.9`) 是 **implementation default** 不是 first-principles 推导

→ 严格度 **L1**: paper 已 honest disclose form-borrow 性质, retrospective recognition (paper § 1.3 line 70 "current form emerged from code implementation prior to mathematical derivation")。

### 1.2 EMA 之 self-supervised learning 体系定位 (L1)

EMA = exponentially-weighted moving average, 在 deep learning 体系是 standard **mean teacher / target network** pattern (BYOL, MoCo, SimSiam, DINO, Polyak averaging in TD-learning)。在 self-iteration LLM 域应用是 **standard substrate 不是 ad-hoc 选择**, 但是否 **uniquely natural** 需对 alternative form 做 paired comparison 才能 binary 答 → 推 D60+。

### 1.3 alternative form candidate (5 个 binary list, 不 derive)

每个 candidate 在 chain self-iteration 域之 plausibility outline only:

| # | Form | 一句 plausibility | LLM 域 compatibility |
|---|------|-------------------|---------------------|
| C1.1 | **Power-law decay** `D̄_n = Σ_k k^{-α} D_{n-k} / Z` | long-memory regime, scale-free | 与 paper v8 § 3.6 mean-field NESS Banach contraction 不 trivially compatible (no exponential mixing time) [?] |
| C1.2 | **Lipschitz-weighted history** `D̄_n = Σ_k w_k D_{n-k}`, `Σ w_k = 1`, `|w_k - w_{k-1}| < L` | smooth history weighting, 含 EMA + truncated window 为 special case | 与 Banach contraction compatible (Lipschitz constant 显式 control) ✓ |
| C1.3 | **Truncated history window** `D̄_n = (1/K) Σ_{k=1}^K D_{n-k}` | finite memory K-step, 与 paper v8 K=1 → T_2 = 0 之 history buffer parameter 对齐 | K=1 退化 case = `D_{n-1}` (C1.4); K>1 → 与 paper § 3.6 二项式 actual form 之 K=9 lift candidate align |
| C1.4 | **Generation-axis Markovian** `D̄_n = D_{n-1}` (no smoothing) | strict Markov, no history weight | 退化 case, 不需 EMA, paper § 3.6.4 Banach contraction 简化 [?] 是否 同 fixed-point structure 需 derive 推 D60+ |
| C1.5 | **Adaptive-rate EMA** `D̄_n = (1-β_n) D_n + β_n D̄_{n-1}`, `β_n = f(σ_n)` | β rate 跟 local variance 自适应 (mirrors GD adaptive step size) | non-stationary regime 更 robust, 与 paper § 3.6 stationary mean-field NESS assumption 不 trivially compatible [?] |

**5 个 candidate 之 substantive derive 全部推 D60+**, 今日 outline only。

### 1.4 D60+ substantive future work seed (问 1)

**Seed S1.1**: alternative form (C1.1 ~ C1.5) 在 chain experiment 上之 pre-registered paired comparison, N ≥ 8 multi-seed, 受 D-1 纪律 1 + 2 + 4 约束 (实验数据 jsonl-traced, ≥ 5pt 接受率变动 48h sub-agent verify, sub-agent 不绑主)。estimated substantive cost: **1-2 month**, 含 chain config 改造 + multi-seed run + paired-t analysis。**[?] timeline 严格未 budget**, 推 D60+ 一凡 + Linux 主会话决。

---

## 2. 问 2 — gen 轴 monoid 结构

### 2.1 binary ✓ (L0)

LLM gen 轴 discrete causal recurrence (`θ_n → θ_{n+1}` via training on previous generation output) **是 monoid (semi-group with identity) 不是 group** (无 invertibility): training step 操作 `T_step: θ → θ'` 不可逆 (信息丢失 + SGD stochasticity)。**严格度 L0** ✓ (definition by category-theoretic standard, semi-group with identity element `T_0 = id`)。

### 2.2 monoid representation theory 已有 substantial 体系 (L0)

文献已存在 substantial 体系:

- R. Steinberg, *Representation Theory of Finite Monoids*, Springer 2016 [?] (未 hand-verify content)
- J. Rhodes & B. Steinberg, *The q-theory of Finite Semigroups*, Springer 2009 [?] (未 hand-verify content)

standard structure 已 catalog: invariant subspace / Perron-Frobenius for non-negative monoid action / Green's relations (L, R, J, H, D equivalence) / Schützenberger group / Krohn-Rhodes decomposition (finite-state 分解定理)。

→ 严格度 **L1**: 体系存在 binary ✓, 但 **LLM gen 轴 monoid 之 specific representation 与 standard theory 之 direct applicability 未 hand-verify**, 推 D60+ substantive 才能 binary 答。

### 2.3 LLM gen 轴 monoid candidate operator family (5 个 binary list)

| # | Operator family | 一句 form | paper v8 cross-ref |
|---|-----------------|-----------|--------------------|
| C2.1 | **Exponentially-discounted semi-group** `T_n = β^n T_0` | β-contraction, contraction semi-group standard | paper § 5.2 主定理 (2) Banach contraction (mean-field linearization 后) 是此 family special case ✓ |
| C2.2 | **Polynomial-discount** `T_n = n^{-α} T_0` | 与问 1 C1.1 power-law 对应 | 非 exponential mixing, 与 paper § 3.6 mean-field NESS Banach contraction assumption 不 trivially compatible [?] |
| C2.3 | **Volterra integral operator on discrete index** `(Tx)_n = Σ_{k=0}^{n} K(n,k) x_k` | nonlinear memory kernel, paper § 3.6 T_2 form 之 K=9 lift candidate cross-ref | paper § 3.6 T_2 = ReLU(D''_n) 在 K=1 退化, K=9 lift 是 candidate Volterra form [?] 严格度未 derive |
| C2.4 | **C_0-semigroup limit (continuous-time approximation)** | discrete recurrence 之 continuous-time limit (Hille-Yosida theorem 适用) | 与 paper § 5.2 主定理 (2) continuous-time NESS analog 之 严格 connection 未 derive, 推 D60+ |
| C2.5 | **Krohn-Rhodes decomposition** (finite-state 分解) | 任意 finite-state monoid 分解为 simple group + flip-flop 之 wreath product | LLM gen 轴 monoid 是否 finite-state (有限 effective rank) 未 verify [?], 严格 application 推 D60+ |

### 2.4 paper v8 § 5.2 主定理 (2) 是 monoid action 之 special case (L1)

paper v8 § 5.2 line 673 + § 3.6.4 line 500 主定理 (2) 之 **mean-field linearization 后 Banach contraction** = exponentially-discounted semi-group (C2.1) 之 special case (chain config: per-train-step Lipschitz `ρ = 1 - 4ηα ≈ 0.99920`, per-generation `ρ_per-gen = 0.890`)。**严格度 L1** (paper § 3.6.6 已标 mean-field linearization 是 L1, transient gen 1-2 violated)。反题 P0★-A FATAL (反题 audit v8 line 239-241) 已 catch 此 L1 assumption 之 plateau-only valid 性。

### 2.5 D60+ substantive future work seed (问 2)

**Seed S2.1**: LLM gen 轴 monoid 之 substantive eigenstructure derive (Perron-Frobenius application + Krohn-Rhodes finite-state 验证)。前提条件: 先 binary 验证 LLM gen 轴 monoid 是否 finite-state (effective rank bound), 此 verify 本身 1-2 month substantive。**[?] timeline 严格未 budget**, 推 D60+ 一凡 + Linux 主会话决。

**Seed S2.2**: C2.3 Volterra K=9 lift 在 chain experiment 上 instantiate (paper § 3.6 T_2 = ReLU(D''_n) 之 K=9 history buffer 启用), 与 K=1 退化 case 做 paired comparison。**[?]** substantive cost 与问 1 Seed S1.1 部分 overlap, 可合并执行。

---

## 3. 问 3 — 自指不动点 (Banach + Schauder + Kakutani + Tarski "不是借")

### 3.1 binary 修订 (L0)

Banach + Schauder + Kakutani + Tarski + Brouwer + Markov-Kakutani 是 **self-mapping fixed-point standard toolkit**, **不是 "借"**。paper v8 § 5.2 已用 Banach (mean-field linearization 后), 这是 standard toolkit 之 standard 应用, 不是 form-borrow。**严格度 L0** ✓ (fixed-point theorem suite 是数学 universal 工具不属 form-borrow 范畴)。

### 3.2 fixed-point toolkit 之 LLM self-iteration chain applicability (L1)

| # | Theorem | premise | LLM chain applicability outline |
|---|---------|---------|--------------------------------|
| T3.1 | **Banach** | complete metric space + Lipschitz contraction | paper v8 § 5.2 已用 (mean-field linearization 后), L1 (plateau-only) |
| T3.2 | **Schauder** | compact convex set + continuous self-map | 不需 contraction, 但需 compactness, LLM parameter space `R^d` 非 compact, 需 restrict to bounded ball [?] |
| T3.3 | **Kakutani** | non-empty convex compact + upper hemicontinuous correspondence | multi-valued fixed-point, 适用 mixed-strategy 类 setting, LLM chain 单 valued 不必要 [?] |
| T3.4 | **Tarski** | complete lattice + monotone self-map | order-theoretic, LLM loss landscape 无 natural lattice 结构 [?] 适用性低 |
| T3.5 | **Brouwer** | compact convex + continuous | finite-dim, parameter space 高维但有限, 需 bounded domain |
| T3.6 | **Markov-Kakutani** | commuting family of continuous affine self-maps + compact convex | 适合 measure-theoretic setting, e.g. invariant distribution on parameter space |

→ 严格度 **L1**: toolkit suite 是 standard, **LLM-specific applicability 之 binary verify** 推 D60+。

### 3.3 反题 P0★ critical gap candidate (5 个 binary list, 反题 v8 audit cross-ref)

反题 audit v8 (ANTITHESIS_LAYER_PAPER_V8_FINAL_AUDIT_20260516.md) line 289 catch **6 P0★ critical**, 其中 3 项 ★★ fatal desk reject trigger:

| # | Gap | 反题 v8 audit cross-ref | severity |
|---|-----|------------------------|----------|
| G3.1 | **P0★-A**: Reading 2 mean-field linearization assumption (plateau-only valid, transient violated) | line 239-241 | ★ substantive (not fatal) |
| G3.2 | **P0★-F**: `D^code` vs `D^paper` definition mismatch 推 D60+ | line 281 | ★★ fatal (paper central comparison not rigorously linked) |
| G3.3 | **P0★-C**: v3 → v8 prediction PPL drift `43 → 54 → 48 → 48 → 55` (5 revisions) post-hoc curve fitting 嫌疑 | line 257 + line 305 | ★★ fatal |
| G3.4 | **non-self-mapping / multi-valued / stochastic fixed-point variants** (LLM training 之 SGD stochasticity → 需 stochastic fixed-point framework) | (paper v8 未 systematically address) [?] | substantive D60+ |
| G3.5 | **Operator splitting / iterative refinement variants** (chain actual two-term form 之 T_1 + T_2 splitting analysis) | (paper § 3.6 T_2 = 0 due to K=1, splitting 简化为 single-operator) | substantive D60+ |

### 3.4 LLM-native fixed-point theory 是否 differ from standard Banach (L1)

binary 修订: **未 derive**, 推 D60+。standard Banach 在 deterministic 设定下 work, LLM training 含 SGD stochasticity + non-convex landscape + adaptive optimizer (Adam, AdamW), **是否需 LLM-native variant** 需 substantive derive 才能 binary 答。

### 3.5 D60+ substantive future work seed (问 3)

**Seed S3.1**: 反题 P0★-A / P0★-F / P0★-C 中 **选 1 个** substantive close (paper v8 不动, 选定 case D60+ deferred work)。各 case substantive cost:

- P0★-A close: mean-field linearization assumption 之 transient regime 严格 valid 范围 derive (Hartree-Fock 或 non-equilibrium statistical mechanics 工具, **1-2 month substantive** [?])
- P0★-F close: `D^code` 与 `D^paper` definition mismatch 之 严格 mathematical linkage derive (paper § 6.1 已 推 D60+), **2-3 month substantive** [?] (含 D-PPL bridge verify, 见 memory)
- P0★-C close: prediction PPL `43 → 54 → 48 → 48 → 55` 五次 revision 之 **independent pre-registered prediction** binary verify (避免 post-hoc curve fitting), 需 **F-1 Phase 2 + N ≥ 8 multi-seed**, **2-3 month substantive** [?]

**[?]** 三 case 之 priority + sequencing 推 D60+ 一凡 + Linux 主会话决, 不今日 declare。

---

## 4. D60+ substantive future work seed binary list (汇总)

5-10 specific 方向, 一句 description 标 [?] 任何未 budget timeline:

1. **S1.1** (问 1): alternative EMA form C1.1-C1.5 在 chain experiment 上之 pre-registered paired comparison, N ≥ 8 multi-seed, **1-2 month** [?]
2. **S2.1** (问 2): LLM gen 轴 monoid Perron-Frobenius + Krohn-Rhodes finite-state binary verify, **1-2 month** [?]
3. **S2.2** (问 2): C2.3 Volterra K=9 lift 在 chain experiment 上 instantiate, 与 K=1 paired comparison, 与 S1.1 部分 overlap, **1 month** [?]
4. **S3.1a** (问 3 P0★-A close): mean-field linearization assumption transient regime 严格 valid 范围 derive (Hartree-Fock), **1-2 month** [?]
5. **S3.1b** (问 3 P0★-F close): `D^code` vs `D^paper` definition mismatch 严格 mathematical linkage derive (D-PPL bridge), **2-3 month** [?]
6. **S3.1c** (问 3 P0★-C close): prediction PPL 5 次 revision 之 independent pre-registered binary verify (F-1 Phase 2 + N ≥ 8 multi-seed), **2-3 month** [?]
7. **S4** (跨问 1-3): stochastic fixed-point theory framework (SGD stochasticity) 之 LLM-native instantiate, **3-6 month** [?]
8. **S5** (跨问 1-3): non-self-mapping / multi-valued fixed-point variants 之 LLM chain applicability binary verify, **2-3 month** [?]
9. **S6** (跨问 2-3): C2.4 C_0-semigroup continuous-time limit 之 LLM chain analog 严格 connection derive, **2-3 month** [?]
10. **S7** (跨问 1-2): Lipschitz-weighted history form (C1.2) + Volterra K=9 (C2.3) 之 unified Banach contraction analysis, **1-2 month** [?]

**全部 10 项 timeline + priority + sequencing 推 D60+ 一凡 + Linux 主会话决**, 不今日 declare ready, 不替 PI 决。

---

## 5. 严格度档位汇总

| 段 | 内容 | 档位 |
|----|------|------|
| § 0 | 修订 framing (Linux 主会话 verdict 引用) | L0 |
| § 1.1 | paper v8 § 3.2 + § 1.3 honest disclose 引用 | L1 (paper 自身已 honest disclose form-borrow) |
| § 1.2 | EMA 之 self-supervised learning 体系定位 | L1 |
| § 1.3 | alternative form 5 candidate list (不 derive) | L2 (form-borrow / 未 derive) |
| § 1.4 | D60+ seed S1.1 | L2 (timeline + 严格度未 budget) |
| § 2.1 | LLM gen 轴 monoid binary ✓ | L0 |
| § 2.2 | monoid representation theory 文献体系 | L1 (cite 未 hand-verify) |
| § 2.3 | monoid operator family 5 candidate list | L2 |
| § 2.4 | paper § 5.2 主定理 (2) = monoid action special case | L1 (mean-field linearization assumption) |
| § 2.5 | D60+ seed S2.1 + S2.2 | L2 |
| § 3.1 | fixed-point toolkit "不是借" binary 修订 | L0 |
| § 3.2 | toolkit LLM applicability outline | L1 |
| § 3.3 | 反题 P0★ critical gap 5 candidate list | L0 (反题 audit cross-ref binary) |
| § 3.4 | LLM-native fixed-point theory differ 与否 | L2 (未 derive) |
| § 3.5 | D60+ seed S3.1a/b/c | L2 |
| § 4 | D60+ seed 汇总 10 项 | L2 (timeline + priority 全部未 budget) |

---

## 6. caveat `[?]` 汇总

1. Steinberg 2016 + Rhodes-Steinberg 2009 content 未 hand-verify [?]
2. C1.1 (power-law) 与 paper § 3.6 mean-field NESS Banach contraction 之 严格 compatibility 未 derive [?]
3. C1.4 (Markovian) 退化 case fixed-point structure 是否同 paper § 3.6.4 未 derive [?]
4. C1.5 (adaptive-rate) 与 stationary mean-field NESS 之 compatibility 未 derive [?]
5. C2.2 (polynomial) 之 non-exponential mixing 严格 framework 未 verify [?]
6. C2.3 (Volterra K=9 lift) 之 严格 mathematical form 未 derive [?]
7. C2.4 (C_0-semigroup continuous-time limit) 之 严格 connection 未 derive [?]
8. C2.5 (Krohn-Rhodes finite-state) 之 LLM gen 轴 effective rank bound 未 verify [?]
9. T3.2 (Schauder) 在 LLM `R^d` 非 compact 上之 restriction 未 derive [?]
10. T3.3 (Kakutani) multi-valued setting 在 LLM chain 之 必要性 未 verify [?]
11. T3.4 (Tarski) 在 LLM loss landscape 上之 lattice 结构 未 verify [?]
12. G3.4 (non-self-mapping / multi-valued / stochastic variants) paper v8 未 systematically address [?]
13. G3.5 (operator splitting / iterative refinement) paper § 3.6 T_2=0 退化, splitting 简化, 未 K=1 → K>1 lift [?]
14. § 3.4 LLM-native fixed-point theory differ from standard Banach 与否 未 derive [?]
15. § 3.5 三 case (P0★-A / -F / -C close) timeline + priority + sequencing 未 budget [?]
16. § 4 全部 10 项 D60+ seed 之 timeline + priority + sequencing 未 budget [?]

---

## 7. 不做项 (D-1 binding 自检)

- ✗ 不写哲学 (哲学线管)
- ✗ 不写代码 (代码线管)
- ✗ 不写实验 protocol
- ✗ 不 estimate probability (反题 zero-context 管 + 一凡 + 反题三方决)
- ✗ 不替 PI declare ready
- ✗ 不 reopen paper v8 final lock manifest (47/47 ✓, 不动)
- ✗ 不 substantive derive 新 form (全部推 D60+)
- ✗ 不 escalate D18+ 任务

---

## 8. binary ack

D-2 数学线 D17 third wave outline binary 完成。

- 三问 outline ✓ (§ 1 + § 2 + § 3 共 ~ 2400 中文字 + LaTeX 公式)
- 5 alternative EMA form candidate ✓ (§ 1.3)
- 5 monoid operator family ✓ (§ 2.3, cite Steinberg 2016 + Rhodes-Steinberg 2009 [?])
- 5 gap candidate ✓ (§ 3.3, 反题 P0★-A/F/C cross-ref)
- D60+ seed 10 项 binary list ✓ (§ 4, timeline 全部 [?])
- 严格度档位标注 ✓ (§ 5)
- caveat [?] list 16 项 ✓ (§ 6)
- D-1 binding 自检 ✓ (§ 7)
- paper v8 final lock 不动 ✓
- 不 escalate D18+ ✓

返回 Linux 主会话。
