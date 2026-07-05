# MaoField Metric-Identity Phase II 深度研究报告

## Evidence Intake Verdict

结论是：**支持当前状态，但只支持一个严格收缩后的、以有限对象为核心的研究起点**。就包内证据而言，当前可安全确认的不是“广义 MaoField 理论已经完成”，而是更窄的六件事：公开的 Open-MaoField 表面存在；正式 Zenodo 预印本 DOI 被记录为 `10.5281/zenodo.21190475`；仓库/软件 DOI 被记录为 `10.5281/zenodo.21157578`；现有数学结果限定在**有限正权二向表**；`2×2` 精确有理见证是证书级证据；浮点 harness 只是回归支持，不是证明；同时，Mode B 仍是 `insufficient_artifact`，duplicate risk 仍是 `MEDIUM`。（`PACKAGE_README.md`; `from_repo/STATE.md`; `from_repo/docs/infra/MAOFIELD_METRIC_IDENTITY_PROGRAMME_ADOPTION_NOTE_20260704.md`; `from_repo/docs/infra/OPEN_MAOFIELD_FORMAL_ZENODO_PREPRINT_PUBLISHED_20260704.md`; `public_open_maofield_snapshot/README.md`）公开 GitHub 页面也独立显示该仓库存在、处于 public 状态、镜像了两个 DOI、并带有一个 `v1.0.0` release 标记。citeturn2view0

最关键的决定性文件链条有八个。第一，`PACKAGE_README.md` 给出了读序、证据边界、RAG 仅作 locator 的规则，以及对“禁止主张”的总锁。第二，`from_repo/STATE.md` 把 live status、DOI、Mode B、duplicate risk、公共仓库记录放到同一状态源里。第三，`from_repo/docs/infra/MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md` 把 Phase II 的目标明确收缩为“metric-object identity problem”，并提出了 chart、transport、defect、OI 等后续对象。第四，`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 给出了当前数学主脊柱：有限正权二向表、`A` 与 `B_0` 的正交条件、顺序缺陷算子 `D_w`、以及非 product 情形下的 pure-main-effect witness。第五，`EXACT_WITNESS_V1_4_20260629.md/json` 提供了当前精确证书。第六，`SYNTHETIC_HARNESS_V1_3_20260628.md` 明确锁死了 harness 的角色边界。第七，`V2_5_FINAL_SYNTHESIS_*` 与 `MAOFIELD_PREPRINT_V2_5_FINAL_SYNTHESIS_20260703.tex` 说明论文面措辞已被压到有限 obstruction 的口径。第八，`OPEN_MAOFIELD_FORMAL_ZENODO_PREPRINT_PUBLISHED_20260704.md` 与公共快照 README 共同形成了 publication state 的包内证据面。（以上文件）

当前包里最坚固的数学核并不是“一个哲学命题”，而是一个具体有限结果：在有限正权二向表上，
\[
w \text{ 为 product} \iff A \perp B_0 \iff D_w=0 \iff R_{Q\to B}=R_{B\to Q},
\]
并且在非 product 权重下，存在纯主效应见证 \(K\in A\) 或 \(K\in B_0\)，满足真加性残差为零，但错误顺序的 sequential stripping 输出非零；因此该非零输出只能被解释为**procedure artifact**，而不是 true interaction / true residual。（`FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`; `MAOFIELD_PREPRINT_V2_5_FINAL_SYNTHESIS_20260703.tex`; `EXACT_WITNESS_V1_4_20260629.md`; `public_open_maofield_snapshot/docs/claim_boundary_note.md`）公共仓库 README 也镜像了同样的窄口径陈述与 `2×2` 数值证书。citeturn2view0

现有精确证书足够支撑“最小阻碍”这一说法。包内给出的主见证是
\[
w=\frac1{11}\begin{pmatrix}1&2\\3&5\end{pmatrix},\quad
K=\left(\frac7{11},-\frac4{11},\frac7{11},-\frac4{11}\right),
\]
满足 \((I-P_N)K=0\)、\(R_{B\to Q}K=0\)，但
\[
R_{Q\to B}K=\left(\frac1{32},\frac5{168},-\frac1{96},-\frac1{84}\right),
\quad \|R_{Q\to B}K\|_w^2=\frac{61}{177408}.
\]
这正是“同一个 intended residual object 在不同程序顺序下并不自动同一”的最小有限反例。（`EXACT_WITNESS_V1_4_20260629.md`; `exact_witness_v1_4_20260629.json`; `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`; `MAOFIELD_PREPRINT_V2_5_FINAL_SYNTHESIS_20260703.tex`）

缺失的东西同样很明确，而且这些缺失决定了本次报告必须保守。包里**没有**任何可支持经验正结果的 live multi-chart artifact；没有冻结好的真实 LLM chart 对比数据；没有“全套 metric identity transport calculus”的正式系统；没有超出当前 `2×2` 证书的 exact certificate library；也没有能把 duplicate risk 从 `MEDIUM` 合法下调的外部权威元数据总审计。包内文件自身反复要求：旧 MaoField empirical line 只能作为 deflated motivation，不能升级为 positive result；bibliography 在若干条目上仍需要外部 authoritative metadata pass。（`PACKAGE_README.md`; `from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md`; `public_open_maofield_snapshot/docs/duplicate_risk_note.md`; `deep_research_v21_package_usage_audit_report22_20260703.md`; `deep_research_formal_preprint_v2_2_strict_review_report23_20260703.md`）

## Minimal Safe Programme Statement

MaoField Phase II 当前最安全、也最有力量的表述，不是“已经发现了某种 LLM 残差场”，而是：**在什么有限、可审计的条件下，不同黑箱评估 chart 中的 metric outputs 才能被当作同一个测量对象**。现有 Open-MaoField 结果只提供了这个更大纲领的第一枚精确楔子：在有限正权二向残差审计表中，若权重不是 product form，则顺序化 nuisance stripping 可能从纯主效应信号制造出非零 residual-like output。那一输出因此不是自动的 model property，而首先是一个 chart-dependent object。换言之，score、residual、ranking、capability claim 都不应先天地被当成模型内在属性；它们首先是由 prompt protocol、task structure、judge、rubric、decoding、weights、aggregation 与 residualization 共同生成的测量对象。（`from_repo/docs/infra/MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md`; `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`; `MAOFIELD_PREPRINT_V2_5_FINAL_SYNTHESIS_20260703.tex`; `public_open_maofield_snapshot/docs/claim_boundary_note.md`）

因此，Phase II 的正确任务不是把旧 finite theorem 夸大成 broad theory，而是把它用作**最小 obstruction**：它说明“同一性不是免费的”。下一步要做的是，把 chart-dependent metric object、identity、transport、invariance、defect certificate、audit-order instability 这些对象正式化，并建立一个 exact certificate library，再在零 GPU、审计优先的边界内设计 protocol v0.1。这样做与现有文献位置并不冲突：现有广义 ANOVA / Hoeffding-Sobol / Shapley / two-projection 文献已经很密集，而 HELM、BIG-bench、LLM-as-a-judge、benchmark contamination、benchmark robustness 也已经占据了大量评估讨论空间；MaoField 若要保持自己的空位，只能把贡献保持在“**chart identity condition + finite obstruction certificate + audit discipline**”这个窄而硬的组合上。citeturn13search0turn11search0turn11search1turn14search0turn11search11turn11search13turn12search2turn12search4turn15search1turn15search5turn9search0turn9search1turn9search2

## Formal Definitions Draft

### Evaluation chart

建议把用户给出的 provisional notation 进行一次有限且更清楚的分离。最干净的写法是把**chart**与**被评估 roster**分开：

\[
c=(P,T,J,R,D,w,A_g,N),
\qquad \mathcal S=\{\sigma_1,\dots,\sigma_M\}.
\]

这里 \(P\) 是 prompt / protocol 分布，\(T\) 是任务或域结构，\(J\) 是 judge / evaluator 机制，\(R\) 是 rubric / score map，\(D\) 是 decoding / output protocol，\(w\) 是采样或聚合权重，\(A_g\) 是 aggregation rule，\(N\) 是 nuisance-stripping / residualization scheme，而 \(\mathcal S\) 单独保存被评估的模型、版本或系统 roster。这样做的好处是：**单模型分数对象**与**多模型排名对象**不再被混成一个符号系统。（这是对用户 provisional chart 的有限 refinement；依据 `MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md` 中 chart notation 的精神，但把 roster 从 chart 本体中分离出来，从而更利于定义 ranking object。）（`from_repo/docs/infra/MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md`; `MAOFIELD_METRIC_IDENTITY_PROGRAMME_ADOPTION_NOTE_20260704.md`）

为了保证“有限、可审计”，对每个 chart 固定一个有限 cell index set \(I_c\)。在最小设定下，\(I_c\) 可以是 prompt-cell、task-cell、judge-cell、decoding-stratum 的有限索引集合，而不是“所有可能文本”的无限空间。对每个系统 \(\sigma\in\mathcal S\)，令
\[
K_c(\sigma)\in \mathbb R^{I_c}
\]
表示在该 chart 下冻结后的原始 score tensor 或 audit table。这样，所有后续对象都可以回到一个有限维线性空间上处理。（`FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 的有限加权表脊柱提供了这种有限对象化的模板；`MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md` 则把它推广为 chart programme。）

### Chart-dependent metric object

最小而干净的定义不是“一个数”，而是一个**chart-indexed processed object**。令
\[
\Phi_c:\mathbb R^{I_c}\to \mathcal O_c
\]
为由 \(R,w,A_g,N\) 共同确定的有限可审计处理算子。则单系统的 chart-dependent metric object 定义为
\[
M_c(\sigma):=(c,\Phi_c(K_c(\sigma))).
\]

这里 \(\mathcal O_c\) 不必是标量空间；它可以是分数向量、残差向量、排序前的多维 summary、或者排名证据对象。只有当 \(\mathcal O_c=\mathbb R\) 时，\(M_c(\sigma)\) 才退化为一个单标量。对于排行榜这类 roster-dependent 对象，建议单独写成
\[
M^{\mathrm{rank}}_{c,\mathcal S}
:=\operatorname{Rank}\big(\Phi_c(K_c(\sigma_1)),\ldots,\Phi_c(K_c(\sigma_M))\big).
\]
这样就避免了把“单模型对象”和“依赖竞品 roster 的顺序对象”误认成同一种对象。（`MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md` 已明确提示 score / residual / ranking / diagnostic 应统一视作 chart-dependent object family。）

这个定义的关键含义是：**数字只是 object 的一个表现层，不是 object 本身**。同一个数值可以来自完全不同的 chart operator；而不同 chart 下的同名“reasoning score”即使都写成一个小数，也并不自动是同一个 measurement object。（`MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md` 关于 measurement-object identity problem 与 metric-form fetishism 的定义段）

### Identity, transport, invariance condition

两个 chart 下的输出若要被合法地称为“同一个对象”，不能靠“名字相同”或“数值接近”；需要一个**lossless, chart-declared, coherent transport**。在有限对象化之后，最自然的正式条件是：存在原始表上的 transport
\[
U_{c\to c'}:\mathbb R^{I_c}\to \mathbb R^{I_{c'}}
\]
和对象空间上的 transport
\[
T_{c\to c'}:\mathcal O_c\to \mathcal O_{c'}
\]
使得在一个声明好的 admissible class \(\mathcal K_{c,c'}\) 上，
\[
T_{c\to c'}\circ \Phi_c
=
\Phi_{c'}\circ U_{c\to c'}.
\]

若要称为**同一对象**，还应至少再要求三件事。第一，\(T_{c\to c'}\) 在相关像空间上应是可逆的；否则那更像比较或压缩，而不是 identity transport。第二，transports 应满足 coherence：
\[
T_{c\to c}=\mathrm{id},\qquad
T_{c'\to c}=T_{c\to c'}^{-1},\qquad
T_{c'\to c''}\circ T_{c\to c'}=T_{c\to c''}.
\]
第三，这个条件应对一个 chart-class 或 system-class 成立，而不是只在单个模型、单个数据点上偶然成立。

**仅仅“可比较”**则弱得多。若只存在一个样本内的单调标定、一个 order-preserving rescaling、或一个把两边都压到共同 summary 的比较映射，那只能说明“numbers are comparable in some reduced sense”，不能说明“objects are identical”。这一点正是 MaoField Phase II 最需要防止的偷换。（`MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md`; `MAOFIELD_METRIC_IDENTITY_PROGRAMME_ADOPTION_NOTE_20260704.md`）

当前 finite order-defect theorem 正好是这个框架的第一个特例：在同一有限加权表上，原始空间 transport 与对象空间 transport 都是恒等映射，而两个程序 \(\Phi_c,\Phi_{c'}\) 分别由 \(R_{Q\to B}\) 与 \(R_{B\to Q}\) 给出；非零
\[
D_w=R_{Q\to B}-R_{B\to Q}
\]
就是 intertwining failure 的 exact certificate。（`FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`; `EXACT_WITNESS_V1_4_20260629.md`; `MAOFIELD_PREPRINT_V2_5_FINAL_SYNTHESIS_20260703.tex`）

### Defect certificate

建议把 defect certificate 直接定义成一个**有限 witness quadruple**：
\[
\mathcal C=(c,c',K,\Delta),
\qquad
\Delta:=T_{c\to c'}M_c(K)-M_{c'}(U_{c\to c'}K).
\]

当 \(\Delta\neq 0\) 时，它就证明了：至少对这个 witness 而言，两边不是同一对象。证书必须附带四种元数据：使用的 chart 声明；transport 声明；witness 本体；范数或序关系下的 defect 大小。这样 defect 不再是松散的“感觉不稳定”，而是一个能被重算、能被版本控制、能被 exact arithmetic 固化的对象。

在当前包里，最小 defect certificate 就是
\[
(c,c',K,D_wK),
\]
其中 \(c\) 与 \(c'\) 只差 residualization order，\(K\in B_0\)，\((I-P_N)K=0\)，但 \(D_wK\neq0\)。这已经足以说明：**wrong-order residual-like output 不是 free residual object**，而是程序依赖物。（`FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`; `EXACT_WITNESS_V1_4_20260629.md/json`; `public_open_maofield_snapshot/docs/claim_boundary_note.md`）

### Audit-order instability

`OI(w)=||D_w||` 只有在**域、陪域、范数**都先被说清楚时才诚实。最适合当前 programme 的正式定义不是无下标的 \(\|D_w\|\)，而是至少区分两个版本。

第一个版本是**受限算子型**：
\[
OI^{\mathrm{op}}_{N}(w)
:=
\big\|D_w\!\restriction_{N_{\mathrm{add}}}\big\|_{L^2(w)\to L^2(w)}.
\]
它只看 additive nuisance subspace 上的 order defect，因此恰好测量“从本应被视为 nuisance 的成分中，程序顺序最多能制造多大的假残差”。

第二个版本是**点态证书型**：
\[
OI^{\mathrm{pt}}_{w}(K)
:=
\frac{\|D_wK\|_w}{\|K\|_w},
\qquad K\neq0,
\]
若特别想对“零真加性残差的主效应 witness”做审计，可再限制 \(K\in A\cup B_0\)。这会让 `OI` 明确变成**程序不稳定性指数**，而不是 capability score、也不是 model property。按照现有 theorem spine，一个很自然的 next-step proposition 就是：
\[
OI^{\mathrm{op}}_{N}(w)=0 \iff w \text{ 为 product form}.
\]
因为 product 时 \(D_w=0\)；非 product 时，Prop. 3 已保证存在 \(K\in A\) 或 \(K\in B_0\subset N_{\mathrm{add}}\) 使 \(D_wK\neq0\)。（`FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`; `MAOFIELD_METRIC_IDENTITY_PROGRAMME_ADOPTION_NOTE_20260704.md`）

### Metric-form fetishism

若要把“metric-form fetishism”正式化，最干净的写法是把它定义为一种**未经许可的 quotienting**。设报告系统试图把 charted object family
\[
\{M_c(\sigma)\}_{c,\sigma}
\]
压到一个 chart-free latent claim \(\theta(\sigma)\in\Theta\)。如果在没有证明一族相容 transports / invariances 的前提下，就把不同 chart 下的 objects 直接通过某个报告映射 \(q_c:\mathcal O_c\to\Theta\) 识别为“同一个模型属性”，那么这一步就是 metric-form fetishism。它不是“指标错了”这么简单，而是：

\[
\text{heterogeneous measurement relation}
\longrightarrow
\text{chart-free model property}
\]

中间缺失了正当的 transport / invariance proof，却先完成了本体化。

因此，metric-form fetishism 的正式反面不是“多做一些 benchmark”，而是：**先把 chart-indexed objects 留在原位，再证明何时可以合法取商**。这正是 current package 最反复强调的 programme discipline。（`MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md`; `MAOFIELD_METRIC_IDENTITY_PROGRAMME_ADOPTION_NOTE_20260704.md`）

## Theorem / Counterexample Candidates

下表只列**值得继续推进**或**必须明确拒绝**的候选对象；状态标签含义分别为 `PROVABLE_NOW`、`PLAUSIBLE`、`SPECULATIVE`、`BAD_IDEA`。

| Candidate | Status | 核心命题 | 需要的假设 | 精确有限对象 |
|---|---|---|---|---|
| Restricted nuisance-subspace instability theorem | **PROVABLE_NOW** | 定义 \(OI^{\mathrm{op}}_{N}(w)=\|D_w\!\restriction_{N_{\mathrm{add}}}\|_{op,w}\)。则 \(OI^{\mathrm{op}}_{N}(w)=0 \iff w\) 为 product form。 | 仅需当前 formal note 的有限正权二向表设定与 Prop. 1–3。 | 任意有限正权二向表；当前 `2×2` 见证已给出非零端。 |
| Rank preservation under bounded transport error | **PROVABLE_NOW** | 对有限 roster \(\mathcal S\)，若两 chart 的 transported score vectors 满足 \(\|T_{c\to c'}s_c-s_{c'}\|_\infty < \gamma/2\)，其中 \(\gamma\) 是所有相邻可区分分数的最小 gap，则 ranking 不变。 | 分数型对象；固定 roster；无 tie 或 tie 规则已冻结。 | 三模型两个 chart 的有理数 score 向量即可。 |
| Scalar coincidence is not identity | **PROVABLE_NOW** | 存在 \(c\neq c'\) 与 \(\sigma_1,\sigma_2\)，使 \(M_c(\sigma_1)=M_{c'}(\sigma_1)\) 但 \(M_c(\sigma_2)\neq M_{c'}(\sigma_2)\)。因此单点数值相等不构成 object identity。 | 只需两个不同 chart operators；不需概率极限。 | 二模型、双 chart、两个不同线性 functionals 即可构造。 |
| Near-product perturbation bound | **PLAUSIBLE** | 在正权 simplex 的紧内点上，\(OI^{\mathrm{op}}_{N}(w)\) 对 \(w\) 局部连续，且应存在 \(OI^{\mathrm{op}}_{N}(w)\le C\,\mathrm{dist}(w,\Pi_{\mathrm{prod}})\) 的局部界。 | 需要补一段投影矩阵对权重的有理/光滑依赖证明。 | 建议从 `2×2` 或 `2×3` 有理权重族 \(w_\varepsilon\) 开始。 |
| Judge-order corollary | **PROVABLE_NOW** | 现有 theorem 对坐标标签完全无偏；把 \(Q\) 与 \(B\) 重新解释为 prompt-axis 与 judge-axis，即得 judge-order toy obstruction。 | 仅需把当前二向表定理做语义重命名。 | 可直接复用现有 `2×2` exact witness。 |
| Universal latent-capability identity theorem | **BAD_IDEA** | 试图在缺乏 transport calculus 与真实多 chart artifact 的情况下证明“benchmark score 就是模型内在能力”。 | 假设过强且与包内边界矛盾。 | 不应推进。 |

其中，**最小、最值得立即写成一页短 note 的新命题**是第一个：`restricted nuisance-subspace instability theorem`。它几乎不需要新增理论重负，却能把当前“存在性反例”提升为一个正式指数对象：不再只是“有一个 witness 会坏”，而是“这个 chart 的 nuisance-order instability 可以被定义、归零、比较”。这一步很小，但对 Phase II 非常关键，因为它把 obstruction 变成了可在 future audit protocol 中复用的对象。（依据当前 formal note 与 programme note）

第二个优先对象是 ranking lemma。它不碰经验正结果，也不要求新数据，却能严格说明：**两 chart 的 ranking 是否能被当成同一 ranking object，不是看两串数字“差不多”，而是看 transport defect 是否被 roster gap 吸收掉。** 这正贴合用户问题中的 scores / rankings / capability claims 三种对象层级。

第三个值得保留但暂不宣称“已可证明”的对象，是 near-product bound。它一旦成立，会把 Engels 式“量变到质变”的 programme 直译成一个可审计数学句子：product manifold 附近的小权重偏离如何导致 order defect 的小但非零增长。（`MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md` 已提出 near-product perturbation bounds 与 commutator norm instability index 的方向）

## Certificate Library Plan

下一库不应只是“多放几个例子”，而应是**一组按 claim boundary 分层的 exact certificates**。建议所有条目统一包含：chart declaration、有限 cell set、权重表、basis / subspace 描述、有关投影矩阵或 transport、witness、defect、范数、negative control、forbidden interpretation、以及一个 machine-readable exact artifact。当前最合适的组织方式如下。

| Library item | 目标 | 建议有限对象 | 预期产出 |
|---|---|---|---|
| Existing `2×2` non-product order defect | 保留当前最小 obstruction 主证书 | 现有 \(w=\frac1{11}\begin{pmatrix}1&2\\3&5\end{pmatrix}\) 与 \(K\in B_0\) | exact JSON、Markdown、脚本、claim boundary；作为全部后续条目的锚点 |
| Product control | 给出“零缺陷”对照 | 建议 `2×3` exact product table，例如由两行三列的有理边际外积构成 | 明确展示 \(D_w=0\)、\(OI^{\mathrm{op}}_{N}(w)=0\)、两种 stripping 与 true residual 完全一致 |
| Near-product perturbation | 做出“接近零但不为零”的家族证书 | 建议 `2×2` 或 `2×3` 的有理参数族 \(w_\varepsilon=w_0+\varepsilon H\)，保持正性并尽量保持边际 | 一个 exact family，展示 defect 如何从零平滑长出；为 local bound 做实验性导向，但不把数值图当证明 |
| Judge-order toy | 把 theorem 直接翻译到 judge axis | 复用现有 `2×2` 代数对象，只把行列标签重命名为 prompt × judge | 说明 judge-first / prompt-first stripping 可在纯 judge main effect 上制造 residual-like artifact |
| Contamination coupling toy | 让 contamination 成为 chart axis，而不是事后解释词 | 建议 `2×3`：行是 fresh / exposed，列是 verbatim / paraphrase / mixed 或相近离散轴 | 一个 exact rational toy，展示 contamination coupling 与权重/聚合如何改变对象身份，而不是只改变分数大小 |
| Ranking instability toy | 把 object identity 从 residual 推到 ranking object | 三模型、双 chart 的有理数 score vectors，含一个可控 gap \(\gamma\) | 一个 exact rank-flip / rank-preservation pair，配套稳定性引理与 failure certificate |

这里最重要的纪律是：**语义标签可以变化，但 algebraic claim boundary 不变**。judge-order toy、contamination toy、ranking toy 都不能被写成“已观察到真实 judge bias / contamination / leaderboard pathology”；它们只能是**finite chart certificates**，用于证明这些对象有可能不是同一 measurement object。这样的 library 才会服务于 Phase II，而不是重新滑回“先看现象、再补解释”的旧路径。（`MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md`; `MAOFIELD_METRIC_IDENTITY_PROGRAMME_ADOPTION_NOTE_20260704.md`; `public_open_maofield_snapshot/docs/claim_boundary_note.md`）

我建议库的技术顺序不是按“最酷”排，而是按“最能封堵误解”排：先 product control，再 restricted instability index，再 near-product family，再 judge / contamination semantic relabels，最后才是 ranking toy。原因很简单：如果没有 product control 与 zero-defect baseline，任何后续 nonzero effect 都容易再次被误读为“发现了一个 field”。当前 package 的整个治理结构，正是在防这种滑移。（`PACKAGE_README.md`; `SYNTHETIC_HARNESS_V1_3_20260628.md`; `V2_5_FINAL_SYNTHESIS_RELEASE_GATE_NOTE_20260703.md`）

## Literature and Duplicate-Risk Map

在数学邻域里，**最近的先占文献不是 MaoField，而是 dependent-input decomposition 系列**。Hooker 2007 已经研究 dependent variables 下的 generalized functional ANOVA；Chastaing、Gamboa、Prieur 的 2012 与 2015 工作把 dependent-variable Hoeffding-Sobol decomposition 与 generalized Sobol sensitivity methods 做成了正式对象；Owen 与 Prieur 2017 又把 dependent inputs 下的 importance allocation 推向了 Shapley 框架；Il Idrissi 等 2025 进一步从 projector characterizations 的角度讨论 dependent random variables 的 Hoeffding decomposition；Lamboni 2026 也已明确进入 non-independent ANOVA-type decompositions。**因此 MaoField 绝不能声称自己开启了 dependent-input ANOVA / Hoeffding / Sobol / Shapley 的新理论。** 它的安全区别只能是：把一个有限加权 chart 的 exact obstruction，嵌回 black-box evaluation 的 measurement-object identity discipline。citeturn13search0turn11search0turn11search1turn14search0turn11search11turn11search13

第二个高密度邻域是**two-projection / two-subspace theory**。Böttcher 与 Spitkovsky 的综述明确把“两投影理论”的基本结果系统化了；Corach 与 Maestripieri 则正面研究 orthogonal projections 的乘积与 polar decomposition。也就是说，`P_{B_0}P_A-P_AP_{B_0}` 这种 commutator 结构本身并不新。MaoField 的安全位置不应是“发现了 projection noncommutativity”，而应是：**在有限 residual metric audit chart 中，给出一类 exact, audit-facing use of that obstruction**。这使它依旧有位置，但这个位置必须窄。citeturn12search2turn12search4

在 LLM evaluation 邻域里，HELM 与 BIG-bench 已经把“多任务、多指标、广覆盖 benchmark”这个空间铺得很开；MT-Bench / Chatbot Arena 把 open-ended judge-based evaluation 推到中心位置，并明确讨论了 position、verbosity、self-enhancement 等偏差；后续工作又进一步单独量化了 position bias、自偏好 bias 与 preference leakage 等 judge-side 失真。于是 MaoField 不能把自己的 novelty 讲成“LLM 评估依赖 judge、依赖 benchmark，因此不可靠”；这些已经是现成邻域。它真正能新增的，只能是：**什么时候这些来自不同 chart 的 judge outputs 与 leaderboard outputs 还有资格被当成同一个 measurement object**。citeturn15search5turn15search1turn9search0turn10search4turn10academia18turn10academia17turn10search2

benchmark contamination 与 benchmark robustness 文献又进一步缩小了可主张空间。rephrased-sample contamination 工作显示，简单 string-based decontamination 可以被翻译或改写轻易绕过；distributional-assumption 工作则表明，benchmark 内 prompt correlations 与 sampling assumptions 会实质改变模型排名。换句话说，MaoField 若想面对“contamination coupling”“ranking instability”“chart dependence”等主题，它并不是第一个发现这些字面风险的人。它唯一可能保持 `MEDIUM` 而不是升到更高 duplicate risk 的路径，是把贡献锁在：**有限 chart identity condition、exact obstruction certificate、与 audit-order discipline**。在现有文献版图下，把 duplicate risk 继续维持在 `MEDIUM` 是合理的；下调到 `LOW` 没有足够依据，上调到 `HIGH` 暂时也缺少 direct duplicate 证据。citeturn9search1turn9search2turn10search4turn10academia18turn10academia17turn11search0turn12search2

因此，这一节的综合判断与包内自审完全一致：**duplicate risk 保持 `MEDIUM`**。理由不是“已经发现 exact duplicate”，而是“广义理论、projection theory、judge-bias、benchmark robustness、contamination 这些大块已被占据；一旦措辞膨胀，立刻会与邻域重叠”。公共仓库 README、包内 duplicate-risk note，以及上述外部主文献共同支持这一判断。（`public_open_maofield_snapshot/docs/duplicate_risk_note.md`; `from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md`）citeturn2view0turn11search0turn12search2turn15search5

## Residual Metric Audit Protocol v0.1

这个 protocol 必须是**零 GPU、审计优先、负控制先行**。它的目的不是“证明某模型有某能力”，而是先检查：一个被报告出来的分数、残差或排名，到底有没有资格被当成稳定 object。建议把 v0.1 固定成下面七步。

1. **Chart freeze**  
   先把 chart 写死：\(P,T,J,R,D,w,A_g,N\) 与 roster \(\mathcal S\) 的每一项都要有机器可读 manifest。没有 frozen chart，就没有后续 object identity 讨论。

2. **Finite cell tensor extraction**  
   把原始评估日志压成有限 \(I_c\) 与 \(K_c(\sigma)\)。judge prompt、judge response、rubric map、aggregation weights、tie rules、sampling exclusions 都必须落到 artifact 里，而不是只留在文字说明里。

3. **Primary negative controls**  
   在任何 real-chart 比较之前，必须先跑四类负控制：  
   - exact product-weight control；  
   - order-commuting control；  
   - label-swap / axis-renaming sanity control；  
   - ranking-gap sanity control。  
   如果这些控制都不过，后面任何 chart claim 都不应该进入 interpretation。

4. **Defect layer**  
   对每个拟比较对象，显式计算或声明 defect：  
   \[
   \Delta_{c,c'}(\sigma)=T_{c\to c'}M_c(\sigma)-M_{c'}(\sigma).
   \]
   若 transport 根本无法声明，则报告应先写“identity not yet licensed”，而不是直接给 capability conclusion。

5. **Instability layer**  
   对残差类对象报告 \(OI^{\mathrm{op}}_{N}(w)\) 或 \(OI^{\mathrm{pt}}_w(K)\)；对 ranking 类对象报告最小 gap \(\gamma\)、\(\infty\)-norm transport defect、以及是否满足 rank-preservation bound。所有这些量都应被写成**程序不稳定性量**，而非模型能力量。

6. **Semantic-axis probes**  
   judge-axis、contamination-axis、aggregation-axis、prompt-distribution-axis 的 probes 只能做成 finite audit comparisons。它们的输出是“identity preserved / identity not licensed / defect certified”，而不是“发现某种真实内部机制”。

7. **Paper-safe output schema**  
   最终输出必须区分四栏：`proven facts`、`package-supported operational claims`、`conjectures`、`future work`。如果 empirical artifacts 不足，结论必须停在 `insufficient_artifact` 或更窄的 audit label，而不能偷渡到 positive result。

这个 v0.1 至少要明确三类**negative controls**。其一，现有 exact `2×2` 非 product 证书与一个 matching product control 要并列出现，防止“凡有非零 defect 就叫发现了新结构”。其二，judge / contamination / ranking toys 必须至少包含一个语义 relabel 版 exact control，证明 effect 来自 chart algebra，而不是解释者的故事。其三，任何 ranking comparison 都必须报告 tie policy 和最小 gap；否则“排名变化”很容易只是未冻结的排序规则造成的对象混淆。（`MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md`; `SYNTHETIC_HARNESS_V1_3_20260628.md`; `public_open_maofield_snapshot/docs/claim_boundary_note.md`）

这个 protocol 还必须内置**forbidden interpretations**。不允许写“观测到了 MaoField residual / interaction / transport / holonomy / metric field”；不允许写“full panel 已跑”“训练或新 loss 获批”；不允许把 harness 或 JSON 浮点输出写成 theorem proof；不允许把 judge-axis instability 直接提升为“模型本体偏差”；不允许把 contamination coupling 直接提升为“模型记忆机制已被证明”；也不允许把 ranking instability 直接提升为“leaderboard 全部失效”。这些禁令不是修辞洁癖，而是当前 programme 免于再次回到旧路线的实际防护墙。（`PACKAGE_README.md`; `STATE.md`; `V2_5_FINAL_SYNTHESIS_RELEASE_GATE_NOTE_20260703.md`; `OPEN_MAOFIELD_FORMAL_ZENODO_PREPRINT_PUBLISHED_20260704.md`; `public_open_maofield_snapshot/docs/claim_boundary_note.md`）

## Requests to Node36 Codex and Next Decision

### Requests to Node36 Codex

当前包**足够支持本次报告**，所以没有 blocking request；但若要把“next rigorous stone”从定义推进到新定理或新证书，下面两项补件会明显降低证明风险。

```text
REQUEST_TO_NODE36_CODEX:
- path or file category: any existing finite 2x3 / 3x3 exact-certificate notes, scripts, scratch markdowns, or JSON artifacts under docs/infra/ or scripts/
- why needed: to determine whether product controls, near-product perturbation toys, judge-order toys, contamination-coupling toys, or ranking-instability toys already exist in bounded primary form
- claim tested: whether the certificate library can be advanced immediately beyond the current 2x2 witness without inventing new package-external evidence
- blocking or optional: optional
```

```text
REQUEST_TO_NODE36_CODEX:
- path or file category: any local proof note, scratch derivation, or audit memo on how P_A, P_B0, P_N, or D_w depend on the positive weight table w
- why needed: to upgrade the near-product perturbation candidate from plausible to provable and to justify a mathematically honest local bound for OI_N^op(w)
- claim tested: whether OI_N^op(w) admits a continuity or local Lipschitz-type control relative to distance from the product-weight manifold
- blocking or optional: optional
```

### Next Decision

`FORMALIZE_DEFINITIONS_FIRST`

原因很直接。当前 package 已经足以证明“free identity 是错的”，但还不足以在 paper-safe 口径下说明“什么才算同一对象”。如果先去堆更多 semantic toys，而 identity / transport / invariance / defect / instability 这些对象还没正式锁死，那么新证书库很容易重新坠回“例子很多、对象不清”的旧状态。相反，先把定义锁住，再立刻用最小命题
\[
OI^{\mathrm{op}}_{N}(w)=0 \iff w \text{ 为 product form}
\]
做第一步推进，之后再建设 certificate library，路线会更稳，也更符合当前包反复强调的 boundary discipline。（`MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md`; `MAOFIELD_METRIC_IDENTITY_PROGRAMME_ADOPTION_NOTE_20260704.md`; `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`）