# MaoField L0 严格证明 — L0-4: D-PPL bridge 线性组合之 non-identifiability 定理

> 不可识别性定理 (negative L0) — C11 之 axiom-first 严格化, 直接对应反题 P0★-F FATAL (D^code vs D^paper definition mismatch)

## §0 Scope (范围声明 + 元数据 + 严守 binding)

### §0.1 元数据

| 项 | 值 |
|---|---|
| 真实日期 binary | `date '+%F %T %Z'` → **2026-05-29 10:32:48 CST** (D29) |
| 生成 agent | Opus 4.8 (1M context) 数学证明专家, 主会话 dispatch ("闭合 L0-4 第一轮严格证明") |
| **agent caveat (诚实 disclose)** | 本证明非 zero-context fresh session: 已 load 项目 memory + CLAUDE.md, 偏离 prompt §13 之独立验证通道设计意图。该 caveat 执行前 disclose, 故 §9 第 5 通道 (反题独立性) 弱于理想 zero-context, 留 PI + 关卡 3 反题三方决再派遣独立 channel 复核 |
| 协议 | axiom-first 严格推导: definition → lemma → theorem (non-identifiability) → proof → corollary → falsifier → limitation; 5 通道 cross-verify; 每数有 jsonl/文献源 |
| input source | S3 PART ATTEMPT1 (MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S3, §1.1-§2.5 三量定义 + L0 未 close 理由 + 4 Path) + D28_MATH_RIGOROUS_AUDIT (C11 tier + §6.1 anchor 4) + MULTI_CHANNEL_ANALYSIS (X5 candidate 3 + N21/N22/N23) + L0-1 PROOF (格式 + 诚实 negative 写法范本) |
| 字数 | ~4200 字 substantive |

### §0.2 闭合什么 / 不闭合什么 (诚实 scope, 反 grandiose)

**本证明严格闭合 (L0 axiom-first, 但 verdict 是 negative)**:

1. **代数层 non-identifiability 完全闭合** — single-chain 数据下, $(w_B, w_C)$ 之 OLS 估计因 design matrix 秩亏而不可识别, 解集是一维 affine 流形; $w_B=w_C=0.5$ 仅是其上无穷多解之一。严格给出唯一识别之必要条件 (Rothenberg 1971 rank condition)。
2. **measure-theoretic 层 non-identifiability 完全闭合** — $D^{\rm code,B/C}$ (train-signal val-set KL) 与 $D^{\rm paper}$ (test-signal log-PPL-ratio) 之 base measure 不重合, 无 trivially well-defined Radon-Nikodym derivative; 即便数值 fit, 也不构成 measure-theoretic identification (直接 P0★-F FATAL 之 root)。
3. **统计层 non-rejectability 完全闭合** — 0.030 abs diff (6.76% rel) 落在 single-chain sampling noise band 内, 现有数据不足以 reject "no structural linear relationship beyond chance" 之 null hypothesis。
4. **close 之必要条件闭式给出** — Path A (33 GPU-hour SGD EMA replay, 5060 fp32 cu130 baseline 重跑) 提供跨 $n$ 变化之多个独立 $(B,C,{\rm paper})$ 三元组 + cross-regime, 是 identifiability 之必要 (非充分) 条件。

**本证明明确 NOT 闭合 (留 D60+ + 反题三方决)**:

- **positive identification** — 本定理 **不** declare 线性组合存在/成立; 只严格证明当前数据下 "若存在也不可识别"。即便 Path A 数据齐全, $(w_B, w_C)$ 之 positive identification + structural interpretation 仍留 D60+ Path D (severe derive) + 反题三方决。
- **P0★-F 之 final close** — 本定理把 P0★-F FATAL 之 root (base measure mismatch) 严格 formalize, 但 **不** declare P0★-F 被 resolve; FATAL tier 之升降留 PI + 反题三方决。

**"negative L0" 之精确含义** = 本证明之结论是一个不可识别性定理 (non-identifiability theorem): 它严格证明 "为何 0.030 coincidence 不构成结构性识别", 而非证明任何 bridge "已 close"。这正是项目最警惕 inflate 之一条 — 把 numerical coincidence 误报为 structural identification。

### §0.3 严守 binding

paper v8 final 47/47 manifest D17 锁定不动; 12 NOT-claim (i)-(xii) 撤回不复活 (本文件 **不** declare D-PPL bridge "已 close" / "first" / paradigm / structural identification); 反题 6 P0★ 严守 (**P0★-F FATAL = 本条核心**, 本证明 formalize 其 root 但不升降 tier; P0★-A = chain 是 $\theta$-space SGD, 本证明全程尊重该 disclose); D29 三 leg arXiv+TMLR+KBS 不动; 本证明 0 commit / 0 push / 0 launch 新实验 / 0 ssh write / 0 sub-agent 派遣; L0 是 D60+ window candidate, 不进 paper v9 spine, 留 PI + 关卡 3/4 决。

---

## §1 Setup (公理化设定)

### §1.1 三个 probability space 与 random variable ($\theta$-space, 遵从反题 P0★-A)

**参数空间**: $\Theta = \mathbb{R}^d$ (OPT-125M, $d \approx 1.25\times 10^8$)。链第 $n$ 代权重 $\theta_n \in \Theta$, 由 SGD-on-$\theta$ 递推产生 (反题 P0★-A: chain reality 是 $\theta$ 空间更新, 非 $D$ 空间)。

**两个 sample space (核心 — 不重合)**:
- $(\mathcal{X}_{\rm val}, \mathcal{F}_{\rm val}, \mu_{\rm val})$ = validation 样本空间 (chain train-signal 分布, val subset 256 句)。
- $(\mathcal{X}_{\rm test}, \mathcal{F}_{\rm test}, \mu_{\rm test})$ = test 样本空间 (wikitext-2 test split, **与 train-signal disjoint**)。

**vocabulary**: $V$, token 分布 $q^\theta(\cdot\mid x), p^\theta(\cdot\mid x) \in \Delta(V)$ (categorical)。

### §1.2 公理 (A1)-(A5)

- **(A1) 三量 well-defined**: $D_n^{\rm code,B}, D_n^{\rm code,C}, D_n^{\rm paper}$ 各为 well-defined random variable (over $\theta_n$ 之 stochastic process + 各自 sample space 之 sampling noise)。[S3 §1.2 A1]
- **(A2) reference measure disjoint-support**: $\mu_{\rm val}$ 与 $\mu_{\rm test}$ 支撑集 disjoint (train/test split disjoint, dataset 构造 enforce)。
- **(A3) single-chain data regime**: 现有数据 = D22 main run, 4 seed × 2 alpha × 10 gen, 9070XT fp16 single ROCm regime; B path n=72 valid, C path n=80 valid。[N21, main_D22.jsonl sha256 `3478be8e...`]
- **(A4) B/C ratio 近似固定**: 跨 $n$ 之 $(D_n^{\rm code,B}, D_n^{\rm code,C})$ 配对之 ratio $r_n := D_n^{\rm code,B}/D_n^{\rm code,C}$ 在 single-chain 内近似常数 (D22 mean ratio B/C $= 0.2883/0.5527 = 0.5216$; D21 pilot $= 0.29622/0.58998 = 0.5021$, 两 regime 一致到 4%)。[N21+N22]
- **(A5) sampling noise scale**: $D^{\rm paper}$ 之 single-chain bootstrap CI half-width $\approx 1.817$ PPL (paper §4.5 bootstrap, $N_{\rm boot}=10000$, seed 20260519), 对应 log-PPL-ratio 尺度 noise band $\gtrsim 0.03$ nat。[M19, paper line 590, 643]

---

## §2 Definitions

**Def 1 (三量精确定义 — 实践先行, 来自 S3 §1.1 code-anchor)**:
$$D_n^{\rm code,B} := \mathbb{E}_{x\sim\mu_{\rm val}}\big[\mathrm{KL}\big(q_{n-1}^{\theta_{\rm proxy\text{-}EMA}}(\cdot\mid x)\,\big\|\,p_n^\theta(\cdot\mid x)\big)\big] \quad (\text{proxy-EMA reference, gen-}(n{-}1))$$
$$D_n^{\rm code,C} := \mathbb{E}_{x\sim\mu_{\rm val}}\big[\mathrm{KL}\big(q_0^{\theta_{\rm base}}(\cdot\mid x)\,\big\|\,p_n^\theta(\cdot\mid x)\big)\big] \quad (\text{base anchor reference, gen-}0)$$
$$D_n^{\rm paper} := \log\big(\mathrm{PPL}_n^{\rm test}/\mathrm{PPL}_0^{\rm test}\big) = \mathcal{L}_n^{\rm test} - \mathcal{L}_0^{\rm test} \quad (\text{test-set log-PPL-ratio})$$
其中 $\mathcal{L}_n^{\rm test}$ = 第 $n$ 代 model 在 test set 之 mean per-token NLL (nat/token)。

**Def 2 (S3 待识别 proposition)**: 存在 $w_B, w_C \ge 0$ 与 noise $\xi_n$ ($\mathbb{E}[\xi_n]=0$) 使
$$D_n^{\rm paper} = w_B\, D_n^{\rm code,B} + w_C\, D_n^{\rm code,C} + \xi_n .$$

**Def 3 (identification — Rothenberg 1971 意义)**: 参数 $(w_B, w_C)$ **identifiable** $\iff$ 由观测数据生成之 likelihood / moment 唯一决定 $(w_B, w_C)$; 等价于不存在两组 distinct $(w_B, w_C) \ne (w_B', w_C')$ 给出 observationally equivalent 分布。

**Def 4 (design matrix 与 rank condition)**: 给定 $N$ 个跨 $n$ 之配对 $\{(D_n^{\rm code,B}, D_n^{\rm code,C})\}_{n=1}^N$, design matrix
$$X := \begin{pmatrix} D_1^{\rm code,B} & D_1^{\rm code,C} \\ \vdots & \vdots \\ D_N^{\rm code,B} & D_N^{\rm code,C} \end{pmatrix} \in \mathbb{R}^{N\times 2}.$$
OLS 估计 $\hat{w} = (X^\top X)^{-1} X^\top y$ 存在唯一解 $\iff \mathrm{rank}(X)=2 \iff (X^\top X)$ 非奇异。

**Def 5 (measure-theoretic identification)**: 线性组合 $D^{\rm paper} = w_B D^{\rm code,B} + w_C D^{\rm code,C}$ **measure-theoretically identified** $\iff$ 存在 well-defined Radon-Nikodym derivative 关系连接 $D^{\rm paper}$ 之 base measure ($\mu_{\rm test}$ 上之 log-loss-ratio) 与 $D^{\rm code,B/C}$ 之 base measure ($\mu_{\rm val}$ 上之 KL), 使线性组合在测度意义下 well-defined (非仅数值 fit)。

---

## §3 Lemmas

### Lemma 1 (single-chain design matrix 秩亏)

在 (A3)+(A4) 下: D22 single-chain 数据之 design matrix $X$ 满足 $\mathrm{rank}(X) \to 1$ (近似秩 1)。

**证**: (A4) $\Rightarrow r_n = D_n^{\rm code,B}/D_n^{\rm code,C} \approx r_\star$ (常数, $r_\star \approx 0.52$)。故每行 $(D_n^{\rm code,B}, D_n^{\rm code,C}) \approx D_n^{\rm code,C}\cdot(r_\star, 1)$, 即所有行近似共线于方向 $(r_\star, 1)$。则 $X \approx \mathbf{c}\,(r_\star,1)$ ($\mathbf{c}\in\mathbb{R}^N$ 列向量), $\mathrm{rank}(X)\approx 1 < 2$。$(X^\top X)$ 之条件数 $\kappa \to \infty$, OLS 不可识别 (Def 4)。$\blacksquare$

> **直觉**: 跨 $n$ 之 B 与 C 同步缩放 (ratio 固定), 故 design 只 "看到" 一个有效自由度。要分开 $w_B$ 与 $w_C$, 必须有 B/C ratio **变化** 之配对 — single-chain 没有。

### Lemma 2 (under-determination 之 affine 解集)

单一聚合等式 $w_B\cdot 0.2883 + w_C\cdot 0.5527 = 0.451 - \bar\xi$ (取 $\bar\xi$ 为 mean residual) 之解集是 $\mathbb{R}^2$ 中一条直线 (一维 affine 流形):
$$\mathcal{S} = \big\{(w_B, w_C)\in\mathbb{R}_{\ge0}^2 : 0.2883\,w_B + 0.5527\,w_C = 0.451 - \bar\xi\big\}.$$

**证**: one equation in two unknowns, 系数非零, 解集是直线与第一象限之交 (非空线段)。$w_B=w_C=0.5$ ($\bar\xi = 0.451-0.4205 = 0.0305$) 是 $\mathcal{S}$ 上一点; $(w_B, w_C)=(0.3, 0.628)$ 验证: $0.2883\times0.3 + 0.5527\times0.628 = 0.0865+0.3471 = 0.4336$, 配 $\bar\xi=0.0174$ 同样满足 Def 2 form。故 $|\mathcal{S}|=\infty$, 无唯一解。$\blacksquare$

> S3 §2.3 + D28 C11 已 surface 此 "one equation in two unknowns ill-posed identification"; 本 Lemma 给出严格 affine-manifold form。

### Lemma 3 (base measure 不重合 → 无 trivial Radon-Nikodym)

在 (A2) 下: $D^{\rm code,B/C}$ 之 base measure $\mu_{\rm val}$ 与 $D^{\rm paper}$ 之 base measure $\mu_{\rm test}$ 互奇异 (mutually singular, $\mu_{\rm val}\perp\mu_{\rm test}$), 故不存在 trivial Radon-Nikodym derivative $\frac{d\mu_{\rm test}}{d\mu_{\rm val}}$。

**证**: (A2) train/test split disjoint $\Rightarrow$ 支撑集 $\mathrm{supp}(\mu_{\rm val}) \cap \mathrm{supp}(\mu_{\rm test}) = \emptyset$ (样本级)。两测度互奇异 $\Rightarrow$ $\mu_{\rm test}$ 关于 $\mu_{\rm val}$ 不绝对连续 ($\mu_{\rm test}\not\ll\mu_{\rm val}$) $\Rightarrow$ Radon-Nikodym 定理之前提不满足, $\frac{d\mu_{\rm test}}{d\mu_{\rm val}}$ 不存在 (作为 $\mu_{\rm val}$-a.e. 有限函数)。$\blacksquare$

> **这是 P0★-F FATAL 之 measure-theoretic root**: $D^{\rm code}$ 是 train-signal 上之 KL (reference = $q^{\rm EMA}/q^{\rm base}$), $D^{\rm paper}$ 是 test-signal 上之 log-loss-ratio; 三量 live 在不同 base measure 上 (S3 §2.1 verbatim "三 random variable 之 base measure binary 不重合")。

### Lemma 4 (统计 non-rejectability)

在 (A5) 下: 现有 single-chain 数据不足以 reject null hypothesis $H_0$ = "no structural linear relationship beyond chance"。

**证**: 0.030 abs diff 之 reject 需 bootstrap CI half-width of $|\hat{D}^{\rm paper} - \hat{D}^{\rm code\text{-}fit}| < 0.030$ (S3 §2.4 criterion 3)。但 (A5) 之 single-chain noise band $\gtrsim 0.03$ nat (由 1.817 PPL bootstrap half-width 换算到 log-PPL-ratio 尺度)。CI half-width $\gtrsim$ effect size $\Rightarrow$ CI 包含 0 $\Rightarrow$ 不 reject $H_0$。$\blacksquare$

> S3 §2.5 candidate 2: 0.030 落在 "单 chain runner + 单 seed cohort + 单 dtype regime 之 sampling noise band 之内", null hypothesis reject 之统计证据不足。

---

## §4 Main Theorem (non-identifiability)

**定理 (D-PPL bridge 线性组合之三层不可识别性)**. 设 (A1)-(A5) 成立。则在现有 single-chain (D22 main) 数据下, Def 2 之线性组合参数 $(w_B, w_C)$ 在以下三个独立意义下 **不可识别**, 且数值符合 ($\tfrac12(B+C)=0.4205$ vs $D^{\rm paper}=0.451$, abs diff 0.030) **不构成** 结构性识别:

**(I) 代数层 (structural under-determination)** — design matrix 秩亏 (Lemma 1), 解集是一维 affine 流形 (Lemma 2)。唯一识别 $(w_B, w_C)$ 之 **必要条件** 是 $\mathrm{rank}(X)=2$, 即跨 $n$ 须有 **$\ge 2$ 个 linearly independent 之 $(D_n^{\rm code,B}, D_n^{\rm code,C})$ 配对** (B/C ratio 必须变化)。single-chain 不满足。

**(II) measure-theoretic 层** — $D^{\rm code,B/C}$ 与 $D^{\rm paper}$ 之 base measure 互奇异 (Lemma 3)。即便数值上 $\tfrac12(B+C)\approx D^{\rm paper}$, 该线性组合 **不** measure-theoretically identified (Def 5): 不存在连接 train-signal 与 test-signal 之 well-defined Radon-Nikodym derivative, 故 "$D^{\rm paper}$ = $D^{\rm code}$ 之线性组合" 在测度意义下不 well-defined。

**(III) 统计层 (non-rejectability)** — 0.030 abs diff (6.76% rel) 落在 single-chain sampling noise band 内 (Lemma 4), 不能 reject "no structural linear relationship beyond chance" 之 $H_0$。

**推论 (verdict)**: C11 之 "$\tfrac12(B+C)\approx D^{\rm paper}$" 是 **numerical coincidence**, 在 (I)(II)(III) 三层意义下均 **非** structural identification。L0-4 之 verdict 是 **negative** (non-identifiability theorem)。

---

## §5 Proof (主定理证明)

**(I) 代数层证明** — 由 Lemma 1, single-chain $X$ 秩亏 ($\mathrm{rank}\to1$), $(X^\top X)$ 奇异, OLS 无唯一解。由 Lemma 2, 聚合等式解集 $\mathcal{S}$ 是一维 affine 流形, $w_B=w_C=0.5$ 与 $(0.3,0.628)$ 等无穷多点同样满足。**必要条件**之严格性 (Rothenberg 1971 Thm, structural identifiability rank condition): 线性模型 $y=Xw+\xi$ 之 $w$ identifiable $\iff$ $\mathrm{rank}(X)$ 等于参数个数 ($=2$)。$\mathrm{rank}(X)=1<2 \Rightarrow$ 不可识别。要达 $\mathrm{rank}(X)=2$, 须至少两行线性无关, 即 $\exists\, n_1, n_2: \det\begin{pmatrix}D_{n_1}^{\rm code,B}&D_{n_1}^{\rm code,C}\\ D_{n_2}^{\rm code,B}&D_{n_2}^{\rm code,C}\end{pmatrix}\ne 0$, 等价 $r_{n_1}\ne r_{n_2}$ (B/C ratio 变化)。$\blacksquare$

**(II) measure-theoretic 层证明** — 由 Lemma 3, $\mu_{\rm val}\perp\mu_{\rm test}$ (A2)。设若线性组合 measure-theoretically identified (Def 5), 则需 $D^{\rm paper}$ 之 base measure 可表为 $D^{\rm code,B/C}$ base measure 之某 affine combination 之测度 (Radon-Nikodym form)。但 $D^{\rm code,B/C}$ 之 base measure 全在 $\mu_{\rm val}$ 上, $D^{\rm paper}$ 之 base measure 在 $\mu_{\rm test}$ 上, 二者互奇异 $\Rightarrow$ 任何 $\mu_{\rm val}$-可测之线性组合在 $\mu_{\rm test}$ 上 $\mu_{\rm test}$-a.e. 不可定义其 RN derivative。矛盾。故线性组合不 measure-theoretically identified。数值 fit ($\tfrac12(B+C)\approx D^{\rm paper}$) 仅是两个 live 在不同测度上之标量之数值接近, 不携带测度同构。$\blacksquare$

> **与 Borji 2024 之衔接**: Borji 2024 (arXiv:2410.12954) "metric-dependent collapse characterization" 已 surface "conclusions drawn can vary depending on the choice of distance metric" (KL stabilize vs Wasserstein grow) — 直接 cover P0★-F 之 measure-dependence (不同 metric / 不同 base measure 给不同 verdict)。但 Borji 2024 **不** declare $\tfrac12(B+C)$ 之 specific linear form (S3 §2.3 + D28 C11)。故本层 borrow Borji 之 measure-dependence message 作 input axiom, 不主张文献首创。

**(III) 统计层证明** — 由 Lemma 4, single-chain noise band $\gtrsim 0.03 \gtrsim$ effect size 0.030, bootstrap CI 包含 0, 不 reject $H_0$。故 0.030 之 "接近" 在统计上与 chance coincidence 不可区分。$\blacksquare$

**verdict 推论证明** — (I)(II)(III) 各自独立成立; 任一层不可识别即足以否定 "structural identification" claim。三层同时成立 $\Rightarrow$ C11 之数值符合是 numerical coincidence 而非 structural identification, L0-4 verdict negative。$\blacksquare$

---

## §6 Corollaries (数值实例化 + close 必要条件)

### Cor 1 (affine 解集之数值实例化)

代入 N21 (D22 mean): $0.2883\,w_B + 0.5527\,w_C = 0.451 - \bar\xi$。
- $w_B=w_C=0.5 \Rightarrow$ LHS $=0.4205$, $\bar\xi=0.0305$ (rel 6.76%, **超 5% strict, 在 10% partial 内**)。[N23]
- $w_B=0.3, w_C=0.628 \Rightarrow$ LHS $=0.4336$, $\bar\xi=0.0174$ (rel 3.86%, 更优 fit!)。
- $w_B=0, w_C=0.816 \Rightarrow$ LHS $=0.4510$, $\bar\xi=0$ (exact, 纯 C anchor)。
- $w_B=1.564, w_C=0 \Rightarrow$ LHS $=0.4510$, $\bar\xi=0$ (exact, 纯 B anchor)。

> **关键 inflate 警示**: $w_B=w_C=0.5$ **不是** best fit (rel 6.76%), $(0.3,0.628)$ 之 rel 3.86% 更好, 纯 C/纯 B anchor 甚至 exact。"对称 $\tfrac12(B+C)$" 之选择 **没有数据支持优越性**, 是 symmetric assumption 之 artifact。这正是 negative theorem 之 honest 价值: 数值符合极易诱导 "对称组合成立" 之误判, 而严格看, 对称解在解集内毫无特殊地位。

### Cor 2 (close 之必要条件 — Path A)

由定理 (I) 之必要条件 ($\mathrm{rank}(X)=2$ + B/C ratio 变化), close L0-4 之 **必要 (非充分) 条件**:

**Path A (33 GPU-hour SGD EMA replay)**:
- 在 **5060 fp32 cu130 baseline 重跑** (不在 9070XT fp16 ROCm regime, 排除 P0★-G confound — D24 surface 之 5060 fp32 36.536 vs 9070XT fp16 93.349 之 +56.81 PPL cross-stack split)。
- 提供跨 $n=1,\dots,9$ 之多个独立 $(D_n^{\rm code,B}, D_n^{\rm code,C}, D_n^{\rm paper})$ **三元组**, 且 B/C ratio 跨 $n$ 变化 (满足 $\mathrm{rank}(X)=2$)。
- cross-regime (fp32 vs fp16) 排除 numerical-stability confound。
- ETA: ~33 GPU-hour (S3 §4 Path A; 留 PI + 关卡 3 + 关卡 4 scheduling 决)。

> **必要 ≠ 充分**: 即便 Path A 给出 $\mathrm{rank}(X)=2$ 数据并算出 $(\hat{w}_B, \hat{w}_C)$ 之有限 CI, 仍只闭合代数层 (I); measure-theoretic 层 (II) 之 base measure mismatch **不因数据量增加而消失** (Lemma 3 是结构性, 非样本量问题)。故 (II) 之 close 须 Path D (severe derive: train-signal-on-test-signal decomposition 之 Radon-Nikodym 关系严格建立, 或证明其不存在)。

### Cor 3 (与 S1/S2 之 cross-tension — frozen regime confound)

S3 §3.2 surface: 若 D22 chain 落入 S1 (b) frozen regime ($\theta_n=\theta_{\rm base}$, fp16 GradScaler skip, L0-1 已严格闭合该 regime), 则 $D_n^{\rm code,C}=\mathrm{KL}(q_0^{\theta_{\rm base}}\|p_n^{\theta_{\rm base}})$ 应 $=0$ (self-KL), 但实测 mean $=0.5527\ne0$。这暗示 D22 数据是 **mixed regime** (部分 frozen + 部分 partial-update) 或 proxy-EMA reference 之非平凡贡献。**此 confound 进一步削弱 single-chain 之 identifiability**: 不仅 ratio 固定 (Lemma 1), 数据本身可能混合两 attractor regime, 使 $(w_B, w_C)$ 即便在代数层也无 stable 解释。留 D60+ 与 S1 joint close。

---

## §7 Falsifier (可证伪条件)

- **F-L0-4-a (代数层证伪)**: 若 Path A 数据 (跨 $n$ B/C ratio 变化) 之 design matrix $X$ 满足 $\mathrm{rank}(X)=2$ **且** OLS $(\hat{w}_B,\hat{w}_C)$ 之 95% CI **同时排除** $(0.5,0.5)$ 之零测度邻域以外之所有点 (即 collapse 到唯一点), 则 "不可识别" 之代数层被部分推翻 (identifiability 恢复)。**成本 = Path A 33 GPU-hour**。
- **F-L0-4-b (measure-theoretic 层证伪)**: 若能严格构造连接 $\mu_{\rm val}$ 与 $\mu_{\rm test}$ 之 well-defined RN derivative (例如 train/test 同分布之 covariate shift 显式 density ratio), 则 Lemma 3 之 "互奇异" 前提被推翻, (II) 层不再成立。**成本 = 数学 derive (Path D), 0 GPU**; 但 (A2) train/test split disjoint 是 dataset 构造事实, 该 falsifier 大概率不成立。
- **F-L0-4-c (统计层证伪)**: 若 N≥8 multi-seed bootstrap 给出 $|\hat{D}^{\rm paper}-\hat{D}^{\rm code\text{-}fit}|$ 之 CI half-width $<0.030$, 则 Lemma 4 之 non-rejectability 被推翻, 可 reject $H_0$。**成本 = N≥8 multi-seed chain runner** (S3 Path B)。
- **F-L0-4-d (residual structure 证伪)**: 若 Path A 之 residual $\xi_n$ 显示 systematic structure (non-zero mean / autocorrelation / heteroskedasticity, by Ljung-Box / Breusch-Pagan), 则 "$\xi_n$ 是纯 noise" 之 Def 2 假设被推翻, 线性 form misspecified (S3 §2.4 criterion 2)。**成本 = Path A 后处理, 0 额外 GPU**。

---

## §8 Limitations (限制)

- **L1 (negative-only scope)**: 本定理只证明 "当前不可识别 + numerical coincidence 非 structural", **不** 证明线性组合不存在。positive non-existence (证明任何 $(w_B,w_C)$ 都不能 structurally 解释 $D^{\rm paper}$) 是更强 claim, 本证明 **不** 主张。
- **L2 (measure-theoretic 层之 absolute-continuity 例外)**: Lemma 3 之互奇异基于样本级 disjoint。若 train/test 来自同一 underlying 连续分布 (population-level absolute continuity), 则在 population 测度上 RN derivative 可能存在 — 但 chain 之 KL/PPL 是 empirical 样本上 computed, 故 empirical 层互奇异仍 binds。该 population-vs-empirical 区分留 D60+ formalize。
- **L3 (ratio 固定之 approximate 性)**: (A4) "B/C ratio 近似固定" 是 D22+D21 两 regime 之 empirical observation (0.5216 vs 0.5021, 一致到 4%), 非严格 0 variance。若实际有微小 ratio variation, $\mathrm{rank}(X)$ 理论上 $=2$ 但条件数 $\kappa$ 巨大, OLS 数值不稳定 (ill-conditioned 而非严格 singular) — 实践上仍不可识别 (Cor 1 之多解共存)。
- **L4 (P0★-G confound 未隔离)**: D22 数据在 9070XT fp16 ROCm regime; cross-stack +56.81 PPL (P0★-G) 之 root cause 未闭合, 故 $D^{\rm paper}$ 之 base PPL 本身可能含 implementation confound, 使三元组之 cross-regime 解释复杂化。Path A 之 5060 fp32 重跑正是为隔离此 confound。
- **L5 (frozen regime mixture)**: Cor 3 之 mixed-regime confound 未定量隔离, 留与 S1 joint close。
- **L6 (agent 非 zero-context)**: §0.1 caveat, 第 5 通道独立性弱于理想, 留反题三方决复核。

---

## §9 5-channel cross-verify (五通道交叉验证)

| 通道 | 内容 | verdict |
|---|---|---|
| **1 数学** (本证明) | Rothenberg rank condition + 互奇异测度无 RN derivative + bootstrap noise band; 三层 non-identifiability 严格 | L0 闭合 (negative): 三层不可识别严格成立; positive identification + P0★-F final close **不**闭合 (留 D60+) |
| **2 代码/数据** | 三量 def code-anchor (S3 §1.1, gen-(n-1) proxy-EMA / gen-0 base anchor / test log-PPL-ratio); main_D22.jsonl path 字段一致 | ✓ 一致: B/C ratio 固定 (0.5216) 来自 jsonl mean; train/test disjoint 来自 dataset 构造 |
| **3 实验** | N21 (B=0.2883 n=72 / C=0.5527 n=80 / D=0.451); N22 (D21 pilot B=0.29622 / C=0.58998); N23 (mean 0.4205, abs diff 0.030, 6.76% rel); ratio B/D=0.640 C/D=1.226 (factor-of-2) | ✓ 一致: 数值符合 confirmed, 但 Cor 1 显示对称解非 best fit (negative 支持) |
| **4 文献** | Rothenberg 1971 (rank condition) / Koopmans-Reiersøl 1950 (factor identification) / Radon-Nikodym / Borji 2024 (metric-dependence) / Manski 2003 (partial identification) / Allman-Matias-Rhodes 2009 (latent class) | ✓ 框架 borrow valid, 非首创; Borji 2024 cover measure-dependence 但不 cover specific $\tfrac12(B+C)$ form |
| **5 反题** | P0★-F FATAL = 本条 root 严格 formalize (base measure mismatch = Lemma 3), tier **不**升降; P0★-A ($\theta$-space SGD) **satisfied** (全程 $\theta$-space) | ✓ P0★-F root 形式化; 但本 agent 非 zero-context (§0.1), 第 5 通道独立性弱, 留反题三方决复核 |

**surface dissonance (诚实)**: (1) C11 currently L1 "partial numerical coincidence", 本定理把其 L0 verdict 严格定为 **negative non-identifiability** — 这是 tier 之 **澄清而非升级** (L1 numerical coincidence ⊂ negative L0 之 "不可识别" 结论, 不矛盾, 互补); (2) Cor 3 之 frozen-regime mixture 与 S1 cross-tension 未隔离; (3) 本 agent 非 zero-context。

---

## §10 Open Questions

**P0 (paper-rigor priority)**:
1. **Path D — train-signal-on-test-signal decomposition 之 RN 关系**: 严格建立 (或证否) $D^{\rm paper}$ 与 $D^{\rm code}$ 之 measure-theoretic 桥 (Lemma 3 互奇异是否可在 population 层绕过)。这是 measure-theoretic 层 (II) close 之唯一路径, 也是 P0★-F FATAL final close 之核心。

**P1**:
2. **Path A 实做后之 positive identification**: 跨 $n$ ratio 变化数据 + OLS CI + residual diagnostics (Ljung-Box / Breusch-Pagan), 在代数层尝试 positive identify $(w_B, w_C)$ (但仍受 (II) 限制)。
3. **与 S1 joint close (frozen-regime mixture 隔离)**: 定量分离 D22 chain 之 frozen vs partial-update fraction (Cor 3), 厘清 $D^{\rm code,C}\ne0$ 之来源。

**P2**:
4. **N≥8 multi-seed bootstrap (统计层)**: reject/accept $H_0$ 之 CI half-width 是否 $<0.030$ (F-L0-4-c)。
5. **partial identification framework (Manski 2003)**: 若 point identification 不可达, 是否可给 $(w_B,w_C)$ 之 identified set (bounds) — 比 point estimate 更诚实之 D60+ 方向。

---

## §11 14-Q self-check (prompt §11)

| # | 问 | 自检 |
|---|---|---|
| 1 | 数字有 jsonl 源? | ✓ B=0.2883 (n=72) / C=0.5527 (n=80) / D=0.451 / mean 0.4205 / abs diff 0.030 / ratio 0.640+1.226 全 main_D22.jsonl (sha256 `3478be8e...`) + N21/N22/N23 verbatim |
| 2 | 概率声明真空 >48h? | ✓ 不 declare 接受率; 仅数学 negative verdict |
| 3 | 数学形式与代码一致? | ✓ 三量 def ⟺ S3 §1.1 code-anchor (proxy-EMA / base anchor / test log-PPL-ratio), 通道 2 |
| 4 | major 声明过子协作者验证? | partial — 本 agent 非 zero-context (§0.1), 留反题三方决复核第 5 通道 |
| 5 | 差异记差异日志? | ✓ Cor 1 surface "$w_B=w_C=0.5$ 非 best fit, $(0.3,0.628)$ rel 3.86% 更优" 不抹平; C11 tier L1→negative L0 之澄清 (§9 dissonance 1) explicit |
| 6 | 真实日期 binary? | ✓ §0.1 `date` 2026-05-29 10:32:48 CST |
| 7 | 哲学位置 outcome 非 starting form? | ✓ 数学是 retrospective 严格化; 起点是 jsonl 数值符合现象 (0.030 coincidence 先于公理), 严格化为不可识别定理 |
| 8 | "自发" 含 multi-agent binding? | ✓ L0 closure 留 PI + 关卡 3/4; Path A/D scheduling 留三方决, 不 unilateral declare |
| 9 | 回顾 scope 含 4 项? | ✓ 12 NOT-claim 不复活 (§0.3, 不 declare structural identification = NOT-claim 防 inflate) + 反题 P0★ (通道 5, P0★-F root) + 5/12+5/19 inflate (本定理 anti-inflate 即防同类: 数值符合误报 structural) |
| 10 | timeline emerge D60+ 非 D22-D60? | ✓ §0.2 + Cor 2 + §10 全标 D60+ candidate, 不入 paper v9 spine |
| 11 | candidate 用 dialectical inclusive form? | ✓ §9 dissonance 1: C11 L1 numerical coincidence 与 negative L0 不可识别 是 inclusive (互补澄清), 不 declare "L1 错"; 不 declare "bridge 全不可能" (只 "当前不可识别") |
| 12 | paradigm-shift emergent D60+ verify? | ✓ 留 D60+ cumulative multi-channel + 反题三方决; 本定理是 negative, 远离 paradigm claim |
| 13 | methodological 4 path binary specify? | ✓ §7 falsifier = path A (multi-channel cross-verify, F-a) + path C (temporal/multi-seed, F-c) + path D (counter-factual decomposition, F-b/d) instantiate |
| 14 | 5 leg 实验 dialectical totality? | ✓ Cor 3 + §10 Q3: 与 S1 joint close (frozen-regime mixture) = cross-layer evidence, 非 single-axis |

任一 no → 不发出。第 4 + 第 5 通道 partial (非 zero-context), 已 explicit disclose, 留复核; 余 ✓。

---

## §12 References (prior art, 反 grandiose: 全为 borrow 非首创)

1. Rothenberg T.J. 1971. *Identification in Parametric Models*. Econometrica 39(3):577-591. [structural identifiability rank condition, 定理 (I) 核心]
2. Koopmans T.C., Reiersøl O. 1950. *The Identification of Structural Characteristics*. Ann. Math. Statist. 21(2):165-181. [identification in factor analysis, under-determination]
3. Radon J. 1913 / Nikodym O. 1930. *Radon-Nikodym theorem*. [测度绝对连续 ⟹ derivative 存在; Lemma 3 之逆否]
4. Borji A. 2024. *A Note on Shumailov et al. (2024): 'AI Models Collapse When Trained on Recursively Generated Data'*. arXiv:2410.12954. [metric-dependent collapse characterization, KL stabilize vs Wasserstein grow — cover P0★-F measure-dependence, 但不 declare $\tfrac12(B+C)$ form]
5. Manski C.F. 2003. *Partial Identification of Probability Distributions*. Springer. [point identification 不可达时之 identified set, §10 Q5]
6. Allman E.S., Matias C., Rhodes J.A. 2009. *Identifiability of Parameters in Latent Structure Models*. Ann. Statist. 37(6A):3099-3132. [latent class identifiability, 多配对 rank 条件]
7. Shumailov I. et al. 2024. *AI models collapse when trained on recursively generated data*. Nature 631:755-759. [model collapse baseline, 项目现象源]
8. Greene W.H. 2018. *Econometric Analysis* (8th ed.), Ch.8. [OLS rank / 多重共线性 ill-conditioning, Lemma 1]

---

**生成**: Opus 4.8 (1M context) 数学证明专家, 主会话 dispatch, 2026-05-29 10:32:48 CST 启动。

**核心 output**: L0-4 = D-PPL bridge 线性组合之 **non-identifiability 定理 (negative L0)**。三层严格不可识别: (I) 代数层 — single-chain design matrix 秩亏 (B/C ratio 固定 0.5216), 解集一维 affine 流形, $w_B=w_C=0.5$ 非 best fit ($(0.3,0.628)$ rel 3.86% 更优, 纯 anchor 甚至 exact); (II) measure-theoretic 层 — train-signal ($\mu_{\rm val}$) 与 test-signal ($\mu_{\rm test}$) 互奇异, 无 well-defined RN derivative, 即便数值 fit 也不构成测度识别 (P0★-F FATAL root); (III) 统计层 — 0.030 abs diff (6.76% rel) 落在 single-chain noise band ($\gtrsim0.03$) 内, 不 reject "no structural relationship" 之 $H_0$。**verdict negative**: $\tfrac12(B+C)\approx D^{\rm paper}$ 是 numerical coincidence, 非 structural identification。

**close 必要条件**: Path A (33 GPU-hour SGD EMA replay, 5060 fp32 cu130 重跑, 跨 $n$ 变化之多个 $(B,C,{\rm paper})$ 三元组 + cross-regime 排除 P0★-G) 闭合代数层 (I) 之必要 (非充分) 条件; measure-theoretic 层 (II) 之 close 须 Path D (RN 关系 severe derive)。falsifier: F-a (rank=2 后 OLS CI collapse) / F-b (构造 RN derivative) / F-c (N≥8 CI half-width <0.030) / F-d (residual structure)。

**留 D60+**: positive identification + P0★-F final close + 与 S1 frozen-regime joint close + partial identification (Manski) identified set。

**严守**: paper v8 final 47/47 + D17 + D29 三 leg + 12 NOT-claim 撤回 (不 declare structural identification / first / paradigm) + 反题 6 P0★ (P0★-F FATAL root 形式化但 tier 不升降 + P0★-A θ-space satisfied) 全 binding。0 commit / 0 push / 0 launch / 0 ssh write / 0 sub-agent。L0 是 D60+ window candidate, 不进 paper v9 spine, 留 PI + 关卡 3/4 决。本 agent 非 zero-context (caveat §0.1 disclosed), 第 5 通道独立性留反题三方决复核。
