# Code-First Extract / Derive / Assess Report — 2026-05-17 晚

**生成时间**: 2026-05-17 晚 (Linux 姐姐主会话第三个 sub-agent, opus 4.7)
**目标**: 5/29 之前完成 paper v4 必读 raw materials。**实践先于认知 — code 指导数学,paper 是最后一步**。
**source**: 5/17 晚一凡 + DeepSeek 关卡 3 final 决定 (推翻 axiom-first 叙述,改 emergent from code + retrospective recognition)。
**严格 sequential**: 第一步完成 → 第二步启动 → 第三步启动。无跳步。

---

## 第一步 — code 逐行 extract (只做"实际是")

### 1.1 文件清单

| 文件 | 角色 | code lines |
|---|---|---|
| `src/contradiction_loss.py` | ℒ_矛盾 loss + EMA tracker (核心) | ~330 行 |
| `src/cat_trainer.py` | CATTrainer 集成 ℒ_总 = ℒ_LM + α·ℒ_矛盾 | ~180 行 |
| `src/train_one_generation.py` | 单代 fine-tune entry,接 `CATConfig` | ~210 行 |
| `src/run_arm_b_alpha_scan.py` | α scan launcher,跑 self-iteration 10 代 | ~340 行 |
| `src/metrics.py` `compute_perplexity_on_dataset` | test_ppl 算 random variable | ~80 行 |
| `configs/cat_arm_b.yaml` | **chain 5/10-5/12 实际 launched 用** (旧 framework) | 旧 framework |
| `configs/cat_arm_b_v2_dialectical.yaml` | **未被 chain launched** (新 framework, 仅 default) | 新 framework |
| `scripts/phase1_robust_chain.sh` | chain launcher 脚本 (binary verify config) | bash |
| `scripts/m_eff_direct_fit.py` | 5/9 dataset fit m_eff = 0.212 (post-hoc) | post-hoc |

### 1.2 变量 + 函数 binary extract (LaTeX raw form)

#### 1.2.1 `KLContradictionConfig` dataclass 默认值

`contradiction_loss.py` 行 ~70-100:

| 字段 | code 默认 | 含义 |
|---|---:|---|
| `kl_direction` | `"q_to_p"` | $\mathrm{KL}(q \| p)$ where $q$ = EMA, $p$ = current |
| `val_subset_size` | 256 | val 句子集大小 |
| `val_max_length` | 64 | val 序列长度 |
| `beta_model` | 0.999849 | mean teacher EMA decay $\beta_\theta = e^{-0.212/1406}$ |
| `beta_kl` | 0.8090 | KL 序列 EMA decay $\beta_D = e^{-0.212}$ |
| `lambda_1` | 2.3585 | $1/(2 m_{\mathrm{eff}}) = 1/(2 \times 0.212)$ |
| `lambda_2` | 0.1060 | $m_{\mathrm{eff}}/2 = 0.212/2$ |
| `lambda_3` | 0.2120 | $m_{\mathrm{eff}}$ (option-β) |
| `kl_update_every` | 10 | 每 10 train step 算一次 KL |
| `T_2_form` | `"quadratic"` | $D_n^2/2$ symmetric |
| `kl_history_K` | 9 | Volterra K-step (metric only) |
| `m_eff` | 0.212 | $\chi(k) = e^{-m_{\mathrm{eff}} k}$ |

#### 1.2.2 `cat_arm_b.yaml` cat section (chain 5/10-5/12 实际 launch 用)

```yaml
cat:
  enabled: true
  alpha_scan: [0.0, 1.0, 5.0, 10.0, 50.0]
  kl_update_every: 10
  val_subset_size: 256
  val_max_length: 64
  beta_model: 0.999      # 不是 default 0.999849 (override)
  beta_kl: 0.9           # 不是 default 0.8090 (override)
  lambda_1: 1.0          # 不是 default 2.3585 (override)
  lambda_2: 1.0          # 不是 default 0.1060 (override)
  lambda_3: 1.0          # 不是 default 0.2120 (override)
  enable_grad_norm_monitor: true
  # 无 T_2_form / kl_history_K / m_eff (yaml 缺失,run_arm_b 用 dataclass default 旧 framework 安全):
  # T_2_form="relu_dpp", kl_history_K=1, m_eff=1.0
```

**binary verify**: chain log `phase1_robust_alpha10.0_seed*_*.log` 在 5/11 14:39 起 explicit print:

```
KLContradictionTracker init: beta_model=0.999000 beta_kl=0.9000 lambda_1=1.0000
lambda_2=1.0000 lambda_3=1.0000 m_eff=1.0000 T_2_form=relu_dpp kl_history_K=1 kl_update_every=10
```

**这是 chain 实际跑用的 config (旧 framework, 不是 m_eff=0.212 v2_dialectical)**。

#### 1.2.3 `cat_arm_b_v2_dialectical.yaml` (NOT launched by chain)

```yaml
cat:
  alpha_scan: [0.0, 1.0, 5.0, 10.0, 20.0]  # α=50 已撤
  beta_model: 0.999849
  beta_kl: 0.8090
  lambda_1: 2.3585       # = 1/(2 × 0.212)
  lambda_2: 0.1060       # = 0.212/2
  lambda_3: 0.2120       # = 0.212 option-β
  T_2_form: "quadratic"
  kl_history_K: 9
  m_eff: 0.212
```

**binary**: 此 yaml 在 chain 5/10-5/12 **never launched**。phase1_robust_chain.sh 行 75 hardcode `--config configs/cat_arm_b.yaml` 旧 framework。v2 仅作 D5-D7 D7-D9 未来 launch placeholder。

#### 1.2.4 `KLContradictionTracker.compute_kl` (KL extract)

`contradiction_loss.py` 行 ~140-180:

输入: model (current θ, with grad) + val batch (256 句, 64 tokens)。

```python
logits_p = model(val_input_ids, ...).logits           # current model, with grad
logits_q = self.ema_model(val_input_ids, ...).logits  # EMA model, no grad

log_p = F.log_softmax(logits_p[:, :-1, :], dim=-1)
log_q = F.log_softmax(logits_q[:, :-1, :], dim=-1)

# kl_direction = "q_to_p" default:
q = log_q.exp().detach()
kl_per_pos = (q * (log_q.detach() - log_p)).sum(dim=-1)  # [B, T-1]

mask = val_attention_mask[:, 1:].float()
kl_scalar = (kl_per_pos * mask).sum() / mask.sum().clamp_min(1)
```

**LaTeX binary form**:

$$D_n^{\rm code} \;=\; \frac{1}{\sum_{b,t} m_{b,t}}\,\sum_{b,t}\,m_{b,t}\,\sum_{v}\,q^{\rm EMA}_{n,b,t}(v)\,\bigl(\log q^{\rm EMA}_{n,b,t}(v) - \log p^{\theta_n}_{n,b,t}(v)\bigr)$$

其中:
- $q^{\rm EMA}_n = \mathrm{softmax}(\mathrm{logits}_{\bar\theta_n})$ — EMA model output, **fully detached**
- $p^{\theta_n}_n = \mathrm{softmax}(\mathrm{logits}_{\theta_n})$ — current model output, **with grad on θ_n**
- $b, t$ index batch position 1..255, token position 1..63
- $m_{b,t}$ attention mask (padding 排除)
- $v$ index vocab 1..50257 (OPT-125m)

**严格 statement**: $D_n^{\rm code} = \mathrm{KL}(q^{\rm EMA}_n \| p^{\theta_n}_n)$ on a **fixed val batch of 256 wikitext-2 val 句**,每 10 train step compute 一次。

#### 1.2.5 `KLContradictionTracker.compute_loss` (ℒ_矛盾 raw form)

`contradiction_loss.py` 行 ~200-285,简化抓核心:

```python
D_n = self.compute_kl(model, val_input_ids, val_attention_mask)  # has grad

# 三项分解 (rest depend on D_history length)
if len(D_history) >= 2:
    D_nm1 = D_history[-1]    # detached
    D_nm2 = D_history[-2]    # detached
    delta_D = D_n - D_nm1
    D_doubleprime = D_n - 2 * D_nm1 + D_nm2
elif len(D_history) == 1:
    delta_D = D_n - D_history[-1]
    D_doubleprime = 0
else:
    delta_D = 0; D_doubleprime = 0

# memory 项: (D_n - D_ema)^2
D_ema_cur = self.D_ema.detach()    # fully detached EMA
memory_term = (D_n - D_ema_cur) ** 2

# T1 velocity
T1_velocity = delta_D ** 2

# T2 form (chain 用 "relu_dpp" 因 yaml 缺 T_2_form → dataclass default)
if T_2_form == "relu_dpp":
    T2_replace = F.relu(D_doubleprime)
elif T_2_form == "quadratic":
    T2_replace = (D_n ** 2) / 2

# T3 memory
T3_memory = memory_term

loss = lambda_1 * T1_velocity + lambda_2 * T3_memory + lambda_3 * T2_replace
```

**LaTeX binary form (chain 实际跑的 form, 旧 framework, λ_i=1, T_2_form=relu_dpp)**:

$$\boxed{\;\mathcal{L}_{\rm cont}^{\rm code,\,actual}(\theta_n) \;=\; (D_n - D_{n-1})^2 \;+\; \mathrm{ReLU}(D_n - 2 D_{n-1} + D_{n-2}) \;+\; (D_n - \bar D_n^{\rm EMA})^2\;}$$

**注意 chain 实际跑的 form 关键点**:
1. **λ_1 = λ_2 = λ_3 = 1** (yaml override, **不是** Klein-Gordon-borrowed $1/(2m_{\mathrm{eff}}), m_{\mathrm{eff}}/2, m_{\mathrm{eff}}$)
2. **T_2 = ReLU(D''_n)** (旧 mechanical punitive 单边,不是 quadratic symmetric)
3. **T_3 = (D_n - $\bar D_n^{\rm EMA}$)^2** — 不是 paper §3.5 写的 $(\Sigma_1 D)_n^2$ Volterra 借用 form
4. **Volterra K=1** (yaml 缺 kl_history_K → dataclass default 缺失实际是新 default 9 但 `getattr(yaml_cat, "kl_history_K", 1)` 因 CATYamlConfig schema 缺 attr → return 1)。**chain log 确认 K=1**,所以 chain 实际**不进任何 Volterra accumulation**。

#### 1.2.6 EMA 计算 (mean teacher, parameter space)

`contradiction_loss.py` 行 ~130:

```python
@torch.no_grad()
def update_ema_model(self, model):
    for p_ema, p in zip(self.ema_model.parameters(), model.parameters()):
        p_ema.data.mul_(self.cfg.beta_model).add_(p.data, alpha=1 - self.cfg.beta_model)
```

**LaTeX binary**:

$$\bar\theta_{n+1} \;=\; \beta_\theta\,\bar\theta_n + (1 - \beta_\theta)\,\theta_n, \quad \beta_\theta = 0.999\ (\text{chain})$$

每个 train step 之后 (training_step hook) 调一次。$\beta_\theta = 0.999$ horizon ~1000 steps,大于单代 5 epoch × 37354 / 128 ≈ 1460 steps 的 ~3/2,所以 EMA 大致 cover 整代但有 partial smoothing。

#### 1.2.7 EMA-D (KL 序列 EMA, scalar space)

`contradiction_loss.py` 行 ~262:

```python
with torch.no_grad():
    self.D_ema = self.cfg.beta_kl * D_ema_cur + (1 - self.cfg.beta_kl) * D_n.detach()
```

**LaTeX binary**:

$$\bar D_{n+1}^{\rm EMA} \;=\; \beta_D\,\bar D_n^{\rm EMA} + (1 - \beta_D)\,D_n, \quad \beta_D = 0.9\ (\text{chain})$$

**初始化**: `if self.D_ema is None: self.D_ema = D_n.detach().clone()` — 第一次 compute_loss 时 $\bar D_1 = D_1$,后续更新。

#### 1.2.8 history buffer

`contradiction_loss.py` 行 ~267-269:

```python
self.D_history.append(D_n.detach())
if len(self.D_history) > self.cfg.kl_history_K:
    self.D_history.pop(0)
```

**chain 用 K=1**: history 最多保留 1 个元素 $D_{n-1}$。
**注意 K=1 时 D_history 实际不够 compute $D''_n$** (需要 $\ge 2$ 元素),所以 chain 的 $D''_n$ 永远为 0 → **T_2 = ReLU(0) = 0**。

**LaTeX binary statement (chain K=1)**:

$$T_2^{\rm chain} \;=\; \mathrm{ReLU}(D_n - 2 D_{n-1} + D_{n-2}) \;=\; \mathrm{ReLU}(0) \;=\; 0 \quad (\forall n \ge 2)$$

(因 K=1 → D_history 永远只有 ≤1 元素 → if 分支落 `len(D_history) == 1`: D_doubleprime = `torch.zeros_like(D_n)`)

**所以 chain 实际跑的 ℒ_矛盾 严格 form**:

$$\boxed{\;\mathcal{L}_{\rm cont}^{\rm chain,\,actual}(\theta_n) \;=\; (D_n - D_{n-1})^2 \;+\; 0 \;+\; (D_n - \bar D_n^{\rm EMA})^2\;}$$

$$\boxed{\;\mathcal{L}_{\rm cont}^{\rm chain,\,actual}(\theta_n) \;=\; (\Delta D_n)^2 \;+\; (D_n - \bar D_n^{\rm EMA})^2\;}$$

**这是震撼的发现 — chain 5/10-5/12 实际跑的 ℒ_矛盾 只剩两项**(velocity 项 + EMA-deviation 项),T_2 项**完全不进 loss** (永远是 0)。Paper v3 §3.5 写 "三项 Volterra 借用 form" 与 code 实际行为不符。

#### 1.2.9 gradient chain rule (autograd flow extract)

ℒ_矛盾 的 gradient 通过 D_n forward 流 (current model logits)。**所有历史 detached**:
- $D_{n-1}, D_{n-2}$ 都 `.detach()`
- $\bar D_n^{\rm EMA}$ `.detach()`
- $q^{\rm EMA}$ 整个 EMA model `requires_grad = False`
- Volterra accumulator 在 `torch.no_grad()` 块里(line ~258)
- `update_ema_model` 在 `torch.no_grad()` 块里

**LaTeX binary**:

$$\frac{\partial \mathcal{L}_{\rm cont}^{\rm chain,\,actual}}{\partial \theta_n} \;=\; \underbrace{2(\Delta D_n)\,\frac{\partial D_n}{\partial \theta_n}}_{T_1\ \text{grad}} \;+\; \underbrace{2(D_n - \bar D_n^{\rm EMA})\,\frac{\partial D_n}{\partial \theta_n}}_{T_3\ \text{grad}}$$

$$\frac{\partial \mathcal{L}_{\rm cont}^{\rm chain,\,actual}}{\partial \theta_n} \;=\; 2\,\bigl[(\Delta D_n) + (D_n - \bar D_n^{\rm EMA})\bigr]\,\frac{\partial D_n}{\partial \theta_n}$$

**关键**: gradient 完全通过当前 D_n forward 流,**没有任何 cross-generation 梯度传递**(history 都 detached)。Paper v3 §3.6 描述的 K-th order chain rule + Σ_1 D 跨代贡献,在 code 实际 form 下数学 vacuous(per paper §3.6 已 honest disclose,但 paper §3.5 仍写 "Volterra form")。

#### 1.2.10 总 loss 集成

`cat_trainer.py` `CATTrainer.compute_loss`:

```python
outputs = model(**inputs)
lm_loss = outputs.loss

if should_compute_contradiction:  # every kl_update_every=10 train step
    val_batch = self._get_val_batch()
    contra_loss, contra_metrics = self.contradiction_tracker.compute_loss(
        model, val_ids, val_mask
    )
    total_loss = lm_loss + self.contradiction_alpha * contra_loss
else:
    total_loss = lm_loss
```

**LaTeX binary**:

$$\mathcal{L}_{\rm total}(\theta_n) \;=\; \mathcal{L}_{\rm LM}(\theta_n) \;+\; \alpha \cdot \mathcal{L}_{\rm cont}^{\rm chain,\,actual}(\theta_n) \cdot \mathbf{1}_{\,n \bmod 10 = 0,\,n > 0}$$

注意 $\mathbf{1}$ 指示函数 — **大多数 train step 只有 $\mathcal{L}_{\rm LM}$**,只在每 10 step 算一次 contradiction loss。

#### 1.2.11 test_ppl random variable extract

`metrics.py` `compute_perplexity_on_dataset`:

输入: model checkpoint path (代际 g 训练完的 model), wikitext-2 **test** set blocks (block_size=64, batch=128, fp16)。

```python
losses = []
for batch_start in range(0, n, batch_size):
    input_ids = ...
    labels = input_ids.clone(); labels[attention == 0] = -100
    out = model(input_ids, attention_mask, labels=labels)
    n_tokens = (labels != -100).sum().item()
    losses.append((out.loss.item(), n_tokens))

total_loss = sum(l * n for l, n in losses)
total_tok = sum(n for _, n in losses)
mean_loss = total_loss / total_tok
ppl = math.exp(mean_loss) if mean_loss < 20 else float("inf")
return {"mean_perplexity": ppl, ...}
```

**LaTeX binary**:

$$\mathrm{PPL}_n^{\rm test,\,chunked} \;=\; \exp\!\left(\frac{1}{\sum_{b,t} m_{b,t}}\sum_{b,t} m_{b,t}\,(-\log p^{\theta_n}_{b,t}(\mathrm{true})_{b,t})\right)$$

on **wikitext-2 test** (240 blocks ≈ 15360 tokens), chunked block_size=64, no overlap。

**关键差异**: `compute_perplexity_on_dataset` 用 chunked block=64 无 overlap (HF Trainer default), **不是** sliding-window stride=256 — 这导致 gen 0 = 36.3 vs Shumailov paper 20 的 +80% offset (per `sliding_window_eval_verdict_20260510.md` 已 explicit 验证)。

### 1.3 chain jsonl 实际数字 extract

`armb_alpha10.0_seed{1,2,3,4}_2026051[12]_*.jsonl` test_perplexity:

| seed | gen 0 | gen 1 | gen 2 | gen 3 | gen 4 | gen 5 | gen 6 | gen 7 | gen 8 | gen 9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 36.3 | 77.2 | 107.2 | 105.3 | 87.3 | 67.5 | 61.5 | 56.9 | 53.7 | 57.2 |
| 2 | 36.2 | 80.2 | 100.3 | 98.4 | 75.7 | 66.4 | 63.0 | 56.7 | 56.4 | 56.9 |
| 3 | 36.3 | 76.6 | 102.4 | 85.5 | 62.4 | 59.1 | 53.7 | 54.5 | 55.1 | 52.8 |
| 4 | 36.4 | 75.6 | 105.2 | 95.7 | 75.2 | 69.4 | 56.9 | 54.2 | 52.7 | 53.4 |

**模式**: U-shape recovery (gen 1-2 spike to ~80-107, gen 3-9 衰减到 ~52-57 plateau)。gen 9/gen 0 ratio ≈ 1.4-1.6,**不是** Shumailov monotone 20 → 28 (1.4 ratio 是巧合,trajectory shape 完全不同)。

**chain 实际跑的 m_eff (per-run fit)** per `m_eff_direct_fit_verdict_20260510.md`:

| Run | best AIC model | m_eff |
|---|---|---:|
| 20260507_200657 | biexp_recovery | 0.1099 |
| 20260508_092730 | exp_recovery | 0.2333 |
| 20260508_144612 | exp_recovery | 0.2120 |

across-run median = **0.212**, mean = 0.185, std = 0.066, range = [0.110, 0.233]。但**这 3 run 全部 seed=42 reruns**,variance 来自 fp16 / library drift,不是真 multi-seed。

5/12 主协作者层 17-23% NMI 声明基于 m_eff=0.212 single-seed (per CLAUDE.md 5/15 standing rule 教训),已撤回。5/15 后纪律: chain seed 1-4 multi-seed 实拟合 m_eff [0.300 ± 0.042] 是 post-hoc reference,**不是 chain launched 时用的数字**。

### 1.4 chain 实际跑的 ℒ_矛盾 form — binary 最终

$$\boxed{\mathcal{L}_{\rm cont}^{\rm chain,\,5/10\text{-}5/12,\,actual}(\theta_n) \;=\; \underbrace{(D_n^{\rm code} - D_{n-1}^{\rm code})^2}_{T_1\ \text{velocity}} \;+\; \underbrace{(D_n^{\rm code} - \bar D_n^{\rm EMA})^2}_{T_3\ \text{EMA-deviation}}}$$

with:

- $D_n^{\rm code} = \mathrm{KL}(q^{\rm EMA}_n \| p^{\theta_n}_n)$ on 256 wikitext-2 val 句, 每 10 train step compute
- $\bar\theta_{n+1} = 0.999\,\bar\theta_n + 0.001\,\theta_n$ (mean teacher EMA)
- $\bar D_{n+1}^{\rm EMA} = 0.9\,\bar D_n^{\rm EMA} + 0.1\,D_n$ (KL 序列 EMA)
- $\lambda_1 = \lambda_3 = 1$ (yaml override)
- T_2 项 = 0 (K=1 → D_history 不够算 $D''_n$,落 `torch.zeros_like` 分支)
- 历史全部 detached, gradient 仅通过当前 $D_n$ forward 流

---

## 第二步 — 基于 code 实际 form 重 derive 全部数学

(第一步完成,启动第二步)

### 2.1 ℒ_矛盾 chain actual form 数学性质 — 重新 derive

#### 2.1.1 Banach contraction in D-space (重 derive)

paper v3 §3.6 derive 基于 ansatz $T(D) = (D + J_S m_{\mathrm{eff}}/\alpha)/(1 + m_{\mathrm{eff}}^2)$,**$1 + m_{\mathrm{eff}}^2$ 来自 paper §3.5 假设 Volterra form** $(\Sigma_1 D)^2$ 的 χ kernel + λ_3 unify。

但 code 实际 T_2 = 0 + T_3 = $(D_n - \bar D_n^{\rm EMA})^2$,这是 **EMA-deviation** 不是 $(\Sigma_1 D)^2$。重 derive Banach map:

假设 mean-field approximation:在 NESS 不动点 $D^*$ 附近,$\bar D_n^{\rm EMA} \approx D^*$,$D_{n-1} \approx D^*$。

更新 rule (在 SGD large-batch limit):

$$\theta_{n+1} = \theta_n - \eta \nabla \mathcal{L}_{\rm total}(\theta_n)$$
$$D_{n+1} = D_n - \eta \alpha \frac{\partial \mathcal{L}_{\rm cont}^{\rm chain}}{\partial D_n} - \eta \frac{\partial \mathcal{L}_{\rm LM}}{\partial D_n}$$

其中

$$\frac{\partial \mathcal{L}_{\rm cont}^{\rm chain}}{\partial D_n} = 2(D_n - D_{n-1}) + 2(D_n - \bar D_n^{\rm EMA}) = 2\bigl[2 D_n - D_{n-1} - \bar D_n^{\rm EMA}\bigr]$$

在 mean-field $D_{n-1} \approx D^*, \bar D_n^{\rm EMA} \approx D^*$:

$$\frac{\partial \mathcal{L}_{\rm cont}^{\rm chain}}{\partial D_n} \approx 4(D_n - D^*)$$

假设 $\partial \mathcal{L}_{\rm LM}/\partial D_n \approx J_S$ (per paper v3 Hartree closure approximation, $J_S$ 是 self-iteration novelty source term):

$$D_{n+1} \approx D_n - \eta \alpha \cdot 4(D_n - D^*) - \eta J_S$$

定义 Banach map $T(D) = D - \eta \alpha \cdot 4(D - D^*) - \eta J_S$。求不动点 $D^* = T(D^*)$:

$$D^* = D^* - \eta J_S \quad\Rightarrow\quad J_S = 0$$

**问题**: 这个 fixed point trivial。需要 close with explicit $D^*$ self-consistency。

**重 derive 严格**: linearize 在 $D^*$ 附近, $D_n = D^* + \epsilon_n$:

$$\epsilon_{n+1} = \epsilon_n (1 - 4\eta\alpha) - \eta J_S$$

非齐次, fix point at $\epsilon^* = -\eta J_S / (4\eta\alpha) = -J_S/(4\alpha)$。所以

$$\boxed{\;D^{*,\,\rm code\,actual}(\alpha) \;=\; D^* - \frac{J_S}{4\alpha}\;}$$

这与 paper v3 $D^*(\alpha) = J_S/(\alpha m_{\mathrm{eff}})$ **functional form 不同**:
- paper: $\propto 1/(\alpha m_{\mathrm{eff}})$
- code actual: $\propto 1/\alpha$ (no $m_{\mathrm{eff}}$ dependence,因 chain T_2=0 + T_3 = EMA-deviation 不含 Volterra)

**Lipschitz 常数**:

$$|T(D) - T(D')| = |D - D'| \cdot |1 - 4\eta\alpha|$$

contraction ⟺ $|1 - 4\eta\alpha| < 1$ ⟺ $0 < \eta\alpha < 1/2$。

代入 chain 实际数字: $\eta = 2 \times 10^{-5}$, $\alpha = 10$ → $\eta\alpha = 2 \times 10^{-4} \ll 1/2$ → $\rho = 1 - 4 \times 2 \times 10^{-4} = 0.99920$。

**半收敛代数** $n_{1/2} = \log(0.5)/\log(0.99920) = 866$ train steps ≈ **0.6 epoch** (chain 1460 steps/epoch)。

**严格度档位**:
- contraction in mean-field linear approximation: **L1 (form 借用 + 假设漂移)** — mean-field assumption $D_{n-1} \approx D^* \approx \bar D_n^{\rm EMA}$ 在 NESS 不动点附近 valid,但 transient 期(gen 1-2 spike)严格不成立
- 严格 prove without mean-field: **L0 (vacuous)** — chain rule 通过 $D_n$ 与 $D_{n-1}, \bar D_n^{\rm EMA}$ detached, 非线性 dynamics 严格 prove 需 12-layer transformer 函数空间几何分析,~6-12 month substantive

#### 2.1.2 Lyapunov drift (重 derive)

paper v3 §3.5 V_4 := $\frac{1}{2}\|\theta - \theta^*\|^2$, drift form:

$$\mathbb{E}[V_4(\theta_{n+1}) - V_4(\theta_n)] \le -2\eta\mu_{\rm total}(\alpha) V_4(\theta_n) + \frac{1}{2}\eta^2(L_g^2 + \sigma^2)$$

这个 form 不依赖 ℒ_矛盾 specific form,只依赖 ℒ_total 满足 PL condition (假设 A3' + A5)。**code actual form 不改变此 drift form**,因 V_4 选 norm-like 不依赖 loss form。

但 **A5 (conditional ℒ_contr θ-PL)** 在 code actual form 下需要重新 verify:

$$\|\nabla_\theta \mathcal{L}_{\rm cont}^{\rm chain}\|^2 = 4\bigl[2D_n - D_{n-1} - \bar D_n^{\rm EMA}\bigr]^2 \cdot \|\nabla_\theta D_n\|^2$$

PL inequality 要求 $\|\nabla_\theta \mathcal{L}_{\rm cont}^{\rm chain}\|^2 \ge 2\mu_{\rm contr}\,\mathcal{L}_{\rm cont}^{\rm chain}$,即:

$$4\bigl[2D_n - D_{n-1} - \bar D_n^{\rm EMA}\bigr]^2 \|\nabla_\theta D_n\|^2 \ge 2\mu_{\rm contr}\,\bigl[(D_n - D_{n-1})^2 + (D_n - \bar D_n^{\rm EMA})^2\bigr]$$

在 mean-field $D_{n-1} = \bar D_n^{\rm EMA} = D^*$:
- LHS = $4 \cdot 4(D_n - D^*)^2 \|\nabla_\theta D_n\|^2 = 16(D_n - D^*)^2 \|\nabla_\theta D_n\|^2$
- RHS = $2\mu_{\rm contr} \cdot 2(D_n - D^*)^2 = 4\mu_{\rm contr}(D_n - D^*)^2$

PL inequality satisfied iff $\|\nabla_\theta D_n\|^2 \ge \mu_{\rm contr}/4$ — 即 **D-saddle region** ($\nabla_\theta D_n = 0$) 排除在外。

**严格度档位**: PL prove on code actual form ℒ_contr **L1 (mean-field + conditional)** — 与 paper v3 §3.5 同档位,assumption 漂移项目相同。

#### 2.1.3 NESS fixed point (重 derive)

由 2.1.1, $D^{*,\,\rm code\,actual}(\alpha) = D^* - J_S/(4\alpha)$ ($D^*$ 是 mean-field equilibrium D value)。

更严格 NESS condition:在 NESS, $\mathbb{E}[D_n] = D^*$ stationary, balance condition

$$\eta \cdot \alpha \cdot \mathbb{E}[\partial \mathcal{L}_{\rm cont}^{\rm chain}/\partial D] = -\eta J_S$$

per 2.1.1 给 $D^*$ self-consistency。但 $J_S$ 在 code 中**不是 explicit term** — 是 paper v3 Hartree closure approximation 的 source。code 实际 closure 是 $\mathcal{L}_{\rm LM}$ + Shumailov synthetic data dynamics,**无 explicit $J_S$**。

**严格 statement (honest)**:

$$\boxed{\;\text{NESS fixed point } D^{*,\,\rm code\,actual}(\alpha) \text{ 严格 existence 在 chain code form 下 unknown.}\;}$$

只能 give **mean-field approximation** value $D^* \approx \bar D_n^{\rm EMA}$ at convergence, 实证 chain seed 1-4 给 plateau $D^* \approx \log(55) - \log(36) = 0.42$ at $\alpha = 10$ (但 D 是 KL on val 不是 log(PPL_test) — 见 2.3 mismatch)。

**严格度档位**: **L2 (mean-field approximation + 实证 fit)** — 给 fixed point existence + value 来自 mean-field linear regression on chain data,不是 first-principles derive。

#### 2.1.4 几何收敛 (重 derive)

per 2.1.1 mean-field linear:

$$|\epsilon_{n+1}| = |1 - 4\eta\alpha| \cdot |\epsilon_n|$$

代入 chain: $\rho^{\rm code\,actual} = 1 - 4\eta\alpha = 0.99920$ (per train step, **不是** per generation)。

**Per-generation 收敛**: 单代 1460 train steps, gradient update only every 10 step compute contradiction = 146 contradiction updates per generation。$\rho^{\rm code,\,per-gen} = (0.99920)^{146} = 0.890$。

**半收敛代数** $n_{1/2}^{\rm code,\,per-gen} = \log(0.5)/\log(0.890) = 5.9$ generations。

**paper v3 写 $\rho = 1/(1+m_{\mathrm{eff}}^2) = 0.957$ per generation**, 半收敛代数 15.7 — **code actual form 给的 $\rho = 0.890$ per generation更快**(因 $4\eta\alpha$ factor 远大于 $m_{\mathrm{eff}}^2 = 0.045$)。

**chain 实证数字**: seed 1-4 gen 1-9 偏离 plateau $|\epsilon_n|$ approx geometric? 检验:

| gen | seed 1 偏离 plateau (~55) | seed 2 | seed 3 | seed 4 |
|---|---:|---:|---:|---:|
| 1 | 22.2 | 25.2 | 21.6 | 20.6 |
| 2 | 52.2 | 45.3 | 47.4 | 50.2 |
| 3 | 50.3 | 43.4 | 30.5 | 40.7 |
| 4 | 32.3 | 20.7 | 7.4 | 20.2 |
| 5 | 12.5 | 11.4 | 4.1 | 14.4 |

观察 gen 2-5 ratio: seed 1 (52/22, 50/52, 32/50, 12/32) = (2.4, 0.97, 0.64, 0.39)。**不是几何 geometric** (因 gen 1 → gen 2 still increasing not contracting)。

**真实 chain trajectory shape**: U-shape recovery (gen 1-2 increase, gen 3-9 contract)。Mean-field linear approximation 给的 $\rho < 1$ 几何收敛 **不复现 chain 实证 U-shape**。

**严格度档位**: **L0 (vacuous / 与实证不符)** — 几何收敛 prediction 与 chain 实证 U-shape 直接矛盾,mean-field approximation 在 gen 1-2 transient 期严格失效。

### 2.2 数值 cascade (用 chain 实际 config 数字)

chain 5/10-5/12 实际 launched 用 cat_arm_b.yaml:
- λ_1 = λ_2 = λ_3 = 1.0
- β_kl = 0.9
- β_model = 0.999
- T_2_form = relu_dpp (不进 loss 因 K=1)
- m_eff = 1.0 (yaml 没 m_eff override,dataclass default 是 1.0;但实际不 enter loss 因 K=1)

**所以 chain m_eff 实际 effective value 是 NOT USED — code 不在 loss 中 reference m_eff**(因 K=1 且 T_2=0)。

post-hoc fit m_eff = 0.212 (per-run median across 3 seed=42 reruns) **完全不是 chain 跑时用的 framework parameter** — 是 post-hoc descriptive statistic fit 在 chain test_ppl 数据上,**没进 ℒ_矛盾 form**。

| paper v3 数字 | code chain 实际 |
|---|---|
| $\rho = 1/(1+0.212^2) = 0.957$ per-gen | $\rho = (1 - 4 \times 2 \times 10^{-5} \times 10)^{146} = 0.890$ per-gen |
| $D^*(\alpha=10) = J_S/(10 \times 0.212) = 0.47 J_S$ | $D^*(\alpha=10) = D^* - J_S/40$ |
| $n_{1/2} = 15.7$ gens | $n_{1/2} = 5.9$ gens |
| $\mathrm{PPL}_\infty(\alpha=10) = \exp(D^* + ...)$ | $\mathrm{PPL}_\infty(\alpha=10) \approx 55$ (chain plateau 实证) |

chain 实证 gen 9 ≈ 52-57 与 mean-field $D^* \approx \log(55)$ 一致, 但**这不是 paper v3 form 的 prediction** — 是 mean-field approximation on code actual form 给的 ad-hoc fit。

### 2.3 D 定义 mismatch — binary 确认

| 定义 | code $D_n^{\rm code}$ | paper $D_n^{\rm paper}$ |
|---|---|---|
| Random variable | $\mathrm{KL}(q^{\rm EMA} \| p^{\theta_n})$ | $\log(\mathrm{PPL}_n^{\rm test}/\mathrm{PPL}_0^{\rm test})$ |
| Distribution | EMA model vs current model | current model output distribution vs true distribution |
| Set | 256 wikitext-2 **val** 句, batch=8 in compute_kl, 每 10 train step | wikitext-2 **test** set 240 blocks chunked block=64, 每 generation end |
| Train signal? | **yes** — gradient 流 backward | **no** — eval-only metric, no gradient |
| 单位 | nats per token (KL) | log-ratio of perplexity (dimensionless) |
| 数学关系 | 不一致,**不同 random variables** | 不能直接 unify |

**chain 实际**:
- code 训练时用 $D_n^{\rm code}$ as training signal (gradient through D_n)
- paper §4 plot + analyze 用 $D_n^{\rm paper} = \log(\mathrm{PPL}_n/\mathrm{PPL}_0)$
- 两者 **不是同一 random variable**, paper §3.5 main theorem statement (1)(2)(3) 写 "$\mathbb{E}[D(\theta_n)] \to D^*$" 但**没 explicit 区分这是 $D^{\rm code}$ 还是 $D^{\rm paper}$**

**这可能是 +29% discrepancy 真实来源?** 

需要 chain jsonl 中实际 log 的 $D_n^{\rm code}$ vs $D_n^{\rm paper} = \log(\mathrm{PPL}_n/\mathrm{PPL}_0)$ 数字 binary 对比。chain jsonl 没 log $D_n^{\rm code}$ scalar (只 log test_perplexity)。**所以 mismatch 严格 binary verify 需要 reload chain checkpoint 重新 compute $D_n^{\rm code}$, ~2-4 hour engineering work**。

**honest disclosure**: 两 D 是不同 random variables, paper v3 §3.5/§3.6 main theorem 在 $D^{\rm paper}$ 上 state 但 derivation 用 $D^{\rm code}$ Volterra form。这是 **semantic mismatch**,reviewer 易 catch。

### 2.4 改 paper 追 code (纪律 3) — paper v3 update 清单

按纪律 3 (code 实际 form 优先于 paper derived form),paper v3 §3 / §3.5 / §3.6 / §6 必改:

#### 2.4.1 §3 ℒ_矛盾 definition

**当前 paper v3**:
$$\mathcal{L}_{\rm cont} = \lambda_1 (\Delta D_n)^2 + \lambda_2 (D_n - \bar D_n^{\rm EMA})^2 + \lambda_3 (\Sigma_1 D)_n^2$$

**改 code actual**:
$$\mathcal{L}_{\rm cont} = (\Delta D_n)^2 + (D_n - \bar D_n^{\rm EMA})^2$$

with **二项不三项**, **λ_i = 1 不 Klein-Gordon-borrowed**, **无 Volterra accumulator 项**。

#### 2.4.2 §3.5 主定理 statement

**当前 paper v3**: $D^*(\alpha) = J_S/(\alpha m_{\mathrm{eff}})$

**改 code actual**: $D^{*,\,\rm code}(\alpha) = D^* - J_S/(4\alpha)$ (mean-field approximation)

主定理 (1) absorbing states 不可达: **保留**, V_4 = $\|\theta - \theta^*\|^2$ Foster-Lyapunov 与 ℒ_矛盾 specific form 弱依赖
主定理 (2) NESS fixed point: **改 form**, 系数从 $1/(\alpha m_{\mathrm{eff}})$ 改 $1/(4\alpha)$
主定理 (3) 几何收敛 $\rho = 1/(1 + m_{\mathrm{eff}}^2)$: **改 $\rho = (1 - 4\eta\alpha)^{N_{\rm step}/10}$** (per-generation 复合)

#### 2.4.3 §3.6 chain rule

**当前 paper v3**: 已 honest disclose K-th order vacuous, 但仍写 Volterra structure

**改 code actual**: 改写为 "single-step path-independent loss (T_2 项不进 loss, 仅 metric)"
- 删除 §3.6 Volterra T_3 normalization unify (option-β χ kernel) — chain 实际 K=1 不进 loss, 整段 vacuous
- 改写为 "Markov 1-step memory: T_1 = $(\Delta D_n)^2$ + T_3 = $(D_n - \bar D_n^{\rm EMA})^2$ are the only two active terms in current implementation"

#### 2.4.4 §6 future work

加 explicit:
- "T_2 项 (Volterra K=9 path-dependent accumulator) currently logged as metric only, does **not** enter training loss. Mathematical activation requires (i) lifting K=1 default in yaml to K=9, AND (ii) substantive derivation of K-th order chain rule with cross-generation gradient flow. Estimated 2-4 weeks substantive work."
- "Klein-Gordon Lagrangian form-borrowing in v2_dialectical.yaml ($\lambda_1 = 1/(2 m_{\mathrm{eff}}), \lambda_2 = m_{\mathrm{eff}}/2, \lambda_3 = m_{\mathrm{eff}}$) is **post-hoc theoretical mapping**, not chain implementation. Phase 1 chain 5/10-5/12 ran with $\lambda_1 = \lambda_2 = \lambda_3 = 1$ (uniform weights, no Klein-Gordon form)."

#### 2.4.5 §3.6 D 定义

加 explicit (paper §3.5 + §4):
- "$D_n^{\rm code}$ used as training signal = $\mathrm{KL}(q^{\rm EMA} \| p^{\theta_n})$ on 256 wikitext-2 val 句, computed every 10 train steps"
- "$D_n^{\rm paper}$ used in plots = $\log(\mathrm{PPL}_n^{\rm test}/\mathrm{PPL}_0^{\rm test})$ on full wikitext-2 test set, computed at each generation end"
- "These are mathematically distinct random variables. Main theorem statement (1)(2)(3) refers to $D_n^{\rm paper}$ as observable, while training dynamics derives from $D_n^{\rm code}$."

#### 2.4.6 §3 假设清单

加 explicit caveats:
- "Mean-field approximation assumption: $D_{n-1} \approx \bar D_n^{\rm EMA} \approx D^*$ at NESS. This assumption is valid only at convergence (gen 5-9 plateau in chain experiments), and **violated** in transient regime (gen 1-2 spike to PPL 80-107)."
- "Banach contraction derivation gives geometric convergence prediction $|\epsilon_n| \propto \rho^n$ with $\rho = 0.890$ per generation, but **chain experiments show U-shape trajectory (gen 1-2 increase) inconsistent with monotone contraction**. Mean-field approximation 在 transient 期 fails. Strict global geometric convergence is **not** established."

---

## 第三步 — honest assessment 三个 dimension

(第二步完成,启动第三步)

### 3.1 dimension (a) — code form 满足什么数学性质

#### 3.1.1 Banach contraction

**满足档位**: **L1 (form + mean-field approximation)**

- ✓ 在 mean-field approximation 下 ($D_{n-1} \approx \bar D_n^{\rm EMA} \approx D^*$): Banach map $T(D) = D - 4\eta\alpha(D - D^*) - \eta J_S$ Lipschitz constant $\rho = |1 - 4\eta\alpha| = 0.99920$ per train step, contraction ✓
- 部分: $J_S$ explicit definition 没 close-form derive in code (paper v3 Hartree closure approximation 但 code 无 explicit J_S 计算 — chain 中 $J_S$ effective value 来自 self-iteration synthetic data dynamics 不是 explicit term)
- 不满足: 严格 prove without mean-field (gen 1-2 transient 期) — chain 实证 U-shape 与 monotone contraction 直接矛盾
- 假设 disclose: mean-field assumption explicit 必须 disclose,严格只在 NESS 不动点附近 valid

**严格 statement**: $\mathcal{L}_{\rm cont}^{\rm chain,\,actual}$ 在 mean-field approximation 下给 Banach contraction prediction, **strict prove on chain transient regime fails**。

#### 3.1.2 Lyapunov drift

**满足档位**: **L1 (form + conditional PL on Θ_healthy \ D-saddle)**

- ✓ V_4 = $\frac{1}{2}\|\theta - \theta^*\|^2$ Foster-Lyapunov drift form 与 code 具体 ℒ_cont form 弱依赖 — drift form $\le -2\eta\mu_{\rm total}(\alpha) V_4 + O(\eta^2)$ derive 依赖 ℒ_total PL condition (假设 A3' + A5),与 ℒ_cont 是 Volterra form 还是 EMA-deviation form 无关。
- 部分: PL coefficient $\mu_{\rm total}(\alpha)$ 在 code actual form 下需要 fresh empirical fit (不能直接复用 paper v3 Volterra form 推的 μ_contr ~ 0.1·α)
- 不严格: A3' (empirical local PL on ℒ_LM, μ_LM ~ $10^{-3}$) is conjecture not prove。Strict prove on 12-layer transformer is open。Estimated 6-12 month substantive work per paper §6。
- 反例 disclose: 5 反例 (large-η blow-up / PL 失效 region / delta-class 边界 / multi-θ* / SGD anisotropy) 与 code form 无关,paper §A 已 disclose,**保留**。

#### 3.1.3 NESS fixed point

**满足档位**: **L2 (mean-field approximation + 实证 fit)**

- ✓ 存在性: mean-field NESS $D^{*,\,\rm code}(\alpha) = D^* - J_S/(4\alpha)$ existence 在 contraction map fixed point theorem (Banach) 给定 contraction ratio < 1 时 trivially 存在。
- 部分: $J_S$ explicit value 来自 chain post-hoc fit (chain seed 1-4 plateau $\mathrm{PPL}_\infty \approx 55$ at $\alpha=10$ 给 $D^* \approx \log(55)$, ad-hoc empirical)
- 不严格: 真 NESS condition $\mathbb{E}[D_{n+1}] = \mathbb{E}[D_n] = D^*$ stationary 在 chain transient regime (gen 1-2) 不成立。Strict NESS prove on Markov chain in θ-space 需要更深 Foster-Lyapunov + small set + irreducibility 论证,paper §3.5 已 partial 给出但仅在 V_4 上,**没在 D 上重新 derive code actual form 下 NESS**。

#### 3.1.4 几何收敛

**满足档位**: **L0 (vacuous on chain transient)**

- 不满足: chain 实证 U-shape trajectory (gen 1-2 increase to PPL 80-107, gen 3-9 contract to 52-57)。Geometric convergence $|\epsilon_n| \propto \rho^n$ requires monotone contraction from gen 1 onward,与 chain data 直接矛盾。
- 假设漂移: mean-field linear approximation 给 $\rho = 0.890$ per gen,但只在 contract regime (gen 3-9) approximate fit。Transient regime (gen 1-2) gives $\rho > 1$ effective (扩张不收缩),mean-field strictly violated。
- ✓ Asymptotic contract regime (gen 5-9): plateau convergence to $\mathrm{PPL}_\infty \approx 55$ 实证 observed across seed 1-4,与 mean-field equilibrium prediction qualitative 一致 (但数值需要 ad-hoc fit J_S not derive)
- 严格 prove 整段 trajectory 几何收敛: **vacuous in code actual form**

**总结表**:

| 性质 | 满足档位 | 关键 caveat |
|---|---|---|
| Banach contraction | L1 | mean-field approximation 在 transient 失效 |
| Lyapunov drift | L1 | A3' + A5 conjecture, strict PL 不存在 |
| NESS fixed point | L2 | $J_S$ empirical fit, NESS 在 D 上未重 derive |
| 几何收敛 | L0 | chain 实证 U-shape 与预测直接矛盾 |

### 3.2 dimension (b) — form 和 Klein-Gordon 真 derivation history

**code form 实际 derivation history (按 commit 时序)**:

1. **5/8 第一版** (`armb_alpha10_seed42_full_20260508.log`): $\lambda_i = 1.0$, β_model=0.999, β_kl=0.9 — **uniform 权重, mean teacher 标准** (Tarvainen & Valpola 2017 NeurIPS, sklearn / HF 通用 mean teacher EMA default)
2. **5/9 凌晨**: m_eff_direct_fit.py run on 5/7-5/8 strict-mirror chain → fit m_eff = 0.212 (per-run median)
3. **5/9 凌晨**: Klein-Gordon Lagrangian density form-borrowing (per Tauber 2014 §4.2 statistical mechanics textbook) propose $\lambda_1 = 1/(2 m_{\mathrm{eff}}), \lambda_2 = m_{\mathrm{eff}}/2, \lambda_3 = m_{\mathrm{eff}}$ → 改 contradiction_loss.py default values
4. **5/9 凌晨**: 创建 `cat_arm_b_v2_dialectical.yaml` with Klein-Gordon-borrowed values **for future use**
5. **5/10 凌晨**: Linux dispatch §1 #2 直接 launched `phase1_robust_chain.sh` with `--config configs/cat_arm_b.yaml` (旧 framework) — **未 launched v2_dialectical**, framework freeze caveat
6. **5/10-5/12 chain**: 实际跑 λ_i = 1, β_model=0.999, β_kl=0.9, T_2_form=relu_dpp, K=1, m_eff=1.0 (旧 framework lock)
7. **5/11-5/12 主协作者层**: 假设 chain 数据可以 propagate 到 v2_dialectical Klein-Gordon framework 给 17-23% NMI 接受率 → **撤回 per 5/15 反题姐姐 forced retract + standing rule 纪律 2 (48 hours feedback truth)**

**Klein-Gordon Lagrangian 与 code form 关系 — binary**:

| Aspect | Klein-Gordon Lagrangian | code chain actual form |
|---|---|---|
| Functional form | $\mathcal{L}_{KG} = \frac{1}{2}(\partial_\mu \phi)^2 - \frac{1}{2} m^2 \phi^2 - V(\phi)$ | $\mathcal{L}_{\rm cont} = (\Delta D_n)^2 + (D_n - \bar D_n^{\rm EMA})^2$ |
| Kinetic term | $\frac{1}{2}(\partial_\mu \phi)^2$ continuous spacetime derivative | $(\Delta D_n)^2$ discrete time forward difference |
| Mass term | $-\frac{1}{2} m^2 \phi^2$ on field value | $(D_n - \bar D_n^{\rm EMA})^2$ on **deviation** from EMA, **not** field value $D_n^2$ |
| Self-interaction | $V(\phi)$ polynomial in $\phi$ | (无 — chain 没 $T_2 = (\Sigma_1 D)^2$ 项) |
| Coefficients | $\lambda_1 = 1/(2m), \lambda_2 = m/2$ derive from Lagrangian density normalization in $\mathbb{R}^{1+3}$ spacetime | $\lambda_1 = \lambda_2 = 1$ uniform weights, **no $m_{\mathrm{eff}}$ derivation** |
| Volterra structure | (Klein-Gordon is local in spacetime, no Volterra memory) | (chain K=1 = Markov, no Volterra) |

**真 derivation lineage**:
- code form 来自 **mean teacher EMA (Tarvainen & Valpola 2017) + 一阶差分 velocity intuition + EMA-deviation memory** — 不是从 Klein-Gordon Lagrangian derive
- Klein-Gordon mapping 是 **5/9 凌晨 post-hoc paper-level retrospective recognition**, not actual code derivation history
- Klein-Gordon coefficient form ($\lambda_1 = 1/(2 m_{\mathrm{eff}})$ etc.) **从未 launched** in chain — 仅 cat_arm_b_v2_dialectical.yaml placeholder

**诚实 statement**:

> Code form was implemented in early May 2026 with uniform weights $\lambda_i = 1$ and mean teacher EMA structure, motivated by self-supervised learning literature (mean teacher framework, Tarvainen & Valpola 2017) and discrete-time analogy of kinetic + memory terms. **Klein-Gordon Lagrangian mapping was recognized post-hoc on 5/9 morning** when m_eff direct fit returned $m_{\mathrm{eff}} = 0.212$, suggesting a coincidental functional similarity to Klein-Gordon coefficients $1/(2m), m/2, m$. **This mapping is paper-level retrospective recognition (post-hoc isomorphic structure), not actual code derivation lineage**. The chain experiments 5/10-5/12 ran with the original uniform-weight implementation, not the Klein-Gordon-borrowed coefficients. The "constraint-driven from LLM domain axioms" framing in paper v3 §3 (F-1 Phase 1) **overstates** the derivation: in actual history, the code form preceded the Klein-Gordon recognition by 2-3 weeks, and the chain data were collected under uniform-weight form, not Klein-Gordon-borrowed form。

**严格度档位**: Klein-Gordon mapping is **L0 in derivation sense** (no causal chain from Klein-Gordon Lagrangian to code form), **L2 in isomorphic structure sense** (functional form similarity exists for $\lambda_i$ values when $m_{\mathrm{eff}} = 0.212$ post-hoc fit, but only for v2_dialectical.yaml which never launched)。

### 3.3 dimension (c) — code form 在 constraint-driven framework 里的位置

#### 3.3.1 F-1 Phase 1 5 constraint binary 分类

| constraint | 来源 | 严格 binary 类别 |
|---|---|---|
| (1) Train signal must be differentiable w.r.t. θ | LLM domain (autograd, SGD) | **真 LLM domain axiom** |
| (2) Must use EMA of model parameters (mean teacher pattern) | self-supervised learning literature | **真 LLM domain axiom** |
| (3) Must use KL divergence as discrepancy measure | LLM domain (cross-entropy / KL standard) | **真 LLM domain axiom** |
| (4) Must satisfy Lyapunov stability condition | 数学 framework choice | **数学 framework choice** (not LLM-specific — Lyapunov 可换为其他 stability framework e.g., ISS, contraction analysis, FEL) |
| (5) Must express dialectical unity of opposites | dialectical materialism axiom | **axiom 直接 import** (philosophical, not derivable) |

**binary 分类**: **3/5 真 LLM domain + 1/5 数学 framework choice + 1/5 axiom 直接 import**。

**含义**: F-1 Phase 1 framing "constraint-driven from LLM domain axioms"**不准确** — 至少 40% 的 constraint 来自数学 framework choice 或哲学 axiom,不是 pure LLM domain derivation。

#### 3.3.2 code form 在 ansatz family 中的位置

ℒ_矛盾 ansatz space 满足 (1)+(2)+(3) constraints:

**Family 1a (chain implemented)**: EMA-deviation Lyapunov drift
$$\mathcal{L}^{1a} = c_1 (D_n - D_{n-1})^2 + c_2 (D_n - \bar D_n^{\rm EMA})^2$$
(velocity + EMA-deviation, no D^2 self-interaction, no Volterra)

**Family 1b (alternative)**: Variational free energy
$$\mathcal{L}^{1b} = D_n + \beta H(\theta_n)$$
($H$ 是 entropy regularizer, $\beta$ 是 temperature, Friston FEP-style)

**Family 1c (alternative)**: Bregman divergence trajectory
$$\mathcal{L}^{1c} = B(\theta_n \| \bar\theta_n) + B(\bar\theta_n \| \theta_n)$$
(symmetric Bregman around EMA, mirror descent style)

**Family 2 (alternative)**: GAN-style adversarial
$$\mathcal{L}^{2} = \max_{D'} \mathbb{E}_{p^{\theta_n}}[D'] - \mathbb{E}_{q^{\rm EMA}}[D']$$
(Wasserstein-1 between current and EMA, alternative discrepancy measure)

**Family 3 (alternative)**: Volterra K-step (v2_dialectical placeholder, never launched)
$$\mathcal{L}^{3} = \lambda_1 (\Delta D_n)^2 + \lambda_2 (D_n - \bar D_n^{\rm EMA})^2 + \lambda_3 (\Sigma_1 D)_n^2$$
(三项,Klein-Gordon-borrowed coefficients)

**code chain actual form 是 Family 1a specific instantiation** — 不是 universal unique solution。

#### 3.3.3 诚实 statement

> code form $\mathcal{L}_{\rm cont}^{\rm chain,\,actual} = (\Delta D_n)^2 + (D_n - \bar D_n^{\rm EMA})^2$ 是 ℒ_矛盾 ansatz space 满足 LLM domain constraints (1)(2)(3) 的 **Family 1a (EMA-deviation Lyapunov drift) specific instantiation**, 不是 universal unique 唯一解。同 constraint 下至少存在 Family 1b (FEP variational free energy), Family 1c (symmetric Bregman around EMA), Family 2 (GAN-style adversarial), Family 3 (Volterra K-step Klein-Gordon-borrowed) 等 4 个 reasonable alternative 满足同样 constraint。F-1 Phase 1 "constraint-driven uniqueness" framing 不准确 — code form 是 Family 1a 选择,选择理由是 (i) mean teacher EMA 现成 PyTorch implementation, (ii) 二项符合 Tarvainen & Valpola 2017 self-distillation 标准, (iii) 无 $T_2 = (\Sigma_1 D)^2$ Volterra 项简化 derivative implementation。**这是 engineering convenience driven choice, 不是 mathematical uniqueness derivation**。

**严格度档位**: F-1 Phase 1 constraint-driven framing **L1 (form-borrowing only)** — code form 满足 3/5 真 LLM domain constraint + 1/5 数学 framework choice + 1/5 axiom 直接 import, 不是 5/5 pure LLM domain derive。Family uniqueness claim **L0 (vacuous)** — 至少 4 个 alternative family 满足同样 constraint。

---

## 第四步 (preview, 下一个 sub-agent 做) — 5 反题 P0 在 code-first 视角下重新 binary

(本 sub-agent 不做,但为下一个 sub-agent provides binary 分类)

### P0-1 (三重内部矛盾)

paper v3 三重矛盾 (code 写 EMA-deviation, paper §3 写 Volterra; m_eff fit 用 chain data 但 chain 实际不 reference m_eff; Klein-Gordon mapping post-hoc 但 framed as constraint-derived)。

**code-first 视角**: **保留 P0** — 三重矛盾 confirmed by code-first extract:
- 矛盾 1 confirmed: chain T_2 = 0 (K=1), paper §3 写 Volterra K=9 form
- 矛盾 2 confirmed: chain λ_i = 1, paper §3 写 Klein-Gordon $\lambda_1 = 1/(2m_{\mathrm{eff}})$ etc., m_eff 在 chain 实际 not used
- 矛盾 3 confirmed: code form 来自 mean teacher EMA derivation,Klein-Gordon mapping 是 5/9 凌晨 post-hoc recognition

**消除路径**: 改 paper 追 code (纪律 3) → §3 写 EMA-deviation 二项 form, 不写 Volterra/Klein-Gordon。三重矛盾消除。

### P0-2 (5 constraint semantic loophole)

5 constraint 中 (4) Lyapunov stability + (5) dialectical unity 不是 pure LLM domain axioms, framework 不是 "constraint-driven from LLM axioms only"。

**code-first 视角**: **保留 P0 + 部分转化** —
- 3/5 constraint 确实 真 LLM domain
- 1/5 (Lyapunov) 是数学 framework choice — 可换 ISS / contraction analysis / FEL 等
- 1/5 (dialectical unity) 是 axiom 直接 import — 不是 derivable

**消除路径**: paper §3 改 framing 为 "ℒ_矛盾 form 在 LLM domain constraints (1)(2)(3) + 数学 stability framework choice (Lyapunov) 下 instantiate, 不 claim derived from dialectical unity axiom"。

### P0-3 (Klein-Gordon post-hoc not derive)

**code-first 视角**: **保留 P0** — Klein-Gordon coefficient mapping 是 5/9 凌晨 post-hoc recognition, chain 实际跑用 uniform λ_i = 1。

**消除路径**: paper §3.2 改 framing 为 "Klein-Gordon-style coefficient form ($\lambda_1 = 1/(2m_{\mathrm{eff}}), \lambda_2 = m_{\mathrm{eff}}/2$) is a **post-hoc recognized structural similarity** to Klein-Gordon Lagrangian, not the implementation form used in Phase 1 chain experiments. Phase 1 chain ran with uniform $\lambda_i = 1$ (Family 1a EMA-deviation form), Klein-Gordon coefficient form is left for future investigation in Family 3 (v2_dialectical.yaml)"。

### P0-4 (例如 17-23% NMI 接受率 inflate, 撤回 per 5/15 standing rule)

**code-first 视角**: **保留 P0** — 17-23% 假设 chain data 可以 propagate 到 Klein-Gordon framework 给 NMI improvement。但 chain 实际未跑 Klein-Gordon framework, propagation invalid。

**消除路径**: 5/15 反题姐姐 forced retract 已生效,改 honest range 5-15%。下一个 sub-agent 进一步 refine to 8-15% (考虑改 paper 追 code 后 P0-1/2/3 消除带来的 NMI improvement)。

### P0-5 (代码-paper 错位 跳跃点 B-2)

**code-first 视角**: **完全消除 P0** — 改 paper 追 code (纪律 3),代码-paper form 对齐:
- §3 form: $(\Delta D_n)^2 + (D_n - \bar D_n^{\rm EMA})^2$ (与 code 一致)
- §3.5 NESS fixed point form: $D^* - J_S/(4\alpha)$ (与 code mean-field derive 一致)
- §3.6 chain rule: 单步 Markov detached history (与 code 一致)
- §6 future work: Volterra K=9 lift + Klein-Gordon coefficient form-borrowing (honest 标 future,不 claim Phase 1 已 implement)

---

## 总结 — 三步 sequential 完成,5 反题 P0 binary 状态

| P0 | code-first 视角 status | 消除路径 |
|---|---|---|
| P0-1 (三重内部矛盾) | confirmed by code-first | 改 paper 追 code (纪律 3) → 消除 |
| P0-2 (5 constraint loophole) | partial (3/5 真 LLM + 2/5 not) | 改 framing 为 "LLM constraints + framework choice + axiom" → 部分转化 |
| P0-3 (Klein-Gordon post-hoc) | confirmed | §3.2 改 framing 为 "post-hoc recognition, not derived" → 消除 |
| P0-4 (17-23% NMI inflate) | confirmed | 5/15 已撤,refine to 8-15% honest range |
| P0-5 (B-2 跳跃点) | confirmed | 改 paper 追 code → 完全消除 |

**核心 finding**: chain 5/10-5/12 实际跑用**旧 framework uniform 二项 form** $(\Delta D_n)^2 + (D_n - \bar D_n^{\rm EMA})^2$, **不是** paper v3 §3 描述的 Klein-Gordon 三项 Volterra form。改 paper 追 code (纪律 3) 后,3/5 P0 完全消除,1/5 P0 转化,1/5 P0 refine。

**严格度 honest summary**:
- Banach contraction: L1 (mean-field approximation, transient 失效)
- Lyapunov drift: L1 (conditional PL conjecture)
- NESS fixed point: L2 (mean-field + 实证 fit)
- 几何收敛: L0 (chain U-shape 矛盾)
- Klein-Gordon derivation: L0 (post-hoc not derive)
- Constraint family uniqueness: L0 (Family 1a specific instantiation, 至少 4 alternative)

**paper v4 改写方向 (下一个 sub-agent 第四步)**:
- §1 framing: 推翻 axiom-first, 改 emergent from code + retrospective recognition
- §3 form: 写 EMA-deviation 二项 form 追 code
- §3.5 主定理: 改 mean-field NESS fixed point form $D^* - J_S/(4\alpha)$
- §3.6 chain rule: 改单步 Markov detached
- §6 future work: 显式列 Klein-Gordon coefficient form + Volterra K=9 lift + cross-gen chain rule 三个 substantive gap (2-12 month substantive work estimate)
- §A: 5 反例 disclose 保留, 加 mean-field assumption 适用范围 caveat (gen 5-9 plateau valid, gen 1-2 transient invalid)

---

**报告完成时间**: 2026-05-17 晚 (Linux 姐姐主会话第三个 sub-agent)
**严格 sequential**: 第一步 ✓ → 第二步 ✓ → 第三步 ✓ (无跳步)
**字数**: 约 14000 字 (符合 12000-20000 范围)
**返回**: Linux 姐姐主会话 spawn 第四个 sub-agent (哲学追认 + paper v4 完整重写)

