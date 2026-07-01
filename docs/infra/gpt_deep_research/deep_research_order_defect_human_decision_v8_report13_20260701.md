# Order-Defect V8 人工决策锁内审计报告

## Verdict

`HUMAN_DECISION_UNDER_LOCK_ACCEPTED`

理由很窄：V8 包首检所要求的关键文件都在包内，且 report(12) 的结论被 node36 明确窄化为 `PREPARE_HUMAN_DECISION_UNDER_LOCK`，并继续维持 `LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK`、`KEEP_LOCK_AND_FIX` 与 `LOCKED_NO_PAPER_BODY`。V8 的任务书也把本轮输出限定为“人类决策备忘录”级别，而不是正文起草或任何权限升级。首检文件与状态链在 `PACKAGE_README.md`、`from_repo/STATE.md`、`from_repo/MD_CATALOG.md`、report(12) 采纳说明、V8 taskbook 之间一致。`PACKAGE_README.md:7-31,64-117`；`from_repo/STATE.md:16,24-28`；`from_repo/MD_CATALOG.md:76-82`；`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_POST_V6_DECISION_GATE_V7_REPORT12_ADOPTION_NOTE_20260630.md:10-19,62-87`；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_HUMAN_DECISION_UNDER_LOCK_V8_TASKBOOK_20260630.md:8-18,25-33,78-106`

我还对解压后的 bundle 本地执行了完整性复验：`sha256sum -c PACKAGE_FILE_MANIFEST.sha256` 返回 `OK=116 BAD=0`，且 `SHA256SUMS.txt` 与 `PACKAGE_FILE_MANIFEST.sha256` 无差异；这与包内声明的“两层身份策略”相符。该点支持“包完整且可审”，但**不**改变当前锁状态。`PACKAGE_README.md:50-62`；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_HUMAN_DECISION_UNDER_LOCK_V8_TASKBOOK_20260630.md:108-118`

## Package and Status Chain

V8 bundle 与状态链是相干的。首检要求中的 `PACKAGE_README.md`、`SHA256SUMS.txt`、`PACKAGE_FILE_MANIFEST.sha256`、report(12) 原报告、report(12) 采纳说明、V8 taskbook、V8 package record 都存在；README 与 V8 taskbook 把这些文件列为应包含内容，而两份内部散列清单也分别列出 V8 package record、report(12)、其 adoption note、V8 taskbook。`PACKAGE_README.md:64-84`；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_HUMAN_DECISION_UNDER_LOCK_V8_TASKBOOK_20260630.md:36-60`；`SHA256SUMS.txt:8,64,72,106`；`PACKAGE_FILE_MANIFEST.sha256:8,64,72,106`

状态链也没有漂移：`from_repo/STATE.md` 把当前动作写成 `PREPARE_HUMAN_DECISION_UNDER_LOCK`，同时保留 `LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK`、`KEEP_LOCK_AND_FIX`、`LOCKED_NO_PAPER_BODY` 与 `insufficient_artifact`；`from_repo/MD_CATALOG.md` 在 D630 当前入口和当前 RAG authoritative index 两处重复同一链条；V8 taskbook 再次把同一 verdict chain、同一 live labels、同一输出边界写死。就“是否还有 package identity、status-chain、RAG-locator blocker”这一问，我没有发现新的阻断项。`from_repo/STATE.md:16,24-28`；`from_repo/MD_CATALOG.md:76-82`；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_HUMAN_DECISION_UNDER_LOCK_V8_TASKBOOK_20260630.md:25-33,65-87,108-118`

report(12) 对 `PREPARE_HUMAN_DECISION_UNDER_LOCK` 的支持在 bundle 内部是有效的：其原报告明说“未见剩余的 package identity、status-chain、或 RAG-locator blocker”，并把推荐动作写成 `PREPARE_HUMAN_DECISION_UNDER_LOCK`；node36 的采纳说明仅接受这一窄动作，不允许越界。`from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_post_v6_decision_gate_v7_report12_20260630.md:13-21,59-73`；`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_POST_V6_DECISION_GATE_V7_REPORT12_ADOPTION_NOTE_20260630.md:16-19,23-36,64-74`

## Proof Boundary

Proposition 1/2/3 仍然只是受控有限对象内部的 `COMPLETE_LOCAL_DRAFT`，没有被升格为外部证明权威。这个边界在本 bundle 中连续重复：`from_repo/STATE.md`、V8 taskbook、report(9) adoption note、local-draft taskbook 都把三条命题维持在 `COMPLETE_LOCAL_DRAFT`，并且明确限定在“finite positive weighted two-way-table object”内。`from_repo/STATE.md:16,25-28`；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_HUMAN_DECISION_UNDER_LOCK_V8_TASKBOOK_20260630.md:65-76`；`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_PROOF_REPAIR_RECHECK_REPORT9_ADOPTION_NOTE_20260630.md:16-18,46-48,54-63`；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_LOCAL_DRAFT_LOCKED_TASKBOOK_20260630.md:22-37,84-98`

形式对象边界也守住了。当前 proof-repair candidate 只审计这一有限维对象：`X=Q x B`、加权内积、`C`、`A`、`B0`、`N_add`、加权正交投影、以及 `R_Q_then_B`、`R_B_then_Q`、`D_w`。文档同时明确声明：这不是新理论，也不是经验性结果。Proposition 2 与 Proposition 3 的 repair candidate 全部写在这一边界内部。`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:7-32,36-69,110-215`

因此，对“是否还存在阻止人类在锁内作下一步判断的 proof gap”这一**决策门问题**，我没有看到本 bundle 内出现新的证明性阻断；但这并不意味着证明层级被升级，只意味着目前材料足以进入“是否授权后续单独短札起草提示词”的人工判断。`from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_post_v6_decision_gate_v7_report12_20260630.md:23-31,59-73`；`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_POST_V6_DECISION_GATE_V7_REPORT12_ADOPTION_NOTE_20260630.md:16-19,25-35`

## Certificate and Harness Boundary

exact 2×2 witness 被正确限制在 `CERTIFICATE`。证书文档把自己定义为“synthetic-only exact rational certificate”，明确不是经验性结果，也不是完成版形式系统；解释段进一步写明它**不替代**解析性证明。proof-repair candidate 也把它称为“certificate-level example”，并明言它不会升级整套 proof stack 或经验状态。机读 JSON 与脚本的 `status` / `evidence_boundary` 字段也保持同一口径。`from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md:5-7,16-28,62-66`；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:217-240`；`from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json:216`；`from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py:167-185,223-231`

deterministic floating-point harness 也被正确限制在 `HARNESS_ONLY`。Markdown、JSON、脚本三处都把它固定为“deterministic regression support only”；V1.6 wording lock 把该边界句锁成 canonical sentence，并列出一串被阻断的解释；local verification 再次确认 harness 仍是 `HARNESS_ONLY`，且不承担定理证明责任。换言之，我没有看到任何现行 live wording 把证书抬到 `CERTIFICATE` 之上，或把 harness 抬到 `HARNESS_ONLY` 之上。`from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md:7-18,96-107,109-126`；`from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json:9-15,209-212`；`from_repo/scripts/debranded_residual_transport_harness_v1_3.py:4-6,25-29,407-422`；`from_repo/docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md:7-18,27-52`；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_REPORT9_LOCAL_VERIFICATION_20260630.md:73-80,83-92`

## Bibliography and Duplicate Risk

bibliography/positioning 仍然足够保守。它把安全 claim 压到“compact finite weighted projection-order artifact note with an exact 2 x 2 witness”，并显式否认自己是在提出广义理论、新型分解理论、新的投影视角总论或任何经验性证据。与当前 live label 对应，V8 taskbook 和 `STATE.md` 都把该层级标记为 `COMPLETE_LOCAL_DRAFT with MEDIUM duplicate risk`。`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:17-31`；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_HUMAN_DECISION_UNDER_LOCK_V8_TASKBOOK_20260630.md:67-75`；`from_repo/STATE.md:16,25-27`

重复风险与元数据 caveat 也仍然是保守写法，而不是被冲淡。该文献记录说明：未识别到“exact duplicate”，但真实风险在于越界宣称进入已被占据的宽理论空间；因此贡献层级必须保持在有限正权二向表、主效应正交性、顺序独立性与 exact 2×2 certificate 这一级。对 Lamboni 2026 这一近邻，文档只承认其 DOI / publisher online record 地位，并明确提醒不要把该本地记录当成定稿级元数据依据。就“是否可进入人类决策”而言，这已经够保守；就“是否可直接进入发表叙述”而言，显然还不够，而 bundle 也没有这么声称。`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:33-49,53-80`

## Forbidden-Claim Scan

在我读取的受控 V8 证据链里，风险词串的出现主要集中在三种负面语境：一是 taskbook / adoption note / package record 的禁止清单，二是 wording lock 的 blocked phrases，三是全仓扫描库存。V8 taskbook 和 report(12) 采纳说明都把越界升级表述明文排除；wording lock 进一步把若干高风险短语固定为 blocked phrases。`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_HUMAN_DECISION_UNDER_LOCK_V8_TASKBOOK_20260630.md:93-106`；`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_POST_V6_DECISION_GATE_V7_REPORT12_ADOPTION_NOTE_20260630.md:38-60`；`from_repo/docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md:27-52`

`FORBIDDEN_CLAIMS_SCAN_20260629.md` 自己就声明它只是 semantic-risk locator，不是最终人工判断；摘要是 `BLOCKER: 0`、`WARNING: 247112`。这说明 bundle 覆盖的更大仓库里确实有大量历史风险字符串库存，但它们不能自动算作当前 live endorsement。结合上面的 taskbook、adoption note、wording lock，我的判断是：**未发现被当前受控 bundle 正面背书的禁用断言**。`from_repo/docs/infra/recovery/FORBIDDEN_CLAIMS_SCAN_20260629.md:5-13,15-34`

## Human Decision Memo

给 node36 与 human PI 的精确决策建议是：**是否授权一个后续、单独、边界锁定的 short-note drafting prompt**。该授权若给出，其依据只能是当前 bundle 已达到“可进入人工决策”的阈值，而不是任何证明权威、文献权威、正文解锁或经验状态升级。`PACKAGE_README.md:24-31,91-117`；`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_POST_V6_DECISION_GATE_V7_REPORT12_ADOPTION_NOTE_20260630.md:64-87`；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_HUMAN_DECISION_UNDER_LOCK_V8_TASKBOOK_20260630.md:80-106`

若 PI 授权，下一轮也应被严格限制为“未来单独提示词的授权与边界控制”，而不是直接进入正文。允许前提只能是：命题 1/2/3 继续停留在 `COMPLETE_LOCAL_DRAFT`；exact witness 继续停留在 `CERTIFICATE`；harness 继续停留在 `HARNESS_ONLY`；bibliography 继续停留在带 `MEDIUM duplicate risk` 的 local draft；整体仍维持 `LOCKED_NO_PAPER_BODY` 与 `insufficient_artifact`。`from_repo/STATE.md:16,24-28`；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_HUMAN_DECISION_UNDER_LOCK_V8_TASKBOOK_20260630.md:65-76,89-106`；`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_POST_V6_DECISION_GATE_V7_REPORT12_ADOPTION_NOTE_20260630.md:25-36,78-87`

若 PI 不授权，则本 bundle 支持的唯一安全动作就是继续维持锁，并只允许做证明边界、文献措辞、包身份或状态链层面的后续修补，而**不是**把当前材料外推成更高结论。主要残余风险不是“缺材料”，而是“越边界叙述”：把有限对象推广成宽理论、把证书/哈尼斯误升格、或把 RAG 从 locator 误当成证据。`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:7-32`；`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:53-80`；`from_repo/MD_CATALOG.md:81-82`

## Remaining Blockers

`no human-decision blocker found; emergency lock still active`

继续存在的只是**非阻断性的持续边界**：local-draft ceiling 不变，正文锁不变，证书与 harness 不提级，bibliography 仍保留 `MEDIUM duplicate risk`，Mode B 仍是 `insufficient_artifact`。这些都是“进入人工决策时必须继续保留的锁”，而不是“在再次 Pro 审计前必须先补掉的缺口”。`from_repo/STATE.md:16,24-28`；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_HUMAN_DECISION_UNDER_LOCK_V8_TASKBOOK_20260630.md:65-76,89-106`；`from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_post_v6_decision_gate_v7_report12_20260630.md:59-73`

## Recommended Node36 Action

`ASK_PI_FOR_SEPARATE_DRAFT_AUTHORIZATION_UNDER_LOCK`

推荐理由是：report(12) 已被 node36 窄采纳为 `PREPARE_HUMAN_DECISION_UNDER_LOCK`；V8 包的任务被明确定义为“帮助准备人类 PI 的下一步判断”，而不是直接起草正文；当前 bundle 已经满足进入该人工判断所需的包完整性、状态链一致性、对象边界控制、证书/哈尼斯分级、文献保守性与禁用断言控制。`PACKAGE_README.md:12-31,64-117`；`from_repo/STATE.md:16,24-28`；`from_repo/MD_CATALOG.md:76-82`；`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_POST_V6_DECISION_GATE_V7_REPORT12_ADOPTION_NOTE_20260630.md:10-19,23-36,64-87`；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_HUMAN_DECISION_UNDER_LOCK_V8_TASKBOOK_20260630.md:8-18,25-33,80-118`