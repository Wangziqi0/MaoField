# [9070XT RESUME — Cell B retry-C verdict + 5060 R1 cross-channel + SIGCONT cuda context stale FAIL + --resume relaunch PASS]

**真实今日日期** (`date '+%F %T %Z'`): `2026-05-25 13:23 CST` (D25)

**Surface**: 9070XT (22) cell B retry-C 跑完 (12:10) + SIGCONT PID 417000 fail (13:18) + --resume relaunch PASS (13:22)

**对象**: 7B13 Linux 姐姐主会话 + 一凡 D25 PI 决 input

**协议**: D-1 纪律 5 (错误 surface 不静默) + D-3.7 PI 主权 (不擅 declare P0★-G root cause final close)

**触发**: PI sequence step 5 写 RESUME_AFTER_CELL_B_AND_CUDA_CONTEXT_STALE_FAIL md sibling RESULT_CELL_B_D25_12_10 + RESUME_LAUNCH_D24_16_40 + TERMINATION_D24_15_33

---

## §1 cell B retry-C verdict (引用 RESULT_CELL_B_D25_12_10_20260525.md §1, 不 repeat full content)

| 项 | 值 |
|---|---|
| yaml | cat_arm_b_fp32_9070XT_gc.yaml (3 处 diff: dtype fp32 + fp16=false + gradient_checkpointing=true) |
| seeds × alphas × gens | 42 × 0.0 × 1 |
| wall-clock | 1h 15m 1s (D25 10:55:11 → 12:10:12) |
| **a1_ppl** | **None (NaN)** |
| val_loss | None (NaN) |
| a2 / a6 | [nan × 12 层] |
| event | chain_gen_done (success, n_done=1/1, 但数值不健康) |

retry sequence: first (OOM) → B fast try (核心已转储) → **C (chain_gen_done 写, 但 a1_ppl NaN)**.

---

## §2 5060 R1 cross-channel verify (引用 RESULT_CELL_B §2)

| 项 | 5060 R1 (Blackwell cu130) | 22 端 cell B retry-C (RDNA4 ROCm 7.2) |
|---|---|---|
| yaml sha256 | 同 D24 SMOKE bit-level identical | 与 fp16 main yaml 之 3 处 diff |
| a1_ppl (seed=42 α=0 gen=0) | **36.536 healthy** (paper §4.6 mean 36.32 之 ballpark match) | **None (NaN)** |

stack diff isolate ROCm 7.2 + gfx1201 stack 之 dominant root candidate ★★★★.

---

## §3 framing update (引用 RESULT_CELL_B §3, two distinct issues)

| issue | tier | binary backing |
|---|---|---|
| **(a) ROCm 7.2 + gfx1201 stack dominant new root** | ★★★★ | R1 cross-channel isolate, 22 端 fp16/fp32 双 dtype 同 NaN |
| **(b) fp16 GradScaler skip partial root** | ★★★ | D24 之 fp16 a1=93 vs fp32 a1=36 之 partial confirm |

22 端先前 framing "fp16 不是 root" 之 partial 错 之 honest disclose: **fp16 仍 partial root, ROCm 7.2 + gfx1201 stack 是 new dominant root** (RESULT_CELL_B §3.2).

---

## §4 SIGCONT PID 417000 fail binary surface (D25 13:18:20)

### §4.1 SIGCONT 之后 5 sec 内 PID 417000 死

- SIGCONT ts: D25 13:18:20 CST
- death ts: ~13:18:25 CST (~5 sec 之后)
- death mode: 核心已转储 exit
- SIGSTOP duration: ~2h 44m (10:34:52 → 13:18:20)

### §4.2 root cause = HIP error `unspecified launch failure`

nohup log tail verbatim:

```
what():  CUDA error: unspecified launch failure
Search for `hipErrorLaunchFailure' in https://rocm.docs.amd.com/projects/HIP/en/latest/index.html
CUDA kernel errors might be asynchronously reported at some other API call
For debugging consider passing AMD_SERIALIZE_KERNEL=3
Exception raised from SetDevice at /pytorch/c10/hip/HIPFunctions.cpp:334

frame #3: c10::cuda::SetDevice(signed char, bool)
frame #6: at::_ops::_local_scalar_dense::redispatch
frame #9: at::native::item
```

SIGCONT 之后第一次 CUDA call (SetDevice) 即 fail. cuda context stale risk 兑现.

### §4.3 SIGSTOP duration vs PI estimate diff

| 项 | 值 |
|---|---|
| PI estimate SIGSTOP duration | ~8h (cell B real run estimate) |
| actual SIGSTOP duration | **2h 44m** (cell B retry-C 实际 1h 15m + 之间 cell B first try + B fast try 之 process churn ~1.5h) |
| cuda context stale 之 trigger duration | **< 2h 44m** (binary evidence preserve) |

binary surface: cuda context stale 之 trigger duration **小于 8h 之 estimate**, 实际 2h 44m 已 trigger. 之 reality 比 β midtest 之 30 min PASS + 16× extrapolation 之 estimate 严. 候选 root (不 declare):
1. cell B 之 3 次 process churn (first OOM + B fast try abort + C 之 fp32 load) 之 GPU state 之 多次 reset 之 累积 effect
2. SIGSTOP > 30 min 之 之 之 driver 之 之 context evict 之 之 threshold
3. ROCm 7.2 gfx1201 之 multi-process GPU sharing 之 specific issue (与 §3 之 dominant root candidate 之 之 之 之 之 之 同一 stack issue 之 candidate)

留 PI + 反题三方 + 数学子协作者决.

---

## §5 --resume relaunch binary verify PASS (D25 13:22:29)

### §5.1 launch cmd (同 D24 16:40 pattern, 仅 nohup log file name diff)

```bash
cd /home/amd/HEZIMENG/MaoField/experiments/exp018_cat && \
source .venv/bin/activate && \
setsid nohup \
  env CUDA_VISIBLE_DEVICES=0 HIP_VISIBLE_DEVICES=0 ROCR_VISIBLE_DEVICES=0 \
  python scripts/candidate_c_runner.py \
    --seeds 42,1337,2024,7,137,271 \
    --alphas 0,5,10 \
    --gens 10 \
    --device cuda \
    --output-dir /tmp/dppl_bridge_verify/output/candidate_c \
    --rsync-target amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/candidate_c/ \
    --resume \
  > /tmp/dppl_bridge_verify/output/candidate_c/candidate_c_resume_d25.nohup.log 2>&1 \
  < /dev/null \
  & disown $!
```

### §5.2 launch 后 binary verify @ 13:22:37 (sleep 8 sec)

| 项 | 期望 | 实际 |
|---|---|---|
| New PID | 找到 | **491900** ✓ |
| PPID | ≠ 1 (5-layer detach pattern, PI α 决 accept) | 491897 (setsid bash child) ✓ |
| **PGID = PID** | session leader | 491900 ✓ |
| **SID = PID** | new session | 491900 ✓ |
| etime | ≥ 5 sec | 8 sec ✓ |
| stat | R 或 S | **Ssl** ✓ (init load wikitext-2) |
| jsonl 行数 | 120 stable | **120 ✓** (resume skip 阶段不写新 entry) |
| nohup log | RESUME logger 行 | `>>> RESUME: 用 existing jsonl=...` + `加载 wikitext-2 cache_dir=...` 之 init phase 之 logger 行 ✓ (`>>> RESUME: 120 tuples 已 done` 之 load_done_set 之后 logger 行 之 ~1 min 之后才写) |

binary 整体 PASS ✓.

### §5.3 120 / 180 chain evidence preserve ✓

| evidence | path | 状态 |
|---|---|---|
| jsonl | /tmp/dppl_bridge_verify/output/candidate_c/candidate_c_20260522_203837.jsonl (120 行) | ✓ preserved |
| ckpt | /tmp/dppl_bridge_verify/output/candidate_c/checkpoints/alpha*/no_preserve_seed*/generation_*/ | ✓ preserved |
| nohup log (D22-D24) | /tmp/dppl_bridge_verify/output/candidate_c/candidate_c.nohup.log + candidate_c_resume_d24.nohup.log | ✓ preserved |
| nohup log (D25 relaunch) | candidate_c_resume_d25.nohup.log (新 file) | ✓ new |
| rsync 7B13 | 持续 push 自动 (--rsync-target 同 D24) | ✓ |

---

## §6 ETA estimate

- 当前 120 / 180 (66.67%)
- 剩 60 代 × ~33.7 min/代 ≈ **20.2 h**
- 完成 estimate: D25 13:22 + 20h ≈ **D26 ~09:00 CST 跑完整 180/180**
- D29 投稿 timeline (5/29) 余 ~3 天 buffer ✓

---

## §7 9070XT 不擅 declare list (D-3.7 严守)

| 不 declare | 留谁决 |
|---|---|
| P0★-G ★★ FATAL critical reproducibility break candidate 之 root cause final close (two distinct issues 之 之间 之 关系) | PI + 反题三方 + 数学子协作者 |
| cuda context stale trigger duration < 2h 44m 之 root cause | PI + 数学子协作者 |
| paper v8 final 47/47 + 反题 6 P0★ disclosed 之 改动 (扩 G) | 反题三方决 |
| paper §5.2 之 Shumailov §5.2 hard binding 之 改动 | PI + 反题三方 + Linux 姐姐 |
| cat_arm_b.yaml main run binding 之 改动 (batch / lr / epoch / fp16) | PI + Linux 姐姐 |
| candidate_c_runner.py / multi_layer_hook.py / train_one_generation.py 之 code 改动 | Linux 姐姐 单点写权 |
| D29 venue (arXiv + TMLR + KBS 三 leg) 之 改动 | PI 关卡 4 决 |
| 5060 之 setup / cell B 之 follow-up | PI 决 |
| PID 491900 之 SIGSTOP / kill / fix | PI 决 |

---

## §8 D-1 + D-3 binding 严守 ack (本 RESUME 自检)

| binding | binary verify |
|---|---|
| D-1 纪律 1 (不等数据不写声明) | ✓ cell B + R1 cross-channel + SIGCONT fail + relaunch PASS 全 jsonl + ps + nohup log raw, 无 [?] |
| D-1 纪律 2 (48h 反馈真空不存活) | ✓ cell B 12:10 完成, RESULT_CELL_B 13:18 写, SIGCONT 13:18 fail, relaunch 13:22, 本 RESUME md 13:23 write (~1h 内全部 surface) |
| D-1 纪律 3 (代码先于 paper) | ✓ jsonl + ps + nohup log + HIP error stack trace 之 binary 实测, 不基于 paper 假设 |
| D-1 纪律 4 (子协作者验证) | ✓ 22 端 + 5060 R1 + 反题 sub-agent 三通道 cross-check (RESULT_CELL_B §2-§3) |
| D-1 纪律 5 (错误 surface 不静默) | ✓ 22 端 12:10 inline "fp16 不是 root" partial 错 之 honest disclose + cuda context stale trigger duration < 8h estimate 之 honest disclose |
| D-1 纪律 5 sub-rule (真实日期) | ✓ head line `date` verbatim D25 13:23 CST |
| D-3.7 PI 主权 binding | ✓ 9 项不 declare list (§7) 全留 PI + 反题三方 + 数学子协作者 + Linux 姐姐决 |

---

## §9 priority 1 = 一凡 alive + sustainable (safety binding standing)

- 010-82951332 / 400-161-9995 hotline standing
- 三个安全检查 standing (绳子 / 安全物理环境 / 主治医生电话)
- 一凡 16 岁双相 + 焦虑, D22 + D23 早 surface 自杀信号
- **D25 cognitive load 高**: R1 verdict + cell B retry-C verdict + cuda context stale fail + framing reframe 之 cognitive surge trigger candidate. 不 push 紧急 paper 改动决.
- 不绕弯, 不 lecture, 不 push paper acceptance bargain
- 本 RESUME md 是工程层 binary record + sequence step 5 之 deliverable, 不挤 PI 决策节奏

---

**生成**: 9070XT (22) Claude Code Opus 4.7 (1M context), D25 cold-start 新 session
**file path** (22 本地): `/tmp/RESUME_AFTER_CELL_B_AND_CUDA_CONTEXT_STALE_FAIL_D25_13_22_20260525.md`
**rsync target** (7B13): `amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/RESUME_AFTER_CELL_B_AND_CUDA_CONTEXT_STALE_FAIL_D25_13_22_20260525.md`

握着. D-1 纪律 5 严守 (cuda context stale trigger duration < 8h estimate 之 honest surface). D-3.7 PI 主权 严守. PID 491900 continue monitor + 等 PI 后续指令.
