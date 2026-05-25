# [9070XT VERIFY — D23 12:55 实验进度 + 代码校验]

**真实今日日期** (`date '+%Y-%m-%d %H:%M:%S %Z'`): `2026-05-23 13:00:47 CST` (D23)

**Surface**: 9070XT (22) 新会话 cold-start by 一凡 Win 端

**对象**: 7B13 Linux 姐姐主会话 + 一凡 D23 binary 决 input

**协议**: D-1 纪律 5 (错误 surface 不静默修正) + D-3.7 PI 主权 (不 unilateral 决)

**状态**: PID 267111 仍活, 32/180 chain_gen_done, 上次 SURFACE_D23 (02:43) 后 +5 代

---

## §0 本会话上下文

- 22 端 D23 02:43 上个会话被 API 拦截 (Usage Policy, Request ID `req_011CbJjHrSiwLs8LvUhhPvpp`)
- Win 端一凡 ssh 22 cold-start 新会话, 任务: 校验现在实验所有进度 + 校验 md 中代码 + 写入 7B13 md
- 不动 PID 267111 (一凡决 scope), 不 kill, 不 resume, 不重启
- 不 git push (7B13 单点写权)
- 不擅自 commit 22 端 uncommitted (留 7B13 主会话决)

---

## §1 实验进度 binary (D23 13:00 CST)

| 指标 | 上次 SURFACE_D23 @ 02:43 | 现在 @ 13:00 | 差 |
|---|---|---|---|
| PID 267111 状态 | alive 132% CPU 14h | alive 132% CPU **16:22:12** | +2h22m |
| chain_gen_done | 27 / 180 (15.0%) | **32 / 180 (17.8%)** | +5 代 |
| 完整 chain (10 代) | 2 (α=0 + α=5) | **3** (α=0 + α=5 + α=10) | +1 |
| 不完整 chain | 1 (α=10 gen 0-6) | **1** (seed=1337 α=0 gen 0-1) | 切换 |
| 当前进行中 | seed=42 α=10 gen=7 | seed=1337 α=0 gen=2 | — |
| Phase 2 wall-clock 已耗 | ~14h | ~16h22m | +2h22m |
| 剩余 chain | 13 partial + 14 待 = ~150 代 (~70%) | ~148 代 待 | 几乎不变 (慢) |

### 32 chain_gen_done 分布

| seed | α | gen 范围 | a1_ppl 状态 |
|---|---|---|---|
| 42 | 0.0 | 0..9 (10 / 10 ✓) | **全 ≈ 93.349** (健康, 与 base PPL 一致, 冻结) |
| 42 | 5.0 | 0..9 (10 / 10 ✓) | 全 None (val_loss=NaN) |
| 42 | 10.0 | 0..9 (10 / 10 ✓) | 全 None (val_loss=NaN) |
| 1337 | 0.0 | 0..1 (2 / 10) | **全 None** (val_loss=NaN, gen 0 首代即 NaN) |

剩余未跑: seed=1337 α=0 gen 2..9, seed=1337 α=5/10 全 10 代, seed 2024/7/137/271 × α 0/5/10 × gen 0..9 = 148 代 (~ ~140-180h ETA, 接 D29-D31 wall-clock).

---

## §2 4-axis raw 数 (binary, jsonl-traced)

### §2.1 seed=42 α=0 gen=9 (健康 chain 之尾代)

```
a1_ppl: 93.34854064062004
val_loss: 4.536340236663818
a2_anisotropy[0:3]: [0.705..., 0.689..., 0.708...]  (12 层 finite)
a6_ema_divergence[0:3]: [6.4e-05, 5.9e-05, 5.7e-05]  (12 层 finite, 之 small drift)
caveats: ['a6_reframed_as_drift_from_gen0_baseline']
```

### §2.2 seed=42 α=5 gen=9 (NaN chain 之尾代)

```
a1_ppl: None
val_loss: None
a2_anisotropy[0:3]: [0.702..., nan, nan]  (12 层 partial NaN)
a6_ema_divergence[0:3]: [0.0, nan, 0.0]   (12 层 partial NaN)
```

### §2.3 seed=42 α=10 gen=9 (NaN chain 之尾代)

```
a1_ppl: None
val_loss: None
a2_anisotropy[0:3]: [nan, nan, nan]   (12 层 全 NaN)
a6_ema_divergence[0:3]: [nan, nan, nan]
```

### §2.4 seed=1337 α=0 gen=0 + gen=1 (**新发现 D23 12:19 + 12:53**)

```
seed=1337 α=0.0 gen=0:
  a1_ppl: None
  val_loss: None
  a2_anisotropy[0:3]: [nan, nan, nan]
  a6_ema_divergence[0:3]: [nan, nan, nan]
  caveats: ['a6_gen0_self_reference_zero_list_expected']

seed=1337 α=0.0 gen=1:
  a1_ppl: None
  val_loss: None
  (同上, 全 NaN)
```

---

## §3 SURFACE_D23 §4 hypothesis vs 新数据 binary 差异

### SURFACE_D23 §4.1 主 hypothesis 原文 (02:43 写)

> α=0 之 baseline 不 trigger contradiction loss (alpha=0 之 short-circuit, contradiction_alpha > 0 才 compute), 但 loss=0.0 + grad_norm=nan 同样出现 → fp16 training 之 lm_loss 本身 underflow.

### 新数据 partial 反驳

- seed=42 α=0 全 10 代 **健康** (a1_ppl ≈ 93.349, a6 finite small drift)
- seed=1337 α=0 gen=0 **首代即 NaN** (a1_ppl=None, val_loss=None, a2/a6 全 NaN)

binary fact: α=0 之 contradiction loss 已 disabled (candidate_c_runner.py L173 `enabled=alpha > 0`), 但同样 α=0 + 同 base model OPT-125m + 同 wikitext-2 train 切片之下, seed 42 健康 vs seed 1337 NaN. **seed 初始化敏感** binary surface.

### 这意味着 (raw fact 不 declare hypothesis 收敛)

- 不是单一 contradiction loss 触发 (α=0 已排除)
- 不是 ROCm gfx1201 fp16 boundary 通用 issue (若是, seed=42 α=0 也应 NaN)
- seed-specific fp16 numerical edge case (mixed precision autocast + 特定初始 weight 配置 触发 underflow)
- 或: train 数据 shuffle (seed=seed+g, L238) 之 某 batch 在 seed=1337 下 trigger 不 finite

具体 root 由 7B13 主会话 + (若需) 反题 sub-agent 决, 9070XT 不 unilateral declare hypothesis 收敛.

---

## §4 代码校验 binary (PID 267111 cmd vs scripts vs SURFACE_D23 §4)

### §4.1 ps 实际 cmd vs candidate_c_runner.py docstring

```bash
# ps 实际:
python scripts/candidate_c_runner.py \
  --seeds 42,1337,2024,7,137,271 \
  --alphas 0,5,10 \
  --gens 10 \
  --device cuda \
  --output-dir /tmp/dppl_bridge_verify/output/candidate_c \
  --rsync-target amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/candidate_c/ \
  --resume
```

candidate_c_runner.py L20-33 docstring 之 "main run" usage 与上一致 ✓ (额外 `--resume` flag 是 nohup launch script 之 add).

### §4.2 train_one_generation.py 之 uncommitted diff (4 行 add)

```diff
+    # D22 candidate C add (Agent 4 catch): attn_implementation="eager" 必 explicit.
+    # 避 OPT model SDPA default 之 output_attentions=True silent fallback 到 eager + warning.
+    # multi-layer A3 attention 头熵 测量 需 output_attentions=True (Phase 1 candidate C binding).
     model = AutoModelForCausalLM.from_pretrained(
         base_model_path,
         torch_dtype=torch.float32,
+        attn_implementation="eager",
     )
```

校验: 这条 add 与 candidate_c_runner.py L17-19 docstring 注解一致:

> attn_implementation="eager" 之 train_one_generation.py line 102-108 之 explicit add (避 SDPA output_attentions=True silent fallback)

代码与 md 描述一致 ✓.

### §4.3 candidate_c_runner.py 之关键逻辑 binary verify

| 行 | 代码 | jsonl 实证 |
|---|---|---|
| L173 | `CATConfig(enabled=alpha > 0, ...)` | α=0 之 chain 无 contradiction (seed=42 α=0 健康验证) ✓ |
| L242-244 | `base_model_path = cfg.model.hf_id if g==0 else gen0_dir` | gen 1+ 都基于 gen 0 (不是 gen g-1), nohup log 见 "加载 model .../generation_0" ✓ |
| L246 | `cat_for_this_gen = None if g==0 else cat_cfg` | gen 0 无 CAT, gen 1+ 才 enable (g=0 之 contradiction log 全 disabled, jsonl caveat 之 a6 gen0 self-ref 一致) ✓ |
| L249 | `fp16_use = cfg.fine_tune.fp16 and device != "cpu"` | cuda + cat_arm_b.yaml fp16=True → fp16 mixed precision ✓ (但 underflow trigger 之 root) |
| L277 | `a1_ppl = math.exp(val_loss) if (val_loss < 20 and finite) else inf` | val_loss=nan → a1_ppl=inf → L408 json null ✓ |
| L165 | `chain_base = checkpoints/alpha{alpha}/no_preserve_seed{seed}` | 输出 jsonl 之 ckpt_path 与之一致 ✓ |

代码 ↔ jsonl 输出一致, runner.py 行为与 docstring 描述一致.

### §4.4 SURFACE_D23 §3 之 a6_ema_divergence claim vs 实际

SURFACE_D23 §3 写: "caveats 字段全是 sub-agent A 之 a6 reframe note ..., sub-agent A 之 honest caveat 但 **没 catch NaN explosion**". 

binary verify:
- seed=42 α=0 之 caveats 现在含 `a6_reframed_as_drift_from_gen0_baseline` (gen ≥ 1) 或 `a6_gen0_self_reference_zero_list_expected` (gen=0) — 与 SURFACE_D23 描述一致 ✓
- runner.py L302-316 之 reframe logic: gen ≥ 1 时 reload gen0 之 model 作 ema_reference, gen=0 时 ema_model=None 之 a6 之 honest disclose ✓
- 但 multi_layer_hook.py L1-21 docstring 之 "A6 每层 EMA 散度: per layer 之 EMA state vs current weight 之 L2 distance" 与 runner.py L294-300 之 reframe ("a6 reframe 之 cat_trainer ema_model 在 trainer destruct 后 已 inaccessible") 不严格一致 — 即 a6 实际 不是 EMA state, 而是 gen0 baseline 之 L2 drift. 这条 candidate_c_runner.py 自己 surface 之 caveat 已 honest disclose (caveats 字段), 不 silent.

### §4.5 nohup log 之 SURFACE_D23 §2 trace 现在仍可重现

SURFACE_D23 §2 trace 之 epoch 3.6 loss=0.0 + grad_norm=nan + contradiction=nan, 现在 nohup log 仍能 grep 到同 pattern 在 seed=42 α=10 gen 7/8/9 之 epoch 3.5+ 段, 与上次描述一致 ✓ (NaN explosion 持续 D23 全程).

---

## §5 22 端 git status uncommitted (review only, 不 commit)

```
位于分支 main, 与 origin/main 一致

 M experiments/exp018_cat/src/train_one_generation.py        (+4 行, §4.2)
?? experiments/exp018_cat/data/
?? experiments/exp018_cat/scripts/candidate_c_runner.py     (D22 evening 写, 645 行)
?? experiments/exp018_cat/src/multi_layer_hook.py           (D22 evening 写, 297 行)
```

3 个 untracked + 1 个 modified 是 PID 267111 跑用之全部源码. 这些代码 D22 evening 由 7B13 主会话 (Linux 姐姐) 之前 session push 到 22, 还没 commit. 留 7B13 主会话决是否 commit 进 main.

9070XT 不 git push, 不 commit (7B13 单点写权 binding).

---

## §6 进度 ETA 估算 (基于已 16h22m 跑 32 代, ~30 min/代)

- 已完成: 32 / 180 = 17.8% (16.4h)
- ETA 全程 ~92h 总 wall-clock = 已 16.4h + 剩 ~75-80h
- 若 (β) continue, 剩余 ~75-80h ≈ D26-D27 evening 跑完
- 若 (α) fp32 重 launch, ~2× wall-clock ≈ 30-60h 新一轮, D24-D26 cover (与 SURFACE_D23 §5.α 之 30h estimate 一致)

(以上 ETA 基于 32 代之实际 elapsed, 不是 SURFACE_D23 §5 之 14h pace 推断)

---

## §7 9070XT 不 unilateral declare 列表 (D-3.7 PI 主权)

| 不 declare | 留谁决 |
|---|---|
| SURFACE_D23 §4.1-§4.3 之 hypothesis 收敛 | 7B13 主会话 + (若需) 反题 sub-agent |
| seed=1337 α=0 NaN 之 root cause attribution | 7B13 + 数学子协作者 |
| α / β / γ binary 决 | 一凡 PI |
| paper v8 final 47/47 改动 | 一凡 + 反题三方 + DS |
| D-1 纪律 4 expand (pre-flight GPU+fp16+α 双 case mandate) | 一凡 + Linux 姐姐 |
| 22 端 4 个 uncommitted file 之 commit | 7B13 主会话 |
| D29 投稿 (arXiv + TMLR + KBS) 改动 | 一凡 + Linux 姐姐 + DS |

---

## §8 9070XT 当前 standby 行为 (不动)

- PID 267111 continue running, 不 kill, 不 resume, 不重启
- jsonl 持续追加 (每 ~30min 一代), rsync push 7B13 持续 ✓ (sibling progress_snapshot_*.md 也持续 push)
- 本 VERIFY md scp 推 7B13 (位置同 SURFACE_D23 sibling)
- 等一凡 + 7B13 主会话 binary 决 α/β/γ + uncommitted file commit scope + 后续

---

## §9 D-1 + D-3 binding 严守 ack (本 VERIFY 自检)

| binding | binary verify |
|---|---|
| D-1 纪律 1 (不等数据不写声明) | ✓ 32 chain_gen_done jsonl-traced, 所有数字 verbatim, 无 [?] 占位符 |
| D-1 纪律 2 (48h 反馈真空不存活) | ✓ 上次 SURFACE 之 27/180 之 32/180 update 在 11h 内 surface |
| D-1 纪律 3 (代码先于 paper) | ✓ 本 verify 基于 candidate_c_runner.py + jsonl + nohup log 之实践 evidence, 不基于 paper 假设 |
| D-1 纪律 4 (子协作者验证) | ✓ 本 surface 即 9070XT 作为 D-1 第二认识通道 之 instantiate (Phase 2 跑 16h 后 surface 新 binary data) |
| D-1 纪律 5 (错误 surface 不静默修正) | ✓ seed=1337 α=0 NaN 之新发现 partial 反驳 SURFACE_D23 §4.1, 不 hide, 不 silent 改 §4.1 |
| D-1 纪律 5 sub-rule (真实日期) | ✓ head line `date` 输出 verbatim print, D23 binary |
| D-3.1 反映论 标准次序 | ✓ 物质 (PID 状态) → 实践 (chain training NaN raw) → 感性认识 (32 chain partial) → 不 unilateral 跃 理性认识 / 哲学判读 |
| D-3.2 抓出 (哲学 outcome 不 starting form) | ✓ 仅 surface raw 数, 不 declare "fp16 fragility paradigm" 或类似 |
| D-3.7 PI 主权 binding | ✓ α/β/γ + paper 改动 + commit 全留 PI 决 |

---

## §10 priority 1 = 一凡 alive + sustainable (健康约束)

- 9070XT Phase 2 NaN explosion 不是 emergency, 是 normal experimental surface, 不需一凡立即 active response
- 一凡 D22 evening 强制休息 ack, D23 早 wake 后 SURFACE_D23 已读
- 安全 binding standing: 010-82951332 / 400-161-9995 hotline, 三个安全检查 (绳子 / 安全物理环境 / 主治医生电话) standing
- 本 VERIFY 仅作进度 + 代码 binary surface, 不 push 任何 paper acceptance bargain

---

**生成**: 9070XT (22) Claude Code Opus 4.7 (1M context), cold-start 新会话
**file path** (22 本地): `/tmp/VERIFY_D23_12_55_PROGRESS_CODE_20260523.md`
**rsync target** (7B13): `amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/VERIFY_D23_12_55_PROGRESS_CODE_20260523.md`

握着. D-1 纪律 5 严守 + D-3.7 PI 主权 严守. 等一凡 + 7B13 binary 决.
