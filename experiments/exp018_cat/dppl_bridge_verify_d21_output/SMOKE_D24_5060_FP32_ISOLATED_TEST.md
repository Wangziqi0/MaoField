# [SMOKE D24-D25 — 5060 fp32 isolated fine-tune test 完成 + a1_ppl 36.536 落 paper §4.6 ballpark]

**真实今日日期** (`Get-Date`): `2026-05-25 09:05 +08:00` (D25 周一)

**Surface**: Win 9955HX 5060 — DS plan step 2 之 fp32 isolated test 完成

**对象**: 7B13 Linux 姐姐主会话 + PI 一凡 + DS 关卡 3 反题三方决 input

**协议**: D-1 纪律 1 jsonl-traced + D-3.7 PI 主权 (5060 不擅 declare verdict)

**触发**: D24 17:35:51 launch (path A 之 downgrade transformers 5.7.0 → 4.49.0 之后), D25 02:11:57 完成, wall-clock 30862.6 秒 = 8h34min

---

## §1 setup binary

### §1.1 cat_arm_b_fp32_5060.yaml fork diff vs main (binary 仅 2 处)

```diff
@@ -51,2 +51,2 @@
-  dtype: "float16"     # 5/10 ROLLBACK fp32→fp16: caveat 4 framework freeze D3-D4
+  dtype: "float32"     # D24 5060 fp32 isolated test (PI + DS 关卡 1 决)

@@ -94,1 +94,1 @@
-  fp16: true                  # 5/10 ROLLBACK fp16: framework freeze D3-D4 binding
+  fp16: false                 # D24 5060 fp32 isolated test
```

其他配置 100% 与 cat_arm_b.yaml main 一致：lr 2e-5 / batch 128 / grad_accum 1 / 5 epoch no_preserve / wikitext-2-raw-v1 block 64 / seed 42 / α=0 (CAT disabled)。

### §1.2 5060 source file sha256 跨机 ≡ 7B13 (commit 76edbb3 / 1836d6a / 0603922)

| file | sha256 | commit |
|---|---|---|
| train_one_generation.py | e83d1ee2... | 76edbb3 |
| candidate_c_runner.py | 5a922566... | 1836d6a |
| multi_layer_hook.py | f126b274... | 0603922 |
| cat_arm_b.yaml | 9af92794... | (main) |
| config.py / data_pipeline.py / 其他 src | 全 跨机 ≡ | 各自最新 |

### §1.3 5060 env post-downgrade (DS path A step 1)

| 包 | 5060 | 9070XT .venv | 一致 |
|---|---|---|---|
| transformers | **4.49.0** | 4.49.0 | ✓ |
| tokenizers | 0.21.4 | 0.21.4 | ✓ |
| accelerate | 1.13.0 | 1.13.0 | ✓ |
| safetensors | 0.7.0 | 0.7.0 | ✓ |
| TrainingArguments params n | 132 | 132 | ✓ |
| torch | 2.11.0+cu130 | 2.12.0+rocm7.2 | backend diff (hardware constraint, 不可改) |
| datasets | 4.8.5 | 2.21.0 | major version diff (5060 D24 fresh / 9070XT D21) |
| numpy | 2.4.2 | 1.26.4 | major version diff |

datasets + numpy diff 候选 confound, 但 不主导 chain fine-tune behavior (HF datasets API surface 4.x vs 2.x 后向兼容)。

---

## §2 raw 数 (jsonl-traced verbatim)

### §2.1 chain_gen_done event 之 关键字段

```json
{
  "event": "chain_gen_done",
  "seed": 42, "alpha": 0.0, "gen": 0,
  "a1_ppl": 36.53597375534226,
  "val_loss": 3.598297357559204,
  "n_tokens_train": 2390656,
  "n_tokens_eval": 16384,
  "elapsed_sec": 30862.590396165848,
  "caveats": ["a6_gen0_self_reference_zero_list_expected"]
}
```

- **a1_ppl = 36.536** (math.exp(3.598297) = 36.531, 与 candidate_c_runner.py L276-277 path 之 binary 一致)
- **val_loss = 3.598** (HF Trainer evaluation_strategy="epoch" 之 末 epoch eval_loss, input 是 wikitext-2 validation)
- elapsed 30862.6 秒 = 8h34min (5060 fp32 + batch 128 + 5 epoch)
- n_tokens_train 2,390,656 = 5 epoch × 478K token ✓
- n_tokens_eval 16,384 = val 256 example × 64 block ✓
- caveat 1 个 (a6 gen=0 没 EMA reference, per design)

### §2.2 multi-layer instrument (a2 / a3 / a6)

- **a2_anisotropy 12 层全 finite**: 0.7349 → 0.7441 → 0.7748 → 0.7996 → 0.8304 → 0.8593 → 0.8828 → 0.8955 → 0.9065 → 0.9116 → 0.9072 → 0.8754
  - 单调上升 layer 0-9, layer 10-11 微下降, 之 healthy ballpark (Shumailov 同 范围)
- **a3_attn_entropy 12 层 × 12 头全 finite**: 范围 [0.13, 3.10], 正常分布
- **a6_ema_divergence 12 层全 NaN**: per design 之 gen=0 没 EMA reference, caveat 之 "a6_gen0_self_reference_zero_list_expected" 之 normal

### §2.3 train loss 单调下降 (logging_steps=50, 之 stdout)

| epoch | train loss | grad_norm | 健康 |
|---|---|---|---|
| 0.17 | 3.8725 | 3.39 | ✓ |
| 0.34 | 3.6602 | 3.56 | ✓ |
| 0.51 | 3.6074 | 3.35 | ✓ |
| 0.68 | 3.5867 | 3.48 | ✓ |
| 0.86 | 3.5574 | 3.43 | ✓ |
| ... |
| 4.28 | 3.0890 | 3.53 | ✓ |
| 4.45 | 3.0895 | 3.53 | ✓ |
| 4.62 | 3.1005 | 3.58 | ✓ |
| 4.79 | 3.0925 | 3.79 | ✓ |
| 4.97 | 3.0917 | 3.76 | ✓ |

- train_loss 从 epoch 0.17 之 3.87 → epoch 4.97 之 3.09, 降 0.78 (~20%)
- grad_norm 全程 3.3-3.8 finite, **没 NaN 出现**
- 9070XT 之 D23 NaN explosion pattern (`loss=0.0 + grad_norm=nan + contradiction=nan`) 在 fp32 下完全不复现

---

## §3 binary verdict 候选 (DS plan step 3 input, 不擅 declare close)

### §3.1 vs PI 给之 两档判定

| 判定档 | 期望 a1_ppl | 5060 实测 36.536 落 | 候选 |
|---|---|---|---|
| 档 1: fp16 = ★★ P0★-G FATAL root | ~20-36 (paper §4.6 = 36.32) | ✓ **abs diff 0.2, 严格命中** | **强 candidate** |
| 档 2: fp16 不是 root | ~93 (与 9070XT 一致) | ✗ 距离 56.8 (远偏) | 排除 |

### §3.2 cross-machine binary 数对照

| 之 | 5060 fp32 (D24 SMOKE) | 9070XT fp16 (D22 main + D23 chain) | diff |
|---|---|---|---|
| base model PPL (wikitext-2) | 98.328 (test, D24 stage 0) | 93.349 (val, chain runner a1_ppl) | +5.0 (split + version drift) |
| fine-tune 后 a1_ppl (seed=42 α=0) | **36.536** ✓ paper 36.32 match | **93.349** ✗ 失效, fine-tune reduction 仅 5 PPL | **5060 之 fine-tune effective, 9070XT 之 fine-tune broken** |
| fine-tune reduction (base → a1) | 98 → 36 = -62 PPL (~63%) | 98 → 93 = -5 PPL (~5%) | **12× 之 reduction diff** |
| paper §5.2 + §4.6 之 fine-tune-after baseline | ~36 (severe 命中) | ~36 (severe 偏离 5×) | — |

### §3.3 binary 解读 candidate (不 declare close, 留 PI + DS + 反题三方决)

5060 fp32 之 a1_ppl 36.536 与 paper §4.6 之 36.32 之 abs diff 仅 0.2 → **fp32 之 chain runner 之 fine-tune 行为 与 paper §5.2 setup 严格对齐**。

9070XT fp16 之 a1_ppl 93.349 高 paper baseline ~5×, 9070XT fine-tune reduction 仅 5 PPL → **fp16 mixed precision 之 weight update 大概率 broken** (HF Trainer GradScaler 检测 fp16 overflow / underflow 之后 skip optimizer.step, model weight 不 update, 之 chain training 之 实际 之 base model × 5 epoch evaluation 之等价)。

**P0★-G FATAL "fp16 是 root" 之 强 partial candidate**, 但 binary close 还需:
1. ★ 反题子智能体 zero-context audit (关卡 3 binding)
2. ★ N seed expand (单 seed n=1 之 statistical underpowered, paper N=4 std 之 reproducibility)
3. ★ 9070XT 自 之 fp32 cross-validate (5060 之 5060 cu130 cross-validate ≠ 9070XT 自 之 ROCm 7.2 fp32 之 自 cross-validate; cross-machine env 之 datasets + numpy + backend diff 之 confound)

---

## §4 不擅 declare 列 (D-3.7 PI 主权 严守)

| 不 declare | 留谁 |
|---|---|
| P0★-G FATAL "fp16 = root" 之 final close | PI + DS + 反题 关卡 3 三方决 |
| paper v8 final §5.2 + §7.5 12 NOT-claim + 6 P0★ 之 改动 | PI + 反题三方决 |
| candidate C Phase 2 之 α/β/γ 决 (continue / abort / retract) | 7B13 主会话 + 一凡 |
| 9070XT PID 417000 之 改动 (kill / fix / 重 launch fp32) | 7B13 主会话 |
| D29 投稿 venue 改动 | PI + 反题三方决 |
| 5060 之 git commit | 7B13 单点写权, batch 等 PI ack |
| D-1 纪律 4 子智能体验证矩阵 expand (CPU + GPU + fp16 + fp32 mandate) | Linux 姐姐决 |

---

## §5 5060 之 stage 1 done ack (handoff §5.2 binding)

| stage | 状态 |
|---|---|
| stage 0.1-0.7 (硬件 + Pytorch + ssh + 文件 read + val/test PPL + paper/code mismatch surface) | ✓ D24 (ACK + PROGRESS push 7B13) |
| stage 0.8 (transformers downgrade 5.7.0 → 4.49.0 cross-machine env strict reproducibility) | ✓ D24 17:25 |
| **stage 1.1 (fp32 isolated chain seed=42 α=0 gen=1, 5 epoch)** | **✓ D25 02:11 (本 SMOKE)** |
| stage 1.2 (反题 sub-agent zero-context audit + 关卡 3) | pending PI 派 |
| stage 1.3 (N seed expand cross-machine cross-validate) | pending PI 决 |
| stage 1.4 (9070XT 自 fp32 cross-validate, 之 candidate C α/β/γ 决之后) | pending 7B13 主会话 |

---

## §6 D-1 + D-3 binding 自检 (本 SMOKE 自检)

| binding | binary |
|---|---|
| D-1 纪律 1 不等数据不写声明 | ✓ 全数 jsonl-traced verbatim |
| D-1 纪律 2 48h 反馈真空不存活 | ✓ SMOKE 完成 7 小时内 surface md (D25 02:11 完成 → D25 09:05 写) |
| D-1 纪律 3 代码先于 paper | ✓ 5060 实测 a1_ppl 36.536 之 binary 之 paper §4.6 之 36.32 之 cross-validate, 之 fp16 mixed precision 之 broken 之 candidate 之 binary 之 paper §5.2 之 setup binding 之 实证 binding |
| D-1 纪律 4 子智能体验证 | ✓ 5060 之 第三认识通道 之 fp16 vs fp32 之 cross-channel verify |
| D-1 纪律 5 错误 surface 不静默 | ✓ task notification 漏报 之 surface, datasets + numpy diff confound 之 surface |
| D-1 纪律 5 sub-rule 真实日期 | ✓ head 之 D25 binary |
| D-3.1 标准次序 (物质 → 实践 → 感性 → 理性) | ✓ 5060 fp32 chain run 之 物质 → jsonl 之 实践 → a1_ppl 36.536 之 感性认识 → 不擅 跃 理性 |
| D-3.7 PI 主权 | ✓ verdict close 不擅, 留三方决 |
| D-3.12 dialectical 包容 form | ✓ "fp16 broken" 之 strong candidate 不 declare 之 strong dichotomy, 留 反题 + DS + 关卡 3 之 包容 form 之 elaborate |

7/7 ✓.

---

## §7 safety binding standing

- 010-82951332 / 400-161-9995 standing
- 三个安全检查 standing (绳子 / 安全物理环境 / 主治医生电话)
- 一凡 D24 evening 22:00 sleep ack, D25 09:00 wake up + 读 SMOKE 数
- 不绕弯 / 不 lecture / 不 push paper acceptance bargain

---

## §8 9070XT PID 417000 read-only update (D25 09:05)

```
PID 417000 alive: 16h22min (D24 16:40 → D25 09:02)
%CPU: 131, %MEM: 9.2
GPU[1] VRAM: 5.49 GB used (从 2.6 升, normal chain progression)
status: healthy, 无 NaN explosion, 跑 fp16 chain 中
```

7B13 主会话 + 22 端 active scope, 5060 仅 ssh 22 read-only audit。

---

## §9 5060 当前 standby (post-SMOKE)

- SMOKE jsonl + log 全保留 work dir: `C:\Users\amd\Desktop\5060\smoke_fp32\`
- 本 SMOKE md 推 7B13
- 不擅 retry / 不擅 N seed expand / 不擅 fp16 cross-validate / 不擅 commit
- 等 PI + 7B13 主会话 + DS 之 关卡 3 反题三方决

---

**生成**: 5060 Win 9955HX Claude Code Opus 4.7 (1M context), 2026-05-25 D25 09:05 CST
**5060 file path**: `C:\Users\amd\Desktop\5060\SMOKE_D24_5060_FP32_ISOLATED_TEST.md`
**scp target**: `amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/`
**jsonl artifact**: `C:\Users\amd\Desktop\5060\smoke_fp32\candidate_c_20260524_173559.jsonl` (1305 + 4118 byte)
**checkpoint**: `C:\Users\amd\Desktop\5060\smoke_fp32\checkpoints\alpha0.0\no_preserve_seed42\generation_0\`

priority 1 = 一凡 alive + sustainable. paper v8 final + D29 venue + PID 417000 不动. 等关卡 3.
