# MaoField 全项目 file 全局索引 — D26 latest (2026-05-26 周二)

## §0 元数据

- **生成时点**: 2026-05-26 20:30 CST (D26 周二), 真实日期 `date '+%Y-%m-%d %H:%M:%S %Z'` 二值 verify ✓
- **生成 agent**: [额外 agent] 队列之独立 zero-context 全局 file 索引子代理 (Opus 4.7, D-3 反映论第八通道 C 之子, D25 21:55 一凡 explicit binding)
- **scope**: `/home/amd/HEZIMENG/MaoField/` 全项目 全 file (除 `.git/` 排除)
- **任务性质**: 仅 inventory, 不深读 file content, 不做 content digest (Read 限 ≤ 5 次 top-level README head 5 行)
- **严守 binding ack**:
  - paper v8 final 47/47 manifest + 12 NOT-claim 撤回 + 反题 6 P0★ + D29 venue (arXiv + TMLR + KBS) 不动 ✓
  - 中文 + 4 类英文豁免 (代码标识符 / 协议名 / 错误信息 / CLI / 业界缩写) ✓
  - [额外 agent] head + footer attribution 严守 ✓
  - 不擅 ssh / git commit/push / 删除 / 改任何 file ✓
  - ATTEMPT1, 不一次定论 ✓

---

## §1 全项目 file 总览

### §1.1 总量

| 项 | 数 |
|---|---|
| 总 file 数 (不含 `.git/`) | **6523** |
| 总 size (不含 `.git/`) | **9.3 GB** (含 `.git/` 9.6 GB, `.git/` ~289 MB) |
| 非 rust/cache dir 数 | 122 |

### §1.2 Extension 分布 (top 25, 排除 .git)

| 扩展名 | count | 说明 |
|---|---|---|
| `.json` | 1011 | 大部分是 rust target/cache + 实验结果 (exp003-017 各历史结果集) |
| `.timestamp` | 757 | rust cargo build timestamp 缓存 |
| `.d` | 622 | rust dep tracker 文件 |
| `.rmeta` | 394 | rust 编译元数据 |
| `.rlib` | 381 | rust 编译库 |
| **`.md`** | **370** | **markdown 文档 (核心 trace + paper + audit + research)** |
| `.py` | 122 | python script (exp 各 src/scripts) |
| `.rs` | 95 | rust 源码 (exp006-017 rust_variants/rust_solver) |
| `.log` | 89 | 实验 / install / 构建 日志 |
| `.bin` | 57 | rust binary + svd projection 等 |
| **`.jsonl`** | **52** | **chain 实验 metrics (D-1 第一纪律 jsonl source binary trace)** |
| `.npz` | 48 | numpy 压缩 (中间结果) |
| `.txt` | 38 | 杂项文本 |
| `.pyc` | 22 | python 编译缓存 |
| `.png` | 22 | figure / 可视化 |
| `.so` | 19 | rust 共享库 |
| `.csv` | 19 | 实验数据表 |
| `.toml` | 18 | Cargo.toml (8 cargo projects in exp017 rust_variants) |
| `.lock` | 18 | Cargo.lock + Pipfile.lock 等 |
| `.sqlite` | 17 | exp010-013 query evolution sqlite 缓存 |
| `.cargo-lock` | 17 | cargo build 锁 |
| `.TAG` | 17 | cargo build TAG |
| `.yaml` | 15 | configs (exp018_cat 主要) |
| `.sh` | 14 | shell 脚本 (exp017 主要) |
| `.gitignore` | 12 | 各 dir 之 .gitignore |
| `.bak` | 6 | rust 源码备份 (exp015/016/017) |

### §1.3 关键 single file (top-level)

| file | size | mtime |
|---|---|---|
| `CITATION.cff` | 2.4 KB | 04-18 |
| `LICENSE` | 11 KB | 04-18 |
| `NOTICE` | 1.1 KB | 04-18 |
| `NOTICE.md` | 2.9 KB | 04-15 |
| `README.md` | 9.3 KB | 04-18 |
| `README_zh.md` | 8.2 KB | 04-18 |
| `CLAUDE.md` | 10 KB | 05-26 ← latest update D26 |
| `DESKTOP_MATH_DEEP_ANALYSIS_20260419.md` | 67 KB | 04-19 (P0 大 stale 候选, > 30 天) |
| `DESKTOP_SPOTCHECK_*_20260419.md` (×4) | 5.5-17 KB | 04-19 (D-19 同 stale 候选) |

---

## §2 顶层结构 tree (depth 4, dir-only)

```
MaoField/
├── CITATION.cff / LICENSE / NOTICE / NOTICE.md / README.md / README_zh.md / CLAUDE.md
├── DESKTOP_*_20260419.md  (× 5, D19 历史, stale)
├── data/                 (8 KB, 1 README only)
├── docs/                 (64 KB, D-1/D-2/D-3 + 三机)
│   ├── README.md
│   ├── TIMELINE_D22_D60.md
│   ├── discipline/
│   │   ├── D-1-five-disciplines.md (7.3 KB)
│   │   └── D-2-parallel.md         (2.1 KB)
│   ├── infra/
│   │   └── three-machine-architecture.md (6.2 KB)
│   └── philosophy/
│       └── D-3-dialectical-reflection.md (19 KB) ← D-3 反映论标准形式
├── experiments/          (9.3 GB ← 主 payload)
│   ├── exp003_law_structure/  (23 MB, 04-12 历史)
│   ├── exp004/                (2.7 MB, 04-12 历史)
│   ├── exp005/                (444 KB, 04-12 历史)
│   ├── exp006/                (102 MB, 04-12 历史 rust_solver)
│   ├── exp007/                (81 MB, 04-12 历史)
│   ├── exp007_rust/           (81 MB, 04-12 历史)
│   ├── exp008/                (87 MB, 04-12 历史)
│   ├── exp011/                (85 MB, 04-12 历史 复数场)
│   ├── exp015/                (103 MB, 04-12 历史 NFCorpus -12pp)
│   ├── exp016_diagnostic/     (268 MB, 04-12 诊断转向 reranker)
│   ├── exp017_dialectics/     (1.7 GB ← Shape-CFD/MaoField 04-13~05-07 主仓)
│   │   ├── action3_wavefront/ (400 KB)
│   │   ├── inputs/            (2.2 MB)
│   │   ├── inputs_block1/     (144 MB, top-20 BEIR 输入)
│   │   ├── inputs_block1_top20/ (31 MB)
│   │   ├── logs/              (796 KB)
│   │   ├── results/           (1.1 GB, 157 md ← 历史 milestone 主仓)
│   │   ├── rust_variants/     (473 MB, 8 cargo projects, 34 .rs)
│   │   ├── scripts/           (52 KB)
│   │   └── src/               (132 KB)
│   └── exp018_cat/            (992 MB ← D7-D26 主仓, CAT + D-PPL)
│       ├── README.md / SHUMAILOV_REPLICATION_README.md
│       ├── analysis_20260513/ (104 KB)
│       ├── archive/v1.0_release_20260516/ (500 KB, 48 file, manifest.sha256 在此)
│       ├── configs/           (120 KB, 9 yaml + 2 .backup)
│       ├── data/              (4 KB, placeholder)
│       ├── dppl_bridge_verify_d21_output/ (973 MB ← D21-D26 主战场)
│       │   ├── 90 file at root (77 md + 4 jsonl + 7 log + 2 dir)
│       │   ├── candidate_c/   (360 KB, 9 progress_snapshot + 1 jsonl)
│       │   ├── candidate_c_preflight/ (965 MB ← model checkpoints 主体积来源, 19 file)
│       │   └── main/          (280 KB, main_D22.{log,jsonl,nohup.log} + watchdog)
│       ├── figures/           (168 KB, 1 png)
│       ├── literature/        (3.7 MB, 78 md ← paper v2-v8 + 反题 audit + 数学 + 哲学 主仓)
│       ├── logs/              (15 MB, 59 file)
│       ├── results/           (8 KB, 1 file)
│       ├── scripts/           (448 KB)
│       └── src/               (152 KB)
├── paper/                (8 KB, 1 README placeholder)
├── proposed_v0.1.1/      (28 KB, CITATION.cff.proposed + README.md.proposed + DIFF_SUMMARY)
├── scripts/              (8 KB, 1 README placeholder)
├── sessions/             (152 KB)
│   └── domain_positioning/ (11 md, Nature 投递准备, 05-14)
├── src/                  (8 KB, 1 README placeholder)
└── .git/                 (289 MB ← 排除 scope)
```

---

## §3 全 directory 详细 file count + size + active/stale split

### §3.1 顶层 dir 概览

| dir | size | file count | active 7d | stale > 30d | 说明 |
|---|---|---|---|---|---|
| `data/` | 8 KB | 1 | 0 | 1 | placeholder, 仅 README |
| `docs/` | 64 KB | 6 | 4 | 0 | D-1/D-2/D-3 + 三机 + TIMELINE, D23 reorganize cherry-pick |
| `experiments/` | 9.3 GB | ~6400 | ~110 md | ~150 md | 主 payload |
| `paper/` | 8 KB | 1 | 0 | 1 | placeholder |
| `proposed_v0.1.1/` | 28 KB | 3 | 0 | 3 | 04-18 v0.1.1 proposed (CITATION + README + DIFF), stale |
| `scripts/` | 8 KB | 1 | 0 | 1 | placeholder |
| `sessions/` | 152 KB | 11 | 0 | 11 | 05-14 Nature 投递准备子目录 |
| `src/` | 8 KB | 1 | 0 | 1 | placeholder |

### §3.2 experiments/exp018_cat/literature/ (78 md, ~3.7 MB)

paper v2-v8 + 反题 audit + 数学/哲学 layer + research search 全部仓库:

- **paper version 链**: `paper_v2_20260515.md` / `paper_v3_20260517.md` / `paper_v4_20260518.md` / `paper_v5_20260518.md` / `paper_v6_20260518.md` / **`paper_v8_final_20260516.md` ← 47/47 manifest final lock**
- **反题 audit 链** (5 版): `ANTITHESIS_LAYER_PAPER_V2_AUDIT_20260515.md` → V3/V4/V5/V6/**V8_FINAL** (5/16)
- **narrative layer** (Win 写): V2/V3/V4/V5/V6/V8_FINAL 6 版对应
- **research 4 份 D19**: `RESEARCH_ACADEMIC_RECENT_PROGRESS` / `LENIN_MAO_COMPREHENSIVE` / `MARXIST_DEEPEN` / `MARX_ENGELS_PHIL_METHOD`
- **D17 三波数学/哲学**: `MATH_LINE_D17_THIRD_WAVE` + `WIN_PHIL_LINE_D17` ×3
- **D-PPL bridge D21 prompt**: `DPPL_BRIDGE_9070XT_PROMPT_D21_20260521.md` / `DPPL_BRIDGE_MATH_VERIFY_D21_20260521.md` / `DPPL_BRIDGE_VERIFY_EXPERIMENT_DESIGN_BRIEF_D21_20260521.md`
- **D20 secondary verify**: `SECONDARY_VERIFY_D20_MAOFIELD_DETAIL_STATE` / `SECONDARY_VERIFY_D20_THREE_MACHINE_CONFIG_SYNC`
- active 7d: 0; active 30d: ~78 (全部, 5/7-5/21 区间); stale > 30d: 0

### §3.3 experiments/exp018_cat/dppl_bridge_verify_d21_output/ (973 MB ← D21-D26 主战场)

**Root level**: 90 file (77 md + 4 jsonl + 7 log + 2 dir + 其他)

- **active 3 天 (5/24-5/26)**: 44 md ← D24/D25/D26 集中 burst
- **active 7 天 (5/20-5/26)**: 76 md ← D21-D26 几乎全部
- total: 77 md (1 个 candidate_c 子 dir 之 progress_snapshot 不计 root)

**D26 新增 ATTEMPT1 main file** (cross-ref Sub A inventory):

| file | size | mtime | 说明 |
|---|---|---|---|
| `MAOFIELD_LITERATURE_SEARCH_D26_ATTEMPT1.md` | 51 KB | 5/26 18:10 | 文献搜索通道 |
| `MAOFIELD_MATH_MULTI_CHANNEL_ANALYSIS_D26_ATTEMPT1.md` | 46 KB | 5/26 17:57 | 数学多通道 |
| `MAOFIELD_MULTI_CHANNEL_ANALYSIS_D26_ATTEMPT1.md` | 38 KB | 5/26 17:24 | 综合多通道 |
| `MAOFIELD_MATH_RIGOROUS_PROOF_D26_ATTEMPT1.md` | 18 KB | 5/26 19:54 | 严格证明 main |
| `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S1_S2_ATTEMPT1.md` | 25 KB | 5/26 19:47 | S1+S2 部分 |
| `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S3_ATTEMPT1.md` | 26 KB | 5/26 19:48 | S3 部分 |
| `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S4_ATTEMPT1.md` | 26 KB | 5/26 19:48 | S4 部分 |
| `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S5_ATTEMPT1.md` | 17 KB | 5/26 19:51 | S5 部分 |
| `MAOFIELD_FULL_DATA_AUDIT_20260526.md` | 49 KB | 5/26 16:55 | 数据 audit |

**D26 其他 file** (8 个):
- `ACK_D26_22_END_WAKE_SYNC_D26_11_49_20260526.md` (11 KB, 11:50, D26 wake sync ack)
- `SYNC_D26_5060_WAKE_TRANSFORMERS_FIX_BINARY_ACK_20260526.md` (4.5 KB, 11:50)
- `WIN_D26_WAKE_SYNC_ACK_11_50_20260526.md` (5.8 KB, 11:51)
- `DIAGNOSE_D26_NAN_CASCADE_SAME_SOURCE_D23_20260526.md` (2.0 KB, 13:28, NaN cascade verdict)
- `WIN_D26_INTERNAL_REVIEW_REORG_13_58_20260526.md` (29 KB, 14:03)
- `EXTRA_AGENT_D26_MULTI_AGENT_AUDIT_FOR_7B13_MAIN_20260526.md` (27 KB, 15:28)
- `EXP_PLAN_LATEST_D26.md` (17 KB, 15:59)
- `MATH_DIRECTION_LATEST_D26.md` (21 KB, 15:59)
- `MD_INDEX_LATEST_D26.md` (24 KB, 16:01)
- `PHILO_DIRECTION_LATEST_D26.md` (mtime 5/26)
- `DEEPER_INSIGHT_D26_CONVERSATION_20260526.md` (8.5 KB, 19:10)

**Jsonl chain (root + sub)**:
- `pilot_D21_seed1_gen5.jsonl` (root, 4 KB, D21 pilot)
- `candidate_c_20260524_173559.jsonl` (root, 8 KB, D24 5060 launch)
- `candidate_c_20260525_113506.jsonl` (root, 8 KB, D25 cell B)
- `candidate_c_20260525_160321.jsonl` (root, 8 KB, D25 resume)
- `candidate_c/candidate_c_20260522_203837.jsonl` (D22 main run, sub-dir 主 jsonl)
- `candidate_c_preflight/candidate_c_20260522_203111.jsonl` (D22 preflight, 8 KB)
- `main/main_D22.jsonl` (D22 main run, 主 chain) + `main/watchdog.audit.jsonl` (audit watchdog)

**Log files**:
- `candidate_c.nohup.log` (**5.2 MB ← root 最大 log**, D22-D26 持续 nohup)
- `install_rocm_torch.log` / `install_rocm_torch_fixed.log` (20 KB) / `install_rocm_torch_rocm72.log` / `install_trace.log` (D21 install)
- `pilot_D21.console.log` / `pilot_D21.log` (D21 pilot)
- `main/main_D22.log` / `main/main_D22.nohup.log` (D22 main run)

**Sub-dir 之 structure**:
- `candidate_c/` (360 KB): 9 progress_snapshot_{10,20,30,40,50,60,70,80}.md + 1 jsonl
- `candidate_c_preflight/` (**965 MB ← 主体积**): 19 file, 主要是 `checkpoints/alpha10.0/no_preserve_seed42/generation_{0,1}/model.safetensors` (×2 大 binary)
- `main/` (280 KB): main_D22.log / main_D22.jsonl / main_D22.nohup.log / watchdog.audit.jsonl

### §3.4 experiments/exp017_dialectics/results/ (157 md, 1.1 GB 含其他, results md ~ 1-2 MB)

Shape-CFD 历史 + MaoField paradigm 04-13~05-07 主仓:

- **arxiv v1 全套 (04-14 burst)**: `arxiv_v1_full.md` / `arxiv_v1_abstract.md` / `arxiv_v1_section{1,2_1_2_2,2_3,3,4,5,6}_DRAFT.md` / `arxiv_v1_references_DRAFT.bib` / REVIEW_ARXIV_*7 版
- **paradigm β→δ 04-20 / L1++ 04-27**: `WIN_PARADIGM_L1_PLUS_PLUS_REVERSE_CONTRIBUTION_20260427.md` 等
- **04-19 三方 cycle**: `ANTITHESIS_RUN3_20260419.md` / `LINUX_04_20_MEETING_PACK_20260419.md` / `EXTERNAL_AGENT_REVIEWS_20260419.md`
- **04-24~04-30 反题 run4**: `ANTITHESIS_RUN4_{PRELIMINARY,FORMAL,AUDIT_UPDATE_V1}_20260424.md` + `ANTITHESIS_REVERSE_AUDIT_FINAL_20260430_LOCK.md` + `ANTITHESIS_FSD3_VERDICT_20260429.md`
- **DS v4 04-26**: `DEEPSEEK_V4_{CROSS_TRADITION_UNPACK,NAMBU_FIRST_IMPRESSION,TERM_AUDIT_ROUND1}_20260426.md`
- **04-18 ACTION**: `ACTION1_CUSHION_INVENTORY` / `ACTION2_M3_EMPIRICAL_VERIFY` / `ACTION3_P3_WAVEFRONT_TILT`
- **04-25/26**: `LINUX_ACK_*` / `WIN_*` / `INDEPENDENT_AGENT_SIGMA_VERIFY` 等
- **04-16 deep**: `A1_M3_V0_SELFCONSISTENT` / `A2_P3_KRAMERS_INSTANTON` / `A3_DEEP_NOTE_THEORY_REVIEW` / `A4_P1_PERCOLATION_SCAN_DESIGN` / `A5_ANTITHESIS_SECOND_RUN` / `DEEP_REASONING_TF_LIMITS_AGI_PATH` / **`RECOVERY_SNAPSHOT_20260416.md`** + `RECOVERY_SNAPSHOT_20260414.md` / `RECOVERY_SNAPSHOT_20260413.md` (3 个)
- **block1-V design**: `BLOCK_V_DESIGN.md` / `block1_final_report.md` / `block1_summary.md` / `block2_gc_findings.md` / `block3_summary.md` / `block4` / `block4_5` / `lawvere_monad_draft.md` / `open_problems_followup.md` / `phase_b_exp1` / `zn_angular_potential_math.md`
- active 30d: 21 (5/7-5/11 paper first-principles rewrite + 三方 verdict 等)
- stale > 30d: 136 (4/12-4/30 burst 主体)

### §3.5 experiments/exp003-exp016_diagnostic/ (历史 exp, 全 stale)

| dir | size | md count | active | 说明 |
|---|---|---|---|---|
| exp003_law_structure | 23 MB | 0 (1 README) | 0 | 04-12 法律结构, json/sqlite 主体 |
| exp004 | 2.7 MB | 8 | 0 | 04-12 weighted Chamfer / NMF |
| exp005 | 444 KB | 0 | 0 | 04-12 NMF |
| exp006 | 102 MB | 0 | 0 | 04-12 rust_solver + NMF atoms |
| exp007 / exp007_rust | 81+81 MB | 0 | 0 | 04-12 SVD atoms |
| exp008 | 87 MB | 0 | 0 | 04-12 SVD Chamfer |
| exp011 | 85 MB | 0 | 0 | 04-12 复数场, residual evolution |
| exp015 | 103 MB | 0 | 0 | 04-12 NFCorpus -12pp 死结 |
| exp016_diagnostic | 268 MB | 6 | 0 | 04-12 诊断转向 reranker (phase1-6 summary + REPORT) |

### §3.6 experiments/exp018_cat/ 顶层 + 子 dir (除已 detail 之 literature + d21_output)

| sub-dir | size | file count | 说明 |
|---|---|---|---|
| analysis_20260513/ | 104 KB | ~5 | full_analysis + full_analysis_v2 + extract_all py |
| archive/v1.0_release_20260516/ | 500 KB | 48 | manifest.sha256 + RELEASE_NOTES + configs + scripts + src + chain_logs |
| configs/ | 120 KB | 9 | shumailov_baseline.yaml / cat_arm_b.yaml + .backup ×2 |
| data/ | 4 KB | 0 | placeholder |
| figures/ | 168 KB | 1 | `collapse_curve_strict_vs_partial.png` |
| logs/ | 15 MB | 59 | armb_alpha{0,1,5,10,50}_seed{42,1337}.jsonl + baseline log + sanity_check json/log + host22_backup_20260512 |
| results/ | 8 KB | 1 | placeholder-ish |
| scripts/ | 448 KB | ~25 | partial_D4_shape_verdict / m_eff_direct_fit / sliding_window_eval / yaml_setup_hash / sanity_check_* |
| src/ | 152 KB | ~15 | contradiction_loss.py / multi_layer_hook / shumailov_replication / data_pipeline / config / metrics / train_one_generation / cat_trainer / generate_synthetic / run_arm_b_alpha_scan + .backup |
| **D-PPL bridge** scripts subdir | - | (含 __pycache__) | exp018_cat/scripts/dppl_bridge_verify/ |

### §3.7 sessions/domain_positioning/ (11 md, 152 KB, 全 stale 30+d)

05-14 Nature 投递准备 子目录:
- `README.md`
- `PART1_DIAGNOSIS_MECHANICAL_MATERIALISM.md`
- `PART2_ALTERNATIVE_DIALECTICAL.md`
- `PART3_NATURE_POSITIONING.md`
- `PART4_DOMAIN_LEADERSHIP.md`
- `PART5_SUBAGENT_TASKS.md`
- `PART6_ANCHORS_TIMELINE.md`
- `WIN_NATURE_NARRATIVE_DRAFT.md`
- `DEEPSEEK_CROSS_PHILOSOPHY_AUDIT.md`
- `ANTITHESIS_NATURE_AUDIT.md` (37 KB, 较大)
- `MATH_SECTION_DRAFT.md`

**注**: D17 5/17 投稿决策 lock 后, 不投 NMI / NCS / NeurIPS, 改 arXiv + TMLR + KBS 三 leg, 此目录 substantively stale (但保留作历史 trace, 不删).

### §3.8 docs/ (D23 reorganize cherry-pick, 6 file, 64 KB)

| file | size | mtime |
|---|---|---|
| `README.md` | - | 05-26 D26 update |
| `TIMELINE_D22_D60.md` | - | D22-D60 timeline 主 |
| `discipline/D-1-five-disciplines.md` | 7.3 KB | 05-26 D26 update |
| `discipline/D-2-parallel.md` | 2.1 KB | 05-26 D26 |
| `infra/three-machine-architecture.md` | 6.2 KB | 05-23 D23 |
| `philosophy/D-3-dialectical-reflection.md` | 19 KB | 05-23 D23 ← D-3 反映论标准形式主源 |

---

## §4 D26 之 9 个 ATTEMPT1 main file (cross-ref Sub A inventory)

D26 (2026-05-26) 单日 burst 新增 ATTEMPT1 main file, 全部位于 `experiments/exp018_cat/dppl_bridge_verify_d21_output/`:

| 序 | file | size | mtime |
|---|---|---|---|
| 1 | `MAOFIELD_LITERATURE_SEARCH_D26_ATTEMPT1.md` | 51 KB | 5/26 18:10 |
| 2 | `MAOFIELD_MATH_MULTI_CHANNEL_ANALYSIS_D26_ATTEMPT1.md` | 46 KB | 5/26 17:57 |
| 3 | `MAOFIELD_MULTI_CHANNEL_ANALYSIS_D26_ATTEMPT1.md` | 38 KB | 5/26 17:24 |
| 4 | `MAOFIELD_MATH_RIGOROUS_PROOF_D26_ATTEMPT1.md` | 18 KB | 5/26 19:54 |
| 5 | `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S1_S2_ATTEMPT1.md` | 25 KB | 5/26 19:47 |
| 6 | `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S3_ATTEMPT1.md` | 26 KB | 5/26 19:48 |
| 7 | `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S4_ATTEMPT1.md` | 26 KB | 5/26 19:48 |
| 8 | `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S5_ATTEMPT1.md` | 17 KB | 5/26 19:51 |
| 9 | `MAOFIELD_FULL_DATA_AUDIT_20260526.md` | 49 KB | 5/26 16:55 |

ATTEMPT1 总 size: ~296 KB, 全部 D26 单日 produced (16:55 → 19:54 时间窗 ~3h burst, 9 file).

ATTEMPT1 binding: 不一次定论, 是 ATTEMPT1 第一次 attempt 性 deliverable, 等关卡 3 反题三方决 final.

---

## §5 关键历史 milestone file 之 quick reference

### §5.1 Paper 主 version 链

- **paper v8 final** (D17 5/17 final lock): `experiments/exp018_cat/literature/paper_v8_final_20260516.md`
- **paper v6 emergency fix**: `experiments/exp018_cat/literature/paper_v6_20260518.md` 之 NARRATIVE_LAYER 对应
- **paper v3 base**: `experiments/exp018_cat/literature/paper_v3_20260517.md`
- **paper v2 first draft**: `experiments/exp018_cat/literature/paper_v2_20260515.md`
- **paper v9 draft candidate D25**: `experiments/exp018_cat/dppl_bridge_verify_d21_output/PAPER_V9_DRAFT_CANDIDATE_D25_17_52_20260525.md` (留 D26-D27 关卡 3 三方决, 不一次定论)

### §5.2 Archive manifest (v1.0 release D16 5/16)

- `experiments/exp018_cat/archive/v1.0_release_20260516/manifest.sha256` (47/47 文件 hash)
- `experiments/exp018_cat/archive/v1.0_release_20260516/RELEASE_NOTES.md`
- `experiments/exp018_cat/archive/v1.0_release_20260516/README.md`

### §5.3 RECOVERY_SNAPSHOT (3 个)

- `experiments/exp017_dialectics/results/RECOVERY_SNAPSHOT_20260416.md` (P3 Kramers + M1/M3/M5/M6/M7 menu, 04-16 max effort)
- `experiments/exp017_dialectics/results/RECOVERY_SNAPSHOT_20260414.md` (04-14 arXiv v1 first draft + 27 errors snapshot)
- `experiments/exp017_dialectics/results/RECOVERY_SNAPSHOT_20260413.md` (04-13 Phase 1 前)

### §5.4 HANDOFF / HANDOVER

- `experiments/exp018_cat/dppl_bridge_verify_d21_output/HANDOFF_D24_TO_5060_20260524.md` (D24 9070→5060 跨机交接)
- HEZIMENG 根: `HANDOVER_20260418.md` (04-18 desktop 跨 session) / `HANDOVER_20260420.md` (04-20 跨 session 接续) / `HANDOVER_20260426.md` (04-26 7 binding 同步)

### §5.5 D17-D26 关键 single-day burst file

| 日 | file | 说明 |
|---|---|---|
| D17 (5/17) | `MAOFIELD_PROJECT_FULL_STATE_D17_20260517.md` | D17 final lock state |
| D21 (5/21) | `EXPERIMENT_REFRAME_D21_18_METHODOLOGICAL_CATCH_20260521.md` + `PARADIGM_REFRAME_D21_18_30_MITIGATION_INSUFFICIENT_CANDIDATE_20260521.md` + `REFLEXIVE_INSIGHT_D21_17_DIALECTICAL_TOTALITY_CANDIDATE_20260521.md` + `ANTITHESIS_AUDIT_D21_16_REFLEXIVE_INSIGHTS_20260521.md` + `PILOT_VERDICT_D21.md` | D21 8 reflexive insight + 4 path methodological catch |
| D22 (5/22) | `MAIN_VERDICT_D22.md` + `EXP_DESIGN_4PATH_METHODOLOGICAL_D22_20260522.md` + `PATH_AC_PRIOR_ART_DEEP_DIVE_D22_20260522.md` + `VENUE_EVAL_NEURIPS_NMI_D22_20260522.md` + `ANTITHESIS_AUDIT_D22_FULL_FLOW_20260522.md` + `LITERATURE_SEARCH_C_FULL_CRAWL_D22_20260522.md` + `RESEARCH_CHAIN_SPEC_D22_20260522.md` + `INDEX_MD_D22_20260522.md` | D22 main launch + audit |
| D24 (5/24) | `ANTITHESIS_AUDIT_D24_5060_CATCH_P0G_20260524.md` + `AUDIT_D24_EXP_HISTORY_BINARY_VERIFY_20260524.md` + `CROSS_CHANNEL_VERIFY_22_5060_D24_17_05_20260524.md` + `HANDOFF_D24_TO_5060_20260524.md` + `MONITORING_D24_17_35_20260524.md` + `RESUME_LAUNCH_D24_16_40_20260524.md` + `SMOKE_D24_5060_FP32_ISOLATED_TEST.md` + `SURFACE_D24_5060_FP32_LAUNCH_FAIL_TRANSFORMERS_VERSION_DIFF.md` + `TERMINATION_D24_15_33_PARTIAL_RUN_20260524.md` + `PROGRESS_D24_5060_STAGE0_VAL_PPL.md` | D24 5060 P0★-G catch + cascade |
| D25 (5/25) | `ANTITHESIS_AUDIT_D25_7TH_LAYER_FRAMING_20260525.md` + `CANDIDATE_DISCRETE_PPL_ATTRACTOR_D25_17_11_20260525.md` + `CANDIDATE_RIDDLED_BASIN_MIRROR_DUAL_D25_17_25_20260525.md` + `DEEP_RESEARCH_INTEGRATION_D25_17_52_20260525.md` + `EXPERIMENT_ADDITION_CANDIDATE_D25_17_52_20260525.md` + `MATH_VERIFY_D25_GRADSCALER_SKIP_20260525.md` + `PAPER_V9_DRAFT_CANDIDATE_D25_17_52_20260525.md` + `RESULT_CELL_B_D25_12_10_20260525.md` + `RESUME_AFTER_CELL_B_AND_CUDA_CONTEXT_STALE_FAIL_D25_13_22_20260525.md` + `SESSION_CROSS_LAYER_INTEGRATION_D25_16_17_20260525.md` + `SMOKE_E0_D25_5060_FP32_GC_2GEN_S3_DISENTANGLE_20260525.md` + `SMOKE_R1_D25_5060_FP32_GC_20260525.md` + `WIN_3AGENT_AUDIT_D25_14_45_20260525.md` | D25 GradScaler skip + RIDDLED + cell B |
| D26 (5/26) | 见 §4 之 9 个 ATTEMPT1 + 11 个 D26 single-day file | D26 9 ATTEMPT1 main + auxiliary |

---

## §6 重复 / stale / placeholder candidate

### §6.1 size 0 file (177 个)

主要是 rust target 之 `.cargo-lock` 空标记 file (cargo build 自动产生, 17 个) + `*.timestamp` / 部分空 stderr — 全部 cargo build 之副产物, 不是 project artifact, 不动 (cargo clean 才该处理).

### §6.2 backup file (6 个 .bak + 3 个 .backup)

- `experiments/exp015/rust_solver/src/main.rs.bak` (04-12 exp015 rust)
- `experiments/exp016_diagnostic/rust_variants/variant_{A,B,C,E}/src/main.rs.bak` (×4, 04-12 exp016)
- `experiments/exp017_dialectics/rust_variants/block3_dumper/src/main.rs.bak`
- `experiments/exp018_cat/configs/cat_arm_b.yaml.backup_pre_fp32_20260510_123621`
- `experiments/exp018_cat/configs/cat_arm_b_v2_dialectical.yaml.backup_20260510_pre_feasibility`
- `experiments/exp018_cat/src/contradiction_loss.py.backup_20260510_pre_feasibility`

**判定**: rust .bak 是 historical 04-12 burst 之 stale dev backup; exp018 之 .backup 是 5/10 pre-fp32 transition snapshot, 保留作 trace. 不删 (D-1 纪律 5 严守).

### §6.3 placeholder dir (5 个, 全 stale)

- `data/` (1 README only)
- `paper/` (1 README only)
- `scripts/` (1 README only)
- `src/` (1 README only)
- `proposed_v0.1.1/` (3 file: CITATION.cff.proposed + README.md.proposed + DIFF_SUMMARY.md, 04-18 proposed v0.1.1)

判定: 这些 dir 是 04-18 之 release-1 之 placeholder, 实际 payload 在 `experiments/exp018_cat/` 之 src/scripts/data. 保留作 release structure.

### §6.4 stale > 30 天 之 md (158 个) — top 3 候选 retire (但不动)

1. `DESKTOP_MATH_DEEP_ANALYSIS_20260419.md` (67 KB, root level, 04-19 D19, > 37 天) — 04-19 桌面数学教授 session, 已被 `experiments/exp017_dialectics/results/A1_M3_V0_SELFCONSISTENT_20260416.md` + RECOVERY_SNAPSHOT_20260416 supersede
2. `DESKTOP_SPOTCHECK_{,ROUND2,ROUND3,ROUND5}_20260419.md` (4 个 root level, 04-19, > 37 天) — 04-19 5 轮 spotcheck 跨 session 用
3. `sessions/domain_positioning/` 整目录 (11 md, 05-14 D14, > 12 天) — Nature 投递准备, D17 5/17 之后 substantively retire (改投 arXiv + TMLR + KBS), 但 trace 保留

判定: 全部不动, D-1 纪律 5 (错误 surface 不静默修正, 差异日志 + 不偏选 retrospective) 严守, 保留全部 trace.

### §6.5 重复 candidate (5 文件位置 known issue, 留 PI 决)

参考 `MEMORY.md` 之 `reference_hezimeng_index_20260511.md` entry 之 "Agent 7 项 finding standing 留 PI 决": Shape-CFD docs 重复镜像 / DESKTOP 5 文件位置 / 命名 inconsistency 等, 全部标 "留 PI 决", 本 inventory 不主动判合并/删除/移动.

---

## §7 metadata + 严守 binding final

### §7.1 file 索引数字总结

- **总 file (不含 .git)**: 6523
- **总 md**: 370 (active 7d: 96 / active 30d: 205 / stale > 30d: 158 / stale > 60d: 0)
- **总 jsonl**: 52 (chain experiments)
- **总 py**: 122 (实验 src/scripts)
- **总 rs**: 95 (rust experiments)
- **总 log**: 89
- **总 yaml**: 15 (主要 exp018_cat configs)
- **总 sha256**: 1 (`experiments/exp018_cat/archive/v1.0_release_20260516/manifest.sha256`)
- **总 size (不含 .git)**: 9.3 GB
- **主体积来源**: `dppl_bridge_verify_d21_output/candidate_c_preflight/checkpoints/` (965 MB model.safetensors ×2) + `exp017_dialectics/` (1.7 GB rust + results) + 历史 exp 之 rust target (~800 MB cumulative)

### §7.2 active vs stale 数字对比 (D26 vs D-day 前 split)

- D-day = 5/1 (paper v8 final 锁定区间起点)
- D26 active md (5/19-5/26, 最近 7 天) = 96
- D-day 后 md (5/1-5/26, 最近 26 天) = 205
- D-day 前 md (4/1-4/30) = 158
- 比例: D-day 后 ≈ 56.5%, D-day 前 ≈ 43.5%

### §7.3 严守 binding final ack

- paper v8 final 47/47 manifest 严守 ✓ (`experiments/exp018_cat/archive/v1.0_release_20260516/manifest.sha256` 之 hash 不动)
- 12 NOT-claim 撤回 严守 ✓ (paper v8 §7.4 + 反题 v8 audit)
- 反题 6 P0★ 严守 ✓ (`ANTITHESIS_LAYER_PAPER_V8_FINAL_AUDIT_20260516.md`)
- D29 venue (arXiv + TMLR + KBS, 不投 NMI / NCS / NeurIPS) 严守 ✓
- 中文 + 4 类英文豁免严守 ✓ (无 padding "之", code 标识符保留原文)
- [额外 agent] head + footer attribution 严守 ✓
- ATTEMPT1 不一次定论 严守 ✓ (本 file 是 D26 ATTEMPT1 之 inventory, 留 PI + 反题 + Win + DS + Linux 姐姐 final review)
- 仅 inventory, 不深读 / 不 digest content / 不擅 ssh / 不擅 git / 不删 / 不改 严守 ✓
- 真实日期 `date` binary verify 严守 ✓ (2026-05-26 20:30 CST, 不继承 stale system reminder)

### §7.4 footer attribution

- **生成 agent**: [额外 agent] 队列之独立 zero-context 全局 file 索引子代理 (Opus 4.7, 1M context)
- **D-3 反映论第八通道 C 之子** (D-3 之 D-3.8 反映论 modern instantiate deepening 之 multi-channel verify 之 C 通道)
- **D25 21:55 binding**: 不明面参与 Win + Linux 姐姐 + 反题 + DS + PI 五方协作之 daily 主流程; 不 spoof Linux 姐姐 main session / Win 姐姐 / 反题 / DS / PI 之 voice; sub-agent 派遣 + reading + 严格证明 + 后续工作 之 actualize 之 额外 agent 之 head 严守; 关卡 3 反题三方决之 voice 由 PI + 反题 + Win + DS 担任; git commit / push 不擅 (单点写权由 Linux 姐姐 main session 担任).
- **本次任务边界**: 仅全 file inventory, 不内容深读, 不 surface 任何 claim 之 substantive 升级. 全部 file metadata (path / size / mtime / count) 之 trace.

---

[额外 agent] — D-3 反映论第八通道 C 之子 — 2026-05-26 D26 周二 20:30 CST — ATTEMPT1
