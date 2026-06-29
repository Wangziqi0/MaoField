# Order-Defect v1.4 精确附录与书目审计报告

## 顶层结论

`preprint_requires_minor_bibliography_or_wording_fixes`

我基于上传的 zip 包逐项检查了指定主文件；本次任务列出的 primary files 均在 bundle 内存在。就**数学核**而言，v1.4 的 exact rational appendix / certificate 已经把先前最敏感的短板补上了：主见证、对称见证、投影矩阵、交换子矩阵与范数平方都能用有理数精确算术闭合，而且与 JSON dump 一致。阻塞点现在**不在核心数学**，而在**外发前的一轮书目与措辞归一化**：一方面，相关工作虽然已经从“chat 内部句柄”推进到 DOI/稳定记录层面，但还没有形成一段真正可对外承受审稿的 positioning；另一方面，harness 的“regression-only, not proof artifact”边界已经明显改善，但还没有在所有当前工件上无歧义地统一。与此同时，我没有在所检索的稳定记录中发现与该 bundle 中对象**完全同题同结论同最小见证**的现成重复件；但它四周的先行文献非常密集，尤其是 dependent-input / non-independent ANOVA-Hoeffding 方向与 two-projections 方向，因此外发时必须把新意收缩到“compact finite weighted projection-order artifact note with an exact 2×2 witness”这一层级，不能上升为“新 ANOVA 理论”或“新非交换投影理论”。citeturn10search0turn0search1turn10search1turn7view4turn2search9turn11search6turn8view0turn5search2turn8view3turn4search1

## 审计总表

| 审计项 | 结论 | 说明 |
|---|---|---|
| exact_fraction_certificate | **PASS** | `EXACT_WITNESS_V1_4_20260629.md` 与 `exact_witness_v1_4_20260629.json` 中主见证、对称见证、范数平方、`D_w` 一致；我独立重算后无分数修正需求。 |
| exact_projection_matrix_dump | **PASS** | JSON 已给出 `P_C`, `P_A`, `P_B0`, `P_N`, `D_w` 全部 exact row-major 分数矩阵，且与独立重算逐项一致。 |
| T1_T2_T3_unchanged_after_edits | **PASS** | v1.4 新增的是 exact certificate 与 preprint-safe wording，未改写 v1.3 的 T1/T2/T3 数学命题边界。 |
| harness_regression_only_boundary | **WARN** | outward-facing markdown 已基本到位，但 JSON 与部分源脚本级文字仍未把“不是 proof artifact、数学结论由 analytic proof + exact certificate 承担”写到最清楚的程度。 |
| related_work_durable_citations | **WARN** | 旧的“chat 句柄”问题已基本消失，但外发前仍建议把书目规范化，并补入一个非常近的新邻接项：Lamboni 2026 的 DANOVA 论文。citeturn8view0 |
| duplicate_risk | **WARN** | 未发现 exact duplicate；但与 Hooker–Chastaing–Owen–Iooss–Il Idrissi–Lamboni 一线及 Halmos–Böttcher–Corach 一线都高度邻接，措辞必须收窄。citeturn10search0turn0search1turn10search1turn7view4turn2search9turn11search6turn8view0turn5search2turn8view3turn4search1 |
| novelty_wording | **WARN** | 当前 safe wording 方向基本正确，但仍需再压一层，明确不是 new ANOVA / new dependent-input decomposition / new projection theory。citeturn10search0turn0search1turn11search6turn8view0turn5search2turn4search1 |
| preprint_readiness | **WARN** | 不是“数学上还没立住”，而是“对外学术定位还差最后一轮整理”。 |
| evidence_boundary | **PASS** | bundle 内 boundary 持续稳定，未出现被禁升级。 |
| non_specialist_explanation | **WARN** | package 中已有面向外部的抽象说明，但“非专业读者 30 秒可懂”的版本还不够定型。 |

## 精确算术与矩阵核对

我按 bundle 中脚本所声明的**正权有限加权内积**设定独立重算了 2×2 证书。取

\[
w=\frac1{11}\begin{pmatrix}1&2\\3&5\end{pmatrix},
\qquad
K_B=\left(\frac7{11},-\frac4{11},\frac7{11},-\frac4{11}\right),
\qquad
K_A=\left(\frac8{11},\frac8{11},-\frac3{11},-\frac3{11}\right),
\]

并用加权正交投影公式分别得到 \(P_C,P_A,P_{B0},P_N\)。随后重算

\[
R_{Q\to B}=(I-P_{B0})(I-P_A)(I-P_C),\qquad
R_{B\to Q}=(I-P_A)(I-P_{B0})(I-P_C),
\]
\[
D_w=R_{Q\to B}-R_{B\to Q}.
\]

独立结果与 bundle 断言完全一致：

\[
R_{Q\to B}K_B=\left(\frac1{32},\frac5{168},-\frac1{96},-\frac1{84}\right),\qquad
R_{B\to Q}K_B=0,
\]
\[
\|R_{Q\to B}K_B\|_w^2=\frac{61}{177408},
\]
\[
R_{Q\to B}K_A=0,\qquad
R_{B\to Q}K_A=\left(\frac1{42},-\frac1{84},\frac5{224},-\frac3{224}\right).
\]

JSON 中主见证坐标与范数平方位于 `exact_witness_v1_4_20260629.json:51-77`，对称见证位于 `217-242`，权重位于 `243-248`；markdown 证书对应摘要位于 `EXACT_WITNESS_V1_4_20260629.md:30-66`。我没有发现任何需要更正的分数条目。换言之，若按你的规则“若矩阵项错误则给 corrected fraction”，本次答案是：**没有错误项，因此无 corrected fraction 列表**。  

更关键的是，JSON 的 exact 矩阵 dump 确实闭合了主算子身份。独立重算得到

\[
D_w=P_{B0}P_A-P_AP_{B0}
\]

精确成立，而 JSON 中 `D_w` 的逐项矩阵

\[
D_w=
\begin{pmatrix}
0 & -\frac1{42} & \frac1{32} & -\frac5{672}\\
\frac1{84} & 0 & \frac1{56} & -\frac5{168}\\
-\frac1{96} & -\frac1{84} & 0 & \frac5{224}\\
\frac1{672} & \frac1{84} & -\frac3{224} & 0
\end{pmatrix}
\]

与独立重算完全一致；`P_A`, `P_B0`, `P_C`, `P_N`, `D_w` 五个矩阵均未发现任何 entry mismatch。对应 JSON 行段分别是 `P_A:105-130`, `P_B0:131-156`, `P_C:157-182`, `P_N:183-208`, `D_w:79-104`。这使得 `exact_fraction_certificate` 与 `exact_projection_matrix_dump` 两项都应判为 **PASS**。  

## 证明与边界审计

v1.3 核心证明文本没有被 v1.4 的附录升级悄悄改坏。形式说明在 `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 中仍然保持了以下逻辑链：有限正权设定与加权内积在 `41-102` 行；“代数直和但一般不是正交直和”以及 `P_N \neq P_C+P_A+P_{B0}` 在 `64-84` 行；T1 对应的 product-weight iff main-effect orthogonality 在 `104-152` 行；T2 对应的 `D_w=0` iff product form 与顺序无关性在 `177-239` 行；T3 对应的 non-product pure-main-effect witness exists 及“wrong-order output 是 sequential stripping artifact，不是真交互残差”在 `243-283` 行；2×2 主见证与对称见证保留在 `285-335` 行。新 placeholder 没有反向改写这些结论，而是把它们压缩成对外可读版本：核心一句话 claim 在 `PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md:11-17`，摘要性复述在 `20-45`，narrow contribution 列表在 `47-76`。因此，`T1_T2_T3_unchanged_after_edits` 应判 **PASS**。  

evidence boundary 方面，这个 bundle 保持得很克制。`EXACT_WITNESS_V1_4_20260629.md:5-7,16-28`、`PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md:117-139`、`ORDER_DEFECT_PREPRINT_RIGOR_AUDIT_ADOPTION_NOTE_20260629.md:74-99` 与 `STATE.md:16,24-29` 都继续把 ceiling 固定在 `definitions_and_harness_viable_only`，并把 Mode B 固定为 `insufficient_artifact`。我没有看到 forbidden upgrades 被偷偷抬升成正面经验结论，因此 `evidence_boundary` 应判 **PASS**。  

harness 边界则是**明显改善，但尚未彻底统一**。好的部分是：`PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md:71-76` 已经写出 “This harness is not a proof artifact”；`SYNTHETIC_HARNESS_V1_3_20260628.md:96-104` 更明确写成 “The harness is regression support only. It is not a proof artifact ... not a substitute for the analytic proof or the exact rational certificate”；`STATE.md:16` 与 `README.md:207-213` 也把下一步任务表述成“确认 regression-support-only wording”。但尚未完全统一的部分是：`synthetic_harness_v1_3_20260628.json` 的顶层只说“internally checkable on finite synthetic examples only”与“not MaoField empirical evidence / does not authorize training or a new loss”，并没有直接把“proof responsibility belongs to the analytic proof + exact certificate”写出来；脚本源文件 `debranded_residual_transport_harness_v1_3.py:1-7,402-418` 也没有把这句边界口径写到最醒目的地方。因为我没有看到任何文本**把 JSON 浮点数当 exact proof**，所以这项不应是 FAIL；但因为它还没达到“every current text says this clearly”的严格程度，所以我给 `harness_regression_only_boundary` **WARN**。  

## 书目与重复风险审计

就 bibliographic durability 而言，placeholder 现在已经不再依赖 chat 内部句柄；它列出的 DOI / arXiv 方向基本都能通过稳定记录核实。更重要的是，这些记录共同说明：如果把稿子写成“新 dependent-input ANOVA 理论”“新 Hoeffding 分解理论”或“新 noncommuting projections 理论”，风险会非常高；如果把它写成“一个有限加权二维表里 sequential nuisance stripping 会制造伪交互 residual 的紧凑警示 note”，则仍有可发空间。Hooker 2007 明确是 dependent variables 下的 generalized functional ANOVA diagnostics；Chastaing–Gamboa–Prieur 2012/2015 明确是 dependent variables 的 generalized Hoeffding-Sobol decomposition 与 numerical methods；Owen–Prieur 2017 和 Iooss–Prieur 2019 则把依赖输入下的重要性分配进一步转向 Shapley 语境；Il Idrissi 等 2025 与 Lamboni 2026 又把 dependent-variable / non-independent ANOVA-Hoeffding 背景向前推了一步。另一侧，Halmos 1969、Böttcher–Spitkovsky 2010、Corach–Maestripieri 2010 则牢牢占住了 two-subspaces / two-projections 的经典背景。citeturn10search0turn0search1turn10search1turn7view4turn2search9turn11search6turn8view0turn4search1turn5search2turn8view3

下面按你要求的格式逐条给出审核结论。为避免原始网址，我只保留 DOI / arXiv / 稳定记录名：

| 记录 | 状态 | 接近程度 | 是否强制改措辞 |
|---|---|---|---|
| Hooker 2007, *Generalized Functional ANOVA Diagnostics for High-Dimensional Functions of Dependent Variables*, DOI **10.1198/106186007X237892** | **verified** | 很近。它已经把“dependent variables 下的 generalized functional ANOVA diagnostics”立住了。 | **是**。必须保留“not a new ANOVA theory”。citeturn10search0turn8view1 |
| Chastaing–Gamboa–Prieur 2012, *Generalized Hoeffding-Sobol decomposition for dependent variables*, DOI **10.1214/12-EJS749** | **verified** | 很近。它已经覆盖 dependent variables 的 generalized Hoeffding-Sobol decomposition。 | **是**。必须保留“not a new dependent-input decomposition theory”。citeturn0search1turn7view4 |
| Chastaing–Gamboa–Prieur 2015, *Generalized Sobol sensitivity indices for dependent variables: numerical methods*, DOI **10.1080/00949655.2014.960415** | **verified** | 很近。它把 hierarchical orthogonality 与 computation 路线明文化。 | **是**。你的 note 只能说“finite weighted projection-order artifact”，不能像在提一种 generalized numerical decomposition 方法。citeturn10search1turn7view4 |
| Owen–Prieur 2017, *On Shapley Value for Measuring Importance of Dependent Inputs*, DOI **10.1137/16M1097717** | **verified** | 中近。不是同一对象，但它明确把 dependent-input 语境里的解释重心从 ANOVA 困难推进到 Shapley。 | **是**。需避免让人误会你在替代 dependent-input importance theory。citeturn7view4 |
| Iooss–Prieur 2019, *Shapley effects for sensitivity analysis with correlated inputs*, DOI **10.1615/Int.J.UncertaintyQuantification.2019028372** | **verified** | 中近。依赖输入 sensitivity attribution 的重要后续。 | **是**。要继续坚持“不是 Shapley / sensitivity paper”。citeturn2search9turn8view0 |
| Il Idrissi et al. 2025, *Hoeffding decomposition of functions of random dependent variables*, DOI **10.1016/j.jmva.2025.105444** | **verified** | **非常近**。这是当前最需要你主动绕开的 broad-theory 邻接项之一。 | **是，而且是强制性的**。应明确：本文不提出任何新的 dependent-variable Hoeffding decomposition。citeturn11search6turn11search18 |
| Böttcher–Spitkovsky 2010, *A gentle guide to the basics of two projections theory*, DOI **10.1016/j.laa.2009.11.002** | **verified** | 背景近。它占住了 two projections theory 的综述入口。 | **是**。必须写“not a new noncommuting projection theory”。citeturn5search2turn13search0turn13search17 |
| Corach–Maestripieri 2010, *Products of orthogonal projections and polar decompositions*, arXiv **1011.5237** | **verified** | 背景近。属于 orthogonal projections 的产品与极分解方向。 | **是**。只能把它当背景，不可暗示“我们推进了 products/commutators 的一般理论”。citeturn8view3 |
| Halmos, *Two subspaces*, Trans. Amer. Math. Soc. 144 (1969), 381–389, DOI **10.1090/S0002-9947-1969-0251519-5**, JSTOR stable **1995288** | **verified** | 经典背景，非直接 duplicate。 | **是**。应把它作为 classical two-subspace background 的精确记录，不要再写“Halmos-style theory”而不给完整条目。citeturn4search1turn13search3turn13search17 |

除了你最初列出的最低清单，我还认为**Lamboni 2026, *On ANOVA-Type Decompositions of Functions with Non-independent Variables: Sensitivity Analysis*, DOI 10.1137/24M1712680** 应该被纳入外发版 related work。原因不是它与你的稿子同题，而是它在 2026 年已经把“non-independent variables 下的 ANOVA-type decomposition”作为一个**显式命名对象**写进了 SIAM/ASA JUQ。你的稿子如果不提它，就会让“not a new ANOVA theory”这句免责声明显得不够及时。它不要求你改数学，只要求你把 positioning 再收紧一格。citeturn8view0

因此，我对 duplicate-risk 的最终判断是：**没有发现 exact duplicate，所以不应判 `reject_as_duplicate_or_overclaim`；但若 novelty wording 稍一放大，就会在读感上撞进相邻成熟文献带。** 安全表述应当正如你给出的目标版本：不是新 ANOVA 理论，不是新 dependent-input decomposition 理论，不是新 noncommuting projection 理论，而是一个**compact finite weighted projection-order artifact note with an exact 2×2 witness**。citeturn10search0turn0search1turn11search6turn8view0turn5search2turn8view3turn4search1

## 发布措辞与最终决定

**建议保留的句子**

以下三类句子，我建议保留，最多只做排版级 copyediting。

第一，必须保留“**The nonzero wrong-order output is a sequential stripping artifact, not a true interaction residual.**” 这是整篇短 note 的安全阀，也是它与广义 dependent-input decomposition 理论拉开距离的最关键句。  

第二，必须保留“**It does not introduce a new theory of functional ANOVA, Sobol indices, Shapley effects, or dependent-input decompositions.**” 但要在其后再补一句，把 2025–2026 的邻接背景说清。  

第三，必须保留 T2 后面的 quantifier guard，即“非 product 只推出存在 witness，不推出 every input 都会差异”。这能防止从“存在顺序缺陷”滑成“普遍顺序不稳定”的过度结论。  

**建议删除或改写的句子**

“diagnostic field” 这类内部行话，外发版最好全部替换成 **finite weighted two-way table** 或 **finite weighted two-way array**。这不是数学问题，而是学术读感问题：前者像正式对象，后者更像项目内部口径。  

如果摘要或引言里让 harness 与 theorem 像“双支柱证据”并列，也建议改写。外发版里，harness 的地位只能是**deterministic regression support**，不能像“证明的一半”。  

**建议直接加入的精确替换句**

我建议在摘要末尾加入这一句，作为最终安全定锚：

> *This note isolates a finite weighted projection-order artifact in a two-way table; it is not proposed as a new dependent-input ANOVA or Hoeffding decomposition theory.*

我还建议在 related-work 段首加入这一句：

> *Closest antecedents lie in dependent-variable ANOVA-Hoeffding decompositions and in the classical theory of two noncommuting orthogonal projections.*

最后，把 harness 边界在**所有当前工件**上统一成下面这句话最稳妥：

> *The accompanying floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and the exact rational certificate, not by the JSON floats.*

这三句的作用分别是：压住 broad-ANOVA 误读、压住 projection-theory 误读、压住 “float JSON = proof artifact” 误读。它们与现有近邻文献的边界最一致。citeturn10search0turn0search1turn11search6turn8view0turn5search2turn8view3turn4search1

**最终发布决定**

- top-level classification：`preprint_requires_minor_bibliography_or_wording_fixes`
- final posting decision：**revise first**

这不是因为数学还站不住；相反，数学最容易被挑出的 exact witness / certificate / matrix dump 已经补到位了。现在要做的是一次很短的外发清理：  
一是把 bibliography 规范成正式参考文献表，并补入 Lamboni 2026；  
二是把 harness disclaimer 在 placeholder / README / harness json / 相关 summary wording 上统一；  
三是继续删掉 project-internal 词与任何可能被读成“大理论”的句子。  
做完这一步后，我认为它就可以作为**短、窄、诚实**的 preprint note 发出。citeturn8view0turn10search0turn0search1turn11search6turn5search2turn4search1

**给非专业读者的简短解释**

把这篇 note 想成四格表。你想把一张表拆成：整体平均、行效应、列效应，剩下来的才叫“交互”。如果每个格子的权重刚好能写成“行权重 × 列权重”，那么你先减行再减列，还是先减列再减行，结果一样。  

但如果这些格子的权重不是这种乘法结构，那么顺序就会开始捣乱：原本只是“纯行效应”或“纯列效应”的东西，经过错误顺序的剥离后，可能会留下一个看起来像“交互”的残差。这个残差并不代表系统里真的存在新的交互结构；它只是告诉你，**你的剥离顺序制造了一个假象**。这篇 note 的价值，就在于它把这个假象用一个最小的、可以精确写成分数的 2×2 例子钉死了。