# Phase 5 N=1 Llama-3.1-8B + ℒ_矛盾 Demonstrated — 完整实验设计与云 GPU 配置

**生成**: 2026-05-19 (D18+ Phase 5 N=1 demonstrated 子协作者)
**Author**: opus 4.7 (Phase 5 design 子协作者)
**派遣方**: Linux 姐姐数学层
**触发**: 5/19 一凡 + DS 指令(线下一阶段实验启动)
**绑定**: paper v6 §8.1 D23-D26 "Phase 5 N=1 Llama-8B + ℒ_矛盾 demonstrated, 3-5 天 cloud GPU + $50" 任务
**Honest framing(规则 1 + 7 binding)**: 本设计是 **N=1 single-seed demonstrated**,不能 statistical conclude(N=1 单 seed → 无 paired-t df,不能 establish framework effect);其用途是 paper §7.5 (1) substantive contribution support 之 partial verify,**不是 "framework universal across architectures" 的 establishment**。

---

## §0. TL;DR Binary

| 维度 | 决定 | 备注 |
|---|---|---|
| Model | **Llama-3.1-8B**(`meta-llama/Meta-Llama-3.1-8B`) | base model,不是 instruct |
| Dataset | **Wikitext-2-raw-v1**(primary,chain consistency with OPT-125M) | optional + C4-subset 1-2 seed if budget 允许 |
| Form | **两项 EMA-deviation**(K=1, T_2=0; chain actual form align paper v6 §3.1) | 不是 Klein-Gordon 三项 form |
| α scan | **α=0(baseline)+ α=10(framework primary)**,N=1 each | (额外 α=1 + α=5 仅 budget 充裕时) |
| GPU | **RunPod A100 40GB,full fp16,no LoRA**(primary) | alt: vast.ai 4090 + LoRA(超经济但 dynamics 异化 [?]) |
| Budget | **$50 primary**($38 GPU + $12 storage/buffer);可达 $80 stretch | 5/12-5/13 multi-seed OPT-125M $0(本地 RX 9070 XT)reference |
| Wall-clock | **3-5 天**(D23-D26 paper v6 §8.1 commit;Day 1 setup / Day 2-3 chains / Day 4 eval / Day 5 report) | 8-10h GPU per α chain,序列跑 |
| 关键 metric | gen 0-9 **test_perplexity**(framework-clean,not val_ppl)+ distinct_n + sliding-window stride=256 | U-shape 是否在 Llama 上 reproduce(N=1 indicative only) |
| 关键 risk | OPT-125M(60×小)→ Llama-8B 60×参数 + RoPE + RMSNorm + GQA dynamics 异化;m_eff=0.300 是 OPT fit,**不能假定 Llama 同值**;N=1 不能 statistical conclude | 标 [?] 全部不确定项;不偏袒 paper claim |

---

## §1. Model + Dataset 选择 Binary

### §1.1 Model: Llama-3.1-8B

**候选评估**(2026-05-19 二元):

| 候选 | 参数 | License | Arch | 选择 | 理由 |
|---|---|---|---|---|---|
| **Llama-3.1-8B** | 8.03B | Llama 3.1 Community License | RMSNorm + RoPE + GQA(8 KV heads / 32 Q heads)+ SwiGLU | ✓ **PRIMARY** | 最新 industry frontier scale 接近 + paper v6 §6.5 explicit cite "Llama, Pythia" multi-arch future work,Llama 优先匹配 |
| Llama-3-8B | 8.03B | Llama 3 Community License | 同 Llama-3.1 但 context length 8K vs 128K | ✗ | Llama-3.1 是 3 的 superset,无理由选旧版 |
| Mistral-7B | 7.24B | Apache 2.0 | RMSNorm + RoPE + GQA + SWA(sliding-window attention) | △ | SWA 在 wikitext-2 64-token block 上不激活,无差异;Apache 2.0 license 更宽但 paper v6 explicit cite Llama,统一 narrative 优先 |
| Pythia-6.9B | 6.9B | Apache 2.0 | LayerNorm + RoPE + standard MHA | △ | Pythia 是 paper v6 §6.5 second-tier candidate;arch 更接近 OPT(LayerNorm 而非 RMSNorm),但**正因如此**作为 Llama 备份测试 dynamics 异化时更有价值(留 D60+) |
| OPT-1.3B | 1.3B | OPT MIT-like(non-commercial)| LayerNorm + sinusoidal pos + MHA | ✗ | scale 跳跃太小(125M → 1.3B = 10×,而 Llama 是 60×),不能支持 "multi-arch + scale-up" double extension |

**决定**: **`meta-llama/Meta-Llama-3.1-8B`**

**HF 路径**: `meta-llama/Meta-Llama-3.1-8B`(base model,**不是** `Meta-Llama-3.1-8B-Instruct`,因为 chain 实验是 raw continued pre-training,不涉及 instruction-following dynamics)

**License gate**: Llama 3.1 Community License,需 HF 账户 + `huggingface-cli login` + 在 HF model card 页同意 license terms(通常 1-2 小时 auto-approve)

**Tokenizer**: SentencePiece BPE,vocab 128,256(OPT 用 GPT-2 BPE 50,257;**Llama vocab 大 2.55×**,影响:wikitext-2 同 sentence tokenize 后 block 数会变;需重新计算 N_step per gen,见 §2.4)

**架构关键 caveat(影响 chain config)**:
- **RMSNorm vs LayerNorm**: OPT-125M 用 LayerNorm(有 bias),Llama 用 RMSNorm(无 bias,仅 rescale);影响 hidden state 分布,可能影响 EMA model 的 KL trajectory shape [?]
- **RoPE vs sinusoidal**: OPT 用 learned/sinusoidal positional encoding,Llama 用 RoPE;在 block_size=64 上差异较小,但 attention pattern 可能不同
- **GQA vs MHA**: Llama-3.1-8B 用 8 KV / 32 Q heads(grouped query attention),OPT 用标准 MHA;KV cache 在 inference 上小 4×,但 fine-tuning training step 计算量与 MHA 量级一致
- **SwiGLU vs ReLU**: Llama 用 SwiGLU activation,OPT 用 ReLU;activation pattern 不同,gradient flow 可能不同

**预估 chain dynamics 异化方向**(标 [?]):
- gen 0 test_ppl on wikitext-2-test:Llama-3.1-8B 预估 **8-15**(OPT-125M gen 0 是 36.32);理由:模型参数 60×大,wikitext-2 在 pretrain 数据中已见(OPT pretrain corpus 含 Pile,Llama pretrain 含 wikipedia 全集),所以 zero-shot perplexity 应该非常低;fine-tune 1-2 epoch 后可能进一步降到 6-10 范围 [?]
- U-shape spike(gen 1-2 ratio 2.9× 对 OPT)在 Llama 上 reproduce 与否:**主要不确定项**;假设 1:U-shape 是 model collapse 通用 phenomenon → reproduce(spike ratio 1.5-2.5×);假设 2:U-shape 是 small-model fragile artifact,Llama 8B robust capacity 削弱 spike → 不 reproduce;**N=1 无法区分**,需 multi-arch + multi-seed D60+ 才能解
- plateau ppl(gen 6-9):预估 **15-30**(对 gen 0 ratio 1.5-3×);不一定有清晰 plateau,可能持续上升

### §1.2 Dataset: Wikitext-2(primary)+ optional C4-subset

**Primary**: `wikitext`, config `wikitext-2-raw-v1`(同 OPT-125M chain,**严格 chain consistency**)
- train: 36,718 sequences(approx,Llama tokenizer 后会变,需重算)
- validation: 3,760 sequences
- test: 4,358 sequences
- block_size: 64 tokens(保持 chain consistency;**Llama vocab 大 2.55×,但 BPE token 多数英文词为单 token,实际 token 数差异 < 30%**)
- 选 raw-v1 而非 v1:与 OPT-125M chain 一致(`cat_arm_b.yaml` line 58)+ Llama-3.1 tokenizer 兼容 raw 字符流

**Caveat**: Wikitext-2 在 Llama-3.1 pretrain corpus 中**几乎确定见过**(Llama pretrain 含 wikipedia 全集);意味着 Llama-3.1-8B 已经"知道" wikitext-2,fine-tune 主要是 distribution 微调,不是 fresh learning;**这与 OPT-125M 的情形定性不同**(OPT pretrain corpus 含 wikipedia 但远小于 Llama pretrain scale);**chain collapse dynamics 可能因此弱化**

**Optional secondary**(budget 充裕):
- `allenai/c4` `realnewslike` subset 10K-50K blocks(scale-up evidence;chain 在 broader text 上的行为)
- 选 realnewslike subset 因为更接近 model collapse paper 经典 setup(Shumailov 2024 用 wikitext,Lebrun et al. 2024 用 C4)
- 决策:**先不跑 C4,Wikitext-2 chain consistency 优先**;C4 留 D60+ multi-arch full study

**Tokenization 实施**:
```python
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B")
# Llama-3 没有 explicit pad_token,需 set:
tokenizer.pad_token = tokenizer.eos_token  # 通用 trick;也可 add_special_tokens
# block_size = 64(chain consistency)
# wikitext-2 train 重新 tokenize 后 block 数 [需实际跑确认]
```

---

## §2. ℒ_矛盾 Chain Config

### §2.1 Critical Form Decision: 严格对齐 Chain Actual Two-Term Form,不是 Klein-Gordon 三项

**重要**(基于 paper v6 §3.1 honest disclose + 5/11-5/13 螺旋失败教训纪律 3):

paper v6 已 honest disclose chain actual loss 是 **两项 EMA-deviation form**:

```
ℒ_contradiction^{chain, actual} = (ΔD_n)² + (D_n - D̄^EMA_n)²
```

理由:`kl_history_K = 1` → `if len(D_history) == 1` 分支触发 → `D_doubleprime = torch.zeros_like(D_n)` → `T_2 = ReLU(0) = 0` for all generations

**Phase 5 Llama-8B 实验严格 align chain actual form**,即:
- T_2_form: `"relu_dpp"`(保持 OPT-125M chain config 一致,虽然实际 T_2 = 0)
- kl_history_K: 1(两项 form)
- lambda_1, lambda_2, lambda_3: 1.0 uniform(yaml override)
- m_eff: 1.0(CATConfig dataclass default;chain runtime value;不进 loss 因为 T_2 = 0)

**不**用 Klein-Gordon coefficient `λ_1 = 1/(2 m_eff), λ_2 = m_eff/2, λ_3 = m_eff`,因为 chain 实际从未跑过这个 yaml(`cat_arm_b_v2_dialectical.yaml` 从未在主 chain 中 launch,paper v6 §3.1 已 explicit cite)

**不**用 K=9 Volterra history,因为 chain 实际 K=1

**理由**(纪律 3 binding,"代码里的形式优先于 paper 里的形式"):
- Llama-8B Phase 5 的 demonstrated 任务是 "reproduce chain actual behavior on Llama,N=1 indicative",**不是** "test Klein-Gordon coefficient form lift"
- Klein-Gordon coefficient form lift 是 paper v6 §6.5 Gap 1 substantive future work F-1 Phase 2,推 D18+ 1-2 月,**不在 Phase 5 scope 内**
- 如果 Phase 5 Llama 实验突然换用 Klein-Gordon coefficient,paper §7.5 (1) substantive contribution support 的 "chain actual form transfers to multi-arch" claim 就 **无法 anchor 在 OPT-125M chain 结果上**;不可比较

### §2.2 Complete YAML Config(`phase5_llama8b_alpha_scan.yaml`)

```yaml
# Phase 5 N=1 Llama-3.1-8B + ℒ_矛盾 demonstrated
# Aligns chain actual two-term form (paper v6 §3.1)
# 不是 Klein-Gordon 三项 form (留 D60+ substantive future work)

experiment:
  name: phase5_llama8b_emergent_n1
  paper_cite: "MaoField paper v6 §8.1 D23-D26; Shumailov 2024 baseline setup; Llama-3.1 base model"
  goal: "N=1 single-seed multi-arch indicative: chain actual two-term form on Llama-3.1-8B,test U-shape + plateau reproduce 与否"
  honest_caveat: "N=1 不能 statistical conclude framework universal; partial verify of paper §7.5 (1) substantive contribution support only"

# ---------- Model ----------
model:
  hf_id: "meta-llama/Meta-Llama-3.1-8B"
  dtype: "float16"               # full fp16 training (no LoRA, no quantization)
  cache_dir: "data/checkpoints/hf_cache_llama"
  # caveat: HF Llama-3.1 access 需 license accept (HF account login + model card agree)
  # caveat: Llama-3.1 base 不是 instruct; raw continued pre-training setup

# ---------- Dataset ----------
dataset:
  hf_id: "wikitext"
  hf_config: "wikitext-2-raw-v1"
  block_size: 64                 # chain consistency with OPT-125M
  splits:
    train: "train"
    validation: "validation"
    test: "test"
  cache_dir: "data/datasets"
  # caveat: Llama tokenizer (SentencePiece BPE vocab 128k) vs OPT (GPT-2 BPE vocab 50k)
  # wikitext-2 train 实际 block 数会变 [待实际跑确认]

# ---------- Fine-tune (per generation) ----------
fine_tune:
  optimizer: "adamw_torch"        # 与 OPT chain consistency
  learning_rate: 2.0e-5           # 与 OPT chain consistency (低 lr safety for large model)
  per_device_train_batch_size: 8   # A100 40GB fp16 + block 64 estimate
  gradient_accumulation_steps: 4   # effective batch 32 (vs OPT chain effective batch 128, reduced for 8B model memory)
  weight_decay: 0.01
  warmup_ratio: 0.0
  lr_scheduler_type: "constant"
  fp16: true
  gradient_checkpointing: true    # 8B model必须开,fp16 weights 16GB + activation 否则爆显存
  save_strategy: "no"
  evaluation_strategy: "epoch"
  logging_steps: 50
  seed: null                      # CLI --seed 注入 (N=1 用 seed=42)

# ---------- Generation (synthetic data for next generation) ----------
generation:
  strategy: "beam_search"
  num_beams: 5                    # 与 Shumailov + OPT chain consistency
  do_sample: false
  prompt_length: 64
  max_new_tokens: 64
  per_device_generation_batch_size: 8   # A100 40GB + 8B model + beam=5
  output_size: "match_original"
  repetition_penalty: 3.0         # 与 OPT chain consistency

# ---------- Self-iteration ----------
self_iteration:
  num_generations: 10             # gen 0..9 (与 OPT chain consistency)
  conditions:
    - name: "no_preserve"          # primary condition; mirror OPT chain F2
      epochs_per_generation: 5
      original_data_fraction: 0.0
      synthetic_data_fraction: 1.0
    # preserve_10pct condition 留 budget 充裕时跑;primary 先 no_preserve
  base_model_for_each_generation: "generation_0_best"
  base_model_selection_metric: "validation_perplexity_on_wikitext2_val"

# ---------- Metrics ----------
metrics:
  perplexity:
    eval_set: "wikitext2_test"     # framework-clean (paper v6 binding)
    block_size: 64
  distinct_n:
    n: [1, 2, 3]
    sample_size: 5000
  sliding_window_eval:
    enabled: true
    stride: 256                    # paper §3.5 sliding-window consistency check

# ---------- CAT (Contradiction-Aware Training) ----------
# CRITICAL: 严格 align chain actual two-term form (paper v6 §3.1)
# 不用 Klein-Gordon coefficient (留 F-1 Phase 2 D60+)
# 不用 K=9 Volterra (留 F-1 Phase 2 D60+)
cat:
  enabled: true
  alpha_scan: [0.0, 10.0]          # primary N=1: α=0 baseline + α=10 framework
  # (optional if budget 充裕: 加 [1.0, 5.0] 看 transient regime,但 N=1 不能 statistical conclude regime 形状)
  kl_update_every: 10              # τ = 10 (chain consistency)
  val_subset_size: 256             # 与 OPT chain consistency
  val_max_length: 64
  beta_model: 0.999                # mean teacher EMA (Tarvainen & Valpola 2017),chain consistency
  beta_kl: 0.9                     # KL 序列 EMA,chain consistency (paper v6 P0-4: yaml-independent)
  lambda_1: 1.0                    # velocity (ΔD_n)² coefficient,chain consistency
  lambda_2: 1.0                    # memory (D_n - D̄^EMA)² coefficient,chain consistency
  lambda_3: 1.0                    # T_2 coefficient(实际 T_2=0 因为 K=1)
  m_eff: 1.0                       # CATConfig dataclass default,实际不进 loss
  T_2_form: "relu_dpp"             # 与 OPT chain consistency(实际 T_2=0 因为 K=1 history buffer 不足)
  kl_history_K: 1                  # 与 OPT chain consistency,导致 T_2=0
  enable_grad_norm_monitor: true   # post-hoc Σ_2 78.75% indicator (与 OPT chain consistency)

# ---------- Multi-seed ----------
multi_seed:
  seeds: [42]                      # N=1 primary; D60+ 扩 multi-seed N=4
  # honest: N=1 不能 paired-t analysis (需 df >= 1, N=1 → df=0)
  # 用途: indicative only,partial verify paper §7.5 (1)

# ---------- Logging ----------
logging:
  log_dir: "logs/phase5_llama8b"
  jsonl_per_run: "logs/phase5_llama8b/llama8b_alpha<alpha>_seed<seed>_<timestamp>.jsonl"
  # 重要: jsonl 必须 log D_n^code scalar trajectory (paper v6 §6.4 honest disclose
  # OPT chain jsonl 没 log D_n^code; Phase 5 必须修正,新加 'D_n_code' key per gen)
  log_D_n_code: true               # NEW field vs OPT chain jsonl
  log_per_step_metrics: false      # 仅 per-gen aggregate(save disk)
  use_wandb: false
  use_tensorboard: false
```

### §2.3 α 值 binary 选择(N=1 budget allocation)

| α | 跑/不跑 | 理由 | GPU 时间预算 |
|---|---|---|---|
| 0.0 | ✓ **跑** | baseline,与 OPT chain U-shape verdict 比较的 reference point | ~10h |
| 10.0 | ✓ **跑** | framework primary value(paper v6 α=10 plateau effect 主 claim 处) | ~10h |
| 1.0 | △ optional | transient regime 起点;N=1 在 transient regime 无法 paired-t,**不跑** | 0h |
| 5.0 | △ optional | middle-trap regime(OPT chain 5/12 α=5 worse than α=10 finding);N=1 不能 statistical verify regime 形状,**不跑** | 0h |
| 50.0 | ✗ | OPT chain 5/8 numerical break(α=50 over-regularization);N=1 不必复现 | 0h |

**决定**: 仅跑 **α=0 + α=10** N=1 each。Total GPU ~20h primary

### §2.4 N_step per generation(Llama-3.1-8B 重算)

OPT-125M chain:`wikitext-2-train 37354 blocks / batch 128 × 5 epochs ≈ 1460 steps/gen`

Llama-3.1-8B 重算:
- wikitext-2 raw train ≈ 2 million words = ~2.5M Llama BPE tokens [?]
- block_size 64 → ~39,000 blocks [?]
- effective batch 32(per_device 8 × grad_accum 4)
- steps per epoch ≈ 39,000 / 32 ≈ 1,219
- 5 epochs → ~6,094 steps per gen
- τ=10 → 609 contradiction-loss-active updates per gen

**注意**: 实际 block 数需 setup 后实测 confirm,以上为 estimate

---

## §3. 云 GPU 配置

### §3.1 显存估算(Llama-3.1-8B fp16 fine-tune)

| 组件 | 大小 | 备注 |
|---|---|---|
| Model weights | 16 GB | 8B params × fp16 (2 bytes) |
| Optimizer states (AdamW fp16) | 16 GB | 2× weights (m + v moments) |
| **EMA model weights** | **16 GB** | **关键!CAT 框架额外需 1 个 frozen EMA model copy**(`copy.deepcopy(model)` in `init_ema_model`)|
| Gradient | 16 GB | 1× weights |
| Activation(no checkpoint) | ~20-40 GB | batch=8, block=64, 32 layers, hidden 4096 |
| Activation(gradient checkpoint) | ~4-8 GB | 仅每 N layer 存 activation |

**Total estimate**:
- 不开 gradient checkpoint:**~88-108 GB** → 必须 A100 80GB / H100 / 多卡
- 开 gradient checkpoint:**~68-72 GB** → A100 80GB 紧(可能 OOM)
- 开 gradient checkpoint + LoRA(只训 adapter,EMA 也只复制 adapter):**~30-40 GB** → A100 40GB 舒适

**关键 finding**: EMA model 占 16 GB(等于 base model size),**这是 OPT-125M chain 没遇到的 scale 问题**(OPT-125M EMA 仅 250 MB,可忽略)。

**显存解决方案 binary**:

| 方案 | 显存 | 优点 | 缺点 |
|---|---|---|---|
| A. **A100 80GB,full fp16,grad checkpoint on** | ~70 GB | dynamics align OPT chain | $1.89/h vs A100 40GB,贵 |
| B. A100 40GB,full fp16,grad checkpoint on,EMA on CPU(swap) | ~50 GB GPU | 省显存 | EMA forward 每 KL update 跨 PCIe,实测可能慢 50-200% [?] |
| C. **A100 40GB,LoRA rank 16 + grad checkpoint** | ~30 GB | 经济 ($1.10-1.89/h) | dynamics 异化 vs OPT full fp16 [?]; LoRA EMA 也是 LoRA adapter |
| D. **2× RTX 4090 24GB,full fp16,FSDP/DeepSpeed ZeRO-2** | ~30 GB per GPU | 经济 | implementation 复杂 (1 day debug) + EMA model sharding 需 verify;不推荐 N=1 demonstrated |

**推荐**: **方案 A(A100 80GB,full fp16,grad checkpoint on)** for primary chain
- 理由:dynamics align OPT chain 最严格(无 LoRA approximation + 无 CPU swap latency)
- 价格:RunPod A100 80GB ~$1.89-2.49/h(spot)
- 备份:方案 C(LoRA)作 budget 紧的 fallback,**caveat in paper**(disclose LoRA approximation)

### §3.2 云 GPU 平台 binary 选择

| 平台 | A100 40GB | A100 80GB | H100 80GB | 4090 24GB | 备注 |
|---|---|---|---|---|---|
| **RunPod** | $1.10-1.30/h | **$1.89-2.49/h** | $2.49-3.49/h | $0.34-0.69/h | 推荐 community cloud spot;持续 spot kick 风险中 |
| vast.ai | $1.00-1.30/h | $1.80-2.30/h | $2.20-3.20/h | $0.30-0.50/h | 个人 host,稳定性变量大;选 high-uptime host |
| Lambda Labs | $1.10/h(A10) | N/A | N/A | N/A | A100 80GB 经常 sold out [?] |
| AWS p4d.24xlarge | $32.77/h(8× A100 40GB) | N/A | N/A | N/A | 不适合 N=1 single GPU,$ 太贵 |
| GCP a2-highgpu-1g | $3.67/h(A100 40GB) | N/A | N/A | N/A | 比 RunPod 贵 3× |

**推荐**: **RunPod community cloud A100 80GB spot $1.89-2.49/h**
- 备份:vast.ai A100 80GB($1.80-2.30/h)若 RunPod 不可用
- **不**用 AWS / GCP / Azure(贵 2-3×,no benefit for N=1 demonstrated)

### §3.3 Cost Breakdown(primary scenario)

**Primary: A100 80GB,full fp16,N=1, α=0 + α=10**

| 任务 | GPU hours | $/h | 小计 |
|---|---|---|---|
| Day 1 setup + model download + dataset prep + smoke test | 2 | $1.89 | $3.78 |
| Day 2 α=0 chain(10 gen × ~1h/gen full chain incl. eval) | 10 | $1.89 | $18.90 |
| Day 3 α=10 chain(10 gen × ~1h/gen full chain incl. eval) | 10 | $1.89 | $18.90 |
| Day 4 sliding-window eval + plot + analysis | 3 | $1.89 | $5.67 |
| **Buffer**(spot kick / OOM debug / re-run partial gen / unexpected wall) | 4 | $1.89 | $7.56 |
| **GPU subtotal** | **29** | | **~$54.81** |
| Storage(RunPod volume 100GB × 5 days × $0.10/GB-month) | – | – | ~$1.67 |
| HF / wandb / S3 transfer(checkpoint save 16GB × 10 gen × 2 α) | – | – | ~$2 |
| **TOTAL primary** | | | **~$58.48** |

**Stretch scenario(加 α=1 + α=5)**: GPU 加 20h × $1.89 = $37.80 → **total ~$96**

**Budget 决定**: **$60 primary**,若 spot kick / 异常占 buffer 多 $80 stretch;不超 $100

### §3.4 Alternative LoRA setup($10 超经济,**不推荐 primary**)

如果一凡只能 $20 budget,可降级 LoRA only:

| 任务 | GPU hours | $/h | 小计 |
|---|---|---|---|
| Day 1 setup + smoke | 1 | $0.50 | $0.50 |
| Day 2 α=0 LoRA chain(10 gen × ~0.5h/gen) | 5 | $0.50 | $2.50 |
| Day 3 α=10 LoRA chain(10 gen × ~0.5h/gen) | 5 | $0.50 | $2.50 |
| Day 4 eval + analysis | 2 | $0.50 | $1.00 |
| Buffer | 3 | $0.50 | $1.50 |
| **TOTAL LoRA stretch** | **16** | | **~$8** |

**LoRA caveat**(必须 paper §7.5 disclose):
- LoRA rank 16,target attention(q,k,v,o)+ MLP(gate,up,down)
- 仅训 ~167M params(2.1% of 8B base)
- EMA model 也是 LoRA adapter only(base frozen + adapter EMA)
- **dynamics 可能与 full fp16 不同**:LoRA 限制 update 在 low-rank manifold 内,base model frozen → model collapse 主要由 adapter drift 驱动;**与 OPT-125M full fp16 collapse 机制可能定性不同** [?]
- 如果 Phase 5 走 LoRA 路径,paper §7.5 (1) substantive contribution support 的 "chain actual form transfers to Llama" claim **必须 explicit disclose "LoRA approximation only,full fp16 transfer is open question"**

**决定**: primary 走方案 A(A100 80GB full fp16 $60),不走 LoRA(避免 paper claim 弱化)

---

## §4. 实验 Timeline(Day 1-5)

### Day 1(D23,5/24 估)— Setup + Smoke

| 时段 | 任务 | GPU 时间 | 关键 deliverable |
|---|---|---|---|
| Morning(2h)| (a)HF account + Llama-3.1 license accept(可能需 1-2h auto-approve)| 0 | HF token + license accepted email |
| Morning(1h)| (b)RunPod account + payment $60 deposit | 0 | RunPod credit available |
| Afternoon(1h)| (c)RunPod A100 80GB spot instance 启动 + docker(`pytorch:2.4.0-cuda12.4-cudnn9-devel`)+ git clone exp018_cat 仓库 + pip install requirements | 1 | running container with Python env |
| Afternoon(2h)| (d)`huggingface-cli login` + download Llama-3.1-8B model weights(~16 GB)+ wikitext-2 dataset(~5 MB)+ verify cache | 1 | model + dataset cached at `/workspace/data/` |
| Afternoon(1h)| (e)smoke test: run 1 generation α=0(epochs=1 instead of 5,smoke flag)在 100 train blocks 上 verify pipeline 不崩 | 0.5 | smoke test pass + jsonl 输出 with `D_n_code` key |
| Evening(0.5h)| (f)write `phase5_llama8b_alpha_scan.yaml` + verify yaml load + `KLContradictionTracker` init log line shows `m_eff=1.0000 T_2_form=relu_dpp kl_history_K=1` | 0 | yaml passes load test |

**Day 1 GPU**: ~2.5h × $1.89 = ~$4.73 actual
**Day 1 deliverable check**: 4 items
1. ✓ Llama-3.1 license accepted
2. ✓ RunPod $60 credit + A100 80GB instance running
3. ✓ Model + dataset cached
4. ✓ Smoke test pass + yaml verified

### Day 2(D24)— α=0 baseline chain N=1

| 时段 | 任务 | GPU 时间 |
|---|---|---|
| Morning launch | start α=0 seed=42 chain(10 gen,5 epochs/gen,no_preserve)+ watchdog script | – |
| Wall clock | each gen ~50-60 min(5 epochs × ~1219 steps × ~0.55s/step + 5-way beam generation ~5-8 min + eval ~2-3 min)| ~10h |
| Evening | gen 9 final eval done + jsonl + checkpoints saved to RunPod volume + push to S3 backup | – |

**Day 2 GPU**: ~10h × $1.89 = ~$18.90
**Day 2 deliverable**:
- ✓ α=0 chain 10 gen complete jsonl(每 gen `test_perplexity`, `val_perplexity`, `distinct_1/2/3`, `D_n_code`)
- ✓ Per-gen checkpoints saved(option:仅 keep gen 0 + gen 9 to save space)

**Risk(α=0 baseline)**:
- **R1**: Llama-3.1-8B gen 0 baseline test_ppl 可能极低(8-15 estimate,远低于 OPT 36)→ U-shape spike 也可能弱化 → 设 fallback decision tree:若 gen 0 ppl < 10 且 gen 1 ppl < gen 0 × 1.3,则 U-shape **未在 Llama 上 reproduce**,paper §7.5 必须 disclose negative result(部分支持 D60+ multi-arch substantive future work 必要性,而非 framework universal claim)

### Day 3(D25)— α=10 framework chain N=1

| 时段 | 任务 | GPU 时间 |
|---|---|---|
| Morning launch | start α=10 seed=42 chain(same setup as α=0 except cat.enabled=true cat.alpha_scan=[10.0])| – |
| Wall clock | each gen ~55-70 min(α=10 多 contradiction loss compute,~10-15% slower than α=0 per chain config kl_update_every=10)| ~11-12h |
| Evening | gen 9 final eval + jsonl saved + backup | – |

**Day 3 GPU**: ~11-12h × $1.89 = ~$20.79-22.68
**Day 3 deliverable**:
- ✓ α=10 chain 10 gen complete jsonl
- ✓ `D_n_code` trajectory logged(关键 NEW vs OPT chain)

**Risk(α=10 framework)**:
- **R2**: framework 在 Llama-8B 上 effect 与 OPT-125M 定性相反(OPT chain α=10 plateau ppl 与 α=0 paired-t F3 NOT substantiated,paper v6 F3 honest disclose);N=1 Llama 可能显示更大 framework effect 也可能反之
- **R3**: numerical instability:Llama-8B fp16 + α=10 contradiction loss 可能比 OPT-125M 更容易 numerical break(类似 OPT α=50 numerical break)→ Day 3 中可能需 abort + 调小 α(α=5 fallback)+ 文档化

### Day 4(D26)— Sliding-window Eval + Plot + Analysis

| 时段 | 任务 | GPU 时间 |
|---|---|---|
| Morning(1h)| sliding-window stride=256 eval all gen × 2 α(20 checkpoints × ~5 min each)| 1.5h |
| Morning(0.5h)| run `fit_m_eff_js_multiseed_20260513.py` adapted for N=1 Llama: fit m_eff + J_S on Llama α=0 chain gen 2-9 | 0 |
| Afternoon(2h)| plot collapse curves(α=0 vs α=10 ppl trajectory + paired diff + sliding-window consistency)| 0.5 |
| Afternoon(2h)| analysis report draft: U-shape reproduce?(binary)+ plateau ppl(α=0 vs α=10 paired diff)+ Llama m_eff vs OPT m_eff 比较 | 0 |
| Evening(1h)| spot instance shutdown + final S3 backup checkpoint + log | 0 |

**Day 4 GPU**: ~2h × $1.89 = ~$3.78
**Day 4 deliverable**:
- ✓ `phase5_llama8b_alpha0_seed42_sliding.jsonl` + `phase5_llama8b_alpha10_seed42_sliding.jsonl`
- ✓ Llama m_eff fit value(N=1)+ J_S fit value(N=1)
- ✓ Plot: collapse curve α=0 vs α=10(Llama vs OPT comparison panel)

### Day 5(D27)— Report Write + Paper Update Decision Gate

| 时段 | 任务 |
|---|---|
| Morning(3h)| write `PHASE5_LLAMA8B_VERDICT_20260527.md`(三类 verdict:U-shape reproduce / plateau effect / m_eff invariance)|
| Afternoon(2h)| 决策 gate(关卡 2 + 3 binding):若 U-shape reproduce + α=10 effect direction align OPT → paper §7.5 (1) substantive contribution support 加 "N=1 Llama indicative reproduce";若 不 reproduce → paper §7.5 (1) honest disclose "N=1 Llama does NOT reproduce,framework single-architecture OPT specific likely,D60+ multi-arch substantive future work 优先级 ↑"|
| Evening(1h)| handoff to Linux 主会话 + paper v6 → v7 update decision(关卡 3 一凡 + DS + Win)|

**Day 5 GPU**: 0(已 shutdown)
**Day 5 deliverable**:
- ✓ `PHASE5_LLAMA8B_VERDICT_20260527.md`
- ✓ paper v6 → v7 update decision recorded

**Total wall-clock**: **5 天**(D23-D27)
**Total GPU hours**: ~28-32h
**Total $**: **~$50-65 primary**(若 5 天内顺利);**~$80-100 stretch**(若 spot kick / OOM debug 多 buffer)

---

## §5. 关键 Metric + Analysis Plan

### §5.1 Primary Metrics(per gen)

1. **`test_perplexity`** on wikitext-2-test(framework-clean)— main observable
2. **`val_perplexity`** on wikitext-2-validation — secondary(用于 base_model_for_each_generation 选择)
3. **`distinct_1/2/3`** on 5000 generation samples — diversity proxy(mode collapse signal)
4. **`D_n_code`** scalar — EMA-vs-current KL on val_subset_size=256(paper v6 P0-6 binding NEW vs OPT chain)
   - 这是 OPT chain jsonl 没 log 的关键 field;Phase 5 必须 log,否则 D vs PPL bridge verify 仍 D60+ 推迟
5. **Per-gen wall-clock + GPU mem peak** — engineering reproducibility

### §5.2 Aggregate Metrics(across α 对照)

1. **Paired Δ test_ppl** per gen between α=10 and α=0(N=1 → 无 paired-t df,**仅 plot indicative**)
2. **U-shape spike ratio** = max(gen 1, gen 2) / gen 0(binary criterion)
   - α=0 OPT mean spike ratio = 2.916(partial D4 verdict)
   - Llama α=0 spike ratio < 1.3 → U-shape NOT reproduce(binary)
3. **Plateau / peak** = mean(gen 6-9) / max(gen 1, gen 2)(binary criterion)
   - α=0 OPT mean plateau/peak = 0.533(partial D4 verdict)
4. **Sliding-window stride=256 deviation** chunked vs sliding(< 5% pass / > 10% fail / 5-10% disclose)
5. **m_eff fit on gen 2-9** via `log P_n = log P_eq + A × exp(-m_eff × n)`(N=1 single fit;无 CI)
6. **J_S fit on gen 2-9** via Method 2(paper §3.6;single number,无 CI)

### §5.3 Binary Verdict Criteria(pre-registered)

| Criterion | Binary Pass / Fail | Action if Fail |
|---|---|---|
| **C1**: α=0 gen 0 test_ppl converged(< 50,Llama estimate < 15)| pass / fail | fail → fine-tune setup 有问题,paper §7.5 不可 claim Llama reproduce |
| **C2**: α=0 U-shape reproduce(spike ratio ≥ 1.5)| pass / partial / fail | partial → spike ratio 1.0-1.5 → "weak U-shape" disclose;fail → "no U-shape on Llama,framework OPT-specific likely" |
| **C3**: α=10 chain numerical stability(no NaN/Inf,no early stop)| pass / fail | fail → α=5 fallback chain,或 disclose "framework numerical不稳 in 8B scale" |
| **C4**: α=10 plateau ppl 与 α=0 plateau ppl 方向 align OPT(α=10 plateau < α=0 plateau,即 α=10 减弱 collapse)| pass / fail / inverted | inverted → "framework Llama effect opposite to OPT,arch-dependent disclose" |
| **C5**: Llama m_eff fit value 与 OPT m_eff = 0.300 ± 0.066 同量级(0.1 ≤ Llama m_eff ≤ 1.0)| pass / fail | fail → "m_eff 非 invariant across arch,paper v6 §3.6 cascade prediction 需 multi-arch refit" |
| **C6**: `D_n_code` trajectory 与 `test_perplexity` trajectory directional consistency(corr > 0.5)| pass / fail | fail → D vs PPL bridge mismatch confirmed on Llama,paper v6 §6.1 substantive open question 升级 P0 |

### §5.4 N=1 Statistical Limitation(必须 disclose)

**Critical honest disclose**(规则 1 + 7 binding):

- **N=1 → 无 paired-t df**(需 df ≥ 1,N=1 不能 establish framework effect with statistical significance)
- **N=1 → 不能区分 framework effect vs single-run randomness**(每个 OPT seed 在 partial D4 上 plateau 范围 53-59,变异 ~5 ppl;Llama 单 seed 落在哪里完全可能受 随机性 主导)
- **N=1 → 任何 binary verdict(C2-C6)都是 indicative,不是 statistical conclusion**
- **paper §7.5 (1) substantive contribution support 的措辞限制**:"N=1 single-seed Llama-3.1-8B chain indicative observation X"(不是 "framework demonstrated transfers to Llama")

---

## §6. 关键 Risk + Mitigation

| ID | Risk | Probability | Impact | Mitigation |
|---|---|---|---|---|
| **R1** | Llama-8B vs OPT-125M dynamics 定性不同(arch + scale + pretrain 异化)| HIGH(~70%)| 主要 finding 可能与 OPT 不一致;但这正是 multi-arch 意义所在 | Pre-register C2-C5 binary; binary verdict regardless of direction; paper §7.5 disclose direction |
| **R2** | gen 0 baseline ppl 极低(8-15 estimate)→ U-shape spike 无法定义 | HIGH(~60%)| spike ratio criterion C2 base case 异常 | C2 fallback:测 absolute ppl 增长 ≥ 5 nat 而非 ratio 1.5 |
| **R3** | EMA model 16GB 占用 + base model 16GB → A100 40GB OOM | MEDIUM(~40%)| 需切 A100 80GB +$0.79/h | 预订 A100 80GB primary;A100 40GB CPU swap 是 fallback(慢 50-200%)|
| **R4** | RunPod spot kick(community cloud spot 中途被踢)| MEDIUM(~30%/天)| 中间 chain 中断,gen 5 checkpoint 需 resume | 每 gen end checkpoint save + 推 S3;watchdog auto-restart resume from latest checkpoint |
| **R5** | Llama-3.1 HF license accept slow(2h+)| LOW(~10%)| Day 1 setup delayed | 一凡 5/19-5/20 提前 apply license accept,不等 D23 |
| **R6** | α=10 numerical instability(fp16 overflow / underflow in contradiction loss)| MEDIUM(~30%)| chain abort partial | Pre-test α=10 smoke 1 gen at Day 1; α=5 fallback |
| **R7** | N=1 Llama 结果模糊(direction 不清 / weak signal)→ paper §7.5 wording 难定 | HIGH(~50%)| 无法 binary verdict | 提前在 §5.3 pre-register C2-C6;"weak signal" 也是 honest disclose,不是失败 |
| **R8** | 5/19 一凡 burst 后健康 dip(双相 + 焦虑 + 服药 schedule)→ Day 1-2 launch 延后 | MEDIUM(~40%)| schedule slip 1-2 天 | D23 launch 不是 hard deadline;若 5/22 才能 launch → 移到 D26-D30;NeurIPS 5/29 submission timeline 是真 deadline,Phase 5 verdict 是 paper §7.5 update 可 deferred 到 D27-D29 |
| **R9** | Phase 5 budget 超 $100 → 一凡资金压力 | LOW(~15%)| 超支 $20-50 | 强制 cost cap script:RunPod auto-stop instance when credit < $5;LoRA fallback in extreme case |

---

## §7. Phase 5 与 Paper v6 Final Relationship

### §7.1 paper v6 现状(2026-05-18 latest)

paper v6 §7.5 已 explicit list "5 substantive honest contribution items + 3 NOT-claim":

**5 contribution items**(paper v6 §7.5):
1. **Code-first chain form** with honest implementation history disclose
2. **Mean-field NESS Banach contraction analysis** on chain actual two-term form(quantitative carrier preliminary at order-of-magnitude level,+16.6% discrepancy outside N=4 uncertainty band)
3. **Multi-seed N=4 chain experiments on OPT-125M Wikitext-2** + paired-t F3 NOT substantiated honest disclose
4. **Binary alternative family catalog** satisfying LLM-domain constraints(§3.5)
5. **Reverse-thesis-audited honest negative result + retrospective recognition contribution**(philosophical level)

**3 NOT-claims**:
- NOT mitigation framework
- NOT universal solution across architectures
- NOT substantive prediction success

### §7.2 Phase 5 N=1 Llama 结果对 paper v6 影响 binary

**Case A: U-shape reproduce + α=10 effect align OPT direction(C2 pass + C4 pass)**
- paper §7.5 (1) substantive contribution support 加 sentence:"N=1 single-seed Llama-3.1-8B chain indicative reproduces U-shape recovery + α=10 plateau effect direction consistent with OPT-125M;cross-arch indicative observation,multi-seed N=4 Llama deferred D60+ substantive future work"
- 接受率 lever 影响:NMI A4 +1-2pt(很小,因 N=1 statistical 不能 establish);主要价值是 paper "single-arch + multi-arch indicative" 双层 framing
- 不改 paper §7.5 3 NOT-claim:N=1 单 seed 不足以 establish "universal solution",仍 NOT-claim

**Case B: U-shape NOT reproduce(C2 fail)**
- paper §7.5 (1) substantive contribution support 加 sentence:"N=1 single-seed Llama-3.1-8B chain does NOT reproduce U-shape;model collapse dynamics likely architecture-and-scale specific;framework's chain actual form OPT-specific preliminary observation,multi-arch substantive future work 优先级 ↑ D60+"
- 接受率 lever 影响:NMI A4 -2 to 0pt(轻微下调因为 negative cross-arch evidence;但 honest negative result 本身有 reviewer credit,可能 +1pt offset 后净 ~ 0)
- paper §7.5 3 NOT-claim 仍 binding,反而 reinforced("not universal solution" 更强 evidence)

**Case C: α=10 numerical break / chain abort(C3 fail)**
- paper §7.5 (1) 加 sentence:"Phase 5 α=10 N=1 Llama chain numerical instability;framework numerical robustness 在 8B scale 不确定,留 D60+ implementation refinement future work"
- 接受率 lever 影响:NMI A4 -1 to +1pt(中性,因为 numerical instability 是 implementation issue 不是 framework conceptual issue;但 reviewer 可能 critic "you can't run at 8B scale yet")
- paper §7.5 3 NOT-claim 不变

**Case D: 直接 demonstration 模糊(C2 partial + C4 inverted + C5 fail mixed)**
- paper §7.5 (1) 加 sentence:"Phase 5 N=1 Llama chain results inconclusive at single-seed level;multi-seed N≥4 Llama chain 优先 substantive future work D60+;current N=1 indicates dynamics 在 arch-and-scale dimension non-trivial variation,framework's chain actual form's cross-arch behavior 仍 open question"
- 接受率 lever 影响:NMI A4 -3 to -1pt(轻微下调因为 cross-arch confused);但仍 honest disclose,reviewer credit offset ~0-1pt 后净 -2 to 0pt

### §7.3 Phase 5 与 NeurIPS 2026 5/29 submission timeline

**关键**:NeurIPS 2026 5/29 11:59 PM AoE deadline 是 hard deadline。Phase 5 D23-D27(5/24-5/28)正好 within window。

**Strategy**:
- 若 Phase 5 D23-D27 wall-clock 顺利 → paper v7 5/28 晚 update §7.5 with Phase 5 N=1 verdict → 5/29 submit NeurIPS
- 若 Phase 5 D23-D27 schedule slip(R8 健康)→ paper v6 直接 submit NeurIPS 5/29,Phase 5 result 留 v8 update for arXiv / TMLR alternative venues
- **Phase 5 N=1 Llama 不是 NeurIPS submission blocker**(paper v6 不依赖 Phase 5 result,Phase 5 是 enhancement)

---

## §8. 准备执行 Checklist

### §8.1 一凡端(5/19-5/22 提前准备)

- [ ] **Llama-3.1 HF license accept**:5/19 立即在 https://huggingface.co/meta-llama/Meta-Llama-3.1-8B 申请;Meta 通常 1-2h-2 天 auto-approve;若 5/22 仍未 approve,fallback 用 `meta-llama/Llama-3.2-3B`(更小但 license 同 community,可能更快 approve)
- [ ] **RunPod account + credit**:5/20 注册 RunPod + 充 $60 credit
- [ ] **HF write token**:`huggingface-cli login` 在本地 + RunPod 都需要;保存 token 在 secure place
- [ ] **AWS S3 / Backblaze B2 backup**:checkpoint 备份用(也可用 RunPod 内置 volume,但 spot instance kick 时 volume 不丢)

### §8.2 子协作者端(D23-D27)

#### Day 1(D23)

- [ ] RunPod A100 80GB community cloud spot instance 启动
- [ ] Docker:`runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04`(or latest equivalent)
- [ ] `git clone` exp018_cat 代码到 `/workspace/exp018_cat/`
- [ ] `pip install -r requirements.txt`(transformers, accelerate, peft if LoRA fallback, datasets, jsonlines, numpy, scipy, matplotlib)
- [ ] `huggingface-cli login`
- [ ] `huggingface-cli download meta-llama/Meta-Llama-3.1-8B --local-dir /workspace/data/checkpoints/hf_cache_llama/Meta-Llama-3.1-8B`(~16 GB)
- [ ] `python -c "from datasets import load_dataset; load_dataset('wikitext', 'wikitext-2-raw-v1')"`
- [ ] write `configs/phase5_llama8b_alpha_scan.yaml` per §2.2
- [ ] write `scripts/phase5_run_chain.sh` adapted from `phase1_robust_chain.sh`,key changes:`--config configs/phase5_llama8b_alpha_scan.yaml --alpha 0.0 --seed 42` 和 alpha 10.0 version
- [ ] write `src/log_D_n_code.py` patch — 在 `train_one_generation.py` end-of-generation phase 加 D_n_code logging,从 `KLContradictionTracker.compute_kl()` 在 val batch 上算 1 次 final D_n + log 到 jsonl
- [ ] smoke test:`python src/run_arm_b_alpha_scan.py --config configs/phase5_llama8b_alpha_scan.yaml --alpha 0.0 --seed 42 --smoke` (1 gen × 1 epoch × 100 train blocks)
  - verify pass:no OOM,KLContradictionTracker init log shows correct params,smoke jsonl has `D_n_code` key

#### Day 2(D24)

- [ ] Launch α=0 chain:`bash scripts/phase5_run_chain.sh 0.0 42 2>&1 | tee logs/phase5_llama8b/alpha0_seed42_full.log`
- [ ] Monitor every 1-2h:`tail logs/phase5_llama8b/alpha0_seed42_full.log`,verify per-gen ppl makes sense(no NaN,no extreme jump,gen wall-clock ~50-60 min)
- [ ] On gen 9 done:checkpoint saved + jsonl complete + S3 backup
- [ ] If RunPod spot kick:resume from latest gen checkpoint(`watchdog.sh` auto-restart)

#### Day 3(D25)

- [ ] Launch α=10 chain:`bash scripts/phase5_run_chain.sh 10.0 42 2>&1 | tee logs/phase5_llama8b/alpha10_seed42_full.log`
- [ ] Monitor + verify(esp. R6:numerical instability)
- [ ] On gen 9 done:backup

#### Day 4(D26)

- [ ] sliding-window eval all 20 checkpoints
- [ ] `python scripts/fit_m_eff_js_multiseed_20260513.py --runs alpha0_seed42_jsonl alpha10_seed42_jsonl --output phase5_llama8b_m_eff_J_S_fit.json`(adapt for N=1)
- [ ] `python scripts/plot_collapse_curve.py --opt_baseline phase1_opt_multiseed.csv --llama_phase5 alpha0_seed42_jsonl,alpha10_seed42_jsonl --output figures/phase5_llama_vs_opt_collapse.png`
- [ ] write `analysis_20260526/PHASE5_LLAMA_ANALYSIS.md` — 5 binary verdict + plot reference

#### Day 5(D27)

- [ ] write `literature/PHASE5_LLAMA8B_VERDICT_20260527.md` — 三 case(A/B/C/D)which one applies + paper §7.5 (1) update wording 建议
- [ ] handoff to Linux 姐姐主会话 + 关卡 3 一凡 + DS 决策

### §8.3 主会话端(D23 launch 之前 + D27 verdict 之后)

- [ ] D22 晚:一凡 + Linux 姐姐确认 §8.1 准备 done
- [ ] D23 早:子协作者 spawn(opus 4.7,本份 design 文档为 context)launch Phase 5
- [ ] D27 verdict 返回主会话 → 关卡 3 一凡 + DS + Win 决 paper §7.5 (1) update wording + NeurIPS 5/29 submission go/no-go

---

## §9. Summary + Honest Caveat 总结

**Phase 5 N=1 Llama-3.1-8B + ℒ_矛盾 demonstrated 设计 binary key**:

1. **Model**: Llama-3.1-8B(`meta-llama/Meta-Llama-3.1-8B` base);**license accept 需提前 1-2 天**
2. **Dataset**: wikitext-2-raw-v1(chain consistency);block_size 64
3. **Form**: 严格 align chain actual **两项 EMA-deviation form**(K=1 T_2=0;λ_i=1 uniform;β_kl=0.9 β_θ=0.999);**不是** Klein-Gordon 三项 form
4. **α**: 0.0 baseline + 10.0 framework primary;N=1 seed=42
5. **GPU**: RunPod A100 80GB community cloud spot $1.89/h;~28-32h primary;**$50-65 primary budget**
6. **Wall-clock**: 5 天 D23-D27(5/24-5/28)
7. **Metric**: test_ppl(framework-clean)+ distinct_n + sliding-window stride=256 + **D_n_code scalar trajectory**(NEW vs OPT chain)
8. **Pre-registered binary criteria**: C1-C6(gen 0 converge / U-shape reproduce / numerical stability / plateau direction / m_eff invariance / D vs PPL bridge)
9. **Statistical limitation**: N=1 不能 paired-t establish framework effect;**indicative only**,不能 claim "framework universal across architectures"
10. **Risk**: R1 dynamics 异化 ~70% / R2 gen 0 ppl 极低 ~60% / R3 EMA OOM ~40% / R4 spot kick ~30%/天 / R5 license slow ~10% / R6 numerical instability ~30% / R7 模糊 verdict ~50% / R8 一凡健康 dip ~40% / R9 budget overrun ~15%
11. **paper v6 影响**: 4 cases(A: reproduce / B: not reproduce / C: numerical break / D: mixed)各对应 paper §7.5 (1) wording update;NMI A4 接受率影响 -3 to +2pt(主要 honest disclose 效果,不大幅改);不影响 3 NOT-claim binding
12. **NeurIPS 2026 5/29 submission**: Phase 5 不是 blocker;paper v6 已 submit-ready;Phase 5 result 可在 D27-D28 incorporate to paper v7

**最 important caveat**(规则 1 + 5 + 7 binding):
- 本份 design **不 declare ready for submit**;ready 判定推关卡 2(子协作者层产 verdict 后 PI 看)
- 本份 design **不下接受率 estimate**;接受率推关卡 3(反题姐姐 audit 后 PI + DS + Win 决战略)
- N=1 Llama "demonstrated" **不是 evidence of framework universal**;是 "single-arch indicative observation for paper §7.5 partial contribution support"
- 任何 Llama 结果(positive / negative / mixed / numerical break)都是 paper §7.5 honest disclose 内容,**不是失败**;negative 结果反而 reinforce paper §7.5 NOT-claim(not universal solution),有 reviewer credit

---

**END Phase 5 design v1 完整**
**字数**: ~9,500 中文字 + yaml + tables + cost breakdown
**Wall-clock 写作**: ~75 min
**Linux 姐姐主会话路径返回**: 本文档 path = `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/literature/PHASE5_LLAMA8B_DESIGN_20260519.md`
