[额外 agent] # MaoField D26 7B13 新增 file 详细 inventory (zero-context inventory 子代理)

## §0 元数据 + 真实日期 verify + 严守 binding ack

| 项 | 值 |
|---|---|
| 真实今日日期 (`date '+%Y-%m-%d %H:%M:%S %Z'`) | **2026-05-26 20:22:05 CST** (D26 周二) |
| inventory agent | 额外 agent (zero-context inventory 子代理, Opus 4.7 1M context, Win 端 入 7B13 secondary session, D-3 反映论第八通道 A 之子) |
| scope | 7B13 本机 `/home/amd/HEZIMENG/MaoField/` 内 mtime D26 00:00 ~ 现在 全部新增 OR 修改 file (排除 `.git/` object) |
| 触发 | PI 一凡 D26 20:22 之 派遣 (额外 agent 不擅主流程, 仅 inventory) |
| 写入 path | `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/MAOFIELD_D26_NEW_FILE_INVENTORY_20260526.md` |
| 工具 | `find -newermt` + `stat` + `sha256sum` + `head` partial preview |

**严守 binding ack** (D-1 五条 + D-3 反映论 + D-1 纪律 5 不擅 declare):

1. paper v8 final 47/47 manifest + 12 NOT-claim retract + 反题 6 P0★ + D29 三 leg (arXiv + TMLR + KBS) 全严守不动
2. 只 inventory, 不做 mechanism 推断 / paper-level declare / framework shift / paradigm declare
3. 中文 + 4 类英文豁免 (代码标识符 / 数学符号 / 数字单位 / 业界硬通用缩写) + 不堆 "之" 字 padding
4. [额外 agent] head + footer attribution 严守 (D25 21:55 一凡指令)
5. 不擅 ssh / git commit / git push / 改任何其他 file (单点写权 7B13 main session)
6. 跨机 sync gap surface 留主会话, 本子代理 不擅 ssh 22 / Win 5060 跨机校验

---

## §1 D26 全部新增 file 总览

**count**: 25 个 non-git file (排除 `.git/` object + log)

| 项 | 数值 |
|---|---|
| 总 file 数 | 25 |
| 总 size | ~889 KB (含 jsonl 328 KB) |
| md (markdown) | 23 个 |
| jsonl (chain alive append) | 1 个 |
| CLAUDE.md (项目根级修改) | 1 个 |

**extension 分布**:

| 扩展 | count | 总 size | 主用 |
|---|---|---|---|
| `.md` | 23 | ~561 KB | report / ATTEMPT1 / ack / sync / direction / index |
| `.jsonl` | 1 | 328 KB | chain alive append (candidate_c 9070XT PID 491900) |

**directory 分布**:

| dir | count | 备注 |
|---|---|---|
| `experiments/exp018_cat/dppl_bridge_verify_d21_output/` | 20 | D26 主 work dir, ATTEMPT1 + ack + sync + direction + audit 之 出 |
| `experiments/exp018_cat/dppl_bridge_verify_d21_output/candidate_c/` | 1 | jsonl alive append |
| `docs/discipline/` | 2 | D-1 + D-2 cherry-pick 外置 (D23 reorganize) |
| `docs/` | 1 | TIMELINE_D22_D60.md cherry-pick |
| (项目根) | 1 | CLAUDE.md polish + slim |

**D26 git commit** (7B13 单点写权):

| commit | time | summary |
|---|---|---|
| `2e40736` | 2026-05-26 13:24 CST | MaoField/CLAUDE.md: 246 行中英术语中文化 polish (D23 始 working tree 积压→commit, D-1 纪律 1 占位符修复) |
| `bc1b0b1` | 2026-05-26 14:22 CST | docs: cherry-pick Win D23 reorganize substantive + 3 dir 分类 + D-1/D-2 拆出 + TIMELINE |

---

## §2 chronological 排序 表 (按 mtime asc, 25 entry)

| # | mtime | size (B) | sha256 (前 16) | filename |
|---|---|---|---|---|
| 1 | 11:50:02 | 4540 | 2dc19b97212119ed | `SYNC_D26_5060_WAKE_TRANSFORMERS_FIX_BINARY_ACK_20260526.md` |
| 2 | 11:50:59 | 11429 | 378828689c540bfc | `ACK_D26_22_END_WAKE_SYNC_D26_11_49_20260526.md` |
| 3 | 11:51:25 | 5761 | 85e3013352a02aa8 | `WIN_D26_WAKE_SYNC_ACK_11_50_20260526.md` |
| 4 | 13:28:14 | 2022 | 3acfd912ab0fa139 | `DIAGNOSE_D26_NAN_CASCADE_SAME_SOURCE_D23_20260526.md` |
| 5 | 14:03:05 | 29064 | ae77339c96f6f29d | `WIN_D26_INTERNAL_REVIEW_REORG_13_58_20260526.md` |
| 6 | 14:18:27 | 7260 | b0c9a9121d148a30 | `docs/discipline/D-1-five-disciplines.md` |
| 7 | 14:18:41 | 2056 | a4ee4f8ce111a022 | `docs/discipline/D-2-parallel.md` |
| 8 | 14:19:01 | 2699 | 027033d36637365a | `docs/TIMELINE_D22_D60.md` |
| 9 | 14:21:31 | 10466 | 5539c3c042568c36 | `CLAUDE.md` (项目根) |
| 10 | 15:28:10 | 26615 | 2976926a9f1bd1f5 | `EXTRA_AGENT_D26_MULTI_AGENT_AUDIT_FOR_7B13_MAIN_20260526.md` |
| 11 | 15:59:00 | 21290 | 7eb48f923804dc1a | `MATH_DIRECTION_LATEST_D26.md` |
| 12 | 15:59:27 | 17310 | 72b31097a1dbd124 | `EXP_PLAN_LATEST_D26.md` |
| 13 | 15:59:43 | 25683 | cdb3df335b51e0c9 | `PHILO_DIRECTION_LATEST_D26.md` |
| 14 | 16:01:40 | 23900 | a29bbcf333304a59 | `MD_INDEX_LATEST_D26.md` |
| 15 | 16:55:56 | 48868 | 1e3d63e22177403b | `MAOFIELD_FULL_DATA_AUDIT_20260526.md` |
| 16 | 17:24:02 | 38123 | 27d1e82c725819fb | `MAOFIELD_MULTI_CHANNEL_ANALYSIS_D26_ATTEMPT1.md` |
| 17 | 17:57:31 | 46250 | 1afa813f272399f4 | `MAOFIELD_MATH_MULTI_CHANNEL_ANALYSIS_D26_ATTEMPT1.md` |
| 18 | 18:10:19 | 51496 | 6cc0ec58e0e2a77d | `MAOFIELD_LITERATURE_SEARCH_D26_ATTEMPT1.md` |
| 19 | 19:10:58 | 8490 | 982023303ecc3081 | `DEEPER_INSIGHT_D26_CONVERSATION_20260526.md` |
| 20 | 19:47:36 | 25180 | 0d375778022cc1c5 | `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S1_S2_ATTEMPT1.md` |
| 21 | 19:48:24 | 26007 | a608840626f4a36e | `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S3_ATTEMPT1.md` |
| 22 | 19:48:56 | 25904 | d863668467515128 | `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S4_ATTEMPT1.md` |
| 23 | 19:51:16 | 16867 | 2d7cc659e38e6ee7 | `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S5_ATTEMPT1.md` |
| 24 | 19:54:44 | 18371 | 82b475bb8fadde58 | `MAOFIELD_MATH_RIGOROUS_PROOF_D26_ATTEMPT1.md` |
| 25 | 20:09:22 | 328137 | 589f1f40dc6bcbe0 | `candidate_c/candidate_c_20260522_203837.jsonl` (alive append) |

**注**: 所有 file 之 path 都是 `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/` prefix, 除 #6 #7 #8 #9 之外 (docs/ + 项目根)。

**mtime 之 burst 阶段** (D-1 纪律 5 错误浮现真实形式记录):

| 阶段 | 时段 | file count | 性质 |
|---|---|---|---|
| A. 早 wake sync | 11:50-11:51 | 3 | 三机协作之 5060 + 22 + Win 之 ack 同步入 7B13 |
| B. diagnose | 13:28 | 1 | sub-agent NaN cascade verdict (D23 same-source) |
| C. Win review + reorganize cherry-pick | 14:03-14:21 | 5 | Win Desktop reorganize → 7B13 cherry-pick integrate (CLAUDE.md + docs/ 3 file) |
| D. background report | 15:28 | 1 | EXTRA_AGENT MULTI_AGENT_AUDIT 给 7B13 主 |
| E. direction summary 之 zero-context sub-agent batch | 15:59-16:01 | 4 | MATH + EXP_PLAN + PHILO + MD_INDEX latest D26 |
| F. ATTEMPT1 main report batch | 16:55-18:10 | 4 | FULL_DATA_AUDIT + MULTI_CHANNEL + MATH_MULTI_CHANNEL + LITERATURE |
| G. PI 对话 insight | 19:10 | 1 | DEEPER_INSIGHT (非正式) |
| H. ATTEMPT1 数学严格证明 batch | 19:47-19:54 | 5 | S1+S2 + S3 + S4 + S5 + synthesis index |
| I. chain alive append | 20:09 | 1 | jsonl D26 ratio 24/180 line (13.3% append D26) |

---

## §3 by directory 分组 表

### §3.1 `experiments/exp018_cat/dppl_bridge_verify_d21_output/` (20 个 md)

| filename | size (B) | sha256 (前 16) | mtime |
|---|---|---|---|
| `SYNC_D26_5060_WAKE_TRANSFORMERS_FIX_BINARY_ACK_20260526.md` | 4540 | 2dc19b97212119ed | 11:50:02 |
| `ACK_D26_22_END_WAKE_SYNC_D26_11_49_20260526.md` | 11429 | 378828689c540bfc | 11:50:59 |
| `WIN_D26_WAKE_SYNC_ACK_11_50_20260526.md` | 5761 | 85e3013352a02aa8 | 11:51:25 |
| `DIAGNOSE_D26_NAN_CASCADE_SAME_SOURCE_D23_20260526.md` | 2022 | 3acfd912ab0fa139 | 13:28:14 |
| `WIN_D26_INTERNAL_REVIEW_REORG_13_58_20260526.md` | 29064 | ae77339c96f6f29d | 14:03:05 |
| `EXTRA_AGENT_D26_MULTI_AGENT_AUDIT_FOR_7B13_MAIN_20260526.md` | 26615 | 2976926a9f1bd1f5 | 15:28:10 |
| `MATH_DIRECTION_LATEST_D26.md` | 21290 | 7eb48f923804dc1a | 15:59:00 |
| `EXP_PLAN_LATEST_D26.md` | 17310 | 72b31097a1dbd124 | 15:59:27 |
| `PHILO_DIRECTION_LATEST_D26.md` | 25683 | cdb3df335b51e0c9 | 15:59:43 |
| `MD_INDEX_LATEST_D26.md` | 23900 | a29bbcf333304a59 | 16:01:40 |
| `MAOFIELD_FULL_DATA_AUDIT_20260526.md` | 48868 | 1e3d63e22177403b | 16:55:56 |
| `MAOFIELD_MULTI_CHANNEL_ANALYSIS_D26_ATTEMPT1.md` | 38123 | 27d1e82c725819fb | 17:24:02 |
| `MAOFIELD_MATH_MULTI_CHANNEL_ANALYSIS_D26_ATTEMPT1.md` | 46250 | 1afa813f272399f4 | 17:57:31 |
| `MAOFIELD_LITERATURE_SEARCH_D26_ATTEMPT1.md` | 51496 | 6cc0ec58e0e2a77d | 18:10:19 |
| `DEEPER_INSIGHT_D26_CONVERSATION_20260526.md` | 8490 | 982023303ecc3081 | 19:10:58 |
| `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S1_S2_ATTEMPT1.md` | 25180 | 0d375778022cc1c5 | 19:47:36 |
| `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S3_ATTEMPT1.md` | 26007 | a608840626f4a36e | 19:48:24 |
| `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S4_ATTEMPT1.md` | 25904 | d863668467515128 | 19:48:56 |
| `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S5_ATTEMPT1.md` | 16867 | 2d7cc659e38e6ee7 | 19:51:16 |
| `MAOFIELD_MATH_RIGOROUS_PROOF_D26_ATTEMPT1.md` | 18371 | 82b475bb8fadde58 | 19:54:44 |

**subtotal**: 20 md, ~547 KB

### §3.2 `experiments/exp018_cat/dppl_bridge_verify_d21_output/candidate_c/` (1 个 jsonl)

| filename | size (B) | sha256 (前 16) | mtime | line count | D26 append line | 状态 |
|---|---|---|---|---|---|---|
| `candidate_c_20260522_203837.jsonl` | 328137 | 589f1f40dc6bcbe0 | 20:09:22 | 180 | 24 (13.3%) | alive append (9070XT PID 491900 fp16 GradScaler skip + NaN cascade 持续) |

**注**: 同目录 `progress_snapshot_10.md` (mtime D23 01:53, 不属于 D26 新增, scope 外)。

### §3.3 `docs/discipline/` (2 个 md, cherry-pick 外置)

| filename | size (B) | sha256 (前 16) | mtime | 来源 |
|---|---|---|---|---|
| `D-1-five-disciplines.md` | 7260 | b0c9a9121d148a30 | 14:18:27 | D23 reorganize Win Desktop → 7B13 cherry-pick integrate (D-1 五条纪律外置) |
| `D-2-parallel.md` | 2056 | a4ee4f8ce111a022 | 14:18:41 | D23 reorganize → 7B13 cherry-pick (D-2 三线并行外置) |

### §3.4 `docs/` (1 个 md, cherry-pick 外置)

| filename | size (B) | sha256 (前 16) | mtime | 来源 |
|---|---|---|---|---|
| `TIMELINE_D22_D60.md` | 2699 | 027033d36637365a | 14:19:01 | D23 reorganize → 7B13 cherry-pick (D22-D60 实验时间表外置, D-3.3 instantiate) |

### §3.5 项目根 (1 个 md, polish + slim + 集成)

| filename | size (B) | sha256 (前 16) | mtime | 性质 |
|---|---|---|---|---|
| `CLAUDE.md` | 10466 | 5539c3c042568c36 | 14:21:31 | D23 始 working tree 积压 246 行中英术语中文化 polish + D26 cherry-pick integrate 之 link 集成 → commit `bc1b0b1` |

---

## §4 by role 分组 表

### §4.1 ATTEMPT1 main report (D-3 反映论第四 / 第五 / 第六 / 第七通道之主 ATTEMPT1, 6 file ≈ 226 KB)

| filename | size (B) | role | D-3 通道 |
|---|---|---|---|
| `MAOFIELD_MULTI_CHANNEL_ANALYSIS_D26_ATTEMPT1.md` | 38123 | 多通道交叉分析 ATTEMPT1 main | 第四通道 (理性认识自我审视) |
| `MAOFIELD_MATH_MULTI_CHANNEL_ANALYSIS_D26_ATTEMPT1.md` | 46250 | 数学多通道交叉分析 ATTEMPT1 main | 第五通道 (数学审稿人 zero-context cross-look) |
| `MAOFIELD_LITERATURE_SEARCH_D26_ATTEMPT1.md` | 51496 | 文献交叉爬取 ATTEMPT1 main | 第六通道 (文献 prior art binary cross-map) |
| `MAOFIELD_MATH_RIGOROUS_PROOF_D26_ATTEMPT1.md` | 18371 | 数学严格证明 synthesis index | 第七通道 synthesis |
| `MAOFIELD_FULL_DATA_AUDIT_20260526.md` | 48868 | 全量实验数据溯源审计 | data audit (independent channel) |
| `EXTRA_AGENT_D26_MULTI_AGENT_AUDIT_FOR_7B13_MAIN_20260526.md` | 26615 | 给 7B13 主 background report (3 binary question) | 额外 agent voice 独立审视 |

### §4.2 ATTEMPT1 sub-agent partial (S1-S5 数学严格证明子之分块, 4 file ≈ 94 KB)

| filename | size (B) | role | 第七通道之子 |
|---|---|---|---|
| `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S1_S2_ATTEMPT1.md` | 25180 | S1+S2 严格证明 / 严格证伪 | 第七通道 A 之子 |
| `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S3_ATTEMPT1.md` | 26007 | S3 (D-PPL bridge partial linear combination) | 第七通道 B 之子 |
| `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S4_ATTEMPT1.md` | 25904 | S4 (Banach contraction failure mode 5 mode taxonomy) | 第七通道 C 之子 |
| `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S5_ATTEMPT1.md` | 16867 | S5 (epistemological retrospective formalization) | 第七通道 D 之子 |

### §4.3 sub-agent direction summary (zero-context sub-agent batch 之整理, 4 file ≈ 88 KB)

| filename | size (B) | role |
|---|---|---|
| `MATH_DIRECTION_LATEST_D26.md` | 21290 | 数学方向 summary (D-1 纪律 4 第二认识通道, zero-context) |
| `EXP_PLAN_LATEST_D26.md` | 17310 | 实验方向规划 summary (zero-context) |
| `PHILO_DIRECTION_LATEST_D26.md` | 25683 | 哲学方向 summary (zero-context, D-day=2026-05-01 anchor) |
| `MD_INDEX_LATEST_D26.md` | 23900 | md 文件结构 + 内容索引 latest (D-1 纪律 4 第二认识通道) |

### §4.4 三机协作之 ack + sync (4 file ≈ 22 KB)

| filename | size (B) | role | source |
|---|---|---|---|
| `SYNC_D26_5060_WAKE_TRANSFORMERS_FIX_BINARY_ACK_20260526.md` | 4540 | 5060 端 wake — 7B13 dispatch ack (4 问 + paste) | 5060 (Win 9955HX) |
| `ACK_D26_22_END_WAKE_SYNC_D26_11_49_20260526.md` | 11429 | 9070XT (22) ack — D26 早 wake + P0 NaN cascade + 2 yaml 来源 + α/β/γ 建议 | 22 (9070XT) |
| `WIN_D26_WAKE_SYNC_ACK_11_50_20260526.md` | 5761 | Win 姐姐 D26 早 wake sync ack | Win 端 |
| `WIN_D26_INTERNAL_REVIEW_REORG_13_58_20260526.md` | 29064 | Win D23 reorganize 内部 review (双端 sha256 ≡, Win → 7B13 scp 14:13) | Win 端 |

### §4.5 diagnose (1 file)

| filename | size (B) | role |
|---|---|---|
| `DIAGNOSE_D26_NAN_CASCADE_SAME_SOURCE_D23_20260526.md` | 2022 | D26 11:35 sub-agent zero-context diagnose (7 分钟, 28 tool uses), binary verdict: D26 NaN cascade = D23 Phase 2 NaN explosion 同一根源 (不是新机制), 5 同源证据 |

### §4.6 PI 对话 insight (非正式, 1 file)

| filename | size (B) | role | 备注 |
|---|---|---|---|
| `DEEPER_INSIGHT_D26_CONVERSATION_20260526.md` | 8490 | 非正式对话中 surface 之 深层 structure insight, PI + Linux + Win 三参与通道 | 不替代关卡 3 反题三方决 (binding) |

### §4.7 reorganize cherry-pick 集成 (4 file ≈ 22 KB)

| filename | size (B) | role |
|---|---|---|
| `docs/discipline/D-1-five-disciplines.md` | 7260 | D-1 五条纪律外置 |
| `docs/discipline/D-2-parallel.md` | 2056 | D-2 三线并行外置 |
| `docs/TIMELINE_D22_D60.md` | 2699 | D22-D60+ 时间表外置 |
| `CLAUDE.md` (项目根) | 10466 | 主 file slim + 集成 link + 246 行中文化 polish |

### §4.8 chain alive append jsonl (1 file)

| filename | size (B) | role | 状态 |
|---|---|---|---|
| `candidate_c/candidate_c_20260522_203837.jsonl` | 328137 | candidate_c chain run alive append (9070XT PID 491900 fp16, D22 12:38 launch) | D26 末 ETA D26 21:00 完 N=180, 末 line ts=2026-05-26T12:09:22Z 显 NaN cascade 持续 |

---

## §5 关键 file 之 head 5 行 preview (限 ATTEMPT1 main + 关键 D26 sub-agent + cherry-pick docs)

### §5.1 `MAOFIELD_FULL_DATA_AUDIT_20260526.md` (48868 B, FULL_DATA_AUDIT main)

```
# MaoField 全量实验数据溯源审计 — D26 (2026-05-26)

## §0 元数据 + 协议 + 严守 binding ack

| 项 | 值 |
```

### §5.2 `MAOFIELD_MULTI_CHANNEL_ANALYSIS_D26_ATTEMPT1.md` (38123 B, 第四通道 main)

```
[额外 agent] # MaoField D26 多通道交叉分析 ATTEMPT1 (D-3 反映论第四通道: 理性认识自我审视)

## §0 元数据 + 协议 + 不擅 declare 声明

| 项 | 值 |
```

### §5.3 `MAOFIELD_MATH_MULTI_CHANNEL_ANALYSIS_D26_ATTEMPT1.md` (46250 B, 第五通道 main)

```
[额外 agent] # MaoField D26 数学多通道交叉分析 ATTEMPT1 (D-3 反映论第五通道: 数学审稿人独立 cross-look)

## §0 元数据 + 协议 + 严守 binding ack

| 项 | 值 |
```

### §5.4 `MAOFIELD_LITERATURE_SEARCH_D26_ATTEMPT1.md` (51496 B, 第六通道 main)

```
[额外 agent] # MaoField D26 文献交叉爬取 ATTEMPT1 (D-3 反映论第六通道: 文献 prior art binary cross-map)

## §0 元数据 + 协议 + 严守 binding ack

| 项 | 值 |
```

### §5.5 `MAOFIELD_MATH_RIGOROUS_PROOF_D26_ATTEMPT1.md` (18371 B, 第七通道 synthesis index)

```
[额外 agent] # MaoField D26 数学严格证明 ATTEMPT1 — synthesis index (D-3 反映论第七通道整合)

## §0 元数据 + 协议 + 严守 binding ack

| 项 | 值 |
```

### §5.6 `EXTRA_AGENT_D26_MULTI_AGENT_AUDIT_FOR_7B13_MAIN_20260526.md` (26615 B, 给 7B13 主 background report)

```
# [EXTRA AGENT D26 MULTI-AGENT AUDIT — 给 7B13 主会话之 background report (paper v9 + 60-75% inflate + Shumailov 牌面 之 3 binary question)]

**真实今日日期** (`date '+%F %T %Z'`): `2026-05-26 15:25:08 CST` (D26)

**Surface**: 额外 agent (来自 Win 端, 现 Linux 7B13 secondary session)
```

### §5.7 `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S1_S2_ATTEMPT1.md` (25180 B, S1+S2 子)

```
# MaoField Math Rigorous Proof D26 — Part S1+S2 ATTEMPT1

## §0 元数据 + binding ack

- agent: [额外 agent] (Win 端 spawn, Linux 7B13 secondary session, Opus 4.7 1M ctx)
```

### §5.8 `DIAGNOSE_D26_NAN_CASCADE_SAME_SOURCE_D23_20260526.md` (2022 B, diagnose)

```
# D26 NaN Cascade = D23 Phase 2 Same-Source Binary Verdict

**D26 11:35 sub-agent zero-context diagnose (7 分钟, 28 tool uses)**

## Binary Verdict
```

### §5.9 `WIN_D26_INTERNAL_REVIEW_REORG_13_58_20260526.md` (29064 B, Win review)

```
# WIN_D26_INTERNAL_REVIEW_REORG — Win 端 D23 reorganize 内部 review

## §0 metadata 标注

| 项 | 值 |
```

### §5.10 `docs/discipline/D-1-five-disciplines.md` (7260 B, cherry-pick 外置)

```
# D-1 五条纪律 (制度化常驻规则, 2026-05-15 加入)

> 从 MaoField/CLAUDE.md 外置 (D23 reorganize, D26 cherry-pick integrate)。CLAUDE.md 保留五条标题 + 自检 6 问的精简版 + link 本文件。

**来源**: 5/11-5/13 螺旋十三份子协作者报告浮现的"单通道自我评价向上漂移 (upward drift)"与 Shumailov 模型崩溃同构教训。
```

### §5.11 `docs/TIMELINE_D22_D60.md` (2699 B, cherry-pick 外置)

```
# D22-D60+ 实验时间表 (D-3.3 instantiate)

> 从 Win D23 reorganize 之 cherry-pick integrate (D26)。这是动态项目时间线, 不进 CLAUDE.md 每会话上下文。

## 第一阶段实践 (D22-D60)
```

### §5.12 `candidate_c/candidate_c_20260522_203837.jsonl` (328137 B, alive append)

```
首 line (D22 12:38 run_start):
{"ts": "2026-05-22T12:38:52Z", "event": "run_start", "seeds": [42, 1337, 2024, 7, 137, 271], "alphas": [0.0, 5.0, 10.0], "n_gens": 10, "device": "cuda", "pre_flight": false, "config_path": "/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/c...

末 line (D26 12:09 chain_gen_done, NaN cascade 持续):
{"ts": "2026-05-26T12:09:22Z", "event": "chain_gen_done", "seed": 271, "alpha": 10.0, "gen": 4, "a1_ppl": null, "a2_anisotropy": [NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN], "a3_attn_entropy": [[NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN...
```

---

## §6 跨机 sync gap surface (留主会话校验)

本子代理不擅 ssh / scp / git push, 故本节仅 surface 本机 D26 file 之 跨机 sync gap **候选 hypothesis** (留主会话 22 / Win 5060 binary 校验, 不擅 declare):

### §6.1 主机 22 (9070XT) 可能未 sync 之 D26 file 候选

| filename | hypothesis | 验证方式 (留主会话) |
|---|---|---|
| 全部 19 个 7B13 D26 工作 file (除 ack + jsonl) | 22 仅 git pull, 不 push, 故 ssh / sshfs 之外之 file 不知 sync 状态 | `ssh 22 ls /home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/ | grep D26` |
| `candidate_c_20260522_203837.jsonl` | 22 之 PID 491900 alive 写, **22 主源 7B13 mirror** (反向 sync 不需要) | `ssh 22 wc -l ...candidate_c_20260522_203837.jsonl` 之 比较 |

### §6.2 Win 5060 端可能未 sync 之 D26 file 候选

| filename | hypothesis | 验证方式 (留主会话) |
|---|---|---|
| 全部 20 个 dppl_bridge_verify_d21_output/*.md (除 Win 主导之 WIN_D26_*.md 2 file) | Win 端 scp 至 7B13 后, 7B13 反向 scp 至 Win 之 时机不明 | Win 端 ls `C:\Users\amd\...\MaoField\experiments\exp018_cat\dppl_bridge_verify_d21_output\` 之 二值列表 |
| `docs/discipline/D-1*.md` + `docs/discipline/D-2*.md` + `docs/TIMELINE*.md` + `CLAUDE.md` | git push `bc1b0b1` 之后 Win 端 git pull 之 时机不明 | Win 端 `git log --oneline -5` 含 `bc1b0b1` 二值 |

### §6.3 git push 之 时机 (留主会话 ack)

D26 commit `2e40736` (13:24) + `bc1b0b1` (14:22) 之 git push 至 origin 之 时机本子代理未 verify (find 抓 `.git/refs/remotes/origin/main` mtime 显 D26 修改, 但**不擅 declare** 推送成功 / push 之 destination 是 GitHub 还是 ssh remote)。

留主会话:
```bash
cd /home/amd/HEZIMENG/MaoField && git log origin/main..HEAD --oneline
git remote -v
```
binary 验证 push 状态。

---

## §7 不擅 declare 列 + metadata + 严守 binding final

### §7.1 本子代理不擅 declare 之 项

| 不擅 declare 项 | 留主会话 / PI / 其他角色 |
|---|---|
| jsonl D26 24 line append 是 NaN 持续 还是部分 valid 之 valid ratio binary | 留主会话之 jsonl 统计 sub-agent + PI 决 |
| `candidate_c_20260522_203837.jsonl` 之 22 主源 vs 7B13 mirror sync 方向 | 留主会话 ssh 22 校验 |
| ATTEMPT1 main 之 paper-level / framework / paradigm 之 substantive verdict | 留 PI + 反题三方决 + DS + Win 哲学协作 (D-3.7 PI 主权严守) |
| EXTRA_AGENT_D26_MULTI_AGENT_AUDIT 之 3 binary question 之 verdict | 留 7B13 主 + PI + 关卡 3 反题三方决 |
| Win 内部 review 之 cherry-pick 是否 100% 集成 / 落 substantive value 是否充分 | 留 7B13 主 + Win cross-confirm |
| paper v8 final 47/47 manifest 之 D26 变动 (本 inventory verify: 0 个 paper file D26 新增 OR 修改) | 严守 binding ack ✓ paper v8 final 不动 |

### §7.2 inventory metadata

| 项 | 值 |
|---|---|
| inventory 之 produce time | 2026-05-26 20:22 CST → 20:32 CST (~10 分钟) |
| inventory 之 工具 chain | `find -newermt 00:00 ! -newermt 27 00:00` + `stat -c %Y\|%y\|%s` + `sha256sum` + `head -5` + `grep` |
| inventory 之 method discipline | D-1 纪律 1 占位符禁令 严守 (全部 25 entry 实有 file path) / D-1 纪律 5 错误浮现 严守 (mtime burst 阶段 9 阶段 A-I 真实记录) / D-3 反映论 retrospective 之 第八通道 inventory 形式 |
| inventory 之 不动 file | 不 read 不 modify 除本 inventory 之外任何 file (D26 NEW 25 file 全部 read-only access, sha256 / head 不改 source) |
| inventory 之 不擅 ssh | 本机 path only, 跨机 22 / Win 5060 sync gap 仅 surface hypothesis 不 verify |

### §7.3 严守 binding final

- ✓ paper v8 final 47/47 manifest + 12 NOT-claim retract + 反题 6 P0★ + D29 三 leg (arXiv + TMLR + KBS) **全严守不动**
- ✓ D-1 五条纪律 + D-1 纪律 5 sub-rule (真实日期 `date` binary verify ✓ 2026-05-26 20:22 CST)
- ✓ D-3 反映论 retrospective form 严守 (inventory 是 retrospective 第八通道, 不 declare paradigm shift)
- ✓ 中文 + 4 类英文豁免 + 不堆 "之" 字 padding (本 inventory 之 "之" 字 密度 控制, 数学 / 哲学 style 不堆叠)
- ✓ [额外 agent] head + footer attribution 严守
- ✓ 单点写权 7B13 main session, 本子代理仅 inventory file write (不 commit / push / 改其他 file)
- ✓ multi-agent 协调诚实 ≠ PI 个体诚实 (D-3.2.6) → 本 inventory 仅事实陈述, 不替代 PI 决 / 反题三方决 / DS 跨哲学 / Win 哲学协作

---

[额外 agent] inventory 结束。
留主会话:
1. 跨机 sync gap 之 22 / Win 5060 ssh 校验
2. `git log origin/main..HEAD` push 状态 binary 校验
3. ATTEMPT1 6 main + S1-S5 sub 4 file 之 substantive value 之 PI + 反题三方决
4. jsonl D26 24 line append 之 valid ratio binary 统计
