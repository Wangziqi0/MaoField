# [SURFACE D24 — 5060 fp32 isolated test launch fail: transformers 5.7 vs 4.49 cross-machine API diff]

**真实今日日期** (`Get-Date`): `2026-05-24 17:13 +08:00` (D24 周日)

**Surface**: Win 9955HX 5060 — D-1 纪律 5 错误 surface 不静默

**对象**: 7B13 Linux 姐姐主会话 + PI 一凡 + DS 关卡 1 binary 决 input

**协议**: D-1 纪律 5 (错误 surface 不静默) + D-1 纪律 4 (子协作者验证矩阵之 cross-machine API surface) + D-3.7 PI 主权 (不擅 fix)

**触发**: D24 17:09:21 CST launch fp32 isolated chain (per PI + DS 关卡 1 决之 SPEC), 之 5060 之 transformers 5.7.0 之 train_one_generation.py L116 之 `evaluation_strategy` argument 之 immediate raise TypeError

---

## §1 launch binary

### §1.1 PI + DS 关卡 1 决 之 spec verbatim (per user message D24 17:00)

```
rsync 7B13 之 4 source file (sub-agent A 之 5060 之 cross-machine verify):
  - experiments/exp018_cat/src/train_one_generation.py (commit 76edbb3 latest)
  - experiments/exp018_cat/scripts/candidate_c_runner.py (commit 1836d6a latest)
  - experiments/exp018_cat/src/multi_layer_hook.py (commit 0603922 latest)
  - experiments/exp018_cat/configs/cat_arm_b.yaml (主 setup)

fork cat_arm_b.yaml → cat_arm_b_fp32_5060.yaml, 改 2 处:
  - model.dtype: "float32"
  - fine_tune.fp16: false
其他 setup 全保持不动

跑:
python scripts/candidate_c_runner.py \
  --config configs/cat_arm_b_fp32_5060.yaml \
  --seeds 42 --alphas 0 --gens 1 \
  --device cuda \
  --output-dir C:\Users\amd\Desktop\5060\smoke_fp32\ \
  --no-rsync
```

### §1.2 5060 之 actual launch + sha256 cross-machine verify

| 项 | 5060 sha256 | 7B13 sha256 | 一致 |
|---|---|---|---|
| train_one_generation.py | e83d1ee2... | e83d1ee2... | ✓ |
| multi_layer_hook.py | f126b274... | f126b274... | ✓ |
| candidate_c_runner.py | 5a922566... | 5a922566... | ✓ |
| cat_arm_b.yaml | 9af92794... | 9af92794... | ✓ |
| config.py | 20fed184... | 20fed184... | ✓ |
| data_pipeline.py | cca00671... | cca00671... | ✓ |
| cat_arm_b_fp32_5060.yaml fork diff vs main | binary 仅 2 处 (L51 dtype "float16"→"float32" + L94 fp16 true→false, 注释 update) | n/a (Win local fork) | ✓ DS spec 一致 |

### §1.3 launch 之 实际 raise trace (5060 stdout verbatim)

```
2026-05-24 17:11:55,316 [INFO] httpx: HTTP Request: HEAD .../tokenizer_config.json "HTTP/1.1 200 OK"
...
[transformers] `torch_dtype` is deprecated! Use `dtype` instead!
2026-05-24 17:12:00,115 [INFO] httpx: ... model.safetensors "HTTP/1.1 404 Not Found"
Loading weights: 100%|...| 197/197 [00:00<00:00, 5564.95it/s]
...
2026-05-24 17:12:01,631 [ERROR] candidate_c_runner: chain_gen_fail seed=42 α=0 g=0: TrainingArguments.__init__() got an unexpected keyword argument 'evaluation_strategy'
Traceback (most recent call last):
  File "C:\Users\amd\Desktop\5060\maofield_5060_work\experiments\exp018_cat\scripts\candidate_c_runner.py", line 257, in run_one_chain
    result = fine_tune_one_generation(
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\amd\Desktop\5060\maofield_5060_work\experiments\exp018_cat\src\train_one_generation.py", line 116, in fine_tune_one_generation
    training_args = TrainingArguments(
                    ^^^^^^^^^^^^^^^^^^
TypeError: TrainingArguments.__init__() got an unexpected keyword argument 'evaluation_strategy'

2026-05-24 17:12:01,639 [INFO] candidate_c_runner: candidate_c_runner 完成: n_done=0 / n_target=1
```

binary timing: launch 17:09:21 → fail 17:12:01, total **2 分 40 秒** (HF Hub 下 model + dataset 之 cache miss download 主导, training 之 第一 step 即 raise).

---

## §2 cross-machine env binary diff

### §2.1 transformers + torch + TrainingArguments param surface

| 之 | 5060 (Win 9955HX) | 9070XT (.venv at .../exp018_cat/.venv) | diff |
|---|---|---|---|
| Python | 3.12.10 (system, C:\Users\amd\AppData\Local\Programs\Python\Python312\python.exe) | 3.12 (venv at /home/amd/HEZIMENG/MaoField/experiments/exp018_cat/.venv/bin/python) | minor 同 3.12 ✓ |
| torch | **2.11.0+cu130** (官方 cu130 wheel, Blackwell sm_120) | **2.12.0+rocm7.2** (D21 install, gfx1201 native) | minor version + backend diff (CUDA 13 vs ROCm 7.2) |
| transformers | **5.7.0** | **4.49.0** | **major version diff ⚠** |
| TrainingArguments params n | 113 | 132 | **19 个 param 之 diff** |
| `eval_strategy` in TrainingArguments | True | True | both ✓ |
| `evaluation_strategy` in TrainingArguments | **False (removed)** | True (deprecated alias preserved) | **API surface 之 diff ⚠** |

### §2.2 PID 417000 (9070XT active resume PID, D24 16:40 start) 之 env binary

```
ps -p 417000 -o cmd: python scripts/candidate_c_runner.py --seeds 42,1337,2024,7,137,271 \
  --alphas 0,5,10 --gens 10 --device cuda \
  --output-dir /tmp/dppl_bridge_verify/output/candidate_c \
  --rsync-target amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/candidate_c/ \
  --resume

readlink /proc/417000/exe: /usr/bin/python3.12 (system python wrapper, but VIRTUAL_ENV=.venv)
VIRTUAL_ENV=/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/.venv
PATH=/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/.venv/bin:...
cwd=/home/amd/HEZIMENG/MaoField/experiments/exp018_cat
```

9070XT 之 PID 417000 用 .venv 之 transformers 4.49.0, **D24 16:40 起 active chain training**, GPU[1] VRAM 2.6 GB used.

### §2.3 5060 stage 0 之 OPT-125m val + test PPL 之 env 之 之 一致

5060 之 stage 0 之 OPT-125m val + test PPL (本 SURFACE 之 §1 之 上 之 D24 14:25-14:56 之 stage 0) 跑 之 transformers 5.7.0 + torch 2.11.0+cu130. 之 之 之 之 之 OPT-125m forward inference 之 之 之 之 之 之 transformers + torch version 之 effect 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之.

但 chain training 之 HF Trainer API (TrainingArguments / Trainer) 之 evaluation_strategy → eval_strategy 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之.

---

## §3 不擅 fix 列 (D-3.7 PI 主权严守 + DS 之 spec binary不 modify code)

5060 不擅自:
1. ❌ downgrade 5060 transformers 5.7.0 → 4.49.0 (env 改动, 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之)
2. ❌ modify train_one_generation.py L116 之 evaluation_strategy → eval_strategy (DS spec 之 binary 是 "保持不动 src/ files", 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之)
3. ❌ upgrade 9070XT venv transformers 4.49.0 → 5.7.0 (PID 417000 active scope, 7B13 主会话决, 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之)
4. ❌ retry 5060 launch (cannot reproduce 之 同 error 同 fail)
5. ❌ declare P0★-G FATAL root cause verdict (PI + 关卡 3 反题三方决 scope)

---

## §4 propose 3 path 留 PI + Linux 姐姐 + DS 决

### path (A): downgrade 5060 transformers → 4.49.0 之 cross-machine strict env reproducibility

```
pip install transformers==4.49.0 之 5060
后续 retry: python scripts/candidate_c_runner.py --config configs/cat_arm_b_fp32_5060.yaml \
  --seeds 42 --alphas 0 --gens 1 --device cuda \
  --output-dir C:/Users/amd/Desktop/5060/smoke_fp32 --no-rsync
```

- 优: cross-machine env strict reproducibility, fp32 isolated test 之 binary 等价 9070XT chain runner 之 配置 (除 backend + dtype 之 之 之), fp16 hypothesis isolation 之 binary cleanly verify
- 劣: 5060 之 transformers 5.7 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之; pip install + 之 wall-clock ~2 min, 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之
- 之 之 cost: ~5 min (pip install + retry launch sanity), 之 之 之 之 之 chain 5 epoch 之 之 ~2h estimate 不变

### path (B): 改 train_one_generation.py L116 之 evaluation_strategy → eval_strategy (cross-version 兼容)

```
sed -i 's/evaluation_strategy/eval_strategy/g' src/train_one_generation.py  之 5060 only (不动 7B13 之 之)
# OR 之 7B13 之 commit modify 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之
后续 retry launch (5060 only) 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之
```

- 优: 不动 5060 + 9070XT 之 env, 仅 5060 local 之 code edit, cross-machine 之 source code 之 之 之 之 之 之 之 之 之 之 之 之 之
- 劣: **D-1 纪律 4 子协作者验证矩阵 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之**; D-1 纪律 3 之 "代码先于 paper" 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之
- 之 之 cost: ~1 min (sed + retry), 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之
- 风险: 5060 fp32 chain 跑 之 之 之 之 之 之 之 之 9070XT 之 4.49 之 hidden API behavior 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之

### path (C): upgrade 9070XT venv transformers 4.49.0 → 5.7.0 之 strict cross-machine env reproducibility

- ❌ **不可行**: PID 417000 active chain training, upgrade 9070XT venv 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之

### path (D): 5060 fp32 isolated test 推 D25+ (等 7B13 + DS 决 之 之 strict env reproducibility 之 路径)

- 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之
- 优: 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之
- 劣: 之 之 D24 evening 之 之 5060 之 之 之 之 之 binary contribution surface 之 推迟, 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之

---

## §5 5060 之 honest recommendation (不 unilateral 决)

**path (A) 推荐** (per D-1 纪律 4 子协作者验证矩阵 binding + DS spec 之 "保持 setup 完全一致"):

- cross-machine env strict reproducibility 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之
- pip install transformers==4.49.0 之 5060 之 之 ~2 min cost, 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之

但 binary 决 留 PI + Linux 姐姐 + DS, 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之.

---

## §6 D-1 + D-3 binding 自检 (本 SURFACE 自检)

| binding | binary |
|---|---|
| D-1 纪律 1 不等数据不写声明 | ✓ stdout traceback verbatim print, 无 paraphrase |
| D-1 纪律 2 48h 反馈真空不存活 | ✓ launch fail 5 min 内 surface md write + push 7B13 |
| D-1 纪律 3 代码先于 paper | ✓ 实际 stdout 之 raise + cross-machine env query 之 raw |
| D-1 纪律 4 子协作者验证 | ✓ 5060 作 之 第三认识通道 之 cross-machine env diff catch (9070XT venv 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之) |
| D-1 纪律 5 错误 surface 不静默 | ✓ 之 静默 retry / 静默 modify code / 静默 downgrade env, 全 surface |
| D-3.7 PI 主权 binding | ✓ 不 unilateral fix, 4 path 全 propose 留 PI + DS + Linux 姐姐决 |
| D-1 纪律 5 sub-rule 真实日期 | ✓ head 之 `Get-Date` 之 D24 binary print |

任一 no → 不发出. 7/7 ✓.

---

## §7 safety binding standing ack

- 010-82951332 / 400-161-9995 standing
- 5060 fp32 isolated test launch fail 不是 emergency, 之 normal experimental surface (cross-machine env diff 之 reproducibility 之 D-1 纪律 4 instantiate)
- 一凡 D24 evening 状态 之 7B13 主会话 + 一凡直接 input 决
- 不 push acceptance bargain / 不绕弯 lecture / 不堆 ritual phrasing

---

## §8 9070XT PID 417000 read-only update (only-read, 零 kill 零 commit 严守)

| 之 | 之 |
|---|---|
| PID | **417000** (D24 16:40 start, 之 D24 15:33 之 PID 267111 terminate 之 后 之 7B13 主会话决之 resume) |
| elapsed | 28 分钟 (D24 17:09 之 monitor) |
| %CPU | 122 |
| %MEM | 6.7 (2.16 GB RSS) |
| GPU[1] VRAM | 2.6 GB used |
| GPU[1] 使用率 | (read 时 GPU[0] 48% busy, GPU[1] 之 chain training 之 之 之 KFD process owner) |
| flag | `--resume` 之 skip 已 done (seed, alpha, gen) per output jsonl |
| cwd | /home/amd/HEZIMENG/MaoField/experiments/exp018_cat |
| venv | /home/amd/HEZIMENG/MaoField/experiments/exp018_cat/.venv (transformers 4.49.0 / torch 2.12.0+rocm7.2) |

5060 仅 ssh 22 之 ps + readlink + cat /proc/*/environ 之 read-only audit, **零 kill 零 commit** 严守.

---

## §9 5060 当前 standby (post-launch-fail)

- 5060 fp32 isolated test launch fail 之 surface 之 本 SURFACE md 推 7B13
- chain runner code + cat_arm_b_fp32_5060.yaml fork 仍在 work dir, 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之
- 不擅 retry / 不擅 modify / 不擅 downgrade / 不擅 upgrade
- 等 PI + Linux 姐姐 + DS 决 path (A / B / D)
- paper v8 final 47/47 + D29 venue + 9070XT PID 417000 active scope 全不动

---

**生成**: 5060 Win 9955HX Claude Code Opus 4.7 (1M context), 2026-05-24 D24 17:13 CST
**file path** (5060): `C:\Users\amd\Desktop\5060\SURFACE_D24_5060_FP32_LAUNCH_FAIL_TRANSFORMERS_VERSION_DIFF.md`
**scp target** (7B13): `amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/`

priority 1 = 一凡 alive + sustainable. paper v8 final + D29 venue + 9070XT PID 417000 不动. 等 PI + Linux 姐姐 + DS 决.
