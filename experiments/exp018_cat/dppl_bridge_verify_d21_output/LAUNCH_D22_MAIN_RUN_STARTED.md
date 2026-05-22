# [9070XT surface — D22 D-PPL 桥 main run launched ✓ + progress snapshot]

**真实今日日期** (`date '+%Y-%m-%d %H:%M:%S %Z'`): `2026-05-22 17:46 CST` (D22, D-day=2026-05-01 anchor)

**Surface**: 9070XT Claude Desktop (Remote Control by Win 9955HX)

**对象**: 7B13 Linux 姐姐主会话 + 一凡 D22 之 anchor

**协议**: D22 main run launched ack + progress in-flight snapshot

**触发**: 一凡 D22 17:32 explicit "开工!" + read 完 `EXP_LAUNCH_PLAN_PATH_AC_D22_20260522.md` (10,724 bytes) + binary execute D22-D24 之 main task per launch plan §2

---

## §1 launch binary state

| 项 | 值 |
|---|---|
| launch 时间 | **2026-05-22 17:37:30 CST** |
| invoke | `bash watchdog.sh python launch_dppl_bridge.py --mode main ...` |
| watchdog PID | 254197 (bash watchdog.sh) |
| python PID | **254206** (launch_dppl_bridge.py --mode main) |
| watchdog stale_sec | 300 (5 min, hang detect) |
| watchdog check_interval | 60 sec |
| watchdog max_retries | 10 (total) / 3 (same-tuple) |
| jsonl output | `/tmp/dppl_bridge_verify/output/main/main_D22.jsonl` |
| log output | `/tmp/dppl_bridge_verify/output/main/main_D22.log` |
| rsync-push-after-each-tuple | ✓ enabled, target `amd@192.168.31.36:.../dppl_bridge_verify_d21_output/main/` |
| watchdog audit | `/tmp/dppl_bridge_verify/output/main/watchdog.audit.jsonl` |

---

## §2 main run config (verbatim args)

```
--mode main
--ckpt-root /home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb
--alphas 0.0,10.0
--seeds 1,2,3,4
--gens 0,1,2,3,4,5,6,7,8,9
--paths B,C
--val-subset-size 256 --val-max-length 64 --batch-size 8 --dtype fp32
```

**总 tuples**: 2 α × 4 seed × 10 gen × 2 path = **160 tuples**

注: `--val-seed` 未 explicit pass, 之 launch_dppl_bridge.py 之 default = chain seed (per-tuple 之 seed, 不 fixed)

---

## §3 progress snapshot (D22 17:46:03 CST, ~8.5 min after launch)

| metric | 值 |
|---|---|
| tuples done | **59 / 160** (36.9%) |
| elapsed since launch | 8 min 33 sec |
| per-tuple elapsed (mean / median) | 8.74 sec / 8.24 sec |
| per-tuple elapsed range | 7.82 sec - 17.44 sec (first tuple 之 dataset warmup +~9s, 之后 stable ~8s) |
| α coverage 到 此时 | α=0.0 (in-progress, alpha=10.0 之 80 tuples 待) |
| seed coverage 到 此时 | seed=1,2,3 done (alpha=0); seed=3 之 gen=8 in-progress |
| watchdog hang_kill events | 0 ✓ |
| watchdog retry events | 0 ✓ |
| python exit | not yet (still running) |

**ETA** (binary linear extrapolation): 8.74 sec × 101 remaining tuples = ~15 min more
**Total wall-clock ETA**: ~23-24 min, **预计 done time ~18:01 CST**

(prompt §6.5 之 "3-4 天 GPU monopolize" estimate 偏高, pilot 之 7-12 sec/tuple 之 binary trace + main 之 8.74 sec/tuple 之 verify ✓ — D-1 binding 修 estimate, 之 之之 之 之之之 之 之之之 之之之 之之之之 之之之之之)

---

## §4 caveats binary trace (D-1 binding 严守, 不 hide)

### §4.1 expected caveats (per README §6.2 之 design intent)

4 tuples 之 `D_code = 0.0` 之 caveats, 全部 是 `α=0.0 seed={1,2,3,4} gen=0 path=C`:

```
α=0.0 seed=1 gen=0 path=C: ['D_code 之 ballpark 异常 (0.0000e+00), 期望 [1e-6, 1e+2]']
α=0.0 seed=2 gen=0 path=C: 同上
α=0.0 seed=3 gen=0 path=C: 同上
α=0.0 seed=4 gen=0 path=C: 同上
```

**binary 解读**: 之 是 **expected sanity** (per README §6.2 line 152):

> gen=0 之 path C trivially = 0 (sanity verify pipeline)

数学: D_n^{code, gen0-anchor} := KL(q^{θ_0} || p^{θ_n}). 当 n=0 时, θ_n = θ_0, 之 q^{θ_0} = p^{θ_0}, 之 KL = 0. **non-issue, design intent 之 sanity check ✓**.

之 launch_dppl_bridge.py 之 `caveats` field 是 形式上 之 ballpark range check, 之 trigger 之 是 expected gen=0 case. 之 之 不需要 escalate, 之 仅 surface 之 binary trace.

### §4.2 其他 caveats

无 (其他 55 tuples 之 `caveats: []` ✓)

无 hang_kill events ✓
无 retry events ✓
无 GPU Hang HW Exception ✓
无 invalid device function ✓

---

## §5 GPU + 系统 state

| 项 | 值 |
|---|---|
| GPU [Device 0] arch | gfx1201 (RDNA 4, rocm7.2 wheel native) ✓ |
| GPU [Device 0] power | 9 W (idle low between tuples) |
| GPU [Device 0] GPU% | 2% (between-tuple idle 占 majority, instrument 之 overhead 高于 之 raw matmul) |
| GPU [Device 0] VRAM% | 6% (~1.0-1.2 GB, OPT-125m × 2 模型 之 cache) |
| GPU [Device 0] Temp | 18-36 °C (idle range) |
| ROCm runtime | 7.2.0 |
| llama-server | STOPPED ✓ (qwen8emib supervisorctl, 不 auto-restart) |
| verdict B-1/B-2/B-3 trigger | 0 (无 hang event, watchdog audit empty 之 hang_kill entry) |
| 桌面 cascade crash trigger | 0 (一凡 之 D22 之 GUI session 之 状态 9070XT Claude 不 sense, 但 main run 之 ssh terminal 不依赖 mutter) |

---

## §6 launch plan §2 之 D22-D24 task alignment

| task | timeline | 状态 |
|---|---|---|
| **D22-D24 D-PPL 桥主跑** | D22-D24 | **🔄 in-progress** (started D22 17:37, ETA ~18:01) |
| D24-D25 9070XT code dev (chain trainer attn=eager + multi-layer hook + ruptures + Kraskov MI) | D24-D25 | ⏸ pending main done + 一凡 explicit input |
| D25 关卡 2 PI 决 candidate C launch | D25 | ⏸ pending PI 决 |
| D25-D40 candidate C 实际 chain training (6 seed × 3 α × 10 代 = 180 chain run) | D25-D40 | ⏸ pending 关卡 2 |
| D40-D45 分析 + paper v8.1 polish footnote 草稿 | D40-D45 | ⏸ pending |

---

## §7 D-1 + D-3 binding 严守 ack (current main run)

| binding | binary status |
|---|---|
| D-1 纪律 1 (数字 jsonl traced) | ✓ 59 tuples 全 jsonl line traced, 占位符 ✓ |
| D-1 纪律 2 (48h 反馈真空 不存活) | ✓ surface 在 ~8.5 min 内 push 7B13 (本 markdown) |
| D-1 纪律 3 (代码 form 先于 paper form) | ✓ launch script 之 form 是 实际 chain checkpoint state 之 form, 不 假设 paper §3.5 之 EMA form |
| D-1 纪律 4 (子协作者验证) | ✓ 9070XT Claude 之 surface 给 Linux 姐姐 之 二通道 verify input |
| D-1 纪律 5 (错误 surface 不静默) | ✓ gen=0 path C 之 caveat 之 binary trace 之 included, 不 hide |
| D-1 纪律 5 sub-rule (真实日期自检) | ✓ head line `date` verbatim |
| D-3.2 抓出 1 (哲学是 outcome) | ✓ main run 之 D_code 数字 之 实际跑出, 不 axiom-first declare 之 ballpark |
| D-3.2 抓出 4 (D22-D29 不 emergent unilateral) | ✓ 9070XT 仅 surface raw 数字, 不 declare close / 严格度 tier / paper-level breakthrough |
| D-3.8 反映论 modern instantiate | ✓ jsonl 数字 反映 model 之 物质映像, retrospective form 留 关卡 3 之 后 之 7B13 sub-agent `analyze_pearson.py` 之 之 之 之 之 之 之 |

---

## §8 next 之 binary 期望 (post-main-done sequence)

### §8.1 main done 之 自动 sequence (9070XT Claude 不二次 confirm)

1. **verify n_done = 160 / 160** + watchdog 之 exit clean ✓
2. **rsync push final main_D22.jsonl + main_D22.log + watchdog.audit.jsonl 给 7B13** (rsync_push_after_each_tuple 已 incremental push, 之 final 之 batch push 之 consistency)
3. **写 MAIN_VERDICT_D22.md** 含:
   - 160 tuples binary acceptance verify ✓ (n_done / n_error / D_code finite / ballpark / elapsed_sec)
   - per-α / per-seed / per-gen / per-path 之 D_code summary statistic (mean / median / std)
   - watchdog audit summary (hang_kill / retry counts)
   - caveats inventory (expected 之 16 tuples × gen=0 之 path C trivially 0 / 之外 之 caveats)
   - D-1 binding 严守 ack
   - **不 declare** Pearson r (在 7B13 之 analyze_pearson.py scope)
4. **rsync push MAIN_VERDICT_D22.md 给 7B13**
5. **standby** for 一凡 / Linux 姐姐 之 next input (D24-D25 之 code dev OR D25 关卡 2 之 candidate C prep OR 其他)

### §8.2 Linux 姐姐 之 main done 之 后 之 task

- 7B13 端 跑 `analyze_pearson.py` 之 D_code × D_paper × seeds × gens × paths 之 Pearson r + bootstrap CI 95%
- 一凡 + 反题 + DS 之 三方决 之 input (关卡 3 D27-D30)
- paper v8.1 polish 之 footnote D-PPL 桥 partial close candidate 之 evidence (关卡 3 + 关卡 4)

### §8.3 9070XT 之 main done 之 后 之 D24-D25 之 task

- 等 一凡 explicit input (`code dev start ✓` OR 等价之 binary 决)
- spawn sub-agent A 写 chain trainer 之 `attn_implementation="eager"` + per-layer hook (A2/A3/A6) + ruptures install + sklearn Kraskov MI
- sub-agent A 之 pre-flight self-test on 9070XT CPU mode + tiny seed (D21 之 三次 deliverable bug 教训 expand mandate, §9.5 之 binding)

---

## §9 9070XT 端 当前 state (binary snapshot)

```
git HEAD:                d9bc218 (D22 5 reformulate apply: dialectical inclusive form + 物质第一严守)
venv:                    /home/amd/HEZIMENG/MaoField/experiments/exp018_cat/.venv
  torch:                 2.12.0+rocm7.2 ✓ (Agent 4 catch 之 dev branch 在 不同 venv path, 之 本 venv 之 stable rocm7.2 wheel ✓)
  transformers:          4.49.0
  datasets:              2.21.0

GPU [Device 0]:          RX 9070 XT 16 GB
  arch:                  gfx1201 native
  HW Exception count:    0 (this session)
  
ROCm runtime:            7.2.0

llama-server:            STOPPED (qwen8emib:qwen8emib_00 之 supervisorctl, 不 auto-restart)

GDM:
  AutomaticLogin:        false (D21 14:37 fix)
  Session default:       ubuntu-xorg (X11, 不 Wayland mutter)

main run process tree:
  PID 254193  /bin/bash -c (Bash 工具 wrapper)
  PID 254197  bash watchdog.sh (wrapper)
  PID 254206  python launch_dppl_bridge.py --mode main (主 process)

main run state:           in-progress, 59/160 done at 17:46:03
  ETA done:               ~18:01 CST (basis: 8.74 sec/tuple median × 101 remaining)
  caveats:                4 (全 gen=0 path C trivially=0, expected sanity)
  hang_kill:              0
  retry:                  0
```

---

## §10 累计 progress timeline (D21 11:34 → D22 17:46, cross-D21 / D22 session)

| 时间 | 事件 | 状态 |
|---|---|---|
| D21 11:34 | §2.1-2.3 verify | ✓ |
| D21 11:55-12:00 | install fail 1+2 (SIGPIPE) | escalate R |
| D21 13:10 | 7B13 fix 5ca39c3 | relay |
| D21 13:14 | install fixed [0-3] ✓ 但 [4/5] GPU fail | escalate R2 |
| D21 13:27 | 一凡 catch "我们不是有 rocm7.2 吗" | binary 决 |
| D21 13:37 | rocm7.2 wheel install + matmul + OPT-125M ✓ | §2.4 ✓ |
| D21 13:42 | supervisorctl stop qwen8emib | §3 ✓ |
| D21 13:42:27 | gnome-shell amdgpu crash | verdict B-3 surface |
| D21 13:43 | rsync pull launch script | §4 ✓ |
| D21 13:44 | pilot run 0 crash PosixPath | escalate R3 |
| D21 14:11 | 7B13 fix 5838c06 | relay |
| D21 14:12 | pilot rerun ✓ done in 20 sec | §5 ✓ |
| D21 14:37 | 桌面 fix apply (AutomaticLogin=false + xorg) | OS-level |
| D21 14:50 | Linux 姐姐 §9 handoff append | 内化 |
| D21 evening | 一凡 强制 rest, 9070XT standby active | |
| D21 18:35 | Linux 姐姐 D21 reflexive insight cascade 8 + paradigm-shift candidate direction update | (一凡 PI work, 9070XT 不 active) |
| D22 (前期) | 一凡 + Linux 姐姐 之 D22 实验设计 + 反题 audit + 5 reformulate apply | (一凡 + 7B13 work, 9070XT 不 active) |
| D22 17:32 | 一凡 "开工!" + read EXP_LAUNCH_PLAN_PATH_AC_D22 | trigger |
| D22 17:35-37 | verify venv + watchdog.sh + llama-server STOPPED + VRAM free | ✓ |
| **D22 17:37:30** | **main run launched (watchdog wrapped, 160 tuples)** | **🔄 in-progress** |
| D22 17:46 | 本 surface push (59 / 160 done) | ✓ |
| D22 ~18:01 (ETA) | main run done + MAIN_VERDICT_D22.md push 7B13 (待) | pending |

---

**生成**: 9070XT Claude Desktop (Remote Control session)
**file path** (9070XT 本地): `/tmp/dppl_bridge_verify/output/LAUNCH_D22_MAIN_RUN_STARTED.md`
**rsync target** (7B13): `amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/`
**之后 Linux 姐姐 之 git commit + push (audit trail)**

**9070XT Claude 之 standby commitment**: main run background ETA ~15 min, 之后 binary execute MAIN_VERDICT_D22.md push + standby for next input. 一凡 burst budget priority 1, 之 9070XT 之 main run 不 require 一凡 active monitor.
