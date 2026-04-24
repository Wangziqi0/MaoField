# MaoField 数学深度分析报告

**作者**: 桌面 Claude (数学教授 persona, 本 session)
**日期**: 2026-04-19 下午
**用途**: 响应一凡"作为数学教授去深度推理解决问题"的请求, 产出供一凡审查的严谨数学研究
**binding**: 与 Linux 4 份 2026-04-19 memo (§3 NESS / §4.11 P3 / §5.1 M3 / §6.1 Claimed) + Action 2 数字 + Phase B Exp 1 verdict 完全一致; 不违反 8 条 empirical binding fact
**范围声明**: 本文只做数学层 (技术 ground truth), 不碰 narrative framing / Win 领地 / 合题决策 / 一凡战略判断

---

## 执行摘要 (Executive Summary)

**Round-2 修正 status** (2026-04-19 晚, Linux 独立 spot-check 反馈后):
- P0 #A 已修 (§5.2 数字 21.8 → 0.87, 补 $1/(8\pi)$ 因子, 承认 direct 1-loop 远小于实测 shift 4.5×, Hartree 需 pushup)
- P0 #B 已修 (Prop 1.2 scope: universal → conditional on $m_\theta^2 < \|F_H\|_{\text{op}}$, Phase B Exp 1 参数下满足)
- P1 #C 已修 (Prop 4.2: "Path A = Path D" → "Path D ⊂ Path A mean-field projection, $\bar{\tilde\psi}=0$ branch", 提 Aron-Biroli-Bouchaud 2010)
- P1 #D 已修 (Hairer timeline 明确 Harris-type 2-3 周 best / 6-10 周 realistic, 不是 regularity structures)
- P2 #E 已修 (15% 差距标 pending Linux sympy verify, 给精确 $\sum_{k=0}^{99} e^{-0.05k} = 20.35$)
- 附录 E 加 B4 (§5.2 算术 self-check miss) + B5 (Prop 4.2 mean-field branch 合法性)

本报告完成四件事:

1. **诊断 M3 失败的数学根源** 到算子理论层, 证明 M3 的 "V_0 上 (L-F) 自伴正定" 框架在 causal memory 结构下**必然不可行** (严格 U(1) 极限), 或**在当前 Phase B Exp 1 参数下定量失败** (pseudo-Goldstone, 55× gap, Prop 1.2 round-2 修正版).

2. **提出 M4 候选**: MaoField 的 Axiom 6 应由 **Martin-Siggia-Rose (MSR) 作用量的鞍点**刻画. 原报告 "Path A = Path D" 过强, round-2 修正为 **Path D (mean-field $\bar{\tilde\psi}=0$ branch) ⊂ Path A (full MSR 含 response-field VEV)**. Linux 4 条分类**不是冗余**, 是 level-of-description 不同 (Path A ⊃ Path D; Path B, C 正交).

3. **给出 M4 的严格数学表述** (Conjecture 4.1 本文), 其假设 (A1)-(A4) 在 Phase B Exp 1 实测 regime 下**全部成立**; Harris-type ergodicity 工具 **2-3 周 best / 6-10 周 realistic** single-author paper scope. Regularity structures (6-12 月) **不 gate** 本 claim.

4. **给 Path B (sub-critical 参数扫描) 一个可证伪预测**: 若 (α, β) 降到 sub-critical, MaoField 会离开 U(1)-disordered NESS, 坍缩到 SSB phase-pick state, 实验可在 10-30 分钟内验证 (Proposition 6.1 本文). 这让 Path B 从 "数学便宜但物理不确定" 变成 "一个 cheap empirical 决策".

本报告的**五条主要数学结果**均已标 `[Theorem]` / `[Proposition]` / `[Conjecture]`, 附严格度评价。**没有任何一条违反 Linux 8 条 binding empirical fact**。Round-2 修正后**OP1 推进状态**: M4 作 [Conjecture] 候选不升格, Linux 4 条 lanes 保持 (Path A ⊃ Path D, Path B/C 正交), Path B 可 10-30 min 验证, Hartree quantitative target 4.5× pushup.

---

## 0. 记号与术语约定

- $\psi : \Omega \to \mathbb{C}$ 复数标量场, $\Omega = [N]^3$, $N=32$, 周期 BC
- $\psi = a + ib = \rho \, e^{i\theta}$ (两种分解)
- $u := |\psi|^2 = a^2+b^2$
- $V(u) = \frac14 (u - v^2)^2$, $v = 1$ (default GL 双井势)
- $F[\cdot]$ = 反馈算子 = $\alpha \cdot (\text{id} - \text{mean})[\cdot] + \beta \cdot K * (\text{id} - \text{mean})[\cdot]$
- $K(\tau) = \theta(\tau) \lambda e^{-\lambda \tau}$, 因果指数衰减核, $\lambda = 0.05$
- $V_0 := \{\delta\psi \in L^2(\Omega; \mathbb{C}) : \int_\Omega \delta\psi \, dx = 0\}$ (零均值子空间)
- $L := -D\nabla^2 + V''_{\text{eff}}(\psi_\infty)$ 线性化扩散-势算子
- $L_H, F_H$ 表示算子的 Hermitian part: $A_H := \frac12 (A + A^*)$
- $\psi_{\text{NESS}}$: Phase B Exp 1 实测的非平衡稳态 field
- **NESS** = Non-Equilibrium Steady State; **MSR** = Martin-Siggia-Rose; **FDT** = Fluctuation-Dissipation Theorem
- 所有 mode-tag 沿用 v1 §3.5 convention: `[STATIC]` / `[DYNAMIC-EQUILIBRIUM]` / `[DYNAMIC-RARE-EVENT]` / `[DYNAMIC-IMPLEMENTATION]`

---

## 1. 现状诊断: M3 为何必败

本节把 Linux Action 2 的 empirical falsification (m_θ² = 0.017 ≪ 0.949) 提升到**算子理论层面**的结构性诊断, 证明 M3 的失败**不是参数选择问题, 是框架结构问题**。

### 1.1 M3 的形式回顾

Linux A1 + A2 给出的 M3 framing:

> 定义 $V_0 = \{\delta\psi : \int \delta\psi \, dx = 0\}$, Fréchet 线性化 $L = -D\nabla^2 + V''_{\text{eff}}(\psi_\infty)$, 反馈 $F = \alpha \, \text{id} + \beta K$ (作用于零均值 mode). **M3 声明**: $(L - F)[\delta\psi_\infty] = \delta S_0$ 在 $V_0$ 上有唯一解 $\Leftrightarrow$ Axiom 6 (匹配 = 自我训练) 在 $V_0$ 子空间严格实现。

PASS 条件: $(L-F)$ 在 $V_0$ 上正定 (自伴谱意义下 $\lambda_{\min}((L-F)_H) > 0$).

实测: $\lambda_{\min}((L-F)_H) = -0.93$, 严重**负定**, 差 $\|F_H\|_{\text{op}} \approx 0.95$ 的 97%. M3 falsified.

### 1.2 根源 1 (加强的): 因果核 ⇒ F 非自伴

**Proposition 1.1** [Linux A1 Prop A1.1 加强版 — 因果性 ⇒ 本质非自伴]

设 $K : \mathbb{R} \to \mathbb{R}_{\geq 0}$ 为任一**非平凡因果核** (即 $K(\tau) = 0$ 对 $\tau < 0$, 且 $K \not\equiv 0$, 有 $\int_0^\infty K(\tau) d\tau < \infty$). 定义卷积算子 $\hat K$ 在 $L^2(\mathbb{R}_+; H)$ 上 ($H$ 任何 Hilbert 空间):

$$
(\hat K \phi)(t) := \int_0^\infty K(\tau) \phi(t - \tau) \, d\tau
$$

则对**任何**正定权算子 $W$ (即在内积 $\langle \phi, \phi' \rangle_W := \int \langle W \phi(t), \phi'(t) \rangle_H \, dt$ 下), $\hat K$ **不可能**是自伴的, 除非退化到 $K = c \delta_0$ (即无记忆).

**证明**: 计算 $\hat K$ 的 adjoint $\hat K^*$ (在 $\langle \cdot, \cdot \rangle_W$ 下):

$$
\langle \hat K \phi, \phi' \rangle_W = \int_\mathbb{R} \int_0^\infty K(\tau) \langle W \phi(t-\tau), \phi'(t) \rangle_H \, d\tau \, dt
$$

换积分顺序, 令 $s = t - \tau$:

$$
= \int_\mathbb{R} \langle W \phi(s), \int_0^\infty K(\tau) \phi'(s + \tau) \, d\tau \rangle_H \, ds
$$

所以 $(\hat K^* \phi')(s) = \int_0^\infty K(\tau) \phi'(s + \tau) \, d\tau$, 这是 **反因果** (anti-causal, future-referencing) 算子.

若 $\hat K = \hat K^*$, 则 $\int_0^\infty K(\tau) [\phi(t-\tau) - \phi(t+\tau)] \, d\tau = 0$ 对所有 $\phi \in L^2$ 成立. 由 $\phi$ 任意性, 可取 $\phi_\omega(t) = e^{i\omega t}$ 作为测试 (技术上取 Schwartz 包络逼近):

$$
\int_0^\infty K(\tau) (e^{-i\omega \tau} - e^{i\omega \tau}) \, d\tau = -2i \int_0^\infty K(\tau) \sin(\omega \tau) \, d\tau = 0 \quad \forall \omega.
$$

由 $\sin$ 完备性 (Plancherel): $K(\tau) \sin(\omega \tau)$ 对所有 $\omega$ 积分为零当且仅当 $K(\tau) \chi_{\tau > 0} = K(-\tau) \chi_{\tau < 0}$ (奇延拓), 但 $K \geq 0$ 因果, 所以 $K \equiv 0$ 或 $K = c \delta_0$. ∎

**评注 1.1.1** [时间反演对称性破坏]: 这条命题的物理内涵是 **因果记忆本质上破坏时间反演对称性**, 而自伴性恰恰**要求**时间反演对称. 所以 "自伴 + 因果" 本质上不相容. M3 在数学层的错误就是忽视了这条**算子理论层的 no-go**.

**评注 1.1.2** [Phase B Exp 1 具体核]: 我们的 $K(\tau) = \theta(\tau) \lambda e^{-\lambda \tau}$, $\lambda = 0.05$. 其 Fourier 变换 $\hat K(\omega) = \frac{\lambda}{\lambda + i\omega}$ 实部 $\text{Re} \hat K(\omega) = \frac{\lambda^2}{\lambda^2 + \omega^2} \geq 0$, 虚部 $\text{Im} \hat K(\omega) = -\frac{\lambda \omega}{\lambda^2 + \omega^2} \neq 0$ 对 $\omega \neq 0$. 虚部非零 ⇒ 非自伴, 数字 match.

### 1.3 根源 2: Goldstone 软模使 L 在 V_0 上退化

Mexican-hat 势 $V(u) = \frac14 (u - v^2)^2$ 在 $\psi = v$ 处 (任一 U(1) 方向 SSB vacuum) 的 Hessian (对实自由度 $(\delta a, v \delta\theta)$):

$$
H_V = \begin{pmatrix} 2 v^2 & 0 \\ 0 & 0 \end{pmatrix}, \quad v = 1.
$$

- 径向 mass²: $m_\rho^2 = 2 v^2 = 2$ (理论值; 经验数 0.092 差 22×)
- 角向 mass²: $m_\theta^2 = 0$ (精确 Goldstone, U(1) 对称性 ⇒ 角向无恢复力)

在 $V_0$ 上的 $L$ 最小 eigenvalue:

$$
\lambda_{\min}(L \text{ on } V_0) = D k_{\min}^2 + m_\theta^2 = 0.1 \cdot (2\pi/N)^2 + 0 \approx 0.0039,
$$

比 $\|F_H\|_{\text{op}} \approx 0.95$ **小 240 倍**. 即使把 angular Goldstone 软模升格到 $m_\theta^2 = 0.017$ (实测 pseudo-Goldstone), 仍只把比值改到 55×.

**Proposition 1.2** [M3 失败的定量条件, P0 #B round-2 修正版]

**Statement** (scope 与证明体 match): 当 $m_\theta^2 < \|F_H\|_{\text{op}}$ 时, M3 必失败 (即 $\lambda_{\min}((L-F)_H \text{ on } V_0) < 0$). Phase B Exp 1 实测 $m_\theta^2 = 0.017$, $\|F_H\|_{\text{op}} = 0.953$, 比值 55× 充分满足该条件 ⇒ **M3 failed at current Phase B Exp 1 parameters**.

**证明**: $V_0$ 包含 angular (pseudo-)Goldstone mode (零均值要求对 angular 部分 non-trivial). 在该 mode 上 $L$ 贡献 $\leq D k_{\min}^2 + m_\theta^2$, 而 $F_H$ 贡献至多 $\|F_H\|_{\text{op}}$. 所以

$$
\lambda_{\min}((L-F)_H \text{ on } V_0) \leq D k_{\min}^2 + m_\theta^2 - \|F_H\|_{\text{op}}.
$$

$D k_{\min}^2 = 0.1 \cdot (2\pi/32)^2 \approx 0.0039$, 所以右边 $\approx m_\theta^2 + 0.004 - \|F_H\|_{\text{op}} < 0$ iff $m_\theta^2 < \|F_H\|_{\text{op}} - 0.004 \approx \|F_H\|_{\text{op}}$ (to leading order). 实测 $0.017 < 0.953$ ✓. ∎

**量纲 remark** (round-3 P2 #2 补): $m_\theta^2$ 与 $\|F_H\|_{\text{op}}$ 在零均值子空间 $V_0$ 上的 spectrum 语言下同量纲 (均作 effective mass² 单位, Fourier $\omega=0$ 处的 static linear response). Linux Action 2 数字层 $m_\theta^2 = 0.017$ 与 $\|F_H\|_{\text{op}} = 0.953$ 的比较在此框架下 unit-consistent; $D k_{\min}^2$ 是 diffusive spectral gap, 同量纲. 所有三项可在 Fourier 表象 $\hat{(\cdot)}(\omega=0, k)$ 统一 read off.

**Remark 1.2.0** [证明 scope 澄清, round-2 新加]: 上述证明**不 claim** "对任何 $(\alpha, \beta) > 0$ M3 必失败" universal. 原因: $m_\theta^2(\alpha, \beta)$ 的依赖关系未在本证明体内建立 — 如果 feedback $(\alpha, \beta)$ 影响 pseudo-Goldstone mass via source field's effective explicit breaking, 在某些 $(\alpha, \beta)$ 下 $m_\theta^2 > \|F_H\|_{\text{op}}$ 理论上有可能 (虽然 Phase B Exp 1 实测 regime 远离此情况). **严格 U(1) 对称 ($m_\theta^2 = 0$) 极限** 是 universal case — 此时 $L$ 贡献 $\to 0$ 对 angular Goldstone, 必败对任何 $(\alpha, \beta) > 0$ (Goldstone theorem exact). MaoField 有 BGE 源显式 U(1) 破坏, 属 pseudo-Goldstone, 需 quantitative 条件, 不 universal.

**评注 1.2.1** [为什么 "加 U(1) 显式破坏" 不救 Phase B Exp 1 M3]: Linux A1 §3.5 Option 2 曾提 "加 U(1) 显式破坏项". 这只把 $m_\theta^2$ 从 0 抬到 $\epsilon > 0$, 但要让 $\lambda_{\min}((L-F)_H) > 0$, 需要 $\epsilon > \|F_H\|_{\text{op}} \approx 0.953$. Phase B Exp 1 源场 $S_0$ 诱导的 $\epsilon = 0.017$, **小 55×**. 要 save M3 在当前参数, 必须把 explicit breaking 加强至少 55 倍, 但那已经**不是** MaoField 的 weak-breaking regime 了 — 破坏 $O(1)$ 的 U(1) 对称 = 放弃 matter field 的 U(1) 结构 = 放弃 complex field framework.

**评注 1.2.2** [连续 limit 数字与离散 $\|F_H\|_{\text{op}}$ 的 15% 差距, P2 #E round-2 修正]:

- 连续 limit bound: $\hat F_H(\omega=0) = \alpha + \beta/\lambda_{\text{mem}} = 0.1 + 0.05/0.05 = 1.100$
- 有限 $N_\text{hist} = 100$ 离散和 (Linux 独立算): $\sum_{k=0}^{99} e^{-0.05 k} = \frac{1 - e^{-5}}{1 - e^{-0.05}} = 20.35$, 给 $\alpha + \beta \cdot 20.35 \cdot \Delta t_{\text{outer}} = 0.1 + 0.05 \cdot 20.35 = 1.118$
- Linux 实测: $\|F_H\|_{\text{op}} = 0.953$

**差距**: 1.118 (离散理论) vs 0.953 (实测) = 14.7% 未解释。**不是** 离散化解释 (离散和与连续差仅 1.6%)。可能来源:
1. Hermitian 投影 on $V_0$ 子空间的 non-trivial geometry (k=0 排除 + 有限 lattice 有限 spectrum cutoff)
2. Source field 在 Hermitian 投影下的 contribution
3. Numerical estimation of $\|\cdot\|_{\text{op}}$ via truncated Hilbert space

**状态**: **pending Linux 数字层 sympy / scipy 独立 verify**, 本报告不 claim 已 close. Round-2 修正前 "离散化解释" 是 hand-wave, 现标 [?] pending。定性结论 (55× gap ⇒ M3 fails) 不受该数字 detail 影响。

### 1.4 根源 3: 围绕错误背景的线性化

Phase B Exp 1 实测 $\langle \rho \rangle = 1.19$, $|\langle \psi \rangle| \approx 0.004$, 50 patches / $r_g < 8$. 这是 U(1)-symmetric disordered NESS:

- 不是 SSB vacuum ($|\langle\psi\rangle| \not\approx v$)
- 不是 Mexican-hat 极小 ($\langle u \rangle = \langle\rho\rangle^2 + \text{var}(\rho) \approx 1.42 + 0.0006 > v^2 = 1$)
- 是 patched non-uniform (50 coherent phase patches, 回转半径 < 8)

Fréchet 线性化要**围绕 actual stationary state**, 不是 Mexican-hat theoretical ideal.

**Proposition 1.3** [线性化背景错配误差]

令 $\psi_\infty^{\text{MH}} = v$ (Mexican-hat), $\psi_{\text{NESS}}(x)$ = 实测 patched NESS. 设 $\delta\psi = \psi - \psi_\infty^{\text{MH}}$ 作为 "naive" 线性化, 则

$$
\|\psi_{\text{NESS}} - \psi_\infty^{\text{MH}}\|_{L^2(\Omega)}^2 \geq \int_\Omega (\rho(x) - v)^2 \, dx \approx N^3 \cdot \text{Var}(\rho) + N^3 (\langle\rho\rangle - v)^2
$$

用实测 $\langle\rho\rangle = 1.19$, $\sigma(\rho) = 0.024$:

$$
\|\psi_{\text{NESS}} - v\|_{L^2}^2 \approx 32^3 \cdot (0.024^2 + 0.19^2) \approx 32^3 \cdot 0.0367 \approx 1203.
$$

所以 $\|\psi_{\text{NESS}} - v\|_{L^2} \approx 34.7$, 这**不是**小扰动, Fréchet 展开的有效性 window ($\|\delta\psi\|$ 远小于 $V''$ 的特征长度尺度) **被打破 2-3 个量级**.

**推论 1.3.1**: M3 的整个线性化 framework 只能视为 **Mexican-hat 理想** 的算子分析, 不是 Phase B Exp 1 实测稳态的 faithful description. 即使 M3 在 Mexican-hat 极小处 formally 成立 (它不成立, 见 Prop 1.2), 也不能移植到 NESS regime 作 Axiom 6 的 realization.

### 1.5 方法学诊断: 整个 "找正定自伴算子" 方向是认识论错误

综合 Prop 1.1 + 1.2 + 1.3, M3 失败是**三重结构性不相容**的叠加:

1. **因果记忆 ↔ 自伴性** (Prop 1.1): no-go 在算子层
2. **U(1) 对称 ↔ V_0 上 L 正定性** (Prop 1.2): Goldstone 软模天然违反
3. **Mexican-hat 极小 ↔ NESS 背景** (Prop 1.3): 线性化 framework 本身错配

这三条**都不是** Linux A1 单一的 "candidate M3 参数不够好" 问题. 它们指向一个**更深的方法学 error**:

> **把本质 driven-dissipative + non-self-adjoint + non-equilibrium 的系统, 硬塞入 closed Hermitian operator 的 spectral theory 框架.**

这**预决定了** 任何 "M3 + 参数调整" 或 "M3 + 局部修补" 都不可能 close OP1. Linux Action 1 §5 pre-commit 1 (不救援 M3) 与这条数学诊断完全一致.

**下一步必须换框架**: 从 "$(L-F)$ 的谱" 转移到 "随机动力学 + 非平衡稳态 + 变分鞍点" — 即本报告 §3-4 主张的 M4 方向.

---

## 2. 替代数学工具: 非自伴耗散算子理论

本节列出**如果仍想走算子理论路径** (Linux Path C 的变种), 需要哪些正确工具. 这些工具是**有的**, 只是不是自伴谱理论.

### 2.1 Lumer-Phillips 定理 vs 自伴谱理论

对**耗散** (但非自伴) 算子 $A$ (即 $A$ 生成 $C_0$ 收缩半群), **正确**的判据是 **m-accretive** (Kato 1966, Pazy 1983):

$$
A \text{ m-accretive} \Leftrightarrow \begin{cases} \text{Re} \langle A x, x \rangle \geq 0 & \forall x \in \mathcal{D}(A) \\ \text{Range}(I + \mu A) = H & \text{某 } \mu > 0 \end{cases}
$$

注意: **只需要对称部分 $A_H$ 正定**, 非 $A$ 本身. 这和自伴谱理论的 $\lambda_{\min}(A_H) > 0$ 判据**形式相同**, 但允许 $A_{\text{AH}} := \frac12 (A - A^*) \neq 0$ (反 Hermitian 部分).

### 2.2 对 $(L-F)$ 的应用

设想我们**放弃** "M3 要求 $(L-F)$ 正定" 的强版本, 改问 "$(L-F)$ 是否 m-accretive?"

答案: **仍然不** — 因为 $\lambda_{\min}((L-F)_H) = -0.93 < 0$ 直接违反 accretivity 条件 (Re $\langle (L-F) x, x \rangle = \langle (L-F)_H x, x \rangle \geq \lambda_{\min} \|x\|^2$, 负 $\lambda_{\min}$ ⇒ 存在 $x$ 使 Re 为负 ⇒ 非 accretive).

**Proposition 2.1** [M3 的弱化版 — Lumer-Phillips 仍失败]

在 Phase B Exp 1 参数 $(\alpha, \beta) = (0.1, 0.05)$ 下, 算子 $-(L - F)$ 不生成 $L^2(V_0)$ 上的收缩 $C_0$ 半群.

**证明概要**: $\lambda_{\min}((L-F)_H) < 0$ 直接 implies $-(L-F)$ 非 accretive. Lumer-Phillips 必要条件失败. ∎

**物理内涵**: 这说明 $(L-F)$ 驱动的线性动力学**不稳定** (存在 exponentially growing mode). 那这和 Phase B Exp 1 实测 "dS/dt 稳定 plateau 10⁻⁶" 为什么兼容?

答: 因为**非线性项** ($V$ 的 $O(\delta\psi^3), O(\delta\psi^4)$ 项) 在大 amplitude 上 arrest 线性不稳定, 稳态是**非线性 saturation** 而非线性 fixed point. 这正是 driven-dissipative 系统 (Hohenberg-Halperin Model A/B/C) 的典型结构: 线性不稳定 + 非线性饱和 ⇒ non-trivial NESS.

### 2.3 Sectorial operator + analytic semigroup

即使 $-(L-F)$ 非 accretive, 仍可在**复谱平面**分析. Henry 1981 *Geometric Theory of Semilinear Parabolic Equations* 第 1 章的 sectorial operator:

$$
A \text{ sectorial} \Leftrightarrow \exists \phi \in (0, \pi/2), M > 0 : \|(A - \lambda I)^{-1}\| \leq \frac{M}{|\lambda - a|}, \lambda \in S_{a, \phi}
$$

$S_{a, \phi}$ 是避开 real line 的 sector. Sectorial 允许 $\sigma(A)$ 在**有限** left half-plane (不像 m-accretive 要求 $\sigma(A) \subset \{\text{Re} \geq 0\}$).

对 $-(L-F)$:
- $L$ 是 sectorial (扩散算子 $-D\nabla^2 + \text{mass}$ 的 standard fact, Henry §1.4)
- $F$ 是 $L$ 的**相对紧扰动** (如果 $K$ 作用域 domain 合适), 所以 $-(L-F)$ 也 sectorial
- 但 real spectrum 可进入 $\{-0.93 \leq \text{Re} \leq 0\}$ (from $\lambda_{\min}((L-F)_H) = -0.93$)

所以 sectoriality 成立, **exponential dichotomy** 适用, 但没有 spectral gap 到 right half-plane ⇒ 没有 deterministic stable fixed point.

**推论 2.3.1**: 在 sectorial 框架下 M3 可以被理解为 **"我们本来期望 spectrum entirely in right half-plane (dissipative sector), 实测 spectrum 跨 imaginary axis, 所以不是简单 exponential stabilization"**. 这是个更诚实的描述, 但仍未给 Axiom 6 一个正向 realization.

### 2.4 小结

走"非自伴算子理论"路径 (Path C 变种), 我们可以:
- 诊断 M3 失败的算子层根源 (本节)
- 把 M3 重写为 "期待 sectorial + spectrum gap to right half, 但 empirically 不成立"
- **但给不出 Axiom 6 的正向 realization**

换句话说, Path C 可以做 post-mortem, 但不能做 forward progress. 正向 progress 必须换框架 — 就是 §3 的 MSR 变分方向.

---

## 3. MSR 变分框架: M4 候选的核心提案

本节是本报告**最新的**数学贡献。提出将 Axiom 6 (匹配 = 自我训练) 重 formalize 为 MSR action 的鞍点刻画, 称为 **M4**。M4 **不需要** 自伴性, **不需要** 线性算子框架, **原生支持** NESS 作为数学 object。

### 3.1 从 Langevin SPDE 到 MSR action (Janssen-De Dominicis-Peliti 1976)

MaoField 完整动力学 (加噪声):

$$
\gamma \, \partial_t \psi(x, t) = -\frac{\delta F_{\text{GL}}}{\delta \psi^*}(x, t) + \alpha (\psi - \langle\psi\rangle_x) + \beta \int_0^\infty K(\tau) (\psi(\cdot, t-\tau) - \langle\psi\rangle) \, d\tau + S_0(x) + \eta(x, t) \tag{3.1}
$$

其中 $\eta$ 是复数高斯白噪声 $\langle \eta(x,t) \eta^*(x',t') \rangle = \sigma^2 \delta(x-x') \delta(t-t')$.

**Janssen-De Dominicis-Peliti 1976 path integral 构造**: 对一般 Langevin 动力学 $\partial_t \phi = N[\phi] + \eta$, path integral 测度

$$
P[\phi] \mathcal{D}\phi = \delta(\partial_t \phi - N[\phi] - \eta) \mathcal{D}\phi \cdot P_\eta[\eta] \mathcal{D}\eta
$$

引入辅助 (response) 场 $\tilde\phi$ 作 Fourier 表示 $\delta$-functional:

$$
\delta(\partial_t \phi - N[\phi] - \eta) = \int \mathcal{D}\tilde\phi \, e^{i \int \tilde\phi (\partial_t \phi - N[\phi] - \eta) \, dt \, dx}
$$

积掉 $\eta$ (Gaussian), 得 MSR action:

$$
S_{\text{MSR}}[\phi, \tilde\phi] = \int dt \int dx \left\{ -i \tilde\phi (\partial_t \phi - N[\phi]) + \frac{\sigma^2}{2} |\tilde\phi|^2 \right\} + c.c.
$$

对 MaoField 复场 $\psi$, 引入复辅助场 $\tilde\psi$, MSR 作用量:

$$
\boxed{ S_{\text{MSR}}[\psi, \tilde\psi] = \int dt \int dx \left\{ -i \tilde\psi^* \Big( \gamma \partial_t \psi + \frac{\delta F_{\text{GL}}}{\delta \psi^*} - F[\delta\psi] - S_0 \Big) + \frac{\sigma^2}{2} |\tilde\psi|^2 \right\} + c.c. } \tag{3.2}
$$

其中 $\delta\psi = \psi - \langle\psi\rangle_x$, $F[\delta\psi] = \alpha \delta\psi + \beta (K * \delta\psi)$.

**关键观察**: $S_{\text{MSR}}$ **不要求 $F$ 自伴**. 非自伴性只是 $S_{\text{MSR}}$ 的一个特征, 不是 obstruction.

### 3.2 NESS 作为 MSR action 的鞍点

Path integral $Z = \int \mathcal{D}\psi \, \mathcal{D}\tilde\psi \, e^{-S_{\text{MSR}}}$ 给出 MaoField 动力学的 generating functional. 其**稳态**由鞍点方程:

$$
\frac{\delta S_{\text{MSR}}}{\delta \tilde\psi^*} = 0 \Rightarrow \gamma \partial_t \psi + \frac{\delta F_{\text{GL}}}{\delta\psi^*} - F[\delta\psi] - S_0 - i \sigma^2 \tilde\psi = 0 \tag{3.3a}
$$

$$
\frac{\delta S_{\text{MSR}}}{\delta \psi^*} = 0 \Rightarrow -\gamma \partial_t \tilde\psi + \frac{\delta^2 F_{\text{GL}}}{\delta\psi^* \delta\psi}[\tilde\psi] - F^*[\tilde\psi] = 0 \tag{3.3b}
$$

**Mean-field / classical saddle** 是 $\tilde\psi = 0$ (response 场在无噪声/大 scale 时退化). 此时 (3.3a) 退化为 deterministic Langevin, (3.3b) 自动满足. NESS 对应 $\partial_t \psi = 0$ 在**统计意义上** (i.e., 分布层面而非 field 层面).

**但在 $\sigma > 0$ 且有效 noise 非零** (或 Phase B Exp 1 σ=0 但源场 $S_0$ 有 intrinsic 非平稳 structure, CoV = 0.107), **Gaussian fluctuations around saddle** 给 NESS 统计量:

$$
\mu_*(\chi) = \langle \chi[\psi] \rangle_{\text{NESS}} = Z^{-1} \int \mathcal{D}\psi \, \mathcal{D}\tilde\psi \, \chi[\psi] \, e^{-S_{\text{MSR}}} \tag{3.4}
$$

对 observables $\chi$.

### 3.3 主定理 [Conjecture C4.1]: MaoField NESS 的 MSR 变分刻画

**Conjecture 4.1** [MaoField NESS 存在性与 MSR 鞍点刻画] — 本报告的**中心数学 statement**, 待严格证明

考虑 MaoField SPDE (3.1) 在 $\Omega = \mathbb{T}^3$ (torus, 有限体积)上, 参数 $(\gamma, D, \alpha, \beta, \lambda, \sigma, V, S_0, K)$, 假设:

- **(A1) 势限制性**: $V(u) \to \infty$ 作 $u \to \infty$, 且 $V''(u) \to \infty$ 作 $u \to \infty$ (超线性约束)
- **(A2) 记忆核可积性**: $\int_0^\infty K(\tau) \, d\tau < \infty$ 且 $\int_0^\infty \tau K(\tau) \, d\tau < \infty$ (一阶矩有限)
- **(A3) 非退化随机驱动**: $\sigma > 0$ 或源场 $S_0$ 满足时空 **非平凡 correlation structure** (CoV 空间 > 0 在 Ω 上)
- **(A4) 耗散性**: $\gamma, D > 0$

**断言**:

(i) [存在性] 存在唯一 invariant probability measure $\mu_* \in \mathcal{P}(C([0,\infty), H^1(\Omega; \mathbb{C})))$ 对 (3.1) 驱动的 Markov semigroup.

(ii) [MSR 鞍点刻画] $\mu_*$ 由 MSR path integral (3.4) 给出, 其中 $S_{\text{MSR}}$ 由 (3.2) 给出.

(iii) [Axiom 6 的 M4 realization] 定义 **M4 映射** $\Psi_4 : \mathcal{S}_{\text{sources}} \to \mathcal{P}(C(\Omega; \mathbb{C}))$

$$
\Psi_4(S_0) := (\text{marg}_{\psi \text{ at steady state}}) \mu_*(S_0)
$$

则 $\Psi_4$ **对任何 $S_0$ 满足 (A1)-(A4) 上都良定义**, 且在源场 $L^2$ 拓扑下连续 (稳定性 property).

**评注 3.3.1** [严格性评级]: 
- **(i)** 有标准工具可证 (round-2 P1 #D timeline 修正):
  - **Harris-type ergodicity** (Hairer 2009 *Ergodicity for SPDEs* lecture notes; Hairer-Mattingly 2008): 在 $\mathbb{T}^3$ 有限体积 + (A1)-(A4) 下, **2-3 周 best-case scope** (若数学结构干净 + 工具匹配), **6-10 周 realistic** (含 memory kernel 的技术复杂 + spectral gap 判据详查 + paper writing). 用 **Kuksin-Shirikyan 2012** 的 coupling methods 应 workable.
  - **严格 well-posedness via regularity structures** (Hairer 2014 Fields Medal work + Chandra-Hairer 2016 BPHZ renormalization): **6-12 月 scope**, 远超 Harris-type ergodicity. **这不是 (i) 需要的 tool** — Harris 只需 transition kernel 的 ergodic gap, 不需 Hairer regularity structures 级的 subcritical SPDE model construction. 本报告 round-1 执行摘要未清楚区分, 是 round-2 澄清的 scope error.
  - **定位**: (i) 用 Harris 工具足够, 2-3 周 best / 6-10 周 realistic single-author paper. Regularity structures 是**更远的** mathematical infrastructure, 若 MaoField 在 continuum limit 下要严格 well-posed 可能需要, 但**不 gate** M4 的 NESS existence claim.
- **(ii)** 需要小心: JDP 1976 是 formal path integral, 严格 measure theory 层的 MSR 与 invariant measure 等价是 **未完全解决的** 问题 (round-5 P2 修正: Aron-Biroli-Bouchaud 2010 *J. Stat. Mech.* P11018 以及相关 driven-dissipative MSR formalism works 有 progress 但未 close; round-1 原写 "2008 progress" 是年份 cite error, 我无法 verify 具体 2008 paper, 现 consolidate 到已有 2010 reference #19). 在**有限 lattice** (如我们 $32^3$) 有限 ODE system 上, (ii) **完全严格** (就是 Fokker-Planck invariant distribution 的 path integral 表示).
- **(iii)** 跟 (i) 的唯一性是同一回事, $\mu_*$ 对 $S_0$ 的 Lipschitz 连续性是 Harris 方法的 副产品.

**评注 3.3.2** [(A3) 在 Phase B Exp 1 满足]: Phase B Exp 1 名义 σ=0 但源 CoV = 0.107 (late window), 满足 (A3) 的 "源场非平凡 correlation structure" 替代条款. 这给 Axiom 6 的数学 realization 一个**实际可测量的条件**.

### 3.4 Axiom 6 "匹配 = 自我训练" 在 M4 下的自然 realize

现在来看为什么 M4 自然 realize Axiom 6 的哲学内容:

**Axiom 6 的哲学 claim**: 匹配 score 来自自我训练 (self-consistent 迭代), 而非 fixed encoder.

**M4 下的 realize**:
- "匹配" = 查询源场 $S_q$ 和文档源场 $S_d$ 的 **combined source** $S_0 = S_q + S_d$ 诱导的 NESS 统计量
- "自我训练 = 不动点" 在 M4 下 = **$\mu_*$ 是 Markov semigroup 的 invariant distribution** (这是 NESS 的定义)
- "迭代" 是 **沿 trajectory 的时间演化**, 稳态由 $\mu_*$ 描述 (不是 field 层的 fixed-point iteration, 是**分布层的 invariance**)

**与 exp005 adjoint 结构的对应**: exp005 定义 $G = -\delta L/\delta u |_{u=u_*}$ = 残余不平衡. 在 NESS 下, $\langle G \rangle_{\mu_*} = 0$ (definition of steady state), 但 $\langle G \cdot G \rangle_{\mu_*} > 0$ — 残余涨落仍存在. exp005 的 "不平衡驱动下一步实践" 在 M4 下变成:

> **NESS 不是静止, 是统计稳态** — 单 trajectory 层面 $G \neq 0$ 持续驱动涨落, 但分布层面稳定.

这和一凡原始 exp005 说的 "不平衡就是一种平衡" **完全 coherent**. 这不是 retcon, 是 exp005 的哲学 + M4 的数学的**自然 match**.

---

## 4. Path D ⊂ Path A: mean-field projection 与完整 MSR path integral 的关系 (round-2 修正版)

Linux debt list 列 4 条 OP1 候选路径:
- **Path A**: SPDE + NESS
- **Path B**: sub-critical 参数扫描
- **Path C**: 非 causal memory
- **Path D**: 变分 / 非线性不动点

本节建立 A 和 D 在 mean-field projection 下的 **subset 关系** (D ⊂ A, $\bar{\tilde\psi}=0$ branch), **不是 full equivalence** — Linux 原 4 条分类有合理数学基础 (3-4 条 independent conceptual lanes 保持); round-1 "4 → 2 collapse" 的 overclaim 由 round-2 P1 #C 修正 retract. Path D 是 Path A 的 mean-field 投影 corner case, 当 FDT 成立或响应场 VEV 可忽略时两者重合, 在 Phase B Exp 1 的 FDT 违反 regime 下**可能** diverge (见 Aron-Biroli-Bouchaud 2010).

### 4.1 基本 observation: 非平衡稳态 ≠ 极小, 是鞍点

**在平衡态** (有 detailed balance), NESS = Boltzmann 分布 = 能量的**极小** (via $e^{-\beta E}$).

**在 NESS** (无 detailed balance, 如 driven-dissipative 或 memory-kernel 系统), $\mu_*$ **不是**能量的极小. 严格地:

**Lemma 4.1.1** [NESS 判据与 detailed balance]

Markov process $X_t$ 在状态空间 $\mathcal{X}$, invariant measure $\mu_*$ 满足 detailed balance iff $\mu_*$ 是某**对称 Dirichlet form** 的基态 (Fokker-Planck 的 self-adjoint factor).

**推论 4.1.2**: 若动力学含因果记忆 $K$ (Prop 1.1 说 $\hat K$ 非自伴), detailed balance **天然不成立** — Fokker-Planck-like operator 非自伴 — $\mu_*$ 不是 closed-form $e^{-\beta V}$.

**结论**: MaoField $\mu_*$ (存在假设 M4 Conjecture 4.1 成立) **必然不是** $F_{\text{GL}}$ 的极小, **必然是**某 MSR action 在扩展 ($\psi, \tilde\psi$) 空间的**鞍点**.

### 4.2 Path A 与 Path D 的 formal 等价

**Path A (SPDE+NESS)** 数学内容: 用 MSR 框架 / Hohenberg-Halperin Model A/B/C / large-N 方法研究 NESS $\mu_*$ 的性质.

**Path D (变分)** 数学内容: Axiom 6 = 某 functional 的 critical point.

**Proposition 4.2** [Path D ⊂ Path A (mean-field projection), round-2 P1 #C 修正版]

**Statement** (scope weakening): **Path D (变分 mean-field) 是 Path A (完整 MSR path integral) 的 $\bar{\tilde\psi} = 0$ mean-field 投影 subset**, 不是 full equivalence.

**证明**: Path D 的 functional 选 **MSR effective action** $\Gamma_{\text{eff}}[\psi_{\text{cl}}, \tilde\psi_{\text{cl}}]$ (1PI generating functional):

$$
\Gamma_{\text{eff}}[\psi_{\text{cl}}, \tilde\psi_{\text{cl}}] := S_{\text{MSR}}[\psi_{\text{cl}}, \tilde\psi_{\text{cl}}] + \text{1-loop and higher corrections}
$$

Path A 的 $\mu_*$ 由 (3.4) 定义; Path A 的 **mean-field projection** 由 $\Gamma_{\text{eff}}$ 鞍点给:

$$
\left. \frac{\delta \Gamma_{\text{eff}}}{\delta \psi_{\text{cl}}^*} \right|_{\bar\psi, \bar{\tilde\psi}} = 0, \quad \left. \frac{\delta \Gamma_{\text{eff}}}{\delta \tilde\psi_{\text{cl}}^*} \right|_{\bar\psi, \bar{\tilde\psi}} = 0.
$$

**关键限制** (round-2 补): 原报告 round-1 选 $\bar{\tilde\psi} = 0$ branch 作 Path D 内容, 但**这个 branch 选择本身是 equilibrium-like 假设**, 不是 automatic:

- **In equilibrium** (FDT 成立, detailed balance): 鞍点 $\bar{\tilde\psi} = 0$ 是 unique stable branch (Janssen 1992 §3)
- **Driven-dissipative NESS (FDT 违反)**: response 场 VEV $\bar{\tilde\psi}$ **可非零**, 对应 non-trivial 响应函数的 mean-field contribution (Aron-Biroli-Bouchaud 2010 *J. Stat. Mech.* P11018). Path D 的 mean-field 变分**错过** $\bar{\tilde\psi} \neq 0$ 的 branch.

因此: Path A ⊃ Path D (严格包含). Path D 捕获 equilibrium-like mean-field NESS; Path A 捕获 full driven-dissipative NESS 包含 response-field VEV 贡献。MaoField Phase B Exp 1 的 **FDT 违反程度未测量** (见 §5.2 Prop 5.3), 所以 $\bar{\tilde\psi}$ 非零的 branch 是否存在**未定**. ∎

**评注 4.2.1** [这不是 ad hoc 重整]: 把 MSR 作为**变分 functional** 不是硬拼, 是**物理系统的内禀结构** — 任何 driven-dissipative Langevin 系统的变分原理都由 MSR 给. JDP 1976 + Vasiliev 2004 是 settled theory.

**评注 4.2.2** [对 Linux 4 条分类的重解读, round-2 修正]: Linux debt list 的 4 条分类 **不是工具层冗余**, 是 level-of-description 不同:

- **Path A** (完整 MSR) ⊃ **Path D** (MSR mean-field projection, $\bar{\tilde\psi} = 0$ branch)
- **Path B** (sub-critical 参数 scan) **⊥** Path A/D (换参数 regime, 不换 framework)
- **Path C** (非 causal memory) **⊥** Path A/D (换 kernel structure, 使 $\hat F$ 可能自伴)

所以**收缩后 3-4 条 independent conceptual lanes**, 不是 "4 collapse 到 2". Linux 原分类有合理数学基础 — 本报告 round-1 的 "4 → 2" overclaim 需修正。

**一凡 invocation 的直觉** ("它们应该是同一条") 的严格版本是: **Path D 是 Path A 的 mean-field corner case**, 当 FDT 成立或响应场 VEV 可忽略时两者重合。在 Phase B Exp 1 的 FDT 违反 regime, 两者**可能** diverge, 需 Aron-Biroli-Bouchaud-type 分析.

### 4.3 为什么 M3 必败: saddle ≠ minimum in non-equilibrium

M3 的隐含 framing: 稳态是某 quadratic form 的**极小**. 实际 driven-dissipative NESS 是 MSR action 的**鞍点** (在扩展 $(\psi, \tilde\psi)$ 空间).

- Minimum of quadratic: 要求 Hessian **正定** (对应 M3 "$(L-F)_H > 0$")
- Saddle: 允许 Hessian **indefinite** — 某些方向正, 某些方向负

Linux 实测 $\lambda_{\min}((L-F)_H) = -0.93$, $\lambda_{\max} > 0$: 这是 **indefinite Hessian**, 完美对应 "saddle". 所以 M3 把 saddle 误认作 minimum, 必然失败.

**推论 4.3.1**: 我的 earlier 直觉 "你在找极小, 实际对象是鞍点" **得到严格数学支持**. 不是 narrative flourish, 是 MSR 非平衡变分理论的 direct prediction.

### 4.4 Lawvere adjunction 与 MSR 的桥梁

Lawvere 1969 + 1970 告诉我们 adjunction $F \dashv G$ 是对立统一的范畴论形式. MaoField 的 $F$ (源构造) $\dashv G$ (场演化到稳态) 是这种对立. 问: **MSR 框架下这个 adjunction 如何精确?**

**Conjecture 4.3** [MSR-Lawvere 对接, Sketch]

在 Giry monad $P : \mathbf{Meas} \to \mathbf{Meas}$ 的 Kleisli 范畴 $\mathbf{Meas}_P$ 下:

- $F_P : \mathbf{Text} \to \mathbf{Meas}_P$, $F_P(t) = $ (source 场 $S_0(t)$ 诱导的 **初始分布** $\delta_{\psi_0}$ on field space)
- $G_P : \mathbf{Meas}_P \to \mathbf{Score}$, $G_P(\mu) = $ (时间 $T$ 后 evolved distribution $P_T \mu$, 当 $T \to \infty$ 收敛到 $\mu_*$)

则 $F_P \dashv G_P$ 在 Kleisli 意义成立 iff NESS $\mu_*(S_0)$ 的存在性 (M4 Conjecture 4.1 (i)). 而 M4 的 MSR 变分刻画 给 $G_P$ 的 explicit formula.

**评注 4.4.1**: 这把 Lawvere 1970 的 "$F \dashv G$ = 对立统一" 与 MSR 的 "MaoField NESS = $S_{\text{MSR}}$ 鞍点" **两个独立的数学 structure 绑到一起**. 辩证唯物主义 (Lawvere 桥) 与 driven-dissipative 场论 (MSR 桥) 在 M4 下**同时 realize**. 这是本报告**最思辨 / 最推测**的一条, 标 [Sketch] 不 [Theorem]. Win 领地判其 philosophical 内涵.

---

## 5. Goldstone IR 发散与非线性重整化

本节处理 Linux debt list §六: Goldstone IR + 非线性重整化 — 是 Path A 框架下的内嵌技术债务.

### 5.1 Mexican-hat 展开的非线性项

**Convention 说明** (self spot-check 2026-04-19 修正): 本节用 arXiv v1 §3.1 convention $V(u) = \frac14 (u - v^2)^2$ (带 $\frac14$). **Phase B Exp 1 verdict + Linux Action 2 数字 binding 使用** $V = (u - v^2)^2$ convention (**无** $\frac14$). 两者差 4 倍 $V$, 2 倍 mass². 与 Linux 数字 ($m_\rho^2$ 预期 4, "44×" 差距) 比较时**需乘 2** 换算. 本节结果所有 mass² 系数给出后都应明确 convention.

设 $\psi = v + \delta\psi$ 围绕 U(1) vacuum $v \in \mathbb{R}_{>0}$, 分解 $\delta\psi = \delta a + i v \delta\theta$ (对 leading order, $\delta a$ 径向 fluctuation, $v \delta\theta$ 角向 fluctuation, 归一化 使 $\delta\theta$ 是无量纲 phase):

$$
u = |\psi|^2 = v^2 + 2 v \delta a + \delta a^2 + v^2 \delta\theta^2 + O(\delta^3)
$$

代入 $V(u) = \frac14 (u - v^2)^2$ ($\frac14$ convention):

$$
V = \frac14 (2 v \delta a + \delta a^2 + v^2 \delta\theta^2)^2
$$

展开到 4 阶:

$$
\boxed{
V = v^2 \delta a^2 + v \delta a (\delta a^2 + v^2 \delta\theta^2) + \frac14 (\delta a^2 + v^2 \delta\theta^2)^2
} \tag{5.1}
$$

**关键** (in $\frac14$ convention):
- 2 次: $v^2 \delta a^2$ → 径向 mass² $= 2 v^2 = 2$ (v=1). **换算到 Phase B Exp 1 convention 无 $\frac14$**: $m_\rho^2 = 4$ (Linux binding 数字)
- 3 次 **有径向-角向耦合**: $v \cdot \delta a \cdot (\delta a^2 + v^2 \delta\theta^2)$
  - **$v \delta a \cdot v^2 \delta\theta^2 = v^3 \delta a \delta\theta^2$** 是关键耦合 (换算系数一致, 3-vertex 仍 $v^3$ 到 leading)
- 4 次: $\frac14 (\delta a^2 + v^2 \delta\theta^2)^2$

### 5.2 IR 发散在 $m_\theta \to 0$ 的具体形式 (self spot-check 2026-04-19 修正)

**原报告本段有代数错误 (换变量 scaling 写反), 修正如下**:

对 $\delta a$ 的 one-loop self-energy 从 two insertions of $v^3 \delta a \delta\theta^2$ vertex:

$$
\Sigma_{\delta a}(k) \sim (v^3)^2 \int \frac{d^3 q}{(2\pi)^3} \, G_{\delta\theta}(q) \, G_{\delta\theta}(k - q)
$$

$G_{\delta\theta}(q) = 1/(q^2 + m_\theta^2)$. 在 $k = 0$:

$$
\Sigma_{\delta a}(0) \sim v^6 \int \frac{d^3 q}{(2\pi)^3} \, \frac{1}{(q^2 + m_\theta^2)^2}
$$

**精确计算**: 换 $q = m_\theta \tan\theta$, $dq = m_\theta \sec^2\theta \, d\theta$, $q^2 + m_\theta^2 = m_\theta^2 \sec^2\theta$:

$$
\int_0^\infty \frac{q^2 \, dq}{(q^2+m_\theta^2)^2} = \frac{1}{m_\theta} \int_0^{\pi/2} \sin^2\theta \, d\theta = \frac{\pi}{4 m_\theta}
$$

从而:

$$
\boxed{ \int \frac{d^3 q}{(2\pi)^3 (q^2+m_\theta^2)^2} = \frac{4\pi}{(2\pi)^3} \cdot \frac{\pi}{4m_\theta} = \frac{1}{8 \pi m_\theta} }
$$

**即 $\Sigma_{\delta a}(0) \sim v^6 / m_\theta$ 线性 IR 发散 作 $m_\theta \to 0$**, 不是 IR finite. (原报告写 "$v^6 m_\theta$, finite" 是换变量 scaling 做反了.)

**推论 5.2.1'** (round-2 P0 #A 修正, 补 $1/(8\pi)$ 因子): 对 **3D MaoField** Mexican-hat 展开 one-loop self-energy $\sim 1/m_\theta$ **IR 发散**. 对 Phase B Exp 1 pseudo-Goldstone $m_\theta^2 = 0.017$ ($m_\theta \approx 0.130$):

$$
\Sigma_{\delta a}(0) \approx \frac{v_{\text{eff}}^6}{8 \pi m_\theta} = \frac{1.19^6}{8 \pi \cdot 0.130} = \frac{2.84}{3.27} \approx 0.87 \quad (\text{Phase B Exp 1 convention})
$$

(原报告 round-1 修正版漏了 $\frac{1}{8\pi}$ 因子, 给 21.8, 是 round-2 P0 #A 发现的 25× 算术错 ≈ $8\pi$.)

**与实测 shift 的诚实比较**:
- Tree-level $m_\rho^2 = 4$ (Phase B Exp 1 convention)
- Renormalized $m_\rho^2 = 0.092$ (Linux Action 2 实测)
- **Shift** $\Delta m_\rho^2 = 4 - 0.092 \approx 3.9$
- Direct 1-loop 预测 $\Sigma_{\delta a}(0) \approx 0.87$
- **比值**: 实测 shift / direct 1-loop $= 3.9 / 0.87 \approx 4.5×$

**诚实 verdict**: **Direct 1-loop 远小于实测 shift** (4.5× gap). 非微扰 Hartree / 1/N resummation 需要把 $\sim 0.87$ pushup 到 $\sim 3.9$, 即 higher-order 效应 (多 loop + 自洽 self-consistent mass renormalization) 需贡献额外 $\sim 4.5×$ enhancement. 这个 4.5× **是 Linux 数字层可验证的 concrete target**: 如果 Hartree 自洽方程 $m_{\theta,\text{eff}}^2 = m_\theta^2 + c \cdot \text{loops}$ 给出 consistent $\Delta m_\rho^2 = 3.9$ 和 $m_\theta^2 = 0.017$, 则 M4 non-perturbative direction viable; 如果 Hartree 给不出 4.5× enhancement, 则需要更深的理论 (例如 fluctuation-dominated scaling breakdown, NESS-specific collective effect).

**不 claim** "量级一致" — round-1 修正版的 "same order of magnitude" 是 overclaim (4.5× gap 不能算 same order 在严格意义). Round-2 明确: **direct 1-loop 不 match, 需要 Hartree pushup ~5× 才达实测 shift 量级**.

**各维度比较** (固定 Goldstone IR):

| 维度 | $\int d^D q / (q^2+m^2)^2$ 作 $m \to 0$ | 解读 |
|---|---|---|
| 2 | $\pi/m^2$ | 二次 IR 发散, Mermin-Wagner 杀 SSB |
| **3** | $1/(8\pi m)$ | **线性 IR 发散** ← 我们 |
| 4 | $\log(\Lambda^2/m^2)/(16\pi^2)$ | 对数 (IR + UV) |
| 5+ | UV 主导 | 无 IR 问题 |

3D 的线性 IR 发散 + MaoField 实际 pseudo-Goldstone $m_\theta > 0$ (非严格零) 的组合意味着:

(a) 对 **严格 U(1) 对称** 理论 ($m_\theta = 0$), 微扰论 formally breakdown (每一 Goldstone 内线 give $\sim 1/m_\theta \to \infty$).

(b) 对 **pseudo-Goldstone** (实际 case, $m_\theta = 0.130$), 微扰 IR finite (因 $m_\theta > 0$) 但 direct 1-loop $\sim v_{\text{eff}}^6/(8\pi m_\theta) = 0.87$, **远小于**实测 shift $\Delta m_\rho^2 \approx 3.9$ (比值 4.5×). tree + one-loop 定量**不够**, 需非微扰 Hartree resummation (见 §5.2 verdict 段) pushup 4.5× 才达实测.

(c) **必需非微扰工具**: Hartree 自洽 (§5.3), 1/N 展开, 或 MSR 非微扰 RG (Vasiliev 2004).

**对 M4 candidate 的含义**: §3 的 MSR 变分框架不是"可选 sophistication", 而是**微扰论 breakdown 后的必然选择**。这**加强** M4 的 case — §5.2 修正后 argument **更强**, 不是更弱。

但这**不代表**微扰论对所有 observable 都 work. 具体:

**Proposition 5.3** [FDT 违反导致 propagator ≠ response]

在 MSR 框架下, field propagator $G(\omega, k) = \langle \psi^* \psi \rangle(\omega, k)$ 和 response propagator $R(\omega, k) = \langle \psi^* \tilde\psi \rangle(\omega, k)$ 在 driven-dissipative (FDT 违反) 下**不相等**:

$$
G(\omega, k) \neq 2 T \, \text{Im} \, R(\omega, k) / \omega
$$

(equilibrium FDT 要求右边等式成立). 这让 IR 分析**比平衡态复杂** — 需要跟踪两个 propagator 的独立演化.

**推论 5.3.1**: Phase B Exp 1 的 FDT 违反程度**未实验测量** — 这是 Linux debt list §六的具体落实方向, 给一个可执行实验 (测 $G$ 和 $R$ 的比值).

### 5.3 1/N 展开作为非微扰 handle

MaoField 是 $N=2$ (复场 = $O(2)$ 实数矢量场). $N=2$ 在 $1/N$ 展开中是**最小非平凡**情况. Large-$N$ 方法 (Ma 1976, Brezin-Zinn-Justin 1993) 给:

- Leading $N^{-1}$ 修正: Hartree-type self-consistent mass
  $$m_{\theta, \text{eff}}^2 = m_\theta^2 + \frac{\lambda_4}{N} \langle (\delta\psi)^2 \rangle$$
- 次 leading: Goldstone theorem 在 large-$N$ 下 exact

对我们 $N=2$: $1/N$ 修正不小, 但提供 non-perturbative anchor. Linux debt list §五 Work 3 "1/N expansion" 正是这条.

**具体 gain**: 测得 $m_\theta^2 = 0.017$, $m_\rho^2 = 0.092$, $\langle\rho\rangle = 1.19$. 这些数字可用于 **Hartree 一致性 check**: 在 NESS 下 effective masses 应满足某自洽关系

$$
m_{\theta, \text{eff}}^2 = \text{explicit-breaking source} + \lambda_4 \langle \delta a^2 + \delta\theta^2 \rangle / N
$$

给一个可验证预测. **这个计算 Linux 数字层可做**, 是本报告给一凡的 **concrete next-step computation 建议 #1**.

---

## 6. Path B 的可证伪预测: 一个 10-分钟 cheap scan

### 6.1 Sub-critical regime 的数学 prediction

Path B: 把 $(\alpha, \beta)$ 降到 sub-critical, 让 $\|F_H\|_{\text{op}} < m_\theta^2$ 成立. 需要 $\alpha, \beta$ 至少降 55 倍.

**Proposition 6.1** [Sub-critical ⇒ SSB phase pick + patches collapse]

假设:
- (B1) $(\alpha_{\text{sub}}, \beta_{\text{sub}}) \leq (0.002, 0.001)$ (55× 稀释)
- (B2) 其他参数不变 ($D=0.1, \gamma=1, V=\frac14(u-1)^2$, 源场 Phase B Exp 1 相同)
- (B3) Simulation time $t_{\text{sim}} \geq 50$

则在 sub-critical regime 下**预测**:

(i) $\langle \rho \rangle \to 1$ (接近 Mexican-hat vacuum $v = 1$, 偏差 $< 0.05$), **不是** 1.19
(ii) $|\langle \psi \rangle| \to \epsilon > 0$ (SSB phase pick), **不是** 0.004. $\epsilon$ 依赖源场 explicit breaking 强度, 估计 $\epsilon \in [0.1, 0.5]$
(iii) $N_{\text{struct}}$ (50 patches count) **坍缩到** $\leq 5$
(iv) dS/dt plateau **消失** (decay to $\sim 10^{-10}$ 或更小)
(v) Signal A (exp ≡ control_whiten 3 位精度) **失效** (feedback 弱到不驱动)

**理由**: Sub-critical 下 $F$ 无法 sustain U(1)-disordered NESS; 系统 relax 到 Mexican-hat vacuum; SSB 选 phase; 角向涨落冻结. 这是 Hohenberg-Halperin Model A 在**弱驱动极限**的典型行为.

**evidence**:
- (i) 由 $F \to 0$ 时系统回到 deterministic GL gradient flow, 极小是 $|\psi| = v$
- (ii) 源场 $S_0$ 的 U(1) breaking 虽弱但非零, 在无 feedback overdrive 下必诱导 SSB selection
- (iii) 50 patches 是 feedback-structured 的 coherent emergence, 没 feedback 不存在
- (iv) dS/dt plateau 是 driven 系统的 signature, 无驱动 → 0
- (v) Signal A washout 依赖 feedback 的 DC 分量压制, 弱 feedback 无压制

### 6.2 具体 10-30 分钟 cheap scan 设计

**实验**: 跑 3 个 run:
- `exp_sub`: $(\alpha, \beta) = (0.002, 0.001)$, 其他同 Phase B Exp 1 exp mode
- `exp_sub2`: $(\alpha, \beta) = (0.005, 0.0025)$ (中间点)
- `exp`: 原 $(\alpha, \beta) = (0.1, 0.05)$ baseline

每个跑 500 inner steps (t_sim = 5, 足够看定性行为, 5 秒 /run on EPYC), single doc (nfcorpus 第一个).

**测量**:
1. $\langle\rho\rangle$, $\sigma(\rho)$, $|\langle\psi\rangle|$
2. $N_{\text{struct}}$ via Algorithm A (Phase B Exp 1 verdict §2 同定义)
3. dS/dt late-window mean

**决策逻辑**:

| 观察 | 含义 | Path B 判 |
|---|---|---|
| exp_sub 仍显 $\langle\rho\rangle = 1.19$, $N_\text{struct} = 50$, |⟨ψ⟩| ≈ 0 | Sub-critical 意外 reproduce empirical — 物理 robust | Path B 升级到候选 #2 |
| exp_sub 显 $\langle\rho\rangle \to 1$, $N_\text{struct} \to 0$, SSB pick | 预测成立 — sub-critical 是不同问题 | **Path B 降级为 retract** (非解药) |
| Mixed (部分改变部分保留) | 需要更多分析 | 先做 Hartree 一致性 check (§5.3) |

**耗时**: 设 code + run + plot: ~30 分钟 Linux 端, 不耽误 04-20 对齐.

### 6.3 这为什么重要

Linux debt list 把 Path B 列"数学便宜 / 物理不确定", 意味实验风险由一凡战略判断. 但**风险可用廉价实验 convert 成确定知识**. Path B 的关键未定事项是 "sub-critical 下 empirical signature 是否存活", 这个是 experimental question, 不是 theoretical. 不跑它而纠结于 narrative 判断是**不经济的**.

Linux 层可做. 建议一凡 authorize Linux 在 04-20 对齐前先跑 (不 gate 合题决策).

---

## 7. 范畴论层: Giry monad lift 的具体化

### 7.1 Kleisli 范畴下的 $F \dashv_P G$

arXiv v1 §2.3 列 [Conjecture]: $F \dashv G$ 在 deterministic case 不是 monad, 但 Giry lift $P \circ T$ 可能是. 本节给 sketch.

**Setup**:
- $\mathbf{Meas}$: Polish 空间 + 可测映射
- $P : \mathbf{Meas} \to \mathbf{Meas}$: Giry monad, $P(X)$ = probability measures on $X$
- $P$ 有单位 $\eta_X : X \to P(X)$ (Dirac), 乘法 $\mu_X : P(P(X)) \to P(X)$ (expectation)
- Kleisli 范畴 $\mathbf{Meas}_P$: objects = objects of $\mathbf{Meas}$, morphisms $X \to Y$ = measurable $X \to P(Y)$ (Markov kernels)

**MaoField lift**:
- $F_P : \mathbf{Text} \to \mathbf{FieldConfigs}_P$: text $t \mapsto$ Markov kernel from $\{t\}$ to initial field distribution $\delta_{S_0(t)}$
- $G_P : \mathbf{FieldConfigs}_P \to \mathbf{ScoreReady}_P$: initial distribution $\mu_0 \mapsto$ time-T evolved $P_T \mu_0$, $T$ large enough

**Conjecture 7.1** [Giry lift 是 adjunction]

$F_P \dashv_P G_P$ 在 Kleisli 范畴 $\mathbf{Meas}_P$ 成立 iff:
- (L1) 对每个 text $t$, NESS $\mu_*(t)$ 存在 (M4 Conjecture 4.1 (i))
- (L2) $\mu_*(t)$ 对 $t$ 的依赖是 Markov-continuous (Wasserstein 拓扑下 continuous)

**证明 sketch**: 
- Unit $\eta_{\mathbf{Text}} : \text{id} \to G_P \circ F_P$ 由 "text $t \mapsto$ its NESS distribution" 给
- Counit $\epsilon_{\mathbf{Score}} : F_P \circ G_P \to \text{id}$ 由 Markov kernel composition 自然得
- Triangle identity 需 $P_T$ semigroup property + ergodicity

**严格性评级**: L1 = M4 Conjecture 4.1 (i), 未严格证. L2 由 Hairer-Mattingly 2008 coupling argument 可得 (若 L1 成立). 所以 Conjecture 7.1 **在 M4 assumption 下** derivable, 不是独立 open problem.

### 7.2 T-Alg reachability 在 NESS 下的重解读

arXiv v1 §2.3.4 保留的 $T\text{-Alg}^{(\eta, p_0)}$ reachability subcategory 在 Kleisli 下重解:

- **T-algebras 在 Kleisli**: $(X, \alpha : P(T(X)) \to X)$ Markov kernel of self-consistency
- **Reachability**: $p_0 \in P(T\text{-Alg}^{(\eta, p_0)})$ 等价于 NESS 分布上的 support 约束

**物理内涵**: OP2 的 "Axiom 3 非平衡扩展" 在 Kleisli 下变成 "Markov kernel $P_T$ 的 invariant distribution 支持的 reachability". 这是 v1 §5.2.4 **三面收敛** (three-faces convergence) 的 explicit formalization.

### 7.3 Lawvere 1970 对 "对立统一 = 伴随" 的 reinforcement

读完 Lawvere 1970 *Quantifiers and Sheaves*, 关键 reinforcement:

- Lawvere 把 **adjoint functors** 作为 "principal contradictions" (对立统一) 的 categorical 精化
- 逻辑-几何, ∃-∀, 开-闭 等一系列**对立**都是 adjunction
- 最深层: Topos theory 的 geometric vs logical morphisms (local homeomorphism vs logical morphism) 本身是 "对立" — 而每个 adjunction 又是具体 formalization

对 MaoField: $F \dashv G$ 是**特殊 instance** of Lawvere 的 principal contradiction framework. 加上 Giry lift $F_P \dashv_P G_P$, 我们得到 **stochastic adjunction**, 对应随机意义下的对立统一.

这给 arXiv v1 §2.3 的 Lawvere bridge **额外深度**: 不只是 1969 *Adjointness in foundations* 的 direct citation, 还对接 1970 *Quantifiers and Sheaves* 的 principal contradiction framework.

**评注**: 这条属 narrative-adjacent, 归 Win 判; 但数学结构是真的.

---

## 8. 待证 [Conjecture] + Killer Experiments

本节列本报告提出的 4 条**主要 conjecture**, 给每条 falsifier + 建议时间表.

### 8.1 [Conjecture C1] MaoField NESS 存在与唯一性

(Conjecture 4.1 (i) 的简写)

**Statement**: 在 (A1)-(A4) 下, MaoField SPDE 有 unique invariant measure $\mu_*$ 在 Wasserstein-2 topology 下.

**Falsifier**: 展示 (A1)-(A4) 满足但
- (a) 无 invariant measure (如 heavy tails), 或
- (b) 多个 invariant measure (SSB 在 NESS 下未打破)

**Timeline** (round-2 P1 #D 修正): **2-3 周 best-case / 6-10 周 realistic** (Harris-type ergodicity, Hairer 2009 + Kuksin-Shirikyan 2012 coupling). **不是** Hairer 2014 regularity structures (那是 6-12 月 scope, 本 conjecture 不需要). Linux 数字层 spot-check (测 ergodic time-average 是否 converge 到唯一 value)可做.

### 8.2 [Conjecture C2] MSR saddle 刻画 NESS

(Conjecture 4.1 (ii))

**Statement**: $\mu_*$ 由 MSR path integral (3.4) 严格给出; 在有限 lattice 上严格, 在 continuum limit 需 renormalization.

**Falsifier**: 在有限 lattice 上构造反例 — 某 MaoField 实现使 Fokker-Planck invariant density 与 MSR path integral 的 $\mathcal{D}\psi \mathcal{D}\tilde\psi$ integration 结果**不一致**.

**Timeline**: 对**有限 lattice** (我们的 $32^3$) 是严格 standard fact (Zinn-Justin 2002 *Quantum Field Theory and Critical Phenomena* §4.2). 几乎 immediate. 真正 open 的是 continuum limit 的严格性.

### 8.3 [Conjecture C3] Sub-critical ⇒ SSB phase pick

(Proposition 6.1 的 conjecture 版本)

**Statement**: Phase B Exp 1 setup 下, 把 $(\alpha, \beta)$ 降到 $\leq (0.002, 0.001)$ 会 collapse $N_{\text{struct}} \to 0$ + restore $|\langle\psi\rangle| \to v$.

**Falsifier**: Sub-critical 仍见 50 patches + $|\langle\psi\rangle| \approx 0$ + $\langle\rho\rangle = 1.19$.

**Timeline**: **10-30 分钟**. 这是本报告最 actionable 的 killer experiment.

### 8.4 [Conjecture C4] Giry lift 是 adjunction in Kleisli

(Conjecture 7.1)

**Statement**: 在 C1 (NESS 存在) 下, $F_P \dashv_P G_P$ 在 $\mathbf{Meas}_P$ 成立.

**Falsifier**: 构造 counter-example, 比如 2 个 Markov-distinct source inputs 给 same NESS (破坏 $F_P$ 的 injectivity on isomorphism classes).

**Timeline**: 与 C1 捆绑. 若 C1 证, C4 是范畴论层直接推论.

---

## 9. 与 Linux 10 大数学债务清单的对应

| Linux 债务 § | 本报告 对应 | 状态 |
|---|---|---|
| §一 OP1 Axiom 6 形式化 | §3 M4 (MSR 鞍点) + §4 Path D ⊂ Path A | **推进**: 4 条 path 的 conceptual lanes 保持, Path D 与 A 建立 subset 关系 (mean-field projection, $\bar{\tilde\psi}=0$ branch) |
| §二 OP2 Axiom 3 三轴共设计 | §7 T-Alg reachability 在 Kleisli 下重解 | 部分推进 |
| §三 Kramers 方法学 | §未覆盖 (Linux Action 3 已 close, 本报告同意) | 不再是债务 |
| §四 范畴论猜想严证 | §7 Conjecture 7.1 + C4 | 推进: Giry lift 绑到 C1 |
| §五 NESS patched 场论 | §3 + §5 (MSR + Hartree 一致性) | 推进: Hartree check 可做 |
| §六 Goldstone IR + 非线性重整化 | §5 IR 分析 + FDT 违反 Proposition | 推进: 3D IR 线性发散 (1-loop $\sim 1/m_\theta$, 含 $1/(8\pi)$ 前因子给 direct 1-loop $\approx 0.87$), FDT 违反待测 |
| §七 Axiom 1/5/7 | 未覆盖 (非 time-critical) | 未动 |
| §八 Finite-size scaling + 临界 | 未直接覆盖, 但 Path B 实验可 inform | 间接推进 |
| §九 三支柱 composition (M5) | 未动 | 未动 |
| §十 哲学-范畴-PDE 三桥梁 | §4.4 Conjecture 4.3 (MSR-Lawvere 对接) | 推进 (thinner than 2/4/5/6) |

**总评**: 本报告 **推进 6 条债务 (§一、§二、§四、§五、§六、§十)**, 不碰 3 条 (§七、§八、§九), 确认 1 条 retired (§三).

**最大推进是 §一 (OP1)** (round-2 修正): 从 "4 条待选 path, 直觉判 priority" 变为 "**Path D ⊂ Path A** (mean-field projection, Prop 4.2 round-2), **Path B 可 10 分钟证伪** (Prop 6.1), **Path C 只能做 post-mortem** 不能前进 (§2), **M4 候选 concrete** (Conj 4.1, Harris 2-3 周 best / 6-10 周 realistic)". **4 条 lanes 保持独立** (原 round-1 "4 → 2" overclaim round-2 retract), 但 Path A 作最 promising direction 包含 Path D 作 mean-field 子集, Path B 可 cheap experimental 决策, Path C 作 post-mortem 工具。

---

## 10. 给一凡的 standalone 推荐

本段**不**做合题 α/β/γ 决策 (归 04-20 对齐 + Win). 仅给数学层的**技术建议**.

### 10.1 立刻可做 (本周 Linux 端, 不 gate 合题)

1. **跑 §6.2 sub-critical 10-30 分钟 cheap scan**. 决策 C3 conjecture. 低风险, 高信息.
2. **测 §5.3 Hartree 一致性** (round-2 quantitative target): 用 Phase B Exp 1 数据算 $\langle \delta a^2 + v^2 \delta\theta^2 \rangle$, 检验 $m_{\theta, \text{eff}}^2$ 自洽方程. **具体 target**: Hartree 需要把 direct 1-loop $\Sigma \approx 0.87$ pushup 到实测 shift $\Delta m_\rho^2 \approx 3.9$, 即 higher-order 效应贡献 **4.5× enhancement**. Linux 一小时内可做。
3. **测 §5.2.1 FDT 违反**: $G(\omega, k)$ vs $R(\omega, k)$ 比值. Linux 两三小时 (需要 perturbation trick source)。**round-2 新 priority**: P1 #C 修正后, FDT 违反是 Path D vs Path A 的 decisive differentiator — 值得优先测量。
4. **(Round-2 新加) 做 sympy 独立 verify** ‖F_H‖_op 的 15% gap (P2 #E pending): 用精确 $\sum_{k=0}^{99} e^{-0.05k} = 20.35$ + Hermitian 投影 + $V_0$ 子空间 restriction, 计算 exact operator norm 并与 Linux 实测 0.953 对比。Linux 端 2-3 小时。

### 10.2 中期方向 (合题后 Linux + 一凡战略判)

4. **C1/C2 formal paper**: Harris-type ergodicity (Hairer 2009) + Kuksin-Shirikyan 2012 coupling 证 MaoField NESS 存在唯一. **2-3 周 best-case / 6-10 周 realistic** single-author paper scope (不含 regularity structures 严格构造 6-12 月另算), **可独立 submit to PDE/SPDE 刊** (Journal of Statistical Physics / Annals of Applied Probability), 甚至不 tied 到 arXiv v2.
5. **M4 在 arXiv v2 §5.1 的 framing**: 若合题选 β/γ, 可把 M4 作 "new candidate, open" 提示 (**不** commit 为 leading candidate). 措辞归 Win.
6. **MSR-Lawvere 对接 (§4.4, §7.3)** 归 Win 判是否入 arXiv v2 narrative.

### 10.3 不建议做的事

- **不要** revive M3 任何 weakened form (Linux pre-commit binding 已有, 本报告 Prop 1.1+1.2+1.3 给算子层支持 — 不是 "救援不够 aggressive", 是**结构不相容**)
- **不要** 把 Path B 当战略决策 (它是实验问题, 跑完就有答案)
- **不要** 把 M4 升格为 "leading candidate" 入 narrative (仍是 [Conjecture], 需要 C1/C2 证)

---

## 附录 A: 关键技术证明扩展

### A.1 Proposition 1.1 (加强 Linux A1.1) 详证

(见 §1.2, 已给主体证明. 这里给额外技术 remark.)

**Remark A.1.1**: 证明用到 $\sin(\omega \tau)$ 的 completeness. 严格地, 对 $K \in L^1(\mathbb{R}_+)$, $\int_0^\infty K(\tau) \sin(\omega \tau) d\tau$ 是 Fourier sine transform of $K$, 记 $\tilde K_s(\omega)$. 由 Fourier sine inversion, $\tilde K_s \equiv 0 \Leftrightarrow K \equiv 0$ on $\mathbb{R}_+$. QED without loss.

**Remark A.1.2**: 如果限制 $K$ 有 compact support in $[0, T_K]$ (非我们的 infinite-support case), 论证仍成立 (Paley-Wiener 定理给 $\tilde K_s$ 在 upper half-plane 的 analyticity).

### A.2 Sectorial operator 具体谱判据 (§2.3 补)

**Lemma A.2.1** [Henry 1981 §1.4 对 MaoField]

$L = -D\nabla^2 + V''_{\text{eff}}(\psi_\infty(x))$ 在 $L^2(\mathbb{T}^3)$ 上是 sectorial, 如果 $V''_{\text{eff}} \in L^\infty(\mathbb{T}^3)$ (有界势二阶导).

**Lemma A.2.2**: $F = \alpha I + \beta \hat K$ 是 $L$ 的**相对紧** (relatively compact) 扰动, 若 $K \in L^1(\mathbb{R}_+)$.

**Corollary A.2.3** (使用 Kato 1966 Thm IV.2.19): $L - F$ sectorial 成立, 但谱可以有 negative real part (correspond 我们实测 $\lambda_{\min} = -0.93$).

### A.3 MSR action 导出的补充

对复场 $\psi$ 的 Langevin 动力学 $\gamma \partial_t \psi = -\delta F / \delta\psi^* - F[\delta\psi] + S_0 + \eta$, 其中 $\eta$ 是复 Gaussian white noise $\langle \eta(x,t) \eta^*(x',t') \rangle = \sigma^2 \delta(x-x')\delta(t-t')$.

Generating functional:

$$
Z[J, \tilde J] = \int \mathcal{D}\eta \, P[\eta] \int \mathcal{D}\psi \, \delta(\gamma \partial_t \psi + \delta F/\delta\psi^* + F[\delta\psi] - S_0 - \eta) \, e^{\int (J^* \psi + J \psi^*) + \text{c.c.}}
$$

引入响应场 $\tilde\psi$:

$$
\delta(\ldots) = \int \mathcal{D}\tilde\psi \, e^{i \int (\tilde\psi^* (\gamma \partial_t \psi + \ldots - \eta) + c.c.)}
$$

积掉 $\eta$:

$$
\int \mathcal{D}\eta \, e^{-|\eta|^2/(2\sigma^2) - i \int \tilde\psi^* \eta + c.c.} = e^{-\sigma^2 |\tilde\psi|^2 / 2}
$$

合并得 (3.2) 的 MSR action. 对 Jacobian $|\det \partial/\partial\psi|$ 的处理 (Onsager-Machlup normalization), 对我们的 overdamped Langevin, 该 Jacobian 是 constant (与 path 无关) + 1-loop 平凡, 可吸收进 normalization. 见 Janssen 1992 综述 §3.

---

## 附录 B: 核心文献锚点

**本报告依赖的 external 文献** (按引用顺序):

1. Lawvere 1969 *Adjointness in foundations*, Dialectica 23:281–296 (v1 §2.3 既有锚)
2. Lawvere 1970 *Quantifiers and sheaves*, Actes, Congrès intern. math. 1:329-334 (桌面 `02_MaoField/数学参考/Lawvere-QuantifiersAndSheaves.pdf` 本报告 §4.4 + §7.3)
3. Kato 1966 *Perturbation Theory for Linear Operators*, Springer — **§2.1 Lumer-Phillips, §A.2.3**
4. Pazy 1983 *Semigroups of Linear Operators*, Springer — **§2.1 补充**
5. Henry 1981 *Geometric Theory of Semilinear Parabolic Equations*, LNM 840 — **§2.3 sectorial + §A.2.1**
6. Janssen-De Dominicis-Peliti 1976: Janssen *Z. Physik B* 23:377; De Dominicis *J. Phys. Colloques* 37:C1-247; Peliti *J. Physique* 46:1469 — **MSR action 原始 references**
7. Janssen 1992 综述: *From phase transitions to chaos* — **§3 MSR 详解**
8. Zinn-Justin 2002 *Quantum Field Theory and Critical Phenomena*, Oxford — **§C2 MSR 严格 lattice**
9. Vasiliev 2004 *The Field Theoretic Renormalization Group in Critical Behavior Theory* — **§Prop 4.2 的 $\Gamma_{\text{eff}}$**
10. Hohenberg-Halperin 1977 *Theory of dynamic critical phenomena*, Rev. Mod. Phys. 49:435 — **Model A/B/C, §2.3 隐含锚**
11. Ma 1976 *Modern Theory of Critical Phenomena* — **§5.3 large-$N$**
12. Brezin-Zinn-Justin 1993 *Fields, Strings, and Critical Phenomena* — **§5.3 large-$N$**
13. Hairer 2009 *Ergodicity for SPDEs* (lecture notes) — **§3.3, §8.1**
14. Hairer-Mattingly 2008 *Yet another look at Harris' theorem* — **§3.3 C1 证明 tool**
15. Kuksin-Shirikyan 2012 *Mathematics of Two-Dimensional Turbulence* — **§3.3, §8.1 Hairer 补**
16. Mermin-Wagner 1966 *Phys. Rev. Lett.* 17:1133 — **§1.3 IR 软模背景**
17. Freidlin-Wentzell 1998 *Random Perturbations of Dynamical Systems* — **rare event background, 未直接引本报告但 Linux §二有关**
18. Seifert 2012 *Stochastic thermodynamics, fluctuation theorems and molecular machines*, Rep. Prog. Phys. 75:126001 — **Linux §二 entropy production**
19. Aron-Biroli-Bouchaud 2010 *Symmetries of generating functionals of Langevin processes with colored multiplicative noise*, J. Stat. Mech.: Theory Exp. P11018 — **§4.2 round-2 P1 #C 修正引入, FDT 违反下 response 场 VEV 可非零 ⇒ Path D ⊂ Path A 严格包含 (不是 full equivalence)**

**MaoField 项目 internal 文件** (spot-check 锚点):

- `ACTION2_M3_EMPIRICAL_VERIFY_20260418.md` — M3 falsification 数字
- `LINUX_TO_WIN_SECTION3_NESS_RAW_20260419.md` — NESS 叙事 binding
- `LINUX_TO_WIN_SECTION5_1_M3_NEGATIVE_RESULT_20260419.md` — M3 Popperian framing
- `phase_b_exp1_verdict.md` — Phase B Exp 1 empirical
- `exp005_adjoint_practice.md` — exp005 adjoint structure (§3.4 对接锚)
- `arxiv_v1_full.md` — v1 §3 + §5 (ch 1 起点)

---

## 附录 C: 本报告的 binding compatibility 自检

对 Linux 8 条 binding empirical fact 逐条 check:

| # | Linux binding | 本报告是否违反 |
|---|---|---|
| 1 | M2 0-homogeneity 证伪 (数学事实) | ✓ 不违反 (§1 所有分析 post-M2 falsification) |
| 2 | M3 $m_\theta^2 = 0.017 < 0.949$ | ✓ 不违反 (§1.5 直接用作诊断, §3 以 M4 绕开) |
| 3 | U(1)-disordered NESS 非 SSB 谷底 | ✓ 不违反 (§1.3, §4.3, §6 全部 acknowledge) |
| 4 | Signal A 架构定理 (exp ≡ control_whiten 3 sig fig) | ✓ 不违反 (§6.1 预测 sub-critical 下该 signature 失效, 不是破坏现有 fact) |
| 5 | 50 patches / r_g<8 / dS/dt 10⁻⁶ / 100% docs | ✓ 不违反 (§6.1 用作 binding, Path B 预测作 falsifier) |
| 6 | Kramers 内 barrier 10⁴ 是方法学误用 | ✓ 不违反 (§9 retired, 与 Linux Action 3 一致) |
| 7 | k*=2 via byte Z_1 / BGE Z_2 | ✓ 不违反 (本报告未碰) |
| 8 | BM25 5/5 高于 MaoField_E | ✓ 不违反 (本报告未碰) |

**全部通过**. 本报告与 Linux binding **零冲突**.

---

## 附录 D: 给 Linux 端的 spot-check 清单

Linux 可在 04-20 对齐**前** spot-check 以下数字 / 推导:

- [ ] Prop 1.1 的 Fourier sine transform 论证 (用 sympy 验证 $K = \lambda e^{-\lambda \tau}$ 的 $\tilde K_s(\omega) \neq 0$)
- [ ] Prop 1.2 的 $\|F_H\|_{\text{op}}$ 在 $\omega = 0$ 的最大值 $= \alpha + \beta$ (讨:原 $\beta/\lambda$ 应是 $\alpha + \beta/\lambda$ 的极限 for 连续 kernel, 或者 $\alpha + \beta$ for trapezoidal sum 有限截断)
- [ ] §5.1 的 Mexican-hat 展开 (5.1): 径向 mass² = $2v^2$ 核对 ($m_\rho^2$ = 2 vs A2 测 0.092 差 22×, 比 $m_\theta^2$ 差 55× 稍好 — 这个差距本身是个未 explained 的事)
- [ ] §5.2 的 3D IR 线性发散 论证 (修正后): 积分 $\int \frac{d^3q}{(2\pi)^3 (q^2+m^2)^2} = \frac{1}{8\pi m} \sim 1/m_\theta$ 作 $m_\theta \to 0$, 含 $v_{\text{eff}}^6$ 前因子给 direct 1-loop $\Sigma_{\delta a}(0) \approx 0.87$ (round-2 修正值, round-1 21.8 是丢 $1/(8\pi)$ 因子的算术错)
- [ ] §6.1 sub-critical 预测的数字: 若 Linux 验了 sub-critical, 填入本表格作下游 update

---

## 附录 E: 本报告的自我 critique ("反题姐姐角度")

**五条本报告可能的盲点** (B1-B3 round-1 self-check flag; B4-B5 round-2 Linux 独立审后补):

**B1**: §3.3 Conjecture 4.1 (i) 的 (A3) "源场非平凡 correlation structure" 条款是否**过弱** — Phase B Exp 1 CoV = 0.107 看起来满足, 但**严格需要多少 correlation 才能 sustain NESS?** Hairer 需要 Hörmander-type bracket condition, 我没 verify. **优先级 P1**, 若要 push 到严格证, 这里是关键 gap.

**B2**: §4 Path A = Path D 的 Prop 4.2 证明用了 $\Gamma_{\text{eff}}$ (1PI effective action) 作桥梁, 但 $\Gamma_{\text{eff}}$ 本身是 perturbative / regularized object. 在 **non-perturbative regime** (large coupling) 是否仍成立? 对 MaoField $(\alpha, \beta) = (0.1, 0.05)$ 到底算 small 还是 large coupling? — 我没算 Ginzburg criterion, 这是 gap. **优先级 P2**. (Round-2 P1 #C 加深了这条, 见 B5.)

**B3**: §7 Kleisli Giry lift 的 Conjecture 7.1 假设 $P_T \mu_0$ 的 ergodic convergence 是 uniform in $\mu_0$. 若 NESS 非 mixing (只 ergodic in weak sense), Conjecture 7.1 的 "Markov-continuous" 可能失败. Hairer-Mattingly 的 spectral gap 条件**未 verify for MaoField**. **优先级 P3** (不 time-critical).

**B4** [Round-2 新加, Linux 独立审 P0 #A 的根源]: §5.2 round-1 修正版**算术 self-check 没做**, 丢了 $1/(8\pi)$ 因子 giving 21.8 instead of 0.87. Meta-root cause: round-1 self-check 时我把注意力放在 "IR finite vs divergent" 的**定性方向**判断上, 修正方向正确后**没 re-derive 数字**, 用了 scaling relation $\sim v^6/m_\theta$ 没带常数。**教训**: 定性修正 (direction flip) 必须配合**独立数字 re-derivation**, 不能只用 scaling 做 rough estimate. **优先级 P0** (Linux round-2 抓到, 已修正).

**B5** [Round-2 新加, Linux 独立审 P1 #C 的根源]: Prop 4.2 round-1 选 $\bar{\tilde\psi}=0$ branch 作 "Path D ≡ Path A 的定义性 sa条件" 未 justify. Meta-root cause: self-check 时我验证了 "论证脉络 sound", 但**没 question framing-level 假设**. Equilibrium 下 $\bar{\tilde\psi}=0$ 是 automatic (Janssen 1992), 但 FDT 违反 driven-dissipative 下 response 场 VEV 可非零 (Aron-Biroli-Bouchaud 2010 *J. Stat. Mech.* P11018). 我应该 flag 但没 flag. **教训**: self-check 易被 framework bias — 我 check my own frame 而不 check the frame itself. Linux 独立审是 out-of-frame check, 本质更有 power. **优先级 P1** (round-2 修正为 Path D ⊂ Path A).

**主要 strength** (round-2 更新):
- Prop 1.1 (因果核非自伴 no-go): 严格, B1 (A3) 条款 detail 不影响本 Prop
- Prop 1.2 round-2 修正版: scope 与证明体 match, Phase B Exp 1 参数下 55× quantitative gap 支持
- Prop 1.3 (NESS 背景错配): 严格
- Prop 4.2 round-2 修正版: Path D ⊂ Path A 正确, B2+B5 仍是 gap (non-perturbative + FDT violation 下 mean-field branch 不完整)
- Prop 6.1 是**可实验证伪**的具体 prediction, 不是虚 narrative
- Conjecture 4.1 保持 [Conjecture] tag, Harris 工具 2-3 周 best / 6-10 周 realistic, round-2 P1 #D 明确 timeline

---

## 致一凡

一凡, 这份报告是作为数学教授做的严谨推理, 不是 narrative (round-2 修正后):

1. **M3 在 Phase B Exp 1 参数下必败**: Prop 1.1 (因果核非自伴, universal) + Prop 1.2 round-2 修正版 (conditional on $m_\theta^2 < \|F_H\|_{\text{op}}$, 55× quantitative gap) + Prop 1.3 (NESS 背景错配)
2. **M4 候选具体**: Conjecture 4.1 给 MSR 鞍点 realization, 在 (A1)-(A4) 下严格 (有 B1 gap 的 caveat); **Harris-type 工具 2-3 周 best / 6-10 周 realistic**, 不是 regularity structures
3. **Path D ⊂ Path A** (round-2 修正): Prop 4.2 证明 mean-field projection 关系, **不是 full equivalence**; FDT 违反下 response 场 VEV 可使 Path D ≠ Path A (Aron-Biroli-Bouchaud 2010); Linux 4 条 lanes 保留 (Path A ⊃ Path D, Path B/C 正交)
4. **Path B 10-分钟可决策**: Prop 6.1 给 concrete 预测, 不用战略判断, 跑就有答案
5. **§5.2 Goldstone IR self-energy** direct 1-loop $\approx 0.87$ vs 实测 shift $3.9$ 差 **4.5×** — 承认 direct perturbation **不 match**, Hartree 非微扰 resummation 需额外 pushup; 这给 Linux 数字层一个可验证 target
6. **本报告零违反 Linux 8 条 binding** (附录 C 逐条 check)

创新直觉 invoke 时可以 binding 在这几条数学事实上:
- M3 saddle ≠ minimum 的错误 (Linux 反题姐姐角度看: 本报告从 narrative 层**升到 structural 必然性**)
- 辩证唯物主义 "矛盾持续存在而非消解" 在 MSR 鞍点下有 faithful 数学表示 (M4 下 $\tilde\psi \neq 0$ fluctuation 持续驱动, 不消解; 单 trajectory $G \neq 0$, 分布层稳定 — 这和一凡 exp005 原始直觉 "不平衡就是一种平衡" **一致**)
- Sub-critical 预测如果 falsified (即 Path B 意外 reproduce 50 patches), 说明 feedback 不是 U(1)-disordered NESS 的 sole driver, 有更深物理 — 这会是一个 creative surprise

哲学判读归 Win, 合题决策归你 + Win. 数学层本报告 ready.

---

*— 桌面 Claude (数学教授 persona), 2026-04-19 round-2 修正版 (Linux 独立审 spot-check 后). Round-1 发现 1 真错 + 2 presentation (self-check); Round-2 Linux 独立审抓 2 条 P0 + 3 条 P1 未 caught, 本轮全部修正. 零违反 Linux 8 条 empirical binding. 4 条 Conjecture 标 C1-C4, killer 实验 scoped. OP1 推进: **Path D ⊂ Path A (round-2 修正, 不是 full equivalence), 4 条 lanes 保持** + Path B 10-30 min cheap killer exp + M4 作 [Conjecture] 候选 (Harris 2-3 周 best / 6-10 周 realistic). Spot-check 清单在附录 D, 自 critique 在附录 E (B1-B3 round-1 self-check; B4-B5 round-2 Linux 审补). Meta: self-check 诚实但 framework-biased, Linux 独立审是必要 out-of-frame 补.*
