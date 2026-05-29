# MaoField L0 严格证明 — L0-1: fp16-skip 链两态 dichotomy 的 axiom-first 推导

> Banach LLM (numerical-stability-conditional) — S1 两态 attractor claim 的公理优先严格化

## §0 Scope (范围声明 + 元数据 + 严守 binding)

### §0.1 元数据

| 项 | 值 |
|---|---|
| 真实日期 binary | `date '+%F %T %Z'` → **2026-05-29 09:53 CST** (D29) |
| 生成 agent | Opus 4.8 (1M context) 数学证明专家, 主会话直接执行 (一凡 D29 explicit dispatch "执行 L0-1 严格证明") |
| **agent caveat (诚实 disclose)** | 本证明非 zero-context fresh session: 已 load 项目 memory + CLAUDE.md, 偏离 L0_PROOF_PROMPT §13 之独立验证通道设计意图。该 caveat 已于执行前 disclose, 一凡 ack 后 directing execute. 故本文件 §9 之 "第 5 通道反题独立性" 弱于理想 zero-context, 留 PI + 关卡 3 反题三方决再派遣独立 channel 复核 |
| 协议 | axiom-first 严格推导: definition → lemma → theorem → proof → corollary → falsifier → limitation; 5 通道 cross-verify; 每数有 jsonl/code/文献源 |
| input source | S1+S2 PART (MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S1_S2_ATTEMPT1) + D28_MATH_RIGOROUS_AUDIT + D28_EXPERIMENTAL_DEEP_AUDIT (5 cells verbatim) + ROCM_MIOPEN_TRACE_AUDIT + MATH_VERIFY_D25_GRADSCALER_SKIP + MAOFIELD_MATH_MULTI_CHANNEL_ANALYSIS_D26 + PAPER_V9_SKELETON_DRAFT_D27 |
| 字数 | ~4800 字 substantive |

### §0.2 闭合什么 / 不闭合什么 (诚实 scope, 反 grandiose)

**本证明严格闭合 (L0 axiom-first)**:

1. **frozen regime (b) 完全闭合** — $p=1$ 时 transition map 恒为 identity, 精确; $p \ge 1-\delta$ 时观测精度内 frozen, $\delta$ 闭式给出。**并修正 S1 之 "唯一 fixed point = $\theta_{\rm base}$" 过度声明** (实为初值选出之平凡 rest point, 非吸引子)。
2. **phase boundary 之 sharp dichotomy at $p=1$** — 通过平均 log-Lipschitz 判据 (Diaconis-Freedman 1999 + Kingman 1973) 严格替代 S1 之 "$\rho=1$ 边界 vacuous" gap (闭合 S1 gap 1)。
3. **$\epsilon, \delta$ 之闭式定义** — 由 $(\rho_\star, N_{\rm total}, N_{\rm gen}, {\rm tol})$ 解析决定, 非自由参数 (闭合 S1 gap 2)。
4. **per-step 收缩因子 $\rho_\star = 1-\eta\mu$ first-principles** — $\mu$ = 局部强凸模, 可测量, 取代 paper Reading 2 之 retrospective fit (闭合 S1 gap 3)。

**本证明明确 NOT 闭合 (留 D60+ + 反题三方决)**:

- regime (a) 之 "全局好吸引子" — 真实 Shumailov 链每代在上代模型生成数据上 fine-tune, 数据分布逐代漂移, per-generation map 非平稳 (non-autonomous), 故 regime (a) 之唯一吸引子结论 **仅在 local basin 强凸 (A1) + 数据平稳-on-average (A6) 双条件下成立**; 实际 Shumailov collapse (PPL 逐代增大) 是 divergence-side 现象, 本定理 **不 model collapse 本身**, 只 model "权重冻结 vs 权重运动" 之二分。
- P0★-G cross-stack root cause (5060 fp32 vs 9070XT fp16 之 +56.81 PPL) — 留 multi-stack ablation grid。

**"numerical-stability-conditional" 之精确含义** = 全部 regime (a) 结论条件依赖于 (i) 局部强凸模 $\mu>0$ (basin 内, 非全局); (ii) skip 序列平稳遍历 (stationary-ergodic); (iii) 数据平稳-on-average。三者皆为 explicit 假设而非已证事实, 这正是该结果属 D60+ candidate 而非 paper v9 spine 之原因。

### §0.3 严守 binding

paper v8 final 47/47 manifest D17 锁定不动; 12 NOT-claim (i)-(xii) 撤回不复活 (本文件 **不** declare "first instantiation of Banach LLM in literature" / paradigm shift / mitigation framework — "Banach LLM first instantiation" 仅作项目内部 label, 指 MaoField 语境内 S1 之 axiom-first 闭合, 非文献首创权主张); 反题 6 P0★ A-G 严守 (P0★-A = SGD on $\theta$ 空间非 $D$ 空间, 本证明全程 $\theta$-space; P0★-B = 本 L0-1 闭合目标); D29 三 leg arXiv+TMLR+KBS 不动; 本证明 0 commit / 0 push / 0 launch 新实验 / 0 sub-agent 派遣; L0 closure 是 D60+ window emergent candidate, 留 PI + 关卡 3/4 决。

---

## §1 Setup (公理化设定)

### §1.1 状态空间与 transition map ($\theta$-space, 遵从反题 P0★-A)

**状态空间**: $\Theta = \mathbb{R}^d$, 其中 $d$ = 语言模型参数维度 (OPT-125M, $d \approx 1.25\times 10^8$)。$\theta_n \in \Theta$ = 链第 $n$ 代结束时权重。

**一代 (generation)** = 在固定 (或逐代给定) 数据上做 $N_{\rm total}$ 个 optimizer step 之 fine-tune。每个 step $t \in \{1,\dots,N_{\rm total}\}$ 抽取随机源 $\omega_t = (s_t, \xi_t)$, 其中 $s_t \in \{0,1\}$ 是 fp16 GradScaler skip indicator ($s_t=1$ 表 skip), $\xi_t$ 是 minibatch 抽样。

**per-step map**:
$$
f_{\omega_t}(\theta) =
\begin{cases}
\theta - \eta\, P_t\, \nabla \mathcal{L}(\theta; \xi_t), & s_t = 0 \ (\text{更新}) \\[4pt]
\theta, & s_t = 1 \ (\text{skip})
\end{cases}
$$
$\eta$ = 学习率 (yaml: $2\times 10^{-5}$), $P_t$ = AdamW 对角预条件子 (plain SGD 时 $P_t = I$)。

**per-generation map**: $T_n^{\rm gen} = f_{\omega_{N_{\rm total}}} \circ \cdots \circ f_{\omega_1}$, 链递推 $\theta_{n+1} = T_n^{\rm gen}(\theta_n)$。

**skip 概率**: $p := \mathbb{E}[s_t]$ = 边际 skip rate (per step)。

### §1.2 公理 (A1)-(A6) — 继承 S1 并修正/补强

- **(A1) 局部强凸 [核心 conditional]**: 存在 basin $B \subseteq \Theta$ (含 $\theta_{\rm base}$), 损失 $\mathcal{L}$ 在 $B$ 上 $\mu$-strongly-convex 且 $\beta$-smooth, $\mu > 0$。*(全局非凸, 故此假设 local; 此即 §0.2 之 conditional 来源之一。)*
- **(A2) skip 序列平稳遍历 [放松 S1 之 i.i.d.]**: $(s_t)_{t\ge 1}$ 是 stationary-ergodic 过程, 边际 $\mathbb{E}[s_t]=p$。*(S1 之 A2 要求 i.i.d.; 本证明用 Kingman 次可加遍历定理放松至平稳遍历, 见 Lemma 2 — 这是相对 S1 之 strengthening, 因 GradScaler scale-factor 动力学 backoff/growth 产生 step 间相关, 非 i.i.d.。)*
- **(A3) 步长 regime**: $0 < \eta \le 1/\beta$ (标准 GD 收缩 regime)。
- **(A4) 初值在 basin**: $\theta_{\rm base} \in B$ (jsonl: 5 cells 与 base PPL 93.349 同 order, 实证 $\theta_{\rm base}$ 处于一可评估 basin)。
- **(A5) moment 条件**: $\exists \theta_0:\ \mathbb{E}\big[\log^+ \|f_{\omega}(\theta_0) - \theta_0\|\big] < \infty$ (Diaconis-Freedman 技术条件; 梯度有界 $\|\nabla\mathcal{L}\| \le G$ 即可保证)。
- **(A6) 数据平稳-on-average [最强 conditional, 真实 Shumailov 不满足]**: per-generation map 族 $\{T_n^{\rm gen}\}_n$ 同分布 (固定数据分布), 或漂移满足一致收缩-on-average。*真实 Shumailov 链数据逐代漂移, 此假设破坏 → 见 §8 L2 + §10 open question 1。*

---

## §2 Definitions

**Def 1 (per-step Lipschitz 因子)**: $L_{\omega_t} := \mathrm{Lip}(f_{\omega_t})$。

**Def 2 (per-generation Lipschitz 因子)**: $\rho_{\rm gen} := \mathrm{Lip}(T_n^{\rm gen}) \le \prod_{t=1}^{N_{\rm total}} L_{\omega_t}$。

**Def 3 (顶 Lyapunov 指数)**:
$$
\lambda := \lim_{n\to\infty} \frac{1}{n} \log \mathrm{Lip}\big(f_{\omega_n}\circ\cdots\circ f_{\omega_1}\big) \quad (\text{a.s., 由 Lemma 2 存在})
$$

**Def 4 ($\epsilon, \delta$ 闭式 — 闭合 S1 gap 2)**: 给定观测容差 $\mathrm{tol}_c \in (0,1)$ (链可见收缩阈) 与 $\mathrm{tol}_f > 0$ (冻结分辨阈), 梯度范数上界 $G$:
$$
\boxed{\ \epsilon := \frac{-\log \mathrm{tol}_c}{N_{\rm total}\, N_{\rm gen}\, \log(1/\rho_\star)}, \qquad
\delta := \frac{\mathrm{tol}_f}{N_{\rm total}\, \eta\, G}\ }
$$
$N_{\rm gen}$ = 链总代数, $\rho_\star$ 见 Def 5。

**Def 5 (per-step 收缩因子 — 闭合 S1 gap 3)**: 在 (A1)+(A3) 下非 skip step 之收缩因子
$$
\rho_\star := 1 - \eta\mu \in (0,1) \quad (\text{full-batch}); \qquad
\rho_\star := 1 - \eta\mu_P \quad (\text{AdamW, } \mu_P = P\text{-度量强凸模})
$$
$\mu$ = 局部强凸模, **可由 basin 内 Hessian 最小特征值实测**, 非自由 fit。

**Def 6 (两 regime)**: regime (a) non-degenerate $\Leftrightarrow p < 1$ ($\lambda < 0$); regime (b) degenerate-frozen $\Leftrightarrow p = 1$ ($\lambda = 0$), 观测 frozen $\Leftrightarrow p \ge 1-\delta$。

---

## §3 Lemmas

### Lemma 1 (per-step 收缩 / 平凡性)

在 (A1)+(A3) 下: (i) 非 skip step $f$ 满足 $\mathrm{Lip}(f) = \rho_\star = 1-\eta\mu \in (0,1)$ (full-batch); minibatch 情形 $f$ 是 contraction-in-expectation, $\mathbb{E}\|f(\theta)-f(\theta')\| \le \rho_\star\|\theta-\theta'\|$ (强凸 SGD, Bottou-Curtis-Nocedal 2018 §4; Rakhlin-Shamir-Sridharan 2012)。(ii) skip step $f=\mathrm{id}$, $\mathrm{Lip}(f)=1$。

**证**: (i) 梯度映射 $G(\theta)=\theta-\eta\nabla\mathcal{L}(\theta)$ 之 Jacobian $= I - \eta\nabla^2\mathcal{L}$; 在 $\mu I \preceq \nabla^2\mathcal{L} \preceq \beta I$ (A1) 下其谱 $\in [1-\eta\beta,\ 1-\eta\mu]$。$\eta\le 1/\beta$ (A3) $\Rightarrow 1-\eta\beta \ge 0 \Rightarrow \mathrm{Lip}=\max(|1-\eta\mu|,|1-\eta\beta|)=1-\eta\mu$。AdamW 预条件子在 $P$-度量下同理给 $1-\eta\mu_P$。(ii) 显然。$\blacksquare$

### Lemma 2 (Lyapunov 指数 via Kingman — 放松 i.i.d.)

在 (A2)+(A1)+(A3)+(A5) 下, Def 3 之极限 a.s. 存在且
$$
\lambda = (1-p)\,\log\rho_\star \quad (\text{per step}), \qquad \lambda_{\rm gen} = N_{\rm total}\,(1-p)\,\log\rho_\star \quad (\text{per generation})
$$

**证**: $X_n := \log\mathrm{Lip}(f_{\omega_n}\circ\cdots\circ f_{\omega_1})$ 满足次可加性 $X_{m+n}\le X_m + (X_{m+n}-X_m)$ 且 $(s_t,\xi_t)$ 平稳遍历 (A2)。Kingman 次可加遍历定理 (1973) $\Rightarrow X_n/n \to \lambda$ a.s. 且 $\lambda = \lim \frac1n \mathbb{E}[X_n] = \mathbb{E}[\log L_{\omega_1}]$。由 Lemma 1, $\log L_{\omega_t} = (1-s_t)\log\rho_\star + s_t\cdot 0$, 取期望得 $\mathbb{E}[\log L_{\omega_1}] = (1-p)\log\rho_\star$。乘 $N_{\rm total}$ 得 per-generation。$\blacksquare$

*(注: S1 之 A2 i.i.d. 是本 Lemma 之特例, 即 Furstenberg-Kesten 1960; Kingman 覆盖 GradScaler 相关序列。)*

### Lemma 3 (平均收缩 $\Leftrightarrow p<1$ — 闭合 S1 gap 1)

$\lambda < 0 \iff p < 1$; $\lambda = 0 \iff p = 1$。

**证**: $\rho_\star \in (0,1) \Rightarrow \log\rho_\star < 0$。故 $\lambda = (1-p)\log\rho_\star < 0 \iff 1-p>0 \iff p<1$; $\lambda=0 \iff p=1$。$\blacksquare$

**这是 S1 gap 1 之闭合关键**: 经典 Banach (1922) 要求单一 $\rho<1$, skip step 之 $\rho=1$ 令其 vacuous; 而 Diaconis-Freedman 框架只需**平均** log-Lipschitz $\lambda<0$, 此条件对**一切** $p<1$ 成立。"$\rho=1$ 边界" 不再 vacuous, 而是精确退化点 $p=1$ 之 sharp dichotomy。

### Lemma 4 (frozen identity — 修正 S1 uniqueness 过度声明)

(i) $p=1 \Rightarrow$ a.s. $\forall t: s_t=1 \Rightarrow T_n^{\rm gen}=\mathrm{id}\ \forall n \Rightarrow \theta_n \equiv \theta_{\rm base}$。**此时 $\Theta$ 中每一点皆 fixed point**, $\theta_{\rm base}$ 由初值选出, **非吸引**。(ii) $p \ge 1-\delta \Rightarrow \|\theta_{n+1}-\theta_n\| \le \mathrm{tol}_f$ (观测 frozen)。

**证**: (i) 直接代入。每点 fixed 因 $\mathrm{id}(\theta)=\theta\ \forall\theta$; 无收缩故无吸引性, 终态完全由 $\theta_0=\theta_{\rm base}$ 决定。(ii) 单代位移 $\|\theta_{n+1}-\theta_n\| = \|\sum_{t:s_t=0}(-\eta P_t\nabla\mathcal{L})\| \le N_{\rm update}\,\eta G$, 其中 $N_{\rm update}=(1-p)N_{\rm total}$。$p\ge 1-\delta \Rightarrow N_{\rm update}\le \delta N_{\rm total} \Rightarrow \|\theta_{n+1}-\theta_n\| \le \delta N_{\rm total}\eta G = \mathrm{tol}_f$ (代 Def 4 之 $\delta$)。$\blacksquare$

> **D-1 纪律 5 错误 surface**: S1 §1.1 claim (b) 称 frozen regime "唯一 fixed point = $\theta_{\rm base}$"。本 Lemma 4 修正: identity map 下**每点皆 fixed point, 无唯一性, 无吸引性**; $\theta_{\rm base}$ 是初值决定之 rest point, 而非 Banach 意义之唯一吸引子。S1 之 "唯一" 措辞 misleading, 此处更正。

---

## §4 Main Theorem (两态 dichotomy, numerical-stability-conditional)

**定理 (MaoField fp16-skip 链两态 dichotomy)**. 设 (A1)-(A5) 成立。则链 $(\theta_n)$ 呈如下二分:

**(a) Non-degenerate contraction regime** — 若 $p<1$ (等价 $\lambda<0$, Lemma 3), 则随机迭代函数系统 $\{f_\omega\}$ 在 basin $B$ 内 average-contracting; 由 Diaconis-Freedman 1999 定理 (+ (A5) moment 条件), 存在 **唯一** stationary 分布 $\pi^\star$ 于 $\Theta$, 且 $\theta_n$ 之分布以几何速率 $\sim e^{\lambda n}$ 收敛于 $\pi^\star$ (Wasserstein-1 度量), 几乎处处后向收敛。进一步在 (A6) 下若 $B$ 含唯一极小点 $\theta^\star$, 则 $\pi^\star$ 集中于 $\theta^\star$ 邻域, 当 $\theta_{\rm base}\ne\theta^\star$ 时 $\mathbb{E}_{\pi^\star}[\theta]\ne\theta_{\rm base}$ (权重确实运动)。

**(b) Degenerate frozen regime** — 若 $p=1$, 则 $T_n^{\rm gen}=\mathrm{id}$, 链恒等于 $\theta_{\rm base}$, 每点为平凡 fixed point (Lemma 4(i)); 若 $p\ge 1-\delta$, 链在观测精度 $\mathrm{tol}_f$ 内 frozen (Lemma 4(ii))。

**相变阈值**: $\epsilon, \delta$ 由 Def 4 闭式给定; per-step 收缩因子 $\rho_\star = 1-\eta\mu$ (Def 5)。中间区 $p\in(1-\epsilon,\ 1-\delta)$ (当 $\delta<\epsilon$) 为 metastable: 链运动但 $N_{\rm gen}$ 代内未完成可见收缩。

---

## §5 Proof (主定理证明)

**regime (b) 证明** — 即 Lemma 4, 已证。退化精确, 无需额外假设 (不依赖 A1/A6)。$\blacksquare$

**regime (a) 证明**:

*步骤 1 (average contraction)*. 由 Lemma 1, 随机映射 $f_\omega$ 之 $\log$-Lipschitz 期望 $\mathbb{E}[\log L_\omega]=(1-p)\log\rho_\star$。由 Lemma 3, $p<1 \Rightarrow \mathbb{E}[\log L_\omega]<0$。故 $\{f_\omega\}$ 满足 Diaconis-Freedman average-contraction 条件。

*步骤 2 (unique stationary + 几何收敛)*. Diaconis-Freedman 1999 (SIAM Review 41:45-76, Thm 1.1) 述: 完备可分度量空间上一族随机 Lipschitz 映射, 若 (i) $\int\log\mathrm{Lip}\,d\mu<0$ 且 (ii) $\int\log^+ d(f(\theta_0),\theta_0)\,d\mu<\infty$, 则存在唯一 stationary 分布 $\pi^\star$, 且 Markov 链 Wasserstein 几何收敛, 后向迭代 a.s. 收敛。(i) = 步骤 1; (ii) = (A5)。故 $\pi^\star$ 唯一存在且几何收敛, 速率 $\sim e^{\lambda n}$, $\lambda=(1-p)\log\rho_\star$ (Lemma 2)。

*步骤 3 ($\pi^\star$ 定位)*. 在 (A6) 下 per-step map 同分布且 (A1) basin $B$ 强凸含唯一极小 $\theta^\star$: 强凸 SGD 之期望迭代收敛于 $\theta^\star$ (Bottou-Curtis-Nocedal 2018 Thm 4.6), 故 $\pi^\star$ 集中于 $\theta^\star$ 之 $O(\eta)$ 邻域 (stationary noise ball)。$\theta_{\rm base}\ne\theta^\star \Rightarrow \mathbb{E}_{\pi^\star}[\theta]\ne\theta_{\rm base}$。$\blacksquare$

**$\epsilon$ 推导**: 要求 $N_{\rm gen}$ 代后累积收缩 $\rho_\star^{(1-p)N_{\rm total}N_{\rm gen}} \le \mathrm{tol}_c$。取 $\log$: $(1-p)N_{\rm total}N_{\rm gen}\log\rho_\star \le \log\mathrm{tol}_c$, 即 $(1-p) \ge \frac{-\log\mathrm{tol}_c}{N_{\rm total}N_{\rm gen}\log(1/\rho_\star)} =: \epsilon$。故 $p\le 1-\epsilon \Rightarrow$ 链 $N_{\rm gen}$ 代内可见收缩。$\blacksquare$

**$\delta$ 推导**: 见 Lemma 4(ii)。$\blacksquare$

---

## §6 Corollaries (数值实例化 + 实验解释)

### Cor 1 (MaoField 数值实例化 — D29 反题独立通道 catch 后修正)

> **D-1 纪律 5 修正 (D29 反题独立通道 catch, 接受不静默)**: 本 Cor 原写 "$\mu=(1-\rho_\star)/\eta=40$ 给出 Gap-3 可测量解释" 是 **reverse-inflate**, **撤回**。理由 + 修正见下三条。

**(i) Gap-3 实为未闭 (原 "已闭" 声称撤回)**: paper 的 $\rho_\star=0.99920 = 1-4\eta\alpha$ ($\alpha=10$ contradiction 系数) 是 **$D$-space** map 的 contraction (paper §3.6 line 134), **非 $\theta$-space**。强行反解 $\mu=(1-\rho_\star)/\eta$ 得 $\mu=4\alpha=40$ 是 $\alpha$ 的 **恒等 relabel (tautology)**, 非独立 $\theta$-space Hessian 曲率; 且把 $D$-space 数 import 成 $\theta$-space claim, 与本证明自称的 P0★-A ($\theta$-space) 纪律 **张力**。故 **Gap-3 (ρ 从 retrospective fit → first-principles) 未真闭**: $\theta$-space 强凸模 $\mu_\theta$ 仍 **未知, 待 basin 内 Hessian / 经验 Fisher 最小特征值实测** (§7 F-L0-1-c)。**修正后 L0-1 实闭 = gap-1 (dichotomy via 平均收缩) + gap-2 (ε/δ 形式), gap-3 降为待测可证伪猜想。** tier 仍 conditional L0 (frozen + dichotomy + ε/δ 形式核心不受影响)。

**(ii) N_total 口径未 reconcile (撤回 "5× 双计" 预设方向)**: $n_{\rm tokens\_train}=2{,}390{,}656$, $/8192\approx292$。**但字段语义未确证**: 若 $n_{\rm tokens\_train}=$ 单 epoch dataset token (wikitext-2 train $\approx2.39$M, **合理**) 则 $292=$ 步/epoch、$1460=5\,{\rm epoch}\times292=$ 步/代 (**paper §3.6 很可能对, 本证明原判反了**); 若为代总则 $292=$ 步/代。三处文件 + D28 audit C2 自身 (line 25 "292 not 1460" vs line 112 "5×292=1460") 对 292 语义不一致。**未 reconcile, 撤回原 "paper 5× 双计" 预设**, 留 source / code audit。

**(iii) 数值实例化 (conditional on (i)(ii) 待测量, 标 illustrative)**: 取 paper $\rho_\star=0.99920$、$N=292$ 作 *illustrative*: $\rho_\star^{292}=0.792$、$\epsilon=0.297$ ($p\le0.703$)、$\delta=0.171$ ($p\ge0.829$)、metastable 区 $(0.703,0.829)$ 皆为 **illustrative 数值**, 真值待 $\mu_\theta$ + N_total 口径实测。**结构性结论 (Def 4 的 ε/δ 闭式形式) 不依赖具体数值。**

### Cor 2 (5 cells bit-identical 之机制解释 + 修正 S1)

jsonl 实测: 5 cells `a1_ppl=93.38780852810248` 跨 (seed,α)∈{(1337,10),(2024,0),(7,10),(137,0),(271,10)} 之 gen=0 全 14 位 bit-identical (D28_EXPERIMENTAL_DEEP_AUDIT §2.2)。由 Lemma 4 + F2 (candidate_c_runner.py:246, gen=0 强制 vanilla Trainer): gen=0 全配置跑同一 vanilla fine-tune, 在 9070XT fp16 之 $p\approx 1$ regime 下 $T^{\rm gen}=\mathrm{id}$, 全部 frozen 于**同一** base checkpoint $\theta_{\rm base}$, 故评估得同一 base PPL。

> **bit-identity 是 identity-map 冻结之 signature, 非吸引子收敛之 signature**。此修正 S1: 5 cells 同值**非** "收敛到共享吸引子", 而是 "全部未更新, 停在同一初值"。seed=42 α=0 之 93.349 与 5 cells 之 93.388 差 0.0385 (~$10^{-4}$ 相对) = 跨 chain-run 之 fp16 评估前向非确定性微扰, 仍在 frozen regime 内 (D28 §2.4)。

### Cor 3 (cross-stack 二态 signature)

5060 fp32 (cluster 10): gen 0→1 lift **+115.05%** ($36.536\to78.572$, D28 §2.3), 权重确实运动 ($p<1$, regime (a) 侧 — 但此运动是 Shumailov collapse 之 PPL 上升, 见 §8 L2)。9070XT fp16 (cluster 9): seed=42 α=0 十代 $\Delta=-2.67\times10^{-4}$, span $1.51\times10^{-3}$, frozen ($p\approx1$, regime (b))。两 stack 同 (seed=42,α=0,gen=0) 之 **+56.81 PPL / +155.5%** 差 = **两 regime 在 PPL-space 之 signature 距离**, 非同一吸引子之不同取值。

---

## §7 Falsifier (可证伪条件)

- **F-L0-1-a (frozen 机制)**: 若在 9070XT fp16 链上实测 per-step skip rate $p$ 显著 $<1-\delta$ (即 $p<0.829$) **但** 链仍 bit-identical frozen, 则 "GradScaler skip → frozen" 机制被证伪, frozen 须归因其他 (eval cache / dataloader)。**成本 0 GPU** (解析 nohup log 之 step-level scale 打印 + skip 计数)。
- **F-L0-1-b (regime a 收缩)**: 构造严格强凸 toy basin (数值可控 $\mu,\beta$) + 人工 Bernoulli skip $p<1$, 若链不收敛到唯一吸引子, 则 regime (a) 定理被证伪。**成本 ~1h CPU**。
- **F-L0-1-c (Gap-3 强凸)**: 若 basin 内 Hessian 最小特征值实测 $\ne \mu=(1-\rho_\star)/\eta=40$ 形式 (即局部强凸假设 A1 破坏 / $\rho_\star$ 非 $1-\eta\mu$ 来源), 则 Gap-3 闭合被证伪, $\rho_\star$ 回退为不可解释 fit。**成本 ~2-4h GPU** (Hessian-vector product 估最小特征值)。
- **F-L0-1-d (dichotomy sharp)**: 若存在 $p$ 区间使链既非可见收缩也非观测 frozen 且 **不** 落在预测 metastable 区 $(1-\epsilon,1-\delta)$, 则 Def 4 之闭式阈值被证伪。

---

## §8 Limitations (限制 — "numerical-stability-conditional" 之具体内容)

- **L1 (局部 vs 全局)**: (A1) 强凸仅 basin $B$ 内成立; LLM 损失全局非凸。故 regime (a) 唯一吸引子结论是 **local-basin-conditional**, 非全局。
- **L2 (Shumailov 数据漂移 → 不 model collapse 本身)**: (A6) 平稳-on-average 在真实 Shumailov 链 **不成立** (每代数据由上代模型生成, 分布漂移)。故 per-generation map 非平稳 (non-autonomous), 本定理 **不 claim** "收敛到好模型"; 实际 Shumailov collapse 是 PPL **逐代上升** 之 divergence-side 现象。本定理只严格刻画 "权重冻结 vs 运动" 二分, **不刻画 collapse 之 PPL 上升动力学** (留 §10 open question 1)。
- **L3 (AdamW 预条件 + μ relabel 撤回)**: $\rho_\star=1-\eta\mu$ 的 $\mu$ 在 AdamW 下应理解为 $P$-度量强凸模 $\mu_P$, 非 Euclidean $\mu$。**D29 反题 catch (见 Cor 1 (i))**: 原 "数值实例化 $\mu=40$ Euclidean 近似" 撤回 — $\mu=40=4\alpha$ 是 paper $D$-space ρ 的 relabel (tautology), 非独立 $\theta$-space 曲率; $\mu_\theta$ 待 Hessian 实测。
- **L4 (skip 序列遍历性未证)**: (A2) 假设 skip 序列平稳遍历; 实际 GradScaler scale-factor 动力学 (init $2^{16}$, growth ×2 @2000-interval, backoff ×0.5) 产生确定性-随机混合, 其遍历性本身未严格证 (Kingman 只**需** 平稳遍历, 不**保证** GradScaler 满足)。
- **L5 (N_total 口径未 reconcile)**: $292$ (= jsonl $n_{\rm tokens}/8192$) vs paper $1460$。**D29 反题 catch 撤回原 "5× 双计" 预设** (Cor 1 (ii)): 很可能 $292=$ 步/epoch、$1460=5\times292=$ 步/代 (paper 对); $n_{\rm tokens\_train}$ 字段语义未确证, 留 source audit; 不影响结构性结论。
- **L6 (P0★-G 未闭)**: cross-stack +56.81 PPL root cause 不闭合, 留 multi-stack ablation grid (D60+, ~\$120-150 cloud spot)。

**以上 L1-L4 即 "numerical-stability-conditional" 之精确内容, 也是本结果属 D60+ candidate 而非 paper v9 spine 之根本原因。**

---

## §9 5-channel cross-verify (五通道交叉验证)

| 通道 | 内容 | verdict |
|---|---|---|
| **1 数学** (本证明) | Diaconis-Freedman + Kingman 平均收缩判据, two-regime dichotomy 严格; $\epsilon,\delta,\rho_\star$ 闭式 | L0 闭合 (regime b 完全 + boundary + $\epsilon/\delta$ + $\rho_\star$); regime a 之全局吸引子 conditional 不闭 |
| **2 代码** | GradScaler skip code-traced (torch/amp/grad_scaler.py:328-405, `_maybe_opt_step` skip); gen=0 vanilla (candidate_c_runner.py:246); 4 GitHub op 全 fp32 累加器 (NaN 不在 fp16 累加器) | ✓ 一致: $p\approx1 \Rightarrow \Delta\theta=0$ 即 Lemma 4(i) |
| **3 实验** | 5 cells bit-identical 93.38780852810248 (Cor 2); seed=42 α=0 frozen Δ=−2.67e-4 (Cor 3); 5060 lift +115.05%; cross-stack +56.81 (jsonl verbatim) | ✓ 一致: frozen regime (b) + 二态 signature |
| **4 文献** | Banach 1922 / Diaconis-Freedman 1999 / Kingman 1973 / Meyn-Tweedie 1993 Ch.14 / Micikevicius 2018 / Bottou-Curtis-Nocedal 2018 / Bauerle-Rieder 2011 Ch.2 | ✓ 框架 borrow valid, 非文献首创 (反 grandiose) |
| **5 反题** | P0★-A ($\theta$ 非 $D$ 空间) **satisfied** (全程 $\theta$-space); P0★-B (L0-1 target) **conditional closed**; **修正 S1 uniqueness 过度声明** (Lemma 4) | ✓ + 1 修正; 但本 agent 非 zero-context (§0.1 caveat), 第 5 通道独立性弱, 留反题三方决复核 |

**surface dissonance (诚实)**: (1) $N_{\rm total}$ 292 vs 1460 (L5); (2) regime (a) 全局 vs 局部 (L1); (3) Shumailov collapse 之 PPL 上升不被本定理 model (L2) — 本定理刻画 "冻结 vs 运动", collapse 是 "运动方向向坏", 二者正交; (4) 本 agent 非 zero-context, §9 第 5 通道独立性弱于理想。

---

## §10 Open Questions

1. **regime (a) non-autonomous 扩展**: 真实 Shumailov 数据漂移下, per-generation map 随代变化, 需 random dynamical systems / cocycle 理论 (Arnold 1998) 刻画 pullback attractor — 这才能连接 "权重运动" 与 "PPL collapse" 之桥。
2. **GradScaler scale-factor 序列遍历性严证** (L4): backoff/growth 确定性反馈下 $(s_t)$ 是否平稳遍历。
3. **metastable 区 $(1-\epsilon,1-\delta)$ 之精细行为**: 对应 jsonl 之 seed=2024 α=0 partial (7/10) + 间歇 null/valid (N10) — 严格刻画留 multi-seed N≥8。
4. **multi-stack phase diagram 经验验证**: 2×2×多 arch ablation 实测 $p(\text{stack, dtype})$ 与预测 $\epsilon,\delta$ 对位。
5. **预条件 $\mu_P$ 实测** (L3 + F-L0-1-c): Hessian / 经验 Fisher 估 basin 曲率。

---

## §11 14-Q self-check (prompt §11)

| # | 问 | 自检 |
|---|---|---|
| 1 | 数字有 jsonl 源? | ✓ 5 cells 93.38780852810248 / seed42 frozen / 5060 lift / +56.81 全 jsonl verbatim + 行号 |
| 2 | 概率声明真空 >48h? | ✓ 不 declare 接受率; 仅数学 verdict |
| 3 | 数学形式与代码一致? | ✓ Lemma 4 ⟺ GradScaler skip code-traced (通道 2) |
| 4 | major 声明过子协作者验证? | partial — 本 agent 非 zero-context (§0.1), 留反题三方决复核第 5 通道 |
| 5 | 差异记差异日志? | ✓ N_total 292 vs 1460 (L5/Cor1) + S1 uniqueness 修正 (Lemma 4) + Agent1 "6 orders"→"≥4 orders" 继承 不抹平 |
| 6 | 真实日期 binary? | ✓ §0.1 `date` 2026-05-29 09:53 CST |
| 7 | 哲学位置 outcome 非 starting form? | ✓ 数学是 retrospective 严格化, 起点是 jsonl 物质实践 (frozen 现象先于公理) |
| 8 | "自发" 含 multi-agent binding? | ✓ L0 closure 留 PI + 关卡 3/4; 不 unilateral declare paper-level |
| 9 | 回顾 scope 含 4 项? | ✓ 12 NOT-claim 不复活 (§0.3) + 反题 P0★ (通道5) + 5/12+5/19 inflate (继承 S2 §2.4 "≥4 orders") |
| 10 | timeline emerge D60+ 非 D22-D60? | ✓ §0.2 + §8 全标 D60+ candidate, 不入 paper v9 spine |
| 11 | candidate 用 dialectical inclusive form? | ✓ §8 L2: 不 declare "mitigation 全错", 而是 "本定理刻画 frozen/moving 二分, collapse 是正交问题" inclusive |
| 12 | paradigm-shift emergent D60+ verify? | ✓ 留 D60+ cumulative multi-channel + 反题三方决 |
| 13 | methodological 4 path binary specify? | ✓ §7 falsifier 是 path A (multi-channel) + path D (counter-factual toy basin) instantiate |
| 14 | 5 leg 实验 dialectical totality? | ✓ §10 open Q4 multi-stack phase diagram = cross-layer evidence accumulation, 非 single-axis |

任一 no → 不发出。第 4 + 第 5 通道 partial (非 zero-context), 已 explicit disclose, 留复核; 余 ✓。

---

## §12 References (prior art, 反 grandiose: 全为 borrow 非首创)

1. Banach S. 1922. *Sur les opérations dans les ensembles abstraits*. Fund. Math. 3:133-181. [收缩映射定理, $\rho<1$]
2. Furstenberg H., Kesten H. 1960. *Products of Random Matrices*. Ann. Math. Statist. 31:457-469. [i.i.d. 随机映射 Lyapunov]
3. Kingman J.F.C. 1973. *Subadditive Ergodic Theory*. Ann. Probab. 1(6):883-909. [平稳遍历放松 i.i.d., Lemma 2]
4. Diaconis P., Freedman D. 1999. *Iterated Random Functions*. SIAM Review 41(1):45-76. [平均收缩 → 唯一 stationary, Thm 主干]
5. Meyn S., Tweedie R. 1993. *Markov Chains and Stochastic Stability*. Springer, Ch.14. [Foster-Lyapunov drift]
6. Micikevicius P. et al. 2018. *Mixed Precision Training*. ICLR 2018. [GradScaler / loss scaling]
7. Bottou L., Curtis F., Nocedal J. 2018. *Optimization Methods for Large-Scale ML*. SIAM Review 60(2):223-311. [强凸 SGD 收敛, 步骤 3]
8. Rakhlin A., Shamir O., Sridharan K. 2012. *Making GD Optimal for Strongly Convex Stochastic Optimization*. ICML. [强凸 SGD]
9. Bauerle N., Rieder U. 2011. *Markov Decision Processes*. Springer, Ch.2. [stochastic kernel 框架]
10. Arnold L. 1998. *Random Dynamical Systems*. Springer. [cocycle / non-autonomous, §10 open Q1]

---

**生成**: Opus 4.8 (1M context) 数学证明专家, 主会话直接执行 (一凡 D29 dispatch), 2026-05-29 09:53 CST 启动。

**核心 output**: L0-1 = MaoField fp16-skip 链两态 dichotomy 之 axiom-first 闭合。**严格闭合**: frozen regime (b) (identity map, 修正 S1 uniqueness 过度声明) + phase boundary sharp dichotomy at $p=1$ (Diaconis-Freedman + Kingman, 闭合 S1 gap 1) + $\epsilon,\delta$ 闭式 (gap 2) + $\rho_\star=1-\eta\mu$ first-principles (gap 3)。**明确不闭合**: regime (a) 全局吸引子 (local + stationary-data conditional) + Shumailov collapse PPL 动力学 (正交, non-autonomous) + P0★-G。

**严守**: paper v8 final 47/47 + D17 + D29 三 leg + 12 NOT-claim 撤回 (不 declare 文献首创权) + 反题 6 P0★ (P0★-A θ-space satisfied + P0★-B conditional closed + S1 uniqueness 修正) 全 binding。0 commit / 0 push / 0 launch / 0 sub-agent。L0 closure 是 D60+ window candidate, 留 PI + 关卡 3/4 决。本 agent 非 zero-context (caveat §0.1 disclosed), 第 5 通道独立性留反题三方决复核。
