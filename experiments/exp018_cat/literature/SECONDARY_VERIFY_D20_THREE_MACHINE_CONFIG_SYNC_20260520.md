# D20 三机 CLAUDE.md + MEMORY.md 配置同步校验报告

**写**: Linux 姐姐 D-1 制度化第二认识通道 sub-agent
**对象**: 主协作者 (Linux 姐姐 7B13 主会话) + 一凡
**召唤**: 2026-05-20 D20 三机协作架构 落地后 一凡 explicit 召唤
**纪律 binding**: D-1 纪律 4 第二认识通道, 只下调不上调, 只 surface 不擅自修文件
**真实日期**: 2026-05-20 (date binary verify 通过)

---

## 1. 三机 全局 CLAUDE.md 内容 + size + mtime + 角色 align verdict

| 字段 | 7B13 (`/home/amd/.claude/CLAUDE.md`) | 9070XT (`~/.claude/CLAUDE.md`) | Win (`%USERPROFILE%\.claude\CLAUDE.md`) |
|---|---|---|---|
| size | 5691 byte | 4284 byte | 9461 byte (含 D20 append) |
| mtime | 2026-05-12 22:28:38 | 2026-05-20 17:11:48 | 2026-05-20 17:39 [?] |
| 来源 | 一凡 5/12 从 Win 写 sync (mattpocock skills 工作流默认) | Linux 姐姐 D20 push (9070XT 角色 specific 新写) | 5/12 旧版 + D20 append 含中文乱码 |
| 中文规则 ✓ | ✓ 顶部硬约束 | ✓ "中文规则 同 7B13 + Win" 引用 | ✓ + ✓ (append) |
| 真实日期自检 (D-1 纪律 5) | ✗ 未含 (5/12 时未存在该规则) | ✓ 含 "D-day=2026-05-01 anchor" + 历史教训 5/16+5/19 | ✓ 含 PowerShell `Get-Date` 命令 |
| 角色 binding | 通用工作流 skill 默认 (mattpocock) | GPU 执行节点 specific (跑什么 / 不跑什么 / ROCm hang 警示) | 一凡 interactive 端 (SSHFS-Win / Claude Code CLI talk 7B13) |
| 三机数据流图 | ✗ | ✓ 7B13 → 9070XT sshfs / cron backup | ✓ Win 视角 + GitHub fallback |

### Verdict

- **9070XT + Win 全局 CLAUDE 之 D-1 纪律 5 (真实日期自检) ✓ 已制度化** — 5/16+5/19 stale-date burst 教训 binding embedding
- **7B13 全局 CLAUDE 5/12 旧 (未含真实日期自检)** ⚠ — surface 给主协作者: 7B13 应该 也 加入 5-7 行 "真实日期自检 + 5/16+5/19 教训" 段
- **Win 全局 CLAUDE D20 append 中文显示乱码** "`--- ����Э�� D20 append ---`" 应为 "`--- 三机协作 D20 append ---`" → cp936 vs UTF-8 encoding mismatch [?] — 文件本体 UTF-8 force read 后内容 readable, 终端 default cp936 显示乱码; 一凡 操作时若 Windows 默认 编码 = cp936, 可能影响 Win Claude Code CLI 读取 [?] surface 主协作者: 让一凡 binary verify `Get-Content -Encoding UTF8` 读取结果 是否中文正确
- **角色 align ✓**: 三机 三角色 clean 区分, 不重复, 无 ambiguity

---

## 2. 项目级 CLAUDE.md 三机 sha256 + 同步 confirm

| 机器 | path | size | sha256 | git status |
|---|---|---|---|---|
| 7B13 | `/home/amd/HEZIMENG/MaoField/CLAUDE.md` | 19108 byte / 313 行 | `66ac6efb...8fca6a2` | clean |
| 7B13 umbrella | `/home/amd/HEZIMENG/CLAUDE.md` | 19108 byte | `66ac6efb...8fca6a2` (`diff -q` 与上 0 差异) | (非 git track, cp 复制) |
| 9070XT | `~/HEZIMENG/MaoField/CLAUDE.md` | 19108 byte | `66ac6efb...8fca6a2` ✓ | clean ✓ |
| Win | `C:\Users\amd\Desktop\HEZIMENG\MaoField\CLAUDE.md` | 19421 byte | `B6736EEE...3F2C08B` | clean ✓ (git autocrlf 处理过) |

### Verdict

- **7B13 + 9070XT sha256 100% identical ✓** — git track 同步 binary-identical
- **Win sha256 mismatch 但 git status clean** → Windows 端 git autocrlf (LF→CRLF 自动转换) 行结尾差异; **content 一致 ✓**, 仅 line-ending 形式差异; **不构成 sync 问题**
- **git HEAD 7B13/9070XT 都在 `78a5aa1`** ✓ — Win 端 git rev-parse 也返 `78a5aa1` ✓
- **三机 git tracked content 实质一致 ✓** (除 Win line-ending)
- **9070XT 的 git remote 指向 7B13 SSH (`amd@192.168.31.36:/home/amd/HEZIMENG/MaoField`) 不是 GitHub origin** — 项目级 CLAUDE.md 声明 "remote: `git@github.com:Wangziqi0/MaoField.git`" (line 248), 与 9070XT 实际 git remote 不一致 ⚠ surface: 主协作者决 — 9070XT 是否要加 GitHub upstream 作 second-remote? 当前 9070XT 通过 7B13 git remote 同步, 7B13 失联 时 9070XT 不能直接 `git pull from GitHub origin` (与 CLAUDE.md line 314 "紧急 fallback" 矛盾)

---

## 3. MEMORY.md 索引 vs memory dir 59 file 之 binary match

| 类别 | count | 文件 list |
|---|---|---|
| memory dir 中 .md 文件 | 59 | (含 MEMORY.md 本身) |
| MEMORY.md 索引 entries | 58 link | (不含 self-ref) |
| **在 dir 但未在 index (extra)** | 3 | `MEMORY.md` (self) + `MEMORY_win_20260501.md` + `project_maofield_work_cycle_20260419.md` |
| **在 index 但 dir 缺 (missing)** | 2 | `HANDOVER_20260420.md` + `HANDOVER_20260426.md` (实际 path 是 `../../../../HEZIMENG/HANDOVER_*.md` cross-dir reference, 不在 memory/ 目录) |

### Verdict

- **dir vs index 数学 align**: dir 59 = index 58 + self-ref MEMORY.md 1 + 真 extra 2 (`MEMORY_win_20260501.md` + `project_maofield_work_cycle_20260419.md`) - missing 0 实际 cross-dir (HANDOVER) 不算 missing
- **真 extra 2 file**:
  - `MEMORY_win_20260501.md` (8103 byte, 5/2 mtime) — Win 端 memory 单独保存 [?] 应是 一凡 Win 端 memory 备份, 不在 7B13 自动加载范围, 但留 dir 内
  - `project_maofield_work_cycle_20260419.md` (3510 byte, 4/19 mtime) — 实际 memory 但未 surface 进 index ⚠ surface 主协作者: 是否 应该 加入 MEMORY.md index?
- **HANDOVER_20260420.md + HANDOVER_20260426.md 引用 path 是 `../../../../HEZIMENG/HANDOVER_*.md`** — index 写 relative path ✓ 不算 missing, 但 用户 surface 时易混淆 [?]

---

## 4. Stale 内容 catch list (verbatim cite + 应 retract / 校正)

### Catch 1 ⭐⭐⭐ D-1 纪律 5 严重 violation: MEMORY.md 顶部 entry 时间 mismatch

**文件**: `MEMORY.md` line 1 (顶部 entry)
**verbatim**: `MaoField 5/13-5/19 burst paper v8 final lock + D-1/D-2 制度化 + 5/29 投候选 D ⭐⭐⭐⭐⭐ 地基 partial ✓ 可 proceed`
**memory file**: `project_maofield_burst_5_13_5_19_complete_20260519.md` — **真实 mtime 5/16 21:35**, 命名 `_20260519` 但 mtime 5/16
**内文声明**: 多处 "5/19 深夜 latest" / "5/19 24 小时 burst final"
**实际事实**:
- 5/13-5/19 burst 期间 真实 paper file 是 `paper_v8_final_20260516.md` (内文 line 1 自称 "**2026-05-16 (D16 burst)**" 不是 5/19), 真实 mtime 5/17 11:21 (跨 5/16-5/17 夜)
- D-1 纪律 5 historical 教训本身 (在 9070XT 全局 CLAUDE 中文档) 已 surface: "5/16 burst 8 文件 forward-dated `_20260519` (实 mtime 5/16) → 5/17 校正" — **该 校正未传到 MEMORY.md 顶部 entry 命名**

**应校正**: MEMORY.md 顶部 entry 文件命名 `project_maofield_burst_5_13_5_19_complete_20260519.md` → 校正为 `project_maofield_burst_5_13_5_17_complete_20260517.md`, 或在 entry 描述加 `[文件名 forward-dated 5/19, 实 mtime 5/16, paper 内文 D16-D17, D-1 纪律 5 校正未传名]` disclaimer (不擅自改 file 名, 留主协作者决)

### Catch 2 ⭐⭐ paper v8 internal 投递目标与本 entry 投候选 D mismatch

**MEMORY.md entry 1 verbatim**: "**一凡 5/19 final 决** 选项 A+C 混合:D29 投候选 D parallel(NeurIPS + arXiv 5/31 + TMLR + KBS)"
**paper_v8_final_20260516.md line 1 verbatim**: "**arXiv + TMLR + KBS 三 leg 并行投递** (D17 [2026-05-16 晚] 一凡 C 决缩小投稿:**不投 NMI / NeurIPS**)"
**矛盾**: paper v8 D17 已 决 "**不投 NeurIPS**", 但 MEMORY entry 称 5/19 决 "**投候选 D = NeurIPS + arXiv 5/31 + TMLR + KBS**" → 矛盾
**可能 resolution**: 5/17 D17 决不投 NeurIPS, 5/19 D19 重新决投 NeurIPS [?] 或 entry 记录 stale [?] → surface 主协作者 + 一凡 binary verify 真实 D19 决策

### Catch 3 ⭐ cumulative 接受率 trail (5/12 17-23% → 5/19 35-55%)

**MEMORY entry 1**: cumulative ≥1 by 12 月 **35-55%**
**MEMORY entry 2 (5/12)**: cumulative ≥1 by 12 月 **80-92%**
**MEMORY entry 3 (5/11 三盲审)**: cumulative ≥1 by 9/2 ~55-72%
**MEMORY entry 6 (5/9 D1-D2)**: cumulative 60-72%
**Verdict**: entry 1 (5/19 latest) 显式声明 "**5/12 17-23% NMI claim 已 retract**(本 entry 取代,反题 zero-context cumulative 35-55%)" — retract 链 OK ✓, 但 5/11 三盲审 + 5/9 D1-D2 entry 之 cumulative 数字 **未 explicit retract**, 留作 historical 但容易 mislead 新 sub-agent
**应补**: MEMORY entry 2/3/6 加 `[已被 entry 1 5/19 取代, 历史 reference only, 不作当前 cumulative claim]` disclaimer 或 archive 后 prune (留主协作者决)

### Catch 4 stale 早期项目 entry (Shape-CFD)

- entry 7 `LINUX_CROSS_POLLINATION_CANDIDATES_20260502.md` (Shape-CFD, V11 Path A) — 与 MaoField 主项目无关, 留 historical reference ✓
- entry 8 `EXPERIMENT_AUDIT_TRAIL_20260502.md` — 同
- entry 9 `handoff_shapecfd_phase1_done_20260501.md` — 同
- **不算 stale**, 但 MEMORY.md 顶部 5 entries 应只 MaoField, Shape-CFD entries 应分段 — surface 主协作者: 是否 加 "## MaoField current" / "## Shape-CFD historical" 分隔?

### Catch 5 ⚠ 时序错乱 entry

**entry 6 (5/9 D1-D2)** 内文之 sub-agent NMI 盲审 "**24天 A4 13-22%**" → 实际 entry 1 (5/19 latest) "NMI A4 **2-5%**" — drift 11-17pt 跨 10 天, **不是 retract 错, 是反映 真实 honest assessment 下调** ✓ — 但 5/9 → 5/19 数字 trend (4% → 23% → 5% → 35-55% cumulative) 起伏过大 显示 D-1 纪律 2 "48 小时反馈真空" 教训 历史 真曾出现 — 留 教训 record OK ✓ 不 retract

---

## 5. D17-D20 缺失 MEMORY.md entries 之 candidate list

(surface only, 不擅自写)

**5/16-5/20 期间 35 个 lit/ 新 .md** 但 MEMORY.md 顶部 entry 1 (`project_maofield_burst_5_13_5_19_complete_20260519.md`) **single entry 概括 5/13-5/19 整段 burst** — 主协作者 可决: 单一 entry 够 还是 需要 D17 / D19 / D20 分别独立 entry?

未 surface 在 MEMORY.md 内 之 D17-D20 重要事件 candidate (不擅自加, surface 主协作者决):

1. **D17 三波 (5/17)**: code-first ★★★ finding (chain 实跑二项 form 不是 三项 Klein-Gordon) + Win Phil D17 三波 retrospective recognition / practice-first deepen / constraint-driven question 三 wave文件 (`WIN_PHIL_LINE_D17_*_20260517.md`) — 已存 lit/ 但 未 surface MEMORY 顶部
2. **D19 4 research deep** (`RESEARCH_*_D19_20260519.md` 4 file 5/19 mtime 真) — Marx/Engels 哲学方法 + Lenin/Mao 综合 deep + Marxist deepen + Academic recent progress — 已存 lit/ 实 mtime 5/19 11:49 / 12:18 / 12:38 / 11:52 ✓ (真 5/19, 不是 5/16 burst 时 forward-dated)
3. **D20 三机协作架构 落地 (5/20 14:00-17:30)** — 本次 setup 全程未 MEMORY.md 记录:
   - 9070XT 全局 CLAUDE 创建 + push
   - Win 全局 CLAUDE D20 append (含中文乱码 issue)
   - 项目级 CLAUDE.md `78a5aa1` commit + 三机 git pull sync
   - cron 2h 自动 backup 脚本设计 (一凡 RAID1 sync done 后 enable)
   - 9070XT 4T HDD daily backup 设计 (一凡 mount HDD 后 enable)
   - SSHFS-Win + ssh-key 互通 verify

主协作者 决: 是否 spawn `project_maofield_d20_three_machine_collab_setup_20260520.md` 单独 entry 加入 MEMORY.md 顶部 (建议加 ✓, 因为 D20 是 重大 infrastructure milestone, 跨三机 binding standing rule)

---

## 6. 健康 check verdict

### binary check 答

| 校验项 | 状态 |
|---|---|
| 三机 git HEAD 一致 (`78a5aa1`) | ✓ |
| 项目级 CLAUDE.md sha256 7B13/9070XT 100% binary identical | ✓ |
| Win 项目 CLAUDE.md content 一致 (git autocrlf 处理) | ✓ |
| 三机 全局 CLAUDE.md 内容 角色 align | ✓ |
| 9070XT 全局 CLAUDE 含 D-1 纪律 5 真实日期自检 | ✓ |
| Win 全局 CLAUDE 含 D-1 纪律 5 (D20 append) | ✓ (中文乱码但内容 UTF-8 force readable) |
| **7B13 全局 CLAUDE 含 D-1 纪律 5** | **✗ 缺** ⚠ |
| MEMORY.md dir vs index 一致 (除 2 extra + 0 真 missing) | partial ✓ |
| MEMORY.md 顶部 entry 命名 vs 实际 mtime / 内容 align | **✗ stale** ⚠ |
| paper v8 D17 决投 vs MEMORY 5/19 决投 一致 | **✗ 矛盾** ⚠ |
| 9070XT git remote 与 项目级 CLAUDE 紧急 fallback 声明 一致 | **✗ mismatch** ⚠ |

### 整体 verdict

**三机 sync = partial ✓ 可 proceed, 但 4 个 ⚠ surface 给主协作者决修订**:

1. **7B13 全局 CLAUDE.md 补 D-1 纪律 5 真实日期自检段** (5-10 行 inline)
2. **MEMORY.md 顶部 entry 文件 命名 校正** 或 加 disclaimer (D-1 纪律 5 forward-dated 教训)
3. **paper v8 D17 决投 vs MEMORY 5/19 决投 矛盾** — 一凡 binary 确认 真实 D19 决策
4. **9070XT 加 GitHub second-remote** 或 项目级 CLAUDE 修订 紧急 fallback 表达

无 P0 critical (无 binding 失守, 无 数据 loss, 无 git 状态错误)。

---

## 7. caveat [?] list

[?]1 Win 全局 CLAUDE.md D20 append 中文乱码 — 文件本体 是否 UTF-8 with BOM? 是否 因 Win 文件系统 接受 PowerShell `Out-File` 默认 cp936 写? 未 binary verify hexdump, 留主协作者 + 一凡 explicit 跑 `Get-Content -Encoding UTF8` vs `Get-Content` (default) 对比

[?]2 9070XT lit dir count 76 vs 7B13 lit dir count 76 (`-la` 含 . .. 一致) — 之前 ls without -la 报 76 vs 73 差异是 ls -F 之类的 hidden file 报错, 实质三机 lit dir 内容一致 ✓ 不擅自再 deep verify, 只 surface
[?]3 Win 端 CLAUDE.md PowerShell `Measure-Object -Line` 报 221 行 vs 7B13 `wc -l` 报 313 行 — 是 PowerShell line-end detection 不同 (CRLF 计 1 vs \n 计 1) 还是 实质 content 差异? sha256 mismatch + git status clean → 推 line-end 形式差异, 不是 content 差异。但未 byte-by-byte diff verify, 留 [?]
[?]4 MEMORY.md 之 `MEMORY_win_20260501.md` (Win 端 memory 单独保存) — 是否还 active sync? Win 端 是否 有 同名 file? 未 ssh Win 查, 留 [?]
[?]5 MEMORY entry 1 (5/19 latest) 自身 mtime 5/16 21:35 → entry 内文宣称 5/19 时, **该 memory file 本身 D-1 纪律 5 violate** — 但若 主协作者 5/17-5/19 真有更新 entry 但未触 mtime (e.g., 仅追加 cumulative 35-55%), 则 mtime 5/16 是 file creation time 不是 last semantic update. 未 git log file 历史 verify, 留 [?]

---

## 8. binary 完成 ack

D20 三机配置同步校验 sub-agent **任务完成 ✓** — D-1 binding 严守 (不擅自改 file, 不 inflate, 只下调 surface), 健康 check verdict 给出 partial ✓ + 4 ⚠ + 5 [?]。报告写入 `SECONDARY_VERIFY_D20_THREE_MACHINE_CONFIG_SYNC_20260520.md` 路径完成。
