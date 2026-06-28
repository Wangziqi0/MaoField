# Formal v1.3 加权 ANOVA 顺序缺陷零上下文证明审计

## 一页结论

本次审计严格把上传 zip 当作唯一主证据包使用，没有把公开 GitHub、搜索引擎、raw 页面或公共 404 页面当作证据；任务边界也明确要求这是一项 **Mode A 有限维数学 proof-audit**，不是 MaoField 经验验证，不允许把结论升级为 full panel、observed field、training/new loss、glass-box、F3/LOSO，或 completed formal system。包内 README、当前状态文件、任务 prompt、以及 node36 的 adoption note 对这一点是一致的。`formal_v1_3_weighted_anova_order_defect_plan_accepted_with_guards` 目前只是被接受的“下一步定理目标”，不是已证明定理，更不是已完成系统。 （证据包：`00-README_FOR_19_AND_PRO.md` 第26-40、42-55、79-83行；`00-CURRENT_STATUS_FOR_PRO.md` 第22-27、46-57、71-91行；`prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md` 第12-33、52-72、159-182行；`from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_3_THEOREM_STRENGTHENING_PLAN_ADOPTION_NOTE_20260628.md` 第23-40、45-91行）

就数学内容本身而言，我的结论是：**该 v1.3 顺序缺陷 theorem package 可以接受，但需要把若干地方写得更严一些；这些修正属于证明与表述收紧，不构成“重开 v1.2 边界”也不构成“定义层退回”。** 更具体地说，T1 为真；T2 也为真，但要明确“算子不等”只推出“存在见证输入”，不能写成“每个输入都会不同”；T3 也为真，而且现有 v1.2 的 `2 x 2` 非乘积权例子已经足够给出最小见证。v1.2 自己只把非乘积情形留在 boundary example 上，因此把它升级成严格 iff/no-go 定理，正是这个包已经指定的最小下一步。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md` 第149-205、278-320、322-347行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第25-158行；`from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_3_theorem_strengthening_plan_20260628.md` 第7-11、25-97、98-106行）

最关键的数学判定如下。第一，**乘积权当且仅当** 零均值 `q-only` 子空间 `A` 与零均值 `b-only` 子空间 `B0` 在加权内积下正交。第二，**顺序缺陷算子**
\[
D_w=R_{Q\to B}-R_{B\to Q}
\]
确实满足
\[
D_w=0 \iff w \text{ 为乘积权},
\qquad
R_{Q\to B}=R_{B\to Q} \iff w \text{ 为乘积权}.
\]
第三，若 \(w\) 不是乘积权，则一定存在纯主效应 \(K\in A\) 或 \(K\in B_0\)，使得真正的正交加性残差 \((I-P_N)K\) 为零，但一个顺序的 sequential stripping 给出零，另一个顺序却给出非零输出；这个非零输出只能称为 **sequential stripping artifact** 或 **interaction-like artifact**，不能升级为“真交互残差”。这些结论正好把 v1.2 已明确保留的 non-product boundary，升级成一个严格的算子级 no-go 包。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md` 第181-205行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第71-158行；`prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md` 第74-157行；`from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_3_THEOREM_STRENGTHENING_PLAN_ADOPTION_NOTE_20260628.md` 第25-40、82-89行）

最终分类我选择且只选择：

```text
v1_3_order_defect_proof_plan_accepted
```

理由是：定理目标本身正确，最小 `2 x 2` 见证存在，当前 bundle 已有足够的本地定义、边界说明、脚本先例与 synthetic provenance；需要的只是把工作计划中的“建议证明”写成严格证明，并把 harness 收紧为三个确定性的 zero-GPU theorem controls，而不是回退至 `requires_v1_3_definition_revision` 或更弱结论。 （证据包：`00-CURRENT_STATUS_FOR_PRO.md` 第28-45行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第69-158行；`from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_3_THEOREM_STRENGTHENING_PLAN_ADOPTION_NOTE_20260628.md` 第13-21、82-89行）

## 定义与记号审计

工作计划给出的有限维设定是可用的：\(Q,B\) 有限，\(X=Q\times B\)，\(w(q,b)>0\) 且总质量为 1；定义加权内积、边际权重、常数子空间 \(C\)、零均值 `q-only` 子空间 \(A\)、零均值 `b-only` 子空间 \(B_0\)，再令 \(N_{\mathrm{add}}=C\oplus A\oplus B_0\)。这与 v1.2 里 product-weight Hoeffding 命题的同一加权 Hilbert 框架完全兼容，只是 v1.3 不再预先假设 \(w\) 已经是乘积权。工作计划还明确用 `B0` 避免与底层集合 `B` 混淆，这个记号选择是正确的。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第36-67行；`prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md` 第74-105行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md` 第149-205行）

这里有两个必须写清的定义细节。其一，`direct-sum` 在此处应理解为**代数直和**，不是先验的正交直和。确实，\(C\perp A\) 与 \(C\perp B_0\) 总成立，因为 \(A,B_0\) 都是零均值子空间；而 \(A\cap B_0=\{0\}\) 也成立，因为若一个函数既只依赖 \(q\) 又只依赖 \(b\)，它只能是常数，而零均值迫使该常数为零。但 \(A\) 与 \(B_0\) 是否正交，恰恰就是 T1 要判定的核心问题，所以在非乘积权下不能把 \(N_{\mathrm{add}}\) 偷写成正交分解。v1.2 已明确警告：非乘积权下，product-weight 的那种正交结构“不一定成立”。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第54-67、71-137行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md` 第189-205行）

其二，投影符号要从一开始就区分：\(P_C,P_A,P_{B_0}\) 是对各个子空间的**加权正交投影**，而 \(P_N\) 是对整个 \(N_{\mathrm{add}}\) 的加权正交投影。一般情形下不能直接写
\[
P_N=P_C+P_A+P_{B_0},
\]
因为这个公式只在 \(C,A,B_0\) 两两正交时成立，也就是 product-form 情形。若不强调这一点，T2 和 T3 会被写坏。正确的“总残差”一直应是 \(I-P_N\)；而两个 sequential stripping 算子
\[
R_{Q\to B}=(I-P_{B_0})(I-P_A)(I-P_C),\qquad
R_{B\to Q}=(I-P_A)(I-P_{B_0})(I-P_C)
\]
只是一般情形下的两个**有序剥离**过程，它们本身不等于 \(I-P_N\) 除非乘积结构成立。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第93-121、139-158行；`prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md` 第91-157行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md` 第181-205行）

从这些定义可以直接推出一组在证明里会用到的显式公式。对任意 \(f\in\mathbb R^{Q\times B}\)，令 \(\mu_f=\sum_{q,b}w(q,b)f(q,b)\)。则
\[
P_Cf=\mu_f\mathbf 1.
\]
再记
\[
E_w[f\mid q]=\frac{\sum_b w(q,b)f(q,b)}{w_Q(q)},\qquad
E_w[f\mid b]=\frac{\sum_q w(q,b)f(q,b)}{w_B(b)}.
\]
因为 \(w(q,b)>0\)，所以 \(w_Q(q),w_B(b)>0\)，这些条件均值都定义良好。于是
\[
P_Af=E_w[f\mid q]-\mu_f,\qquad
P_{B_0}f=E_w[f\mid b]-\mu_f,
\]
其中右边分别视作只依赖 \(q\) 或只依赖 \(b\) 的函数。这些公式虽然是本审计根据给定设定直接推出的，但它们与 v1.2 在 product-weight 情形使用条件均值与主效应投影的写法完全一致。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第36-67、95-107行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md` 第172-200行）

## T1 证明审计

T1 结论是正确的，而且 centered indicator 证明可以严格成立。正向方向最简单：若
\[
w(q,b)=w_Q(q)w_B(b)\quad\forall (q,b),
\]
则对任意 \(a\in A\)、\(b\in B_0\)，有
\[
\langle a,b\rangle_w
=\sum_{q,b}w_Q(q)w_B(b)a(q)b(b)
=\Big(\sum_q w_Q(q)a(q)\Big)\Big(\sum_b w_B(b)b(b)\Big)=0.
\]
因此 \(A\perp B_0\)。这正是 v1.2 product-weight Hoeffding 命题中已经使用过的关键正向计算。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md` 第181-200行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第71-91行）

反向方向是 v1.3 真正补上的部分。固定任意 \(q_0\in Q\)、\(b_0\in B\)，定义
\[
a_{q_0}(q)=\mathbf 1_{\{q=q_0\}}-w_Q(q_0),\qquad
b_{b_0}(b)=\mathbf 1_{\{b=b_0\}}-w_B(b_0).
\]
先检查归属：因为 \(\sum_q w_Q(q)=1\)，所以
\[
\sum_q w_Q(q)a_{q_0}(q)=w_Q(q_0)-w_Q(q_0)\sum_q w_Q(q)=0,
\]
同理 \(\sum_b w_B(b)b_{b_0}(b)=0\)，因此 \(a_{q_0}\in A\)、\(b_{b_0}\in B_0\)。若假设 \(A\perp B_0\)，那么
\[
0=\langle a_{q_0},b_{b_0}\rangle_w.
\]
而直接展开可得
\[
\langle a_{q_0},b_{b_0}\rangle_w
=\sum_{q,b}w(q,b)(\mathbf 1_{q=q_0}-w_Q(q_0))(\mathbf 1_{b=b_0}-w_B(b_0))
= w(q_0,b_0)-w_Q(q_0)w_B(b_0).
\]
于是每个单元格都满足
\[
w(q_0,b_0)=w_Q(q_0)w_B(b_0).
\]
因为 \(q_0,b_0\) 任意，故 \(w\) 必为乘积权。证明闭合。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第71-91行；`prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md` 第110-127行）

这一证明里有三个边角问题也都没出错。第一，严格正权 \(w(q,b)>0\) 自动推出 \(w_Q(q)>0\) 与 \(w_B(b)>0\)，所以后续投影与条件均值里不会出现除零。第二，若 \(|Q|=1\) 或 \(|B|=1\)，则 \(A=\{0\}\) 或 \(B_0=\{0\}\)；此时“正交”是平凡真的，而任何这种单行或单列正权表也确实自动等于其边际乘积，所以 T1 仍然成立。第三，记号上必须持续使用 `B0` 代表 `b-only` 零均值子空间，否则会和底层索引集合 `B` 冲突。也就是说，T1 不需要修 theorem 内容，只需要把“代数直和”和“`B0` 记号”写得更明确。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第54-67、71-91行；`prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md` 第74-127行）

## T2 证明审计

T2 作为 iff 判据也是正确的，不需要改成更弱的说法；真正需要修的是**陈述的锋利度**。首先，工作计划中的代数化简是安全的：
\[
R_{Q\to B}-(R_{B\to Q})
=(I-P_{B_0})(I-P_A)(I-P_C)-(I-P_A)(I-P_{B_0})(I-P_C)
=(P_{B_0}P_A-P_AP_{B_0})(I-P_C).
\]
再因为 \(P_A1=P_{B_0}1=0\)，所以
\[
(P_{B_0}P_A-P_AP_{B_0})P_C=0,
\]
从而作为整个空间上的算子，确实可以简写为
\[
D_w=P_{B_0}P_A-P_AP_{B_0}.
\]
因此工作计划第一个化简没有数学错误。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第93-121行；`prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md` 第91-141行）

然后证明 iff。若 \(w\) 为乘积权，则由 T1 知 \(A\perp B_0\)。于是 \(P_A\) 在 \(B_0\) 上为零，\(P_{B_0}\) 在 \(A\) 上也为零，所以
\[
P_{B_0}P_A=P_AP_{B_0}=0,
\qquad D_w=0.
\]
这时 \(C,A,B_0\) 是两两正交的，因此
\[
P_N=P_C+P_A+P_{B_0},
\]
并且
\[
R_{Q\to B}=R_{B\to Q}=I-P_C-P_A-P_{B_0}=I-P_N.
\]
所以 product-form 一定推出 T2 中的两个等价式，而且还推出更强的
\[
R_{Q\to B}=R_{B\to Q}=I-P_N.
\]
这与 v1.2 在 product-weight 下的正向 Hoeffding 命题完全一致。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md` 第181-205行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第93-121、139-158行）

反向方向也成立。假设 \(D_w=0\)。取任意 \(b\in B_0\)。因为 \(P_{B_0}b=b\)，所以
\[
0=D_w b=P_{B_0}P_A b-P_A b.
\]
这说明 \(P_A b=P_{B_0}P_A b\in B_0\)。但同时 \(P_A b\in A\)，于是
\[
P_A b\in A\cap B_0=\{0\},
\]
故 \(P_A b=0\) 对一切 \(b\in B_0\) 成立。现在再取任意 \(a\in A\)、\(b\in B_0\)，就有
\[
\langle a,b\rangle_w=\langle a,P_A b\rangle_w=0.
\]
因此 \(A\perp B_0\)，由 T1 立刻推出 \(w\) 必是乘积权。于是
\[
D_w=0\iff w \text{ 为乘积权}.
\]
而
\[
R_{Q\to B}=R_{B\to Q}\iff D_w=0,
\]
故第二个 iff 也同时成立。工作计划里对此的直觉是对的。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第110-121行；`prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md` 第129-141行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md` 第202-205行）

真正需要 sharpen 的地方，是量词而不是定理真假。若 \(D_w\neq 0\)，结论只能是：**存在** 某个输入 \(f\) 使 \(R_{Q\to B}f\neq R_{B\to Q}f\)。不能写成“所有输入都不同”。事实上，常数子空间 \(C\) 全部在核里，因为两个算子前面都有 \((I-P_C)\)；而且任意真正的正交加性残差 \(r\in N_{\mathrm{add}}^\perp\) 也满足 \(P_Cr=P_Ar=P_{B_0}r=0\)，所以两种顺序都返回同一个 \(r\)。因此，在非乘积情形下，“算子不相等”与“存在见证输入”是正确说法；“每个输入都不相等”是错误升级。工作计划已经提醒这一点，我同意保留这个保护栏。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第116-121、133-137行；`prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md` 第138-157行）

## T3 证明审计与最小见证

T3 也是正确的，而且可以用一个很短的抽象证明完成。设 \(w\) 不是乘积权。由 T1 的逆否命题，\(A\) 与 \(B_0\) 不正交。于是存在 \(b\in B_0\) 使 \(P_A b\neq 0\)；否则若对所有 \(b\in B_0\) 都有 \(P_A b=0\)，则对任意 \(a\in A\)、\(b\in B_0\) 都有
\[
\langle a,b\rangle_w=\langle a,P_A b\rangle_w=0,
\]
这会强迫 \(A\perp B_0\)，与非乘积权矛盾。现在取这样一个 \(K\in B_0\)。因为 \(K\in N_{\mathrm{add}}\)，所以真正的正交加性残差是
\[
(I-P_N)K=0.
\]
又因为 \(K\in B_0\) 且 \(P_CK=0\)，有
\[
R_{B\to Q}K=(I-P_A)(I-P_{B_0})(I-P_C)K=0.
\]
另一方面，
\[
R_{Q\to B}K=(I-P_{B_0})(I-P_A)K=-(I-P_{B_0})P_AK.
\]
若这也等于 0，则 \(P_AK=P_{B_0}P_AK\in B_0\)。但 \(P_AK\in A\)，故 \(P_AK\in A\cap B_0=\{0\}\)，这与 \(P_AK\neq 0\) 矛盾。于是
\[
R_{Q\to B}K\neq 0.
\]
所以 T3 建议的 no-go 命题成立；对称地，也可以从 \(A\) 中找见证，让相反顺序出错。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第122-137行；`prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md` 第143-157行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md` 第202-205行）

最小数值见证可以直接采用工作计划指定、v1.2 harness 已经使用过的 `2 x 2` 非乘积权原始权重 \((1,2,3,5)\)。把它归一化后得到
\[
w=\frac1{11}
\begin{pmatrix}
1 & 2\\
3 & 5
\end{pmatrix},
\qquad
w_Q=\Big(\frac3{11},\frac8{11}\Big),
\qquad
w_B=\Big(\frac4{11},\frac7{11}\Big).
\]
对应的乘积边际表是
\[
w_Q\otimes w_B=\frac1{121}
\begin{pmatrix}
12 & 21\\
32 & 56
\end{pmatrix},
\]
所以单元偏差矩阵为
\[
w-w_Q\otimes w_B=
\frac1{121}
\begin{pmatrix}
-1 & 1\\
1 & -1
\end{pmatrix}\neq 0.
\]
这说明它确实是非乘积权，而且正是 v1.2 `product_reweighting_separation` 使用的边界例。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第133-137行；`from_repo/scripts/debranded_residual_transport_harness_v1_2.py` 第362-381行；`from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json` 第106-128行）

在这个权重下，取纯 `b-only` 零均值主效应
\[
K(b)=\mathbf 1_{\{b=1\}}-\frac4{11},
\]
按单元顺序 \((q_1,b_1),(q_1,b_2),(q_2,b_1),(q_2,b_2)\) 写成向量即
\[
K=\Big(\frac7{11},-\frac4{11},\frac7{11},-\frac4{11}\Big).
\]
这是一个 \(K\in B_0\) 的纯主效应，所以
\[
(I-P_N)K=0.
\]
接着按上节投影公式直接计算：
\[
P_AK=\Big(-\frac1{33},-\frac1{33},\frac1{88},\frac1{88}\Big),
\]
于是
\[
(I-P_A)K=\Big(\frac23,-\frac13,\frac58,-\frac38\Big).
\]
再按列做 \(B_0\)-投影，得到
\[
R_{Q\to B}K=
\Big(\frac1{32},\frac5{168},-\frac1{96},-\frac1{84}\Big)\neq 0,
\]
而
\[
R_{B\to Q}K=0.
\]
因此，这个非零输出就是一个由错误顺序制造出来的 **sequential stripping artifact**。它不是“真交互残差”，因为真正的正交加性残差明明已经是零。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第122-137、160-170行；`prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md` 第143-157行；见证权重来源同上，本段其余等式为依定义直接计算）

如果需要一个对称见证，也可以取纯 `q-only` 零均值主效应
\[
K'=\Big(\frac8{11},\frac8{11},-\frac3{11},-\frac3{11}\Big)\in A.
\]
这时
\[
R_{Q\to B}K'=0,
\qquad
R_{B\to Q}K'=
\Big(\frac{11}{42},-\frac{11}{84},\frac{55}{224},-\frac{33}{224}\Big)\neq 0.
\]
因此 T3 并不是偶然依赖单一方向；非乘积权会在两个主效应方向上都制造顺序伪象。最小 harness 只需保留其中一个见证即可。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第124-137、141-158行；见证权重来源：`from_repo/scripts/debranded_residual_transport_harness_v1_2.py` 第362-381行；本段等式为依定义直接计算）

## 最小 harness 含义与精确门槛

v1.2 harness 已经建立了一个“single-source threshold contract + central evaluator”的风格：阈值由 `build_threshold_contract()` 集中生成，pass/fail 只由 `evaluate_test()` 赋值，JSON 回写并核对 threshold contract hash。这种做法是可继承的；但 v1.3 不应新增 full panel、训练、推理或 MaoField 数据，只应新增最小、确定性、zero-GPU 的 theorem controls。v1.2 文档、JSON 和脚本都写得非常清楚：当前 synthetic harness 只能支持 formal design review，不是经验升级。 （证据包：`from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md` 第30-43、44-63、86-110行；`from_repo/scripts/debranded_residual_transport_harness_v1_2.py` 第72-130、682-829行；`from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json` 第1-39、40-104、317-338行）

我建议的最小 v1.3 harness 只有三个 block，而且都不需要随机向量。因为要验证的是有限维算子恒等式，**标准基**已经足够。下面给出精确的 pass/fail quantities。

第一块可以保留工作计划名 `product_weight_order_independence_control`。用 v1.2 里已有的精确乘积表：
\[
q=\Big(\frac27,\frac57\Big),\qquad
b=\Big(\frac3{14},\frac2{7},\frac12\Big),
\qquad
w=q\otimes b.
\]
这正对应脚本里 `exact_product_weight_equality_control` 的 `2 x 3` 例子。该块应检查四件事：  
\[
\max_{q,b}|w(q,b)-w_Q(q)w_B(b)|\le 10^{-12},
\]
\[
\|D_w\|_F\le 10^{-12},
\]
\[
\max_i \|(R_{Q\to B}-R_{B\to Q})e_i\|_w\le 10^{-12},
\]
\[
\max_i \|(R_{Q\to B}-(I-P_N))e_i\|_w\le 10^{-12},
\quad
\max_i \|(R_{B\to Q}-(I-P_N))e_i\|_w\le 10^{-12},
\]
其中 \(e_i\) 为标准基。既然空间维数有限，这样比“basis/random test vectors”更小也更充分。 （证据包：`from_repo/scripts/debranded_residual_transport_harness_v1_2.py` 第343-359行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第139-158行；`from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json` 第89-104行）

第二块可以保留工作计划名 `centered_indicator_product_iff_control`。它应该同时在一个 product 表和一个 non-product 表上跑。对每个单元格都计算
\[
\varepsilon_{q,b}
=
\langle a_q,b_b\rangle_w-
\big(w(q,b)-w_Q(q)w_B(b)\big),
\]
要求
\[
\max_{q,b}|\varepsilon_{q,b}|\le 10^{-12}.
\]
然后在 product 例上再要求
\[
\max_{q,b}|w(q,b)-w_Q(q)w_B(b)|\le 10^{-12},
\]
而在 non-product `2 x 2` 例
\[
w=\frac1{11}\begin{pmatrix}1&2\\3&5\end{pmatrix}
\]
上，要求得到精确偏差矩阵
\[
\frac1{121}
\begin{pmatrix}
-1&1\\
1&-1
\end{pmatrix}
\]
的坐标值，数值容差仍取 \(10^{-12}\)。这样才能把“indicator identity 正确”与“product/non-product 分类正确”严格绑在一起。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第71-91、149-152行；`prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md` 第110-127行；`from_repo/scripts/debranded_residual_transport_harness_v1_2.py` 第362-381行）

第三块可以命名为 `nonproduct_pure_main_effect_no_go_control`，也是真正最重要的一块。仍然用非乘积 `2 x 2` 见证权重 \((1,2,3,5)/11\)，以及纯 `b-only` 见证
\[
K=\Big(\frac7{11},-\frac4{11},\frac7{11},-\frac4{11}\Big).
\]
该块应要求：
\[
\|(I-P_N)K\|_w\le 10^{-12},
\qquad
\|R_{B\to Q}K\|_w\le 10^{-12},
\]
并且坐标级检查
\[
\left\|
R_{Q\to B}K-
\Big(\frac1{32},\frac5{168},-\frac1{96},-\frac1{84}\Big)
\right\|_\infty
\le 10^{-12}.
\]
若更想保留一个“明显非零”的单指标，也可同时记录
\[
\|R_{Q\to B}K\|_w^2=\frac{61}{177408}\approx 0.00034384,
\]
因此
\[
\|R_{Q\to B}K\|_w\approx 0.0185429282>10^{-6}.
\]
但既然坐标向量已经是确定的，最小 harness 其实不需要这条附加门槛。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第122-158行；`prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md` 第143-157行；见证来源：`from_repo/scripts/debranded_residual_transport_harness_v1_2.py` 第362-381行；本段等式为依定义直接计算）

我的建议是不新增第四块。因为一旦这三块都过，T1 的等价、T2 的算子 iff、T3 的 no-go witness 就已经被最小而充分地覆盖了；再加随机测试只会扩大 harness，而不会提高 theorem-level 可信度。v1.2 之所以有随机块，是因为 Beta 定律本来就是概率命题；v1.3 这里不是那种情况。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md` 第110-147、278-320行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第139-158行）

## 必须继续禁止的表述

本包的最重要边界之一，就是即便 T1、T2、T3 都成立，也**绝不能**把它们写成 MaoField 经验发现，更不能把它们写成训练或系统层结论。README、当前状态、prompt、adoption note、v1.2 formal note、v1.2 harness 文档与 JSON，全部都把这一点锁死了。 （证据包：`00-README_FOR_19_AND_PRO.md` 第42-77行；`00-CURRENT_STATUS_FOR_PRO.md` 第46-57、71-91行；`prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md` 第52-72、181-182行；`from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_3_THEOREM_STRENGTHENING_PLAN_ADOPTION_NOTE_20260628.md` 第45-91行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md` 第322-347行；`from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md` 第86-110行）

因此，下面这些表述必须继续列入 kill list，而且一个都不能偷偷升级。不能说：full panel has run；16-cell aggregate exists；MaoField residual / interaction / quotient-residual / transport / holonomy field has been observed；glass box broken；LOSO passed；F3 positive；training authorized；new loss authorized；Formal v1.3 completed；completed formal system；theorem stack complete。就 v1.3 本题而言，还必须额外禁止一句：**在非乘积权下把顺序伪象称作 product-measure Hoeffding interaction 或 true interaction residual。** 正确用语只能是 `sequential stripping artifact` 或 `interaction-like artifact`。 （证据包：`00-README_FOR_19_AND_PRO.md` 第42-55行；`00-CURRENT_STATUS_FOR_PRO.md` 第71-91行；`prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md` 第61-72、154-157行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第133-170行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md` 第202-205、322-337行）

还要再补一条文字边界：即使 T2 证明了“顺序无关 iff product-form”，也不能把它说成“所有非乘积权输入都会产生伪残差”。正确说法只有：“非乘积权意味着两个 ordered stripping 算子不相等，因此存在见证输入；常数信号与真正的 \(N_{\mathrm{add}}^\perp\) 残差信号仍然会给出相同输出。” 这条边界并不弱，反而更数学、更准确。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第116-121行；`prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md` 第138-141行）

## 初中生解释

可以把这件事想成“你有一张表，行是一种分类，列是另一种分类；你想把‘行的影响’和‘列的影响’从数据里剥掉，看最后还剩什么”。如果这张表的权重很规整，正好就是“行权重 × 列权重”的乘积，那么先减行、再减列，和先减列、再减行，最后结果一样。这个就是 product-form 的好处。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md` 第149-205行；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第36-121行）

但如果权重不是那种规整乘积，而是像
\[
\frac1{11}\begin{pmatrix}1&2\\3&5\end{pmatrix}
\]
这样歪掉了，那么“先减哪一种影响”就会影响结果。更糟的是，本来只是“纯行影响”或“纯列影响”的东西，也可能被错误顺序算成“好像还有别的复杂剩余”。这个“好像多出来的剩余”不一定是真的结构，很可能只是顺序造成的假象。 （证据包：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_WORKPLAN_20260628.md` 第122-158行；`from_repo/scripts/debranded_residual_transport_harness_v1_2.py` 第362-381行；`from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json` 第106-128行）

所以这次 v1.3 要证明的，其实就是一句很朴素的话：**只有在权重真正能拆成“行 × 列”的时候，去主效应这件事才不看顺序；一旦权重不是乘积，顺序本身就会制造假象。** 这是一条有限维数学边界，不是 MaoField 已经观察到什么东西，更不是训练许可。 （证据包：`00-CURRENT_STATUS_FOR_PRO.md` 第36-45、46-57行；`from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_3_THEOREM_STRENGTHENING_PLAN_ADOPTION_NOTE_20260628.md` 第25-40、45-91行；`prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_3_ORDER_DEFECT_PROOF_PROMPT_20260628.md` 第29-33、61-72行）