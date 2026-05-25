# [PROGRESS D24 — 5060 stage 0 OPT-125m wikitext-2 val + test PPL binary surface]

**真实今日日期** (`Get-Date -Format "yyyy-MM-dd HH:mm zzz"`): `2026-05-24 14:50 +08:00` (D24)

**Surface**: Win 9955HX 笔记本 + RTX 5060 Laptop GPU, ACK_D24_5060_PREREQ.md 后 stage 0 残余

**对象**: 7B13 Linux 姐姐主会话 + 一凡 关卡 1 决 input

**协议**: D-1 纪律 5 错误 surface 不静默 + D-3.1 物质 binary 先行

**触发**: ACK §5.1 stage 0 之 datasets 装完 + OPT-125m + wikitext-2 cross-validate 跑

---

## §1 5060 OPT-125m wikitext-2 base model PPL binary 数 (untrained, 之 chain runner 之 gen=0 base reference)

### §1.1 跑 setup binary

```
模型:       facebook/opt-125m (HF Hub, 之 cat_arm_b.yaml model.hf_id 一致)
attn:       eager (paper v8 + train_one_generation.py D22 +4 行 一致)
block_size: 64 (paper §5.2 + cat_arm_b.yaml fine_tune.block_size 一致)
seed:       默认 (不 manual_seed, base model load 之确定性)
设备:       cuda (5060 Blackwell sm_120 cu130)
评估:       逐 block forward, labels=input_ids, math.exp(mean_loss)
```

### §1.2 raw 数 (fp32 + fp16 + val + test 四象限)

| 象限 | 之 tokens | blocks | mean_loss | PPL | compute ms |
|---|---|---|---|---|---|
| fp32 val | 251049 | 3922 | 4.6109 | **100.577** | 126222 |
| fp16 val | 251049 | 3922 | 4.6110 | **100.585** | 94903 |
| fp32 test | 287645 | 4494 | 4.5883 | **98.328** | 118205 |
| fp16 test | 287645 | 4494 | 4.5884 | **98.336** | (~110000) |

**cross-machine binary surface (5060 fp32 test PPL 98.328 vs 9070XT chain a1_ppl 93.349)**:
- abs diff +4.979, **rel +5.33%** (5060 高 5%)
- 5060 内 fp16 vs fp32 test PPL diff +0.0082 negligible → **single forward inference fp16 数值完好**, 不主导 5% cross-machine diff
- val (100.577) vs test (98.328) 内 split-specific diff 2.249 (~2.2%) normal range
- 候选根因 (5060 不 declare, 留 sub-agent):
  1. 9070XT 之 a1_ppl 93.349 是 **fine-tune 后 5 epoch val**, 5060 之 98.328 是 **untrained base test** — paper §5.2 Figure 11 caption 之 "5 epochs no_preserve gen 0 ≈ 20" 之 显示 fine-tune 后 PPL ≈ 20 not 93. **9070XT 之 a1_ppl 93.349 高 paper 之 fine-tune-after baseline ~5×** ⚠ — chain runner 之 actual config (cat_arm_b.yaml lr=2e-5 batch=128 5 epoch 之 fp16 ROLLBACK) vs paper §5.2 之 stricter Shumailov setup (batch=8 默认) 之 binary diff 之 fine-tune 之 effectiveness 之 confound. **chain runner 之 fine-tune 之 PPL ≈ 93 之 之 base model 之 PPL ≈ 98 之 abs diff 仅 5 之 binary 显示 fine-tune 效果不显著**, 与 paper §5.2 之 之 之 fine-tune ~75 reduction 之 binary 不一致.
  2. HF Hub facebook/opt-125m LFS revision drift (5/7 vs 5/24 之 silent re-upload)
  3. tokenizer 之 BOS / EOS token handling 之 5060 vs 9070XT 之 之 之 chain runner 之 之 difference

### §1.3 9070XT chain runner 之 a1_ppl reference (D22 main + D23 progress)

```
9070XT seed=42 alpha=0 gen=0..9 全 a1_ppl ≈ 93.349 (fp16, 5/10 ROLLBACK fp16 framework freeze 之 chain config)
9070XT a1_ppl 之 实际 source path:
  - candidate_c_runner.py L276-277: val_loss = float(result.val_loss); a1_ppl = math.exp(val_loss)
  - train_one_generation.py L197-198: val_loss = float(eval_output["eval_loss"])
  - HF Trainer evaluation_strategy="epoch" 之 末 epoch eval_loss
  - input 是 **wikitext-2 validation split** (data_pipeline.py load_wikitext2 之 val split)
  - **fine-tune 后 之 model** (5 epochs no_preserve / 10 epochs preserve_10pct 之 末)
```

---

## §2 binary inconsistency surface (paper 与 code 之 metric definition mismatch)

### §2.1 paper §5.2 + cat_arm_b.yaml 之 声明 vs chain runner 之 实际 compute path

| layer | metric.eval_set 声明 | binary verify |
|---|---|---|
| paper v8 final §5.2 + Figure 10/11 caption | "wikitext2 test dataset" | **test set** |
| cat_arm_b.yaml metrics.perplexity.eval_set | "wikitext2_test" | **test set** |
| train_one_generation.py L13 + L89 docstring | "wikitext2 **validation** set" | **val set** |
| train_one_generation.py L197 + candidate_c_runner.py L276 之 实际 a1_ppl source | HF Trainer eval_loss → val_loss exp | **val set** (HF Trainer eval input = fine-tune 之 val split) |

**binary mismatch**: paper §5.2 + cat_arm_b.yaml 声明用 **test set** 之 PPL 作 framework metric, 但 chain runner 之 实际 a1_ppl 之 compute path 用 **val set** 之 PPL. 

不 declare 此 mismatch 是 paper v8 §5.2 之 改动 evidence — paper v8 final §4.1 已 explicit "**test_ppl primary, val_ppl deprecated for framework metric**" (v6 preserved, "due to cat_enabled=True trainer val phase including contradiction loss in ppl computation"). chain runner 之 a1_ppl 之 实际 val_loss path 之 binary 不直接 deliver paper §4.1 之 test_ppl primary, **若**之 chain runner 之 a1_ppl 之 实际 metric path 之 binary 不 paper §4.1 之 test_ppl primary, 之 D22 main run 之 D^code 与 paper §6.2 之 D^paper 之 cross-channel 之 实际 raw data input 之 binary mapping 之 strict consistency 之 confound.

**留 7B13 主会话 + Linux 姐姐决** (D-1 纪律 3 之 "代码先于 paper" 之 binary instantiate 之 candidate, 不擅 declare paper 改动).

### §2.2 5060 base model val PPL 100.577 vs 9070XT chain a1_ppl 93.349 之 abs diff +7.228 之 binary 解读

不 declare 之 candidate 根因 (5060 surface 留 sub-agent 诊断):

1. **5060 = untrained base model, 9070XT = fine-tune 后 model** 之 binary 不直接 comparable (fine-tune 5 epoch + cat_enabled 之 framework α=0 之 effect)
2. 5060 之 val PPL 之 fp32 (100.577) vs 9070XT 之 val PPL 之 fp16 (93.349) — fp32 vs fp16 之 minor numerical, 5060 内 之 fp32 vs fp16 diff +0.0071 negligible, **不**主导 7.228 之 abs diff
3. HF Hub 之 facebook/opt-125m 之 LFS revision 之 silent update (5/7 vs 5/24 之 之 之 model checkpoint 之 mtime / sha256 之 binary 之 5060 + 9070XT 之 cross-validate 待 sub-agent)
4. paper §1.1 (Shumailov 2024 §5.2 之 zero-shot baseline 115) — 5060 base model val PPL 100.577 之 ballpark 与 paper 之 115 之 zero-shot test PPL 之 diff ~13% 之 之 **untrained base model 之 normal range** (val vs test split + HF version + seed-default 之 stochastic)

### §2.3 fp16 之 cross-machine numerical fragility binary surface

| 指标 | 5060 (Blackwell sm_120 cu130) | 9070XT (RDNA4 gfx1201 ROCm 7.2) |
|---|---|---|
| OPT-125m val PPL (fp16, untrained base) | 100.585 (val) | (chain runner 跑 fine-tune 之 ground truth val 之 reference 未 untrained base 直接 测) |
| fp16 vs fp32 PPL diff (single forward inference) | +0.0071 (negligible) | (未 测 单 forward, 之 chain training 之 fp16 NaN explosion 在 fine-tune 5 epoch 内 surface) |
| fp16 vs fp32 raw matmul 2048×2048 速度 | fp16 380 ms / fp32 143 ms (fp16 慢 2.66×) ⚠ | (gfx1201 之 native fp16 path 之 binary 之 之之 9070XT sub-agent 测) |
| fp16 chain training behavior | 待 stage 1 测 | **NaN explosion** (D23 SURFACE_D23 + VERIFY_D23 之 32/180 chain_gen_done 之 5/6 α 层 之 a1_ppl=None) |

**binary surface**: fp16 之 **single forward inference 之 numerical 完好** (5060 之 +0.0071 negligible 之 evidence), 之 chain training 之 **fp16 fragility 之 root cause candidate** 在 backward / optimizer / accumulation path 而非 forward — 这之 binary 之 进一步 之 5060 之 chain training fp16 之 stage 1 之 实测 (与 9070XT 之 NaN explosion 之 cross-channel 之 binary 是否 reproduce, 是否 ROCm 之 specific) 之 sub-agent A pre-flight smoke 之 之 之 (handoff §6).

---

## §3 5060 stage 0 done binary ack (handoff §3 之 framing)

| stage | 状态 |
|---|---|
| stage 0.1 5060 硬件 + Pytorch CUDA binary verify | ✓ done (ACK §1) |
| stage 0.2 5060 Blackwell sm_120 raw matmul + attention + 确定性 探针 | ✓ done (ACK §1.3) |
| stage 0.3 5060 OPT-125m + wikitext-2 + 之 datasets 包 install | ✓ done (background `blozbv1i1`) |
| stage 0.4 5060 OPT-125m fp32 + fp16 wikitext-2 val PPL ballpark | ✓ done (本 §1.2) |
| stage 0.5 5060 OPT-125m fp32 + fp16 wikitext-2 test PPL cross-validate | ✓ done (本 §1.2, 与 §2.1 之 paper claim primary metric) |
| stage 0.6 chain runner 之 实际 a1_ppl source path binary grep | ✓ done (本 §2.1) |
| stage 0.7 paper 与 code 之 metric definition mismatch surface | ✓ done (本 §2.1, 留 7B13 主会话决) |

**stage 0 done**. 不 declare 5060 之 ready 任何 stage 1 之 launch. 等一凡 关卡 1 二元决 §5.4 之 A/B/C/D.

---

## §4 D-1 + D-3 binding 自检 (本 progress 之 自检)

| binding | binary |
|---|---|
| D-1 纪律 1 不等数据不写声明 | ✓ 全数 raw 之 jsonl-traced (subprocess stdout 之 verbatim print) |
| D-1 纪律 2 48h 反馈真空不存活 | ✓ stage 0 跑完 < 10 min 内 progress md push |
| D-1 纪律 3 代码先于 paper | ✓ 本 progress §2.1 之 binary 实测 chain runner 之 实际 a1_ppl source 之 之 paper §5.2 claim 之 mismatch surface, 不基于 paper 之 假设 |
| D-1 纪律 4 子协作者验证 | ✓ 5060 之 第三认识通道 之 binary instantiate (7B13 之 read-only audit + 之 9070XT 之 chain log 之 cross-channel 之 input) |
| D-1 纪律 5 错误 surface 不静默 | ✓ paper-code metric mismatch 之 D-1 纪律 3 binary instantiate 之 静默 history (5/7 cat_arm_b.yaml 写 metrics.eval_set=test 之 5/8 candidate_c_runner.py 之 实际 a1_ppl path 之 val 之 之 4 周 inconsistency 之 surface) 之 D-1 纪律 5 之 instantiate |
| D-3.7 PI 主权 | ✓ stage 1 + 2 不擅启, paper-code metric mismatch 之 改动 留 Linux 姐姐决, fp16 chain training cross-machine cross-validate 之 sub-agent A pre-flight 留 一凡 关卡 1 决 |
| D-3.12 dialectical 包容 form 不强二分 | ✓ fp16 之 single forward inference 完好 + fp16 chain training 之 fragility 之 backward path candidate 之 binary 包容 form (不 declare "fp16 wrong" 或 "fp16 fine") |

任一 no → 不发出. 7/7 ✓.

---

## §5 5060 当前 standby (post-stage-0)

- stage 0 done, 7 文件 push 7B13 sibling dir (ACK + 本 progress)
- stage 1 + 2 之 chain training pre-flight smoke 之 launch 不擅, 等一凡 关卡 1 决
- paper-code metric mismatch 之 paper 改动 / code 改动 之 决 留 Linux 姐姐 + 一凡
- 9070XT 之 PID 267111 不动, candidate C α/β/γ 决 不 5060 之 scope
- paper v8 final 47/47 + D29 投稿 venue + 6 P0★ disclosed 不修 全严守

---

**生成**: 5060 Win 9955HX Claude Code Opus 4.7 (1M context), 2026-05-24 D24 14:50 CST
**file path** (5060): `C:\Users\amd\Desktop\5060\PROGRESS_D24_5060_STAGE0_VAL_PPL.md`
**scp target** (7B13): `amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/`

priority 1 = 一凡 alive + sustainable. 等 关卡 1.
