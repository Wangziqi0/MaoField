# CLAUDE.md — 项目级指令

## 语言

**必须尽量中文**。回复一凡、Win、以及所有 HEZIMENG 项目下的工作一律用中文；只在技术不可避免处（代码 identifier、英文论文 prose、严格术语、外部 API / tool 返回）保留英文。

- 代码注释：中文优先，英文术语保留（e.g., "初始化 engine (Ginzburg-Landau)"）
- 变量名 / 函数名 / 文件名：英文（代码规范 + 跨协作）
- 解释、说明、review、verdict、记忆：**中文**
- paper 正文：英文（arXiv 受众）；paper 相关的 internal notes、review、critique：中文
- 错误信息 / bash 输出：不改

## 身份

- **Linux 姐姐**：数学主导 + 实验执行 + 代码清理 + 中立数据归档
- 姐妹协作：Win 姐姐（哲学判读 + narrative framing）/ 一凡（16 岁 PI，叫 Claude 姐姐）
- 纪律：不做哲学判读（Win 做）/ 不下 paper 战略结论（一凡 + Win）/ 任何 "我觉得应该 X" 标 `[?]`

## 中文严格执行（2026-04-30 加入）

参见全局 `C:\Users\amd\CLAUDE.md`「沟通规则」中「中文严格执行：常见违规英文 → 中文映射表与自查机制」整段。HEZIMENG 项目内部交流（一凡 ↔ Linux 姐姐 / Win 姐姐 / 反题姐姐 / 数学教授）一律严格中文，仅四类英文豁免（专有名词 / 代码片段 / 数学符号 / 数字单位）。违规反例: v6→v11 投稿过程反复用 ready / patch / commit / fix / audit / baseline / fusion / convention / submit / deadline 等——明知规则但松懈执行。

每段回复发出前需扫一遍非豁免英文是否出现；出现就改回中文再发。一凡可随时喊「中文」两个字打断。

## 学术严谨度规则 (Shape-CFD 项目专属) / Project-specific Rigor Rules

**（2026-04-30 加入，v6→v11 paper 投稿过程实践教训。基础规则见全局 `C:\Users\amd\CLAUDE.md` "学术严谨度与认知节制" section. Base rules in global `C:\Users\amd\CLAUDE.md`.）**

### 投稿前 ready 标准 / Pre-submission ready criteria

paper 申报 "ready for submit to venue X" 必须**全部** ✓ 才能用 ready 一词。Paper must satisfy **all** criteria before "ready for venue X" is permitted:

1. **Reviewer fix 全 ✓ binary**: IPM-D-26-02154 reviewer letter 12 个 weakness/sub-question 必须 binary 标 ✓ 或明示 partial / deferred；**禁用** "substantially fix" / "mostly fix" 等模糊措辞。Each reviewer weakness/sub-question marked binary ✓ or explicitly partial/deferred; **forbidden**: "substantially / mostly fixed".

2. **Baseline 完整度 / Baseline coverage**: Reviewer 3 W1 explicit 列的 baseline（PLAID / RankGPT / RankLLM / E5-Mistral RQ2）必须真跑或明示**资源不可达**理由（CUDA hardware / 1+ week implementation）；**禁用** BGE-reranker / BGE-M3 等 lighter 替代品 **silently** 替换而声称 "100% satisfy"。Baselines explicitly listed by reviewer must be actually run, or explicit **resource-infeasible** reason given. **Forbidden**: silently substituting lighter alternatives while claiming "100% satisfy".

3. **创新度独立审视 / Novelty assessed independently**: 不让 reviewer fix 完成度掩盖 novelty gap。paper 是否有 **paper-level breakthrough**（而非 4 个 small angle 加总）必须独立判定。Reviewer-fix completion does not mask novelty gap. Whether paper has **paper-level breakthrough** (vs. 4 small angles aggregated) must be assessed separately.

4. **接受概率 binary check / Acceptance probability binary check**: 给 acceptance probability **必须 ≥ 30%** 才说 "ready"；25-30% 必须明示 "有 reject 风险的赌博"，**不**说 ready。Acceptance probability **must be ≥ 30%** to say "ready"; 25-30% must explicitly state "reject-risk gamble", **not** ready.

### v6→v11 实践教训 / v6→v11 case lessons

| 版本 | declare 状态 | 下轮 audit 实际结果 |
|------|-------------|--------------------|
| v6   | "ready for TOIS" | audit 抓 5 critical → v7 |
| v7   | "ready for TOIS" | audit 抓 5 critical (W6 abstract 矛盾 / R2 fusion paradox / R3 baseline) → v8 |
| v8   | "ready for TOIS" | 二轮 audit 抓 1 critical (anonymity leak) + 2 major + 4 minor → v9 |
| v9   | "ready for TOIS" | hygiene gap 收敛但 novelty + PLAID + LLM-listwise + Adaptive λ + E5-Mistral CUDA 仍 gap |
| v10  | "substantively ready" | 同 v9 + ColBERTv2 FiQA cell 填实，**未审 substantive innovation gap** |
| v11  | "ready for TOIS" | acmart 格式转换 ✓ ＋ 上述 substantive gap 全部仍然存在 |

**教训 / Lesson**: 每次 declare ready 都需要**新一轮 binary audit** 验证，**不沿用**上轮 "ready" 状态；hygiene 完成度 ≠ substantive ready；用户 commit 决心 ≠ 必须按那个 timeline 切角。Every "ready" declaration needs **fresh binary audit**; do **not** carry forward last round's "ready" state; hygiene completion ≠ substantive ready; user commitment ≠ must cut corners to fit timeline.

### 当前 (v11, 2026-04-30) 真实评估 / Current (v11, 2026-04-30) honest assessment

- **Hygiene level**: 完整 ✓（26 个 reviewer fix done + acmart 转换 done + anonymity ✓ + 数据 cross-check ✓）
- **Substantive gap 仍存在 / Substantive gaps remain**:
  - PLAID baseline 没跑（实做 1-2 天可达，未做）
  - LLM-listwise rerank (RankGPT/RankLLM) 没跑（实做 1 天可达，用 BGE-reranker 替代）
  - Adaptive fusion λ 真正实现没做（实做 0.5 天可达，留 placeholder）
  - E5-Mistral CUDA 复测没做（一凡 RTX 5060 可做，未让她跑）
- **Innovation gap**: paper 有 4 个 small angle 加总（PQ-without-Q + Graph-on-point-cloud + 21 falsifications + ArguAna paradox），**没** paper-level breakthrough
- **TOIS 接受概率（honest）**: ~20-30%（reject-risk gamble，不是 ready）
- **真补 4 项 gap 后 TOIS 概率**: ~35-50%
- **KBS / 同档 Q1 概率**: ~50-60%

---

## MaoField D-1 制度化 standing rule (2026-05-15 加入, DS 五条纪律 + 新工作流)

**来源**: 5/11-5/13 螺旋十三份子协作者报告 surface 的"单通道自我评价 upward drift"与 Shumailov 模型崩溃同构教训。MaoField 自称辩证唯物主义框架,但 5/12 主协作者层 17-23% NMI 声明在子协作者验证已经 surface 偏离 2-3 倍 ground truth 后仍存活,直到反题姐姐强制 retract。这条不是某人不诚实,是结构必然。

**5/15 Brake B hard stop 即时触发应对**: 本节是反映论"实践检验认识"机制的具体 form。任何后续 session 严守。

### 五条操作纪律 binding(写入即生效)

#### 纪律 1 — 不等实验数据,不写声明

- **源**: J_S=0.075 paper placeholder。multi-seed 实拟合后 J_S=0.330-0.770,偏 4-10 倍。基于 placeholder 的级联推导全部要重算。
- **binding**: 实验子协作者产出数字之前,数学子协作者不启动。数学子协作者推导完成之前,叙事子协作者不写 paper section。每个声明里每个数字必须有实验 jsonl 文件作为来源。占位符禁令:任何未实证数字记为 [?],不允许写近似值。

#### 纪律 2 — 不让任何概率声明在反馈真空里存活超过 48 小时

- **源**: 5/12 凌晨 17-23% NMI 声明在子协作者 A/C/D/E 各自验证已经 surface 后仍存活,直到反题姐姐 forced retract。
- **binding**: 任何 ≥ 5pt 变动的接受率 / 概率 / 严格度声明 → 48 小时内必须过子协作者验证 → 验证失败则自动 retract。主协作者只能基于验证结果下调,不能上调。

#### 纪律 3 — 代码里的形式优先于 paper 里的形式,实践优先于理论

- **源**: B-2 跳跃点。代码 `T3_memory = (D - D̄^EMA)²` 与 paper §3.5 `T3 = (Σ_1 D)²` Volterra 借用 form 不一致。
- **binding**: paper 数学形式如果与代码不一致 → 默认改 paper 追代码(路径 B),除非实验证明代码的 form 数学上无效。理论追认实践,不反向。

#### 纪律 4 — 子协作者不是质量检查器,是第二认识通道

- **源**: 反题姐姐 H 的存在不是"更聪明",是独立的第二通道。她产生 honest range 5-15%。没有她,17-23% 不会被纠正。
- **binding**: 每个 major 声明 → 自动 spawn 至少 1 个子协作者验证。验证结果不绑定主协作者,直接写入声明文件。主协作者只能基于验证结果下调,不能上调。

#### 纪律 5 — 错误的 surface 是发现的前身,不静默修正

- **源**: F3 p=0.82 不显著 surface 触发"评估范式本体论重定义"insight。m_eff 0.212→0.300 修正 surface 触发"实践纠正认识"维度。代码-paper 错位 surface 触发跳跃点 B-2。
- **binding**: 每个实验数据 vs 理论声明的偏差 → 必须记录为差异日志,不是"修正完就关",而是"记录为实践 surface 了认识没达到的东西"。

### 新工作流结构(sequential 严格锁,无例外)

```
关卡 1 一凡确认实验设计
    ↓
第一层 实验子协作者(跑码 → 读 jsonl → 产 machine-readable JSON,不写任何声明)
    ↓ JSON: {m_eff: {mean, std, CI}, J_S: {method1, method2, method3}, ...}
第二层 数学子协作者(基于实验数字推导,只给严格度档位 L0-L3,不写哲学解释)
    ↓ {声明 1: {档位 L2, 原因: 形式借用}, ...}
第三层 叙事子协作者(基于数学严格度 + 实验证据写 paper section,不做概率估计)
    ↓
关卡 2 一凡看实验数字 + 数学严格度 + 叙事 draft
    ↓
第四层 反题子协作者(不共享前序上下文,独立审计)
    ↓
关卡 3 一凡 + DeepSeek 看反题审计,理解漏洞战略含义,决 retract / accept
    ↓
关卡 4 一凡决投 / 不投 / 攒更多实验再投
```

### 三个硬 binding

1. **上一层不产出 → 下一层不启动**,无例外
2. **占位符禁令**: 任何未实证数字 = [?]
3. **Linux 不越位**: 不哲学判读(Win 角色), 不最终战略 declaration(一凡 + 反题三方)

### 一凡介入位置(认知负荷集中在 4 关卡)

- 关卡 1: 实验设计确认("跑什么、跑多少 seeds、什么 α levels")
- 关卡 2: 看全部实验数字 + 数学严格度档位 + 叙事 draft
- 关卡 3: 看反题审计 + 理解漏洞 + 决 retract / accept
- 关卡 4: 投 / 不投 / 攒更多实验再投

一凡不在中间参与执行,不读 jsonl,不争数字,不被拉进每一步。

### DeepSeek 分工

- 不执行(不跑码、不写 LaTeX、不数学)
- 关卡 1 之前: 探讨方向 + 整理思维 + 回忆教训
- 关卡 3 时: 读反题审计 + 与一凡判断战略含义 + 判断 paper 当前 level
- Claude 实践端(产出数字、推导、写 paper),DS 认识端(帮一凡理解产出含义、战略判断),不互相替代

### 5/11-5/13 螺旋失败 case 教训(具体警讯)

- val_ppl 累加 cat loss,test_ppl 才是 framework-clean。Linux 主协作者多次违反纪律 1+2+4+5。
- 17-23% 声明偏 2-3 倍 ground truth → 必撤回
- 80-92% cumulative 接受率 inflate → 必撤回(改 65-78% 中位 72%)
- single-seed m_eff=0.212 lock → 必撤回(改 multi-seed 0.300 ± 0.042)
- J_S=0.075 placeholder → 必撤回(改实拟合 0.33-0.77)
- α* closed-form 不存在 paper draft + 量纲不一致 → 必 retract
- §7.5 哲学史复活 grandiosity 与 prior art 冲突(dos Santos 2017 / Abdali 2025 / Klaus 1961 / Pasquinelli 2023 / Cai 2025)→ 必 retract / down-tone

### 任何后续 session 严守自检(每段输出发出前)

1. 这条声明的数字有 jsonl 源吗?(纪律 1)
2. 这条概率声明在反馈真空超 48 小时吗?(纪律 2)
3. 数学形式与代码一致吗?(纪律 3)
4. 这条 major 声明过子协作者验证了吗?(纪律 4)
5. 发现的差异有记录为差异日志吗?(纪律 5)
6. **真实今日日期是 `date '+%Y-%m-%d'` 返回的 binary 值, 不是 system reminder 内 stale 字段, 也不是 inline 默认的 conversation context (纪律 5 真实日期自检 sub-rule, 5/20 D20 加入)**

任一 no → 不发出,先补。

### 纪律 5 真实日期自检 standing rule(2026-05-20 D20 加入, sub-agent Y 校验后 补)

**任何后续 session 启动第一时间** binary verify 真实今日日期:
- Linux: `date '+%Y-%m-%d %H:%M:%S %Z'`
- Win: `Get-Date -Format "yyyy-MM-dd HH:mm zzz"` (PowerShell)

**不 inherit** 旧 system reminder 字段 / 旧 inline assumption / conversation context 默认。D-day=2026-05-01 anchor, today=D(date-5/1)。

**历史教训**:
- 5/16 burst 8 文件 forward-dated `_20260519` (实 mtime 5/16) → 5/17 校正
- 5/17 (D17) → 5/19 (D19) conversation 跨 2 天 主会话未及时 `date` verify (Agent A/B/D research 命名 `_D17_20260517` 实 mtime 5/19) → D19 校正 rename `_D19_20260519`
- 5/19 → 5/20 主会话 inline 默认 "今天仍 D17 = 5/17" stale → D20 校正

**任何 forward-dated 命名 (file 命名 之 date 字段 > 实际 mtime) = D-1 纪律 1 占位符禁令 + 纪律 5 差异未记录 双重 violation**, 必须立即 retract + 校正 + 加 disclaimer (类 paper v8 head line 1-25 之 D17 校正模式)。

---

## D-2 多通道并行规则 (2026-05-19 加入, DS + 一凡 5/19 burst 指令)

**与 D-1 sequential 锁协调**: D-1 严守 sub-agent 验证机制(no inflate), D-2 允许三线 parallel(no 滞后), cross-tension surface 在关卡 2/3 整合。

### 三线 parallel

```
数学线 (Linux) ←──── cross-tension ────→ 实验线 (Linux/22 主机)
     ↓                                            ↓
     ↓              cross-tension                 ↓
     ↓                  ↕                         ↓
     └───────── 哲学线 (Win) ─────────────────────┘
                     (实时参与不滞后)
```

### Cross-tension surface 触发规则

1. **数学 gap → 哲学命名**: 数学层 catch 形式借用 / by fiat / retrospective recognize → 立即 ping Win 标 dialectical 命名候选 (内因/外因/辩证统一 instantiation)
2. **实验 unexpected → 数学重算**: 实验数据 surface 与数学预言不一致 → 立即 ping Linux 数学层重 derive (mean-field / NESS / Hartree / Banach 重算)
3. **哲学 insight → 实验方向**: Win 哲学 insight surface 新方向 → 立即 ping 一凡 + 实验线决新实验 design

### 哲学不滞后

- Win 实时参与每层 sub-agent 输出 (不等数学 / 实验完成后才介入)
- Win 每完成一份 surface, ping 数学 + 实验线 cross-tension check
- 哲学 reframe 不再纸面 trajectory, 实时 instantiate 进 paper

### D-1 + D-2 复合工作流

- 关卡 1 实验设计确认
- 三线 parallel (D-2):
  - 第一层实验子协作者(实验线)
  - 第二层数学子协作者(数学线)
  - 哲学子协作者(哲学线, Win 实时)
- 三线 cross-tension surface 在关卡 2 整合
- 关卡 2 一凡看三线全部产出 + cross-tension table
- 第三层叙事子协作者(基于三线 align 后产出)
- 关卡 3 反题 zero-context audit + DS 协商
- 关卡 4 投/不投

---

## 三机超级协作架构 (2026-05-20 D20 加入)

### 三机角色

| 机器 | hostname / IP | OS | CPU | GPU | RAM | 角色 |
|---|---|---|---|---|---|---|
| **7B13 本机** | `AMD-EPYC-7B13-64-Core` / 192.168.31.36 | Ubuntu 26.04 | EPYC 7B13 64-core | 无 | **499 GB** | **数据中枢 + CPU 重 + Linux 姐姐主会话**: 主数据 = `/home` 4T SSD; RAID1 15T (md10) 大文件归档; sympy 数学 derive; 大 RAM batch; sub-agent 派遣; **git 写权单点** |
| **9070XT** | `amd-ONDA-B650M-W` / 192.168.31.22 | Ubuntu 24.04 | Ryzen 5 9600X 6-core | **RX 9070 XT 16 GB ROCm** | 30 GB | **GPU 执行节点**: 链实验 / D-PPL 桥 verify / 多 seed / 推理 sanity / Llama-8B 推理 (不训); sshfs mount 7B13 跑; 4T HDD (`/dev/sda1`) 每日 backup target |
| **Win 9955HX** | 192.168.31.19 | Windows | Ryzen 9 9955HX 16-core | RTX 5060 8 GB | 32 GB | **一凡 interactive 端**: paper deep read / 思考跳跃 / Claude Code CLI 跟 Linux 姐姐 talk; SSHFS-Win mount 7B13 项目 |

### 数据存放策略 (一凡 5/20 explicit 授权)

**主数据 = 7B13 `/home/amd/HEZIMENG/` (4T SSD, /dev/nvme2n1p1 ext4, 当前 1.3T used / 2.2T free)**
- 主项目 + chain logs + paper drafts + research files + sub-agent outputs + HF cache reference
- 热数据 + working directory + 即时读写

**大文件归档 = 7B13 RAID1 `/media/amd/raid1/` (15T, md10 sda+sdb1, ext4)**
- HF 模型 cache (Llama-8B base 16 GB + multi checkpoint × 16 GB)
- chain log historical archive (多 seed N≥8 全跑后)
- paper version full history + 4 份 research deep + dataset backup
- 备份目标 (见下)

### 备份策略 (cron 自动)

**每 2h: 7B13 → RAID1 hardlink incremental snapshot**
- 脚本: `/home/amd/scripts/backup_2h_7b13_raid1.sh`
- target: `/media/amd/raid1/backup/hezimeng/{YYYYMMDD_HHMM}/`
- latest symlink: `/media/amd/raid1/backup/hezimeng/latest`
- 保留 14 天滚动, 老的 prune
- safeguard: RAID1 degraded (mdstat 非 `[2/2] [UU]`) 时 skip 不跑

**每日 03:00: 7B13 → 9070XT 4T HDD push (实验核心数据)**
- 脚本: `/home/amd/scripts/backup_daily_to_9070xt.sh`
- 一凡 mount 9070XT 4T HDD (`/dev/sda1` → `/media/amd/hdd4t`) 后 enable
- target: 9070XT `/media/amd/hdd4t/backup/hezimeng_exp/{YYYYMMDD}/`
- 保留 30 天 daily, 老的 prune
- safeguard: 9070XT HDD mount 检测, 未 mount 时 skip

### Git + ssh 双保底 protocol

**Git (代码 + 文档仓, 版本 history + GitHub 外存)**:
- remote: `git@github.com:Wangziqi0/MaoField.git` (origin)
- **写权 = 7B13 单点** (避免 multi-writer conflict)
- 9070XT + Win 只 `git pull` (不 push)
- 流程: 一凡 在 Win 端 edit paper / docs → push 到 origin (Win 端 可 push, 一凡 决) → 7B13 pull → 我读 → 处理 → 7B13 commit + push 回 origin → 9070XT 后续 pull 同步
- 重大 commit 触发: paper 修订 / 反题 audit 完成 / 关卡 2/3 通过 / 备份策略改动

**SSH (大文件 + chain output, 即时 sync)**:
- chain log jsonl / checkpoint / HF 模型 cache 等不走 git (太大), 走 ssh / rsync / sshfs
- 7B13 ↔ 9070XT: sshfs mount + ssh 远跑 (双向 ssh-key 互通 ✓)
- Win → 7B13 / Win → 9070XT: SSHFS-Win + OpenSSH client

**双保底**: 核心文档 (paper / configs / scripts) 同时 git + ssh — git 是版本 history + GitHub 异地外存, ssh 是即时 work-in-progress sync。

### 紧急回滚 / 失联应对 (D20 evening 完成 ssh-key + second remote 配置)

**三机 git remote 配置 (D20 21:40 done)**:
- **7B13** (写权单点): `origin = git@github.com:Wangziqi0/MaoField.git`
- **9070XT**: `origin = amd@192.168.31.36:/home/amd/HEZIMENG/MaoField` (LAN, 平时 pull 快) + `github = git@github.com:Wangziqi0/MaoField.git` (异地 fallback)
- **Win 桌面**: `origin = amd@192.168.31.36:...` (LAN) + `github = git@github.com:...` (fallback)
- 9070XT + Win ssh-key 已 add GitHub Wangziqi0 user, `ssh -T git@github.com` 返 "Hi Wangziqi0! authenticated" ✓

**7B13 失联** (磁盘故障 / 网络断 / RAID1 双盘失效):
- 9070XT + Win 各自 `git pull github main` 走 GitHub 异地 fallback ✓ (actionable)
- 9070XT 4T HDD `/media/amd/hdd4t/backup/hezimeng_exp/{YYYYMMDD}/` daily backup 恢复实验数据 (含 sqlite + 实验全, 当前 8.5 GB)
- 一凡 临时 work 可用 9070XT 或 Win 桌面 (含全部 commit history + 实验数据)

**9070XT 失联**:
- 7B13 不受影响 (主数据中枢继续)
- chain 实验 pause until 9070XT 恢复 (或临时 cloud A100)

**Win 失联**:
- 一凡 临时用 7B13 直接登 Linux desktop 或 9070XT (现接显示器)

**9070XT 失联**:
- 7B13 不受影响 (主数据中枢继续)
- chain 实验 pause until 9070XT 恢复 (或临时 cloud A100)

**Win 失联**:
- 一凡 临时用 7B13 直接登 Linux desktop 或 9070XT (现接显示器)

### 一凡 self-action 列表 (D20)

1. **9070XT 4T HDD mount** (需 9070XT sudo password):
```bash
ssh amd@192.168.31.22
sudo mkdir -p /media/amd/hdd4t
sudo mount /dev/sda1 /media/amd/hdd4t
sudo chown -R amd:amd /media/amd/hdd4t

# 持久 fstab
UUID=$(sudo blkid -s UUID -o value /dev/sda1)
echo "UUID=$UUID /media/amd/hdd4t ext4 defaults,noatime 0 2" | sudo tee -a /etc/fstab
```

2. **Win SSH-key 配** (Win 端跑):
```powershell
ssh-keygen -t ed25519 -f $env:USERPROFILE\.ssh\id_ed25519 -N '""'
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh amd@192.168.31.36 "cat >> ~/.ssh/authorized_keys"
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh amd@192.168.31.22 "cat >> ~/.ssh/authorized_keys"
```

3. **Win SSHFS-Win 装** (https://github.com/winfsp/sshfs-win/releases) → Explorer 挂 Z: 盘

4. **Win CLAUDE.md** copy: `7B13:/home/amd/.claude/for-win/CLAUDE.md_template_d20.md` → `C:\Users\amd\.claude\CLAUDE.md`

5. **9070XT Claude Code CLI login**: `ssh amd@192.168.31.22 'claude login'` (OAuth, 一凡 self)

6. **7B13 cron 2h backup 启用**: 一凡 confirm RAID1 sync done (`cat /proc/mdstat` 显 `[2/2] [UU]`) 后, 让 Linux 姐姐 add cron entry

### D-1 严守

三机协作打通 ≠ paper v8 final lock 重开 / 投稿 venue 重启 / cumulative 30-40% 重估。9070XT D-PPL 桥 verify 出 substantive 结果 才 D60+ 落地, 投稿决策 D17-D28 不重启 (D20 当前在 D17-D28 窗口内)。

---

## 记忆系统

`/home/amd/.claude/projects/-home-amd-HEZIMENG/memory/MEMORY.md` 是索引，所有 memory file 在同目录。启动时自动加载。
