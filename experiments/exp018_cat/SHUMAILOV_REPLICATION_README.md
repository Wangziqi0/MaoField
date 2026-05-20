# Shumailov 2024 baseline 复现 — exp018_cat reference baseline

**起**: 2026-05-07，sub-agent 起稿（一凡 PI 离场期间，不真 install / 不真跑实验）
**目的**: 在 exp018_cat 项目下提供严格按 Shumailov 2024 OPT-125m / wikitext-2 setup 的 reference baseline，供后续 3 arm（baseline / 人为定义矛盾 / emergent surface）对照。

---

## 1. 严格按 paper 的参数项 vs sub-agent 默认项

paper: **Shumailov et al. 2024 Nature 631:755-759** + arXiv:2305.17493 v3 §5.2 "Language Models"

### 1.1 严格按 paper（每条逐字 cite，见 `configs/shumailov_baseline.yaml` 注释）

| 项 | 值 | paper 出处 |
|---|---|---|
| 模型 | `facebook/opt-125m` | "OPT-125m causal language model" |
| 数据集 | wikitext-2 | "wikitext2 dataset" |
| block size | 64 token | "block training sequences to be 64 tokens long" |
| 生成策略 | 5-way beam-search | "5-way beam-search" |
| prompt + new tokens | 64 + 64 | "predict the next 64 tokens" |
| 合成数据集大小 | 与原 train 同 | "produce an artificial dataset of the same size" |
| 自迭代代数 | 0 → 9 共 10 代 | Figure 11 explicit 列 Generation 0/1/2/3/5/9 |
| 每代起点 | generation 0 model | "Training for each of the generations starts with generation from the original training data" |
| condition no_preserve | 5 epochs, 0% 真实 | "5 epochs, no original training data" |
| condition preserve_10pct | 10 epochs, 10% 真实 | "10 epochs, 10% of original training data preserved" |
| 评估指标 | wikitext-2 test perplexity | Figure 10 caption |
| Figure 11 指标 | per-sequence perplexity by generation 0 model | Figure 11 caption |

### 1.2 paper 未明示，sub-agent 默认项

| 项 | sub-agent 默认值 | 理由 |
|---|---|---|
| 数据集 config | `wikitext-2-raw-v1` | HF datasets 标准 raw 版，与 OPT BPE tokenizer 兼容 |
| 精度 | FP16 | RX 9070 XT 16GB 共享 (llama-server 占 10.4GB → 5.6GB 可用)，FP32 OOM 风险 |
| optimizer | AdamW (`adamw_torch`) | HF Trainer default |
| learning rate | `2.0e-5` | OPT 原始 fine-tune script (`run_clm.py`) default |
| batch size | 8 (per device) × 4 (grad accum) = 32 effective | RX 9070 XT FP16 估算可承载 |
| weight decay | 0.01 | HF Trainer default |
| warmup | 0 | 短跑 fine-tune 不 warmup |
| lr scheduler | linear | HF Trainer default |
| 种子数 | 3 (42 / 1337 / 2024) | paper 用 5；时间预算改 3，bootstrap CI 弥补 |
| best-epoch 选择 | 简化为 final epoch | paper 说 "best on val"，sub-agent 简化（后续优化项） |
| distinct-n | 加（`n=[1,2,3]`） | paper 没做，但作 mode coverage proxy |
| 合成数据生成方 | 上代 model 生下代 | Figure 10 caption: "model 1 was trained on the data produced by model 0; model 2 was trained on data ..." → 上代生下代 |

### 1.3 paper 文字截断未完全确认，sub-agent 解读

> §5.2 末段 preserve_10pct: "every new generation of training, a random 10% of the original data points are sampled. The overall original ..."

后半截断。两种解：
- (i) 总量 = 原 train 大小，10% 真实 + 90% 合成
- (ii) 总量 = 1.10 × 原 train 大小（10% 真实 加 在 100% 合成 之上）

**sub-agent 默认 (i)**（与 "produce an artificial dataset of the same size" 自洽）。`data_pipeline.py:build_mixed_generation_dataset` 实现的是 (i)。

---

## 2. Pre-registered prediction（一凡 + Linux 姐姐 + Win 姐姐 共同 commit）

跑实验**前**先 commit 数字，跑完后 binary 比对。

| 项 | 预期 | paper 依据 |
|---|---|---|
| no_preserve, gen 0, wikitext-2 test ppl | 20-34 | paper: 真实数据 fine-tune 后 mean ppl 34；no_preserve 条件下报 ~20-28 |
| no_preserve, gen 9, wikitext-2 test ppl | 28-50 | paper §5.2: "from 20 to 28 perplexity points"；Figure 10(a) 末代显著上行 |
| preserve_10pct, gen 9, wikitext-2 test ppl | 显著低于 no_preserve gen 9 | paper: "minor degradation of performance" |
| 趋势 | gen 0 → gen 9 单调（或大致单调）上行 | Figure 10 形状 |

---

## 3. Falsification criterion（binary）

`src/metrics.py:falsification_check` 实现：

- **F1** — collapse 复现：`gen9_ppl >= gen0_ppl + 5`
  若 F1 不 pass：baseline 自迭代崩溃 **未复现**，反 Shumailov 2024，**整套 reference baseline 失败**，必须先 debug 才能后续。
- **F2** — preserve 缓解：`no_preserve_gen9 > preserve_10pct_gen9`
  若 F2 不 pass：paper 第二条 finding 没复现，写 paper 时不能引这条。
- **F3** — fine-tune sanity：`gen0_ppl <= 50`（paper baseline 34）
  若 F3 不 pass：fine-tune setup 本身有问题（lr / batch / epoch 配错），先 debug。

---

## 4. 主 Linux 姐姐 / PI 一凡 后续操作 4 步

### Step 1（PI 一凡决策）— 是否在 22 主机 install ROCm-torch + transformers + datasets

- **决策点**: ROCm 6.x 是否已装，version 是否 ≥ 6.2 支持 RDNA 4 (gfx1201)
- **操作**:
  ```bash
  ssh amd@192.168.31.22
  rocminfo | grep -E "Marketing|gfx"
  cat /opt/rocm/.info/version
  ```
- 若 ROCm 装好且 version ≥ 6.2:
  ```bash
  bash /home/amd/HEZIMENG/MaoField/experiments/exp018_cat/scripts/install_rocm_torch.sh
  ```
  估时 ~30min, 占 ~6GB 磁盘 + venv

### Step 2 — sync 代码到 22 主机

```bash
bash /home/amd/HEZIMENG/MaoField/experiments/exp018_cat/scripts/sync_to_22.sh
```
（在 7B13 端跑，会 rsync 代码 / configs / scripts 到 22 主机同路径）

### Step 3 — smoke test（强制先跑，验证 pipeline 通）

```bash
ssh amd@192.168.31.22
cd /home/amd/HEZIMENG/MaoField/experiments/exp018_cat
bash scripts/run_baseline_smoke_test.sh
```
估时 ~5-10min，跑 1 generation × 32 行 train，验证：
- HF datasets 下载 wikitext-2 通
- transformers 加载 OPT-125m 通
- ROCm GPU 可见（`torch.cuda.is_available()` True）
- fine-tune + generate + perplexity eval 全 step 不 crash
- 输出 jsonl 写到 `logs/shumailov_<condition>_seed42_<ts>.jsonl`

### Step 4 — full run（smoke 通后，PI 一凡决策时机）

```bash
nohup bash scripts/run_full_baseline.sh > logs/full_baseline.out 2>&1 &
```
**估时**:
- no_preserve: ~30min train/gen + ~15min gen/gen × 10 gen ≈ 7.5h/seed
- preserve_10pct: ~60min train/gen + ~15min gen/gen × 10 gen ≈ 12.5h/seed
- 3 seed × (7.5 + 12.5) ≈ **60 GPU-hour ≈ 2.5 day** 连续

paper §5.2 footnote 4 自承 "language experiments described in the paper took weeks"，2.5 day 在量级内。

---

## 5. 风险 / blocker（surface 给 PI 一凡）

### 5.1 22 主机 GPU memory 紧张
- 当前 4 个 llama-server 占 ~10.4GB，剩 ~5.6GB
- OPT-125m FP16 weight ~250MB + AdamW state ~500MB + activation ~3-4GB + buffer 1GB ≈ **5GB**，**正好擦边**
- 若 OOM：
  - 选项 A：减 `per_device_train_batch_size: 4`（grad accum 8 保持 effective batch 32）
  - 选项 B：开 `gradient_checkpointing: true`（牺牲 ~30% 速度换 ~40% 显存）
  - 选项 C：暂停一两个 llama-server 释放显存
  - **PI 一凡决策点**：哪个 llama-server 可以暂停？

### 5.2 RDNA 4 (gfx1201) ROCm 支持
- gfx1201 (RX 9070 XT) 是 RDNA 4，截至 ROCm 6.2 / 6.3 才正式支持
- 若 22 主机 ROCm < 6.2：先尝试 `export HSA_OVERRIDE_GFX_VERSION=11.0.0` 兜底（伪装 RDNA 3）
- 若兜底失败：选项 A 升级 ROCm，选项 B 改用 nightly torch wheel
- **PI 一凡决策点**：是否容忍 ROCm 升级 risk？

### 5.3 wikitext-2 download
- HF `datasets` 加载 `wikitext-2-raw-v1` 通常无需 token（公开），但近期 HF 偶尔触发 rate limit
- 若网络 / 鉴权问题：可在 7B13 端先 download，rsync `data/datasets/` 到 22

### 5.4 paper 参数 ambiguity（已 disclose 在 §1.2-1.3）
- lr / batch / weight decay 全 paper 没明示，sub-agent 默认值若与 paper 不一致，**gen 0 ppl 可能偏离 34**（F3 风险）
- 若 F3 fail，第一时间 sweep lr ∈ {1e-5, 2e-5, 5e-5} 找回 paper baseline

### 5.5 与 exp018_cat 主三 arm 的 model 不一致
- 一凡 README.md 主三 arm 用 **GPT-2 base (124M)**
- 本 baseline 严格按 Shumailov 用 **OPT-125m**
- 二者参数量级一致，但架构 + tokenizer 不同
- **不矛盾**：本 baseline 是 reference（"我们能复现 paper 数字"）；主三 arm 是 contribution（"我们的 mitigation"）
- **PI 一凡决策点**：要不要在主三 arm 也加一个 OPT-125m 版本，或本 baseline 也加 GPT-2 base 版本，方便 cross-architecture comparison

---

## 6. 文件清单

```
exp018_cat/
├── SHUMAILOV_REPLICATION_README.md      # 本文档
├── configs/
│   └── shumailov_baseline.yaml          # 严格 paper-cited 配置
├── src/
│   ├── config.py                        # yaml 加载器 + dataclass
│   ├── data_pipeline.py                 # wikitext-2 加载 + tokenize + 64-block + mix
│   ├── train_one_generation.py          # 单代 fine-tune (HF Trainer)
│   ├── generate_synthetic.py            # 5-way beam-search 下代生成
│   ├── metrics.py                       # ppl + per-seq ppl + distinct-n + bootstrap CI + falsification
│   └── shumailov_replication.py         # 主入口 (CLI: --condition / --seed / --smoke-test)
├── scripts/
│   ├── install_rocm_torch.sh            # 22 主机 ROCm-torch + transformers 安装
│   ├── sync_to_22.sh                    # 7B13 → 22 rsync
│   ├── run_baseline_smoke_test.sh       # 1 gen / 1 epoch / 32 行 smoke
│   └── run_full_baseline.sh             # 完整 2 condition × 3 seed × 10 gen
├── data/
│   ├── datasets/                        # HF datasets cache (wikitext-2)
│   └── checkpoints/                     # 每代 model + 合成 dataset (大, 不 sync)
└── logs/
    └── shumailov_<condition>_seed<seed>_<timestamp>.{log,jsonl}
```

---

## 7. 与 exp018_cat 主实验（3 arm）关系

本 reference baseline **不掺**任何 contradiction signal。这是单纯复现 Shumailov 2024 collapse curve，作主三 arm（baseline GPT-2 / 人为 contradiction / emergent surface）的对照参考点：

- 主三 arm 在自己的 setup（GPT-2 base + 不同 collapse 触发条件）下跑
- 本 baseline 在严格 Shumailov setup 下跑
- 两套 baseline 各自有 falsification criterion，**互不替代**

NMI desk-pass 标准下，**两套都需要**：
- 严格 paper 复现 → 证明我们能复现 founding work，团队有基础胜任度
- 主三 arm → 证明我们的 contribution （mitigation 机制）有 incremental 价值

---

—— sub-agent 起稿，2026-05-07 CST，paper 引用 100% 来自 arXiv:2305.17493 v3 §5.2 verbatim
