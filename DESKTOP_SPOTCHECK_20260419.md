# Desktop Spot-Check: DESKTOP_MATH_DEEP_ANALYSIS_20260419.md

**作者**: 桌面 Claude (同一 session, 作为"数学教授" 独立 spot-check 自己早先的报告)
**日期**: 2026-04-19 傍晚
**binding**: 诚实 > cushion。发现的错误如实报告, 不 hide, 不 soften。
**对象**: 一凡 + Linux (04-20 对齐前的 self-critique 补齐)

---

## 0. 执行摘要

本次 spot-check 覆盖原报告附录 D 的 5 条任务, **发现 1 条 substantive 数学错误 + 2 条 presentation/convention 不一致 + 2 条通过**:

| # | 任务 | 结果 |
|---|---|---|
| 1 | Prop 1.1 Fourier sine transform | ✓ 通过 |
| 2 | Prop 1.2 $\|F_H\|_{\text{op}}$ 最大值表达式 | ⚠️ 内部不一致 (conclusion vs bracket explanation) |
| 3 | §5.1 Mexican-hat $m_\rho^2$ convention | ⚠️ convention 差异未明确 |
| 4 | §5.2 3D one-loop IR finiteness | ❌ **错误** — 真正的数学错误, 是 IR divergent (∼1/m), 不是 finite |
| 5 | §6.1 sub-critical 55× 稀释数字 | ✓ 通过 |

**核心 verdict**:
- Prop 1.1, 1.2, 1.3 的**定性结论仍成立** (M3 在当前参数必败; 且在 Prop 1.2 的 U(1) conservation regime 任何参数必败)
- Prop 4.2 (Path A = Path D) 不受影响, 仍成立
- Conjecture 4.1 (M4 候选) 不受影响, 仍成立
- Prop 6.1 (sub-critical prediction) 数字自洽, 仍成立
- **但 §5.2 Goldstone IR 分析段必须实质性重写** (错误方向相反)

错误的根源: §5.2 的变量代换 + 积分 scaling 我做反了。原文 claim "3D IR finite", 实际 3D 这个 diagram **IR divergent**, 作 $m_\theta \to 0$ 线性发散 $\sim 1/m_\theta$. 这**不改变** M4 的 viability (Hartree 可 resum, 1/N 可 fix), 但改变**为什么需要非微扰工具**的论证性质 — 是**必须**, 不是可选。

---

## 1. Spot-Check 1: Prop 1.1 Fourier sine transform

### 1.1 任务

验证: 对 $K(\tau) = \lambda e^{-\lambda \tau}$ (因果核), 其 Fourier sine transform

$$
\tilde K_s(\omega) := \int_0^\infty K(\tau) \sin(\omega \tau) \, d\tau
$$

非恒零, 从而 Prop 1.1 的 "$\tilde K_s \equiv 0 \Leftrightarrow K \equiv 0$" 推论成立。

### 1.2 独立计算

用 $\sin(\omega\tau) = \frac{1}{2i}(e^{i\omega\tau} - e^{-i\omega\tau})$:

$$
\tilde K_s(\omega) = \frac{\lambda}{2i} \int_0^\infty \left[ e^{(-\lambda + i\omega)\tau} - e^{(-\lambda - i\omega)\tau} \right] d\tau
$$

$$
= \frac{\lambda}{2i} \left[ \frac{1}{\lambda - i\omega} - \frac{1}{\lambda + i\omega} \right]
= \frac{\lambda}{2i} \cdot \frac{2i\omega}{\lambda^2 + \omega^2}
= \frac{\lambda \omega}{\lambda^2 + \omega^2}
$$

### 1.3 结论

$\tilde K_s(\omega) = \frac{\lambda \omega}{\lambda^2 + \omega^2}$, 对任何 $\omega \neq 0$ 非零。

特别对 $\lambda = 0.05$ (项目值):
- $\tilde K_s(\omega = 0.1) = 0.05 \cdot 0.1 / (0.0025 + 0.01) = 0.005/0.0125 = 0.4$
- $\tilde K_s(\omega = 1) = 0.05/(0.0025 + 1) = 0.0499$

Fourier sine completeness (Plancherel 定理对奇延拓): $\tilde K_s$ 不恒零 ⇒ $K$ 不可能为零或 $c \delta_0$, 所以 $\hat K$ 非自伴。

**结果**: ✓ **通过**. Prop 1.1 数学严格, 无 errors.

---

## 2. Spot-Check 2: Prop 1.2 $\|F_H\|_{\text{op}}$ 最大值表达式

### 2.1 任务

原报告 Prop 1.2 证明中:
> "$F_H$ 贡献至少 $\alpha + \beta/\lambda_{\text{mem}}$ (Fourier 表象下 $\text{Re} \hat K(\omega) = \lambda_{\text{mem}}^2/(\lambda_{\text{mem}}^2+\omega^2)$ 在 $\omega = 0$ 处取最大 $1$, 所以 $\hat F_H(\omega=0) = \alpha + \beta$)"

**内部不一致**: conclusion 用 $\alpha + \beta/\lambda$, 括号解释给 $\alpha + \beta$. 到底哪个对?

### 2.2 独立验证

Phase B Exp 1 的 feedback 形式 (verdict §1):
$$
\delta S_{\text{history}}(t) = \sum_{k=0}^{N_\text{hist}-1} w_k \cdot \delta\psi(t - k \Delta t_{\text{outer}}) \cdot \Delta t_{\text{outer}}, \quad w_k = e^{-\lambda k \Delta t_{\text{outer}}}
$$

取连续 limit ($\Delta t \to 0$, $N_\text{hist} \to \infty$, $N_\text{hist} \cdot \Delta t$ 大):

$$
\delta S_{\text{history}}(t) \to \int_0^\infty e^{-\lambda \tau} \delta\psi(t - \tau) \, d\tau
$$

所以**项目的实际 kernel** 是 **non-normalized** $K_{\text{project}}(\tau) = e^{-\lambda \tau}$ (积分 $= 1/\lambda$).

Fourier: $\hat K_{\text{project}}(\omega) = \int_0^\infty e^{-\lambda\tau} e^{-i\omega\tau} d\tau = \frac{1}{\lambda + i\omega}$

$\text{Re} \hat K_{\text{project}}(\omega) = \frac{\lambda}{\lambda^2 + \omega^2}$

$\omega = 0$: $\text{Re} \hat K_{\text{project}}(0) = 1/\lambda$

所以 $\hat F_H(\omega=0) = \alpha + \beta \cdot (1/\lambda) = \alpha + \beta/\lambda$.

**数值**: $\alpha = 0.1, \beta = 0.05, \lambda = 0.05 \Rightarrow \alpha + \beta/\lambda = 0.1 + 1.0 = 1.1$

与 Linux Action 2 实测 $\|F_H\|_{\text{op}} \approx 0.95$ 的**差 15%**, 由有限 $N_\text{hist} = 100$ 截断 + 离散化 (Δt_outer = 1) 解释:

- 有限 $N_\text{hist}$ 截断因子: $(1 - e^{-\lambda N_\text{hist} \Delta t}) = 1 - e^{-5} \approx 0.993$ (<1% 影响)
- Riemann 和逼近连续积分 (Δt = 1 vs 理想 $\to 0$): 对 $K$ 在 $[0, \Delta t_{\text{outer}}]$ 变化快度, 梯形 approximation 可能 overestimate 约 15% — **match 观察到的 differential**.

### 2.3 结论

**正确 bound**: $\|F_H\|_{\text{op}} \leq \alpha + \beta/\lambda$ (连续 limit), 实测 $\approx 0.95$ 与此 consistent.

**原报告的错误**: 括号内 "$\hat F_H(\omega=0) = \alpha + \beta$" 错, 应是 "$\alpha + \beta/\lambda$". conclusion 正确。

**修正需求**: Prop 1.2 证明中括号解释 **需要改**. 定性结论 ("$\|F_H\| \geq c > 0$, $L$ 贡献 $\to 0$, 必败") **不受影响** — 因为 $\alpha + \beta/\lambda > 0$ 对任何 $(\alpha, \beta, \lambda) > 0$ 都成立。

**严重性**: 低 (presentation error, 数字 1.1 vs 0.15 区别, 但定性结论一致). 需要 Edit 修正。

**结果**: ⚠️ **内部不一致, 需要 Edit 修正文字** (下面 §6 执行).

---

## 3. Spot-Check 3: §5.1 Mexican-hat $m_\rho^2$ convention

### 3.1 任务

原报告 §5.1 展开:

$$
V = v^2 \delta a^2 + v \delta a (\delta a^2 + v^2 \delta\theta^2) + \frac14 (\delta a^2 + v^2 \delta\theta^2)^2
$$

并说 "径向 mass² $= 2 v^2 = 2$ (v=1)". 但 Linux Action 2 给出 "Mexican-hat 预期 $V'' = 8v^2 = 8$ 对 $|\psi|^2$ 或 $4$ 对 $\psi$: $m_\rho^2 \approx 4$".

到底哪个 convention 对?

### 3.2 独立核对

关键区分: arXiv v1 §3.1 vs Phase B Exp 1 verdict §1 **用不同 $V$ convention**:

| 来源 | $V$ 形式 | $V''(u)$ | 预期 $m_\rho^2$ |
|---|---|---|---|
| arXiv v1 §3.1 | $V(u) = \frac14 (u - 1)^2$ | $V''(u) = \frac12$ | 展开:quadratic 是 $v^2 \delta a^2$, $m_\rho^2 = 2v^2 = 2$ |
| Phase B Exp 1 verdict §1 | $V = (u - v^2)^2$ (**无** $\frac14$) | $V''(u) = 2$ | 展开: quadratic 是 $4v^2 \delta a^2$, $m_\rho^2 = 8v^2 = 8$ |
| Linux Action 2 memo | "$V'' = 4$ 对 $\psi$" | — | $m_\rho^2 = 4$ (physics convention, $\mathcal L \supset \frac12 m^2 \phi^2$) |

**原报告 §5.1 用的是 arXiv v1 convention** ($\frac14$), 给 $m_\rho^2 = 2$.
**Linux 数字 binding 用的是 Phase B Exp 1 convention** (无 $\frac14$), 给 $m_\rho^2 = 4$.

两个 convention 相差 factor of 4 在 $V$ 值, factor of 2 在 $m_\rho^2$ (因为 quadratic 系数差 4 倍, mass² 差 2 倍).

### 3.3 数字比较

- 实测 $m_\rho^2 = 0.092$ (Linux Action 2)
- v1 convention 预期: 2 → 比值 22×
- Phase B Exp 1 convention 预期: 4 → 比值 44× (Linux 文件的 "44×" 数字)

**Linux 文件用 44×** (`LINUX_TO_WIN_SECTION3_NESS_RAW_20260419.md` §2.2), 所以 Phase B Exp 1 convention (无 $\frac14$) 是**实测数字 binding 的**。

### 3.4 结论

**原报告 §5.1 用的 convention** (arXiv v1 的 $\frac14$) 与**Linux empirical binding convention** (Phase B Exp 1 的无 $\frac14$) **不一致**, 导致 "$m_\rho^2 = 2$" 和 Linux "44× 差距" 表面冲突 (实际只是 convention 切换).

**修正需求**: §5.1 需要在 header 或引用点 **明确标注 convention**, 并在与 empirical 比较时**换算到一致 convention**. 这是 presentation issue, 不是数学 error.

**严重性**: 低-中 (可能误导读者, 但数学 content 正确).

**结果**: ⚠️ **convention 标注缺失, 需要 Edit 添加 note + 换算**.

---

## 4. Spot-Check 4: §5.2 3D one-loop IR finiteness

### 4.1 任务

原报告 §5.2 claim:

> "**推论 5.2.1**: 对 **3D MaoField** (我们的 $\Omega = \mathbb{T}^3$) 在 Mexican-hat 展开下 one-loop self-energy **IR finite**, $m_\theta \to 0$ 极限在 perturbation theory 下 well-defined."

并给出 计算:
> "$\Sigma_{\delta a}(0) \sim v^6 \int \frac{d^3 q}{(2\pi)^3} \frac{1}{(q^2 + m_\theta^2)^2}$
> 换变量 $q = m_\theta p$:
> $\Sigma_{\delta a}(0) \sim v^6 m_\theta \int \frac{d^3 p}{(2\pi)^3} \frac{1}{(p^2 + 1)^2} = v^6 m_\theta \cdot C$, finite."

### 4.2 独立验证 — 发现致命代数错误

换变量 $q = m_\theta p$: $d^3 q = m_\theta^3 \, d^3 p$, $(q^2 + m_\theta^2) = m_\theta^2 (p^2 + 1)$, $(q^2 + m_\theta^2)^2 = m_\theta^4 (p^2+1)^2$.

$$
\int \frac{d^3 q}{(q^2 + m_\theta^2)^2} = \int \frac{m_\theta^3 \, d^3 p}{m_\theta^4 (p^2+1)^2} = \frac{1}{m_\theta} \int \frac{d^3 p}{(p^2 + 1)^2}
$$

**原报告写的是 $\propto m_\theta$, 应该是 $\propto 1/m_\theta$**. 这是直接的代数错误 — 我在换变量时**把 scaling 写反了**.

### 4.3 精确计算

$$
\int \frac{d^3 q}{(2\pi)^3 (q^2+m^2)^2} = \frac{4\pi}{(2\pi)^3} \int_0^\infty \frac{q^2 \, dq}{(q^2 + m^2)^2}
$$

用代换 $q = m \tan\theta$, $dq = m \sec^2\theta \, d\theta$, $q^2+m^2 = m^2 \sec^2\theta$:

$$
\int_0^\infty \frac{q^2 \, dq}{(q^2+m^2)^2} = \int_0^{\pi/2} \frac{m^2 \tan^2\theta \cdot m \sec^2\theta \, d\theta}{m^4 \sec^4\theta} = \frac{1}{m} \int_0^{\pi/2} \sin^2\theta \, d\theta = \frac{\pi}{4m}
$$

所以:

$$
\boxed{ \int \frac{d^3 q}{(2\pi)^3 (q^2+m^2)^2} = \frac{4\pi}{(2\pi)^3} \cdot \frac{\pi}{4m} = \frac{1}{8 \pi m} }
$$

**作 $m \to 0$**: 该积分**线性 IR 发散**, 如 $1/m$.

### 4.4 物理内涵

这是 **3D $O(N)$ 模型在 Goldstone-massless 极限的典型 IR 发散**. 对比其他维度:

| 维度 | $\int d^D q / (q^2+m^2)^2$ 作 $m \to 0$ | 解读 |
|---|---|---|
| 2 | $\pi/m^2$ | 二次 IR 发散, Mermin-Wagner 杀 SSB |
| **3** | $1/(8\pi m)$ | **线性 IR 发散** |
| 4 | $\log(\Lambda^2/m^2) / (16\pi^2)$ | 对数 (IR + UV) |
| 5+ | UV 主导 | 无 IR 问题 |

3D 线性 IR 发散意味着: **Goldstone 模在 3D 微扰论中不能当作普通 massless 模处理**; 任何涉及 Goldstone 内线的 one-loop correction 都以 $v^6/m_\theta$ 发散速率 blow up.

### 4.5 对 MaoField 的具体后果

**Pseudo-Goldstone with $m_\theta^2 = 0.017$** (从 Phase B Exp 1 实测):

$$
\Sigma_{\delta a}(0) \sim v^6 / m_\theta \sim (1)^6 / \sqrt{0.017} \sim 7.67 \quad (\text{natural units})
$$

与 tree-level $m_\rho^2 = 4$ (Phase B Exp 1 convention) 比较: **self-energy correction 接近 2× tree-level mass**, 这是**严格非微扰 regime**.

实测 $m_\rho^2 = 0.092$ (Action 2), 与 tree $4$ 差 44×, 说明 self-energy 把 tree mass 从 4 降到 0.092, 绝对值 shift 接近 4. 这**大致与 non-perturbative shift $\sim v^6/m_\theta$** **量级上 consistent**:

- tree $m_\rho^2 = 4$
- renormalized $m_\rho^2 = 0.092$
- shift $\Delta m_\rho^2 = 4 - 0.092 \approx 3.9$
- 预测 $\sim v^6/m_\theta \sim 7.67$

同量级 (factor 2 内), 这给了一个**可计算的一致性 check**. 量级 match 支持 "NESS 下 Goldstone IR 非微扰 shift" 的物理 picture, **但不 quantitatively close**, 因为:
- $v^6/m_\theta$ 是 leading IR-enhanced 1-loop, 还有高阶和 counter-term
- $v$ 本身在 NESS 下 not = 1 (实测 $\langle\rho\rangle = 1.19$), 所以 $v^6$ 应用 effective $v_{\text{eff}}^6 \approx 1.19^6 \approx 2.84$, 给 $\sim 21.8$, 反而**超** tree shift

实际 resummation 需要 Hartree / 1/N, 直接 tree + 1-loop 定量不准.

### 4.6 结论

**原报告 §5.2 的推论 5.2.1 "IR finite in 3D" 是 substantive 数学错误**。

**正确 statement** (替换原 §5.2 段):

> **Proposition 5.2'** [3D one-loop IR behavior, 修正版]: 对 MaoField 3D Mexican-hat 展开, one-loop self-energy $\Sigma_{\delta a}(0) \sim v^6/m_\theta$ **线性 IR 发散**作 $m_\theta \to 0$. 对 Phase B Exp 1 实测 pseudo-Goldstone $m_\theta^2 = 0.017$ (即 $m_\theta \approx 0.13$), 该 correction 给 $\sim v_{\text{eff}}^6/m_\theta \sim O(10)$ in natural units — **大于 tree-level mass $m_\rho^2 = 4$**.
>
> **推论 5.2.1'**: Phase B Exp 1 regime **必需非微扰工具** (Hartree 自洽, 1/N 展开, 或 MSR RG) 处理 Goldstone sector. 普通 tree + one-loop 微扰论 formally breakdown。这加强了 M4 候选走 **非微扰 variational (MSR effective action)** 路径的**必要性** — 不只是 "可选", 是 "otherwise breakdown".

### 4.7 修正需求 + 严重性

**需要**:
1. 重写 §5.2 整段, 把 "IR finite" 改为 "IR divergent, 线性 scale $1/m_\theta$"
2. 更新推论 5.2.1: 非微扰工具不是 "可选加 sophistication", 是 "微扰否则 breakdown"
3. 给出 量级 check: $v^6/m_\theta \sim 10$ vs tree $m_\rho^2 = 4$, **非微扰 shift 量级与实测 $\Delta m_\rho^2 \approx 4$ consistent**
4. 对 Linux 数字层: 给具体 Hartree 自洽方程 (§5.3 已 mentioned) 作一致性 check — 这可以 quantitatively verify

**严重性**: **中-高**. 这是真正的数学错误, 但**定性方向的影响是正向的** (加强非微扰必要性, 加强 M4 walks MSR 路径的 sufficiency). 不影响 Prop 1.1/1.2/1.3, 不影响 Prop 4.2, 不影响 Conjecture 4.1. 只影响 §5 的技术细节 + §5.3 Hartree 自洽的 motivation 强度。

**结果**: ❌ **substantive 数学错误, 需要 Edit 重写 §5.2 整段** (下面 §6 执行).

---

## 5. Spot-Check 5: §6.1 sub-critical 55× 稀释数字

### 5.1 任务

验证: "sub-critical ⇒ $(\alpha, \beta) \leq (0.002, 0.001)$, 即 55× 稀释".

### 5.2 独立计算

要求 $\|F_H\|_{\text{op}} < m_\theta^2$. 

**使用 Spot-Check 2 修正后的**: $\|F_H\|_{\text{op}} = \alpha + \beta/\lambda$ (连续 limit), 或 Linux 实测 0.95 (有限 $N_\text{hist}$).

用 Linux 实测 binding: $\|F_H\|_{\text{op}} / m_\theta^2 = 0.95 / 0.017 \approx 55.9$

要降到 sub-critical, $(\alpha, \beta) \to (\alpha/55.9, \beta/55.9) = (0.001789, 0.000894)$.

约等于 $(0.002, 0.001)$, **55× 比例**.

### 5.3 结论

**数字 consistent**. Linux 实测值为 binding, 换算精确. 原报告 §6.1 的 sub-critical prediction setup 数字上正确.

**细节改进建议**: 可以在 Prop 6.1 中明确**用实测 binding 0.95 换算, 不是 Prop 1.2 理论 1.1**; 这样读者不会 confuse.

**严重性**: 无 error, 可改进表达.

**结果**: ✓ **通过**, 可选改进.

---

## 6. 执行修正 (Edit 原报告)

接下来对原报告 `DESKTOP_MATH_DEEP_ANALYSIS_20260419.md` 执行 3 处修正:

- **修正 A** (Prop 1.2 括号): $\alpha + \beta$ → $\alpha + \beta/\lambda$
- **修正 B** (§5.1 convention 标注): 加 note 明确 $\frac14$ convention 与 Phase B Exp 1 convention 区别
- **修正 C** (§5.2 重写): "IR finite" → "IR divergent $\sim 1/m_\theta$", 加量级 check 与 non-perturbative 必要性

(执行见 next step)

---

## 7. Meta-reflection: 为什么数学教授角色也会犯这种错

§5.2 的 IR scaling 代换错误是个典型的 "快速估算时符号 flip". 换变量 $q = m p$ 时 $d^3q = m^3 d^3 p$, 被分母的 $m^4$ 除 给 $1/m$. 我当时写的 "$m_\theta \cdot \int \ldots$" 是混了 numerator 和 denominator 的 scaling.

这说明即使作为"严谨数学教授", 自己 spot-check 自己的文档 **仍有必要, 不是形式主义**. Popperian 精神要求 errors 暴露后立即承认 + 修正, 不 cushion.

对 Linux / Win / 一凡 的借鉴: 每个 deliverable 的**自 spot-check 不能代替**独立审查 — 我发现了自己的 1 个真错 + 2 个 presentation 问题, 但可能还有我看不到的盲点, 等 Linux scp 文件回去**独立 verify** 附录 D 的数字 (特别是 Prop 1.2 的 $\alpha + \beta/\lambda = 1.1$ vs 实测 0.95 的 15% 差距的解释 — 我给了 "有限 $N_\text{hist}$ + 离散化" 的 hand-wave, Linux 可以真算 discrete Fourier 验证).

---

## 8. 给一凡的 bottom line

1. **原报告的 3 条主要数学结果 (Prop 1.1, 1.2, 4.2) 不受 spot-check 影响, 仍成立**
2. **Conjecture 4.1 (M4 候选) 不受影响, 仍成立**
3. **Prop 6.1 (sub-critical prediction) 数字自洽, 10-分钟实验仍可跑**
4. **§5.2 Goldstone IR 段 有实质数学错误, 需要重写** (IR divergent 不是 finite)
5. **修正后**: §5 加强了 **M4 的非微扰必要性 argument** — 改错反而让 case 更强

**对 Linux 的建议**: 等文件到, 独立 verify 附录 D 的 4 条 (我自己 spot-check 已做, 但 Linux 独立审仍需要 — 尤其 Prop 1.2 的 $\alpha + \beta/\lambda = 1.1$ 实测 0.95 差 15% 的具体 discrete-Fourier 来源).

**对 Win 的**: 这个 spot-check 不碰 narrative / 哲学 framing, 只做数学 verify. Win 可以在 04-20 会议用修正后的版本作 binding.

**对合题的**: spot-check 后原报告核心 5 条 claim 仍成立, **推进结论 (4 候选 → collapse 到 2, M4 candidate concrete, Path B 10-min 可决策) 不受影响**. α/β/γ 合题决策仍归 04-20 + Win + 一凡.

---

*— 桌面 Claude, 2026-04-19 傍晚, 同 session self spot-check. 发现 1 真错 (§5.2 IR) + 2 presentation (Prop 1.2 括号, §5.1 convention) + 2 通过 (Prop 1.1, §6.1). 修正执行见原报告 Edit. Linux 独立审仍需要, 这不是可替代的.*
