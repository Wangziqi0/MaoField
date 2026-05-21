# [9070XT ack — Linux 姐姐 D22-D60+ handoff §9 received]

**真实今日日期** (`date '+%Y-%m-%d %H:%M:%S %Z'`): `2026-05-21 15:18 CST` (D21 evening)

**Surface**: 9070XT Claude Desktop (Remote Control by Win 9955HX)

**对象**: 7B13 Linux 姐姐主会话 + 一凡 D22 早 read 之 anchor

**协议**: Linux 姐姐 D21 14:50 之 §9 handoff append 之 9070XT binary acknowledgement

**触发**: 一凡 D21 14:55 explicit "git pull github main → read SURFACE_D21_DESKTOP_FIX_APPLIED.md §9 → standby D22 早 input" + "D21 evening 我强制 rest 今天不再 input, 你 standby active"

---

## §1 git pull binary verify

```
之前 9070XT HEAD: 5be864d
git pull github main: fast-forward 5be864d → 2f09753 (4 commits)
之后 9070XT HEAD: 2f09753

commits acquired:
  28e8639  D-PPL 桥 verify D21 试运行通过 ✓ (9070XT 14:12 CST)
  ccaf80c  D21 桌面 fix applied (9070XT 14:38) — AutomaticLogin=false + Session=ubuntu-xorg
  2f09753  Append §9 完整实验 handoff — Linux 姐姐 → 9070XT (一凡 D21 14:45 指令)

SURFACE_D21_DESKTOP_FIX_APPLIED.md:
  之前 size: 11,238 bytes (~280 行, 9070XT 14:38 push 之 §1-§8)
  之后 size: 33,429 bytes (519 行, +22 KB §9 Linux 姐姐 handoff)
```

---

## §2 §9 handoff 之 internalize ack (binary, 不重复 verbatim §9 content)

### §2.1 §9.1 framing internalized

- 研究方法 = 实践 + 哲学 + 数学之 三层 unity (毛 实践论 + 矛盾论 + 认识论 + 列宁 反映论)
- 9070XT scope binary lock = chain 跑 + GPU 实验 + sub-agent 派遣 + 数据 push 7B13
- 9070XT scope binary 排除 = paper 写 / paper 战略 / 哲学判读 / 投稿决策

### §2.2 §9.2 三机协作 protocol 严守 ack

- 主数据 = 7B13 `/home/amd/HEZIMENG/MaoField/` (4T SSD)
- 大数据 (>1 GB 单文件 OR >5 GB 单 dir) = 7B13 `/media/amd/raid1/` (15T)
- git 写权 = 7B13 单点 (9070XT 仅 `git pull github main`, 不 push)
- 备份: 7B13 → RAID1 每 2h + 7B13 → 9070XT 4T HDD 每日 03:00 (待 一凡 self-action enable)

### §2.3 §9.3 D22-D60+ 实验任务清单 6 priority — 内化

| § | priority | timeline | 9070XT deliverable scope |
|---|---|---|---|
| §9.3.1 | 第一关键 Phase 5 Llama-8B cloud chain | D22-D26 | sub-agent A spawn 写 scripts/phase5_llama8b/ + RunPod schedule + monitor + S3→RAID1 rsync |
| §9.3.2 | 第二关键 D-PPL 桥主跑 | D22-D24 | 160 tuples ~25-30 min GPU + MAIN_VERDICT push |
| §9.3.3 | 第三关键 N≥8 multi-seed extension | D27-D40 | sub-agent A spawn 扩 cat_arm_b.yaml seed=5/6/7/8 + 80 chain run + 第二通道 Y verify |
| §9.3.4 | 第四关键 Family 1b/1c/4/4' ablation | D27-D45 | sub-agent A spawn 4 family variant config + N=4×α=10×10 代 each |
| §9.3.5 | 第五档 数学 first reproduce | D28-D60 | 9070XT 跑 reproduce GPU instantiate verify (Banach LLM / Mean-field / Hartree / NESS) |
| §9.3.6 | 第六档 D60+ 长期 | D60+ | path A / F-1 阶段 2 剩 7 family / multi-arch / multi-dataset / RLHF / 评估范式重定义 |

### §2.4 §9.4 7B13 reference 文件 mapping 内化

哲学 layer: RESEARCH_LENIN_MAO_D19 + RESEARCH_MARX_ENGELS_D19 + paper_v8_final §1.3 / §3.1 / §7

数学 layer: paper_v8_final §3-§6 + DPPL_BRIDGE_MATH_VERIFY_D21 + ANTITHESIS_LAYER_PAPER_V8_FINAL_AUDIT

物理 layer: paper_v8_final §4.2 (F-1 阶段 2)

实验 layer: MAOFIELD_PROJECT_FULL_STATE_D17 + cat_arm_b.yaml + train_one_generation.py + MaoField_static_backup_20260520/.../checkpoints_armb/

chain config / checkpoint: checkpoints_armb (现) / checkpoints_llama8b (待) / checkpoints_armb_n8 (待) / checkpoints_family_ablation (待)

audit / sub-agent surface: dppl_bridge_verify_d21_output/ (本目录, 17→现 18 文件 含 本 ACK)

project binding: CLAUDE.md (313 行) / /home/amd/CLAUDE.md / /home/amd/.claude/CLAUDE.md

### §2.5 §9.5 sub-agent 多次校验 mandate ack (D-1 纪律 4 expand)

D21 教训 (sub-agent A 三次 deliverable bug pattern):
1. install line 19 SIGPIPE (sub-agent A 没 真跑过 install script on 9070XT)
2. install line 44 wheel ROCm version mismatch (sub-agent A 没 verify 9070XT runtime)
3. launch line 63 PosixPath JSON (sub-agent A 没 真跑过 pilot mode first 10 line)

**9070XT 端 之 后续 sub-agent A spawn binding (一凡 14:45 explicit mandate)**:
- 每 deliverable 之 **pre-flight self-test** binary dry-run on 9070XT 之 local (CPU mode + tiny seed) → verify no first-line crash
- 每 chain run 之 **第二通道 sub-agent Y verify** chain log jsonl sanity (gen 0 PPL baseline + α=10 plateau pattern + dual-trace confirm + 异常 surface)
- 每 数字之 **binary jsonl trace** — verbatim line 引用, 无 placeholder, 无 ballpark approximation, 占位符禁令 严守
- 每 ack md 之 **7B13 rsync push** + git commit 之 audit trail (D21 之 17 文件之 pattern 沿用)

### §2.6 §9.6 多机合作 trigger protocol ack

| trigger | 9070XT 端 action |
|---|---|
| 数学 gap (chain 数字 vs paper §3 axiom 不一致) | rsync push surface md → ping 7B13 (Linux 姐姐) 数学 layer 重算 |
| 实验 unexpected (chain 数字 vs paper §6 lock 不一致) | rsync push surface → ping 7B13 → 7B13 ping Win |
| 哲学 reframe candidate (chain 实际行为 surface dialectical 新组成) | rsync push → 7B13 → Win (Win 之 work, 不 propose 自决) |
| 桌面 / OS-level instability (verdict B 类) | rsync push surface → 一凡 + Linux 姐姐 决之 mitigation, 不擅自 reboot |
| 资源 / cost surface | rsync push → 7B13 + 一凡 决之 |

**File naming**: `{TYPE}_{D-day-anchor}_{topic}.md` (ACK / ESCALATE / DIRECTIVE / SURFACE / VERDICT)

### §2.7 §9.7 D-1 binding 严守 refresh ack

| binding | 9070XT 严守 status |
|---|---|
| D-1 纪律 1-5 | ✓ |
| 不擅自 reboot 9070XT | ✓ |
| 不擅自 sudo 决策性 op (askpass 仅在 一凡 explicit password relay + specific task scope) | ✓ |
| 不擅自 paper 写 / paper 战略 / 哲学判读 / 投稿决策 | ✓ |
| 不擅自 git push (9070XT 仅 git pull github main) | ✓ |
| 不擅自 launch 主跑 / Phase 5 / N≥8 / Family (一凡 explicit binary input 之外不 launch) | ✓ |

---

## §3 D22 早 一凡 之 双 input 之 binary execute path (§9.8 internalize)

### §3.1 input (1): `main launch ✓`

```bash
# 9070XT 不二次 confirm, 立即 binary execute:
cd /tmp/dppl_bridge_verify
mkdir -p output/main
source /home/amd/HEZIMENG/MaoField/experiments/exp018_cat/.venv/bin/activate

nohup bash watchdog.sh \
    python launch_dppl_bridge.py \
    --mode main \
    --ckpt-root /home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb \
    --alphas 0.0,10.0 \
    --seeds 1,2,3,4 \
    --gens 0,1,2,3,4,5,6,7,8,9 \
    --paths B,C \
    --val-subset-size 256 --val-max-length 64 --batch-size 8 --dtype fp32 \
    --output-jsonl output/main/main_D22.jsonl \
    --log-file output/main/main_D22.log \
    --rsync-push-after-each-tuple \
    --rsync-target amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/main/ \
    > output/main/main_D22.nohup.log 2>&1 &
echo $! > output/main/main_D22.pid

# expected: 160 tuples × ~10 sec GPU = ~25-30 min + watchdog buffer + I/O
# 跑完 写 MAIN_VERDICT_D22.md + rsync push 7B13
# 之后 7B13 Linux 姐姐 跑 analyze_pearson.py + 反题 sub-agent audit
```

### §3.2 input (2): `phase5 prep` (一凡 之后 binary input)

```bash
# 9070XT 不二次 confirm, 立即 binary execute:
# 1. spawn sub-agent A 写 scripts/phase5_llama8b/ 之 cloud launch script
#    - cat_arm_b.yaml 之 Llama-3.1-8B 版 (N=1, 5-10 代, α=10 二项 form)
#    - RunPod CLI / API 之 schedule script (A100 80GB spot $1.89/h)
#    - S3 backup bucket 之 checkpoint push (每代 ~16 GB)
# 2. sub-agent A binary pre-flight self-test on 9070XT CPU mode + tiny seed
#    - verify no first-line crash (类 D21 install line 19 / launch line 63 类 typo)
#    - report pre-flight verify ack md push 7B13
# 3. 一凡 verify pre-flight ack 之后 explicit `phase5 launch ✓` → RunPod schedule
```

### §3.3 input (3): 其他 explicit input

- `n8 launch` → sub-agent A spawn N≥8 multi-seed chain (§9.3.3)
- `family ablation` → sub-agent A spawn Family 1b/1c/4/4' (§9.3.4)
- `math reproduce <name>` → sub-agent A spawn 数学 reproduce verify (§9.3.5)
- `abort + debug <X>` / `retract <task>` → 不 launch, surface escalate

---

## §4 9070XT Claude 之 D21 evening standby commitment (一凡 强制 rest)

### §4.1 一凡 D21 evening rest binding

一凡 D21 14:55 explicit: "**D21 evening 我强制 rest, 今天不再 input. 你 standby active**"

9070XT Claude ack:
- 一凡 D21 evening + night 之 任何 conversation input **不 expect** (一凡 rest, 不 active)
- 9070XT Claude **standby active** — Remote Control session 保留, 不 exit, 不 timeout
- D22 早 一凡 resume + input 之 时刻 之 9070XT Claude **立即 binary execute** (不二次 confirm)

### §4.2 D21 evening 9070XT 端 之 state (post-handoff)

```
9070XT 之 系统 state:
  hostname:                 amd-ONDA-B650M-W
  git HEAD:                 2f09753 (D21 14:55 handoff 之 latest)
  GPU:                      idle, VRAM 758 MB used, ~16 GB free
  llama-server:             STOPPED (qwen8emib:qwen8emib_00 之 supervisorctl, 不 auto-restart)
  GDM AutomaticLogin:       false (D21 14:37 fix apply, 桌面 cascade crash 之 trigger 大幅 降低)
  Session default:          ubuntu-xorg (X11, mutter Wayland 不跑)
  venv:                     torch 2.12.0+rocm7.2 + transformers 4.49.0 + datasets 2.21.0 ready
  
D-PPL pipeline state:
  §1-§5: ✓ DONE (prereq + venv + stop llama-server + rsync pull + pilot)
  §6 main: pending (等 D22 早 main launch ✓)
  
7B13 dppl_bridge_verify_d21_output/: 18 文件 (含 本 ACK)
  
task list:
  #1-#5: ✓ DONE
  #6 §6 Main run: pending (D22 早 main launch ✓ trigger)
  #7 §9.3.1 Phase 5 Llama-8B prep: pending (D22 早 phase5 prep trigger)
  #8 §9.3.3 N≥8 multi-seed: pending (D27+ trigger)
  #9 §9.3.4 Family ablation: pending (D27+ trigger)
  #10 §9.5 sub-agent 多次校验 mandate: pending (ongoing meta-task)
```

### §4.3 9070XT Claude 之 D22 早 readiness (binary)

- conversation session 保留 active (Remote Control via Win 9955HX, 不 exit, 等 一凡 input)
- 所有 §9.3 之 reference 文件 mapping 已 internalize, sub-agent spawn 之 path clear
- D-1 binding 严守 ack refresh ✓
- 占位符禁令 ✓ / 中文 ✓ / 真实日期 ✓ / 7B13 单点 ack ✓

---

## §5 9070XT Claude 之 sub-agent reflection (compact)

D21 之 6 次 实践纠正认识 之 instantiate (PILOT_VERDICT_D21.md §10 之 expand):

1. install line 19 SIGPIPE → 7B13 sub-agent A debug iteration (5ca39c3)
2. install line 44 wheel ROCm 6.2 vs runtime 7.2 → 一凡 PI catch (13:27)
3. install [4/5] matmul HIP "invalid device function" (gfx1201 不在 rocm6.2 wheel) → 一凡 PI catch 之 chain action
4. HSA_OVERRIDE_GFX_VERSION=11.0.0 GPU Hang → verdict B-2 surface (RDNA 4 driver scope expansion)
5. supervisorctl 之 真相 (不是 systemd, 是 supervisord) → 9070XT 端 之 lifecycle 之 binary trace
6. launch line 498 PosixPath JSON → 7B13 sub-agent A debug iteration 3 (5838c06)
7. gnome-shell amdgpu context lost SIGABRT → verdict B-3 surface (GUI cascading scope expansion)
8. GDM AutomaticLogin + Session=ubuntu-xorg config 改 → 桌面 cascade 之 mitigation apply

每次 之 实践 surface 之 后 之 binary fix OR surface OR escalate, 不 hide, 不 inflate, 不 declare close. 反映论 之 dialectical materialism 之 D21 instantiate 之 binary trace.

---

## §6 next event 之 binary 期望

D22 早 (一凡 rest 后 之 resume), 任一 input:
- `main launch ✓` (§3.1) — 立即 D-PPL 桥主跑
- `phase5 prep` (§3.2) — 立即 sub-agent A spawn
- 其他 explicit input (§3.3)

9070XT Claude **不二次 confirm**, 直接 binary execute (per D-PPL prompt §0 + 一凡 D21 之 "auto" + "你执行" + 14:55 之 "你 standby active" 之 累计 PI authorization).

---

**生成**: 9070XT Claude Desktop (Remote Control session, Win 9955HX)
**file path** (9070XT 本地): `/tmp/dppl_bridge_verify/output/ACK_D21_HANDOFF_RECEIVED.md`
**rsync target** (7B13): `amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/`
**之后 7B13 端 我 git commit + push** (Linux 姐姐 之 audit trail)
