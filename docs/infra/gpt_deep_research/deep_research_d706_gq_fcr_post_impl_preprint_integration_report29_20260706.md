# D706 GQ-FCR 实现后审计与预印本整合闸门报告

## 审计范围与证据边界

本次审计严格以附件包中的指定材料为主证据，并只把能直接核验的官方 arXiv / 出版社页面作为外部先行文献依据。包内说明已经把本轮对象限定为：node36 已实现的 v1.5 `Gauge-Quotiented Finite Consistency Radius` 精确有理证书；该包明确不是论文授权、不是同行评审、不是 MaoField 经验正结果，也不是用 JSON 浮点或 deterministic harness 代替数学证明的场合。（附件包：`PACKAGE_README.md:L5-L17`；`from_repo/STATE.md:L16-L28`）

我按题面顺序核读了核心材料，重点交叉了四组证据：其一是 formal note、exact script、JSON/Markdown 证书之间是否一致；其二是 Report28 与 adoption note 是否已经把语义边界收紧为“声明式 overlap gauge quotient 的有限证书”；其三是 V2.5 预印本当前主定理与 v1.5 GQ-FCR 是否属同一对象；其四是包内旧经验材料是否仍被当作权威。综合这些文件，当前包内自洽地把 v1.5 定位为一个**狭义、有限、精确、与 v1.3/v1.4 相邻而非同一**的新对象，并维持 `Mode B = insufficient_artifact` 与 `duplicate risk = MEDIUM`。（附件包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L11-L16,L229-L244,L246-L277`；`from_repo/docs/infra/gpt_deep_research/deep_research_d706_gq_fcr_implementation_gate_report28_20260706.md:L183-L223`；`from_repo/docs/infra/gpt_deep_research/D706_GQ_FCR_IMPLEMENTATION_GATE_REPORT28_ADOPTION_NOTE_20260706.md:L24-L50`；`from_repo/docs/infra/recovery/D706_GQ_FCR_NEXT_PRO_RAG_STATUS_GREP_SYNTHESIS_20260706.md:L139-L189`）

就外部文献边界而言，相关邻域已经相当成熟：Robinson 的 sheaf-assignment 文献明确使用 “consistency radius” 描述重叠局部截面的相容程度，并把正的 consistency radius 解释为 global section 的障碍；Abramsky–Brandenburger 直接把 contextuality/non-locality 与 global sections 的不存在对应起来；Curry 的 thesis 则把 cellular sheaves 描写为由 cell complex 参数化的有限向量空间与映射家族。换句话说，凡是把本对象说成“新 consistency-radius 理论”“新 sheaf/global-section 理论”“新 contextuality obstruction”的说法，都会明显越界。citeturn3view1turn4view3turn4view1turn4view2

## 实现正确性裁定

从定义层面看，v1.5 formal note 给出的数据是完备且收缩过的：有限集合 `I_1, I_2, O_12`，有理线性 restriction maps `rho_i : H_i -> V_12`，逐点严格正的重叠权重，以及一个声明的 overlap gauge 子空间 `Gamma_12`。在这个数据上，原始 mismatch `m_12(s_1,s_2)=rho_1 s_1-rho_2 s_2` 与带权内积都定义清楚，而“权重严格正”足以保证有限维带权 Hilbert 空间的正定性。这一层定义没有数学缺口。（附件包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L17-L53`）

投影公式也用对了。formal note 明写
`P_Gamma = G (G^T W G)^(-1) G^T W`，script 中 `projection_matrix` 的循环实现恰好对应这个矩阵式；它不是用“先验正交”偷换计算，而是真正通过 Gram 矩阵与其逆来构造投影。随后脚本又对 `P^2=P` 与 `W P = P^T W` 做了 exact check，JSON 证书中这些检查均为 `true`，因此“带权正交投影”这一核心算子在本证书里是落实到位的。（附件包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L70-L79`；`from_repo/scripts/debranded_residual_transport_exact_gq_fcr_v1_5.py:L87-L101,L187-L203`；`from_repo/docs/infra/debranded_residual_transport/exact_gq_fcr_v1_5_20260706.json:L22-L38,L317-L409`）

`Delta^2=0 iff m in Gamma` 的证明，当前也被安全地限定在“声明式 gauge quotient compatibility”层面，而没有越级宣称“真实局部 gauge 调整后必可 paste”。formal note 先给出核心 iff，再单独把“realized-gauge pasting”放到有额外 `G_1,G_2,lambda_1,lambda_2` 数据时才成立的条件性 corollary；adoption note 也把这点列为已采纳要求。这是本轮最关键的语义修补，而且已经正确落实。（附件包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L81-L139`；`from_repo/docs/infra/gpt_deep_research/D706_GQ_FCR_IMPLEMENTATION_GATE_REPORT28_ADOPTION_NOTE_20260706.md:L27-L37`）

gauge monotonicity 的表述也是正确的：把最小化集合从 `Gamma_12` 扩大到 `Gamma'_12`，最小值不可能变大。formal note 以“更大声明 gauge 下 obstruction 可能被吸收”为严格含义；脚本则用 `Gamma' = span{one,q,b,checkerboard}` 做了精确 witness，JSON 记录 `Delta^2(m_minus;Gamma)=1`、`Delta^2(m_minus;Gamma')=0`。这与“障碍是相对于所声明的 gauge 而言”的 fail-closed 纪律完全一致。（附件包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L140-L158,L213-L219`；`from_repo/scripts/debranded_residual_transport_exact_gq_fcr_v1_5.py:L168-L203`；`from_repo/docs/infra/debranded_residual_transport/exact_gq_fcr_v1_5_20260706.json:L66-L147`）

`2×2` 控制算术也过关。formal note 选取统一权重 `w=(1/4,1/4,1/4,1/4)` 与 additive gauge basis `one,q,b`；JSON 给出的 Gram 矩阵与其逆均为单位阵，说明在该权重下这三条基向量正交归一。对应地，正控 `m_plus=(1,2,3/2,5/2)` 的 gauge 系数精确为 `7/4,1/4,1/2`，残差为零，`Delta^2=0`；反控 `m_minus=(1,-1,-1,1)` 与三条 gauge basis 的带权内积全为零，残差等于自身，`Delta^2=1`。这些值在 formal note、script、JSON 三处一致，并且包内 `STATE.md` 也记录了 `15/15` exact Fraction checks 通过。（附件包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L160-L219`；`from_repo/scripts/debranded_residual_transport_exact_gq_fcr_v1_5.py:L155-L203`；`from_repo/docs/infra/debranded_residual_transport/exact_gq_fcr_v1_5_20260706.json:L22-L38,L225-L316`；`from_repo/STATE.md:L16-L28`）

我给出的数学正确性裁定是：**通过，但附带一个不阻断的实现备注**。`build_control()` 里 `gauge_coefficients_for_basis` 的计算方式是 `⟨m,g_i⟩_w / ||g_i||_w^2`，这在当前 `one,q,b` 正交归一的最小控制中是正确系数；但若未来有人把该字段机械复用于**非正交** gauge basis，它就不再等于一般意义上的坐标展开系数。好在本证书真正承载证明力的对象不是这个字段，而是通过 Gram 逆构造的投影矩阵及其 exact checks，因此这只是一个**字段语义/未来泛化**问题，不影响当前 v1.5 通过。（附件包：`from_repo/scripts/debranded_residual_transport_exact_gq_fcr_v1_5.py:L136-L152,L187-L203`）

## 预印本整合裁定

V2.5 预印本的主对象非常明确：它证明的是**有限正权二维表上的 projection order defect**，即 product weights、`A ⟂ B_0`、两种 sequential stripping map 的次序无关性之间的等价，并给出一个 exact `2×2` 非 product 见证，其平方范数是 `61/177408`。预印本还把 MaoField 部分明确放在“programmatic only / future work / no empirical result”的边界之下。也就是说，V2.5 的主脊柱仍然是 **same-carrier order-defect theorem**，而不是 overlap-gauge quotient 证书。（附件包：`from_repo/docs/infra/debranded_residual_transport/MAOFIELD_PREPRINT_V2_5_FINAL_SYNTHESIS_20260703.tex:L35-L39,L177-L231,L281-L298`；`from_repo/docs/infra/recovery/V2_5_FINAL_SYNTHESIS_COMPARISON_AND_ADOPTION_20260703.md:L50-L75`）

与之相比，v1.5 formal note 已经明说：它研究的是**两个局部 sections 在 overlap 上、模掉一个声明式 gauge 子空间之后的 mismatch 距离**；它与 v1.3/v1.4 的关系是 “adjacency, not identity”。这意味着如果现在把 GQ-FCR 塞回现有 Zenodo 预印本正文，安全边界就会立刻变差，因为你必须同时改 abstract、对象说明、future mathematical objects、related work 和 duplicate-risk positioning，且很容易把“相邻对象”误写成“统一理论延伸”。（附件包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L229-L244`；`from_repo/docs/infra/recovery/D706_GQ_FCR_NEXT_PRO_RAG_STATUS_GREP_SYNTHESIS_20260706.md:L141-L189`）

所以我的出版边界裁定不是“立即 patch 现有 Open-MaoField 预印本”，而是：**把 GQ-FCR 维持为独立 exact note，并把现有 V2.5 / Zenodo preprint 先保持不动**。这个结论与 Report28 的原始方向一致：v1.5 是本轮可落地的新对象，但 three-chart cocycle 与 support-rank ANOVA 在此时都不是更安全的直接下一步。（附件包：`from_repo/docs/infra/gpt_deep_research/deep_research_d706_gq_fcr_implementation_gate_report28_20260706.md:L213-L223`）

如果要做整合，唯一安全的整合方式也不应是**现在**改 Zenodo PDF，而应是**之后**在一个新版本号下，添加一句非常克制的邻接说明，而不是把 GQ-FCR 纳入现有主定理链条。我不建议当前就去修订已经形成 publication record 的 `10.5281/zenodo.21190475`；包内自己的 Zenodo 记录文件也把它描述为 `Publication -> Preprint` 记录，而非同行评审结果。（附件包：`from_repo/docs/infra/OPEN_MAOFIELD_FORMAL_ZENODO_PREPRINT_PUBLISHED_20260704.md:L11-L25,L48-L52,L115-L145`）

## 旧经验材料的处置

旧经验稿 `paper_v8_final_20260516.md` 的价值，仅在于说明 MaoField 原先的企图是什么：它关心 LLM 自迭代/塌缩、黑箱评测、KL/Wasserstein 异常、以及一种想把经验历史和数学骨架连起来的雄心。就文本自身而言，它确实是一份“empirical pilot study”式的旧稿，而不是当前数学对象的权威来源。（附件包：`from_repo/experiments/exp018_cat/literature/paper_v8_final_20260516.md:L64-L77`）

但包内当前权威状态已经明确把这份旧稿降级了：D706 synthesis 直说它“historical context only”，并要求它不得覆盖后来的 negative-centered 收口与 `Mode B = insufficient_artifact`；`STATE.md` 也把主线描述为从原 empirical pilot 转向 debranded finite order-defect / residual-audit 数学对象。（附件包：`from_repo/docs/infra/recovery/D706_GQ_FCR_NEXT_PRO_RAG_STATUS_GREP_SYNTHESIS_20260706.md:L126-L177`；`from_repo/STATE.md:L22-L28`）

因此，我的建议是：**未来正文中，旧经验材料只允许以“deflated motivation”出现；如果一定要保留更多背景，最多放在 historical appendix，而不应成为新 preprint 的结果支撑、卖点段落或理论合法性来源。** 它当然也可以被写成一个 negative-centered measurement-audit case，但那种写法比“一句 deflated motivation + 附录收纳”更容易把旧的经验雄心重新带回主文，所以我不推荐把它放进当前主叙述中心。（附件包：`from_repo/docs/infra/recovery/D706_GQ_FCR_NEXT_PRO_RAG_STATUS_GREP_SYNTHESIS_20260706.md:L126-L177`；`from_repo/docs/infra/debranded_residual_transport/MAOFIELD_PREPRINT_V2_5_FINAL_SYNTHESIS_20260703.tex:L233-L279,L289-L298`）

## 先行文献与重复风险

就“consistency radius / sheaf assignment / global-section obstruction”这条线而言，先行文献已经非常近。Robinson 的论文不只用了 `consistency radius` 这一术语，而且把它定义为衡量 assignment 在重叠局部截面上一致性的量，并明确说“正的 consistency radius 是 assignment 不是 global section 的障碍”；Abramsky–Brandenburger 则把 contextuality/non-locality 精确对应为 global sections 不存在的障碍。由此看，v1.5 若被表述成“新的 consistency radius 理论”或“新的 global-section obstruction 理论”，重复/越界风险会立刻升高。citeturn3view1turn4view3

就 cellular sheaf 这条线，Curry 明确把它描述为“由 cell complex 参数化的有限向量空间与映射家族”，而且 thesis 中已经触及 sheaf cohomology、global sections 与 pseudo-metric/interleaving 等更广结构。这说明 v1.5 与这些成熟框架只是**局部切片上的线性代数邻接**，并不足以支撑“进入广义 sheaf/cellular-sheaf 理论”的新颖性叙述。citeturn4view1turn4view2

就 dependent-input decomposition 而言，Hooker 早就讨论了 dependent variables 下的 generalized functional ANOVA；Chastaing–Gamboa–Prieur 给出了 dependent variables 的 generalized Hoeffding-Sobol decomposition；Owen–Prieur 又明确指出，当输入依赖时，基于 ANOVA 的量会遇到概念与计算问题，而 Shapley value 可以作为替代。由此看，把 v1.5 的 additive gauge 说成“新的 dependent-input ANOVA / Sobol / Shapley 理论”是站不住的。citeturn1search3turn2search0turn3view5

就投影理论而言，Böttcher–Spitkovsky 的综述直接把 two projections / two subspaces 作为一个成熟领域来处理，并点名 Halmos 的经典结果。于是，无论 v1.3/v1.4 还是 v1.5，都不能被写成“两投影理论的新总论”；最多只能说，v1.5 把“先声明 nuisance，再看 surviving mismatch”的操作纪律搬到了 two-chart overlap setting 里。citeturn3view7

综合这些先行文献，我的重复风险裁定是：**当前仍应维持至少 `MEDIUM`，而且一旦把叙述向 broad sheaf / consistency-radius / contextuality / dependent-ANOVA / two-projection theory 推开，风险会从中等迅速抬升。** 真正还可能保留的一点“新意”，不是一般理论，而只是一个**受限的、精确有理的、两图 overlap-gauge quotient 证书包**：它把有限线性代数、exact rational controls、严格 claim boundary、以及与 v1.3/v1.4 的程序性邻接捆成一个可复核对象。换言之，它最多是**有限示例化与包式整合上的狭义新对象**，不是抽象层面的新理论。 （附件包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L11-L16,L229-L277`；`from_repo/STATE.md:L16-L28`）citeturn3view1turn4view1turn4view3turn1search3turn2search0turn3view5turn3view7

## 最终裁定与 node36 动作

**最终唯一裁定：**
`APPEND_GQ_FCR_AS_SEPARATE_EXACT_NOTE`
这个裁定的含义是：**数学上允许保留 v1.5 GQ-FCR；出版上不把它并入当前 Zenodo V2.5 预印本正文；程序上把它维持为一个边界收紧的相邻 exact note。**（附件包：`from_repo/docs/infra/recovery/D706_GQ_FCR_NEXT_PRO_RAG_STATUS_GREP_SYNTHESIS_20260706.md:L179-L191`；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L229-L277`）

数学正确性裁定是：**通过，且我认为当前 formal note 的 theorem/corollary 分裂是正确的。** 唯一需要警惕的是脚本里 `gauge_coefficients_for_basis` 的字段语义，不应在未来非正交 basis 场景下被误解成一般坐标系数；但这不影响当前证书的成立，因为真正承担证明力的是投影矩阵、残差向量与 15 项 exact checks。（附件包：`from_repo/scripts/debranded_residual_transport_exact_gq_fcr_v1_5.py:L136-L152,L187-L203`；`from_repo/docs/infra/debranded_residual_transport/exact_gq_fcr_v1_5_20260706.json:L22-L38`）

出版边界裁定是：**当前 Zenodo 预印本不应立刻改版。** 现有 V2.5 要保持其“finite projection order defect + exact witness + programmatic future work”的结构完整性；GQ-FCR 现在只是相邻对象，不是对该主定理的自然补丁。关于“现有 Zenodo preprint 应该现在、以后、还是不碰”：我的答案是**以后再说，但不是现在**；也就是只有在未来确实要发行一个新版本时，才允许加入一句非常克制的“adjacent exact note”说明。（附件包：`from_repo/docs/infra/debranded_residual_transport/MAOFIELD_PREPRINT_V2_5_FINAL_SYNTHESIS_20260703.tex:L177-L298`；`from_repo/docs/infra/OPEN_MAOFIELD_FORMAL_ZENODO_PREPRINT_PUBLISHED_20260704.md:L11-L25,L115-L145`）

重复风险裁定是：**维持 `MEDIUM`，并且所有 broad-framing 尝试都不安全。** 之所以这样判断，不是因为 v1.5 一无可取，而是因为相关邻域——consistency radius、global-section obstruction、cellular sheaves、dependent-input decomposition、two projections——都有强而近的先行文献，v1.5 最安全的定位只能是 narrow finite certificate。citeturn3view1turn4view1turn4view3turn1search3turn2search0turn3view5turn3view7

我建议 node36 的精确动作只有以下几步，不扩展、不换题：

- **冻结现有四件 v1.5 工件为独立 exact note 套件**：`FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md`、`debranded_residual_transport_exact_gq_fcr_v1_5.py`、`exact_gq_fcr_v1_5_20260706.json`、`EXACT_GQ_FCR_V1_5_20260706.md`；不要把它们并入当前 Zenodo V2.5 预印本文本。 （附件包：`from_repo/docs/infra/gpt_deep_research/D706_GQ_FCR_IMPLEMENTATION_GATE_REPORT28_ADOPTION_NOTE_20260706.md:L52-L64`）

- **只在非论文型文档中增加一条交叉索引，而不是修改预印本正文**。最安全的落点是仓库说明或 source-map 类型文件，而不是 `MAOFIELD_PREPRINT_V2_5_FINAL_SYNTHESIS_20260703.tex` / PDF。安全一句话可以直接复用 formal note 的授权上限：
  `A separate exact note records the v1.5 Gauge-Quotiented Finite Consistency Radius as an adjacent finite certificate; it does not alter the theorem or claims of the V2.5 order-defect preprint.`
  这句话的数学内容和边界都已被包内 formal note 支持。 （附件包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L248-L277`）

- **补一个非阻断的代码语义修整**：把 `gauge_coefficients_for_basis` 改成真正通过 Gram 逆求得的 basis coordinates，或者把字段重命名为不易误解的名字；这一步只为防未来误用，不影响当前证书通过。 （附件包：`from_repo/scripts/debranded_residual_transport_exact_gq_fcr_v1_5.py:L136-L152`）

- **本轮不要继续推进 three-chart cocycle，也不要转支到 support-rank ANOVA defect。** three-chart 更接近 Čech / contextuality 语言，先行文献碰撞更近；而且当前最安全的 publication action 不是再长一个对象，而是先把 v1.5 的边界位置固定下来。 （附件包：`from_repo/docs/infra/gpt_deep_research/deep_research_d706_gq_fcr_implementation_gate_report28_20260706.md:L217-L223`）

精确 forbidden wording list 如下；这些短语或近义表达，在当前轮次都不应进入任何外发说明、摘要、标题、结论句或版本说明：

```text
new consistency-radius theory
new sheaf theory / new cellular-sheaf theory
new contextuality obstruction / global-section theorem
new dependent-input ANOVA / Hoeffding-Sobol / Shapley theory
new two-projection / noncommuting-projection theory
MaoField empirical positive result
full panel has run
checkpoint inference / model inference / training / new loss authorized
observed residual field / transport field / holonomy field / gluing field
glass box broken
peer-reviewed / journal published / journal submitted / arXiv submitted
proof by JSON floats
proof by deterministic harness
```

这份 forbidden list 不是额外加码，而是 formal note、adoption note 和 Zenodo publication note 里现成边界的更可执行翻译。（附件包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L258-L277`；`from_repo/docs/infra/gpt_deep_research/D706_GQ_FCR_IMPLEMENTATION_GATE_REPORT28_ADOPTION_NOTE_20260706.md:L39-L50`；`from_repo/docs/infra/OPEN_MAOFIELD_FORMAL_ZENODO_PREPRINT_PUBLISHED_20260704.md:L115-L150`）

最后，用一句话收束本轮：**v1.5 GQ-FCR 作为一个有限 exact mathematical certificate 是成立的；作为当前 Open-MaoField Zenodo 预印本的即时修补，则并不安全。最稳妥的下一步不是扩张，而是把它固定为独立 exact note。**（附件包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_5_GAUGE_QUOTIENTED_CONSISTENCY_RADIUS_20260706.md:L248-L277`；`from_repo/docs/infra/debranded_residual_transport/MAOFIELD_PREPRINT_V2_5_FINAL_SYNTHESIS_20260703.tex:L281-L298`）