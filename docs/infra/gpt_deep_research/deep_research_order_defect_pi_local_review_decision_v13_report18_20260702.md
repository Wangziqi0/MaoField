# CONFIRM_PI_LOCAL_REVIEW_ONLY_KEEP_LOCK

## 简要审计

我确认本轮最稳妥的结论仍是 **`CONFIRM_PI_LOCAL_REVIEW_ONLY_KEEP_LOCK`**。依据包内 README、`STATE.md`、V13 taskbook、V13 package record、report(17) 及其 adoption note，本包的目标就是在 **锁内** 帮助 node36 与 human PI 做本地审阅决策，而不是解除紧急锁、不是英文重写关卡、不是发布关卡，也不是任何 proof/bibliography/posting/submission authority 的替代物；当前本地状态已经明确写成 `PI_LOCAL_REVIEW_ONLY_KEEP_LOCK`、`BOUNDARY_LOCKED_LOCAL_DRAFT_CANDIDATE_ONLY`、`EMERGENCY_LOCK_STILL_ACTIVE`，且 V13 明确禁止输出英文稿。由此看，继续保持“中文 PI 锁内本地审阅件”的决定，与包的当前任务、状态链和边界约束完全一致。

report(17) 的外部建议是 `RECOMMEND_PI_LOCAL_REVIEW_ONLY_KEEP_LOCK`，而 node36 的采纳已经收窄为 `PI_LOCAL_REVIEW_ONLY_KEEP_LOCK`；其 adoption note 同时明确：report(15) 目前可以作为 **中文锁内本地审阅件** 被 node36 与 human PI 阅读，没有当前数学硬阻塞，但任何未来英文稿若要存在，都必须在 **PI 另行授权**、并且用 **新的包** 重新开启独立 English rewrite gate，而不是在本任务内直接生成或默许。V13 taskbook 也重复了这一点。基于这一链条，我不建议此刻切换到 `REQUEST_HYGIENE_PATCH_BEFORE_PI_LOCAL_REVIEW`，也不建议此刻切换到 `RECOMMEND_SEPARATE_ENGLISH_REWRITE_GATE_AFTER_PI_CHOICE`。后者只能在 **PI 明确选择之后** 再单独开启。

必须原样保留的 live labels，我在本审计中维持如下，不作任何升格或软化：

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

## 包完整性与任务一致性

首检要求列出的必需文件在压缩包内都存在且可读：`PACKAGE_README.md`、`SHA256SUMS.txt`、`PACKAGE_FILE_MANIFEST.sha256`、`from_repo/STATE.md`、`from_repo/MD_CATALOG.md`、report(17)、report(17) adoption note、V13 taskbook、V13 package record 均已出现，并且它们对 V13 任务的描述彼此一致：V13 是 “PI local-review decision gate only”，不是英文写作或公开发布任务。`MD_CATALOG.md` 也把当前权威入口指到了 V13 prompt、V13 taskbook、V13 package record 与 node19 V13 zip。

我还基于包内文件做了本地一致性复核：`SHA256SUMS.txt` 对包内文件定义了内部身份，V13 package record 说明了 zip 内部用 `SHA256SUMS.txt` 与 `PACKAGE_FILE_MANIFEST.sha256` 做 package-content identity，而最终 zip 容器哈希应在 zip 外部记录；这与包的双层哈希政策一致。就本地核对结果看，`sha256sum -c SHA256SUMS.txt` 全部通过，`PACKAGE_FILE_LIST.txt` 的哈希与 `PACKAGE_FILE_MANIFEST.sha256` 给出的值一致，文件表数量也与实际解压文件数对齐。因此就“缺件、坏件、任务错包或 bundle 自相矛盾”而言，我没有发现触发 `INSUFFICIENT_BUNDLE` 的证据。

这也意味着：本任务应当继续停留在 **“决策与边界审计”** 层，而不是进入文稿起草层。任何偏离这一点的输出，都会与包 README、V13 taskbook 和 package record 相冲突。

## 数学与对象边界审计

本 bundle 对数学对象的边界限定是清晰而稳定的：只审有限正权二向表 `X = Q x B`、加权内积空间、常数子空间 `C`、中心化行主效应空间 `A`、中心化列主效应空间 `B0`、加性 nuisance 空间 `N_add = C + A + B0`、相应加权正交投影、两种 ordered stripping operators 与 `D_w`，以及精确 `2 x 2` witness。formal note 与 proof-repair candidate 都把讨论限定在这个有限对象里，并明确否认将其外推为广义 ANOVA、广义 dependent-input decomposition、广义 noncommuting projection theory 或 MaoField empirical result。report(15)、report(16)、report(17) 也都保持了这一边界。

就命题本身而言，我的审计结论与 report(17) 一致，且可以由 formal note / repair candidate 的证明链支撑：

Proposition 1 的“乘积权当且仅当 `A ⟂ B0`”表述是自洽的。正向用 `w(q,b)=w_Q(q)w_B(b)` 的边际分解，直接得到任意 `a∈A` 与 `b∈B0` 的加权内积为零；反向则通过 centered indicators `a_q0(q)=1_{q=q0}-w_Q(q0)` 与 `b_b0(b)=1_{b=b0}-w_B(b0)` 展开得到 `<a_q0,b_b0>_w = w(q0,b0)-w_Q(q0)w_B(b0)`，从而恢复每个单元格上的乘积权恒等式。这个证明不依赖广义理论，只依赖当前有限对象中的有限和与 centered indicators。

Proposition 2 的等价链也成立。formal note 与 repair candidate 的关键步骤完全一致：若 `w` 是乘积权，则由 Proposition 1 得 `A ⟂ B0`，于是 `C`、`A`、`B0` 成为正交直和，`P_N=P_C+P_A+P_B0` 且 `P_AP_{B0}=P_{B0}P_A=0`，两种 ordered stripping 都化简为 `I-P_N`；反向若 `D_w=0`，对任意 `b∈B0` 有 `0=D_w b=P_{B0}P_A b-P_A b`，故 `P_A b=P_{B0}P_A b∈A∩B0`，而 `A∩B0={0}`，所以 `P_A b=0`，进一步推出 `A ⟂ B0`，再由 Proposition 1 回推 product weight。等价于 `R_Q_then_B = R_B_then_Q` 则只是 `D_w` 的定义改写。

Proposition 3 在当前 bundle 中保留了正确的 **存在性** 量词，而没有被写成全称命题。formal note 先给出量词护栏：`D_w != 0` 的正确结论是 “there exists a witness signal”，并明确指出 “It is false to claim that every input differs”。随后在 Proposition 3 中构造了 `K ∈ B0` 的纯主效应 witness：因为非乘积权等价于 `A` 与 `B0` 不正交，所以存在 `b∈B0` 使 `P_A b ≠ 0`；令 `K=b`，则 `(I-P_N)K = 0`、`R_B_then_Q K = 0`，且若 `R_Q_then_B K = 0` 则会推出 `P_A K ∈ A∩B0={0}` 与 `P_AK ≠ 0` 矛盾，所以 `R_Q_then_B K ≠ 0`。这正是“wrong-order 非零输出是 sequential stripping artifact，而不是 true additive residual”的逻辑核心。

因此，我对数学正确性的最终判断是：在 **当前受控有限对象边界内**，Proposition 1、Proposition 2、Proposition 3 维持 `COMPLETE_LOCAL_DRAFT` 是合理的；同时必须继续坚持两个边界句式，不得滑移：其一，非乘积纯主效应 witness 是 **存在性命题**；其二，`(I-P_N)K` 的 true additive residual 与 wrong-order sequential stripping output 必须严格区分。

## 证书、harness 与书目边界

精确 `2 x 2` 证书在 bundle 内是自洽的。certificate Markdown、canonical JSON 与 exact script 一致地给出主 witness
`K = ['7/11','-4/11','7/11','-4/11']`，并给出
`(I-P_N)K = 0`、
`R_B_then_Q K = 0`、
`R_Q_then_B K = ['1/32','5/168','-1/96','-1/84']`、
`||R_Q_then_B K||_w^2 = 61/177408`。
exact script 还把这些内容编码为明确检查项：`main_b0_true_additive_residual_zero`、`main_b0_zero_order_residual_zero`、`main_b0_artifact_vector_exact`、`main_b0_artifact_norm_sq_exact` 等，并要求 `order_defect_equals_commutator_exact` 与 `order_defect_nonzero` 为真。基于 bundle 内脚本的本地复跑，我看到 `all_checks_passed=True`；复跑 JSON 与 canonical JSON 的差异落在 `runtime` 元数据，而核心数学字段一致，这与 report9 local verification 对“whole-file hash 可能因 runtime 漂移、应核对数学证书内容”的说明一致。

deterministic harness 的角色也没有被越界。Markdown、JSON、script 与 wording lock 都反复写明：floating-point harness 只是 **deterministic regression support only**，数学 claims 由 analytic proof 与 exact rational certificate 承载，而不是由 JSON floats 承载。harness 的四个 block 分别是 `product_weight_order_independence_control`、`centered_indicator_product_iff_control`、`nonproduct_pure_main_effect_no_go_control` 与 `threshold_contract_single_source_control`；它们服务于 theorem-control / regression guard，不服务于 theorem proof，更不服务于 MaoField empirical evidence。我的本地复跑中，四个 block 仍全部为 pass，合约哈希仍为 `ec2a3a70dce8d19be5635b2b2a7f51caae17ee8e0a8bce2ec20ed4a55f9a82f6`，但这并不会改变它的 `HARNESS_ONLY` 定位。

书目与定位方面，本 bundle 仍然只能维持 `COMPLETE_LOCAL_DRAFT with MEDIUM duplicate risk`。bibliography/positioning file 明确把安全定位压缩为 `a compact finite weighted projection-order artifact note with an exact 2 x 2 witness`，同时显式否认 “new ANOVA theory / new dependent-input Hoeffding decomposition theory / new Sobol/Shapley sensitivity theory / new noncommuting projection theory / MaoField empirical evidence”。bibliography rescue audit 进一步说明：风险并不是已找到 exact duplicate，而是只要措辞向 broad theory 外扩，就会与已有 dependent-variable ANOVA/Hoeffding、projection theory 邻域发生覆盖与过度主张冲突，尤其 Lamboni 2026 被标成近邻且 duplicate risk 为 `MEDIUM`。因此这一标签不能软化。

关于 hygiene patch，我的结论是：**当前不需要因为它而阻断 PI local review**，但它对任何未来 rewrite / package-facing text 是强制前置条件。唯一明确指出的 hygiene 问题，是 report(15) 内残留了包外 scratch 路径 `/tmp/orderdefect_v10/rerun/harness.json`。path hygiene note 说得很清楚：不要改动作为归档件的 report(15) 原文；但之后的本地草稿、adoption note、package record、prompt 都必须改引稳定的 bundle 内路径。report(17) adoption note 也把它定义为 “不是当前 PI local review blocker，而是任何 future rewrite / package-facing text 的 blocker”。因此，V13 现在不必退回去要求 “先做 hygiene patch 才能给 PI 看”；但必须把这件事写进 PI checklist。

至于 forbidden claims，我没有在本次审计范围内看到被当作已授权事实去正面背书的情形。相关词项在 report(15)、report(16)、report(17) 与 adoption notes 里出现时，均位于免责声明、禁止清单、边界账本或 release blocker 语境，而不是肯定宣称语境。因此“absence of affirmative forbidden claims”这一点，目前可以维持。

## 阻塞项、风险与 PI 本地审阅清单

**剩余硬阻塞**：
就“是否允许 human PI 在锁内审阅 report(15)”这一狭义问题而言，我没有看到当前硬阻塞。包完整性通过，数学主干在受控对象内可维持本地草稿状态，exact certificate 与 harness boundary 都没有塌掉，forbidden claims 也没有被正面写成授权事实。

**剩余软风险**：
第一，`MEDIUM duplicate risk` 仍是实质风险；任何措辞扩张到 broad ANOVA / general dependent-input decomposition / projection theory，都会重新触发定位风险。第二，report(15) 的文体是“边界账本 + 证明梗概 + 风险台账”的混合体，适合中文锁内审阅，不适合直接变成英文稿底稿。第三，exact/harness 的 rerun whole-file hash 或环境浮点差异，不应再被误读为证据不稳；应比较 exact 数学字段、阈值合约哈希与 canonical boundary wording，而不是跨环境 whole-file hash。第四，路径卫生问题虽不是当前 PI 审阅阻塞，但若 PI 之后想开英文重写关卡，它会立刻变成必须先处理的 rewrite blocker。

**PI local-review checklist**：
- 确认本轮只做 **锁内本地审阅**，不解除 emergency lock，不改变 `BOUNDARY_LOCKED_LOCAL_DRAFT_CANDIDATE_ONLY`。
- 确认七条 live labels 原样保留，尤其是 `CERTIFICATE`、`HARNESS_ONLY`、`MEDIUM duplicate risk`、`insufficient_artifact`。
- 逐项复核 Proposition 3 仍然是 **存在性** witness，而不是“所有输入都出现顺序差异”。
- 逐项复核正文始终区分真实加性残差 `(I-P_N)K` 与 wrong-order sequential stripping output。
- 逐项复核 exact `2 x 2` witness 的核心数值不被改写，尤其 `61/177408`。
- 逐项复核 harness 仍然只作为 regression support，不把 JSON floats 或 pass blocks 写成 theorem proof。
- 记录 `/tmp/orderdefect_v10/rerun/harness.json` 仅保留为 report(15) 的历史痕迹；任何未来 rewrite / package-facing text 必须改引稳定 bundle 路径。
- 如果 PI 未来想要英文稿，只能 **另行授权一个新的 English rewrite gate 与新的包**，并且必须从 formal notes / proof-repair candidate / exact witness / harness boundary / bibliography 重写，不能在本任务内直译 report(15)。
- 继续把 bibliography/positioning 锁定在最窄句式，不降低 `MEDIUM duplicate risk`。
- 继续检查 forbidden claims 只出现在否定或禁止语境中，不得转写为正面背书。

**给 human PI 的三个短问题**：
- 你现在的方向选择是：继续保持 report(15) 为 **中文锁内本地审阅件**，还是在之后另开一个 **独立英文重写 gate**？
- 如果以后授权英文稿，你更偏好 **terse theorem note**、**methodological cautionary note**，还是 **appendix-style certificate note**？
- 对 `MEDIUM duplicate risk`，你的容忍策略是 **窄做推进**、**先补书目复核**，还是 **停放/停止**？

This remains a boundary-locked PI local-review decision gate only. Node36 and
the human PI retain final authority. This is not paper-ready, preprint-ready,
posted, or submission-authorized.