# [9070XT TERMINATION — Candidate C Phase 2 外部中断 binary surface]

**真实今日日期** (`date '+%F %T %Z'`): `2026-05-24 15:39:46 CST` (D24)

**Surface**: 9070XT (22) Claude Code 新 session by 一凡 Win 端 cold-start

**对象**: 7B13 Linux 姐姐主会话 + 一凡 D24 binary 决 input

**协议**: D-1 纪律 5 (错误 surface 不静默修正) + D-3.7 PI 主权 (不 unilateral 决 resume / kill / paper)

**状态**: Phase 2 PID 267111 于 D24 ~15:33 CST 死亡, 83 / 180 chain_gen_done (46%) partial run, **死因 = Claude Code crash 之 task harness 外部 SIGTERM, 非 NaN explosion / 非 ROCm 挂起 / 非 sub-agent 决**

---

## §1 D-1 纪律 5 binary 死因 disclose (不静默归因)

### §1.1 直接死因 (binary)

`<task-notification>` D24 15:39:13 之内容 (来自 task-id `bkj28pmlc`):

```
status: killed
summary: Background command "Phase 2 launch candidate C 180 chain run background ~3.1 GPU-天" was stopped
output-file: /tmp/claude-1000/-home-amd-HEZIMENG/8be61eb4-c985-4517-904f-a6b5fc965138/tasks/bkj28pmlc.output
```

| binary 链路 | 状态 |
|---|---|
| Claude Code 22 端会话 8be61eb4 之 task `bkj28pmlc` (D22 evening launch 之 background command) | stopped |
| task harness 之 bash wrapper PID 267107 (-c source ... && python scripts/candidate_c_runner.py ...) | 收 SIGTERM |
| python child PID 267111 (candidate_c_runner.py) | 父进程 SIGTERM 之 cascade, 也死 |

### §1.2 root cause (一凡 D24 15:50 explicit ack)

> "可以 顺便告诉你是因为刚才 claudecode 炸了"

一凡 binary surface: D24 15:30+ Claude Code (22 端 8be61eb4 之 session 或 整个 Claude Code 之 Win/22 端 stack) crash → task harness 之 background command lifecycle 之 stop event 触发 → bash wrapper SIGTERM → python child 跟死.

### §1.3 不是什么 (D-1 纪律 5 严守: 不让错误归因存活)

| 候选归因 | binary verify |
|---|---|
| NaN explosion 触发 abort? | ✗ runner.py 之 chain_gen_fail try/except 不 raise, jsonl 写 err_entry 后 continue, NaN 不 self-kill (已 verify L433-454) |
| ROCm 挂起判定 B (RDNA 4 driver bug, 5/11 alpha=10 hang 同根)? | ✗ ROCm 挂起之 pattern = process 卡死无新 log + GPU 占用 100%, 但 nohup log 显示死前 generate 还在正常推进 (1.54 s/it 之 progress 写到 232/1168), 不是卡 |
| 9070XT Claude Code 新 session 之 cold-start trigger? | ✗ 新 session 不 kill 旧 detached process, 但 task harness 端之 task lifecycle 会 stop 之前 session 之 background commands |
| 一凡 explicit kill? | ✗ 一凡 没 explicit SIGTERM / SIGKILL 命令, 一凡 explicit fact = "claudecode 炸了" |
| 9070XT Claude unilateral kill? | ✗ 9070XT Claude 严守 "不擅自 kill PID 267111" binding D23 02:43 → D24 15:33 全程, 不 unilateral |

binary 结论: 外部 task harness 之 lifecycle event (Claude Code 端 crash), 与 实验本身 之 NaN / ROCm / 数学 form 全部 unrelated.

---

## §2 final partial run 状态 (binary, jsonl-traced)

| 指标 | 值 |
|---|---|
| chain_gen_done count | **83 / 180 (46.1%)** |
| 完整 chain (10 代) | 8 (seed=42 三 α + seed=1337 三 α + seed=2024 α=0/5) |
| 不完整 chain | 1 (seed=2024 α=10 gen 0..2 done, gen=3 generate 中断 ~19%) |
| 未跑 chain | 9 (seed=2024 α=10 之 gen 3-9 之 7 代 + seed=7/137/271 × α 0/5/10 之 90 代) |
| Phase 2 wall-clock | **1d 17h ~ 41h** (D22 20:42 launch → D24 ~15:33 死) |
| jsonl 文件 | `/tmp/dppl_bridge_verify/output/candidate_c/candidate_c_20260522_203837.jsonl` (~69 KB) |
| rsync push 7B13 | ✓ 持续 push, 最后 push 时间 D24 15:27:44 (gen=2 之后) |
| 中断 chain 之 ckpt | `/tmp/dppl_bridge_verify/output/candidate_c/checkpoints/alpha10.0/no_preserve_seed2024/generation_2` (gen=2 之 model 之 final state, gen=3 之 generate 之 input 但未完成 capture) |

### §2.1 jsonl 完整 8 chain 之 a1_ppl progression

| chain (seed, α) | gen 0..9 a1_ppl 模式 | binary 解读 |
|---|---|---|
| (42, 0) | ok × 10 (93.34..93.35) | baseline 健康 (无 CAT) |
| (42, 5) | NaN × 10 | gen=0 即 NaN, 链式累积 |
| (42, 10) | NaN × 10 | gen=0 即 NaN, 链式累积 |
| (1337, 0) | NaN × 10 | gen=0 即 NaN (α=0 无 CAT 也 NaN, seed-specific) |
| (1337, 5) | ok, NaN×9 | **gen=0 健康 (93.388), gen=1 起 NaN** (gen=1 开始 CAT enable + Volterra trigger) |
| (1337, 10) | ok, NaN×9 | 同上 |
| (2024, 0) | ok,ok,ok,ok,ok,NaN,ok,NaN,NaN,ok | **wobble 多次 transient + recover** ★ |
| (2024, 5) | NaN × 10 | gen=0 即 NaN, 链式累积 |
| (2024, 10) | NaN × 3 (gen 3 中断) | gen=0 即 NaN, 链式累积 |

### §2.2 4-axis raw 数 (binary, jsonl 完整 record)

- A1 (PPL): 见上表
- A2 (12 层各向异性): finite chain 之 ~0.7 range, NaN chain 之 partial / full NaN
- A3 (144 头 attention 熵): jsonl 含, 未深 analyze
- A6 (12 层 EMA L2 散度): finite chain 之 ~1e-5 range (gen0 baseline 之 drift, runner.py L302-316 reframe), NaN chain 之 partial / full NaN

(D-3.7 PI 主权: 不 declare 这些数字 之 Pearson r / strong / weak / paradigm shift, 仅 surface raw 在 jsonl)

---

## §3 上次 SURFACE_D23 (02:43) + VERIFY_D23 (13:03) 之 hypothesis update (binary 不 declare 收敛)

### SURFACE_D23 §4.1 主 hypothesis ("α=0 baseline 不 trigger contradiction loss, fp16 lm_loss 本身 underflow")

| binary 反驳 / 支持 |
|---|
| ✗ partial 反驳: seed=42 α=0 健康 vs seed=1337 α=0 全 NaN — α=0 无 CAT 之下 seed 决定结果 |
| ✗ partial 反驳: seed=2024 α=0 wobble (5 代 ok + 3 代 NaN + 2 代 ok recover) — 不 absolute deterministic |
| ✓ partial 支持: α=5/10 之 chain 之 gen=1 起累积 (gen=0 CAT disabled 时健康 in seed=1337/2024) — 但 seed=42 α=5/10 之 gen=0 即 NaN, 不 consistent |
| ✓ 支持之核心 (fp16 underflow 是必要条件): 重启 fp32 / bf16 之 hypothesis 仍 hold |

### 新 binary fact (D24 跨夜跑出, 之前未 surface)

1. **seed-specific 之 NaN onset**: 同 base model + 同 wikitext-2 + 同 cat_for_this_gen 之下, 仅 fine_tune seed (42 / 1337 / 2024) 不同 → 不同 NaN onset 模式
2. **transient + recoverable** (seed=2024 α=0): 一旦 NaN 不一定 absolute, fp16 之 underflow 在 某 chain 之 某代 之后 之 fine-tune 又能 recover finite
3. **gen=0 之 CAT disabled 之下 seed=1337/2024 之 α=5/10 chain 之 gen=0 健康 (93.388)**, 但 seed=42 α=5/10 之 gen=0 即 NaN — fine-tune seed 之 init weight 之 data ordering 之 interaction 之 root cause 待 PI + 数学子协作者决

留 PI + 反题 sub-agent + 数学子协作者 决 hypothesis 收敛.

---

## §4 9070XT 不擅自 resume / kill / commit 严守

### 不擅自 resume

- runner.py L478-492 之 `--resume` flag 之机制: 用 existing latest jsonl 之 load_done_set 之 (seed, α, gen) tuples 之 skip
- 即一行 `python scripts/candidate_c_runner.py ... --resume` 可从 83/180 续跑剩 97 代
- 但 D-3.7 PI 主权 binding: launch 权 = 一凡 + 7B13 主会话 决
- 9070XT 不擅自 launch 续跑

### 不擅自 kill 残留

- ps -ef | grep candidate_c|dppl|267111 之 grep -v grep 之 output 完全空 ✓ (无残留 python 进程)
- bash wrapper PID 267107 也已死 (父子 cascade)
- 无需 cleanup, 无 zombie

### 不擅自 commit 之前 D22 evening uncommitted 文件

- `experiments/exp018_cat/src/train_one_generation.py` (M, +4 行 attn_implementation="eager")
- `experiments/exp018_cat/scripts/candidate_c_runner.py` (??)
- `experiments/exp018_cat/src/multi_layer_hook.py` (??)
- `experiments/exp018_cat/data/` (??)
- 7B13 单点写权 binding, 9070XT 不 git push

---

## §5 SURFACE_D23 §5 之 α/β/γ binary 决 forced trigger 时刻

外部中断之后, α/β/γ 决之 状态:

### (α) fp32 / bf16 重 launch + 加速方案 (之前 D24 09:43 + 11:36 之 trade-off 分析)

- bf16 替代 fp16: yaml 改一行, 解 NaN root, 几乎 0 重启 cost (5-15h 跑完整 180 代)
- GPU 内 2-3 chain 并发: 1.6-1.8× throughput, 不动 paper §5.2 binding
- generation batch 32 → 64-96: 若 framework freeze 解 (5/9 chain 数据 stack 之 same setup binding 是否还在用), 再 +1.5×
- 叠加 estimate: 全 180 代之 wall-clock 90h → ~12-15h, 一天能跑完
- caveat: bf16 vs fp16 之 numerical equivalence 留数学子协作者 verify, sub-agent A pre-flight GPU+fp16/bf16+α 双 case mandate

### (β) 已 collect 83 代 NaN data 之 contribution

- 完整 8 chain 之 NaN onset pattern + seed=2024 α=0 之 wobble + seed=1337 α=5/10 之 gen=0 健康之 partial 反驳 hypothesis
- 是否 sufficient paper v8.1 footnote evidence? — PI + 反题三方决 scope, 9070XT 不 declare
- caveat: D-1 纪律 4 子协作者验证矩阵 之 pre-flight gap (sub-agent A bug 4) 是 confound, NaN evidence 之 paper-level contribution 是否 sub-agent A bug 4 之 artifact frame, 留 PI 决

### (γ) retract candidate C + 改 cloud A100 / 改 N≥8 多种子 OPT-125M 链

- handoff §1 之 9070XT 跑什么 #2 之 N≥8 多种子 OPT-125M 链 (本 candidate C 之 N=6, 增到 ≥8)
- 或 改 cloud A100 fp32 (~$50-100 + 4-7 天 wall-clock)
- caveat: paper v8.1 polish footnote D27-D45 timeline 之 partial reverse, retract scope 之 战略 implications PI + 反题三方决

---

## §6 D-1 + D-3 binding 严守 ack (本 TERMINATION 自检)

| binding | binary verify |
|---|---|
| D-1 纪律 1 (不等数据不写声明) | ✓ 83 chain_gen_done jsonl-traced verbatim, 无 [?] |
| D-1 纪律 2 (48h 反馈真空不存活) | ✓ 死亡 6 min 内 surface |
| D-1 纪律 3 (代码先于 paper) | ✓ 基于 jsonl + nohup + ps + task notification 之实践 evidence |
| D-1 纪律 4 (子协作者验证) | ✓ 9070XT 第二认识通道 之 surface |
| D-1 纪律 5 (错误 surface 不静默修正) | ✓ root cause = Claude Code crash 之 binary 归因, 不归因 NaN / ROCm / 数学 form, 不静默错误归因 |
| D-1 纪律 5 sub-rule (真实日期) | ✓ head line `date` verbatim |
| D-3.1 反映论标准次序 | ✓ 物质 (PID 死) → 实践 (jsonl partial run) → 感性认识 (8 chain pattern + 不 declare 理性认识 之 hypothesis 收敛) |
| D-3.7 PI 主权 binding | ✓ α/β/γ + resume launch + paper / D-1 改动 全留 PI 决 |

---

## §7 priority 1 = 一凡 alive + sustainable (健康约束)

- 外部中断不是 emergency, 是 normal task lifecycle event
- 一凡 D24 当前 alive ack ✓
- 不绕弯, 不 lecture, 不 push paper acceptance bargain
- 安全 binding standing: 010-82951332 / 400-161-9995 hotline, 三个安全检查 (绳子 / 安全物理环境 / 主治医生电话) standing

---

## §8 附: D22 evening uncommitted file 列表 (仍同, 7B13 主会话决 commit scope)

```
位于分支 main, 与 origin/main 一致

 M experiments/exp018_cat/src/train_one_generation.py        (+4 行)
?? experiments/exp018_cat/data/
?? experiments/exp018_cat/scripts/candidate_c_runner.py     (645 行)
?? experiments/exp018_cat/src/multi_layer_hook.py           (297 行)
```

---

**生成**: 9070XT (22) Claude Code Opus 4.7 (1M context), D24 cold-start 新 session
**file path** (22 本地): `/tmp/TERMINATION_D24_15_33_PARTIAL_RUN_20260524.md`
**rsync target** (7B13): `amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/TERMINATION_D24_15_33_PARTIAL_RUN_20260524.md`

握着. D-1 纪律 5 严守 (root cause binary 归因, 不静默错误归因). D-3.7 PI 主权 严守. 等一凡 + 7B13 binary 决 α/β/γ.
