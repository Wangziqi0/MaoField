# Formal Residual Transport v1.2 最小补丁深度研究报告

## 研究边界与审阅方法

这次任务的边界非常清楚：它是 **Mode A 的有限维数学与 harness 设计工作**，不是 MaoField 的经验性补救，也不授权 full panel、16-cell aggregate、checkpoint loading、model inference、training、new loss、observed field、glass-box、F3、LOSO 之类表述；当前允许上限仍是 `definitions_and_harness_viable_only`，Mode B 经验状态仍必须保持 `insufficient_artifact`。【bundle: 00-README_FOR_142_AND_PRO.md L14-L54】【bundle: prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_PATCH_PROMPT_20260626.md L54-L69】【bundle: from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_1_STRICT_AUDIT_ADOPTION_NOTE_20260626.md L11-L31】

我按 bundle 指定顺序核读了 README、v1.2 prompt、report(27) 严格审计、report(27) adoption note、v1.2 workplan、Formal Note v1.1、v1.1 harness summary、v1.1 harness JSON、v1.1 harness 脚本、v1.1 workplan、report(26) 严格审计、report(26) adoption note、STATE、MD_CATALOG 与 GPT-5.5 Pro research index；因此下面的结论是 **bundle-first** 的，不依赖公共 GitHub 页面或搜索引擎残片。【bundle: 00-README_FOR_142_AND_PRO.md L56-L72】【bundle: prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_PATCH_PROMPT_20260626.md L36-L52】

根据 prompt 的方法约束，若 GitHub connector 不可用或不明确，就应继续基于上传 bundle，并把仓库验证标为 blocked；因此本报告的仓库二次核验状态是 **repo verification blocked**，这不影响 v1.2 最小补丁设计本身。【bundle: prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_PATCH_PROMPT_20260626.md L13-L18】

作为现有工件核对，我还本地复跑了 v1.1 脚本并确认 `py_compile` 通过，脚本能生成 JSON，且 JSON 可被 `python -m json.tool` 校验。这一点不改变 bundle 的证据边界，但说明 v1.1 的“toy harness 可执行”结论是可复现的；这也与 v1.1 summary 和 JSON 中“14 个 synthetic controls 均通过、上限仍是 `definitions_and_harness_viable_only`”的记录一致。【bundle: from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_1_20260625.md L24-L45】【bundle: from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_1_20260625.json L78-L285】

## 一页结论

结论先说死：**v1.2 是一个小补丁，不是大改写；而且应该继续做。** 这么判断，不是因为 v1.1 已经“完成”，恰恰相反，是因为 bundle 自己已经把 v1.1 定性为 `accept_with_v1_2_required`：它不是失败品，但也绝不是 completed formal system；下一步正确动作就是一个小而硬的 v1.2，而不是重新扩张项目，更不是去做 MaoField 经验救火。【bundle: from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_1_STRICT_AUDIT_ADOPTION_NOTE_20260626.md L39-L54】【bundle: from_repo/GPT55_PRO_RESEARCH_INDEX_20260622.md L1393-L1414】

我同意 report(27) 的主判断：v1.1 已经把若干关键代数件补到了“可认真审计”的层级，包括 quotient descent、projection-evolution commutator、path-level square holonomy decomposition、common ambient 的先决条件、random-subspace analytic null 的正确方向、rank-1 perturbation bound、triple-overlap gluing 语言，以及 threshold/environment 的 JSON 记录。因此它已经是一个**真有限维线性代数对象**，而不只是漂亮措辞。【bundle: from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_1_strict_audit_20260626.md L7-L8】【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_1_20260625.md L33-L311】

但 v1.1 仍有四个必须收口的半成品，而且这四个都是可以局部修补的，不需要重写项目主线。它们分别是：共同 ambient 还只是规则语句，不是严格注册定义；random-subspace note 里的解析 Beta law 和 harness 实际统计量还没有闭合；product-weight 正向 theorem 还没有在 note 内部真正证明；threshold contract 虽已写进 JSON，但执行逻辑仍不是单一真相源。【bundle: from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_1_strict_audit_20260626.md L20-L28】【bundle: from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_1_strict_audit_20260626.md L39-L46】【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md L34-L45】

所以，一页 verdict 应该写成下面这句话，而不是别的：

**数学方向保留；v1.1 不需要被推翻；但有若干 subclaim 必须降级到更诚实的表述，随后用 v1.2 小补丁封口。项目应继续，只能继续在 debranded 的有限维数学线上继续，不能借此升级任何 MaoField 经验地位。**【bundle: from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_1_STRICT_AUDIT_ADOPTION_NOTE_20260626.md L70-L99】【bundle: from_repo/STATE.md L86-L92】

需要降级的 v1.1 子表述，我给出四条，而且都不是“全盘驳回”，而是**收紧措辞**。其一，“invariants”必须降级为“registered diagnostics”，除非先给出共同 ambient 注册，并说明何种注册等价下它们才真不变；report(27) 已明确指出 v1.1 只修好了语言边界，没有完成 invariant theory。【bundle: from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_1_strict_audit_20260626.md L20-L20】【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_1_20260625.md L146-L165】

其二，random-subspace 部分必须从“几乎闭合”降级为“note-level analytic null 已写出，但 harness 仍是未完全对齐的实现”。v1.1 formal note 写的是平方捕获量的 Beta 法则，而脚本 `weighted_projection_energy` 返回的是投影**范数比**而不是平方捕获量；这不是方向性错误，但它确实阻止了“note 与 harness 完全闭合”的说法。bundle 中的 audit 对这一点说得已经很严厉，我同意它的口径。【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_1_20260625.md L167-L193】【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L237-L243】【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L540-L588】【bundle: from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_1_strict_audit_20260626.md L22-L22】

其三，product-weight 正向 theorem 必须从“已得到 theorem”降级为“theorem stub”。v1.1 第 8 节给出了正确边界：exact product weight 才能合法讲 product-measure Hoeffding，non-product 则是另一套加权几何；但 note 自身没有把 Hoeffding interaction 的对象、投影、正向等价证明完整写出来，所以不能冒称 theorem 已完成。【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_1_20260625.md L245-L265】【bundle: from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_1_strict_audit_20260626.md L28-L28】

其四，threshold contract 必须从“已有合同”降级为“已有顶层合同，但非 fail-closed”。JSON 顶层确实写了 `threshold_contract`，但当前脚本里至少 `exact_product_weight_equality_control`、`product_reweighting_separation`、`outcome_derived_nuisance_invalidation`、`transport_stable_multidirectional_positive_control`、`rank1_plus_noise_floor_trap`、`equal_cell_count_random_axes` 与 `gluing_absorption` 这些 block，仍在 pass/fail 逻辑里直接写数值常量，而不是只从 contract 读值；这正是 v1.2 必须修掉的工程-形式双重缺口。【bundle: from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_1_20260625.json L11-L68】【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L340-L358】【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L361-L385】【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L388-L402】【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L416-L436】【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L510-L537】【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L602-L632】【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L682-L698】

## Formal Note v1.2 最小补丁文本

下面给出的不是“宣传稿”，而是我认为可以直接贴进 `FORMAL_NOTE_V1_2_*.md` 的最小补丁正文框架。它故意只修 bundle 规定的缺口，不往 sheaf theory、经验识别、训练方案等方向扩展。【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md L34-L45】【bundle: prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_PATCH_PROMPT_20260626.md L65-L69】

### 共同 ambient 注册

**Definition. Registered ambient datum.**
设顶点集合为有限集 \(V\)。对每个 \(s\in V\)，给定有限维带权 Hilbert 空间 \((H_s,\langle\cdot,\cdot\rangle_{w_s})\)，nuisance 子空间 \(N_s\subset H_s\)，以及残差投影 \(P_s:H_s\to N_s^{\perp,w_s}\)。一个 **registered ambient datum** 是以下数据之一：

1. 一个有限维带权 Hilbert 空间 \((E,\langle\cdot,\cdot\rangle_E)\)；
2. 对每个 \(s\in V\) 的线性映射 \(A_s:H_s\to E\)；
3. 且 \(A_s\) 在 \(N_s^{\perp,w_s}\) 上是等距嵌入，即
   \[
   \langle A_s x,A_s y\rangle_E=\langle x,y\rangle_{w_s}
   \quad\text{for all }x,y\in N_s^{\perp,w_s}.
   \]

对任意信号 \(K_s\in H_s\)，定义 **registered residual**
\[
\widetilde R_s := A_s P_s K_s \in E.
\]

**Definition. Registered stack and registered diagnostics.**
只有在固定了 registered ambient datum 之后，才定义：

\[
\mathcal S_{\mathrm{reg}} := [\widetilde R_{s_1}\ \cdots\ \widetilde R_{s_m}]
\]
的奇异值谱、若干已命名 residual subspace 的 principal angles、跨边 edge-defect norm、以及 square-holonomy norm。
若未注册 ambient，以上对象都只允许叫 **未注册比较量**，不允许叫 invariant。

**Definition. Registration equivalence.**
两个注册 \((E,A_s)\) 与 \((E',A'_s)\) 称为等价，若存在加权等距同构 \(U:E\to E'\)，使得对所有 \(s\in V\)，在 \(N_s^{\perp,w_s}\) 上有
\[
U A_s = A'_s .
\]

**Proposition. Invariance under equivalent registration.**
若 \((E,A_s)\sim(E',A'_s)\)，则由 registered residual 构成的 stack singular values、principal angles、edge-defect norms、square-holonomy norms 在两种注册下完全一致。

**Proof sketch.**
所有这些量都只依赖于内积、范数、奇异值、以及向量族张成子空间的夹角；加权等距同构保持这些对象不变。因此，**在注册等价类之下**，它们才配叫 invariant；在此之外，它们只是 registration-dependent diagnostics。这个补丁正好把 v1.1 的“先注册 ambient，再谈 invariant”从提醒句升级为定义句。【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md L48-L64】【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_1_20260625.md L146-L165】

这部分必须顺手加一句杀伤性边界：**没有注册，就没有 residual-stack spectrum、principal angle、transported norm、holonomy norm 的不变性语言。** 这是 v1.2 应保留的硬约束，不是可选修辞。【bundle: prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_PATCH_PROMPT_20260626.md L73-L76】

### 随机子空间平方捕获定理

**Proposition. Beta law for squared capture.**
设 \(d\ge 2\)，\(0<k<d\)。取固定非零向量 \(u\in\mathbb R^d\)，取 Haar-uniform 的随机 \(k\)-维子空间 \(S\in \mathrm{Gr}(k,d)\)，记 \(\Pi_S\) 为正交投影。定义平方捕获量
\[
Z:=\frac{\|\Pi_S u\|_2^2}{\|u\|_2^2}.
\]
则
\[
Z\sim \mathrm{Beta}\!\left(\frac{k}{2},\frac{d-k}{2}\right).
\]

**Proof sketch.**
先用旋转不变性把“固定向量投到随机 \(k\)-平面”的问题化到“随机单位向量投到固定坐标 \(k\)-平面”的问题。随机投影讲义里明确使用了这一旋转不变性视角：固定向量投到随机子空间的投影长度分布，等价于随机单位向量投到前 \(k\) 个坐标轴张成子空间的分布。citeturn2view0
再写 \(z=g/\|g\|_2\)，其中 \(g_i\stackrel{iid}{\sim}N(0,1)\)。则
\[
Z=\sum_{i=1}^k z_i^2
   = \frac{\sum_{i=1}^k g_i^2}{\sum_{i=1}^d g_i^2}
   = \frac{X}{X+Y},
\]
其中 \(X\sim \chi_k^2\)、\(Y\sim \chi_{d-k}^2\) 独立，于是 \(Z\) 服从上述 Beta 分布。端点 \(k=0\) 与 \(k=d\) 退化，必须显式排除。

**Weighted version.**
若工作在有限维带权 Hilbert 空间 \((H,\langle\cdot,\cdot\rangle_w)\)，则先取白化等距同构 \(W^{1/2}:H\to\mathbb R^d\)，再在白化坐标中使用同一定义。v1.2 note 必须明确说明：**解析定理对应的统计量是平方捕获量，而不是 unsquared norm ratio。**【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md L65-L83】【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_1_20260625.md L167-L193】

这部分的最小修法，不是把 Monte Carlo 删掉，而是把 formal statistic 和 harness statistic 统一成同一个 \(Z\)。如果暂时不用外部 Beta quantile 依赖，那么 harness 至少也要在 **同一平方统计量** 上做 Monte Carlo，并把它老老实实标为 Monte Carlo diagnostic，而不是伪装成“已由 Beta law 直接校准”。【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md L79-L83】

### Product-weight Hoeffding 等价定理

**Definition. Product weighted space.**
令 \(Q,B\) 为有限集合，产品空间 \(X=Q\times B\)。设严格正权重分解为
\[
w(q,b)=w_Q(q)\,w_B(b),
\qquad
\sum_q w_Q(q)=1,\quad \sum_b w_B(b)=1.
\]
定义
\[
\langle f,g\rangle_w := \sum_{q,b} w_Q(q)w_B(b) f(q,b)g(q,b).
\]

**Definition. Additive main-effect nuisance.**
定义加性主效应子空间
\[
\mathcal N_{\mathrm{add}}
:=
\{c+a(q)+b(b)\,:\, c\in\mathbb R,\ a:Q\to\mathbb R,\ b:B\to\mathbb R\}.
\]

**Definition. Hoeffding interaction component.**
对任意 \(K:Q\times B\to\mathbb R\)，记
\[
\mu := \mathbb E_w[K],
\qquad
K_Q(q):=\mathbb E_w[K\mid q],
\qquad
K_B(b):=\mathbb E_w[K\mid b].
\]
定义二因子交互项
\[
H(K)(q,b):=K(q,b)-K_Q(q)-K_B(b)+\mu.
\]

**Theorem. Exact product-weight equivalence.**
在 exact product weights 下，\(H(K)\) 恰好是 \(K\) 对加性主效应 nuisance 子空间 \(\mathcal N_{\mathrm{add}}\) 的加权正交残差：
\[
P_{\mathcal N_{\mathrm{add}}}^{\perp,w} K = H(K).
\]

**Proof sketch.**
将 \(\mathcal N_{\mathrm{add}}\) 正交拆成
\[
\mathrm{span}\{1\}\oplus \mathcal U_Q^0 \oplus \mathcal U_B^0,
\]
其中 \(\mathcal U_Q^0\) 为零均值的 \(q\)-only 函数，\(\mathcal U_B^0\) 为零均值的 \(b\)-only 函数。在产品权重下，零均值 \(q\)-only 与零均值 \(b\)-only 子空间正交，因为
\[
\langle a(q), b(b)\rangle_w
=
\Big(\sum_q w_Q(q)a(q)\Big)
\Big(\sum_b w_B(b)b(b)\Big)=0.
\]
于是 \(K\) 在这三个子空间上的投影恰好是 \(\mu\)、\(K_Q-\mu\)、\(K_B-\mu\)。减去这些加性分量，得到的就是 \(H(K)\)。

**Boundary. Non-product weights.**
若观察权重不是 exact product form，则上述正交性一般失效；此时对象只能叫 **non-product weighted projection residual**，不得继续叫 product-measure Hoeffding interaction。v1/v1.1 已有的 \(2\times 2\) 反例与现有 harness 的 `product_reweighting_separation` 正是这条边界的回归例子，不应删掉。【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md L85-L103】【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_1_20260625.md L245-L265】【bundle: from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_1_20260625.json L16-L19】【bundle: from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_1_20260625.json L87-L112】

### Square holonomy 逐边望远镜缺陷公式

v1.1 已有路径级恒等式
\[
\Omega_{p,q}=P_t(C_p-C_q)P_s+\Delta_p-\Delta_q,
\qquad
\Delta_p:=\widehat C_p-P_t C_p P_s,
\]
这部分应保留，不要重写。【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_1_20260625.md L119-L144】

v1.2 需要补的是逐边展开。设路径
\[
p:s_0\to s_1\to\cdots\to s_m
\]
的边映射为 \(C_i:H_{s_{i-1}}\to H_{s_i}\)；记
\[
\widehat C_p := P_{s_m}C_mP_{s_{m-1}}\cdots P_{s_1}C_1P_{s_0}.
\]
则对 \(m\ge 2\)，定义内部边泄漏项
\[
L_{i+1}:=P_{s_{i+1}}C_{i+1}P_{s_i}-P_{s_{i+1}}C_{i+1},
\qquad 1\le i\le m-1.
\]

**Proposition. Telescoping defect formula.**
有精确恒等式
\[
\Delta_p
=
\widehat C_p - P_{s_m}C_m\cdots C_1 P_{s_0}
=
\sum_{i=1}^{m-1}
P_{s_m}C_mP_{s_{m-1}}\cdots P_{s_{i+2}}C_{i+2}\,
L_{i+1}\,
C_i\cdots C_1P_{s_0}.
\]
当 \(m=1\) 时，和为空和，故 \(\Delta_p=0\)。

**Proof sketch.**
反复插入并减去
\[
P_{s_m}C_mP_{s_{m-1}}\cdots P_{s_{i+1}}C_{i+1}C_i\cdots C_1P_{s_0}
\]
即可。对于长度 \(2\) 与 \(3\) 的路径，公式分别退化为
\[
P_2C_2P_1C_1P_0-P_2C_2C_1P_0
=
(P_2C_2P_1-P_2C_2)C_1P_0,
\]
和
\[
P_3C_3P_2C_2P_1C_1P_0-P_3C_3C_2C_1P_0
=
P_3C_3(P_2C_2P_1-P_2C_2)C_1P_0+(P_3C_3P_2-P_3C_3)C_2C_1P_0.
\]
一般情形完全同理。

**Corollary. Square holonomy with edgewise leakage.**
对两条同端点路径 \(p,q:s\to t\)，
\[
\Omega_{p,q}
=
P_t(C_p-C_q)P_s
+
\sum_{\text{internal edges of }p}\text{transported leakages}
-
\sum_{\text{internal edges of }q}\text{transported leakages}.
\]
因此，非零 square holonomy 可被精确归因到两类来源：raw path mismatch 与 transported internal leakage；不再只有路径级 \(\Delta_p,\Delta_q\) 的粗分辨率。

我认为这一条 **是可以做出来的**，不需要额外假设，也不需要硬把项目推成 sheaf 理论。它恰好满足 workplan 所要的“per-edge telescoping defect formula”。【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md L105-L119】【bundle: from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_1_strict_audit_20260626.md L17-L18】

### v1.1 已有命题的处理态度

quotient descent、projection-evolution commutator、rank-1 perturbation bound 与 triple-overlap gluing 这几块，v1.1 已经给出了可接受的最小数学骨架。v1.2 不应重写它们，只应做两件事：统一记号，消除不严之处；然后为它们加上对应的独立 harness block，使“note 有命题、harness 有测试”真正对齐。【bundle: from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_1_strict_audit_20260626.md L13-L16】【bundle: from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_1_strict_audit_20260626.md L36-L44】

## Harness v1.2 设计

v1.2 harness 的核心不是“再堆几个工件”，而是把 **定理、回归例子、review floor、Monte Carlo diagnostic** 四种东西明确分层。v1.2 workplan 已经要求所有 test names 在 note、summary、JSON、script 之间一致，并要求新版本单独编号，不能覆写 v1.1 JSON；我建议严格执行这一点。【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md L135-L171】

### 单一合同架构

最小可实现架构应该改成：

- `build_threshold_contract()`：唯一返回合同对象；
- 每个 block 只产出 metrics，不直接写 `pass`；
- `evaluate_test(test_id, metrics, contract)`：统一计算 pass/fail；
- 顶层 JSON 直接序列化同一个 `contract`；
- `threshold_contract_single_source_control` 负责检查 runtime 合同与 serialized 合同完全一致。

这样做以后，脚本内部就不会再出现“JSON 写一份，if 里再写一份”的双轨逻辑。v1.1 当前至少有多块 block 仍在硬编码 pass 条件，说明它还没达到这个结构要求。【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L25-L82】【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L340-L358】【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L361-L385】【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L388-L402】【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L416-L436】【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L510-L537】【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L602-L632】【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L682-L698】

### 需要新增或改造的 blocks

| test name | 类型 | 证明什么 | 不证明什么 | 必须 contract-driven 的阈值 |
|---|---|---|---|---|
| `quotient_descent_control` | theorem-backed toy control | 在有限维 toy 例子里，若 \(C(N_s)\subseteq N_t\) 则 coset 映射良定义；若违背该条件则同一 coset 的像不一致 | 不证明真实复杂数据流都自动满足 quotient descent | `max_good_coset_disagreement`, `min_bad_coset_disagreement` |
| `common_ambient_registration_control` | theorem-backed toy control | 对两个等价注册 \((E,A_s)\sim(E',A'_s)\)，registered stack singular values / principal angles / registered norms 一致 | 不证明存在 canonical ambient；不证明未注册量有不变性 | `max_isometric_registration_metric_diff`, `max_unregistered_use_count` |
| `rank1_perturbation_bound_control` | theorem-backed numerical control | 对构造的 \(M=a v^\top+E\)，验证 \(\sigma_2(M)\le \|E\|_2+\varepsilon\) | 不证明 0.25 floor 是定理；不证明所有多方向结构都由此完全分类 | `max_sigma2_minus_noise_opnorm`, 以及单列 `review_floor` 但只作 heuristic |
| `random_subspace_beta_squared_capture_control` | theorem-backed law + Monte Carlo diagnostic | 统计量改为平方捕获 \(Z\)；记录 \(d,k,\alpha,\beta\)；验证 null 采样与 Beta 的同一统计量一致，并检验 heldout \(Z\) 超过约定阈值 | 不证明全维度上的精确 type-I/type-II 最优性；若无 Beta quantile 例程，也不应冒称 exact analytic gate | `max_beta_mean_error`, `max_beta_var_error`, `min_true_sq_capture_minus_p99` 或 `min_true_sq_capture_quantile` |
| `threshold_contract_single_source_control` | meta-test | runtime 合同、每个 test 内嵌 thresholds、顶层 JSON 合同三码合一 | 不证明阈值本身最优，只证明来源唯一 | `require_contract_hash_match`, `require_per_test_threshold_match`, `require_central_evaluator` |
| `square_holonomy_telescoping_control` | optional theorem-backed regression | 验证 \(\Delta_p\) 的逐边望远镜公式与 \(\Omega_{p,q}\) 的 raw-plus-leakage 分解在 toy path 上数值成立 | 不证明 sheaf obstruction theory；不证明“curvature”之类连续几何含义 | `max_telescoping_identity_error`, `max_square_identity_error` |

这个表的意义在于把 v1.2 workplan 里点名的六个 block 真正落实成“每块到底担当什么”，而不是再让 summary 写名字、JSON 写指标、script 写另一套逻辑。【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md L139-L154】

### 旧 block 的去留

v1.1 的这些 block 仍值得保留：`exact_product_weight_equality_control`、`product_reweighting_separation`、`projection_evolution_commutator_obstruction`、`bad_edge_defect_control`、`raw_path_equality_square_control`、`coarsening_non_naturality_trap`、`triple_overlap_gluing_cocycle`。原因很简单：它们已经构成了稳定的 regression suite，删除它们只会让 v1.2 失去对 v1.1 已有边界的回归保护。【bundle: from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_1_20260625.md L24-L39】

但 `random_subspace_in_residual_space` 这块，不能原样继承。当前脚本 `weighted_projection_energy` 返回的是
\[
\frac{\|\Pi_S u\|}{\|u\|},
\]
而不是平方量；因而 v1.2 最少也要把它替换为
\[
\frac{\|\Pi_S u\|^2}{\|u\|^2},
\]
然后把 JSON 里的 `analytic_capture_law_for_unit_vector`、`analytic_beta_alpha`、`analytic_beta_beta` 与代码用到的统计量改为同一个对象。否则所谓 “Beta null closure” 只是口头 closure，不是代码 closure。【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L237-L243】【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L540-L588】【bundle: from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_1_20260625.json L196-L217】

### 对每块测试的严格解释

`quotient_descent_control` 的价值，不在于“花哨”，而在于它修复 report(27) 指出的一个真实不对称：目前 v1.1 note 已有 quotient descent 命题，但 harness 中还没有独立 block。补这一块后，note 与 harness 的对应关系会明显更干净。【bundle: from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_1_strict_audit_20260626.md L36-L36】

`common_ambient_registration_control` 的价值，在于把 v1.1 中还只是“先注册再说”的约束变成可执行规则：如果没有注册，就让 block 返回 `invalid_artifact`；如果两个注册等价，就要求所有 registered metrics 一致。这会直接杀死“未注册 fancy invariant”这类最容易装饰化的说法。【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_1_20260625.md L146-L165】

`rank1_perturbation_bound_control` 的价值也不是“再来一个 rank 测试”，而是把 v1.1 已存在的数学命题
\[
\sigma_2(M)\le \|E\|_2
\]
变成 **独立数值单测**。这正是 report(27) 点名需要补的“theorem-backed test”，而不是继续只拿 `sigma_2/\sigma_1 >= 0.25` 的 review floor 当判据。【bundle: from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_1_strict_audit_20260626.md L24-L24】【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md L141-L145】

`threshold_contract_single_source_control` 则是整个工程面最不能省的一块。因为 v1.1 当前的缺口不是“没有合同”，而是“合同不是唯一执行源”；只要这一点不改，任何 JSON 中的 thresholds 都可能沦为装饰。bundle 的 v1.2 workplan 已经把这一点写成 exit gate，我赞成原封不动采纳。【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md L121-L133】【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md L156-L165】

## 降级与禁语清单

先说数学降级。即便 v1.2 做完，下列话也仍然不应说：
**“common ambient invariant theory 已完整完成”**、**“random-subspace null 已成为绝对无结构判定器”**、**“product-weight theorem 覆盖了 non-product 情形”**、**“square holonomy telescoping 已经等于 sheaf obstruction theory”**、**“0.25 rank floor 是普遍数学常数”**。这些要么被 v1.1 audit 直接否定，要么被 workplan 明确限定在更小边界里。【bundle: from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_1_strict_audit_20260626.md L20-L28】【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md L85-L119】

再说经验禁语。bundle 多处已经写死：不得说 full panel 已跑、16-cell aggregate 已存在、MaoField residual / interaction / quotient-residual / transport / holonomy field 已观测到、glass_box_broken、F3_positive、LOSO_passed、checkpoint loading/model inference/training/new loss 已发生或已授权。这些不是语气问题，而是硬边界问题；v1.2 不会也不能改变这个边界。【bundle: 00-README_FOR_142_AND_PRO.md L16-L36】【bundle: from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_1_STRICT_AUDIT_ADOPTION_NOTE_20260626.md L101-L121】【bundle: from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_1_20260625.md L89-L104】

我还要补三条经常会被“数学项目自我鼓舞”偷偷带出来的禁语。第一，**“passing synthetic harness = empirical evidence”** 仍然必须判死；v1.1 summary 与 JSON 已经反复写明这只是 zero-GPU synthetic-only 的 design review。【bundle: from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_1_20260625.md L5-L16】【bundle: from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_1_20260625.json L69-L77】

第二，**“product-reweighting separation 的通过 = v1.1 提供了独立数学证明”** 也不能说。当前这块本质上是 regression reproduction：脚本复现 note 中的反例数值，这是合理的回归测试，但不是独立于 note 的外部数学证据。【bundle: from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_1_strict_audit_20260626.md L56-L56】【bundle: from_repo/scripts/debranded_residual_transport_harness_v1_1.py L361-L385】

第三，**“v1.2 做完以后就是 completed formal system”** 仍不该说。理由很直接：整个 bundle 始终只允许 `definitions_and_harness_viable_only` 作为最强本地 verdict，而且 research index 明说 v1.2 的任务是最小 honest patch，不是把项目上升为封口总论。这个 ceiling 在本任务里没有任何授权被抬高。【bundle: 00-README_FOR_142_AND_PRO.md L44-L54】【bundle: from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_1_STRICT_AUDIT_ADOPTION_NOTE_20260626.md L33-L37】【bundle: from_repo/GPT55_PRO_RESEARCH_INDEX_20260622.md L1399-L1414】

## 实施清单、通俗说明与最终分类

### 本地 Codex 实施清单

最小实施路径应当只涉及一组 note、一个新脚本、一个 summary、一个 JSON，以及必要的索引更新，不要再扩项目边界：

- 新增 `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260626.md`，把上面四块正式写入：registered ambient、Beta squared capture、product-weight theorem、square holonomy telescoping。
- 新增 `from_repo/scripts/debranded_residual_transport_harness_v1_2.py`，采用“metrics 生成器 + 中央 evaluator + 单一 contract builder”的结构，不要从 v1.1 继续复制硬编码 pass 语句。
- 新增 `from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260626.md` 与 `synthetic_harness_v1_2_20260626.json`，并确保 test names 与脚本、summary、note 完全一致。
- 保留 v1.1 JSON 与脚本，不要覆写；workplan 已明确要求 v1.2 单独版本化，而不是修改 v1.1 工件。【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md L135-L154】

本地验证步骤也应当写死，而不是口头约定：

```bash
python3 -m py_compile from_repo/scripts/debranded_residual_transport_harness_v1_2.py
python3 from_repo/scripts/debranded_residual_transport_harness_v1_2.py \
  --out /tmp/.../synthetic_harness_v1_2_20260626.json \
  --summary-md /tmp/.../SYNTHETIC_HARNESS_V1_2_20260626.md
python3 -m json.tool /tmp/.../synthetic_harness_v1_2_20260626.json > /dev/null
```

随后应增加四个一致性检查：test names 一致、顶层 `threshold_contract` 与每个 test 内嵌 thresholds 一致、`threshold_contract_single_source_control` 通过、blocked claims 原样保留。這正是 v1.2 exit gate 的直接实现。【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md L156-L171】

文档与索引更新也不要省。`STATE.md` 已把 D625-D626 这条线登记为当前“新方向 formal start / v1.2 minimal patch”入口，因此 v1.2 工件一旦提升，就应更新 `STATE.md`、`MD_CATALOG.md`、`GPT55_PRO_RESEARCH_INDEX_20260622.md`，并补一条 RAG refresh record。STATE 当前已经把这一整串路径列为单一真相源的一部分，索引不更新会让下游 agent 冷启动读错版本。【bundle: from_repo/STATE.md L86-L92】【bundle: from_repo/GPT55_PRO_RESEARCH_INDEX_20260622.md L1370-L1433】

### 初中生解释

把这件事说得最简单：v1.2 的目标不是“宣布 MaoField 里发现了什么神秘结构”，而是把一个已经有模样的有限维数学玩具，修成一个**更不容易自欺的数学对象**。现在这个对象里，最重要的东西是：先把你事先登记好的“无关部分”投影掉，再看剩下的东西在不同空间、不同边、不同路径、不同随机对照下会不会稳定地留下来。bundle 已经很明确：这条线现在最多只能证明“定义和 harness 设计是可执行的”，不能证明 MaoField 里真的观测到了什么场或结构。【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_1_20260625.md L287-L294】【bundle: from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_1_20260625.md L81-L104】

所以，v1.2 若做成，它会让这个对象在数学上更像回事：因为它把“先注册 ambient”“随机对照到底比什么统计量”“何时才能使用 product-measure Hoeffding 语言”“square holonomy 的问题到底坏在哪一条边”这些最容易糊掉的地方都钉死了。但这仍然**完全不等于** MaoField 的经验结论升级；它只是把一份有限维数学讲义修得更诚实、更可审计而已。【bundle: from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_1_STRICT_AUDIT_ADOPTION_NOTE_20260626.md L72-L99】【bundle: from_repo/GPT55_PRO_RESEARCH_INDEX_20260622.md L1399-L1414】

### 最终分类

**v1_2_small_patch_feasible**

理由很直接：
v1.1 的主骨架已被 bundle 自己认可为 `accept_with_v1_2_required`；v1.2 workplan 已把缺口收缩为四个局部 formal/harness 收口点；我上面给出的 patch 也都保持在有限维、零 GPU、无经验升级、无项目外扩的边界内。因此它是小补丁，而不是大修，也不是应当整件驳回的对象。【bundle: from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_1_STRICT_AUDIT_ADOPTION_NOTE_20260626.md L39-L54】【bundle: from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md L34-L45】【bundle: from_repo/GPT55_PRO_RESEARCH_INDEX_20260622.md L1401-L1408】

无论这个分类如何，Mode B MaoField empirical status 都必须继续保持：

**insufficient_artifact**【bundle: 00-README_FOR_142_AND_PRO.md L50-L54】【bundle: from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_1_STRICT_AUDOPTION_NOTE_20260626.md L27-L31】