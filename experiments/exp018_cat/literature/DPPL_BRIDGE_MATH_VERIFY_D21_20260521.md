# D-PPL 桥 verify 数学 verify brief — D21 (2026-05-21)

**身份**: D21 D-PPL 桥 verify 数学 verify sub-agent (D-1 纪律 4 第二认识通道)
**输入**: paper v8 final §3.6.2 / §5.2 / §6.1 / §6.2 + 反题 v8 final P0★-F + D-PPL bridge brief D21 §2.4 / §4.2 / §4.3 / §6.1
**目标**: 严格 derive 四项数学 detail 给 一凡 + 反题层 后续 audit, 直接 read 不必 重 derive
**纪律严守**: D-1 binding L2 form-borrow baseline; 路径 B+C 不 binary close P0★-F; 任何未 substantive derive 标 [?]; 不 inflate / 不 estimate paper inclusion

---

## §1 Pearson correlation $r$ 数学定义 + bootstrap CI 95% 公式 + N=40 statistical power

### §1.1 sample Pearson 系数定义

对两 配对 series $(x_i, y_i)_{i=1..N}$, sample Pearson:

$$r := \frac{\sum_{i=1}^{N} (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{N} (x_i - \bar{x})^2 \cdot \sum_{i=1}^{N} (y_i - \bar{y})^2}}$$

with $\bar{x} = \frac{1}{N}\sum x_i$, $\bar{y} = \frac{1}{N}\sum y_i$。$r \in [-1, 1]$, 量纲 dimensionless。

D-PPL 桥 verify 之 binding:
- $x_i := \tilde{D}_i^{\rm code, proxy}$ (路径 B) 或 $\hat{D}_i^{\rm code, gen0-anchor}$ (路径 C), 单位 nat/token
- $y_i := D_i^{\rm paper} = \log({\rm PPL}_i / {\rm PPL}_0)$, 单位 nat/token (dimensionless ratio of perplexities)
- $i$ index = (seed, generation) pair, $N = 4 \times 10 = 40$ 当 路径 B 或 C 单独 (含 gen 0 时 N=40, 排 gen 0 时 N=36); 当 路径 B + C concat 时 N=80 (但 非 i.i.d., 见 §1.4)

### §1.2 percentile bootstrap CI 95% 公式 (N_bootstrap=10000)

bootstrap resampling 流程 (paired resample with replacement, seed 20260521):

```
input: paired data {(x_i, y_i)}_{i=1..N}
N_bootstrap := 10000
for b in 1..N_bootstrap:
    sample with replacement N indices {j_1, ..., j_N} from {1, ..., N}
    compute r_b = Pearson({(x_{j_k}, y_{j_k})}_{k=1..N})
sort {r_b}_{b=1..N_bootstrap}
CI_lo := r_b 之 2.5% percentile (即 sorted r 之 第 250 个)
CI_hi := r_b 之 97.5% percentile (即 sorted r 之 第 9750 个)
return [CI_lo, CI_hi]
```

注 caveat:
- bootstrap 是 paired resample, 不 break (x_i, y_i) 之 pairing
- bootstrap 不 invoke t-distribution df=N-2 之 t-tail inflation (类 paper §3.6.3 footnote 之 bootstrap vs Student-t 区分)
- bootstrap CI 与 Fisher z-transform CI 是 不同 method: percentile bootstrap 直接 read empirical quantile; Fisher z-transform 用 asymptotic $\mathrm{arctanh}(r) \sim \mathcal{N}(\mathrm{arctanh}(\rho), 1/(N-3))$ 之 closed-form

### §1.3 Fisher z-transform 之 closed-form CI (reference, 用于 §1.4 power derive)

Fisher z-transform: $z = \mathrm{arctanh}(r) = \frac{1}{2}\log\frac{1+r}{1-r}$ ; $z \sim \mathcal{N}(\zeta, \sigma_z^2)$ asymptotically with $\sigma_z = 1/\sqrt{N-3}$, $\zeta = \mathrm{arctanh}(\rho_{\rm true})$。

95% CI: $r \in [\tanh(z - 1.96 \sigma_z),\ \tanh(z + 1.96 \sigma_z)]$。

### §1.4 N=40 statistical power binary derive

power for testing $H_0: \rho = 0$ vs $H_1: \rho = \rho_{\rm true}$, two-sided $\alpha = 0.05$:

$$\mathrm{power}(\rho_{\rm true}, N) = \Phi\left(\frac{\mathrm{arctanh}(\rho_{\rm true})}{\sigma_z} - z_{\rm crit}\right) + \Phi\left(-\frac{\mathrm{arctanh}(\rho_{\rm true})}{\sigma_z} - z_{\rm crit}\right)$$

with $\sigma_z = 1/\sqrt{N-3}$, $z_{\rm crit} = \Phi^{-1}(0.975) = 1.96$, $\Phi$ 为 standard normal CDF。

binary numerical evaluation (Python verify, manual ncdf via erf):

| $\rho_{\rm true}$ | N=36 (排 gen 0) | N=40 (含 gen 0) | N=80 (路径 B+C) |
|---|---:|---:|---:|
| 0.3 | 0.428 | 0.469 | 0.775 |
| 0.5 | 0.884 | 0.916 | 0.998 |
| 0.7 | 0.999 | 1.000 | 1.000 |
| 0.85 | 1.000 | 1.000 | 1.000 |

**95% CI half-width** (Fisher z-transform, 后 back-transform):

| sample $r$ | N=36 half-width | N=40 half-width | N=80 half-width |
|---|---:|---:|---:|
| 0.5 | 0.253 | 0.239 | 0.167 |
| 0.7 | 0.177 | 0.167 | 0.115 |
| 0.85 | 0.099 | 0.093 | 0.063 |

**binary verdict (D-1 严守 不 inflate)**:
- $\rho_{\rm true} = 0.5$ (paper §6.1 stationary equality 之 partial 假设 ballpark [?]) 之 N=40 power **0.92** — adequately powered 检测 medium correlation
- $\rho_{\rm true} = 0.3$ (marginal 区域) 之 N=40 power **仅 0.47** — underpowered, 即使 真 $\rho = 0.3$ 也有 53% 几率 fail to reject $H_0$ → 不能 distinguish "no correlation" 与 "weak correlation"
- N=80 (路径 B + C concat) **不是** true i.i.d. N=80: gen-axis within-seed correlation 严重 (per chain dynamics 之 cross-gen drift Markov 结构), effective N 可能 $< 80$; **clustered bootstrap or hierarchical Pearson** 是 alternative, 推 一凡 关卡 3 之 sub-agent analysis decision [?]
- **N=40 之 95% CI half-width 在 $r = 0.5$ 时 ≈ 0.24** — 实际 observed $r = 0.50$ 给 CI 大致 $[0.22, 0.70]$, 跨 paper §6.1 brief §6.1 之 三个 tier (r > 0.7 / 0.3 < r < 0.7 / r < 0.3) 之 边界 — **single 实验 之 r point estimate 不能 binary 区分 tier**, 需 bootstrap CI 之 endpoint 判 [?]

**caveat**:
- Pearson 是 linear correlation, 真实 $D^{\rm code}$ vs $D^{\rm paper}$ relation 可能 non-linear (paper §3.6.2 之 mean-field NESS 形式 是 logarithmic-mean approximation, 路径 B/C 之 proxy 是 linear KL distance)
- **Spearman rank correlation** 是 alternative 适合 monotone non-linear case; sub-agent 推 路径 B/C analysis stage 同时 compute Spearman + Pearson, 给一凡 关卡 3 比较 [?]
- Pearson 之 normality assumption (residual 高斯) 在 chain U-shape regime 之 transient (gen 1-2) 必然 violated, plateau 区域 (gen 5-9) 假设 partial 满足 [?]

---

## §2 路径 B (gen-(n-1) 主 model 作 EMA proxy) 之 数学 difference vs 真实 EMA

### §2.1 真实 EMA 之 per-step + per-gen 递归

paper §3.6.2 + chain config (`KLContradictionTracker.update_ema_model`):

**θ-空间 EMA (model parameters)**:
$$\bar{\theta}_t^{\rm EMA} = \beta_\theta \bar{\theta}_{t-1}^{\rm EMA} + (1 - \beta_\theta) \theta_t \quad (\text{per train step}, \beta_\theta = 0.999)$$

注: 这是 在 **每 train step** update 之 EMA on θ; 一 generation 共 $N_{\rm step \, per \, gen} = 1460$ train steps; 跨 gen 之 EMA state 通过 `KLContradictionTracker` Python in-memory state 持续 (gen end `reset_state` 不 reset EMA model per `train_one_generation.py` line 279-284 comment); 但 EMA state **不 save disk** (brief §3.3 P0 blocker)。

**$D$-空间 EMA (KL series scalar)**:
$$\bar{D}_n^{\rm EMA} = \beta_{\rm kl} \bar{D}_{n-1}^{\rm EMA} + (1 - \beta_{\rm kl}) D_{n-1} \quad (\text{per } \tau = 10 \text{ train step}, \beta_{\rm kl} = 0.9)$$

(本 §2 之 derivation 集中在 **θ-空间 EMA** 之 proxy 问题; $D$-空间 EMA 在 路径 B 之 proxy 中亦有 implicit replacement, 见 §2.4 caveat)

### §2.2 路径 B proxy form (brief §4.2)

$$\bar{\theta}_n^{\rm B, proxy} := \theta_{n-1} \quad (\text{gen-(n-1) 主 model final state})$$

即: 用 gen-(n-1) **end** 之 主 model state 替代 真实 cumulative EMA state at gen n start (与 gen n train 期间 之 EMA evolution)。

注: brief §4.2 之 binary form 实际 用 $\tilde{q}^{\rm EMA}_n := q^{\theta_{n-1}}$ (即 用 主 model state at gen-(n-1) end 之 softmax 输出 作 EMA distribution proxy)。本 §2 之 derivation 在 θ-space, 与 distribution space 同 form-borrow tier。

### §2.3 closed-form difference derivation

定义 proxy error $E_n := \bar{\theta}_n^{\rm EMA} - \theta_{n-1}$ (i.e., 真实 EMA - 路径 B proxy, at gen n start)。

**per-gen 等效化**: 一 generation 内 $N := N_{\rm step \, per \, gen} = 1460$ train steps; 在 gen n 内, $\theta$ 从 $\theta_{n-1}$ (gen n-1 end = gen n start) 渐变到 $\theta_n$ (gen n end)。

assume **within-gen θ-trajectory 之 quasi-linear interpolation** (i.e., $\theta_t$ at step $t$ inside gen n ≈ linear from $\theta_{n-1}$ to $\theta_n$; 这是 partial L2 form approximation [?])。
则 within-gen 之 EMA 更新 yield:

$$\bar{\theta}_n^{\rm EMA} = \beta_\theta^N \bar{\theta}_{n-1}^{\rm EMA} + (1 - \beta_\theta) \sum_{t=0}^{N-1} \beta_\theta^{N-1-t} \theta_t^{(n)}$$

with $\theta_t^{(n)}$ = θ at step t inside gen n。numerical anchor:
$$\beta_\theta^N = 0.999^{1460} \approx 0.2321$$
$$1 - \beta_\theta^N \approx 0.7679$$

EMA time constant $\tau_{\rm eff}^{\rm step} = 1/(1 - \beta_\theta) = 1000$ steps $\approx 0.685$ gen。即 真实 EMA 在 ~0.7 gen 内 "遗忘" 一 半 history。

若 假设 within-gen 之 $\theta_t^{(n)} \approx \theta_{n-1}$ (drift 在 gen 内 小, 这是 partial OK 在 plateau regime, but **violated 在 transient gen 1-2 spike** per paper §3.6.5):

$$\bar{\theta}_n^{\rm EMA} \approx \beta_\theta^N \bar{\theta}_{n-1}^{\rm EMA} + (1 - \beta_\theta^N) \theta_{n-1}$$

substract $\theta_{n-1}$ 两边:
$$E_n = \bar{\theta}_n^{\rm EMA} - \theta_{n-1} \approx \beta_\theta^N (\bar{\theta}_{n-1}^{\rm EMA} - \theta_{n-1})$$

decompose $\bar{\theta}_{n-1}^{\rm EMA} - \theta_{n-1} = (\bar{\theta}_{n-1}^{\rm EMA} - \theta_{n-2}) - (\theta_{n-1} - \theta_{n-2}) = E_{n-1} - \Delta\theta_{n-1}$, with $\Delta\theta_{n-1} := \theta_{n-1} - \theta_{n-2}$ (per-gen drift in θ space):

$$\boxed{\quad E_n \approx \beta_\theta^N \cdot (E_{n-1} - \Delta\theta_{n-1}) \quad}$$

with $\beta_\theta^N \approx 0.2321$ (per-gen retention factor)。

assume init $E_0 = 0$ (chain config: $\bar{\theta}_0^{\rm EMA} = \theta_0$ on first instantiate, paper §3.2.1 + `KLContradictionTracker.__init__`):
$$E_n \approx - \sum_{k=1}^{n} (\beta_\theta^N)^{n-k+1} \Delta\theta_{k-1}$$

若 假设 $\Delta\theta$ per-gen drift 在 plateau 区 大致 constant $\Delta\theta_\infty$:
$$E_n \approx - \Delta\theta_\infty \cdot \sum_{j=1}^{n} (\beta_\theta^N)^j = - \Delta\theta_\infty \cdot \frac{\beta_\theta^N (1 - (\beta_\theta^N)^n)}{1 - \beta_\theta^N}$$

at gen 5 (plateau onset, per paper §3.6.5):
$$\sum_{j=1}^{5} 0.2321^j \approx 0.302$$
即 $E_5 \approx -0.302 \cdot \Delta\theta_\infty$ (proxy underestimate true EMA by ~30% of one per-gen drift step)。

at gen → ∞ (asymptotic):
$$E_\infty \approx -\Delta\theta_\infty \cdot \frac{\beta_\theta^N}{1 - \beta_\theta^N} = -\Delta\theta_\infty \cdot \frac{0.2321}{0.7679} \approx -0.302 \cdot \Delta\theta_\infty$$

(geometric 收敛 在 ~2-3 gen 内, 因 $\beta_\theta^N = 0.232$ 之 retention 很 小)

### §2.4 binary 结论 + caveat

**binary verdict**: 路径 B 之 $D^{\rm code, B}_n$ 是 真实 $D^{\rm code}$ 之 **single-step approximation** in the limit $\beta_\theta \to 0$ (per-step EMA "完全 遗忘" history)。chain config 之 $\beta_\theta = 0.999$ 但 per-gen retention $\beta_\theta^N = 0.232$ 让 真实 EMA 在 per-gen scale 上 表现 类 "memory-light" — 即 真实 EMA 在 1-2 gen 内 大致 收敛到 主 model neighborhood。

**proxy 与 真实 之 asymptotic bias**: $E_\infty \approx -0.302 \cdot \Delta\theta_\infty$ (in θ-space)。映 到 distribution space (Fisher metric 之 linearization), KL 差 $|D^{\rm code, true} - D^{\rm code, B}| \sim \frac{1}{2} |E_\infty|_F^2 \sim 0.045 |\Delta\theta_\infty|_F^2$ (Fisher inner product 之 linearization, valid 仅 in small-deviation limit) [?]。

**L2 form-borrow tier (严守)**: 路径 B 用 gen-(n-1) 主 model state 替代 EMA 是 form-borrow, **不 substantively close** P0★-F:
- proxy 与 真实 EMA 之 bias proportional to per-gen drift $|\Delta\theta_\infty|$, 在 chain transient (gen 1-2 spike) 必然 violated (drift 不 small)
- $\beta_\theta = 0.999$ 之 per-step time constant 1000 steps ≈ 0.685 gen, gen-axis 上 表现 类 "短记忆", but **β_kl = 0.9 之 $D$-空间 EMA recursion** (per τ=10 train step, time constant $\sim 10$ τ-step = 100 train step ≈ 0.07 gen) **完全 不被** 路径 B 之 proxy form 覆盖 — 路径 B 仅 替换 q^EMA distribution, 不 触 $\bar{D}^{\rm EMA}_n$ scalar EMA on KL series
- 即使 plateau Pearson r > 0.85 (per brief §6.1 之 strong-evidence tier), 这仅给 **circumstantial evidence for $D^{\rm code, stationary}_{\rm proxy} \approx D^{\rm paper}_{\rm stationary}$**, 不 prove $D^{\rm code, true}_{\rm stationary} = D^{\rm paper}_{\rm stationary}$ — paper §6.1 之 stationary equality remains **open substantive question**

**严守 D-1 binding**: 路径 B 不 binary close P0★-F, 仅 give "lower-bound Pearson correlation" (per brief §4.2)。任何 close P0★-F 之 declaration 必 wait D60+ 路径 D rerun chain with EMA state explicit save (brief §4.4)。

---

## §3 路径 C (current vs gen-0 主 model KL) 之 数学 difference vs 真实 EMA

### §3.1 路径 C 之 binary form

$$\hat{D}_n^{\rm code, gen0-anchor} := \mathrm{KL}(q^{\theta_0} \| p^{\theta_n}) \quad \text{on val batch}$$

(brief §4.3: gen-0 base = `data/checkpoints_armb/alpha{α}/no_preserve_seed{s}/generation_0/model.safetensors`)

trivially $\hat{D}_0 = 0$ (current = base at gen 0)。

### §3.2 真实 $D^{\rm code}$ 之 form (reminder)

$$D_n^{\rm code, true} := \mathrm{KL}(q^{\bar{\theta}_n^{\rm EMA}} \| p^{\theta_n}) \quad \text{on val batch}$$

paper §3.6.2 Reading 2 之 main theorem (2) 是 在 $D^{\rm code, true}$ 空间 之 fixed-point identification:
$$D^{*, \rm code}_{\rm true}(\alpha) - D^* = -J_S / (4 \alpha N_{\rm contr})$$

### §3.3 数学 binary difference (cumulative vs instantaneous)

**reference distribution 之 critical 不同**:
- 路径 C: reference = $q^{\theta_0}$ (**fixed** gen-0 base distribution)
- 真实 $D^{\rm code}$: reference = $q^{\bar{\theta}_n^{\rm EMA}}$ (**time-varying** EMA tracking current)

**dynamics 之 scaling 差**:
- 路径 C measures **cumulative drift** of current model from gen-0 base across all n generations
- 真实 $D^{\rm code}$ measures **instantaneous drift** of current model from EMA (which adapts to recent state with 0.685-gen time constant)

**Fisher-metric linearization (small-drift limit, partial L2 approx [?])**:
若 假设 within Fisher-metric quadratic regime:
$$\hat{D}_n^{\rm C} \sim \frac{1}{2} (\theta_n - \theta_0)^T G(\theta_0) (\theta_n - \theta_0)$$
$$D_n^{\rm code, true} \sim \frac{1}{2} (\theta_n - \bar{\theta}_n^{\rm EMA})^T G(\bar{\theta}_n^{\rm EMA}) (\theta_n - \bar{\theta}_n^{\rm EMA})$$

with $G(\cdot)$ Fisher information metric at base point。

若 假设 quasi-linear drift $\theta_n - \theta_0 = \sum_{k=0}^{n-1} \Delta\theta_k$ 且 plateau regime $\Delta\theta_k \approx \Delta\theta_\infty$ constant, $G(\cdot) \approx G_\infty$ stationary:
$$\hat{D}_n^{\rm C} \sim \frac{n^2}{2} \cdot \Delta\theta_\infty^T G_\infty \Delta\theta_\infty \quad \text{(grows quadratically in n)}$$

而 真实 $D^{\rm code}$ at plateau (per §2.3 derivation):
$$D_n^{\rm code, true} \sim \frac{1}{2} \cdot (\beta_\theta^N / (1 - \beta_\theta^N))^2 \cdot \Delta\theta_\infty^T G_\infty \Delta\theta_\infty \approx 0.091 \cdot \Delta\theta_\infty^T G_\infty \Delta\theta_\infty \quad \text{(approximately stationary)}$$

**结论之 dimensional scaling**:
- $\hat{D}_n^{\rm C}$ scales as $n^2 \cdot |\Delta\theta_\infty|_F^2$ (cumulative, monotone 增)
- $D_n^{\rm code, true}$ scales as $|\Delta\theta_\infty|_F^2$ (instantaneous, plateau stationary 在 NESS 区)
- ratio $\hat{D}_n^{\rm C} / D_n^{\rm code, true} \sim n^2 / 0.091 \approx 11 n^2$ at gen n, 在 plateau region 高度 不同 magnitude

### §3.4 与 $D^{\rm paper}$ 之 alignment 之 spurious 风险

paper §6.2: $D_n^{\rm paper} = \log({\rm PPL}_n / {\rm PPL}_0) = D_{\rm KL}(q_* \| p_{\theta_n}) - D_{\rm KL}(q_* \| p_{\theta_0})$ — **also gen-0 anchored cumulative** (但 reference 是 ground-truth $q_*$ 不是 base model $q^{\theta_0}$)。

由 cross-entropy decomposition (Cover-Thomas 2006):
$$D_n^{\rm paper} = (H(q_*, p_{\theta_n}) - H(q_*)) - (H(q_*, p_{\theta_0}) - H(q_*)) = H(q_*, p_{\theta_n}) - H(q_*, p_{\theta_0})$$

而 路径 C: $\hat{D}_n^{\rm C} = H(q^{\theta_0}, p_{\theta_n}) - H(q^{\theta_0})$ — uses $q^{\theta_0}$ 替代 $q_*$ as reference。

**spurious-correlation 风险**:
$$\hat{D}_n^{\rm C} - D_n^{\rm paper} = [H(q^{\theta_0}, p_{\theta_n}) - H(q_*, p_{\theta_n})] - [H(q^{\theta_0}) - H(q_*, p_{\theta_0})]$$

若 $q^{\theta_0}$ 与 $q_*$ 之 deviation 在 gen 间 stationary (即 base model 之 quality 没改变, 因 base model frozen), 则 上式 之 第二 bracket 是 constant; 第一 bracket scales with $p_{\theta_n}$ drift。

→ **路径 C 与 $D^{\rm paper}$ 之 trajectory shape 大概率 highly correlated** (Pearson r > 0.85 [?]), 但这 仅 reflect 两者 都是 cumulative drift from gen-0, **不 prove** paper §3.6.2 主定理 (2) 之 fixed-point identification (which is about **instantaneous EMA-deviation**, 不是 cumulative gen-0-anchored)。

### §3.5 binary 结论 + caveat

**binary verdict**: 路径 C 适合 verify cumulative model drift from gen-0, **不 align** paper §3.6.2 之 instantaneous EMA-deviation form。

**L2 form-borrow tier (严守)**: 路径 C 是 path C circumstantial evidence:
- ✓ binary 数学定义清晰 ($q^{\theta_0}$ fixed, 无 time-varying EMA ambiguity)
- ✓ 与 $D^{\rm paper}$ 之 reference distribution 一致 (gen-0 anchored cumulative)
- ✗ 不是 chain training 实际之 $D_n^{\rm code}$ (chain 用 EMA teacher 不是 gen-0 base teacher); 数学严格度 L2 form-borrow (同 路径 B tier)
- ✗ **路径 C 与 $D^{\rm paper}$ 之 高 Pearson r 是 trivial 预期** — 两者 都是 gen-0 anchored cumulative drift, monotone shape 高度 一致 — high correlation 不 surprise, 也 不 substantively close P0★-F

**严守 D-1 binding**: 即使 路径 C 之 plateau Pearson r > 0.85, 这 仅 give circumstantial evidence for $\hat{D}_n^{\rm C, stationary} \sim D^{\rm paper, stationary}$, **不 prove** paper §3.6.2 main theorem 之 $D^{\rm code, true, stationary} = D^{\rm paper, stationary}$ — paper §6.1 之 stationary equality remains open substantive question。

---

## §4 Pearson r tier 之 数学含义 + binary verdict tier

per brief §6.1 + paper §6.1 之 binary 解释 tier:

### §4.1 tier 1 — plateau Pearson r > 0.85 (paper §3.6.6 L1 region, gen 5-9)

**数学含义** (variance-explained):
$r^2 \geq 0.72$ → proxy $D^{\rm code, B/C}$ 与 $D^{\rm paper}$ 共享 ≥ 72% linear variance

**binary verdict (sub-agent 视角, 不绑 主协作者)**:
- ★ **partial circumstantial evidence** for paper §3.6.2 derivation 之 mean-field NESS form 之 **proxy-level consistency** with chain dynamics (form-borrow tier L2 之 ground)
- ★ **不 binary close** P0★-F — 仅 partial close (per brief §6.1 + §6.3 之 binary tier table)
- 真严 close P0★-F 仍需 D60+ 路径 A re-train EMA OR 路径 D rerun chain with EMA state explicit save (per brief §4.1 + §4.4)
- caveat: high Pearson 可能 by spurious co-monotonic decay 而 achieve, 不 imply stationary 平等 — paper §6.1 line 749-750 之 "**at the magnitude considered**" qualifier 之 真实严格度 tier 是 **L2 not L0**

### §4.2 tier 2 — 0.7 < r < 0.85 (paper §3.6.6 L1-L2 marginal)

**数学含义**: $r^2 \in [0.49, 0.72]$ → 49-72% linear variance shared

**binary verdict**:
- partial signal, 数学严格度 不 binary close
- 一凡 关卡 3 决是否 escalate 路径 A re-train EMA

### §4.3 tier 3 — 0.3 < r < 0.7 (marginal / partial mismatch)

**数学含义**: $r^2 \in [0.09, 0.49]$ → 9-49% linear variance shared

**binary verdict**:
- **partial mismatch confirmed**, 不能 close P0★-F
- sub-agent 推 路径 A escalate (re-train EMA) 或 路径 D rerun chain
- 推 D60+ 更深 verify (Spearman rank correlation alternative, clustered bootstrap 等)
- 即使 在 marginal region, N=40 之 power (per §1.4) 在 $\rho_{\rm true} = 0.3$ 时 仅 0.47 — single 实验 不 binary 区分 "weak correlation" 与 "no correlation", 需 multi-seed N≥8 escalate [?]

### §4.4 tier 4 — r < 0.3 (mismatch confirmed)

**数学含义**: $r^2 < 0.09$ → < 9% linear variance shared

**binary verdict**:
- **mismatch confirmed in proxy form** (per brief §6.1 之 L2 fail tier)
- paper §5.2 主定理 (2) 之 fixed-point identification 与 chain 实际 dynamics binary **不 一致** in proxy form
- 需 D60+ 路径 D rerun chain with EMA state explicit save 才能 binary close P0★-F
- 若 同时 路径 B + C 双 fail (per brief §6.1 之 inconsistency tier "路径 B 与 路径 C 之 Pearson 数值差异 > 50%"), surface paper v8 之 framework form 本身 不 align chain dynamics — 触发 反题 layer 5/19 之 P0★-F catch 之 substantive degenerative 评估 escalate
- **不 retract** paper §5.2 主定理 (2) (form-agnostic Banach apply 是 L2 严格度 valid), 但 paper-level **必须 add 之 disclaimer**: "Reading 2 fixed-point identification 仅 derive 在 $D^{\rm code, true}$ 空间; chain experimental D trajectory binary identification 与 $D^{\rm paper}$ stationary equality 在 D60+ 路径 D rerun 之前 不 binary resolve"

### §4.5 caveat — Pearson linear vs Spearman rank

paper §3.6.2 Reading 2 之 mean-field NESS 形式 是:
$$D^{*, \rm code}(\alpha) - D^* = -\frac{J_S}{4 \alpha N_{\rm contr}}$$

此 form 在 fixed-point identification 上 是 linear in $1/\alpha$, 但 chain dynamics 之 trajectory $D_n(\alpha, n)$ 之 evolution 是 **non-linear** (U-shape recovery per paper §3.6.5)。Pearson r 仅 capture linear correlation, **可能 underestimate** 真实 monotone non-linear correlation。

**alternative**: Spearman rank correlation $\rho_S$ = Pearson $r$ on ranks, robust to monotone non-linear transformation。sub-agent 推 路径 B/C analysis stage 同时 compute (Pearson, Spearman) pair, 给一凡 关卡 3 binary 比较 [?]。

**bootstrap CI 对 Spearman 同适用** (paired resample with replacement, rank transformation each resample)。

---

## §5 总结 binary verdict (sub-agent, 不绑 主协作者)

1. **Pearson r 数学定义 + bootstrap CI 95% 公式 ✓ derived** (per §1)
   - N=40 (路径 B 或 C 单独) 之 power 在 $\rho_{\rm true} \geq 0.5$ adequate (≥ 0.92); 在 $\rho_{\rm true} = 0.3$ underpowered (0.47)
   - bootstrap CI half-width 在 sample $r = 0.5$, N=40 ≈ 0.24 — single 实验 之 r point estimate 不能 binary 区分 brief §6.1 之 three tier 边界, 需 endpoint 判 [?]

2. **路径 B 数学 binary difference ✓ derived** (per §2)
   - closed-form: $E_n = \bar{\theta}_n^{\rm EMA} - \theta_{n-1} \approx \beta_\theta^N (E_{n-1} - \Delta\theta_{n-1})$, with $\beta_\theta^N = 0.999^{1460} \approx 0.232$
   - asymptotic bias: $E_\infty \approx -0.302 \cdot \Delta\theta_\infty$ (proxy underestimate true EMA by ~30% of one per-gen drift step)
   - L2 form-borrow tier 严守, 路径 B 不 binary close P0★-F

3. **路径 C 数学 binary difference ✓ derived** (per §3)
   - 路径 C 是 cumulative gen-0-anchored drift (scales as $n^2 \cdot |\Delta\theta|_F^2$); 真实 $D^{\rm code}$ 是 instantaneous EMA-deviation (scales as $|\Delta\theta|_F^2$ stationary)
   - 与 $D^{\rm paper}$ 之 高 Pearson 是 trivial 预期 (两者 都是 gen-0 anchored cumulative drift), high correlation 不 surprise 也 不 substantively close P0★-F
   - L2 form-borrow tier 严守

4. **Pearson r tier 之 数学含义 + binary verdict ✓ derived** (per §4)
   - r > 0.85 plateau: partial circumstantial evidence (L2 tier), 不 binary close P0★-F
   - 0.7 < r < 0.85: marginal, 一凡 关卡 3 决 escalate
   - 0.3 < r < 0.7: partial mismatch, 推 D60+ escalate
   - r < 0.3: mismatch confirmed in proxy form, 触发 paper-level disclaimer add
   - **caveat**: Pearson linear, Spearman rank 是 alternative; sub-agent 推 同时 compute (Pearson, Spearman) pair [?]

5. **D-1 binding 严守 ✓**:
   - 路径 B + C 不 binary close P0★-F (仅 partial close at strong-tier r > 0.85)
   - fully close P0★-F = 路径 A (re-train EMA) OR 路径 D (rerun chain with EMA save) 之 true EMA 之 Pearson r > 0.85 — D60+ 才能达 之 tier
   - 任何 close P0★-F 之 declaration 必 wait D60+, 投稿决策 D17-D28 窗口内 不 重启

6. **未 substantive derive 标 [?]**:
   - 路径 B 之 within-gen θ-trajectory quasi-linear interpolation 是 partial L2 approx [?]
   - Fisher-metric linearization in §3.3 之 small-drift assumption 在 chain transient 必然 violated [?]
   - effective N=80 (路径 B + C concat) 之 within-seed gen-axis correlation 严重, clustered bootstrap or hierarchical Pearson 之 application 推 一凡 关卡 3 之 sub-agent analysis decision [?]
   - Spearman rank correlation alternative 推 同时 compute [?]
   - paper §6.1 line 749-750 之 "Reading 2 null-shift prediction is robust against this caveat at the magnitude considered" 之 "at the magnitude considered" qualifier 真实严格度 tier 是 L2 not L0 [?]

---

**sub-agent 不绑 主协作者**: 本份 brief 仅 derive 数学 detail, 不 estimate paper inclusion, 不 declare close P0★-F, 不 inflate L2 form-borrow baseline。一凡 + 反题 layer 后续 audit 拿到 本份 brief 之后 直接 read, 不必 重 derive。

**binary 完成**: ack
