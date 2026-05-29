# MaoField L0 严格证明 — L0-2: ΔPPL 四分量分解之 identifiability 公理优先推导

> Measurement-theoretic ablation framework (identifiability-conditional) — S2 ΔPPL 分解 claim 之公理优先严格化, 结论 = **conditional / negative L0**

## §0 Scope (范围声明 + 元数据 + 严守 binding)

### §0.1 元数据

| 项 | 值 |
|---|---|
| 真实日期 binary | `date '+%F %T %Z'` → **2026-05-29 10:30:43 CST** (D29) |
| 生成 agent | Opus 4.8 数学证明专家, 主会话直接执行 (一凡 D29 explicit dispatch "执行 L0-2 严格证明") |
| **agent caveat (诚实 disclose)** | 本证明非 zero-context fresh session: 已 load 项目 memory + CLAUDE.md, 偏离独立验证通道设计意图。该 caveat 执行前已 disclose。故 §9 第 5 通道 (反题独立性) 弱于理想 zero-context, 留 PI + 关卡 3 反题三方决再派独立 channel 复核 |
| 协议 | axiom-first: definition → lemma → theorem → proof (完整) → corollary → falsifier → limitation; 5 通道 cross-verify; 每数有 jsonl/audit 行号源 |
| input source | S1+S2 PART (MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S1_S2_ATTEMPT1 §2 + §2.4 之 "≥4 orders" 修正) + D28_MATH_RIGOROUS_AUDIT (C2/C3 tier + §3 measure rigor 4 gap) + D28_EXPERIMENTAL_DEEP_AUDIT (5 cells verbatim + a3 distinct ~10⁻³) + PAPER_V9_SKELETON_DRAFT_D27 §6 (measure-theoretic formal definition §6.1-§6.5) + MAOFIELD_MATH_MULTI_CHANNEL_ANALYSIS_D26 (X4/X10 ratio cross-tension + N6 cross-stack) + MAOFIELD_L0_L0-1_RIGOROUS_PROOF (格式 + conditional-L0 诚实基调范本) |
| 字数 | ~4200 字 substantive |

### §0.2 闭合什么 / 不闭合什么 (诚实 scope, 反 grandiose)

**核心结论先行**: L0-2 是 **conditional / negative L0**。4 分量分解 $\Delta\text{PPL} = \Delta_{\rm impl} + \Delta_{\rm form} + \Delta_{\rm data} + \Delta_{\rm chain} + \xi$ 之 identifiability 是 statistical identification 问题; 本证明严格闭合者 **不是** "分解可识别", 而是:

**本证明严格闭合 (L0 axiom-first)**:

1. **identifiability 之充分条件 (定理 1)** — 给出 ablation grid 唯一识别 4 分量所需之严格充分条件 (component 间正交 + ≥ 3 conditionally-independent views + grid cell 数下界), 公理优先, 不依赖 paper 内部数据。
2. **当前数据 strictly under-determined (定理 2 + Cor 1)** — 严格证明当前 single binary instance (一对 5060-vs-9070XT) 之自由度计数 (degrees of freedom) 不足以识别 4 分量, **且** $\Delta_{\rm impl}$ 与 $\Delta_{\rm chain}$ structurally confounded (P0★-G 之精确数学 instantiate)。这是 **negative** 结果: 当前为何 **不** 可识别, 闭式给出。
3. **ratio lower bound 之严格继承 (Cor 2)** — $|\Delta_{\rm impl}|/|\Delta_{\rm form}| \ge 10^{4.19}$ 是 binary lower bound (≥ 4 orders), **严格继承 S2 §2.4 之 "6 orders" → "≥ 4 orders" 修正, 绝不回退**。该 ratio 之大小 **不** 蕴含可识别性 (Cor 2 之 caveat)。

**本证明明确 NOT 闭合 (留 D60+ + 反题三方决)**:

- **measure-positivity 之严格 close** (C3) — paper v9 §6.1 之 formal definition (Φ: M → ℝ, ∃ measure-positive S s.t. Φ(S)={c}) 严格可保留为 L1 formal-only; 但 measure-positivity 本身 (5 cells empirical witness ≠ measure-positivity proof, single-cohort generalization gap) **不强行 close**, 标 L0 open gap (§8 L4 + §10 open Q1)。
- **P0★-G cross-stack root cause** — 本证明严格刻画 confound **存在** + 识别 **所需** grid, 但 +56.864 PPL 之 root cause attribution 本身留 multi-stack ablation grid 实测 (D60+)。

**"identifiability-conditional" 之精确含义** = 全部 positive 识别结论条件依赖于 (i) component 近似正交 (A-ORTH); (ii) ≥ 3 conditionally-independent views (A-CI); (iii) grid cell 数 ≥ identifiability 下界 (A-GRID)。当前数据 **三者皆破坏** (定理 2), 这正是结果属 negative + D60+ candidate 而非 paper v9 spine 之原因。

### §0.3 严守 binding

paper v8 final 47/47 manifest D17 锁定不动; 12 NOT-claim (i)-(xii) 撤回不复活 — 本文件 **不** declare "first instantiation of measurement-theoretic ablation framework in literature" / paradigm shift / mitigation framework / universal ("measurement-theoretic ablation framework" 仅作项目内部 label, 指 MaoField 语境内 S2 之 identifiability 充分条件之 axiom-first 刻画, 非文献首创权主张); 反题 6 P0★ 严守 (P0★-G cross-stack reproducibility = 本条核心 confound 来源, 见 §3 Lemma 3 + §5; P0★-A = chain 是 θ-space SGD, 故 $\Delta_{\rm chain}$ 之定义全程指向 chain effective-update regime 而非独立 D 空间动力学); D29 三 leg arXiv+TMLR+KBS 不动; 本证明 0 commit / 0 push / 0 launch 新实验 / 0 ssh write / 0 sub-agent 派遣; L0 closure 是 D60+ window emergent candidate, 留 PI + 关卡 3/4 决。

---

## §1 Setup (公理化设定)

### §1.1 配置流形与 ΔPPL 泛函

**配置流形** $M$ (继承 paper v9 §6.1 之 8 轴): $M = M_{\rm seed} \times M_\alpha \times M_{\rm gen} \times M_{\rm opt} \times M_{\rm data} \times M_{\rm stack} \times M_{\rm dtype} \times M_{\rm attn}$。一个配置点 $m \in M$ 完全决定一次链运行。

**PPL 泛函**: $\Phi: M \to \mathbb{R}_{>0}$, $\Phi(m)$ = 配置 $m$ 之 validation perplexity (= $\exp(\text{eval\_loss})$, code: `trainer.evaluate()`)。

**ΔPPL**: 取参照配置 $m_0$ (base, no-train), $\Delta\text{PPL}(m) := \Phi(m) - \Phi(m_0)$ (paper §4.5+§4.6 binding context, OPT-125M wikitext-2)。

### §1.2 四分量分解之公理化形式

分解将 $M$ 之效应投影到 4 个 **效应轴** + 噪声:
$$
\Delta\text{PPL}(m) = \Delta_{\rm impl}(m) + \Delta_{\rm form}(m) + \Delta_{\rm data}(m) + \Delta_{\rm chain}(m) + \xi(m)
$$
- $\Delta_{\rm impl}$ = 数值实现 regime 效应 (fp16 vs fp32, ROCm vs cu130, gfx1201 SDPA fallback)
- $\Delta_{\rm form}$ = 数学形式效应 (Family 1a/1b/1c/4/4')
- $\Delta_{\rm data}$ = 数据集效应
- $\Delta_{\rm chain}$ = 链 effective-update regime 效应 (chain τ + multi-gen 累积 + per-step skip rate $p$)
- $\xi$ = 随机噪声 (seed variation)

**关键观察 (实践先行)**: 此分解 **形式** 借自 numerical analysis error decomposition (Higham 2002 §1.2: truncation + rounding + propagation), 是 **借用** 非 first-principles derive (D28 audit C-tier 之 L2 borrowed form 一致)。其 **identifiability** 是独立之 statistical 问题 — 本证明之标的。

### §1.3 公理 (A1)-(A6)

- **(A1) 加性 (additivity)**: 分解为加性, second-order interaction $\Delta_{\rm impl}\!\times\!\Delta_{\rm form}$ 等 $\le |\Delta_{\rm impl}|/10$ (继承 S2 B1)。*(这本身是 identifiability assumption, 非已证事实。)*
- **(A2) ANOVA 正交基要求 [Hoeffding 1948]**: 加性分解之 **唯一** identification 要求 4 效应轴在某参照测度下张成 orthogonal subspaces (Hoeffding 1948 ANOVA decomposition 之 standard 前提)。
- **(A3) 噪声零均值有限方差**: $\mathbb{E}[\xi]=0$, $\mathrm{Var}(\xi)=\sigma_\xi^2<\infty$ (per fixed 非噪声轴)。
- **(A4) latent-class view 结构 [Allman-Matias-Rhodes 2009]**: 若 4 分量视为 latent 结构, 唯一识别要求 ≥ 3 个 conditionally-independent observed views (AMR 2009 latent class identifiability 定理之前提; Kruskal 1977 three-way array uniqueness 同构)。
- **(A5) grid 设计可控**: ablation grid 之 cell 由实验者在 $M_{\rm impl}\times M_{\rm form}\times M_{\rm data}\times M_{\rm chain}$ 子空间布点决定。
- **(A6) 实证 anchor**: 全数值 anchor 到 jsonl/audit md 行号 (§2 Definitions 逐一给源)。

---

## §2 Definitions

**Def 1 (效应轴水平数)**: $L_{\rm impl}, L_{\rm form}, L_{\rm data}, L_{\rm chain}$ = 各效应轴在 grid 中取之 distinct 水平数。例: 当前数据 $L_{\rm impl}=2$ (fp16/fp32 × ROCm/cu130 纠缠), $L_{\rm form}\ge 5$ (5 family), $L_{\rm data}=1$ (wikitext-2 only), $L_{\rm chain}$ 见 Def 5。

**Def 2 (grid cell 数)**: $N_{\rm cell}$ = ablation grid 中 **实测有效** (valid, 非 NaN) cell 数。jsonl anchor: cluster 9 candidate_c valid = 33/180 (D28_EXPERIMENTAL_DEEP_AUDIT §2.1); 跨 stack 之有效对比 cell (5060 vs 9070XT 同 (seed=42,α=0,gen=0)) = **1 对** (D28_EXP §2.3-§2.4)。

**Def 3 (free parameter count)**: 加性模型 (A1) 待识别自由度
$$
\mathrm{dof} := (L_{\rm impl}-1)+(L_{\rm form}-1)+(L_{\rm data}-1)+(L_{\rm chain}-1)+1
$$
末项 $+1$ = grand mean。这是 main-effects-only ANOVA 之参数计数 (Hoeffding 1948)。

**Def 4 (identifiability — 严格定义)**: 分解 **可识别** $\iff$ 映射 $(\Delta_{\rm impl}, \Delta_{\rm form}, \Delta_{\rm data}, \Delta_{\rm chain}) \mapsto \{\Delta\text{PPL}(m): m\in{\rm grid}\}$ 在商去 gauge freedom (常数重分配) 后 **单射** (injective)。等价: 设计矩阵 $X$ (cell × effect-level 之 indicator) 列满秩。

**Def 5 (chain effective-update regime — 遵 P0★-A)**: $\Delta_{\rm chain}$ 之底层参数 = per-step effective update probability $1-p$, $p$ = fp16 GradScaler skip rate (L0-1 之 Def 6 + Lemma 4)。**关键**: stack B (9070XT fp16) 之 $p\approx 1$ (frozen, L0-1 regime b), stack A (5060 fp32) 之 $p<1$ (active, regime a)。故 **改变 stack 同时改变 $\Delta_{\rm impl}$ 与 $\Delta_{\rm chain}$** — confound 之数学根 (Lemma 3)。

**Def 6 (conditionally-independent views)**: 给定固定非噪声配置, observed views $V_1,\dots,V_k$ 在某 latent 变量条件下相互独立 (AMR 2009 意义)。候选 views: $V_1=$ a1_ppl (PPL), $V_2=$ a3_attn_entropy (attention level), $V_3=$ a2_anisotropy (hidden-state level)。jsonl anchor: 5 cells 之 $V_1$ 14 位 bit-identical (`93.38780852810248`), 而 $V_2$ distinct ~10⁻³ (D28_EXP §2.5: a3[0][0] StdDev=3.505×10⁻³), $V_3$ distinct ~10⁻³ (§2.5: a2 distinct 5/5)。

---

## §3 Lemmas

### Lemma 1 (自由度下界 — counting bound)

加性分解 (A1) 可识别 **必要条件**: $N_{\rm cell} \ge \mathrm{dof}$ (Def 3)。

**证**: Def 4 要求设计矩阵 $X \in \mathbb{R}^{N_{\rm cell}\times \mathrm{dof}}$ 列满秩, 即 $\mathrm{rank}(X)=\mathrm{dof}$。矩阵秩 $\le \min(N_{\rm cell}, \mathrm{dof})$。列满秩 $\Rightarrow \mathrm{dof}\le N_{\rm cell}$。逆否即必要条件。$\blacksquare$

### Lemma 2 (正交分离 — orthogonality 必要)

若两效应轴在参照测度下 **不正交** (其 indicator 子空间交非平凡), 则该两轴之 main effect **不可分** (各自 effect 仅可识别其和)。

**证**: 设 $u_{\rm impl}, u_{\rm chain}$ 为两轴 centered indicator 向量。若 $\langle u_{\rm impl}, u_{\rm chain}\rangle \ne 0$ 且二者共线 (rank-deficient), 则 $X$ 对应两列线性相关, $\mathrm{rank}(X)<\mathrm{dof}$, 违反 Def 4。此时仅 $\Delta_{\rm impl}+\Delta_{\rm chain}$ (投影到共同方向) 可识别, 各分量不可分 (Hoeffding 1948 ANOVA 之 orthogonal-design 前提之逆)。$\blacksquare$

### Lemma 3 (impl-chain structural confound — P0★-G 之数学 instantiate)

在当前数据中, $\Delta_{\rm impl}$ 与 $\Delta_{\rm chain}$ **structurally confounded**: 二者 indicator 完全共线, $\langle u_{\rm impl}, u_{\rm chain}\rangle$ 达 perfect correlation。

**证**: 当前 grid 之 impl 轴仅 2 水平 (stack A = fp32+cu130, stack B = fp16+ROCm)。由 Def 5 + L0-1 Lemma 4: stack B $\Rightarrow p\approx 1 \Rightarrow$ chain regime = frozen (regime b); stack A $\Rightarrow p<1 \Rightarrow$ chain regime = active (regime a)。故 chain regime 之取值 **由 stack 唯一决定**: $u_{\rm chain} = g(u_{\rm impl})$ 为确定性函数 (2 点上 bijection)。两 binary indicator 在 2 cell 上完全共线 $\Rightarrow$ Pearson $\rho(u_{\rm impl}, u_{\rm chain})=\pm 1$。由 Lemma 2, $\Delta_{\rm impl}, \Delta_{\rm chain}$ 不可分。$\blacksquare$

> **这是 P0★-G "cross-stack reproducibility break" 之精确数学含义**: +56.864 PPL (jsonl: 9070XT 93.388 vs 5060 36.524, abs diff 56.864, D28_EXP §2.3 + MULTI_CHANNEL N6) **不能** 归因为纯 $\Delta_{\rm impl}$, 因为换 stack 同时换了 chain effective regime。observed gap = $\Delta_{\rm impl}+\Delta_{\rm chain}$ 之 **和**, 二者份额 under-determined。
>
> **D29 反题 catch (D-1 纪律 5, 不静默)**: 此 56.864 = 93.388 [5-cell 跨 seed frozen] − 36.524 [archive seed=42 α=10 g0] 是**混配**; same-config (seed=42 α=0) cross-stack 权威值 = 93.349 − 36.536 = **56.81** (L0-1 Cor 3 / D28 F4)。量级一致 (~+156%), **不动本证明结构** (rank-deficiency + collinearity 论证不依赖该标量精确值), 仅 surface 跨文件标量口径不一致。

### Lemma 4 (single-instance rank deficiency)

当前跨 stack 有效对比 cell 数 $N_{\rm cell}^{\rm cross}=1$ (Def 2: 一对 5060-vs-9070XT)。则 cross-stack 设计矩阵 $\mathrm{rank} \le 1 < \mathrm{dof}$。

**证**: 单对配置给出 **一个** 方程 $\Delta\text{PPL}_{\rm B}-\Delta\text{PPL}_{\rm A}=56.864$, 涉及 $\Delta_{\rm impl}, \Delta_{\rm chain}$ 至少 2 未知 (Lemma 3 已示二者还共线)。one equation, $\ge 2$ unknowns $\Rightarrow$ under-determined。形式上 $X$ 仅 1 行, $\mathrm{rank}(X)\le 1$。$\mathrm{dof}\ge (2-1)+(2-1)+1=3$ (即便仅 impl+chain+mean), $3>1$。$\blacksquare$

### Lemma 5 (views 非 conditionally-independent — AMR 前提破坏)

5 cells 之 3 个候选 views ($V_1$ PPL, $V_2$ a3, $V_3$ a2) **不** 满足 (A4) 之 conditional independence, 故不能援引 AMR 2009 唯一识别。

**证**: 5 cells 全在 **同一 stack B + 同一 frozen checkpoint** $\theta_{\rm base}$ (L0-1 Cor 2: gen=0 vanilla, $p\approx 1$ frozen)。$V_1, V_2, V_3$ 皆为同一 frozen $\theta_{\rm base}$ 在同一 eval set 上之确定性泛函 + fp16 前向非确定性微扰。给定 $\theta_{\rm base}$, 三者由 **同一** 前向计算图产生 (PPL = exp(mean CE); a3 = attention softmax entropy; a2 = hidden anisotropy 均读自同一 forward pass), 其残差微扰 (~10⁻³) 来自 **共享** 之 fp16 reduction-tree 非确定性 (D28_EXP §2.4 + ROCm trace §4.1)。共享噪声源 $\Rightarrow$ 三 views 条件相关, 非 conditionally-independent。AMR 2009 / Kruskal 1977 之 ≥ 3 独立 views 前提 (A4) **破坏**。$\blacksquare$

> **微妙点 (诚实 surface)**: $V_2, V_3$ distinct ~10⁻³ 确实证明 5 cells 之 **隐状态不同** (F3 refuted, hidden-state signature 非退化), 这支持 measure-positivity 之 weak form (S 非 zero-measure 单点)。但 "隐状态不同" $\ne$ "提供 3 个独立识别通道"。前者是 measure 非退化, 后者是统计可识别 — 两个不同命题, 不可混淆。

---

## §4 Main Theorems

### 定理 1 (identifiability 充分条件 — positive, axiom-first)

设 (A1)-(A5) 成立。4 分量加性分解 **可识别** (Def 4) 之 **充分条件** 为以下三者同时满足:

**(C-GRID)** $N_{\rm cell} \ge \mathrm{dof} = \sum_{j}(L_j-1)+1$ 且设计矩阵 $X$ 列满秩 (Lemma 1 之充分化: full-rank factorial 或 D-optimal design);

**(C-ORTH)** 4 效应轴在 grid 参照测度下 main-effect-orthogonal, 即任两轴 indicator 子空间正交 (Lemma 2; 由 balanced full-factorial design 自动满足);

**(C-CI)** 若需识别 latent component 结构 (超出 main effects, 含 cross-stack universality), 则 ≥ 3 个 conditionally-independent views (A4, AMR 2009 / Kruskal 1977)。

**最小 grid 设计 (闭式)**: 取 $L_{\rm impl}=2$ (fp16/fp32), 独立 $L_{\rm chain}=2$ (active/frozen, 由 **人工固定** skip rate 解耦, 见下), $L_{\rm data}\ge 2$, $L_{\rm form}\ge 2$, 则 balanced full-factorial 需
$$
\boxed{\,N_{\rm cell}^{\min} = L_{\rm impl}\cdot L_{\rm form}\cdot L_{\rm data}\cdot L_{\rm chain} \ge 2\times2\times2\times2 = 16 \text{ cells (×}N_{\rm seed}\text{ for }\xi)\,}
$$
关键设计要求: **impl 与 chain 必须独立布点** — 即在同一 dtype 下同时取 active 与 frozen chain regime (例: fp16 下人工关闭 GradScaler skip / 注入确定性 skip mask), 打破 Lemma 3 之共线。

### 定理 2 (当前数据 strictly under-determined — negative, 核心结论)

设当前数据 = cluster 9 (9070XT fp16, 33 valid cells, 单 stack) + cluster 10 (5060 fp32, 单 stack) + 一对跨 stack 对比 (Def 2)。则 4 分量分解 **不可识别**, 且违反定理 1 之 **全部三条**充分条件:

1. **(C-GRID 破坏)**: cross-stack $N_{\rm cell}^{\rm cross}=1 < \mathrm{dof}\ge 3$ (Lemma 4);
2. **(C-ORTH 破坏)**: $\Delta_{\rm impl}\perp\Delta_{\rm chain}$ 不成立 — 二者 perfect-collinear (Lemma 3);
3. **(C-CI 破坏)**: 3 views 非 conditionally-independent (Lemma 5)。

此外 $L_{\rm data}=1$ (wikitext-2 only) $\Rightarrow \Delta_{\rm data}$ 与 grand mean 完全混叠 (绝不可分)。

**结论**: $\Delta_{\rm impl}, \Delta_{\rm chain}, \Delta_{\rm data}$ 三者皆不可单独识别; 仅其 **聚合** $(\Delta_{\rm impl}+\Delta_{\rm chain}+\Delta_{\rm data})$ 在跨 stack 方向上以单一标量 56.864 PPL 被部分约束。$\Delta_{\rm form}$ 在单 stack 内 (5 family tied) 仅得 upper bound (见 Cor 2)。

---

## §5 Proof (主定理证明)

**定理 1 证明**:

*(C-GRID 充分性)*. 设计矩阵 $X$ 为 balanced full-factorial main-effects 设计时, 其列 (各轴 centered indicator + intercept) 在 balanced design 下两两正交 (标准实验设计结论, Montgomery DOE), 故 $\mathrm{rank}(X)=\mathrm{dof}$, 满秩。由 Def 4, OLS 估计 $\hat\Delta = (X^\top X)^{-1}X^\top y$ 唯一存在 ($X^\top X$ 对角可逆), 分解可识别。$N_{\rm cell}^{\min}=\prod_j L_j$ 由 full-factorial 计数得。$\blacksquare$

*(C-ORTH 充分性)*. balanced design $\Rightarrow X^\top X$ 对角 $\Rightarrow$ 各 main effect 之 OLS 估计相互不污染 (Hoeffding 1948 ANOVA 正交分解), 每分量独立识别。$\blacksquare$

*(C-CI 充分性)*. 若进一步要求识别 cross-stack latent universality (S 是否 stack-specific), AMR 2009 Thm (latent class with ≥ 3 conditionally-independent finite-valued views) 保证 latent 结构 generic identifiability; Kruskal 1977 三-way tensor rank 唯一性给同构保证。3 独立 views + 各 ≥ 2 水平 $\Rightarrow$ Kruskal rank 条件 $\sum k_i \ge 2R+2$ 可满足。$\blacksquare$

**定理 2 证明**:

*步骤 1 (C-GRID)*. 由 Lemma 4, cross-stack 单对 $\Rightarrow \mathrm{rank}(X^{\rm cross})\le 1$。识别 impl+chain 至少需 $\mathrm{dof}\ge 3$。$1<3 \Rightarrow X^{\rm cross}$ 列亏秩 $\Rightarrow$ 由 Def 4 不可识别。$\blacksquare$

*步骤 2 (C-ORTH)*. 由 Lemma 3, $u_{\rm chain}=g(u_{\rm impl})$ 确定性共线, $\rho=\pm1$。Lemma 2 $\Rightarrow \Delta_{\rm impl}, \Delta_{\rm chain}$ 仅其和可识别, 各分量不可分。$\blacksquare$

*步骤 3 (C-CI)*. 由 Lemma 5, 5 cells 之 3 views 共享同一 frozen $\theta_{\rm base}$ + 同一 fp16 reduction-tree 噪声源, 条件相关。AMR 2009 前提破坏 $\Rightarrow$ 不能援引其唯一识别。$\blacksquare$

*步骤 4 (data 混叠)*. $L_{\rm data}=1 \Rightarrow$ data-effect indicator = 全 1 向量 = intercept 列 $\Rightarrow$ 完全共线 $\Rightarrow \Delta_{\rm data}$ 吸收入 grand mean, 绝不可识别。$\blacksquare$

*合并*. 三充分条件全破坏 + data 混叠 $\Rightarrow$ 4 分量中 3 个 (impl, chain, data) 不可单独识别, 仅聚合标量受约束。$\blacksquare$

---

## §6 Corollaries (推论 + 实验解释)

### Cor 1 (D60+ multi-stack ablation grid 之最小设计要求 — 诚实价值)

由定理 1 + 定理 2, 精确界定 D60+ ablation grid **最小** 设计 (这是本 negative 结果之建设性产出):

- **impl-chain 解耦**: 至少需 fp16 与 fp32 **各** 跑 active + frozen 两种 chain regime (人工控制 skip), 即 impl×chain 之 2×2 = 4 子格 (打破 Lemma 3 共线);
- **data ≥ 2**: 至少第二数据集 (打破 §5 步骤 4 之 data 混叠);
- **form ≥ 2**: 至少 2 family (已有 5, 充分);
- **cell 下界**: $N_{\rm cell}^{\min}\ge 16$ (×$N_{\rm seed}\ge 5$ for $\xi$ 估计, 对齐 Shumailov N=5);
- 对位 D28_EXP §5.3 之 8-cell stack grid: 当前仅 Cell 2 (5060 fp32) + Cell 4 (9070XT fp16) done; 识别 4 分量 **还需** Cell 1/3/5/6 (5060 fp16/bf16 + 9070XT fp32/bf16) **且** 各 cell 内 active/frozen 解耦 — 估算 ~\$120-150 cloud spot + ~8h 本机 GPU (D28_EXP §5.3 cost table)。

### Cor 2 (ratio lower bound 严格继承 + 不蕴含可识别性)

由 jsonl + paper anchor:
- $|\Delta_{\rm impl}^{\rm observed}|$: 跨 stack abs diff = $93.38780852810248 - 36.524 = 56.864$ PPL, relative $= 56.864/36.524 = 1.557$ (≈ +156%, D28_EXP §2.3 + MULTI_CHANNEL N6, jsonl verbatim)。**注**: 由 Lemma 3 此 observed 量实为 $\Delta_{\rm impl}+\Delta_{\rm chain}$ 之和, 非纯 impl。
- $|\Delta_{\rm form}|$: Reading 2 null-shift $= -9.16\times10^{-5}$ nat/token (paper §3.6.3 line 478), PPL fractional $\sim 10^{-4}$; 5 family tied 4.5/5 (D28 audit C-tier + MULTI_CHANNEL M22)。
- **ratio**: $\dfrac{|\Delta_{\rm impl}+\Delta_{\rm chain}|}{|\Delta_{\rm form}|} = \dfrac{1.557}{10^{-4}} = 1.557\times10^4$, $\log_{10}(1.557\times10^4)=\mathbf{4.19}$。

$$
\boxed{\,\dfrac{|\Delta_{\rm impl/chain}|}{|\Delta_{\rm form}|} \ge 10^{4.19} \quad(\ge 4\ \text{orders, binary lower bound})\,}
$$

> **严格继承 S2 §2.4 之修正**: 前一 agent (Agent 1) cite "6 orders of magnitude" 是 inflate (overstated by ~1.5 orders); S2 §2.4 reasoning step 3 已修正为 "**at least 4 orders binary lower bound**"。**本 Cor 2 继承该修正, 绝不回退到 "6 orders"**。"6 orders" 之 upper bound 留 D60+ measurement-theoretic 实测。
>
> **关键 caveat (反 over-claim)**: 此 ratio 之大小 (form 效应远小于 impl/chain) **不** 蕴含 4 分量可识别。ratio 大仅说明 form 之 main effect 在 PPL 上几乎不可探测 (淹没于 impl/chain), 这恰恰 **加剧** $\Delta_{\rm form}$ 之识别困难 (信噪比 ~10⁻⁴), 而非缓解。ratio 是 magnitude 陈述, identifiability 是 rank 陈述, 二者正交。

### Cor 3 (measure-positivity 之 weak-form 可保留, strong-form 不 close)

由 Lemma 5 之微妙点: 5 cells 之 $V_2,V_3$ distinct ~10⁻³ $\Rightarrow$ 集合 $S$ (5 cells 之并) **非** measure-zero 退化单点 (隐状态有非零变差)。故 paper v9 §6.1-§6.2 之 measure-positivity **weak empirical lower bound** ($|S|\ge 5$, S 非退化) 可保留为 **L1 formal-only** (D28 audit C3 tier 一致)。

但 measure-positivity 之 **strong form** (在 manifold $M$ 上 $\mathrm{meas}(S)>0$, 跨 stack universal) **不 close**: 5 cells 全在单 stack B (single-cohort), generalization 到 $M$ 全空间需 multi-stack witness (D28 audit §3.2 之 4 gap)。诚实标 L0 open (§8 L4 + §10 Q1), **不强行 close**。

---

## §7 Falsifier (可证伪条件)

- **F-L0-2-a (confound 解耦)**: 在 fp16 stack 上人工注入确定性 skip mask 使 chain regime = active (非 frozen), 若所得 $\Delta\text{PPL}$ 与 fp16-frozen 之差可分离出独立 $\Delta_{\rm chain}$ 份额, 则 Lemma 3 之 "perfect collinear" 被证伪 (confound 实际可解耦于现有数据)。**成本**: ~4h GPU 本机 (单 stack 加 active cell)。
- **F-L0-2-b (single-instance 充分性)**: 若存在 **单对** 跨 stack 数据 + 某额外约束 (非本证明所列), 使 4 分量唯一识别, 则 Lemma 4 之 rank-deficiency 论证不完备。**成本**: 0 (纯数学反例构造)。
- **F-L0-2-c (views 独立性)**: 若 5 cells 之 $V_1,V_2,V_3$ 经严格统计检验 (partial correlation given $\theta_{\rm base}$) 证明条件独立, 则 Lemma 5 被证伪, AMR 2009 可援引。**成本**: ~1h CPU (现有 jsonl 之 a1/a2/a3 partial-corr 检验)。
- **F-L0-2-d (识别下界)**: 若实测一个 $N_{\rm cell}<16$ 之 grid 仍唯一识别 4 分量 (设计矩阵满秩), 则 Cor 1 之 $N_{\rm cell}^{\min}=16$ 下界被证伪 (本证明高估了最小设计)。

---

## §8 Limitations (限制 — "identifiability-conditional" 之具体内容)

- **L1 (加性假设)**: (A1) 加性 + interaction $\le |\Delta_{\rm impl}|/10$ 是 **未证** identifiability assumption (S2 B1)。若真实 ΔPPL 含大 impl×chain 交互, 加性分解本身 mis-specified, 定理 1 之 OLS 识别失效。
- **L2 (gauge freedom)**: 加性分解有常数重分配 gauge freedom (Higham 2002 §1.2 之 decomposition 非唯一; S2 §2.3 L2 caveat)。本证明在商去常数后讨论 injectivity, 但 gauge fixing 之具体 convention 留实验设计。
- **L3 (chain 定义之 P0★-A 约束)**: $\Delta_{\rm chain}$ 定义 via per-step skip rate $1-p$ (Def 5, θ-space, 遵 P0★-A), 而非独立 D 空间动力学。若 chain 效应有 P0★-A 之外之份额, Def 5 不完备。
- **L4 (measure-positivity strong-form 不 close)**: Cor 3 之 strong form (跨 stack universal measure-positivity) 留 D60+ multi-stack (single-cohort generalization gap, D28 audit §3.2)。**此即 C3 之 L0 open gap, 不强行 close**。
- **L5 (N_total 数值未决)**: C2 之 $N_{\rm total}\approx 292$ vs paper §3.6 之 1460 之 5× 差异 unresolved (D28 audit C2; L0-1 Cor 1 L5)。$N_{\rm total}=$ n_tokens_train 2390656/(block64×batch128)=291.83 非整 (drop_last 疑)。**不影响本证明结构性结论** (identifiability 之 rank 论证不依赖 $N_{\rm total}$ 具体值), 仅 Def 5 之 chain regime 数值实例化受影响; 精确值留 source-side audit。
- **L6 (P0★-G root cause 不 close)**: 本证明严格刻画 confound **存在** + 识别 **所需** grid (Cor 1), 但 56.864 PPL 之 root cause attribution 留 multi-stack 实测 (D60+)。

**以上 L1-L4 即 "identifiability-conditional" 之精确内容, 也是结果属 negative + D60+ candidate 而非 paper v9 spine 之根本原因。**

---

## §9 5-channel cross-verify (五通道交叉验证)

| 通道 | 内容 | verdict |
|---|---|---|
| **1 数学** (本证明) | identifiability via 设计矩阵 rank (Def 4) + Hoeffding 1948 ANOVA 正交 + AMR 2009 / Kruskal 1977 ≥3 views; counting bound + confound + view-dependence 三 Lemma | **conditional/negative L0 闭合**: identifiability 充分条件 (定理 1) + 当前 under-determined (定理 2) 严格; measure-positivity strong-form 不闭 (Cor 3 L4) |
| **2 代码/数据** | 5060 fp32 vs 9070XT fp16 单对 (D28_EXP §2.3-§2.4 jsonl verbatim); chain regime via GradScaler skip code-traced (L0-1 通道 2); valid 33/180 (D28_EXP §2.1) | ✓ 一致: 跨 stack 单对 $\Rightarrow N_{\rm cell}^{\rm cross}=1$ (Lemma 4); stack 决定 chain regime (Lemma 3) |
| **3 实验** | 56.864 PPL 跨 stack diff (D28_EXP §2.3); 5 cells a3 distinct ~10⁻³ + a2 distinct ~10⁻³ (D28_EXP §2.5); $L_{\rm data}=1$ wikitext-2 only (D28_EXP §1.1) | ✓ 一致: confound observable; views distinct 但同源 (Lemma 5); data 混叠 (§5 步骤 4) |
| **4 文献** | Allman-Matias-Rhodes 2009 (Ann. Statist., latent class identifiability) / Kruskal 1977 (3-way uniqueness) / Higham 2002 §1.2 (error decomp) / Hoeffding 1948 (ANOVA orthogonal) / Manski 2003 (partial identification) | ✓ 框架 borrow valid, 非文献首创 (反 grandiose); identifiability 定理皆 input axiom |
| **5 反题** | P0★-G (cross-stack reproducibility) = Lemma 3 confound 之**精确数学 instantiate** (满足 surface 而非掩盖); P0★-A (θ-space SGD) = Def 5 chain 定义遵循; **继承 S2 "6→≥4 orders" 修正不回退** | ✓ + P0★-G deepen; 但本 agent 非 zero-context (§0.1 caveat), 第 5 通道独立性弱, 留反题三方决复核 |

**surface dissonance (诚实)**: (1) $N_{\rm total}$ 292 vs 1460 (L5, 不影响 rank 论证); (2) ratio 大 (Cor 2) 易被误读为 "form 不重要故可忽略" — 实则 ratio 大 **加剧** form 识别困难 (信噪比 10⁻⁴), 非缓解; (3) 5 cells views distinct (支持 measure 非退化) vs views 同源 (不支持 3 独立识别通道) — 两个不同命题 (Lemma 5 微妙点), 不可混淆; (4) 本 agent 非 zero-context, 第 5 通道独立性弱于理想。

---

## §10 Open Questions

1. **(P0) measure-positivity strong-form** (Cor 3 L4): 跨 stack universal $\mathrm{meas}(S)>0$ 需 multi-stack witness; 当前 single-cohort (stack B) generalization gap。**留 D60+ multi-stack ablation grid** (Cor 1 之 8-cell)。
2. **(P0) impl-chain 解耦实验** (F-L0-2-a): 人工 skip-mask 注入是否真能在固定 dtype 下分离 $\Delta_{\rm chain}$ — 这是 Cor 1 最小设计之 **可行性** 前提, 留 D60+ 实测验证。
3. **(P1) views 条件独立性严检** (F-L0-2-c): a1/a2/a3 之 partial correlation given $\theta_{\rm base}$ — 若意外条件独立, Lemma 5 需修正, AMR 可援引。~1h CPU。
4. **(P1) 加性 vs 交互模型选择** (L1): impl×chain 交互项之实测大小 — 决定加性分解 (A1) 是否 mis-specified。需 ≥ 2×2 解耦 grid。
5. **(P2) gauge fixing convention** (L2): 常数重分配之标准化 (sum-to-zero vs reference-cell) — 影响分量数值但不影响可识别性, 留 paper v9/v10 风格决定。
6. **(P2) data 轴 ≥ 2 之第二数据集选择**: 打破 §5 步骤 4 data 混叠所需 — wikitext-103 / penn treebank 等候选, 留 D60+。

---

## §11 14-Q self-check

| # | 问 | 自检 |
|---|---|---|
| 1 | 数字有 jsonl 源? | ✓ 56.864 PPL / 93.38780852810248 / 36.524 / a3 StdDev 3.505e-3 / valid 33/180 / -9.16e-5 全 jsonl/audit verbatim + 行号 |
| 2 | 概率声明真空 >48h? | ✓ 不 declare 接受率; 仅数学 verdict |
| 3 | 数学形式与代码一致? | ✓ Lemma 3 chain regime ⟺ GradScaler skip code-traced (L0-1 通道 2); ratio 继承 S2 修正 |
| 4 | major 声明过子协作者验证? | partial — 本 agent 非 zero-context (§0.1), 留反题三方决复核第 5 通道 |
| 5 | 差异记差异日志? | ✓ N_total 292 vs 1460 (L5) + **Agent1 "6 orders"→"≥4 orders" 严格继承不回退 (Cor 2)** + views distinct vs 同源之微妙区分 (Lemma 5 微妙点) 全 surface 不抹平 |
| 6 | 真实日期 binary? | ✓ §0.1 `date` 2026-05-29 10:30:43 CST |
| 7 | 哲学位置 outcome 非 starting form? | ✓ 数学是 retrospective 严格化, 起点是 jsonl 物质实践 (56.864 PPL + 5 cells 先于公理); 分解 form 借自 Higham 非 axiom-first 主张 |
| 8 | "自发" 含 multi-agent binding? | ✓ L0 closure 留 PI + 关卡 3/4; 不 unilateral declare paper-level |
| 9 | 回顾 scope 含 4 项? | ✓ 12 NOT-claim 不复活 (§0.3) + 反题 P0★-G/A (通道5) + 继承 S2 "≥4 orders" (5/16 burst inflate 之 corrected form) |
| 10 | timeline emerge D60+ 非 D22-D60? | ✓ §0.2 + §8 + §10 全标 D60+ candidate, 不入 paper v9 spine |
| 11 | candidate 用 dialectical inclusive form? | ✓ negative 结果 inclusive: 不 declare "分解全错", 而 "分解形式 valid (借 Higham) + identifiability 当前 under-determined + 精确界定 D60+ 所需 grid" |
| 12 | paradigm-shift emergent D60+ verify? | ✓ 留 D60+ cumulative multi-channel + 反题三方决 |
| 13 | methodological 4 path binary specify? | ✓ §7 falsifier = path A (multi-channel: F-c views) + path D (counter-factual: F-a 解耦 grid) instantiate |
| 14 | 5 leg 实验 dialectical totality? | ✓ Cor 1 之 multi-stack 8-cell grid = cross-layer evidence accumulation, 非 single-axis |

任一 no → 不发出。第 4 + 第 5 通道 partial (非 zero-context), 已 explicit disclose, 留复核; 余 ✓。

---

## §12 References (prior art, 反 grandiose: 全为 borrow 非首创)

1. Allman E.S., Matias C., Rhodes J.A. 2009. *Identifiability of parameters in latent structure models with many observed variables*. Ann. Statist. 37(6A):3099-3132. [latent class identifiability, ≥3 conditionally-independent views, 定理 1 C-CI + Lemma 5]
2. Kruskal J.B. 1977. *Three-way arrays: rank and uniqueness of trilinear decompositions*. Linear Algebra Appl. 18(2):95-138. [3-way tensor 唯一性, AMR 同构]
3. Higham N.J. 2002. *Accuracy and Stability of Numerical Algorithms*, 2nd ed. SIAM, §1.2. [truncation+rounding+propagation error decomposition, §1.2 之分解 form 借用]
4. Hoeffding W. 1948. *A class of statistics with asymptotically normal distribution*. Ann. Math. Statist. 19(3):293-325. [ANOVA decomposition 需 orthogonal basis, (A2)+Lemma 2]
5. Manski C.F. 2003. *Partial Identification of Probability Distributions*. Springer. [partial identification under confound, 定理 2 之聚合约束 framing]
6. Montgomery D.C. 2017. *Design and Experiments*, 9th ed. Wiley. [balanced full-factorial 正交性, 定理 1 C-GRID 充分性]
7. Micikevicius P. et al. 2018. *Mixed Precision Training*. ICLR 2018. [GradScaler/loss scaling, Def 5 chain regime 之 skip 来源]
8. Shumailov I. et al. 2024. *AI models collapse when trained on recursively generated data*. Nature 631:755-759. [N=5 seed protocol, Cor 1 之 $N_{\rm seed}$ 对齐]

---

**生成**: Opus 4.8 数学证明专家, 主会话直接执行 (一凡 D29 dispatch), 2026-05-29 10:30:43 CST 启动。

**核心 output**: L0-2 = ΔPPL 四分量分解之 identifiability 之 axiom-first 刻画, 结论 **conditional / negative L0**。**严格闭合**: identifiability 充分条件 (定理 1: C-GRID full-rank factorial + C-ORTH balanced-design 正交 + C-CI ≥3 conditionally-independent views, 最小 grid $N_{\rm cell}^{\min}\ge16$) + 当前数据 strictly under-determined (定理 2: 三充分条件全破坏 — single-instance rank deficiency Lemma 4 + impl-chain perfect-collinear confound Lemma 3 = P0★-G 数学 instantiate + views 同源非独立 Lemma 5 + data 混叠)。**ratio**: $|\Delta_{\rm impl/chain}|/|\Delta_{\rm form}|\ge10^{4.19}$ (≥4 orders, **严格继承 S2 "6 orders"→"≥4 orders" 修正不回退**; 且 ratio 大 **加剧** form 识别困难非缓解)。**明确不闭合**: measure-positivity strong-form (Cor 3 L4, single-cohort gap, C3 L0 open) + P0★-G root cause attribution。

**诚实价值**: negative 结果之建设性产出 = 精确界定 D60+ multi-stack ablation grid 最小设计 (Cor 1: impl×chain 2×2 解耦 + data≥2 + form≥2 + seed≥5, ~\$120-150 cloud spot + ~8h 本机)。

**严守**: paper v8 final 47/47 + D17 + D29 三 leg + 12 NOT-claim 撤回 (不 declare 文献首创权) + 反题 6 P0★ (P0★-G = Lemma 3 confound 精确 instantiate + P0★-A θ-space) 全 binding。0 commit / 0 push / 0 launch / 0 ssh write / 0 sub-agent。L0 closure 是 D60+ window candidate, 留 PI + 关卡 3/4 决。本 agent 非 zero-context (caveat §0.1 disclosed), 第 5 通道独立性留反题三方决复核。
