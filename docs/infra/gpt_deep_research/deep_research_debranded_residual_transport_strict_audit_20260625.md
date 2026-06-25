# 去品牌化残差传输项目严格审计

本报告按你给定的读序，主要依据提供的 ZIP bundle 进行审计；关于仓库级别验证，归档的运输/holonomy 数学审计已明确写明当时未能建立可用的 GitHub connector 读取链路，因此本轮最稳妥的证据边界仍应视为“以 supplied bundle 为准，仓库级别连接器复核视为 blocked，不能拿公共 GitHub 页面、raw 页面、搜索摘要或 404 结果充当规范仓库证据”。这一点不会改变下面的核心判断：**MaoField 作为经验阳性叙事已经被严格压回负中心 pilot；但从这些被“去魅”的材料里，仍然可以抽出一个干净的、有限维的、可被杀死也可形成 no-go 定理的数学项目。**（bundle：`docs/infra/gpt_deep_research/deep_research_transport_holonomy_math_turn_audit_20260624.md`:3–13；`STATE.md`:16–27）

## 证据边界

先把能说和不能说的范围钉死。bundle 多处重复同一结论：MaoField 当前**只能**支持零 GPU formal preregistration、schema/occupancy 检查、checker 可执行性、synthetic harness 可执行性、以及负中心的 measurement-audit 结论；它**不能**支持 full panel 已运行、16-cell full-panel aggregate 已存在、任何 residual/interaction/quotient-residual/transport/holonomy field 已被观察到、LOSO 已通过、F3 为正、glass box 已被打破、training 已获授权、或 new loss 已获授权。当前 Mode B 的固定裁定仍是 `stable non-scalar residual object = insufficient_artifact`，现有 interaction smoke 的固定裁定仍是 `smoke_conjecture_only`。passing future gates 的天花板也仍然只是 `eligible_for_next_design_review_only`，而不是“发现了对象”。（bundle：`STATE.md`:16–27, 84–89；`docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_STATUS_20260624.md`:10–24, 100–114；`docs/infra/gpt_deep_research/QUOTIENT_RESIDUAL_MAINLINE_ADOPTION_NOTE_20260624.md`:25–39, 62–99；`docs/infra/math_turn_20260622/NULL_TESTS_CONTRACT_20260624.md`:5–45；`scripts/q4_hypercube_interaction_prereg_analysis.py`:1–7, 33–55, 566–602）

这意味着我必须严格拒绝两种“偷升级”。第一种，是把 smoke、checker dry-run、schema completeness、toy harness、small residual hints 之类东西，偷换成经验发现。第二种，是把哲学词汇、历史叙事或“老 MaoField claim 的去通胀版”偷换成定义、命题和反例。bundle 自己已经把这条边界写得很硬：新线是去品牌化的 finite weighted residual transport / holonomy / no-go 项目；MaoField 本体保留为 negative-centered empirical line，不得用新线给旧线加正面光环。（bundle：`docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_STATUS_20260624.md`:8–24, 100–127；`docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_CORE_DESCRIPTION_20260624.md`:11–34, 91–134；`docs/infra/gpt_deep_research/TRANSPORT_HOLONOMY_MATH_TURN_AUDIT_ADOPTION_NOTE_20260624.md`:25–38, 92–123）

我的严格结论因此很简单：**MaoField 经验线目前不配任何阳性升级；但这并不自动杀死数学线。真正值得保留的不是“已经发现了某种场”，而是“是否存在一个在去除了 nuisance 之后、还能在尺度间一致运输并通过随机化与低秩控制的有限维对象”。** 这正是一个可以成功地产生 no-go 定理的数学项目，而不是一个必须产出阳性经验结果的项目。（bundle：`docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_CORE_DESCRIPTION_20260624.md`:17–34, 123–134；`docs/infra/gpt_deep_research/RESIDUAL_TRANSPORT_HOLONOMY_ADOPTION_NOTE_20260624.md`:41–93）

## 形式对象审计

这个项目若要成立，底层对象不能只是单尺度的“一个残差数值”，而应当是**一个有限尺度格上的算子包**。最干净的写法是：对每个有限尺度 \(s\)，给出可容许三元组 \((X_s,w_s,N_s)\)，其中 \(X_s\) 是有限表格，\(w_s(x)>0\) 是正权重，\(N_s\subset H_s:=L^2(X_s,w_s)\cong\mathbb R^{X_s}\) 是**预注册、pre-outcome、与结果无关**的 nuisance 子空间；内积取
\[
\langle f,g\rangle_s=\sum_{x\in X_s} w_s(x) f(x)g(x).
\]
令 \(P_s=\Pi_{N_s^\perp,w_s}\) 为加权正交投影，则局部残差定义为
\[
R_s(K)=P_sK_s.
\]
这是有限维加权 Hilbert 空间里的标准正交投影/最小范数商代表构造：\(R_s(K)\) 既是从 \(K_s\) 中剔除 nuisance 后的唯一最小距离代表，也是商空间 \(H_s/N_s\) 中 \([K_s]\) 的最小范数代表。这个层面上，对象是严格的，不是隐喻。（bundle：`docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_CORE_DESCRIPTION_20260624.md`:36–67；`docs/infra/gpt_deep_research/QUOTIENT_RESIDUAL_FINITE_ANOVA_ADOPTION_NOTE_20260623.md`:24–49；`docs/infra/gpt_deep_research/deep_research_quotient_residual_finite_anova_kill_framework_20260623.md`:23–57）

有效的 nuisance 子空间必须满足三条硬条件。它必须在看结果之前就固定；它必须只由常数项、主效应、预注册 slope、预注册 smooth trend、matched mean/slope 模板、coarse-scale pullback 等**前置结构**生成；它不得把由 \(K\) 本身“看出来”的方向事后塞进 nuisance。否则，所谓 residual 只是后验清洗产生的剩余项，不具“对象同一性”。（bundle：`docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_CORE_DESCRIPTION_20260624.md`:38–52, 91–121；`docs/infra/gpt_deep_research/deep_research_quotient_residual_finite_anova_kill_framework_20260623.md`:34–38）

有效的 coarsening/refinement 映射也必须被严格固定。若 \(\rho:s\to s'\) 表示细到粗的粗化边，则最自然的 \(C_\rho:H_s\to H_{s'}\) 是**加权块平均**或更一般的、由预注册 block 结构诱导的加权条件期望；若要走粗到细的 refinement，则应明确使用 pullback 或 coarsening 的加权伴随，而不能把“复制”“插值”“归一化权重修补”混作一谈。否则，edge defect 的非零就可能来自你改写了算子本身，而不是对象真的不自然。bundle 的深层文档已经给出 block-average 的标准写法，这一选择是正确的方向。（bundle：`docs/infra/gpt_deep_research/deep_research_quotient_residual_finite_anova_kill_framework_20260623.md`:186–224）

在此基础上，边缺陷应定义为
\[
D_\rho(K)=C_\rho P_sK_s-P_{s'}C_\rho K_s,
\]
它精确测量“先剔 nuisance 再粗化”和“先粗化再剔 nuisance”之间的不交换。square holonomy 也不应当停留在口号层面，而应写成一个明确回路差：对一个 refinement square
\[
s_0\to s_1\to s_2,\qquad s_0\to s_1'\to s_2,
\]
定义
\[
H_\square(K)=C_{\rho_2}P_{s_1}C_{\rho_1}P_{s_0}K_{s_0}
-
C_{\rho'_2}P_{s'_1}C_{\rho'_1}P_{s_0}K_{s_0}.
\]
这才是“holonomy defect”的严肃版本：它不是说终点 residual 大不大，而是说**同一对象沿两条尺度路径运输后是否同一**。若你不把它写成一个终点空间里的明确差向量，这个词就只是在美化 path dependence。 （bundle：`docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_CORE_DESCRIPTION_20260624.md`:53–67；`docs/infra/gpt_deep_research/RESIDUAL_TRANSPORT_HOLONOMY_ADOPTION_NOTE_20260624.md`:53–93；`docs/infra/gpt_deep_research/deep_research_transport_holonomy_math_turn_audit_20260624.md`:51–87, 118–164）

我建议采用两层等价关系。第一层是**nuisance gauge 等价**：若 \(K_s-K'_s\in N_s\) 对所有尺度都成立，则二者定义同一 residual family。第二层是**transport isomorphism 等价**：若存在一族保持内积的加权等距 \(U_s:H_s\to \widetilde H_s\)，满足 \(U_sN_s=\widetilde N_s\) 且 \(U_{s'}C_\rho=\widetilde C_\rho U_s\)，则两套系统是同一个对象的坐标重写。真正应该保留的不变量，不是某个坐标名字，而是：各尺度残差范数、堆叠残差的奇异值谱、principal-angle profile、edge defect profile、square holonomy profile、与随机同维子空间对比后的 capture quantile、以及满足所有 guards 的最小有效维数，也就是我会称作 **transport-stable rank** 的东西。principal angles 由正交基内积矩阵的奇异值给出，而随机同维子空间的自然零分布住在 Grassmann 流形的正交不变测度上，所以“随机同维子空间”作为 kill control 在数学上不是拍脑袋，而是正好对准了“不要奖励被命名的坐标轴”。citeturn4view2turn4view3

我的审计结论是：**这个对象作为有限维数学对象是成立的，但前提是你把它当成一个 projection–coarsening operator package 来定义，而不是把“residual transport”“holonomy”当作经验发现名词。** 一旦如此定义，它是严肃的；一旦不如此定义，它就是包装术。 （bundle：`docs/infra/gpt_deep_research/TRANSPORT_HOLONOMY_MATH_TURN_AUDIT_ADOPTION_NOTE_20260624.md`:73–123；`docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_CORE_DESCRIPTION_20260624.md`:36–67）

## 产品权重与非产品权重

这里必须非常严格，因为这是当前 bundle 最容易被偷换概念的地方。经典 functional ANOVA / Hoeffding 语言之所以“干净”，是因为它在独立、产品型参考测度下有正交分解、零边际、以及方差分解这些标准性质；Hooker 在标准 functional ANOVA 综述里明确给出这种分解、零均值、正交性与 variance decomposition 的结构，并指出当输入存在强依赖时，沿用 uniform/product-type 诊断会把质量放到低概率区域，因而需要改用基于一般 \(L^2\) 权重和投影的 generalized / weighted functional ANOVA。Rahman 则进一步在 dependent probability measures 下发展 generalized ANOVA decomposition，强调它与经典独立情形不是同一件事。citeturn2search0turn7view0turn4view1

因此，**什么时候 Hoeffding 语言合法**，标准必须写死。若 \(X=\prod_jA_j\)，且权重满足
\[
w(x)=\prod_j w_j(x_j),
\]
并具有满支撑，那么可以合法地说 classical Hoeffding / product-measure functional ANOVA：各阶项可按坐标子集组织，正交性和“自然的交互项”都有规范地位。若权重不是产品型，但仍然是正的，那么你当然仍可做有限维加权正交投影，把 \(\mathcal A=\{\mu+\alpha(q)+\beta(b)\}\) 之类子空间当 nuisance 并求其正交补；**但这时你得到的是“hierarchical weighted projection residual”，不是 canonical Hoeffding interaction**。这不是文字洁癖，而是对象类型真的变了。citeturn7view0turn4view1

bundle 在这一点上给了非常具体、而且足以终止偷换的内部证据：当前 q4×tokenpos4 schema weights 不是精确的 product-form weights；状态快照和 adoption note 给出同一组数值，最大绝对偏差约为 `0.0045863`，相对 product expectation 的最大相对偏差约为 `0.0721`。这意味着**当前载体只能说“non-product weighted hierarchical projection / residual program”**，不能说“canonical product-measure Hoeffding 已成立”。（bundle：`docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_STATUS_20260624.md`:78–98；`docs/infra/gpt_deep_research/TRANSPORT_HOLONOMY_MATH_TURN_AUDIT_ADOPTION_NOTE_20260624.md`:39–71；`STATE.md`:16–24）

显式 product reweighting 是第三种情况。若你以后真的构造一个新的产品参考测度 \(\widetilde w=\bigotimes_j \widetilde w_j\)，并明确宣布之后所有正交性、ANOVA、交互项、defect 与 holonomy 都是在 \(\widetilde w\)-geometry 里定义的，那么 Hoeffding 语言可以重新合法；但那时研究对象已经不再是“观察到的 source-only schema geometry”，而是“一个显式重加权后的参考几何”。这在数学上完全可以做，前提是你**不能把 reweighted object 伪装成 observed object**。若不做这层区分，整个项目会在术语层面上崩坏。 （bundle：`docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_STATUS_20260624.md`:90–98；`docs/infra/gpt_deep_research/deep_research_quotient_residual_finite_anova_kill_framework_20260623.md`:127–159）

所以我的判定是：当前 carrier 上，**合法语言只有两种**。一种是“strict additive nuisance 的加权正交投影残差”；另一种是“非产品权重下的 hierarchical weighted projection / transport / holonomy”。任何把当前 carrier 直接包装成 canonical Hoeffding carrier 的写法，我都视为错误。 （bundle：`docs/infra/gpt_deep_research/QUOTIENT_RESIDUAL_FINITE_ANOVA_ADOPTION_NOTE_20260623.md`:31–49；`docs/infra/gpt_deep_research/TRANSPORT_HOLONOMY_MATH_TURN_AUDIT_ADOPTION_NOTE_20260624.md`:39–71）

## 定理与禁行议程

这个项目要有价值，不能靠“指标清单”；它必须有命题、反例和 no-go。下面我给出七个足够精确、而且确实能把弱想法杀死的目标。

**秩一阴影空洞命题。** 把多个 residual 向量堆成矩阵 \(M\)。若 \(\operatorname{rank}(M)=1\)，则存在固定模板 \(u\) 与标量轨道 \(c_t\)，使 \(R_t=c_tu\)。于是所有 split-wise principal-angle stability 都退化为同一条直线的稳定性；这不是“发现了稳定的结构”，而只是“同一个模板亮暗变化”。因此，若 \(\sigma_2/\sigma_1\) 不过门槛，principal-angle stability 是空洞指标。这个命题与 bundle 已设的 `sigma2/sigma1 >= 0.25` 设计审查门槛完全一致。（bundle：`docs/infra/math_turn_20260622/NULL_TESTS_CONTRACT_20260624.md`:68–77；`scripts/q4_hypercube_interaction_prereg_analysis.py`:33–45, 576–599；`docs/infra/gpt_deep_research/deep_research_transport_holonomy_math_turn_audit_20260624.md`:170–174）

**随机同维子空间不可区分 no-go。** 设 \(V=N^\perp\) 且 \(\dim V=m\)。若候选 \(r\)-维 residual 子空间 \(E\subset V\) 的 capture statistic 在随机同维子空间零分布下并不显著更好，那么 \(E\) 不具坐标不变的结构意义，只是自由度消费。随机同维子空间之所以是自然零模型，是因为 Grassmann 上的均匀分布对正交变换不变，不偏袒被命名的轴。citeturn4view3turn4view2

**coarsening–projection 交换命题。** 对边 \(\rho:s\to s'\)，有
\[
C_\rho P_s=P_{s'}C_\rho
\]
当且仅当 \(C_\rho(N_s)\subseteq N_{s'}\) 且 \(C_\rho(N_s^\perp)\subseteq N_{s'}^\perp\)。若这不成立，则 \(D_\rho\) 稳定非零，说明该对象在尺度间不是自然运输的，而是 partition artifact 或 nuisance mismatch artifact。这个命题几乎是一行证明，但它把“好看的路径图”变成了真正会杀对象的条件。（bundle：`docs/infra/gpt_deep_research/deep_research_quotient_residual_finite_anova_kill_framework_20260623.md`:186–224）

**square holonomy no-go。** 若一个 refinement square 上每条边都满足 \(D_\rho\equiv 0\)，则该 square 上的 holonomy defect 必为零。反过来，若某个 square 观测到 \(H_\square(K)\neq 0\)，则至少有一条边不自然，或者中间 nuisance family 不是 functorial。换言之：holonomy 不是“更高级的神秘结构”，而是 path dependence 的可检验剩余。它的价值不是造词，而是把失败定位到边或中间尺度族上。（bundle：`docs/infra/gpt_deep_research/RESIDUAL_TRANSPORT_HOLONOMY_ADOPTION_NOTE_20260624.md`:78–93；`docs/infra/gpt_deep_research/deep_research_transport_holonomy_math_turn_audit_20260624.md`:172–184）

**commutator leakage 命题。** 若 \(P=\Pi_{N^\perp,w}\)，\(T\) 是 generation evolution 的线性近似，则 \([P,T]=0\) 当且仅当 nuisance sector 与 residual sector 都在 \(T\) 下不相互泄漏。非零 commutator 表示“先去 nuisance 再演化”和“先演化再去 nuisance”不是同一件事；但只有在它通过随机轴、rank-shadow 与 matched-template 控制之后，这个泄漏才配称作对象，而不是 nuisance leakage 的别名。（bundle：`docs/infra/gpt_deep_research/deep_research_quotient_residual_finite_anova_kill_framework_20260623.md`:226–264）

**gluing absorption no-go。** 所谓局部 obstruction，必须先模去“允许的局部 nuisance 扩张类”。若 overlap mismatch 在预注册允许的局部 nuisance 扩张下可被吸收到零，那么它不是几何障碍，而只是 gauge artifact。只有扩张之后仍然剩下稳定正的 obstruction，才配称 gluing obstruction。这个命题的效果是强迫项目放弃“局部不一致听起来很深”的叙事诱惑。（bundle：`docs/infra/gpt_deep_research/deep_research_quotient_residual_finite_anova_kill_framework_20260623.md`:266–296）

**非产品权重反例。** 构造一个 \(2\times 2\) 或 \(4\times 4\) 正权重表，使 \(w\neq w_Q\otimes w_B\)。在这种表上，按实际 \(w\) 做的加权正交投影残差，与按 product-marginal 外积参考测度做的 canonical interaction，一般不会相同。于是“同一个对象同时是 observed weighted residual 与 canonical Hoeffding interaction”的说法直接破产。这个反例不是可选项，而是当前 carrier 的必要清洗程序。（bundle：`docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_STATUS_20260624.md`:78–98；`docs/infra/gpt_deep_research/TRANSPORT_HOLONOMY_MATH_TURN_AUDIT_ADOPTION_NOTE_20260624.md`:39–71）

这七个目标里，前五个已经足以构成一个严肃的 no-go research program；后两个负责防止术语污染与载体偷换。我认为这正是这个项目最强的地方：**它不需要先假定对象存在；它可以通过证明对象不存在来成功。**（bundle：`docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_CORE_DESCRIPTION_20260624.md`:123–134）

## 最小合成 harness

bundle 已经有一个四块 toy harness：`scale_square_holonomy`、`nuisance_functoriality_digest`、`rank1_angle_vacuity_guard`、`random_same_dim_angle_gap`，且第一次归档运行全部通过，但最强 verdict 仍然只是 `synthetic_harness_only_no_maofield_claim`。这条边界是对的，必须保留。我的看法不是重写它，而是把它扩成**七块最小闭环**，每块都有正控和反控，仍然只在零 GPU 的小矩阵世界运行。（bundle：`docs/infra/math_turn_20260622/RESIDUAL_TRANSPORT_HOLONOMY_SYNTHETIC_HARNESS_20260624.md`:32–40, 69–110；`docs/infra/math_turn_20260622/RESIDUAL_TRANSPORT_HOLONOMY_SYNTHETIC_RESULT_20260624.md`:50–92）

第一块是**non-product weighted projection**。正控：product weights 的 \(4\times4\) 表，比较 canonical additive-interaction residual 与 weighted orthogonal residual，应接近机器误差。反控：构造正的但非产品型权重表，用同一信号比较两者，差异应显著非零。通过标准不是“差异小”，而是“正控几乎零、反控明显非零”。这块是为了防止 product-Hoeffding 语言偷偷回流。

第二块是**edge defect**。正控：细尺度与粗尺度使用 functorial additive nuisance，block-average coarsening 下 \(\|D_\rho\|\) 应接近零。反控：在粗尺度故意改坏 nuisance，例如只保留一边主效应或删掉必要 pullback，\(\|D_\rho\|\) 应抬高到明确阈值之上。bundle 当前脚本已经在这个方向上成功给出了自然/坏 nuisance 的分离，这一块应直接保留并制度化。

第三块是**square holonomy**。正控：\(4\times4\to 2\times4\to 2\times2\) 与 \(4\times4\to 4\times2\to 2\times2\) 两条路径上都用兼容 nuisance，要求 \(H_\square\approx 0\)。反控：只在一条路径的中间尺度放入 non-functorial nuisance，要求 \(H_\square\) 可见地非零。若正控都不过，定义坏；若反控不过，测试无辨识力。

第四块是**rank-shadow guard**。负控应是一簇重复模板 \(R_t=c_tu\)，要求 \(\sigma_2/\sigma_1\) 近零并被 kill；正控应是两方向或三方向 toy residual family，要求越过 `0.25` 的设计门槛。bundle 已经给出一个 barely-above-floor 的多方向正控，这很好，因为它能逼门槛真正工作，而不是只奖励巨大信号。（bundle：`docs/infra/math_turn_20260622/RESIDUAL_TRANSPORT_HOLONOMY_SYNTHETIC_RESULT_20260624.md`:61–72）

第五块是**random-subspace guard**。在固定 ambient dimension 下放一个已知真子空间，用 held-out vector 或 held-out family 的 capture ratio 与随机同维子空间的经验分布相比；必须要求真子空间分位数至少高于 \(95\%\) 或更保守阈值。否则，子空间解释没有坐标不变内容。

第六块是**gluing absorption**。取两个重叠 chart。正控应是一个只相差局部 offset / slope 的伪冲突，扩大局部 nuisance 后 obstruction 应被吸收到接近零。反控应是一个真正横跨 overlap 的非局部残差模式，扩大允许 nuisance 后仍剩稳定 obstruction。这块的目的不是追求 sheaf 术语，而是防止 sheaf 术语空转。

第七块是**commutator obstruction**。正控选一个保持 \(N\) 与 \(N^\perp\) 的块对角线性演化算子 \(T\)，要求 \([P,T]=0\) 或近零。反控则故意引入从 nuisance 到 residual、或反方向的泄漏块，要求 commutator norm 明显非零。如此一来，“projection-evolution leakage”才有了硬的 toy 原型。

这七块的意义，不是给 MaoField 升级，而是验证**定义是可执行的，正反控是可分的，门槛是可机械检查的**。这正是一个成熟的零 GPU 数学 harness 应该完成的任务。 （bundle：`docs/infra/gpt_deep_research/TRANSPORT_HOLONOMY_MATH_TURN_AUDIT_ADOPTION_NOTE_20260624.md`:112–123；`docs/infra/gpt_deep_research/RESIDUAL_TRANSPORT_HOLONOMY_ADOPTION_NOTE_20260624.md`:116–126）

## fail-closed 击杀套件

正式 kill suite 不应被理解为“更多指标”，而应被理解为**一组优先于一切解释的淘汰门**。bundle 当前的 null-tests contract 已经很接近正确形态：缺块或格式坏，直接 `insufficient_artifact`；若出现 outcome-derived weights、原始 provenance 错配、checker 自己去加载 checkpoint 或做 inference/train/new loss，则直接 `invalid_artifact`；若 noise floor 不过，直接 `killed_by_noise_floor`；若 \(\sigma_2/\sigma_1<0.25\)，直接 `killed_by_rank1_shadow`；其余块各自映射到 `killed_by_random_axis`、`killed_by_coarsening` 或 `insufficient_artifact`。我赞成这个 fail-closed 结构，并且建议原样继承到去品牌化项目。（bundle：`docs/infra/math_turn_20260622/NULL_TESTS_CONTRACT_20260624.md`:46–148；`scripts/q4_hypercube_interaction_prereg_analysis.py`:33–45, 56–157, 566–602）

但若要真正够“残忍”，我会把 kill suite 的文字说明改成下面这组硬门槛。**matched mean/slope** 不过，直接判定对象可被标量背景吸收。**random equal-size axes**、**within-axis shuffle**、**bad-axis labels**、**same-dimension random subspace** 任一不过，直接判定对象缺乏坐标不变意义。**rank/noise** 不过，直接说明你看到的是 low-rank shadow 或噪声边缘。**coarsening/refinement** 不过，直接说明对象是 partition artifact。**seed/generation holdout** 不过，则说明对象没有稳定可迁移身份，只能留在 `insufficient_artifact`。**local-to-global gluing controls** 若在允许的局部 nuisance 扩张下被吸收，则任何 obstruction 叙事即刻作废。 （bundle：`docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_CORE_DESCRIPTION_20260624.md`:91–121；`docs/infra/math_turn_20260622/NULL_TESTS_CONTRACT_20260624.md`:153–173）

我会把最终 verdict 规则写得更绝对一些。只要有一个高优先级 kill 触发，就立刻停止解释，不做“但也许仍有弱信号”的补叙。只有在 provenance、schema、noise floor、rank floor、random-axis、same-dim random-subspace、coarsening/refinement、seed/generation holdout、gluing sanity 全部通过后，才允许输出
\[
\texttt{eligible\_for\_next\_design\_review\_only}.
\]
而且这仍然**不是** observed field，不是 LOSO pass，不是 F3 positive，不是 glass-box breakthrough，更不是 training/new loss authorization。bundle 已经把这一点写死了，我建议在独立项目里继续保持这种紧口径。（bundle：`docs/infra/math_turn_20260622/NULL_TESTS_CONTRACT_20260624.md`:33–45, 121–148；`scripts/q4_hypercube_interaction_prereg_analysis.py`:586–602）

换句话说，这个 kill suite 的哲学应当是：**你不是先证明对象存在，再给它安排很多解释；你是先穷尽最便宜的伪对象机制，直到它们都杀不死，才允许对象“活到下一轮设计审查”。** 这才配叫 fail-closed preregistration。

## 最佳下一步

我选 **E：拆成一个单独的去品牌化项目，并写它的第一份正式说明**。

我不选 A，因为“继续纯数学定义”太含糊；bundle 其实已经有了相当清晰的定义骨架，真正缺的不是再堆一点定义，而是把它从 MaoField 的经验叙事里彻底剥离，变成一个自洽的 operator/no-go 项目。
我不选 B，因为延长零 GPU harness 固然必要，但它应该作为 E 的一部分，而不是顶替项目级决策。
我不选 C，因为任何 real aggregate 请求都会重新把项目拖回 MaoField 经验线，而当前 bundle 已经明确：full panel 仍未获批，且不应借数学线反向加压经验线。
我不选 D，因为对象并没有作为**数学对象**坍塌；坍塌的是“把它说成 MaoField 已有经验发现”的企图。
因此，最干净的选择就是 E：**经验旧线继续负中心、证据锁死；数学新线独立命名、独立 formal note、独立 theorem/no-go agenda。**（bundle：`docs/infra/gpt_deep_research/TRANSPORT_HOLONOMY_MATH_TURN_AUDIT_ADOPTION_NOTE_20260624.md`:28–38, 112–123；`docs/infra/gpt_deep_research/RESIDUAL_TRANSPORT_HOLONOMY_ADOPTION_NOTE_20260624.md`:28–39, 114–134；`docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_STATUS_20260624.md`:8–24；`STATE.md`:16–27）

这份第一 formal note 应该只做四件事。第一，固定 admissible triples、weighted projections、coarsening maps、edge defects、square holonomy、equivalence notions 与 invariants。第二，明确宣布当前 carrier 为 non-product weighted hierarchical projection setting。第三，列出前述七个 theorem/no-go targets 与七块最小 synthetic harness。第四，继承 fail-closed verdict 体系，并把 strongest allowed outcome 明确限制为“definitions/harness viable”或“eligible for next design review only”。做到这四点，项目就从被动防守，变成一个拥有清晰成功条件的数学线。

## 初中版解释

把所有容易作假的痕迹都擦掉之后，**有一块真的东西还剩下，但它不是“已经在 MaoField 数据里发现的神秘场”**。

剩下来的那块真实东西，更像一道数学题。你先有一张张带权重的小表格；先把平均数、主效应、平滑趋势、坏轴、低秩影子这些普通背景拿掉；再问：这些“剩下来的东西”，在换尺度、换分箱、换路径的时候，还是不是同一个对象？如果沿不同路径走一圈还能对上，而且不是随机子空间、不是单一模板拖着走、也不是局部补丁就能吸掉的错位，那才说明它有真正的形状。反过来，如果一加严控它就消失，那并不是什么都没得到；那恰恰证明，旧故事里那些看起来很复杂的结构，其实只是标量投影、低秩模板、坐标命名或分箱方式在放大自己。 （bundle：`docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_STATUS_20260624.md`:116–127；`docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_CORE_DESCRIPTION_20260624.md`:17–34, 123–134）

所以我的最后结论是：**经验阳性形状目前没有留下来；但一个更干净、更严格的数学形状留下来了。** 它的名字不该再是 MaoField 的自证叙事，而应该是：**有限维、带权重的残差传输与 holonomy 的 operator/no-go 项目**。这个项目最体面的成功方式，甚至可能不是“证明有某个神秘对象存在”，而是“证明在这些控制下，任何看起来神秘的对象都不可能成立”。这反而更硬。