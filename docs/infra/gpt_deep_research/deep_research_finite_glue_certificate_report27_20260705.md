# 有限粘合障碍证书严格评估

## 结论与证据边界

本包已经足以**严格地定义并落地一个最小 exact rational 的两图粘合障碍证书**，但最安全的首个对象不应被包装成广义 sheaf、广义 holonomy、广义 ANOVA，甚至也不应先追求“富含语义的 chart 大一统定义”。更稳妥的做法，是先把对象压缩成一个**有限、加权、可精确重算的 overlap obstruction certificate**：它只比较两个局部 section 在 overlap 上、经声明好的 gauge 类吸收之后，是否仍有不可消掉的剩余失配。这个方向与包内已接受的决策完全一致：`Report26` 与 adoption note 都把当前分支锁定为 `FINITE_GLUE_OBJECT_FIRST`，并把目标表述为“两局部 chart + overlap + local residual sections + restriction maps + allowed local gauge + gauge-minimized mismatch”；同时明确说明旧 transport / holonomy / gluing harness 只是历史脚手架或回归支持，而**不是**当前风格的 exact rational gluing certificate。 [来源：PACKAGE_README.md:13-20；from_repo/STATE.md:24-28；from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_object_atlas_glue_report26_20260705.md:64-76,106-108,138-146；from_repo/docs/infra/gpt_deep_research/METRIC_IDENTITY_OBJECT_ATLAS_GLUE_REPORT26_ADOPTION_NOTE_20260705.md:40-49,61-85,96-101；from_repo/docs/infra/recovery/MAOFIELD_D705_FINITE_GLUE_OBJECT_TASKBOOK_20260705.md:14-26,43-61]

我给出的严格判断是：**可以现在就设计**，而且不需要再先停回 `PATCH_DEFINITIONS_BEFORE_GLUE`。但需要把“最小对象”设计成一个**比较侧优先**的证书，而不是一上来就绑定某个宏大“全局 K 的统一生成理论”。原因很直接：包内已经有成熟的有限加权投影语言、真残差与 procedure artifact 的区分、exact rational 证书风格，以及旧 gluing absorption guard 的公式原型；这些足以支持一个新的 bounded object，却还不足以授权更大的总体理论。 [来源：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:41-80,156-191,243-255,337-369；from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md:30-66；from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py:78-95,126-220；from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_20260625.md:344-367]

因此，我的最终取向不是“旧 MaoField 正结果辩护”，也不是“论文草稿写作”，而是：**把当前材料压成一个新的有限线性代数对象**。这个对象的最安全原型是“**two-chart overlap certificate**”，其 primitive 版本以局部 sections 为基本输入；若 node36 之后想加一个由公共源向量 `K` 生成的 subtype，可以在同一 schema 下向上兼容，而不需要重写核心定义。这个判断也符合 programme note 对 chart、transport、defect、certificate library 的骨架建议。 [来源：from_repo/docs/infra/MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md:665-718,782-810；from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_object_atlas_glue_report26_20260705.md:82-94,108-108,146-146]

## 精确有限定义

### 最小对象的选择

我建议把首个 rigorously safe 的对象定义成：

```text
primitive two-chart overlap obstruction certificate
```

而不是一开始就写成必须由“单一全局 K”生成的对象。用户提示里已经允许我把 `Obs_{12}(K)` 改成更干净的记号；数学上更稳的 primitive 记号是：

```text
Obs_{12}(s_1,s_2)
```

这里 `s_1, s_2` 是两个 chart 上已经声明好的 local sections。随后再把 `Obs_{12}(K)` 作为一个派生版本加入：若每个 chart 都额外给出 extraction map 与 local section map，则可由 `K` 生成 `(s_1,s_2)`。这样做的优点是，**第一版证书不依赖尚未完全冻结的“全局提取语法”**，但仍然满足 taskbook 要求的 finite, exact, zero-GPU, file-backed 风格。 [来源：GPT55_PRO_FINITE_GLUE_OBJECT_CERTIFICATE_PROMPT_20260705.md:67-104；from_repo/docs/infra/recovery/MAOFIELD_D705_FINITE_GLUE_OBJECT_TASKBOOK_20260705.md:14-26,53-61；from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_object_atlas_glue_report26_20260705.md:82-94]

### 证书数据

一个**两图有限粘合障碍证书**可定义为如下有穷有理数据：

设 `I_1, I_2` 为两个有限 chart carrier，`O_{12}` 为有限 overlap 对象。给定 restriction maps

```text
rho_1 : Q^{I_1} -> Q^{O_12}
rho_2 : Q^{I_2} -> Q^{O_12}
```

以及 overlap 上的正有理权重 `w_12(o) > 0`。再给定两个局部 section 空间 `H_1 = Q^{I_1}`, `H_2 = Q^{I_2}`，两个局部 nuisance / gauge 参数空间 `G_1, G_2`，与它们到 overlap 的 gauge-transfer maps

```text
lambda_1 : G_1 -> Q^{O_12}
lambda_2 : G_2 -> Q^{O_12}.
```

对于已声明的 local sections `s_i in H_i`，定义 raw overlap mismatch

```text
m_12(s_1,s_2) = rho_1 s_1 - rho_2 s_2.
```

定义有效 overlap gauge 子空间

```text
Gamma_12 = { lambda_1(g_1) - lambda_2(g_2) : g_i in G_i } subseteq Q^{O_12}.
```

在加权内积

```text
<u,v>_{w_12} = sum_{o in O_12} w_12(o) u(o) v(o)
```

下，令 `P_{Gamma_12}` 是对 `Gamma_12` 的加权正交投影，则 obstruction functional 定义为

```text
Obs_12(s_1,s_2)
  = min_{g_1,g_2} || m_12(s_1,s_2) - (lambda_1(g_1)-lambda_2(g_2)) ||_{w_12}
  = || (I - P_{Gamma_12}) m_12(s_1,s_2) ||_{w_12}.
```

这是一个完全有限、完全线性代数、完全可 exact-rational 化的对象；其形式直接继承了包内既有的“有限加权内积 + 投影 away from declared nuisance”的做法。旧 formal note v1 已经把 gluing absorption guard 的核心句型写成：局部 residual sections 的 overlap mismatch 若被 overlap nuisance 消掉，就不是 gluing obstruction；只有在投影 away from nuisance 后仍非零，才是候选障碍。 [来源：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_20260625.md:348-367；from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:49-79；from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py:78-99]

### 局部残差型版本

若 node36 希望证书与当前主核更紧地耦合，则可直接加入 local section maps：

```text
S_i : Q^{I_i} -> Q^{I_i},    im(S_i) subseteq N_i^{perp,w_i}
```

典型选择是

```text
S_i = I - P_{N_i},
```

其中 `N_i` 是 chart `i` 的局部 nuisance 子空间，`w_i` 是 chart `i` 的正有理权重。此时对局部原始数据 `x_i in Q^{I_i}` 定义 `s_i = S_i x_i`，对公共源 `K` 与 extraction maps `E_i` 则定义 `x_i = E_i K`，进而得到派生的 `Obs_12(K)`。这与 programme note 里 chart、metric object、transport、defect certificate 的形式骨架是相容的，只是把它压缩到最小可执行对象上。 [来源：from_repo/docs/infra/MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md:665-718；from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_object_atlas_glue_report26_20260705.md:86-92]

### 证书 tuple

我建议保存的 certificate tuple 字段至少包括：

```text
Xi_12 =
(
  artifact_id,
  chart_1_id, chart_2_id,
  carrier_manifest_1, carrier_manifest_2, overlap_manifest_12,
  weights_1, weights_2, weights_12,
  section_map_1, section_map_2,
  nuisance_basis_1, nuisance_basis_2,
  gauge_basis_1, gauge_basis_2,
  gauge_transfer_1, gauge_transfer_2,
  restriction_matrix_1, restriction_matrix_2,
  local_section_1, local_section_2,
  overlap_mismatch_raw,
  overlap_gauge_basis,
  projected_mismatch,
  obstruction_norm_squared,
  exact_checks,
  evidence_boundary
).
```

其中 `section_map_i`、`nuisance_basis_i` 可以在最小 primitive 版本中退化为恒等与零空间；但证书 schema 最好一开始就为它们留位，这样后续从 primitive certificate 升级到 `K`-generated certificate 时无需改 JSON 结构。 [来源：GPT55_PRO_FINITE_GLUE_OBJECT_CERTIFICATE_PROMPT_20260705.md:88-104,156-162；from_repo/docs/infra/MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md:797-810]

### JSON 必须保存的元数据

JSON 中必须保存以下 exact 元数据，而且**所有有理数都应以字符串形式写入**，不允许把 exact 数据降成 float：

```text
schema_version
artifact_name
date
status
arithmetic = "fractions.Fraction"
chart / overlap row order
rational weights as strings
basis vectors / matrices as strings
restriction matrices
gauge-transfer matrices
raw mismatch
projected mismatch
obstruction_norm_squared
all exact checks
runtime metadata
sha256 of JSON and markdown
strongest_allowed_verdict
blocked_claims / forbidden_interpretations
```

这一点与现有 exact witness 的做法完全同型：v1.4 exact witness 由 `fractions.Fraction` 构造，JSON 保存 basis、projection matrices、witness、exact checks 与 evidence boundary；而 v1.3 harness note 又明确说 float harness 只是 regression support，数学 claim 由 analytic proof 与 exact rational certificate 承载。 [来源：from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py:126-220；from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json:1-77；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md:7-18,96-107]

## 正负控制

### 我建议的最小 exact 控制尺寸

如果目标是**尽量紧贴当前 package 的 two-way-table / additive core**，那么最小而又“有内容”的 overlap 不应选 1 维或 2 维线段，而应选一个 **4-cell overlap**。原因是：当前主核的 nuisance 语言是 `C ⊕ A ⊕ B0`，而最小能承载一个真正非加性方向的有限对象，就是 `2×2` 表；这正是 formal note v1.3 与 exact witness v1.4 已经证明过的最小非平凡载体。相比之下，`3-cell charts + 2-cell overlap` 虽然在集合论上更小，但会把 gauge 设计推向更任意的 1 维线性代数，不如 2×2 overlap 那样自然地继承当前主核。 [来源：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:41-79,285-344；from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_object_atlas_glue_report26_20260705.md:68-76,100-108]

因此，我建议第一版 exact control 采用：

```text
O_12 = 2 x 2 overlap
w_12 = uniform = (1/4,1/4,1/4,1/4)
Gamma_12 = N_add(O_12)
```

其中 overlap nuisance 取当前 package 已熟悉的 additive space：

```text
N_add(O_12) = span{1, q-centered, b-centered}.
```

这是对旧 gluing absorption guard 的 exact-rational 正规化，而不是新造一个任意 gauge 线。 [来源：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_20260625.md:348-367；from_repo/scripts/debranded_residual_transport_harness.py:286-301；from_repo/scripts/debranded_residual_transport_harness_v1_1.py:682-697]

### 兼容正控

取 overlap 行主序为

```text
(q1,b1), (q1,b2), (q2,b1), (q2,b2)
```

令两个局部 sections 的 overlap mismatch 为

```text
m_plus = (1, 2, 3/2, 5/2).
```

这是一个严格的 additive 向量，因此属于 `N_add(O_12)`，故

```text
Obs_12^2 = 0.
```

若要把它写成真正两图对象，只需令 `rho_1 s_1 - rho_2 s_2 = m_plus`；例如最小做法可以取 `rho_1 s_1 = 0`，`rho_2 s_2 = -m_plus`。若 node36 坚持“proper overlap 而非全重合 chart”，则可在两个 chart 各加一个 overlap 外 dummy cell，且把该 cell 上的局部 section 设为 0；obstruction 值不变。这个正控的本质不是“局部 sections 完全相同”，而是“它们的差只落在声明允许吸收的 additive gauge 类里”。这一点正好对应旧 gluing absorption 逻辑。 [来源：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_20260625.md:356-367；from_repo/scripts/debranded_residual_transport_harness.py:286-301；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_1_20260625.md:75-78]

### 障碍反控

取 overlap mismatch 为

```text
m_minus = (1, -1, -1, 1).
```

这是标准 checkerboard 方向。对 uniform `2×2` overlap 与 additive nuisance，`m_minus` 恰好张成 `N_add(O_12)^{\perp}`，因此投影 away from `N_add` 后仍是它自己，且 exact weighted norm 为

```text
Obs_12^2 = ||m_minus||_{w_12}^2 = 1.
```

这给出一个最小 exact rational obstruction witness。它与 v0/v1.1 gluing_absorption block 的“absorbed mismatch vs checkerboard obstruction”模式完全同源，只是把 float regression 模式升级为 exact rational certificate。 [来源：from_repo/scripts/debranded_residual_transport_harness.py:286-301；from_repo/scripts/debranded_residual_transport_harness_v1_1.py:682-697；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V0_20260625.md:59-68；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_1_20260625.md:75-78]

### 控制所需的 exact 数据

首个 package-grade gluing certificate 所需的 exact 数据其实很少。正负控都只需要：

- overlap manifest 的固定顺序；
- overlap weights；
- overlap nuisance basis；
- 两个 local restricted sections，或者等价地，一个 overlap mismatch；
- projection matrix 或可重算的 basis + weights；
- `Obs^2` 的 exact fraction；
- evidence boundary 与 forbidden interpretations。 [来源：from_repo/docs/infra/MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md:797-810；GPT55_PRO_FINITE_GLUE_OBJECT_CERTIFICATE_PROMPT_20260705.md:88-111]

## 证明义务与判定

### `Obs = 0` 当且仅当局部 sections 在允许 gauge 下兼容

这个命题为**真**，而且几乎是定义级别的。因为 `Obs_12` 本身就是 mismatch 到有效 overlap gauge 子空间 `Gamma_12` 的加权距离；在有限维带权内积空间里，距离为 0 当且仅当该向量属于该子空间。因此

```text
Obs_12(s_1,s_2)=0
iff
m_12(s_1,s_2) in Gamma_12
iff
exists g_1,g_2 such that rho_1 s_1 + lambda_1(g_1) = rho_2 s_2 + lambda_2(g_2).
```

这正是“compatible modulo declared gauge”的严格线性代数版本。 [来源：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_20260625.md:348-367；from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py:78-99]

### `Obs > 0` 蕴含不存在 declared gauge 类内的全局 pasted object

这个命题为**真，但需按有限两图 cover 的语义精确表述**。若“global pasted object”指的是在有限并集 carrier `I_1 ∪ I_2` 上的一个 section `s`，其限制与 gauge-adjusted local sections 相等，那么两图情形下，**overlap 上相等就是存在 piecewise 全局 section 的充分必要条件**。因此 `Obs>0` 直接推出：在声明的 gauge 类内，不存在满足这一定义的 pasted object。若额外要求更强的 global regularity、更多 chart coherence、或额外 transport 约束，则必须把那些条件再写进证书，不应偷带。 [来源：GPT55_PRO_FINITE_GLUE_OBJECT_CERTIFICATE_PROMPT_20260705.md:121-124；from_repo/docs/infra/recovery/MAOFIELD_D705_FINITE_GLUE_OBJECT_TASKBOOK_20260705.md:20-26,53-61]

### 扩大 gauge 会吸收障碍，因此 gauge 声明不是装饰

这个命题为**真**，而且是本对象必须 fail-closed 的核心。旧 formal note v1 已经明确说：若 overlap mismatch 在允许 nuisance/gauge 内被吸收，则它**不是** gluing obstruction；反过来，如果轻微放大 gauge 就能把原障碍吸掉，那么原障碍只能是“相对于旧 gauge 声明”的障碍，而不能被夸大为更深结构。Report26 也把这一点单独作为“必须保留的降温句”。 [来源：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_20260625.md:356-367；from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_object_atlas_glue_report26_20260705.md:74-76]

### 这个对象不是现有两投影 order-defect 定理换词

这个命题应判为**真，但要加条件说明**。若把两 chart 退化成“同一 carrier、同一 overlap、restriction 为恒等、gauge 为零”的特例，那么它当然会塌回 order-defect 风格的 same-carrier mismatch，甚至可直接取 `m_12(K)=D_w K`。但一般的 two-chart certificate 还包含三个当前 v1.3 order-defect note 没有的层次：第一，真正的 chart-indexed局部对象；第二，restriction 到 overlap 的比较；第三，对 overlap gauge 的最小化。因此它是**邻接对象**，不是原 theorem 的简单改名。 [来源：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:156-191,243-255；from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_object_atlas_glue_report26_20260705.md:45-46,64-76]

### 这个对象仍然只是有限线性代数，而不是广义 sheaf 理论

这个命题为**真**。包内多处边界都明确禁止把当前材料升级为 broad sheaf / holonomy / field theory；taskbook 也要求任何 sheaf / holonomy / gluing 类比都必须标成 finite analogy。我的定义完全只用到了有限维有理向量空间、正权重、restriction 矩阵、gauge 子空间、正交投影与 piecewise pasting，不需要任何超出当前包证据边界的结构。 [来源：PACKAGE_README.md:13-20；from_repo/docs/infra/gpt_deep_research/METRIC_IDENTITY_OBJECT_ATLAS_GLUE_REPORT26_ADOPTION_NOTE_20260705.md:112-122；from_repo/docs/infra/recovery/MAOFIELD_D705_FINITE_GLUE_OBJECT_TASKBOOK_20260705.md:53-61,63-75]

## 与现有 order-defect 主核的关系

这个新对象与现有主核**有关联，但不是同一命题**。它最稳妥的定位，是“**单图 procedural mismatch 的 overlap/generalized neighbor**”。

现有主核的环境是有限正权二向表 `Q×B`，定义了 `C, A, B0, N_add`，再由加权投影构造真加性残差 `I-P_N`、两种 sequential stripping outputs，以及它们的差 `D_w`。在 non-product 权重下，formal note v1.3 证明：存在 `K in A` 或 `K in B0` 使得真残差为零、一个顺序输出为零、另一个顺序输出非零，因此非零量只能解释为 procedure artifact；exact witness v1.4 又把最小 `2×2` 例子升级为 exact rational 证书。 [来源：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:64-79,156-191,243-255,285-344；from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md:30-66]

新的 gluing certificate 与这条主核的具体关系可以精确写成五句。

其一，它继续使用**相同的有限 weighted Hilbert-space 语法**。也就是说，overlap 上仍然是“正权重 + 有限向量空间 + 子空间 + 加权投影 + 范数”这一套，而不是额外引入 broad theory。若把 overlap 取成一个 `2×2` 表，则 overlap gauge 甚至可以直接取 `N_add(O_12)`，与主核的 additive nuisance 完全同型。 [来源：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:41-79；from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_20260625.md:348-367]

其二，它把“真 residual vs wrong-order artifact”的判别逻辑，改写成“**可 absorb mismatch vs surviving obstruction**”的判别逻辑。order-defect 主核问的是：单一 carrier 上两种 stripping 顺序给出的差异，是否只是 procedure artifact。gluing certificate 问的是：两个局部 sections 的 overlap 差异，在声明好的 gauge 类下是否还能存活。两者的共同点都是：**不把任何非零差异自动当成深层对象，而必须先 project away declared nuisance/gauge**。 [来源：from_repo/docs/infra/MAOFIELD_METRIC_IDENTITY_PROGRAMME_20260704.md:706-718；from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_20260625.md:356-367；from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_object_atlas_glue_report26_20260705.md:74-76]

其三，`D_w` 在这个新对象里只占一个**特例位置**。若两个 chart 恰好是在同一 overlap 上比较两种局部程序，那么可把

```text
m_12(K) = rho_1 s_1(K) - rho_2 s_2(K)
```

特化成 `D_w K`。但一般 two-chart glue certificate 允许 carrier、restriction、局部 section map、以及有效 gauge 类都发生变化，因此它比 `D_w` 更一般，又比广义 chart theory 更小。 [来源：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:156-191；from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_object_atlas_glue_report26_20260705.md:64-76]

其四，exact `2×2` witness 不是这个对象的完整替身，但它是最好的**companion artifact**。它可以作为同一 package 内的 negative companion：在 same-carrier / zero-gauge 退化情形下，`D_w K != 0` 给出一个“不可兼容”的严格见证；与此同时，gluing certificate 第一版则把“局部—整体 compatibility failure”单独做成一个 overlap object。两者并行，反而比强行把新对象说成旧 theorem 直接推广更诚实。 [来源：from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md:44-66；from_repo/docs/infra/gpt_deep_research/METRIC_IDENTITY_OBJECT_ATLAS_GLUE_REPORT26_ADOPTION_NOTE_20260705.md:46-49,83-85]

其五，`OI^{op}_{N_add}(w)` 是**伴随指标**，不是 glue certificate 的替代品。Report26 已明确指出：`OI^{op}_{N_add}(w)=0 iff w is product form` 与 exact product control 是“容易立即补齐”的 companion task，但本轮真正有创造性的对象仍是 finite gluing obstruction certificate。换言之，`OI` 是单图上的 operator-norm instability summary，而 `Obs_12` 是两图间的 pointwise compatibility certificate；它们相邻，但角色不同。 [来源：from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_object_atlas_glue_report26_20260705.md:100-108；from_repo/docs/infra/gpt_deep_research/METRIC_IDENTITY_OBJECT_ATLAS_GLUE_REPORT26_ADOPTION_NOTE_20260705.md:83-85]

## 既有工件审计

现有包中的“older residual transport / holonomy / gluing”材料**确实能提供骨架与测试图样**，但还没有任何一个可以直接被当作当前风格的 exact rational finite gluing certificate。adoption note 已经把这一点说得很清楚：旧 gluing/holonomy 材料存在，但它们还不是 exact rational finite gluing obstruction certificate；同时也没有找到现成的 exact `2×3/3×3` certificate library。 [来源：from_repo/docs/infra/gpt_deep_research/METRIC_IDENTITY_OBJECT_ATLAS_GLUE_REPORT26_ADOPTION_NOTE_20260705.md:87-101]

我对重要旧工件的分类如下。

### 可复用与不可复用分类

| 工件 | 分类 | 严格理由 |
|---|---|---|
| `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_20260625.md` 中的 gluing absorption guard | `CAN_REUSE_CORE_IDEA` | 它已经给出有限 cover、restriction 到 overlap、局部 residual sections、overlap mismatch、以及投影 away from overlap nuisance 的判别句型；这正是新证书的定义核心。 |
| `from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py` 与对应 v1.4 exact witness | `CAN_REUSE_CORE_IDEA` | 它提供 exact rational 矩阵/投影/JSON/Markdown 三位一体的实现模板，可直接复用到 glue certificate。 |
| `from_repo/scripts/debranded_residual_transport_harness.py` 与 `SYNTHETIC_HARNESS_V0_20260625.md` 中的 `gluing_absorption` | `CAN_REUSE_TEST_PATTERN_ONLY` | 它清楚给出“absorbed mismatch vs checkerboard obstruction”的正反控图样，但全部是 float regression 模式，还没有 exact rational 证书。 |
| `from_repo/scripts/debranded_residual_transport_harness_v1_1.py` 与 `SYNTHETIC_HARNESS_V1_1_20260625.md` 中的 `gluing_absorption`、`triple_overlap_gluing_cocycle` | `CAN_REUSE_TEST_PATTERN_ONLY` | 这些 block 对两图/三图后续测试很有用，但仍是 deterministic float harness；v1.1 note 自己也把它限定在 formal design review only。 |
| `from_repo/scripts/debranded_residual_transport_harness_v1_2.py` 与 `SYNTHETIC_HARNESS_V1_2_20260627.md` 中的 `square_holonomy_telescoping_control`、`triple_overlap_gluing_cocycle` | `CAN_REUSE_TEST_PATTERN_ONLY` | 可为后续三图循环与 square-path 扩展提供模式，但并不产出当前 round 所需的 exact rational two-chart certificate。 |
| `from_repo/scripts/debranded_residual_transport_harness_v1_3.py` 与 `SYNTHETIC_HARNESS_V1_3_20260628.md` | `REGRESSION_SUPPORT_ONLY` | v1.3 已收缩为 theorem-control harness，明确声明 float harness 只是 regression support，数学 claim 由 analytic proof 与 exact certificate 承载；它更适合作为 OI/product companions 的回归守卫，不是 gluing 核心。 |
| `from_repo/scripts/residual_transport_holonomy_synthetic.py` | `STALE_OR_RISKY` | 这是更早的 residual_transport_holonomy synthetic harness，仍带随机抽样与旧命名面，虽然边界谨慎，但与当前 package 的 exact rational certificate 风格不一致。 |

上述分类的依据并不靠 RAG 摘要，而是靠包内一手 note 与脚本本身：v1 formal note 有 gluing absorption 的定义雏形；v0/v1.1/v1.2 harness 提供 gluing 与 cocycle 的 toy test pattern；v1.3 则显式把 float harness 定位为 regression support only；而 adoption note 又确认这些旧材料尚未达到当前 round 要求的 exact rational certificate 级别。 [来源：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_20260625.md:344-367；from_repo/scripts/debranded_residual_transport_harness.py:286-301；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V0_20260625.md:40-44,59-68；from_repo/scripts/debranded_residual_transport_harness_v1_1.py:682-737；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_1_20260625.md:24-39,75-87；from_repo/scripts/debranded_residual_transport_harness_v1_2.py:646-663；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md:44-57,86-93；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md:7-18,41-47,96-107；from_repo/scripts/residual_transport_holonomy_synthetic.py:1-8,310-344]

## 实现规范与最终决定

### 最小 node36 实施方案

若 node36 现在就执行，我建议直接落成如下四个新文件，并保持与 v1.4 exact witness 相同的风格：

```text
from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_5_TWO_CHART_GLUE_CERTIFICATE_20260705.md
from_repo/scripts/debranded_residual_transport_exact_glue_certificate_v1_5.py
from_repo/docs/infra/debranded_residual_transport/exact_glue_certificate_v1_5_20260705.json
from_repo/docs/infra/debranded_residual_transport/EXACT_GLUE_CERTIFICATE_V1_5_20260705.md
```

formal note 应只做四件事：冻结 primitive certificate 定义；给出 `Obs=0 iff compatibility modulo declared gauge` 的证明；给出 `Obs>0` 排除 declared gauge 类内全局 pasting 的两图引理；最后明确这个对象只是 finite linear algebra，不是 broad sheaf theory。script 则只负责 exact rational 计算、JSON 生成、Markdown 回写与 sha256 记录。 [来源：from_repo/docs/infra/recovery/MAOFIELD_D705_FINITE_GLUE_OBJECT_TASKBOOK_20260705.md:76-89；from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py:126-220,223-280]

### 必须通过的 exact assertions

实现时必须做成 fail-closed。至少应包含下列 exact assertions：

- 所有权重为正有理数，并按声明归一化。
- restriction matrices 与 overlap manifest 一致。
- gauge basis 与 nuisance basis 的秩检查通过。
- `Gamma_12` 的 Gram matrix 可逆于其独立基上。
- 正控 `m_plus` 的 projected mismatch **恰好**为零。
- 反控 `m_minus` 的 projected mismatch **恰好**等于声明值，且 `Obs^2` 为严格正的 reduced fraction。
- 若提供 proper-overlap 扩展版，则去掉 dummy exterior cells 后 obstruction 不变。
- JSON 与 Markdown 的 sha256 可回读一致。
- 所有 runtime arithmetic 均标记为 `fractions.Fraction`，禁止 silently cast 到 float。 [来源：from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py:118-123,126-220；from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md:30-42；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md:30-42]

### forbidden wording scan 与状态更新

forbidden wording scan 应至少拦截以下语气：

```text
observed field
sheaf theorem
holonomy theory
broad ANOVA
dependent-input theory
peer reviewed
paper ready
arXiv
journal
MaoField empirical positive
full panel
training
inference
new loss
F3 positive
LOSO passed
```

这不是文风问题，而是 package governance 的硬边界。实现完成后，node36 应更新 `STATE.md`，把“已设计并落地 exact two-chart glue certificate”写成**bounded mathematical artifact**，并保留 Mode B `insufficient_artifact`、duplicate risk `MEDIUM`、以及“非 peer review / 非经验正结果”的边界；随后再做一次 RAG refresh 和 hash record。 [来源：PACKAGE_README.md:13-20；from_repo/STATE.md:24-28；from_repo/docs/infra/gpt_deep_research/METRIC_IDENTITY_OBJECT_ATLAS_GLUE_REPORT26_ADOPTION_NOTE_20260705.md:112-122；from_repo/docs/infra/recovery/MAOFIELD_D705_FINITE_GLUE_OBJECT_TASKBOOK_20260705.md:63-89]

### 是否还需要向 node36 追要文件

本轮**没有阻塞性请求**。adoption note 已说明 node36 的补充搜索没有发现现成 exact gluing certificate、也没有发现现成的 exact `2×3/3×3` library 或权重连续性证明 note；但这并不妨碍当前最小对象的定义与 exact control 构造。若之后要做 near-product bound、三图 cocycle exact 化、或 square-path defect exact 化，再去请求额外旧稿会更合适。 [来源：from_repo/docs/infra/gpt_deep_research/METRIC_IDENTITY_OBJECT_ATLAS_GLUE_REPORT26_ADOPTION_NOTE_20260705.md:87-101；from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_object_atlas_glue_report26_20260705.md:112-136]

### 最终决定

```text
DESIGN_TWO_CHART_GLUE_CERTIFICATE
```

原因是：当前包已经拥有这个对象所需的全部“硬部件”——有限加权投影语法、exact rational artifact 模板、gluing absorption 的定义矿脉、正负控历史图样，以及被明确接受的 round-level branch 选择；缺的不是定义层本身，而是把它们真正压成一个最小 exact object。相反，若此时退回 `PATCH_DEFINITIONS_BEFORE_GLUE`，大概率只会再写一轮 definitions prose；若改走 `BUILD_OI_AND_PRODUCT_CONTROLS_FIRST`，虽然 companion tasks 很容易补齐，但会错过本轮最有价值的新对象。最合理的执行顺序，是先实现我上面给出的 **primitive overlap-core two-chart certificate**，再把它升格成带 proper-overlap carriers 与局部 residual maps 的 subtype；等这一对象稳定后，再扩展到三图循环与 square-path。 [来源：from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_object_atlas_glue_report26_20260705.md:100-108,138-146；from_repo/docs/infra/gpt_deep_research/METRIC_IDENTITY_OBJECT_ATLAS_GLUE_REPORT26_ADOPTION_NOTE_20260705.md:46-49,61-85,124-133；from_repo/docs/infra/recovery/MAOFIELD_D705_FINITE_GLUE_OBJECT_TASKBOOK_20260705.md:41-50,76-89]