# MaoField 路径闭合研究结果修订稿

## 修订后的总裁决

本次按“ZIP 仓库事实 + MAOFIELD 紧凑提示词 + 旧版深度研究报告 + 新增二轮增量提示词”重新整理后的结论仍然是：**主裁决保留为 `PATCH_DEFINITIONS_THEN_RECHECK`**。理由不是方向错误，而是对象已经足够窄、足以成为一个 bounded formal note，但还没有把 chart、path、cycle、transport、restriction、operator norm 与路径缺陷合成律写成一个完全类型一致的有限维线性代数对象；在这一步完成之前，不宜把它上升为完整 formal note，更不宜放大成黑箱机制理论、经验性正结果或 NMI-ready 叙述。紧凑提示词明确要求把 v1.6 quantitative OI 保持为有限二向表上的局部数学结果，并把“同一性不是命名，而是物质关系中的路径闭合”只当作 programme framing；旧报告也已把当前最稳妥的 verdict 定为“先补定义，再复核”。fileciteturn0file0 fileciteturn0file1

与旧稿相比，这次修订最重要的增量有两点。第一，我把“辩证唯物主义定位 pass”前置化了：validity、benchmark sensitivity、calibration、referential security、rubric drift、model collapse 都不再只作为“相邻领域”，而被当作**相邻矛盾**来处理，再从中抽出 MaoField 当前要抓住的**主要矛盾**。第二，我把“ distinct contribution ”收得更窄：它不再被表述为任何宽泛的 benchmark critique，而是被收束为**finite metric-object identity audit**，也就是“声明 chart operators 与 declared transports 后，检查 path closure / intertwining，输出 exact defect certificates，并研究 finite cycle-iteration defect propagation”的那一小块。这个收束既符合 ZIP 里的边界，也更能避开现有文献的高重叠区。fileciteturn0file0 fileciteturn0file1 citeturn0academia0turn3academia1turn1academia0turn1academia1turn5academia2

## 仓库数学骨架的再审查

就当前 ZIP 所承载的数学骨架而言，最稳的链条仍然是：v1.3 finite order-defect spine，D706 OI zero/nonzero corollary，D707 v1.6 quantitative OI，然后才轮到 programme-level 的 path-closure 方向。紧凑提示词要求完整保留的 chain 也正是这一条：最初预印本中的 metric-object identity obstruction，压缩为 finite order-defect / OI，再压缩为 quantitative OI，之后才过渡到“同一性不是命名，而是物质关系中的路径闭合”、cycle-iteration defect、black-box evaluation audit 与 NMI route。这里最关键的纪律，是始终区分四类对象：`THEOREM`、`SUPPORT_ARTIFACT`、`EMPIRICAL_HYPOTHESIS`、`PROGRAMME_FRAMING`；旧稿对这条纪律的重申是正确的，应当完整保留。fileciteturn0file0 fileciteturn0file1

v1.6 quantitative OI 仍然可以稳定保留，而且应当明确写成一个**有限正权二向表上的 two-projection commutator geometry companion note**。旧稿指出，当前对象仍然是同一个有限对象：`X=Q×B`、加权 Hilbert 空间 `L2(w)`、常数子空间 `C`、两条中心主效应空间 `A` 与 `B0`，以及 `D_w = P_B0 P_A - P_A P_B0` 的受限算子范数；公式 `OI^{op}_{N_add}(w)=max_j rho_j sqrt(1-rho_j^2)` 应继续被理解为两正交投影交换子范数的有限维专门化，而不是任何更广泛的 projection theory 或 dependent-input theory。旧稿还正确强调了四个需要在正式稿中写死的接口：零维边界、`rho=1` 公共块的排除或解释、`N_add` 限制的处理，以及“operator norm after input normalization ≠ one fixed witness output norm”的 normalization guard。fileciteturn0file1

因此，压缩后的 chain 最好重写成如下判断，而不是再写成长叙事：**v1.3／D706／D707 已经给出一个有限维 exact spine，它说明 evaluation-derived object 的同一性不能仅靠名字授权；若要跨 chart 认作同一对象，就必须声明 transport，并检查 path closure / intertwining。** 这类表述与当代评测有效性文献的主轴是相容的，因为这些文献都在反复指出：分数、排名和 benchmark 表现不是自解释对象，真正决定其可解释性的，是 measurement target、aggregation、scope、sampling 与推断目标是否写清楚。Binette 与 Reiter 把这一点明确写进了 estimands 框架；construct validity 文献则要求 benchmark 与其声称的能力构念之间建立更强的理论与经验联系。MaoField 可以把这部分视为背景同向性，但不能把它据为独创。fileciteturn0file1 citeturn0academia0turn0academia1turn0academia2

## 路径闭合对象的最小形式化补丁

当前最需要修订的，不是哲学口号，而是定义接口。旧稿已经指出，programme brief 给出的雏形是正确的：对 chart `c` 给出 `H_c`、`O_c`、`Phi_c`，对 chart 之间的边给出 `U_{c→c'}` 与 `T_{c→c'}`，然后定义 edge defect `Delta_{c→c'} = T_{c→c'} Phi_c - Phi_{c'} U_{c→c'}`。但如果要把它真正抬升成 bounded formal note，这些定义至少还缺四块硬补丁：有限维赋范或 Hilbert 结构、一般路径的合成规则、restriction 与 operator norm 的明示约定、以及路径缺陷的组合引理。旧稿对这四个补丁的诊断是准确的，这次修订保留这一结论。fileciteturn0file1

最小补丁可以写成如下形式。对每个 chart `c`，明言 `H_c` 与 `O_c` 是有限维实 Hilbert 空间，`Phi_c: H_c → O_c` 是线性算子。对每条边 `c→c'`，明言 `U_{c→c'}: H_c → H_{c'}` 与 `T_{c→c'}: O_c → O_{c'}` 是线性算子。然后不先从 cycle 入手，而是先对任意可合成路径 `alpha: c_0→c_1→…→c_k` 定义 `U_alpha` 与 `T_alpha` 的复合，并规定空路径有恒等元。这样就能统一定义一般路径缺陷 `Delta_alpha = T_alpha Phi_{c_0} - Phi_{c_k} U_alpha : H_{c_0}→O_{c_k}`；cycle defect 只是 `c_k=c_0` 的特例。`CID_gamma(S)` 与 `CIC_N(gamma,S)` 只需要求 `S⊆H_{c_0}` 是有限维子空间，并明确使用由域与陪域诱导的 operator norm；不必过早假定 `S` 对 `U_gamma` 不变，除非后续需要更强的增长界。这个补丁很小，但它把 programme brief 从“正确方向”推进到“可审数学对象”。fileciteturn0file1

在这套补丁加上之后，旧稿给出的 finite telescoping identity 是成立的，而且它恰好展示了为什么 cycle-iteration defect 仍然是一个**受控的有限维线性代数对象**，而不是动态塌缩大理论。设 `Delta_{gamma,n}=T_gamma^n Phi_{c_0}-Phi_{c_0}U_gamma^n`。只要先写出组合引理 `Delta_{beta∘alpha}=T_beta Delta_alpha + Delta_beta U_alpha`，就立刻得到递推式 `Delta_{gamma,n+1}=T_gamma Delta_{gamma,n}+\Delta_gamma U_gamma^n`，再由归纳得到  
`Delta_{gamma,n} = Σ_{j=0}^{n-1} T_gamma^{n-1-j} Delta_gamma U_gamma^j`。  
于是，一旦 `Delta_gamma=0`，全部迭代都闭合；若 `Delta_gamma≠0`，则在显式范数假设下可以得到有限视窗的增长上界，例如在 `||T_gamma||≤a`、`||U_gamma||≤b` 时给出几何或线性型的粗界。这里真正新增的对象不是“collapse”，而是**finite cycle defect propagation under declared transports**。fileciteturn0file1

因此，修订版 md 里应把这一节的对象分类改写得更硬一些：finite order-defect 与 OI 是 theorem / corollary，quantitative OI 是 theorem，`路径闭合` 这句话是 programme framing，cycle-iteration defect 在补完定义与 telescoping proof 后才是 theorem candidate，black-box evaluation audit 仍只是 method schema，NMI route 只能是 gate-based roadmap。紧凑提示词本身就要求维持这种分类，且明确禁止把 harness、JSON、经验结果与哲学 framing 误写成证明权威。fileciteturn0file0 fileciteturn0file1

## 辩证唯物主义定位与主要矛盾

加入“辩证唯物主义定位 pass”之后，最有用的做法不是把 MaoField 说成这些领域的总和，而是把它们看成一组**相邻矛盾**。在这个意义上，construct validity 与 estimands 处理的是“你到底在测什么、你的推断目标是否被正确定义”的矛盾；benchmark sensitivity 处理的是“不同 benchmark、不同任务采样和不同表述会不会让相对优劣翻盘”的矛盾；IRT calibration 处理的是“不同题集、不同时间、不同样本之间如何保持可比性”的矛盾；referential security 处理的是“同名模型是否仍然是同一可识别对象”的矛盾；rubric drift 与 judge bias 处理的是“评判者与评判规则是否在不显眼地漂移”的矛盾；model collapse 处理的是“递归训练或迭代生成是否会丢失尾部分布并造成退化”的矛盾。相关工作分别从不同侧面把这些矛盾对象化了。citeturn0academia0turn3academia1turn3academia0turn1academia0turn1academia1turn1academia3turn5academia2turn5academia1turn5academia0

在这组相邻矛盾中，MaoField 现在最应该自觉承认并抓住的**主要矛盾**是：**metric-object identity is unlicensed unless declared transport and path-closure hold**。也就是说，构念、benchmark、judge、rubric、model name、甚至 calibration 本身都不自动授予“同一对象”资格；只有当 chart operations 与 raw/object transports 被显式声明，并且对应的 intertwining 或 path closure 成立时，“这是同一 metric object”这一断言才被授权。这个主矛盾比一般的有效性批评更窄，也比 referential security 更聚焦于“evaluation-produced object”而非“served model artifact”本身。fileciteturn0file0 fileciteturn0file1 citeturn1academia0turn0academia0

分别来看，每个相邻领域都解决了某些关键问题，但也留下了 MaoField 想要补上的缺口。**Validity / construct validity / estimands** 告诉我们：不能把 benchmark 分数直接等同于能力，也不能在 measurement target 与 aggregation 未定义时谈稳健比较；但它们通常不会把“跨 chart 的 evaluation object 是否还是同一对象”写成一个带 `Phi`、`U`、`T` 与 `Delta` 的有限维缺陷 calculus。**Benchmark sensitivity / contamination** 告诉我们：换 benchmark、换样本、换 rephrase 之后，排名和性能判断都可能改变；但它们仍然更偏向“脆弱性诊断”，而不是“对象同一性授权”的显式数学证书。citeturn0academia0turn0academia1turn0academia2turn3academia1turn2academia1turn4academia0

**IRT calibration** 的优势，是把 item difficulty、discrimination、anchor items、固定参数校准与可比性维护做得更精细。ATLAS 展示了 IRT 排名与普通 accuracy 排名可能显著不同，Growing Pains 进一步用固定参数与锚题处理跨时间 benchmark 扩展的 comparability；这些都是高价值工作。但它们主要解决的是“标度对齐”和“跨测试可比较性”，并未自然给出“chart operator 与 transport 已声明时，何处 failure，failure 的 exact defect certificate 是什么”这一级对象。**Judge / rubric drift** 则说明，哪怕 benchmark 验证通过，judge 依然可能存在位置偏置、任务偏置或因 rubric 改写而发生 stealthy preference drift；但这些工作通常输出的是 bias diagnosis 与 drift evidence，而不是一个一般性 path-closure calculus。citeturn3academia0turn1academia2turn1academia3turn1academia1

**Referential security** 与 MaoField 的邻近性最大，也因此是先行艺术风险最高的一块。它已经明确提出：公开名称不变，并不保证底层权重、提示、检索、服务栈等保持不变；因此 model identity 本身需要能被验证，而不是被默认。MaoField 若要继续，就必须正面承认这一近邻，而不能通过无视它来论证新颖性。MaoField 真正剩下的空间，不在“同一性不是命名”这句口号本身，而在于把**evaluation-derived metric object** 的同一性，收缩为一个有限维 chart/transport/defect 对象。相对地，**model collapse** 文献研究的是递归训练或迭代生成引发的数据分布尾部丢失、信息畸变与性能退化；那是训练生态与生成链条中的动力学问题，并不等于已声明 chart 下的 finite cycle path defect。把 `CIC_N` 直接命名为“collapse theory”，既会和现有文献撞题，也会破坏当前 bounded note 的边界。citeturn1academia0turn5academia2turn5academia1turn5academia0

## 先行艺术风险与剩余贡献

这次修订后的 novelty 判断必须更严格。首先，**MaoField 不能靠“评测对象不是自解释的”“benchmark 会脆弱”“judge 会漂移”“同名模型未必同一”这些一般命题来立新**，因为这些命题分别已经被 estimands、construct validity、benchmark lottery、benchmark contamination、IRT calibration、referential security 与 rubric drift 文献处理过，而且其中不少工作给出的不是模糊提醒，而是成体系的方法论或实证框架。把这些已有成果统统降格为“背景”而不正面承认，会构成明显的先行艺术风险。citeturn0academia0turn3academia1turn2academia1turn3academia0turn1academia2turn1academia0turn1academia1

在承认这些重叠之后，MaoField 仍可能保住的剩余贡献，只剩下一个**非常窄而且必须精确定义**的对象：**finite metric-object identity audit**。它的最小核心不是一般性“评估反思”，而是五件事：声明有限 chart operator `Phi_c`，声明 raw/object transports `U` 与 `T`，把 identity 条件写成 intertwining / path closure，把 failure 写成 exact defect certificate `Delta`，再把 repeated loop 的传播写成有限视窗中的 `Delta_{gamma,n}` 与 `CIC_N`。在这个版本里，MaoField 既不声称自己取代 validity theory，也不声称自己解释黑箱机制，更不声称自己建立了任何 dynamic-collapse 大理论；它只是给这些现有议程补上一个“当 comparability 被主张时，如何输出有限 defect certificate”的局部 calculus。fileciteturn0file0 fileciteturn0file1 citeturn0academia0turn1academia0turn1academia1turn3academia0

从辩证唯物主义定位来看，这个对象之所以值得保留，不是因为它“证明了辩证法”，而是因为它把一句总纲压缩成了一个受控数学对象：**同一性不是抽象命名，而是在具体关系结构与实践路径下才能被授权的闭合性。** 这里“物质关系”在有限数学中对应的，不是宏大本体论，而是具体的权重结构、chart data、transport declaration 与 operator composition；“矛盾”对应的是不同 chart 或不同路径下对象认定不自动一致；“主要矛盾”则是同一性授权条件本身。只要把这点收窄，哲学 framing 就仍然有组织研究对象的作用；一旦把它抬高成“哲学证明数学”或“数学证明整个哲学 chain”，就会突破当前 ZIP 明确设下的边界。fileciteturn0file0 fileciteturn0file1

## 修订后的推进架构与下一步

多会话推进架构本身不需要大改，紧凑提示词给出的主框架仍然成立：一个 Codex 主会话做状态冻结与 claim hygiene，多个隔离 loop Codex 会话做窄任务，一个主 Pro 会话综合裁决，多个独立子 Pro 会话分别负责 finite math、implementation audit、empirical design、NMI framing 与 adversarial red-team。这个设计的价值在于把“证明”“工件”“方法”“过度叙述”拆开，最大限度减少单会话自我放大。旧稿对这一架构的采纳是合理的，应保留。fileciteturn0file0 fileciteturn0file1

但当前顺序应再强调一次：**不要直接推进 Loop 6 或 Loop 7，也不要讨论 NMI-ready。** 现在的正确顺序是先做 `Loop 0` 的 state freeze 与 forbidden-claims cleanup，再做 `Loop 3` 的 typed chart/path definition patch，随后做 `Loop 4` 的 cycle defect formal note 与 telescoping proof，之后把结果交给主 Pro 与子 Pro A/E 复核。只有在 `Phi`、`U`、`T`、`Delta_alpha`、`Delta_gamma`、`CID`、`CIC_N` 与组合引理全部类型闭合之后，metric-object audit schema 才值得进入 `Loop 5`；而 real black-box audit 至少应等到方法门与数学门都被明确通过之后才谈。紧凑提示词也明确要求，在四个 gate——math、method、empirical、reproducibility——全部通过前，不得宣称 NMI readiness。fileciteturn0file0 fileciteturn0file1

因此，修订版 md 最终应把“exact next action”写得更明确一些：**node36 现在最该实现的，不是新 empirical panel，也不是黑箱机制解释，而是一个 bounded typed note**。这个 note 的最小目标，是把 finite chart/path/cycle defect 的定义写死，把 path composition lemma 与 telescoping identity 证明完，把 `CIC_N` 的基本上界与额外假设分开写清，并把所有 forbidden upgrades 再贴一遍：不得声称 empirical-positive，不得把 JSON 或 harness 当证明，不得声称 observed transport / holonomy / gluing / collapse field，不得推进 dynamic-collapse 大理论，不得作 NMI-ready 过早声明。做到这一步以后，再复核，才是符合 ZIP 与新增增量提示词要求的修订路线。fileciteturn0file0 fileciteturn0file1