# 有限加权残差传输的最小下一步数学推进审查报告

## 总判决

本报告只把上传的 bundle 当作证据边界；不把公开 GitHub、搜索引擎、raw 页面或 404 页面当作私仓证据。bundle 内的主提示词明确要求本次工作是一次 **Mode A** 的零上下文数学审查，只允许使用上传文件、本地 note/script/JSON/summary 的一致性，以及从有限维设定直接推出的定义、定理、证明草图和反例；同时明确禁止把结论升级成 full panel、observed field、training/new loss、glass-box、F3/LOSO、或 completed formal system。当前被接受的本地状态也被锁定为：`formal_v1_2_patch_accepted_after_minor_revision`、`definitions_and_harness_viable_only`、`insufficient_artifact`。这一点在主提示词、包内 README、report(30) adoption note 以及 `STATE.md` 中是一致的。（证据：`GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_THEOREM_STRENGTHENING_PROMPT_20260628.md`，6–10、17–27、31–55行；`README_FOR_PRO_FORMALV13_THEOREM_STRENGTHENING_20260628.md`，22–44行；`FORMAL_RESIDUAL_TRANSPORT_V1_2_REPORT30_ACCEPTANCE_ADOPTION_NOTE_20260628.md`，7–16、29–36、70–101行；`STATE.md`，16、24–29行）

结论很明确：**不应在 v1.2 处停下；v1.3 是正当且必要的；应优先做候选方向中的“乘积权与非乘积权边界”**。最小且真正有价值的 v1.3 对象，不是再加一个 toy metric，而是把 v1.2 已有的“exact product-weight Hoeffding theorem + 一个 non-product regression boundary”提升成一个**精确的充要条件与 no-go 定理**：在有限正权重的二因子空间里，只有当权重严格分解为乘积权时，行主效应与列主效应的去除才是顺序无关的；一旦权重不是乘积权，任何“先去 q 再去 b”或“先去 b 再去 q”的 sequential stripping 都会变成 projection-order dependent，而且甚至可能从**纯主效应**里制造出假的“interaction residual”。这直接填补了 v1.2 自己承认仍只停在“boundary example”的缺口，且不需要任何经验升级。（证据：`FORMAL_NOTE_V1_2_20260627.md`，149–205行；`SYNTHETIC_HARNESS_V1_2_20260627.md`，44–57、86–93行；`synthetic_harness_v1_2_20260627.json`，106–128行）

为什么不是别的方向先做。方向“商与注册定理”当然有价值，但它把 v1.1 的 quotient descent 与 v1.2 的 common ambient registration 融成更大的比较不变量框架，数学跨度更大，不是“最小下一步”。方向“square holonomy interpretation limits”虽然重要，但 v1.2 已经把“它只是有限路径恒等式，不自动等于 sheaf obstruction 或 curvature theorem”说出来了，继续做主要是解释学收紧，而不是最小的新定理。方向“projection-evolution commutator”在 v1.1 里已有等价命题雏形，若把它重新升格，更像是把旧命题搬回主线，而不是最经济的新推进。方向“random-subspace/rank-shadow”则更依赖概率阈值与 review heuristic；v1.1 甚至明确写了 `sigma2/sigma1 >= 0.25` 不是定理，只是 review guard。方向“finite gluing obstruction”和“coarsening/refinement naturality”都需要额外的图、限制映射或多尺度兼容数据，搭建成本更大。相比之下，方向“乘积权与非乘积权边界”完全建立在 v1.2 已批准的加权 Hilbert 结构与 product-weight proposition 上，是最小、最干净、也最容易 proof-check 的提升。（证据：`FORMAL_NOTE_V1_2_20260627.md`，52–108、149–205、267–276、278–320行；`FORMAL_NOTE_V1_1_20260625.md`，48–69、87–115、195–217、219–265行；`FORMAL_RESIDUAL_TRANSPORT_V1_2_REPORT30_ACCEPTANCE_ADOPTION_NOTE_20260628.md`，38–49、92–101行）

因此，本报告的主张是：**v1.3 首个目标应选候选方向二，并把它具体化为“加权 ANOVA 顺序缺陷定理”**。这一步既比“全套 quotient-registration 比较理论”更小，也比“再谈 holonomy 能证明什么”更实；它把当前主线里唯一还停在单个 regression example 的地方，提升成一个真正的有限维定理/反定理边界。（证据：`FORMAL_NOTE_V1_2_20260627.md`，202–205行；`README.md`，128–146行；`GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_THEOREM_STRENGTHENING_PROMPT_20260628.md`，56–93、95–132行）

## 当前版本严格审计

按当前被接受的 v1.2 来看，**已经达到“定理级且足够稳”的部分**有四块。第一块，是“先注册，后比较”的 common ambient requirement：Definition 1–3 与 Proposition 1 已经把 registered ambient datum、registered diagnostics、equivalent registration 以及等价注册下的谱/Gram/角度/范数不变性说清楚了。第二块，是 squared-capture 的 Beta 定律：v1.2 已把 analytic null 精确钉在平方捕获率 \(Z=\|\Pi_Su\|^2/\|u\|^2\) 上，而不是未平方范数比。第三块，是 exact product weights 下的 Hoeffding residual 命题：在精确乘积权下，加性 nuisance 的正交残差就是 product-measure 下的二因子 Hoeffding interaction。第四块，是 path defect 的逐边 telescoping 公式与 square holonomy 的分解恒等式。就“定义是否闭合、结论是否可表述、证明思路是否存在”而言，这四块已经足以算 v1.2 的正式数学核。（证据：`FORMAL_NOTE_V1_2_20260627.md`，40–108、110–147、149–205、207–276行；`FORMAL_RESIDUAL_TRANSPORT_V1_2_REPORT30_ACCEPTANCE_ADOPTION_NOTE_20260628.md`，38–49行）

实现层面，v1.2 的 **single-source threshold contract** 也已经闭合，但这属于 implementation adequacy，不应被误写成“新数学”。脚本把所有阈值集中到 `build_threshold_contract()`，所有 pass/fail 集中到 `evaluate_test()`，meta-block `threshold_contract_single_source_control` 只生成 metrics，不自己宣布 pass；JSON 侧阈值合同哈希也来自写盘后的 readback，而不是 runtime mirror。report(30) adoption note 与归档 JSON 都确认了这条闭环已经关闭，且 12 个 synthetic blocks 全部为 pass。这里可以说它“实现上自洽”，但不能说它“完成了 theorem stack”。（证据：`debranded_residual_transport_harness_v1_2.py`，72–130、682–810行；`deep_research_formal_residual_transport_v1_2_report29_minor_revision_audit_20260628.md`，17–31、63–69行；`FORMAL_RESIDUAL_TRANSPORT_V1_2_REPORT30_ACCEPTANCE_ADOPTION_NOTE_20260628.md`，13–27、48–49、70–90行；`synthetic_harness_v1_2_20260627.json`，89–104、317–337行）

**仍然只是设计级或 harness-level 的部分**，恰恰也是 v1.3 应该挑一个去正式化的地方。`quotient_descent_control`、`projection_evolution_commutator_obstruction`、`coarsening_non_naturality_trap`、`rank1_perturbation_bound_control`、`triple_overlap_gluing_cocycle` 在脚本和 JSON 里都存在，并且都 pass；但在已接受的 v1.2 formal note 中，它们并没有被纳入当前主数学核的正式命题结构，而是被列为 harness blocks。summary 也明确说这些 pass 只支持 “formal design review only”。这意味着它们现在的地位仍然更接近“有合成正负控制的设计对象”，而不是“已进入主线的审定理”。（证据：`FORMAL_NOTE_V1_2_20260627.md`，278–320行；`SYNTHETIC_HARNESS_V1_2_20260627.md`，44–57、86–93行；`synthetic_harness_v1_2_20260627.json`，140–190、207–219、222–314行）

更严格地说，**有些命题的旧版本曾在 v1.1 中写成 proposition，但它们并没有以“当前被接受的 v1.2 数学核”身份保留到今天**。最明显的是 quotient descent criterion 和 commutator criterion：v1.1 的 Formal Note 里已经有了 “\(C(N_s)\subseteq N_t\) 当且仅当商映射良定义” 与 “\(PT=TP\) 当且仅当 nuisance 与 residual 子空间都不变” 这样的命题，但 report(30) adoption note 在总结当前接受的核心数学时，点名保留的是 registered ambient、squared-capture Beta、exact product-weight Hoeffding、square-holonomy telescoping，而没有把 v1.1 的 quotient/commutator 命题列入“当前 accepted mathematical/core-design items”。所以，把这些内容重新搬回 v1.3 可以做，但它更像“主干重吸收”，不如直接补齐 v1.2 里自己承认仍停留在 regression boundary 的 product/non-product 缺口来得经济。（证据：`FORMAL_NOTE_V1_1_20260625.md`，48–69、87–115行；`FORMAL_RESIDUAL_TRANSPORT_V1_2_REPORT30_ACCEPTANCE_ADOPTION_NOTE_20260628.md`，38–49行；`README.md`，87–94、140–146行）

综上，当前 v1.2 的严格审计结论是：**它足够支撑 v1.3 规划，不需要再回去做 v1.2 revision；但它离“completed formal system”仍明显很远。** 最恰当的后续动作不是重开 implementation audit，也不是往经验线偷渡，而是选一个当前仍只有 boundary example、但已经具备有限维闭合基础的方向，把它升格为正式定理。方向二正好满足这个标准。（证据：`FORMAL_RESIDUAL_TRANSPORT_V1_2_REPORT30_ACCEPTANCE_ADOPTION_NOTE_20260628.md`，92–101行；`README.md`，140–146行；`STATE.md`，24–29行）

## 拟议对象

建议把 v1.3 的正式对象定义为 **加权 ANOVA 顺序缺陷算子**。设 \(Q,B\) 为有限集合，\(H=\mathbb R^{Q\times B}\)，权重 \(w(q,b)>0\) 且 \(\sum_{q,b}w(q,b)=1\)。定义加权内积
\[
\langle f,g\rangle_w=\sum_{q,b}w(q,b)f(q,b)g(q,b).
\]
再定义边际权重
\[
w_Q(q)=\sum_b w(q,b),\qquad w_B(b)=\sum_q w(q,b).
\]
这与 v1.2 的二因子 product-weight 设定完全同源，只是现在不预先假设 \(w=w_Q\otimes w_B\)。（基础设定见 `FORMAL_NOTE_V1_2_20260627.md`，149–179行；由该有限维框架直接延伸）

定义三个子空间。常数子空间
\[
C=\operatorname{span}\{1\}.
\]
零均值的 q-only 子空间
\[
A=\{a(q): \sum_q w_Q(q)a(q)=0\},
\]
把它视为 \(Q\times B\) 上只依赖 \(q\) 的函数。零均值的 b-only 子空间
\[
B=\{b(b): \sum_b w_B(b)b(b)=0\},
\]
把它视为 \(Q\times B\) 上只依赖 \(b\) 的函数。令
\[
N_{\mathrm{add}}=C\oplus A\oplus B.
\]
因为常数函数与零均值 q-only、b-only 函数总是正交，而 \(A\cap B=\{0\}\)，所以这是一个定义良好的有限维加性 nuisance 空间；但在非乘积权下，\(A\) 与 \(B\) 不一定正交，因此 \(N_{\mathrm{add}}\) 虽然仍有唯一的正交投影 \(P_{N_{\mathrm{add}}}\)，却不再具有 product ANOVA 那种“先减哪一个都一样”的正交分解结构。（基础设定与 product-weight 命题见 `FORMAL_NOTE_V1_2_20260627.md`，160–205行；“non-product 时 orthogonality 不必成立”见同文件 202–205 行）

令 \(P_C,P_A,P_B,P_N\) 分别表示到 \(C,A,B,N_{\mathrm{add}}\) 的加权正交投影。然后定义两个**有序剥离残差算子**：
\[
R_{Q\to B}=(I-P_B)(I-P_A)(I-P_C),
\]
\[
R_{B\to Q}=(I-P_A)(I-P_B)(I-P_C).
\]
它们表示“先去常数，再去 q 主效应，再去 b 主效应”和相反顺序。v1.3 的核心新对象则定义为
\[
D_w = R_{Q\to B}-R_{B\to Q}.
\]
因为 \(P_A1=P_B1=0\)，所以 \(D_w\) 实际上就是
\[
D_w=P_B P_A - P_A P_B,
\]
也就是两个主效应投影的顺序缺陷。这个对象不是新 metric，而是一个**有限维算子级 no-go 证据对象**：它直接回答“ANOVA hierarchy 是否顺序无关”这一数学问题。（由上面定义直接推出；当前 harness 中与之最接近的现有边界控制是 `product_reweighting_separation`，见 `debranded_residual_transport_harness_v1_2.py`，362–381行；`synthetic_harness_v1_2_20260627.json`，106–128行）

之所以说这就是“最小真实推进”，原因在于：v1.2 已经证明了乘积权时的正向结论，却把非乘积权下的情况停在一句 boundary 说明和一个固定 regression example 上。把那个 regression example 提升成一个“当且仅当 product weight 才有顺序无关剥离”的算子定理，正好是从 v1.2 往前跨出的最小一步，而且完全留在有限维、零 GPU、无经验升级的证据边界里。（证据：`FORMAL_NOTE_V1_2_20260627.md`，181–205行；`SYNTHETIC_HARNESS_V1_2_20260627.md`，88–93行）

## 定理与证明计划

第一条应当正式写成 **乘积权—主效应正交等价定理**。命题可表述为：对任意有限正权 \(w\)，下列两件事等价：其一，\(w(q,b)=w_Q(q)w_B(b)\) 对所有 \((q,b)\) 成立；其二，零均值 q-only 子空间 \(A\) 与零均值 b-only 子空间 \(B\) 在 \(\langle\cdot,\cdot\rangle_w\) 下正交。正向方向其实就是 v1.2 Proposition 3 证明中的关键一步；反向方向则是 v1.2 尚未写出的缺口。证明最短的做法，是取 centered indicator testers
\[
a_{q_0}(q)=\mathbf 1_{\{q=q_0\}}-w_Q(q_0),\qquad
b_{b_0}(b)=\mathbf 1_{\{b=b_0\}}-w_B(b_0),
\]
直接计算
\[
\langle a_{q_0}, b_{b_0}\rangle_w
= w(q_0,b_0)-w_Q(q_0)w_B(b_0).
\]
于是“对所有 centered q-only 与 centered b-only 都正交”立刻等价于“所有单元都满足乘积分解”。这样，v1.2 的正向 product theorem 就被强化成精确充要条件，而不是只保留一个 forward implication。（基础设定与 v1.2 正向 theorem 见 `FORMAL_NOTE_V1_2_20260627.md`，149–205行；其当前缺口在 202–205 行被明确承认）

第二条应当写成 **顺序缺陷等价定理**。命题为：下列陈述等价。其一，\(w\) 是乘积权；其二，\(D_w=0\)；其三，\(R_{Q\to B}=R_{B\to Q}\)；其四，
\[
R_{Q\to B}=R_{B\to Q}=I-P_N.
\]
证明思路很短。若 \(w\) 为乘积权，则由上一条得 \(A\perp B\)，于是 \(P_AP_B=P_BP_A=0\)，所以两个有序剥离算子相同，并化成
\[
I-P_C-P_A-P_B=I-P_N.
\]
反过来，若 \(R_{Q\to B}=R_{B\to Q}\)，把任意 \(b\in B\) 代入即可：右边顺序先剥 \(b\)-effect，所以给出 \(0\)；左边顺序则给出 \(-(I-P_B)P_A b\)。因此必有 \((I-P_B)P_A b=0\)，即 \(P_A b\in B\)。但 \(P_A b\in A\) 同时成立，而 \(A\cap B=\{0\}\)，故 \(P_A b=0\) 对所有 \(b\in B\) 成立，所以 \(A\perp B\)，再由上一条得到 product weights。这个定理一旦写清楚，就把“projection-order dependent”从一句警告升级成了一个严格 iff 判据。（基于本节拟议定义直接推导；其动机来源于 v1.2 只在 product 情形给正向定理、在 non-product 情形只给 boundary 警告，见 `FORMAL_NOTE_V1_2_20260627.md`，181–205行）

第三条应当写成 **非乘积权下的纯主效应假残差 no-go 定理**。命题为：若 \(w\) 不是乘积权，则存在某个纯 \(b\)-主效应 \(K\in B\setminus\{0\}\)，使得
\[
R_{B\to Q}K=0,\qquad R_{Q\to B}K\neq 0,
\]
并且
\[
(I-P_N)K=0.
\]
也就是说，真正的正交加性残差是零，但“先剥 q 再剥 b”的 sequential stripping 会凭空制造一个非零残差。对称地，也存在纯 \(q\)-主效应在另一个顺序下出现同样现象。证明方法很直白：非乘积权 \(\Rightarrow A\not\perp B\)，所以可取 \(b\in B\) 使 \(P_A b\neq 0\)。因为 \(K=b\in B\)，故 \(R_{B\to Q}K=0\)；但是
\[
R_{Q\to B}K=(I-P_B)(I-P_A)b=-(I-P_B)P_A b.
\]
若这一项为零，则 \(P_A b\in B\)，又因 \(P_A b\in A\)，只可能 \(P_A b=0\)，矛盾。于是得到 sharp no-go：**非乘积权下，“顺序化剥离”甚至会把纯主效应误造为 interaction-like residual。** 这正是当前主线最需要的一把数学斧头，因为它把“别误叫 Hoeffding interaction”从术语警告变成了结构性不可能性定理。（该 no-go 直接建立在上两条定理上；v1.2 对“non-product observed weight 不得再叫 product-measure Hoeffding interaction”的边界警告见 `FORMAL_NOTE_V1_2_20260627.md`，202–205行）

bundle 里现成就有一个可复用的具体反例：脚本 `product_reweighting_separation` 用的 \(2\times 2\) 非乘积权是原始权重 \((1,2,3,5)\) 归一化后得到的 \(w=(1,2,3,5)/11\)。在这个例子里，
\[
w_Q=(3/11,8/11),\qquad w_B=(4/11,7/11),
\]
所以
\[
w(0,0)-w_Q(0)w_B(0)=1/11-12/121=-1/121\neq 0,
\]
已经直接证明了它不是乘积权。取
\[
a(q)=\mathbf 1_{\{q=0\}}-3/11,\qquad
b(b)=\mathbf 1_{\{b=0\}}-4/11,
\]
则 \(\langle a,b\rangle_w=-1/121\neq 0\)，于是 \(A\) 与 \(B\) 不正交。把 \(K=b\) 当成纯 \(b\)-主效应，就得到上面那条 no-go 的最小 \(2\times 2\) 见证。这比现有 harness 只报告“某个 residual difference 非零”更强，因为它说明**错误来自顺序化剥离本身，而不只是来自换了几何后数值不同**。（证据：`debranded_residual_transport_harness_v1_2.py`，362–381行；`synthetic_harness_v1_2_20260627.json`，106–128行；上式计算由该权重例子直接推得）

真正需要补完的证明义务其实不多，且都有限维、初等、一次性可写清。第一，要把 \(A\cap B=\{0\}\) 写成一个单独引理。第二，要把 centered indicator identity 写成正式引理，而不是只在证明里口算。第三，要把 \(D_w=P_BP_A-P_AP_B\) 的展开写清，避免记号歧义。第四，要明确限定本定理只处理“二因子、有限正权、加性 nuisance 的顺序化剥离”，**不**顺带承诺多因子一般理论、图上传输、或经验对象识别。这些 proof obligations 都很小，完全符合“最小真实推进”的标准。（证据边界见 `GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_THEOREM_STRENGTHENING_PROMPT_20260628.md`，31–49、56–93行）

## 最小化验证含义

这条 v1.3 只需要做**零 GPU、定理行为级**的 harness 验证，不需要任何 full panel，也不需要接入 MaoField 经验线。现有 v1.2 harness 已经有单一阈值源、统一 evaluator 和 JSON readback 机制，所以最小实现方案是沿用当前 contract 结构，只新增几个 theorem-targeted blocks，而不是扩展经验流水线。（证据：`debranded_residual_transport_harness_v1_2.py`，72–130、682–810、843–946行；`SYNTHETIC_HARNESS_V1_2_20260627.md`，30–42行）

最小新增检查建议只有三项。第一项，做一个 **product_weight_order_independence_control**：在精确乘积权的 \(2\times 3\) 或 \(3\times 3\) 例子上，验证 \(\|D_w\|_F\le\varepsilon\)，并验证 \(R_{Q\to B}\)、\(R_{B\to Q}\) 与 \(I-P_N\) 在若干随机信号和基函数上都一致。第二项，做一个 **nonproduct_pure_main_effect_no_go_control**：复用 v1.2 已有的 \(2\times 2\) 非乘积权例子，构造中心化的纯 \(b\)-主效应 \(K\)，验证 \(R_{B\to Q}K=0\)、\(R_{Q\to B}K\neq0\)、且 \((I-P_N)K=0\)。第三项，做一个 **centered_indicator_product_iff_control**：逐单元验证
\[
\langle a_{q_0},b_{b_0}\rangle_w = w(q_0,b_0)-w_Q(q_0)w_B(b_0),
\]
从而把“乘积权 \(\Leftrightarrow\) \(A\perp B\)”的关键反向证明直接落成脚本可审计对象。这样，JSON 里就不是再存一个孤立的 toy metric，而是存三个对应定理核心部位的 identity/no-go witness。（构造基础见 `FORMAL_NOTE_V1_2_20260627.md`，149–205行；现有非乘积权例子见 `debranded_residual_transport_harness_v1_2.py`，362–381行）

这三项之外，不建议本轮再引入新的 review heuristic。尤其不应把像 `sigma2/sigma1 >= 0.25` 这样的 reviewing floor 偷渡成 theorem threshold；v1.1 与当前脚本都已经明确，它只是审稿卫生线，不是普适数学常数。v1.3 的阈值应尽量围绕“恒等式误差接近零”与“反例中的非零量有可计算下界”来设，而不是继续堆经验型门槛。（证据：`FORMAL_NOTE_V1_1_20260625.md`，195–217行；`debranded_residual_transport_harness_v1_2.py`，507–536行；`FORMAL_NOTE_V1_2_20260627.md`，322–337行）

## 禁语清单

即使 v1.3 采用本报告建议方向，下列说法仍然必须保持禁止，不得越界：

- 不得说 **completed formal system**，因为当前 bundle 自己把上限锁在 `definitions_and_harness_viable_only`，并反复声明 report(30) 只关闭了 threshold-contract minor revision，而不是完成 theorem stack。
- 不得说 **theorem stack complete**，因为当前仍有若干对象只处于 harness-level 或旧版本 provenance 层。
- 不得说 **full panel has run**、**16-cell aggregate exists**，因为 bundle 的 boundary 与 blocked claims 明确禁止。
- 不得说已经观察到 **MaoField residual / interaction / quotient-residual / transport / holonomy field**。
- 不得说 **glass box broken**、**LOSO passed**、**F3 positive**。
- 不得说 **checkpoint loading / inference / training / new loss** 已获授权。
- 不得把非乘积权下由 sequential stripping 产生的东西称为 **product-measure Hoeffding interaction**；在本报告建议的 v1.3 下，恰恰应当把这种误称正式判死。
- 不得把 square holonomy 再次抬升成 **curvature theorem / sheaf obstruction theorem**；v1.2 已明确它只是有限路径恒等式，除非额外结构被完整定义。
- 不得把 `0.25` 之类 review floor 说成数学常数。
- 不得把本报告提出的 v1.3 no-go 定理，偷换成 MaoField 经验真值升级。

（证据：`FORMAL_NOTE_V1_2_20260627.md`，16–38、202–205、267–276、322–347行；`FORMAL_RESIDUAL_TRANSPORT_V1_2_REPORT30_ACCEPTANCE_ADOPTION_NOTE_20260628.md`，70–101行；`synthetic_harness_v1_2_20260627.json`，11–29、336–338行；`GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_THEOREM_STRENGTHENING_PROMPT_20260628.md`，38–49行）

## 初中生解释

把它想成一个带权重的表格。表格的每一格都有一个“重要程度”权重。现在要从表格里的总变化里，先减掉“行的影响”，再减掉“列的影响”，看看最后剩下什么。如果这些权重恰好能拆成“行权重 × 列权重”，那先减行再减列，还是先减列再减行，结果都一样，最后剩下的才像一个真正稳定的“交互剩余”。v1.2 已经把这个“乘积权时可以这样做”的方向讲清楚了，但对“不满足乘积权时到底会怎样坏掉”还只给了一个例子，没有给定理。（证据：`FORMAL_NOTE_V1_2_20260627.md`，149–205行）

本报告建议 v1.3 干的，就是把那句“会坏掉”变成严格数学：**只要权重不是乘积型，先减行再减列和先减列再减行就可能不一样，而且甚至会从原本只有‘行作用’或只有‘列作用’的东西里，凭空造出一个假的剩余。** 所以 v1.3 最应该先证明的，不是“我们发现了什么新场”，而是“什么时候这种剩余是坐标/顺序假象，什么时候它才是顺序无关的真正对象”。这一步很小，但很关键，因为它把“别乱叫”变成了“数学上就是不能乱叫”。（证据：`FORMAL_NOTE_V1_2_20260627.md`，202–205行；`SYNTHETIC_HARNESS_V1_2_20260627.md`，46–57、88–93行）

## 最终分类

```text
v1_3_theorem_strengthening_plan_accepted
```