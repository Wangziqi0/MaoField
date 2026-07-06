# OI 伴随推论审稿裁决

## 裁决

**最终动作：`DRAFT_ONE_PAGE_OI_COROLLARY_COMPANION`。**
我给出这个结论的理由很窄也很明确：在包内既有的 v1.3 证明链中，命题 2 已经给出“`D_w=0` 当且仅当 `w` 为 product form”，而命题 3 又给出“若 `w` 非 product，则存在一个纯主效应见证 `K∈A` 或 `K∈B0`，它属于 `N_add`，真加性残差为零，但两种有序剥离输出一零一非零”，因此 `D_w K ≠ 0`。这正好足以推出受限算子范数版本
\[
OI^{op}_{N_{\mathrm{add}}}(w)=\|D_w|_{N_{\mathrm{add}}}\|_{L^2(w)\to L^2(w)}
\]
满足
\[
OI^{op}_{N_{\mathrm{add}}}(w)=0 \iff w\ \text{是 product form}.
\]
这里没有把存在性见证偷换成全称命题，也没有把 wrong-order 输出误当成真交互残差；相反，v1.3 命题 3 正是明确把它定性为 sequential stripping artifact。包内当前状态文件、索引文件和 report31 adoption 也都把这一结论仅定位为“可立即整理成 v1.3 的一页 companion corollary”，而不是当前 V2.5 Zenodo 预印本补丁，更不是任何更广泛理论。 （依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:154-227,243-283`; `from_repo/docs/infra/recovery/MAOFIELD_D706_OI_COROLLARY_COMPANION_TASKBOOK_20260706.md:37-71`; `from_repo/STATE.md:16,25-28`; `from_repo/docs/infra/gpt_deep_research/METRIC_IDENTITY_OI_COROLLARY_DECISION_REPORT31_ADOPTION_NOTE_20260706.md:54-81`; `from_repo/docs/infra/debranded_residual_transport/METRIC_OBJECT_IDENTITY_EXACT_NOTES_INDEX_20260706.md:134-152`）

## 清洁定义

在有限正权二维表 \(X=Q\times B\) 上，设 \(w(q,b)>0\) 且 \(\sum_{q,b}w(q,b)=1\)。带权内积定义为
\[
\langle f,g\rangle_w=\sum_{q,b}w(q,b)f(q,b)g(q,b).
\]
令
\[
C=\operatorname{span}\{1\},\qquad
A=\{a(q):\sum_q w_Q(q)a(q)=0\},\qquad
B_0=\{b(b):\sum_b w_B(b)b(b)=0\},
\]
并设
\[
N_{\mathrm{add}}=C\oplus A\oplus B_0.
\]
v1.3 定义了有序剥离算子
\[
R_{Q\to B}=(I-P_{B_0})(I-P_A)(I-P_C),\qquad
R_{B\to Q}=(I-P_A)(I-P_{B_0})(I-P_C),
\]
以及顺序缺陷算子
\[
D_w=R_{Q\to B}-R_{B\to Q}=P_{B_0}P_A-P_AP_{B_0}.
\]
因此，当前候选量的最干净写法应为
\[
OI^{op}_{N_{\mathrm{add}}}(w)
:=
\bigl\|D_w|_{N_{\mathrm{add}}}\bigr\|_{(N_{\mathrm{add}},\|\cdot\|_w)\to L^2(w)}.
\]
我建议把定义写成上面这个版本，只是为了把“定义域是 `N_add` 的受限算子、范数来自 \(L^2(w)\) 的诱导范数、陪域仍是 \(L^2(w)\)”说清楚；这属于编辑性澄清，不构成需要“先补定义再重审”的理论阻塞。这个定义也正与 taskbook 和 report25/report26 中对受限算子型 OI 的包内记号修正一致。 （依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:43-100,156-175`; `from_repo/docs/infra/recovery/MAOFIELD_D706_OI_COROLLARY_COMPANION_TASKBOOK_20260706.md:43-56`; `from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_phaseii_report25_20260705.md:124-147`; `from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_object_atlas_glue_report26_20260705.md:92,100`）

## 定理陈述

**定理。** 设 \(X=Q\times B\) 为有限正权二维表，\(w(q,b)>0\)，\(\sum_{q,b}w(q,b)=1\)。以上述 \(C,A,B_0,N_{\mathrm{add}},R_{Q\to B},R_{B\to Q},D_w\) 为定义，则
\[
OI^{op}_{N_{\mathrm{add}}}(w)=0
\quad\Longleftrightarrow\quad
w(q,b)=w_Q(q)w_B(b)\ \text{对所有 }(q,b)\in Q\times B.
\]
也就是说，**受限算子型 audit-order instability 在且仅在 product 权重情形下为零。** v1.3 已经证明：product 权重当且仅当 \(A\perp B_0\)；进一步当且仅当 \(D_w=0\)，等价地两种 ordered stripping maps 相等。命题 3 又给出非 product 情形下的纯主效应存在性见证。这个 companion corollary 并不发明新对象，只是把已有证明脊柱压成一个严格受限的算子范数结论。 （依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:104-152,177-227,243-283`; `from_repo/docs/infra/recovery/MAOFIELD_D706_OI_COROLLARY_COMPANION_TASKBOOK_20260706.md:39-56`; `from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_oi_corollary_decision_report31_20260706.md:245-301`）

## 证明

先证“若 \(w\) 为 product form，则 \(OI^{op}_{N_{\mathrm{add}}}(w)=0\)”。由 v1.3 命题 2，若 \(w\) 为 product form，则
\[
D_w=0,
\qquad
R_{Q\to B}=R_{B\to Q}=I-P_N.
\]
既然 \(D_w\) 在整个 \(R^{Q\times B}\) 上恒为零，它在子空间 \(N_{\mathrm{add}}\) 上的限制当然也是零映射，因此
\[
\bigl\|D_w|_{N_{\mathrm{add}}}\bigr\|_{(N_{\mathrm{add}},\|\cdot\|_w)\to L^2(w)}=0.
\]
所以
\[
OI^{op}_{N_{\mathrm{add}}}(w)=0.
\]
这一步不需要任何额外假设；v1.3 的 product-weight 结论已经足够。 （依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:177-227`）

再证“若 \(OI^{op}_{N_{\mathrm{add}}}(w)=0\)，则 \(w\) 为 product form”。由算子范数为零的基本事实可知，
\[
OI^{op}_{N_{\mathrm{add}}}(w)=0
\]
等价于
\[
D_wK=0\qquad\text{对所有 }K\in N_{\mathrm{add}}.
\]
现在反设 \(w\) 不是 product form。根据 v1.3 命题 3，存在一个纯主效应见证 \(K\in A\) 或 \(K\in B_0\)。因为 \(N_{\mathrm{add}}=C\oplus A\oplus B_0\)，故这类 \(K\) 自动属于 \(N_{\mathrm{add}}\)。同时命题 3 还给出三件事：其一，\((I-P_N)K=0\)，即它的真加性残差为零；其二，两种有序剥离输出中有一个为零；其三，另一个非零。于是
\[
D_wK
=
R_{Q\to B}K-R_{B\to Q}K
\neq 0.
\]
这与“对所有 \(K\in N_{\mathrm{add}}\) 都有 \(D_wK=0\)”矛盾。因此反设不成立，\(w\) 必为 product form。 （依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:64-71,243-283`）

这里需要特别说明，命题 3 只提供**存在性**见证，而这对反向证明已经完全够用：要证明受限算子不是零映射，只需存在一个 \(K\in N_{\mathrm{add}}\) 使 \(D_wK\neq0\)。因此并没有犯“把存在性见证偷换成全称不稳定”的错误。反过来，v1.3 还专门加了 quantifier guard，强调若 \(D_w\neq0\)，正确结论仅是“存在某个 witness 输入会出现顺序差异”，而不是“所有输入都差异”。本 corollary 的论证与这条 guard 完全一致。 （依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:229-239,243-283`）

还需要再加一层术语防混淆。命题 3 明确指出：在非 product 情形下，上述非零 wrong-order 输出是 **sequential stripping artifact**，**不是**真交互残差，因为真正的正交加性残差已经由 \((I-P_N)K=0\) 表明为零。故本 corollary 衡量的是“从 additive nuisance 成分中，程序顺序最多能制造多大的伪残差”，而不是“真实 interaction 大小”。这正是为什么候选量必须写成受限算子型 OI，而不能把它误说成广义 residual theory。 （依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:245-255,263-283`; `from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_phaseii_report25_20260705.md:126-147`; `from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_oi_corollary_decision_report31_20260706.md:247-299`）

因此，定理得证。并且严格说，corollary 的直接证明只需要 v1.3 命题 2、命题 3 与一个初等算子范数事实；命题 1 的作用则是作为 v1.3 内部证明链的上游支点，保证整条 product-weight spine 在包内是闭合的。 （依据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:106-152,177-227,243-283`）

## 边界

这个 corollary **不**证明任何 MaoField 经验正结果，不证明 full panel、training、inference、checkpoint、new loss、F3 positive、LOSO passed，也不证明任何 observed residual / interaction / transport / holonomy / gluing field。它也**不**把当前有限正权二维表结论扩张成广义 ANOVA、dependent-input、projection、sheaf、contextuality、consistency-radius 或 dynamic-collapse theory。taskbook、STATE、report31 adoption note 和 exact-notes index 都把这些扩张明确列为禁区。 （依据：`from_repo/docs/infra/recovery/MAOFIELD_D706_OI_COROLLARY_COMPANION_TASKBOOK_20260706.md:107-120`; `from_repo/STATE.md:16,26-28`; `from_repo/docs/infra/gpt_deep_research/METRIC_IDENTITY_OI_COROLLARY_DECISION_REPORT31_ADOPTION_NOTE_20260706.md:54-100`; `from_repo/docs/infra/debranded_residual_transport/METRIC_OBJECT_IDENTITY_EXACT_NOTES_INDEX_20260706.md:154-165`）

此外，包里的 v1.4 exact witness、JSON 与脚本只能当作**一致性展示与 exact example**，不能当作 theorem proof authority。v1.4 文件自己就写明它“does not replace the analytic proof”，而 taskbook 也明确禁止“proof by deterministic harness or JSON floats”。所以，这个 companion 的证明文本应只依赖 v1.3 Proposition 1–3 与初等有限维事实；v1.4 最多可在注记中作为一个 2×2 exact rational illustration。 （依据：`from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md:5-7,30-66`; `from_repo/docs/infra/recovery/MAOFIELD_D706_OI_COROLLARY_COMPANION_TASKBOOK_20260706.md:107-118`）

## 发布位置建议

这条结论应当写成**单独的一页 companion corollary**，而**不应**作为当前 Zenodo V2.5 预印本的补丁。包内最新状态、report31 adoption note 和 exact-notes index 都反复把本条目定位为：如果 PI 要继续 exact-math，那么它只是 v1.3 的“下一张、窄边界、一页 companion”；而当前 V2.5 preprint 保持 unpatched，v1.5 GQ-FCR 也必须继续保持 separate exact note。换句话说，最合适的出版动作不是“改写现有主预印本”，而是“在 v1.3 theorem spine 旁边补上一张 bounded corollary companion”。 （依据：`from_repo/STATE.md:16,25-28`; `from_repo/docs/infra/gpt_deep_research/METRIC_IDENTITY_OI_COROLLARY_DECISION_REPORT31_ADOPTION_NOTE_20260706.md:54-81`; `from_repo/docs/infra/debranded_residual_transport/METRIC_OBJECT_IDENTITY_EXACT_NOTES_INDEX_20260706.md:134-152`; `from_repo/docs/infra/recovery/MAOFIELD_D706_OI_COROLLARY_COMPANION_TASKBOOK_20260706.md:20-22,58-71`）

若把它写成实际的一页 companion，建议篇幅和措辞都保持极窄：先重述 v1.3 的有限正权二维表设定与 \(D_w\)；再给出受限定义
\[
OI^{op}_{N_{\mathrm{add}}}(w)
=
\|D_w|_{N_{\mathrm{add}}}\|_{(N_{\mathrm{add}},\|\cdot\|_w)\to L^2(w)};
\]
随后用两段证明完成双向推出；最后加一个边界段，明确它不是广义 instability theory，不是经验发现，也不把 v1.5 GQ-FCR 并入本文。这样写最符合 taskbook 的“make it narrower, not larger”要求，也与 report31 的 `FORMALIZABLE_NOW_AS_COROLLARY_COMPANION` 分类完全一致。 （依据：`from_repo/docs/infra/recovery/MAOFIELD_D706_OI_COROLLARY_COMPANION_TASKBOOK_20260706.md:13-22,37-71`; `from_repo/docs/infra/gpt_deep_research/METRIC_IDENTITY_OI_COROLLARY_DECISION_REPORT31_ADOPTION_NOTE_20260706.md:63-81`; `from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_oi_corollary_decision_report31_20260706.md:245-301`）