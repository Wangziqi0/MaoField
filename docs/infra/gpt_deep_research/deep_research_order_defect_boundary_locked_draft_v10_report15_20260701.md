BOUNDARY_LOCKED_LOCAL_DRAFT_CANDIDATE

# 边界锁定有限加权顺序缺陷短札局部草稿候选

## 摘要

本地首检与边界核验已通过：上传 zip 内首检所要求的核心文件均存在且可读；我对 `SHA256SUMS.txt` 与 `PACKAGE_FILE_MANIFEST.sha256` 分别做了本地校验，均返回通过。包内状态链也一致地把本轮任务限定为“在锁内生成局部短札草稿候选”，而不是解除锁、授权发布、授权投稿，或把外部模型提升为证明/书目权威。〔依据：`PACKAGE_README.md:3-21,23-53`; `from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_draft_authorization_v9_report14_20260701.md:5-9,17-23,53-59`; `from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_DRAFT_AUTHORIZATION_V9_REPORT14_ADOPTION_NOTE_20260701.md:13-18,27-32,43-56`; `from_repo/docs/infra/recovery/ORDER_DEFECT_D701_BOUNDARY_LOCKED_DRAFT_V10_TASKBOOK_20260701.md:5-17,22-29,55-92`; `from_repo/docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_BOUNDARY_LOCKED_DRAFT_V10_20260701.md:11-18,67-109`; `from_repo/STATE.md:7-21,24-28`〕

本文本因此只作为**局部草稿候选**：它讨论的对象严格限于有限正权二向表 `X = Q x B`、其加权 Hilbert 空间结构、常数子空间 `C`、行主效应子空间 `A`、列主效应子空间 `B0`、加性扰动子空间 `N_add = C + A + B0`、相应加权正交投影，以及两种有序 stripping 算子与顺序缺陷算子 `D_w`。它不把该对象推广成广义 ANOVA 理论、广义 dependent-input decomposition 理论、广义 noncommuting-projection 理论，亦不触及 MaoField 的经验正结论。〔依据：`from_repo/docs/infra/recovery/ORDER_DEFECT_D701_BOUNDARY_LOCKED_DRAFT_V10_TASKBOOK_20260701.md:31-52,74-92`; `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:7-32,34-69`; `from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:17-31,51-80`〕

```text
Proposition 1: COMPLETE_LOCAL_DRAFT
Proposition 2: COMPLETE_LOCAL_DRAFT
Proposition 3: COMPLETE_LOCAL_DRAFT
Exact 2 x 2 rational witness: CERTIFICATE
Deterministic harness: HARNESS_ONLY
Bibliography/positioning: COMPLETE_LOCAL_DRAFT with MEDIUM duplicate risk
Overall status: BOUNDARY_LOCKED_LOCAL_DRAFT_CANDIDATE_ONLY
Mode B MaoField empirical status: insufficient_artifact
```

上述 live labels 是 V10 包要求原样保留的边界标签。〔依据：`PACKAGE_README.md:35-45`; `from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_DRAFT_AUTHORIZATION_V9_REPORT14_ADOPTION_NOTE_20260701.md:43-50`; `from_repo/docs/infra/recovery/ORDER_DEFECT_D701_BOUNDARY_LOCKED_DRAFT_V10_TASKBOOK_20260701.md:20-29`〕

## 引言与贡献

本文考虑一个非常窄的有限维问题：在有限正权二向表上，如果先剥离常数项、再依次剥离行主效应与列主效应，那么当权重不是边际乘积时，这两种剥离顺序一般不给出同一结果。更具体地说，即便输入信号本身只是纯主效应，真实加性残差为零，错误顺序的 sequential stripping 也可能制造出一个非零输出；这个输出应理解为**顺序伪影**，而不是“真实交互残差”。〔依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:110-159,164-215`; `from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:53-59`〕

这份局部草稿候选的贡献被有意压低到以下层级。第一，它在有限正权二向表对象内陈述并概述三条局部命题：乘积权与主效应正交性的等价、顺序独立性与乘积权的等价、以及非乘积权下纯主效应 witness 的存在性。第二，它把展示用 2×2 witness 固定为精确有理证书，而不是浮点回归件。第三，它把 deterministic harness 明确压到“回归支持”而非“定理证明”角色。第四，它继承本地 bibliography/positioning 对近邻文献的保守定位，因此只允许“有限加权 projection-order artifact note”这一小范围陈述。〔依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:82-108,110-240`; `from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md:30-66`; `from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md:5-18,96-107`; `from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:17-31,51-80`〕

## 有限加权设置与记号

令 `Q` 与 `B` 为有限集合，`X = Q x B`，并赋予严格正的归一化权重 `w(q,b) > 0`，满足 `\sum_{q,b} w(q,b)=1`。在 `\mathbb{R}^{Q\times B}` 上定义加权内积
\[
\langle f,g\rangle_w=\sum_{q,b} w(q,b)f(q,b)g(q,b),
\]
以及边际
\[
w_Q(q)=\sum_b w(q,b),\qquad w_B(b)=\sum_q w(q,b).
\]
这是本文唯一工作的加权 Hilbert 空间。〔依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:34-43`; `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:33-49`〕

定义子空间
\[
C=\mathrm{span}\{1\},\qquad
A=\{a(q): \sum_q w_Q(q)a(q)=0\},\qquad
B0=\{b(b): \sum_b w_B(b)b(b)=0\},
\]
并记
\[
N_{\mathrm{add}}=C+A+B0.
\]
令 `P_C`、`P_A`、`P_B0`、`P_N` 分别表示到这些子空间的加权正交投影。这里需要保留一个关键边界：一般并不能先验写成 `P_N=P_C+P_A+P_B0`；只有在 product-weight 情形下，这个分解才退化为正交直和。〔依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:45-55,112-136`; `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:51-69,158-186`〕

本文讨论的两种有序 stripping 算子是
\[
R_{Q\text{ then }B}=(I-P_{B0})(I-P_A)(I-P_C),\qquad
R_{B\text{ then }Q}=(I-P_A)(I-P_{B0})(I-P_C),
\]
并定义顺序缺陷算子
\[
D_w=R_{Q\text{ then }B}-R_{B\text{ then }Q}.
\]
由于 `P_A 1 = P_B0 1 = 0`，局部证明稿已把它化简为
\[
D_w=P_{B0}P_A-P_AP_{B0}.
\]
因此，本文研究的不是抽象“大理论”，而是一个具体有限对象里两类主效应投影是否交换的问题。〔依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:57-69`; `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:127-144`〕

## 命题与证明概要

**Proposition 1: COMPLETE_LOCAL_DRAFT.** 对有限正权 `w`，`w(q,b)=w_Q(q)w_B(b)` 对所有单元成立，当且仅当 `A` 与 `B0` 在 `\langle\cdot,\cdot\rangle_w` 下正交。证明梗概是标准且有限维的：若 `w` 为乘积权，则任意 `a\in A`、`b\in B0` 的内积按边际分解后立即为零；反向则取中心化指标
\[
a_{q_0}(q)=1_{q=q_0}-w_Q(q_0),\qquad
b_{b_0}(b)=1_{b=b_0}-w_B(b_0),
\]
并利用
\[
\langle a_{q_0},b_{b_0}\rangle_w = w(q_0,b_0)-w_Q(q_0)w_B(b_0),
\]
逐格恢复乘积权恒等式。〔依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:80-125`; `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:82-108`〕

**Proposition 2: COMPLETE_LOCAL_DRAFT.** 在有限正权情形，下列条件等价：`w` 是乘积权、`A ⟂ B0`、`D_w=0`、以及 `R_{Q\text{ then }B}=R_{B\text{ then }Q}`。当这些条件成立时，两种有序 stripping 都等于真正的加性残差投影 `I-P_N`。证明梗概分两步。正向：乘积权给出 `A ⟂ B0`，于是 `C`、`A`、`B0` 成为正交直和，从而 `P_N=P_C+P_A+P_B0` 且 `P_AP_{B0}=P_{B0}P_A=0`，所以两种顺序都简化为 `I-P_N`。反向：若 `D_w=0`，对任意 `b\in B0` 有
\[
0=D_w b=P_{B0}P_A b-P_A b,
\]
故 `P_A b` 同时落在 `A` 与 `B0` 中；而局部引理指出 `A\cap B0=\{0\}`，因此 `P_A b=0`，进而 `A ⟂ B0`，再由 Proposition 1 反推 `w` 为乘积权。〔依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:71-80,110-162`; `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:145-187`〕

**Proposition 3: COMPLETE_LOCAL_DRAFT.** 若 `w` 不是乘积权，则存在一个纯主效应 witness `K`，使得 `K\in N_{\mathrm{add}}`、真实加性残差 `(I-P_N)K=0`、一种顺序残差为零，而相反顺序残差非零。局部修补稿选择 `K\in B0` 的版本：由非乘积权得到 `A` 与 `B0` 不正交，于是存在 `b\in B0` 满足 `P_A b\neq 0`，令 `K=b`。因为 `K\in B0`，它自动满足 `P_CK=0`、`P_{B0}K=K`，从而
\[
R_{B\text{ then }Q}K=(I-P_A)(I-P_{B0})(I-P_C)K=0.
\]
另一方面，
\[
R_{Q\text{ then }B}K=-(I-P_{B0})P_AK.
\]
若它也为零，则 `P_AK=P_{B0}P_AK`，所以 `P_AK\in A\cap B0=\{0\}`，与 `P_AK\neq 0` 矛盾。因此 wrong-order 输出必须非零。这里要特别保留量词边界：命题只给出**存在性** witness，并不声称所有输入都出现顺序差异。〔依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:164-215`; `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:188-255`〕

以上三条命题之所以能在本包里被保留为 `COMPLETE_LOCAL_DRAFT`，并不是因为它们被提升成外部证明权威，而是因为此前 proof-repair recheck 的本地采纳已经把它们限定在“受控有限正权二向表对象内部”的局部草稿地位，同时继续维持 emergency lock。〔依据：`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_PROOF_REPAIR_RECHECK_REPORT9_ADOPTION_NOTE_20260630.md:16-18,42-63,65-81`; `from_repo/docs/infra/recovery/ORDER_DEFECT_D630_REPORT9_LOCAL_VERIFICATION_20260630.md:81-92`; `PACKAGE_README.md:35-45`〕

## 精确二维见证与证书角色

**Exact 2 x 2 rational witness: CERTIFICATE.** 局部证明稿把展示用例固定为
\[
w=\frac1{11}\begin{bmatrix}1&2\\3&5\end{bmatrix},
\qquad
K=\left(\frac7{11},-\frac4{11},\frac7{11},-\frac4{11}\right)\in B0.
\]
对这个 witness，证书给出精确等式
\[
(I-P_N)K=0,\qquad
R_{B\text{ then }Q}K=0,
\]
以及
\[
R_{Q\text{ then }B}K=
\left(\frac1{32},\frac5{168},-\frac1{96},-\frac1{84}\right),
\qquad
\|R_{Q\text{ then }B}K\|_w^2=\frac{61}{177408}.
\]
这正是本短札展示顺序伪影的核心局部证书。〔依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:217-240`; `from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md:30-52`; `from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json:1-57`〕

证书文件还给出对称的 `A`-side witness，但本地最小展示并不依赖它；`B0` witness 已足以支撑 Proposition 3 的“存在性”版本。更重要的是，证书的意义被包内文档反复压到一个窄层级：它把 2×2 例子从 float-based regression support 升级为**精确有理算术的 certificate**，却不替代解析证明，也不授权任何 MaoField 经验性结论。〔依据：`from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md:54-66`; `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:239-240`; `from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_DRAFT_AUTHORIZATION_V9_REPORT14_ADOPTION_NOTE_20260701.md:43-50,63-67`〕

我也在本地复跑了证书脚本。复跑文件的整文件哈希会因为运行时平台元数据而漂移，但数学内容核验通过；这一点与早先的本地 verification 记录一致，后者明确把 `61/177408` 视为相关的数学证书内容，而不是跨环境整文件哈希。〔依据：`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_REPORT9_LOCAL_VERIFICATION_20260630.md:25-49`; `from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_PROOF_REPAIR_RECHECK_REPORT9_ADOPTION_NOTE_20260630.md:29-30`〕

## Harness 边界与相关工作重复风险

**Deterministic harness: HARNESS_ONLY.** v1.3 synthetic harness 被包内文档定义为 zero-GPU、synthetic、theorem-control harness；它不读取 MaoField 数据，不授权训练、checkpoint loading、full-panel generation、model inference 或 new loss。它包含四个通过的控制块：`product_weight_order_independence_control`、`centered_indicator_product_iff_control`、`nonproduct_pure_main_effect_no_go_control` 与 `threshold_contract_single_source_control`；其摘要还给出与精确证书相容的数值量，例如非乘积 pure-main-effect 控制里的 `artifact_weighted_norm_squared ≈ 0.00034384018759`，与精确值 `61/177408` 一致。〔依据：`from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md:5-18,32-77,96-107`; `/tmp/orderdefect_v10/rerun/harness.json:1-154`〕

但这类通过绝不能被解释为“浮点 JSON 证明了定理”。包内 canonical sentence 已将其锁死：**“The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats.”** 该句同时出现在 wording lock、harness 文档、proof-repair candidate、以及本地 verification 中。〔依据：`from_repo/docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md:7-18,27-52`; `from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md:7-18`; `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:25-32`; `from_repo/docs/infra/recovery/ORDER_DEFECT_D630_REPORT9_LOCAL_VERIFICATION_20260630.md:73-79`〕

**Bibliography/positioning: COMPLETE_LOCAL_DRAFT with MEDIUM duplicate risk.** 本地 bibliography/positioning 记录把最安全的定位压到一句话：这是 “a compact finite weighted projection-order artifact note with an exact 2 x 2 witness”。它显式否认自己是在提出新 ANOVA 理论、新 dependent-input Hoeffding decomposition 理论、新 Sobol/Shapley 理论或新 noncommuting projection 理论。其“最接近前件”被放在两类文献邻域：dependent-variable ANOVA/Hoeffding 分解，以及经典两投影/两子空间理论。〔依据：`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:17-31,51-59`〕

因此，这里的重复风险不是发现了 exact duplicate，而是**一旦措辞外扩，就会撞进已经拥挤的广域理论空间**。本地 bibliography 明确点名的近邻包括 Hooker 2007、Chastaing–Gamboa–Prieur 2012/2014-2015、Owen–Prieur 2017、Iooss–Prieur 2019、Il Idrissi 等 2025、Lamboni 2026，以及 Böttcher–Spitkovsky、Corach–Maestripieri、Halmos 等投影背景文献。由此，本短札只能维持在“有限正权二向表、product-weight iff main-effect orthogonality、order-independence iff product weight、existential witness、exact 2×2 certificate”这一层。〔依据：`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:33-49,65-80`〕

## 局限、禁断断言与 Node36/PI 发布前检查

这份文本的局限故意写得比数学核心更强。它不是 proof authority，不是 bibliography authority，不是 paper-ready authority，不是 posting authority，也不是 submission authority。它没有解除 emergency lock，也没有把 MaoField Mode B 从 `insufficient_artifact` 提升出去。它也不表述 full panel、16-cell aggregate、checkpoint loading、inference、training、new loss、observed residual/interaction/quotient-residual/transport/holonomy field、F3、LOSO、glass-box、completed formal system，或任何 MaoField empirical positive result。〔依据：`PACKAGE_README.md:18-21`; `from_repo/docs/infra/recovery/ORDER_DEFECT_D701_BOUNDARY_LOCKED_DRAFT_V10_TASKBOOK_20260701.md:74-92,94-103`; `from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_DRAFT_AUTHORIZATION_V9_REPORT14_ADOPTION_NOTE_20260701.md:30-32,63-67`; `from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_PROOF_REPAIR_RECHECK_REPORT9_ADOPTION_NOTE_20260630.md:65-81`〕

在进入任何公共发布决定之前，Node36 与 human PI 至少需要逐项复核以下事项：其一，确认外部模型输出没有越过上述禁断断言；其二，确认命题标签、证书标签、harness 标签、书目风险标签与整体状态标签保持原样；其三，确认正文只讨论有限正权二向表对象及其局部解析证明依赖；其四，确认 exact witness 仍只作为 certificate，而 harness 仍只作为 regression support；其五，确认 bibliography/positioning 仍保留 `MEDIUM duplicate risk` 并维持窄定位；其六，确认任何拟发布文本仍明确写出 emergency lock 未解除。〔依据：`from_repo/docs/infra/recovery/ORDER_DEFECT_D701_BOUNDARY_LOCKED_DRAFT_V10_TASKBOOK_20260701.md:18-29,54-67,74-103,105-112`; `from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_DRAFT_AUTHORIZATION_V9_REPORT14_ADOPTION_NOTE_20260701.md:43-56,55-56,63-67`; `from_repo/STATE.md:7-21,24-28`〕

## Boundary Ledger

**Allowed claims.** 允许的核心陈述只有这些：在有限正权二向表上，乘积权与 `A ⟂ B0` 等价；顺序独立 `R_{Q\text{ then }B}=R_{B\text{ then }Q}` 与乘积权等价；非乘积权下存在纯主效应 witness，使真实加性残差为零而 wrong-order stripping 产生非零伪影；展示性 `2×2` witness 具有精确有理证书，主 witness 的平方加权范数为 `61/177408`。这些 claim 都必须继续被限定在 controlled finite object 内。〔依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:82-108,110-240`; `from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:67-77`〕

**Forbidden claims.** 禁止宣称或背书：`emergency lock lifted`、`paper-ready`、`preprint-ready`、`posted`、`submission authorized`、`completed formal system`、`broad new ANOVA theory`、`broad new dependent-input decomposition theory`、`broad new noncommuting-projection theory`、`MaoField empirical positive result`、`full panel has run`、`16-cell aggregate exists`、`checkpoint loading`、`inference`、`training`、`new loss`、`MaoField residual observed`、`interaction observed`、`quotient-residual observed`、`transport field observed`、`holonomy field observed`、`glass box broken`、`F3 positive`、`LOSO passed`、`JSON floats prove theorem`、`harness proves theorem`。这些禁断语在 V10 taskbook 中被逐条列出。〔依据：`from_repo/docs/infra/recovery/ORDER_DEFECT_D701_BOUNDARY_LOCKED_DRAFT_V10_TASKBOOK_20260701.md:74-103`〕

**Proof dependencies.** 本局部草稿依赖的证明链条是：有限维加权设置与子空间定义；`A\cap B0=\{0\}`；“product weight iff main-effect orthogonality”；随后才是 Proposition 2 与 Proposition 3 的局部修补证明。换言之，文本依赖的是 `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 与其 `PROOF_REPAIR_CANDIDATE` 的解析骨架，而不是外部模型自身的权威。〔依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:33-69,80-187,188-255`; `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:34-240`〕

**Exact certificate role.** `EXACT_WITNESS_V1_4_20260629.md` 与对应 JSON/script 的角色是 `CERTIFICATE`：把展示例从浮点示例提升为 exact rational arithmetic certificate，并核定主 witness 的精确向量、投影结果与范数；但它“不替代解析证明”，也“不升级 MaoField 经验状态”。〔依据：`from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md:5-7,30-66`; `from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:217-240`〕

**Harness role.** `SYNTHETIC_HARNESS_V1_3_20260628.md` 与对应 JSON/script 的角色是 `HARNESS_ONLY`：它只做 deterministic regression support 和 theorem-control regression checks，不能被提升为 theorem proof，也不能被提升为 MaoField empirical evidence。〔依据：`from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md:5-18,41-52,96-107,109-126`; `from_repo/docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md:7-18,27-52`〕

**Bibliography caveats.** bibliography/positioning 只达到 `COMPLETE_LOCAL_DRAFT with MEDIUM duplicate risk`。安全定位是“有限加权 projection-order artifact note”，而不是新广义理论。风险不在 exact duplicate，而在过度扩张措辞时与 dependent-variable ANOVA/Hoeffding 与 classical two-projections 邻域发生覆盖冲突；Lamboni 2026 也只能作为当前 drafting 的 DOI / publisher-online-record 级近邻，不能被误当 camera-ready 元数据锚点。〔依据：`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:17-31,33-49,51-80`〕

**Release blockers.** 对任何公共发布而言，当前仍有实质性 blocker：emergency lock 仍在；整体状态仍是 `BOUNDARY_LOCKED_LOCAL_DRAFT_CANDIDATE_ONLY`；Mode B 仍是 `insufficient_artifact`；外部模型输出不得被当作 proof authority、bibliography authority、paper-ready authority、posting authority 或 submission authority。换言之，这份文本只能停留在本地候选层。〔依据：`PACKAGE_README.md:18-21,35-45`; `from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_DRAFT_AUTHORIZATION_V9_REPORT14_ADOPTION_NOTE_20260701.md:30-32,43-56,113`; `from_repo/docs/infra/recovery/ORDER_DEFECT_D701_BOUNDARY_LOCKED_DRAFT_V10_TASKBOOK_20260701.md:5-17,22-29,54-67,105-112`; `from_repo/STATE.md:7-21,24-28`〕

This is a boundary-locked local draft candidate only. Node36 and the human PI
retain final authority. This is not paper-ready, preprint-ready, posted, or
submission-authorized.