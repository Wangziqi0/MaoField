# MaoField MD_CATALOG — 全 ~429 md 分层梳理 (navigate reference)

> **STATE.md §7 指针目标。新 session 不必读全部** —— 看 §0 导航选 ACTIVE 核心 (~25 份),历史整组 SKIP (~250 份)。
> **维护**: 新增重要 md 归类追加;季度 review 把 SUPERSEDED 下沉历史区。本文件是 reference,不进每会话 context (STATE.md 才是 cold-start 必读)。
> **戳**: 2026-06-17 D617 晚 · HEAD `5608621` (+解耦线 [A−] 落盘复算 verdict 登记,落盘未 commit;实时以 `git log -1` 为准)
> **2026-06-22 导航补丁**: 新增仓库内 GPT-5.5 Pro 网页索引用研究证据地图 `GPT55_PRO_RESEARCH_INDEX_20260622.md`。它比本 catalog 更新，合并 D619 数学线 verdict、实际代码数学、exp020 C 证据库、exp019 superseded 关系和 do-not-revive guardrails；接 GPT/web 索引时优先读它。
> **2026-06-22 RAG 补丁**: 新增 GPT deep-research 报告目录 `docs/infra/gpt_deep_research/` 与 RAG 全量扫描目录 `docs/infra/rag_rebuild_20260622/`。报告是 claim source, not evidence; 数据只以 digest 进入默认 RAG, 原始 JSON/JSONL/log 仍需 direct verification。15:50 CST 追加第三份 `deep_research_mean_null_vector_field_killtest_20260622.md` 作为 proposed-method audit; 无新增 observed evidence。D622 post-q4 使用 node22 临时 bge-m3 GPU worker 完成默认 RAG 重建: report(3)/(4)/(6) + q4 runbook/smoke/adoption notes 已可由默认 RAG 定位。D623 report(7) refresh: 311 active md / 8603 chunks, report(7)+adoption note 已进入默认 RAG。D623 q4-gate refresh: 313 active md / 8615 chunks, `Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md` 已进入默认 RAG。D623 report(9) refresh: 316 active md / 8674 chunks, residual-field audit + adoption note 已进入默认 RAG。D623 report(11) refresh: 320 active md / 8734 chunks, hypercube audit + adoption note + zero-GPU feasibility audit 已进入默认 RAG。D623 report(13) refresh: 323 active md / 8780 chunks, current-repo hypercube audit + adoption note 已进入默认 RAG。D623 report(15) refresh: 327 active md / 8843 chunks, interaction-field memo + adoption note + smoke audit 已进入默认 RAG。D623 report(17) refresh: 331 active md / 8898 chunks, math-ore quotient residual audit + adoption note + hypercube prereg design 已进入默认 RAG。
> **2026-06-22 数学转向 gate 补丁**: 新增 `docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md` 与 `docs/infra/math_turn_20260622/`。当前 aggregate zero-GPU audit verdict=`insufficient_artifact`: F3 LOSO delta weak pass, matched-mean fail, rank/residual fail/blocked; 不授权新训练。16:58 追加 panel primary artifact coordination/prereg draft: 六 agent 审查已完成。17:08 追加 locked q4 schema/runbook: q4 primary schema locked; q8 sensitivity candidate not locked due empty bin。17:36 追加 generator smoke: manifest-only + seed1/gen0 one-checkpoint pass, old aggregate row reproduction abs diff all 0; no full panel generated。
> **2026-06-22 report(4) 补丁**: 新增 `docs/infra/gpt_deep_research/deep_research_math_turn_framework_gate_20260622.md` 与 `MATH_TURN_FRAMEWORK_ADOPTION_NOTE_20260622.md`。report(4)=external math-framework gate audit; repo-specific facts 对该 auditor blocked; 本地采用 keep/deflate/reject, 不授权训练。
> **2026-06-22 report(6) q4 strict audit 补丁**: 新增 `docs/infra/gpt_deep_research/deep_research_q4_panel_strict_audit_20260622.md` 与 `Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md`。report(6)=q4 panel bundle strict audit, 直接审上传 bundle / raw_wip, 不是新增实验结果；结论: full 50-checkpoint panel **not approved**, 当前 q4 schema + one-checkpoint smoke 仅够进入 implementation review。
> **2026-06-22 negative smoke 补丁**: 新增 `scripts/q4_panel_negative_smoke_20260622.py` + `PANEL_PRIMARY_ARTIFACT_NEGATIVE_SMOKE_20260622.md` + `negative_smoke_20260622.json`。验证 expected schema hash / builder hash / wrong split / source hash / q4 bin-size 错误均 fail fast; wording guard pass; no checkpoint loaded。
> **2026-06-22 multi-checkpoint smoke 补丁**: 新增 `PANEL_PRIMARY_ARTIFACT_MULTI_SMOKE_20260622.md` + `multi_checkpoint_smoke_20260622.json` + seed2/gen5, seed42/gen9 smoke manifests/aggregates。seed1/gen0 + seed2/gen5 + seed42/gen9 all reproduce old aggregate rows; no full panel generated。
> **2026-06-23 report(7) q4 object strict math audit 补丁**: 新增 `docs/infra/gpt_deep_research/deep_research_q4_object_strict_math_audit_20260623.md` 与 `Q4_OBJECT_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md`。report(7)=q4 object package 的严格数学审计; 结论加强 block: 当前实现只是 schema/smoke alignment, 不是数学推进；未来对象应是 fold-local q4 mean-null residual audit；full panel / training / glass-box claim 仍 blocked。
> **2026-06-23 q4 implementation gate 补丁**: 新增 `docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md` 与 `scripts/q4_full_panel_foldlocal_analysis.py`; `highorder_raw_logprob_panel.py` 增加 full-panel dry-run + PI approval-token guard。dry-run 只枚举 50 checkpoint, `no_checkpoint_loaded=true`; old rare/freq aggregate 被 separate analysis 拒收为 `invalid_artifact`。仍无 full panel / no training / no new result。
> **2026-06-23 report(9) q4 residual-field strict audit 补丁**: 新增 `docs/infra/gpt_deep_research/deep_research_q4_residual_field_strict_math_audit_20260623.md` 与 `Q4_RESIDUAL_FIELD_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md`。采纳对象定义 `r_i = u_i - <v,u_i>_w v`; 本地 q4 analysis 已补 projection geometry、fold-local scalar-slope residual、rank/noise 与 random mean-null projection multiplicity guard; legacy LOSO 脚本已拒收 q4 panel input。
> **2026-06-23 report(11) q4 hypercube extension strict audit 补丁**: 新增 `docs/infra/gpt_deep_research/deep_research_q4_hypercube_extension_strict_math_audit_20260623.md` 与 `Q4_HYPERCUBE_EXTENSION_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md`。本地新增 `scripts/build_hypercube_schema_20260623.py`、`scripts/q4_hypercube_zero_gpu_audit.py`、`hypercube_schema_q4_tokenpos4_20260623.json`、`Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.{json,md}`；verdict=`formal_prereg_only`, 不是 full panel / 不是科学结果。
> **2026-06-23 report(13) current-repo hypercube strict audit 补丁**: 新增 `docs/infra/gpt_deep_research/deep_research_q4_hypercube_current_repo_strict_audit_20260623.md` 与 `Q4_HYPERCUBE_CURRENT_REPO_STRICT_AUDIT_ADOPTION_NOTE_20260623.md`。report(13) 用 current repo/connector 复核 report(11) 边界: `Q_freq4 x B_tokenpos4` 只是 zero-GPU formal prereg coordinate system; no code change / no full panel / no training / no new loss。
> **2026-06-23 report(15) future math-object 补丁**: 新增 `docs/infra/gpt_deep_research/deep_research_future_math_objects_interaction_field_audit_20260623.md` 与 `FUTURE_MATH_OBJECTS_INTERACTION_FIELD_ADOPTION_NOTE_20260623.md`。采纳 weighted product-partition interaction field `I_i = Pi_{A_perp,w} K_i` 为 future math/audit direction；本地新增 `scripts/q4_hypercube_interaction_smoke_audit.py` 与 `Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.{json,md}`，verdict=`smoke_conjecture_only`，不是 full panel / 不是科学结果。默认 RAG 已刷新到 327 active md / 8843 chunks。
> **2026-06-23 report(17) math-ore quotient residual 补丁**: 新增 `docs/infra/gpt_deep_research/deep_research_math_ore_quotient_residual_strict_audit_20260623.md` 与 `MATH_ORE_QUOTIENT_RESIDUAL_ADOPTION_NOTE_20260623.md`。采纳去品牌化底层问题: 固定有限带权乘积空间与 nuisance 后, 检验 `R_t = Pi_{N_perp,w} K_t` 是否作为稳定非标量对象存活；当前 MaoField 仍只支持 `smoke_conjecture_only` / negative-centered。新增 `docs/infra/math_turn_20260622/HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md` 作为未来 zero-GPU kill-suite 设计, 不运行 full panel / 不训练 / 不授权 new loss。
> **2026-06-23 Mode A/Mode B 补丁**: 新增 `docs/infra/gpt_deep_research/GPT55_PRO_MODE_A_MATH_DISCOVERY_PROMPT_20260623.md` 与 `scripts/q4_hypercube_interaction_prereg_analysis.py`。前者给 GPT-5.5 Pro 做去魅材料的自由数学发现；后者是 future-only q4 x token-position interaction prereg gate skeleton, 无 future aggregate 时 `insufficient_artifact`, 旧 q4 aggregate `invalid_artifact`, strongest verdict=`eligible_for_next_design_review_only`。不运行 full panel / 不训练 / 不授权 new loss；RAG refresh 待后续完成。
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
| **GPT-5.5 Pro 网页索引入口 ★** | `GPT55_PRO_RESEARCH_INDEX_20260622.md` = 仓库内脱敏研究证据地图; 合并 Claude 数学交接 + 实际 code math + exp019/exp020 verdict + superseded/do-not-revive guardrails |
| **GPT deep-research 报告 ★** | `docs/infra/gpt_deep_research/` = GPT/PRO claim-source reports + adoption notes; report(3)=mean-null vector-field / LOSO-rank kill-test proposed audit; report(4)=external math-framework gate audit, repo facts blocked for auditor; report(6)=q4 strict bundle audit, full 50-checkpoint panel **not approved**; report(7)=q4 object strict math audit, rejects current implemented artifact as math advance and defines future fold-local q4 mean-null residual audit target; report(9)=q4 residual-field strict audit, adopts `r_i = u_i - <v,u_i>_w v` plus random projection multiplicity guard; report(11)=q4 residual-field hypercube extension audit, zero-GPU formal prereg only; report(13)=current-repo hypercube audit, confirms zero-GPU-only / no code authorization; report(15)=future math-object interaction-field memo + smoke reproduction, verdict=`smoke_conjecture_only`; report(17)=math-ore quotient residual strict audit, adopts `R_t = Pi_{N_perp,w} K_t` object-existence problem; `GPT55_PRO_MODE_A_MATH_DISCOVERY_PROMPT_20260623.md`=下一轮 Mode A 提示词; 均需回查 code/log/verdict/JSON |
| **RAG 重建 / 数据 digest ★** | `docs/infra/rag_rebuild_20260622/` + `scripts/rag_scan_maofield.py` + `scripts/rag_rebuild_maofield_36.sh` + `scripts/rag_rebuild_node22_runner.sh`; D623 report(17) refresh 后扫描 7804 files, 默认索引 331 active md / 8898 chunks + `maofield_data_digest_20260622.md`; node22 vector rebuild/refresh 记录见 `NODE22_VECTOR_REBUILD_20260622.md`、`NODE22_VECTOR_REFRESH_REPORT7_20260623.md`、`NODE22_VECTOR_REFRESH_Q4_GATE_20260623.md`、`NODE22_VECTOR_REFRESH_REPORT9_20260623.md`、`NODE22_VECTOR_REFRESH_REPORT11_20260623.md`、`NODE22_VECTOR_REFRESH_REPORT13_20260623.md`、`NODE22_VECTOR_REFRESH_REPORT15_20260623.md`、`NODE22_VECTOR_REFRESH_REPORT17_20260623.md`; 原始数据不直接入向量 |
| **当前实验收敛 + 数学转向 gate ★** | `docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md` + `docs/infra/math_turn_20260622/MATH_TURN_LOSO_AUDIT_VERDICT_20260622.md` + `docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_{COORDINATION,PREREG_DRAFT,RUNBOOK,SMOKE,NEGATIVE_SMOKE,MULTI_SMOKE}_20260622.md` + `docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md` + `docs/infra/math_turn_20260622/HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md` + `docs/infra/math_turn_20260622/panel_schema_freq_q4_audit_targets_20260622.json` + `docs/infra/math_turn_20260622/hypercube_schema_q4_tokenpos4_20260623.json` + `docs/infra/math_turn_20260622/Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.{json,md}` + `docs/infra/math_turn_20260622/Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.{json,md}` + `scripts/{math_turn_loso_audit.py,build_panel_schema_20260622.py,build_hypercube_schema_20260623.py,q4_panel_negative_smoke_20260622.py,q4_full_panel_foldlocal_analysis.py,q4_hypercube_zero_gpu_audit.py,q4_hypercube_interaction_smoke_audit.py,q4_hypercube_interaction_prereg_analysis.py}` + `experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py` + `experiments/exp020_metric_stress_test/panel_primary_20260622/`; zero-GPU aggregate verdict=`insufficient_artifact`; q4 schema/runbook locked, one-checkpoint + negative + multi-checkpoint smoke pass; D623 full-panel dry-run + approval guard + separate fold-local analysis path implemented; report(9) residual-field guard incorporated; report(11)/(13) hypercube feasibility verdict=`formal_prereg_only`; report(15) interaction-field smoke verdict=`smoke_conjecture_only`; report(17) math-ore object-existence problem adopted; Mode B future-only skeleton rejects missing/old aggregates; still no full panel / no training / no new result |

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
- **`docs/infra` RAG/GPT 接管** `[ACTIVE ★]`: `gpt_deep_research/` GPT/PRO reports + adoption notes(外部 claim source / bundle audit) + `rag_rebuild_20260622/` 全量扫描 inventory/digest/file-list; 默认 RAG 只索引 active md + digest,不直接嵌入 raw data
- **early exp004-016** `[ARCHIVE]`: exp004 (8 md, 3D 反应扩散语义场) + exp016_diagnostic (6 md, 源场可分性诊断)。其余 exp 目录仅代码无 md
- **sessions/domain_positioning** `[S]`: 11 md (5/14 Nature 领域引导叙事 PART1-6,已被 D17 "pilot study 三 leg 不投 Nature" 取代)
- **顶层 DESKTOP 数学** `[ARCHIVE]`: DESKTOP_MATH_DEEP_ANALYSIS + SPOTCHECK_{R1,R2,R3,R5}_20260419 (5 份)
- **release metadata** `[ACTIVE skeleton]`: README + README_zh + NOTICE ‖ `[占位]`: paper/src/scripts/data 各 README + proposed_v0.1.1/DIFF_SUMMARY `[未 merge]`

---

*梳理: 4 zero-context agent (dppl/exp017/early) + bash (literature),2026-05-31 D31。新 session 读 STATE.md 即可开工,需 navigate 历史 md 时查本 catalog。*
