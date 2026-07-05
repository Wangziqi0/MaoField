# MaoField 对象图谱与有限粘贴回合严格评审

## 证据范围与方法

本评审严格把 ZIP 包内部材料当作唯一权威层，遵守三条边界。第一，`PACKAGE_README.md` 明确要求：本轮任务是做“对象图谱、claim-chain map、有限 gluing/pasting 候选”，并且 RAG 结果只是 locator，不是证明；禁止把材料升级成经验正结果、广义 ANOVA 理论、观测到的 residual/transport/holonomy field、或 harness/JSON 即证明。第二，`from_repo/STATE.md` 把项目当前状态钉死在一个更窄的数学程序上：公开可复现实面与 Zenodo 记录存在，但数学核仍然只是“有限正权二向表 + order-defect 定理 + 2×2 精确见证”；Mode B 仍为 `insufficient_artifact`，duplicate risk 仍为 `MEDIUM`。第三，`PACKAGE_FILE_LIST.txt` 给出了本包实际随附文件清单，因此凡 RAG 命中却未出现在该清单中的主文件，我都不当作已随包提供的主证据。

就数学核心而言，当前包内最硬的脊柱没有歧义：`FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 给出有限正权二向表、加权内积、`C/A/B0/N_add` 子空间、顺序剥离算子 `R_{Q→B},R_{B→Q}` 与顺序缺陷 `D_w`；并证明了 product 权重与 `A ⟂ B0`、`D_w=0`、顺序独立之间的等价，以及非 product 权重下纯主效应 witness 会被错误顺序制造出假残差。`EXACT_WITNESS_V1_4_20260629.md` 与其 JSON 把该最小 `2×2` 见证升到 exact rational 证书层；`debranded_residual_transport_exact_witness_v1_4.py` 说明该证书确实由 `fractions.Fraction` 构造，而 `debranded_residual_transport_harness_v1_3.py` 则把 floating-point harness 明确限定为“deterministic regression support only”。

在“更大对象链”的层面，我采用如下审计标准：凡当前包内已有 formal note、programme note、adoption note、脚本、JSON 的对象，可进入 `PROVEN_IN_PACKAGE` 或 `FORMALIZABLE_NOW`；凡包内只有 programme/深研报告支持、但尚无主证明或 exact artifact 的对象，进入 `PACKAGE_SUPPORTED_DIRECTION`；凡 RAG 指到更旧链条，但所依赖的一手主文件并未随 ZIP 附带，进入 `NEEDS_NODE36_FILES`；凡与当前边界直接冲突的对象或话语，进入 `BAD_OR_FORBIDDEN_OBJECT`。这一区分并非修辞，而是包本身治理结构要求的研究纪律。`MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md` 允许把 MaoField Phase II 重写为“measurement-object identity problem”，并建议 chart、transport、defect、`OI`、certificate library 与 audit protocol；`METRIC_IDENTITY_PHASEII_REPORT25_ADOPTION_NOTE_20260705.md` 则把默认旧建议锁成 `FORMALIZE_DEFINITIONS_FIRST`，但同时承认可继续推进定义层、library、judge/contamination/ranking toys 等 bounded 对象。`MAOFIELD_D705_OBJECT_ATLAS_AND_GLUE_PACKAGE_TASKBOOK_20260705.md` 明确说明本包正是为了让下一轮 Pro 对“对象图谱 + gluing/pasting”做受控扩展。】

还有一个重要的审计结论：RAG 对象链是有用的，但并不完整落地在 ZIP 里。`rag_results/00_summary_paths.txt` 与各主题 RAG 文件命中了若干未随包提供的主文件，如 `OPEN_MAOFIELD_FORMAL_ZENODO_PREPRINT_FORM_VALUES_20260704.md`、`ORDER_DEFECT_D630_TASKBOOK_NEXT_PRO_20260630.md`、`HANDOFF_TO_GPT55PRO_20260629.md`、`deep_research_formal_residual_transport_v1_2_implementation_audit_20260627.md`、若干更旧 harness/report 文件等；而 `PACKAGE_FILE_LIST.txt` 中并无这些路径。因此，凡某一对象若其关键“一手筋骨”恰落在这些缺失文件上，我都会把它降级到 `NEEDS_NODE36_FILES`，而不是借 RAG 摘要越权下结论。】

## 对象图谱

总判断先说在前面：当前包真正“已站稳”的对象只有一条紧主链——有限正权二向表、可加 nuisance 子空间、真加性残差、顺序剥离输出、顺序缺陷算子、以及 `2×2` 精确证书。围绕它可以立即再长出的，是定义层对象与一小批 exact certificates；而更远的 quotient residual、finite ANOVA、hypercube、transport、holonomy、gluing 分支虽然在包里留下了清晰“矿脉”，但只有一部分已经足够 formalize，另一部分仍缺 node36 上的旧主文件。这样的分层，与 programme note 对“真正空位”的表述是一致的：空位不在广义 dependent-input ANOVA，也不在抽象两投影理论本身，而在“finite weighted residual metric audit + exact obstruction certificate + metric-object identity discipline”这一窄而硬的组合。】

| 对象名 | 来源文件 / RAG 命中 | 当前状态 | 当前可写的有限定义 | 与 `2×2` order-defect 定理的关系 | 现有证明或证书 | 缺失证明义务 | 查重 / 先占风险 | 保留 / 修订 / 淘汰 |
|---|---|---|---|---|---|---|---|---|
| 有限正权二向表 `X=Q×B,w>0` | `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`:41-62 | `PROVEN_IN_PACKAGE` | 有限集合、正权重、加权内积 | 是全部主定理的环境空间 | formal note 已完整给出 | 无 | 低 | 保留 |
| 加性 nuisance 子空间 `C,A,B0,N_add` | `FORMAL_NOTE...`:64-100 | `PROVEN_IN_PACKAGE` | `C=span{1}`, `A` 为 q-only 零均值，`B0` 为 b-only 零均值，`N_add=C⊕A⊕B0` | 是“真加性残差”与假残差区分的基底 | formal note 已给出 | 无 | 中 | 保留 |
| 投影族 `P_C,P_A,P_B0,P_N` | `FORMAL_NOTE...`:77-100；`exact_witness_v1_4_20260629.json`:78-208 | `PROVEN_IN_PACKAGE` | 加权正交投影 | 生成真残差与顺序缺陷 | exact JSON 给出当前 `2×2` 坐标；exact 脚本给出一般构造套路 | 无 | 中 | 保留 |
| 真加性残差 `I-P_N` | `FORMAL_NOTE...`:177-204,243-283 | `PROVEN_IN_PACKAGE` | `K` 到 `N_add^\perp` 的正交余量 | 用来判断“wrong-order residual”是否真 residual | formal note 命题链已给出 | 无 | 中 | 保留 |
| 顺序剥离输出 `R_{Q→B},R_{B→Q}` | `FORMAL_NOTE...`:156-175；`exact_witness...md`:44-60 | `PROVEN_IN_PACKAGE` | 两种固定顺序的 stripping 算子 | `2×2` 证书正是比较这两个输出 | formal note + exact witness | 无 | 中 | 保留 |
| 顺序缺陷算子 `D_w` | `FORMAL_NOTE...`:156-184；`exact_witness.json`:79-104 | `PROVEN_IN_PACKAGE` | `D_w=R_{Q→B}-R_{B→Q}=P_{B0}P_A-P_AP_{B0}` | 主定理核心对象 | 命题 2 与 exact JSON 都支持 | 无 | 中高，邻接两投影理论 | 保留，但严禁写成 broad projection theory |
| 真残差与 sequential stripping 输出之差 | `FORMAL_NOTE...`:243-283,315-335 | `PROVEN_IN_PACKAGE` | 对 `K∈A` 或 `K∈B0` 比较 `(I-P_N)K` 与两种 ordered outputs | 是“procedure artifact”命题本体 | 命题 3 + `2×2` exact witness | 无 | 中 | 保留 |
| `2×2` 精确见证 tuple | `EXACT_WITNESS_V1_4_20260629.md`:44-66；JSON:51-104；脚本:126-219 | `PROVEN_IN_PACKAGE` | `w=(1/11)[[1,2],[3,5]]`，`K=(7/11,-4/11,7/11,-4/11)` | 当前全部论证的证书锚点 | exact rational script/JSON/Markdown 三位一体 | 无 | 低 | 保留，作为锚点 |
| 受限算子型不稳定指数 `OI^{op}_{N_add}(w)` | `MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md`:742-760；`Report25`:124-147；`Report25 Adoption`:85-105 | `FORMALIZABLE_NOW` | `||D_w|_{N_add}||_{op,w}` | 把“存在性见证”升级为可比较指数对象 | 还无单独 note，但 formal note 命题 2–3 已足够推出零当且仅当 product | 需写成单独定理与记号规范 | 中 | 保留并立即形式化 |
| 点态证书型不稳定指数 `OI^{pt}_w(K)` | `Report25`:136-147 | `FORMALIZABLE_NOW` | `||D_wK||_w / ||K||_w` | 是 witness 级别 defect 的规范化版本 | 当前 `2×2` 见证已给非零实例 | 需补充 domain、零向量排除、报告格式 | 低中 | 保留 |
| Evaluation chart `c=(P,T,J,R,D,w,A_g,N)` | `programme`:665-704；`programme adoption`:62-82；`Report25 Adoption`:57-82 | `FORMALIZABLE_NOW` | 有限 chart 元组；但需剥离 roster | 把 order-defect 从“单表程序”抬升到一般 chart 语言 | 有 programme 支持，无正式定理 | 需补 `I_c`、manifest、coherence 元数据 | 中 | 保留并修订 |
| Roster `S={σ_1,…,σ_M}` | `Report25 Adoption`:57-68；`Report25`:39-70 | `FORMALIZABLE_NOW` | 与 chart 分离的被评估系统有限集 | 为 ranking object 清理语法 | programme/report25 已支持 | 需固定 tie/版本规则 | 低 | 保留 |
| Chart-dependent metric object `M_c(σ)` | `programme`:686-718；`Report25`:54-73 | `FORMALIZABLE_NOW` | `M_c(σ)=(c,Φ_c(K_c(σ)))`，`Φ_c` 可取 score/residual/rank-pre-summary | 是把 `2×2` 定理推广成一般“object not free”语言的桥 | 仅 programme 与 report25 定义性支持 | 需区分标量对象与 roster-dependent 排名对象 | 中 | 保留并修订 |
| Identity transport / intertwining 条件 | `programme`:692-718；`Report25`:74-105；`Report25 Adoption`:71-83 | `FORMALIZABLE_NOW` | `T_{c→c'}∘Φ_c=Φ_{c'}∘U_{c→c'}` | `2×2` 情形是最小特例：同一 carrier 上恒等 transport 的失败 | 报告层已说明，formal note 提供特例直觉 | 需补“可逆性 + coherence + admissible class” | 中高 | 保留 |
| Defect certificate tuple `C=(c,c',K,Δ)` | `Report25`:107-123；`Report25 Adoption`:78-84 | `FORMALIZABLE_NOW` | `Δ=T_{c→c'}M_c(K)-M_{c'}(U_{c→c'}K)` | 当前 `2×2` 证书就是其 order-only 特例 | 最小特例已在 exact witness 中阴影出现 | 需补 transport declaration、norm、metadata | 低中 | 保留 |
| Certificate library | `programme`:782-810；`Report25`:186-201；`Report25 Adoption`:93-105 | `PACKAGE_SUPPORTED_DIRECTION` | 一组 exact artifacts，而非散例堆积 | 把 `2×2` 证书扩展成有层级的库 | 目前只有锚点和 float harness block | 缺 exact `2×3/3×3` 工件 | 中 | 保留 |
| Product control | `programme`:787-795；`harness_v1_3.py`:233-253 | `FORMALIZABLE_NOW` | exact `2×3` product 权重对照 | 是 order-defect 零缺陷对照面 | float harness 已有 `2×3` theorem control | 缺 exact rational markdown/json | 低 | 保留并尽快做 exact 版 |
| Near-product perturbation family | `programme`:789-790；`Report25`:176,194-201,267-272 | `PACKAGE_SUPPORTED_DIRECTION` | 正权 simplex 内靠近 product 流形的有理族 | 给 `D_w` 从零生长的局部机理 | 目前只有概念与 library 规划 | 缺 `P_A,P_B0,P_N,D_w` 对 `w` 的依赖证明 | 中高 | 保留，但先不夸大 |
| Judge-order toy | `programme`:793；`Report25`:177,195 | `FORMALIZABLE_NOW` | 对现有二向表做 prompt×judge 语义重命名 | 直接是 order-defect 的语义翻译 | 现有 theorem 已足够 | 只需明确“语义重命名不是经验发现” | 高，judge-bias 邻域拥挤 | 保留，严格限于 finite toy |
| Contamination-coupling toy | `programme`:792；`report21`:143-153；`Report25`:196 | `PACKAGE_SUPPORTED_DIRECTION` | 例如 `fresh/exposed × verbatim/paraphrase/mixed` 的有限 chart | 属于“chart 轴改变对象身份”的演示 | 仅 programme/report21/report25 提到 | 缺 exact table、claim boundary、negative control | 高 | 保留，但只做 toy |
| Ranking-instability toy | `programme`:794；`Report25`:174,197,241-249 | `PACKAGE_SUPPORTED_DIRECTION` | 有限 roster 上的双 chart score vectors 与 gap 证书 | 把“非同一对象”推到 ranking 层 | 目前只有方向、无 artifact | 缺 exact score vectors/tie policy/transport 文档 | 高 | 保留，但后置 |
| Quotient residual object `R_t=Π_{N^\perp,w}K_t` | `deep_research_quotient_residual_mainline_debranded_program_20260624.md`，§形式化定义/Mode A；`deep_research_quotient_residual_finite_anova_kill_framework_20260623.md`:23-57 | `PACKAGE_SUPPORTED_DIRECTION` | 有限乘积空间上的商类最小范数代表元 | 是把当前二向表主链向更一般 carrier 推广的自然母对象 | 包内有清晰定义，但无与当前主线同等级主 note | 需单独主文件/采用 note 把其地位压实 | 中高，靠近 dependent-input 分解 | 保留，但只作方向 |
| 有限 ANOVA / interaction field `I_t=Π_{A^\perp,w}K_t` | `deep_research_quotient_residual_mainline...`，§Mode A；`deep_research_future_math_objects_interaction_field_audit_20260623.md`:45-60 | `PACKAGE_SUPPORTED_DIRECTION` | strict additive nuisance 的正交余量 | 是 order-defect 的“高维亲族”，不是其现有结论 | deep-research 层支持 | 缺随包主工件与现成 full proof | 高 | 保留，但严禁说 broad ANOVA theory |
| Hypercube residual tensor `Q_freq4×B_tokenpos4` | `deep_research_future_math_objects_interaction_field_audit_20260623.md`:45-60,139-147；`deep_research_quotient_residual_finite_anova...`:20-22 | `NEEDS_NODE36_FILES` | 可写成 16-cell tensor，但依赖缺失的 hypercube schema / prereg / audit 主文件 | 只是从 order-defect 向 `4×4` 载体的延伸构想 | 当前 ZIP 只保留二手报告 | 缺 schema、prereg、audit、script 等一手文件 | 高 | 修订后等待 node36 文件 |
| Generation path in quotient/tensor space | `deep_research_transport_holonomy_math_turn_audit_20260624.md`，§传输稳定秩对象；`deep_research_residual_transport_holonomy_split_project_20260624.md`，§最干净的有限维对象 | `NEEDS_NODE36_FILES` | 把多时点 residual 堆叠成路径或矩阵 | 试图把 `K` 的单张表拓展到演化序列 | 当前包无 full-panel primarys；Mode B 仍 `insufficient_artifact` | 缺 panel artifacts 与 null blocks | 高 | 暂停 |
| Projection-evolution commutator `[P,T]` | `deep_research_quotient_residual_mainline...`:103-122,182-194；`deep_research_quotient_residual_finite_anova...`:226-264 | `FORMALIZABLE_NOW` | 在 `H_w=N⊕N^\perp` 上的块泄漏算子 | 是 `D_w` 由静态顺序缺陷走向动态泄漏对象的抽象延展 | 包内二手定义已很清楚 | 缺一个不依赖 Mode B 的 standalone finite note | 中高，邻接算子理论 | 保留，但先去品牌化 |
| Scale-edge defect `Δ_ρ` / square holonomy defect `H_□` | `deep_research_quotient_residual_finite_anova...`:186-224,226-297；`deep_research_transport_holonomy_math_turn_audit_20260624.md`，§尺度边缺陷/§方格 holonomy 缺陷 | `FORMALIZABLE_NOW` | `Δ_ρ(K)=||C_ρP_fK-P_cC_ρK||`；`H_□` 为两路径差 | 是“有限 gluing/pasting”最直接的方格对象；与 `2×2` order-defect 同属“先后次序不自由”主题 | 包内已有相当明确的公式化 | 缺 exact synthetic certificate 与 paired control | 中高 | 强烈保留 |
| 局部 gluing obstruction `Obs(K)` | `deep_research_quotient_residual_mainline...`:125-142；`deep_research_quotient_residual_finite_anova...`:266-297 | `FORMALIZABLE_NOW` | 局部 sections 在允许局部 nuisance gauge 后仍不可吸收的 overlap mismatch | 把 `2×2` 的“程序顺序不交换”提升到“局部对象是否能粘成全局对象” | 公式已在包内，尚无 exact artifact | 需最小有限 cover、restriction maps、exact witness | 中高 | 强烈保留，适合作为下一对象 |
| Metric-form fetishism 作为 illicit quotienting | `programme`:177-212,764-780；`Report25`:149-165；`programme adoption`:41-60 | `FORMALIZABLE_NOW` | 未经 transport/invariance 证明就把 charted objects 压成 chart-free model property | 是当前 `2×2` 定理的上层解释纪律 | programme/report25 已给精确定义草稿 | 需把它写成 reporting rule，而不是 empirical thesis | 高，概念邻域广 | 保留，但只作纪律性定义 |
| “observed residual / interaction / transport / holonomy field” | `PACKAGE_README.md`:19-21；`STATE.md`:27-28；`OPEN_MAOFIELD_FORMAL_ZENODO_PREPRINT_PUBLISHED_20260704.md`，§Boundaries；`FINAL_DUPLICATE_RISK...`:27-29,56-74 | `BAD_OR_FORBIDDEN_OBJECT` | 不允许定义成当前包已证对象 | 与 `2×2` theorem 无合法推演桥梁 | 无 | 与边界直接冲突 | 极高 | 淘汰 |

这个表最关键的含义是：**当前包里已经够硬的“次新对象”，其实不是 hypercube，不是经验 transport，不是所谓 field，而是四类小而可落地的东西：`OI^{op}_{N_add}`、chart/transport/defect 定义层、product/near-product 小证书、以及 finite gluing obstruction。** 其中前三类大体延续 Report25 的建议；第四类则是本轮 object-atlas 之后真正浮出水面的“严格新对象”候选。它既来源于 RAG 链中的 gluing/sheaf/holonomy 分支，也能被压回纯有限线性代数而不越界。】

## 论证链地图

旧 MaoField 的经验线在这个包里并没有被“修成正结果”；相反，它被明确降格成一个负中心、审计导向的前史。`STATE.md` 直接说：原 empirical pilot 仍是 negative-centered / measurement-audit case，而当前主线已经转入“同一仓库内的 debranded finite weighted order-defect local-draft rescue”；同时，“旧路线不能复活”的硬边界、Mode B 的 `insufficient_artifact`、以及不许宣称 full panel / training / inference / new loss / F3-positive / LOSO-passed / observed field 等，都被反复钉死。也就是说，经验材料今天的制度角色，只剩下“为何必须做 measurement audit discipline”的动因，而不是任何已成立的经验发现。】

被保留下来的“矿石”并不是旧结论，而是旧项目逼出来的一个更深问题：score、residual、ranking 这类产物究竟何时有资格被当成同一个对象。`MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md` 把这一步明确改写成“measurement-object identity problem”，并进一步用“metric-form fetishism”命名那种未经 transport/invariance 证明、就把异质测量关系压成模型内在属性的做法；`deep_research_metric_field_programme_reframe_report21_20260703.md` 则把 order-defect theorem 重新定位成一个楔子：它不是大理论本身，而是说明“指标不是透明窗口，指标是带权、带顺序、带 judge、带 aggregation 的测量装置”的最小有限模型。也因此，当前真正保留下来的 conceptual ore，不是“经验复杂性本身”，而是“对象同一性不是免费的”。】

已经被包内严格证明的有限命题，只有三层。第一层是结构等价：在有限正权二向表上，product 权重、`A ⟂ B0`、`D_w=0`、和两种 ordered residual maps 相等是等价的。第二层是 no-go：在非 product 权重下，存在纯主效应 witness，其真加性残差为零，但错误顺序输出非零，所以该非零量只能被解释为 procedure artifact。第三层是 exact certificate：当前主见证 `w=(1/11)[[1,2],[3,5]]`、`K=(7/11,-4/11,7/11,-4/11)` 的 artifact 向量与加权范数平方已由 exact rational script 和 JSON 固化。任何超出这三层的说法，若没有新的定义与证书，都会立刻越界。】

包内确实支持若干未来方向，但它们被严格分了层。定义层对象——chart、roster、`K_c(σ)`、`M_c(σ)`、identity transport、defect certificate、`OI`——已经足以 formalize；更远一点的 certificate library 方向也被 programme note 与 Report25 adoption note 正式接纳。再远一点，quotient residual、finite ANOVA、projection-evolution commutator、edge defect、square holonomy defect、local gluing obstruction，这些在旧 deep-research 链中已经有相当清楚的公式形状，因此可以作为 package-supported 或 formalizable 的纯数学对象继续推进。相反，hypercube residual tensor、generation-path objects、以及任何带 real panel 语气的 transport/holonomy 讨论，由于主载体文件并未随包附带，且 Mode B 状态未升级，必须停在 `NEEDS_NODE36_FILES` 或更低。】

## 有限粘贴对象评估

我的裁决是：**可以，而且现在就可以，构造一个新的严格有限对象；但它必须是“有限 gluing obstruction certificate”，不是广义 sheaf theory，不是广义 holonomy theory，更不是任何已观测 LLM field。** 这一结论并非凭空想象。包内旧链条已经给出了三块足够坚实的砖：第一，chart/transport/defect 的新语言已经在 programme note 与 Report25 中成熟到可 formalize 的程度；第二，`deep_research_quotient_residual_mainline_debranded_program_20260624.md` 与 `deep_research_quotient_residual_finite_anova_kill_framework_20260623.md` 已经把局部 section、restriction、overlap mismatch、以及 gauge-minimized obstruction 的公式写了出来；第三，现有 exact witness script/harness 说明 zero-GPU、exact-rational、file-backed 证书风格已经成熟。因此，真正的下一对象不是再写一篇“更大愿景”，而是把这些公式压成一个最小 exact artifact。】

我建议把“有限粘贴”分成三个层次，其中只有第一个应当立刻做成新对象，后两个作为紧随其后的扩展。第一个层次是**两图重叠粘贴证书**；第二个层次是**三图循环缺陷证书**；第三个层次是**有限尺度方格路径缺陷证书**。它们都完全可以做成零 GPU、exact rational、机器可重算的对象，但严格程度、对旧链条的依赖程度、以及最小示例大小并不相同。下面是具体判断。

| 粘贴提案 | 最小有限例大小 | 需要的精确有理数据 | 将被证明的内容 | 仍只是类比的部分 | 为什么不只是 generic projection/ANOVA | 是否可零 GPU 实现 |
|---|---|---|---|---|---|---|
| 两图重叠粘贴证书 `Obs_{12}(K)` | 我建议从 4 个全局 cells、两个 3-cell 局部 chart、2-cell overlap 起步 | 一个全局有理向量 `K`；两个局部正权重；两个局部 nuisance bases；restriction maps；允许的局部 gauge 类 | 在允许的局部 nuisance 下，两个局部 residual sections 不能在 overlap 上一致，从而**不能 paste 成同一全局对象** | 不应把它叫 sheaf 定理；这里只是一个 finite overlap obstruction certificate | generic projection 只看单个投影；这里比较的是“局部投影 + restriction + gauge minimization + overlap compatibility”的复合对象 | 可以，直接仿照 exact witness 的 `Fraction` 风格实现 |
| 三图循环缺陷证书 | 最小可从 5–6 个 cells 与三个 pairwise-overlap charts 起步；我建议不要比这更小 | 三个局部 charts、三对 overlap 权重、三组局部 nuisances、一个全局 `K`、以及循环比较规则 | 证明 pairwise 看似可比较，不代表 whole cycle 一致；可出现“局部两两还行，但整体循环闭不上” | 只能称为 cocycle-like finite failure，不能上升为 cohomology 结果 | generic ANOVA 不编码多 chart 循环兼容性；generic projection 也不编码三重局部拼接 | 可以，但比两图证书更易定义漂移；应后做 |
| 方格路径缺陷证书 `H_□(K)` | 一个 `4×4` 细尺度表，加两条中间 coarse 路径到 `2×2` 终点，是最干净起点 | 细尺度权重与 `K`；两条 block-average coarse maps；终点和中间尺度 nuisance families；显式路径差 | 证明“先按 q 粗化再按 b 粗化”与“先按 b 再按 q”给出的终点 residual 并非同一对象 | 最多只能叫 square-holonomy-like defect，绝不能声称广义 holonomy theory | 这里研究的不是单尺度分解，而是**路径依赖的对象同一性**；与普通 ANOVA 的 order terms 不同 | 可以，且非常适合 paired positive/negative controls |

在这三个提案里，我认为**最值得立即创建的对象是第一个：两图重叠粘贴证书**。理由很简单。它比 square-holonomy 更小，比三图循环更不依赖复杂 cover，也最直接把 “chart-dependent object + defect certificate + allowed local gauge” 三个新定义压到一张有限表上。它本质上是一条更高阶但仍然完全有限的 no-go：**即便局部对象都是合法 residual-like objects，也不代表它们自动能被粘成同一个全局对象。** 这正好是 order-defect 主线的自然上推：原来的 no-go 是“同一 carrier 上，两个过程顺序不能随便互换”；新的 no-go 是“不同局部 chart 上，局部 residual sections 不能自动拼成同一对象”。两者的精神完全一致，且都属于“同一性不是免费的”。】

这里最重要的“降温句”必须保留：即便做出了 `Obs(K)>0` 的 exact certificate，也**只**能证明一个有限局部—整体兼容性失败；它不能证明广义 sheaf obstruction theory，也不能证明现实 LLM evaluation 中已经观测到了 transport/holonomy/gluing field。包内旧报告自己就反复强调：sheaf、holonomy、gluing 这些语言只有在 local sections、restriction maps、overlap mismatch、以及 gauge-minimized obstruction 都写清之后才有资格出现，而且只要轻微扩大允许的局部 nuisance 就能吸收掉 mismatch，就必须判成 gauge artifact，而不是“更深结构”。这条 fail-closed 纪律若不保留，有限粘贴对象本身就会滑回旧路线的夸张叙事。】

## 定义层与定理候选审计

### 下一定义层审计

我不建议把 Report25 的定义草稿推倒重来；总体上它们是对的，但多数需要“把句子削得更硬”。尤其要注意，下一轮若真要做 finite gluing object，定义必须支持 chart、local section、restriction、transport、certificate 这几层同时出现，而不能只够写一页 programme prose。】

| 定义 | 选择 | 严格理由 |
|---|---|---|
| `c = (P,T,J,R,D,w,A_g,N)` | `ACCEPT_WITH_REVISION` | 这个骨架是对的，而且 programme/adoption 已支持把 chart 写成评估装置元组；但若进入 finite gluing，对每个 chart 还应补充一个冻结的有限 carrier 或 cell index manifest `I_c`，至少在附属数据中明确。否则 `K_c(σ)∈R^{I_c}` 没有真正落地。`N` 这一位也应明确是 nuisance-stripping scheme，而不是抽象标签。】 |
| `S = {sigma_1, ..., sigma_M}` | `ACCEPT_AS_IS` | Report25 把 roster 与 chart 分离是正确动作，因为单系统对象和 roster-dependent 排名对象必须分开。下一轮只需补 tie policy / version freeze，不必改符号。】 |
| `K_c(sigma) in R^{I_c}` | `ACCEPT_WITH_REVISION` | 形式是对的，但要加一句：`K_c(σ)` 必须来自 frozen chart manifest 的有限提取规则，而不是“原始评估日志的模糊摘要”。对 gluing/object identity 而言，这一步是 carrier 落地的关键。】 |
| `M_c(sigma) = (c, Phi_c(K_c(sigma)))` | `ACCEPT_WITH_REVISION` | 这是正确的上层对象定义，但应把 codomain 写明为某个 chart-specific 对象空间 `O_c`；并且排名对象最好另列成 roster-dependent 版本，而不是和单模型 score/residual object 混写。】 |
| `T_{c->c'} o Phi_c = Phi_{c'} o U_{c->c'}` | `ACCEPT_WITH_REVISION` | 作为 identity license 的核心条件，它是对的；但若只写这一句，仍无法区分“identity”与“mere comparability”。我建议补三条：`T_{c→c}` 为恒等；在相关像空间上可逆；对三图复合满足 coherence。没有这些，就不应把它叫 identity transport。】 |
| `C = (c, c', K, Delta)` | `ACCEPT_WITH_REVISION` | tuple 本身可以保留，但 `Δ` 的定义依赖 transport 与范数，故元数据至少还要含：`U_{c→c'}`、`T_{c→c'}`、norm/order rule、以及 forbidden interpretation。没有这些，证书只能算半成品。】 |
| `OI_N^op(w) = || D_w restricted to N_add ||_{op,w}` | `ACCEPT_WITH_REVISION` | 实质对，但记号应统一成 `OI^{op}_{N_add}(w)`，因为当前 restriction 实际写的是 `N_add`。此外必须明确：当前只在“有限正权二向表”设定内使用，不能偷偷把它推广成广义 metric instability theory。】 |

这组审计的核心结论是：**定义层已经成熟到可以被冻结，但最好不是再做一轮抽象定义清单，而是直接拿来压一个新的有限对象。** 也就是说，定义层今天最缺的不是第三次措辞修补，而是一个会“反咬定义”的具体构造。只要它能在这个构造里站住，定义就算真的锁了。这个判断，正是我下面不再继续选择 `FORMALIZE_DEFINITIONS_FIRST` 的原因。】

### 下一定理与证书候选

| 候选 | 评级 | 严格判断 |
|---|---|---|
| `OI_N^op(w)=0 iff w is product form` | `PROVABLE_NOW` | 这几乎已经在包里：若 `w` 为 product，则 formal note 命题 2 给 `D_w=0`，所以 restriction 也为零；若 `w` 非 product，则命题 3 给出 `K∈A` 或 `K∈B0⊂N_add` 使 `D_wK≠0`，所以 `D_w|_{N_add}` 非零，算子范数必正。只需把这条推演整理成一页短 note。】 |
| product-control certificate | `PROVABLE_NOW` | 现有 harness 已经有 `2×3` product theorem-control block，且其度量本身就是要验证 `D_w=0` 与 ordered maps 等于 true residual。把它升级成 exact rational artifact 只是工程问题，不是理论问题。】 |
| near-product perturbation bound | `PLAUSIBLE_WITH_SMALL_PROOF` | 方向非常合理，但当前包自己也把它放在“需要补 `P_A,P_B0,P_N,D_w` 对权重依赖的本地证明/备忘录”之后。换言之，这不是坏想法，但现在还差关键一页证明。】 |
| judge-order finite toy | `PROVABLE_NOW` | 这不是新数学，只是现有二向表 theorem 的语义重命名；因此可以立即做，而且正因为它不新，所以更要严格写成 semantic relabel toy，不能冒充经验 judge bias 发现。】 |
| contamination-coupling finite toy | `PLAUSIBLE_WITH_SMALL_PROOF` | 可以用 exact `2×3` 或 `3×3` toy 做，但当前包并没有现成 artifact。它适合进入 certificate library，不适合作为第一新定理。】 |
| ranking-preservation / rank-flip certificate | `PLAUSIBLE_WITH_SMALL_PROOF` | 排名保持的 gap 引理本身很小，但要做成 package-grade certificate，必须同时冻结 roster、tie policy、score vectors、transport defect 和 gap。当前尚无工件，因此不应写成 `PROVABLE_NOW`。】 |
| finite gluing obstruction certificate | `PLAUSIBLE_WITH_SMALL_PROOF` | 公式已经有，zero-GPU 实现路径也清楚；真正缺的是一个最小 exact cover/witness。它比 near-product bound 更“对象化”，也更符合本轮任务，但仍需要先做一个 bounded construct 才能变成 `PROVABLE_NOW`。】 |

由此我给出一个更尖锐的排序：**数学上最容易立即完成的是 `OI^{op}_{N_add}` 定理与 product control；研究上最值得立即创造的新对象，则是 finite gluing obstruction certificate。** 这两者并不矛盾。前者是把旧 order-defect 主链补成指数对象；后者是让 chart/transport/defect 语言第一次在局部—整体层次上落成一个 bounded object。真正错误的做法，是再去堆 contamination/ranking 等语义 toys，却没有先拿一个更硬的 finite glue object 把定义层压实。】

## Node36 请求与最终决断

本包**足够完成当前评审**，因此没有 blocking request；但若 node36 要把下一步立刻变成 taskbook，我建议补三类**可选**文件，全部保持 bounded。请求格式如下。

```text
REQUEST_TO_NODE36_CODEX:
- path or file category: any existing finite 2x3 / 3x3 exact-certificate notes, scripts, scratch markdowns, or JSON artifacts under docs/infra/ or scripts/
- why needed: to determine whether product controls, near-product families, contamination-coupling toys, or ranking-instability toys already exist in primary exact form
- claim tested: whether the certificate library can advance immediately beyond the current 2x2 witness without inventing new package-external mathematics
- blocking or optional: optional
```

```text
REQUEST_TO_NODE36_CODEX:
- path or file category: any local proof note, scratch derivation, or audit memo on how P_A, P_B0, P_N, or D_w depend on the positive weight table w
- why needed: to decide whether near-product perturbation bounds can be upgraded from plausible to provable and to support a mathematically honest local bound for OI^{op}_{N_add}(w)
- claim tested: whether D_w and the relevant projections admit a clean continuity or local Lipschitz-type control on the positive-weight simplex
- blocking or optional: optional
```

```text
REQUEST_TO_NODE36_CODEX:
- path or file category: any synthetic transport / holonomy / gluing script, note, markdown, or JSON artifact referenced by older residual-transport reports, especially exact or zero-GPU finite examples not shipped in the current ZIP
- why needed: to check whether a finite overlap-obstruction or square-path defect certificate already has a partial implementation that can be normalized into the current package style
- claim tested: whether FINITE_GLUE_OBJECT_FIRST can start from an existing bounded primary artifact rather than from a fresh build
- blocking or optional: optional
```

我的最终选择是：

```text
FINITE_GLUE_OBJECT_FIRST
```

原因不是“定义层不重要”，恰恰相反，是因为**定义层已经成熟到足够支撑一个具体新对象，而继续停留在 definitions-only 会边际收益递减**。本轮 object atlas 已经完成，不需要再选 `OBJECT_ATLAS_FIRST`；而若再选 `FORMALIZE_DEFINITIONS_FIRST`，下一轮很可能只是把 Report25 的草稿再写一遍。相比之下，`FINITE_GLUE_OBJECT_FIRST` 可以把 chart、transport、defect、local section、restriction、allowed local gauge 这些分散定义一次压成一个**最小 exact finite object**，从而顺手检验定义层是否真的牢靠。与此同时，这个分支仍然保持零 GPU、完全 finite、严格 anti-hype，并且与 order-defect 主脊柱同构：原来证明的是“同一 carrier 上顺序不自由”，下一步证明的是“局部 chart objects 也不自动可粘”。这正是 wider RAG object chain 中最像“下一块硬石头”的对象。】

如果 node36 现在就要把它转成操作化 taskbook，我建议直接落成四步，且全部围绕一个 bounded exact artifact 组织。先冻结本报告接受后的定义层最小修订版：`chart + roster + K_c + M_c + transport + certificate + OI^{op}_{N_add}`。然后新建一个 exact-rational 零 GPU 脚本，专做“两个重叠局部 charts 的 gauge-minimized overlap obstruction”，输出 Markdown + JSON + sha256。再给它配一个 paired control：一个 `Obs(K)=0` 的可粘 product-like 正控，一个 `Obs(K)>0` 的严格反控。最后，只有在这个最小 gluing object 稳固之后，才扩展到 square-path defect 和更远的 ranking / contamination toys。这样做既不跳出当前 package 的证据边界，又真正把“对象图谱回合”转换成了一个可以执行的下一工程。】