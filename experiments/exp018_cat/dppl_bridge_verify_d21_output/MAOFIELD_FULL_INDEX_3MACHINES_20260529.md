# MaoField 跨三机全量索引 master (给 PI 后续深究用) — 2026-05-29 (D29)

> **本文件性质**: 跨三机 (7B13 + 9070XT/22 + 5060-Win/19) 全量 catalog + 状态标记 master 索引。
> **第一优先 = completeness**: 宁可标 `[未能访问/待补]` 也绝不静默遗漏 (见 §7 自检)。
> **read-only 产出**: 0 commit / 0 push / 0 launch / 0 ssh-write (ssh 仅 find/ls/wc/du/sha256sum/cat 小文件)。仅写本 1 个 output md。
> **不下 paper-level 结论**: 本文件只 catalog + 状态标记。是否超越基线 / collapse 是否被 mitigate / 接受率 / tier 升降 — 全留 PI + 关卡 3 反题三方决。
> 生成 agent: 额外 agent (Win 端来源, Opus), zero-context catalog 通道。

---

## §0 元数据

| 项 | 值 |
|---|---|
| 真实日期 `date '+%Y-%m-%d %H:%M:%S %Z'` | **2026-05-29 17:07:18 CST** (D29, D-day=2026-05-01 anchor, today=D28→实际标 D29 per CLAUDE.md latest) |
| 三机 | 7B13 = 192.168.31.36 (本机, Linux EPYC) · 22 = 192.168.31.22 (9070XT, ROCm gfx1201, hostname `amd-ONDA-B650M-W`) · 19 = 192.168.31.19 (5060 Laptop, Win/CUDA sm_120, hostname `LAPTOP-GVING7T3`) |
| 三机可达性 | 22 ✓ (ssh BatchMode read-only) · 19 ✓ (ssh BatchMode, dir/PowerShell/type read-only) · 均本 session 实测可达 |
| 基座模型 | `facebook/opt-125m` (全 run; `model.safetensors` = 500,979,600 B ≈ 478 MiB; 解释 fp16 OOM 的 OPT modeling traceback) |
| 7B13 全 md 计数 | **424 个** (`find ... -name '*.md'`) |
| 7B13 git HEAD | `0c4d4c6691e5...` `2026-05-29 16:07:07 +0800` "D29 验证级联归档: 跨三机数据完整性 + L0 多通道审视 + 元数据审计" |
| dppl_bridge_verify_d21_output 目录总大小 | 975 MB (含 candidate_c.nohup.log 等大 log) |
| binding | read-only; 0 commit/push/launch/ssh-write; paper v8 final 47/47 D17 锁定不动; 12 NOT-claim 撤回不复活; 反题 6 P0★ tier 不擅升降; D29 三 leg (arXiv+TMLR+KBS) 不动; 留 PI + 关卡 3 反题三方决 |

---

## §1 TOC (可导航)

- **§2 三机数据全景表** — 全部实验 run/cluster × (机器, dtype, seed/α/gen, jsonl record 数, checkpoint, 训练状态)
- **§3 全 md 分类索引** — 424 md (重点 dppl_bridge_verify_d21_output 110 个 + 5060 桌面 21 个), 10 类
- **§4 checkpoint sha256 分组** — 22 端 candidate_c 全 180 + 5060 桌面 6 + 边角, bit-identical(frozen) vs distinct(trained)
- **§5 跨机 map + 单点/缺失 flag** — 哪个 run 几台机器有副本; 哪些单点 ephemeral; 哪些被引用但缺失
- **§6 时间线** (按真实 mtime, D7→D29)
- **§7 completeness 自检** — 列出全部未能访问/待补项, 不静默遗漏

---

## §2 三机数据全景表

> 路径前缀: `EXP7B13` = `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat`; `22:` = `192.168.31.22:/tmp`; `19:` = `192.168.31.19:C:\Users\amd\Desktop\5060`。
> 训练状态判定来源 = D29 cascade 文档 + 本 session 直接 sha256/wc 复核; 不下 paper-level 结论, 仅 catalog 字节事实。

### §2.1 早期 armb / baseline 系列 (真训练, paper v8 负结果数据基底)

| # | run | 机器·路径 | mtime | record 数 | seed/α/gen 覆盖 | 训练状态 (字节事实) |
|---|---|---|---|---|---|---|
| E1 | shumailov_no_preserve s42 (主) | `EXP7B13/logs/shumailov_no_preserve_seed42_20260507_200657.jsonl` | 05-08 01:40 | 5057 B | s42 / baseline / 10 gen | 真训练 (动态轨迹, gen0≈36.73) |
| E2 | shumailov_no_preserve s42 (重跑) | `EXP7B13/logs/shumailov_no_preserve_seed42_20260508_092730.jsonl` | 05-08 14:01 | 5126 B | s42 / baseline / 10 gen | 真训练 (gen0≈36.52) |
| E3 | shumailov_preserve_10pct s42 | `EXP7B13/logs/shumailov_preserve_10pct_seed42_20260507_162206.jsonl` | 05-07 16:22 | 717 B | s42 / preserve / 短 | 真训练 (short) |
| E4 | armb_alpha0.0 s42 | `EXP7B13/logs/armb_alpha0.0_seed42_20260508_144612.jsonl` | 05-08 19:20 | 4800 B | s42 / α0 / 10 gen | 真训练 (10 distinct sha256/链, loss 收敛, 0 NaN) |
| E5 | armb_alpha1.0 s42 | `EXP7B13/logs/armb_alpha1.0_seed42_20260509_000459.jsonl` | 05-09 04:42 | 4799 B | s42 / α1 / 10 gen | 真训练 |
| E6 | armb_alpha5.0 s42 | `EXP7B13/logs/armb_alpha5.0_seed42_20260509_044342.jsonl` | 05-09 09:21 | 4800 B | s42 / α5 / 10 gen | 真训练 |
| E7 | armb_alpha10.0 s42 | `EXP7B13/logs/armb_alpha10.0_seed42_20260508_192435.jsonl` | 05-09 00:02 | 4837 B | s42 / α10 / 10 gen | 真训练 |
| E8 | armb_alpha50.0 s42 | `EXP7B13/logs/armb_alpha50.0_seed42_20260509_092134.jsonl` | 05-09 09:21 | 143 B | s42 / α50 / 早停 | 短/失败 (143 B = 仅 1-2 record) |
| E9 | phase1_robust multi-seed s0-4 α0/10 | `EXP7B13/logs/host22_backup_20260512/armb_alpha{0,10}.0_seed{1,2,3,4}_*.jsonl` (8 file) + `phase1_robust_*.audit.jsonl` | 05-12 20:00 (备份 mtime) | 各 ~4.1-5.0 KB | s{0-4} / α{0,10} / 10 gen | 真训练 (paper v8 F3 multi-seed 基, N=5/4) |

  - **early armb 备份副本**: `EXP7B13/archive/v1.0_release_20260516/chain_logs/*.jsonl` (17 jsonl, 内容与 logs/ 同名一致, 含 seed0 链 `armb_alpha0.0_seed0_20260509_203605.jsonl`)
  - **总计早期 jsonl 副本**: 同一批数据在 7B13 有 **3 处副本** (`logs/` + `logs/host22_backup_20260512/` + `archive/v1.0_release_20260516/chain_logs/`)

### §2.2 candidate_c (22, 9070XT fp16, N=180) — 全冻/NaN (不可用于定量结论)

| 项 | 值 (字节事实, 本 session 复核) |
|---|---|
| 主 jsonl | `22:/tmp/dppl_bridge_verify/output/candidate_c/candidate_c_20260522_203837.jsonl` |
| record 数 | **186 行** (含 run_start 等非 chain_gen_done 行; 180 = 18 链 × 10 gen 的 chain_gen_done) |
| 7B13 副本 | `EXP7B13/dppl_bridge_verify_d21_output/candidate_c/candidate_c_20260522_203837.jsonl` (335356 B, 05-26 23:01) |
| a1_ppl=null | **147 / 186** (≈79% null) |
| a1_ppl 非 null | 33 / 186 |
| seed/α/gen 覆盖 | seed {42,137,271,7,1337,2024} × α {0.0, 5.0, 10.0} × gen 0-9 = 18 链 × 10 |
| checkpoint | **180 model.safetensors** (`.../candidate_c/checkpoints/`); 仅 **52 distinct hash** (见 §4) |
| grad_norm nan (nohup) | `candidate_c.nohup.log` 命中 **2306**; `_resume_d24` 957; `_resume_d25` 1856 (合计 5119 行级命中) |
| nohup logs | `candidate_c.nohup.log` 16.4 MB · `_resume_d24.nohup.log` 6.6 MB · `_resume_d25.nohup.log` 12.8 MB · (7B13 副本 `candidate_c.nohup.log` 5.3 MB) |
| 训练状态 | **frozen / NaN** (GradScaler skip → optimizer 不 update; "跑满算力没学到", 每 cell ~34 min 跑满 forward+backward) |
| 进度快照 | `EXP7B13/.../candidate_c/progress_snapshot_{10..80}.md` (8 个, 各 169 B, 05-23~24) |

### §2.3 candidate_c 衍生 cell (22, fp32, 正交 NaN bug) — 单点 ephemeral

| run | 机器·路径 | record 数 | seed/α/gen | 状态 |
|---|---|---|---|---|
| cell_B (fp32) | `22:/tmp/dppl_bridge_cell_B/output/candidate_c_20260525_103458.jsonl` | 3669 B | s42/α0/1gen | NaN/失败 (fp32 ROCm bug) |
| cell_B_retry_B | `22:/tmp/dppl_bridge_cell_B_retry_B/output/candidate_c_20260525_104441.jsonl` | 353 B | s42/α0 | 极短/失败 |
| cell_B_C (fp32) | `22:/tmp/dppl_bridge_cell_B_C/output/candidate_c_20260525_105513.jsonl` | **1730 行** (a1_ppl null 1/3 在 chain 行) | s42/α0/1gen | NaN (`a1_ppl=null/val_loss=null`); 1 model.safetensors |
| cell_B_C nohup | `22:/tmp/dppl_bridge_cell_B_C/cell_B_C.nohup.log` | 118636 B | — | — |
| candidate_c_preflight | `22:/tmp/dppl_bridge_verify/output/candidate_c_preflight/candidate_c_20260522_203111.jsonl` | 4 行 | s42/α10/2gen | preflight (2 safetensors) |
| verify_smoke | `22:/tmp/dppl_bridge_verify_smoke/candidate_c_smoke/candidate_c_20260522_203837.jsonl` | 167686 B | — | smoke 副本 |

### §2.4 main run (22, D22) + pilot (22, D21)

| run | 路径 | record 数 | 状态 |
|---|---|---|---|
| main_D22 | `22:/tmp/dppl_bridge_verify/output/main/main_D22.jsonl` | **162 行** (+ main_D22.log 178771 B + watchdog.audit.jsonl 598 B) | 与 candidate_c 同期 9070XT run |
| pilot_D21 | `22:/tmp/dppl_bridge_verify/output/pilot_D21_seed1_gen5.jsonl` | 4 行 (+ pilot_D21.log 3325 B + .console.log 2652 B) | D21 桌面 pilot |

### §2.5 5060 桌面 (19, Win/CUDA) — fp32 + fp16 健康对照 (cross-platform 对照证据)

| run | 路径 `19:` | jsonl record | seed/α/gen | safetensors | 状态 (字节事实) |
|---|---|---|---|---|---|
| E0_disentangle_S3 (fp32) | `E0_disentangle_S3/candidate_c_20260525_160321.jsonl` | 4 行 (7980 B) | s42/α0/2gen | 2 (gen0 `BD88E350`, gen1 `C663D66B`) **distinct** | 健康 (g0=36.536→g1=78.572, +115%) |
| SMOKE fp16 crosscheck | `SMOKE_5060_FP16_CROSSCHECK_GRADSCALER/candidate_c_20260527_220312.jsonl` | 6 行 (8497 B) | s42/α0/2gen | 2 (gen0 `7463003E`, gen1 `FB608459`) **distinct** | 健康 (g0=36.5377→g1=78.0735, +113.7%, 无 GradScaler skip) |
| SMOKE fp16 (早 run) | `SMOKE_5060_FP16_CROSSCHECK_GRADSCALER/candidate_c_20260527_210536.jsonl` | 3 行 (5622 B) | s42/α0 | (并入上目录) | 同上目录早 run |
| smoke_fp32 (D24) | `smoke_fp32/candidate_c_20260524_170933.jsonl` (3 行 1305 B) + `..._173559.jsonl` (3 行 4118 B) | 3+3 行 | s42/α0/1gen | 1 (gen0 `BD88E350`) | 健康 (gen0 与 E0 同 hash) |
| smoke_fp32_gc_R1 (D25) | `smoke_fp32_gc_R1_D25/candidate_c_20260525_113506.jsonl` | 3 行 (4143 B) | s42/α0/1gen | 1 (gen0 `BD88E350`) | 健康 (gen0 同 hash) |
| smoke_fp32_N_seed (D25) | `smoke_fp32_N_seed_D25/candidate_c_20260525_092037.jsonl` | 1 行 (401 B) | s1337/α0/gen0 卡 24% 被 kill | 0 (gen0 未完成无 safetensors?) | 1-cell smoke (顺带印证 N_total=1460 步/代) |

  - **5060 桌面 log**: `E0_launch.log` 300 KB · `SMOKE..._err_gen1.log` 184 KB · `..._err_v2.log` 106 KB · `smoke_fp32_relaunch.log` 119 KB · `smoke_fp32_gc_R1_launch.log` 109 KB · 等 (全 §2.5 log 见 §6 时间线)
  - **5060 代码副本**: `19:maofield_5060_work/experiments/exp018_cat/{src,scripts,configs}` (cat_trainer.py / contradiction_loss.py / train_one_generation.py 等全套 + 3 yaml config + wikitext-2 数据集 arrow 缓存)

### §2.6 历史实验 (exp001-017, 早于 exp018 CAT) — 非 self-iteration chain, 简列

| cluster | 机器·路径 | 内容 | 状态 |
|---|---|---|---|
| exp001-012 | `22:experiments/exp00*` (Shape-CFD 衍生, 在 22 home) + 各 `*_results.json` | NFCorpus/query evolution/SVD atoms/PQ 等检索实验 | 历史归档 (Shape-CFD→MaoField 过渡期) |
| exp015/016_diagnostic | `EXP7B13/../exp016_diagnostic/` | reranker 诊断, phase1-6 summary | 历史归档 (6 md) |
| exp017_dialectics | `EXP7B13/../exp017_dialectics/` | 辩证法范式 + 三方协作 (157 md, 见 §3) | 历史归档 (paper v1-v8 trajectory) |

  - **22 端大 sqlite**: `22:experiments/evolved_query_*.sqlite` + `expanded_query_*.sqlite` (各 ~330-455 MB, 共 ~14 个, query evolution 检索实验产物, 历史) — 单点在 22, 非 self-iteration chain 数据

---

## §3 全 md 分类索引

> 7B13 共 **424 md**, 按目录: exp018_cat 221 · exp017_dialectics 157 · sessions/domain_positioning 11 · exp004 8 · exp016 6 · docs 5 · 顶层/其他 ~16。
> 本 §重点穷举 **dppl_bridge_verify_d21_output (110 md)** + **5060 桌面 (21 md)** + exp018_cat 顶层 + docs;exp017 (157) 因属历史 paper trajectory 仅按类汇总 (PI 深究可 `find exp017_dialectics -name '*.md'`)。
> 分类: L0=数学证明 · EXP=实验结果 · AUDIT=数据审计 · DEC=决策包 · PHIL=哲学 · IDX=索引 · HO=handoff · PAP=paper · ANTI=反题audit · LIT=文献 · MISC=其他。

### §3.1 dppl_bridge_verify_d21_output (110 md, 全枚举, mtime + 大小 + 分类 + 1 行描述)

| mtime | 大小 | 文件 | 类 | 描述 |
|---|---|---|---|---|
| 05-21 11:46 | 6101 | ACK_D21_PREREQ.md | HO | D21 22 端 prereq ack |
| 05-21 13:39 | 9238 | ACK_D21_INSTALL_DONE.md | HO | D21 ROCm torch 安装完成 ack |
| 05-21 15:20 | 12343 | ACK_D21_HANDOFF_RECEIVED.md | HO | D21 handoff 接收 ack |
| 05-24 14:43 | 28638 | ACK_D24_5060_PREREQ.md | HO | D24 5060 prereq (基座/env 确认) |
| 05-26 11:50 | 11429 | ACK_D26_22_END_WAKE_SYNC_*.md | HO | D26 22 端 wake sync |
| 05-26 21:19 | 14024 | ACK_D26_EVENING_22_END_SYNC_*.md | HO | D26 evening 22 sync |
| 05-26 21:18 | 8927 | ACK_EXTRA_AGENT_D26_*.md | HO | D26 额外 agent ack |
| 05-21 16:52 | 19221 | ANTITHESIS_AUDIT_D21_16_REFLEXIVE_INSIGHTS_*.md | ANTI | D21 反题 16 reflexive insight audit |
| 05-22 17:13 | 38830 | ANTITHESIS_AUDIT_D22_FULL_FLOW_*.md | ANTI | D22 反题 full flow audit |
| 05-24 17:07 | 26428 | ANTITHESIS_AUDIT_D24_5060_CATCH_P0G_*.md | ANTI | D24 反题 catch P0★-G (5060 FATAL) |
| 05-25 09:21 | 36508 | ANTITHESIS_AUDIT_D25_7TH_LAYER_FRAMING_*.md | ANTI | D25 反题 7th-layer framing audit |
| 05-27 13:27 | 22700 | ANTITHESIS_D26_GATE3_CHANNEL_D_VERDICT_*.md | ANTI | 关卡3 通道D verdict (cross-layer counter-factual) |
| 05-24 21:17 | 36445 | AUDIT_D24_EXP_HISTORY_BINARY_VERIFY_*.md | AUDIT | D24 实验历史 binary verify (P0★-G surface) |
| 05-25 17:17 | 11446 | CANDIDATE_DISCRETE_PPL_ATTRACTOR_D25_*.md | EXP | discrete-PPL attractor 候选 (Q1 trivial attractor) |
| 05-25 17:28 | 15937 | CANDIDATE_RIDDLED_BASIN_MIRROR_DUAL_D25_*.md | EXP | riddled basin mirror-dual 候选 (后 P0 inflate flag) |
| 05-24 17:07 | 13535 | CROSS_CHANNEL_VERIFY_22_5060_D24_*.md | AUDIT | 22 vs 5060 cross-channel verify |
| 05-28 10:12 | 18303 | D28_4ENDPOINT_VERIFICATION_AUDIT_*.md | AUDIT | D28 4-endpoint 验证 audit |
| 05-28 13:34 | 46033 | D28_CROSS_VERIFY_ABLATION_REPORT_*.md | AUDIT | D28 cross-verify ablation report |
| 05-28 17:03 | 35989 | D28_EXPERIMENTAL_DEEP_AUDIT_*.md | AUDIT | D28 实验深度 audit |
| 05-28 13:52 | 34354 | D28_EXPERIMENT_INVENTORY_AND_SUFFICIENCY_AUDIT_*.md | AUDIT | D28 实验 inventory + sufficiency (cluster 编号 schema 源) |
| 05-28 16:48 | 41470 | D28_MATH_RIGOROUS_AUDIT_*.md | L0 | D28 数学严格 audit |
| 05-28 16:48 | 30772 | D28_MD_CROSS_CHANNEL_AUDIT_*.md | AUDIT | D28 md cross-channel audit |
| 05-28 16:49 | 49917 | D28_MLRC_PAPER_DRAFT_*.md | PAP | D28 MLRC paper draft |
| 05-28 14:20 | 38034 | D28_VENUE_SCOUTING_MID_JUNE_*.md | DEC | D28 venue scouting (mid-June) |
| **05-29 15:09** | 9728 | **D29_VERIFICATION_CASCADE_UPDATE_*.md** | AUDIT | **D29 cascade 差异日志** (C3 退化 ~99% sha256 双通道; cluster-11 NO-GO 撤销; candidate_c 元数据补全) |
| **05-29 14:29** | 22886 | **DATA_COMPLETENESS_AUDIT_INDEP_*.md** | AUDIT | **zero-context 数据完整性校验** (只看 jsonl+log+sha256; 全 chain inventory) |
| 05-26 19:10 | 8490 | DEEPER_INSIGHT_D26_CONVERSATION_*.md | PHIL | D26 deeper insight 对话 |
| 05-27 12:10 | 3297 | DEEPSEEK_CHECKPOINT3_FINAL_*.md | DEC | DS 关卡3 final |
| 05-27 12:04 | 23907 | DEEPSEEK_CHECKPOINT3_LANGUAGE_AUDIT_*.md | ANTI | DS 关卡3 语言 audit |
| 05-27 12:07 | 34563 | DEEPSEEK_CHECKPOINT3_STRATEGY_AUDIT_*.md | DEC | DS 关卡3 策略 audit |
| 05-25 18:02 | 36080 | DEEP_RESEARCH_INTEGRATION_D25_*.md | LIT | D25 deep research 整合 |
| 05-27 10:40 | 24176 | DEEP_SYNTHESIS_D26_EVENING_*.md | PHIL | D26 evening deep synthesis |
| 05-26 13:28 | 2022 | DIAGNOSE_D26_NAN_CASCADE_SAME_SOURCE_D23_*.md | EXP | D26 NaN cascade = same-source D23 诊断 |
| 05-21 13:10 | 4597 | DIRECTIVE_D21_FIX_INSTALL_RELAY.md | HO | D21 install fix relay |
| 05-21 14:01 | 6380 | DIRECTIVE_D21_FIX_R3_RELAY.md | HO | D21 fix R3 relay |
| 05-22 18:42 | 11725 | DIRECTIVE_D22_CANDIDATE_C_AUTO_LAUNCH.md | HO | D22 candidate_c auto-launch directive |
| 05-27 10:26 | 300448 | E0_launch.log (**非 md, log**) | EXP | (5060 E0 launch log 的 7B13 副本) |
| **05-29 17:06** | 5628 | **E1E2_DECISION_PACKAGE_VERIFIED_*.md** | DEC | **E1/E2 决策包 verified 版** (4 决策卡点; fp16冻/fp32死/5060健康 验过) |
| 05-21 12:00 | 7528 | ESCALATE_D21_INSTALL_FAIL.md | HO | D21 install fail escalate |
| 05-21 13:24 | 10680 | ESCALATE_D21_INSTALL_FAIL_R2.md | HO | D21 install fail R2 |
| 05-21 13:47 | 8975 | ESCALATE_D21_PILOT_FAIL_R3.md | HO | D21 pilot fail R3 |
| 05-25 18:02 | 14553 | EXPERIMENT_ADDITION_CANDIDATE_D25_*.md | EXP | D25 实验追加候选 |
| 05-21 20:16 | 7702 | EXPERIMENT_REFRAME_D21_18_METHODOLOGICAL_CATCH_*.md | PHIL | D21 17:55 方法论 catch (4 path A/B/C/D) |
| 05-22 14:59 | 40718 | EXP_DESIGN_4PATH_METHODOLOGICAL_D22_*.md | EXP | D22 4-path 实验设计 |
| 05-22 17:28 | 10724 | EXP_LAUNCH_PLAN_PATH_AC_D22_*.md | EXP | D22 path A+C launch plan |
| 05-26 15:59 | 17310 | EXP_PLAN_LATEST_D26.md | EXP | D26 latest 实验 plan |
| 05-26 15:28 | 26615 | EXTRA_AGENT_D26_MULTI_AGENT_AUDIT_FOR_7B13_MAIN_*.md | AUDIT | D26 额外 agent multi-agent audit |
| 05-27 15:00 | 25791 | E_NEW_2_EVAL_PIPELINE_AUDIT_*.md | AUDIT | E_NEW_2 评估 pipeline audit |
| **05-29 15:59** | 7727 | **HANDOFF_7B13_D29_ACTIONS_*.md** | HO | **D29 → 7B13 主会话 action 交接** (A1备份/A2 git入库/A3实验ack) |
| 05-24 14:23 | 8976 | HANDOFF_D24_TO_5060_*.md | HO | D24 → 5060 handoff |
| 05-22 14:59 | 47886 | INDEX_MD_D22_*.md | IDX | D22 md 索引 |
| 05-29 09:37 | 29775 | L0_PROOF_PROMPT_OPUS48_D28_*.md | L0 | L0 证明 prompt (Opus 4.8) |
| 05-22 20:41 | 9748 | LAUNCH_CANDIDATE_C_STARTED_D22.md | EXP | candidate_c launch 起始 |
| 05-22 17:48 | 12005 | LAUNCH_D22_MAIN_RUN_STARTED.md | EXP | D22 main run launch |
| 05-21 17:46 | 70653 | LITERATURE_SEARCH_A_ML_CRITICAL_AGI_D21_*.md | LIT | 文献 A (ML/critical/AGI, 94 paper) |
| 05-21 17:35 | 84794 | LITERATURE_SEARCH_B_PHILOSOPHY_SOCIOLOGY_DIAMAT_SR_D21_*.md | LIT | 文献 B (哲学/社会学/diamat/SR) |
| 05-22 14:59 | 51100 | LITERATURE_SEARCH_C_FULL_CRAWL_D22_*.md | LIT | 文献 C full crawl |
| 05-27 15:17 | 22905 | LITERATURE_SEARCH_PAPER_V9_ANCHORS_D27_*.md | LIT | paper v9 anchor 文献 |
| 05-22 18:07 | 19181 | MAIN_VERDICT_D22.md | EXP | D22 main run verdict |
| 05-26 20:30 | 55095 | MAOFIELD_D26_MULTIAGENT_DEEP_DIGEST_*.md | AUDIT | D26 multi-agent deep digest |
| 05-26 20:26 | 23379 | MAOFIELD_D26_NEW_FILE_INVENTORY_*.md | IDX | D26 new file inventory |
| 05-26 20:37 | 36226 | MAOFIELD_D26_STRATEGIC_PANORAMA_REPORT_*.md | DEC | D26 战略全景 (530 行整合) |
| **05-29 14:59** | 14307 | **MAOFIELD_EXP_METADATA_INVENTORY_5060DESKTOP_*.md** | AUDIT | **agent Y: 5060 桌面元数据 inventory** (基座 opt-125m / env 确认) |
| **05-29 15:00** | 17056 | **MAOFIELD_EXP_METADATA_INVENTORY_LINUX22_*.md** | AUDIT | **agent X: 7B13+22 元数据 inventory** (180 ckpt + early-armb + main) |
| **05-29 15:13** | 8176 | **MAOFIELD_EXP_METADATA_MASTER_*.md** | AUDIT/IDX | **merge X+Y 元数据 master** |
| 05-26 16:55 | 48868 | MAOFIELD_FULL_DATA_AUDIT_*.md | AUDIT | D26 full data audit |
| **05-29 12:16** | 11672 | **MAOFIELD_GATE_DATA_INTEGRITY_*.md** | AUDIT | **L0 GATE 数据完整性 forensics** (NO-GO 数据不得 build on) |
| 05-26 20:30 | 27615 | MAOFIELD_GLOBAL_FILE_INDEX_*.md | IDX | D26 global file index |
| **05-29 12:16** | 23925 | **MAOFIELD_INDEX_EXP_LOGIC_*.md** | IDX | **D29 实验历程+逻辑 2 维索引** (cluster 编号 schema) |
| **05-29 12:16** | 29893 | **MAOFIELD_INDEX_MATH_PROP_*.md** | IDX | **D29 数学+命题 2 维索引** (每命题三元组 tier/源/通道) |
| **05-29 12:17** | 30443 | **MAOFIELD_INDEX_PHILO_ARG_*.md** | IDX | **D29 哲学+论点 2 维索引** (retrospective/starting-form/FAIL/retracted 标注) |
| **05-29 12:36** | 11479 | **MAOFIELD_L0_FULL_ROUND1_SUMMARY_*.md** | L0 | **L0 第1轮全量: 0 unconditional close / 2 conditional / 3 negative / 3 FAIL** |
| **05-29 11:28** | 28777 | **MAOFIELD_L0_L0-1_RIGOROUS_PROOF_*.md** | L0 | L0-1 严格证明 |
| **05-29 11:28** | 34293 | **MAOFIELD_L0_L0-2_RIGOROUS_PROOF_*.md** | L0 | L0-2 严格证明 |
| **05-29 10:36** | 32070 | **MAOFIELD_L0_L0-3_RIGOROUS_PROOF_*.md** | L0 | L0-3 严格证明 |
| **05-29 10:36** | 31083 | **MAOFIELD_L0_L0-4_RIGOROUS_PROOF_*.md** | L0 | L0-4 严格证明 |
| **05-29 10:42** | 14596 | **MAOFIELD_L0_L0-5-6-7_FAIL_VERDICT_*.md** | L0 | **L0-5/6/7 honest FAIL verdict** (3 条 inflate 最高危, 第1轮不能闭) |
| **05-29 11:28** | 18193 | **MAOFIELD_L0_L0-8_RIGOROUS_PROOF_*.md** | L0 | L0-8 严格证明 |
| **05-29 11:01** | 12640 | **MAOFIELD_L0_ROUND1_ADVERSARIAL_VERIFY_*.md** | L0 | L0 第1轮对抗验证 |
| **05-29 10:51** | 8225 | **MAOFIELD_L0_ROUND1_VERIFY_PROMPT_*.md** | L0 | L0 第1轮 verify prompt |
| **05-29 12:30** | 30593 | **MAOFIELD_L0_ROUND2_CHANNEL_P_*.md** | L0 | **L0 第2轮 通道P (证明)** (C3 fractal-vs-退化 binary 判定) |
| **05-29 12:29** | 17426 | **MAOFIELD_L0_ROUND2_CHANNEL_V_*.md** | L0 | **L0 第2轮 通道V (对抗复核)** (价值在 disagree) |
| **05-29 14:47** | 11359 | **MAOFIELD_L0_ROUND2_INTEGRATION_*.md** | L0 | **L0 第2轮整合** (含 D29 LATE UPDATE banner, 3 处更正指向 cascade) |
| 05-26 18:10 | 51496 | MAOFIELD_LITERATURE_SEARCH_D26_ATTEMPT1.md | LIT | D26 文献 search attempt1 |
| 05-26 17:57 | 46250 | MAOFIELD_MATH_MULTI_CHANNEL_ANALYSIS_D26_ATTEMPT1.md | L0 | D26 数学 multi-channel 分析 |
| 05-26 19:54 | 18371 | MAOFIELD_MATH_RIGOROUS_PROOF_D26_ATTEMPT1.md | L0 | D26 数学严格证明 |
| 05-26 19:47 | 25180 | MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S1_S2_ATTEMPT1.md | L0 | D26 证明 S1-S2 |
| 05-26 19:48 | 26007 | MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S3_ATTEMPT1.md | L0 | D26 证明 S3 |
| 05-26 19:48 | 25904 | MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S4_ATTEMPT1.md | L0 | D26 证明 S4 |
| 05-26 19:51 | 16867 | MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S5_ATTEMPT1.md | L0 | D26 证明 S5 |
| 05-26 17:24 | 38123 | MAOFIELD_MULTI_CHANNEL_ANALYSIS_D26_ATTEMPT1.md | AUDIT | D26 multi-channel 分析 |
| 05-26 15:59 | 21290 | MATH_DIRECTION_LATEST_D26.md | L0 | D26 latest 数学方向 |
| 05-25 09:30 | 24247 | MATH_VERIFY_D25_GRADSCALER_SKIP_*.md | L0/EXP | **GradScaler skip 数学机制 verify** (fp16 冻结 root cause) |
| 05-26 16:01 | 23900 | MD_INDEX_LATEST_D26.md | IDX | D26 latest md 索引 |
| 05-24 17:36 | 7936 | MONITORING_D24_17_35_*.md | EXP | D24 监控 |
| 05-27 17:41 | 21093 | NATURE_EDITOR_DESK_REVIEW_SIMULATION_*.md | DEC | Nature 主编 desk review 模拟 |
| 05-27 21:10 | 35164 | PAPER_V81_FOOTNOTE_DRAFT_WIN_LEAD_*.md | PAP | paper v8.1 footnote draft (Win lead) |
| 05-25 18:02 | 14856 | PAPER_V9_DRAFT_CANDIDATE_D25_*.md | PAP | paper v9 draft 候选 |
| 05-27 21:22 | 39356 | PAPER_V9_SKELETON_DRAFT_D27_*.md | PAP | paper v9 skeleton draft |
| 05-21 20:26 | 7634 | PARADIGM_REFRAME_D21_18_30_MITIGATION_INSUFFICIENT_CANDIDATE_*.md | PHIL | D21 18:30 paradigm reframe (mitigation insufficient 候选) |
| 05-22 15:46 | 49581 | PATH_AC_PRIOR_ART_DEEP_DIVE_D22_*.md | LIT | path A+C prior art deep dive |
| 05-26 15:59 | 25683 | PHILO_DIRECTION_LATEST_D26.md | PHIL | D26 latest 哲学方向 |
| 05-21 14:22 | 22057 | PILOT_VERDICT_D21.md | EXP | D21 pilot verdict |
| 05-22 20:35 | 18601 | PRE_FLIGHT_VERIFY_CANDIDATE_C_D22.md | EXP | candidate_c pre-flight verify |
| 05-24 14:56 | 10747 | PROGRESS_D24_5060_STAGE0_VAL_PPL.md | EXP | D24 5060 stage0 val PPL |
| 05-21 17:33 | 9006 | REFLEXIVE_INSIGHT_D21_17_DIALECTICAL_TOTALITY_CANDIDATE_*.md | PHIL | D21 17:00 dialectical totality 候选 |
| 05-22 17:28 | 11748 | RESEARCH_CHAIN_SPEC_D22_*.md | EXP | research chain spec |
| **05-29 14:27** | 16630 | **RESULTS_REDERIVATION_INDEP_*.md** | AUDIT | **zero-context 结果 re-derivation** (α 效应; 早期 armb vs candidate_c) |
| 05-25 13:18 | 9305 | RESULT_CELL_B_D25_*.md | EXP | cell B 结果 (fp32 NaN) |
| 05-25 13:24 | 9857 | RESUME_AFTER_CELL_B_AND_CUDA_CONTEXT_STALE_FAIL_D25_*.md | EXP | cell B 后 resume (CUDA ctx stale fail) |
| 05-24 16:54 | 9693 | RESUME_LAUNCH_D24_16_40_*.md | EXP | D24 resume launch |
| 05-27 21:24 | 34997 | ROCM_MIOPEN_TRACE_AUDIT_*.md | AUDIT | ROCm/MIOpen trace audit (gfx1201 bug) |
| 05-25 16:20 | 10716 | SESSION_CROSS_LAYER_INTEGRATION_D25_*.md | PHIL | D25 cross-layer 整合 |
| 05-28 09:40 | 9457 | SMOKE_5060_FP16_CROSSCHECK_GRADSCALER_*.md | EXP | 5060 fp16 crosscheck (健康对照) |
| 05-25 09:05 | 10710 | SMOKE_D24_5060_FP32_ISOLATED_TEST.md | EXP | D24 5060 fp32 隔离测试 |
| 05-25 19:40 | 10191 | SMOKE_E0_D25_5060_FP32_GC_2GEN_S3_DISENTANGLE_*.md | EXP | E0 fp32 2gen S3 disentangle (g0=36.536→g1=78.572) |
| 05-25 12:17 | 10705 | SMOKE_R1_D25_5060_FP32_GC_*.md | EXP | R1 5060 fp32 GC smoke |
| 05-21 13:54 | 12340 | SURFACE_D21_DESKTOP_CASCADE_CRASH.md | EXP | D21 桌面 cascade crash surface |
| 05-21 15:11 | 33429 | SURFACE_D21_DESKTOP_FIX_APPLIED.md | EXP | D21 桌面 fix applied |
| 05-23 10:43 | 9957 | SURFACE_D23_CANDIDATE_C_NAN_EXPLOSION.md | EXP | **D23 candidate_c NaN explosion surface** (Phase2 NaN root) |
| 05-24 17:17 | 16605 | SURFACE_D24_5060_FP32_LAUNCH_FAIL_TRANSFORMERS_VERSION_DIFF.md | EXP | D24 5060 fp32 launch fail (transformers 版本差) |
| 05-26 21:19 | 7034 | SYNC_5060_EVENING_ACK_F91F272_D26_*.md | HO | D26 5060 evening sync ack |
| 05-26 11:50 | 4540 | SYNC_D26_5060_WAKE_TRANSFORMERS_FIX_BINARY_ACK_*.md | HO | D26 5060 wake transformers fix ack |
| 05-24 15:43 | 11377 | TERMINATION_D24_15_33_PARTIAL_RUN_*.md | EXP | D24 partial run termination |
| 05-22 11:48 | 47600 | VENUE_EVAL_NEURIPS_NMI_D22_*.md | DEC | venue 评估 (NeurIPS/NMI; D17 决不投) |
| 05-23 13:03 | 12656 | VERIFY_D23_12_55_PROGRESS_CODE_*.md | EXP | D23 progress code verify |
| 05-25 15:38 | 17210 | WIN_3AGENT_AUDIT_D25_14_45_*.md | ANTI | Win 3-agent audit |
| 05-26 21:19 | 12643 | WIN_D26_EVENING_SYNC_ACK_17_10_*.md | HO | Win D26 evening sync ack |
| 05-26 14:03 | 29064 | WIN_D26_INTERNAL_REVIEW_REORG_13_58_*.md | DEC | Win D26 内部 review reorg |
| 05-26 11:51 | 5761 | WIN_D26_WAKE_SYNC_ACK_11_50_*.md | HO | Win D26 wake sync ack |
| 05-27 13:26 | 28335 | WIN_D27_GATE3_PHILO_JUDGEMENT_V81_FOOTNOTE_*.md | DEC/PHIL | Win 关卡3 哲学判读 (v8.1 footnote) |

  - **同目录非 md log** (catalog 完整性): `E0_launch.log` 300 KB · `install_rocm_torch*.log` (4 个) · `pilot_D21.log/.console.log` · `smoke_fp32*.log` (4 个: `_N_seed` 24817 B / `_gc_R1` 109344 B / `` 15886 B / `_relaunch` 118647 B)

### §3.2 5060 桌面 md (19, 21 个)

> 大部分是 7B13 同名文件的 PULL/副本 (跨机 sync), + 少量 5060 本地产出。

| mtime | 大小 | 文件 `19:` | 类 | 是否 7B13 有副本 |
|---|---|---|---|---|
| 05-24 14:42 | 28638 | ACK_D24_5060_PREREQ.md | HO | ✓ 同名在 7B13 |
| 05-24 14:22 | **0 B** | han.md | MISC | **空文件** (0 字节, 疑似占位/误建, flag) |
| 05-27 21:10 | 35164 | PAPER_V81_FOOTNOTE_DRAFT_WIN_LEAD_*.md | PAP | ✓ |
| 05-24 14:55 | 10747 | PROGRESS_D24_5060_STAGE0_VAL_PPL.md | EXP | ✓ |
| 05-27 21:05 | 22700 | PULL_ANTITHESIS_D26_GATE3_CHANNEL_D_VERDICT_*.md | ANTI | ✓ (PULL = 从主仓拉) |
| 05-27 21:05 | 3297 | PULL_DEEPSEEK_CHECKPOINT3_FINAL_*.md | DEC | ✓ |
| 05-27 13:21 | 24176 | PULL_DEEP_SYNTHESIS_D26_EVENING_*.md | PHIL | ✓ |
| 05-27 21:05 | 25791 | PULL_E_NEW_2_EVAL_PIPELINE_AUDIT_*.md | AUDIT | ✓ |
| 05-27 13:21 | 36226 | PULL_MAOFIELD_D26_STRATEGIC_PANORAMA_REPORT_*.md | DEC | ✓ |
| 05-25 09:05 | 10710 | SMOKE_D24_5060_FP32_ISOLATED_TEST.md | EXP | ✓ |
| 05-25 19:40 | 10191 | SMOKE_E0_D25_5060_FP32_GC_2GEN_S3_DISENTANGLE_*.md | EXP | ✓ |
| 05-25 12:17 | 10705 | SMOKE_R1_D25_5060_FP32_GC_*.md | EXP | ✓ |
| 05-24 17:17 | 16605 | SURFACE_D24_5060_FP32_LAUNCH_FAIL_*.md | EXP | ✓ |
| 05-26 21:19 | 7034 | SYNC_5060_EVENING_ACK_F91F272_D26_*.md | HO | ✓ |
| 05-26 11:49 | 4540 | SYNC_D26_5060_WAKE_TRANSFORMERS_FIX_BINARY_ACK_*.md | HO | ✓ |
| 05-25 15:38 | 17210 | WIN_3AGENT_AUDIT_D25_14_45_*.md | ANTI | ✓ |
| 05-26 21:19 | 12643 | WIN_D26_EVENING_SYNC_ACK_17_10_*.md | HO | ✓ |
| 05-26 14:02 | 29064 | WIN_D26_INTERNAL_REVIEW_REORG_13_58_*.md | DEC | ✓ |
| 05-26 11:51 | 5761 | WIN_D26_WAKE_SYNC_ACK_11_50_*.md | HO | ✓ |
| 05-27 13:26 | 28335 | WIN_D27_GATE3_PHILO_JUDGEMENT_V81_FOOTNOTE_*.md | DEC/PHIL | ✓ |
| 05-28 09:40 | 9457 | maofield_5060_work/.../SMOKE_5060_FP16_CROSSCHECK_GRADSCALER_*.md | EXP | ✓ (嵌在 5060 工作副本树内) |

### §3.3 exp018_cat 顶层 + docs + sessions (其余非 dppl md)

| mtime | 大小 | 文件 | 类 | 描述 |
|---|---|---|---|---|
| 05-07 15:23 | 2346 | `EXP7B13/README.md` | MISC | exp018_cat README |
| 05-07 15:57 | 10638 | `EXP7B13/SHUMAILOV_REPLICATION_README.md` | EXP | Shumailov 复现 README |
| 05-23 12:16 | 19261 | `docs/philosophy/D-3-dialectical-reflection.md` | PHIL | D-3 辩证反映论 work mode |
| 05-23 12:16 | 6186 | `docs/infra/three-machine-architecture.md` | MISC | 三机架构 doc |
| 05-26 14:18 | 7260 | `docs/discipline/D-1-five-disciplines.md` | MISC | D-1 五纪律 doc |
| 05-26 14:18 | 2056 | `docs/discipline/D-2-parallel.md` | MISC | D-2 三线 parallel doc |
| 05-26 14:19 | 2699 | `docs/TIMELINE_D22_D60.md` | IDX | D22-D60 timeline |
| 05-14 19:50~59 | 各 1.6-31 KB | `sessions/domain_positioning/{PART1-6, README, WIN_NATURE_NARRATIVE, MATH_SECTION, DEEPSEEK_CROSS_PHILOSOPHY_AUDIT, ANTITHESIS_NATURE_AUDIT}.md` | PHIL/PAP/ANTI | 11 md, Nature 定位 + 4 维 draft (D14) |
| (各) | — | `EXP7B13/../exp016_diagnostic/results/{REPORT, phase1/3/4/6_summary}.md` | EXP | 6 md, reranker 诊断历史 |

### §3.4 exp017_dialectics (157 md, 历史 paper trajectory) — 按类汇总

> 全 157 md 是 2026-04-18~05-07 的辩证法范式 + 三方协作 (Win/Linux/反题/DS) + paper v1-v8 trajectory + 数学教授 verify。**属历史归档, 非 D29 深究核心**。PI 深究可: `find /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics -name '*.md' -printf '%T+ %s %p\n' | sort`。
>
> 代表 (mtime 最新几个): `results/LINUX_INSTITUTIONALIZE_LOG.md` (05-07) · `results/WIN_TASK_SPAWN_PROTOCOL_*.md` (05-07) · `results/WIN_NATURE_HANDOFF_LINUX_20260430.md` (60 KB, 05-04) · `results/ANTITHESIS_REVERSE_AUDIT_FINAL_20260430_LOCK.md` · `results/LINUX_VERIFY_STAMP_V3_20260430.md` (48 KB) · `results/LINUX_P0_C_CHI_HARTREE_20260430.md` (37 KB) 等。
> 类分布: ANTI (反题 audit run1-4) · L0 (数学教授 verify + P0-C χ Hartree) · PHIL (paradigm L0/L1/L1+/L1++) · HO (Win/Linux handoff) · PAP (Nature first paper trajectory)。

---

## §4 checkpoint sha256 分组

> 全部 `model.safetensors` (基座 opt-125m, 500,979,600 B); 取 sha256 前 12 位分组。
> **bit-identical** = 同 hash 多 ckpt = 权重未变 (frozen, optimizer 被 skip / 退化); **distinct** = 每 gen 不同 hash = 权重真动 (真训练)。
> **判定纯字节事实, 不下 paper-level 结论。** 已知锚点 (任务给定) 全部命中对齐: 22 端 frozen cell gen0=`b3a67b42504e` ✓; seed42α0 链各异 gen0=`dff90856` ✓; 5060 fp32 gen0=`BD88E350` ✓。

### §4.1 22 端 candidate_c 全 180 ckpt 分组 (180 文件, **52 distinct hash**)

**(A) 大 frozen 簇 `020badecf014` = 70 个 ckpt 完全 bit-identical** (=权重从未更新):
- alpha0.0: seed1337 (gen0-9 全) · seed271 (全) · seed7 (全) = 3 链 × 10
- alpha10.0: seed137 (全) · seed2024 (全) · seed42 (全) = 3 链 × 10
- alpha5.0: seed2024 (全) = 1 链 × 10
- 合计 7 链 × 10 = 70 个**完全冻结链** (整链同一 hash, optimizer 全程 skip)

**(B) gen0 共享锚点 `b3a67b42504e` = 5 个** (任务给定 frozen 锚点, 各链 gen0 起点):
- alpha0.0/seed137/gen0 · alpha0.0/seed2024/gen0 · alpha10.0/seed1337/gen0 · alpha10.0/seed271/gen0 · alpha10.0/seed7/gen0
- = 多链 gen0 共享同一初始权重 (起点相同, 后续是否动看各链)

**(C) 部分动 / 退化簇 (同 hash 跨 gen 反复出现 = riddled/退化, 非单调真训练)**:
- `9346b3a9c8ec` ×13 (alpha10 seed1337 gen1-8 + seed271/seed7 若干 gen, 反复回到同 hash)
- `ec31f5e14097` ×10 (alpha5/seed42 gen0-9 **整链同 hash** = 该链也冻结)
- `7d4b57dcaacd` ×10 (alpha5/seed137 gen0-9 **整链同 hash** = 该链也冻结)
- `99a100ff35a2` ×5 · `5eabb9cf6031` ×5 · `1373e4e9285a` ×5 · `98440bf93a61` ×4 · `0872f3625857` ×4 · `9791f0b5fae9` ×3 · `bfdf48244228` ×2 · `bf55a1f9dc71` ×2 · `bbad8a58b714` ×2 · `8dcd29bfdf4c` ×2 · `126504166f46` ×2 (这些多 = 跨 gen 重复, 退化/riddled 模式)

**(D) 唯一真动链 — seed42 alpha0.0 (gen0-9 = 10 distinct hash)**:
- gen0 `dff908569813` (任务给定锚点 ✓) → gen1 `8c8d6296aff8` → gen2 `a5eb597409e1` → gen3 `b03d0db20310` → gen4 `cbec7652e7e4` → gen5 `59be0680fe64` → gen6 `a10f11d69374` → gen7 `3bac88ac8e4d` → gen8 `17fa19907bb9` → gen9 `2b2b3bd3ab48`
- = **唯一一条 gen0-9 全 distinct 的链** (权重逐代真变); 其余多链 gen0 共享 `b3a67b42` 或整链冻 `020badecf014`

**(E) seed42 alpha0.0 之外的 distinct (各 1 次)**: seed137 各 gen 多 distinct (`382247db195a`/`e2af5f412142`/...); seed2024 各 gen 多 distinct (`bd9fecc0400a`/`fdaee40dc9e7`/...); alpha5 seed271 部分 distinct; alpha5 seed7 部分 distinct

> **§4.1 字节事实小结 (catalog only)**: 180 ckpt → 52 distinct hash; 至少 9 链中多链整链冻结 (70+10+10 = ≥90 ckpt 落在整链冻结的 hash 上); 唯一明确 gen0-9 全 distinct 的真动链 = seed42/alpha0.0。任务给定 3 锚点全对齐。**是否"训练有效/无效"的判定留 PI。**

### §4.2 5060 桌面 ckpt 分组 (6 文件, 全 distinct, 锚点对齐)

| hash (前12) | 路径 `19:` | 备注 |
|---|---|---|
| `BD88E350C56A` | E0_disentangle_S3 gen0 · smoke_fp32 gen0 · smoke_fp32_gc_R1_D25 gen0 | **3 处 gen0 bit-identical** (同 config 同 seed 起点; 任务给定 fp32 锚点 ✓) |
| `C663D66BE956` | E0_disentangle_S3 gen1 | distinct (g0→g1 权重真变, fp32 健康) |
| `7463003EE48D` | SMOKE_5060_FP16_CROSSCHECK gen0 | distinct (fp16 起点) |
| `FB608459A69C` | SMOKE_5060_FP16_CROSSCHECK gen1 | distinct (g0→g1 真变, fp16 健康无 skip) |

> 5060 全部 ckpt 在 gen0→gen1 均 distinct (3 个 gen0 共享起点 hash, 但各自 gen1 不同) = **5060 两种精度 (fp32+fp16) 权重都真动**。字节事实, 判定留 PI。

### §4.3 22 衍生 cell + preflight ckpt

| 路径 `22:` | safetensors 数 | 备注 |
|---|---|---|
| cell_B_C/output/.../alpha0.0/seed42/generation_0 | 1 | fp32 NaN run (a1_ppl null) |
| candidate_c_preflight/.../alpha10.0/seed42/generation_{0,1} | 2 | preflight 2gen |
| cell_B / cell_B_retry_B | 0 (本 session find 未见 safetensors, 仅 jsonl) | 极短/失败 run, 可能未存 ckpt |

---

## §5 跨机 map + 单点/缺失 flag

### §5.1 同一 run 的跨机副本 map

| run | 7B13 | 22 | 19 (5060) | 副本数 | 备份充分性 |
|---|---|---|---|---|---|
| 早期 armb / phase1_robust (真训练, v8 基底) | ✓ `logs/` + `logs/host22_backup/` + `archive/.../chain_logs/` (jsonl ×3 副本) | ✗ (22 端 static backup 已不存在, 见 §5.2) | ✗ | jsonl 3 副本在 7B13, **git 入库** | **充分** (在 git 仓内) |
| candidate_c jsonl (N=180) | ✓ `dppl_.../candidate_c/*.jsonl` (335 KB 副本) | ✓ `/tmp/.../candidate_c/*.jsonl` (源) | ✗ | 2 | jsonl 有副本; **180 ckpt 仅在 22 /tmp 单点** |
| candidate_c 180 checkpoint (safetensors) | ✗ | ✓ `/tmp/.../checkpoints/` (单点) | ✗ | **1 (单点)** | ⚠️ **单点 ephemeral** |
| candidate_c nohup logs (16+13+7 MB) | ✓ `candidate_c.nohup.log` 5.3 MB (部分) | ✓ 全 3 个 (源) | ✗ | 部分 | 22 单点为主 |
| main_D22 + pilot_D21 | ✗ (仅 verdict md 在 7B13) | ✓ `/tmp/.../main/` + `pilot_*` (单点) | ✗ | **1 (单点)** | ⚠️ **单点 ephemeral** |
| cell_B / cell_B_C / retry / smoke (fp32 NaN) | ✗ (仅 RESULT md) | ✓ `/tmp/dppl_bridge_cell_*` (单点) | ✗ | **1 (单点)** | ⚠️ **单点 ephemeral** |
| 5060 E0 + SMOKE fp16/fp32 (健康对照) | ✓ md + E0_launch.log 副本; ckpt ✗ | ✗ | ✓ `Desktop\5060\` (源 + ckpt) | jsonl/log 部分双; ckpt 单点 | ⚠️ **ckpt + jsonl 单点在 19 桌面无 backup** |
| 5060 代码工作副本 | ✓ (主仓 src/) | ✗ | ✓ `maofield_5060_work/` (副本) | 2 | 充分 (主仓 git) |
| D29 cascade + L0 + index md (今日产出) | ✓ (源, git 入库) | ✗ | ✗ (部分 PULL) | 1-2 | 充分 (git) |

### §5.2 单点 / ephemeral / 缺失 flag (⚠️ PI 关注)

1. ⚠️ **22 `/tmp` 全部 ephemeral, 重启即失**: candidate_c 180 ckpt (~85 GB 量级) + main_D22 + pilot_D21 + cell_B/cell_B_C/retry/smoke + nohup logs (合计 30+ MB) **全在 `/tmp`, 单点, 无 backup**。`df /tmp` = 1.9T 用 20% (空间够, 但 /tmp 不持久)。
2. ⚠️ **22 端 `/tmp/MaoField_static_backup_20260520` 已不存在** (本 session ls 确认): prior 元数据文档 (`MAOFIELD_EXP_METADATA_MASTER`) 标早期 armb 备份在 "22 `MaoField_static_backup_20260520`", **但该路径现已消失**。早期 armb 真训练数据当前 **仅靠 7B13 git 仓内 3 处 jsonl 副本存活** (ckpt 早已无)。**这是 prior 文档与当前字节状态的差异, 按 D-1 纪律 5 surface, 不静默。**
   - ✅ **[D29 后续验证更正 — 本条部分有误]**: 消失的只是 `/tmp` 副本。静态备份**存在于 22 的 `/home/amd/HEZIMENG/MaoField_static_backup_20260520/` (持久 /home, 63G)**, 含 `checkpoints_official/no_preserve_seed42/gen0-9` (10 ckpt)。故 v8 的 **seed42 参考链 ckpt 有持久副本** (非 ephemeral); 其余 seed 的 ckpt 是否存在未确认。"早期 armb ckpt 早已无" 过强 — 至少 seed42 链在。(7B13 本机无此目录, 该备份单点在 22 /home。)
3. ⚠️ **5060/19 桌面 ckpt + jsonl 单点无 backup**: E0/SMOKE 的 safetensors + jsonl 仅在 `C:\Users\amd\Desktop\5060\`, Win 桌面, 无 git/无远程副本 (md 有 PULL 副本, 但**实验数据本体单点**)。
4. ⚠️ **candidate_c 180 ckpt 的 jsonl 有 7B13 副本, 但 safetensors 无 7B13 副本**: 若 22 /tmp 清空, 180 ckpt (sha256 分组证据本体) 永久丢失, 只剩 jsonl 数字 + 本文件记录的 sha256 前 12 位。
5. **被引用但需注意**: `E1E2_DECISION_PACKAGE_VERIFIED` §1-4 标 `src/train_one_generation.py:107/:126` 精度 wiring "未独立验" (该通道 grep 未命中) — 代码事实待 PI/7B13 主会话复核 (本文件未独立验该行号)。
6. **空文件 flag**: `19:Desktop\5060\han.md` = **0 字节** (疑占位/误建)。

### §5.3 早期 armb 真训练数据存活路径 (v8 安全性关键, catalog)

> per HANDOFF_7B13_D29 §1-2: paper v8 负结果建在早期 armb (05-08~12) 真训练数据, 与 candidate_c (broken fp16) 是另一 run。本文件 catalog 其存活路径:
- jsonl 副本 1: `EXP7B13/logs/armb_*.jsonl` + `shumailov_*.jsonl` (git 入库)
- jsonl 副本 2: `EXP7B13/logs/host22_backup_20260512/armb_*.jsonl` (git 入库)
- jsonl 副本 3: `EXP7B13/archive/v1.0_release_20260516/chain_logs/armb_*.jsonl` (17 jsonl, git 入库)
- **ckpt (safetensors)**: ⚠️ **[D29 后续验证更正]** seed42 参考链 **有持久副本** 在 `22:/home/amd/HEZIMENG/MaoField_static_backup_20260520/.../checkpoints_official/no_preserve_seed42/gen0-9` (持久 /home, 非 /tmp); 其余 seed 的 ckpt 是否存在未确认。v8 核心数据本是 jsonl (安全); ckpt 主要用于重算 — seed42 链可重算。

---

## §6 时间线 (按真实 mtime, 三机合并)

| 日期/时段 | 机器 | 事件 (数据/md, 带路径线索) |
|---|---|---|
| 05-07 16:00~ | 7B13 | exp018_cat 启动: smoke_test + shumailov_no_preserve s42 短跑 (`logs/`) |
| 05-08 01:40 | 7B13 | shumailov_no_preserve s42 主跑 10gen 完 (5057 B jsonl) + baseline FULL log 4.1 MB |
| 05-08 14:00~19:20 | 7B13 | 重跑 s42 + sanity_check (opt125m/gpt2/kl) + armb_alpha0/10 s42 真训练 |
| 05-09 00:02~16:23 | 7B13 | armb_alpha1/5/10/50 s42 + alpha0 s1337 真训练链 (v8 single-seed U-shape) |
| 05-10~05-12 | 22→7B13 | phase1_robust multi-seed s0-4 α0/10 (22 跑, 05-12 20:00 备份回 7B13 `host22_backup`) |
| 05-13 16:05 | 7B13 | host22_backup 续 (armb s1 alpha0 早 run) + analysis_20260513 |
| 05-14 19:50~59 | 7B13 | sessions/domain_positioning 11 md (Nature 定位 + 4 维 draft) |
| 05-16 22:00 | 7B13 | archive/v1.0_release_20260516 建 (17 chain_logs jsonl 归档) |
| 05-21 11:46~20:26 | 22+7B13 | D21: pilot (22 pilot_D21 4 行) + install ROCm + 桌面 cascade crash/fix + 反题 16 insight + 8 reflexive insight (REFLEXIVE/PARADIGM/EXPERIMENT_REFRAME) + 文献 A/B |
| 05-22 11:48~20:41 | 22+7B13 | D22: main_D22 launch (162 行) + candidate_c launch (203837 jsonl 186 行) + preflight + venue eval + path A/C 设计 + 文献 C |
| 05-23 01:53~13:03 | 22+7B13 | candidate_c 跑中 progress_snapshot_10~30 + **D23 NaN explosion surface** + VERIFY progress code |
| 05-24 14:15~21:17 | 22+5060+7B13 | candidate_c snapshot_40~80 + D24 5060 fp32 isolated test + **P0★-G FATAL surface** (9070 fp16 vs 5060 fp32) + 反题 catch P0★-G + AUDIT exp history binary |
| 05-25 09:05~19:40 | 22+5060+7B13 | cell_B/cell_B_C (fp32 NaN) + 5060 smoke_fp32/gc_R1/N_seed + **E0 fp32 disentangle (g0=36.5→g1=78.6 健康)** + MATH_VERIFY GradScaler skip + 反题 7th-layer framing + deep research 整合 |
| 05-26 11:49~23:01 | 22+5060+7B13 | D26: NaN cascade = same-source D23 诊断 + full data audit + multi-channel 数学 + math rigorous proof S1-S5 + 文献 + global file index + 战略全景 + candidate_c jsonl 副本回 7B13 (23:01) |
| 05-27 10:26~21:24 | 22+5060+7B13 | D27: E0_launch.log + smoke_fp32 log 回 7B13 (10:26) + **5060 SMOKE fp16 crosscheck (g0=36.5→g1=78.1 健康, 21:05~22:03)** + DS 关卡3 + Nature desk review sim + paper v8.1 footnote + v9 skeleton + ROCm/MIOpen trace + 文献 v9 anchor |
| 05-28 00:34~17:03 | 5060+7B13 | 5060 SMOKE fp16 err_gen1 (00:34) + D28: 4-endpoint verify + cross-verify ablation + exp deep audit + exp inventory + math rigorous + md cross-channel + MLRC paper draft + venue scouting + L0 proof prompt |
| **05-29 09:37~17:06** | 7B13 (+ssh 22/19 read) | **D29: L0 8 条第1+2轮 (10:36~14:47, 0 unconditional close/2 cond/3 neg/3 FAIL) + 6 维 index (12:11~12:17) + GATE (12:16) + cascade update (13:15~15:09) + 数据完整性/re-derivation 独立通道 (14:20~14:29) + 元数据 inventory X/Y/master (14:52~15:13) + E1E2 决策包 verified (17:06) + HANDOFF_7B13 (15:59) + git HEAD 16:07** |

---

## §7 completeness 自检 — 未能访问 / 待补 / 不确定项 (不静默遗漏)

### §7.1 已穷尽 verify (✓)
- ✓ 三机可达性实测 (7B13 本机 / 22 ssh / 19 ssh+PowerShell)
- ✓ 真实日期 `date` binary (2026-05-29 17:07 CST)
- ✓ 7B13 全 424 md 计数 + 按目录分组 + dppl_bridge (110) + 5060 桌面 (21) + 顶层/docs/sessions 全枚举
- ✓ 22 candidate_c 全 **180** safetensors sha256 (52 distinct hash, 任务给定 3 锚点全对齐)
- ✓ 5060 桌面全 6 safetensors sha256 + 全 7 jsonl 行数 + 全 11 log 大小/mtime + 全 21 md
- ✓ 22 cell_B/cell_B_C/retry/preflight/smoke/main/pilot jsonl 行数 + null 统计 + grad_norm:nan 计数
- ✓ 早期 armb 真训练数据 3 处副本路径确认
- ✓ D29 cascade 11 文档结论行串联 (§3.1 加粗条目)

### §7.2 待补 / 未能完全访问 (留 PI)
1. **[待补] exp017_dialectics 157 md 未逐条枚举**: 仅按类汇总 + 代表列出。属历史 paper trajectory, 非 D29 深究核心。PI 深究命令已给 (§3.4)。
2. **[待补] exp001-016 + 22 端历史检索实验 (sqlite ~14 个, ~330-455 MB 各)** 仅按 cluster 简列 (§2.6); 非 self-iteration chain 数据, 未逐文件 catalog。
3. **[未独立验] `src/train_one_generation.py:107/:126` 精度 wiring 行号**: 引 E1E2 决策包, 本文件未独立 grep 验 (该决策包自标"未独立验")。留 7B13 主会话复核。
4. **[不确定] 22 端早期 armb ckpt 是否曾存在**: 当前 `/tmp/MaoField_static_backup_20260520` 已不存在 (§5.2), 早期 armb 当前仅 jsonl 存活。"曾存 ckpt 否 / 何时清空"需 PI 确认 (本 session 只能确认现状: ckpt 无)。
5. **[未访问] cell_B / cell_B_retry_B 是否真无 safetensors**: 本 session find 在这两目录未见 model.safetensors (仅 jsonl + nohup), 但未排除存在非标准命名 ckpt 的可能 (极短/失败 run, 大概率确无)。
6. **[待 PI] 22 端 9070XT 上是否有 candidate_c 之外的其他 active run**: 本 session 扫 `/tmp/*mao* *dppl*`, 命中 6 个 dppl 目录 (verify/cell_B/cell_B_C/cell_B_retry_B/verify_smoke); 未扫 22 端 home / 其他挂载点的潜在 MaoField 数据。
7. **[catalog 边界] 本文件不下任何 paper-level 结论**: "candidate_c 是否污染 v8 / collapse 是否被 α mitigate / C3 是否 fractal 还是退化 / 接受率 / tier" — 全部留 PI + 关卡 3 反题三方决。本文件 §4 的 frozen/distinct 是**纯字节分组事实**, 不等于"训练有效性判定"。

### §7.3 binding 自检 (逐条 ✓)
- ✓ read-only: 全程 find/ls/wc/du/sha256sum/cat 小文件 + ssh read-only + PowerShell Get-FileHash/Get-ChildItem; **0 commit / 0 push / 0 launch / 0 ssh-write**
- ✓ 仅写本 1 个 output md (`MAOFIELD_FULL_INDEX_3MACHINES_20260529.md`)
- ✓ 所有数字带路径 (jsonl record 数 / sha256 / 大小 / mtime 均附三机路径)
- ✓ 真实日期先 `date` binary 验 (§0)
- ✓ 不下 paper-level 结论 (§7.2-7 + 全文 catalog-only)
- ✓ paper v8 final 47/47 / 12 NOT-claim / 反题 P0★ tier / D29 三 leg — 本文件仅 catalog 其状态, 不触动
- ✓ completeness > 简洁: 全枚举 + 未访问项显式列出 (§7.2), 不静默遗漏
