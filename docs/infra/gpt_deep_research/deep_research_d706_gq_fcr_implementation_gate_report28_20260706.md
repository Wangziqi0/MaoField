# D706 外部数学落地闸门裁决

## 裁决摘要

我的结论是：**该对象在严格收缩后的表述下可以落地，node36 可以直接实现 v1.5 exact rational artifacts；但实现的必须是“狭义、有限、声明式 gauge quotient 的两图重叠证书”，而不是任何广义 sheaf / contextuality / dependent-ANOVA / projection theory 叙事。** 因而我选择的唯一分支是：

```text
APPROVE_NODE36_IMPLEMENT_V1_5_GQ_FCR
```

这一结论与包内当前意图一致：`PACKAGE_README.md` 明确把本轮任务限定为“修复或批准 Gauge-Quotiented Finite Consistency Radius”，并强调本包不是论文授权、不是经验性证据、也不是广义理论宣称；`STATE.md` 与 D706 external scan 也都把当前安全目标收束为一个**gauge-quotiented residual-audit specialization**，而不是更大的 sheaf / contextuality / ANOVA / projection 理论。（仓库：`PACKAGE_README.md` 5-11 行；`from_repo/STATE.md` 24-28 行；`from_repo/docs/infra/external_math_search/EXTERNAL_MATH_OBJECT_SCAN_D706_20260706.md` 14-22、45-79、144-173 行）

但我要同时指出一个**必须在 formal note 中立即修补的语义点**：当前 draft 中“`Delta^2>0` 排除 declared-gauge pasted object”这句话，只有在你把“declared gauge”解释为**重叠空间上的商兼容性**，或者额外加入**局部 gauge 参数空间与 overlap transfer maps**时才严格成立。否则，“只给一个 overlap gauge 子空间 Γ”并不能自动推出“存在真实局部 gauge 调整”的语义。这个修补不阻止实现，反而正好给 v1.5 一个清楚的核心定理 / 条件推论分裂结构。（仓库：`from_repo/docs/infra/debranded_residual_transport/TWO_CHART_GLUE_CERTIFICATE_V1_5_MATH_LANDING_DRAFT_20260706.md` 121-155 行；`from_repo/docs/infra/gpt_deep_research/deep_research_finite_glue_certificate_report27_20260705.md` 31-71 行）

## 先行文献闸门

先说最重要的一句：**MaoField 不能声称自己发明了 consistency radius。** Robinson 的官方期刊页面直接把“assignment to a sheaf”“consistency radius”“consistency filtration”“robust to perturbations”这些关键词都摆在摘要里，因此任何把本对象包装成“新的 consistency radius 理论”的说法都会越界。MaoField 能说的，只能是：在自己的有限 residual-audit 语境里，取了一个**声明式 overlap gauge quotient**，并把它压成 exact rational paired controls；这是一种**特化实现**，不是 abstract notion 的首创。citeturn6view0

同样，**MaoField 不能声称自己进入了广义 cellular sheaf / sheaf cohomology / global sections 理论。** Curry 的 thesis 摘要已经把 cellular sheaves 说成“由 cell complex 参数化的有限向量空间与映射家族”，并且已经讨论到 sheaf cohomology、cellular sheaf homology、interleaving distance 与 global sections 的结构性结果。也就是说，只要你用“有限 carriers + restriction maps + overlap compatibility”这套语言，你就已经站在一个文献非常成熟的地带里；MaoField 最多只是借用其中一个**极窄的有限线性代数切片**。citeturn7view1turn7view2

对 **Abramsky–Brandenburger contextuality** 也必须严格降温。其 arXiv 官方摘要明确写到：contextuality（以及 non-locality）与**global sections 的存在障碍**严格对应，并且给出线性代数计算框架与 no-go hierarchy。于是，MaoField 绝不能把自己的两图 overlap obstruction 说成“新的 contextuality obstruction”，也不能说它已经进入一般 measurement cover 框架。最多只能说：**在一个非常窄的有限重叠设置里，它给出一个与“global-section failure”形式相近的兼容性证书。** citeturn7view0turn7view3

对 **dependent-input ANOVA / Hoeffding-Sobol / Shapley** 也一样。Hooker 已处理 dependent variables 下的 generalized functional ANOVA；Chastaing–Gamboa–Prieur 已给 generalized Hoeffding-Sobol decomposition；Owen–Prieur 则明确指出，输入依赖时，基于 ANOVA 的替代量会遇到概念与计算问题，而 Shapley value 是现成回应之一。于是，MaoField 完全不能把自己的 `2×2` additive gauge 说成新的广义 dependent-input decomposition。它能说的，只是：**这里重用了一种“声明 nuisance 子空间再投影 away”的有限证明风格**，而不是建立新的分解理论。citeturn5search1turn5search2turn6view5

至于 **two-projection / two-subspace theory**，Böttcher–Spitkovsky 的官方摘要已经把这块背景说得很清楚：该文是 two projections 理论的 survey，并特别包含 Halmos 关于 two orthogonal projections 的经典结果。于是，MaoField 不能声称在投影理论本身上有新定理；它只能说，自己已有的 v1.3/v1.4 order-defect spine 与此邻近，而 v1.5 GQ-FCR 只是把“先声明 nuisance 再看 surviving mismatch”的逻辑，搬到了两个局部 section 的 overlap 上。citeturn6view6

因此，**MaoField 此轮可 claim / 不可 claim 的边界**应写成下面这样：

可 claim 的只有这句：**给定有限 carriers、restriction maps、正有理 overlap 权重与声明的 overlap gauge 子空间，可以构造一个 exact rational 的 gauge-quotiented overlap mismatch certificate；在 `2×2` uniform-additive toy control 中，它有严格的正控 `Delta^2=0` 与反控 `Delta^2=1`，并与现有 same-carrier order-defect spine 形成一个狭义邻接对象。** 这与包内 external scan、draft、taskbook 的安全表述是一致的。（仓库：`from_repo/docs/infra/external_math_search/EXTERNAL_MATH_OBJECT_SCAN_D706_20260706.md` 55-79、153-171 行；`from_repo/docs/infra/recovery/MAOFIELD_D706_EXTERNAL_MATH_LANDING_TASKBOOK_20260706.md` 31-48、63-81 行；`from_repo/docs/infra/debranded_residual_transport/TWO_CHART_GLUE_CERTIFICATE_V1_5_MATH_LANDING_DRAFT_20260706.md` 245-290 行）

不可 claim 的包括：发明 sheaf consistency radius；建立 broad sheaf/cellular-sheaf/global-section/cohomology/contextuality 理论；提出新的 dependent-input ANOVA / Hoeffding-Sobol / Shapley 框架；提出一般 two-projection / two-subspace 新理论；以及任何 MaoField empirical positive result。这个边界既是外部文献强加的，也是包内 `STATE.md`、decision brief、taskbook 明示的。（仓库：`from_repo/STATE.md` 24-28 行；`from_repo/docs/infra/recovery/MAOFIELD_D706_PRO_DECISION_BRIEF_FROM_RAG_STATUS_MEMORY_20260706.md` 99-117 行；`from_repo/docs/infra/recovery/MAOFIELD_D706_EXTERNAL_MATH_LANDING_TASKBOOK_20260706.md` 63-77 行） citeturn6view0turn7view1turn7view3turn6view5turn6view6

## 定义闸门

我建议把 v1.5 的**核心定义**与**加强版 realized-gauge 定义**分开写。

核心定义只需要以下有限数据。给定有限集合 `I_1, I_2, O_12`，令 `H_i = Q^{I_i}`、`V_12 = Q^{O_12}`；给定有理线性 restriction maps `rho_i : H_i -> V_12`；给定逐点严格正的 overlap 权重 `w_12(o)>0`；再给定一个声明的 overlap gauge / nuisance 子空间 `Gamma_12 ⊆ V_12`。对任意局部 sections `s_1, s_2`，定义 raw overlap mismatch
\[
m_{12}(s_1,s_2)=\rho_1 s_1-\rho_2 s_2,
\]
以及带权内积
\[
\langle u,v\rangle_{w_{12}}=\sum_{o\in O_{12}} w_{12}(o)u(o)v(o).
\]
再定义
\[
\Delta^2_{12}(s_1,s_2;\Gamma_{12})
=
\min_{\gamma\in\Gamma_{12}}
\|m_{12}(s_1,s_2)-\gamma\|_{w_{12}}^2.
\]
如果脚本以一组独立 gauge basis `G=[g_1 ... g_r]` 给出 `Gamma_12`，则 exact projection 应明确写成
\[
P_\Gamma = G\,(G^\top W G)^{-1}G^\top W,
\qquad W=\mathrm{diag}(w_{12}),
\]
于是
\[
\Delta^2_{12}=\|(I-P_\Gamma)m_{12}\|_{w_{12}}^2.
\]
这与当前 draft 的主公式一致，也与 v1.4 exact script 里“带权投影矩阵 + Fraction 逆 Gram 矩阵”的实现风格同型。（仓库：`from_repo/docs/infra/debranded_residual_transport/TWO_CHART_GLUE_CERTIFICATE_V1_5_MATH_LANDING_DRAFT_20260706.md` 33-83 行；`from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py` 51-99 行）

这里有一个小但重要的**修补**：`Gamma_12` 作为抽象子空间已经足够定义 `Delta^2`，所以 core object 完全成立；但如果想把“compatible modulo gauge”进一步翻译成“存在真实局部 gauge 调整后可以 paste”，那么还必须补入 **realized gauge data**：
\[
G_1,\;G_2,\;\lambda_1:G_1\to V_{12},\;\lambda_2:G_2\to V_{12},
\]
并要求
\[
\Gamma_{12}=\mathrm{im}(\lambda_1)-\mathrm{im}(\lambda_2).
\]
这一层在 Report27 中其实已经写得更严谨；只是当前 v1.5 draft 把它压缩掉了。我建议 formal note 直接把这层写成**条件性加强版 corollary**，而不是硬塞进 core definition。这样既不扩大对象，也把语义漏洞补上。（仓库：`from_repo/docs/infra/gpt_deep_research/deep_research_finite_glue_certificate_report27_20260705.md` 31-71 行）

因此，我认可的 **certificate tuple** 应该是：

\[
\Xi_{12}^{\mathrm{core}}=
(
artifact\_id,
I_1,I_2,O_{12},
\rho_1,\rho_2,
w_{12},
\Gamma_{12},
s_1,s_2,
m_{12},
P_\Gamma,
(I-P_\Gamma)m_{12},
\Delta^2_{12},
checks,
evidence\_boundary
).
\]

若要支持“realized local gauge”语义，再可选扩展为

\[
\Xi_{12}^{\mathrm{realized}}
=
\Xi_{12}^{\mathrm{core}}
\cup
(G_1,G_2,\lambda_1,\lambda_2).
\]

JSON 里所有有理数必须是字符串；矩阵按 row-major 存；并保留 `arithmetic = "fractions.Fraction"`、`runtime`、`strongest_allowed_verdict`、`blocked_claims` 这套 v1.4 风格元数据。Report27 对 schema 的建议与 v1.4 exact witness 都支持这一点。（仓库：`from_repo/docs/infra/gpt_deep_research/deep_research_finite_glue_certificate_report27_20260705.md` 91-144 行；`from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json`；`from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md` 30-66 行）

## 定理闸门

**核心定理我予以通过。**

设
\[
m = m_{12}(s_1,s_2)=\rho_1 s_1-\rho_2 s_2.
\]
因为所有权重严格为正，所以 `V_12` 上的带权内积是正定内积；有限维情形下，`Gamma_12` 有唯一带权正交分解
\[
m=P_\Gamma m + (I-P_\Gamma)m.
\]
因此
\[
\Delta^2_{12}(s_1,s_2;\Gamma_{12})
=
\min_{\gamma\in\Gamma_{12}}\|m-\gamma\|_{w_{12}}^2
=
\|(I-P_\Gamma)m\|_{w_{12}}^2.
\]
于是
\[
\Delta^2_{12}=0
\iff
(I-P_\Gamma)m=0
\iff
m\in \Gamma_{12}.
\]
这就严格证明了 **“`Delta^2=0` 当且仅当 compatibility modulo declared overlap gauge”**。所以 core theorem 没有问题，而且它本质上就是“到声明子空间的带权平方距离”的零判别命题。（仓库：`from_repo/docs/infra/debranded_residual_transport/TWO_CHART_GLUE_CERTIFICATE_V1_5_MATH_LANDING_DRAFT_20260706.md` 94-119 行）

接下来是你要求的更强命题：**“`Delta^2>0` 排除 declared-gauge pasted object。”** 这一条我给出的是**条件通过**。如果 formal note 里的 “pasted object” 只指**商意义下的重叠兼容性**，也就是“在 quotient `V_{12}/\Gamma_{12}` 中两者 restrictions 相等”，那么它立即由上面的 iff 定理推出；此时 `Delta^2>0` 就等价于“不存在落在同一 declared gauge class 的 overlap compatibility”。但如果“pasted object”被解释成“存在真实局部 gauge 参数 `g_1,g_2`，使 gauge-adjusted restrictions 在 overlap 上相等”，那就必须加入上节说的 `G_i,\lambda_i` 数据，并要求 `\Gamma_{12}=\mathrm{im}\lambda_1-\mathrm{im}\lambda_2`。在这个附加前提下，
\[
\rho_1 s_1-\lambda_1 g_1 = \rho_2 s_2-\lambda_2 g_2
\iff
m \in \Gamma_{12}
\iff
\Delta^2_{12}=0.
\]
于是 `Delta^2>0` 才能严格推出“无 realized-gauge paste”。我的裁决是：**formal note 必须把这两层语义切开。** 这不是否决，而是必要修辞修补。（仓库：`from_repo/docs/infra/debranded_residual_transport/TWO_CHART_GLUE_CERTIFICATE_V1_5_MATH_LANDING_DRAFT_20260706.md` 121-155 行；`from_repo/docs/infra/gpt_deep_research/deep_research_finite_glue_certificate_report27_20260705.md` 40-71、220-240 行）

**Gauge monotonicity** 也通过。若 `\Gamma_{12}\subseteq \Gamma'_{12}`，那么最小化是对更大可选集合进行，因此
\[
\Delta^2_{12}(s_1,s_2;\Gamma'_{12})
\le
\Delta^2_{12}(s_1,s_2;\Gamma_{12}).
\]
这句话必须被解释为：一切 obstruction 都是**相对于声明的 gauge**而言；一旦扩大 gauge 后 obstruction 消失，原结论就只能是“相对旧 gauge 的障碍”，而不是更深的结构性矛盾。这和包内 draft / Report27 反复强调的 fail-closed 纪律完全一致。（仓库：`from_repo/docs/infra/debranded_residual_transport/TWO_CHART_GLUE_CERTIFICATE_V1_5_MATH_LANDING_DRAFT_20260706.md` 136-155 行；`from_repo/docs/infra/gpt_deep_research/deep_research_finite_glue_certificate_report27_20260705.md` 238-240 行）

**`2×2` 正负控制** 也通过，并且可以 exact rational 化。按 row-major 顺序
\[
(q_1,b_1),(q_1,b_2),(q_2,b_1),(q_2,b_2),
\]
取 uniform 权重 `w=(1/4,1/4,1/4,1/4)`，再取 additive gauge basis
\[
\mathbf 1=(1,1,1,1),\quad
q=(-1,-1,1,1),\quad
b=(-1,1,-1,1).
\]
在此带权内积下，这三个向量是正交归一的，因此 `P_\Gamma` 极易 exact 计算。对正控
\[
m_+=(1,2,3/2,5/2)
=
(7/4)\mathbf 1 + (1/4)q + (1/2)b,
\]
故 `m_+ \in \Gamma`，所以 `Delta^2(m_+;\Gamma)=0`。对反控
\[
m_-=(1,-1,-1,1),
\]
它与 `\mathbf 1,q,b` 全部带权正交，故它正好落在 additive gauge 的正交补方向上，于是
\[
(I-P_\Gamma)m_-=m_-,
\qquad
\Delta^2(m_-;\Gamma)=\|m_-\|_w^2=1.
\]
这与 v0/v1.1 harness 的 “absorbed mismatch / checkerboard obstruction” 模式完全同源，只是 v1.5 将其升级成 exact Fraction 证书。（仓库：`from_repo/docs/infra/debranded_residual_transport/TWO_CHART_GLUE_CERTIFICATE_V1_5_MATH_LANDING_DRAFT_20260706.md` 157-223 行；`from_repo/docs/infra/gpt_deep_research/deep_research_finite_glue_certificate_report27_20260705.md` 152-204 行；`from_repo/scripts/debranded_residual_transport_harness_v1_1.py` 682-697 行）

**它与旧 same-carrier order-defect theorem 的关系，是“邻接而非同一”。** v1.3 / v1.4 的核心内容是：在非 product 权重下，`P_A` 与 `P_B0` 的顺序剥离会出现 noncommuting order defect，并存在纯主效应 witness，使真加性残差为零、一个顺序输出为零、另一个顺序输出非零；v1.4 则把这个最小 `2×2` 见证做成了 exact rational 证书。GQ-FCR 则完全不同：它只测量两个局部 sections 的 overlap mismatch 到某个声明 gauge 子空间的距离。它**不**给 product / non-product weights 的 iff，不讨论 ordered stripping operators 的交换子，也不推出 v1.3 的存在性 no-go。它和 v1.3 的唯一正式关系，是：在退化的 same-carrier 特例里，任何给定 mismatch 向量都可被喂进 `Delta^2`；但那只是 specialization，不是 theorem identity。（仓库：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 156-191、241-321、360-369 行；`from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md` 30-66 行；`from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py` 126-220 行）

## 实现闸门

node36 现在就可以实现下面四个工件，不需要再向我请求更多仓库文件：

```text
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md
scripts/debranded_residual_transport_exact_gq_fcr_v1_5.py
docs/infra/debranded_residual_transport/exact_gq_fcr_v1_5_20260706.json
docs/infra/debranded_residual_transport/EXACT_GQ_FCR_V1_5_20260706.md
```

formal note 的结构我建议写成四块：先写 **Core Definition**；再写 **Core Compatibility Theorem**；然后写 **Conditional Realized-Gauge Corollary**；最后写 **Exact `2×2` Controls** 与 **Relation to v1.3/v1.4**。其中“realized-gauge corollary”必须明确以 `G_i,\lambda_i` 的存在为条件，否则不要用“gauge-adjusted local sections can be pasted”这种更强句式。（仓库：`from_repo/docs/infra/recovery/MAOFIELD_D706_EXTERNAL_MATH_LANDING_TASKBOOK_20260706.md` 31-48、50-81 行；`from_repo/docs/infra/gpt_deep_research/deep_research_finite_glue_certificate_report27_20260705.md` 31-71、91-144 行）

`scripts/debranded_residual_transport_exact_gq_fcr_v1_5.py` 必须强制执行以下 exact assertions：

- 所有有理数一律经 `fractions.Fraction` 解析；脚本内**不得**以浮点数作为证明权威。这个要求与 v1.4 风格一致。（仓库：`from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py` 1-15、126-220 行）
- 控制实例可直接采取最小 primitive 版本：`I_1 = I_2 = O_12`，`rho_1 = rho_2 = I`，然后分别取 `(s_1,s_2)=(m_+,0)` 与 `(m_-,0)`；这样就既满足“carrier / sections / restrictions”元数据要求，又不引入不必要 chart 语法。（仓库：`from_repo/docs/infra/gpt_deep_research/deep_research_finite_glue_certificate_report27_20260705.md` 176-188 行）
- `weights_row_major` 必须逐项严格为正；控制中取 uniform `1/4` 四元组。
- `gauge_basis_row_major = [1,q,b]` 必须做 rank check；独立基的 Gram 矩阵 `G^T W G` 必须可逆。
- 计算出的 `P_Gamma` 必须 exact 满足 `P^2=P`，并满足 weighted self-adjointness，即 `W P = P^T W`。
- 正控必须 exact 验证 `m_plus = (7/4)1 + (1/4)q + (1/2)b`、`projected_mismatch = 0`、`Delta^2 = 0`。
- 反控必须 exact 验证 `⟨m_-,1⟩_w = ⟨m_-,q⟩_w = ⟨m_-,b⟩_w = 0`、`projected_mismatch = m_-`、`Delta^2 = 1`。
- gauge monotonicity 必须有一个 exact witness：取 `Gamma' = span{1,q,b,c}`，其中 `c=(1,-1,-1,1)`，并验证 `Gamma ⊂ Gamma'`、`Delta^2(m_-;\Gamma') = 0 ≤ 1 = Delta^2(m_-;\Gamma)`。
- JSON 中所有有理数、向量、矩阵都必须以字符串保存；矩阵 row-major；并声明 `arithmetic = "fractions.Fraction"`。
- `EXACT_GQ_FCR_V1_5_20260706.md` 必须像 v1.4 一样，打印 artifact 名、sha256、所有 exact checks、正控与反控的关键向量、`Delta^2` 值以及 boundary sentence。（仓库：`from_repo/docs/infra/debranded_residual_transport/TWO_CHART_GLUE_CERTIFICATE_V1_5_MATH_LANDING_DRAFT_20260706.md` 269-290 行；`from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md` 9-66 行）

我建议 `exact_gq_fcr_v1_5_20260706.json` 至少包含这些顶层字段：`artifact`、`date`、`status`、`evidence_boundary`、`carrier_manifest_1`、`carrier_manifest_2`、`overlap_manifest_12`、`restriction_matrices_row_major`、`weights_row_major`、`gauge_basis_row_major`、`gauge_gram_matrix_row_major`、`projection_matrix_row_major`、`complement_projection_matrix_row_major`、`positive_control`、`negative_control`、`enlarged_gauge_monotonicity_check`、`checks`、`all_checks_passed`、`runtime`。若想为未来兼容 realized-gauge 版本，可预留 `gauge_transfer_matrices_row_major`，但在 v1.5 primitive control 里允许置空。这个 schema 与 Report27 建议和 v1.4 exact witness 风格兼容。（仓库：`from_repo/docs/infra/gpt_deep_research/deep_research_finite_glue_certificate_report27_20260705.md` 91-144 行；`from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json`；`from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py` 167-220 行）

这里还要补一句实现边界：**不要把 v1.5 写成 broad consistency-radius theory、broad sheaf theory、contextuality theorem、dependent-input ANOVA theorem，或 two-projection theorem companion paper。** node36 写 formal note 时必须在 boundary 段中明确说明：这只是一个 finite exact certificate，MaoField empirical Mode B 仍然是 `insufficient_artifact`，Zenodo/GitHub 只是记录面而非同行评审。这个边界包内早已锁死。（仓库：`from_repo/STATE.md` 24-28 行；`from_repo/docs/infra/recovery/MAOFIELD_D706_PRO_DECISION_BRIEF_FROM_RAG_STATUS_MEMORY_20260706.md` 99-117 行；`from_repo/docs/infra/recovery/MAOFIELD_D706_EXTERNAL_MATH_LANDING_TASKBOOK_20260706.md` 63-77 行）

## 最终决定

最终决定如下：

```text
APPROVE_NODE36_IMPLEMENT_V1_5_GQ_FCR
```

执行含义是：**立刻实现 v1.5，但实现内容必须是“core overlap-gauge quotient certificate”，并把“realized-gauge pasting”降为条件性 corollary。** 不需要 pivot 到 three-chart cocycle，也不需要转向 support-rank ANOVA defect，因为 external scan 已把三图对象标成 “next after two-chart”，并明确指出它更接近 Čech / contextuality 语言、先行文献风险更高；support-rank ANOVA defect 则被标成 promising later，而不是当前首落地点。（仓库：`from_repo/docs/infra/external_math_search/EXTERNAL_MATH_OBJECT_SCAN_D706_20260706.md` 81-118、144-173 行）

如果 node36 严格按以上边界写 note、脚本、JSON、markdown 证书，那么这轮对象既**足够数学化**，又**没有越过先行文献边界**。换句话说：它不是新的大理论，但它是一个真实、有限、可 exact-rational 验证、并且足以接到 v1.3/v1.4 主脊柱上的新对象。这正是本轮应当落地的东西。（仓库：`from_repo/docs/infra/external_math_search/EXTERNAL_MATH_OBJECT_SCAN_D706_20260706.md` 47-79、153-173 行；`from_repo/docs/infra/recovery/MAOFIELD_D706_EXTERNAL_MATH_LANDING_TASKBOOK_20260706.md` 31-48；`from_repo/docs/infra/debranded_residual_transport/TWO_CHART_GLUE_CERTIFICATE_V1_5_MATH_LANDING_DRAFT_20260706.md` 269-290 行）