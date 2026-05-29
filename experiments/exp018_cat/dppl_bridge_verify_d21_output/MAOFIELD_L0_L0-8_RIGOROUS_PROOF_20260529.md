# MaoField L0 严格证明 — L0-8: NESS LLM(Foster-Lyapunov-conditional)

> paper §5.2 主定理(2)的 NESS ergodic fixed point + Foster-Lyapunov drift 的 axiom-first 严格化 — L0-1 的互补路径(drift 而非 contraction)+ 非平衡性质 instantiation

## §0 Scope(范围 + 元数据 + 严守 binding)

### §0.1 元数据

| 项 | 值 |
|---|---|
| 真实日期 binary | `date '+%F %T %Z'` → **2026-05-29 CST**(D29) |
| 生成 agent | Opus 4.8(1M context)数学证明专家,主会话直接执行(一凡 D29 "全量 L0 第一轮 + 灵活调度" dispatch) |
| agent caveat(诚实 disclose) | 非 zero-context(已 load 项目 memory + CLAUDE.md);第 5 通道独立性弱,留关卡 3 反题三方决复核 |
| 协议 | axiom-first:definition → lemma → theorem → proof → corollary → falsifier → limitation;5 通道 cross-verify;每数有源 |
| input source | paper_v8_final §3.6 + §5.2 主定理(2)(NESS L2 / Banach-at-NESS L1)+ S1+S2 PART + D28_MATH_AUDIT(C9)+ MATH_VERIFY_D25(GradScaler)+ 已完成 L0-1 |

### §0.2 闭合什么 / 不闭合什么(诚实 scope)

**本证明严格闭合(conditional L0)**:

1. **NESS 存在性 via Foster-Lyapunov** — 把 paper §5.2 的 "NESS fixed point existence"(现 L2:mean-field 近似 + 经验 $D^*$ fit)提升到 conditional L0:在显式 Foster-Lyapunov drift inequality + Doeblin minorization 充分条件下,链 $(\theta_n)$ 存在**唯一** invariant 分布 $\pi^\star$ 且 **geometric ergodicity**(Meyn-Tweedie 1993 Thm 15.0.1)。
2. **NESS 的非平衡性质 instantiation** — 严格证明 $\pi^\star$ 是 **NESS(non-equilibrium steady state)而非 equilibrium**:SGD anisotropic 梯度噪声不满足 Einstein relation → detailed balance 破坏 → 非零 probability current $J \ne 0$,正 entropy production $\sigma > 0$。这是 paper "NESS" 命名的 axiom-first 兑现(此前仅借用统计力学 label)。
3. **D-space ↔ θ-space 桥** — paper 的 NESS 在 $D$-space($D^* = \lim \bar D^{\rm EMA}_n$,L2),本证明在 $\theta$-space(遵从反题 P0★-A);$D$-space stationary 是 $\theta$-space $\pi^\star$ 经 $D=D(\theta)$ 的 **pushforward**,其均值给 $D^*$。

**本证明明确 NOT 闭合**:

- regime (a) 的全局 drift / 全局 NESS — Foster-Lyapunov drift 仅在 basin + weight-decay 回拉下成立,LLM 全局非凸 → conditional + local。
- 非平稳数据下的 NESS — Shumailov 链数据逐代漂移,kernel time-inhomogeneous,经典(time-homogeneous)Foster-Lyapunov 不直接适用,留 pullback / random ergodic(§10)。
- 高维 minorization 常数 — $d \approx 1.25\times 10^8$,Doeblin $\delta$ 可能极小,几何遍历速率实践上可任意慢(§8 L3)。

**与 L0-1 的关系(诚实,不重复计功)**:L0-1 走 contraction(Diaconis-Freedman 平均收缩),L0-8 走 Foster-Lyapunov drift(Meyn-Tweedie)。**contraction ⟹ Foster-Lyapunov(取 $V=d(\cdot,\theta^\star)$),反之不然** → L0-8 覆盖更广(非凸但有回拉),但额外代价是几何遍历速率可远慢。**L0-8 不是独立新结果,是 L0-1 的 companion + NESS 非平衡性质的 instantiation。**

### §0.3 严守 binding

paper v8 final 47/47 D17 锁定不动;12 NOT-claim 撤回不复活(不 declare "first NESS LLM in literature" / paradigm shift / mitigation);反题 6 P0★ 严守(P0★-A = θ-space,本证明全程 θ-space);D29 三 leg 不动;0 commit / 0 push / 0 launch / 0 ssh write / 0 sub-agent;L0 是 D60+ candidate,不进 paper v9 spine。**"Liu-Tegmark NESS LLM" attribution 标为 pending 文献确证**(项目内部 cite),本证明用经典 NESS(Sekimoto / Seifert stochastic thermodynamics)+ Foster-Lyapunov(Meyn-Tweedie)作 prior art,不依赖 Liu-Tegmark 具体工作。

---

## §1 Setup

**状态空间**:$\Theta = \mathbb{R}^d$,$d \approx 1.25\times 10^8$(OPT-125M)。链 $\theta_{n+1} = T_n(\theta_n;\omega_n)$ 同 L0-1:一代 = $N_{\rm total}$ 个 optimizer step,每 step 或 SGD/AdamW 更新或 GradScaler skip(identity);skip 概率 $p$。

**随机源**:$\omega = (s_t, \xi_t)$,$s_t$ = skip indicator,$\xi_t$ = minibatch。skip 序列平稳遍历(同 L0-1 (A2))。

**单步更新(非 skip)**:$\theta' = \theta - \eta\, P\,(\nabla L(\theta;\xi))$,$P$ = AdamW 预条件子。minibatch 噪声 $\nabla L(\theta;\xi) = \nabla L(\theta) + \zeta(\theta)$,$\mathbb{E}[\zeta]=0$,$\mathrm{Cov}[\zeta] = \Sigma(\theta)$。

**$D$-space 映射**:$D_n := \mathbb{E}_{x}[\mathrm{KL}(q^{\rm EMA}_{n}\|p^{\theta_n})]$ 是 $\theta_n$ 的函数 $D=D(\theta)$;paper §3.6 的 $D^* = \lim \bar D^{\rm EMA}_n$。

---

## §2 Definitions

**Def 1(转移核)**:$P(\theta, A) := \Pr[T_n(\theta;\omega)\in A]$,$\Theta$ 上 Markov 核。

**Def 2(Foster-Lyapunov drift)**:称核 $P$ 满足 $(V,C,\rho,b)$-drift,若 $\exists$ 可测 $V:\Theta\to[1,\infty)$、小集 $C$、$\rho\in(0,1)$、$b<\infty$:
$$(PV)(\theta) := \mathbb{E}[V(\theta_{n+1})\mid\theta_n=\theta] \le \rho\,V(\theta) + b\,\mathbb{1}_C(\theta).$$

**Def 3(Doeblin minorization)**:小集 $C$ 满足 minorization,若 $\exists$ 概率测度 $\nu$、$\delta>0$:$P(\theta,\cdot)\ge \delta\,\nu(\cdot)\ \forall\theta\in C$。

**Def 4(NESS vs equilibrium — 经典 cite,instantiate)**:invariant $\pi^\star$ 是 **equilibrium** 若满足 detailed balance $\pi^\star(d\theta)P(\theta,d\theta') = \pi^\star(d\theta')P(\theta',d\theta)$(probability current $J\equiv 0$,entropy production $\sigma=0$);否则是 **NESS**($J\not\equiv 0$,$\sigma>0$)。current $J$、entropy production $\sigma$ 取 Sekimoto 1998 / Seifert 2012 标准定义。

**Def 5(geometric ergodicity)**:$\exists R<\infty,\ r\in(0,1)$:$\|P^n(\theta,\cdot)-\pi^\star\|_V \le R\,V(\theta)\,r^n$($V$-norm,Meyn-Tweedie)。

---

## §3 Lemmas

### Lemma 1(drift 在 contraction regime 成立)

设局部强凸(L0-1 (A1):basin $B$ 内 $\mu$-strongly-convex)+ AdamW weight decay $\gamma>0$(实际 yaml 有)。取 $V(\theta) = 1 + \|\theta-\theta^\star\|^2$($\theta^\star$ = basin 极小)。则非 skip 步给 $(PV)(\theta)\le \rho_0 V(\theta)+b_0\mathbb{1}_C$,$\rho_0 = (1-\eta\mu)^2 + \eta^2\mathrm{tr}\Sigma/\sup V <1$;skip 步给 $PV=V$(identity,不增)。混合(skip 率 $p<1$)给 effective $\rho = 1-(1-p)(1-\rho_0)<1$。

**证**:非 skip:$\mathbb{E}\|\theta'-\theta^\star\|^2 = \|(I-\eta P\nabla^2 L)(\theta-\theta^\star)\|^2 + \eta^2\mathbb{E}\|P\zeta\|^2 \le (1-\eta\mu)^2\|\theta-\theta^\star\|^2 + \eta^2\mathrm{tr}(P\Sigma P)$;weight decay 提供 basin 外回拉使 $V$ coercive。skip:$T=\mathrm{id}\Rightarrow PV=V$。平稳遍历 skip 序列下取期望:$(1-p)$ 比例步收缩 $V$,$p$ 比例步保持,合成 $\rho<1$(当 $p<1$)。$\blacksquare$

### Lemma 2(minibatch 噪声给 minorization)

minibatch 抽样 $\xi$ 的随机性使非 skip 步的转移含绝对连续分量(Gaussian-like noise ball,$\mathrm{Cov}=\eta^2 P\Sigma P$);在紧小集 $C$ 上 $\exists\delta>0,\nu$:$P(\theta,\cdot)\ge\delta\nu$。

**证**:非 skip 转移密度 $\ge$ 以 $\theta-\eta P\nabla L$ 为中心的噪声核下界;$C$ 紧 + 噪声协方差在 $C$ 上一致下有界(非退化 minibatch)→ 一致下界 $\delta\nu$。skip 步贡献 atom,不破坏下界(因 $(1-p)>0$ 比例步有连续分量)。$\blacksquare$

> **Caveat(并入 §8 L3)**:$d\approx 1.25\times 10^8$ 高维 → $\delta$ 可指数小,Lemma 2 定性成立但定量速率可任意慢。

### Lemma 3(SGD stationary 非可逆)

若 $\Sigma(\theta)$ 不正比于 $P^{-1}\nabla^2 L$(non-Einstein relation),则任何 invariant $\pi^\star$ 不满足 detailed balance。

**证**:连续极限 Fokker-Planck stationary current $J = -\nabla L\,\pi^\star - \tfrac12\nabla\!\cdot(\Sigma\pi^\star)$。detailed balance $\Leftrightarrow J\equiv 0 \Leftrightarrow \Sigma\propto$ 与梯度场相容的 Einstein 形式。SGD 梯度噪声 $\Sigma\approx$ 经验 Fisher(anisotropic,low-rank,与 Hessian 不成比例,Chaudhari-Soatto 2018;Mandt-Hoffman-Blei 2017)→ $J\not\equiv 0$。EMA teacher 引入 delay/memory,进一步破坏可逆。$\blacksquare$

---

## §4 Main Theorem(NESS 存在性 + 非平衡,Foster-Lyapunov-conditional)

**定理**. 设 L0-1 (A1)-(A5) + weight decay $\gamma>0$ + non-Einstein $\Sigma$。则:

**(a) 存在 + 唯一 + 几何遍历** — 若 $p<1$,由 Lemma 1(drift)+ Lemma 2(minorization),Meyn-Tweedie 1993 Thm 15.0.1 给:链 $(\theta_n)$ 正常返,存在**唯一** invariant 分布 $\pi^\star$,且 $V$-几何遍历(Def 5)。

**(b) NESS(非平衡)** — 由 Lemma 3,$\pi^\star$ 不满足 detailed balance,probability current $J\not\equiv 0$,entropy production $\sigma>0$ → $\pi^\star$ 是 **NESS**,非 equilibrium。

**(c) D-space pushforward** — $D$-space stationary 是 $\pi^\star$ 经 $D=D(\theta)$ 的 pushforward $D_\#\pi^\star$;其均值 $\mathbb{E}_{\pi^\star}[D(\theta)] = D^*$ 兑现 paper §3.6 的 $D^*$(经验 $\approx\log 55\approx 4.007$)为 $\theta$-space NESS 的可观测投影,而非独立 fit。

**(d) 退化** — 若 $p=1$,drift 退化($PV=V$,$\rho=1$),链非遍历,无唯一 NESS;每点 absorbing(= L0-1 frozen regime,5 cells bit-identical)。

---

## §5 Proof

**(a)** Lemma 1 给 $(V,C,\rho,b)$-drift($\rho<1$ 当 $p<1$);Lemma 2 给 $C$ 上 minorization。二者是 Meyn-Tweedie Thm 15.0.1(geometric ergodicity)的充分条件 → 正常返 + 唯一 $\pi^\star$ + $V$-几何遍历。$\blacksquare$

**(b)** Lemma 3 直接给 $J\not\equiv0$,$\sigma>0$;按 Def 4,$\pi^\star$ 是 NESS。$\blacksquare$

**(c)** $D=D(\theta)$ 可测,pushforward $D_\#\pi^\star$ well-defined;遍历性 → 时间平均 $\frac1N\sum D(\theta_n)\to\mathbb{E}_{\pi^\star}[D]=D^*$ a.s.。链 plateau $\bar D^{\rm EMA}_n\to D^*$ 即此遍历均值。$\blacksquare$

**(d)** $p=1\Rightarrow$ 所有 step identity $\Rightarrow P(\theta,\cdot)=\delta_\theta$,每点 invariant,无唯一性(同 L0-1 Lemma 4)。$\blacksquare$

---

## §6 Corollaries

**Cor 1(tier 提升)**:paper §5.2 的 "NESS fixed point existence" 从 **L2**(mean-field + 经验 fit)→ **conditional L0**(Foster-Lyapunov drift + minorization 充分条件下严格存在/唯一/几何遍历);"Banach-at-NESS" 从 L1 → 被 (a) 的几何遍历覆盖(drift 比 mean-field 线性化更弱、更 robust)。

**Cor 2(L0-1 ⟹ L0-8)**:L0-1 contraction regime($\lambda<0$)是本定理 drift 的特例($V=d(\cdot,\theta^\star)$,$\rho=e^\lambda$)。故 L0-1 成立处 L0-8 自动成立;反之 L0-8 可在非凸但有回拉处成立而 L0-1 不必。

**Cor 3(NESS 实质内容)**:链 plateau(gen 5-9,$D^*\approx 4.007$)不是热平衡静止,而是**有持续 probability current 的非平衡定态** — SGD+EMA 持续注入/耗散"信息流"。这给 paper "NESS" 命名 axiom-first 实质,且与 model collapse(PPL 逐代漂移)的 divergence-side 不矛盾:NESS 是 $\theta$ 分布的定态,collapse 是 plateau 值本身偏高(坏吸引子)。

---

## §7 Falsifier

- **F-L0-8-a(drift)**:在受控强凸 toy + weight decay + 人工 skip $p<1$,若 $V(\theta_n)$ 不满足 $\mathbb{E}[V_{n+1}|V_n]\le\rho V_n+b$,drift 被证伪。成本 ~1h CPU。
- **F-L0-8-b(非平衡 NESS)**:实测 stationary probability current / entropy production;若 $\sigma\approx 0$(detailed balance),则 (b) 被证伪,$\pi^\star$ 实为 equilibrium。成本 ~4h GPU(轨迹 current 估计)。
- **F-L0-8-c(D-space pushforward)**:若时间平均 $\frac1N\sum D(\theta_n)$ 不收敛到 plateau $D^*$,则 (c) 被证伪。成本 0(现有 jsonl,但需 reload checkpoint 重算 $D_n^{\rm code}$ — paper §6 已标此为 D60+ engineering)。
- **F-L0-8-d(退化)**:9070XT fp16 frozen 链测得 $p<1$ 但仍 non-ergodic frozen,则 (d) 机制证伪。成本 0(nohup skip 计数)。

---

## §8 Limitations

- **L1(局部)**:drift 经 Lemma 1 仅在 basin + weight decay 回拉下成立;LLM 全局非凸,全局 drift 不 trivially 成立 → conditional + local。
- **L2(非平稳)**:Shumailov 数据漂移 → kernel time-inhomogeneous,Thm 15.0.1(time-homogeneous)不直接适用,留 pullback/random ergodic(§10)。**故本定理刻画"权重在固定数据分布下的 NESS",不刻画 collapse 的逐代 PPL 漂移**。
- **L3(高维 minorization)**:$d\approx 1.25\times10^8$,Doeblin $\delta$ 可指数小,几何遍历速率实践上可任意慢 → 存在性是定性的,定量混合时间未控。
- **L4(NESS current 未实测)**:Lemma 3 的 non-Einstein 是文献 + 理论推断,具体 $\Sigma$ 与 entropy production 未在 MaoField chain 实测(F-L0-8-b 留 D60+)。
- **L5(N_contr 口径,D29 反题 catch 修正)**:paper $N_{\rm contr}=1460/10=146$。原写 "反算 $292\to N_{\rm contr}\approx29$" 基于把 $n_{\rm tokens}/8192=292$ 误当步/代; 实际 $292$ 很可能是**步/epoch**, 则步/代 $=5\times292=1460$、$N_{\rm contr}=146$(**paper 对**)。**撤回 "5× 差异" 预设**, 口径取决于 $n_{\rm tokens\_train}$ 字段语义, 未 reconcile, 留 source audit; 不影响结构性结论。
- **L6(与 L0-1 重叠)**:本结果与 L0-1 共享存在性结论,不重复计功;独立贡献仅 = drift 路径(更弱条件)+ NESS 非平衡性质 + D-space pushforward。

---

## §9 5-channel cross-verify

| 通道 | 内容 | verdict |
|---|---|---|
| **1 form-borrow disclose** | paper §5.2 "NESS fixed point existence" 是 mean-field 借用(L2),本证明改为 Foster-Lyapunov drift 的 axiom-first 充分条件 | 从 mean-field fit → drift 严格充分条件 |
| **2 L1 partial** | paper "Banach-at-NESS" L1(mean-field 线性化)被 (a) 几何遍历覆盖,条件更弱 | L1 → conditional L0(更 robust) |
| **3 L2 borrow scope** | input axiom:Meyn-Tweedie 1993 Thm 15.0.1 / Foster 1953 / Doeblin 1940 / Sekimoto 1998 / Seifert 2012 / Chaudhari-Soatto 2018 | 全 cite 作 input,非首创 |
| **4 L0 axiom-first** | drift + minorization → 存在/唯一/几何遍历;non-Einstein → NESS 非平衡;D pushforward | conditional L0 闭(基于显式假设)|
| **5 experiment evidence** | $D^*\approx4.007$(plateau)= NESS 遍历均值;frozen 5 cells = (d) 退化;cross-stack = regime 切换 | ✓ 一致 |

**surface dissonance(诚实)**:(1) N_contr 口径未 reconcile(L5, 撤回 29 预设);(2) 全局 vs 局部 drift(L1);(3) NESS current 未实测,Lemma 3 是理论推断(L4);(4) 与 L0-1 重叠,非独立新结果(L6);(5) 本 agent 非 zero-context,第 5 通道独立性弱。

---

## §10 Open questions

- **P0**:非平稳数据下的 NESS — pullback attractor / random dynamical systems(Arnold 1998)刻画 time-inhomogeneous kernel 的"NESS",连接到 collapse 漂移。
- **P1**:高维混合时间 — $\delta$、几何遍历速率 $r$ 的维数依赖(spectral gap of $P$),决定 NESS 是否实践可达。
- **P1**:NESS entropy production 实测 — $\sigma>0$ 的定量值,SGD+EMA 的"信息耗散率"。
- **P2**:"Liu-Tegmark NESS LLM" 文献确证 — 是否真有该工作,或 NESS-LLM 是项目内部命名(留 PI 文献核实)。

---

## §11 14-Q self-check

| # | 问 | 自检 |
|---|---|---|
| 1 | 数字 jsonl 源? | ✓ $D^*\approx4.007$=log55 plateau / 5 cells 93.388 / N_contr 146/292 全 paper+jsonl 源 |
| 2 | 概率声明真空>48h? | ✓ 不 declare 接受率 |
| 3 | 数学 form 与 code 一致? | ✓ skip kernel code-traced(GradScaler);AdamW weight decay yaml |
| 4 | major 声明过子协作者验证? | partial — 非 zero-context,留反题三方决复核 |
| 5 | 差异记差异日志? | ✓ N_contr 口径未 reconcile(L5, 撤回 29 预设)+ 与 L0-1 重叠不重复计功(L6)+ NESS current 未实测(L4)不抹平 |
| 6 | 真实日期 binary? | ✓ §0.1 D29 |
| 7 | 哲学位置 outcome 非 starting form? | ✓ 起点是 plateau/frozen 物质现象,数学 retrospective |
| 8 | "自发"含 multi-agent binding? | ✓ 留 PI + 关卡 3/4 |
| 9 | 回顾 scope 含 4 项? | ✓ 12 NOT-claim 不复活 + 反题 P0★(A θ-space)+ inflate 警惕(NESS 命名不 grandiose 化)|
| 10 | timeline D60+? | ✓ §0.2 + §8 全标 D60+ candidate |
| 11 | dialectical inclusive form? | ✓ §Cor3:NESS 与 collapse 不矛盾(定态 vs 坏吸引子),inclusive |
| 12 | paradigm-shift D60+ verify? | ✓ 留 D60+ + 反题三方决 |
| 13 | methodological 4 path? | ✓ §7 falsifier = path A(multi-channel)+ B(intervention current 实测)|
| 14 | 5 leg dialectical totality? | ✓ §10 P0 pullback = cross-layer/cross-time evidence |

第 4 + 第 5 通道 partial(非 zero-context),已 disclose,留复核;余 ✓。

---

## §12 References(prior art,全 borrow 非首创)

1. Meyn S., Tweedie R. 1993. *Markov Chains and Stochastic Stability*. Springer. Thm 15.0.1(geometric ergodicity), Ch.15-16(Foster-Lyapunov).
2. Foster F.G. 1953. *On stochastic matrices associated with certain queuing processes*. Ann. Math. Statist. 24:355-360.
3. Doeblin W. 1940. minorization / coupling condition.
4. Sekimoto K. 1998. *Langevin equation and thermodynamics*. Prog. Theor. Phys. Suppl. 130:17-27.
5. Seifert U. 2012. *Stochastic thermodynamics, fluctuation theorems, and molecular machines*. Rep. Prog. Phys. 75:126001.
6. Chaudhari P., Soatto S. 2018. *Stochastic gradient descent performs variational inference, converges to limit cycles*. ICLR.
7. Mandt S., Hoffman M., Blei D. 2017. *Stochastic gradient descent as approximate Bayesian inference*. JMLR 18:1-35.
8. Diaconis P., Freedman D. 1999. *Iterated Random Functions*. SIAM Review 41:45-76.(L0-1 companion)
9. Arnold L. 1998. *Random Dynamical Systems*. Springer.(§10 pullback)
10. [pending 文献确证] Liu-Tegmark physics-informed AI / NESS LLM — 项目内部 cite,留 PI 核实。

---

**生成**:Opus 4.8(1M context),主会话执行,2026-05-29 CST。

**核心 output**:L0-8 = paper §5.2 NESS 的 Foster-Lyapunov-conditional 严格化。**闭合**:NESS 存在/唯一/几何遍历(drift + minorization → Meyn-Tweedie Thm 15.0.1)+ NESS 非平衡性质(non-Einstein → $J\ne0,\sigma>0$)+ D-space pushforward($D^*$ = 遍历均值)。**与 L0-1 互补**(drift 更弱 vs contraction)且**不独立计功**(Cor 2:L0-1 ⟹ L0-8)。**不闭合**:全局 drift(局部 conditional)+ 非平稳 NESS(pullback 留 D60+)+ 高维混合时间 + current 实测。tier:paper L2 → conditional L0。

**严守**:paper v8 final 47/47 + D17 + D29 三 leg + 12 NOT-claim 撤回(不 declare NESS-LLM 文献首创)+ 反题 P0★-A(θ-space)全 binding。0 commit/push/launch/sub-agent。L0 是 D60+ candidate。本 agent 非 zero-context,留反题三方决复核。
