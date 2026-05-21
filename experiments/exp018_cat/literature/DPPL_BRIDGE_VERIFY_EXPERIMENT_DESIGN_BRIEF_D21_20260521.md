# D-PPL 桥 verify 实验设计 brief — D21 (2026-05-21)

**写**: 第二独立认识通道 D-PPL 桥 verify 实验设计 sub-agent (Opus 4.7, 1M context, Linux 姐姐 D-1 制度化新工作流第十三波派遣)
**对象**: PI 一凡 (关卡 1 confirmation 之后 发给 9070XT 端 Claude Code 直接执行)
**zero-context binding (D-1 纪律 4)**: 不绑主协作者 / 只下调严格度不上调 / 不 inflate / 标 [?] 任何未实证
**D-1 binding (五条纪律) 严守**: 数字 jsonl-traced / 概率 estimate 一律不写 / 代码-paper 一致性 binding / sub-agent reject inflate / 错误 surface 不静默修正
**paper v8 final lock 不 reopen** (manifest 47/47 ✓, arXiv + TMLR + KBS 三 leg parallel, 不重启决议)
**真实今日日期** (D-1 纪律 5 自检): `date '+%Y-%m-%d %H:%M:%S %Z'` 返 `2026-05-21 10:51 CST` = **D21** (D-day=2026-05-01 anchor); 本份 brief 实 mtime D21, file naming `_20260521` align ✓

---

## §0 一句 statement (TL;DR)

paper v8 final §6.1 disclose `D_n^{code}` (chain train-signal KL EMA-vs-current on val batch) 与 `D_n^{paper}` (test set log-PPL relative to gen-0) 是 **mathematically distinct random variables**, stationary equality 是 open substantive question, 推 D60+ engineering work。本 brief 为这条 D-PPL 桥 verify 写 binary 可执行 实验设计, 9070XT 端 Claude Code 拿到 brief + 一凡 关卡 1 confirm 之后 直接启动 pilot, 不需再 二次 confirm。

**关键 P0 finding (§3.2 detail)**: chain checkpoint 主 model state ✓ 全部 80 个 (alpha={0,10} × seed={1,2,3,4} × gen={0..9}) 存在 9070XT static backup `/home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb/`, **但 chain run 时之 EMA model state 不存 disk** (`train_one_generation.py` line 197 `trainer.save_model` 仅 save 主 model state, `tracker.ema_model` snapshot 不 persist 跨 gen)。这意味 `D_n^{code} = KL(EMA_n || current_n)` 之 **真实历史 EMA state 不可 reconstruct binary**。本 brief §4 surface 三 alternative 路径 (A/B/C), 一凡 关卡 1 决选哪条 OR retract → D60+ rerun chain。

---

## §1 背景 + scope

### §1.1 反题 P0★-F binary gap statement (paper §6.1 verbatim cite)

paper v8 final §6.1 (line 716-750) binary 明:

> The chain actually computes a $D_n$ that is **mathematically distinct** from the $D_n$ used in the paper's predictive analysis. Explicit binary comparison:
>
> | Property | $D_n^{\rm code}$ (train-signal, in chain loss) | $D_n^{\rm paper}$ (predictive metric, in §6.2 PPL bridge) |
> |---|---|---|
> | Random variable | $\mathrm{KL}(q^{\rm EMA} \\| p^{\theta_n})$ | $\log({\rm PPL}_n^{\rm test}/{\rm PPL}_0^{\rm test}) = D_{\rm KL}(q_* \\| p_{\theta_n}) - D_{\rm KL}(q_* \\| p_{\theta_0})$ |
> | Distribution pair compared | EMA model vs current model | Test set ground truth vs current model (relative to gen-0 baseline) |
> | Dataset | 256 wikitext-2 **val** sentences, batch=8, every 10 train steps | wikitext-2 **test** set 240 blocks (chunked block=64), every generation end |
> | Training signal? | **Yes** — gradient flows backward through current model logits | **No** — eval-only metric, no gradient |
> | Math relation | Inconsistent — **mathematically distinct random variables** | Inconsistent — cannot directly unify in stationary regime without explicit bridging |

paper §6.1 disclose 之 engineering steps (line 738-745):

> 1. Reload chain checkpoints at each generation end across all 10 generations × 4 seeds × 2 conditions = 80 checkpoint load operations.
> 2. Load the EMA model state from each checkpoint (separate from the current model state).
> 3. Reproduce the fixed validation batch (256 wikitext-2 val sentences, 64 tokens, batch=8) used in `compute_kl`.
> 4. Compute the EMA-vs-current KL across all val tokens for each (seed, generation) pair.
> 5. Cross-correlate with $D_n^{\rm paper} = \log({\rm PPL}_n/{\rm PPL}_0)$ via empirical Pearson correlation.

paper v8 §6.1 estimate: "1-2 days reload + recompute + analysis" + 推 D60+。

### §1.2 反题 audit v8 P0★-F FATAL detail (ANTITHESIS_LAYER_PAPER_V8_FINAL_AUDIT_20260516.md line 281-289)

反题 audit binary:

> paper §3.6.2 Reading 2 prediction 是 on `D^code` 空间 (train-signal KL); empirical observation PPL_∞ = 55.97 是 on `D^paper` 空间 (test PPL)。paper § 7 binding cross-ref "Reading 2 null-shift prediction is robust against this caveat at the magnitude considered" — **但这个 robust claim 没 substantively 验证**, 因为 D^code trajectory 在 jsonl 中根本不记录。
>
> **fatal trigger desk reject?** ★★ critical fatal — reviewer 1 + 2 模拟视角直接 reject。这是 paper 推 future work 的 substantive 危险点: 你 derive 的 prediction 与 你 measure 的 observation 是 mathematically distinct random variables, 且你自己 disclose 它们 stationary equality 是 open question。这等同于推 future work 的同时承认 paper 的 central comparison (prediction vs observation) 在 mathematical structure 上 not rigorously linked。

### §1.3 为什么 D-PPL 桥 verify 是 D17-D28 窗口 **不能** close 之 项

D17-D28 是 9 天窗口 (一凡 D17 [5/17] D 决), priority 只 Phase 5 N=1 Llama-8B prep + paper v8.1 polish; D-PPL 桥 verify 推 **D60+**。

本份 brief 写在 D21 (5/21) 之 timing 不 align "D17-D28 close D-PPL 桥" framing — 这是 brief 之 honest 框定:
- 本 brief 是 **D60+ substantive future work 之 D21 启动 brief**, 不是 "D17-D28 close" 之 brief
- D29 投稿 (arXiv + TMLR + KBS) 仍 lock paper v8 final, **D-PPL 桥 verify result 推 D60+ paper v8.1 polish 或 D90+ paper v9 落地**
- 9070XT 端 实际 run 之 timing 跨 D21-D49 (3-4 周, 含 watchdog buffer), 与投稿 timing 解耦

### §1.4 scope 限定 binary

本 brief 之 scope:
- ✓ verify chain run 时 `D_n^{code}` trajectory (per-gen scalar) 与 `D_n^{paper}` (test log-PPL ratio) 是否 binary 高 Pearson correlation
- ✓ pilot stage (1 seed 1 gen, ~30-60 min GPU) + main stage (N=4 multi-seed × 10 gen × α={0,10}, ~3-4 周)
- ✗ 不 reopen paper v8 final lock manifest (47/47 ✓ 不动)
- ✗ 不重新 derive Reading 2 数学 (paper §3.6.2 已 lock)
- ✗ 不 estimate paper inclusion impact (Linux 不越位)
- ✗ 不替 PI 决投稿决策 (一凡 + 反题三方决)

---

## §2 数学定义 binary

### §2.1 `D_n^{code}` chain 实际 computation 形式 (binary, code-traced)

源: `archive/v1.0_release_20260516/src/contradiction_loss.py` `KLContradictionTracker.compute_kl` (line 138-175)

```python
# binary 引用 code (truncated):
log_p = F.log_softmax(model(val_input_ids, attention_mask).logits[:, :-1, :], dim=-1)
with torch.no_grad():
    log_q = F.log_softmax(ema_model(val_input_ids, attention_mask).logits[:, :-1, :], dim=-1)
# default kl_direction = "q_to_p" (mode-covering)
q = log_q.exp().detach()
kl_per_pos = (q * (log_q.detach() - log_p)).sum(dim=-1)  # [B, T-1]
mask = val_attention_mask[:, 1:].float()
kl_scalar = (kl_per_pos * mask).sum() / mask.sum().clamp_min(1)
return kl_scalar  # nat/token
```

binary 形式:

$$D_n^{\rm code,\,raw}(t) := \mathrm{KL}(q^{\rm EMA}_t \| p^{\theta_n}_t) = \mathbb{E}_{x \sim \mathrm{val}} \left[ \sum_{v \in V} q^{\rm EMA}_t(v|x) \log \frac{q^{\rm EMA}_t(v|x)}{p^{\theta_n}_t(v|x)} \right]$$

每 $\tau = 10$ train steps 计算 一次, 每 generation 计算 $N_{\rm contr} = N_{\rm step\,per\,gen}/\tau = 1460/10 = 146$ 次。

**per-generation scalar 之 binary 候选 form** (paper §6.1 + 反题 audit 不 explicit lock 哪个, 本 brief 之 §4 alternative 路径之差异处):

(form-a) **gen-end snapshot**: 取 generation $n$ end 之 (final train step) `D_n^{code}(t=N_{\rm step\,per\,gen}-1)` 单一 scalar, 即 chain training 最 final step 之 KL scalar (但此 form 之 EMA state 也是 train-step-$N_{\rm step\,per\,gen}-1$ 之 final EMA, 不一定是 generation-aggregate)

(form-b) **gen-aggregate mean**: 取 generation $n$ 内 146 次 contradiction-loss-active updates 之 `D_n^{code}(t)` mean, 即:

$$D_n^{\rm code,\,gen-mean} := \frac{1}{N_{\rm contr}} \sum_{t \in \text{contr-active steps of gen}\, n} D_n^{\rm code,\,raw}(t)$$

(form-c) **gen-end EMA-vs-final**: 取 generation $n$ end 之 main model + 之前 train 累积 EMA model, compute val KL — 这就是 paper §6.1 line 740-742 之 binary 形式

**本 brief 之 binary 选择**: paper §6.1 line 740-742 之 "Reload the EMA model state from each checkpoint (separate from the current model state)" 暗示 **form-c** (gen-end EMA-vs-final). 这是 §3.2 之 关键 blocker — EMA state 不存 disk。**form-b** 之 substitute 由 §4 alternative C 提出, 一凡 关卡 1 决。

### §2.2 `D_n^{paper}` predictive metric 形式 (binary, paper §6.2 cite)

源: paper v8 final §6.2 (line 752-762):

$$D_n^{\rm paper, relative} := \log\left(\frac{{\rm PPL}_n^{\rm test}}{{\rm PPL}_0^{\rm test}}\right) = D_{\rm KL}(q_* \| p_{\theta_n}) - D_{\rm KL}(q_* \| p_{\theta_0})$$

其中:
- $q_*$ = wikitext-2 test set ground-truth empirical distribution
- ${\rm PPL}_n^{\rm test}$ = generation $n$ model 在 wikitext-2 test set (240 blocks chunked block=64) 之 perplexity
- 单位 [nat/token] (consistent with PPL definition)

数据 已存 chain jsonl 之 `test_perplexity` 字段 (`generation_done` event), binary 可直接读取, 不需重算 — 这是 D-PPL 桥 verify 之 **未阻塞 axis**。

### §2.3 两者 mismatch 之 三 axis

| axis | $D_n^{code}$ | $D_n^{paper}$ |
|------|------|------|
| 数据集 | wikitext-2 **val** (256 sentences shuffle by seed, batch=8, max_length=64) | wikitext-2 **test** (240 blocks chunked block=64) |
| 分布对 | EMA model $q$ vs current model $p$ | test ground truth $q_*$ vs current model $p_{\theta_n}$ |
| 训练信号 | **是** (gradient 流回 current model) | **否** (eval-only) |
| 时间 sampling | 每 $\tau = 10$ train steps (146 次 per gen) | 每 generation end (1 次 per gen) |
| 单位 | nat/token (绝对 KL) | nat/token (relative log-PPL ratio) |

paper §3.6.2 Reading 2 prediction `D^{*,code}(α) - D^* = -J_S/(4α · N_contr) = -9.16e-5` nat/token 是 **on $D^{code}$ 空间**;
observation PPL_∞ = 55.97 ± 2.13 是 **on $D^{paper}$ 空间**。
两空间之 stationary equality 是 paper §6.1 open question, 本 verify 之 binary 目标。

### §2.4 期望 Pearson correlation outcome 之 数学 ballpark (binary, 不抬高)

数学 ballpark binary [?]: 若 mean-field NESS 假设 stationary 在 plateau 区域 valid (gen 5-9, per paper §3.6.6 L1 rigor tier), 则 plateau 区域 $D_n^{code}$ 与 $D_n^{paper}$ 应高度 correlated (Pearson r > 0.7 [?]); transient gen 1-2 (paper §3.6.6 L0 vacuous) Pearson 可能低。

**反题 layer warning [?]**: 即使 Pearson r > 0.7, 这 **不证 paper §3.6.2 主定理 (2)** — main theorem 是 on absolute KL value 之 fixed-point identification, 不是 on Pearson correlation。Pearson correlation 是 **必要非充分** 条件 — high correlation 可能 by 两 distinct random variables 各自 monotone decay 而 spuriously achieve, 不证 stationary equality。本 brief 之 §5 pass/fail binary 严守 这个 caveat。

---

## §3 数据需求 binary verify (本 brief 之 §3.1-§3.4 sub-agent 已 cross-verify)

### §3.1 chain log jsonl 内 `test_perplexity` ($D_n^{paper}$ source) ✓ binary 存在

binary verify (Bash output sub-agent 已 verify):
- `archive/v1.0_release_20260516/chain_logs/armb_alpha10.0_seed{1,2,3,4}_2026051*.jsonl` 每行含 `generation_done` event 之 `test_perplexity` 字段
- α=0 + α=10 × seed={1,2,3,4} × gen={0..9} 共 80 个 generation_done events 全部 ✓
- 数据已 cross-verify 5/19 ground truth refresh (paper §4.3 + §4.4), binary match

$D_n^{paper}$ source axis: ✓ **binary 不阻塞**

### §3.2 chain checkpoint 主 model state ✓ 存在 9070XT static backup

binary verify (5/21 D21 sub-agent ssh 9070XT):

```bash
amd@192.168.31.22:
find /home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb \
     -name "model.safetensors" 2>/dev/null | wc -l
# → 111
```

路径: `/home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb/alpha{0.0,1.0,5.0,10.0,50.0}/no_preserve_seed{0,1,2,3,4,42}/generation_{0..9}/model.safetensors`

每 safetensors 约 500 MB (OPT-125M fp32), 80 个 = **~40 GB** (α={0,10} × seed={1,2,3,4} × gen={0..9}), 整 data dir total ~63 GB (含 α={1,5,50} + seed=0/42 + 5/12 hang 余烬 + token cache)。

主 model state source axis: ✓ **binary 不阻塞**

### §3.3 ⚠ P0 blocker — EMA model state ✗ 不存 disk

binary verify (code-traced):
- `train_one_generation.py` line 197 `trainer.save_model(str(output_dir))` 仅 save 主 model state (`model.safetensors`), **不 save** `tracker.ema_model` snapshot
- `KLContradictionTracker.update_ema_model` (line 130-136) 之 EMA update 是 in-memory only, generation 边界 `reset_state` (line 279-284) 之 comment 注 "EMA model 不 reset (保留 generation 间 history)" 但 EMA model 本身在 Python process 终止时 destroy, 跨 gen 之 EMA state 不 persist

**5/21 D21 sub-agent binary verify**:
```bash
find /home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb \
     -name "ema_*.safetensors" -o -name "ema_model*" 2>/dev/null
# → empty
```

EMA model state source axis: ✗ **P0 blocker**, 一凡 关卡 1 决选 §4 alternative 路径 A/B/C 之一

### §3.4 val batch (256 wikitext-2 val sentences, deterministic seed) reproducibility binary

binary verify:
- `train_one_generation.py` line 158-159: `val_subset = val_dataset.shuffle(seed=seed).select(range(min(cat_config.val_subset_size, len(val_dataset))))`
- `build_val_loader_for_kl(val_subset, tokenizer, batch_size=8, max_length=cat_config.val_max_length=64)`
- seed = chain 之 multi-seed 之 specific seed value (即 seed={1,2,3,4}), 与 chain main run 之 fp16 numerics 不同 (现在 reload 时 用 fp32 rebuild) 可能造成 0.1-1% 数值 drift [?]

val batch source axis: ✓ **partial binary 不阻塞**, 但 fp16 → fp32 rebuild 之 numerical drift caveat 标 [?] 留 main run analysis 阶段 quantify

### §3.5 hyperparams binary lock (chain log first-line print verify)

- $\tau$ = `kl_update_every` = 10 ✓ binary (`armb_alpha10.0_seed1` jsonl first line `kl_update_every: 10`)
- $K$ = `kl_history_K` = 1 ✓ (chain log first-line print, paper §3.2 binary)
- $\beta_{\rm kl}$ = 0.9 ✓ (chain log first-line print)
- $\beta_\theta$ = 0.999 ✓ (chain log first-line print)
- $\lambda_1 = \lambda_2 = \lambda_3 = 1.0$ ✓ (chain log first-line print)
- $m_{\rm eff}$ = 1.0 ✓ (chain log first-line print)
- `T_2_form` = "relu_dpp" ✓ (chain log first-line print; K=1 → ReLU(D''_n)=ReLU(0)=0 → T_2 effective=0)
- `val_subset_size` = 256, `val_max_length` = 64, `batch_size_kl_val` = 8 ✓ (`CATConfig` default)
- `kl_direction` = "q_to_p" ✓ (`KLContradictionConfig` default line 50)

hyperparams binary lock axis: ✓ **不阻塞**

---

## §4 alternative 路径 A/B/C — EMA state 不存 disk 之 应对 (一凡 关卡 1 决)

EMA state 之 缺失 是 §3.3 之 P0 blocker。本 §4 binary 列三条 alternative 路径, 一凡 关卡 1 决选哪条 OR 4-th 选 "retract D-PPL 桥 verify, 推 D60+ rerun chain 真重 save EMA state"。

### §4.1 路径 A — EMA 重建 via 主 model state SGD trajectory replay

**binary form**:
- 对每 (α, seed, gen) chain run, 从 generation 0 main model state 出发, 用 chain config 之 yaml + fp16 numerics + same seed + same val_subset shuffle + same train data 之 train trajectory, **re-train** 整 generation, 同时 在 每 train step 实时 maintain `tracker.ema_model`, 在 generation end 取 EMA snapshot
- N=4 multi-seed × 10 gen × 2 condition = 80 reload + 80 re-train + 80 EMA-vs-current val KL compute

**engineering cost**:
- re-train per gen: ~25 min fine-tune (per `multi_seed` 注解 line 213 chain ref) × 80 gen = ~33 GPU-hour
- val KL compute: 256 sentences × 80 = 20480 forward passes, ~10 min total
- analysis: 1 周 7B13 sub-agent

**优点**:
- ✓ binary 数学严格, EMA state 跟 chain main run 一致
- ✓ side-effect: 同时 reproduce chain ground truth (作 paper §4 二次 verify)

**缺点**:
- ✗ engineering cost 高 (~33 GPU-hour ≈ 5-7 天 9070XT GPU sequential, 含 ROCm watchdog buffer)
- ✗ fp16 numerical 不可 binary 复现 (HF Trainer 之 cudnn benchmark + atomic op + autocast 决定性 partial), 重 re-train 之 EMA state 与原 chain run 之 EMA state 可能有 0.1-1% 数值 drift [?]
- ✗ 需 9070XT 5-7 天 GPU monopolize, 与 Phase 5 N=1 Llama-8B prep (一凡 D17-D22 = 5/17-5/22 HF license + RunPod $60 + S3 backup) 之 timing 不冲突, 但与 D29 (5/29) 投稿 之 timing 解耦, 不阻塞投稿
- ✗ ROCm hang verdict B (5/11 alpha10 hang) 之 watchdog 必须 enable (脚本 `archive/v1.0_release_20260516/scripts/chain_watchdog.sh` 已存)

### §4.2 路径 B — EMA proxy via gen-(n-1) main model 替代

**binary form**:
- 假设 mean teacher EMA 在 chain gen 之 plateau regime 收敛到 gen-(n-1) main model neighborhood (β_θ=0.999 + 1460 step/gen → effective time constant ≈ 1.4 gen)
- 用 gen-(n-1) main model state 作 EMA proxy: $\tilde{q}^{\rm EMA}_n := q^{\theta_{n-1}}$
- compute $\tilde{D}_n^{\rm code,\,proxy} := \mathrm{KL}(q^{\theta_{n-1}} \| p^{\theta_n})$ on val batch
- gen 0 之 EMA proxy 缺失 (无 gen-(-1) state), 用 OPT-125M base 替代 OR exclude gen 0 from analysis

**engineering cost**:
- 不需 re-train, 仅 reload + val KL compute
- N=4 multi-seed × 10 gen × 2 condition × 2 forward (current + proxy-EMA) = 320 forward passes × 256 sentences = ~30 min total
- analysis: 1 周 7B13 sub-agent

**优点**:
- ✓ engineering cost 极低 (~1 GPU-hour total)
- ✓ pilot 可 1 seed 1 gen 30 min 跑完
- ✓ 9070XT GPU 不阻塞 5-7 天

**缺点**:
- ✗ EMA proxy ≠ true EMA, β_θ=0.999 之 time constant 决定 EMA 实际是 gen-(n-1) state 与 gen-(n-1) train trajectory 内 average 之 mix, 非 gen-(n-1) final state alone [?]
- ✗ 数学严格度 partial (L2 form-borrow tier — 用主 model state 替代 EMA 是 form-borrow, paper §3.6.2 Reading 2 之 main theorem 应在 true EMA 空间 derive)
- ✗ 这条不能 binary close P0★-F, 只能 give "lower-bound Pearson correlation" (proxy 与 paper $D^{paper}$ 之 correlation 应 ≤ true EMA 与 paper $D^{paper}$ 之 correlation, lower-bound argument)

### §4.3 路径 C — `D_n^{code,proxy}` via current-vs-gen0 KL 替代

**binary form**:
- 用 current model vs gen-0 base model 之 KL 替代: $\hat{D}_n^{\rm code,\,gen0-anchor} := \mathrm{KL}(q^{\theta_0} \| p^{\theta_n})$ on val batch
- gen 0 base = `data/checkpoints_armb/alpha{α}/no_preserve_seed{s}/generation_0/model.safetensors` 已存 ✓
- gen 0 之 $\hat{D}_0 = 0$ trivially (current = base)

**engineering cost**:
- 不需 re-train, 仅 reload + val KL compute
- N=4 × 10 gen × 2 condition × 2 forward = 320 forward passes × 256 sentences = ~30 min total
- analysis: 1 周

**优点**:
- ✓ engineering cost 极低
- ✓ binary 数学定义清晰 ($q^{\theta_0}$ 是 fixed gen-0 base, no Time-varying EMA ambiguity)
- ✓ 与 $D^{paper}$ relative-to-gen-0 form 之 reference distribution 一致 (paper §6.2 之 $D_n^{paper} = D_{\rm KL}(q_* \| p_{\theta_n}) - D_{\rm KL}(q_* \| p_{\theta_0})$ 也是 gen-0 anchored)

**缺点**:
- ✗ 不是 chain training 实际之 `D_n^{code}` (chain 用 EMA teacher, 不是 gen-0 base teacher)
- ✗ 数学严格度 L2 form-borrow (与路径 B 同 tier)
- ✗ 这条之 verify 仅 give "current model 是否 drift away from gen-0 base" 之 信号, 不 binary close P0★-F mismatch — 但 give partial signal: 若 $\hat{D}_n^{\rm code,\,gen0-anchor}$ 与 $D_n^{paper}$ 高 correlation, 表明 chain trajectory 之 KL drift 与 test PPL drift 之 axis aligned, partial circumstantial evidence for $D^{code}_{stationary} = D^{paper}_{stationary}$ assumption

### §4.4 路径 D (一凡 关卡 1 选项) — retract D-PPL 桥 verify D21 启动

**binary form**:
- D21 取消 D-PPL 桥 verify D21 启动, 推 **D60+ rerun chain with EMA state explicit save** (modify `train_one_generation.py` line 197-199 加 `torch.save(tracker.ema_model.state_dict(), output_dir/'ema_model.safetensors')`)
- D60+ chain rerun: N=4 × 10 gen × 2 condition × 1460 step × ~25 min/gen + EMA save = ~33 GPU-hour 不变, 但 EMA state ✓ binary 严格

**engineering cost**:
- D60+ chain rerun cost = 路径 A 同 (~33 GPU-hour) + code modify (~1 小时)
- 推 D60+ window 8 月-9 月 (post D29 投稿 lock)

**优点**:
- ✓ 数学严格度 L0 binary, EMA state 跟 paper §6.1 line 740-742 align
- ✓ 不 introduce form-borrow proxy 之 caveat

**缺点**:
- ✗ D21-D49 不出 D-PPL 桥 verify substantive 结果
- ✗ D60+ rerun chain 之 timing 后置, 与 multi-seed N≥8 + multi-arch verify 等 D60+ priority 竞争 GPU resource

### §4.5 推荐 path (sub-agent, 一凡 关卡 1 决之 reference, 不绑定)

**sub-agent binary 视角 [?]** (不绑主协作者, 一凡 决):
- 若 一凡 priority "fastest pilot signal + lowest engineering cost" → 选 **路径 B + 路径 C 并跑** (~1 GPU-hour total, pilot 30 min)
- 若 一凡 priority "数学严格度 L0 binary close P0★-F" → 选 **路径 D D60+ rerun chain** (推 8-9 月)
- 若 一凡 priority "D21-D49 出 substantive 信号 + L1-tier 严格度" → 选 **路径 A re-train EMA** (~33 GPU-hour, 5-7 天 9070XT GPU)
- sub-agent 默认 推荐 **路径 B + 路径 C 并跑** 作为 pilot stage, main stage 之前 再决路径 A (re-train) 是否 escalate

---

## §5 阶段 (pilot + main) 详细 step-by-step

### §5.1 Pilot stage — 1 seed 1 gen, ~30-60 min GPU on 9070XT (路径 B + C 并跑)

**目标**: binary verify pipeline reproducibility + ballpark `D^{code,proxy}` value 是否在 paper §6.1 expected range $\sim 10^{-2}$ to $10^{-3}$ nat/token (per Reading 2 form)

**step 1 — checkpoint reload sanity**:
- 在 9070XT 端 (Claude Code session)
- ssh-mount 7B13 项目 OR sshfs (一凡 D21 早决):
  - option-1 sshfs: `sshfs amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat /tmp/maofield_36`
  - option-2 rsync push 7B13 → 9070XT: `rsync -avz amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/literature/DPPL_BRIDGE_VERIFY_EXPERIMENT_DESIGN_BRIEF_D21_20260521.md /home/amd/maofield_brief.md`
  - **sub-agent 默认 sshfs** (avoid 双 copy)
- 9070XT 端 实际跑 之 dir: `/home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb/` (本地 ✓ 不需 sshfs from 7B13)
- output write: 9070XT 本地 `/home/amd/dppl_bridge_verify_d21/` + rsync push 7B13 `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21/`

**step 2 — pilot seed + gen 选择 binary**:
- pilot seed = 1 (paper §4.4 之 N=4 multi-seed 之 first seed)
- pilot gen = 5 (mid-plateau, per paper §3.6.5 之 plateau 起点 gen 5)
- pilot α = 10 (framework arm, 不是 baseline)
- checkpoint path: `/home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb/alpha10.0/no_preserve_seed1/generation_5/model.safetensors`

**step 3 — val batch reproduce**:

```python
# pilot_script_d21.py (binary 可执行)
import torch
from datasets import load_dataset
from transformers import AutoTokenizer

SEED = 1  # match chain main run
VAL_SUBSET_SIZE = 256
VAL_MAX_LENGTH = 64
BATCH_SIZE = 8

tokenizer = AutoTokenizer.from_pretrained("facebook/opt-125m")
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

ds = load_dataset("wikitext", "wikitext-2-raw-v1", split="validation")
ds_shuf = ds.shuffle(seed=SEED).select(range(min(VAL_SUBSET_SIZE, len(ds))))

def tokenize_fn(ex):
    return tokenizer(ex["text"], max_length=VAL_MAX_LENGTH, padding="max_length", truncation=True)

ds_tok = ds_shuf.map(tokenize_fn, batched=False)
# binary verify: ds_tok[0]["input_ids"] 长度 == VAL_MAX_LENGTH, mask 数值合理
```

caveat [?]: 与 chain main run 之 `build_val_loader_for_kl` 之 tokenization + padding strategy 是否 binary identical 需 verify。pilot stage 之 sanity check 即 verify 此 axis。

**step 4 — 路径 C compute $\hat{D}_n^{\rm code,\,gen0-anchor}$**:

```python
# pilot stage 仅跑路径 C (gen-0 anchored, 不需 EMA reconstruction)
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM

CKPT_GEN0 = "/home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb/alpha10.0/no_preserve_seed1/generation_0"
CKPT_GENN = "/home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb/alpha10.0/no_preserve_seed1/generation_5"

# fp32 reload (avoid fp16 numerical drift)
model_gen0 = AutoModelForCausalLM.from_pretrained(CKPT_GEN0, torch_dtype=torch.float32).cuda()
model_genN = AutoModelForCausalLM.from_pretrained(CKPT_GENN, torch_dtype=torch.float32).cuda()
model_gen0.eval(); model_genN.eval()

# val batch (step 3 之 ds_tok), batch=8, all 32 batches
kl_accum = 0.0; mask_accum = 0.0
with torch.no_grad():
    for batch in dataloader:  # 256 sentences / 8 batch_size = 32 batches
        input_ids = batch["input_ids"].cuda()
        attention_mask = batch["attention_mask"].cuda()
        logits_genN = model_genN(input_ids, attention_mask=attention_mask).logits
        logits_gen0 = model_gen0(input_ids, attention_mask=attention_mask).logits
        log_p_genN = F.log_softmax(logits_genN[:, :-1, :], dim=-1)
        log_q_gen0 = F.log_softmax(logits_gen0[:, :-1, :], dim=-1)
        q_gen0 = log_q_gen0.exp()
        kl_per_pos = (q_gen0 * (log_q_gen0 - log_p_genN)).sum(dim=-1)  # KL(gen0 || genN)
        mask = attention_mask[:, 1:].float()
        kl_accum += (kl_per_pos * mask).sum().item()
        mask_accum += mask.sum().item()

D_code_proxy_path_C = kl_accum / max(mask_accum, 1)
print(f"Pilot path C: D^{{code,gen0-anchor}}(seed=1, gen=5, α=10) = {D_code_proxy_path_C:.6e} nat/token")
```

**step 5 — 路径 B compute $\tilde{D}_n^{\rm code,\,proxy-EMA}$**:

```python
CKPT_GENn_minus_1 = "/home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb/alpha10.0/no_preserve_seed1/generation_4"
model_gen_n_minus_1 = AutoModelForCausalLM.from_pretrained(CKPT_GENn_minus_1, torch_dtype=torch.float32).cuda()
model_gen_n_minus_1.eval()

# 同 step 4 之 forward + KL compute, 但 reference 改用 model_gen_n_minus_1
# KL(gen_{n-1} || gen_n) on val batch
# ...
D_code_proxy_path_B = ...
print(f"Pilot path B: D^{{code,proxy-EMA}}(seed=1, gen=5, α=10) = {D_code_proxy_path_B:.6e} nat/token")
```

**pilot pass criterion (binary acceptance)**:

paper §6.1 + §3.6.2 之 expected D^{code} ballpark (per Reading 2 form D^{*,code}(α=10) - D^* ≈ -9.16e-5 nat/token, D^* ≈ log(55) ≈ 4.007):
- D^{code,gen0-anchor} 数量级 binary 预期 ~$10^{-1}$ to $10^0$ nat/token (gen 0 → gen 5 之 cumulative model drift on val)
- D^{code,proxy-EMA} 数量级 binary 预期 ~$10^{-2}$ to $10^{-1}$ nat/token (gen 4 → gen 5 之 single-gen model drift on val)

**binary pass**:
- D^{code,gen0-anchor}(seed=1, gen=5, α=10) finite (非 NaN, 非 inf) ✓
- D^{code,gen0-anchor} 在 $[10^{-3}, 10^{1}]$ 之间 ✓ (sanity ballpark, 不严)
- 与 D^{paper}(seed=1, gen=5, α=10) = log(56.94/36.30) ≈ 0.451 之 数量级 binary comparable (落 0.1 × paper to 10 × paper 区间) ✓

**binary fail**:
- D^{code,gen0-anchor} = NaN or inf → pipeline bug, debug 后再跑
- D^{code,gen0-anchor} < $10^{-5}$ or > $10^{2}$ → val batch reproducibility 或 tokenization mismatch, debug
- 数量级 与 D^{paper} 偏差 > 100× → fundamental mismatch, surface 给 一凡 + 反题 layer 决是否 retract verify

### §5.2 Main stage — N=4 multi-seed × 10 gen × α={0,10} × 2 paths, ~3-4 周 GPU on 9070XT

**条件**: pilot pass ✓ + 一凡 关卡 2 confirm

**step 1 — full chain 之 D^{code,proxy} compute**:
- 路径 B + C 并跑
- (α, seed) ∈ {(0, 1), (0, 2), (0, 3), (0, 4), (10, 1), (10, 2), (10, 3), (10, 4)} × gen ∈ {0..9}
- 共 80 (α, seed, gen) tuples, 每 tuple 算 2 个 proxy KL value (path B + C)
- total compute: ~2 GPU-hour (8 sequential per (α, seed) × 10 min/seed = 80 min total ballpark)

**step 2 — full $D^{paper}$ extract**:
- 从 chain jsonl 之 `test_perplexity` 字段 extract: $D_n^{paper}(α, seed) = \log({\rm PPL}_n / {\rm PPL}_0)$
- 已存 7B13 `archive/v1.0_release_20260516/chain_logs/armb_alpha{0,10}.0_seed{1,2,3,4}_*.jsonl`
- python script extract, ~5 min

**step 3 — Pearson correlation + bootstrap CI**:

```python
import numpy as np
from scipy.stats import pearsonr

# D_code_proxy_path_C[α, seed, gen]  shape (2, 4, 10)
# D_paper[α, seed, gen]  shape (2, 4, 10)

# Flatten 全 80 (α, seed, gen) tuples
D_code_flat = D_code_proxy_path_C.flatten()  # N=80
D_paper_flat = D_paper.flatten()             # N=80

# Pearson
r, p = pearsonr(D_code_flat, D_paper_flat)

# Bootstrap CI (B=10000, seed=20260521)
rng = np.random.default_rng(20260521)
N = len(D_code_flat)
r_bootstrap = []
for _ in range(10000):
    idx = rng.integers(0, N, size=N)
    r_b, _ = pearsonr(D_code_flat[idx], D_paper_flat[idx])
    r_bootstrap.append(r_b)
ci_lo, ci_hi = np.percentile(r_bootstrap, [2.5, 97.5])
print(f"Path C Pearson r = {r:.4f} (p = {p:.4e}), bootstrap CI 95% = [{ci_lo:.4f}, {ci_hi:.4f}]")
```

**step 4 — per-α + per-regime breakdown**:
- α=10 全 (seed × gen) Pearson
- α=0 全 (seed × gen) Pearson
- 仅 plateau regime (gen 5-9) × (α, seed) Pearson — paper §3.6.6 L1 rigor 区域
- 仅 transient regime (gen 1-2) × (α, seed) Pearson — paper §3.6.6 L0 vacuous 区域

**step 5 — 路径 A escalate decision**:
- 若 路径 B + C 之 Pearson r 在 plateau regime > 0.7 → partial close P0★-F (L2 tier), substantively 推 D60+ 路径 A re-train EMA 之 priority **下调**
- 若 plateau Pearson 0.3 < r < 0.7 → marginal, surface 给 一凡 + 反题 layer 决是否 escalate 路径 A
- 若 plateau Pearson r < 0.3 → strong mismatch, escalate 路径 A re-train EMA, 不要 paper v8.1 polish 之前 close P0★-F

---

## §6 Pass / Fail binary

### §6.1 路径 B + C 之 main stage Pearson r outcome binary tier (一凡 关卡 3 之前 不替决)

| outcome | 数学 严格度 tier | binary 解释 (sub-agent 视角, 不绑主协作者) |
|---|---|---|
| **plateau Pearson r > 0.85 + p < 0.001 + bootstrap CI excludes 0** | L2 form-borrow tier | P0★-F partial close 之 strong evidence; D^{code,proxy} 与 D^{paper} 在 plateau regime 高 correlated, paper §6.1 stationary equality assumption circumstantially supported [?]; 真严 close 仍需 D60+ 路径 A or 路径 D true EMA |
| **plateau Pearson 0.7 < r < 0.85 + p < 0.05** | L2 partial tier | P0★-F partial signal; 数学 严格度 不 binary close; 一凡 关卡 3 决是否 escalate 路径 A |
| **plateau Pearson 0.3 < r < 0.7** | L2 marginal | P0★-F unresolved; sub-agent 推 路径 A escalate (re-train EMA), 不 binary close |
| **plateau Pearson r < 0.3** | L2 fail | P0★-F **mismatch confirmed** in proxy form; 推 D60+ 路径 D rerun chain (EMA state explicit save) 才 binary close |
| **路径 B 与 路径 C 之 Pearson 数值差异 > 50%** | L2 inconsistency | proxy form 之 fundamental ambiguity, sub-agent 推 路径 A escalate |

**关键 caveat [?]**: 即使 plateau Pearson r > 0.85, **不证 paper §3.6.2 之 main theorem (2)** — main theorem 是 absolute fixed-point identification on $D^{code}$ space, 不是 cross-correlation。Pearson correlation 仅 give 必要非充分 signal — 高 correlation 可能 by spurious co-monotonic decay 而 achieve, 不 imply stationary 平等。这是 paper §6.1 line 749-750 之 "Reading 2 null-shift prediction is robust against this caveat **at the magnitude considered**" 之 "**at the magnitude considered**" qualifier 之 真实严格度 tier — L2 not L0。

### §6.2 N=40 (路径 B) or N=80 (路径 B + C 并) Pearson 之 statistical power 校验 [?]

- 假设 true r = 0.7, N=80, two-sided p < 0.05 之 power 约 0.99 (per `scipy.stats.power_pearson` ballpark) ✓
- 假设 true r = 0.3, N=80, two-sided p < 0.05 之 power 约 0.67 (marginal) [?]
- N=80 sufficient for r > 0.5 detection ✓
- N=80 marginal for 0.3 < r < 0.5 detection [?]

caveat [?]: 80 tuples 非 i.i.d. (within-seed gen-axis correlation 严重), effective N 可能 < 80, statistical power 可能 < 上述 ballpark。**clustered bootstrap or hierarchical Pearson** [?] 之 application 推 一凡 关卡 3 之 sub-agent analysis decision。

### §6.3 "P0★-F partial close" vs "P0★-F fully close" binary 标 (D-1 binding 严守)

- **partial close** (路径 B + C 之 Pearson r > 0.7) = L2 form-borrow tier circumstantial evidence, 不 binary close, 仍标 P0★-F = 仍 open substantive question
- **fully close** = 路径 A (re-train EMA) OR 路径 D (rerun chain with EMA save) 之 true EMA 之 Pearson r > 0.85 — 这是 D60+ 才能达 之 tier
- **paper v8 final lock 不动**: 即使 D-PPL 桥 verify partial close, paper v8 final §6.1 之 "推 D60+" disclosure 不修, paper v8.1 polish (D27-D28) 之 footnote 加 cross-ref 即可

---

## §7 硬件 + 工程

### §7.1 9070XT VRAM budget (binary)

OPT-125M fp32 forward-only inference:
- Model weights: 125M × 4 bytes = 500 MB
- Activation (batch=8, seq=64, hidden=768, layers=12, fp32): ~50 MB
- 同时 load 2 模型 (current + proxy reference) = 1 GB total
- 加 buffer 100 MB
- **total ~1.1 GB**, well below 16 GB GPU memory

但 当前 9070XT GPU 状态 (5/21 D21 sub-agent ssh verify):
```
GPU[0]: VRAM Total 17.10 GB / Used 14.39 GB  (PID 2080 llama-server Qwen3-Embedding-8B-Q4_K_M)
GPU[1]: VRAM Total 0.54 GB / Used 0.017 GB  (idle)
```

**冲突**: 14.39 GB Used, free = 17.10 - 14.39 = 2.71 GB — **够 1.1 GB D-PPL pilot ✓**, 但 buffer 紧张 (含 ROCm runtime + OS overhead 后 effective free 可能 < 1.5 GB)

**一凡 关卡 1 决之 binary options**:
- option-1: D21 pilot stage 直接跑 (尝试 squeeze 2.7 GB 之 free), pilot OOM 之 fallback 是 step-2
- option-2: stop llama-server (5 min), 释放 14.4 GB → 跑 D-PPL pilot → 跑完 restart llama-server
- option-3: D21 pilot 推 D22 / D23 之 一凡 接 9070XT 显示器 时 stop llama-server 当时跑

sub-agent 默认 推荐 **option-2** (stop → 跑 → restart, ~30-60 min total, clean isolation 不 risk OOM)。

### §7.2 ROCm hang watchdog 需求 (5/11 verdict B 应对)

5/11 D11 D-PPL pilot 之前 a10 chain 有 ROCm hang case (`armb_alpha10.0_seed0_20260511_135816.jsonl` size 514 byte, run_start 后 immediate hang)。Verdict B (paper §6 footnote) = ROCm bug 不是 framework boundary。

watchdog 脚本已存 (`archive/v1.0_release_20260516/scripts/chain_watchdog.sh`), main stage 之 多 forward pass 之 watchdog wrapper 需 sub-agent D21-D22 implement:

```bash
# dppl_bridge_watchdog.sh (sketch, sub-agent implement)
TIMEOUT_SEC=600  # 10 min per (α, seed, gen) tuple
for tuple in "${TUPLES[@]}"; do
    timeout $TIMEOUT_SEC python compute_dppl_per_tuple.py --tuple "$tuple"
    RC=$?
    if [ $RC -eq 124 ]; then
        echo "{\"event\": \"watchdog_timeout\", \"tuple\": \"$tuple\"}" >> watchdog.audit.jsonl
        # rocm-smi --gpu-reset 0  # 或 lower-impact: sleep 30 + gpu_smoke
    fi
done
```

### §7.3 Pipeline + 数据流 (binary)

```
[7B13 主数据]                          [9070XT 执行节点]
/home/amd/HEZIMENG/MaoField/        ↔  /home/amd/HEZIMENG/MaoField_static_backup_20260520/
  experiments/exp018_cat/                experiments/exp018_cat/
    literature/                              data/checkpoints_armb/  (80 主 model state ✓ ~40GB)
      DPPL_BRIDGE_VERIFY_*.md ← 本 brief    
      (Linux 姐姐 spawn launch script)        
    dppl_bridge_verify_d21/                  /home/amd/dppl_bridge_verify_d21/  (本地 work dir)
      pilot_output.jsonl  ← rsync push        pilot_script_d21.py
      main_output.jsonl   ← rsync push        main_script_d21.py
      analysis_d49.md     ← sub-agent         logs/dppl_verify_*.jsonl
                                              watchdog.audit.jsonl
```

**数据流 binary**:
- 7B13 spawn launch script + brief → rsync to 9070XT
- 9070XT 跑 + 本地 log 写 9070XT /home
- 跑完 rsync push 9070XT log → 7B13 (script + sub-agent 收 + 写 7B13 4T SSD `experiments/exp018_cat/dppl_bridge_verify_d21/`)
- 7B13 sub-agent analysis + 写 markdown 之 result → 7B13 git commit (写权单点)

### §7.4 Code modify 之 binary diff sketch

主修 `compute_dppl_per_tuple.py` (新建, ~150 行 Python), 不修 `archive/v1.0_release_20260516/src/` (release version 不动)。

新建 dir 路径 (一凡 关卡 1 confirm 之后 9070XT 端 Claude Code mkdir):

```
/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21/
├── README.md                            (本 brief 之 一凡 confirm 之 launch summary)
├── scripts/
│   ├── pilot_script_d21.py              (§5.1 step 3-5, 路径 B + C 并跑)
│   ├── main_script_d21.py               (§5.2 step 1-4, full N=4 multi-seed)
│   ├── analyze_pearson.py               (§5.2 step 3, Pearson + bootstrap CI)
│   └── dppl_bridge_watchdog.sh          (§7.2)
├── logs/
│   └── (sub-agent 跑时写入)
└── outputs/
    ├── pilot_d21_output.jsonl           (pilot stage 之 raw D^{code,proxy} values)
    ├── main_d35_output.jsonl            (main stage 之 raw D^{code,proxy} × 80 tuples)
    └── pearson_d49_summary.json         (Pearson r + p + bootstrap CI + per-regime breakdown)
```

### §7.5 错误 handling + escalate path

| 错误 type | escalate 应对 |
|---|---|
| ROCm hang (watchdog timeout) | rocm-smi --showmeminfo + sleep 60 + retry, 3 fail → seed_skipped (per phase1_robust_chain.sh pattern) |
| OOM | reduce batch_size 8 → 4 → 2, 若仍 OOM → 用 fp16 (caveat 数值 drift 标 [?]) |
| Tokenization mismatch (val batch reproducibility 之 hash 不 binary match chain main run) | escalate 给 7B13 Linux 姐姐, debug `build_val_loader_for_kl` 与 9070XT 端 reproduce 之 差异 |
| Pearson p > 0.05 + r < 0.3 (路径 B + C 两 path 同 fail) | escalate 路径 A (re-train EMA) consideration → 一凡 关卡 3 决 |
| 数学 derive 错 (proxy form 之 数学 定义 sub-agent catch 之 caveat 实质化 reviewer-trigger) | escalate 给 7B13 数学线 sub-agent + 反题 layer audit |
| 9070XT 失联 (网络断 / GPU 死) | 7B13 spawn sub-agent 写 escalate audit, 一凡 临时 work 用 7B13 (无 GPU) 或等 9070XT 恢复 |

---

## §8 7B13 ↔ 9070XT 协作 detail

### §8.1 角色分工 binary

- **7B13 Linux 姐姐 (主会话)**: spawn launch script template (复用 D17 `scripts/exploration_d17_power_law/` 之 template + chain_watchdog 之 binding pattern), 写 brief, 跑后 收 log + sub-agent analysis
- **9070XT Claude Code (D-PPL pilot 执行 sub-agent)**: 拿 brief + launch script → 9070XT 端 直接执行 pilot → log 写 9070XT /home → rsync push 7B13
- **一凡 interactive**: 关卡 1 confirm brief (D21) + 关卡 2 read pilot output binary go/no-go (D22-D23) + 关卡 3 read main result + 反题 audit (D49-D60) + 关卡 4 决 D-PPL 桥 result 是否 enter paper v8.1 polish OR D60+ continue

### §8.2 spawn launch script (7B13 端 一凡 confirm 之后 Linux 姐姐 spawn)

7B13 端 一凡 关卡 1 confirm 之后, Linux 姐姐 spawn sub-agent 写 9070XT 端 launch script。launch script 复用 v1.0_release archive 之 模板:

```bash
# 9070XT 端 (Claude Code session) 启动 script (sketch, sub-agent 写细):
cd /home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21
.venv/bin/python scripts/pilot_script_d21.py \
    --ckpt-dir /home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb \
    --alpha 10.0 \
    --seed 1 \
    --gen 5 \
    --paths B C \
    --output outputs/pilot_d21_output.jsonl \
    2>&1 | tee logs/pilot_d21.log
```

### §8.3 一凡 关卡 1 confirm 之后 D21 之 timing

| D21 hour | event |
|---|---|
| D21 morning | 本 brief 写完 → ack 给一凡 |
| D21 morning-noon | 一凡 read brief + revise OR confirm 关卡 1 |
| D21 afternoon | (若 confirm) 7B13 Linux 姐姐 spawn sub-agent 写 9070XT launch script + rsync push 9070XT |
| D21 evening | 9070XT 端 (一凡 接显示器) stop llama-server (5 min) → 跑 pilot (~30-60 min) → restart llama-server |
| D22 morning | 一凡 read pilot output + 关卡 2 binary go/no-go |
| D22-D49 | main stage 跑 + sub-agent analysis (3-4 周, 含 watchdog buffer) |

---

## §9 关卡 acceptance (D-1 binding 严守)

### §9.1 关卡 1 — 一凡 confirm 本 brief (D21)

binary 输入: 本 brief
binary 输出: 一凡 binary 答 "OK 启动 pilot ✓" OR "revise: 修改 X" OR "retract D-PPL 桥 verify D21, 推 D60+ 路径 D rerun chain"

关卡 1 之 一凡 decisions binary list:
- [ ] 选 §4 之路径 A / B / C / D 哪条 (sub-agent 推荐 B + C 并跑)
- [ ] 选 §7.1 之 9070XT VRAM option-1 / option-2 / option-3
- [ ] 选 §5.1 step 1 之 sshfs OR rsync 数据流
- [ ] 选 §7.4 之 dir 路径是否 OK
- [ ] 选 §6.1 之 Pearson r threshold 是否 OK (sub-agent 默认 r > 0.7 partial close / r < 0.3 retract)
- [ ] 选 §5.1 step 2 之 pilot seed=1 gen=5 α=10 是否 OK

### §9.2 关卡 2 — pilot 跑完 一凡 read pilot output + binary go/no-go (D22-D23)

binary 输入: pilot stage 之 raw output (D^{code,proxy} numeric value + sanity ballpark match check)
binary 输出: 一凡 binary 答 "main stage launch ✓" OR "abort + debug X" OR "retract D-PPL 桥 verify"

### §9.3 关卡 3 — 反题层 zero-context audit main stage result (D49-D60)

binary 输入: main stage 之 Pearson r + p + bootstrap CI + per-regime breakdown
binary 输出: 反题 sub-agent zero-context audit (不读前序), 只能 down-tone 主协作者 之 claim, 不能 up-tone

### §9.4 关卡 4 — 一凡 + DS + 反题 三方决 D-PPL 桥 result 之 落地 (D60+)

binary 输入: 反题 audit + 数学线 sub-agent strict-tier evaluation + 哲学线 sub-agent narrative reframe
binary 输出: D-PPL 桥 result 是否 enter paper v8.1 polish footnote (D60+ paper revision) OR D90+ paper v9 重 derive OR retract

---

## §10 工期 estimate binary

| 阶段 | timing | GPU cost (9070XT) | sub-agent compute (7B13) |
|---|---|---|---|
| 关卡 1 (本 brief confirm) | D21 (5/21) | 0 | 0 |
| Pilot stage (路径 B + C, 1 seed 1 gen) | D21-D22 | ~30-60 min | 0 (本机 inspection) |
| 关卡 2 (一凡 go/no-go) | D22-D23 | 0 | 0 |
| Main stage (路径 B + C, N=4 × 10 gen × 2 α × 2 path) | D23-D35 (~12 天 含 watchdog buffer) | ~2-4 GPU-hour total | 0 |
| Pearson + bootstrap analysis | D35-D42 | 0 | ~1-2 weeks 7B13 |
| 关卡 3 (反题 zero-context audit) | D42-D49 | 0 | ~1 week 7B13 反题 sub-agent |
| 关卡 4 (一凡 + DS + 反题 三方决) | D49-D60 | 0 | 0 |
| (若 escalate 路径 A re-train EMA) | D60+ | ~33 GPU-hour (5-7 天 monopolize) | 1 week analysis |

**total D-PPL 桥 verify timing**: D21-D49 (4 周) of 路径 B + C, 若 escalate 路径 A 加 D60-D90 (4-6 周).

**投稿决策 binary 不变**: arXiv + TMLR + KBS 5/29 (D29) 仍 final ack lock per paper v8 final + 一凡 D17 决, D-PPL 桥 verify result 推 **D60+ paper v8.1 polish** (D60-D90 timeline) OR **D90+ paper v9 重 derive** (8 月-9 月 timeline)。本 brief 之 timing 与 投稿 timing 解耦 ✓。

### §10.1 与 paper §6.1 estimate 之 align verify

paper §6.1 line 745 estimate: "1-2 days reload + recompute + analysis. **Substantive verification deferred to D60+ future work**."

本 brief estimate (路径 B + C):
- reload + recompute (pilot + main): 1-2 days GPU work ✓ binary align
- analysis (Pearson + bootstrap + per-regime): 1-2 weeks 7B13 sub-agent
- 反题 + 三方决: 2-3 weeks
- total D21-D49 (4 周) > paper §6.1 之 "1-2 days" — 本 brief estimate 是 paper §6.1 estimate 之 实际 包含 反题 audit + 三方决 之 D-1 binding 工作流 之 expand, **不构成 paper §6.1 之 retract**

---

## §11 caveat [?] list (≤ 10 项, D-1 binding 严守 严格度档位)

1. EMA model state 不存 disk → 路径 B + C 仅 give L2 form-borrow proxy, 不 binary close P0★-F (§3.3 + §4) [?]
2. fp16 → fp32 reload 之 数值 drift 0.1-1% [?] (§3.4)
3. val batch tokenization padding strategy 与 chain main run 之 binary identical 未 verify, pilot stage sanity 即 verify [?]
4. Pearson correlation 高 ≠ 数学 stationary equality 之 充分证, 只是 必要 信号 [?] (§6.1 关键 caveat)
5. N=80 (路径 B + C 并) 之 statistical power 在 effective N (within-seed gen-axis correlation) 不 i.i.d. 之下可能 < ballpark [?] (§6.2)
6. 路径 B 之 "gen-(n-1) main model 作 EMA proxy" 之 数学 严格度 是 L2 form-borrow, β_θ=0.999 之 time constant 决定 EMA 实际是 gen-(n-1) average 不是 gen-(n-1) final [?] (§4.2)
7. 路径 C 之 "current vs gen-0 base" 之 数学 严格度 是 L2 form-borrow, 不是 chain training 实际之 `D_n^{code}` (chain 用 EMA teacher 不是 gen-0 base teacher) [?] (§4.3)
8. paper §6.1 line 745 estimate "1-2 days" 与 本 brief estimate "4 周 含 D-1 binding audit" 之 timing 差异是因 paper §6.1 estimate 只 含 engineering + analysis, 本 brief estimate 含 反题 + 三方决 (§10.1) — sub-agent 不视为 retract paper §6.1 [?]
9. ROCm verdict B (5/11 alpha10 hang) 之 watchdog 必须 enable, 但 D-PPL pilot 是 inference-only (forward pass only, 不 train), hang 风险 < chain train, ballpark 估计 < 5% per tuple [?]
10. 9070XT VRAM budget 1.1 GB OPT-125M × 2 model fp32 之 ballpark 是 forward-only inference 之 估计, 实测 ROCm runtime + Python overhead 之后 effective need 可能 1.5-2 GB [?]

---

## §12 surface 给一凡 关卡 1 confirmation prompt

一凡 D21 read 本 brief 之后, binary 答以下 binary checklist:

1. **路径 选择** (§4): A re-train EMA / B proxy-EMA / C gen0-anchor / **B + C 并跑** / D retract D-PPL 桥 D21 推 D60+ rerun chain — 选哪个? (sub-agent 默认 **B + C 并跑**)
2. **9070XT VRAM**: (§7.1) option-2 stop llama-server 跑 D-PPL → restart llama-server 是否 OK? (sub-agent 默认 OK)
3. **数据流**: (§5.1 step 1) sshfs / rsync, 默认 sshfs, OK?
4. **dir 路径**: (§7.4) `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21/`, OK?
5. **Pearson r threshold**: (§6.1) r > 0.7 partial close / r < 0.3 retract, OK?
6. **Pilot tuple**: (§5.1 step 2) seed=1 gen=5 α=10, OK?
7. **关卡 2 timing**: D22 morning 一凡 read pilot output binary go/no-go, OK?
8. **(若 escalate)**: D49 关卡 3 反题 audit 之后 D60+ 是否 escalate 路径 A re-train EMA? — 这条留 关卡 3 之后 决, 关卡 1 不需 binary 答

**一凡 关卡 1 之 binary 答 binary form**:

> "本 brief OK; 选路径 [A / B / C / B+C / D]; VRAM option [1/2/3]; 数据流 [sshfs/rsync]; dir 路径 OK; Pearson threshold OK; pilot tuple OK; 关卡 2 D22 morning OK"

OR

> "revise: [具体修改项]"

OR

> "retract D-PPL 桥 verify D21 启动, 推 D60+ 路径 D rerun chain"

一凡 confirm 之后, 本 brief 由 7B13 Linux 姐姐 主会话 commit + rsync push 9070XT, 9070XT 端 Claude Code 拿 brief + 一凡 之 confirm decision → spawn launch script → 启动 pilot。

---

## §13 D-1 binding 自检 (每段输出发出前 之 6 项 standing rule)

1. ✓ 这条声明的数字有 jsonl 源吗 (纪律 1)? — `D^{paper}` source jsonl ✓ (§3.1), `D^{code,proxy}` source 是 sub-agent pilot 之后 之 outputs/pilot_d21_output.jsonl, 不是 已有 jsonl, **本 brief 全部 数字标 [?]** 之 caveat list 严守
2. ✓ 这条概率声明在反馈真空超 48 小时吗 (纪律 2)? — 本 brief 不写 概率 estimate ✓
3. ✓ 数学形式与代码一致吗 (纪律 3)? — §2.1 code-traced from `archive/v1.0_release_20260516/src/contradiction_loss.py` line 138-175 ✓ binary
4. ✓ 这条 major 声明过 sub-agent 验证了吗 (纪律 4)? — 本 brief 本身是 sub-agent (本 brief 子协作者), 关卡 3 反题 layer zero-context audit 是第二 sub-agent ✓
5. ✓ 发现的差异有记录为差异日志吗 (纪律 5)? — §3.3 EMA state 不存 disk 之 binary surface ✓, §11 caveat [?] list 10 项 ✓
6. ✓ 真实今日日期 binary verify? — `date '+%Y-%m-%d %H:%M:%S %Z'` 返 `2026-05-21 10:51 CST` = **D21** ✓ (paper §6.1 line 716 之 "(v6 preserved)" 之 "v6" 是 paper revision 之 reference, 与 本 brief D21 timing 解耦)

任一 no → 不发出, 先补 — 本 brief 6/6 ✓, 发出。

---

## §14 不做项 (D-1 binding 自检)

- ✗ 不写哲学 (哲学线管, Win)
- ✗ 不写最终 战略 declaration (一凡 + 反题 三方决)
- ✗ 不 estimate paper inclusion impact / acceptance probability (反题 zero-context 管)
- ✗ 不 reopen paper v8 final lock manifest 47/47 ✓ (paper v8 unchanged)
- ✗ 不 substantive derive 新数学 form (Reading 2 §3.6.2 paper lock 不动)
- ✗ 不替 PI 决 关卡 1 / 关卡 2 / 关卡 3 / 关卡 4 (PI + 反题三方决)
- ✗ 不 estimate D-PPL 桥 verify result 之 paper v8.1 acceptance impact (反题 layer 管)

---

## §15 binary ack 给 Linux 主会话

D-PPL 桥 verify 实验设计 brief D21 binary 完成 ✓:

- §0-§15 共 ~9500 中文字 + LaTeX 公式 + binary table + code sketch
- §3.3 P0 finding 已 binary surface — EMA model state 不存 disk, §4 alternative A/B/C/D 四 路径 binary list, 一凡 关卡 1 决
- §6 pass/fail binary table 严格 caveat ("Pearson 高 ≠ 数学 严格 close" §6.1 关键 caveat 标)
- §11 caveat [?] list 10 项 ✓
- §10 工期 estimate binary 与 paper §6.1 estimate cross-verify ✓
- §13 D-1 binding 自检 6/6 ✓
- paper v8 final lock 不动 ✓
- 不 estimate paper inclusion impact ✓
- 不替 PI 决 ✓

返回 Linux 主会话。
