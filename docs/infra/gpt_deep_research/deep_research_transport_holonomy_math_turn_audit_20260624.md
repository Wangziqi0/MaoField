# 运输与 Holonomy 数学转向审计报告

连接器边界先说清楚：本次运行里，我没有成功建立可用的 GitHub connector 读取链路，因此**没有**把公共 GitHub 页面、`raw.githubusercontent.com`、搜索摘要或 404 页面当作规范仓库证据；以下关于 MaoField 仓库现状的判断，全部以上传的两份 ZIP bundle 为证据边界，并只把外部网络用于补充一般数学文献背景。

## 证据边界

就 bundle 本身能支持的内容而言，MaoField 目前的上限非常窄，而且这些上限在 `STATE.md`、`GPT55_PRO_RESEARCH_INDEX_20260622.md`、`QUOTIENT_RESIDUAL_MAINLINE_ADOPTION_NOTE_20260624.md`、`NULL_TESTS_CONTRACT_20260624.md`、`HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md` 与 `q4_hypercube_interaction_prereg_analysis.py` 里是重复锁死的：**当前只支持零 GPU formal prereg、schema/occupancy 检查、checker 可执行性、smoke feasibility，以及未来 aggregate 的 fail-closed 合约设计**。Mode B 的固定裁定仍是 `stable non-scalar residual object = insufficient_artifact`，现有 interaction smoke 的固定裁定仍是 `smoke_conjecture_only`；即便未来 prereg checker 全部通过，脚本的最强 verdict 也只能到 `eligible_for_next_design_review_only`，不能升级成任何“observed residual field”措辞。（bundle：`from_repo/STATE.md`；`from_repo/GPT55_PRO_RESEARCH_INDEX_20260622.md`；`from_repo/docs/infra/gpt_deep_research/QUOTIENT_RESIDUAL_MAINLINE_ADOPTION_NOTE_20260624.md`；`from_repo/docs/infra/math_turn_20260622/NULL_TESTS_CONTRACT_20260624.md`；`from_repo/scripts/q4_hypercube_interaction_prereg_analysis.py`）

就 bundle 明确**不能**支持的内容而言，也同样没有解释空间：不能说 full panel 已经运行；不能说存在 16-cell full-panel aggregate；不能说 hypercube residual、interaction field、quotient residual、transport field 或 holonomy field 已被观察到；不能说 LOSO passed、F3 positive、glass box broken；不能说 training authorized，不能说 new loss authorized。smoke、schema occupancy、checker dry-run、synthetic harness、以及 small residual hints，都不是这些结论的替代证据。（bundle：`from_repo/STATE.md`；`from_repo/docs/infra/math_turn_20260622/Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.md`；`from_repo/docs/infra/math_turn_20260622/RESIDUAL_TRANSPORT_HOLONOMY_SYNTHETIC_HARNESS_20260624.md`；`from_repo/docs/infra/math_turn_20260622/RESIDUAL_TRANSPORT_HOLONOMY_SYNTHETIC_RESULT_20260624.md`）

还有一个关键细节必须补上。你给的 ZIP 里其实包含了 `hypercube_schema_q4_tokenpos4_20260623.json`，我直接检查了其中 16 个 cell 的 source-only weights。结果是：它们**不是精确的 product-form weights**；把 q 边际与 b 边际相乘后得到的外积，与实际 cell weights 的最大绝对偏差约为 `0.00459`，最大相对偏差约为 `7.7%`。因此，对当前载体最安全的语言不是“canonical product-measure Hoeffding 已成立”，而是“在非产品权重下的预注册层级加权投影/残差程序”。这一点恰好和 bundle 主线文档的谨慎边界保持一致：**product weights 与 full support 才允许你轻松说 canonical Hoeffding；否则只能老老实实说 weighted hierarchical projection**。关于 classical ANOVA/Hoeffding 对 product-type measures 的依赖，以及 dependent / non-product measures 下需要 generalized ANOVA 的事实，文献上也是明确的。citeturn8search0turn9view0

最后，第二个 ZIP addendum 的价值也必须摆正。它新增的是一个**Mode A 纯合成 harness**，用四个 toy controls 去检验定义是否可执行；它的最强 allowed verdict 仅是 `synthetic_harness_only_no_maofield_claim`。这说明“尺子可以做出来并在玩具例子上工作”，不说明“MaoField 里已经有被尺子量到的对象”。（bundle：`from_repo/docs/infra/math_turn_20260622/RESIDUAL_TRANSPORT_HOLONOMY_SYNTHETIC_HARNESS_20260624.md`；`from_repo/scripts/residual_transport_holonomy_synthetic.py`）

## 候选数学对象

从 bundle 的 report(17)/(19)/(21)/(22)/(23) 主线往下抽象，至少有六个**彼此 genuinely different** 的底层对象。它们不是一个词换另一个词，而是不同层级的有限维对象：有的在单尺度上定义，有的在尺度边上定义，有的在方格回路上定义，有的是动态或局部—整体层面的障碍对象。Hoeffding/functional ANOVA 的历史原点在 Hoeffding 1948；而对非产品、相关或依赖测度，后续 generalized ANOVA 文献强调必须从“产品型正交分解”退回到更弱的层级正交/耦合方程框架。主角与子空间夹角则可经奇异值来表达。citeturn8search0turn9view0turn7search8

### 单尺度商残差

**定义。** 给定可容许三元组 \((X,w,N)\)，令 \(H_w=\mathbb R^X\)，内积为 \(\langle f,g\rangle_w=\sum_{x\in X}w(x)f(x)g(x)\)。对观测表 \(K_t\in H_w\)，定义
\[
R_t=\Pi_{N^\perp,w}K_t.
\]

**环境。** 有限维加权 Hilbert 空间。
**nuisance quotient。** 直接把 \(N\) 商掉；\(R_t\) 是 \([K_t]\in H_w/N\) 的最小范数代表。
**observable statistic。** \(\|R_t\|_w\)、堆叠矩阵的奇异值谱、跨 seed/generation 的主角。
**null model。** mean/slope only；matched mean/slope；rank-1 template；random same-dimension subspace。
**fast kill test。** 若 \(\sigma_2/\sigma_1<0.25\) 或 matched mean/slope 后方向不稳，则优先判死。
**theorem target。** 最小范数代表唯一性；rank-1 shadow vacuity；同维随机子空间不可区分 no-go。

### 二阶加权交互场

**定义。** 在 \(X=Q\times B\) 上，把 strict additive 子空间
\[
A=\{\mu+A(q)+B(b)\}
\]
作为 nuisance，定义
\[
I=\Pi_{A^\perp,w}K.
\]

**环境。** 有限乘积空间上的加权表格；若权重是 product-form 且满支撑，则可谈 classical Hoeffding / functional ANOVA；否则只应谈 hierarchical weighted projection。citeturn8search0turn9view0
**nuisance quotient。** 去掉 global mean、q 主效应、b 主效应。
**observable statistic。** interaction norm、cellwise residual shape、rank spectrum。
**null model。** random equal-size partitions；within-q position shuffle；bad-axis control。
**fast kill test。** 若真实 position 轴不优于随机同规模分箱，或 shuffle 后统计量不降，则判 `killed_by_random_axis`。
**theorem target。** 在 product weights 下的唯一加性—交互分解；在非产品权重下的 canonical-language 边界。

### 尺度边缺陷

**定义。** 对尺度边 \(\rho:s\to s'\)，给定 coarse map \(C_\rho:H_s\to H_{s'}\) 与两端投影 \(P_s,P_{s'}\)，定义
\[
D_\rho(K)=C_\rho P_sK-P_{s'}C_\rho K.
\]

**环境。** 尺度图或尺度格上的算子族。
**nuisance quotient。** 比较的是“先商掉再粗化”和“先粗化再商掉”这两个 quotient 操作。
**observable statistic。** \(\|D_\rho(K)\|_{w_{s'}}\) 与 relative defect。
**null model。** functorial additive nuisance；bad coarse nuisance family。
**fast kill test。** 任何重要边上 defect 稳定非零，就说明 coarsening/projection 不自然。
**theorem target。** \(D_\rho\equiv0\) 的充要条件：\(C_\rho N_s\subseteq N_{s'}\) 且 \(C_\rho N_s^\perp\subseteq N_{s'}^\perp\)。

### 方格 holonomy 缺陷

**定义。** 取一个 refinement square，例如
\[
(q8,b8)\to(q4,b8)\to(q4,b4)
\]
与
\[
(q8,b8)\to(q8,b4)\to(q4,b4),
\]
定义
\[
H_\square(K)=
C_{\rho_2}P_{s_1}C_{\rho_1}P_{s_0}K-
C_{\rho'_2}P_{s'_1}C_{\rho'_1}P_{s_0}K.
\]

**环境。** 有限尺度格上的回路差。
**nuisance quotient。** 不是看某个尺度上的 residual 大不大，而是看 residual 能否沿不同路径被一致运输。
**observable statistic。** \(\|H_\square(K)\|\)；不同 square 的 holonomy profile。
**null model。** product/additive natural family；故意 non-functorial 中间 nuisance。
**fast kill test。** natural positive control 若不接近 0，说明定义本身坏；真实对象若与 bad path 不可分，也应判死。
**theorem target。** edge-natural \(\Rightarrow\) square-zero；nonzero square holonomy \(\Rightarrow\) 至少一条边或一个中间 nuisance family 非 functorial。

### 传输稳定秩对象

**定义。** 令 \(M\) 为把多个 \(R_s\) 或多个 \(R_t\) 堆叠后的矩阵，定义 transport-stable rank 为满足 rank floor、主角稳定、同维随机子空间分离以及 coarsening naturality 的最小有效维数。

**环境。** 加权残差轨道的子空间几何。主角可由奇异值/SVD 表达。citeturn5view0turn7search8
**nuisance quotient。** 已去掉 mean、main effects、pre-outcome nuisance 后的 residual sector。
**observable statistic。** \(\sigma_2/\sigma_1\)、principal angles、held-out capture ratio。
**null model。** repeated rank-1 template；Haar-like random same-dimension subspaces on Grassmannian。对均匀随机子空间，canonical angles 的分布只依赖维数与环境维数，而不偏袒任何被命名的坐标轴。citeturn4view2
**fast kill test。** \(\sigma_2/\sigma_1<0.25\)；或者真实二维/九维子空间不优于随机同维子空间。
**theorem target。** rank-1 vacuity no-go；random-subspace indistinguishability no-go。

### 局部胶合障碍

**定义。** 取覆盖 \(\{U_\alpha\}\) 及局部 nuisance \(N_\alpha\)，定义局部 residuals
\[
R_\alpha=\Pi_{N_\alpha^\perp,w_\alpha}K|_{U_\alpha},
\]
再定义 overlap mismatch，并把它在允许的局部 nuisance 扩张后最小化，得到 obstruction
\[
\mathrm{Obs}(K).
\]

**环境。** 有限覆盖上的局部—整体拼接问题。
**nuisance quotient。** 允许的局部 gauge 先固定、后最小化。
**observable statistic。** overlap mismatch、扩张前后 obstruction drop、是否被 local nuisance 吸收。
**null model。** 可胶合局部模型；只差一个局部 slope/mean gauge 的伪冲突。
**fast kill test。** 若轻微局部 nuisance 扩张即可吸收 mismatch，则不是 obstruction。
**theorem target。** “可吸收 mismatch 不是几何障碍” 的 no-go 定理。

## 最佳底层对象

我选的**最佳底层对象**不是单个 \(R_t\)，也不是单个 \(\|R_t\|\)，而是：

\[
\mathfrak T
=
\bigl\{(H_s,w_s,N_s,P_s)_{s\in\Sigma},\ (C_\rho)_{\rho:s\to s'}\bigr\}
\]
上诱导出的**有限尺度格商残差传输系统**，其数据是所有局部 residual \(R_s=P_sK_s\)、所有 edge defect \(D_\rho\)，以及所有 square holonomy \(H_\square\)。

把它写成最干净的形式，就是：

\[
H_s=\mathbb R^{X_s},\qquad
P_s=\Pi_{N_s^\perp,w_s},\qquad
R_s(K)=P_sK_s,
\]
\[
D_\rho(K)=C_\rho P_sK-P_{s'}C_\rho K,
\]
\[
H_\square(K)=
\bigl(C_{\rho_2}P_{s_1}C_{\rho_1}P_{s_0}
-
C_{\rho'_2}P_{s'_1}C_{\rho'_1}P_{s_0}\bigr)K.
\]

一个最小但已经足够有力的尺度格可以是：

```text
(q8,b8) ──q-coarsen──> (q4,b8)
   │                       │
 b-coarsen              b-coarsen
   │                       │
(q8,b4) ──q-coarsen──> (q4,b4)
```

如果要再往下压，可以继续接到 `(q2,b4)`、`(q4,b2)`、`(q2,b2)`。这个对象比单尺度 \(R_t\) 更好，原因有四个。

第一，它是**有限维的**。不需要无穷维泛函分析，不需要连续极限，不需要训练、不需要新 loss；只要有限表格、加权内积、投影矩阵、coarsening 矩阵就能完整定义。因此它特别适合 Proposition / Counterexample / Zero-GPU synthetic harness。

第二，它不是“标量指标换皮”。单个 norm 只告诉你“剩余有多大”；而 \(\mathfrak T\) 同时要求**局部形状、跨尺度一致性、路径无关性、维数非退化性**。两个对象可以有一模一样的 \(\|R_s\|\)，但一个在所有边上 \(D_\rho\approx0\)、在所有方格上 \(H_\square\approx0\)，另一个却 path-dependent；这两者显然不是同一个数学对象。

第三，它天然吸收了 bundle 已经明确重视、但还没有统一到底层定义里的东西：rank-shadow guard、same-dimension random subspace、principal-angle stability、coarsening naturality、gluing sanity、projection-evolution leakage。主角与子空间角度之所以适合这里，正是因为 principal angles 可以通过 SVD 的奇异值来表达；而随机同维子空间的自然零分布住在 Grassmann manifold 上。citeturn5view0turn4view2

第四，它和当前 bundle 的负中心主线相容。现有材料已经把单尺度母对象 \(R_t=\Pi_{N^\perp,w}K_t\) 立住了，但也反复提醒：如果只停在这一层，就太容易被 rank-1 shadow、random same-dimension subspace、scale-choice artifact、bad axis、以及 absorbable local mismatch 伪装。因此最佳升级，不是去发明更热闹的词，而是把**“同一对象能否沿尺度格一致运输”**做成真正的一层。

## 定理与禁行议程

下面这组命题里，有些几乎是一行证明，有些需要把 bundle 中零散的方向正式写成 theorem。它们共同组成一个**theorem / no-go agenda**，而不是 dashboard 指标清单。

**秩一影子空洞命题。** 设把多个 residual 向量堆成矩阵 \(M\)。若 \(\mathrm{rank}(M)=1\)，则存在固定模板 \(u\) 与标量轨道 \(c_t\)，使 \(R_t=c_tu\)。于是任何把样本切块后比较 residual subspace 的主角稳定性测试都会退化到同一条直线 \(\mathrm{span}(u)\) 上；换言之，在 rank-1 情形下，“principal-angle stability”几乎天然好看，却没有结构内容。这个命题说明：**\(\sigma_2/\sigma_1\) 不过关时，主角稳定性是空洞指标**。主角与奇异值之间的关系是标准结论。citeturn5view0turn7search8

**方格 holonomy no-go。** 若某个 refinement square 上的每条边都满足 \(D_\rho\equiv0\)，那么该 square 上必有 \(H_\square\equiv0\)。证明直接来自两条路径都等于“把 \(K\) 压到终点尺度后再做终点投影”。反过来，只要某个 square 上测得 \(H_\square(K)\neq0\)，就能严厉推出：至少有一个中间 nuisance family 或一个 coarsening step 不是 functorial 的。这里没有比喻空间；这就是 path dependence 的有限维版本。

**随机同维子空间不可区分命题。** 在 isotropic 的 Grassmannian null 下，固定维数的随机子空间分布对坐标命名是不偏心的；相应 principal angles / capture statistics 的零分布只依赖环境维数与候选维数，而不依赖“你给这个轴起了什么名字”。因此，如果一个自称“真实交互子空间”的对象，在 held-out capture 或 angle gap 上并不优于随机同维子空间，它就不拥有坐标不变的结构特权。关于均匀 Grassmannian 分布与 canonical angles 的维数依赖，已有明确结果。citeturn4view2

**局部胶合可吸收则非障碍命题。** 定义 obstruction 时，必须先固定允许的局部 nuisance 扩张类。若 overlap mismatch 在这类扩张下可被压到零，那么它是 gauge artifact，不是 sheaf/gluing obstruction。这个命题的重要性在于：它要求你先把“允许吸收什么”预注册清楚；否则所谓局部冲突几乎总能被故事化包装。

**粗化—投影非自然性命题。** 对边 \(\rho:s\to s'\)，若 \(C_\rho(N_s)\not\subseteq N_{s'}\) 或 \(C_\rho(N_s^\perp)\not\subseteq N_{s'}^\perp\)，则一般有
\[
C_\rho P_s\neq P_{s'}C_\rho.
\]
这不是审美标准，而是对象同一性的硬条件。只要不自然，所谓“同一 residual 在粗尺度上的表现”就没有被数学保住。

**产品权重边界命题。** 对二阶或高阶 functional ANOVA，若权重是独立/product-type measure 且支撑满，那么 classical Hoeffding/ANOVA 正交分解有天然地位；若权重不是 product-form，则必须退回 generalized / hierarchical projection 的说法，且高阶项解释会耦合、不会再保留同样的 canonical 意义。Hoeffding 的原始分解与后来对 dependent measures 的 generalized ANOVA 都支持这一边界。citeturn8search0turn9view0

把这些命题合在一起，你会发现一个很强的结论：**真正值得证明的，不是“某个 residual 的数值大于零”，而是“对象同一性是否 survives quotient、transport、randomization 与 gluing”**。一旦这些 no-go 全部成立，旧的复杂 collapse narrative 就会被压回更简单的标量/低秩/坐标伪影解释。

## 预注册击杀套件

在任何 full panel、任何训练、任何新 loss 之前，先把 kill suite 立好，而且要**fail-closed**。这也是 bundle 中最成熟、最值得保留的部分：不是“怎样把对象说得更真”，而是“怎样先把它杀干净”。当前脚本与 contract 已经把 allowed verdict 列成一个窄集合：`invalid_artifact`、`killed_by_noise_floor`、`killed_by_random_axis`、`killed_by_rank1_shadow`、`killed_by_coarsening`、`insufficient_artifact`、`eligible_for_next_design_review_only`；并明确把 observed field / LOSO / F3 / glass-box / training / new loss 之类 verdict 设为 forbidden。（bundle：`from_repo/docs/infra/math_turn_20260622/NULL_TESTS_CONTRACT_20260624.md`；`from_repo/scripts/q4_hypercube_interaction_prereg_analysis.py`）

下面是我认为应当直接冻结成 prereg 的 kill matrix：

| 关卡 | 需要的输入 | 失败信号 | fail-closed verdict | 解释 |
|---|---|---|---|---|
| provenance / schema / weights | aggregate metadata、raw hash、schema id、outcome-independent weights | 缺字段、旧 aggregate、权重来源不干净 | `invalid_artifact` | 连对象的样本身份都不稳，讨论结构无意义 |
| full-panel completeness | 5 seeds × 10 generations × 16 cells 的完整性 | 缺 seed、缺 generation、缺 cell | `insufficient_artifact` | 先别谈结构，连载体都没满 |
| matched mean/slope | global mean、q4 slope、方向对齐、sign consistency | 方向一旦 match 就塌 | `killed_by_rank1_shadow` | 说明“对象”只是标量模板阴影 |
| noise floor | interaction/noise median ratio | \(\le 1\) | `killed_by_noise_floor` | 剩余不高于噪声 |
| rank/noise | weighted singular spectrum | \(\sigma_2/\sigma_1<0.25\) | `killed_by_rank1_shadow` | 先过秩，再谈 subspace 稳定性 |
| random equal-size partition | 真 token-position 轴 vs 随机等规模分箱 | 不优于 null | `killed_by_random_axis` | 真轴没有坐标特权 |
| within-q shuffle | q 内 position 标签洗牌 | 统计量不掉 | `killed_by_random_axis` | 标签换一下还差不多，说明不是结构 |
| bad-axis control | `audit_block_id` 等坏轴 | 坏轴也做出同等信号 | `killed_by_random_axis` | 说明是轴选择 artifact |
| same-dim random subspace | 真 9D 或真 2D 子空间 vs 随机同维子空间 | 不优于随机 | `killed_by_random_axis` | 说明只是自由度消费 |
| coarsen/refine naturality | 所有 \(\Delta_\rho=\|D_\rho\|\) | vanishing / flip / unstable | `killed_by_coarsening` | 说明对象在尺度之间不保形 |
| principal-angle holdout | held-out seed / generation blocks | 主子空间任意旋转 | `insufficient_artifact` | 说明没有可迁移的同一对象 |
| gluing sanity | obstruction 扩张前后比较 | 一扩张局部 nuisance 就吸收 | `killed_by_coarsening` 或 `insufficient_artifact` | 说明 sheaf 语言只是空转 |

如果用一句话总结这套 kill suite，就是：**先证明对象没有被 mean、slope、noise、rank-1、random axis、same-dim random subspace、coarsening choice、local gauge 伪造，再允许它进入下一轮设计审查**。这和 bundle 已有 contract 完全一致，只是我把它提升到 transport/holonomy 级别之后，要求它从“坏轴”扩展到“坏路径”。

## 零 GPU 合成 harness

这部分 bundle 其实已经给出一个很好的起点：`residual_transport_holonomy_synthetic.py`。我还在本地按 addendum 脚本重新跑了一次，结果与存档 markdown/json 一致到数值误差范围内。它的价值不是“给 MaoField 加证据”，而是**先把定义、反例、正例的拓扑骨架跑通**。

最先应该实现和冻结的 synthetic controls，我建议保持四个，而且每个都要含**正控**和**反控**：

| 测试块 | 正控 | 反控 | 预期行为 |
|---|---|---|---|
| `scale_square_holonomy` | product weights + additive nuisance at every scale | 在一条路径的中间尺度上塞入 non-functorial nuisance | 正控的 square holonomy 近机器零；反控显著非零 |
| `nuisance_functoriality_digest` | natural coarse nuisance | bad coarse nuisance，只保留粗 q 主效应或只保留一边 nuisance | natural edge defect 近零；bad nuisance edge defect 明显升高 |
| `rank1_angle_vacuity_guard` | genuine two-direction residual family | repeated one-template family | rank-1 的 \(\sigma_2/\sigma_1\) 近零并被杀；多方向对象至少过 `0.25` floor |
| `random_same_dim_angle_gap` | 已知真二维 residual subspace + held-out vector | 1000 个随机同维子空间 | 真子空间的 capture 必须超过随机 p95 |

在 addendum 的已存档合成运行里，四块都通过了：`natural_square_holonomy_norm ≈ 3.14e-16`、`bad_nuisance_square_holonomy_norm ≈ 1.1944`、`natural_edge_relative_defect ≈ 1.64e-15`、`bad_nuisance_edge_relative_defect ≈ 0.4636`、`rank1_sigma2_over_sigma1 ≈ 9.74e-17`、`multidirectional_sigma2_over_sigma1 ≈ 0.2529`、`random_subspace_true_capture = 1.0`、`random_subspace_p95_capture ≈ 0.5965`。我本地重跑得到的数值与之非常接近：例如 natural holonomy 约 `1.57e-16`，multidirectional \(\sigma_2/\sigma_1\) 约 `0.252865`。这说明**定义是可执行的，正反控是可分的，rank floor 也是可机械检查的**；但 strongest allowed verdict 仍然只是 `synthetic_harness_only_no_maofield_claim`。（bundle：`from_repo/docs/infra/math_turn_20260622/RESIDUAL_TRANSPORT_HOLONOMY_SYNTHETIC_RESULT_20260624.md`；`from_repo/scripts/residual_transport_holonomy_synthetic.py`）

这里的策略很明确。先在纯合成世界里把三类反例钉死：
其一，**rank-1 family**，用来证明主角稳定性为什么会空洞。
其二，**bad path / bad nuisance family**，用来证明 holonomy 与 edge defect 的病理感度。
其三，**random same-dimension subspaces**，用来证明“真对象”必须比 Grassmannian null 更好。
只有这些最廉价的 toy counterexample 都讲清楚了，才有资格碰未来 full-panel aggregate。关于随机子空间与 canonical angles 的 Grassmannian 几何，文献已经给出统一分布与维数控制的框架。citeturn4view2

## Mode B 护栏翻译

把上面的 Mode A 数学程序翻回 MaoField 时，必须极其克制。正确翻译方式不是“我们已经找到了 transport/holonomy field”，而是：

**未来若有 provenance-clean 的 full-panel aggregate，可做 evidence-gated 检查；当前不升级任何 MaoField 实证结论。**

具体地，未来的 verdict map 应只允许下面这些句子：

- `invalid_artifact`：metadata、schema、hash、weights provenance、top-level contract 出问题。
- `killed_by_noise_floor`：interaction/residual 不高于噪声地板。
- `killed_by_random_axis`：真轴、真子空间、真路径并不优于随机轴、坏轴、随机同维子空间。
- `killed_by_rank1_shadow`：\(\sigma_2/\sigma_1\) 过低，或 matched mean/slope 已吸收掉所谓对象。
- `killed_by_coarsening`：edge defect / square holonomy / gluing sanity 不过关。
- `insufficient_artifact`：缺 full panel、缺 null blocks、缺 holdout、缺稳定性证据。
- `eligible_for_next_design_review_only`：所有 prereg gates 都过，但仍只是下一轮设计审查资格。

绝对不该允许的 verdict 仍然是：

- `interaction_field_observed`
- `hypercube_residual_observed`
- `residual_field_observed`
- `LOSO_passed`
- `F3_positive`
- `glass_box_broken`
- `training_authorized`
- `new_loss_authorized`

因此，把本报告翻回当前 MaoField 的**唯一合法 Mode B 结论**，仍然只有两句：
当前 `stable non-scalar residual object = insufficient_artifact`；当前 `existing interaction smoke = smoke_conjecture_only`。
任何再往上的说法，都会违反 bundle 内已经锁死的 fail-closed contract。（bundle：`from_repo/STATE.md`；`from_repo/docs/infra/math_turn_20260622/NULL_TESTS_CONTRACT_20260624.md`；`from_repo/scripts/q4_hypercube_interaction_prereg_analysis.py`）

## 给 PI 的初中版解释与最终裁决

给非技术 PI 的版本可以非常简单：

现在你们手里有一把**尺子雏形**。这把尺子会把一张很多格子的表，先减去“最普通的背景”——总平均、行效应、列效应、平滑趋势——看看还剩什么。

但“减完还有剩余”，**不等于**“藏着一个真的结构”。因为剩余可能只是：

- 同一张模板忽亮忽暗；
- 随便换个分箱方法也能做出来；
- 把标签打乱后还差不多；
- 一旦把表格粗化，就立刻消失；
- 或者只是局部模型没对齐，但稍微改一下局部背景就能吸收掉。

所以 smoke 的真正含义只是：**尺子能拿起来比一比**。它不表示“已经量到了隐藏结构”。这正是 bundle 当前所有 guardrails 的共同意思：先证明尺子不会把噪声、随机轴、低秩影子、坏路径和可吸收局部误差错认成“对象”，再说下一步。

**教授最终裁决：我选择 E——拆分成一个与 MaoField 独立的去品牌化新项目。**

我选 E，而不是 A、B、C、D，原因如下。

A 不够好，因为现在不缺抽象词，缺的是一个**可证明、可反例、可 fail-closed** 的有限维对象；单做纯抽象，很容易再次滑回“漂亮命名”的陷阱。
B 也不够好，因为虽然更多零 GPU contracts 仍然必要，但 bundle 自己已经指出：最值得保留的东西不再是 MaoField 品牌，而是一个更一般的 operator / no-go program。
C 现在不成立，因为 evidence boundary 明确不允许请求 full-panel generation 作为当前主建议。
D 又过头了，因为现有 addendum 说明**数学对象的骨架本身是活的**；死的主要是当前 MaoField Mode B 的实证升级想象，不是整个问题。
所以最干净的路线，就是 E：把问题改写成一个去品牌化的新项目，例如“**有限尺度格上的加权商残差传输、方格 holonomy 与 no-go 分类**”。

这个新项目的最终目标，可以用一句话概括：

> 在去掉标量指标、主效应、decode 伪影、平滑趋势、预注册 nuisance 与坐标自由之后，是否还存在一个稳定的、非标量的、可跨尺度一致运输的 residual object？

如果**存在**，它揭示的将不是“玻璃盒被打破”这类旧叙事，而是一个更朴素也更硬的限制：某种 degeneration / recovery / interpretability / control 现象里，确实有一个**不能被均值、主效应、单模板轨道、随机轴或局部 gauge 吸收**的结构剩余。
如果**不存在**，那同样是强结论：它会把很多复杂 collapse narrative 统一压回几类 no-go——噪声地板、rank-1 scalar shadow、random-axis artifact、coarsening non-naturality、或 absorbable gluing mismatch。那时你得到的不是“没发现任何东西”，而是一个更有杀伤力的结论：**旧叙事没有对象同一性，它们只是标量投影的扩音器。**