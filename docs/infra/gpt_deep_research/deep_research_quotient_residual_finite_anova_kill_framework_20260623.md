# 商残差母对象、有限加权 ANOVA 与 MaoField 零GPU击杀框架研究报告

## 证据边界与仓库现状

本报告只依据本轮上传 bundle 中的仓库快照文本与脚本，不把任何 public GitHub 页面、搜索摘要或外部网页当作私有仓库事实证据。先把边界钉死：仓库当前采纳的底层对象层级已经从具体的 q4 残差或 16-cell 交互场，收缩为更一般的母对象
\[
R_t=\Pi_{\mathcal N^\perp,w}K_t,
\]
其中 weighted interaction、ANOVA、rank、coarsening/refinement、commutator、gluing obstruction 都只是派生结构，不是已经建立的阳性发现。与此同步，Mode B 的当前仓库裁定没有变化：稳定非标量结构仍然只是 `insufficient_artifact`，现有 interaction smoke 仍然只是 `smoke_conjecture_only`；没有 full panel、没有训练授权、没有 new loss 授权，也没有任何 “glass box broken” 的合法措辞。（STATE.md:L16-L27；GPT55_PRO_RESEARCH_INDEX_20260622.md:L88-L95；MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md:L30-L60）

这条边界不是口头谨慎，而是已经被未来分析脚本与设计文档写进 fail-closed 机制。`HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md` 明确说，它只是 zero-GPU preregistration design，不运行 checkpoint，不生成 full panel，不训练，也不建立 scientific result；允许 verdict 只有 `invalid_artifact`、`killed_by_noise_floor`、`killed_by_random_axis`、`killed_by_rank1_shadow`、`killed_by_coarsening`、`insufficient_artifact`、`eligible_for_next_design_review_only`，而 `interaction_field_observed`、`residual_field_observed`、`LOSO_passed`、`F3_positive`、`glass_box_broken`、`training_authorized`、`new_loss_authorized` 都被列为 forbidden verdict。与之吻合的 `q4_hypercube_interaction_prereg_analysis.py` 只接受 provenance-checked 的未来 full-panel aggregate，最强可能输出也只是 `eligible_for_next_design_review_only`。（HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md:L7-L10, L77-L145；q4_hypercube_interaction_prereg_analysis.py:L1-L8, L25-L40, L291-L307, L415-L420）

当前 concretization 也必须说死。仓库当前的具体载体是
\[
X=Q_{\mathrm{freq4}}\times B_{\mathrm{tokenpos4}},
\]
其中 token-position 轴采用 outcome-independent 的固定分箱规则
\[
\mathrm{position\_bin}=\min\!\left(3,\left\lfloor \frac{4(\mathrm{token\_pos}-1)}{63}\right\rfloor\right),
\]
并要求 `w` 是 source-only cell weights、在 outcome analysis 之前固定。对这一 \(4\times 4\) 载体，strict additive nuisance 空间维数是 \(7\)，对应残差补空间维数是 \(9\)。这件事很重要，因为后面所有“对象”都必须落在一个先验固定的有限维 Hilbert 空间里，而不是事后挑出来的 dashboard 剩余项。（HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md:L18-L35；hypercube_schema_q4_tokenpos4_20260623.json:L157-L200；build_hypercube_schema_20260623.py:L223-L250）

## 商残差母对象与可容许三元组

先给严格定义，而不是先讲故事。设
\[
X=\prod_{j=1}^d A_j
\]
是预注册的有限乘积空间，\(w:X\to (0,\infty)\) 为正权重且 \(\sum_{x\in X}w(x)=1\)。定义加权 Hilbert 空间
\[
H_w=\mathbb R^X,\qquad 
\langle f,g\rangle_w=\sum_{x\in X}w(x)f(x)g(x).
\]
一个**可容许三元组**
\[
(X,w,\mathcal N)
\]
应满足三条硬条件。第一，\(X\) 的轴、cell、coarsening 关系都在看结果之前固定。第二，\(w\) 是 outcome-independent 的正权重；它可以来自 source-only counts 或其他预注册规则，但不允许从 \(K_t\) 反推。第三，\(\mathcal N\subset H_w\) 是 pre-outcome nuisance 子空间，只能由常数项、主效应、预注册 slope、预注册 smooth-trend、matched mean/slope 模板、预注册 baseline 模板等组成，不能把由 \(K_t\) 自身“看出来”的方向塞回 nuisance。否则，所谓 residual 只是事后拟合的剩余，不是对象。（deep_research_mode_a_quotient_residual_kill_framework_20260623.md:L15-L21, L31-L36, L68-L84；MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md:L30-L52）

在这个定义下，**商残差恒等式**是整个问题的核心：
\[
R_t=\Pi_{\mathcal N^\perp,w}K_t
      =K_t-\Pi_{\mathcal N,w}K_t.
\]
这不是装饰性记号，而是一个严格的最小距离命题。因为 \(H_w\) 有限维，\(\mathcal N\) 闭，故每个 \(K_t\) 唯一分解为
\[
K_t=n_t+R_t,\qquad n_t\in \mathcal N,\quad R_t\in \mathcal N^\perp.
\]
并且 \(R_t\) 是唯一解于
\[
\min_{n\in\mathcal N}\|K_t-n\|_w.
\]
因此，\(R_t\) 恰好是商类 \([K_t]\in H_w/\mathcal N\) 的最小范数代表元；商范数满足
\[
\|[K_t]\|_{H_w/\mathcal N}=\|R_t\|_w.
\]
这一点把“残差”从随手减背景，提升为一个严格的 quotient object。也正因为如此，母对象应当写成 \(R_t\)，而不是更狭窄的 \(I_t\)。（MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md:L30-L47；deep_research_mode_a_quotient_residual_kill_framework_20260623.md:L31-L36, L66-L84）

坐标不变性也必须给出硬条件。设 \(\phi:X\to X\) 是一个预注册双射，定义
\[
(U_\phi f)(x)=f(\phi^{-1}x).
\]
若 \(\phi\) 保持权重，即 \(w(\phi x)=w(x)\)，并且保持 nuisance 结构，即 \(U_\phi\mathcal N=\mathcal N\)，则 \(U_\phi\) 是 \(H_w\) 上的加权酉算子，且
\[
U_\phi \Pi_{\mathcal N^\perp,w}
=
\Pi_{\mathcal N^\perp,w}U_\phi.
\]
因此
\[
U_\phi R_t
=
\Pi_{\mathcal N^\perp,w}(U_\phi K_t),
\]
\(\|R_t\|_w\)、堆叠残差后的奇异值谱、主子空间夹角等都在这类坐标变换下不变。反过来说，若一个“对象”只在某个后验轴命名、某个后验分箱或某个后验选出来的子空间下成立，而在这些可接受的加权等距变化下不协变，那么它没有对象同一性，只是坐标依赖的剩余项。这正是仓库 insist on random-axis / same-dimension-subspace / coarsening checks 的数学原因。（GPT55_PRO_QUOTIENT_RESIDUAL_NEXT_PROMPT_20260623.md:L58-L99, L120-L145；MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md:L44-L52）

给一个当前载体上的严格例子。取 \(X=Q_{\mathrm{freq4}}\times B_{\mathrm{tokenpos4}}\)，\(w\) 为 schema 中锁定的 source-only 16-cell 权重，\(\mathcal N=\mathcal A\) 为 strict additive nuisance，则
\[
\mathcal A=\{\mu+\alpha(q)+\beta(b)\},
\qquad
R_t=\Pi_{\mathcal A^\perp,w}K_t=:I_t.
\]
这是可容许三元组的一个特例，不是母对象本身。要是未来把 q4 slope、generation smooth trend、matched templates 也纳入 nuisance，那么 \(I_t\) 立刻变成较大母对象 \(R_t\) 的一个次级投影，而不再是问题终点。（HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md:L18-L35；MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md:L37-L43）

## 严格加性特例与加权超立方 ANOVA

现在进入严格加性特例。对 \(X=Q\times B\)，定义
\[
\mathcal A=\{\mu+\alpha(q)+\beta(b)\}.
\]
则任意 \(K\in H_w\) 唯一分解为
\[
K(q,b)=\mu+A(q)+B(b)+I(q,b),\qquad I\in\mathcal A^\perp.
\]
若 \(w\) 只是任意正 cell weights，这个分解的存在唯一性仍然成立，因为它只是有限维加权最小二乘投影。于是
\[
I=\Pi_{\mathcal A^\perp,w}K,\qquad
I=0 \iff K\in \mathcal A.
\]
这就是最严格的“可加—交互”判别：交互项不是叙事标签，而是一个正交投影后的剩余。当前仓库所说的 16-cell interaction residual，本质上正是这个对象。（deep_research_mode_a_quotient_residual_kill_framework_20260623.md:L23-L29, L88-L93；HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md:L18-L35）

若进一步假设权重分解为产品形式
\[
w(q,b)=w_Q(q)\,w_B(b),
\]
则有更干净的显式公式：
\[
\mu=\sum_{q,b}w_Q(q)w_B(b)K(q,b),
\]
\[
A(q)=\sum_b w_B(b)K(q,b)-\mu,
\qquad
B(b)=\sum_q w_Q(q)K(q,b)-\mu,
\]
\[
I(q,b)=K(q,b)-\mu-A(q)-B(b).
\]
并带有标准零均值约束
\[
\sum_q w_Q(q)A(q)=0,\qquad
\sum_b w_B(b)B(b)=0,
\]
\[
\sum_q w_Q(q)I(q,b)=0,\qquad
\sum_b w_B(b)I(q,b)=0.
\]
这里 \(I\) 才是真正的二阶交互项。若权重不是产品型，唯一分解仍存在，但 \(A,B\) 不能再被简单写成边际均值；那时应老实地把它称为“加权正交投影分解”，而不要偷换成 canonical Hoeffding marginals。

把这一点推广到有限超立方。设
\[
X=\prod_{j=1}^d A_j,\qquad w(x)=\prod_{j=1}^d w_j(x_j)
\]
是**产品权重**。对任意坐标子集 \(S\subseteq[d]\)，定义加权条件期望算子
\[
(E_S f)(x_S)
=
\sum_{x_{S^c}}
\Bigl(\prod_{j\notin S}w_j(x_j)\Bigr)f(x_S,x_{S^c}),
\]
并定义 Hoeffding 分量
\[
f_S
=
\sum_{T\subseteq S}(-1)^{|S|-|T|}E_T f.
\]
则有严格正交分解
\[
f=\sum_{S\subseteq[d]} f_S,
\qquad
\langle f_S,f_T\rangle_w=0\quad(S\neq T).
\]
每个 \(f_S\) 只依赖于 \(x_S\)，并且在 \(S\) 中任一坐标方向上都满足加权零边际：
\[
\sum_{a_j\in A_j} w_j(a_j) f_S(x_S)=0,\qquad j\in S.
\]
于是 \(|S|=0\) 给常数项，\(|S|=1\) 给主效应，\(|S|=2\) 给二阶交互，等等。对 \(d=2\) 的当前载体，\(f_{\{1,2\}}\) 就是 strict additive residual \(I\)。

但必须严厉地区分两种情形。若权重不是产品型，或者原始 hypercube 有空 cell / 零权重，那么上面的 canonical Hoeffding orthogonality 一般就不再自动成立：条件期望不再按坐标可分，Möbius 反演虽然形式上还能写，但正交性与“每阶效应唯一”的含义会依赖你选择的投影层级与 Gram 矩阵。此时可以做**层级投影分解**，但不应轻率称为 canonical weighted Hoeffding。换句话说：严格的有限维 ANOVA 可以做，但“自然的坐标分量”只有在产品权重与满支撑条件下才干净。仓库当前已经固定了 source-only weights 与 full-cell carrier；若未来要做高维 ANOVA，最好从同一 raw token panel 再派生出 product-form 的 axis marginals，或者明确承认自己做的是非产品权重下的 hierarchical projection，而不是 canonical Hoeffding。（MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md:L37-L43；HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md:L30-L35, L41-L75）

## 三个主要 no-go 与多尺度自然性

第一条 no-go 是**rank-1 scalar shadow**。把每个时点残差 \(R_t\in H_w\) 按固定 cell 次序堆成矩阵
\[
M\in \mathbb R^{T\times |X|}.
\]
若 \(\operatorname{rank}(M)=1\)，则存在固定模板 \(u\in H_w\) 与标量轨道 \(c_t\) 使得
\[
R_t=c_tu.
\]
这意味着一切“动态”都退化为一条标量时间路径在拖动同一个空间模板，根本不配叫多方向结构。更进一步，由 Eckart–Young 定理，若奇异值满足 \(\sigma_2\ll \sigma_1\)，则
\[
\min_{\operatorname{rank}(L)\le 1}\|M-L\|_F^2=\sum_{k\ge 2}\sigma_k^2,
\]
所以小的 \(\sigma_2/\sigma_1\) 直接说明“近 rank-1 阴影”。这条 no-go 与仓库当前 smoke 审计非常贴合：三份 smoke 的 uncentered \(\sigma_2/\sigma_1\approx 0.132\)，而三对形状相似度又很高，因此最该优先准备的不是颂歌，而是 rank-1 反证器。（Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.md:L44-L65；deep_research_mode_a_quotient_residual_kill_framework_20260623.md:L45-L50, L95-L96）

第二条 no-go 是**随机同维子空间不可区分性**。把 residual ambient space 记作 \(V=\mathcal N^\perp\)，\(\dim V=m\)。若只关心一个 \(r\)-维候选子空间 \(E\subset V\)，那么在各向同性高斯零模型
\[
Z\sim \mathcal N(0,\sigma^2 I_V)
\]
下，
\[
\|\Pi_E Z\|_w^2/\sigma^2
\]
的分布只依赖维数 \(r\)，不依赖 \(E\) 的具体位置。因此，在 isotropic null 下，没有任何固定 \(r\)-维子空间有先验特权。由此得到一条严厉的推论：若经验统计量 \(\Phi(E_{\mathrm{true}},K)\) 并不优于随机同维子空间或随机等规模分箱的零分布，那么 \(E_{\mathrm{true}}\) 就没有坐标不变意义；你看到的不是结构，而是自由度消费。这正是 same-dimension random subspace guard 与 random equal-size partition null 必须并列进入 kill suite 的理论原因。（MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md:L44-L52；deep_research_mode_a_quotient_residual_kill_framework_20260623.md:L105-L106, L117-L129）

第三条 no-go 是**coarsening/projection non-naturality**。先定义多尺度映射。对未来的频率轴细化，建议直接采用嵌套分箱：
\[
\rho^{(Q)}_{8\to 4}(i)=\left\lfloor \frac{i}{2}\right\rfloor,\qquad
\rho^{(Q)}_{4\to 2}(i)=\left\lfloor \frac{i}{2}\right\rfloor,
\]
其中 \(i\in\{0,\dots,7\}\) 或 \(\{0,\dots,3\}\)。对 token position 轴，沿用仓库已有的 source-only 分箱思想，定义
\[
b_8(p)=\min\!\left(7,\left\lfloor \frac{8(p-1)}{63}\right\rfloor\right),\quad
b_4(p)=\min\!\left(3,\left\lfloor \frac{4(p-1)}{63}\right\rfloor\right),\quad
b_2(p)=\min\!\left(1,\left\lfloor \frac{2(p-1)}{63}\right\rfloor\right),
\]
并令 \(\rho^{(B)}_{8\to 4},\rho^{(B)}_{4\to 2}\) 都是“并两格”的块映射。相应 coarsening 算子定义为 block-average：
\[
(C_\rho f)(y)=\frac{1}{w_c(y)}\sum_{\rho(x)=y}w_f(x)f(x),
\qquad
w_c(y)=\sum_{\rho(x)=y}w_f(x).
\]
然后定义自然性缺陷
\[
\Delta_\rho(K)=\|C_\rho \Pi_{N_f^\perp,w_f}K-\Pi_{N_c^\perp,w_c}C_\rho K\|_{w_c}.
\]

这里有一个严格命题：设 \(P_f=\Pi_{N_f^\perp,w_f}\), \(P_c=\Pi_{N_c^\perp,w_c}\)。则
\[
C_\rho P_f=P_cC_\rho
\]
当且仅当
\[
C_\rho(N_f)\subseteq N_c
\quad\text{且}\quad
C_\rho(N_f^\perp)\subseteq N_c^\perp.
\]
证明很短：把任意 \(x\in H_f\) 分解为 \(x=n+r\)（\(n\in N_f, r\in N_f^\perp\)），比较 \(C_\rho P_f x=C_\rho r\) 和 \(P_cC_\rho x=P_c(C_\rho n + C_\rho r)\) 即可。于是，若 coarsening 会把 fine nuisance 推出 coarse nuisance，或者会把 fine residual 推回 coarse nuisance，那么 exact naturality 必然失败；这时对象就是 partition artifact，而不是“同一对象在不同尺度上的表现”。这一条不是可选美学，而是对象同一性的必要条件。（GPT55_PRO_QUOTIENT_RESIDUAL_NEXT_PROMPT_20260623.md:L96-L109；deep_research_mode_a_quotient_residual_kill_framework_20260623.md:L38-L43, L98-L103）

严格地说，未来如果要让自然性成立，一个够强的充分条件是
\[
N_f = C_\rho^*N_c \oplus \ker C_\rho,
\]
即 fine nuisance 恰好由 coarse nuisance 的拉回部分与“粗化时必然消失的纯细节”组成。若做不到这一点，就不要默认 \(q8\to q4\to q2\) 或 `tokenpos8→4→2` 之间存在“同一对象”；必须实打实测 \(\Delta_\rho(K)\)。这也解释了为什么仓库把 coarsening/refinement check 列为必需 gate，而不是可选补图。（HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md:L82-L93；MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md:L44-L52）

## 对易子与 gluing 障碍的严格定义

现在给两个更高层，但仍然必须严格定义的对象。

先看**投影—演化对易子**。令 \(P=\Pi_{\mathcal N^\perp,w}\)，令 \(T:H_w\to H_w\) 是 generation evolution 的线性近似或局部线性化算子。按分解
\[
H_w=\mathcal N\oplus \mathcal N^\perp
\]
把 \(T\) 写成块矩阵
\[
T=
\begin{pmatrix}
A & B\\
C & D
\end{pmatrix},
\qquad
P=
\begin{pmatrix}
0&0\\
0&I
\end{pmatrix}.
\]
则
\[
[P,T]=PT-TP=
\begin{pmatrix}
0&-B\\
C&0
\end{pmatrix}.
\]
所以
\[
[P,T]=0
\iff
B=0 \text{ 且 } C=0
\iff
T(\mathcal N)\subseteq \mathcal N,\; T(\mathcal N^\perp)\subseteq \mathcal N^\perp.
\]
这给出一个非常硬的解释：commutator 不是什么玄学“运动性”，它就是 nuisance sector 与 residual sector 之间的泄漏矩阵。若 \(B\) 和 \(C\) 都为零，动力学只是在各自 sector 内演化；若不为零，则“先去 nuisance 再演化”和“先演化再去 nuisance”不是同一件事。只有在它能通过随机轴、matched templates 与 rank-shadow null 之后，commutator 才值得被当作对象；否则它很可能只是 nuisance leakage 的别名。（GPT55_PRO_QUOTIENT_RESIDUAL_NEXT_PROMPT_20260623.md:L101-L104；deep_research_mode_a_quotient_residual_kill_framework_20260623.md:L52-L57, L108-L109）

再看**gluing obstruction**。这里必须先定义四件事，否则 sheaf 语言一律作废。其一，局部 chart：一族子集 \(U_\alpha\subseteq X\)。其二，局部 section：在每个 chart 上的局部 residual
\[
s_\alpha=\Pi_{N_\alpha^\perp,w_\alpha}(K|_{U_\alpha}).
\]
其三，restriction map：若 \(U_\alpha\cap U_\beta\neq\varnothing\)，定义
\[
r_{\alpha\beta}:H(U_\alpha)\to H(U_\alpha\cap U_\beta)
\]
为普通坐标限制。其四，overlap mismatch：定义
\[
\delta_{\alpha\beta}
=
r_{\alpha\beta}(s_\alpha)-r_{\beta\alpha}(s_\beta).
\]
只有这些都写清，sheaf/gluing 才有资格进入讨论。

更严格一点，真正可测的 obstruction 不应是裸差，而应是**在允许的局部 nuisance gauge 之后仍然消不掉的重叠不一致**。因此建议定义
\[
\operatorname{Obs}(K)
=
\inf_{n_\alpha\in N_\alpha}
\left(
\sum_{\alpha<\beta}
\left\|
r_{\alpha\beta}(K|_{U_\alpha}-n_\alpha)
-
r_{\beta\alpha}(K|_{U_\beta}-n_\beta)
\right\|^2_{w_{\alpha\beta}}
\right)^{1/2}.
\]
若 \(\operatorname{Obs}(K)=0\)，局部对象可 glue 成全局对象；若 \(\operatorname{Obs}(K)>0\)，且在预注册允许的局部 nuisance 扩张下依然显著为正，才可以说存在 gluing obstruction。若稍微放宽一点局部 nuisance 它就消失，那 sheaf 语言是空转，不准继续用。仓库对 sheaf 的态度正该如此苛刻：先定 local sections、restriction maps、overlap mismatch 与 measurable obstruction，做不到就丢掉。（GPT55_PRO_QUOTIENT_RESIDUAL_NEXT_PROMPT_20260623.md:L106-L109；deep_research_mode_a_quotient_residual_kill_framework_20260623.md:L59-L64；MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md:L40-L43, L62-L66）

## 零GPU 击杀套件与 Mode B 判决图

仓库当前最值得保留的，不是某个 smoke 图，而是“对象必须先配刑具”的态度。未来的 16-cell interaction 分析不该比现有 q4 residual gate 更松，只能更严。现有 q4 fold-local 脚本已经把一个最低参考线写进代码：LOSO 弱门槛 \(\Delta R^2\ge 0.02\)，单侧 permutation \(p\le 0.10\)，matched-mean 稳定性要求 stable fraction \(\ge 0.70\) 且 \(|z|\ge 2.58\)，rank/noise 方面要求 \(\sigma_2/\sigma_1\ge 0.25\)，并且残差幅度要超过 \(2\times \max\{\)seed-bootstrap p90, rank1-control p90\(\}\)。interaction 线若想升格，阈值不能比这更松。（q4_full_panel_foldlocal_analysis.py:L250-L270, L348-L397, L444-L477；deep_research_mode_a_quotient_residual_kill_framework_20260623.md:L111-L132）

下面给出我认为足够“残忍”的 zero-GPU kill suite。它与仓库设计文档、adoption note 与 future-only skeleton 一致，但比叙事更硬。

| 关卡 | 统计对象 | 失败即判 | 说明 |
|---|---|---|---|
| provenance / schema / digest 完整性 | `artifact_kind`、schema id、repo head、builder sha256、raw sha256、source-only weights | `invalid_artifact` | 先排除伪工件 |
| full-panel completeness | 必须恰好 `5 seeds × 10 generations = 50 rows`，且 future null blocks 齐全 | `insufficient_artifact` | 数据不够，不准半分析 |
| strict additive annihilation | \(\operatorname{median}_t\|I_t\|_w/\operatorname{median}_t \text{noise}_t\) | \(\le 1\Rightarrow\) `killed_by_noise_floor` | 过不了噪声地板，直接死 |
| matched mean / matched slope | 匹配全局均值与 q4 slope 后的残差方向 | 不稳定或只剩 slope-shadow \(\Rightarrow\) `killed_by_rank1_shadow` | 排除标量+斜率伪影 |
| rank / amplitude | \(\sigma_2/\sigma_1\)、rms amplitude、rank1-control floor | 过低 \(\Rightarrow\) `killed_by_rank1_shadow` | 排除单模板阴影 |
| random equal-size partition | 真 position 轴 vs 随机等规模分箱 | 真轴不优于 null \(\Rightarrow\) `killed_by_random_axis` | 排除自选分箱 |
| within-q shuffle | q 内位置标签打乱前后统计降幅 | 不降 \(\Rightarrow\) `killed_by_random_axis` | 排除 cell 构造伪影 |
| bad-axis control | `audit_block_id` 等坏轴 | 坏轴也能出同级“信号” \(\Rightarrow\) `killed_by_random_axis` | 排除自由度膨胀 |
| same-dimension random subspaces | 真 9 维残差空间 vs 随机 9 维子空间 | 不优于随机 \(\Rightarrow\) `killed_by_random_axis` | 排除坐标偶然性 |
| coarsen/refine naturality | \(\Delta_\rho(K)\) 与主子空间翻转 | 失败 \(\Rightarrow\) `killed_by_coarsening` | 排除 partition artifact |
| principal-angle stability | seed / generation 留出后的主子空间角 | 只在局部成立 \(\Rightarrow\) `killed_by_random_axis` 或 `insufficient_artifact` | 排除 seed-local 偶然性 |
| gluing sanity | \(\operatorname{Obs}(K)\) 在局部 nuisance 后是否仍为正 | 可被局部 nuisance 吸收 \(\Rightarrow\) `insufficient_artifact` | 防止 sheaf 空转 |

这张表不是“若通过则发现成立”，而是“若不过则立刻判死”。即便所有关卡都过，根据当前 future-only 脚本与设计文档，允许的最强措辞也仍然只是 `eligible_for_next_design_review_only`，而不是 observed field，更不是机制性发现。（HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md:L77-L145；q4_hypercube_interaction_prereg_analysis.py:L273-L307；MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md:L48-L52, L68-L87）

回到当前 MaoField 材料，Mode B 的 verdict map 很机械，不需要解释学。第一，若输入是旧 rare/freq aggregate、schema mismatch、hash mismatch、source-only weights mismatch 或缺少 top-level fields，则应判 `invalid_artifact`。这是 interaction skeleton 代码直接写死的。（q4_hypercube_interaction_prereg_analysis.py:L130-L176, L179-L226, L339-L346）

第二，若未来有合格 full panel，但 median interaction/noise ratio \(\le 1\)，则应判 `killed_by_noise_floor`；若 \(\sigma_2/\sigma_1\) 太低或 matched mean/slope 后只剩单模板轨道，则判 `killed_by_rank1_shadow`；若真轴不优于随机等规模分箱、坏轴或随机同维子空间，则判 `killed_by_random_axis`；若 coarsen/refine 失败，则判 `killed_by_coarsening`。这些 verdict 在 prereg script 里已经被机械化，不该被后验解释改写。（q4_hypercube_interaction_prereg_analysis.py:L291-L307）

第三，就**当前** bundle 而言，唯一合法 verdict 仍是 `insufficient_artifact`。原因很直接：没有 PI-approved 50-checkpoint full panel、没有 interaction full-panel aggregate、没有 prereg null blocks、没有 held-out seed / generation-block leave-out 结果、没有 random partitions / same-dimension subspaces / coarsening tests 的真正输出块。仓库状态文件、设计文档、adoption note 与脚本对此完全一致。（STATE.md:L16-L27；HYPERCUBE_INTERACTION_ANALYSIS_PREREG_DESIGN_20260623.md:L37-L75, L98-L145；MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md:L54-L87）

至于当前 smoke，只能当“将来优先准备哪种 no-go 反证器”的线索，不能当 evidence bridge。仓库自己的 smoke 审计写得非常明白：三份现有 smoke raw 上，可以复算出一个小的 additive-residual 交互项，三对形状相近，但这不是 full panel，不能支持 scientific or philosophical claim；同时低的 uncentered \(\sigma_2/\sigma_1\) 还提示它很接近单一主模板。因此，今天能说的最强 MaoField-specific 话，不是“看到了 interaction field”，而只是“smoke 上可复算出一个小的 strict-additive residual hint；它依旧只配 `smoke_conjecture_only` 与 `insufficient_artifact` 的组合边界”。（Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.md:L7-L19, L44-L77；STATE.md:L16-L24）

## 最终结论

### Mode A 的最强底层数学问题

去掉 MaoField 品牌、旧叙事与经验包袱之后，真正值得保留的底层问题只有一个，而且它必须写成母对象的 existence/no-go 问题，而不是某个具体 dashboard 残差的追认：

\[
\boxed{
\text{在所有可容许三元组 }(X,w,\mathcal N)\text{ 上，是否存在一个商残差族 }
R_t=\Pi_{\mathcal N^\perp,w}K_t
\text{，它同时}
}
\]
\[
\boxed{
\text{高于噪声地板、不是 rank-1 scalar shadow、优于随机同维子空间与随机等规模分箱，并在预注册 coarsening/refinement 下保持自然性？}
}
\]

若答案为**有**，得到的是一个不能被主效应、平滑 nuisance、标量轨道或坐标重命名吸收的有限维结构对象。若答案为**无**，得到的也不是“暂时没找到”，而是一条更强的统一 no-go：所谓复杂结构不过是 scalar projection、low-rank template 或 coordinate artifact。换言之，这个问题阳性有价值，阴性同样有价值；它不依赖 MaoField 品牌存活。（deep_research_mode_a_quotient_residual_kill_framework_20260623.md:L66-L84, L158-L164；MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md:L30-L47）

### 当前允许的最强 MaoField 特定结论

当前允许的最强 MaoField-specific claim 只有下面这句，不能再多：

**MaoField 目前只支持一个 zero-GPU formal preregistration 与 smoke-feasibility 边界：在三份现有 smoke raw 上，按 \(Q_{\mathrm{freq4}}\times B_{\mathrm{tokenpos4}}\) 的 strict additive subtraction 可以复算出一个小的 16-cell interaction residual hint；但这既不是 observed hypercube residual，也不是 observed interaction field，更不是 stable residual field。当前关于稳定非标量结构的正式 verdict 仍然是 `insufficient_artifact`，interaction smoke 仍然只是 `smoke_conjecture_only`。**（STATE.md:L16-L27；GPT55_PRO_RESEARCH_INDEX_20260622.md:L88-L95, L510-L526, L600-L612；Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.md:L55-L77；MODE_A_QUOTIENT_RESIDUAL_KILL_FRAMEWORK_ADOPTION_NOTE_20260623.md:L54-L87）

这就是严格答案。再往上说，都是越界。