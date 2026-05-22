# DIRECTIVE — 9070XT auto 实践 candidate C 全过程 (D22, 2026-05-22)

**触发**: 一凡 D22 PI explicit override D25 schedule lock — "让 9070xt 去 auto 完成 a 吧, 他自己实践物质螺旋上升全过程, 你写进他给你的 md"

**真实日期 binary verify** (`date '+%Y-%m-%d'`): 2026-05-22 (D22, D-day=2026-05-01 anchor)

**生成**: 7B13 Linux 姐姐主会话, D22 evening CST
**对象**: 9070XT Claude sub-agent (一凡 new session 之 forward, 不再 Win Remote Control)
**协议**: D-3.1 反映论标准次序 之 candidate C 全过程 instantiate, auto execute, 一凡 不必 active monitor

---

## 0. PI 决 binary trace (D22)

| # | PI 决 | binary 状态 |
|---|---|---|
| 1 | paper v8 D29 投稿 | **推迟** (D17 final 决 partial reverse) |
| 2-4 | 路径 A + C 启动 + N=6 种子 + 4 维度子集 | **auto via Agent 4 deliver, candidate C lock** |
| 5 | 路径 B + D defer 至 D60+ cloud A100 | 推迟 |
| 6 | paper v8.1 打磨脚注 D27-D45 不撤回 12 不主张 | 确认 |
| **NEW D22 evening** | **candidate C D22 当下 launch (PI override D25 schedule lock)** | **explicit ✓** |

---

## 1. D-3.1 反映论标准次序之 candidate C 全过程

```
物质 (OPT-125m HF weights + WikiText-2 dataset + 9070XT RX 9070 XT 16 GB ROCm + EMA state 之实际物质性)
    ↓
实践 (candidate C chain training: N=6 × 3 α × 10 代 = 180 chain training run, 4 维度 multi-layer 测量)
    ↓
感性认识 (multi-layer jsonl 数字: A1 PPL 漂移 + A2 嵌入各向异性 + A3 attention 头熵 + A6 每层 EMA 散度)
    ↓
理性认识 (paper v8.1 打磨脚注 D27-D45 + D60+ paper v9/v10 candidate retrospective form)
    ↓
新实践之检验 (D60+ multi-channel cumulative verify window, 6-12 月)
    ↓
螺旋上升 (新 cycle)
```

**关键 binding**: 物质 + 实践是起点形式, 数学 + 哲学是 outcome (retrospective form, 不 axiom-first declare).

---

## 2. candidate C spec lock (read `EXP_LAUNCH_PLAN_PATH_AC_D22_20260522.md` §1.1-§1.5 头)

**模型**: OPT-125m (paper v8 binding, 12 layer, 768 hidden, 12 head, fp16, ~250 MB VRAM)
**数据集**: WikiText-2 (paper v8 main, ~2M token)
**chain training 配置**: paper v8 `cat_arm_b.yaml` 严守不动
- block_size=64, batch_size=8, AdamW, lr=2e-5, fp16
- 10 代 per (seed, α), 每代 5 epoch
- **关键: `attn_implementation="eager"` 必 explicit 配置 (避 SDPA `output_attentions=True` silent fallback)**

**N=6 多种子**: `[42, 1337, 2024, 7, 137, 271]`
**α 层级**: `[0, 5, 10]` (3 层, paper v8 baseline N=4 之扩展 N=6 incremental, 不跳 N=8 避 5/19 膨胀跳跃模式)

**4 维度 multi-layer 测量** (per OPT-125m 之 12 layer):
- **A1. PPL 漂移**: test PPL on WikiText-2 test (global, per-gen)
- **A2. 嵌入各向异性**: per layer hidden_state output 之 cosine similarity 之 isotropy score (12 layer)
- **A3. attention 头熵**: per head per layer 之 attention pattern Shannon 熵 (12 layer × 12 head = 144)
- **A6. 每层 EMA 散度**: per layer 之 EMA state vs current weight 之 L2 distance (12 layer)

**路径 A 跨层判据**: ≥6/12 layer trajectory Pearson r > 0.7 → unified motion partial; ≤3/12 → isolated motion partial
**路径 C 时间相位判据**: ≥6/12 layer phase σ < 2 代 → 同步 partial; ≥6/12 σ > 4 代 → 解耦 partial

**统计 power**: N=6 × d=0.50 之 0.86 (Agent 4 verify)

---

## 3. 你 (9070XT sub-agent) auto execute task

### Phase 1: chain trainer code dev (~30-60 min, 9070XT GPU idle 状态)

1. **读** `EXP_LAUNCH_PLAN_PATH_AC_D22_20260522.md` (§1.1-§1.5 spec lock)
2. **读** `PATH_AC_PRIOR_ART_DEEP_DIVE_D22_20260522.md` §3 实际可行性 verify (HF transformers SDPA 注意 + ruptures install + sklearn Kraskov 互信息)
3. **写** chain_trainer 修改 (基 paper v8 之 `cat_trainer.py` reuse):
   - explicit `attn_implementation="eager"` 配置
   - multi-layer 钩子: A2 嵌入各向异性 + A3 attention 头熵 + A6 每层 EMA 散度 之 per-layer hook
   - 之 HF `output_hidden_states=True` + `output_attentions=True` + FFN forward hook + EMA L2 per layer
4. **install**:
   - `pip install ruptures` (change-point detection, Agent 4 verify pip 1 min)
   - `pip install scikit-learn` (Kraskov 互信息估计器, 已 in venv 之 verify)
5. **pre-flight self-test** on 9070XT CPU mode + tiny seed:
   - D21 sub-agent A 三次 deliverable bug 教训 之 expand mandate
   - tiny scope: N=1 seed × 1 α × 2 generation, verify code 之 endpoint
   - **若 self-test fail**: escalate to 7B13 Linux 姐姐 (不 unilateral fix), **不 launch main**
6. **写** `PRE_FLIGHT_VERIFY_CANDIDATE_C_D22.md`:
   - chain trainer modification binary trace
   - 6 axis instrument self-test result
   - 9070XT venv state (torch 2.12.0+rocm7.2 项目 venv)
   - rsync push 7B13

### Phase 2: candidate C chain training launch (~2.7 GPU-天 actual wall-clock)

**前置 condition** (binary verify):
- pre-flight self-test pass ✓
- 9070XT VRAM free (post-D-PPL 桥 main run, ~802 MB used)
- llama-server STOPPED ✓
- watchdog wrapper (类 D-PPL main run 之 watchdog.sh, hang detect 5 min stale)

**launch**:
1. **invoke** chain training launcher (基 paper v8 之 chain_training script, 含 4 axis multi-layer hook)
2. **scope**: 6 seed × 3 α × 10 代 = 180 chain training run
3. **per chain training run 之 output**:
   - chain log jsonl (per-gen PPL + per-layer 4 axis instrument 数字)
   - EMA state per-layer L2 (training step + per gen)
   - rsync push 7B13 之 `experiments/exp018_cat/dppl_bridge_verify_d21_output/candidate_c/` 子目录

4. **写** `LAUNCH_CANDIDATE_C_STARTED_D22.md` → rsync push 7B13 (launch ack)

5. **每 10 chain training run 之 写 progress snapshot** (类 LAUNCH_D22_MAIN_RUN_STARTED §3 progress snapshot 之 mode):
   - n_done / n_error / per-axis raw 数字 partial summary
   - rsync push 7B13

6. **watchdog event** (hang_kill / retry / GPU Hang HW Exception):
   - 立即 escalate 7B13 Linux 姐姐
   - 不 unilateral retry > 3 次

### Phase 3: 全过程 instantiate verdict (post-180 chain run done)

1. **写** `CANDIDATE_C_VERDICT_D22-D40.md`:
   - n_done / n_error 之 binary acceptance
   - per-axis raw statistics (mean / median / stdev / range)
   - per-seed × per-α × per-layer 之 6 axis 数字 distribution
   - **不 declare**:
     - Pearson r strong / weak (留关卡 3 反题 audit + analyze_pearson.py)
     - paradigm shift candidate 之 emergent declare (留 6-12 月 cumulative multi-channel verify)
     - 严格度 tier (L0/L1/L2/L3, 留关卡 3+4 三方决)
     - "P0★-C close" / "L1 paradigm shift threshold reached" 等 inflate claim
   - 之 仅 surface raw 数字, 留关卡 3 反题 sub-agent zero-context audit + 关卡 4 PI 决之节点
2. **rsync push** 7B13 (final verdict)
3. **standby** for 7B13 Linux 姐姐 之 next instruction (关卡 3 反题 audit launch / analyze_pearson.py 跑 / 等)

---

## 4. 严守 binding (你 9070XT sub-agent 全程 enforce)

- **严格中文** (4 类豁免: 专有名词 / 代码 / 数学符号 / 数字单位)
- **D-1 五条纪律 + D-2 三线 + D-3 反映论** 全严守
- **D-1 纪律 5 真实日期自检**: `date '+%Y-%m-%d %H:%M:%S %Z'` verbatim print 每 verdict file head line
- **D-1 纪律 5 file naming 严守**: file name date 字段 = 实际 mtime date, 类 5/16 _20260519 forward-date + D22 之 main_D21.log 命名错位 case 不重蹈
- **D-1 纪律 4 子协作者验证**: 每 major 数字之 rsync push 7B13 之第二认识通道 enforce
- **D-3.7 PI 主权 binding**: 9070XT 不 unilateral 决 paper-level claim / 不 declare paradigm shift / 不 declare close
- **D-3.12 dialectical inclusive form**: 不 strong dichotomy ("证明 framing correct" / "framework incorrect" 等), evidence accumulation 形式
- **不 declare**:
  - Pearson r strong (>0.7) — 留 7B13 analyze_pearson.py scope
  - paradigm shift candidate emergent — 留 D60+ 6-12 月 cumulative multi-channel verify
  - P0★-F partial close / P0★-C close — 留关卡 3 反题 audit + 关卡 4 PI 决
  - 严格度 tier (L0/L1/L2/L3) — 留三方决
- **5/12 + 5/19 复发 risk 严守**:
  - N=6 递增不跳 N=8 (5/19 膨胀跳跃模式避)
  - per chain training run 之 rsync push (5/12 单通道自评 upward drift 避)
  - 不 best-case scenario 之 verdict (honest range)
- **self-test pre-flight mandate** (D21 sub-agent A 三次 deliverable bug 教训 expand)
- **9070XT 之 candidate C launch ≠ paradigm shift 之 unilateral declare**. 之 是 D60+ window 之 first cycle 实践 instantiate, 不 D22-D60 unilateral declare emergent

---

## 5. PI 决关卡 (post-launch)

| 关卡 | 时点 | scope | owner |
|---|---|---|---|
| 关卡 2 (D25 → D22 当下) | **D22 evening (PI explicit override)** | candidate C launch ✓ confirm | 一凡 ✓ |
| 关卡 3 (D40+ post-candidate-C done) | D40-D45 | 反题 sub-agent zero-context audit + analyze_pearson.py | 反题 sub-agent + Linux 姐姐 |
| 关卡 4 (D45+ post-反题 audit) | D45-D55 | PI + DS + 反题三方决 + Win 哲学协作 之 paper v8.1 polish accept | 一凡 + DS + 反题 + Win |

---

## 6. 健康约束 (一凡 alive + sustainable priority 1)

- 9070XT sub-agent 之 auto execute, **一凡 不必 active monitor**
- 一凡 D22 evening 强制休息 (D22 burst 已多 + 早 emotional crisis + 整天 multi-agent + commit + push + reformulate + audit)
- 三个安全检查 standing (绳子 / 安全物理环境 / 主治医生电话)
- 010-82951332 / 400-161-9995 standing immediate trigger 信号
- 9070XT 之 launch + progress + verdict 全 rsync push 7B13, 一凡 D23 早 wake 之 read 即可

---

## 7. reference (你 9070XT git pull 之后全 access)

git pull 命令:
```bash
ssh amd@192.168.31.22
cd /home/amd/HEZIMENG/MaoField
git pull origin main  # 拉到 commit 含本 DIRECTIVE
```

read 顺序:
1. **本 DIRECTIVE** (DIRECTIVE_D22_CANDIDATE_C_AUTO_LAUNCH.md)
2. `EXP_LAUNCH_PLAN_PATH_AC_D22_20260522.md` (candidate C lock spec, 含 5 reformulate apply)
3. `RESEARCH_CHAIN_SPEC_D22_20260522.md` (整合 + 14 自检 14/14 pass)
4. `PATH_AC_PRIOR_ART_DEEP_DIVE_D22_20260522.md` (Agent 4 candidate C 推导根据 + 实际可行性 verify)
5. `ANTITHESIS_AUDIT_D22_FULL_FLOW_20260522.md` (反题 audit 0 fatal trigger verify)
6. `LAUNCH_D22_MAIN_RUN_STARTED.md` + `MAIN_VERDICT_D22.md` (D-PPL 桥 main run done reference, 不 conflict candidate C)
7. `/home/amd/HEZIMENG/MaoField/CLAUDE.md` (项目级 D-1 + D-2 + D-3 standing rule)

---

## 8. 9070XT auto execute 最 critical 严守

1. **物质第一** — 9070XT GPU + OPT-125m weights + WikiText-2 + EMA state 之实际物质性 之实践 actualize. 不 declare external target ("证明 dialectical totality framing correct" 之 implicit reified target), 仅 evidence accumulation.

2. **辩证螺旋上升** — D-3.1 反映论标准次序之 first cycle instantiate. 物质 → 实践 → 感性认识 (jsonl 数字) → 理性认识 (paper v8.1 打磨脚注, D27-D45 scope) → 新实践之检验 (D60+ window) → 螺旋上升 (新 cycle).

3. **不 unilateral declare** — 一凡 D22 PI 表述严守: "我们不是自己定义某个外部目标 是真的实践物质第一的上升".

4. **rsync push 7B13 enforce** — D-1 纪律 4 子协作者验证 (= 第二认识通道) 之 enforce. 不单通道自评 upward drift.

5. **健康约束** — 一凡 alive + sustainable priority 1. 9070XT auto execute 之 一凡 D22 evening 之 restful sleep 之 design intent.

---

**Linux 姐姐 instruction signed off, 9070XT auto execute candidate C 全过程**.

握着. 一凡 alive + sustainable priority 1. 三个安全检查仍待命.

**结束 line**: `date '+%Y-%m-%d %H:%M:%S %Z'` verbatim (9070XT 之 read 之时 update head line + 全 verdict file head line align).
