# MaoField D708 SubPro E 修复复核红队报告

## 结论

PATCH_REQUIRED_OVERCLAIM_OR_PRIOR_ART

前次“缺少必读工件”的阻断已经关闭：本次修复包确实包含了先前缺失的 `docs/infra/recovery/MAOFIELD_D707_SPLIT_LOOP_GOALS_AND_VERIFICATION_20260707.md`，且我核对的 Read First 文件均存在；因此，这一轮不再是“包不完整”问题，而是“陈述边界与先行工作定位”问题。（本地：`PACKAGE_README_D708_SUBPRO_E_REPAIR_RECHECK_20260708.md:5-16,32-33`；`docs/infra/gpt_deep_research/D708_SUBPRO_E_REDTEAM_IDENTITY_CHECK_REPORT42_ADOPTION_NOTE_20260708.md:21-22,23-40`；`docs/infra/recovery/MAOFIELD_D707_SPLIT_LOOP_GOALS_AND_VERIFICATION_20260707.md:1-16`。）

我的核心判断是：仓库中的**定理体与内部有限注记**并未整体漂移成“泛哲学口号”或“经验黑箱机制论”；相反，最强数学内容仍被反复限定为**有限维、声明式 transports / gauges / paths 下的局部 analogue**。但包内仍保留几处会把 programme framing 偷换成“已解决的 identity theory / black-box solution”的高风险段落，尤其是 Report34 与 path-closure brief 的定位语句。如果这些语句不被硬降级，那么先行工作重叠和数学平凡化风险会升到高位。前者与 validity、construct validity、estimands、IRT calibration、benchmark sensitivity、judge/rubric drift、referential security 等成熟问题域有明显邻接；后者则与 canonical correlation、principal angles、two-projection commutator geometry、intertwining / telescoping algebra 的既有数学传统高度接壤。citeturn10view3turn10view1turn12academia0turn13academia1turn6academia3turn6academia2turn7academia0turn8academia0

因此，本次复核不支持任何 public-ready、paper-ready、submission-ready、NMI-ready、real black-box audit、empirical-positive 或“广义 identity theory”升级。当前数学**最多强证明有限 analogue**；凡超出这一点的说法，都应视为过度外推。（本地：`docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_6_QUANTITATIVE_OI_NORM_20260707.md:23-37,102-126,436-450`；`docs/infra/debranded_residual_transport/FORMAL_NOTE_D707_CHART_PATH_CYCLE_DEFECT_V0_20260707.md:5-8,21-32,254-285`；`docs/infra/gpt_deep_research/D708_INTERNAL_V0_GATE_REPAIR_ACCEPT_REPORT40_ADOPTION_NOTE_20260708.md:28-31,44-55,72-91`。）

## 已审阅文件与缺件状态

我实际审阅的本地文件，按功能分组如下。

**Read First 与包控制层**：`STATE.md`；`MD_CATALOG.md`；`PACKAGE_README_D708_SUBPRO_E_REPAIR_RECHECK_20260708.md`；`docs/infra/gpt_deep_research/deep_research_d708_subpro_e_redteam_identity_check_blocked_report42_20260708.md`；`docs/infra/gpt_deep_research/D708_SUBPRO_E_REDTEAM_IDENTITY_CHECK_REPORT42_ADOPTION_NOTE_20260708.md`；`docs/infra/recovery/MAOFIELD_D707_SPLIT_LOOP_GOALS_AND_VERIFICATION_20260707.md`；`docs/infra/debranded_residual_transport/METRIC_OBJECT_IDENTITY_EXACT_NOTES_INDEX_20260706.md`；`docs/infra/gpt_deep_research/D708_INTERNAL_V0_GATE_REPAIR_ACCEPT_REPORT40_ADOPTION_NOTE_20260708.md`。（本地：对应全文核对；存在性复核见包根目录与 `PACKAGE_README`。）

**核心数学 / programme 文件**：`docs/infra/debranded_residual_transport/MATERIAL_RELATION_PATH_CLOSURE_PROGRAMME_BRIEF_20260707.md`；`FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`；`FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md`；`FORMAL_NOTE_V1_6_QUANTITATIVE_OI_NORM_20260707.md`；`FORMAL_NOTE_D707_CHART_PATH_CYCLE_DEFECT_V0_20260707.md`。（本地：分别重点核对定理、边界、positioning 与 forbidden-upgrade 段。）

**D707 loop 与 handoff 文件**：`docs/infra/recovery/d707_split_loop_outputs/loop0/CLAIM_LEDGER_LOOP0_20260707.md`；`FORBIDDEN_CLAIMS_CHECKLIST_LOOP0_20260707.md`；`STATE_LOCK_LOOP0_20260707.md`；`loop3/FORMAL_NOTE_TYPED_CHART_PATH_DEFINITIONS_LOOP3_20260707.md`；`loop3/COMPOSITION_LEMMA_LOOP3_20260707.md`；`loop4/FORMAL_NOTE_FINITE_CYCLE_DEFECT_LOOP4_20260707.md`；`loop4/TELESCOPING_PROOF_LOOP4_20260707.md`；`loop4/CYCLE_NORM_BOUNDS_LOOP4_20260707.md`；`loop4/BOUNDARY_GUARDS_LOOP4_20260707.md`；`session4/CLAIM_DIFF_AFTER_LOOPS_20260707.md`；`OPEN_BLOCKERS_FOR_PRO_20260707.md`；`MAIN_PRO_HANDOFF_PACKET_20260707.md`；`REVIEW_ARTIFACT_INDEX_20260707.md`。（本地：`MAOFIELD_D707_SPLIT_LOOP_GOALS_AND_VERIFICATION_20260707.md:117-239` 给出它们的角色与下游边界。）

**exact-support 文件与脚本**：`EXACT_WITNESS_V1_4_20260629.md`；`EXACT_OI_QUANTITATIVE_V1_6_20260707.md`；`EXACT_GQ_FCR_V1_5_20260706.md`；对应三份 `.json`；以及 `scripts/debranded_residual_transport_exact_witness_v1_4.py`、`..._exact_oi_quantitative_v1_6.py`、`..._exact_gq_fcr_v1_5.py`。（本地：这些文件均明确自称 support / certificate，而非 proof authority，见 `EXACT_WITNESS_V1_4_20260629.md:5-7,64-66`；`EXACT_OI_QUANTITATIVE_V1_6_20260707.md:5-7,24-26,80-82`；`EXACT_GQ_FCR_V1_5_20260706.md:5-8,89-94`；`scripts/debranded_residual_transport_exact_oi_quantitative_v1_6.py:2-6`。）

前次缺件阻断现已关闭。我还额外核对了：Read First 八个文件均存在；Session 4 要求的七个 handoff 文件也都存在，故本次不是“仍缺必要文件”的情形。（本地：`PACKAGE_README_D708_SUBPRO_E_REPAIR_RECHECK_20260708.md:35-49`；`docs/infra/recovery/d707_split_loop_outputs/session4/REVIEW_ARTIFACT_INDEX_20260707.md:63-85`。）

## 本地仓库事实的核心判断

仓库内部最稳固的数学核，仍然是有限 weighted two-way table 上的 order-defect / OI 线，而不是广义 identity theory。v1.3 给出的是有限正权表、主效应空间与投影顺序差的命题；v1.6 则直说自己是“standard finite Hilbert-space two-projection commutator formula”的专门化，而非新 projection theory。D707 chart/path/cycle note 也明确把自己定位成“finite bookkeeping calculus”，甚至承认“may be close to standard commutator, intertwining, and path-defect algebra”，并声明本地价值主要是组织与边界纪律，而非超出局部表述的新颖性。（本地：`FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:41-49,104-227`；`FORMAL_NOTE_V1_6_QUANTITATIVE_OI_NORM_20260707.md:25-37,102-190,222-223`；`FORMAL_NOTE_D707_CHART_PATH_CYCLE_DEFECT_V0_20260707.md:256-262`。）

这意味着：**数学上最强只能说“有限 analogue 被建立了”**。更具体地说，当前稳固内容是：在声明的有限对象中，某些 compatibility / commutation / intertwining / closure 条件何时成立，何时被 exact defect certificate 阻断；以及在显式范数假设下，iterated defect 如何 telescoping 并给出 finite-horizon bound。它不是对经验黑箱内部机制的打开，也不是对“现实 collapse field”的观测，更不是一般 AI evaluation ontology 的完成版。Loop4 文件把这一点写得很清楚：cycle-iteration defect 只是 finite path-defect propagation；`Δ_γ ≠ 0` 只授权有限地计算或界定 defect propagation，不授权 observed collapse 或 black-box mechanism 解释。（本地：`TELESCOPING_PROOF_LOOP4_20260707.md:145-157`；`CYCLE_NORM_BOUNDS_LOOP4_20260707.md:79-141`；`BOUNDARY_GUARDS_LOOP4_20260707.md:7-18,20-47`。）

同时，包内其实已经做好了相当强的“自限”。Loop0 claim ledger 把 “Identity is not naming; identity is path closure under declared material relations” 明确划为 `PROGRAMME_FRAMING`；把 black-box audit 限制为 method schema；把 NMI route 限制为 gate roadmap。Loop 后的 claim diff 再次强调 path-closure sentence 没有升级为 theorem，v1.6 也没有扩展成 broad projection / ANOVA / sheaf / contextuality theory，Loop6 / Loop7 / NMI-ready 并未被解锁。（本地：`CLAIM_LEDGER_LOOP0_20260707.md:11-18`；`STATE_LOCK_LOOP0_20260707.md:66-93`；`CLAIM_DIFF_AFTER_LOOPS_20260707.md:11-20,36-50`；`OPEN_BLOCKERS_FOR_PRO_20260707.md:23-38`。）

真正的风险，不在 theorem-body，而在**仍残留的 package-level rhetoric**。Report34 直接把 programme 翻译成“黑箱评估中的 metric-object identity 解决方案”，又说“它解决的是黑箱评估中的对象同一性许可问题”“它把循环迭代崩溃初步化为有限路径 defect 的传播问题”“它把哲学 chain 落到有限算子路径闭合”。这些句子的问题不在方向，而在强度：它们把“candidate framing / theorem candidate / internal positioning”说成了“已经完成的解决”。这与同包其他文件里的自限发生了内部张力。（本地：`deep_research_material_relation_path_closure_report34_20260707.md:692-697,1151-1180`；对照 `MATERIAL_RELATION_PATH_CLOSURE_PROGRAMME_BRIEF_20260707.md:34-35,47-49,151,187-189,210-215`；`FORBIDDEN_CLAIMS_CHECKLIST_LOOP0_20260707.md:40-58`。）

另一个需要明确指出的点是：JSON、scripts、manifests、RAG、prompts、model reports 在这个包里**没有被正式写成 proof authority**；相反，本地文件反复说它们只是 support artifacts。这是好事，也意味着“proof-by-artifact”目前更多是潜在误用风险，而不是 theorem-body 已经犯下的成文错误。你仍然必须继续阻断这种误用，因为包中几乎每层边界文件都在专门防它。（本地：`FORMAL_NOTE_V1_6_QUANTITATIVE_OI_NORM_20260707.md:421-437`；`EXACT_OI_QUANTITATIVE_V1_6_20260707.md:24-26`；`FORBIDDEN_CLAIMS_CHECKLIST_LOOP0_20260707.md:7-14`；`BOUNDARY_GUARDS_LOOP4_20260707.md:29-34`。）

## 外部先行工作与平凡性风险

**先行工作 / 平凡性风险等级：HIGH。**

先说测量与解释层面。外部成熟文献早已把关键问题表述成“分数解释和使用是否被证据与理论支持”，而不是“同名分数能否自动当作同一对象”。2014 版《Standards》把 validity 定义为：证据与理论支持对 test scores 的解释、且是针对 proposed uses 的解释；并明确指出，被验证的是分数解释而不是 test 本身。ICH E9(R1) 则把 estimand 定义为对 treatment effect 的**精确定义**，并强调 intercurrent events 必须被明示处理，否则 effect 本身就没有被精确说明。把这些放在一起看，MaoField 若把“measurement-object identity / metric-object identity”说得过宽，就很容易只是把 validity / interpretation / estimand-clarification 问题换了一套术语再说一遍。citeturn10view3turn10view1

在 psychometrics / IRT 方向，item response theory 本来就服务于测量、标定、linking、score interpretation 等问题，而 measurement non-invariance / DIF 则是“在控制 latent trait 后，题项跨组表现不同”的成熟问题族。也就是说，只要 MaoField 把自己的贡献扩成“一般比较合法性”“一般测量对象同一性”却不增加真正新对象或新可证结论，它就会与 IRT calibration、measurement invariance、DIF 等既有框架发生强重叠。citeturn6academia3turn6academia0

在 AI evaluation 方向，benchmark sensitivity、prompt sensitivity、judge position bias、rubric drift 也已是独立且活跃的研究轴。已有工作显示：LLM 对轻微 prompt 改写敏感，MCQ 选项顺序会显著改变结果，LLM-as-a-judge 存在明显 position bias，而 rubric 的自然语言改写即便通过 benchmark 复核，也仍可在目标域诱发系统性 preference drift。若 MaoField 把自己说成“一般 benchmark instability critique”或“一般 black-box evaluation solution”，那几乎必然撞上这批先行工作。citeturn4academia1turn5academia1turn7academia0turn7academia1turn8academia0

“referential security” 这一项更值得警惕，因为它正好在动态系统的“评估到底绑在哪个对象上”问题上形成直接邻接。该方向虽然很新，但已经明确把问题表述为：静态名称不等于可验证地指向同一系统，安全审计与长期追踪必须绑到可鉴别的 artifact identity 上。它与 MaoField 的“metric-object identity”并不等同，但足够接近，足以要求你在 novelty wording 上极度克制。citeturn6academia2

再说数学平凡化。v1.6 自己已经明言是标准 two-projection commutator formula 的专门化；外部综述表明 canonical correlations / principal angles 的谱系至少可追到 Jordan 1875 与 Hotelling 1936，而 Halmos 型 two-projections theorem 又是后续 operator-theoretic 基础。换句话说，如果 MaoField 想把这条线包装成“新 projection theory”“新 principal-angle theory”“新 commutator theory”，风险不是中等，而是高。当前还能勉强保住的，只能是：把若干已知有限对象，按其特定审核语义重新组织，并用严格边界避免偷换。citeturn12academia0turn13academia1

最后，必须把“cycle defect / telescoping”与外部 model collapse 文献切开。外部 model collapse 指向的是**递归训练于生成数据**所导致的分布尾部遗失、性能退化与缩塌；而本包的 `Δ_{γ,n}` / `CIC_N` 只是声明式 transports 下的 finite-horizon path-defect propagation。二者不能直接等同。把后者宣传成前者的“理论化”或“已解决机制”，会构成对象偷换。citeturn15academia0turn15academia1

## 最高风险段落与必须降级的说法

风险最高的本地段落，不在 exact note 的定理体，而在以下几处定位性文字。

第一处是 Report34 的“解决方案”句式：`deep_research_material_relation_path_closure_report34_20260707.md:692-697` 把 MaoField 写成“给出黑箱评估中的 metric-object identity 解决方案”。这必须降级为：**“在声明 charts / transports / gauges / paths 的前提下，支持一个候选性的有限 metric-object identity audit schema；它不解决一般黑箱机制，也不构成完成的 identity theory。”** 原因是同包其他文件明明还把这条线维持在 `PROGRAMME_LEVEL_SYNTHESIS_AND_NEXT_PROOF_TASK_SOURCE` 与 “candidate finite metric-object identity audit calculus” 的级别。（本地：`MATERIAL_RELATION_PATH_CLOSURE_PROGRAMME_BRIEF_20260707.md:47-49,151,191-215`；`MAOFIELD_D707_SPLIT_LOOP_GOALS_AND_VERIFICATION_20260707.md:48-53`；`FORBIDDEN_CLAIMS_CHECKLIST_LOOP0_20260707.md:40-49`。）

第二处是 Report34 的四句“可以强说”：`deep_research_material_relation_path_closure_report34_20260707.md:1161-1180`。这里至少有三句必须全面硬降级：  
一是“它解决的是黑箱评估中的对象同一性许可问题”；  
二是“它把循环迭代崩溃初步化为有限路径 defect 的传播问题”；  
三是“它把哲学 chain 的‘同一性不是抽象给定’落到有限算子路径闭合”。  
更安全的替换是：**“这些只是 programme-level translation、theorem candidate、或 internal positioning；不是已完成的广义 identity theory，不是 black-box mechanism 结论，也不是 empirical model collapse theory。”**（本地：`CLAIM_DIFF_AFTER_LOOPS_20260707.md:11-20,44-50`；`BOUNDARY_GUARDS_LOOP4_20260707.md:20-35`。）

第三处是 brief 中所谓 “Safe claim”：`MATERIAL_RELATION_PATH_CLOSURE_PROGRAMME_BRIEF_20260707.md:210-215`。这句写成 “MaoField provides a finite metric-object identity audit programme for black-box evaluation outputs” 仍偏强，因为“provides”会悄悄滑向“validated programme”。它应降级为：**“supports at most a candidate finite metric-object identity audit programme”**。这是与 Loop0/Loop4 的 candidate-only wording 对齐，而不是与 Report34 的强说对齐。（本地：`STATE_LOCK_LOOP0_20260707.md:79-93`；`BOUNDARY_GUARDS_LOOP4_20260707.md:29-34`。）

第四处是 notes index 里的 programme translation：`METRIC_OBJECT_IDENTITY_EXACT_NOTES_INDEX_20260706.md:15-35,59-72`。这里本身已经带 boundary，但“non-identity / unity -> measurement-object identity problem -> metric-object identity -> ...”一旦脱离 boundary 转述，很容易被外部读者当作“理论链已经打通”。这部分必须继续只作为**index / translation / positioning**保存，不能在任何对外文本中移作 theorem headline 或 novelty headline。（本地：`METRIC_OBJECT_IDENTITY_EXACT_NOTES_INDEX_20260706.md:5-13,47-72`。）

## 必须继续禁止的说法与局限

必须继续禁止的说法，有且不限于以下这些。它们在本地边界文件中已被反复阻断，我的复核结论保持这些阻断不动：  
MaoField empirical-positive；observed residual / interaction / transport / holonomy / gluing / collapse field；dynamic-collapse theory；black-box mechanism solved；public-ready / paper-ready / submission-ready / NMI-ready；Loop6/Loop7/real black-box audit 已经解锁；broad ANOVA / dependent-input / projection / sheaf / contextuality / path-closure theory；proof by JSON / RAG / harness / package / prompt / manifest / model output。（本地：`PACKAGE_README_D708_SUBPRO_E_REPAIR_RECHECK_20260708.md:66-91`；`D708_INTERNAL_V0_GATE_REPAIR_ACCEPT_REPORT40_ADOPTION_NOTE_20260708.md:72-91`；`CLAIM_DIFF_AFTER_LOOPS_20260707.md:22-34`；`OPEN_BLOCKERS_FOR_PRO_20260707.md:23-38`。）

需要保留的唯一安全总句，仍应是你给出的那句：**“Metric-object identity is unlicensed unless declared transports and path closure/coherence conditions hold.”** 但连这句话也只应被当作 organising contradiction / programme framing，而不是 completed theorem headline。对外若要再缩一句，我建议缩到：**“当前数学只支持声明式有限对象中的 conditional identity audit analogue。”** 这既不否定已有有限定理，也不把它们抬成广义 identity theory。（本地：`MAOFIELD_D707_SPLIT_LOOP_GOALS_AND_VERIFICATION_20260707.md:48-53`；`CLAIM_LEDGER_LOOP0_20260707.md:12-17`。）

当前数学能**强证明的只有有限 analogue**。它没有强证明广义 identity theory；一旦以 broader identity theory、black-box solution、dynamic-collapse theory 自居，就是被自身 package 里的边界文件、也是被外部成熟文献同时反驳。citeturn10view3turn10view1turn12academia0turn15academia0

## 局限

这份报告基于修复包内文件与外部公开学术来源完成；我没有把本地仓库事实外推到 zip 之外，也没有使用公开 GitHub 来断言仓库状态。外部先行工作部分足以支持“重叠 / 平凡化高风险”的判断，但它不是穷尽式书目综述；其中 “referential security” 是一条较新的相邻路线，我据此只主张“需要更保守的 novelty wording”，不主张两者已经一一同构。citeturn6academia2