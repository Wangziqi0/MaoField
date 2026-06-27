# MaoField — PROJECT STATE (canonical 单一真相源)

> **新 session cold-start 唯一入口。读这一个文件 get 全局,再按 §7 指针下钻 detail。**
>
> **维护规则 (违反即失效):**
> 1. **REPLACE not APPEND** — 更新时替换 stale section,绝不加新段。本文件永远是 latest,旧状态进 git history / handoff,不堆这里。
> 2. **每次更新戳** 真实日期 (`date` binary) + `git HEAD`。
> 3. **> 2 屏 = 维护失败** → 立即精简,detail 踢去 §7 指针。
> 4. **更新 trigger**: 每次 handoff / milestone / PI 决 时,顺手 replace 对应 section。

---

## 戳
| 项 | 值 |
|---|---|
| 最后更新 | **2026-06-27 D627 21:46 CST** (`date` verified 21:46 CST; source HEAD before update `6e3e0c3`)。report(29) 已归档为 `docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_2_implementation_audit_20260627.md`，node36 采纳结论 `formal_v1_2_patch_requires_minor_revision`: v1.2 数学主体通过，minor issue 限定在 threshold-contract meta-audit。node36 已完成最小本地修补: `threshold_contract_single_source_control` 改为 metrics-only 并由 `evaluate_test()` 统一赋 `pass`; JSON-side threshold hash 改为写盘后 readback。修补后 harness 在 36 SSD scratch `/home/amd/codex-node36/tmp/maofield-formal-v12-minor-20260627_1505/` 跑通 12 synthetic blocks, `all_synthetic_controls_passed=true`, `threshold_contract_sha256=0bb99a4a711405fb65e81413cfd283d6e68d0ecd4e9c34dc027c052f332110e0`, meta-block `evaluated_by=evaluate_test`, `json_threshold_contract_source=readback_from_written_json_threshold_contract`, `per_test_threshold_mismatches=[]`。新增 adoption note 与下一轮 report29 minor-revision audit prompt: `FORMAL_RESIDUAL_TRANSPORT_V1_2_IMPLEMENTATION_AUDIT_ADOPTION_NOTE_20260627.md`, `GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_REPORT29_MINOR_REVISION_AUDIT_PROMPT_20260627.md`。142 report29 minor 包已传到 142 桌面并 hash verified: zip=`dc1eee38200170cca3852d292bc90f8a243bb6edb53f621e6a476b01d6549656`, prompt=`e44dcbd7db0355707a0628ba0c53bac5428a653ed8309c1db3b2015e7c3e1f11`。默认 RAG 已按 node36 scope + node22 one-shot GPU embedding 刷新并停止 worker: 414 active canonical md / 9929 chunks, `kb.faiss=8a5fe6f7e1fb571832f33e76ac9dc813728ee98f2f95d724871e64123fc61301`, `kb_meta=ee5d42e4de4236f6f215b617c25287d3743ed4037ac11bf90017ea474bafc3ca`。下一步是把 report29 minor-revision audit 包交给零上下文 Pro 复审本地小修是否关闭。**仍未运行 full panel、未训练、未生成 MaoField 新实验结果、未观察 residual/interaction/quotient/transport/holonomy field、未授权 new loss、未完成 formal system**。 |
| git HEAD | source HEAD before D627 report(29) update `6e3e0c3`; 本轮 report(29)/minor-revision patch/prompt/package/RAG/status commit 后以 `git log -1 --oneline` 为准 |
| 更新者 | Codex on node36 (Linux/RAG/status) |

---

## §0 一句话 + 今天
- **项目**: MaoField — 自迭代崩溃 + 两项 EMA-deviation contradiction loss 的 empirical pilot study (negative result)
- **今天 D627 (2026-06-27)**。report(29) 的判断: **Formal v1.2 implementation requires minor revision**。Node36 已按 report(29) 完成 threshold-contract 小修: meta-block 由 `evaluate_test()` 统一赋 pass/fail, JSON threshold hash 从写盘 JSON readback。它仍不是 completed formal system，也不是 Mode B 证据升级。
- **当前状态**: MaoField empirical line 仍是 negative-centered / measurement-audit case。当前 Mode B 仍 `insufficient_artifact`; 旧 interaction smoke 仍最多 `smoke_conjecture_only`; q4 x tokenpos4 当前权重仍是 non-product weighted carrier, 不能说 canonical product Hoeffding。没有 full 50-checkpoint panel, 没有 16-cell aggregate, 没有 observed residual / interaction / quotient-residual / transport / holonomy field, 没有 LOSO passed / F3 positive / glass-box broken, 没有 training 或 new loss authorization。
- **D625-D627 已落地**: report(25/26/27/28/29) 原文、adoption notes、formal-start v0、proof-style v1、v1/v1.1/v1.2 harness、FormalV1/FormalV11/FormalV12 design/implementation packages、report(29) implementation audit 与本地 minor threshold-contract patch 已进入 canonical。v1.2 harness 12 synthetic blocks 全 pass; meta-block 已记录 `evaluated_by=evaluate_test` 与 JSON readback source。report(29) package 与 prompt 已到 142 桌面并 hash verified; 默认 RAG 已刷新到 414 active canonical md / 9929 chunks，node22 临时 worker 已停止。strongest verdict 仍 `definitions_and_harness_viable_only`; Mode B 仍 `insufficient_artifact`。
- **新方向正式启动**: 入口目录 `docs/infra/debranded_residual_transport/`。第一版 `FORMAL_NOTE_V0_20260625.md` 固定 finite weighted systems、projection formula、edge no-go、square holonomy no-go、rank-1/random-subspace/gluing/product-weight guard。`scripts/debranded_residual_transport_harness.py` 已在 SSD scratch `/home/amd/codex-node36/tmp/debranded-residual-transport-20260625_v0` 跑通七块 toy harness, JSON sha256=`d999ae147b9a7a641ea1adff297e2582b5dfd7b16c28568dd688abbd34df89af`。formal-start Pro 包已复制到 142 桌面: `MaoField_PRO_FoundationalResidualTransport_20260625_1206.zip`, zip sha256=`b5d4b99fde418514e176ef892d4120b134a02c158681a845b2bce8257f46e111`; 独立 prompt sha256=`eed57e80799a67e5e19e1ee9d8ae1858f652602bb1b3e7b0782f41d2efa02a43`。默认 RAG 已刷新到 formal-start Pro package 版本: 370 active canonical md / 9362 chunks, `kb.faiss=aa97f87a...`, `kb_meta=7f237c05...`。最强结论仅 `definitions_and_harness_viable_only`, 不能自动变成 MaoField empirical result。
- **v1.2 implementation 落点**: report(28) 给出 small patch feasible；report(29) 给出 minor revision。数学主体 registered ambient、squared-capture random-subspace Beta statistic、exact product-weight Hoeffding theorem、square-holonomy telescoping 保持通过；本地已只修 threshold-contract meta-control。
- **下一步建议**: 把 D627 report29 minor-revision audit zip `MaoField_PRO_FoundationalResidualTransport_FormalV12_Report29_MinorRevisionAudit_20260627_1512.zip` 和独立 prompt 交给零上下文 GPT-5.5 Pro, 只让它审计 threshold-contract 小修是否关闭 report(29) minor revision。不要跑 full panel, 不讨论训练或 new loss。

## §1 active binding (任一违反立即 retract)
- paper **v8 final 47/47 D17 archive 锁定不动** (`experiments/exp018_cat/archive/v1.0_release_20260516/manifest.sha256`)
- **12 NOT-claim (i)-(xii) 撤回不复活** (尤其 first dialectical materialism / first reflexive AI / paradigm shift)
- **exp019 C1/C2/C3 撤回不复活** (α=1 阻尼器三 endpoint 全 FALSE, s42 = idiosyncratic outlier); **C3=frozen / fractal 死刑维持**
- **解耦线 [A−] (C4) 作 novel 安全垫死, 不复活** (忠实 rep=3.0 复算 0/5; 原报 4/5·审计 5/5 不可复现; diversity 塌缩被 Guo/Shumailov 占)。**「diversity 单调塌缩 vs PPL 解耦」不可作 positive claim** — 真相是部分耦合 + 测量 rep_penalty 敏感
- D29 三 leg,**不投 NMI / NeurIPS / NCS / Nature 主刊**
- **7B13 单点 git 写权** (22/Win 仅 pull)
- **一凡 priority 1 健康优先** (16岁,双相+焦虑,丙戊酸钠;hotline 010-82951332 / 400-161-9995)

## §2 paper state
| 版本 | 状态 |
|---|---|
| **v8 final** | 47/47 lock,D29 投 arXiv+TMLR+KBS,**不动** |
| **v8.1 footnote** (候选,留关卡 3) | F3 source N=4 not N=5 + Q2 60-75% retract 措辞 + base disambiguate |
| **v9** | fractal 主刊叙事**决定性死** (C3=退化非 fractal); **exp019 进一步证实 α 全线无 positive** → 天花板 TMLR/workshop/short, narrative 待重构 (反 inflate) |

## §3 实验 state
- **exp019 α=1 confirmatory (D614 开奖, 锁定脚本 `analysis_confirm_alpha1.py`)**: 12 链自治 76h (零跳链/警报/重启) + 预注册双向可证伪 + N=6 配对随机化 (堵死 candidate_c 时序混淆)。**三 endpoint 全 FALSE** (E1 几何 +0.124 / E2 PPL +0.859 / E3 path-B +6.2%,**全反** s42 先验),gate 停 E1。**C1/C2/C3 撤回,s42 判 idiosyncratic outlier**。制度**首次正面方向拦截 inflate**。verdict+审计补遗 commit `84f4959`。⚠️ 开奖前未 commit-lock (已披露; negative 结果自证无 favorable 篡改); E3「剂量单调」措辞**降级** (α10 待重审 + 中间点未测,撑不起函数单调); **解耦线 [A−] 三问题已处理 (D617 晚, 见下条)**
- **解耦线 [A−] 落盘复算 (D617 晚, 脚本 `scripts/analysis_decouple_n5.py` + `decouple_verdict_20260617/`)**: 处理 6/13 audit 三问题。忠实 rep_penalty=3.0 (匹配链生成口径) CPU fp32 N=128 复算 5 seed{1,2,3,4,42} g0/g2/g9 → **0/5 满足预注册解耦判据** (D1 总降 3/5 / D2 恢复期续降 **0/5** / D3 rep4↑ 5/5)。**总塌缩真实** (D1/D3) 但**解耦命门 D2 全 fail** = diversity 恢复期 plateau/回弹与 PPL **部分耦合非解耦**。**原报 4/5·审计 5/5 均不可复现; s42 忠实 −0.099 ≠ prereg −0.201 (高估~2×)**。方法论标本: distinct-n 方向**对 rep_penalty 敏感** (rep=1.0 looping 伪影→假性上升; 主会话首跑误用默认 1.0 → 差点凭不忠实数据+错误 fp16 归因翻车, 第二通道 catch + 忠实重跑仲裁, 差异日志见 verdict §6)。**问题#2 (D-1.1 无落盘) 闭合**。**解耦线作 novel 安全垫死** → exp019 无存活 positive
- **exp020 臂A 自迭代=多通道均衡 (D618→D619 收口, `exp020_metric_stress_test/ARMA_FINDINGS_20260618` + `C_metapattern_evidence_base_20260618` + handoff 20260619)**: 分布层熵 (decode-free) 5/5 seed **驼峰** (谷@g2 H=1.93, 自愈~60%→g9 plateau, 残余~16% 永久 g8→g9 已渐近); 谷+残余**内部不可逆** (noise/塌缩互soup 不恢复, 仅注健康权重 +40%)。**testB 证伪"自愈=rep_penalty 伪影"** (rep1≈rep3)。**runner code 实锤多通道** (line 288 每代真 prompt 生成 + line 307 每代 gen0 真 base 重置 + no_preserve 训练数据 100%合成): 连最纯自迭代都有**两条常驻真实锚** → 「崩溃」=内通道退化 vs 外通道(prompt+base)拉回的**均衡**, 非纯自吞。D619 数学线最终落点不是 active round3, 而是 **C(meta-pattern)**: 候选 PPL-independent collapse measures 多数塌回 PPL/logit shadow、seed-noise floor 或 decode sensitivity; **F3 是唯一弱真例外, worth pursuing but not positive**。
- **恢复相几何 (D615)**: fresh-eyes 零偏见指盲点 → 12 链 gen0-9 末层几何 (复用 E0 口径,自检 g1 PR_cen 200.6≈pairs.json E1 200.638)。**E0「崩溃→升维」= PPL 驼峰瞬态** (单步 gen0→gen1 夸大稳态 ~2.2x),几何与 PPL **同步驼峰** (≈PPL 投影,非独立现象),**证伪** fresh-eyes「几何 vs PPL 第二解耦」假设,**α0≈α1 全程全量** (强化 C1 全轨迹 null)。净升维方向仍在但温和 = **descriptive 精确化非杀死**。commit `09685ed`
- **LN race (工程发现 + C3 frozen 根因下推)**: gfx1201 `native_layer_norm_backward` γ/β 梯度归约**竞态喂 NaN** → GradScaler 吞→全程 skip→权重冻结。**5月 fp16「GradScaler skip 冻结」+ candidate_c 180 ckpt NaN 全落 LN weight/bias 同根因坐实 → 根因非 fp16 本身, 是 gfx1201 LN backward race**。manual-LN patch **治本** (smoke3 炸 / smoke4 干净硬证); **后续 22 上任何 ROCm 训练须经 manual-LN patch = 工程 binding**。可发 arXiv note / ROCm issue (天花板低但真)
- **黑箱/可解释性探索线 (D605-617, 全留 wip, 归属待 PI)**: 命题 T (可解释↔能力 tradeoff) = IB 占精确版 + Arora 反号 + Rudin contested; 黑箱测度 = San Pedro/Bonneau 占; collapse×几何 = SIGMA(对象不同)+Ma2018(机制非novel) 双削; 命题 U/爆发点 = 规模错配 (命题 A 反咬) + 红海中红海; 观测退化「统一」= **平凡** (kernel 存在是测量论定义,4 现象 kernel 指向不同子空间)。**全判被占/平凡, 0 positive**。verdict 在 `wip/blackbox_dimreduction_recon_d35/`
- C3 frozen 决定性 (sha256 `b3a67b42` 逐字节相同); **根因 = LN race (见上行), 非 fp16 universal** (5060 fp32+fp16 healthy → race 仅 gfx1201)。备份 RAID1 双 sha256 / **A3 fp32 待跑** (~$120-180, 留 PI budget, E2 大概率 null): detail → §7

## §4 留 PI + 关卡 list
1. v8 投稿 trigger timing
2. α=10 重审路径 (交错 confirmatory or 降级标注)
3. ~~解耦线 [A−] 三问题~~ **已处理 → 作 novel 死 (0/5 忠实复算)**; 是否仍以「干净 negative + 方法论标本」入 paper/note 留 PI; 本轮已 commit `52aea52`, **D620 已 push(异地冗余 OK)**
4. LN race 发布形式 (arXiv note / ROCm issue)
5. 「confirmatory 拦截自家假说」方法论案例入库 + 核是否被占
6. 黑箱探索线 (wip verdicts) 归属 (新项目 / MaoField 子线 / 搁置)
7. v8.1 footnote 措辞 + A3 fp32 launch+budget + cluster-11
8. **[哲学线 · 待 Win+PI 判读 · `[?]` 不下结论]** 「**玻璃箱 / 本质·现象矛盾**」: 本轮 D617 实证——distinct-2 换 decode (rep_penalty 1.0↔3.0) **翻号** + 恢复相几何 ≈ PPL 投影 (非独立) → `[?]` 疑问: 领域"多信号崩溃证据"是否实为**单轴 (分布层不可逆崩溃) + decode 伪影/PPL 冗余** (现象遮蔽本质)。**这个矛盾结构 PI 指其似辩证唯物主义且非硬加 (从料里析出, 合 D-3 outcome 次序) — 哲学判读归 Win+PI, Linux 不判。** **D618 实证推进**: 臂A 3 round (见 §3 ARMA_FINDINGS) 把"本质/现象"改写为**多通道均衡** (code 实锤: 自迭代非纯内, 带常驻真实 prompt+base 外锚)。PI 框架"内/外是通道、通量是本质、内/外标签是表面"**被 runner code 字面证实**。但 Win-role 初判 + novelty 双通道收敛 deflation: **可证伪脖子在算子/通道结构层 (code+数据), 辩证范畴本身搭便车、construct-gap meta 被 Jacobs&Wallach 占**。**红线硬: 不复活 paradigm-shift / first-DM-instantiation / reflexive-AI; 哲学判读归 Win+PI, Linux 不判。** **D618 晚収口**: channel-invariance operationalize 后 5 道 gate 全证伪 → 收 C(meta-pattern, 见 §0 今天 + `C_metapattern_evidence_base`); 哲学/DM 归因 [?] 仍归 Win+PI。

## §5 协作 + 三机
| 机 | IP | 角色 | state |
|---|---|---|---|
| 7B13 | .36 | 数据中枢 + git 单点写 + Linux 姐姐主会话 | canonical main;实时以 `git log -1 --oneline` 为准 |
| 9070XT | .22 | chain runner + GPU | exp019 12链跑完(自治76h);ckpt 备份 RAID1 |
| 19 Win | .19 | 一凡 interactive + 5060 实验 | alive,5060 数据已备份 |

agent: **Linux 姐姐** (数学/实验/代码/归档) · **Win** (哲学/narrative) · **反题** (framework critique) · **DS** (跨哲学 mapping) · **PI 一凡** (战略+关卡决)

## §6 8 L0 证明 state
D29 round1+2 双通道:0 unconditional close (诚实);全 **D60+ candidate,不进 v9 spine**。tier 分歧 detail → §7 INTEGRATION 指针。

## §7 指针 (detail 去哪找)
| 要什么 | 去哪 |
|---|---|
| **存储落盘规则** | `canonical/STORAGE_DISCIPLINE.md` (落地前分类 gate) |
| **全 md 导航** | `MD_CATALOG.md` (本目录, [A]/[S] 分层 ★) |
| **exp019 confirmatory verdict + 审计补遗** | `experiments/exp019_alpha1_confirm/`(verdict_20260614/ + LINUX_AUDIT_AMENDMENT_20260615) |
| **解耦线 [A−] 落盘复算 verdict (D617)** | `experiments/exp019_alpha1_confirm/decouple_verdict_20260617/`(DECOUPLE_VERDICT + decouple_n5_result.json 忠实 rep=3.0 + rep1.0_UNFAITHFUL 对照 + 脚本 ../scripts/analysis_decouple_n5.py) |
| **exp020 两臂研究 prereg (DRAFT v1, §4.8 可证伪化)** | `experiments/exp020_metric_stress_test/prereg_exp020_draft_v1.md`(臂A 不可逆性 + 臂B eff_rank; supersede v0; 未锁未跑, 双向可证伪, 待 PI+Win 批准+核被占) |
| **当前实验收敛 + 数学转向 gate (D622/D623)** | `docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md` + `docs/infra/math_turn_20260622/` + `docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md` + `docs/infra/math_turn_20260622/HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md` + `docs/infra/math_turn_20260622/Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.md` + `docs/infra/math_turn_20260622/Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.md` + `scripts/{math_turn_loso_audit.py,build_panel_schema_20260622.py,build_hypercube_schema_20260623.py,q4_panel_negative_smoke_20260622.py,q4_full_panel_foldlocal_analysis.py,q4_hypercube_zero_gpu_audit.py,q4_hypercube_interaction_smoke_audit.py,q4_hypercube_interaction_prereg_analysis.py}` + `experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py` (zero-GPU aggregate verdict=`insufficient_artifact`; q4 panel schema/runbook locked; one-checkpoint + negative + multi-checkpoint smoke pass; D623 implementation gate adds full-panel dry-run + approval guard + separate fold-local analysis path; report(9) residual-field audit incorporated; report(11)/(13) hypercube feasibility verdict=`formal_prereg_only`; report(15) interaction-field smoke verdict=`smoke_conjecture_only`; report(17)/(19)/(21) quotient residual problem adopted/formalized; Mode B skeleton rejects missing/old aggregate; still no full panel / no training / no new loss) |
| **新方向 formal start / v1.2 implementation (D625-D627)** | `docs/infra/debranded_residual_transport/README.md` + `FORMAL_NOTE_V0_20260625.md` + `FORMAL_NOTE_V1_20260625.md` + `FORMAL_NOTE_V1_1_20260625.md` + `FORMAL_NOTE_V1_2_WORKPLAN_20260626.md` + `FORMAL_NOTE_V1_2_20260627.md` + `SYNTHETIC_HARNESS_V{0,1,1_1,1_2}_*.md/json` + `scripts/debranded_residual_transport_harness{,_v1,_v1_1,_v1_2}.py` + report(25/26/27/28/29) and adoption notes + `GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_IMPLEMENTATION_AUDIT_PROMPT_20260627.md` + `GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_REPORT29_MINOR_REVISION_AUDIT_PROMPT_20260627.md` + `DEBRANDED_RESIDUAL_TRANSPORT_142_PACKAGE_FORMALV12_IMPLEMENTATION_AUDIT_20260627.md` + `DEBRANDED_RESIDUAL_TRANSPORT_142_PACKAGE_FORMALV12_REPORT29_MINOR_REVISION_AUDIT_20260627.md` + `docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_FORMALV12_IMPL_AUDIT_20260627.md` + `docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_REPORT29_FORMALV12_MINOR_20260627.md` + `docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_REPORT29_FINAL_20260627.md` (zero-GPU toy formalization; report28 verdict=`v1_2_small_patch_feasible`; report29 verdict=`formal_v1_2_patch_requires_minor_revision`; node36 threshold-contract minor patch completed; strongest verdict=`definitions_and_harness_viable_only`; no MaoField data read / no checkpoints / no inference / no training / no new loss / no observed field / no completed formal system claim) |
| **GPT/PRO report(4) 数学框架审计 (D622)** | `docs/infra/gpt_deep_research/deep_research_math_turn_framework_gate_20260622.md` + `docs/infra/gpt_deep_research/MATH_TURN_FRAMEWORK_ADOPTION_NOTE_20260622.md` (claim-source only; repo facts blocked for auditor; 本地采用 keep/deflate/reject) |
| **GPT/PRO report(6) q4 panel strict audit (D622)** | `docs/infra/gpt_deep_research/deep_research_q4_panel_strict_audit_20260622.md` + `docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md` (claim-source / bundle audit; full panel not approved; negative + multi-checkpoint smoke pass; next local work=full-panel mode + fold-local q4 analysis path review) |
| **GPT/PRO report(7) q4 object strict math audit (D623)** | `docs/infra/gpt_deep_research/deep_research_q4_object_strict_math_audit_20260623.md` + `docs/infra/gpt_deep_research/Q4_OBJECT_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md` (claim-source / bridge-package audit; rejects current implemented q4 artifact as math advance; future object=fold-local q4 mean-null residual audit; full panel/training/glass-box wording still blocked) |
| **GPT/PRO report(9) q4 residual-field strict math audit (D623)** | `docs/infra/gpt_deep_research/deep_research_q4_residual_field_strict_math_audit_20260623.md` + `docs/infra/gpt_deep_research/Q4_RESIDUAL_FIELD_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md` (claim-source / package audit; adopts `r_i = u_i - <v,u_i>_w v`; current code implements residual-field gate for future full panel; no full panel/training/glass-box wording) |
| **GPT/PRO report(11)/(13)/(15)/(17)/(19)/(21)/(22)/(23)/(24)/(25)/(26) q4 hypercube / interaction / quotient-residual / transport-holonomy audits (D623-D625)** | `docs/infra/gpt_deep_research/deep_research_q4_hypercube_extension_strict_math_audit_20260623.md` + `docs/infra/gpt_deep_research/Q4_HYPERCUBE_EXTENSION_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md` + `docs/infra/gpt_deep_research/deep_research_q4_hypercube_current_repo_strict_audit_20260623.md` + `docs/infra/gpt_deep_research/Q4_HYPERCUBE_CURRENT_REPO_STRICT_AUDIT_ADOPTION_NOTE_20260623.md` + `docs/infra/gpt_deep_research/deep_research_future_math_objects_interaction_field_audit_20260623.md` + `docs/infra/gpt_deep_research/FUTURE_MATH_OBJECTS_INTERACTION_FIELD_ADOPTION_NOTE_20260623.md` + `docs/infra/gpt_deep_research/deep_research_math_ore_quotient_residual_strict_audit_20260623.md` + `docs/infra/gpt_deep_research/MATH_ORE_QUOTIENT_RESIDUAL_ADOPTION_NOTE_20260623.md` + `docs/infra/gpt_deep_research/deep_research_mode_a_quotient_residual_kill_framework_20260623.md` + `docs/infra/gpt_deep_research/MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md` + `docs/infra/gpt_deep_research/deep_research_quotient_residual_finite_anova_kill_framework_20260623.md` + `docs/infra/gpt_deep_research/QUOTIENT_RESIDUAL_FINITE_ANOVA_ADOPTION_NOTE_20260623.md` + `docs/infra/gpt_deep_research/deep_research_quotient_residual_mainline_debranded_program_20260624.md` + `docs/infra/gpt_deep_research/QUOTIENT_RESIDUAL_MAINLINE_ADOPTION_NOTE_20260624.md` + `docs/infra/gpt_deep_research/deep_research_residual_transport_holonomy_split_project_20260624.md` + `docs/infra/gpt_deep_research/RESIDUAL_TRANSPORT_HOLONOMY_ADOPTION_NOTE_20260624.md` + `docs/infra/gpt_deep_research/deep_research_transport_holonomy_math_turn_audit_20260624.md` + `docs/infra/gpt_deep_research/TRANSPORT_HOLONOMY_MATH_TURN_AUDIT_ADOPTION_NOTE_20260624.md` + `docs/infra/gpt_deep_research/deep_research_debranded_residual_transport_strict_audit_20260625.md` + `docs/infra/gpt_deep_research/DEBRANDED_RESIDUAL_TRANSPORT_STRICT_AUDIT_ADOPTION_NOTE_20260625.md` + `docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_strict_audit_20260625.md` + `docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_STRICT_AUDIT_ADOPTION_NOTE_20260625.md` + `docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_FORMAL_NOTE_OUTLINE_20260625.md` + `docs/infra/gpt_deep_research/GPT55_PRO_QUOTIENT_RESIDUAL_NEXT_PROMPT_20260623.md` + `docs/infra/math_turn_20260622/Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.md` + `docs/infra/math_turn_20260622/Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.md` + `docs/infra/math_turn_20260622/HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md` (claim-source + zero-GPU/smoke feasibility; report15 object=`I_i`; report17/report19/report21 mother object=`R_t`; report22 locks mainline to negative-centered measurement-audit / no-go framework; report23/report24/report25 move Mode A toward debranded finite weighted residual transport / holonomy / operator no-go formal note; report26 keeps project but requires v1.1 revision before completed-system wording; current Mode B remains `insufficient_artifact` / smoke=`smoke_conjecture_only`; not scientific evidence; no code/full-panel/training authorization beyond zero-GPU design/audit) |
| **恢复相几何 + E0 dim-probe** | `experiments/exp018_cat/analysis/`(RECOVERY_GEOMETRY_FINDINGS_20260615 + FINDINGS + probe_output_vs_hidden_NOTE) |
| **黑箱探索 recon verdicts** | `wip/blackbox_dimreduction_recon_d35/`(在途, 归属待 PI; 全判被占/平凡) |
| 最新跨 session 交接 | `canonical/sessions/handoff-*.md` (持久) + `/tmp/.../handoff-*.md`; hook 扫两处取最新 mtime |
| **GPT 交接包 (2026-06-26 交接 GPT-5.5Pro/Codex)** | `canonical/sessions/handoff-gpt-20260626/` — **00-README 入口** + AGENTS.md + 01-07 章(三机/研究/runbook/项目/纪律/Claude→GPT翻译/基础设施安全)。⚠️含发现的备份死循环故障(已修)+ 全 FLAG 漂移汇总 |
| 历史 + 偏好 | memory `MEMORY.md` (cwd=canonical 对齐 harness 自动召回) |
| 纪律全文 (D-1/D-2/D-3) | `docs/{discipline,philosophy,infra}/` + 本目录 `CLAUDE.md` |
| D29 多通道总整合 + 8 L0 证明 | `experiments/exp018_cat/dppl_bridge_verify_d21_output/MAOFIELD_L0_ROUND2_INTEGRATION_20260529.md` (+ 同 dir L0 proofs / GATE / A3 fp32 提示词) |
| paper v8 final | `experiments/exp018_cat/literature/paper_v8_final_20260516.md` |

---

*本文件 = 项目当前 state 的单一真相源。新 agent 读完此页即可开工;binding 见 §1,纪律全文见 CLAUDE.md。*
