# MaoField L0 严格证明 — L0-3: 5-mode failure taxonomy 的 regime distinctness + transition kernel 性质

> Banach LLM (numerical-stability-conditional) — S4 PART 的 5-mode taxonomy 之 axiom-first partial 严格化: regime distinctness 闭 + exhaustivity 诚实 FAIL + Markov/memory partial

## §0 Scope (范围声明 + 元数据 + 严守 binding)

### §0.1 元数据

| 项 | 值 |
|---|---|
| 真实日期 binary | `date '+%F %T %Z'` → **2026-05-29 10:32 CST** (D29) |
| 生成 agent | Opus 数学证明 specialist, zero-context 派遣 (一凡 D29 explicit dispatch "执行 L0-3 严格证明") |
| **agent caveat (诚实 disclose)** | 本证明非完全 zero-context fresh session: 已 load 项目 memory + CLAUDE.md (system reminder auto-inject), 偏离理想独立验证通道意图。该 caveat 已 disclose。故 §9 第 5 通道反题独立性弱于理想 zero-context, 留 PI + 关卡 3 反题三方决再派遣独立 channel 复核 |
| 协议 | axiom-first 严格推导: definition → lemma → theorem → proof → corollary → falsifier → limitation; 5 通道 cross-verify; 每数有 jsonl/code/文献源 |
| input source | S4 PART (5-mode taxonomy 原始 + A5 transition kernel) + S1_S2 PART (两态 regime 对应) + ROCM_MIOPEN_TRACE (GradScaler scale-factor 动力学 + NaN cascade) + D28_EXPERIMENTAL_DEEP_AUDIT (5 cells + seed=2024 间歇 + fp64 overflow verbatim) + MAOFIELD_L0_L0-1_RIGOROUS_PROOF (Lyapunov/Kingman/regime 写法 + 诚实 tier 范本) |
| 字数 | ~4200 字 substantive |

### §0.2 闭合什么 / 不闭合什么 (诚实 scope, 反 grandiose)

**本证明严格闭合 (L0 axiom-first)**:

1. **regime distinctness 完全闭合** — 5 mode 嵌入统一的 transition-kernel regime classification, 用 (i) Lyapunov 指数 $\lambda$ 之符号 + (ii) IEEE-754 数值边界 (fp16/fp64 overflow threshold) + (iii) Markov-switching 三个 classifier, 严格证明 5 mode 是 **pairwise distinct dynamical regime** (Thm 1)。即: 不可能两个不同 mode 是同一 regime 之不同取值 — 它们由不同 classifier 值或不同数值边界触发。

**本证明诚实判 FAIL (不可达)**:

2. **exhaustivity (穷尽性) FAIL** — 无法证明 "只有这 5 种 mode 而无第 6 种"。全 $\theta$-space ($d \approx 1.25\times 10^8$ 非凸) 之穷尽性严格不可达 (Thm 2 + L1)。**可做之弱版本**: 在受限 framework (1-D order parameter $D_n$ + bounded multiplicative noise + IEEE-754 有限精度) 内, regime 数被边界条件限制为有限类 (Lemma 5)。明确区分 "受限 framework 内有限分类 (可做)" vs "全 $\theta$-space 穷尽性 (FAIL)"。

**本证明 partial 判定 (部分可达, 完整留 D60+)**:

3. **transition kernel Markov vs memory-bearing — PARTIAL** — 用 Doeblin condition (Meyn-Tweedie 1993 Ch.16) 部分判定。关键事实: GradScaler scale-factor 动力学 (init $2^{16}$, growth ×2 @2000-interval, backoff ×0.5) **依赖历史** → skip 序列 $(s_t)$ 非纯 Markov (memory-bearing); 但 weight chain $(\theta_n)$ 在 scale-factor 固定之局部窗口内 **条件 Markov** (Thm 3)。严格陈述这个 **hierarchical / mixed 结构** (weight 层条件 Markov + scale-factor 层 memory)。整体 Doeblin minorization 是否成立之完整判定留 D60+。

**"numerical-stability-conditional" 之精确含义** = regime distinctness 结论依赖 5 mode 之 classifier 值 (λ符号 / IEEE-754 边界 / Markov-switching) 之可测量性; exhaustivity 之 FAIL 源于全空间非凸不可枚举; kernel 之 memory 源于 GradScaler 反馈动力学。三者皆 explicit, 这是该结果属 D60+ candidate 而非 paper v9 spine 之原因。

### §0.3 严守 binding

paper v8 final 47/47 manifest D17 锁定不动; 12 NOT-claim (i)-(xii) 撤回不复活 (本文件 **不** declare "first 5-mode taxonomy" / "complete classification" / paradigm shift; "5-mode taxonomy" 仅作 MaoField 项目内部 label, 非文献首创权主张); 反题 6 P0★ A-G 严守 (P0★-A = SGD on $\theta$ 空间非 $D$ 空间, 本证明 regime distinctness 全程 $\theta$-space 之 induced dynamics, mode 之 $D_n$ 观测量是 $\theta_n$ 之 functional); D29 三 leg arXiv+TMLR+KBS 不动; 本证明 0 commit / 0 push / 0 launch 新实验 / 0 ssh write / 0 sub-agent 派遣; L0-3 closure 是 D60+ window emergent candidate, 留 PI + 关卡 3/4 决, 不进 paper v9 spine。

---

## §1 Setup (公理化设定)

### §1.1 状态空间与 mode 观测量 ($\theta$-space, 遵从反题 P0★-A)

**权重状态空间**: $\Theta = \mathbb{R}^d$, $d$ = LM 参数维度 (OPT-125M, $d \approx 1.25\times 10^8$)。$\theta_n \in \Theta$ = 链第 $n$ 代权重。chain 长 $n \in \{0,1,\dots,9\}$ (paper v8 chain length)。

**order parameter (观测量)**: $D_n \in \overline{\mathbb{R}_{\ge 0}} = [0, +\infty]$ 是 $\theta_n$ 之 functional (本证明主线取 $D_n = $ validation PPL 或 KL-on-train; 二者皆 $\theta_n$ 之确定性函数加 fp16 评估前向微扰)。$\overline{\mathbb{R}_{\ge 0}}$ 是含 $+\infty$ 之 one-point 紧化, 容纳 overflow。

**per-step random source**: $\omega_t = (s_t, \xi_t, c_t)$, 其中 $s_t \in \{0,1\}$ = fp16 GradScaler skip indicator ($s_t=1$ 表 skip), $\xi_t$ = minibatch 抽样, $c_t \in \{0,1\}$ = NaN-corruption event indicator (该 step weight 是否被 NaN 覆盖, ROCM_MIOPEN_TRACE §3.2 证据 B/D 实证之 first-NaN event)。

**per-generation map**: $\theta_{n+1} = T_n^{\rm gen}(\theta_n; \omega_n)$, $\omega_n$ = 第 $n$ 代之 step-level source 序列。

### §1.2 公理 (A1)-(A7)

- **(A1) GradScaler scale-factor 动力学 [核心 memory 来源]**: scale factor $\sigma_t$ 按 $\sigma_0 = 2^{16}$, found_inf $\Rightarrow \sigma_{t+1} = 0.5\,\sigma_t$ (backoff), 连续 2000 步无 inf $\Rightarrow \sigma_{t+1} = 2\,\sigma_t$ (growth) 更新 (源: PyTorch grad_scaler.py:407-459, ROCM_MIOPEN_TRACE §2.1)。$\sigma_t$ **由历史 $(\sigma_{t'})_{t'<t}$ 与 inf 事件历史确定** → 确定性反馈控制。
- **(A2) skip indicator 由 scale 与梯度联合决定**: $s_t = \mathbb{1}\{\exists i: |\sigma_t \nabla\mathcal{L}_i| \text{ 非有限}\}$ (源: grad_scaler.py:328-405 `_maybe_opt_step`)。故 $s_t$ **依赖 $\sigma_t$, 而 $\sigma_t$ 依赖历史** → $(s_t)$ 非纯 Markov。
- **(A3) NaN-corruption 是吸收性单向事件**: 一旦 $c_{t_0}=1$ (weight 被 NaN 覆盖), 则 $\forall t > t_0$ 该 chain 之 $D$ 为 NaN, 除非显式 reload 干净 checkpoint (源: ROCM_MIOPEN_TRACE F7 — g=1 接手 g=0 之 NaN weights; D28 §3.2 seed-level cascade)。
- **(A4) IEEE-754 数值边界确定**: fp64 finite max $= M_{64} := 1.7976931348623157\times 10^{308}$ (`sys.float_info.max`); fp16 finite max $M_{16} := 65504$。overflow 触发当 $D$ 计算之中间量超对应 $M$。
- **(A5) 局部强凸 [继承 L0-1]**: 存在 basin $B \subseteq \Theta$ 含 $\theta_{\rm base}$, $\mathcal{L}$ 在 $B$ 上 $\mu$-strongly-convex 且 $\beta$-smooth, $\mu>0$。*(全局非凸, local 假设。)*
- **(A6) per-step Lipschitz [继承 L0-1 Lemma 1]**: 非 skip step 之 $\mathrm{Lip} = \rho_\star = 1-\eta\mu \in (0,1)$; skip step $= \mathrm{id}$, $\mathrm{Lip}=1$。
- **(A7) single-trajectory 观测 [继承 S4 A1]**: $D_n$ 是 trajectory-realized, 不做 ensemble averaging; 故 $\lambda$ (下 Def 3) 按 trajectory a.s. 极限理解。

---

## §2 Definitions

**Def 1 (5 mode)**: 继承 S4 §1.2, 锚定 jsonl:
- **(i) U-shape transient**: $\exists n_0\in\{1,2\}$, $D_{n_0} > D_0$ (PPL spike), 之后 $D_n \downarrow$ recover (anchor: 5060 fp32 gen 0→1 lift +115.05%, D28 §2.3, $36.536\to78.572$)。
- **(ii) frozen plateau**: $T^{\rm gen} = \mathrm{id}$ a.s., $\theta_n \equiv \theta_{\rm base}$ (anchor: 5 cells bit-identical 93.38780852810248, D28 §2.2; seed=42 α=0 span 1.51e-3, D28 §2.4)。**$\equiv$ S1 (b) regime**。
- **(iii) metastable trap**: $\mathrm{Lip} < 1$ strict 但 $\to 1^-$ slow, escape time $\tau \gg N_{\rm chain}$ (anchor: paper plateau 55.97±2.13 over gen 6-9 slow approach + Geshkovski 2024 metastability)。
- **(iv) fp64 overflow**: $\exists n_1$, $D_{n_1} = M_{64}$, 之后 recover (anchor: shumailov rerun gen 4 $= 1.7976931348623157\times 10^{308}$, gen 5-9 recover ∈ [55.332, 60.595], D28 §2 + S4 §1.2)。
- **(v) intermittent null/valid**: $(D_n)$ 是 {valid, NaN} 之 stochastic 混合, marginal 不 admit ergodic averaging (anchor: seed=2024 α=0 = gen5 null/gen6 valid 93.378/gen7,8 null/gen9 valid 93.285, D28 §3.2; 7/10 valid)。

**Def 2 (统一 transition-kernel regime classifier)**: 定义三元 classifier
$$
\Psi(\text{mode}) = \big(\,\mathrm{sgn}(\lambda),\ \beta_{\rm num},\ \kappa_{\rm switch}\,\big) \in \{-,0,+,\varnothing\}\times\{\text{none},16,64\}\times\{0,1\}
$$
其中 $\lambda$ = 顶 Lyapunov 指数 (Def 3); $\beta_{\rm num}$ = 触发之 IEEE-754 边界 (none / fp16 $M_{16}$ / fp64 $M_{64}$); $\kappa_{\rm switch}$ = 是否含 Markov-switching 之 random 在 valid/absorbing 间切换 (1=是)。

**Def 3 (顶 Lyapunov 指数, 继承 L0-1 Def 3)**: $\lambda := \lim_{n\to\infty}\frac1n \log\mathrm{Lip}(f_{\omega_n}\circ\cdots\circ f_{\omega_1})$ (a.s., 由 L0-1 Lemma 2 之 Kingman 1973 存在)。对 mode 而言: contraction $\Rightarrow \lambda<0$; frozen identity $\Rightarrow \lambda=0$; transient expansion 段 $\Rightarrow$ 局部 $\lambda>0$; overflow event 处 $\lambda$ ill-defined (记 $\varnothing$)。

**Def 4 (Doeblin minorization, Meyn-Tweedie 1993 Ch.16)**: Markov kernel $P$ 在集合 $C$ 上满足 Doeblin condition, 若 $\exists$ 概率测度 $\nu$, 常数 $\epsilon_D>0$, 整数 $m\ge 1$ 使 $P^m(x,\cdot) \ge \epsilon_D\,\nu(\cdot)\ \forall x\in C$。满足 $\Rightarrow$ 几何遍历 + unique stationary。

**Def 5 (memory-bearing vs Markov)**: 序列 $(s_t)$ 称 **Markov** 若 $\mathbb{P}(s_{t+1}\mid s_t,s_{t-1},\dots) = \mathbb{P}(s_{t+1}\mid s_t)$; 否则 **memory-bearing**。称 $(\theta_n)$ **条件 Markov on window** $W$ 若在 $\sigma_t$ 固定于 $W$ 内时 $(\theta_n)_{n\in W}$ 是 Markov。

---

## §3 Lemmas

### Lemma 1 (mode classifier 之闭式取值)

5 mode 之 $\Psi$ 取值:
| mode | $\mathrm{sgn}(\lambda)$ | $\beta_{\rm num}$ | $\kappa_{\rm switch}$ |
|---|---|---|---|
| (i) U-shape | $+$ then $-$ (transient expansion) | none | 0 |
| (ii) frozen | $0$ (identity) | none | 0 |
| (iii) metastable | $-$ (slow, $\to 0^-$) | none | 0 |
| (iv) fp64 overflow | $\varnothing$ at event | **64** | 0 |
| (v) intermittent | trajectory-ill-defined | (可含) | **1** |

**证**: (i) L0-1 Lemma 1 + S4: transient 段 $D$ 增 ($\lambda>0$ 局部), 后段收缩 ($\lambda<0$); 无数值边界触发 (fp32, 5060 gen 1=78.572 远 < $M_{16}$ 之 PPL 等价)。(ii) L0-1 Lemma 4: $T=\mathrm{id}\Rightarrow\lambda=0$, frozen, 无边界, 无 switch。(iii) Foster-Lyapunov drift $c\to 0^+$ degenerate (S4 §2.2), $\lambda<0$ 但缓; 无边界。(iv) overflow event 处 $\mathrm{Lip}$ 在 $\overline{\mathbb{R}_{\ge 0}}$ 边界 ill-defined ($\lambda=\varnothing$), 触发 fp64 边界 $M_{64}$ (A4)。(v) NaN absorbing + 随机 reentry → valid/NaN 间 Markov-switching, $\kappa_{\rm switch}=1$; trajectory-realized $\lambda$ 不 admit ensemble averaging (A7)。$\blacksquare$

### Lemma 2 (mode (ii) 之 IEEE-754 区分 — frozen 非 overflow)

mode (ii) 之 frozen ($\beta_{\rm num}=$ none) 与 mode (iv) overflow ($\beta_{\rm num}=64$) 之触发机制不相交: frozen 源于 $T=\mathrm{id}$ (skip rate $p\to1$, 权重不动, $D$ 停在 base 93.349); overflow 源于 $D$ 之中间量超 $M_{64}$ (权重已运动且发散)。

**证**: frozen 之 $D_n - D_0$ 之 span $= 1.51\times10^{-3}$ (D28 §2.4 verbatim), 远在 $M_{64}$ 之内且权重位移 $\to 0$ (L0-1 Lemma 4(ii))。overflow 之 $D_{n_1} = M_{64}$ 要求 $\exp(\text{loss})$ 累积超 $10^{308}$, 须权重显著发散 ($s_t=0$ 之非平凡更新)。二者 skip regime 相反 ($p\to1$ vs $p<1$), 不相交。$\blacksquare$

### Lemma 3 (GradScaler 序列 memory-bearing — 闭合 S4 A5 之 partial)

$(s_t)$ 是 memory-bearing (非 Markov)。

**证**: 由 (A2) $s_t = \mathbb{1}\{\sigma_t\cdot|\nabla\mathcal{L}|\text{ 非有限}\}$, 故 $s_t$ 经 $\sigma_t$ 依赖 scale。由 (A1) $\sigma_t$ 之更新含 growth rule "连续 2000 步无 inf $\Rightarrow \times2$", 即 $\sigma_{t+1}$ 依赖 $(s_{t}, s_{t-1}, \dots, s_{t-1999})$ 之全窗口 (是否连续 2000 步无 found_inf)。故 $\mathbb{P}(s_{t+1}\mid s_t) \ne \mathbb{P}(s_{t+1}\mid s_t,\dots,s_{t-1999})$, $(s_t)$ 之转移依赖 $\ge 2000$ 步历史 → memory-bearing (Def 5)。$\blacksquare$

> **这是 kernel partial 判定之核心**: skip 序列层 memory-bearing 由 GradScaler growth-interval=2000 之确定性反馈严格 derive, 非假设。

### Lemma 4 (weight chain 之条件 Markov)

在 scale factor 固定于窗口 $W$ ($\sigma_t \equiv \bar\sigma\ \forall t\in W$) 之条件下, weight chain $(\theta_n)_{n}$ 限制在对应 generation 段是 Markov。

**证**: $\sigma$ 固定 $\Rightarrow s_t$ 仅依赖当前梯度 $\nabla\mathcal{L}(\theta;\xi_t)$ (经 $\bar\sigma$), 即 $s_t$ 给定 $\theta$ 后条件独立于历史。per-step map $f_{\omega_t}(\theta)$ (A6) 仅依赖当前 $(\theta, s_t, \xi_t)$。$(\xi_t)$ i.i.d. 抽样。故 $\theta_{n+1}\mid\theta_n$ 条件独立于 $(\theta_{n-1},\dots)$ → 条件 Markov (Def 5)。$\blacksquare$

### Lemma 5 (受限 framework 内有限分类 — exhaustivity 之弱版本可做)

在受限 framework $\mathcal{F}_0$ = {1-D order parameter $D_n\in\overline{\mathbb{R}_{\ge0}}$ + bounded multiplicative noise $|f'|\le L_{\max}$ + IEEE-754 有限精度 (fp16/fp64 边界)} 内, 由 $\Psi$ classifier 诱导之 regime 数有限, 上界 $|\{-,0,+,\varnothing\}|\times|\{\text{none},16,64\}|\times|\{0,1\}| = 4\times3\times2 = 24$。

**证**: $\Psi$ 之三分量各取有限值 (Def 2), 笛卡尔积 $\le 24$。bounded multiplicative noise $\Rightarrow \lambda$ 之 sign 有限分类 (Kingman a.s. 存在, L0-1 Lemma 2); IEEE-754 有限精度 $\Rightarrow$ 边界触发仅 fp16/fp64 两类 + none; Markov-switching $\Rightarrow$ 二值。故 $\mathcal{F}_0$ 内 regime 由有限 $\Psi$-cell 覆盖。$\blacksquare$

> **关键区分**: Lemma 5 之有限性 **仅在 $\mathcal{F}_0$ 之 1-D + bounded 假设内成立**。全 $\theta$-space ($d\approx1.25\times10^8$ 非凸) 不满足 1-D 假设, 见 §5 Thm 2。

---

## §4 Main Theorems

### Theorem 1 (regime distinctness — L0 闭合)

设 (A1)-(A7)。则 5 mode (i)-(v) 是 **pairwise distinct dynamical regime**: 对任意 $i\ne j$, $\Psi(\text{mode}_i) \ne \Psi(\text{mode}_j)$ 或其触发数值边界不相交。即不存在两个不同 mode 是同一 regime 之不同取值。

### Theorem 2 (exhaustivity — 诚实 FAIL on 全 $\theta$-space)

在全 $\theta$-space $\Theta=\mathbb{R}^d$ ($d\approx1.25\times10^8$, 非凸) 上, 命题 "$\bigcup_{i=1}^5 M_i = \Omega\setminus\Omega_{\rm ergodic}$" (5 mode 穷尽全非平凡 sample) **不可严格证明**。受限版本 (Lemma 5, $\mathcal{F}_0$ 内有限分类) 可做。

### Theorem 3 (transition kernel — PARTIAL, hierarchical mixed 结构)

链之 transition kernel 呈 **hierarchical mixed** 结构: (a) scale-factor / skip 层 $(s_t)$ memory-bearing (Lemma 3, 非 Markov); (b) weight 层 $(\theta_n)$ 在 scale 固定窗口内条件 Markov (Lemma 4)。整体 $(\theta_n, \sigma_t)$ 联合是否满足 Doeblin minorization (Def 4) 之完整判定留 D60+。

---

## §5 Proofs

**Theorem 1 证明**. 逐对 $\binom{5}{2}=10$ 对验证 (用 Lemma 1 之 $\Psi$ 表 + Lemma 2):

- (i,ii): $\mathrm{sgn}(\lambda)$: $\{+,-\}$ vs $0$ — 不同。
- (i,iii): (i) 含 transient expansion ($\lambda>0$ 段) vs (iii) 全程 $\lambda<0$ — 不同 (S4: (i) 二段, (iii) 单调 slow contraction)。
- (i,iv): $\beta_{\rm num}$ none vs 64 — 不同 (Lemma 2)。
- (i,v): $\kappa_{\rm switch}$ 0 vs 1 — 不同。
- (ii,iii): $\mathrm{sgn}(\lambda)$ $0$ vs $-$ — 不同 (frozen identity vs strict contraction)。
- (ii,iv): $\beta_{\rm num}$ none vs 64 + skip regime $p\to1$ vs $p<1$ — 不同 (Lemma 2)。
- (ii,v): $\kappa_{\rm switch}$ 0 vs 1; 且 (ii) 全 valid frozen vs (v) valid/NaN 间歇 — 不同。
- (iii,iv): $\beta_{\rm num}$ none vs 64 — 不同。
- (iii,v): $\kappa_{\rm switch}$ 0 vs 1 — 不同。
- (iv,v): $\beta_{\rm num}$ 64 vs (v) 之 NaN-absorbing (注: fp64 overflow $M_{64}$ 是 **finite** 大数后 recover; intermittent 是 **NaN** = IEEE-754 special value, 不同 IEEE-754 类别) + $\kappa_{\rm switch}$ 0 vs 1 — 不同。

10/10 对 pairwise distinct。故 5 mode 是 distinct regime。

**关键 anchor 实证**: (ii) frozen 之 5 cells = 93.38780852810248 (span 1.51e-3) 与 (iv) overflow 之 $M_{64}=1.7976931348623157\times10^{308}$ 相差 $\sim 10^{306}$ 量级 — 物理上不可能是同一 regime; (v) seed=2024 之 null/valid 交替 (7/10 valid) 与 (ii) 之 10/10 valid frozen 之 $\kappa_{\rm switch}$ binary 不同。$\blacksquare$

**Theorem 2 证明 (FAIL 之严格陈述)**. 穷尽性命题等价于: 对 $\Theta=\mathbb{R}^d$ 上一切初值 + 一切 $(s_t,\xi_t,c_t)$ 实现, 诱导之 $D_n$ 动力学落入 5 个 $\Psi$-cell 之一。

反例存在性论证: 全 $\theta$-space 非凸 ($d\approx1.25\times10^8$), 损失景观含未知数目之 saddle / basin。S4 §2.4 已列 3 个 unsurfaced candidate: (vi) quasi-periodic limit cycle (无 ergodic mixing, $T^K(D)=D$ 但 $T(D)\ne D$) — 此 mode 之 $\lambda=0$ 但非 frozen identity, $\Psi$ 与 (ii) 之 $\mathrm{sgn}(\lambda)=0$ 碰撞却动力学不同 (period-$K$ orbit ≠ fixed point), 说明 $\Psi$ 之 3 分量**不足以区分一切可能 regime**; (vii) cross-trajectory bifurcation; (viii) measure-theoretic riddled basin (Ly-Gong 2025, uncertainty exponent ≈ 0)。

要排除这些须穷举 $d\approx1.25\times10^8$ 维非凸景观之全部不变集 — 无 generating mathematical structure 强制有限分类时, 此为不可达 (与 L0-1 §0.2 之 "全局非凸不可枚举" 同构)。**故 exhaustivity 在全 $\theta$-space 严格 FAIL**。

**可做之弱版本 (Lemma 5)**: 在 $\mathcal{F}_0$ (1-D + bounded + IEEE-754) 内, regime 数 $\le 24$ 有限。但 $\mathcal{F}_0$ 之 1-D 假设 **不等于** 真实 $d\approx1.25\times10^8$ chain; 故 "$\mathcal{F}_0$ 内有限" **不蕴含** 真实链穷尽性。二者必须明确区分。$\blacksquare$

**Theorem 3 证明 (PARTIAL)**.

*(a) skip 层 memory-bearing*: Lemma 3 已证 $(s_t)$ 非 Markov (依赖 $\ge2000$ 步历史 via growth interval)。

*(b) weight 层条件 Markov*: Lemma 4 已证 $(\theta_n)$ 在 scale 固定窗口内 Markov。

*(c) 整体 mixed*: 联合过程 $(\theta_n, \sigma_{t(n)})$ 之 kernel = weight 层条件 Markov ⊗ scale 层 memory 反馈。整体非纯 Markov (因 $\sigma$ 层 memory), 亦非纯 memory-bearing (因 weight 层条件 Markov), 是 **hierarchical mixed**。

*(d) Doeblin 完整判定留 D60+*: 整体 $(\theta_n,\sigma_t)$ 是否满足 Def 4 之 minorization 需: (i) 验证 absorbing NaN state (A3) 之存在破坏 minorization (一旦 $c_{t_0}=1$ 进入 NaN absorbing, $P^m(x,\cdot)$ 不 minorize 干净测度) — 这暗示 **全局 Doeblin FAIL** (因 NaN 是吸收态); (ii) 但在 NaN-free sub-chain (如 seed=42 α=0 之 10/10 valid) 上, 限制 kernel 可能满足 Doeblin。完整判定 (含 absorbing state 之 sub-stochastic 分解 + scale-factor 遍历性) 留 D60+。$\blacksquare$

> **诚实标注**: Thm 3 (d) 之 "全局 Doeblin 可能 FAIL (NaN absorbing)" 是 **方向性观察非严格证明** — 严格须证 absorbing state 在测度上非可忽略, 留 D60+。

---

## §6 Corollaries

### Cor 1 (5 mode 与 S1 两态之 hierarchical 关系 — 闭合 S4 §3.1)

由 Thm 1 + L0-1 主定理: mode (ii) frozen $\equiv$ S1 (b) degenerate regime ($\lambda=0$, $p\to1$); mode (i,iii,iv,v) $\subset$ S1 (a) regime ($\lambda<0$ 或 $p<1$ 之非平凡更新内之 trajectory-level 子结构)。故 S1 是 macro regime classifier (两态), S4 之 5 mode 是 (a) regime 内之 micro 子结构 catalog + (b) regime 之 direct subsume。**二者不矛盾, 是 hierarchical**。

### Cor 2 (intermittent (v) 是 Markov-switching 之 instantiate)

由 Lemma 1 + Lemma 3: mode (v) seed=2024 之 null/valid 交替 (gen5 null, gen6 valid 93.378, gen7,8 null, gen9 valid 93.285, D28 §3.2) 是 NaN-absorbing 与 random reentry 之 Markov-switching (Horn-Kelly / switching-systems family)。注意: reentry 机制 (为何 gen6/gen9 能 recover) 在单 trajectory 上 ill-defined, 留 multi-seed N≥8 之 statistical 刻画 (与 L0-1 open Q3 一致)。

### Cor 3 (fp64 overflow (iv) 之 transient 性质)

由 Lemma 2 + A4: mode (iv) 之 $D_{n_1}=M_{64}=1.7976931348623157\times10^{308}$ (finite, 非 NaN) 后 gen 5-9 recover 到 [55.332, 60.595] (D28 §2), 说明 overflow 是 $\overline{\mathbb{R}_{\ge0}}$ 边界之 transient escape + return interior, 非 absorbing。这与 (v) 之 NaN absorbing (A3) 本质不同 — 故 Thm 1 (iv,v) pairwise distinct 之实证基础。

---

## §7 Falsifier (可证伪条件)

- **F-L0-3-a (regime distinctness)**: 若构造 toy chain 使两个 S4 mode 之 $\Psi$ classifier 三分量全同 **且** 数值边界相同, 则 Thm 1 之 pairwise distinct 被证伪。**成本 ~1-2h CPU** (1-D toy $D_n$ + 人工 Bernoulli skip + 人工 overflow inject)。
- **F-L0-3-b (memory-bearing)**: 若解析 9070XT nohup log 之 step-level scale 打印, 实测 $(s_t)$ 满足 1-step Markov (转移不依赖 >1 步历史), 则 Lemma 3 之 memory-bearing 被证伪, GradScaler 退化为 Markov。**成本 0 GPU** (解析已有 nohup log 之 scale trace; 但 ROCM_MIOPEN_TRACE F8 指出当前 logging cadence 250 步太粗, 须更细 step-level 打印, 留 ssh 主会话)。
- **F-L0-3-c (exhaustivity 受限版)**: 若在 $\mathcal{F}_0$ 内发现一个动力学不落入 24 个 $\Psi$-cell 任一, 则 Lemma 5 之有限分类被证伪。**成本 ~2h CPU**。
- **F-L0-3-d (Doeblin / NaN absorbing)**: 若 multi-seed 统计显示 NaN state 总能 a.s. reentry valid (非 absorbing), 则 A3 之 absorbing 假设被证伪, Thm 3(d) 之 "全局 Doeblin FAIL" 方向逆转。**成本 multi-seed N≥8 chain** (D60+)。

---

## §8 Limitations ("numerical-stability-conditional" 之具体内容)

- **L1 (exhaustivity 全空间 FAIL)**: 这是本证明之**主诚实点**。全 $\theta$-space ($d\approx1.25\times10^8$ 非凸) 穷尽性不可达 (Thm 2)。受限 $\mathcal{F}_0$ 内有限分类 (Lemma 5) **不蕴含** 真实链穷尽性。6th-7th-8th mode candidate (quasi-periodic / bifurcation / riddled basin, S4 §2.4) 未排除。
- **L2 (classifier $\Psi$ 不完备)**: Thm 2 证明中 (vi) quasi-periodic 之 $\lambda=0$ 与 (ii) frozen 碰撞却动力学不同, 说明 3 分量 $\Psi$ **不足以区分一切 regime** — distinctness (Thm 1) 仅对 **已 enumerate 之 5 mode** 成立, 非对一切可能 mode。
- **L3 (kernel partial)**: Thm 3 仅严格陈述 hierarchical mixed 结构 (skip 层 memory + weight 层条件 Markov); 整体 Doeblin minorization 完整判定 + scale-factor 序列遍历性 (与 L0-1 L4 同 gap) 留 D60+。Thm 3(d) 之 NaN-absorbing 破坏 Doeblin 是方向性观察非严格证明。
- **L4 (single-trajectory)**: mode (iv)(v) 之 $\lambda$ 在单 trajectory 上 ill-defined (A7), overflow/intermittent 之 repeatable statistical 性质留 multi-seed N≥8 (D28 §1.2 + Cor 2)。
- **L5 (NaN reentry 机制未闭)**: mode (v) 之 valid reentry (gen6/gen9 recover) 之机制 (为何能从 NaN absorbing 恢复) 与 A3 之 strict absorbing 假设存在张力 — 可能是 chain runner 之 reload 或 fp16 评估非确定性, 留 PI + ssh 主会话 step-level audit。
- **L6 (mode (iii) maofield 直接证据弱)**: metastable trap 之 maofield 直接 evidence 中等 (paper plateau slow approach), 主要靠 Geshkovski 2024 literature; 与 maofield 12-layer 之 dimension mismatch (Geshkovski single-layer) — 留 D60+ 平均场 transformer 12-layer extension。

**以上 L1-L3 即 "numerical-stability-conditional" 之精确内容, 也是本结果属 D60+ candidate 而非 paper v9 spine 之根本原因。**

---

## §9 5-channel cross-verify (五通道交叉验证)

| 通道 | 内容 | verdict |
|---|---|---|
| **1 数学** (本证明) | $\Psi$ classifier (Lyapunov + IEEE-754 + Markov-switching) 之 pairwise distinctness 严格 (Thm 1, 10/10 对); exhaustivity 全空间 FAIL (Thm 2); kernel hierarchical mixed partial (Thm 3) | regime distinctness 闭; exhaustivity FAIL; kernel partial |
| **2 代码** | GradScaler 动力学 code-traced (grad_scaler.py:407-459 growth/backoff, ROCM_MIOPEN_TRACE §2.1); skip = `_maybe_opt_step` (328-405); NaN absorbing = g=1 接手 g=0 NaN weights (F7); growth-interval=2000 (Lemma 3 之 memory source) | ✓ 一致: memory-bearing 由 code 严格 derive |
| **3 实验** | 5 cells 93.38780852810248 frozen (Def 1 ii); 5060 lift +115.05% U-shape (i); fp64 $M_{64}$ overflow (iv); seed=2024 null/valid 间歇 (v); seed=42 span 1.51e-3 (ii) — 全 jsonl verbatim (D28) | ✓ 一致: 4 mode 有直接 jsonl anchor, (iii) metastable 中等 + literature |
| **4 文献** | Meyn-Tweedie 1993 Ch.5/16 (Doeblin) / Kingman 1973 (Lyapunov) / Geshkovski 2024-2025 (metastability) / IEEE-754 standard (fp16/fp64) / Horn-Kelly switching-systems (Markov-switching) | ✓ 框架 borrow valid, 非文献首创 (反 grandiose) |
| **5 反题** | P0★-A ($\theta$ 非 $D$ 空间): regime distinctness 全程 $\theta$-space 之 induced dynamics, $D_n$ 是 $\theta_n$ functional **satisfied**; exhaustivity FAIL 诚实 disclose 不 inflate; "5-mode taxonomy" 不 declare 文献首创 | ✓; 但本 agent 非完全 zero-context (§0.1 caveat), 第 5 通道独立性弱, 留反题三方决复核 |

**surface dissonance (诚实)**: (1) $\Psi$ classifier 不完备 (L2, quasi-periodic 与 frozen $\lambda=0$ 碰撞) — distinctness 仅对已 enumerate 5 mode; (2) exhaustivity 受限版可做 vs 全空间 FAIL 必须区分 (L1); (3) NaN reentry (v) 与 absorbing (A3) 张力 (L5); (4) 本 agent 非完全 zero-context (§0.1), §9 第 5 通道独立性弱于理想。

---

## §10 Open Questions

**P0 (优先, 影响 kernel 判定)**:
1. **整体 Doeblin minorization 完整判定**: 联合过程 $(\theta_n,\sigma_t)$ 含 NaN absorbing state (A3) 时, 全局是否满足 Def 4。方向性观察 (Thm 3d) 暗示全局 FAIL, 但须证 absorbing state 测度非可忽略 — 留 D60+ sub-stochastic 分解。
2. **NaN reentry 机制 (L5)**: mode (v) 之 valid reentry vs A3 absorbing 张力之 root cause (reload? fp16 评估非确定性?) — 留 ssh 主会话 step-level audit。

**P1 (次优, 影响 exhaustivity 弱版与 classifier)**:
3. **$\Psi$ classifier 完备化 (L2)**: 增加分量 (如 period detector 区分 quasi-periodic vs frozen) 使 distinctness 对更大 mode 集成立 — 但全空间穷尽性仍 FAIL (Thm 2)。
4. **GradScaler 序列遍历性严证 (L3 + L0-1 L4 同 gap)**: growth/backoff 确定性反馈下 $(s_t)$ 是否平稳遍历。
5. **mode (iv)(v) repeatable statistical 性质**: multi-seed N≥8 之 overflow/intermittent 频率分布。

**P2 (长程, D60+ paradigm candidate)**:
6. **6th-8th mode candidate 排除或吸收**: quasi-periodic / bifurcation / riddled basin (S4 §2.4) 之严格处理, 留 D60+ Ly-Gong 数学 instantiate + 平均场 transformer 12-layer。

---

## §11 14-Q self-check

| # | 问 | 自检 |
|---|---|---|
| 1 | 数字有 jsonl 源? | ✓ 5 cells 93.38780852810248 / 5060 lift +115.05% / fp64 $M_{64}$ 1.7976931348623157e308 / seed=2024 null/valid / span 1.51e-3 全 jsonl verbatim (D28) |
| 2 | 概率声明真空 >48h? | ✓ 不 declare 接受率; 仅数学 verdict |
| 3 | 数学形式与代码一致? | ✓ Lemma 3 memory-bearing ⟺ GradScaler growth-interval=2000 code-traced (通道 2); A3 NaN absorbing ⟺ F7 |
| 4 | major 声明过子协作者验证? | partial — 本 agent 非完全 zero-context (§0.1), 留反题三方决复核第 5 通道 |
| 5 | 差异记差异日志? | ✓ L2 classifier 不完备 + L5 NaN reentry 张力 + Thm 3(d) 方向性非严格 全 explicit disclose, 不抹平 |
| 6 | 真实日期 binary? | ✓ §0.1 `date` 2026-05-29 10:32 CST |
| 7 | 哲学位置 outcome 非 starting form? | ✓ 数学是 retrospective 严格化, 起点是 jsonl 物质实践 (5 mode 现象先于 classifier) |
| 8 | "自发" 含 multi-agent binding? | ✓ L0-3 closure 留 PI + 关卡 3/4; 不 unilateral declare paper-level |
| 9 | 回顾 scope 含 4 项? | ✓ 12 NOT-claim 不复活 (§0.3, 不 declare "first taxonomy"/"complete classification") + 反题 P0★ (通道5) + 5/12+5/19 inflate (不 inflate exhaustivity, 诚实 FAIL) |
| 10 | timeline emerge D60+ 非 D22-D60? | ✓ §0.2 + §8 + §10 P2 全标 D60+ candidate, 不入 paper v9 spine |
| 11 | candidate 用 dialectical inclusive form? | ✓ §8: exhaustivity 不 declare "全空间可分类", 而是 "受限可做 + 全空间 FAIL" inclusive; 不 declare "mitigation 全错" |
| 12 | paradigm-shift emergent D60+ verify? | ✓ §10 P2 留 D60+ cumulative multi-channel + 反题三方决 |
| 13 | methodological 4 path binary specify? | ✓ §7 falsifier 是 path A (multi-channel: F-L0-3-b 解析 log) + path D (counter-factual toy: F-L0-3-a/c) instantiate |
| 14 | 5 leg 实验 dialectical totality? | ✓ §10 P1.5 multi-seed N≥8 + P2 multi-stack = cross-layer evidence accumulation, 非 single-axis |

任一 no → 不发出。第 4 + 第 5 通道 partial (非完全 zero-context), 已 explicit disclose, 留复核; 余 ✓。

---

## §12 References (prior art, 反 grandiose: 全为 borrow 非首创)

1. Banach S. 1922. *Sur les opérations dans les ensembles abstraits*. Fund. Math. 3:133-181. [收缩映射, $\rho<1$]
2. Kingman J.F.C. 1973. *Subadditive Ergodic Theory*. Ann. Probab. 1(6):883-909. [Lyapunov 指数 a.s. 存在, Def 3]
3. Meyn S., Tweedie R. 1993. *Markov Chains and Stochastic Stability*. Springer, Ch.5 (Markov stability) + Ch.16 (Doeblin condition). [Thm 3 kernel + Def 4]
4. Diaconis P., Freedman D. 1999. *Iterated Random Functions*. SIAM Review 41(1):45-76. [平均收缩, regime (a) 继承 L0-1]
5. Geshkovski B., Letrouit C., Polyanskiy Y., Rigollet P. 2024/2025. *Dynamic Metastability in the Self-Attention Model* / mean-field transformer. [mode (iii) metastable, L6]
6. Micikevicius P. et al. 2018. *Mixed Precision Training*. ICLR 2018. [GradScaler / loss scaling, A1]
7. IEEE Computer Society. 2019. *IEEE Standard for Floating-Point Arithmetic (IEEE 754-2019)*. [fp16/fp64 数值边界 $M_{16}/M_{64}$, A4 + Lemma 2]
8. Horn R.A., Kelly C.T. / switching-systems literature. [Markov-switching, mode (v) + Cor 2]
9. Bottou L., Curtis F., Nocedal J. 2018. *Optimization Methods for Large-Scale ML*. SIAM Review 60(2):223-311. [强凸 SGD, A5/A6 继承 L0-1]
10. Ly N., Gong S. 2025 (S4 cite). *riddled basin / measure-theoretic ill-posedness*. [mode (viii) candidate, §10 P2]

---

**生成**: Opus 数学证明 specialist, zero-context 派遣 (一凡 D29 dispatch), 2026-05-29 10:32 CST 启动。

**核心 output**: L0-3 = MaoField chain 5-mode failure taxonomy 之 axiom-first partial 严格化。**严格闭合**: regime distinctness — 5 mode 由 $\Psi$ classifier (Lyapunov 符号 + IEEE-754 边界 + Markov-switching) pairwise distinct (Thm 1, 10/10 对)。**诚实 FAIL**: exhaustivity — 全 $\theta$-space ($d\approx1.25\times10^8$ 非凸) 穷尽性不可达 (Thm 2); 受限 $\mathcal{F}_0$ 内有限分类 $\le24$ cell 可做 (Lemma 5) 但不蕴含真实链穷尽。**PARTIAL**: transition kernel — hierarchical mixed (skip 层 memory-bearing via GradScaler growth-interval=2000 严格 derive Lemma 3 + weight 层条件 Markov Lemma 4); 整体 Doeblin 完整判定 (含 NaN absorbing 破坏) 留 D60+。

**严守**: paper v8 final 47/47 + D17 + D29 三 leg + 12 NOT-claim 撤回 (不 declare "first 5-mode taxonomy"/"complete classification") + 反题 6 P0★ (P0★-A θ-space induced dynamics satisfied) 全 binding。0 commit / 0 push / 0 launch / 0 ssh write / 0 sub-agent。L0-3 closure 是 D60+ window candidate, 留 PI + 关卡 3/4 决。本 agent 非完全 zero-context (caveat §0.1 disclosed), 第 5 通道独立性留反题三方决复核。
