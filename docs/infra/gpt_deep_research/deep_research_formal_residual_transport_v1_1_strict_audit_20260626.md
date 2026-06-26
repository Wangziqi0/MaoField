# Formal Residual Transport v1.1 严格审计报告

## 审计范围与总判决

本次审计严格按上传 bundle 的边界执行：它只允许把 v1.1 当作 **Mode A 的有限维数学补丁**，不允许把它当作 MaoField 经验结果；包内 README、零上下文审计 prompt、Formal Note v1.1、以及 harness summary/JSON 都一致把当前上限锁在 `definitions_and_harness_viable_only`，并继续禁止 full panel、observed field、checkpoint loading、model inference、training、new loss 等说法。对 MaoField 的 Mode B 结论因此必须维持 `insufficient_artifact`，这一点在包内是反复写死的。仓库二次核验方面，prompt 明确要求“若 GitHub connector 不可用或不明确，则继续基于上传 bundle，并把仓库验证标记为 blocked”；本次会话里没有可用 GitHub 仓库连接器，所以本报告是 **bundle-first、repo verification blocked** 的审计。 （包内证据：00-README_FOR_142_AND_PRO.md:14-41,62-90；GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_1_AUDIT_PROMPT_20260625.md:13-18,63-89,159-175；FORMAL_NOTE_V1_1_20260625.md:15-31,267-311；SYNTHETIC_HARNESS_V1_1_20260625.md:5-16,81-104；synthetic_harness_v1_1_20260625.json:69-77,269-284）

我的最严格、仍可辩护的结论是：**v1.1 不是失败品，也不是完成品；它应被接受为有效补丁方向，但必须要求一个小而硬的 v1.2 修补。** 原因很清楚。它确实补上了 v1 最显眼的代数漏洞：商下降命题、`[P,T]` 交换子判据、square holonomy 的精确分解、共同 ambient 空间先决条件、随机子空间解析 null 的正确方向、rank-1 扰动界、三重重叠 gluing 语言、以及 threshold/environment 的 JSON 合同都已被明确写出。换句话说，**这个对象现在已经是“真的有限维线性代数对象”，不再只是包装语言**。但与此同时，它仍然留下几个不能装作没看见的硬缺口：若干“定理级”表述仍无证明或定义不够封闭；共同 ambient/invariant 仍是规则语句而非完整定理；随机子空间 note 里的解析 Beta 法则与 harness 实际统计量没有完全对齐；JSON threshold contract 已出现，但代码尚未完全由该 contract 驱动，因而还不是彻底 fail-closed。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:33-69,71-117,119-165,167-217,219-265,267-311；FORMAL_NOTE_V1_1_WORKPLAN_20260625.md:32-55,57-155,156-189；synthetic_harness_v1_1_20260625.json:6-68,78-268；debranded_residual_transport_harness_v1_1.py:23-82,89-94,741-791）

如果把用户要的“一页 verdict”压缩成一句话，那就是：**数学项目保留；Formal v1.1 可接受，但只能作为 patch，不足以视为封口版 formal system；Mode B MaoField 经验地位一律不升级。** 这也与 bundle 自己的边界一致，而不是我额外加戏。 （包内证据：00-README_FOR_142_AND_PRO.md:62-90；FORMAL_RESIDUAL_TRANSPORT_V1_STRICT_AUDIT_ADOPTION_NOTE_20260625.md:63-99,100-118；STATE.md:22-29）

## Formal Note v1.1 的证明审计

先说通过项。**Proposition 1 的 quotient descent 命题是对的。** “`C` 在商空间上良定义，当且仅当 `C(N_s) <= N_t`” 是标准线性代数命题，v1.1 还正确地区分了“商映射存在”与“正交余代表元在 `C` 下自然”的更强条件 `C P_s = P_t C`。这正好修复了 v1 把 residual representative 与 quotient language 混在一起的缺口。形式上唯一想补的，只是把命题明确地嵌回带权 Hilbert 语境，或者显式说明“本命题纯代数，与权无关”，这样记号层面会更平滑。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:33-69；FORMAL_NOTE_V1_1_WORKPLAN_20260625.md:41-55）

**Proposition 2 的 projection-evolution commutator 判据也是对的。** 在有限维带权 Hilbert 空间里，`PT=TP` 与 “`T` 同时保持 `N` 和 `N^{\perp,w}`” 等价；再通过带权伴随把第二个不变性改写成 `T^{*,w}(N) <= N` 也是成立的。v1.1 终于把 v1 缺失的 operator theme 补成了明确命题，这一点是实质修补，不是润色。小问题有两个：其一，证明里第 113 行写成了 `N^perp`，而上下文一直使用 `N^{perp,w}`，这是记号不严；其二，它没有把带权伴随的具体公式再写一遍，虽然在 finite-dimensional 语境里不难补。问题都不致命，但仍值得在 v1.2 收口。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:71-117；FORMAL_RESIDUAL_TRANSPORT_V1_STRICT_AUDIT_ADOPTION_NOTE_20260625.md:47-59,82-99）

**Square holonomy decomposition 的公式本身是精确成立的。** 只要定义 `Delta_p = Chat_p - P_t C_p P_s`，那么插入并减去 `P_t C_p P_s` 与 `P_t C_q P_s` 就得到
`Omega_{p,q} = P_t(C_p-C_q)P_s + Delta_p - Delta_q`。这个身份非常重要，因为它把“raw path mismatch”与“投影/transport 非自然性”分开了；v1 的 square no-go 只是在这三个项全为零时的特例。这里我仍然不给满分，原因不是公式错，而是 **分解的诊断粒度还不够细**：workplan 写的是想把 holonomy 进一步拆成 raw mismatch、transported edge defects、endpoint projection effects；v1.1 给出的却是路径级 `Delta_p` / `Delta_q`，不是望远镜式的逐边 defect 展开。所以它修复了“有没有分解”的问题，但还没修到“最可审计的逐边分解”层级。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:119-144；FORMAL_NOTE_V1_1_WORKPLAN_20260625.md:82-92）

**共同 ambient 空间章节是正确的修辞收缩，但还不是完整 invariant theory。** 它终于承认不同顶点的 residual vectors 默认不在同一向量空间里，因此在谈 singular values、principal angles、stack spectra、holonomy norms 前，必须先注册一个共同 ambient：基点 transport、带权直和、或者公共坐标空间都可以。这一步是必要修复，因为 v1 确实在“先有 invariant 还是先有共同空间”这件事上说得过快。但 v1.1 仍然只是“先决条件说明”，而不是定理：它没有给 principal angles 的定义，没有给 transported stack 的构造定理，也没有证明不同注册方案下哪些量是等价的、哪些只是选择依赖的 diagnostics。也就是说，**语言边界被修对了，但“invariant”两字仍未完全封口。** （包内证据：FORMAL_NOTE_V1_1_20260625.md:146-165；FORMAL_NOTE_V1_20260625.md:269-301；FORMAL_NOTE_V1_1_WORKPLAN_20260625.md:93-105）

**随机子空间 null 的方向是对的，但 formal note 与 harness 之间还差一层闭合。** 数学上，在 whitening 后的 `R^d` 中，对固定单位向量 `u` 和 Haar-uniform 的随机 `k`-平面 `S`，平方捕获量 `||Pi_S u||^2` 服从 `Beta(k/2,(d-k)/2)`，这条陈述在一般位置下是标准的。v1.1 把它写进 note，是对的；同时 note 也克制地说：harness 可以继续用 Monte Carlo quantile，但必须记录 `d`、`k`、draws、discarded draws、calibration statistic、threshold。问题在于，当前 harness 的 `weighted_projection_energy` 实际计算的是 **范数比**，不是平方捕获量；random-subspace block 的经验阈值比较也是在这个 unsquared statistic 上进行，而 JSON 文字又同时记了 Beta law。换言之，**解析 null 是对的，但它没有被当前 harness 以同一统计量直接校准。** 这不至于推翻 v1.1，却足以阻止我把这部分称为“完全封闭”。此外，formal note 对 `k=0`、`k=d` 等退化端点也没有单独声明。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:167-193；debranded_residual_transport_harness_v1_1.py:237-243,540-588；synthetic_harness_v1_1_20260625.json:196-217）

**Rank-1 shadow perturbation 部分是 v1.1 最干净的修补之一。** `M = a v^T + E` 时，由 Weyl 型奇异值不等式得到 `sigma_2(M) <= ||E||_2`，这正是 v1 审计要求的“近 rank-1 阴影”定量版本。更重要的是，v1.1 没有把 `sigma_2/sigma_1 >= 0.25` 伪装成数学常数，而继续老老实实称它为 source-fixed review floor。这种节制是对的。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:195-217；FORMAL_NOTE_V1_1_WORKPLAN_20260625.md:117-127）

**Finite gluing complex 的写法也是对的，而且比 v1 收敛。** 它明确说 pairwise absorption 不是完整 sheaf obstruction，想谈 obstruction 就要显式做 triple-overlap / cocycle 检查。这正中上一轮审计要害。我要指出的弱点不是数学错误，而是层级：这一节仍然是“有限 overlap 语言”和“toy residual cycle”规则，不是 sheaf 定理，也没有把 charts、transition maps、residualization operators 组成一个严格对象。所以它完成的是 **限制误用**，不是建立完整 gluing 理论。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:219-244；FORMAL_NOTE_V1_1_WORKPLAN_20260625.md:129-141）

**Product-weight boundary 方向正确，但 theorem 还欠证。** v1.1 在第 8 节写出：若权恰为 product 形式，且 nuisance 是常数加各轴 main effects 的加性子空间，那么带权 residual 与 product-measure Hoeffding 交互项一致；若观察权不是 product，则对象只能叫 non-product weighted projection residual，而不是 product-measure Hoeffding。这一判断方向正确，而且与 v1 保留下来的 `2×2` 反例完全同向。但严格审计里我仍然要扣分：这一节没有给出该“正向等价定理”的明确定义与证明，甚至没有在 note 内部形式化定义 “Hoeffding interaction component”。所以目前它更像一个**正确但未证明完成**的 theorem stub。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:245-265；FORMAL_NOTE_V1_20260625.md:369-433；FORMAL_NOTE_V1_1_WORKPLAN_20260625.md:143-155）

## 与上一轮严格审计的差距对照

下面给出 report(26) 九个缺口的逐项结论。这里的“已修复”只表示 **相较 v1 的缺项已被补上到可审计程度**，不等于“再无 v1.2 义务”。

| 缺口主题 | 本次判断 | 审计说明 |
|---|---|---|
| quotient descent | 已修复 | v1.1 新增明确命题，并与 residual representative naturality 分开；这是对 v1 缺口的直接修复，但暂时没有独立 harness block。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:33-69；FORMAL_NOTE_V1_1_WORKPLAN_20260625.md:41-55；debranded_residual_transport_harness_v1_1.py:741-757） |
| projection-evolution commutator | 已修复 | v1.1 增补了 `PT=TP` 的等价判据与 weighted-adjoint 形式；harness 也新增 standalone commutator control。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:71-117；SYNTHETIC_HARNESS_V1_1_20260625.md:24-39；synthetic_harness_v1_1_20260625.json:146-158；debranded_residual_transport_harness_v1_1.py:292-327,741-749） |
| square holonomy decomposition | 大体修复 | 路径级精确分解已给出，且 harness 区分了 raw-path-equal square control 与 non-naturality trap；但还没有逐边 defect 的望远镜展开。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:119-144；FORMAL_NOTE_V1_1_WORKPLAN_20260625.md:82-92；synthetic_harness_v1_1_20260625.json:159-173；debranded_residual_transport_harness_v1_1.py:439-507） |
| common ambient invariants | 部分修复 | “先注册 ambient，再谈谱/角/范数”这一语言边界修好了；但还没有完整 invariant 定义与证明。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:146-165；FORMAL_NOTE_V1_20260625.md:269-301） |
| analytic random-subspace null | 部分修复 | formal note 写出了正确方向的 Beta null，并要求记录 `d,k,draws,discarded,statistic,threshold`；harness 也记了这些信息，但实际统计量用的是范数比而非平方捕获量，因此解析 law 与代码统计量尚未完全闭合。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:167-193；synthetic_harness_v1_1_20260625.json:196-217；debranded_residual_transport_harness_v1_1.py:237-243,540-588） |
| rank perturbation | 已修复 | v1.1 给出 `sigma_2(M) <= ||E||_2`，同时保持 `0.25` 只是 review floor。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:195-217；FORMAL_NOTE_V1_1_WORKPLAN_20260625.md:117-127） |
| triple-overlap gluing | 已修复 | formal note 明确把三重重叠/cocycle 检查写进 gluing language，harness 也补了 triple-overlap toy block。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:219-244；SYNTHETIC_HARNESS_V1_1_20260625.md:24-39；synthetic_harness_v1_1_20260625.json:255-267；debranded_residual_transport_harness_v1_1.py:701-738,741-757） |
| product-weight equivalence | 部分修复 | 边界写对了：exact product 才能合法讲产品测度 Hoeffding；non-product 仍属另一几何。可惜正向 theorem 仍未在 note 内部证明完成。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:245-265；FORMAL_NOTE_V1_20260625.md:369-433；FORMAL_NOTE_V1_1_WORKPLAN_20260625.md:143-155） |
| JSON threshold / environment contract | 部分修复 | v1.1 的 JSON 确实新加了 `threshold_contract` 与 `environment`；但代码里不少 block 仍把阈值硬编码在 pass 逻辑里，没有完全由该 contract 驱动，所以还不算“彻底 fail-closed”。 （包内证据：synthetic_harness_v1_1_20260625.json:6-68；debranded_residual_transport_harness_v1_1.py:25-82,89-94,278-289,313-324,566-587,661-678,725-737；debranded_residual_transport_harness_v1_1.py:340-358,361-385,388-402,416-436,476-485,488-507,510-537,602-632,682-698） |

综合这一张表，合理结论不是“v1.1 没修”，也不是“v1.1 已全修完”。更准确的说法是：**它把 v1 的核心漏洞大多修到可继续审计的层级，但至少还有四个点只修到一半——共同 ambient invariants、analytic null 与 harness 的统计闭合、product-weight 正向 theorem 的证明、以及 threshold contract 的真正 fail-closed 化。** （包内证据：FORMAL_NOTE_V1_1_20260625.md:146-165,167-193,245-265,267-311；synthetic_harness_v1_1_20260625.json:6-68,196-217；debranded_residual_transport_harness_v1_1.py:25-82,237-243,540-588）

## Harness v1.1 审计

先说 **这 14 个 toy controls 真正证明了什么**。它们证明的是：这套定义可以被编码成一个零 GPU、synthetic-only、带 JSON 输出的有限维测试台；在这个测试台里，产品权等价、非产品分离、后验 nuisance 失效、好边/坏边、commutator leakage、raw-equal square closure、coarsening trap、rank-1 shadow、random-subspace null、random axes、shuffle null、pairwise gluing absorption、triple-overlap cocycle 等设计情形都能被脚本稳定地区分。换句话说，**它证明的是“定义与玩具合同可执行”，而不是任何 MaoField 经验对象已被观测到。** 这不是我额外降级，而是 harness summary、JSON boundary、以及 script 返回对象里明牌写着的边界。 （包内证据：SYNTHETIC_HARNESS_V1_1_20260625.md:5-16,24-45,81-104；synthetic_harness_v1_1_20260625.json:69-77,78-268,269-284；debranded_residual_transport_harness_v1_1.py:741-791）

再说 **它没有证明什么**。它没有证明 quotient descent 在真实复杂数据流上稳健；没有证明共同 ambient invariants 已被正式注册；没有证明 Beta law 已被同一统计量严格校准；没有证明 `sigma_2(M) <= ||E||_2` 的 perturbation bound 已有独立数值单测；更没有证明任何 MaoField residual / interaction / transport / holonomy field 被观测到。尤其是最后一点，bundle 从 README 到 STATE 到 harness JSON 都要求你别说这种话。 （包内证据：00-README_FOR_142_AND_PRO.md:14-41,87-90；STATE.md:22-29；FORMAL_NOTE_V1_1_20260625.md:287-294；synthetic_harness_v1_1_20260625.json:69-77,271-284；debranded_residual_transport_harness_v1_1.py:765-790）

这套 harness 里有几块是 **必要但偏容易的控件**。`transport_stable_multidirectional_positive_control` 把 coarse toy pattern 直接 repeat 到 fine 网格，再用与之匹配的 coarsening 和 additive nuisance 去检验，因此它证明的是“代码能保留手工种下的、多方向的 source-fixed 结构”，而不是“任意合理结构都能 survive”；`raw_path_equality_square_control` 选择的是 raw path 本来就相等的 square，因此它的近零 holonomy 更像 sanity check；`equal_cell_count_random_axes` 和 `within_axis_shuffle_null_distribution` 也都让 named direction 与 signal 高度同源，故 pass 本身可预期。它们都不是坏控件，但都属于**验证 harness 通路有效**，不是强对抗性证据。 （包内证据：debranded_residual_transport_harness_v1_1.py:405-436,439-485,591-632,635-679；SYNTHETIC_HARNESS_V1_1_20260625.md:24-39,81-88）

有两处我必须明确点名。第一，**`product_reweighting_separation` 带有一致性-而非独立性 检查的味道**：它直接把 v1 formal note 给出的反例常数抄进脚本，当输出与 note 中已知数值吻合时判定通过，因此它证明的是“脚本实现复现了 note 里的例子”，而不是“一个独立于 note 的新推导成立”。这对 regression test 是合理的，但不能当作额外数学证据。第二，**threshold contract 还没有真正 fail-closed**：JSON 顶层确实记录了 `threshold_contract`，而部分 block 也会从 `THRESHOLDS` 读取阈值；但不少 pass 逻辑仍直接写死数值常量，等于把“合同”和“执行”各写了一份。如果未来有人只改 JSON 不改 if 条件，artifact 仍可能“看上去有合同”，却没有真正受合同约束。对严格审计来说，这不是小事。 （包内证据：FORMAL_NOTE_V1_20260625.md:387-433；debranded_residual_transport_harness_v1_1.py:25-82,361-385；synthetic_harness_v1_1_20260625.json:11-68,86-112；debranded_residual_transport_harness_v1_1.py:340-358,388-402,416-436,476-485,488-507,510-537,602-632,682-698）

最需要 v1.2 修的 harness 细节，是 **随机子空间部分的统计闭合**。formal note 声称解析 law 针对 `||Pi_S u||^2`；但 `weighted_projection_energy` 返回的是 `||Pi_S u|| / ||u||`，random-subspace block 比较的也是这个 norm ratio 的 Monte Carlo 分位数。这样写当然还能当设计门槛，但它不能直接说“我们已把 Beta null 落成代码合同”。必须二选一：要么脚本改成平方统计量并与 Beta 量化对齐；要么 note 改口，明确解析 law 是理论参考，而当前 harness 用的是经单调变换后的 Monte Carlo statistic。现在这两句话混写，严格上不够封口。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:167-193；debranded_residual_transport_harness_v1_1.py:237-243,540-588；synthetic_harness_v1_1_20260625.json:196-217）

最后，v1.1 比 v1 的 harness 确实有可见进步：v1 只有 11 块，缺 standalone bad-edge、standalone commutator、triple-overlap、shuffle null distribution、threshold/environment contract；v1.1 则增到了 14 块，并把 threshold/environment 提升进 JSON。这一点应该记功，但不能多记。 （包内证据：SYNTHETIC_HARNESS_V1_20260625.md:24-36；synthetic_harness_v1_20260625.json:1-165；debranded_residual_transport_harness_v1.py:521-566；SYNTHETIC_HARNESS_V1_1_20260625.md:24-39；synthetic_harness_v1_1_20260625.json:1-285；debranded_residual_transport_harness_v1_1.py:741-791）

## 最小 v1.2 补丁计划

v1.2 不需要搞“大研究计划”；它需要的是 **最小而硬** 的收口。

第一，formal note 只加三块硬证明即可：给 random-subspace Beta law 一个两三段的正式证明草图，并显式写出适用域 `0<k<d`；给 product-weight 正向 theorem 补上“Hoeffding interaction component”的精确定义与证明；把 square holonomy 的路径级 `Delta_p` 分解再推进一步，给出逐边 defect 的 telescoping 公式，哪怕只在最基本路径记号下陈述也行。这样做能把目前最像“正确口号”的三段变成真正 theorem text。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:119-144,167-193,245-265；FORMAL_NOTE_V1_1_WORKPLAN_20260625.md:82-92,107-127,143-155）

第二，common ambient 一节要从“警告语”升级为“定义语”。v1.2 只需固定一种最小注册法，例如“选一个 base vertex，把其余顶点 residual transport 到该基点”，然后在这个框架内真正定义 residual stack、principal angles、edge-defect norm、square-holonomy norm，顺手注明这些量对注册 choice 的依赖/不依赖边界。没有这一步，就不要再把这些量叫 invariants；叫 registered diagnostics 更诚实。 （包内证据：FORMAL_NOTE_V1_1_20260625.md:146-165；FORMAL_NOTE_V1_1_WORKPLAN_20260625.md:93-105）

第三，harness 只要补四个自测就够了：一个 quotient descent toy block；一个 common-ambient registration block；一个数值化的 `sigma_2(M) <= ||E||_2` perturbation test；一个 squared-capture vs Beta quantile calibration block。尤其是最后一个，必须让 note 的解析 null 与 code 的统计量严格一致。 （包内证据：FORMAL_NOTE_V1_1_WORKPLAN_20260625.md:41-55,107-127,156-172；debranded_residual_transport_harness_v1_1.py:741-757）

第四，threshold contract 必须做成 **单一真相源**。最小改法很简单：所有 pass/fail 逻辑一律从 `THRESHOLDS[...]` 读取；然后再加一个 meta-test，检查 JSON dumped 出来的阈值与运行时阈值完全一致。现在这种“合同写一份、if 条件再写一份”的状态，在普通工程里也许勉强可忍，在严格审计里不够。 （包内证据：debranded_residual_transport_harness_v1_1.py:25-82,278-289,313-324,566-587,661-678,725-737；debranded_residual_transport_harness_v1_1.py:340-358,361-385,388-402,416-436,476-485,488-507,510-537,602-632,682-698；synthetic_harness_v1_1_20260625.json:11-68）

## 禁止语句、通俗解释与最终分类

v1.1 之后，以下说法仍然必须一律判死。经验层面，不得说：full panel 已跑、16-cell full-panel aggregate 已存在、MaoField residual / interaction / quotient-residual / transport / holonomy field 已观测到、glass box broken、LOSO passed、F3 positive、checkpoint loading 做过、model inference 做过、training 已授权、new loss 已授权。数学层面，也不得说：v1.1 已完成完整 invariant theory、已完成完整 gluing/sheaf obstruction theorem、已把解析 random-subspace null 与 harness 完全闭合、已把 product-weight 正向 theorem 在 note 内部证明完毕、或已把 threshold contract 做成真正 fail-closed。前一组是 bundle 明文禁止；后一组是本次审计根据文本与代码结构得出的“仍然禁止夸口”。 （包内证据：00-README_FOR_142_AND_PRO.md:16-41；GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_1_AUDIT_PROMPT_20260625.md:63-89；FORMAL_RESIDUAL_TRANSPORT_V1_STRICT_AUDIT_ADOPTION_NOTE_20260625.md:100-118；FORMAL_NOTE_V1_1_20260625.md:164-165,219-244,245-265,287-294；synthetic_harness_v1_1_20260625.json:69-77,271-284；debranded_residual_transport_harness_v1_1.py:765-790）

如果用初中生能懂的话来解释：**是的，v1.1 现在已经定义出了一个真的数学对象。** 这个对象大概就是：“在有限个格子上放一个带权重的数据表；先把你事先登记好的‘无关部分’投影掉；再看剩下的部分在不同粗细尺度之间怎么传输、哪里不相容、绕方块一圈会不会出现差异。” 这是真的线性代数，不是空话。**但它仍然只是一个还没封口的讲义版对象。** 原因不是对象不存在，而是几条最重要的“高级论断”——哪些量真能叫 invariant、随机子空间 null 怎样与代码完全对齐、product-weight 正向 theorem 怎样严格证明——还没彻底打磨好。玩具 harness 的成功，也只说明“小实验台跑得通”，不说明 MaoField 已看到这种结构。 （包内证据：DEBRANDED_RESIDUAL_TRANSPORT_CORE_DESCRIPTION_20260624.md:36-52,69-105,123-135；FORMAL_NOTE_V1_1_20260625.md:33-69,71-144,146-165,167-217,219-311；SYNTHETIC_HARNESS_V1_1_20260625.md:81-104）

最终分类我给：

**accept_with_v1_2_required**

并且无论这个分类如何，Mode B 的 MaoField 经验状态都必须保持：

**insufficient_artifact** （包内证据：00-README_FOR_142_AND_PRO.md:87-90；GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_1_AUDIT_PROMPT_20260625.md:86-89；STATE.md:24-29）