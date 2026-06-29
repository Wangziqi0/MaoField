# Order-Defect 预印本占位稿严格审计报告

## 一页裁决

我在上传的压缩包中找到了你点名的全部主文件；就这组本地证据而言，当前 v1.3 order-defect 数学核心已经足以支撑一篇**短、窄、诚实**的占位型预印本，但还**不宜按现状直接对外贴出**。阻碍点不在 T1/T2/T3 的真伪，而在两个更像“学术合规”而不是“定理崩坏”的问题：一是 related-work 需要重写，尤其必须补上 Hooker 2007 与经典“两正交投影/乘积/交换子”文献；二是 harness 只能当作确定性回归工件，不能把 float-based JSON 当成精确分数证明。形式 note 本身已经正确地区分了代数直和与正交直和，也正确加上了 T2 的存在量词护栏，并把 T3 的非零输出限定为 sequential stripping artifact，而不是“真交互残差”。（证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 41-102、154-255、285-369行；`from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md` 11-45、72-133行；`from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_AUDIT_ADOPTION_NOTE_20260628.md` 27-30、53-85、144-161行）

```text
preprint_placeholder_requires_related_work_reframing
```

更具体地说，我没有在本地 formal note 中发现会推翻定理的数学错误。有限加权设定是干净的：`N_add` 被明说为一般情形下的**代数**直和，而不是先验正交直和；`P_N` 也没有被错误地在非乘积权情形下偷写成 `P_C+P_A+P_B0`。Prop. 1、Prop. 2、Prop. 3 的证明链条是闭合的，且主 `2 x 2` 见证的分数坐标与范数平方都能按 note 的定义精确重算出来。现有占位稿最需要修的，是把“这不是新 ANOVA 理论，而是一条有限加权诊断工件警告”的定位写得更硬、更窄、更有文献背景支撑。（证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 73-84、104-152、164-191、229-255、285-335行；`from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md` 40-45、72-96行）

从外部文献看，当前占位稿若只列 dependent-input Sobol/Shapley 文献而不补 Hooker 2007 与投影论背景，会让读者误以为作者在 claims novelty over the whole dependent-input decomposition area。Hooker 2007 已经明确讨论了**dependent variables 下的 weighted functional ANOVA diagnostics**，这与“有限加权诊断残差”的语境非常接近；Chastaing–Gamboa–Prieur 2012/2015、Owen–Prieur 2017、Iooss–Prieur 2019、Il Idrissi et al. 2025 则构成 dependent-input decomposition / sensitivity 的主干背景；而 Halmos 1969、Böttcher–Spitkovsky 2010、Corach–Maestripieri 2011 则是本 note 在“非交换正交投影”这一侧的应有背景。换言之，安全的新意只能表述为：**把一个经典的非交换投影现象专门化为有限双轴加权表中的可诊断 artifact，并给出最小有理见证与确定性回归 harness。** citeturn5search5turn10view6turn6search0turn6search1turn4view1turn7search1turn1search26turn12search1turn12search4turn4view5

预印本发布决定是：

**revisе first。**

不是“不要写”，也不是“数学推倒重来”，而是先完成三件事再贴：补齐 related work；把 harness 降格成“regression support, not proof”；再在正文或附录里补一个 exact symbolic check，用分数而不是十进制浮点来锁死主见证。这样处理后，它可以成为一篇学术上诚实的 4–6 页短 note；不这样处理，最容易出的问题不是算错，而是**被读成 overbroad novelty claim**。 （证据包：`from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md` 72-96、121-133行；`from_repo/scripts/debranded_residual_transport_harness_v1_3.py` 197-224、276-308、319-423行；`from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json` 30-58、120-205行）

## 审计总表

| 组件 | 结论 |
|---|---|
| finite_weighted_setup | PASS |
| projection_notation_and_subspaces | PASS |
| T1_product_weight_iff_orthogonality | PASS |
| T2_order_defect_iff_product | PASS |
| T3_nonproduct_pure_main_effect_artifact_no_go | PASS |
| exact_2x2_rational_witness | WARN |
| harness_script_summary_json_consistency | WARN |
| preprint_claim_boundary | PASS |
| related_work_and_duplicate_risk | WARN |
| future_object_roadmap | WARN |
| non_specialist_explanation | PASS |

这些结论的本地依据主要来自：formal note 对有限设定、投影记号、T1/T2/T3 和 `2 x 2` 见证的陈述与证明；script 对 block、阈值契约、central evaluator、JSON readback 的实现；preprint placeholder 对禁止 claims、related-work 边界和短 note 计划的现有写法。（证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 41-335行；`from_repo/scripts/debranded_residual_transport_harness_v1_3.py` 142-169、197-224、232-308、319-423、590-610行；`from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md` 30-37、52-92行；`from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json` 30-58、60-205行；`from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md` 72-133行）

## 数学审计

有限设定与投影记号这一层，我给 **PASS**。note 在一开始就把 `C`,`A`,`B0`,`N_add` 说清楚了，也明确写出了关键护栏：`N_add` 一般只是代数直和；`C` 永远与 `A`,`B0` 正交，但 `A` 与 `B0` 的正交性**恰恰就是后续要判定的内容**；因此一般情形下不能写 `P_N=P_C+P_A+P_B0`。这几点是你在 prompt 中特别要求检查的，而 local note 都处理对了。（证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 64-84行）

`P_C f = mu_f`、`P_A f = E_w[f|q]-mu_f`、`P_B0 f = E_w[f|b]-mu_f` 这组公式在一般正权有限情形下也是对的。原因很简单：`q`-only 子空间可以分解成常数加零均值 `q`-only，`b`-only 子空间同理；而条件均值正是到对应 axis-only 子空间的正交投影，再减去总均值就落到零均值主效应子空间。note 给出了公式本身，作为短 note 建议再补一行“为何这确为正交投影”的说明，但这属于 rigor polish，不属于错误修复。（证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 86-102行）

T1 我给 **PASS**。正向方向是标准分离：若 `w(q,b)=w_Q(q)w_B(b)`，则任意 `a in A` 与 `b in B0` 的加权内积因式分解，两个零均值因子相乘为零。反向方向使用 centered indicators
`a_q0(q)=1_{q=q0}-w_Q(q0)` 与 `b_b0(b)=1_{b=b0}-w_B(b0)`，展开后精确得到
`<a_q0,b_b0>_w = w(q0,b0)-w_Q(q0)w_B(b0)`；只要 `A ⟂ B0`，每个单元格的 product gap 都被迫为零，于是整张表是乘积权。note 还补上了单行/单列退化情形，这一点也正确。（证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 104-152行）

T2 也给 **PASS**。从代数上，
\[
D_w
=R_{Q\to B}-R_{B\to Q}
=(P_{B0}P_A-P_AP_{B0})(I-P_C),
\]
而因为 `P_A 1 = P_B0 1 = 0`，该交换子对常数子空间为零，所以在整个空间上等价地有
\[
D_w=P_{B0}P_A-P_AP_{B0}.
\]
这一步是合法的，不需要额外条件。更关键的是，note 没有犯量词错误：它明确写出“若 `D_w != 0`，结论只能是存在某个 witness input”，而不是“所有输入都不同”。这正是严谨版本应该有的保护栏。（证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 156-175、177-239行）

T2 的逆向证明也闭合：假设 `D_w=0`，取任意 `b in B0`，由 `P_B0 b=b` 得
\[
0=D_w b=P_{B0}P_A b-P_A b,
\]
故 `P_A b` 同时落在 `A` 与 `B0` 中；而 `A ∩ B0 = {0}`，所以 `P_A b=0`。再由投影自伴性，
\[
\langle a,b\rangle_w=\langle a,P_A b\rangle_w=0
\]
对所有 `a in A`, `b in B0` 成立，于是 `A ⟂ B0`，再由 T1 推回 product form。这个证明既短又够硬。（证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 206-227行）

T3 同样给 **PASS**。它的证明逻辑是：非乘积权时，`A` 与 `B0` 不正交，所以至少存在某个 `b in B0` 满足 `P_A b ≠ 0`；令 `K=b`，因为 `K ∈ N_add`，故真正的正交加性残差 `(I-P_N)K=0`。但当按 `Q` 再 `B` 的顺序剥离时，
\[
R_{Q\to B}K=-(I-P_{B0})P_AK,
\]
若这也为零，则 `P_AK` 会同时属于 `A` 和 `B0`，矛盾。因此一边顺序给零，另一边顺序给非零。这正是“错误顺序制造出来的 interaction-like artifact”，不是“真交互残差”。（证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 241-283行）

`2 x 2` 主见证的数学内容本身是对的。我按 note 的定义独立重算，主见证
\[
w=\frac1{11}\begin{pmatrix}1&2\\3&5\end{pmatrix},\qquad
K=\left(\frac7{11},-\frac4{11},\frac7{11},-\frac4{11}\right)\in B0
\]
确实满足
\[
(I-P_N)K=0,\qquad
R_{B\to Q}K=0,
\]
且
\[
R_{Q\to B}K=
\left(\frac1{32},\frac5{168},-\frac1{96},-\frac1{84}\right),
\qquad
\|R_{Q\to B}K\|_w^2=\frac{61}{177408}.
\]
optional 的对称 `A` 方向见证也已在本地文件中统一修正为
\[
K'=\left(\frac8{11},\frac8{11},-\frac3{11},-\frac3{11}\right),\qquad
R_{B\to Q}K'=\left(\frac1{42},-\frac1{84},\frac5{224},-\frac3{224}\right).
\]
因此，**数学上的 11 倍缩放 slip 已经在当前本地版本中修掉**。之所以把 `exact_2x2_rational_witness` 记为 **WARN** 而不是 PASS，不是因为分数错了，而是因为 script/summary/JSON 序列化时把这些有理数降成了浮点十进制近似。（证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 285-335行；`from_repo/scripts/debranded_residual_transport_harness_v1_3.py` 281-289行；`from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md` 77-92行；`from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json` 132-174行；`from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_AUDIT_ADOPTION_NOTE_20260628.md` 53-85行）

**Mathematical error list:** none found。

不过，作为严格短 note，我仍建议三条“收紧而非改错”的写法：第一，在 setup 末尾加一句说明 `P_A` 与 `P_B0` 投影公式为什么成立；第二，在 T2 里保留 `(I-P_C)` 版本再说明其与交换子全空间版本等价，避免读者误读为偷换；第三，在 T3 开头明确写一句“`K in B0 subset N_add`，因此 `(I-P_N)K=0`”。这些都属于论文工整度，而不是 theorem repair。（证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 77-102、164-175、263-279行）

## Harness 与脚本审计

我对 harness 的总体结论是：**它是合格的 deterministic regression harness，但不是精确证明工件。** 这就是为什么 `harness_script_summary_json_consistency` 给 **WARN**。正面部分很多：script 的 docstring 明说 synthetic-only；代码只包含 `argparse`、`hashlib`、`json`、`numpy` 等线性代数与 IO，没有 MaoField 数据读取、checkpoint loading、推理、训练、full-panel 执行或新 loss 逻辑；summary 和 JSON 也都反复把 strongest allowed verdict 限制在 `definitions_and_harness_viable_only`，并保留 `insufficient_artifact` 的 Mode B 状态。（证据包：`from_repo/scripts/debranded_residual_transport_harness_v1_3.py` 2-7、11-21、402-418、579-610行；`from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md` 5-22、30-37、94-119行；`from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json` 9-29、207-208行）

harness 的结构也确实符合你要求的 contract discipline。阈值由 `build_threshold_contract()` 集中定义；每个 block 的 pass/fail 只能由 `evaluate_test()` 分配；meta block 会核对 per-test thresholds 与 contract hash；主程序还执行了 JSON 写出后的 readback hash 校验。这一部分在脚本层和 JSON 层是一致的。（证据包：`from_repo/scripts/debranded_residual_transport_harness_v1_3.py` 197-224、319-389、392-423、590-610行；`from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json` 30-58、188-205行）

问题出在“support level”而不是“工程洁净度”。脚本的 witness、expected artifact、gap matrix、projection matrix 计算全部走的是 `float`、`lstsq`、`pinv` 和十进制 JSON 序列化路线；summary 也把“精确坐标”写成了小数，而不是分数。换句话说，它验证的是“在 `1e-12` 量级上数值一致”，而不是“exact rational identities are symbolically true”。这对于 regression control 足够，但对于一篇数学短 note，**不能把它当 proof**。（证据包：`from_repo/scripts/debranded_residual_transport_harness_v1_3.py` 72-112、281-288、295-306行；`from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md` 77-89行；`from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json` 140-174行）

还有一个更细的严格点：script 虽然存了 `expected_artifact_weighted_norm_squared = 61/177408`，但 evaluator 并**没有**把这个 exact squared norm 作为 pass/fail 条件之一；它只检查了向量无穷范数误差、零序残差小、真加性残差小，以及 artifact weighted norm 大于一个极小阈值。这意味着 harness 的主 block 对“分数范数平方”只做了**记录**，没有做“门控检验”。对当前占位稿而言这不致命，但作为 proof-support 还差一步。（证据包：`from_repo/scripts/debranded_residual_transport_harness_v1_3.py` 212-218、290-308、338-345行；`from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json` 152-181行）

**Harness/script/JSON error list with exact fixes:**

- 当前 harness 应明确按  
  ```text
  do_not_use_harness_as_proof
  ```  
  处理。它是 deterministic theorem-control regression，不是 exact proof artifact。（证据包：`from_repo/scripts/debranded_residual_transport_harness_v1_3.py` 307-308、416-418行）

- 必须新增  
  ```text
  symbolic_fraction_check
  ```  
  至少覆盖主 `2 x 2` 见证：精确验证 `P_A K`、`R_Q_then_B K`、`R_B_then_Q K`、`||R_Q_then_B K||_w^2` 以及对称 `A` 见证坐标。最简单做法是脚本附带一个 `fractions.Fraction` 或 SymPy 分支，只跑 `2 x 2`，零 GPU，零随机。

- 强烈建议新增  
  ```text
  exact_projection_matrix_dump
  ```  
  对 `2 x 2` case 输出 `P_C,P_A,P_B0,P_N,D_w` 的精确有理矩阵到附录 markdown。这样读者能直接看到 `D_w` 的非零结构，而不是只看到近似浮点坐标。

-  
  ```text
  additional_random_nonproduct_regression
  ```  
  **不需要**。当前数学对象是有限维精确 no-go；随机回归只能增加工程感，并不能增强证明力。

## 相关工作与重复工作风险

外部文献层面，我的结论是：

```text
no_exact_duplicate_found_but_close_prior_work
```

但这个结论必须连着一条学术安全说明一起读：**没有找到“与你当前对象完全同名同包”的标准定理或论文，不等于你可以宣称 broad novelty。** 原因是近邻文献非常多，而且有两条都离你很近。

第一条近邻是 dependent-input decomposition / diagnostics。Hooker 2007 已明确研究 **dependent variables 下的 generalized weighted functional ANOVA diagnostics**，这与当前占位稿的“finite weighted diagnostic residual”语境高度相关；Chastaing–Gamboa–Prieur 2012 建立 generalized Hoeffding-Sobol decomposition for dependent variables；其 2015 文又讨论数值方法；Owen–Prieur 2017 与 Iooss–Prieur 2019 则说明当输入相关时，传统 ANOVA/Sobol 解释会出现概念问题，Shapley effects 是一种替代解释；Il Idrissi 等 2025 则把 dependent-variable Hoeffding decomposition 又向前推进了一步。也就是说，**你的 note 绝不能写成“新 ANOVA 理论”或“首次 dependent-input decomposition”**。 citeturn5search5turn10view6turn6search0turn6search1turn4view1turn7search1turn7search10turn1search26

第二条近邻是经典正交投影理论。Halmos 1969 讨论 two subspaces；Böttcher–Spitkovsky 2010 是两投影理论的综述；Corach–Maestripieri 2011 研究 products `PQ` 与 `PQP`。你的 T2 本质上就是把一个经典的“两个正交投影不交换就会出现顺序/乘积差异”的现象，专门化到有限加权双轴主效应子空间上。因此，你也**不能**把 T2 包装成“发现了非交换投影现象本身”。真正可说的新意，只能是：把该现象写成一个**对有限加权经验管线有直接诊断意义**的 artifact statement，并给出最小 `2 x 2` 有理 witness 与明确 evidence boundary。 citeturn12search1turn12search4turn4view5turn3search11

所以，我对 duplicate-work 的窄问题回答是：在我检索到的这些确切论文里，**尚未看到一篇把以下四件事原封不动打包在一起**：非乘积 cell weights、以两个 centered main-effect orthogonal projections 做 ordered stripping、纯主效应导致 interaction-like residual 的最小有限 witness、以及一个 deterministic diagnostic harness。这个“打包后的 compact artifact note”看起来不是现成标准条目；但其每一块组成件都明显站在成熟先行文献之上，因此安全 framing 必须是：

> **not a new ANOVA theory; a compact diagnostic artifact note for finite weighted empirical pipelines**

这也是我主张当前分类用 `preprint_placeholder_requires_related_work_reframing`，而不是 `reject_as_duplicate_or_overclaim` 的原因。严格说，全球穷尽式检索我并没有完成，因此“绝对无重复”我不做担保；我只说：**在已核对的近邻文献中，未见 exact duplicate，但 close prior work 很强。** citeturn5search5turn6search0turn6search1turn4view1turn7search1turn1search26turn12search1turn12search4turn4view5

## 未来数学对象路线图

下面这份路线图是按**学术安全性优先**排的。我刻意把它收窄成“当前对象的近邻数学延伸”，而没有顺着更大的 transport / holonomy / gluing 叙事继续外推。

**精确符号闭包。** 定义草图：把当前 `2 x 2` order-defect note 的主 witness、对称 witness、投影矩阵、交换子矩阵全部写成 exact fractions。它能支持的 theorem/no-go 不是新 theorem，而是把现有 T1/T2/T3 的最小例子从“analytic proof + float regression”升级到“analytic proof + exact certificate”。重复风险很低；更接近 proof appendix，而不是独立方向。最小 zero-GPU harness 就是 `Fraction`/SymPy 单例检查。kill criterion 是：若 exact appendix 不能显著增强可信度，那它就不该独立成文。preprint suitability：**now，作为附录，不作为单独预印本。**

**任意 nuisance 子空间的交换子范数与见证提取。** 定义草图：固定有限维加权内积空间中的两个 nuisance 子空间 `U,V`，研究 `D=[P_V,P_U]` 的范数、秩、以及从 `D` 提取最小 witness 的方法。它可支持的 theorem 是“当交换子非零时，可构造 witness，使一类 ordered stripping 与正交 residual 分离”；这会把当前双轴主效应 object 推广为一般有限 nuisance-subspace 诊断命题。重复风险主要来自经典 two projections / products / commutator 文献，所以 novelty 必须限定在“finite diagnostic witness extraction”而不是“new projection theory”。最小 zero-GPU harness：小维度 exact rational matrices。kill criterion：若最终只重述了经典 commuting-projections 事实而没有提供新的 finite diagnostic corollary，就停。preprint suitability：**later**。 citeturn12search1turn12search4turn4view5

**多轴有限加权顺序缺陷。** 定义草图：把两轴 `A,B0` 推到三轴或多轴 `A_1,\dots,A_m`，研究 ordered stripping 链  
\[
(I-P_{A_m})\cdots(I-P_{A_1})(I-P_C)
\]
对排列次序的依赖。它能支持的 theorem/no-go 是“何时所有 axis main-effect subspaces pairwise commute / orthogonalize；何时存在排列导致纯低阶信号出现伪高阶 residual”。重复风险来自 dependent-variable decomposition 与 alternating projections 背景；如果写得太广，很容易撞上 generalized Hoeffding-type 文献或抽象投影链文献。最小 zero-GPU harness：`2×2×2` 或 `2×2×3` 的 exact rational examples。kill criterion：若结论只能用巨大枚举呈现、不能给出干净的 iff 或 no-go，就停。preprint suitability：**later**。 citeturn6search0turn1search26turn3search11

**source-fixed quotient residuals with nuisance registry。** 定义草图：不是泛泛谈 residual，而是对每个 residual 明确记录 ambient space、weight、nuisance registry、以及 residual operator 名字，比如  
\[
R=P_{N^\perp,w}K
\]
并把不同 residual 的可比性做成 registry discipline。它可支持的 theorem/no-go 是“不同 registry 下 residual 不能直接比较”或“某些 seemingly comparable residuals 其实 living in different quotient conventions”。重复风险与 Hooker 式 weighted diagnostic decomposition 有邻接，但我没有检到与这种“registry-first quotient residual discipline”完全对应的标准命名对象，因此这里的 prior-work 风险我标成 `not verified`。最小 zero-GPU harness：固定几个 registry，比较同一 `K` 在不同 registry 下的 exact outputs。kill criterion：若它不能提供清楚的 no-go statement，只剩术语管理，那就不值得单独成文。preprint suitability：**later**。 citeturn5search5turn10view6

**随机轴与随机子空间负对照。** 定义草图：不是拿随机性证明 theorem，而是把随机轴顺序、随机 nuisance basis、随机 but controlled nonproduct weights 当作 negative controls，测试某个 diagnostic 是否只在结构化 noncommutativity 下稳定触发。它可支持的是 methods no-go，而不是核心数学 theorem。重复风险目前我只能写 `not verified`，因为这更像工件设计，不像现成命名理论。最小 zero-GPU harness：小维度多次重复但固定 seed 的矩阵实验。kill criterion：若它不能分辨“结构性 order defect”与“数值偶然性”，就停。preprint suitability：**later，最好做 supplemental note，不做主线首发。**

**不建议现在推进的对象。** `scale-lattice residual transport with edge defect and square-holonomy telescoping`、以及“gluing / local-to-global obstruction”在当前证据边界下都**不值得现在写**。原因不在于它们必假，而在于它们离当前被严格证明的对象太远，且极易被读成在借用 sheaf obstruction 或更大几何语言做 overclaim。重复风险我这里也只能写 `not verified`，因为一旦跨进那条叙事线，相关背景会迅速扩张，已经超出本次严格 order-defect 预印本审计的安全范围。preprint suitability：**not worth it now**。

## 短 note 起草方案与精确措辞

如果要把它压成 4–6 页，我建议结构非常朴素，甚至刻意“像一则数学警告说明书”，不要像 program manifesto。

**建议章节标题：**

- *Introduction and claim boundary*  
- *Finite weighted setup*  
- *Product weights and main-effect orthogonality*  
- *Ordered stripping and the commutator criterion*  
- *An exact `2 x 2` witness*  
- *Related work and scope of the claim*  

这样写的好处是，正文从头到尾只服务一个对象：**finite weighted order defect**。harness 只占半页，放在最后当 deterministic regression appendix summary 即可，不要让它在正文里喧宾夺主。（证据包：`from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md` 121-133行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 337-369行）

**建议保留的原句或原意：**

- “The nonzero wrong-order output is a sequential stripping artifact, not a true interaction residual.” 这句是整篇文章最重要的学术安全阀，必须保留。（证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 254-255行）
- “It does not introduce a new theory of functional ANOVA, Sobol indices, Shapley effects, or dependent-input decompositions.” 这句也应该保留，但要放在**补齐 related work 之后**，否则像单方面免责声明，不像有文献自觉的定位。（证据包：`from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md` 40-45行）
- “If `D_w != 0`, the correct conclusion is existential.” 这句最好以 remark 形式保留在 T2 后面，因为它直接防止过度推广。（证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 229-239行）

**建议删除或替换的措辞：**

- 把 “finite two-axis weighted diagnostic field” 换成更标准的 “finite two-way weighted array model” 或 “finite weighted two-way table”。“diagnostic field” 对 bundle 内部语境也许顺手，但对外不够标准，容易显得项目内行话。（证据包：`from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md` 13-16行）
- 不要在摘要里让 harness 与 theorem 并列得像“双证据通道”。当前 harness 的正确地位是 regression support，不是证明的一半。（证据包：`from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md` 40-45、67-70行；`from_repo/scripts/debranded_residual_transport_harness_v1_3.py` 281-308行）
- 删除当前 related-work 段落里“只列 sensitivity analysis 文献”的不完整状态；必须把 Hooker 2007 与两投影背景并入，否则读者会误判新意边界。 citeturn5search5turn10view6turn12search1turn12search4turn4view5

**建议新增的精确措辞：**

可以在摘要末尾加入这一句：

> *This note isolates a finite weighted projection-order artifact in a two-way table; it is not proposed as a new dependent-input ANOVA theory.*

这句话能同时压住“新理论”误读与“项目宣言化”风险。其学术位置也与 Hooker 2007、Chastaing et al. 2012、以及两投影理论背景更一致。 citeturn5search5turn6search0turn12search4turn4view5

在 related-work 段开头加入这一句：

> *Close antecedents include weighted or generalized ANOVA-type decompositions for dependent variables and the classical theory of noncommuting orthogonal projections.*

这句话能把两侧背景一次性摆平。 citeturn5search5turn6search0turn1search26turn12search1turn12search4turn4view5

在 harness 说明里加入这一句：

> *The accompanying harness is included only as deterministic regression support for the displayed finite examples; the mathematical claims are established analytically.*

这句会显著降低“把 JSON 当 theorem proof”的风险。（证据包：`from_repo/scripts/debranded_residual_transport_harness_v1_3.py` 392-418行；`from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md` 94-100行）

**Preprint posting decision：**

**revise first。**  
具体就是：先补 related work，删项目内行话，再补 exact symbolic appendix；完成这三步后，可以发布一个窄而诚实的占位稿。现在直接发，不至于数学失真，但很容易在 scholarly framing 上吃亏。（证据包：`from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md` 72-133行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 360-369行）

## 给非专业读者的短解释

把它想成一个只有四个格子的表格。行代表一种分类，列代表另一种分类。你有一张数值表，想把它分成三部分：整体平均、行的主效应、列的主效应，剩下的才叫“交互残差”。

如果每个格子的权重刚好等于“该行权重 × 该列权重”，那么先减行效应再减列效应，和先减列效应再减行效应，结果会一样。可是一旦格子的权重不是这种乘法结构，两种“先减谁后减谁”的做法就可能不一样。这样一来，哪怕原来的信号明明只是一个纯主效应，错误的顺序也可能造出一块看起来像“交互”的剩余图案。当前 note 证明的，就是这种“假交互”确实会发生，而且最小 `2 x 2` 的有理数例子就能发生。（证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 108-152、156-191、241-255、285-335行）

用 bundle 里的主见证说，就是这张加权表
\[
\frac1{11}\begin{pmatrix}1&2\\3&5\end{pmatrix}
\]
不是“行权重 × 列权重”的形式，所以顺序开始变重要。对某个纯列主效应信号 `K`，真正的加性残差其实是零；但按一个顺序剥离时，最后却会剩下一小块非零向量。这并不表示系统里真的有新的交互结构，而只表示：**你的剥离顺序把一个纯主效应加工成了看起来像交互的东西。** 这就是整篇 note 想提醒非专业读者的一句话版本。（证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 245-255、309-335行；`from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md` 13-16、34-45行）