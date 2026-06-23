# MaoField q4 超立方体扩展严格数学审计

## 结论

我的结论是：**Allow zero-GPU audit only**。这不是保守用词，而是当前仓库证据的上界。当前 `main` 已经把 q4 的后续对象收紧为“加权 slope-orthogonal residual field”这一**待审计对象**，并且新增了 `Q_freq4 x B_tokenpos4` 的零 GPU 形式化预注册方案；但仓库同样明确写明：真实 q4 full panel **未运行**，训练**未授权**，新 loss **未授权**，强数学表述**仍 blocked**，而 hypercube 的最强状态仅是 `formal_prereg_only`。因此，超立方体扩展现在**不是已观察到的非标量现象**，也**不是可批准的 full-panel 科学对象**；它只是一个被约束得更清楚的、尚未获得识别资格的候选分析坐标系。fileciteturn1file0L18-L18 fileciteturn5file0L20-L36 fileciteturn5file0L59-L74 fileciteturn7file0L40-L55

更严厉地说，`Q_freq4 x B_tokenpos4` **目前没有解决识别问题**。它只做了三件事：第一，固定了一个 outcome-independent 的第二坐标轴 `token_pos`；第二，给出了 source-only cell weights；第三，预先声明了必须剔除的 nuisance subspace。除此之外，它并没有提供新的观察结果，也没有产生任何 full-panel 级别的 fold-local 证据。只要没有这类证据，超立方体只是在把四维 q4 向量扩成十六维 cell 向量；维数变大不等于对象更真。fileciteturn12file0L4-L9 fileciteturn12file0L171-L181 fileciteturn21file0L159-L177 fileciteturn21file0L352-L394

## 证据边界

本次审计**只使用 GitHub connector 读取私有仓库 `Wangziqi0/MaoField` 的 `main` 分支内容**。仓库是私有的，连接器可访问；因此没有任何理由诉诸 public GitHub 404、公开网页或记忆补全。仓库元数据确认该仓库为 private，默认分支为 `main`，且当前连接器拥有读写访问权限。fileciteturn1file0L18-L19

我实际读取了用户点名的全部核心文件，且**没有出现连接器失败**：`STATE.md`、`GPT55_PRO_RESEARCH_INDEX_20260622.md`、`docs/infra/gpt_deep_research/deep_research_q4_hypercube_extension_strict_math_audit_20260623.md`、`Q4_HYPERCUBE_EXTENSION_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md`、`docs/infra/math_turn_20260622/Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.md`、`docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md`、`scripts/build_hypercube_schema_20260623.py`、`scripts/q4_hypercube_zero_gpu_audit.py`、`scripts/q4_full_panel_foldlocal_analysis.py`、`experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py`。为重建当前 q4 对象，我还读取了 `Q4_RESIDUAL_FIELD_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md`、`deep_research_q4_residual_field_strict_math_audit_20260623.md`、`docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md`、`docs/infra/gpt_deep_research/MATH_TURN_FRAMEWORK_ADOPTION_NOTE_20260622.md`、`scripts/math_turn_loso_audit.py`、`docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` 与 `docs/infra/math_turn_20260622/hypercube_schema_q4_tokenpos4_20260623.json`。fileciteturn1file0L24-L29 fileciteturn2file0L81-L120 fileciteturn3file0L15-L18

证据类别必须分开。仓库中最强的一级证据是：代码、JSON/JSONL、manifest、runbook、状态文件和脚本明文；deep-research 报告与 adoption note 只能作为 claim-source 或 design constraints，不是“现象已经成立”的证据。仓库自身在 `EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md` 与研究索引里就是这样规定的。fileciteturn10file0L11-L25 fileciteturn2file0L64-L71

按这个边界，当前可以当作**仓库事实**的内容包括：q4 的锁定 schema、generator 的 smoke/full-panel-dry-run/approval-token 边界、未来 q4 residual-field 分析脚本、以及 hypercube 的 zero-GPU prereg schema 与 feasibility audit。不能当作仓库事实的内容包括：“hypercube residual 已被观察到”“full panel 已运行”“强数学 claim 已授权”“training/new loss 已授权”。这些都被状态文件、adoption notes 与零 GPU 审计明确阻断。fileciteturn20file0L14-L27 fileciteturn7file0L88-L101 fileciteturn6file0L10-L20 fileciteturn5file0L59-L74

## 当前 q4 对象重建

当前 q4 的样本单位不是 token，也不是整个 fold，而是**一个 panel 行** \(i=(s,g)\)：固定 checkpoint root 下某个 `seed` 与某个 `generation` 的组合。runbook 将 panel scope 锁定为 seeds `[1,2,3,4,42]` 与 generations `0..9`，而未来 q4 full-panel 分析脚本也要求恰好 50 行并检查这组笛卡尔积是否完整。fileciteturn20file0L127-L142 fileciteturn14file0L27-L31 fileciteturn14file0L177-L201

在每个样本单位 \(i\) 上，当前观测向量是
\[
k_i=(k_{i0},k_{i1},k_{i2},k_{i3})\in\mathbb R^4,
\]
其中 \(k_{ij}\) 是第 \(j\) 个 q4 slice 上的 `mean_logprob`。这不是解释，而是 generator 的直接输出：`aggregate_smoke()` 对四个 slice 分别计算 `mean_logprob`，写入 `slice_rows`，并把 `k_value_type` 明确标成 `target_logprob_mean`。相应的 q4 schema 也锁死了 `edges=[2,10,73]` 与 `bin_sizes=[1374,2581,2020,2089]`。fileciteturn20file0L77-L108 fileciteturn16file0L170-L180 fileciteturn17file0L14-L36

令 \(n=(1374,2581,2020,2089)\)，则权重为
\[
w_j=\frac{n_j}{\sum_{\ell=0}^{3} n_\ell},
\qquad
\langle x,y\rangle_w=\sum_{j=0}^{3} w_j x_j y_j.
\]
当前均值模为
\[
D_i=\langle \mathbf 1,k_i\rangle_w,
\]
均值去除向量为
\[
u_i=k_i-D_i\mathbf 1.
\]
这正是 runbook 的明文定义，也是 `weighted_projection()` 的实现方式：先算 `d_value = sum(weights * k)`，再做 `u = k - d_value`。fileciteturn20file0L97-L108 fileciteturn16file0L310-L325

当前主方向是锁定的 q4 ordered frequency slope。先取
\[
v_{\mathrm{raw}}=(-1.5,-0.5,0.5,1.5),
\]
再做 weighted-center 与 unit-normalize，得到 \(v\)。当前 generator 只显式产出一个主标量
\[
P_i=\langle v,u_i\rangle_w.
\]
因此，就**已观察到并已输出的对象**而言，当前 q4 主载体仍然是三元组 \((D_i,u_i,P_i)\)，而其中最强诊断载体仍是标量 \(P_i\)。这点在 runbook 中被写得非常直白：**“No other projection can trigger the strongest verdict.”** fileciteturn20file0L97-L108 fileciteturn16file0L310-L325

当前仓库对“真正想审计的对象”已经给出更严格的后续定义。q4 residual-field adoption note 和后续分析脚本都将对象写成
\[
r_i=u_i-\langle v,u_i\rangle_w v,
\]
并且额外要求一个更严格的 fold-local scalar-slope residual：用非 held-out seeds 上拟合的 \(\alpha(D,g,g^2)\) 去消去 \(v\) 方向，而不是用全局观测后的 \(\langle v,u_i\rangle_w\) 直接消去。在线性代数上，q4 的 ambient 维度为 4，去掉常数模后是 3 维，再去掉 slope 方向后残差子空间是 2 维。仓库代码确实实现了这一 q4 后续分析门：它检查 projection geometry、fold-local residualization、matched-mean、rank/noise 以及 random mean-null projection multiplicity guard。fileciteturn8file0L21-L33 fileciteturn14file0L4-L13 fileciteturn14file0L225-L249 fileciteturn15file0L20-L26 fileciteturn15file0L125-L172 fileciteturn15file0L191-L231

但必须把“已实现”和“已观测”分开。`scripts/q4_full_panel_foldlocal_analysis.py` **只分析未来的 q4 full-panel aggregate**；它不产生 full panel，也不读取 checkpoint，更不会授权训练。相反，它首先要求恰好 50 行 q4 aggregate 输入，并明确拒收老的 rare/freq aggregate。也就是说：**q4 residual-field analysis path 已实现，q4 residual-field phenomenon 仍未被观察到。** 这是工程状态，不是正结果。fileciteturn14file0L4-L13 fileciteturn14file0L130-L174 fileciteturn14file0L177-L201 fileciteturn7file0L15-L24

相对地，`scripts/math_turn_loso_audit.py` 只是**旧 high-order aggregate 的 legacy audit**。它对 `F1_var`、`F1_tail`、`F3_slice_gap` 这些旧标量做 LOSO、matched-mean 和一个两切片 placeholder 式 rank audit；而且它在文件头与函数 `reject_q4_panel_input()` 中都明确说：如果输入看起来像 q4 panel aggregate，就应该改用 `scripts/q4_full_panel_foldlocal_analysis.py`。因此，旧 LOSO 脚本**不能**为任何 q4 residual-field 或 hypercube residual-field 兜底背书。fileciteturn19file0L4-L13 fileciteturn19file0L167-L193 fileciteturn19file0L196-L207

## 超立方体候选定义

当前仓库为 hypercube extension 预注册的最小候选是
\[
C=Q_{\mathrm{freq4}}\times B_{\mathrm{tokenpos4}},
\]
其中 \(Q_{\mathrm{freq4}}=\{0,1,2,3\}\) 继承锁定的 q4 frequency slice，而 \(B_{\mathrm{tokenpos4}}=\{0,1,2,3\}\) 来自 `token_pos` 的 source-only coarse binning：分别对应 token positions `1..16`、`17..32`、`33..48`、`49..63`。这一候选既写在超立方体 adoption note 中，也写进了 `build_hypercube_schema_20260623.py` 与生成出来的 schema JSON。fileciteturn5file0L24-L36 fileciteturn12file0L190-L214 fileciteturn21file0L159-L203

因此，若未来有一个真实的 full-panel hypercube aggregate，则每个样本单位 \(i=(s,g)\) 的观测对象应定义为一个 16 维 cell 向量
\[
k_i(c)\in\mathbb R,\qquad c\in C,
\]
其中 \(k_i(q,b)\) 是该 checkpoint 在 cell \((q,b)\) 上的平均 token logprob。仓库目前**还没有**写出这样的 full-panel hypercube aggregate 生成器或分析器；它只给出了 schema 和 zero-GPU feasibility audit。因此，上式是对现有 prereg 方案的**数学化重写**，不是仓库中已经存在的 observed artifact。支撑这一重写的仓库事实只是：raw JSONL 已包含 `slice_id` 与 `token_pos` 字段，故 \(Q\times B\) 的 cell assignment 在 source-only 层面是可构造的。fileciteturn12file0L83-L136 fileciteturn17file0L90-L115 fileciteturn13file0L32-L45

cell 权重必须定义为 source-only 的
\[
w_c=\frac{n_c}{\sum_{c'\in C} n_{c'}},
\]
其中 \(n_c\) 由固定 train audit blocks 决定，而不能从 outcome 中反推。当前 schema JSON 已把 16 个 cells 的 `n_tokens` 与 `weight` 全部写死，并给出 occupancy matrix
\[
\begin{bmatrix}
363&324&360&327\\
629&690&656&606\\
550&511&499&460\\
506&523&533&527
\end{bmatrix},
\]
所以 16 个 cells 目前在 smoke raw rows 上都非空，最小 cell count 为 324，最大为 690。这个事实只说明“不会因为空 cell 立即死亡”；它**不说明** hypercube residual 作为科学对象已经成立。fileciteturn21file0L205-L350 fileciteturn6file0L22-L56

如果把该对象写干净，那么均值模态应是常数 cell 向量 \(\mathbf 1_C\)，均值去除投影为
\[
\Pi_{\mathrm{mean}}^\perp(k_i)
=
k_i-\langle \mathbf 1_C,k_i\rangle_w\,\mathbf 1_C.
\]
但仅去常数模态远远不够。当前仓库为 hypercube prereg 明文规定的**mandatory nuisance space** 至少包括三类方向：常数 cell mean mode \(1_C\)；锁定 q4 slope 在新轴上的 lifted 版本 \(v_Q\otimes 1_B\)；以及所有中心化的纯 token-position main effects \(1_Q\otimes g_B\)。schema JSON 与 builder script 都将这一 mandatory nuisance 的维度写成 5，而 residual dimension 写成 11。fileciteturn12file0L225-L243 fileciteturn21file0L352-L369

因此，一个数学上干净的 hypercube 候选残差应定义为
\[
r_i
=
P_{N^\perp}k_i,
\]
其中
\[
N_{\mathrm{mand}}
=
\operatorname{span}
\left\{
1_C,\;
v_Q\otimes 1_B,\;
1_Q\otimes g_B^{(1)},\;
1_Q\otimes g_B^{(2)},\;
1_Q\otimes g_B^{(3)}
\right\}.
\]
若采用更严格的 additive nuisance，则应进一步比较
\[
N_{\mathrm{strict}}
=
\operatorname{span}
\left\{
1_C,\;
\text{all centered q4 main effects},\;
\text{all centered token-position main effects}
\right\},
\]
其维度为 7，剩余维度为 9。这里的“mandatory”与“optional”不能混淆：**constant、lifted q4 slope、token-position main effects 是最低要求；all centered q4 main effects 是更严格但也更诚实的对照。** 否则所谓 interaction residual 很容易只是被遗漏的 q4 main effect 伪装出来的。仓库实际上已经在 schema 中把这两套空间都明文列出。fileciteturn12file0L225-L243 fileciteturn21file0L352-L369

fold-locality 也必须保留。如果未来真的构造 hypercube residual，那么 nuisance 系数、matched-mean 配对方向、乃至任何 generation-related 校正，都必须像当前 q4 residual 脚本那样在 non-held-out seeds 上拟合，再投到 held-out seed 上，不能用全体样本作全局残差化。当前仓库已有 q4 版的 held-out-seed residualization、matched-mean 与 permutation/null 机制；但 hypercube **尚未实现对应分析脚本**。因此，fold-local hypercube 目前只是一个必要条件，不是已完成功能。fileciteturn14file0L77-L99 fileciteturn15file0L20-L26 fileciteturn15file0L43-L92

最后，空 cell 或稀疏 cell 应直接杀死候选。当前 zero-GPU audit 的门槛是 required fields 正确、每个 raw 文件只含一个 \((seed,generation)\)、schema/source_split 正确、所有 16 cells 非空，且最小 cell count 至少不低于默认阈值 128。现在三个 smoke raw files 的 min cell count 都是 324，所以**只通过了 occupancy feasibility**，并且最终 verdict 仍然只能是 `formal_prereg_only`。这正是“能放进数学定义里”与“有证据支持现象存在”之间的边界。fileciteturn13file0L149-L243 fileciteturn6file0L5-L20

## 识别问题与反定理

先给结论：**`Q_freq4 x B_tokenpos4` 目前没有改进识别，只是增加了自由度。** 之所以这么说，不是因为这个对象永远没价值，而是因为它现在只解决了“坐标系预注册”的问题，没有解决“对象是否可辨识”的问题。仓库自己在 framework adoption note 中已经承认：标量 KL 不唯一决定向量场；任何从 scalar KL 到 mean-null object 的提升都必须先固定 slice schema、reference measure、projection rule 与 normalization。hypercube 只是把 slice schema 从一维 q4 扩成二维 product partition；若没有更强的 invariance 与 guard，它仍然不唯一。fileciteturn11file0L19-L27 fileciteturn10file0L72-L87

第一个根本漏洞是**scalar-to-vector non-uniqueness**。四维 q4 已经存在这个问题，所以仓库才把对象从标量 \(D\) 或 \(P\) 收紧到 residual field。十六维 hypercube 并不会自动消除这一非唯一性；它只会让“你可以选择的方向”更多。如果 nuisance subspace 不是事前锁死、如果 axes 不是 outcome-independent、如果 projection 不是预注册，那么你总能在更大的空间里找到看起来“剩下了点什么”的坐标。这不是数学推进，这是坐标投机。fileciteturn8file0L21-L33 fileciteturn5file0L24-L36 fileciteturn21file0L371-L377

第二个漏洞是**partition arbitrariness**。当前 hypercube PREREG 只允许把 `token_pos` 作为新的 secondary axis，并明确把 `seed`、`generation`、`fold`、未预注册映射的 token type、未预注册 baseline surprise、以及 post-hoc result-selected axes 列为 forbidden。这个限制是对的，但也暴露了事实：如果没有这种禁令，hypercube 很容易退化为“看哪个轴好看就用哪个轴”。所谓 tensor structure 在这里并不自动给出不变量；它首先给你的是一张更大的 dashboard。fileciteturn12file0L244-L268 fileciteturn21file0L371-L394

第三个漏洞是**multiple comparisons 与 random subspace inflation**。q4 residual 脚本之所以引入 random mean-null projection multiplicity guard，就是因为单个投影的 \(\Delta R^2\) 很容易被随机方向复制甚至超越。hypercube 把 ambient 维度从 4 拉到 16，只会让这个问题更严重，而不是更轻。若未来不把“random same-dimension subspace guard”做进 hypercube analysis path，那么任何“某个 residual looks good”的表述都不可信。仓库现有 q4 脚本已明确要求对主投影与随机 mean-null unit directions 比较，并用经验 \(p\)-value 控制。对 hypercube 来说，这个 guard 只能更强，不能更弱。fileciteturn15file0L175-L231

第四个漏洞是**rank inflation 与 sparse-cell instability**。十六维对象表面上残差维度更高，但这不代表真正的有效秩更高。当前 q4 脚本已经把 “\(\sigma_2/\sigma_1<0.25\)” 与“残差振幅低于 \(2\max(\text{bootstrap p90}, \text{rank1-control p90})\)” 作为 kill 条件；hypercube 至少也要满足同类 rank/noise 守门。否则你只是在更高维空间里堆出一个低秩噪声片。至于 sparsity，当前 zero-GPU audit 的确显示 16/16 cells 非空、min count 324，但这只是 smoke rows 的 occupancy 事实，并不能替代真实 50-row full panel 上的稳定性评估。fileciteturn15file0L125-L172 fileciteturn6file0L22-L56

第五个漏洞是**Simpson-style reversals 与 post-hoc axis selection**。一旦把 token position 与 q4 frequency 交叉，main effects 和 interactions 的分离就变得更脆弱。如果不先把常数模、lifted q4 slope、token-position main effects 乃至严格 additive main effects 从结果里投掉，那么所谓“interaction residual”几乎没有解释力；它可能只是不同 marginal weights 带来的加权混合效应。当前 hypercube schema 至少承认了这一点，把 mandatory nuisance 与 strict additive nuisance 都写出来了。仓库在这点上是诚实的；问题在于它还没有拿出 full-panel 证据来表明这些投影之后**真的还剩下东西**。fileciteturn21file0L352-L369

因此可以给出一个近似定理。

**命题：当前仓库工件下的 hypercube 非可识别性命题。**
设未来想审计的 hypercube 观测对象为 \(k_i\in\mathbb R^{16}\)，残差为 \(r_i=P_{N^\perp}k_i\)，其中 \(N\) 至少包含常数模、lifted q4 slope 与 token-position main effects。若仓库中没有真实 50-row hypercube full-panel aggregate，也没有对该 aggregate 的独立 fold-local analysis artifact，而只有 schema 与 smoke-row occupancy，则“存在稳定、非标量、超出 scalar smoother 的 hypercube residual field”这一命题在当前证据下**不可识别**。证明思路很简单：当前可用工件只足以验证坐标构造、字段完整性、cell occupancy 与宣传边界；它们不提供任何对 \(r_i\) 的跨 seed / generation 稳定性、rank/noise、matched-mean、matched-slope、random-subspace guard 或 coarsening/refinement 稳健性的观测量。没有这些观测量，命题既不能被支持，也不能被严格反驳，只能停留在 formal preregistration feasibility。这个命题与仓库当前所有边界文件一致。fileciteturn5file0L47-L74 fileciteturn6file0L10-L20 fileciteturn7file0L40-L55 fileciteturn7file0L88-L101 fileciteturn1file0L24-L29

由此得到对“真实数学推进”的最小标准。要算推进，至少必须同时满足：坐标轴与 cell weights 预注册且 source-only；nuisance subspace 在看 outcome 前固定；所有 residualization、配对与方向选择都是 fold-local；残差矩阵在真实 full panel 上满足 rank/noise 门且优于 random same-dimension subspaces；matched-mean 与 matched-slope 不崩；leave-one-seed 之外还要看 generation block 的留出稳定性；coarsening/refinement 不导致对象消失；并且任何一条 kill gate 失败就直接退回 `killed` 或 `insufficient_artifact`。如果缺任意一条，hypercube 不过是“更大的剩余项容器”。其中前半部分是仓库当前 q4 gate 的自然扩张，后半部分——尤其 coarsening/refinement 与 matched-slope——是我认为 hypercube 想避免沦为 dashboard 时必须额外承担的负担。fileciteturn20file0L181-L315 fileciteturn15file0L234-L253

## 零 GPU 审计与条件性后续

当前已经存在、而且唯一被允许的 hypercube 路线，是一个**零 GPU 审计**。它的精确输入是：固定的 q4 schema JSON、由此衍生出的 hypercube schema JSON，以及现有 smoke raw JSONL 文件；脚本 `q4_hypercube_zero_gpu_audit.py` 只读取原始 raw rows，不加载 checkpoint，不跑推理，不训练，不生成 full panel，也不授权新 loss。它对每个 raw 文件检查 required fields、单一 seed/generation、一致的 `schema_id`、`source_split=train`、有限 logprob、16-cell occupancy 和最小 cell count 门槛。若任何条件不满足，输出 `invalid_artifact`；若全部满足，最强也只能输出 `formal_prereg_only`。这条路径已经由仓库代码和 markdown 产物完整记录。fileciteturn13file0L4-L9 fileciteturn13file0L32-L55 fileciteturn13file0L149-L243 fileciteturn6file0L5-L20

这条零 GPU 审计有价值，但价值很有限。它能回答的只有三类问题：第一，`Q_freq4 x B_tokenpos4` 是否在 source-only 层面定义得出来；第二，现有 smoke rows 上 16 cells 是否非空且不至于立刻稀疏死亡；第三，mandatory nuisance space 是否在 outcome inspection 之前被写死。它**刻意不回答**“残差是否存在”“是否稳定”“是否超出 scalar smoother”“是否具有科学意义”这些问题。换言之，这个脚本不是证据发生器，而是防止你以后偷换对象的约束器。fileciteturn5file0L47-L74 fileciteturn13file0L227-L243 fileciteturn21file0L379-L394

如果未来某天 PI 单独批准 full panel，那么 hypercube 仍然**不能**直接复用零 GPU 脚本充当分析器；它必须有一条独立的 post-panel analysis path，边界应当与 q4 residual 脚本类似而更严格。最少需要包含：由 guarded full-panel generator 产生的 50 个 \((seed,generation)\) raw JSONL；固定的 schema/provenance 字段，包括 `repo_head`、`schema_sha256`、`builder_script_sha256`、`generator_script_sha256`、source hashes、checkpoint inventory 与 raw hashes；一个 deterministic 的 preprocessing 规范；以及一个新的 hypercube fold-local analysis script，它只消费 full-panel hypercube aggregate，而不碰旧 aggregate，更不直接碰训练。当前仓库已经把 q4 full-panel generator 的 dry-run、approval token、checkpoint inventory 与 q4 separate analysis boundary 写明；但 hypercube 对应的 full-panel generator/analysis artifact **尚不存在**。所以这里仍然只能是条件性路径描述，不能视为批准。fileciteturn7file0L13-L24 fileciteturn7file0L63-L87 fileciteturn16file0L4-L15 fileciteturn16file0L202-L257 fileciteturn17file0L140-L172 fileciteturn17file0L212-L267

如果真要列“最快 kill tests”，我给六个，而且都应当是脚本化的。第一，**strict additive kill**：在 \(N_{\mathrm{strict}}\) 下若 residual 能量崩掉，则 hypercube 没有交互对象。第二，**matched-mean 与 matched-slope kill**：对 held-out seed，用训练 seeds 决定方向，若方向稳定性在任何预注册 tolerance 上失败，则直接杀。第三，**rank/noise kill**：若 centered residual matrix 的有效秩塌为近 rank-1，或幅度不超过 noise floor，则直接杀。第四，**random subspace kill**：若随机同维子空间经常达到或超过主 residual 的分数，则所谓对象只是 multiplicity 偶然。第五，**coarsening/refinement kill**：若 `tokenpos4` 改成更粗或更细但仍 source-only 的预注册方案时对象立即消失，则它过度依赖坐标挑选。第六，**generation-block leave-out kill**：如果仅在某些 generation 段可见，而留出 generation block 即崩，则它更像局部配平伪影而非稳定结构。前四项有现有 q4 gates 作为模板；后两项是 hypercube 若想避免“只是更大的 dashboard”所必需的新负担。fileciteturn20file0L212-L315 fileciteturn15file0L43-L92 fileciteturn15file0L125-L172 fileciteturn15file0L191-L231

对 node36 上的 Codex，下一步不该是训练，也不该是批准 full panel，而应该是**边界更硬的审计实现**：第一，保持 `build_hypercube_schema_20260623.py` 只做 source-only schema，不允许结果回写进 axis choice；第二，若以后要写 hypercube full-panel generator，必须在 `highorder_raw_logprob_panel.py` 的 guarded boundary 之外新增显式 artifact kind，不得偷改 q4 primary schema；第三，新增一个单独的 `q4_hypercube_foldlocal_analysis.py`，并强制它拒收零 GPU occupancy 文件与旧 rare/freq aggregate；第四，把 matched-slope、strict additive nuisance、generation-block leave-out 和 coarsening/refinement checks 做成 machine-readable JSON gates；第五，继承并扩展 q4 的 wording guard，禁止一切“残差已观察到”“LOSO passed”“glass box broken”式表述。当前仓库已经把这类 guard philosophy 贯彻到了 q4 residual 与 hypercube zero-GPU 方案中；缺的是 hypercube full-panel 的独立 observed artifact 与独立 analysis path。fileciteturn5file0L18-L36 fileciteturn7file0L26-L55 fileciteturn12file0L244-L268 fileciteturn21file0L379-L394

## 最终决定

下面是最简决策表。

| 对象/动作 | 判定 | 理由 |
|---|---|---|
| q4 residual-field 作为**未来审计对象** | keep | 仓库已给出对象定义与 q4 separate analysis path，但未给出观测到的正结果。fileciteturn8file0L21-L33 fileciteturn14file0L4-L13 |
| `Q_freq4 x B_tokenpos4` 作为**形式化预注册候选** | keep | 轴、weights、mandatory nuisance 已 source-only 锁定，16/16 cells 在 smoke rows 上非空。fileciteturn12file0L171-L243 fileciteturn21file0L159-L369 |
| “hypercube 改善了识别” | deflate | 当前只增加坐标自由度，没有 full-panel residual evidence，也没有 hypercube fold-local analysis artifact。fileciteturn5file0L22-L36 fileciteturn6file0L10-L20 |
| “hypercube residual 已被观察到” | reject | 仓库明确禁止该表述，且 zero-GPU audit 的最强 verdict 只有 `formal_prereg_only`。fileciteturn5file0L59-L74 fileciteturn6file0L58-L67 |
| full-panel generation 现在可批准 | blocked | 状态文件与实现 gate 都明确说 full panel 未运行，且仍需 PI approval token。fileciteturn1file0L18-L18 fileciteturn7file0L16-L24 fileciteturn16file0L274-L289 |
| training / new loss | blocked | 仓库多处明文禁止。fileciteturn5file0L63-L74 fileciteturn7file0L88-L101 |

**最终裁决：Allow zero-GPU audit only。**
精确含义是：允许把 hypercube extension 继续保留为一个**形式化预注册与零 GPU 可识别性审计对象**；不允许把它提升为已观察到的数学现象，不允许把它当成 full-panel generation 的批准理由，不允许把它变成训练或新 loss 的授权。若以后想得到更强结论，缺失工件至少包括：真实的 50-checkpoint hypercube full-panel raw rows/aggregate、独立的 hypercube fold-local analysis 脚本、strict additive 与 matched-slope 的 machine-readable gates、generation-block leave-out 审计、coarsening/refinement 稳健性审计，以及通过这些 gates 后仍然只能得到**下一轮 design review 资格**，而不是正结果用语。fileciteturn5file0L59-L74 fileciteturn7file0L99-L101