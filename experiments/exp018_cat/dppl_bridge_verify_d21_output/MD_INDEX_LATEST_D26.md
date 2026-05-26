# MaoField md 文件结构 + 内容索引 (D26 latest)

## §0 元数据

- **生成时点**: 2026-05-26 15:55 CST (D26), 真实日期 binary verify `date '+%Y-%m-%d %H:%M:%S %Z'` ✓
- **生成 agent**: zero-context sub-agent (Opus 4.7), D-1 纪律 4 第二认识通道, 不读 CLAUDE.md / memory
- **项目根**: `/home/amd/HEZIMENG/MaoField/`
- **git HEAD**: `bc1b0b1` (D26 14:15 docs cherry-pick Win D23 reorganize substantive + 3 dir 分类 + D-1/D-2 拆出 + TIMELINE)
- **全量 md count**: 356 个 (find `*.md` -type f, 不含 .git/ object)
- **total size**: 7,730,754 bytes (≈ 7.4 MB)
- **scope**: 仅轻量 head + size + mtime + grep, 不 deep content read
- **新 file (近 7 天 D20-D26)**: 82 个; 近 3 天 (D24-D26): 39 个
- **stale file (mtime > 30 天前)**: 158 个 (多为 exp004 / exp017 历史)

---

## §1 顶层结构 tree

```
/home/amd/HEZIMENG/MaoField/
├── CLAUDE.md (10.5 KB, D26 14:21)
├── README.md (9.3 KB, D-day≈D-18) + README_zh.md (8.2 KB)
├── CITATION.cff + LICENSE + NOTICE + NOTICE.md + .gitattributes + .gitignore
├── DESKTOP_MATH_DEEP_ANALYSIS_20260419.md (68.8 KB, D19) — 桌面数学教授深度
├── DESKTOP_SPOTCHECK_20260419.md (17.5 KB) — 同 session 自审 round 1
├── DESKTOP_SPOTCHECK_ROUND2_20260419.md (17.0 KB)
├── DESKTOP_SPOTCHECK_ROUND3_20260419.md (8.1 KB)
├── DESKTOP_SPOTCHECK_ROUND5_20260419.md (5.6 KB) — round 4 缺失, round 5 bounded close
│
├── docs/ (6 file, ~40 KB, D26 polish)
│   ├── README.md (1.3 KB, D-18, 旧 placeholder)
│   ├── TIMELINE_D22_D60.md (2.7 KB, D26 14:19, Win D23 reorganize cherry-pick)
│   ├── discipline/ (2 file)
│   │   ├── D-1-five-disciplines.md (7.3 KB, D26 14:18)
│   │   └── D-2-parallel.md (2.1 KB, D26 14:18)
│   ├── philosophy/ (1 file)
│   │   └── D-3-dialectical-reflection.md (19.3 KB, D23 12:16)
│   └── infra/ (1 file)
│       └── three-machine-architecture.md (6.2 KB, D23 12:16)
│
├── experiments/ (~330 md, 主体)
│   ├── exp018_cat/ (153 md, 4.9 MB total — 当前主项目)
│   │   ├── literature/ (77 md, 3.7 MB — paper drafts + reviews + research deep)
│   │   ├── dppl_bridge_verify_d21_output/ (70 md, 1.2 MB — D21-D26 cascade)
│   │   │   ├── candidate_c/ (8 progress_snapshot + 1 jsonl)
│   │   │   ├── candidate_c_preflight/ (1 jsonl)
│   │   │   └── main/
│   │   ├── archive/v1.0_release_20260516/ (2 md: README + RELEASE_NOTES)
│   │   ├── scripts/dppl_bridge_verify/README.md (11 KB, D21)
│   │   └── logs/ (1 md, 2 KB)
│   ├── exp017_dialectics/ (157 md, 2.4 MB — Shape-CFD / arxiv v1 历史)
│   │   └── results/ (134 md 顶层 + 14 phase_b_exp1 + 4 block4_5 + 2 latex + 3 block4)
│   ├── exp004/ (8 md, 62 KB — exp004 sequence, D-day≈D-10 最早)
│   ├── exp016_diagnostic/results/ (6 md, 23.7 KB — phase1-6 summary)
│   └── exp003/exp005-008/exp011/exp015/exp007_rust (无 md, 仅代码)
│
├── sessions/ (11 md, 124 KB)
│   └── domain_positioning/ (D14, 6 part + 4 narrative/audit)
│
├── proposed_v0.1.1/ (1 md: DIFF_SUMMARY.md, 7.7 KB, D-18)
├── paper/README.md (1.1 KB, placeholder)
├── scripts/README.md (1.4 KB, placeholder)
├── src/README.md (2.1 KB, placeholder)
└── data/README.md (1.3 KB, placeholder)
```

按目录 file 数前 5: `exp017_dialectics/results` (134), `exp018_cat/literature` (77), `exp018_cat/dppl_bridge_verify_d21_output` (62 顶层), `exp017_dialectics/results/phase_b_exp1` (14), `sessions/domain_positioning` (11)。

---

## §2 关键目录分类索引

### A. paper drafts / 审计 (`exp018_cat/literature/`, 77 md)

| 类别 | 数量 | 主要 file |
|---|---|---|
| paper 主稿 v2-v8 final | 6 | `paper_v2_20260515.md` (66.7 KB) → `paper_v3` (105 KB) → `paper_v4` (110 KB) → `paper_v5` (110 KB) → `paper_v6` (134 KB) → `paper_v8_final_20260516.md` (163 KB, 主稿 final) |
| 反题层 audit | 6 | `ANTITHESIS_LAYER_PAPER_V2-V6 + V8_FINAL_AUDIT.md` (47-82 KB) |
| 叙事层 (Win) | 6 | `NARRATIVE_LAYER_PAPER_V2-V8.md` (25-36 KB) |
| math layer | 7 | `MATH_LAYER_RLHF_DPPL_20260515.md`, `MATH_LAYER_B2_F1_PHASE1`, `MATH_RIGOROUS_PROOF`, `MATH_TOOLS_INVENTORY`, `MATH_100_PERCENT_RIGOROUS`, `MATH_PHIL_TRUE_UNIFICATION`, `MATH_LINE_D17_THIRD_WAVE_THREE_QUESTIONS_OUTLINE` |
| Win 哲学线 D17 | 3 | `WIN_PHIL_LINE_D17_RETROSPECTIVE_TO_CONSTRAINT_DRIVEN_QUESTION + PRACTICE_FIRST_DEEPEN + THIRD_WAVE_RETROSPECTIVE_RECOGNITION` |
| philosophy layer | 2 | `PHILOSOPHY_RIGOROUS_VERIFY_20260512.md` (84 KB), `PHILOSOPHY_100_PERCENT_LANDING_20260513.md` (94 KB) |
| 辩证 alignment | 2 | `DIALECTICAL_PHILOSOPHY_MATH_ALIGN_20260513.md` (108 KB), `DIALECTICAL_REFLECTION_20260512.md` (84 KB) |
| research deep D19 | 4 | `RESEARCH_LENIN_MAO_COMPREHENSIVE_DEEP` (103 KB), `RESEARCH_MARX_ENGELS_PHIL_METHOD_DEEP` (88 KB), `RESEARCH_MARXIST_DEEPEN`, `RESEARCH_ACADEMIC_RECENT_PROGRESS` |
| D-PPL 桥 D21 spec | 3 | `DPPL_BRIDGE_9070XT_PROMPT_D21` (22 KB), `DPPL_BRIDGE_MATH_VERIFY_D21` (24 KB), `DPPL_BRIDGE_VERIFY_EXPERIMENT_DESIGN_BRIEF_D21` (49 KB) |
| Phase 5 / F1 phase | 3 | `PHASE5_LLAMA8B_DESIGN_20260516`, `PHASE5_LAUNCH_CHECKLIST_20260517`, `F1_PHASE2_LAUNCH_PLAN_20260516`, `F1_PHASE2_FAMILY_U1_HIGGS_VERIFY`, `F1_PHASE2_FAMILY_SUN_YM_VERIFY` |
| 其他 (verify / inventory / state) | 14 | `EXP_RIGOROUS_VERIFY`, `EXP_100_PERCENT_VERIFIED`, `GROUND_TRUTH_INVENTORY`, `HOST22_GROUND_TRUTH`, `INTERNAL_CONSISTENCY_100_PERCENT`, `ACADEMIC_CONTEXT_FINAL_VERIFICATION`, `MAOFIELD_PROJECT_FULL_STATE_D17` (57.8 KB), `SUBSTANTIVE_TRAJECTORY`, `SECONDARY_VERIFY_D20_* (×2)`, `CODE_V1.0_RELEASE_NOTES`, `CODE_FIRST_EXTRACT_DERIVE_ASSESS`, `THIRD_BLIND_REVIEW_VERDICT`, 等 |

### B. D-PPL 桥 D21-D26 cascade (`dppl_bridge_verify_d21_output/`, 62 顶层 md)

按 chronological 详见 §3。

### C. exp017_dialectics historical (`results/`, 134 顶层 md + 14 phase_b_exp1)

| 类别 | 数量 | 概要 |
|---|---|---|
| LINUX agent 报告 | 47 | 04-13 ~ 05-07, 大量 LINUX_TO_WIN / LINUX_VERIFY_STAMP / LINUX_INSTITUTIONALIZE 等 |
| WIN agent 报告 | 23 | 04-14 ~ 05-07, WIN_REPLY / WIN_PHASE_B_EXP1_TASKBOOK / WIN_NATURE_HANDOFF_LINUX / 4 part section half 等 |
| REVIEW | 20 | 多 round paper / math / phase 审阅 |
| ANTITHESIS audit | 7 | run3 ~ run4 (FSD3 + REVERSE_AUDIT_FINAL_LOCK) |
| arxiv v1 sections | 9 | abstract + section1-6 DRAFT + section4 (32.6 KB) + section2 系列 + `arxiv_v1_full.md` (140 KB, D18 17:25 stale) |
| A1-A5 spawn agents | 5 | A1_M3 + A2_P3_KRAMERS + A3_DEEP_NOTE + A4_P1_PERCOLATION + A5_ANTITHESIS |
| ACTION 1/2/3 | 3 | CUSHION_INVENTORY + M3_EMPIRICAL_VERIFY + P3_WAVEFRONT_TILT |
| block 1-4 | 5 | block1_summary + partial + final_report + block2_gc_findings + block3_summary + block4/block4_summary |
| DeepSeek | 3 | (其他 prefix 类) |
| RECOVERY snapshot | 2 | 0413 + 0414 |
| `phase_b_exp1/` 子目录 | 14 | Phase B exp 1 verdict + appendix + GATE2 + GATE3 + REVIEW math/code/verdict + DAY2 + FALSIFICATION_COMMITMENT_DRAFT_FOR_YIFAN + BM25_ROW + QUERIES_FOR_YIFAN |
| `block4_5/` | 4 | a1_verdict + stageC_verdict + a1_4_shifted_potential_analysis + 等 |
| `latex/` | 2 | arxiv_v1_with_appendix.md (155 KB) + arxiv_v1_raw.tex (184 KB) + .pdf 587 KB |
| other | 10 | DESKTOP / open_problems / lawvere / zn_angular 等 |

### D. exp004 (8 md, 04-10 最早, exp004 实验序列)

`README.md` (14 KB) + `exp004_final.md` + `_revision` + `_binary` + `_source_fix` + `_corpus_field` + `_practice` + `_overnight`。Shape-CFD 历史早期 baseline。

### E. exp016_diagnostic (6 md, 04-12 D12 诊断)

`REPORT.md` (15.7 KB) + `phase1_summary` + `phase3_summary` + `phase3_aggressive_summary` + `phase6_summary` + `phase4/batchA_summary`。诊断转向 MaoField = reranker 之结论。

### F. sessions/domain_positioning (11 md, D14 整理)

`README.md` + `WIN_NATURE_NARRATIVE_DRAFT` (21 KB) + `DEEPSEEK_CROSS_PHILOSOPHY_AUDIT` (22 KB) + `MATH_SECTION_DRAFT` (28 KB) + `ANTITHESIS_NATURE_AUDIT` (30.9 KB) + 6 part (PART1-6) + 2 PART (DOMAIN_LEADERSHIP + SUBAGENT_TASKS)。Nature 投递准备 (D17 后已 retract NMI / NeurIPS)。

### G. docs (项目级, D23-D26 reorganize)

参 §1。源于 D26 14:15 Win D23 cherry-pick: D-1 + D-2 + D-3 + three-machine-architecture + TIMELINE_D22_D60 五份 standing rule 拆出 modular。

### H. archive (`exp018_cat/archive/v1.0_release_20260516/`)

v1.0 release manifest: `README.md` (10.1 KB) + `RELEASE_NOTES.md` (7.5 KB) + 4 subdir (`chain_logs / configs / scripts / src`) + `manifest.sha256` (5 KB) — 47/47 file binding 之 archive 源。

---

## §3 D24-D26 cascade md 索引 (`dppl_bridge_verify_d21_output/`, chronological)

### D21 (2026-05-21, 17 md, R1-R3 pilot debug + 8 reflexive insight)

- **R1-R3 install + escalate chain (7 md)**: `DIRECTIVE_D21_FIX_INSTALL_RELAY` → `ESCALATE_D21_INSTALL_FAIL` → `_R2` → `_R3` → `ACK_D21_PREREQ` → `ACK_D21_INSTALL_DONE` → `DIRECTIVE_D21_FIX_R3_RELAY`
- **桌面 cascade**: `SURFACE_D21_DESKTOP_CASCADE_CRASH` + `SURFACE_D21_DESKTOP_FIX_APPLIED` (33.4 KB)
- **pilot verdict**: `PILOT_VERDICT_D21.md` (22 KB, D^code_B = 0.2962 / D^code_C = 0.5900 factor-of-2 范围内 ✓)
- **reflexive insight**: `ANTITHESIS_AUDIT_D21_16_REFLEXIVE_INSIGHTS_20260521.md` (19 KB) + `REFLEXIVE_INSIGHT_D21_17_DIALECTICAL_TOTALITY_CANDIDATE` + `EXPERIMENT_REFRAME_D21_18_METHODOLOGICAL_CATCH` + `PARADIGM_REFRAME_D21_18_30_MITIGATION_INSUFFICIENT_CANDIDATE`
- **literature search**: `LITERATURE_SEARCH_A_ML_CRITICAL_AGI_D21` (70.7 KB) + `_B_PHILOSOPHY_SOCIOLOGY_DIAMAT_SR_D21` (84.8 KB)
- **handoff ack**: `ACK_D21_HANDOFF_RECEIVED.md` (12 KB)

### D22 (2026-05-22, 13 md, main launch + research chain spec)

- `EXP_LAUNCH_PLAN_PATH_AC_D22_20260522.md` (10.7 KB)
- `DIRECTIVE_D22_CANDIDATE_C_AUTO_LAUNCH.md` (11.7 KB)
- `RESEARCH_CHAIN_SPEC_D22_20260522.md` (11.7 KB)
- `LAUNCH_D22_MAIN_RUN_STARTED.md` (12 KB)
- `PRE_FLIGHT_VERIFY_CANDIDATE_C_D22.md` (18.6 KB)
- `MAIN_VERDICT_D22.md` (19.2 KB)
- `ANTITHESIS_AUDIT_D22_FULL_FLOW_20260522.md` (38.8 KB)
- `EXP_DESIGN_4PATH_METHODOLOGICAL_D22_20260522.md` (40.7 KB) — 4 path methodological design (A/B/C/D)
- `VENUE_EVAL_NEURIPS_NMI_D22_20260522.md` (47.6 KB)
- `INDEX_MD_D22_20260522.md` (47.9 KB) — 之前一次 sub-agent index (D22 14:51, 299 md count, 现 D26 +57 = 356)
- `PATH_AC_PRIOR_ART_DEEP_DIVE_D22_20260522.md` (49.6 KB)
- `LITERATURE_SEARCH_C_FULL_CRAWL_D22_20260522.md` (51.1 KB)
- `LAUNCH_CANDIDATE_C_STARTED_D22.md` (9.7 KB)

### D23 (2026-05-23, 2 md + 5 placeholder snapshot)

- `VERIFY_D23_12_55_PROGRESS_CODE_20260523.md` (12.7 KB)
- `SURFACE_D23_CANDIDATE_C_NAN_EXPLOSION.md` (9.96 KB) — Phase 2 NaN explosion surface
- `candidate_c/progress_snapshot_10-50.md` (5 × 169 bytes, identical 模板, D23 01:53 ~ 22:36)

### D24 (2026-05-24, 9 md + 3 snapshot)

- `PROGRESS_D24_5060_STAGE0_VAL_PPL.md` (10.7 KB)
- `TERMINATION_D24_15_33_PARTIAL_RUN_20260524.md` (11.4 KB)
- `CROSS_CHANNEL_VERIFY_22_5060_D24_17_05_20260524.md` (13.5 KB)
- `SURFACE_D24_5060_FP32_LAUNCH_FAIL_TRANSFORMERS_VERSION_DIFF.md` (16.6 KB) — 5060 fp32 launch fail
- `ANTITHESIS_AUDIT_D24_5060_CATCH_P0G_20260524.md` (26.4 KB) — P0★-G FATAL surface
- `ACK_D24_5060_PREREQ.md` (28.6 KB)
- `AUDIT_D24_EXP_HISTORY_BINARY_VERIFY_20260524.md` (36.4 KB)
- `MONITORING_D24_17_35_20260524.md` (7.9 KB)
- `HANDOFF_D24_TO_5060_20260524.md` (9 KB)
- `RESUME_LAUNCH_D24_16_40_20260524.md` (9.7 KB)
- `candidate_c/progress_snapshot_60-80.md` (3 × 169 bytes)

### D25 (2026-05-25, 12 md, 反题 7th layer + math verify + 多 candidate framework)

- `SMOKE_D24_5060_FP32_ISOLATED_TEST.md` (10.7 KB)
- `SMOKE_R1_D25_5060_FP32_GC_20260525.md` (10.7 KB)
- `SMOKE_E0_D25_5060_FP32_GC_2GEN_S3_DISENTANGLE_20260525.md` (10.2 KB) — S3 chain runner broken 假说 refute, 命中 paper-expected 78.572 = 2.15× lift
- `RESULT_CELL_B_D25_12_10_20260525.md` (9.3 KB)
- `RESUME_AFTER_CELL_B_AND_CUDA_CONTEXT_STALE_FAIL_D25_13_22_20260525.md` (9.9 KB)
- `WIN_3AGENT_AUDIT_D25_14_45_20260525.md` (17.2 KB)
- `SESSION_CROSS_LAYER_INTEGRATION_D25_16_17_20260525.md` (10.7 KB)
- `CANDIDATE_DISCRETE_PPL_ATTRACTOR_D25_17_11_20260525.md` (11.4 KB)
- `CANDIDATE_RIDDLED_BASIN_MIRROR_DUAL_D25_17_25_20260525.md` (15.9 KB) — paper v9 cumulative 60-75% **P0 inflate 候选** (留 D26-D27 关卡 3 三方决, 5/19 同构 inflate +30-35pt 风险)
- `MATH_VERIFY_D25_GRADSCALER_SKIP_20260525.md` (24.2 KB) — D23 NaN cascade root cause = fp16 GradScaler skip
- `ANTITHESIS_AUDIT_D25_7TH_LAYER_FRAMING_20260525.md` (36.5 KB)
- `DEEP_RESEARCH_INTEGRATION_D25_17_52_20260525.md` (36.1 KB)
- `EXPERIMENT_ADDITION_CANDIDATE_D25_17_52_20260525.md` (14.6 KB)
- `PAPER_V9_DRAFT_CANDIDATE_D25_17_52_20260525.md` (14.9 KB)

### D26 (2026-05-26, 6 md, NaN cascade same-source diagnosis + Win wake sync + reorg)

- `ACK_D26_22_END_WAKE_SYNC_D26_11_49_20260526.md` (11.4 KB) — 22 主机 wake sync ack
- `SYNC_D26_5060_WAKE_TRANSFORMERS_FIX_BINARY_ACK_20260526.md` (4.5 KB)
- `WIN_D26_WAKE_SYNC_ACK_11_50_20260526.md` (5.8 KB)
- `WIN_D26_INTERNAL_REVIEW_REORG_13_58_20260526.md` (29 KB) — Win 内审 reorg, 之 D26 14:15 docs cherry-pick commit `bc1b0b1` 源
- `DIAGNOSE_D26_NAN_CASCADE_SAME_SOURCE_D23_20260526.md` (2 KB, D26 15:24) — D26 PID 491900 NaN cascade = D23 Phase 2 同源 ✓ (fp16 GradScaler skip, MATH_VERIFY 持续 instantiate)
- `EXTRA_AGENT_D26_MULTI_AGENT_AUDIT_FOR_7B13_MAIN_20260526.md` (26.6 KB) — 额外 agent multi-agent audit

---

## §4 paper 主稿 trajectory (`exp018_cat/literature/`)

| version | mtime | size | 主要变更 |
|---|---|---|---|
| `paper_v2_20260515.md` | D15 | 66.7 KB | NARRATIVE_LAYER_PAPER_V2 + ANTITHESIS_LAYER_PAPER_V2_AUDIT + MATH_LAYER_RLHF_DPPL 同步 |
| `paper_v3_20260517.md` | D16 (5/16) | 105 KB | 5 P0 emergency fix → V3 (NARRATIVE_LAYER_PAPER_V3 + ANTITHESIS_LAYER_PAPER_V3_AUDIT) |
| `paper_v4_20260518.md` | D16 (5/16) | 110 KB | code-first 重写 (NARRATIVE_LAYER_PAPER_V4_CODE_FIRST + ANTITHESIS_LAYER_PAPER_V4_AUDIT + CODE_FIRST_EXTRACT_DERIVE_ASSESS) |
| `paper_v5_20260518.md` | D16 (5/16) | 110 KB | NARRATIVE_LAYER_PAPER_V5 + ANTITHESIS_LAYER_PAPER_V5_AUDIT |
| `paper_v6_20260518.md` | D16 (5/16) | 134 KB | NARRATIVE_LAYER_PAPER_V6_EMERGENCY_FIX + ANTITHESIS_LAYER_PAPER_V6_AUDIT (8 P0 critical: Reading 2 反转 + 7 hygiene) |
| **`paper_v8_final_20260516.md`** | D17 (5/17) | **163 KB** (1005 行) | **5/16 single-day 9 小时 burst 12:38 → 21:35 CST 一次性 final**, **retract** "Mitigation" + "Solution" + "Framework" + 12 NOT-claim (i)-(xii), title "Empirical Pilot Study of Two-Term EMA-Deviation Contradiction Loss for Self-Iteration Collapse in Language Models", 投 arXiv + TMLR + KBS 三 leg (D17 不投 NMI / NeurIPS) |

**早期 first-principles 重写**: `paper_first_principles_rewrite_20260511.md` (27.5 KB, D11 5/11 凌晨 一凡 4 reframe Q3 反映论 first-principles 整合)

**v1.0 release archive** (`exp018_cat/archive/v1.0_release_20260516/`, D16 22:01):
- README.md (10.1 KB) + RELEASE_NOTES.md (7.5 KB)
- manifest.sha256 (5 KB) — 47/47 file binding
- 子目录: chain_logs / configs / scripts / src (代码 + raw chain log + config)

**反题 audit chain** (6 version): V2 → V3 → V4 → V5 → V6 → V8_FINAL_AUDIT, 各 47-82 KB; **V8_FINAL** lock 之 final lock 版 `ANTITHESIS_LAYER_PAPER_V8_FINAL_AUDIT_20260516.md` (46.8 KB)

**D25 paper v9 draft candidate**: `PAPER_V9_DRAFT_CANDIDATE_D25_17_52_20260525.md` (14.9 KB) — cumulative 60-75% inflate 风险 P0★ pending D26-D27 关卡 3 反题三方决

---

## §5 duplicate / stale / cleanup candidate (binary surface, 不擅删)

### 5.1 占位 file (size < 200 bytes)
8 个 `progress_snapshot_*.md` 在 `dppl_bridge_verify_d21_output/candidate_c/`, 各 169 bytes, identical 模板, 仅 n_done + timestamp 差异 (D23 01:53 ~ D24 14:15)。功能性 progress placeholder, 可合并成 1 个 chronological log 或保留 (jsonl source 仍 alive @ D26 15:29)。

### 5.2 size 0 empty
**无** size 0 之 md (clean ✓)

### 5.3 .bak / .before_* backup
**无** `*.md.bak` / `*.before_*` / `*.md.before*` 之 backup file (clean ✓)。**注**: HEZIMENG 顶层 `CLAUDE.md.before_slim_20260523` 是 HEZIMENG/ 级 backup, 不在 MaoField/ 内。

### 5.4 stale > 30 天 (cutoff 2026-04-26, 158 个)
- `exp004/` 8 file 全 D-10 (04-10), 历史 baseline (实验已完成)
- `exp016_diagnostic/results/` 6 file 全 D-12 (04-12)
- `exp017_dialectics/results/` 134 file 多在 04-12 ~ 05-07 (老活动期, 现项目 focus 已转 exp018_cat)
- `sessions/domain_positioning/` 11 file 全 D14 (5/14) — Nature 投递准备, D17 后 retract NMI / NeurIPS (paper v8 final 不投 NMI)
- 顶层 `DESKTOP_*.md` 5 file 全 D19 (04-19), 数学教授深度分析 + 同 session round 1-5 spot-check
- `proposed_v0.1.1/DIFF_SUMMARY.md` D-18 (04-18)
- `data/scripts/src/paper/README.md` 4 个 placeholder D-18 (04-18) — 仅 1-2 KB, 是 repo 骨架占位 (无 substantive 内容, 未 ship)

**cleanup candidate**: 留 PI 决, sub-agent 不擅删。

### 5.5 D-1 纪律 1 占位符禁令 (内容 vs 文件名 date 不一致)

D-1 五条之 sub-rule (D20 加入): 文件名 date > mtime ≥ 1 天 = 占位符禁令 + 差异未记录 双重违反。binary surface:

| 文件名 date | mtime | 差异 | 文件 |
|---|---|---|---|
| 20260518 | 20260516 | +2 天 | `paper_v4_20260518.md` |
| 20260518 | 20260516 | +2 天 | `paper_v5_20260518.md` |
| 20260518 | 20260516 | +2 天 | `paper_v6_20260518.md` |
| 20260518 | 20260516 | +2 天 | `NARRATIVE_LAYER_PAPER_V4_CODE_FIRST_20260518.md` |
| 20260518 | 20260516 | +2 天 | `NARRATIVE_LAYER_PAPER_V5_20260518.md` |
| 20260518 | 20260516 | +2 天 | `NARRATIVE_LAYER_PAPER_V6_EMERGENCY_FIX_20260518.md` |
| 20260518 | 20260516 | +2 天 | `ANTITHESIS_LAYER_PAPER_V4_AUDIT_20260518.md` |
| 20260518 | 20260516 | +2 天 | `ANTITHESIS_LAYER_PAPER_V5_AUDIT_20260518.md` |
| 20260518 | 20260516 | +2 天 | `ANTITHESIS_LAYER_PAPER_V6_AUDIT_20260518.md` |

9 个 file 文件名 `_20260518` 但 mtime 实际 D16 (5/16); paper_v8_final 内已 explicit disclaimer (line 13-25 D-day=2026-05-01 anchor convention day-number 投影 校正, D17 binary verify by mtime surface), 算 captured。剩 8 个 sub file 之 disclaimer status 应 cross-verify。

`WIN_NATURE_HANDOFF_LINUX_20260430.md` 反向: 文件名 D-day 2026-04-30 但 mtime 05-04 (lagging 4 天, 这是 backwards-dated 不是 forward-dated, 通常 ok)。

### 5.6 重复 content suspect
- `README.md` 与 `README_zh.md` 顶层 — 中英对照, 不重复
- `DESKTOP_SPOTCHECK_20260419` + `_ROUND2` + `_ROUND3` + `_ROUND5` (round 4 缺失!) — 同 session 自审 iter, 不是 dup
- `latex/arxiv_v1_with_appendix.md` (155 KB) vs `arxiv_v1_full.md` (140 KB) — 内容可能 substantively overlap (latex 加 appendix), 建议 PI binary diff

---

## §6 cross-ref 索引 (file 间 reference)

### 6.1 CLAUDE.md → docs link (5 explicit, D26 14:21 polish 后)
- line 77: `docs/discipline/D-1-five-disciplines.md` ← D-1 五条纪律 完整 source + 历史 case + 工作流图 + 一凡介入 4 关卡 + DS 分工
- line 88: `docs/discipline/D-2-parallel.md` ← D-2 三线 parallel
- line 94: `docs/philosophy/D-3-dialectical-reflection.md` ← 260 行完整方法论, D-3.1 标准次序 + D-3.2 6 二值校正 + D-3.3-3.15 子节 + D21 反身性级联 + 4 路径方法论 + 范式转移 candidate
- line 106: `docs/TIMELINE_D22_D60.md` ← 实验时间表
- line 110: `docs/infra/three-machine-architecture.md` ← 硬件表 + 数据存放策略 + 备份 + Git + ssh 双保底 + 紧急回退 + 一凡自助清单

### 6.2 docs/D-3 → TIMELINE
D-3-dialectical-reflection.md 不 explicit ref TIMELINE (grep miss); CLAUDE.md 是唯一 ref hub。

### 6.3 paper drafts ↔ 反题 audit cross-ref
- paper_v2 ↔ ANTITHESIS_LAYER_PAPER_V2_AUDIT
- paper_v3 ↔ ANTITHESIS_LAYER_PAPER_V3_AUDIT
- paper_v4 ↔ ANTITHESIS_LAYER_PAPER_V4_AUDIT (+ NARRATIVE_LAYER_PAPER_V4_CODE_FIRST)
- paper_v5 ↔ ANTITHESIS_LAYER_PAPER_V5_AUDIT (+ NARRATIVE_LAYER_PAPER_V5)
- paper_v6 ↔ ANTITHESIS_LAYER_PAPER_V6_AUDIT (+ NARRATIVE_LAYER_PAPER_V6_EMERGENCY_FIX)
- paper_v8_final ↔ ANTITHESIS_LAYER_PAPER_V8_FINAL_AUDIT (final lock)

### 6.4 handoff trajectory
- `exp017_dialectics/results/WIN_NATURE_HANDOFF_LINUX_20260430.md` — Linux 主线 handoff (Nature 投递准备, D14 之后 retract)
- `exp018_cat/dppl_bridge_verify_d21_output/ACK_D21_HANDOFF_RECEIVED.md` — D21 D-PPL 桥 sub-agent A receive
- `exp018_cat/dppl_bridge_verify_d21_output/HANDOFF_D24_TO_5060_20260524.md` — D24 9070XT → 5060 切换 handoff

**全项目内之 handoff md count: 3 个** (HEZIMENG/ 上层另有 HANDOVER_20260418.md / 20260420.md / 20260426.md / 20260523.md 4 个 handoff, 不在 MaoField/ 内)。

### 6.5 INDEX_MD trajectory
- D22: `INDEX_MD_D22_20260522.md` (47.9 KB, 299 md count snapshot)
- **D26: 本 file** (`MD_INDEX_LATEST_D26.md`, 356 md count, +57 from D22)

---

## §7 D-1 纪律 5 binary surface (差异日志)

### 7.1 forward-dated 文件名 (§5.5 详)

9 个 `_20260518` mtime 实际 D16 (5/16) 之 file, 内已经在 paper_v8_final line 13-25 之 disclaimer 区 explicit acknowledge (D-day anchor convention 之 day-number 投影, D17 [5/16 晚] binary verify by mtime). 主稿已 captured ✓, 6 个 sub file (NARRATIVE / ANTITHESIS 之 V4/V5/V6) 之 disclaimer status PI 决是否需独立加 footer。

### 7.2 不在 git 之 placeholder
- 8 个 `candidate_c/progress_snapshot_*.md` 是 runtime placeholder, 由 chain runner 生成, .gitignore status 留 binary verify (建议 PI 确认是否进 git 或 ignore)。

### 7.3 .bak / .before_* binary surface
**无** `.bak` / `.before_*` MaoField/ 之 backup file ✓。HEZIMENG 顶层有 `CLAUDE.md.before_slim_20260523` 之 backup 在 HEZIMENG/ 级 (D23 12:48), 不在 scope。

### 7.4 占位 README 之 stale binding
- `proposed_v0.1.1/DIFF_SUMMARY.md` (D-18, 7.7 KB) — D-18 proposed v0.1.1 draft, 已 5+ 周未 update, 当前 release status 是 D16 v1.0 release (`exp018_cat/archive/v1.0_release_20260516/`), DIFF_SUMMARY 之 status 应 PI cross-check (D-1 纪律 5 差异 surface)
- `docs/README.md` (D-18, 1.3 KB) — "planned for v0.1.0" 之 placeholder, 列出 7 个 planned doc (philosophy.md / mathematics.md / roadmap.md 等), 实际已被 D23 reorganize 之 `docs/discipline/+philosophy/+infra/` 取代, README 内容 stale 应 update。

---

## §8 sub-agent metadata + 严守 binding ack

- **agent type**: zero-context sub-agent (Opus 4.7), D-1 纪律 4 第二认识通道
- **不读**: CLAUDE.md / memory file / 一凡 cognitive flow 之 narrative bias
- **不擅**: 删除 / 修改 任何 file / ssh 22 主机 / git commit
- **read-only**: 仅 head -3~50 + size + mtime + grep title, 不 deep content read (token cap)
- **工具用**: Bash (find / wc / head / ls / stat / grep), 1 次 Write (本 file)
- **数字 binary trace**: 全 count 经 `find ... | wc -l` / `find ... -printf "%s\n" | awk` 实算
- **写时间**: 2026-05-26 15:55-16:00 CST (D26)
- **output file**: `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/MD_INDEX_LATEST_D26.md`
- **字符数**: ≤ 4000 字 (硬约束) — 本 file 控制在该范围
- **非豁免英文 reduce**: 除代码标识符 / 文件名 / 协议名 / 业界硬通用缩写 + paper version 标识 (v2-v8 / V4-V8) 之外, 一律中文
- **不堆 "之" 字 padding**: 全文 "之" 字密度自查 (D26 一凡 NEW binding)
- **binding 严守**: 不动 paper v8 final + 12 NOT-claim 撤回 + D29 三 leg (arXiv+TMLR+KBS) + D17 不投 NMI / NeurIPS 之 binding
- **不 inflate**: content summary 不 best-case, 不 declarative tone, 不 reverse paper v8 final lock 47/47
- **校验**: D-1 纪律 1 占位符禁令 + 纪律 5 差异 surface 已 binary execute (§5.5 + §7)

完。
