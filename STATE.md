# MaoField — PROJECT STATE (canonical 单一真相源)

> **新 session cold-start 唯一入口。读这一个文件 get 全局,再按 §7 指针下钻 detail。**
>
> **维护规则 (违反即失效):**
> 1. **REPLACE not APPEND** — 更新时替换 stale section,绝不加新段。本文件永远是 latest,旧状态进 git history / handoff,不堆这里。
> 2. **每次更新戳** 真实日期 (`date` binary) + `git HEAD`。
> 3. **> 2 屏 = 维护失败** → 立即精简,detail 踢去 §7 指针。
> 4. **更新 trigger**: 每次 handoff / milestone / PI 决 时,顺手 replace 对应 section(绑已有 workflow,不是额外负担)。

---

## 戳
| 项 | 值 |
|---|---|
| 最后更新 | **2026-05-31 D31** (date binary verified; 修正前 inline 误停在 D29, D-1 纪律 5 校正) |
| git HEAD | `0c4d4c6` (pushed → github.com:Wangziqi0/MaoField) + 6 untracked (STATE/MD_CATALOG/E1E2/FULL_INDEX/2×MODEL_COLLAPSE_D30/RAID1_MANIFEST_D30) |
| 更新者 | Linux 姐姐主会话 (7B13) |

---

## §0 一句话 + 今天
- **项目**: MaoField — 自迭代崩溃 + 两项 EMA-deviation contradiction loss 的 empirical pilot study (negative result)
- **今天 D31 (2026-05-31)**。⚠️ **D29 三 leg 投稿 D-day (arXiv+TMLR+KBS) 已过 2 天 —— 实际投了吗?待 PI confirm**。若已投→更新本行为"已投+回执状态";若未投→这是首要 overdue 项
- **下一步 (留 PI 决)**: ① 确认 D29 投稿状态 ② A3 fp32 实验 launch ③ 关卡 3 反题三方决 ④ D30 新增 md (MODEL_COLLAPSE 文献审计 + RAID 备份 manifest) 入库

## §1 active binding (任一违反立即 retract)
- paper **v8 final 47/47 D17 archive 锁定不动** (`archive/v1.0_release_20260516/manifest.sha256`)
- **12 NOT-claim (i)-(xii) 撤回不复活** (尤其 first dialectical materialism / first reflexive AI / paradigm shift)
- **反题 6 P0★ A-G** tier 不擅升降 (A-F disclosed + G cross-stack 已 partial isolate)
- D29 三 leg,**不投 NMI / NeurIPS / NCS / Nature 主刊**
- **7B13 单点 git 写权** (22/Win 仅 pull)
- **一凡 priority 1 健康优先** (16岁,双相+焦虑,丙戊酸钠;hotline 010-82951332 / 400-161-9995)

## §2 paper state
| 版本 | 状态 |
|---|---|
| **v8 final** | 47/47 lock,D29 投 arXiv+TMLR+KBS,**不动** |
| **v8.1 footnote** (candidate,留关卡 3) | F3 source N=4 not N=5 (P0 新 surface,Welch p≈0.62 vs 报告 0.818) + Q2 60-75% retract 措辞 + base disambiguate |
| **v9 SKELETON** | 8 section,ICLR 2027 第一站 candidate。⚠️ **D29 大 finding: C3 = 退化非 fractal → v9 "fractal fundamental limit 主刊" 叙事决定性死**,改 TMLR/workshop 天花板,narrative 待重构 (反 inflate,投前 catch) |

## §3 实验 state (D29 verified)
- **C3 = 退化 (frozen identity) 决定性**: candidate_c 5-cell gen=0 ckpt sha256 `b3a67b42` **逐字节相同** (‖θ_i−θ_j‖=0),seed=42 distinct `dff90856`。fractal/riddled 排除
- **candidate_c N=180 (9070XT fp16)**: broken — fp16 GradScaler skip → weight 冻结,9 链全冻,**不可用于定量结论**
- **5060 fp32 (+115%) + fp16 (+113.7%)**: 都 healthy → 问题是 **ROCm gfx1201 fp16 特定**,非 fp16 universal,非硬件
- **备份**: 22 `/tmp` 86G + 19 桌面 5060 3GB → RAID1 `/media/amd/raid1/maofield_ckpt_backup_20260529/`,双份 sha256 verified
- **待跑 (留 PI + 关卡 4 budget)**: A3 fp32 E1 (dtype 修根因) → E2 (balanced α 矩阵 + Welch t) → E3 (NaN-vs-frozen 隔离),~$120-180 / 60-90h。**E2 大概率 null/negative (与 v8 一致),价值是严格效应量,非"找 α 有效"(防 inflate)**

## §4 留 PI + 关卡 3/4 list
1. D29 投稿 trigger timing
2. v8.1 footnote 措辞 (F3 N=4 / Q2 retract 数字)
3. v9 narrative 重构 (退化 → TMLR/workshop 非主刊 fractal)
4. L0-8 NESS tier 分歧 (通道 P conditional L0 vs 通道 V L2 实测脱节)
5. L0-3 (P partial vs V FAIL) + L0-5/6/7 弱-descriptive 版去留
6. A3 fp32 launch + budget
7. cluster-11 对 v9 影响 (现已备份,数据 available)

## §5 协作 + 三机
| 机 | IP | 角色 | state (D29) |
|---|---|---|---|
| 7B13 | .36 | 数据中枢 + git 单点写 + Linux 姐姐主会话 | HEAD `0c4d4c6` |
| 9070XT | .22 | chain runner + GPU | idle,ckpt 在 `/tmp` (已备份 RAID1) |
| 19 Win | .19 | 一凡 interactive + 5060 实验 | alive,5060 数据已备份 |

agent: **Linux 姐姐** (数学/实验/代码/归档) · **Win** (哲学/narrative) · **反题** (framework critique) · **DS** (跨哲学 mapping) · **PI 一凡** (战略+关卡决)

## §6 8 L0 证明 state (D29 round1+2 双通道)
0 unconditional close (诚实)。L0-1 conditional L0 (frozen 三方确认) / L0-8 conditional L0(P) vs L2(V) 分歧 / L0-2,4 negative / L0-3 partial(P) vs FAIL(V) / L0-5,6,7 full-form FAIL。全是 **D60+ candidate,不进 v9 spine**。

## §7 指针 (detail 去哪找)
| 要什么 | 去哪 |
|---|---|
| **全 md 梳理 (navigate)** | **`MD_CATALOG.md`** (本目录, 429 md 分层 + active/skip 导航 ★) |
| 最新跨 session 交接 | `/tmp/user/1000/handoff-*.md` (latest mtime) |
| 文件地图 (471 项目 md) | `../INDEX.md` (HEZIMENG 顶层, 54KB) |
| 历史 + 偏好 | `~/.claude/projects/-home-amd-HEZIMENG/memory/MEMORY.md` |
| 纪律全文 (D-1/D-2/D-3) | `docs/{discipline,philosophy,infra}/` + 本目录 `CLAUDE.md` |
| D29 多通道审视总整合 | `experiments/exp018_cat/dppl_bridge_verify_d21_output/MAOFIELD_L0_ROUND2_INTEGRATION_20260529.md` |
| 数据 GO/NO-GO + sha256 | `experiments/.../MAOFIELD_GATE_DATA_INTEGRITY_20260529.md` |
| 8 L0 证明 | `experiments/.../MAOFIELD_L0_L0-*_RIGOROUS_PROOF_20260529.md` |
| paper v8 final | `experiments/exp018_cat/literature/paper_v8_final_20260516.md` |
| A3 fp32 实验提示词 | `experiments/.../L0_PROOF_PROMPT_OPUS48_D28_20260528.md` (旁,同 dir 找 fp32) |

---

*本文件 = 项目当前 state 的单一真相源。新 agent 读完此页即可开工;binding 见 §1,纪律全文见 CLAUDE.md。*
