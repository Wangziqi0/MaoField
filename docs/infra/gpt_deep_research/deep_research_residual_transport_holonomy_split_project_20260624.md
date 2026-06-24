# MaoField 材料的去魅数学审计与新底层对象提案

## 证据边界

本报告把你附带的 ZIP 包视为**唯一主证据**。`GPT55_PRO_RESEARCH_INDEX_20260622.md` 明确把仓库目标写成 `Wangziqi0/MaoField`，同时要求把材料区分为 observed、derived、claimed、blocked 四类；我没有在本会话中拿到可核验的 GitHub connector 返回，因此**仓库连接器核验记为 blocked**，下面一律只依据 ZIP 内 `from_repo/` 快照行文，不把私有 canonical 仓库本身当作已独立验证的事实。另一个技术限制是：本会话的 `file_search` 没有索引到这个 ZIP，所以我只能用“包内文件名:行号”的方式做精确引文。[^1] [GPT55_PRO_RESEARCH_INDEX_20260622.md:151–166]

当前硬边界非常清楚，而且已经被多处重复写死：Mode B 的固定裁定仍是 `stable non-scalar residual object = insufficient_artifact` 与 `existing interaction smoke = smoke_conjecture_only`；没有 full panel，没有 16-cell full-panel aggregate，没有训练授权，没有 new loss 授权；D624 允许的工作只剩 future-only 的零 GPU prereg、schema/checker 收紧，以及 smoke feasibility，**smoke 不是 residual evidence**。即便未来所有 prereg null blocks 都通过，分析脚本给出的最强 verdict 也只能是 `eligible_for_next_design_review_only`，而不是“观察到 residual field”。[STATE.md:16–17, 24–27; QUOTIENT_RESIDUAL_MAINLINE_ADOPTION_NOTE_20260624.md:64–99; NULL_TESTS_CONTRACT_20260624.md:13–22, 33–45; q4_hypercube_interaction_prereg_analysis.py:1–8, 586–602]

这里还有一个必须说明的证据缺口：包内脚本把 source-only weights 的真来源绑定到 `hypercube_schema_q4_tokenpos4_20260623.json`，并且该 schema 决定加权投影、残差范数和 `source_only_weights` 一致性校验；主线文档又明确说，只有在**产品权重且满支撑**时，才可以谈 canonical Hoeffding/functional ANOVA，非产品权重时只能谈预注册的层级加权投影程序。由于这个具体 schema JSON 不在我能直接援引的 ZIP 证据里，**我不能从包内证据独立确认当前权重是否真是产品型**，所以任何“canonical Hoeffding 已经成立”的说法都必须保留。 [q4_hypercube_interaction_prereg_analysis.py:23–35, 198–209, 236–282, 753–770; deep_research_quotient_residual_mainline_debranded_program_20260624.md:77–93]

## 旧解释的去魅

先把旧叙事压扁。包内主线已经把大部分“听起来像发现”的措辞撤掉了：不能说 observed interaction field、不能说 observed residual field、不能说 LOSO pass、不能说 F3 positive、不能说 glass box broken、不能说 training/new loss authorized。主线采用说明与 STATE 一致：现在允许的只是“negative-centered measurement-audit / no-go framework”，不是正向 MaoField claim。 [STATE.md:16, 24, 27; QUOTIENT_RESIDUAL_MAINLINE_ADOPTION_NOTE_20260624.md:37–39, 64–79, 101–113; QUOTIENT_RESIDUAL_FINITE_ANOVA_ADOPTION_NOTE_20260623.md:51–82; MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md:54–87]

更关键的是，唯一现成的 interaction 证据只是三份 smoke raw 上做出的一个小型加权残差计算。这个 smoke audit 自己写得很诚实：它只读三份现有 raw JSONL，不加载 checkpoint、不做 inference、不训练、不生成 full panel；三份 smoke 的 pairwise weighted correlation 大约在 `0.947` 到 `0.969`，但 weighted uncentered `sigma2/sigma1 = 0.132356799...`，文档明确警告“the three-smoke pattern is close to one dominant shape”，并同时承认缺少 random equal-size partition、within-q shuffle、bad-axis、cell variance/noise、held-out seed、generation-block leave-out 等控制。所以这份材料最多说明“可复算的 smoke hint”，说不到“稳定多方向对象”。 [Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.md:7–20, 44–65]

零 GPU hypercube audit 也没有给你任何额外的实证资本。它只证明现有三份 smoke raw 在 `Q_freq4 × B_tokenpos4` 上有 `16/16` 个非空 cell，因此 verdict 只能是 `formal_prereg_only`；同一文件还把 `audit_block_id` 轴直接标成 `rejected_sparse_high_dimensional_axis` 的坏轴方向。这意味着当前仓库材料真正支持的，不是“发现了 hypercube”，而只是“这个 carrier 在 smoke raw 上不空，可以拿来做 future-only prereg 设计”。 [Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.md:8–19, 20–29, 44–65]

因此，旧解释里最需要被扔掉的，不只是哲学包装，而是一个更底层的误会：**把“有一个可见剩余图样”误认成“已经有一个对象”**。包内真正稳定下来的东西不是对象本身，而是如何把这个对象杀掉：随机轴、同维随机子空间、秩一影子、coarsening failure、gluing absorption、以及 fail-closed contract。它留下的不是阳性证据，而是一套“对象必须先配刑具”的研究纪律。 [NULL_TESTS_CONTRACT_20260624.md:26–45, 55–77, 121–148, 153–173; HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md:77–97, 125–158; deep_research_quotient_residual_mainline_debranded_program_20260624.md:206–210]

## 最干净的有限维对象

包内已经把“母对象”压到
\[
R_t=\Pi_{\mathcal N^\perp,w}K_t,
\]
并把 strict additive special case 压到
\[
I_t=\Pi_{\mathcal A^\perp,w}K_t,\qquad \mathcal A=\{\mu+\alpha(q)+\beta(b)\}.
\]
这一层是对的，但我认为它还**不够底层**。因为单个 \(R_t\) 或单条 residual 序列，仍然太容易被 rank-1 shadow、随机同维子空间、以及 scale-choice 伪影伪装。包内材料真正不断抬高权重的，其实是 coarsening naturality、projection-evolution commutator、principal-angle stability、gluing sanity 这些“对象在不同坐标/尺度下是否真是同一个”的问题。 [deep_research_quotient_residual_mainline_debranded_program_20260624.md:51–75, 95–142, 160–210; QUOTIENT_RESIDUAL_FINITE_ANOVA_ADOPTION_NOTE_20260623.md:24–49; MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md:30–52]

所以我建议把新的底层对象改写为：

\[
\boxed{\text{有限尺度格上的加权商残差传输预层}}
\]

更具体地说，取尺度格
\[
\Sigma=\{(q2,b2),(q2,b4),(q2,b8),(q4,b2),\dots,(q8,b8)\},
\]
对每个尺度 \(s\in\Sigma\)，给一个可容许三元组
\[
(X_s,w_s,\mathcal N_s),
\]
定义加权 Hilbert 空间 \(H_s=\mathbb R^{X_s}\)、正交投影 \(P_s=\Pi_{\mathcal N_s^\perp,w_s}\)，以及局部残差 section
\[
R_s(K)=P_sK_s.
\]
对每条 coarse edge \(\rho:s\to s'\)，给加权块平均 \(C_\rho:H_s\to H_{s'}\)。然后不把“对象”定义成某个单独的 \(R_s\)，而定义成整套 transport data：
\[
\mathscr R(K)=\{R_s(K),\ D_\rho(K),\ H_\square(K),\ \operatorname{Obs}_{\mathrm{loc}}(K)\},
\]
其中
\[
D_\rho(K)=C_\rho P_sK-P_{s'}C_\rho K
\]
是**边自然性缺陷**，而每个 refinement square 的
\[
H_\square(K)=P_{s_0}C_{\rho_2}P_{s_2}C_{\rho_1}P_sK-
P_{s_0}C_{\rho_2'}P_{s_1}C_{\rho_1'}P_sK
\]
是**方格 holonomy 缺陷**。如果 \(H_\square\neq 0\)，就说明“先按 q 缩再按 b 缩”和“先按 b 缩再按 q 缩”得到的 residual 不是同一个对象。这个量比单独的 commutator 或单独的 residual vector 更底层，因为它直接编码了**对象是否能在尺度格上被一致运输**。这是包内 commutator、coarsening defect 与 gluing obstruction 的自然合并版，但它在当前材料里还没有被显式定义出来。 [deep_research_quotient_residual_mainline_debranded_program_20260624.md:103–142, 178–194, 237–248; NULL_TESTS_CONTRACT_20260624.md:159–170]

于是，真正干净的 bottom-level problem 不再是“某个 4×4 剩余图样是否存在”，而是下面这个纯数学问题：

\[
\textbf{对哪些可容许三元组族 }(X_s,w_s,\mathcal N_s)_{s\in\Sigma},
\textbf{所有 }D_\rho\textbf{ 与 }H_\square\textbf{ 同时消失，且 residual subspace 又能显著区别于随机同维子空间？}
\]

这个问题一旦成立，得到的是一个**可传输、可粘合、非随机、非秩一影子**的对象；一旦失败，得到的则是一个比“没发现阳性”更强的 no-go：说明所谓结构只是坐标、尺度或 gauge 的产物。 [QUOTIENT_RESIDUAL_MAINLINE_ADOPTION_NOTE_20260624.md:43–61, 101–113; deep_research_quotient_residual_mainline_debranded_program_20260624.md:237–248]

## 不可能性定理与反例

第一条我建议正式写成**秩一影子下的稳定性空洞引理**。设 \(M\) 是把各时刻 residual \(R_t\) 堆成的矩阵。如果 \(\operatorname{rank}(M)=1\)，则存在固定模板 \(u\) 与标量轨道 \(c_t\)，使得 \(R_t=c_tu\)。这件事在包内主线里已经被点明；但它还有一个更狠的推论：任何把样本切成若干块、再比较各块 residual subspace 主角的“principal-angle stability”测试，在 rank-1 情形下都自动趋于零角度，因为每一块的 span 都是同一个 \(\mathrm{span}(u)\)。也就是说，**principal-angle 稳定性在 rank-1 shadow 下是空洞的**；它只能在 \(\sigma_2/\sigma_1\) 先过关以后才有意义。当前 contract 正是据此把 `weighted_uncentered_sigma2_over_sigma1` 放到优先 kill 位置，并把 design-review floor 收紧到 `>=0.25`。 [deep_research_quotient_residual_mainline_debranded_program_20260624.md:97–101, 170–176, 206–210; NULL_TESTS_CONTRACT_20260624.md:68–77, 136–148; q4_hypercube_interaction_prereg_analysis.py:31–35, 350–376, 586–599]

第二条我建议写成**方格 holonomy no-go 定理**。定义上面的 \(D_\rho\) 与 \(H_\square\)。那么如果每条边都满足 \(D_\rho\equiv 0\)，即 coarsening 与 residual projection 在每个 edge 上都自然交换，那么所有 refinement square 都满足 \(H_\square\equiv 0\)。证明只有一行：两条路径都等于“先把 \(K\) 通过原始 coarsening 压到终点，再做终点的 residual projection”。因此，只要你在某个 square 上测得 \(H_\square(K)\neq 0\)，就可以严格推出：**至少有一个中间尺度的 nuisance family 不是 functorial 的，或者 coarsening naturality 已经失败**。这才是“holonomy-like obstruction”的严格落地，不是比喻。包内文档虽提出了 commutator、coarsening defect 与 holonomy/gluing 方向，但还没有把这个 square-loop defect 显式封装成底层对象；我认为这正是最值得写成新 theorem 的地方。 [deep_research_quotient_residual_mainline_debranded_program_20260624.md:103–123, 178–194, 202–208; MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md:40–52]

一个完全有限维的反例可以说明这不是空谈。取一个 \(4\times4\) 的细尺度表 \(K\)，把它朝 \(2\times4\) 与 \(4\times2\) 两条中间路径 coarse，再到 \(2\times2\) 终点。若中间两个尺度各自偷偷带上**不相容的额外 nuisance 方向**，那么两条路径的终点 residual 会不同。我构造的一个显式例子中，两条路径在 \(2\times2\) 终点给出
\[
\begin{pmatrix}
-0.0481 & 0.0481\\
0.0481 & -0.0481
\end{pmatrix}
\quad\text{与}\quad
\begin{pmatrix}
0.00753 & -0.00753\\
-0.00753 & 0.00753
\end{pmatrix},
\]
二者 Frobenius 距离约为 \(0.1113\)。这说明只要 nuisance family 不是 functorial 的，所谓“跨尺度同一对象”立刻破产。这个反例不依赖任何 GPU，也不依赖 MaoField 数据；它是纯有限维线性代数。

第三条应写成**局部可吸收 mismatch 的 sheaf 失效引理**。包内已经把 gluing obstruction 定义成对局部 nuisance gauge 最小化后的 overlap mismatch。于是结论很直接：如果某个所谓局部冲突一旦允许轻微扩张局部 nuisance 就能被吸收，那么它不是几何结构，不是 holonomy，不是“更深矛盾”，只是 gauge artifact。换句话说，**局部 mismatch 本身毫无价值；只有“在预注册允许的局部 nuisance 扩张后仍不可吸收”的 mismatch 才可能配得上 obstruction 这个词**。这条引理应当被明确写成 fail-closed 优先级，而不是讨论性语言。 [deep_research_quotient_residual_mainline_debranded_program_20260624.md:125–142, 192–194; NULL_TESTS_CONTRACT_20260624.md:167–173]

第四条应写成**随机同维不可识别性 no-go**。包内已经给出理论动机：在 isotropic 零模型下，落到某个 \(r\)-维子空间上的能量分布只依赖 \(\dim E=r\)，不依赖该子空间 “位于哪里”。因此，任何只看投影能量、却不显式和随机同维子空间分布比较的“真子空间解释”，都没有坐标不变意义。由此可知，true 9D interaction space 若不优于随机 9D spaces，就不应再被称为对象。这个 guard 不是可有可无的装饰，而是堵死“坐标命名学”的最低条件。 [deep_research_quotient_residual_mainline_debranded_program_20260624.md:95–101, 176–186; NULL_TESTS_CONTRACT_20260624.md:55–66, 140–148; q4_hypercube_interaction_prereg_analysis.py:121–145]

最后补一句最刺耳但必要的话：当前三份 smoke 的 uncentered `sigma2/sigma1 ≈ 0.132`，自己就已经落在 D624 新 design-review floor `0.25` 以下；虽然这不是 full-panel verdict，也不会被我拿来冒充结论，但它恰好说明你现在最该研究的不是“如何包装稳定对象”，而是**为什么这么容易出现单模板标量影子**。这件事本身比继续追逐 smoke narrative 更像一个像样的数学问题。 [Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.md:50–60; STATE.md:24, 27; NULL_TESTS_CONTRACT_20260624.md:68–77]

## 可能的正向路线

有，但必须彻底去品牌化，而且要承认它首先是**纯数学项目**。

第一条正向路线，是把上面的“加权商残差传输预层”做成一个真正的分类问题。你可以研究：在给定尺度格 \(\Sigma\) 上，哪些 nuisance family \((\mathcal N_s)\) 是 functorial 的，使得所有 edge defect \(D_\rho\) 都为零；进一步，哪些 family 还使所有 square holonomy \(H_\square\) 都为零，并且局部 sections 可以无障碍 gluing。这个问题的产出不是某条实验结论，而是一类**零 holonomy 的 admissible systems 分类定理**。它一旦做出来，MaoField 只是可能的一个实例，不再是对象本身。这个方向完全契合包内把 report(17)/(19)/(21)/(22) 压缩成“可证明、可击杀、可否证”的有限维程序。 [STATE.md:16, 24; QUOTIENT_RESIDUAL_MAINLINE_ADOPTION_NOTE_20260624.md:27–39, 43–61, 101–113]

第二条正向路线，是研究**最小非平凡秩**。包内已经把 rank-1 shadow 视为首要 no-go 风险，但还没有问得足够干净：在给定 scale lattice、随机同维 guard 与 naturality guard 下，一个 transport-stable residual family 至少需要多大“有效秩”才不至于退化成标量影子？这可以导向一个新定义，例如 transport-stable rank
\[
r_\ast=\min\{r:\ \exists\ \text{一个跨尺度稳定且显著优于随机同维空间的 } r\text{-维 residual family}\}.
\]
如果你能证明 \(r_\ast\ge 2\) 或更强，那么你得到的是一个漂亮的 no-go 下界；如果能分类 \(r_\ast=2\) 的全部情形，那就是正面结构定理。 [deep_research_quotient_residual_mainline_debranded_program_20260624.md:170–186, 237–248; NULL_TESTS_CONTRACT_20260624.md:68–77, 159–170]

第三条正向路线，是把“commutator leakage”从解释性语言压成一个**谱量**。不是只问 \([P,T]\neq 0\)，而是问：在 residual sector 与 nuisance sector 的块矩阵分解里，泄漏块 \(B,C\) 的奇异值能否同时被 random-axis、same-dimension random subspace、以及 gluing absorption 的 null guards 排除？如果不能，那所谓动态/运动/恢复轨迹就仍然只是 sector leakage；如果能，才有资格继续谈 transport dynamics。这一点与包内“contradiction = noncommutation / gluing obstruction”的哲学落地恰好一致，但你必须把它完全翻译成算子理论语言。 [MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md:62–67; deep_research_quotient_residual_mainline_debranded_program_20260624.md:114–123, 190–194]

因此，正向路线不是“继续给 MaoField 找证据”，而是把它拆成一个新的 finite-dimensional operator project：**残差、运输、自然性、holonomy、random-subspace calibration**。这条路是可以继续的，但它与当前 empirical MaoField verdict 不是一回事。 [QUOTIENT_RESIDUAL_MAINLINE_ADOPTION_NOTE_20260624.md:43–61, 64–79]

## 仅限零GPU的核验方案

我建议只做下面这套零 GPU 计划，而且全部 fail-closed。

第一步，是把当前包内定义精炼成一份纯线性代数规范：固定每个尺度 \(s\) 的 carrier \(X_s\)、权重 \(w_s\)、nuisance basis digest、以及 coarsening map digest，生成一个只依赖 JSON/NumPy 的验证器。现有脚本已经说明，分析器应完全独立于 generator，不加载 checkpoint、不做 inference、不训练，只消费 future aggregate 或 synthetic aggregate；这个边界必须原封不动保留。 [HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md:125–158; q4_hypercube_interaction_prereg_analysis.py:1–8, 621–678]

第二步，是在**纯合成数据**上先把 theorem 与 counterexample 跑通。构造 `q8/q4/q2 × tokenpos8/4/2` 的尺度格，分别测试产品权重与非产品权重、functorial nuisance 与非 functorial nuisance、rank-1 family 与 genuine rank-2 family。你要验证的不是“某实验有没有发现”，而是：哪些情形下 \(D_\rho=0\)、哪些情形下 \(H_\square\neq 0\)、哪些情形下 principal-angle test 失去意义。只要 theorem 在 toy models 上都讲不清，碰真实面板只会更糟。这个顺序也符合包内“先有 kill suite，再谈对象”的主线。 [deep_research_quotient_residual_mainline_debranded_program_20260624.md:206–233; NULL_TESTS_CONTRACT_20260624.md:33–45, 153–173]

第三步，是把 new object 所需的 contract 明确加到 future-only `null_tests` 里。我建议至少再增四块：`scale_square_holonomy`、`nuisance_functoriality_digest`、`rank1_angle_vacuity_guard`、`random_same_dim_angle_gap`。每个 block 仍必须遵守 D624 contract：机器可读字段、布尔 `pass`、明确的 `kill_verdict_if_fail`、原始 provenance digest 一致、`outcome_independent = true`，缺失或畸形一律 fail-closed。 [NULL_TESTS_CONTRACT_20260624.md:48–119, 121–148; q4_hypercube_interaction_prereg_analysis.py:64–87, 396–475, 681–785]

第四步，是把“坏轴”扩展成**坏路径**。当前 contract 已经有 `bad_axis_audit_block_id`，但如果你转向尺度格研究，就应当新增“bad transport path”对照：故意采用不 functorial 的 nuisance family，检查 square holonomy 是否机械升高；如果真路径与坏路径不可区分，则对象应判死。这个思路与当前 bad-axis 思维完全同构，只是提升到路径层。 [NULL_TESTS_CONTRACT_20260624.md:58–66, 140–148; HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md:82–93]

第五步，也是最重要的一步，是继续保留现在的结论上限。哪怕未来真有 PI-gated full panel 进入，这条新数学线也只能把实证接为“某个实例是否落入既定 operator framework”的问题；**绝不能倒过来让实证残渣去决定对象定义**。包内最可贵的纪律，就是 nuisance、weights、carrier、bad axes、kill conditions 必须先锁死；任何用 outcome 反推这些定义的做法，都应直接记为 invalid artifact。 [NULL_TESTS_CONTRACT_20260624.md:79–119, 129–148; QUOTIENT_RESIDUAL_MAINLINE_ADOPTION_NOTE_20260624.md:83–99]

## 给PI的初中版解释

把它想成一个表格游戏就够了。

你先有一个 \(4\times4\) 表格。行代表一种分箱，列代表 token 位置分箱。表里每个格子放一个数。第一件事不是兴奋，而是先减掉最普通的背景：整体平均值、行的平均偏差、列的平均偏差。减完以后剩下的，才叫“候选剩余”。这一步包内已经写成了“4×4 表格先减 ordinary background”的 plain explanation。 [NULL_TESTS_CONTRACT_20260624.md:153–170; HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md:16–30]

但“有剩余”还远远不够。因为它可能只是同一张模板忽亮忽暗，也可能只是把格子换个分法就得到的假图样，也可能把列标签打乱后还差不多，也可能一合并成更粗的格子就没了。所以真正该问的不是“有没有图样”，而是“这个图样是不是在各种合理变换下都还能算同一个东西”。这正是当前 null tests 在问的问题：随机轴、同维随机子空间、coarsen/refine naturality、principal angles、gluing sanity。 [NULL_TESTS_CONTRACT_20260624.md:159–170; HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md:77–97]

我给你的新建议可以缩成一句话：**不要再问“剩余大不大”，要问“这个剩余在缩表格的两条路径下，最后是不是同一个剩余”**。如果先缩行再缩列，与先缩列再缩行，得到的是不同答案，那它就不是一个真正的对象，只是测量方式在骗你。这个问题比现在的 smoke 讨论更底层，也更值得做成数学。

还有一句更直白的：如果所有块看起来都很稳定，但其实只是“一张固定模板在变亮变暗”，那不叫深结构。它只叫一个影子。当前 contract 之所以把 `sigma2/sigma1` 放得这么前，就是为了防这种事。 [q4_hypercube_interaction_prereg_analysis.py:350–376, 586–599; Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.md:50–60]

## 教授式最终裁决

我的最终裁决是：**拆分为新项目**。

理由很简单，而且我故意说得不客气。对 MaoField 当前经验主线而言，结论已经固定：它只支持 zero-GPU formal prereg、schema/checker feasibility 与 smoke feasibility；现有 Mode B verdict 仍是 `insufficient_artifact`，interaction smoke 仍是 `smoke_conjecture_only`。在这个边界下，继续把现有材料包装成“观察到稳定对象”是错误路线。 [STATE.md:16, 24, 27; QUOTIENT_RESIDUAL_MAINLINE_ADOPTION_NOTE_20260624.md:64–99; NULL_TESTS_CONTRACT_20260624.md:13–22, 38–45]

但对数学而言，不必停。应当立刻把品牌叙事剥离，把项目改名为类似“有限尺度格上的加权商残差传输与 holonomy no-go”之类的纯数学课题。保留 D624 的 fail-closed contract，把新对象升级为“残差传输预层 + square holonomy defect + random-subspace calibration”，先在纯有限维合成世界里做 theorem、counterexample、classification。未来若 PI 真批准 full panel，它也只能作为**这个新数学项目的一个实例化输入**，而不是倒过来定义对象。 [QUOTIENT_RESIDUAL_MAINLINE_ADOPTION_NOTE_20260624.md:27–39, 43–61, 83–99, 101–113; deep_research_quotient_residual_mainline_debranded_program_20260624.md:214–248]

所以，如果必须在你给的选项里只选一个，我不选“继续 MaoField 经验线”，也不选“当场停止所有数学”。我选的是最严格、也最干净的那个：**split into a new project**。经验旧线按 projection/smoke artifact 处理；数学新线按纯 operator/no-go project 继续；所有未来实证，一律 PI-gated，而且即便通过，也最多进入下一轮 design review，不得擅自晋升为“已经发现结构”。 [STATE.md:24, 27; NULL_TESTS_CONTRACT_20260624.md:33–45, 121–148; q4_hypercube_interaction_prereg_analysis.py:599–602]

[^1]: 本报告引文均来自附件 ZIP 解压后的包内文件与行号；由于本会话 file_search 无法索引该 ZIP，无法使用 `filecite...` 格式。