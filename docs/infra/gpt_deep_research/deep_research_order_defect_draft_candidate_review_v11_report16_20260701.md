DRAFT_CANDIDATE_ACCEPTABLE_FOR_NODE36_PI_LOCAL_REVIEW

## 简要审计结论

我先按任务书要求完成了包首检。`PACKAGE_README.md`、`SHA256SUMS.txt`、`PACKAGE_FILE_MANIFEST.sha256`、`from_repo/STATE.md`、`from_repo/MD_CATALOG.md`、report(15) 主文、其 adoption note、V11 taskbook 与 V11 package record 均存在、可读，并且与当前 V11 任务链一致；包内 `SHA256SUMS.txt` 校验通过，`PACKAGE_FILE_MANIFEST.sha256` 中列出的文件也能在解压内容中逐项对上，没有发现缺件或 manifest 不一致。

就数学主干而言，report(15) 对 Proposition 1、Proposition 2、Proposition 3 的表述与当前主证明链一致，且都没有越出“有限正权二向表”边界。支持文件仍是 `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 与 `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md`。其中，Proposition 1 的“乘积权当且仅当 `A ⟂ B0`”表述正确；Proposition 2 对 `D_w=0`、两种 stripping 顺序一致、以及 product-weight 条件之间的等价链也写对了；Proposition 3 保留了正确的存在性量词，并明确把非零 wrong-order 输出解释为 sequential stripping artifact，而不是 `(I-P_N)K` 意义下的真实加性残差。

精确 `2 x 2` witness 的数值也一致。`from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md`、对应 JSON、以及 `from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py` 彼此一致；在 bundle 内重跑该脚本后，数学字段与 canonical JSON 一致，主 witness 仍给出
`K = (7/11,-4/11,7/11,-4/11)`、
`(I-P_N)K = 0`、
`R_B_then_Q K = 0`、
`R_Q_then_B K = (1/32, 5/168, -1/96, -1/84)`，
以及精确平方加权范数 `61/177408`。运行环境字段会引起整文件哈希漂移，但这不影响证书内容本身。

deterministic harness 的角色也保持正确。`from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md`、其 JSON、脚本 `from_repo/scripts/debranded_residual_transport_harness_v1_3.py` 与 `from_repo/docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md` 都把 harness 锁定为 regression support only；report(15) 没有把它提升成 theorem proof，也没有把 JSON 浮点输出当作证明主载体。bibliography/positioning 方面，report(15) 仍然停留在 `COMPLETE_LOCAL_DRAFT with MEDIUM duplicate risk`，与 `from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md` 及 `from_repo/docs/infra/recovery/BIBLIOGRAPHY_RESCUE_AUDIT_20260629.md` 一致，没有擅自把定位扩成广义 ANOVA、广义 dependent-input decomposition 或广义 noncommuting-projection 理论。

总体判断是：report(15) 的局部草稿候选在数学边界、live labels、存在性措辞、true additive residual 与 wrong-order artifact 的区分、exact witness 数值、harness 角色、以及 duplicate-risk 定位方面都达到了“可供 node36/PI 进行本地审阅”的标准。我没有发现需要立刻停止使用该草稿的数学性 blocker，也没有发现把 emergency lock 实质抬升的正面越界表述。

## 残留软风险

第一，report(15) 在 “Harness 边界与相关工作重复风险” 一段里仍保留了一个包外路径引用：`/tmp/orderdefect_v10/rerun/harness.json`。这不是当前 bundle 内证据路径，因此属于归档卫生风险，而不是数学主干风险。它不妨碍 node36/PI 做本地审阅，但在后续继续整理本地说明稿时，最好把这一处统一改写为 bundle 内文件引用，例如 `from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json`，必要时再辅以 `from_repo/docs/infra/recovery/ORDER_DEFECT_D630_REPORT9_LOCAL_VERIFICATION_20260630.md`。

第二，report(15) 采用的是中文局部草稿体裁，适合 node36/PI 当前锁内审阅；但如果未来真的需要形成英文数学短札，本稿更适合“基于同一 bundle 重新英文重写”，而不是逐句直译。原因不是数学不对，而是当前文本兼具边界账本、状态保护语与数学摘要三种功能，适合作为 locked local draft，不适合作为直接外文短札底稿。

第三，bibliography/positioning 虽然已经收窄，但 `MEDIUM duplicate risk` 仍是实质性保留项，不应在后续本地讨论中被软化。任何未来英文说明只要把措辞往“大理论”“广义 decomposition”“广义 projection theory”方向扩一点，就会重新撞上该风险。

## Node36 与 PI 本地审查清单

本地审查时，建议 node36 与 human PI 逐项确认以下几点。

- 保持 live labels 原样，不改写 `Proposition 1/2/3`、`CERTIFICATE`、`HARNESS_ONLY`、`MEDIUM duplicate risk`、`BOUNDARY_LOCKED_LOCAL_DRAFT_CANDIDATE_ONLY`、`insufficient_artifact`。
- 复核 Proposition 3 的量词仍是存在性，不把 pure-main-effect witness 写成全称断言。
- 复核正文始终区分 `(I-P_N)K` 的真实加性残差与 wrong-order sequential stripping 输出，不把后者误写成真实 interaction residual。
- 复核 exact witness 的主数值仍是 `61/177408`，且主向量与两种顺序输出不被改写。
- 复核 harness 仍仅作 regression support，继续保留 wording lock 中的 canonical sentence。
- 把 report(15) 中的包外 `/tmp/.../harness.json` 引用改回 bundle 内文件引用，作为归档卫生清理。
- 若以后要做英文短札，不做直译，而是以 `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`、`FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md`、`EXACT_WITNESS_V1_4_20260629.md` 和 `BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md` 为骨架重新重写。
- 继续把 bibliography/positioning 保持在窄定位，不降低 `MEDIUM duplicate risk`。
- 继续确认全文没有把外部模型提升为 proof authority、bibliography authority、posting authority 或 submission authority。
- 保留最终锁定免责声明，不把当前状态解释为任何公开发布或投稿状态。

This remains a boundary-locked local draft candidate review only. Node36 and
the human PI retain final authority. This is not paper-ready, preprint-ready,
posted, or submission-authorized.