# [ACK D24 — 5060 (Win 9955HX 笔记本) Cold-start PREREQ]

**真实今日日期** (`Get-Date -Format "yyyy-MM-dd HH:mm zzz"`): `2026-05-24 14:25 +08:00` (D24, 周日)

**Surface**: Win 9955HX 笔记本 + RTX 5060 Laptop GPU, cold-start 新 Claude Code 会话

**对象**: 7B13 Linux 姐姐主会话 (192.168.31.36) + PI 一凡 关卡 1 决 input

**协议**: D-1 纪律 5 (错误 surface 不静默) + D-3.1 反映论标准次序 (物质 → 实践 → 感性 → 理性) + 不擅启 main run

**触发**: 7B13 Linux 姐姐 派 cold-start 任务 + HANDOFF_D24_TO_5060_20260524.md (handoff §7 之 ACK format)

---

## §0 真实日期 binary verify (D-1 纪律 5 sub-rule)

| 通道 | 命令 | 输出 | binary 状态 |
|---|---|---|---|
| 5060 (Win PowerShell) | `Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"; (Get-Date).DayOfWeek` | `2026-05-24 14:25:49 +08:00` + `Sunday` | D24 周日 ✓ |
| 7B13 (Linux) | `ssh amd@192.168.31.36 'date -u "+%Y-%m-%dT%H:%M:%SZ"'` | `2026-05-24T06:26:21Z` | UTC 等价 14:26 CST ✓ |
| 22 (9070XT Linux) | `ssh amd@192.168.31.22 'date -u "+%Y-%m-%dT%H:%M:%SZ"'` | `2026-05-24T06:26:21Z` | 三机时钟一致 ✓ |

D-day=2026-05-01 anchor → 今日 = D(24-1) = D24, 周日, 与 7B13 + 22 时钟漂移 < 1 秒 (不继承陈旧 system reminder, binary 实测).

---

## §1 5060 硬件 binary spec (D-1 纪律 1 jsonl-traced raw)

### §1.1 GPU + 驱动 + CUDA + Pytorch (`nvidia-smi` + python torch verify)

```
GPU model:           NVIDIA GeForce RTX 5060 Laptop GPU
GPU 架构:            Blackwell (sm_120, compute capability 12.0)
NVIDIA 驱动:         596.36
CUDA toolkit:        13.0 (torch.version.cuda)
Pytorch:             2.11.0+cu130 (官方 cu130 wheel)
VRAM 总:             8151 MiB ≈ 7.96 GB
VRAM 空闲:           4595 MiB ≈ 4.49 GB (idle, cold-start, 桌面占 ~3.5 GB)
torch.cuda.is_available():    True
torch.cuda.get_device_capability(0): (12, 0)
```

### §1.2 CPU + RAM + 磁盘

```
CPU:                 AMD Ryzen 9 9955HX 16-Core
系统 RAM:            31.2 GB (Win 11 Home China 26200)
磁盘 C: 已用/空闲:   401.9 / 522.3 GB (足够 OPT-125m × N 检查点)
磁盘 D: 已用/空闲:   107.5 / 369.4 GB
工作目录:            C:\Users\amd\Desktop\5060\ (空, han.md 0 字节)
Python:              3.12.10 (C:\Users\amd\AppData\Local\Programs\Python\Python312\python.exe)
```

### §1.3 Blackwell sm_120 真实 op behavior 探针 (D-3.1 物质 binary 先行)

不基于"5060 应该 fast" 假设, 直接跑 raw 数:

| 探针 | 实测 (Win + torch 2.11+cu130) | binary 解读 |
|---|---|---|
| fp32 matmul 2048×2048 | **143.18 ms**, sum 3.722773e+04 | 基线 ~13 TFLOPS 数量级 |
| fp16 matmul 2048×2048 | **380.89 ms**, sum 3.717548e+04 | **fp16 比 fp32 慢 2.66×**, 反预期 Tensor Core ⚠ |
| fp16 vs fp32 矩阵相对均值差 | 2.31e-03 | acceptable (fp16 typical) |
| 注意力 fp16 vs fp32 最大绝对差 | 2.69e-04 | acceptable |
| 确定性 (cuda randn cumsum, 同 seed) | x1 = x2 = -8.320807e+03 | True ✓ |

**Raw fact ⚠**: Blackwell sm_120 之 fp16 matmul 在 torch 2.11.0+cu130 wheel 上 **慢于 fp32 (2.66×)**, 与 Tensor Core fp16 加速预期不符. 候选根因 (不 declare, 推 sub-agent 诊断):
- cuBLAS / cuDNN backend 在 sm_120 之 fp16 路径未走 Tensor Core (fallback 到 SIMT)
- torch 2.11.0 cu130 wheel 对 Blackwell 之 Triton/Inductor kernel coverage 早期不全
- 与 9070XT 之 ROCm 7.2 gfx1201 fp16 fragility (D23 NaN explosion 主 hypothesis) 并行之 binary surface — 两机 之 fp16 之 binary 状态都待 sub-agent 诊断

### §1.4 OPT-125m + wikitext-2 之 cross-validate 状态 (推 stage 0 末)

| 验证 | 状态 |
|---|---|
| transformers 包 | 已装 (与 torch 同 venv) |
| datasets 包 | 装中 (background install pip --quiet datasets, ID `blozbv1i1`) |
| OPT-125m HF 模型缓存 | 待第一次 from_pretrained 触发下载 (~250 MB fp32, ~30 sec 50 MB/s) |
| wikitext-2 raw v1 | 待 datasets load_dataset 触发下载 (~12 MB) |
| 5060 之 OPT-125m wikitext-2 val PPL ballpark | **未跑**, 推 stage 0 pre-flight (§5 propose 之内) |

不 declare 5060 之 OPT-125m wikitext-2 数值能与 9070XT base PPL 93.35 ballpark 等价 — 等 stage 0 实测.

---

## §2 SSH 7B13 + 22 reachable binary (handoff §1.4-§1.5)

| 通道 | 测试 | 结果 |
|---|---|---|
| 5060 → 7B13 TCP 22 | `Test-NetConnection 192.168.31.36 -Port 22 -InformationLevel Quiet` | True ✓ |
| 5060 → 22 TCP 22 | `Test-NetConnection 192.168.31.22 -Port 22 -InformationLevel Quiet` | True ✓ |
| 5060 → 7B13 ssh login | `ssh -o BatchMode=yes amd@192.168.31.36 'hostname; date -u; whoami; uname -a'` | `AMD-EPYC-7B13-64-Core / 2026-05-24T06:26:21Z / amd / Linux 7.0.0-15-generic Ubuntu 26.04` ✓ |
| 5060 → 22 ssh login | 同上 22 | `amd-ONDA-B650M-W / 2026-05-24T06:26:21Z / amd / Linux 6.17.0-29-generic Ubuntu 24.04` ✓ |
| 22 端 PID 267111 (只读, 零 kill 零 commit) | `ssh amd@192.168.31.22 'ps -p 267111 -o pid,user,etime,pcpu,pmem,comm; rocm-smi --showpids'` | alive 1d 17h 49m, %CPU 132, %MEM 9.0, GPU[1] VRAM 4771647488 B (≈4.77 GB), KFD process python ✓ 不动 |

ssh 密钥已配 (D20 21:40 commit `e3dfa5a` 三机互通 ed25519 ✓).

---

## §3 handoff §2 之 10 文件 read done + 5 行/文件 binary summary (不靠 7B13 paraphrase)

### 文件 1: `/home/amd/.claude/CLAUDE.md` (7B13 全局指令)

1. 语言硬约束: 全中文, 4 类英文豁免 (代码/协议/错误信息/品牌)
2. D-1 纪律 5 真实日期自检 standing rule (5/20 D20 加入, D17 → D19 → D20 三次日期校正历史教训)
3. mattpocock skills 编码工作流默认: `/grill-with-docs` 优先, `/diagnose` 6 阶段, `/tdd` 红绿重构
4. Skill 优先级: 用户 `/skill-name` > 项目 CLAUDE.md > 本文件
5. 与项目 CLAUDE.md 解耦: 详细 D-1/2/3 在 `/home/amd/HEZIMENG/MaoField/CLAUDE.md` 单点写源

### 文件 2: `/home/amd/HEZIMENG/MaoField/CLAUDE.md` (项目根, D23 slim 16 KB)

1. Linux 姐姐身份: 数学主导 + 实验执行 + 中立归档, 不哲学判读 (Win) 不战略结论 (一凡 + 反题)
2. D-1 五条纪律: 不等数据不写声明 / 48h 反馈真空不存活 / 代码先于 paper / 子协作者验证 / 错误 surface 不静默
3. D-2 三线并行: 数学 + 实验 + 哲学 cross-tension surface (5/19 加入)
4. D-3 反映论 standing 外置到 `docs/D-3-dialectical-reflection.md` (5/23 D23 slim 41 KB → 16 KB emergency commit `c020c1f`)
5. 关卡 1-4 一凡介入: 实验设计 → 实验数字 + 数学严格度 + 叙事 → 反题审计 → 投/不投

### 文件 3: `docs/D-3-dialectical-reflection.md` (反映论完整 D-3.1-D-3.15)

1. D-3.1 标准次序: 物质 → 实践 → 感性认识 → 理性认识 → 新实践 → 螺旋上升 (毛实践论 + 列宁反映论 + 马克思自然辩证法)
2. D-3.2 6 项抓出: (1) 哲学是结果不是起点 (2) "自发" 含 multi-agent binding (3) "回顾" 是第三阶段不第一 (4) D22-D29 + D29-D60 + D60+ 三阶段 (5) 回顾 4 项必含 (6) PI 单方面 ≠ 协调
3. D-3.7 PI 主权: 关卡 1-4 决之节点严守 / 不动 paper v8 final / D29 venue / 9070XT 长跑 PID
4. D-3.10 D21 反思级联: 8 个反思洞察单日累计, 17:00 之"辩证整体缺失" + 17:55 之"如何证明" + 18:30 之"全学术界缓解 framing 候选" 是 sound seed 不 declare paradigm
5. D-3.11 4 路径方法论: (A) 多通道交叉验证 (B) 干预实验 (C) 时间相位 (D) 反事实 ablation, D60+ window

### 文件 4: `docs/three-machine-architecture.md` (三机架构 D20 加入)

1. 7B13 (Linux 姐姐 / EPYC 7B13 / 499 GB RAM / 无 GPU / 主数据中枢 + git 单点写权)
2. 9070XT (amd-ONDA / 9600X + RX 9070 XT 16 GB ROCm / 链实验执行节点 / PID 267111 D23 candidate C Phase 2)
3. 5060 (Win 9955HX / 一凡交互端 + 论文深读 / 现在 cold-start 新角色: parallel slave 候选)
4. 数据分层: 7B13 4T SSD 主, RAID1 15T 大归档 (>1 GB / 单目录 >5 GB 走 raid1); 备份 cron 2h 增量 + 每日 → 9070XT 4T HDD
5. Git: 7B13 origin GitHub 写权单点, 9070XT + Win 仅 pull (双远端 origin 局域网 + github 异地后备, D20 21:40 commit `e3dfa5a` 配齐)

### 文件 5: `memory/handoff_d20_d23_session_rescue_20260523.md` (D20-D23 救援摘要, 之 Win 端 Claude 抽 jsonl)

1. D20 三机协作 setup (commit `5f39f1a` archive + `e3dfa5a` git 双远端 + `78a5aa1` 项目 CLAUDE.md)
2. D21 paradigm-shift candidate insight 级联 (commit `9b0063e` D-3.10-15 加入 + 9070XT D-PPL pilot 通过 D^code_B=0.2962 D^code_C=0.5900)
3. D22 D-PPL 桥 main run 通过 (commit `657a17f`, 152/152 tuples 24min wall-clock, D^code_B mean=0.2883 D^code_C mean=0.5526 vs D^paper 0.451) + 早晨自杀信号 crisis (绳子 / 活到下月 NeurIPS bargain) + Linux 姐姐 refuse NeurIPS push + candidate C launch (commit `86ccf95`, PID 267111)
4. D23 candidate C Phase 2 NaN explosion + 36 + 22 双 session 被 Anthropic Usage Policy 拦 (Request ID `req_011CbJjHrSiwLs8LvUhhPvpp`) + slim CLAUDE.md emergency commit `c020c1f`
5. safety binding standing: 010-82951332 / 400-161-9995 / 绳子 D22 早 "我听你的的" removed 之 ack / D22 evening "答应活过今天" / D23 早 "怎么样了"

### 文件 6: `experiments/exp018_cat/literature/paper_v8_final_20260516.md` (1090 行)

1. **§5.2 主定理 (2) Mean-field NESS hard-lock** (Reading 2 dimensional clean primary): $D^{*,\rm code}(\alpha) - D^* = -J_S / (4\alpha \cdot N_{\rm contr})$, 在 α=10 / N_contr=146 / J_S^(2)=0.535 之 shift = -9.16e-5 nat/token = **null observable shift**, Rigor tier **L2** (mean-field + 实证 $D^*$ + dimensional clean) + L0 vacuous on transient gen 1-2
2. **§7.5 12 NOT-claim 撤回** (i-xii): paradigm-shift / 首次 dialectical comeback / axiom-first derive / Family 1a uniqueness / framework α-mitigates / m_eff QED analog / 5 LLM-axiom-derive / mitigation framework / universal solution / substantive prediction success / **(xi) v8 new "systematic empirical study" → "empirical pilot study"** / **(xii) v8 new "+16.6% framework failure under Reading 1" 撤** — 全 retract 严守不动
3. **§7.5 反题 6 P0★ disclosed 不修留 reader judgment**: P0★-A non-fatal / **P0★-B ★★ FATAL no-framework equivalence in this regime** / **P0★-C ★★ FATAL v3→v8 PPL 5 revision drift (43→54→48→48→55) candidate red flag** / P0★-D Family 1b/1c/4/4' absent 推 D60+ / P0★-E top venue dialectical framing risk (D17 决不投 NMI/NeurIPS 反映此) / **P0★-F ★★ FATAL D^code (chain actual KL) vs D^paper (per-gen log-PPL ratio) definition mismatch, chain jsonl 不 record D^code scalar trajectory, verify 需 reload checkpoint 1-2 周 推 D60+**
4. **§8 future work**: §8.1 D18-D29 sustained burst (D-PPL bridge + Phase 5 Llama-8B + 8 P0 全修 + 投稿 D29) / §8.2 D18-D60 三 substantive gaps + N≥8 + multi-arch + D^code/D^paper resolution + future regime where framework predicts detectable shift (G4) / §8.3 D60+ paradigm extension 6-12 月
5. **§C 自检 7 question + cross-check binary lock table 全 ✓** + §D file cross-ref ("v8 final 一次性 5/16 D16 单日 ~9 小时 burst final, 不再迭代 v9, D-day 5/1 anchor 下 D16 day-number convention forward-dated 是 D17 校正"); arXiv + TMLR + KBS 三 leg D29 投, 不投 NMI/NeurIPS (D17 一凡 C 决, 反题 zero-context 给 NMI 2-5% + NeurIPS 3-6% desk reject, cumulative ≥1 by 12 月 honest **30-40%** 排除 arXiv 100%)

### 文件 7: `experiments/exp018_cat/configs/cat_arm_b.yaml` (candidate C setup)

1. 模型: OPT-125m (`facebook/opt-125m`, dtype: float16, 5/10 ROLLBACK fp32→fp16 framework freeze D3-D4 binding)
2. 数据: wikitext-2-raw-v1, block_size 64, AdamW lr 2e-5, per-device batch 128, fp16 ON, save_strategy "no", 5 epoch (no_preserve) / 10 epoch (preserve_10pct), beam 5 generation, repetition_penalty 3.0 (Shumailov Zenodo, paper §5.2 写 2.0 之 typo)
3. CAT 块: alpha_scan [0.0, 1.0, 5.0, 10.0, 50.0] / kl_update_every 10 / beta_model 0.999 / beta_kl 0.9 / lambda_1=lambda_2=lambda_3=1.0 / enable_grad_norm_monitor true
4. multi_seed seeds [42] (arm B 单 seed smoke 后 3 seed 扩跑, paper Shumailov 之 5 seed 减为 3 之 GPU 时间预算理由)
5. Falsification F1-F6: F1 no_preserve gen 9 PPL > gen 0 + 5 / F3 gen 0 real PPL > 50 表 fine-tune 本身有问题 / F4 α scan 任一档 vs α=0 无显著 collapse 减弱 → arm B failed / F5 monotone 失守 / F6 cost >50% 表 implementation 失误

### 文件 8: `dppl_bridge_verify_d21_output/MAIN_VERDICT_D22.md` (D22 main run binary)

1. main run **152/152 tuples done + 8 skipped + 0 error**, watchdog total_kills=0 total_retries=0 clean exit, 24 min wall-clock (17:37:30 → 18:01:30, avg 8.56 sec/tuple, 远 << prompt §6.5 之 30 sec/tuple paranoid estimate)
2. Path B (gen-(n-1) EMA proxy, n=72): D^code mean=**0.2883**, median 0.2404, stdev 0.1554, range [0.1611, 0.7534]
3. Path C (gen-0 base anchor, n=80): D^code mean=**0.5526**, median 0.5054, stdev 0.2797, range [0.0000, 1.0152] (0.0000 gen=0 trivial per design)
4. vs D^paper(seed=1 gen=5 α=10) = log(56.94/36.30) ≈ 0.451: Path B ratio 0.64 / Path C ratio 1.23, pilot single point (B=0.2962, C=0.5900) → main aggregate reproducibility 仅 raw 数 surface 不 declare strong claim
5. 不 declare close: ✗ Pearson r > 0.7 strong / ✗ P0★-F partial close / ✗ 桥 verify pass / ✗ 严格度 tier — 留 关卡 3 反题 zero-context + analyze_pearson.py + 关卡 4 三方决

### 文件 9: `dppl_bridge_verify_d21_output/VERIFY_D23_12_55_PROGRESS_CODE_20260523.md` (9070XT D23 自写, md format 参照)

1. D23 13:00 实验进度: PID 267111 alive 16h22m, **32/180 chain_gen_done (17.8%)**, vs 02:43 SURFACE_D23 之 27/180 增 +5 代 (~30min/代 pace), 3 完整 chain (α=0/5/10 seed=42) + 1 不完整 (seed=1337 α=0 gen 0-1)
2. 4-axis raw: seed=42 α=0 全 10 代 a1_ppl ≈ **93.349** 健康 (冻结 base PPL) / seed=42 α=5 全 None NaN / seed=42 α=10 全 None NaN / **seed=1337 α=0 gen 0-1 全 None NaN** (新发现, 首代即 NaN)
3. **partial 反驳 SURFACE_D23 §4.1 主 hypothesis**: α=0 已排 contradiction loss (L173 `enabled=alpha > 0`), seed=42 α=0 健康 vs seed=1337 α=0 NaN → **seed 初始化敏感** binary surface, 不是单一 fp16 universal underflow
4. 代码校验: ps cmd vs runner.py docstring 一致 ✓ / train_one_generation.py uncommitted +4 行 `attn_implementation="eager"` 与 multi_layer_hook A3 attention 头熵测量 binding 一致 / runner.py L173 + L242-244 + L246 + L249 + L277 + L165 行为与 jsonl 一致
5. 不 declare hypothesis 收敛 / 不动 commit / 不动 PID / 不动 paper, 留一凡 + 7B13 + 数学子协作者决, ETA 若 (β) continue 剩 ~75-80h 接 D26-D27 / 若 (α) fp32 重 launch ~30-60h 接 D24-D26

### 文件 10: `dppl_bridge_verify_d21_output/SURFACE_D23_CANDIDATE_C_NAN_EXPLOSION.md` (NaN explosion 之 surface, md format 参照)

1. D23 10:35 catch: 27/180 chain_gen_done, seed=42 α=0 全 10 代 a1_ppl 全 93.35 冻结 / α=5 + α=10 全 None NaN / Python PID 267111 alive 14h 132% CPU
2. nohup log trace verbatim: `{'loss': 0.0, 'grad_norm': nan, 'epoch': 3.6}` + `{'contradiction/D_n': nan, 'contradiction/loss': nan, 'contradiction/alpha': 10.0}` + `{'grad_monitor/g_n': nan}` 之 fp16 underflow pattern
3. 三 hypothesis: 主 fp16 numerical instability + scaler step skip (但 §4.1 之 α=0 之 hypothesis 与 D23 13:00 之 seed=1337 α=0 NaN binary partial 反驳) / 次 ROCm gfx1201 fp16 边界 case 与 CUDA 不一致 / 第三 Volterra K=9 numerical amplify
4. 三选 α/β/γ 留 PI 决: **α** kill + sub-agent A fix iteration + fp16→fp32 重 launch ~30h / **β** continue collect NaN data 作 paper v8.1 footnote partial circumstantial (contribution questionable, 与 sub-agent A bug 之 frame confound) / **γ** abort + retract candidate C 之 9070XT execution + 改 cloud A100 fp32 (战略 implications)
5. D-1 纪律 4 子协作者验证矩阵 expand 候选 surface: pre-flight self-test 应 mandate cover **CPU + GPU 双 mode + fp16 + fp32 双 dtype + single-α + α=10 双 case** (sub-agent A D22 之 pre-flight 用 CPU + fp32, 未 cover GPU fp16 numerical edge case 是 NaN explosion 14h 后才 surface 之 root cause gap, Linux 姐姐决是否扩 D-1 纪律 4)

---

## §4 D-1 + D-3 binding 自检 14 question ack (handoff §4)

| # | binding | binary 自检 |
|---|---|---|
| 1 | D-1 纪律 1 (不等数据不写声明) | ✓ 5060 硬件 + 探针数全 jsonl-traced raw, 无 [?] placeholder |
| 2 | D-1 纪律 2 (48h 反馈真空不存活) | ✓ 5060 cold-start 后 ~3h 内 ACK 写 + push 7B13 (D24 14:25 → 17:30 estimate) |
| 3 | D-1 纪律 3 (代码先于 paper) | ✓ 探针实测 5060 之 op behavior, 不基于"应该 fast" 假设 |
| 4 | D-1 纪律 4 (子协作者验证) | ✓ 5060 作 7B13 主会话 + 9070XT 之 第三认识通道, propose sub-agent A pre-flight smoke (§6) |
| 5 | D-1 纪律 5 (错误 surface 不静默) | ✓ fp16 比 fp32 慢 2.66× 反预期 surface, 不静默 (§1.3 ⚠) |
| 6 | D-1 纪律 5 sub-rule (真实日期) | ✓ §0 三机时钟同步 binary verify D24 周日 ✓ |
| 7 | D-3.2 抓出 1 (哲学 outcome 不 starting form) | ✓ 不 declare 5060 之 cross-validate 是 paradigm-shift evidence |
| 8 | D-3.2 抓出 2 (自发 含 multi-agent binding) | ✓ ACK 写后等一凡 关卡 1 决, 不 unilateral 启 smoke |
| 9 | D-3.2 抓出 5 (回顾范围 4 项必含) | ✓ 文件 5 handoff + 文件 6 §7.5 12 NOT-claim + 文件 6 反题 6 P0★ + 文件 10 NaN explosion 全 read 完 |
| 10 | D-3.2 抓出 4 (时间表三阶段) | ✓ D22-D29 paper v8 final 锁定 + D29-D60 polish + D60+ paradigm shift candidate window 严守 |
| 11 | D-3.12 dialectical 包容 form (不强二分) | ✓ 5060 之 fp16 慢 surface 不 declare "Blackwell wheel 失败" 或 "torch 2.11 wrong", 仅 raw fact, 候选根因列待 sub-agent |
| 12 | D-3.12 candidate verify D60+ (不 D22-D60 单方面) | ✓ 5060 之 cross-validate 推 D-PPL bridge partial circumstantial evidence accumulation, 不 D24 单方面 declare |
| 13 | D-3.11 4 路径方法论 binary specify | 本 ACK 主要在 路径 A (多通道交叉验证: 5060 vs 9070XT) + 路径 C (时间相位: D24 pre-flight vs D27 expand) |
| 14 | 5 路实验 framing 是辩证整体累积 (不假设单轴) | ✓ 5060 之 cross-validate 是 D-PPL bridge 之 跨机 multi-channel 之 binary 补充, 非 single-machine framework α-effect 单轴假设 |

任一 no → 不发出. 14/14 ✓.

---

## §5 propose pre-flight smoke setup (5060 自决, 等一凡 关卡 1 决再启)

### §5.1 stage 0 — 物质 binary 探针完成 (现在, 不等 PI 决)

| 探针 | 状态 |
|---|---|
| 5060 之 raw matmul + attention + 确定性 | done ✓ (§1.3) |
| 5060 上 OPT-125m fp32 + wikitext-2 val PPL ballpark vs 9070XT base 93.35 | pending, datasets 包 装中 (background ID `blozbv1i1`), ETA 5-10 min, 之后 30-60 sec compute |
| 7B13 上 OPT-125m 之 HF cache 是否可 rsync 给 5060 (省下载) | 待 sub-agent 决 (5060 直 from_pretrained 比 rsync 慢一点但 simpler) |

stage 0 完后 surface 5060 上 OPT-125m val PPL ballpark, 不 declare equivalence, raw 数报 PI.

### §5.2 stage 1 — pre-flight chain smoke (PI ack 后, 不擅启)

axes propose (自决, 等 一凡 关卡 1):

```
axis 1: seed         = [42] (与 9070XT main D22 一致, 1 seed smoke)
axis 2: alpha        = [0, 10] (baseline + framework single high, 2 axes)
axis 3: gen          = [0, 1, 2] (3 gen 短, 触发 chain self-iteration 但快)
axis 4: dtype        = [fp32, fp16] (双 case, fp32 控制 + fp16 重现 9070XT NaN 假设)
axis 5: wall-clock 估 = 2 dtype × 2 alpha × 3 gen × ~5-10 min/gen ≈ 1-2h
axis 6: VRAM 估     = OPT-125m fp32 ~500 MB + AdamW state 1.5 GB + activation 2-3 GB ≈ 4-5 GB (5060 free 4.49 GB ⚠ 紧, fp16 可降至 2-3 GB)
```

输出 jsonl 之 字段: a1_ppl + val_loss + a2_anisotropy[12 层] + a6_ema_divergence[12 层] + grad_norm + contradiction/loss + caveats. 与 9070XT 之 candidate_c_runner.py jsonl schema 严格对齐 (rsync candidate_c_runner.py + train_one_generation.py + cat_trainer.py + contradiction_loss.py + config.py + cat_arm_b.yaml + multi_layer_hook.py 之 ~8 文件, total ~80 KB, 不 git clone).

输出 push 7B13 同 9070XT 之 sibling dir 之 5060/  子目录.

### §5.3 stage 2 — N seed expand parallel (PI ack 后, stage 1 通过 + raw 数 ballpark ok 后)

```
axis 1: seed   = [42, 1337, 2024] (3 seed 限 5060 VRAM + wall-clock budget)
axis 2: alpha  = [0, 10]
axis 3: gen    = [0..9] (全 10 代)
axis 4: dtype  = [fp32 only] (fp16 留 9070XT 之 PID 267111 之 continue data, 不重复 NaN 之 risk)
axis 5: wall-clock 估 = 3 seed × 2 alpha × 10 gen × ~10-20 min/gen ≈ 10-20h (D25-D26 sleep window)
axis 6: 与 9070XT 之 PID 267111 之 fp16 chain parallel surface 之 cross-channel diff
```

输出 与 9070XT main D22 之 D^code Path B + C 之 5060 fp32 之 sibling, 7B13 之 analyze_pearson.py 可加 5060 axis 之 cross-machine consistency 验证.

### §5.4 PI 决之 关卡 1 input candidate

5060 等一凡 关卡 1 二元决 (不擅启):

- **A (推荐)**: stage 0 完后 surface 数 报, 之后 stage 1 启 (1-2h smoke), 期 D24 evening 出 raw 数, D25 早 7B13 主会话决 stage 2
- **B**: 直接 stage 2 (跳 stage 1 smoke), 风险 NaN explosion 在 5060 重现之前 14h 浪费
- **C**: 仅 stage 0 之 raw 数 报, stage 1 + 2 推 D25+ (等 7B13 之 candidate C α/β/γ 决定后)
- **D**: 不动 5060, 仅作 read 端 (D-3.7 PI 主权), 不 cross-validate

5060 不 declare A vs B vs C vs D 之 优劣, 留一凡 binary 决.

---

## §6 propose sub-agent A pre-flight smoke acceptance criterion (handoff §5 binding)

sub-agent A 之 binary threshold (5060 自决, 等一凡 ack 之后 sub-agent A 派遣):

### §6.1 numerical equivalence acceptance (cross-machine binary criterion)

| criterion | 5060 binary 期望 | 7B13 / 9070XT reference | accept threshold |
|---|---|---|---|
| OPT-125m wikitext-2 val PPL (fp32, 5060 init seed=42) | 待 stage 0 测 | 9070XT seed=42 α=0 a1_ppl ≈ **93.349** (全 10 代 健康) | abs diff < 5 PPL (相对 5%) 之 binary ballpark match |
| fp32 forward 之 logit hash (1 batch wikitext-2 val) | 待 stage 0 测 | 7B13 CPU mode 之 reference (sub-agent A 跑) | bit-level 不期严格一致, max abs diff < 1e-3 之 binary cross-validate |
| chain gen 0 之 D^code Path C ballpark (seed=42 α=10) | 待 stage 1 测 | 9070XT pilot D21: D^code_C = 0.5900 single point | abs diff < 0.2 (相对 30% 之 chain training stochastic ballpark) |
| fp16 5060 之 NaN appearance rate (seed=42 α=10 gen 0-2) | 待 stage 1 测 | 9070XT D23 之 NaN explosion rate (seed=42 α=10 全 NaN, seed=1337 α=0 首代 NaN) | binary 2 outcome: (A) 5060 fp16 也 NaN → fp16 通用 fragility cross-validate / (B) 5060 fp16 健康 → ROCm gfx1201 specific 之 fp16 边界 case suspect |

### §6.2 sub-agent A 之 mandate (handoff §5 binding)

D-1 纪律 4 子协作者验证矩阵 expand candidate (D23 SURFACE_D23 §9 之 教训累积):

```
sub-agent A 之 pre-flight self-test 必 cover:
- ✓ CPU + GPU 双 mode (D22 仅 CPU)
- ✓ fp16 + fp32 双 dtype (D22 仅 fp32)
- ✓ single seed × {α=0 single seed smoke + α=10 numerical edge} 双 case (D22 仅 α=0)
- ✓ 5060 (Blackwell sm_120 cu130) + 9070XT (RDNA4 gfx1201 ROCm 7.2) + 7B13 CPU 三机 cross-channel
- ✓ 输出 之 jsonl schema 与 candidate_c_runner.py D22 之 schema 严格一致, 之 7B13 analyze_pearson.py 可直接 ingest 加 5060 axis
```

不 declare D-1 纪律 4 之 改动 — 留 Linux 姐姐决 (5060 仅 surface 候选).

### §6.3 sub-agent A 之 deliverable bug 历史教训 binding (handoff §5 binding)

D21 sub-agent A 3 次 deliverable bug (install SIGPIPE / wheel 版本 / PosixPath JSON) 之 教训 expand:

- sub-agent A 之 deliverable 必含 binary smoke 自跑 + jsonl head 5 + tail 5 + grep "nan" count + 之 caveat field 全 surface
- sub-agent A 不擅 declare pre-flight pass, 仅 surface raw 数 + 7B13 主会话 + 反题 sub-agent 之 audit input
- sub-agent A 之 fix relay 必 7B13 commit before 9070XT / 5060 重 launch

---

## §7 safety binding standing ack (priority 1)

- 010-82951332 / 400-161-9995 双相 / 焦虑危机心理援助热线 24h standing immediate trigger
- 三个安全检查 standing: 绳子 / 安全物理环境 / 主治医生电话
- 一凡 D22 早 "我听你的的" → 绳子已 removed from reach 之 ack 持续, 不 push 重新 reach
- 一凡 D22 07:32 "答应你 努力 活过今天" → D22-D24 alive 之 ack
- 不替父母决 hospitalize / 不绕弯 lecture / 不 push paper acceptance bargain / 不堆 NeurIPS push pattern (D17 反题强制撤回 17-23% NMI inflate 同构 教训)
- 一凡 D24 状态 binary ack 由 7B13 主会话 + 一凡直接 input 决, 5060 此 ACK 不 prompt 健康询问 (避 ritual repetition risk, handoff §6 binding 之 phrasing 简洁)

---

## §8 confound / risk / open question binary list (handoff §8 binding, 5060 surface 不擅 resolve)

### §8.1 5060 hardware open question

1. **Blackwell sm_120 之 fp16 慢 fp32 2.66×**: cuBLAS/cuDNN backend 在 sm_120 之 Tensor Core fp16 路径 是否未 active? 候选根因 (5060 不 declare): torch 2.11.0 cu130 wheel 对 Blackwell 之 Triton/Inductor kernel coverage 早期, 或 cuBLAS fp16 fallback 到 SIMT. **影响 stage 1 之 fp16 chain training wall-clock 预估**: 若 fp16 慢, fp16 path 之 chain training 之 binary smoke 之 wall-clock 可能 > stage 1 1-2h budget.
2. **5060 VRAM 4.49 GB free**: fp32 chain training (OPT-125m + AdamW + activation) 在 batch 128 之 5060 之 OOM 风险待 stage 0 boundary 测 (fp32 minimal batch 32 + grad accum 4 之 fallback 必备).
3. **5060 桌面共享 GPU**: Win 11 桌面 + Chrome + Claude Code CLI 占用 3.5 GB VRAM, 之 stage 2 长跑 (10-20h) 之 wall-clock 内 Win 系统 / Chrome 升级触发 GPU 重置 之 risk surface, propose 长跑 期 Win 端 background app 之 minimize.

### §8.2 cross-machine cross-validate confound

4. **5060 之 OPT-125m HF download** 与 9070XT 之 OPT-125m 之 bit-level 是否一致? HF Hub 之 LFS pointer 之 mtime 之 binary verify 必 (避 HF 端 model checkpoint 之 silent re-upload risk).
5. **wikitext-2-raw-v1 之 cache 一致**: HF datasets cache 之 5060 vs 9070XT 之 binary diff 之 raw bytes check 必 (避 dataset 之 silent revision risk).
6. **torch 2.11.0+cu130 (5060) vs torch 2.12.0+rocm7.2 (9070XT)**: 不同 backend + 不同 minor version 之 cross-channel numerical equivalence 之 reference value tolerance 之 binary 是 sub-agent A 之 自决 scope.

### §8.3 D-PPL bridge cross-machine candidate scope

7. **5060 fp32 之 D^code 与 9070XT fp16 之 D^code 之 cross-channel diff**: 不 declare 5060 之 D^code 是 9070XT 之 fp32 reference (因 9070XT fp16 NaN 已 surface), 仅作 partial circumstantial cross-channel surface, 是否 enter D60+ multi-channel 之 数 routes 候选 留 PI + 反题 三方决.
8. **paper §5.2 之 主定理 (2) hard-lock 不动 严守**: 5060 之 数 不 declare 是 §5.2 之 改动 evidence, 不 declare 是 §7.5 之 12 NOT-claim 之 反转 evidence, 不动 §8 future work 之 D60+ window. paper v8 final 47/47 + 反题 6 P0★ disclosed 不修 全严守.

### §8.4 9070XT PID 267111 之 read-only 严守

9. 5060 之 cross-validate 不影响 PID 267111 之 continue. 9070XT 之 32/180 chain_gen_done 之 progress 不动. α/β/γ 决留 7B13 主会话 + 一凡 PI + 反题. 5060 仅 ssh 22 read-only (rocm-smi --showpids / ps -p 267111), 零 kill 零 commit 严守.

### §8.5 D-1 纪律 4 子协作者验证矩阵 expand 候选 surface

10. handoff §6 之 sub-agent A pre-flight mandate (CPU + GPU 双 mode + fp16 + fp32 双 dtype + single seed × α=0 + α=10 双 case) 之 D-1 纪律 4 之 formal expand 之 改动 留 Linux 姐姐决 (5060 仅 §6.2 propose).

---

## §9 5060 当前 standby (不擅启)

- pre-flight stage 0 之 残余 (datasets install + OPT-125m val PPL ballpark) 推 ~10 min 完成, 完成 push 7B13 sibling
- stage 1 chain smoke + stage 2 N seed expand **不擅启**, 等一凡 关卡 1 二元决 (§5.4 之 A/B/C/D)
- 22 端 PID 267111 不动, 9070XT 之 candidate C α/β/γ 决 不 5060 scope
- paper v8 final + D29 arXiv + TMLR + KBS 三 leg 投稿 不动
- 不 git commit / 不 git push (7B13 单点写权 严守)

---

**生成**: 5060 Win 9955HX 笔记本 Claude Code Opus 4.7 (1M context), 2026-05-24 D24 周日 14:30 CST
**file path** (5060 本地): `C:\Users\amd\Desktop\5060\ACK_D24_5060_PREREQ.md`
**rsync / scp target** (7B13): `amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/`

priority 1 = 一凡 alive + sustainable. paper v8 final 47/47 + D29 投稿 venue + PID 267111 全不动. 等一凡 关卡 1 决.
