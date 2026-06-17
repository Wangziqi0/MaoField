# MaoField MD_CATALOG — 全 ~429 md 分层梳理 (navigate reference)

> **STATE.md §7 指针目标。新 session 不必读全部** —— 看 §0 导航选 ACTIVE 核心 (~25 份),历史整组 SKIP (~250 份)。
> **维护**: 新增重要 md 归类追加;季度 review 把 SUPERSEDED 下沉历史区。本文件是 reference,不进每会话 context (STATE.md 才是 cold-start 必读)。
> **戳**: 2026-06-17 D617 晚 · HEAD `5608621` (+解耦线 [A−] 落盘复算 verdict 登记,落盘未 commit;实时以 `git log -1` 为准)
> **梳理法**: 4 zero-context agent 分区 scan md head + bash title 提取。全部仅读 head,substantive detail `[未细看]`。

---

## §0 新 session 导航 TL;DR ★最重要

### 当前 (D29-D31) ACTIVE 核心 ~25 份 (该看)
| 类 | 文件 (在 `experiments/exp018_cat/dppl_bridge_verify_d21_output/` 除非注明) |
|---|---|
| **数据 ground truth** | `D29_VERIFICATION_CASCADE_UPDATE_20260529` (最新更正主锚) · `MAOFIELD_GATE_DATA_INTEGRITY_20260529` · `MAOFIELD_EXP_METADATA_MASTER_20260529` |
| **L0 数学现状** | `MAOFIELD_L0_FULL_ROUND1_SUMMARY_20260529` (0 close/2 cond/3 partial/3 FAIL) · `MAOFIELD_L0_L0-{1,2,3,4,5-6-7,8}_*_20260529` · `MAOFIELD_L0_ROUND2_{CHANNEL_P,CHANNEL_V,INTEGRATION}_20260529` |
| **投稿物** | `PAPER_V9_SKELETON_DRAFT_D27_20260527` · `PAPER_V81_FOOTNOTE_DRAFT_WIN_LEAD_20260527` · `D28_MLRC_PAPER_DRAFT_20260528` · `literature/paper_v8_final_20260516` [LOCKED] |
| **战略/关卡3** | `MAOFIELD_D26_STRATEGIC_PANORAMA_REPORT_20260526` · `DEEPSEEK_CHECKPOINT3_{FINAL,LANGUAGE,STRATEGY}_AUDIT_20260527` · `ANTITHESIS_D26_GATE3_CHANNEL_D_VERDICT_20260526` |
| **机制根因** | `DIAGNOSE_D26_NAN_CASCADE_SAME_SOURCE_D23_20260526` · `ROCM_MIOPEN_TRACE_AUDIT_20260527` · `MATH_VERIFY_D25_GRADSCALER_SKIP_20260525` |
| **待执行/待决** | `HANDOFF_7B13_D29_ACTIONS_20260529` · `RAID1_BACKUP_MANIFEST_D30_20260530` · `E1E2_DECISION_PACKAGE_VERIFIED_20260529` |
| **最新文献线** | `MODEL_COLLAPSE_LITERATURE_AUDIT_D30_20260530` (+ near-dup `_FIXABILITY_` 版) |
| **方向入口** | `MAOFIELD_INDEX_{EXP_LOGIC,MATH_PROP,PHILO_ARG}_20260529` · `{MATH,PHILO,EXP_PLAN}_*_LATEST_D26` |
| **纪律 binding** | `docs/discipline/D-1*` · `docs/discipline/D-2*` · `docs/philosophy/D-3*` · `docs/infra/three-machine*` · `docs/TIMELINE_D22_D60` |
| **本轮 D614-617 ★** | `experiments/exp019_alpha1_confirm/` (verdict_20260614 + LINUX_AUDIT_AMENDMENT_20260615 + prereg) = α=1 confirmatory **三 endpoint 全 FALSE / C1·C2·C3 撤回 / s42 outlier** + LN race 根因 ‖ `…/decouple_verdict_20260617/` (DECOUPLE_VERDICT + analysis_decouple_n5.py) = **解耦线 [A−] 复算 0/5 死 / D2 全 fail=部分耦合 / distinct-n rep_penalty 敏感 / 问题#2 闭合** ‖ `experiments/exp018_cat/analysis/` (RECOVERY_GEOMETRY_FINDINGS_20260615 + probe_output_vs_hidden_NOTE + FINDINGS) = **E0 升维=驼峰瞬态 / 几何≈PPL投影** ‖ `wip/blackbox_dimreduction_recon_d35/` (4 recon verdict,归属待 PI,RAG 排除) = 黑箱/命题 T·U **全判被占/平凡** |

### 整组可 SKIP 历史 ~250 份
- **exp017_dialectics 全 157** (4/12-5/7 早期 dialectics + arXiv v1 整稿 + 四方协作流水) → 整组 ARCHIVE
- **literature 之 paper v1-v7 历史版本** (final = v8) + 5/8-5/20 之 100%-verify / 反题 layer audit 群
- **dppl 之 D21-D24 ops trail** (launch/escalate/resume/snapshot ~25) + ACK/SYNC 11 + candidate_c snapshot 8 + ATTEMPT1 数学 S1-S5 (已被 L0 取代)
- **early exp004-016** (8+6 md) + **sessions/domain_positioning 11** (5/14 Nature 领域引导,已被 D17 取代) + **顶层 DESKTOP_*_20260419 5**

### 4 条贯穿事实 (多文件交叉,head 实证)
1. candidate_c (9070XT fp16 N=180) **训练无效/冻结** — 5-cell gen=0 ckpt 逐字节相同 `b3a67b42`,C3 退化 ~99% sha256
2. root cause = **fp16 GradScaler silent skip optimizer.step** → 权重不更新 → NaN (D23=D26 同源)。**D615 根因下推: 非 fp16 本身, 是 gfx1201 `native_layer_norm_backward` 竞态喂 NaN → scaler 吞 → skip (LN race; manual-LN patch 治本)**
3. 5060 **fp32 a1_ppl=36.536** 落 paper ballpark,vs 9070XT fp16=93.349 (P0★-G FATAL,+157%)
4. L0 第一轮 **0 unconditional close** — 诚实分类 (2 cond + 3 partial/negative + 3 FAIL) 是主产出

---

## §1 当前主战场 — dppl_bridge_verify_d21_output (142 md, D21-D31)

> 21 cluster。`[A]`=ACTIVE `[S]`=SUPERSEDED `[R]`=ROUTINE。

- **L0 严格证明** `[A]`: FULL_ROUND1_SUMMARY + L0-1~8 + ROUND2_{P,V,INTEGRATION} + ROUND1_ADVERSARIAL + L0_PROOF_PROMPT 模板。8 条 = 0 close / 2 conditional (L0-1 Banach, L0-8 NESS) / 3 negative-partial (L0-2,3,4) / 3 FAIL (L0-5,6,7)
- **数据完整性/元数据** `[A]`: D29_VERIFICATION_CASCADE_UPDATE (更正主锚) + GATE_DATA_INTEGRITY + EXP_METADATA_{MASTER,LINUX22,5060DESKTOP} + DATA_COMPLETENESS_AUDIT_INDEP + RESULTS_REDERIVATION_INDEP + FULL_DATA_AUDIT_D26
- **全量索引** `[A]`: FULL_INDEX_3MACHINES_D29 + INDEX_{EXP_LOGIC,MATH_PROP,PHILO_ARG}_D29 ‖ `[S]`: GLOBAL_FILE_INDEX_D26 / MD_INDEX_LATEST_D26 / INDEX_MD_D22
- **D26 多通道 ATTEMPT1** `[S→被 L0 取代]`: MATH_RIGOROUS_PROOF_D26 (+S1-S5 PART) / MATH_MULTI_CHANNEL ‖ `[A]`: MULTI_CHANNEL_ANALYSIS_D26 (DS 引用) + MULTIAGENT_DEEP_DIGEST_D26
- **战略/深综合** `[A]`: STRATEGIC_PANORAMA_REPORT_D26 (530 行主锚) + DEEP_SYNTHESIS_D26_EVENING + DEEPER_INSIGHT_D26 + EXTRA_AGENT_D26_MULTI_AGENT_AUDIT + DEEPSEEK_CHECKPOINT3×3
- **paper v8.1/v9/venue** `[A]`: PAPER_V9_SKELETON_D27 + PAPER_V81_FOOTNOTE_WIN_D27 + WIN_D27_GATE3 + MLRC_PAPER_DRAFT_D28 + LITERATURE_SEARCH_V9_ANCHORS_D27 + VENUE_SCOUTING_D28 + NATURE_EDITOR_DESK_SIM_D27 ‖ `[S]`: PAPER_V9_DRAFT_D25 / VENUE_EVAL_NEURIPS_NMI_D22
- **D28 cross-channel audit** `[A]`: D28_{4ENDPOINT,CROSS_VERIFY_ABLATION,EXPERIMENTAL_DEEP,EXPERIMENT_INVENTORY,MATH_RIGOROUS,MD_CROSS_CHANNEL}_AUDIT
- **ROCm/fp16/NaN** `[A]`: ROCM_MIOPEN_TRACE_AUDIT_D27 + SMOKE_5060_FP16_CROSSCHECK_D27 + MATH_VERIFY_GRADSCALER_SKIP_D25 + DIAGNOSE_NAN_SAME_SOURCE_D23_D26 ‖ `[S]`: SESSION_CROSS_LAYER_D25 (S3 已 refute)
- **5060 cross-stack** `[A]`: SMOKE_{E0,R1}_D25 + SMOKE_D24_FP32_ISOLATED ‖ `[S]`: PROGRESS_D24_STAGE0 / SURFACE_D24_LAUNCH_FAIL
- **bit-identical/riddled** `[A]`: CANDIDATE_DISCRETE_PPL_ATTRACTOR_D25 + CANDIDATE_RIDDLED_BASIN_MIRROR_DUAL_D25 (v9 Anchor2) + DEEP_RESEARCH_INTEGRATION_D25
- **文献审计可修复性** `[A, D30 最新]`: MODEL_COLLAPSE_LITERATURE_AUDIT_D30 + _FIXABILITY_ (near-dup,二选一合并)
- **Win/反题/DS verdict** `[A]`: ANTITHESIS_D26_GATE3 + WIN_3AGENT_D25 + WIN_D26_INTERNAL_REVIEW + ANTITHESIS_AUDIT_D25_7TH_LAYER ‖ `[S]`: ANTITHESIS_AUDIT_{D21,D22,D24} + CROSS_CHANNEL_VERIFY_D24
- **D21 reflexive insight (D60+ 哲学源)** `[A]`: REFLEXIVE_INSIGHT_D21_17_DIALECTICAL_TOTALITY + PARADIGM_REFRAME_D21_18_30 + EXPERIMENT_REFRAME_D21 + EXP_DESIGN_4PATH_D22
- **方向 LATEST** `[A]`: {MATH,PHILO}_DIRECTION_LATEST_D26 + EXP_PLAN_LATEST_D26
- **实验 spec/待决** `[A]`: RESEARCH_CHAIN_SPEC_D22 + PATH_AC_PRIOR_ART_D22 + EXPERIMENT_ADDITION_CANDIDATE_D25 + E1E2_DECISION_PACKAGE_VERIFIED_D29 + E_NEW_2_EVAL_PIPELINE_AUDIT_D27
- **文献 search** `[A]`: LITERATURE_SEARCH_{A_ML,B_PHILOSOPHY,C_FULL_CRAWL}_D21-22
- **待执行** `[A]`: HANDOFF_7B13_D29_ACTIONS + RAID1_BACKUP_MANIFEST_D30
- **D21-D24 ops trail** `[S, 整组 skip]`: MAIN_VERDICT_D22 / PILOT_VERDICT_D21 / SURFACE_D23_NAN_EXPLOSION / PRE_FLIGHT / DIRECTIVE / LAUNCH / RESUME / TERMINATION / MONITORING / ESCALATE_R1-3 / SURFACE_D21_CRASH / HANDOFF_D24_TO_5060 (~25 份)
- **ACK/SYNC** `[R, 整组 skip]`: 11 份 (D26 f91f272 收讫 + D21 install + D24 5060 prereq)
- **candidate_c/ snapshot** `[S]`: progress_snapshot_{10..80}.md (8 份,机器生成,run 已判无效)

## §2 paper + 文献 — literature (77 md, 5/7-5/20)

- **paper 主稿版本链** `[LOCKED=v8]`: paper_v2_0515 → v3_0517 → v4_0518 → v5_0518 → v6_0518 → **`paper_v8_final_20260516`** [LOCKED 47/47 D17,投稿即此版]。早期: paper_first_principles_rewrite_0511 + section drafts (0509-0510)。v1→v7 全 `[S]`
- **反题 layer audit** `[S, 历史]`: ANTITHESIS_LAYER_PAPER_V{2,3,4,5,6}_AUDIT + V8_FINAL_AUDIT (v8 那份可留作 v8 审计记录) + ANTITHESIS_AUDIT_F1_YI_PATH
- **叙事 layer** `[S]`: NARRATIVE_LAYER_PAPER_V{2,3,4,5,6,8}
- **100%-verify 群** `[S, 5/12-5/13 历史]`: {MATH,PHILOSOPHY,EXP,INTERNAL_CONSISTENCY,PHILOSOPHY_100_LANDING,EXP_100,DIALECTICAL_PHILOSOPHY_MATH_ALIGN}_*_2026051x + GROUND_TRUTH_INVENTORY + HOST22_GROUND_TRUTH + SUBSTANTIVE_TRAJECTORY
- **数学推导** `[A 参考]`: DETAILED_MATH_DERIVATION_0513 + MATH_100_RIGOROUS + MATH_TOOLS_INVENTORY + sigma2_to_loss_derivation + MATH_LAYER_RLHF_DPPL + MATH_LAYER_B2_F1_PHASE1
- **Phase 5 / F1 Phase2** `[A, D60+ 设计]`: PHASE5_LLAMA8B_DESIGN + PHASE5_LAUNCH_CHECKLIST + F1_PHASE2_{LAUNCH_PLAN,FAMILY_SUN_YM,FAMILY_U1_HIGGS}
- **文献综述/盲审** `[A 参考]`: literature_review_20260507 (Model Collapse) + shumailov_audit_0508 + THIRD_BLIND_REVIEW_VERDICT_0511 + RESEARCH_{MARX_ENGELS,LENIN_MAO,MARXIST,ACADEMIC_RECENT}_D19
- **D-PPL 桥 brief** `[A]`: DPPL_BRIDGE_{9070XT_PROMPT,MATH_VERIFY,VERIFY_EXPERIMENT_DESIGN}_D21
- **项目 state 历史** `[S]`: MAOFIELD_PROJECT_FULL_STATE_D17 + SECONDARY_VERIFY_D20×2 (已被本 STATE.md 取代)
- **v8 final archive** `[LOCKED]`: `experiments/exp018_cat/archive/v1.0_release_20260516/` (2 md + manifest.sha256 47/47)

## §3 历史区 — exp017_dialectics (157 md, 整组 ARCHIVE, 4/12-5/7)

> 早期 "辩证法四重检验" 实验 + arXiv v1 整稿 + 四方协作流水。整组 skip,仅 ★ 留历史 single-source。
- **核心实验** `[ARCHIVE]`: results/FINAL_REPORT ★ (Block I-IV 数据) + block{1,2,3}/block4_5 诊断
- **arXiv v1 稿** `[S]`: arxiv_v1_full + section1-6 + REVIEW_* (~30 份,v1 4/20,已演进到 v8)
- **Phase B Exp1** `[ARCHIVE]`: phase_b_exp1/phase_b_exp1_verdict ★ + EXPLORATION + GATE3_SUMMARY (14 份)
- **反题/Win/DS 协作流水** `[S]`: ANTITHESIS_RUN{3,4}/REVERSE_AUDIT_FINAL_LOCK ★ + LINUX_* (~50) + WIN_* (~22) + DEEPSEEK_V4_* (3)
- **理论 note/ACTION** `[ARCHIVE]`: DEEP_REASONING_TF_LIMITS_AGI + ACTION1-3 + RECOVERY_SNAPSHOT_{0413,0414}

## §4 早期实验 + session + 纪律 (38 md)

- **`docs/` 纪律** `[ACTIVE binding ★]`: D-1-five-disciplines + D-2-parallel + D-3-dialectical-reflection + three-machine-architecture + TIMELINE_D22_D60 (CLAUDE.md 外置正文,需全文时查这里) ‖ docs/README `[占位]`
- **early exp004-016** `[ARCHIVE]`: exp004 (8 md, 3D 反应扩散语义场) + exp016_diagnostic (6 md, 源场可分性诊断)。其余 exp 目录仅代码无 md
- **sessions/domain_positioning** `[S]`: 11 md (5/14 Nature 领域引导叙事 PART1-6,已被 D17 "pilot study 三 leg 不投 Nature" 取代)
- **顶层 DESKTOP 数学** `[ARCHIVE]`: DESKTOP_MATH_DEEP_ANALYSIS + SPOTCHECK_{R1,R2,R3,R5}_20260419 (5 份)
- **release metadata** `[ACTIVE skeleton]`: README + README_zh + NOTICE ‖ `[占位]`: paper/src/scripts/data 各 README + proposed_v0.1.1/DIFF_SUMMARY `[未 merge]`

---

*梳理: 4 zero-context agent (dppl/exp017/early) + bash (literature),2026-05-31 D31。新 session 读 STATE.md 即可开工,需 navigate 历史 md 时查本 catalog。*
