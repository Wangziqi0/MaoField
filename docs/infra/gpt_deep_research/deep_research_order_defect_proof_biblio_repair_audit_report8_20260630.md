# Order-Defect Proof Repair and Bibliography Audit

## 审计摘要

**Current Verdict**

`KEEP_LOCK_AND_FIX`

理由并不含糊。bundle 内的活动指令、node36 当前状态、dual-Pro 采纳说明、以及 D630 dual-Pro repair taskbook 全都把当前轮次限定为 recovery / proof / bibliography repair，而不是论文正文起草；同时，它们一致把当前项目上限锁在 `definitions_and_harness_viable_only`，把 MaoField 的 Mode B 状态锁在 `insufficient_artifact`。因此，当前总状态仍然是“继续上锁并修补”，而不是“解锁进入短札起草”。（`pro_prompt/GPT55_PRO_ORDER_DEFECT_PROOF_BIBLIO_REPAIR_AUDIT_V3_PROMPT_20260630.md`, L17-L31, L76-L98, L147-L179；`from_repo/STATE.md`, L16-L18, L24-L28；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_DUAL_PRO_REPAIR_TASKBOOK_20260630.md`, L8-L23, L45-L68；`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_RECOVERY_REPAIR_DUAL_PRO_AUDIT_ADOPTION_NOTE_20260630.md`, L24-L39, L42-L60）

**Status and RAG Consistency**

就“prompt / bundle / status / RAG record 是否一致”这一题，答案是：**基本一致，而且 bundle 自己还写明了如何处理局部旧快照的残余歧义**。v3 prompt 明确要求以 `KEEP_LOCK_AND_FIX`、`definitions_and_harness_viable_only`、`insufficient_artifact` 为当前边界；`STATE.md` 用 D630 更新把 dual-Pro 报告、采纳说明、RAG 刷新结果和 emergency lock 一并写入；`MD_CATALOG.md` 也把 dual-Pro 补丁、README supersession 修补、Lamboni 元数据降格和 480 files / 10856 chunks 的 RAG 指标记成当前导航事实；RAG refresh 记录则再次说明 dual-Pro adoption refresh 已把报告、采纳说明和 taskbook 纳入默认 canonical scope，并且 smoke checks 能召回 README supersession、Lamboni 的 DOI / publisher-online-record-only 处理、以及 emergency lock / Mode B 边界。换言之，主线文件彼此对齐。需要注意的唯一细节是：`EVIDENCE_INDEX_SINCE_20260625.md` 自己已经声明 D630 overlay 会 supersede 其下方仍然残留的 D629-only 生成表格片段；因此，解释当前状态时应以 overlay、`STATE.md`、dual-Pro 采纳说明和 D630 RAG 记录为准，而不是机械照抄旧生成表。 （`pro_prompt/GPT55_PRO_ORDER_DEFECT_PROOF_BIBLIO_REPAIR_AUDIT_V3_PROMPT_20260630.md`, L76-L98；`from_repo/STATE.md`, L16-L18, L24-L28；`from_repo/MD_CATALOG.md`, L7-L10；`from_repo/docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_ORDERDEFECT_RECOVERY_REPAIR_V2_20260630.md`, L159-L224；`from_repo/docs/infra/recovery/EVIDENCE_INDEX_SINCE_20260625.md`, L5-L28）

**Gate Results**

| Gate | 结果 | 审计结论 |
|---|---|---|
| Gate 1 | **PASS** | v1.6 canonical harness sentence 已在 README、placeholder、harness md、harness JSON、harness script 中按锁定要求逐字出现；Gate Rescue Audit 也把这一点逐项判定为 PASS。 （`from_repo/docs/infra/recovery/GATE_RESCUE_AUDIT_20260629.md`, L7-L17；`from_repo/docs/infra/debranded_residual_transport/README.md`, L240-L246；`from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md`, L73-L77；`from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md`, L7-L18；`from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json`, L9-L15, L209-L212；`from_repo/scripts/debranded_residual_transport_harness_v1_3.py`, L2-L7, L24-L25；`from_repo/docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md`, L7-L25） |
| Gate 2 | **PASS** | bundle 仍把对象严格限定为有限正权二向表 / 加权 Hilbert 空间 / `C, A, B0, N`，并保留“product-weight iff orthogonality”“order-independence iff product weights”“non-product 只能给 existential witness”“wrong-order output 是 sequential stripping artifact，不是真 interaction residual”“exact 2×2 rational witness”这一整套边界。Gate Rescue Audit 对这些点逐条给出 PASS。 （`from_repo/docs/infra/recovery/GATE_RESCUE_AUDIT_20260629.md`, L19-L31, L43；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`, L16-L39, L43-L100, L106-L152, L177-L227, L229-L255, L285-L321, L360-L369；`from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md`, L16-L66） |

## 阻断条件

**Hard Blockers**

当前阻止“现在就写短札正文”的硬阻断有三项，而且它们都来自 bundle 自己，而不是外推判断。

第一，**external-model emergency lock 仍然有效**。`STATE.md` 明写当前外部模型输出只可作为 `non_authoritative_scratch` / `gate_only_audit`，不得用于 paper draft、proof authority、bibliography authority、ready/posting 决策或 claim promotion；dual-Pro taskbook 与 adoption note 重复了同一边界。只要这一锁没有被用户明确解除，就不能把本次外部审计结果升级成起草权限。 （`from_repo/STATE.md`, L16-L18, L24-L28；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_DUAL_PRO_REPAIR_TASKBOOK_20260630.md`, L25-L33；`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_RECOVERY_REPAIR_DUAL_PRO_AUDIT_ADOPTION_NOTE_20260630.md`, L21-L23, L32-L39, L81-L95）

第二，**bundle 没有展示一个已经封口的 clean committed recovery snapshot**。adoption note 虽然说明 `a0adf14` 已修复 final3 package self-consistency，但也明确写道：在双报告采纳这一轮真正提交之前，node36 仍不得声称 fully clean worktree；并且 clean-snapshot 证据应来自 git status 与 commit history，而不是 zip 自证。`STATE.md` 也保留了“after commit use `git log -1 --oneline`”这类未封口表述。这意味着当前 bundle 依然不是可直接升级为 drafting authority 的“清洁终态快照”。 （`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_RECOVERY_REPAIR_DUAL_PRO_AUDIT_ADOPTION_NOTE_20260630.md`, L62-L79；`from_repo/STATE.md`, L16-L18；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_DUAL_PRO_REPAIR_TASKBOOK_20260630.md`, L88-L99）

第三，**数学上仍没有理由把 Proposition 2 与 Proposition 3 升格为“已完成正式系统”**。taskbook 要求保留现有 proof-risk labels：Proposition 1 为 `COMPLETE_LOCAL_DRAFT`，Proposition 2 与 Proposition 3 仅为 `PLAUSIBLE_LOCAL_DRAFT`；Math Proof Rescue Audit 也给出同样分级。也就是说，未来短札若要走到“严格而狭义”的可起草状态，至少还需要一次窄范围 proof repair。 （`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_DUAL_PRO_REPAIR_TASKBOOK_20260630.md`, L58-L68；`from_repo/docs/infra/recovery/MATH_PROOF_RESCUE_AUDIT_20260629.md`, L19-L27, L59-L61）

## 证明状态

**Mathematical Proof Audit**

| 对象 | 分类 | 有限和 / 线性代数理由 |
|---|---|---|
| Proposition 1 | `COMPLETE_LOCAL_DRAFT` | 这部分是当前 bundle 中最扎实的解析证明块。正向只用乘积权把双和拆成两个边缘加权和；反向则对任意固定的 `(q_0,b_0)` 构造 centered indicators，并把内积精确展开成 `w(q0,b0)-w_Q(q0)w_B(b0)`，从而逐格推出乘积形式。其论证是全有限和、无外部装置，taskbook 与 rescue audit 都把它停在 `COMPLETE_LOCAL_DRAFT` 而不是再向上拔高。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`, L106-L152；`from_repo/docs/infra/recovery/MATH_PROOF_RESCUE_AUDIT_20260629.md`, L21-L27；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_DUAL_PRO_REPAIR_TASKBOOK_20260630.md`, L58-L68） |
| Proposition 2 | `PLAUSIBLE_LOCAL_DRAFT` | 文本中的证明思路是合理的：先把 `D_w` 写成 `P_B0P_A - P_AP_B0`；若 `w` 为 product form，则 Proposition 1 给出 `A ⟂ B0`，从而两个投影互相湮灭且 `P_N = P_C + P_A + P_B0`，于是两种顺序都化为 `I-P_N`。反方向若 `D_w=0`，对任意 `b∈B0` 有 `0=D_w b=P_B0P_A b-P_A b`，故 `P_Ab ∈ A∩B0`；再用“同时仅依赖 `q` 与 `b` 的函数必为常数，而零均值迫使该常数为 0”推出 `A∩B0={0}`，于是 `P_A|_{B0}=0`，再由 `<a,b>_w=<a,P_A b>_w` 得到 `A ⟂ B0`，最后回到 Proposition 1。这个链条在线性代数上是通的，但 bundle 自己尚未把它盖章升为 completed proof authority，所以当前最稳妥的标签仍是 `PLAUSIBLE_LOCAL_DRAFT`。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`, L156-L227；`from_repo/docs/infra/recovery/MATH_PROOF_RESCUE_AUDIT_20260629.md`, L21-L27, L28-L35；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_DUAL_PRO_REPAIR_TASKBOOK_20260630.md`, L58-L68） |
| Proposition 3 | `PLAUSIBLE_LOCAL_DRAFT` | 这里的存在性结构同样合理但仍只到本地草稿级。若权重非 product form，则 Proposition 1 给出 `A` 与 `B0` 非正交；因此至少存在 `b∈B0` 使 `P_A b ≠ 0`，否则 `P_A` 在 `B0` 上处处为零，就会反推 `A ⟂ B0`。取 `K=b` 后，因 `K∈B0⊂N`，得到 `(I-P_N)K=0`；又因 `P_CK=0` 且 `P_B0K=K`，得到 `R_B_then_QK=0`；若再假设 `R_Q_then_BK=0`，则 `(I-P_B0)P_AK=0`，从而 `P_AK∈A∩B0={0}`，与 `P_AK≠0` 矛盾。所以必有一侧 wrong-order residual 非零。这个证明是窄而可修的，但 bundle 当前并未把它升格到 complete。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`, L241-L283；`from_repo/docs/infra/recovery/MATH_PROOF_RESCUE_AUDIT_20260629.md`, L21-L27, L28-L35；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_DUAL_PRO_REPAIR_TASKBOOK_20260630.md`, L58-L68） |
| Exact witness | `COMPLETE` | 这不是一般性理论，而是证书级有限例子。formal note、exact witness markdown、exact JSON、以及 shipped exact script 对同一 `2×2` 见证给出一致数据：`K=(7/11,-4/11,7/11,-4/11)`，`(I-P_N)K=0`，`R_B_then_QK=0`，`R_Q_then_BK=(1/32,5/168,-1/96,-1/84)`，且 `||R_Q_then_BK||_w^2 = 61/177408`。脚本还用 `fractions.Fraction` 把这些等式编码为 exact checks，并要求 `order_defect_equals_commutator_exact` 与 `order_defect_nonzero` 同时成立。因此，作为“证书级例子”它已经是 complete；它的作用是验证一个最小有理见证，而不是替代一般性解析证明。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`, L285-L335；`from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md`, L30-L66；`from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json`, L24-L76, L216-L248；`from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py`, L126-L165, L192-L213） |

**Minimum Proof Repairs**

存在**安全且最小**的 repair 路径；不需要引入任何更广理论。

**Proposition 2 的最小替换定理陈述**

建议把命题严格收窄成下面这句，并在未来修稿中原样替换旧的宽松表述：

> 对有限正权重 `w` 于 `X=Q×B`，设 `C, A, B0, N=C+A+B0` 分别为常数、居中的 `q`-主效应、居中的 `b`-主效应与加性 nuisance 子空间，`P_C, P_A, P_B0, P_N` 为其在 `L^2(w)` 上的加权正交投影。定义
> `R_Q_then_B=(I-P_B0)(I-P_A)(I-P_C)`，
> `R_B_then_Q=(I-P_A)(I-P_B0)(I-P_C)`，
> `D_w = R_Q_then_B - R_B_then_Q`。
> 则下列命题等价：
> `w(q,b)=w_Q(q)w_B(b)` 对所有 `(q,b)` 成立；
> `A ⟂ B0`；
> `D_w=0`；
> `R_Q_then_B = R_B_then_Q = I-P_N`。
> 这里的结论只限于有限正权二向表，不推广到一般 dependent-input ANOVA 理论。
> 这个替换与 bundle 当前对象、记号和 claim boundary 完全同向，只是把“隐含子步骤”显式化。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`, L41-L100, L156-L227；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_DUAL_PRO_REPAIR_TASKBOOK_20260630.md`, L58-L68, L70-L86；`pro_prompt/GPT55_PRO_ORDER_DEFECT_PROOF_BIBLIO_REPAIR_AUDIT_V3_PROMPT_20260630.md`, L118-L145）

对应的**最小证明骨架**应只补三个显性步骤。第一步，单列一个子引理：`A∩B0={0}`，证明方式就是“若函数既只依赖 `q` 又只依赖 `b`，则必为常数；而 `A` 与 `B0` 的零均值条件迫使该常数为 0”。第二步，证明 `product ⇒ A ⟂ B0 ⇒ P_AP_B0=P_B0P_A=0 ⇒ R_Q_then_B = R_B_then_Q = I-P_N`。第三步，证明 `D_w=0 ⇒ P_A|_{B0}=0`：对任意 `b∈B0`，有 `0=D_w b=P_B0P_A b-P_A b`，所以 `P_A b∈A∩B0={0}`，故 `P_A b=0`；于是对任意 `a∈A,b∈B0`，`<a,b>_w=<a,P_A b>_w=0`，从而 `A ⟂ B0`，再借 Proposition 1 回到 product weights。这个 repair 不扩对象、不引入新命名、也不需要任何 paper-body 化修辞。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`, L150-L152, L170-L175, L193-L227；`from_repo/docs/infra/recovery/MATH_PROOF_RESCUE_AUDIT_20260629.md`, L21-L35）

**Proposition 3 的最小替换定理陈述**

建议把命题写成以下精确版本，而不要多说任何“普遍 order dependence”：

> 若 `w` 不是 product form，则存在 `K∈A∪B0`，使得 `K∈N`，因此 `(I-P_N)K=0`，并且恰有一个顺序的 sequential stripping residual 为零，而另一个顺序的 residual 非零。该非零量是 sequential stripping artifact，不是真 interaction residual。
> 这一定理是 existential 的；它不意味着“每个非 product 输入都发生顺序依赖”。
> 该陈述正是 current file set 已经允许的最窄版本。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`, L229-L255；`from_repo/docs/infra/recovery/GATE_RESCUE_AUDIT_20260629.md`, L27-L30；`pro_prompt/GPT55_PRO_ORDER_DEFECT_PROOF_BIBLIO_REPAIR_AUDIT_V3_PROMPT_20260630.md`, L129-L145）

对应的**最小证明骨架**同样只需把现有思路收束。先由“`w` 非 product”结合 Proposition 1 得到 `A` 与 `B0` 不正交。于是至少存在一种方向的非零投影；不失一般性，取 `b∈B0` 满足 `P_A b≠0`。令 `K=b`。因为 `K∈B0⊂N`，故 `(I-P_N)K=0`。又因为 `P_CK=0` 且 `P_B0K=K`，得 `R_B_then_QK=0`。若假设 `R_Q_then_BK=0`，则 `(I-P_B0)P_AK=0`，故 `P_AK∈B0`；但又有 `P_AK∈A`，所以 `P_AK∈A∩B0={0}`，与 `P_AK≠0` 矛盾。于是 `R_Q_then_BK≠0`。最后单独写一句解释句：该非零量来自顺序剥离，并非真 `N^\perp` 残差，因为 `K` 本身就在 `N` 内。这个证明只需要显式引用 `A∩B0={0}` 子引理与 quantifier guard 即可闭合。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`, L241-L283；`from_repo/docs/infra/recovery/MATH_PROOF_RESCUE_AUDIT_20260629.md`, L28-L35, L36-L61）

## 书目与定位

**Bibliography Audit**

当前 bundle 的 bibliography floor 已经足够支撑**保守的本地 recovery audit**。`BIBLIOGRAPHY_RESCUE_AUDIT_20260629.md` 给出了十条相关记录的 DOI / arXiv floor，并明确把它们理解为“近邻约束”，而不是未来 camera-ready 版面元数据的终审；`BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md` 也把 safe claim 收窄为“a compact finite weighted projection-order artifact note with an exact 2 x 2 witness”，并明言它**不是** new ANOVA theory、new dependent-input Hoeffding decomposition theory、new Sobol/Shapley theory、new noncommuting projection theory、也不是 MaoField empirical evidence。这个定位是保守且正确的。 （`from_repo/docs/infra/recovery/BIBLIOGRAPHY_RESCUE_AUDIT_20260629.md`, L5-L18, L24-L32；`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md`, L17-L31, L51-L80）

Lamboni 2026 是这里最需要守住元数据边界的一条。救援审计明确规定：**把 Lamboni 2026 视为 DOI / online-or-publisher-record status only，不要暗示超出抓取记录的 final print issue metadata**。当前 bundle 中的 v1.5 bibliography 文件已经按这一要求处理：它没有把 Lamboni 写成更饱满的期卷页终态，而是显式写成“DOI / publisher online record status only for current drafting”，并附带“Do not rely on this local record as final camera-ready print metadata”的警告。RAG dual-Pro refresh 还把 “Lamboni 2026 DOI / publisher-online-record-only handling” 列为 smoke check 的可检索项。就本 bundle 而言，这意味着**Lamboni 已经做到了保守修补；后续起草时只需保持这一降格，不要反向升级**。 （`from_repo/docs/infra/recovery/BIBLIOGRAPHY_RESCUE_AUDIT_20260629.md`, L20-L23；`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md`, L35-L49；`from_repo/docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_ORDERDEFECT_RECOVERY_REPAIR_V2_20260630.md`, L215-L220）

从 duplicate-risk 角度看，当前 bundle 的判断也很克制：它没有宣称找到“精确重复项”，而是把真正风险定位为**向已成熟的广义 dependent-variable ANOVA / Hoeffding-Sobol / Shapley / two-projections 文献区过度扩张**。因此，安全的相关工作说法只能是：这是一篇有限正权二向表上的 projection-order artifact note；它给出 product-weight iff orthogonality、order-independence iff product weights、existential pure-main-effect witness、以及 exact 2×2 rational certificate。不能再往 continuous measures、general dependent-input decompositions、completed formal system、或 MaoField empirical evidence 方向推进。 （`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md`, L65-L80；`from_repo/docs/infra/recovery/BIBLIOGRAPHY_RESCUE_AUDIT_20260629.md`, L24-L32；`from_repo/docs/infra/recovery/HANDOFF_TO_GPT55PRO_20260629.md`, L34-L39, L70-L83）

就“当前 bundle 内是否还有文本把 wrong-order artifact 写成 true interaction residual、或把 non-product 写成 universal claim、或把 deterministic floats 当 proof”这三个子问题而言，我的结论是：**在本次 required read set 与受控核心文件中，没有发现当前有效文本仍然这么写；相反，核心文件是明确反向写死的。** formal note 与 placeholder 都直接声明 wrong-order nonzero 是 sequential stripping artifact，不是真 interaction residual；formal note 还单列 quantifier guard，写明“there exists a witness”且“it is false to claim that every input differs”；README、placeholder、harness md/json、harness script、wording lock、taskbook、adoption note 则反复声明 floating-point harness 只是 deterministic regression support，数学责任在 analytic proof 与 exact rational certificate 上。需要补充的是：全仓扫描仍然发现 **247112** 条 WARNING，所以这一“没有发现”只对**受控文件集**成立，而不适用于 whole-repository absorption。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`, L229-L255；`from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md`, L34-L47, L120-L125, L126-L136；`from_repo/docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md`, L7-L25, L27-L52；`from_repo/docs/infra/recovery/GATE_RESCUE_AUDIT_20260629.md`, L27-L31；`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_RECOVERY_REPAIR_DUAL_PRO_AUDIT_ADOPTION_NOTE_20260630.md`, L52-L57, L83-L95；`from_repo/docs/infra/recovery/FORBIDDEN_CLAIMS_SCAN_20260629.md`, L5-L12）

## 受控范围

**Controlled File Set**

如果后续要做**proof repair**，我建议把文件集分成两层，而不是“一把吸全仓”。

第一层是**可直接作为 future proof-repair / narrow-note core inputs** 的文件。真正承担数学和相关工作主体的，应限于：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`、`from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md`、`from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json`、`from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py`、`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md`、以及 `from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md` 中那些只负责“窄题名 / 窄摘要 / forbidden claims / related-work boundary”的段落。这里面，formal note 提供解析论证草稿，exact witness 三件套提供证书级最小见证，bibliography file 提供保守定位，placeholder 只应被当成边界化的占位框架，而不是 authority source。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`, L41-L100, L106-L335；`from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md`, L30-L66；`from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json`, L24-L76, L216-L248；`from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py`, L126-L165, L192-L213；`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md`, L17-L31, L35-L80；`from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md`, L49-L77, L79-L125, L126-L167）

第二层是**可作为 boundary / gate / regression support 使用，但不得当成 theorem authority 的审计辅助文件**。这一层包括：`from_repo/STATE.md`、`from_repo/MD_CATALOG.md`、`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_DUAL_PRO_REPAIR_TASKBOOK_20260630.md`、`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_RECOVERY_REPAIR_DUAL_PRO_AUDIT_ADOPTION_NOTE_20260630.md`、`from_repo/docs/infra/recovery/GATE_RESCUE_AUDIT_20260629.md`、`from_repo/docs/infra/recovery/MATH_PROOF_RESCUE_AUDIT_20260629.md`、`from_repo/docs/infra/recovery/BIBLIOGRAPHY_RESCUE_AUDIT_20260629.md`、`from_repo/docs/infra/debranded_residual_transport/README.md`、`from_repo/docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md`、`from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md`、`from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json`、`from_repo/scripts/debranded_residual_transport_harness_v1_3.py`。这些文件的功能是钉死边界、统一措辞、回归检查与 proof-risk 分级，而不是直接证明一般命题。 （`from_repo/AGENTS.md`, L22-L24, L41-L47；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_DUAL_PRO_REPAIR_TASKBOOK_20260630.md`, L45-L68, L70-L99；`from_repo/docs/infra/recovery/GATE_RESCUE_AUDIT_20260629.md`, L7-L31, L43；`from_repo/docs/infra/recovery/MATH_PROOF_RESCUE_AUDIT_20260629.md`, L19-L27, L59-L61；`from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md`, L7-L12, L96-L107；`from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json`, L9-L15, L59-L60, L209-L212；`from_repo/scripts/debranded_residual_transport_harness_v1_3.py`, L2-L7, L24-L41）

必须保持为**superseded-risk 或 audit-only** 的文件也很清楚。dual-Pro 报告 `deep_research_order_defect_recovery_repair_dual_pro_report6_20260630.md` 与 `...report7_20260630.md` 只能算 model outputs / gate-only audit；RAG refresh record `NODE22_VECTOR_REFRESH_ORDERDEFECT_RECOVERY_REPAIR_V2_20260630.md` 只能证明“index 能定位什么”，不能证明定理；`FORBIDDEN_CLAIMS_SCAN_20260629.md` 与 `EVIDENCE_INDEX_SINCE_20260625.md` 是风险定位与导航覆盖文件，不是 theorem source；而旧的 v1.6 paper-draft prompt 家族则应始终保持 superseded-risk provenance only。bundle 自己对这些层级区分写得已经很清楚。 （`from_repo/docs/infra/recovery/EVIDENCE_INDEX_SINCE_20260625.md`, L11-L28；`from_repo/docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_ORDERDEFECT_RECOVERY_REPAIR_V2_20260630.md`, L215-L224；`from_repo/docs/infra/recovery/FORBIDDEN_CLAIMS_SCAN_20260629.md`, L5-L12；`from_repo/STATE.md`, L24-L28；`from_repo/MD_CATALOG.md`, L7-L9；`pro_prompt/GPT55_PRO_ORDER_DEFECT_PROOF_BIBLIO_REPAIR_AUDIT_V3_PROMPT_20260630.md`, L73-L74）

**Forbidden Claims**

未来任何短札都不应出现以下几类主张：已经跑完 full panel；16-cell aggregate 已存在；checkpoint loading / inference / training / new loss 已授权或已发生；MaoField residual / interaction / quotient-residual / transport / holonomy field 已被观察到；glass box broken；F3 positive；LOSO passed；completed formal system；posted 或 paper-ready preprint；broad new ANOVA theory；broad new dependent-input decomposition theory；broad new noncommuting-projection theory；以及“JSON floats 或 deterministic harness 证明了定理”。另外，也决不能把非 product case 写成“every input differs”；formal note 已明确写出这是 false。 （`pro_prompt/GPT55_PRO_ORDER_DEFECT_PROOF_BIBLIO_REPAIR_AUDIT_V3_PROMPT_20260630.md`, L100-L116, L166-L173；`from_repo/STATE.md`, L16-L18, L24-L28；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_DUAL_PRO_REPAIR_TASKBOOK_20260630.md`, L70-L86；`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_RECOVERY_REPAIR_DUAL_PRO_AUDIT_ADOPTION_NOTE_20260630.md`, L81-L95；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`, L231-L239）

## Node36 建议

**Recommended Next Node36 Action**

`PATCH_PROOFS_THEN_RECHECK`

这是我给 node36 的单一步骤建议。原因不是 bibliography 仍有未补的硬伤，而是当前受控核心书目已经完成了 Lamboni 的“DOI / publisher-online-record only”降格，RAG 也能稳定召回这一保守处理；相比之下，真正还没有被 bundle 自己升格完成的是 Proposition 2 与 Proposition 3 的 proof seal。最合理的下一步 therefore 是：**只在 `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 中做窄范围 proof repair**，把 Proposition 2 与 Proposition 3 按上文的最小版本重写，显式加入 `A∩B0={0}` 子引理、`D_w=0 ⇒ P_A|_{B0}=0` 的中间步、以及 Proposition 3 中“若 wrong-order 为零则落入 `A∩B0` 矛盾”的 contradiction step；随后仅用 current controlled file set 重新检查 proof labels、exact witness、和 harness boundary，不做任何 paper-body drafting、claim promotion 或 broader theory expansion。整个动作仍然应在 `KEEP_LOCK_AND_FIX` 的总状态下进行。 （`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_DUAL_PRO_REPAIR_TASKBOOK_20260630.md`, L16-L23, L45-L68；`from_repo/docs/infra/recovery/MATH_PROOF_RESCUE_AUDIT_20260629.md`, L19-L27；`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_RECOVERY_REPAIR_DUAL_PRO_AUDIT_ADOPTION_NOTE_20260630.md`, L52-L57, L125-L135；`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md`, L35-L49；`from_repo/docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_ORDERDEFECT_RECOVERY_REPAIR_V2_20260630.md`, L215-L220）