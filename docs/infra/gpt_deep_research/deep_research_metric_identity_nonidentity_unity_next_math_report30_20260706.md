# MaoField 指标对象同一性与非同一性严格数学决策评审

## 原始 claim-chain 的裁定

**唯一裁定：`TRANSLATION_CORRECT_BUT_INCOMPLETE`。** 包内自己的最高层安全口径已经把原始 “non-identity / unity” 论链收缩并翻译为一组可数学化对象：`measurement-object identity / metric-object identity / metric-form fetishism / defect certificate`；同时又明确声明，这还**不是**一个完成的广义理论，当前真正完成的硬对象只有狭义有限精确工件：v1.3/v1.4 的 order-defect 主脊柱与精确 `2×2` 见证，再加上作为**独立相邻 exact note** 保留的 v1.5 GQ-FCR。也就是说，翻译方向本身是对的，但它的严格可证部分仍然是窄核，而不是一套已经收官的总理论。 （`PACKAGE_README.md:L30-L50`; `from_repo/STATE.md:L16-L28`; `from_repo/docs/infra/MAOFIELD_METRIC_IDENTITY_PROGRAMME_ADOPTION_NOTE_20260704.md:L36-L73`）

更具体地说，原始的“非同一”已经有了一个真正的数学落点：在有限正权二向表上，若权重不是 product form，则顺序化 nuisance stripping 的两个输出不再相同，而且这种失败可以用精确算子差 `D_w=R_{Q→B}-R_{B→Q}` 与 exact `2×2` 见证来证成；原始的“统一”也有了数学落点，但它不是无条件的“统一”，而是**在声明好的 transport / invariance / coherence 条件下的条件同一性**。因此，“unity”不能再被理解为先验本体同一，而只能理解为一个要被证明的 transport 命题。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:L156-L227`; `from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md:L30-L66`; `from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_phaseii_report25_20260705.md:L74-L123`）

这套翻译之所以只能判为“正确但未完成”，而不能判为“已经足够强到下一对象全部成立”，原因有三。第一，programme note 与 adoption note 只把 chart、transport、defect、`OI`、certificate library 等对象提升到了**定义层 / 方向层**，并未把它们全部提升为 formal note 级定理。第二，v1.5 GQ-FCR 已经精确落地，但 formal note 明言它与 v1.3/v1.4 的关系是 **adjacency, not identity**，因此它不能被当成“同一总理论的自然补丁”。第三，包内持续锁死了大量 forbidden upgrades：不能从这些对象跳到 broad ANOVA、broad sheaf/contextuality、观测到真实 transport/holonomy/gluing field、或 MaoField empirical positive result。 （`from_repo/docs/infra/MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md:L663-L810`; `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L229-L277`; `PACKAGE_README.md:L30-L41`; `from_repo/STATE.md:L22-L28`）

因此，原始“non-identity and unity”的有效数学着陆应当被精确表述为：**非同一** = 在有限 charted metric object 之间，transport / intertwining / coherence 失败，并可由 exact defect certificate 见证；**统一** = 只有在声明的原始 transport 与对象 transport 下满足 intertwining 且具备 coherence 时，两个输出才被许可视作“同一个对象”。这与原始哲学矿石是同向的，但比原始表述更窄、更硬、也更可审计。 （`from_repo/docs/infra/MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md:L21-L38,L134-L173,L692-L718`; `from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_phaseii_report25_20260705.md:L74-L165`）

## 安全数学核心

| 条目 | 分类 | 简短理由 | 关键证据 |
|---|---|---|---|
| finite positive weighted two-way table | `PROVEN_IN_PACKAGE` | v1.3 formal note 以 `X=Q×B`、严格正权、加权内积为环境，属于主定理设定本体。 | `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:L41-L62` |
| additive nuisance subspace | `PROVEN_IN_PACKAGE` | `C, A, B0, N_add=C⊕A⊕B0` 被正式定义，并是“真加性残差/假残差”区分的基础。 | `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:L64-L103` |
| product-weight iff main-effect orthogonality | `PROVEN_IN_PACKAGE` | Proposition 1 直接证明 `w` 为 product form 当且仅当 `A ⟂ B0`。 | `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:L104-L153` |
| order-independence iff product weights | `PROVEN_IN_PACKAGE` | Proposition 2 直接证明 `D_w=0 iff w` 为 product form，等价于 `R_{Q→B}=R_{B→Q}`。 | `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:L177-L227` |
| exact 2 x 2 order-defect witness | `CERTIFICATE_COMPLETE` | v1.4 Markdown/JSON/script 已把最小 `2×2` 非 product 见证做成 exact rational 证书。 | `EXACT_WITNESS_V1_4_20260629.md:L30-L66`; `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:L285-L335` |
| deterministic harness | `COMPLETE_LOCAL_DRAFT` | harness 工件完整存在，但其角色被明确限制为 deterministic regression support，而非证明载体。 | `SYNTHETIC_HARNESS_V1_3_20260628.md:L96-L107`; `PACKAGE_README.md:L32-L41` |
| metric-object identity definition | `FORMALIZABLE_NOW` | programme note 与 report25 adoption 已给出 chart-dependent object 的定义骨架，但尚未提升为独立 formal note。 | `MAOFIELD_METRIC_IDENTITY_PROGRAMME_ADOPTION_NOTE_20260704.md:L62-L73`; `METRIC_IDENTITY_PHASEII_REPORT25_ADOPTION_NOTE_20260705.md:L54-L84` |
| chart transport / intertwining condition | `FORMALIZABLE_NOW` | `T_{c→c'}∘Φ_c=Φ_{c'}∘U_{c→c'}` 已被明确提出为 identity 的必要结构，但仍停在定义层。 | `deep_research_metric_identity_phaseii_report25_20260705.md:L74-L105`; `METRIC_IDENTITY_PHASEII_REPORT25_ADOPTION_NOTE_20260705.md:L71-L77` |
| defect certificate tuple | `FORMALIZABLE_NOW` | `C=(c,c',K,Δ)` 与 `Δ=T_{c→c'}M_c(K)-M_{c'}(U_{c→c'}K)` 已被清晰提出，可立即冻结。 | `deep_research_metric_identity_phaseii_report25_20260705.md:L107-L123`; `METRIC_IDENTITY_PHASEII_REPORT25_ADOPTION_NOTE_20260705.md:L78-L83` |
| audit-order instability index `OI` | `FORMALIZABLE_NOW` | `OI^{op}_{N_add}` 与 `OI^{pt}_w(K)` 已被明确提出，且 `OI^{op}_{N_add}(w)=0 iff w` 为 product form 被报告判为 `PROVABLE_NOW`。 | `deep_research_metric_identity_phaseii_report25_20260705.md:L124-L147,L171-L180`; `METRIC_IDENTITY_PHASEII_REPORT25_ADOPTION_NOTE_20260705.md:L85-L102` |
| two-chart gluing obstruction | `COMPLETE_LOCAL_DRAFT` | report27 已给 primitive two-chart overlap obstruction 的精确定义草案；其安全窄化版随后落地为 v1.5 GQ-FCR，但“广义 gluing obstruction”本身仍不宜宣称为更大理论。 | `deep_research_finite_glue_certificate_report27_20260705.md:L11-L73,L218-L248`; `FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L110-L158,L229-L244` |
| GQ-FCR | `CERTIFICATE_COMPLETE` | v1.5 formal note、exact script、JSON、Markdown 全部已经存在，15/15 exact checks 通过，且边界被收紧为 narrow finite exact note。 | `FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L55-L79,L81-L158,L160-L227`; `EXACT_GQ_FCR_V1_5_20260706.md:L31-L94`; `from_repo/STATE.md:L16-L28` |
| three-chart cocycle | `PACKAGE_SUPPORTED_DIRECTION` | external scan 将其标为 `NEXT_AFTER_TWO_CHART`，但明确说它更接近 Čech/contextuality 语言，需要更强 prior-art 定位。 | `EXTERNAL_MATH_OBJECT_SCAN_D706_20260706.md:L81-L92,L144-L173`; `deep_research_metric_identity_object_atlas_glue_report26_20260705.md:L68-L76` |
| support-rank ANOVA | `PACKAGE_SUPPORTED_DIRECTION` | external scan 将其标为 `PROMISING_LATER`，同时提醒 broad dependent-input ANOVA 空间已被占据。 | `EXTERNAL_MATH_OBJECT_SCAN_D706_20260706.md:L106-L118,L166-L173`; `BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:L17-L31,L65-L79` |
| Mode B empirical MaoField residual field | `FORBIDDEN` | 包内持续声明 Mode B 仍为 `insufficient_artifact`，并禁止“observed residual field / transport field / holonomy field / gluing field”式主张。 | `PACKAGE_README.md:L35-L41`; `from_repo/STATE.md:L26-L28`; `FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L258-L277` |

## 非同一性与统一性的有限形式化

我建议把当前包已经支持的定义层冻结为下面这一组有限对象。首先，**evaluation chart** 取为
\[
c=(P,T,J,R,D,w,A_g,N),
\]
其中 \(P\) 是 prompt distribution，\(T\) 是 task/benchmark axis，\(J\) 是 judge，\(R\) 是 rubric，\(D\) 是 decoding rule，\(w\) 是 weight table，\(A_g\) 是 aggregation chart，\(N\) 是 residualization / nuisance-stripping scheme；而被评系统的有限 roster 另行写成 \(\mathcal S=\{\sigma_1,\dots,\sigma_M\}\)，不再与 chart 混写。这个 chart-freeze 语法与 programme note 的 chart 元组，以及 report25 adoption 将 chart 与 roster 分离的建议是一致的。 （`from_repo/docs/infra/MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md:L665-L684`; `METRIC_IDENTITY_PHASEII_REPORT25_ADOPTION_NOTE_20260705.md:L54-L69`）

其次，对每个 chart \(c\)，定义一个**有限 carrier** \(I_c\)。包内没有把 \(I_c\) 固定成单一通用模板，但 adoption note 已经明确使用 `K_c(\sigma) in R^{I_c}` 的记法；exact certificates 又持续使用 manifest / row order / carrier labels 的写法。因此最安全的有限定义是：\(I_c\) 是 chart \(c\) 冻结后得到的有限 cell-index 集合，记录 raw audit table 的条目次序；在 exact certificate 场景中，它可以特化为有理向量空间 \(\mathbb Q^{I_c}\)，在一般定义层则先写成 \(\mathbb R^{I_c}\)。 （`METRIC_IDENTITY_PHASEII_REPORT25_ADOPTION_NOTE_20260705.md:L64-L69`; `deep_research_metric_identity_phaseii_report25_20260705.md:L217-L220`; `EXACT_GQ_FCR_V1_5_20260706.md:L39-L41`; `exact_gq_fcr_v1_5_20260706.json:L3-L21`）

在这个 carrier 上，定义**raw audit table**
\[
K_c(\sigma)\in \mathbb R^{I_c}
\]
为系统 \(\sigma\) 在 chart \(c\) 下、尚未经过最终 object map 的原始有限表。然后令
\[
\Phi_c:\mathbb R^{I_c}\to \mathcal O_c
\]
是 chart \(c\) 的对象化算子，输出可以是 score、residual、ranking-pre-summary 或其他 diagnostic。于是**chart-dependent metric object** 定义为
\[
M_c(\sigma)=(c,\Phi_c(K_c(\sigma))).
\]
这正把对象定义从“一个裸分数”改成了“chart-labeled processed object”；数字只是其中的表现层，而不是对象本体。 （`METRIC_IDENTITY_PHASEII_REPORT25_ADOPTION_NOTE_20260705.md:L64-L69`; `deep_research_metric_identity_phaseii_report25_20260705.md:L70-L72`; `MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md:L686-L690`）

接着，把“同一对象”定义成一个**transport 命题**，而不是默认本体。对两个 charts \(c,c'\)，声明原始表上的 transport
\[
U_{c\to c'}:\mathbb R^{I_c}\to\mathbb R^{I_{c'}}
\]
和对象空间上的 transport
\[
T_{c\to c'}:\mathcal O_c\to\mathcal O_{c'}.
\]
在一个声明好的 admissible class \(\mathcal K_{c,c'}\) 上，要求满足 **invariance / intertwining condition**
\[
T_{c\to c'}\circ \Phi_c
=
\Phi_{c'}\circ U_{c\to c'}.
\]
如果这条式子只在少数偶然样本上成立，或者只能通过先压缩成共同 summary 才“看起来可比”，那都还不够构成 identity。包内报告进一步要求：若要称为统一意义下的同一对象，至少还要有 object-side 的可逆性与 coherence，
\[
T_{c\to c}=\mathrm{id},\qquad
T_{c'\to c}=T_{c\to c'}^{-1},\qquad
T_{c'\to c''}\circ T_{c\to c'}=T_{c\to c''}.
\]
这就是当前 package 中“unity”的安全数学定义。 （`deep_research_metric_identity_phaseii_report25_20260705.md:L74-L99`; `MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md:L692-L704`; `METRIC_IDENTITY_PHASEII_REPORT25_ADOPTION_NOTE_20260705.md:L71-L77`）

在这个框架里，**defect certificate** 就可以精确写成有限 witness tuple
\[
\mathcal C=(c,c',K,\Delta),
\qquad
\Delta:=T_{c\to c'}M_c(K)-M_{c'}(U_{c\to c'}K),
\]
再附上 norm / order metadata、chart declaration、transport declaration、witness body 与 evidence boundary。若 \(\Delta\neq 0\)，则至少对这个 witness 而言，两边不能被当作同一对象。当前 package 的最小特例正是 same-carrier 情形：\(c,c'\) 只差残差化顺序，\(U=T=\mathrm{id}\)，而 defect 退化成
\[
\Delta=D_wK=R_{Q\to B}K-R_{B\to Q}K.
\]
当 \((I-P_{N_{\mathrm{add}}})K=0\) 但 \(D_wK\neq 0\) 时，包里已经有 exact certificate 证明 wrong-order residual-like output 不是 free residual object，而是 procedure artifact。 （`deep_research_metric_identity_phaseii_report25_20260705.md:L107-L123`; `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:L241-L283`; `EXACT_WITNESS_V1_4_20260629.md:L44-L66`）

用这组定义回译原始概念，其含义就很清楚了。**unity** 不是“所有 chart 终归测同一物”的先验形而上学断言，而是“在声明好的 \(U,T\) 与 coherence 下，两个 charted objects 可以合法识别为同一对象”的条件命题。**non-identity** 不是模糊的“有点不稳定”，而是 transport 失败、intertwining 失败、或 coherence 缺失所产生的 exact defect。**metric-form fetishism** 则是报告系统在没有证明 transports / invariances 的前提下，先把一族 charted objects \(\{M_c(\sigma)\}_{c,\sigma}\) 通过某个 quotient map \(q_c\) 压成一个 chart-free model property \(\theta(\sigma)\)；这正是把 heterogeneous measurement relation 非法地本体化为 intrinsic model property。 （`deep_research_metric_identity_phaseii_report25_20260705.md:L149-L165`; `MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md:L177-L212`; `MAOFIELD_METRIC_IDENTITY_PROGRAMME_ADOPTION_NOTE_20260704.md:L41-L73`）

## 下一步 exact object 的决策

**唯一选择：`KEEP_GQ_FCR_AS_SEPARATE_NOTE_AND_WRITE_INDEX`。** 这不是因为 GQ-FCR 比所有未来对象都“更深”，而是因为包内最新权威状态已经把 D706 的落地动作锁成：数学上保留 v1.5 GQ-FCR，出版上不把它并入当前 Zenodo V2.5 预印本，程序上冻结为独立相邻 exact note，并只做交叉索引，不继续在本轮扩张到 three-chart cocycle 或 support-rank ANOVA。这个动作与 `STATE.md` 的 current action、report29 的唯一裁定、以及 v1.5 formal note 的 “adjacency, not identity” 口径完全一致。 （`from_repo/STATE.md:L16-L28`; `deep_research_d706_gq_fcr_post_impl_preprint_integration_report29_20260706.md:L56-L78,L100-L100`; `FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L229-L277`）

### 精确对象定义

本次应被“保留并索引”的 exact finite object 不是笼统的 gluing rhetoric，而是 v1.5 已经实现的狭义对象
\[
\mathbf{GQ}_{12}
=
\bigl(I_1,I_2,O_{12},\rho_1,\rho_2,w_{12},\Gamma_{12},s_1,s_2,P_\Gamma,\Delta_{12}^2,\mathrm{checks}\bigr),
\]
其中
\[
\Delta_{12}^2(s_1,s_2;\Gamma_{12})
=
\|(I-P_\Gamma)(\rho_1 s_1-\rho_2 s_2)\|_w^2
=
\min_{\gamma\in\Gamma_{12}}\|\rho_1 s_1-\rho_2 s_2-\gamma\|_w^2.
\]
formal note 已把它定义为 finite weighted overlap mismatch 到 declared gauge 的 exact squared distance；exact certificate 又把 manifest、Gram matrix、projection matrix、controls 与 all_checks 全部写实。索引动作应当针对这个**已定型对象**，而不是再把它升格为更大的 gluing/cocycle/contextuality 理论。 （`FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L17-L79`; `EXACT_GQ_FCR_V1_5_20260706.md:L31-L61`; `exact_gq_fcr_v1_5_20260706.json:L1-L38,L148-L169`）

### no-go statement

本轮不应再寻求新的整合定理，而应明确写出一个 no-go statement：**当前 package 没有任何已授权定理允许把 v1.5 GQ-FCR 识别为 v1.3/v1.4 order-defect spine 的“同一主定理扩展”，也没有任何已授权动作允许立刻 patch 当前 Zenodo V2.5 预印本。** formal note 自己明确写的是 “adjacency, not identity”；report29 的唯一裁定也是“保留为 separate exact note，而不是 patch 现有 preprint”。因此这一步的目标不是统一理论，而是防止对象错配。 （`FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L229-L244`; `deep_research_d706_gq_fcr_post_impl_preprint_integration_report29_20260706.md:L28-L34,L56-L78`; `from_repo/STATE.md:L16-L28`）

### 证明义务

就数学本身而言，v1.5 的主要证明义务已经完成：一是 `\Delta_{12}^2=0 iff \rho_1 s_1-\rho_2 s_2\in\Gamma_{12}` 的核心 iff；二是 realized-gauge pasting 必须降为有额外 `G_i,\lambda_i` 数据时才成立的条件 corollary；三是 gauge monotonicity；四是 exact `2×2` 正负控制。这些都是 formal note 与 exact certificate 已经覆盖的内容。本轮剩余义务不再是“再多证明一个新大对象”，而是把索引边界写对，把“separate exact note”身份写清。 （`FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L81-L158,L160-L227`; `EXACT_GQ_FCR_V1_5_20260706.md:L43-L94`; `deep_research_d706_gq_fcr_post_impl_preprint_integration_report29_20260706.md:L68-L76`）

### 最小有理见证与控制设计

最小理性控制已经固定，不应在本轮改写。正控使用 uniform `2×2` overlap、additive gauge \(\Gamma=\mathrm{span}\{1,q,b\}\) 与
\[
m_+=(1,2,3/2,5/2)=(7/4)\,1+(1/4)\,q+(1/2)\,b,
\]
从而得到 \(\Delta^2=0\)。反控使用
\[
m_-=(1,-1,-1,1),
\]
它与 `1,q,b` 全部带权正交，因此 \(\Delta^2=1\)。单调性控制再取
\[
\Gamma'=\mathrm{span}\{1,q,b,m_-\},
\]
使反控在扩大的 gauge 下被吸收，得到 \(\Delta^2(m_-;\Gamma')=0\le 1=\Delta^2(m_-;\Gamma)\)。这些控制正是 node36 现在应当继续冻结、而不是再重设计的 exact witness 面。 （`FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L160-L219`; `EXACT_GQ_FCR_V1_5_20260706.md:L63-L87`; `from_repo/STATE.md:L26-L28`）

### 脚本与 JSON 要求

脚本与 JSON 也不应在本轮扩写成更宏大的 schema，而应保持当前 exact discipline：所有有理数由 `fractions.Fraction` 承载；JSON 用字符串保存 rationals；保留 carrier manifests、weights、gauge basis、Gram matrix、projection/complement projection、positive/negative controls、monotonicity check、checks、all_checks_passed 与 evidence boundary。换言之，本轮最需要的不是“更多字段”，而是**稳定字段语义与索引位置**。report29 甚至已经把唯一允许的非阻断代码修整改成字段语义层面的整理，而不是数学内容的扩张。 （`FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L70-L79,L221-L227`; `EXACT_GQ_FCR_V1_5_20260706.md:L39-L61`; `exact_gq_fcr_v1_5_20260706.json:L22-L38,L148-L169`; `deep_research_d706_gq_fcr_post_impl_preprint_integration_report29_20260706.md:L24-L24,L70-L76`）

### 负控制、风险与禁语

负控制方面，当前最重要的不是再加新花样，而是继续保留 `m_-` 以及 enlarged-gauge monotonicity 这两个 fail-closed 面，让读者无法把 obstruction 误读成绝对深层结构。风险方面，包内最新一致结论仍是 `duplicate risk = MEDIUM`：consistency radius、global-section obstruction、cellular sheaves、dependent-input ANOVA/Hoeffding、two-projection theory 都是近邻，因此任何 broad-framing 都会显著抬高越界/重复风险。相应地，禁语也应继续原封不动地锁住：不得说 broad sheaf / consistency-radius / contextuality / dependent-input ANOVA / noncommuting projection theory，不得说 MaoField empirical positive result，不得说 observed residual/transport/holonomy/gluing field，不得说 proof by JSON floats 或 deterministic harness。 （`deep_research_d706_gq_fcr_post_impl_preprint_integration_report29_20260706.md:L44-L54,L66-L98`; `FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L246-L277`; `PACKAGE_README.md:L30-L41`; `from_repo/STATE.md:L16-L28`）

## 严格 prior-art 与 duplicate-risk 复核

安全立场**维持不变：`duplicate risk = MEDIUM`。** 这不是因为包内已经找到 exact duplicate；相反，order-defect bibliography 对 v1.3/v1.4 的窄核给出的口径是：尚未识别 exact duplicate，但主要风险在于把狭义有限对象夸大进已经被占据的 broad theory。bibliography 直接要求把贡献压在有限正权二向表、product-weight iff main-effect orthogonality、order-independence iff product weights、existential non-product pure-main-effect witness、exact `2×2` rational certificate 这一窄层级，不得向 continuous measures、general dependent-input decompositions、completed formal system 或 MaoField empirical evidence 升级。 （`BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:L17-L31,L65-L79`）

对 v1.5 来说，风险只会更近，不会更远。external scan 明确把 Robinson 的 consistency radius、Abramsky–Brandenburger 的 global-section obstruction、Curry 的 finite sheaf/cosheaf framing、Hooker 与 Chastaing–Gamboa–Prieur 的 dependent-input decomposition、以及 Böttcher–Spitkovsky / Halmos 的 two-projection 邻域都列成边界设置器。scan 的结论不是“风险下降”，而是：当前安全着陆只能是 **gauge-quotiented residual-audit specialization**；一旦把表述推成 broad sheaf / consistency-radius / contextuality / dependent-input ANOVA / projection theory，风险立即上升。 （`EXTERNAL_MATH_OBJECT_SCAN_D706_20260706.md:L30-L43,L166-L173`; `deep_research_d706_gq_fcr_post_impl_preprint_integration_report29_20260706.md:L44-L54,L66-L66`）

同时，项目状态源与 programme adoption 也没有给出任何可合法下调风险的包内新证据。相反，`STATE.md` 明确写到 duplicate risk 仍是 `MEDIUM`；programme adoption note 也把 `MEDIUM` 当作继续有效的全局边界。因此，在当前证据包内，既不能把风险下调为 `LOW`，也没有足够依据上调成“已见 direct duplicate 的 `HIGH`”；最严格且最诚实的位置，仍然是 `MEDIUM`。 （`from_repo/STATE.md:L16-L28`; `MAOFIELD_METRIC_IDENTITY_PROGRAMME_ADOPTION_NOTE_20260704.md:L97-L110`）

## 给 node36 的最终指导

node36 现在最该做的不是再扩写理论名词，而是把已经落地的狭义数学对象守住边界：把“non-identity / unity”固定翻译成**chart-dependent metric object + declared transport/intertwining + coherence + exact defect certificate**，承认这套翻译是对的但仍然未完成；冻结 v1.5 GQ-FCR 为**独立 exact note**并只加交叉索引，不要 patch 现有 Zenodo V2.5 预印本，不要把它写成新 sheaf / consistency-radius / ANOVA / projection 理论，也不要复活任何 Mode B empirical positive rhetoric；若以后确实重新开启新的 exact math，一页短 note 级别最干净的首个新定理仍是 `OI^{op}_{N_add}(w)=0 iff w` 为 product form，但那是**索引冻结之后**的下一步，而不是这一步现在要抢着扩张的方向。 （`from_repo/STATE.md:L16-L28`; `METRIC_IDENTITY_PHASEII_REPORT25_ADOPTION_NOTE_20260705.md:L35-L50,L85-L102,L137-L146`; `deep_research_d706_gq_fcr_post_impl_preprint_integration_report29_20260706.md:L56-L78,L100-L100`）