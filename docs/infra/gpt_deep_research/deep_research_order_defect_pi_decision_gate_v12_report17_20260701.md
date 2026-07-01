RECOMMEND_PI_LOCAL_REVIEW_ONLY_KEEP_LOCK

## 简要审计

我已按首检要求核对 zip 内必需文件；所列 V12 首检文件与后续必读文件均存在、可读，且包内状态链与 V12 任务一致。解压后我本地执行了 `sha256sum -c SHA256SUMS.txt`，133 个条目全部通过；`PACKAGE_FILE_MANIFEST.sha256` 与实际解压文件表一致，没有发现缺件、坏件或任务错包迹象。（见 `PACKAGE_README.md` 3-21；`from_repo/STATE.md` 16-28；`from_repo/MD_CATALOG.md` 79-81；`from_repo/docs/infra/recovery/ORDER_DEFECT_D701_PI_DECISION_AND_ENGLISH_REWRITE_GATE_V12_TASKBOOK_20260701.md` 9-34）

数学主干可继续进入 node36 / human PI 的**锁内本地审阅**。report(15) 的对象边界仍严格限定在有限正权二向表、加权 Hilbert 空间、`C`、`A`、`B0`、`N_add`、相应正交投影、两种 stripping 算子与 `D_w` 上，没有外扩成广义 ANOVA、广义 dependent-input decomposition、广义 noncommuting-projection 理论，也没有外溢到 MaoField 经验正结论。（见 report(15) 9-18, 42-67, 132-156；`FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 17-31, 51-69, 177-205, 241-283；`BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md` 17-31, 51-80）

对三条命题的判断如下。Proposition 1 的“乘积权当且仅当 `A ⟂ B0`”证明链是自洽的：正向用边际分解，反向用 centered indicators 恢复单元格乘积恒等式。Proposition 2 的等价链也是成立的：`D_w=0` 时，对任意 `b∈B0` 有 `P_A b ∈ A∩B0`，而引理给出 `A∩B0={0}`，故 `P_A b=0`，于是 `A ⟂ B0`，再回推 product weight；在 product-weight 情形下两种 stripping 都化简为 `I-P_N`。Proposition 3 仍正确保持为**存在性**命题，不是全称命题；而且文本明确把 wrong-order 非零输出区分为 sequential stripping artifact，而不是 `(I-P_N)K` 意义下的真实加性残差。（见 report(15) 71-96；`FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md` 71-80, 110-215；`FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 177-239, 243-283）

精确 `2 x 2` 证书一致。我核对了 Markdown、JSON 与 exact-witness 脚本，并在 bundle 内本地重跑 exact 脚本；`all_checks_passed=True`。主 witness 仍是 `K=(7/11,-4/11,7/11,-4/11)`，并满足 `(I-P_N)K=0`、`R_B_then_Q K=0`、`R_Q_then_B K=(1/32,5/168,-1/96,-1/84)`、`||R_Q_then_B K||_w^2=61/177408`。整文件哈希在重跑后会因 runtime 字段漂移，但这正与本地 verification 记录一致，因此相关数学字段而非 whole-file rerun hash 才是应比较对象。（见 report(15) 102-124；`EXACT_WITNESS_V1_4_20260629.md` 30-66；`exact_witness_v1_4_20260629.json`；`scripts/debranded_residual_transport_exact_witness_v1_4.py` 126-220；`ORDER_DEFECT_D630_REPORT9_LOCAL_VERIFICATION_20260630.md` 25-49）

deterministic harness 也保持在正确层级。我本地重跑了 harness；`all_synthetic_controls_passed=True`，`threshold_contract_sha256` 与 bundle 内记录一致，canonical wording-lock 句子存在。report(15) 虽然引用了一个包外 scratch 路径，但它并没有把 harness 提升成 theorem proof；bundle 内正式文本、wording lock、report9 local verification 都仍把 harness 固定在 regression support only。（见 report(15) 126-130, 152-154；`SYNTHETIC_HARNESS_V1_3_20260628.md` 7-18, 32-77, 96-107；`WORDING_LOCK_V1_6_20260629.md` 7-25；`ORDER_DEFECT_D630_REPORT9_LOCAL_VERIFICATION_20260630.md` 51-79）

书目/定位仍应保持在 `MEDIUM duplicate risk`，不能软化。bundle 内最安全的定位仍是：

```text
Proposition 1: COMPLETE_LOCAL_DRAFT
Proposition 2: COMPLETE_LOCAL_DRAFT
Proposition 3: COMPLETE_LOCAL_DRAFT
Exact 2 x 2 rational witness: CERTIFICATE
Deterministic harness: HARNESS_ONLY
Bibliography/positioning: COMPLETE_LOCAL_DRAFT with MEDIUM duplicate risk
Overall status: BOUNDARY_LOCKED_LOCAL_DRAFT_CANDIDATE_ONLY
Mode B MaoField empirical status: insufficient_artifact
```

这组 live labels 与 V12 包、STATE、report(16) adoption note、report(15) adoption note一致，应原样保留。（见 `PACKAGE_README.md` 9-21；`STATE.md` 16-28；`ORDER_DEFECT_DRAFT_CANDIDATE_REVIEW_V11_REPORT16_ADOPTION_NOTE_20260701.md` 37-88；`ORDER_DEFECT_BOUNDARY_LOCKED_DRAFT_V10_REPORT15_ADOPTION_NOTE_20260701.md` 44-61）

综合判断：当前**不需要 stop/park**，也**不宜马上升级为英文重写候选**。更稳妥的结论是：把 report(15) 继续视为**中文锁内本地审阅件**，PI 可在锁内审阅，但继续保持 lock；若未来真要做英文稿，应从 formal note / proof-repair candidate / exact witness / harness boundary / bibliography 重新写，不应逐句翻译 report(15)。（见 report(16) 22-26, 37-41；V12 taskbook 14-19, 73-82）

## 剩余硬阻塞

当前**没有数学硬阻塞**妨碍 node36 / human PI 在锁内审阅 report(15)。

但有一个**后续重写前的强制前提**：`/tmp/orderdefect_v10/rerun/harness.json` 不能再作为未来本地草稿、未来包、未来 adoption-note、未来 PI-facing rewrite 的证据路径。路径卫生说明已经明确：不要改写归档的 report(15) 原件；而应在未来本地稿件、adoption notes、package records、prompts 中改引 bundle 内稳定路径。（见 `ORDER_DEFECT_REPORT15_PATH_HYGIENE_NOTE_20260701.md` 10-18, 20-44；report(16) 22-24, 37-38）

换句话说，这一项**不是当前中文本地审阅的 blocker**，但它是**任何后续 local rewrite 的 blocker**。

## 剩余软风险

第一，`MEDIUM duplicate risk` 是实质性风险，不是礼貌性保留。只要措辞稍微外扩到“general theory / ANOVA-type decomposition / projection theory”，就会重新撞上近邻文献边界，因此英文重写在方向和语气上都需要 PI 先定得非常窄。（见 `BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md` 17-31, 53-80；`BIBLIOGRAPHY_RESCUE_AUDIT_20260629.md`）

第二，report(15) 目前是“边界账本 + 证明梗概 + 风险台账”混合文体，作为中文锁内审阅件是合适的，但直接拿它做英文数学短札底稿并不划算。report(16) 已明确指出：若要英文稿，应从 formal-note 体系重写，而非逐句翻译。（见 report(16) 24-26, 37-38）

第三，exact-witness 与 harness 的 rerun whole-file hash 存在环境漂移，不应再被误当成跨环境不变证据对象。比较应落在 exact 数学字段、canonical wording sentence、以及 threshold contract 上，而不是 rerun 文件哈希。（见 `ORDER_DEFECT_D630_REPORT9_LOCAL_VERIFICATION_20260630.md` 47-49, 59-79；`MATH_PROOF_RESCUE_AUDIT_20260629.md` 33-48）

第四，我没有发现 report(15) / report(16) 中有**肯定式** forbidden claim。相关词项出现于免责声明、禁止清单、或边界账本，而不是被当作已授权事实来背书；这一点仍需 PI 本地复核时保持警觉。（见 report(15) 138-156；`ORDER_DEFECT_DRAFT_CANDIDATE_REVIEW_V11_REPORT16_ADOPTION_NOTE_20260701.md` 84-88）

## PI 决策清单

- 确认本轮只做**锁内本地审阅**，不改变当前总体状态标签。
- 确认三条 live labels、`CERTIFICATE`、`HARNESS_ONLY`、`MEDIUM duplicate risk`、`BOUNDARY_LOCKED_LOCAL_DRAFT_CANDIDATE_ONLY`、`insufficient_artifact` 原样保留。
- 复核 Proposition 3 仍是**存在性** witness，不得写成“所有输入都出现顺序差异”。
- 复核正文始终区分 `(I-P_N)K` 的 true additive residual 与 wrong-order sequential stripping output。
- 复核 exact `2 x 2` 见证核心值不被改写，尤其是 `61/177408`。
- 复核 harness 仍只作 regression support，canonical wording-lock 句子保持不变。
- 记录：`/tmp/orderdefect_v10/rerun/harness.json` 只在归档 report(15) 中保留为历史痕迹；任何未来 rewrite / package-facing 文本必须改引稳定 bundle 路径。
- 若 PI 以后授权英文稿，要求**从 formal notes / proof-repair candidate / exact witness / harness boundary / bibliography 重写**，而非直译 report(15)。
- 继续把 bibliography/positioning 锁定在最窄句式，不降低 `MEDIUM duplicate risk`。
- 继续核对所有 forbidden claims 只出现在否定/禁止语境中，不出现在正面背书语境中。

## 给 human PI 的三个短问题

1. 你现在更想把 report(15) 保持为**中文本地审阅件**，还是希望尽快进入一个**全新英文重写提纲**？
2. 如果后续确实授权英文稿，你偏好它是**terse theorem note**、**methodological cautionary note**，还是**appendix-style certificate note**？
3. 对 `MEDIUM duplicate risk`，你的容忍策略是**窄做推进**、**先补更多书目复核**，还是**先停放**？

This remains a boundary-locked PI decision and local rewrite gate only. Node36
and the human PI retain final authority. This is not paper-ready,
preprint-ready, posted, or submission-authorized.