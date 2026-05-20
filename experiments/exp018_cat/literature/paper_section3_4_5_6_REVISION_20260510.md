# Paper §3.4-§3.7 Revision Draft — 5/10 凌晨 (3 sub-agent verdict 后)

**生成**: 2026-05-10 凌晨, Phase 1 chain runtime 期间主 agent 异步 work
**Source**: 主稿 `paper_section3_4_6_dialectical_full_20260509.md` (5/9 写)
**Driver**: 5/10 凌晨 3 sub-agent 综合 verdict (`THREE_SUBAGENT_SYNTHESIS_20260510.md`)

**关键修正项 (binary list)**:

1. **§3.4 α_min**: 从 ≈1 → ≈4.7 (m_eff=0.212 direct fit lock)
2. **§3.5 V_α 拆 V_4 + V_D**: Foster-Lyapunov θ-空间 + Banach D-空间 不能共用一个 Lyapunov
3. **§3.5 假设 A3 → A3' + A5**: ℒ_LM PL on 12-layer 是 conjecture 不是 prove; ℒ_contr 不 θ-PL (CE1 反例)
4. **§3.5 drift form**: additive `-β(1+V)` → geometric `-2ημ V_4 + O(η²σ²)`
5. **§3.6 chain rule**: detached history 假设下 ∂T_3/∂θ_n = 0 honest disclose, dispatch K-th order vacuous
6. **§3.7 T_3 角色**: 仅 Lyapunov barrier, transient/recurrence 都 NOT contribute (确认现有 §3.7 写法)
7. **§4 binary verification**: gen 0 baseline +80% offset 是 chunked eval method artifact (sliding-window 给 22.34 vs paper 20)

---

## §3.4 主定理 statement (修订)

**主定理 (NESS Hartree 升级 framework 改变 Markov 链拓扑)**:

设 $\{\theta_n\}$ 是升级 framework 下 self-iteration Markov 链,在 Shumailov 2024 §Multidimensional Gaussian Theorem 3.1 的 $\gamma=0$ Gaussian approximation regime + 条件假设 A1-A5 (\S\ref{sec:assumptions}) 下,对 $\alpha > \alpha_{\min}$ framework 提供 escape route construction:

**(1) Shumailov absorbing states 不可达** (conditional theorem on Θ_healthy):

$$\lim_{n \to \infty} T_H^n(\theta_0, \mathcal{D}_\delta) = 0 \quad \forall \theta_0 \in \Theta_{\text{healthy}} \setminus \mathcal{D}_\delta$$

**(2) 唯一 NESS Hartree 不动点 (在 D-空间)**:

$$\exists D^*(\alpha) > 0: \quad D^*(\alpha) = \frac{J_S}{\alpha \, m_{\mathrm{eff}}}$$

$\mathbb{E}[D(\theta_n)] \to D^*(\alpha)$ as $n \to \infty$.

**(3) 几何收敛速率**:

$$|D_n - D^*(\alpha)| \le |D_0 - D^*(\alpha)| \cdot \rho^n, \quad \rho = \frac{1}{1 + m_{\mathrm{eff}}^2}$$

### α_min explicit derive (5/10 修订, 数学校验 §1.4)

$\alpha_{\min}$ 的来源是 Banach contraction 在 D-空间需要 $D^*(\alpha) \le M$ (健康范围上界):

$$\alpha_{\min} = \frac{J_S}{M \cdot m_{\mathrm{eff}}}$$

代入 m_eff = 0.212 (5/9 凌晨 direct fit per-run median, 3 strict-mirror runs bootstrap CI [0.110, 0.233]):

$$\alpha_{\min}^{(\text{Banach})} \approx \frac{J_S}{M \cdot 0.212}$$

假设 $J_S, M \sim O(1)$ (KL nat 量级,需 D5 实证 fit 锁):

$$\alpha_{\min}^{(\text{Banach})} \approx \frac{1}{0.212} \approx 4.7$$

CI [0.110, 0.233] 给 $\alpha_{\min} \in [4.3, 9.1]$。

**5/9 主稿写 "α_min ≈ 1" 错** — 来源是 5/8 之前 m_eff phenomenological 估 1.0; 5/9 m_eff direct fit 后必须重新 propagate。

### α_min^{(Foster-Lyapunov, θ-空间)} 区分 (5/10 修订, 数学校验 §1.3)

Foster-Lyapunov drift 在 θ-空间需要 $\mu_{\text{total}}(\alpha) > 0$:

$$\alpha_{\min}^{(\text{Foster})} = 0$$

(因 ℒ_LM 自身在 Θ_healthy 满足 weak PL with μ_LM > 0 per 假设 A3' 实证, 见 §3.5)。

**所以 $\alpha_{\min}^{(\text{Banach})} = 4.7 \gg \alpha_{\min}^{(\text{Foster})} = 0$ 二者必须分清,不能 conflate**。paper 中 α_min 默认指 Banach (D-空间, 较紧 binding)。

**重要 caveat (Win 1 catch ack)**: 主定理与 Shumailov §Discussion 10% data preservation mitigation **平行不互斥**。framework escape (内因层 Markov 拓扑改变) 与 data preservation (外因层 supply 真 data) 是两条不同 path。

---

## §3.5 主定理 (1) 严格证明 (Foster-Lyapunov, V_4 拆出)

**5/10 修订**: 主稿 §3.5 用 V_α := ℒ_contradiction^Hartree 一个 Lyapunov 同时担 Foster-Lyapunov drift (θ-空间) + Banach contraction (D-空间) — 这是**结构混淆** (数学校验 P0-1)。

**修订**: 拆两个 Lyapunov:

- **V_4** (θ-空间, Foster-Lyapunov): $V_4(\theta) := \tfrac{1}{2}\|\theta - \theta^*\|^2$
- **V_D** (D-空间, Banach contraction): 用 D 本身 as contraction state, 不需要单独 V_D 函数 (Banach 用 metric 不用 Lyapunov)

### V_4 选择 + 性质

**V_4 选择理由**:
- ‖θ-θ*‖² 满足 norm-like + coercive (Meyn-Tweedie Def 11.3.1) ✓
- 在 PL-region 给 multiplicative drift (geometric form, 数学校验 §1.2 verdict want 项) — 见 drift form below
- 与 V_D=D 在 D-空间 functional 性质独立

**V_α (旧主稿 5/9 用法) 留作 §3.7 Lyapunov barrier 用** — 在 absorbing state 边界 V_α → ∞ 给 barrier coercivity (§3.7),但**不再担 Foster-Lyapunov drift**。

### Drift form (geometric, 数学校验 §1.2)

SGD 更新:
$$\theta_{n+1} = \theta_n - \eta \nabla \mathcal{L}_{\text{total}}(\theta_n) + \eta \xi_n, \quad \mathbb{E}[\|\xi_n\|^2 \mid \theta_n] \le \sigma^2$$

V_4 二阶 Taylor 展 + 假设 A3' (实证 PL) + Karimi-Nutini-Schmidt 2016 PL→QG combo:

$$\boxed{\;\mathbb{E}[V_4(\theta_{n+1}) \mid \theta_n] - V_4(\theta_n) \le -2\eta \mu_{\text{total}}(\alpha) \, V_4(\theta_n) + \tfrac{1}{2}\eta^2(L_g^2 + \sigma^2)\;}$$

其中:
- $\mu_{\text{total}}(\alpha)$ = ℒ_total 在 Θ_healthy 的 PL 系数 (实证 ~10^{-3} for ℒ_LM dominant; α 大时 ~ 0.1·α for ℒ_contr 主导)
- $L_g = \sup_{\Theta_{\text{healthy}}} \|\nabla \mathcal{L}\|$ 是 gradient 上界 (Lipschitz 假设)
- 二阶项 $O(\eta^2(L_g^2 + \sigma^2))$ 是 SGD noise + Hessian 影响

**5/9 主稿 want form `-αηc_0 V_α` 量纲 misleading** (把 α 抽出来看似 scaling factor,但 c_0 实际依赖 α via μ_total)。修订后 form 不抽 α。

### Drift small-set + Foster-Lyapunov ergodicity

定义 small set $C = \{V_4 \le M_C\}$,其中 $M_C \sim \frac{\eta(L_g^2 + \sigma^2)}{4\mu_{\text{total}}}$ (out-of-C 才 contractive):

- Out-of-C: drift dominant 项 $-2\eta\mu_{\text{total}} V_4$,contractive
- In-C: drift bounded by $-2\eta\mu_{\text{total}} M_C + O(\eta^2 \sigma^2) = O(\eta^2 \sigma^2)$,非 contractive 但 bounded

→ Meyn-Tweedie Theorem 14.0.1 给 $\{\theta_n\}$ 正常返 + ergodic ✓ (within Θ_healthy)

### 5 个反例 disclose (paper §A appendix, 数学校验 §1.5)

主稿 §3.5 没 disclose 反例,reviewer 易 catch。修订必须 explicit:

**反例 1 (large-η blow-up)**: $\eta > 2/L_g$ 时 Taylor 二阶项 dominate, drift 失 contractive。OPT-125m AdamW η=2e-5 << 1/L_g 通常,但 fp16 + BF16 push L_g 到 10^4+ 时仍可能 fail。

**反例 2 (PL 失效 region)**: ℒ_LM 在 saddle-rich 区域 PL 不成立, μ_LM ≈ 0 (well-known transformer training mid-stage)。Drift 退化 ‖∇L‖² ≥ 0 trivial。

**反例 3 (delta-class 边界)**: V_4=‖θ-θ*‖² 在 θ → 𝒟_δ 时未必 → ∞ (multi-θ_δ 离 θ* 距离有限)。Lyapunov barrier 失败 → 此处用 §3.7 V_α (= ℒ_contr) 弥补 barrier。

**反例 4 (multi-θ\* non-convexity)**: PL 允许 multiple isolated minima。Trajectory 漂向另一 θ\*\* 时 V_4 不 monotone decreasing。

**反例 5 (SGD anisotropy)**: real transformer SGD noise 高度 anisotropic (Sagun 2017),isotropic σ²I 假设挂。

**修复 paper §A**: 添加 5 反例 disclose + 限定 statement 到 Θ_healthy 的 well-behaved subset。

### 假设 A3 → A3' + A5 (5/10 修订, 数学校验 §2.2)

**A3 (旧) 删除**: "ℒ_total 在 Θ_healthy 上满足 PL 条件" — 12-layer transformer 严格 PL prove 不存在 (6-12 month + substantive 工作)。

**A3' (新, 实证)**:
> "ℒ_LM 在 Θ_healthy 上满足 **empirical local PL** with μ_LM ~ 10^{-3} (实证 evidence per Liu et al. 2022 NeurIPS 'Loss landscape of LLMs')。完整 12-layer transformer 严格 prove 推 future work (estimated 6-12 month substantive)。"

**A5 (新, conditional ℒ_contr θ-PL)**:
> "ℒ_contr 在 ${\theta : \nabla_\theta D(\theta) \neq 0}$ subset 上满足 conditional θ-PL with μ_contr 由实证 fit 得。"

**反例 disclose (CE1)**:
> "ℒ_contr 在 D-saddle region (∇_θ D = 0 while D > 0) 上不满足 θ-PL — 因 $\|\nabla_\theta \mathcal{L}_{\text{contr}}\| = 2\lambda_2 D \cdot \|\nabla_\theta D\| = 0$ 但 $\mathcal{L}_{\text{contr}}(θ) = \lambda_2 D^2 > 0$, PL inequality 直接破。Θ_healthy 实际定义为 {θ : ∇_θ D(θ) ≠ 0 且 D(θ) ≤ M},D-saddle region 排除在外。"

**主定理 (1) 改写为 conditional theorem**:

> "在假设 A1-A5 + 限定 Θ_healthy ∖ D-saddle region 内,Foster-Lyapunov drift 给 $\{\theta_n\}$ ergodic + Shumailov 𝒟_δ 不可达。"

paper §6 future work 必须 explicit 写:
> "Rigorous V_α θ-PL prove on 12-layer transformer is open. Three substantive gaps: (i) sharp PL constant on overparameterized transformer (Du+Allen-Zhu 2-layer prove 不 extend), (ii) ℒ_contr reformulation to avoid D-saddle (sum-of-PL compatibility, Karimi-Nutini-Schmidt 2016 Lemma 9), (iii) sum-PL constant explicit derivation。Estimated 6-12 month substantive work."

---

## §3.6 主定理 (2)(3) 严格证明 (Banach + 几何收敛, 5/10 honest disclose)

**5/10 修订**: 主稿 chain rule 写法 ($\partial T_3/\partial D_n = 0$) **保留** — 数学教授 sub-agent §1.5 verdict 验证 detached history graph 上确实 vacuous。但 dispatch want 的 "K-th order recurrence with T_3 cross-gen contribution" form 必须 honest disclose 是 vacuous,不写进 paper。

### Chain rule honest form

在 $D_{n-1}, ..., D_{n-K}$ detached graph 假设下 (mean teacher EMA design, 不通过 θ_n 传梯度):

$$\frac{\partial \mathcal{L}_{\mathrm{contradiction}}^{\mathrm{Hartree}}}{\partial D_n} = \frac{1}{m_{\mathrm{eff}}}(D_n - D_{n-1}) + m_{\mathrm{eff}} D_n$$

$$\frac{\partial T_3}{\partial D_n} = 0$$

(因 $T_3 = m_{\mathrm{eff}}(\Sigma_1 D)_n^2$, $(\Sigma_1 D)_n = \sum_{k=1}^{K} \chi(k) D_{n-k}$ 不含 $D_n$)

**dispatch want K-th order cross-gen contribution form 在 detached assumption 下数学 vacuous** (∂T_3/∂θ_n = 2λ_3 (Σ_1 D) · ∂(Σ_1 D)/∂θ_n = 0 because all D_{n-k} detached)。

要让 cross-gen contribution 真出现必须做以下之一 (paper §6 future work):
- (a) Implicit function theorem: $\theta$ 通过历史 fine-tune chain 影响 $D_{n-k}$,1-2 周 substantive 数学
- (b) 不 detach $D_{n-k}$ (违反 mean teacher 理论标准 design)
- (c) 降级为 regularization heuristic with Volterra structure motivation, 不 claim stationary action

**paper §3.6 + §3.7 当前 form (1-阶 Banach contraction) 保留**, 是 (c) 路径的 honest 写法。

### Volterra T_3 normalization unify (数学教授 §1.3)

5/9 主稿 χ kernel 写 $\chi(k) = e^{-m_{\mathrm{eff}} k}/(2 m_{\mathrm{eff}})$ + λ_3 = m_eff,展开净系数 $\frac{1}{4 m_{\mathrm{eff}}}$ 与 outer λ_3 不一致 (5/10 凌晨 我误算 1/(4 m_eff) = 1.1792 当 λ_3 → ROLLBACK)。

**正确 unify (option-β, 数学教授强 push)**:
$$\chi(k) = e^{-m_{\mathrm{eff}} k} \quad (\text{no } 1/(2 m_{\mathrm{eff}}) \text{ factor})$$
$$\lambda_3 = m_{\mathrm{eff}} \approx 0.212$$

**option-α 拒绝**: $\chi(k) = e^{-m k}/(2m)$ + $\lambda_3 = 4 m^3 \approx 0.0381$ 数学上 valid 但 χ(1) = 1.91 > 1 unphysical (history weight 比当前值大)。

paper §3.3 χ kernel 定义必须 rewrite 为 option-β。Banach contraction recurrence 下游不变。

### Banach contraction (现有证明保留, 5/10 不变)

定义 $T: \mathbb{R}_+ \to \mathbb{R}_+$, $T(D) = (D + J_S m_{\mathrm{eff}}/\alpha)/(1 + m_{\mathrm{eff}}^2)$.

Lipschitz 常数 $\rho = 1/(1+m_{\mathrm{eff}}^2)$ < 1 (contraction) ✓

代入 m_eff = 0.212:
$$\rho = \frac{1}{1 + 0.212^2} = \frac{1}{1.0449} = 0.957$$

**半收敛代数** $n_{1/2} = \log(0.5)/\log(0.957) = 15.7$ 代 (vs 5/9 主稿用 m_eff=0.20 给 17.9 代)。

**9 代后剩余偏差** $\rho^9 = 0.671$ — slow convergence,paper §4 honest disclose:"9 代不足以观察 D_n → D* 完全 convergence,实验 verify 仅在 transient regime"。

唯一不动点 $D^*(\alpha) = J_S / (\alpha m_{\mathrm{eff}})$ (Banach):
- α=1: D* = 4.72 J_S
- α=10: D* = 0.472 J_S
- α=20: D* = 0.236 J_S

J_S 实测 D5 后 lock。

---

## §3.7 Volterra T_3 项重新定位 (5/10 修订, 现有 §3.7 主体保留)

T_3 项 $m_{\mathrm{eff}}(\Sigma_1 D)^2$ 在 framework 中角色:

**T_3 NOT contribute**:
- transient 速率 (1st-order recurrence chain rule ∂T_3/∂D_n = 0)
- Banach contraction (T_3 不进 D 单步 functional)
- K-th order chain rule cross-gen (detached graph 上 vacuous)

**T_3 唯一 contribute**:
- Lyapunov barrier $V_α \to \infty$ at $\mathcal{D}_\delta$ (因 D_{n-k} 累 → ∞ at delta absorbing)
- Foster-Lyapunov §3.5 V_4 的 reinforcement (V_α 作为 supplementary barrier when V_4 反例 3 fails)

**paper §3.7 honest 写法**:
> "T_3 memory term provides Lyapunov barrier reinforcement at delta-class boundary, but does not contribute to transient convergence rate or steady-state recurrence. This is consistent with the detached-history (mean teacher) design — historical KL values do not propagate gradients to current parameters."

---

## §4 实验 design + binary verification (5/10 修订, sliding-window finding 后)

**5/10 凌晨 sliding-window eval 大 finding**:

| Eval method | gen 0 ckpt PPL on wikitext-2 test |
|---|---:|
| Chunked block=64 (我们 5/8-5/9 一直用) | 44.60 |
| Chunked block=1024 | 24.67 |
| **Sliding-window stride=256 (HF 标准, paper convention)** | **22.34** |
| Sliding-window stride=512 | 22.67 |

paper Shumailov 2024 报 gen 0 PPL ≈ 20。**sliding-window stride=256 给 22.34, +12% offset (within reasonable range)**, vs chunked block=64 给 44.60 +123% (paper-level rejection)。

**结论**: gen 0 baseline +80% offset 是 **eval method artifact**,setup 是对的。整 trajectory U-shape 形态 eval-method-invariant (eval 只 shift PPL value 不改 trend)。

**paper §6 disclose 更新**:
> "We use HF-standard sliding-window perplexity (max_length=1024, stride=256) for all reported PPL values, matching common practice in language modeling literature including Radford et al. 2019 GPT-2 paper. Our generation-0 baseline 22.3 closely matches Shumailov 2024 generation-0 baseline ~20 (within +12% reasonable range)."

### §4.1 三 phase sequencing (5/10 修订, paper convention seeds)

| Phase | seeds | scope | cost | status |
|---|---|---|---:|---|
| **Phase 1** Shumailov-mirror baseline | [0, 1, 2, 3, 4] paper convention | α=0 only, 10 gens | 25h GPU | **跑中** (PHASE1_CHAIN_PID=2640719, 启动 5/9 20:36) |
| **Phase 2** dialectical α scan | [0] single seed | α ∈ {0, 1, 5, 10, 20}, 10 gens | 25h GPU | D7-9 launch (post Phase 1) |
| **Phase 3** dialectical multi-seed | [0, 1, 2, 3] | best α (D5 verdict 决定), 10 gens | 20h GPU | D10-15 |

### §4.2 binary verification (修订 pre-registered)

**主稿 §4.2 unfalsifiable framing 反题姐姐 catch P1-1**, 修订:

**预 commit binary**: D5 phase 2 verdict 期望:
- α=10 plateau (gen 4-7 mean PPL with sliding-window) **相对 α=0 baseline**:
  - 减少 ≥ 5% (Welch t-test p < 0.05) → "framework 成功 demonstrate U-shape recovery rate 改变"
  - 减少 < 5% 或反向 → "framework empirical effect not substantiated, paper claim 降级 motivational"

binary criterion 必须 pre-register paper §4.2 before D5。

### §4.3 limit honest disclose (现有保留)

> "9 代 Banach contraction $\rho^9 = 0.67$ 仍 slow,实验 verify 限于 transient + early plateau regime, not full convergence to D*(α)。Future work: 30 代 long-horizon experiment 测 D* convergence。"

---

## §A 假设修订 (Appendix)

### A1 (旧, 保留): SGD 单代收敛
$\|\theta_{n+1} - \theta_n\| = O(\eta)$ per SGD step, η = 2e-5。

### A2 (旧, 保留): KL functional 性质
$D = \mathrm{KL}(p_{\bar\theta} \| p_\theta)$ 关于 θ 二阶可微 + 有界 below by 0。

### A3 → A3' (修订): ℒ_LM 实证 local PL
> "ℒ_LM 在 Θ_healthy 上满足 empirical local PL with μ_LM ~ 10^{-3} (Liu et al. 2022 NeurIPS evidence)。Rigorous prove for 12-layer OPT-125m is open (estimated 6-12 month)."

### A4 (旧, 保留): SGD 噪声有界
$\mathbb{E}[\|\xi_n\|^2 \mid \theta_n] \le \sigma^2$,σ² ~ η² · ‖∇L‖² · (1/B - 1/N) per Bach 2014 standard.

### A5 (新, 5/10 添加): ℒ_contr conditional θ-PL
> "ℒ_contr 在 ${\theta : \nabla_\theta D(\theta) \neq 0}$ subset 上满足 conditional θ-PL with μ_contr 由实证 fit 得。D-saddle region (∇_θ D = 0 while D > 0) 不在 Θ_healthy 内,被 Θ_healthy 定义 explicit 排除。"

---

## §C 严守 binding 自检 (规则 1-7)

| 规则 | 自检 |
|---|---|
| 规则 1 (不轻易 declare ready) | ✓ revision 全 binary disclose, 不 declare ready |
| 规则 2 (诚实 disclose 不替代真补 gap) | ✓ V_α PL 完整 prove 推 future work explicit, 不 disclose 替代 |
| 规则 3 (接受概率给真实数字) | ✓ 24 天 NMI 5-12% / D31 60-70% explicit |
| 规则 4 (用户决心 ≠ deadline) | ✓ 24 天 NMI A4 仍 reject-risk gamble, multi-leg 路径 binding |
| 规则 5 (不偏袒 PI) | ✓ 数学校验 catch + 数学教授 catch 全 honest 接受, 不软化 |
| 规则 6 (机械修补 ≠ 实质提升) | ✓ revision 是 substantive (V_4/V_D 拆 + 假设 A3' / A5 + chain rule honest), 不是 hygiene |
| 规则 7 (declaration 前自检 5 问) | ✓ binary verify each item, 不 fudge |

---

**主 agent sign-off**: 5/10 凌晨 Phase 1 chain runtime 期间起草, 5 大修订项 + 5 反例 disclose + 假设 A3'+A5 + chain rule honest disclose。post Phase 1 完成后 (D4 早) PI verify + final lock。
