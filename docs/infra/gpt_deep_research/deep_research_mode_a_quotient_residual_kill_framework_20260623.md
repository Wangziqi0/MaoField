# MaoField 去魅后的底层数学问题与严格击杀框架

## 证据边界

先把边界写死，再谈对象。

当前 MaoField 允许的最强说法，不是“已经看到了某个稳定非标量结构”，而只是：项目处于 **negative-centered** 的审计性状态；`Q_freq4 × B_tokenpos4` 目前只是一个 **zero-GPU formal prereg** 坐标系统；interaction 方向的现有结果也只是三份 smoke 原始数据上可复算的小残差，因此只能算 **smoke_conjecture_only**。仓库与状态文件都明确阻断以下升级表述：不能说 full panel 已运行，不能说 hypercube interaction field 或 residual field 已被观察到，不能说 `LOSO passed`、`F3 positive`、`glass box broken`、`training authorized`、`new loss authorized`。fileciteturn4file0L18-L19 fileciteturn4file0L24-L29 fileciteturn8file0L103-L119 fileciteturn9file0L7-L12 fileciteturn9file0L100-L125

更严格地说，当前仓库材料只支持两类事实。第一类是**工程—分析闸门**：已存在一个未来用的 interaction prereg skeleton，它只接受 provenance-checked 的未来 full-panel aggregate，最强 verdict 也只是 `eligible_for_next_design_review_only`；没有 aggregate 时应输出 `insufficient_artifact`，schema 或 provenance 不合格时应输出 `invalid_artifact`。第二类是**smoke 级别的可复算提示**：三份 smoke 文件上的 4×4 cell-mean 矩阵，在去掉常数项、q4 主效应、position 主效应后，确有一个小的非加性残差，但这仍不是 observed field，更不是科学性结果。fileciteturn10file0L132-L178 fileciteturn10file0L231-L306 fileciteturn11file0L17-L56 fileciteturn13file0L11-L21 fileciteturn13file0L57-L79

这意味着，**Mode B 的答案已经确定**：截至 2026-06-23，MaoField 没有证明“稳定非标量结构”存在。最多只能说，还没有把某个候选残差彻底杀死，但更没有把它立起来。仓库内部的严格数学审计把这个结论写得很直接：当前中心问题应当从“是否已有发现”改写为“在预注册的有限带权乘积空间中，固定 nuisance 之后，商空间残差是否作为稳定非标量对象存活”。fileciteturn19file0L9-L23 fileciteturn7file0L30-L44 fileciteturn21file0L61-L66

## 候选数学对象

下面进入 Mode A。这里我不把 MaoField 当作一个需要维护旧叙事的项目，而把它当作一个暴露了 **identification failure** 的失败试材：过去的问题常常不是“是否存在新结构”，而是“某个标量阴影能否被重新讲述成新结构”。真正的底层对象，必须在均值、主效应、平滑 generation 趋势、匹配 slope、随机轴自由度之后，仍然留下来。fileciteturn18file0L3-L11 fileciteturn19file0L27-L33

共同的环境我先固定。令 \(X=\prod_{j=1}^d A_j\) 是预注册的有限乘积空间，\(w:X\to(0,1]\) 为正权重且 \(\sum_x w(x)=1\)，令
\[
H_w=\mathbb R^X,\qquad \langle f,g\rangle_w=\sum_{x\in X}w(x)f(x)g(x).
\]
若 carrier、weights、nuisance 不是先固定，后面所谓“残差对象”就没有对象同一性。对当前 concretization，仓库已经把 `Q_freq4 × B_tokenpos4`、source-only 权重、strict additive nuisance 以及 forbidden axes 全部写死，其中 \(4\times4\) 情形的严格加性 nuisance 维数为 \(7\)，其补空间维数为 \(9\)。fileciteturn20file0L15-L23 fileciteturn15file0L41-L61 fileciteturn15file0L76-L119

**候选对象一：加权乘积划分交互场 \(I_t\)。**
形式定义：
\[
I_t=\Pi_{\mathcal A^\perp,w}K_t,\qquad
\mathcal A=\{\mu+\alpha(q)+\beta(b)\},
\]
其中 \(K_t(q,b)\) 是 checkpoint \(t\) 的 16-cell mean-logprob 场。环境空间是 \(H_w=\mathbb R^{Q\times B}\)。nuisance quotient 是“常数项 + q4 主效应 + token-position 主效应”的严格加性子空间。可观测统计量应至少包括 \(\|I_t\|_w\)、跨 checkpoint 的 flattening 奇异值谱、\(\sigma_2/\sigma_1\)、以及 matched contrast 的符号稳定性。零模型不是“\(I_t=0\)”这么简单，而是随机等规模 position 分箱、within-q shuffle、坏轴 `audit_block_id`、随机同维子空间。快杀测试是：若 \(\|I_t\|_w\) 落到 noise floor，或真轴不优于随机分箱/坏轴，立刻杀。定理目标不是做 dashboard，而是证明“带权可加—交互分解存在且唯一”，并给出 \(I_t=0\iff K_t\) 带权可加。这个对象与仓库 adoption note 和 prereg design 完全对齐，但它仍是**具体 instantiation**，不是最底层对象。fileciteturn8file0L27-L46 fileciteturn9file0L18-L37 fileciteturn20file0L3-L13 fileciteturn20file0L69-L80

**候选对象二：一般 nuisance 商残差族 \(R_t\)。**
形式定义：
\[
R_t=\Pi_{\mathcal N^\perp,w}K_t,
\]
其中 \(\mathcal N\) 不再局限于加性主效应，而是所有**在看 outcome 之前就注册好的** nuisance：均值、主效应、q4 slope、generation smooth trend、matched mean/slope 模板、decode-policy 诱导模板、seed baseline 等。环境空间仍是 \(H_w\)，但对象真正属于商空间类 \([K_t]\in H_w/\mathcal N\)。可观测统计量是 \(\|R_t\|_w\)、rank 结构、对随机同维子空间的优势、以及 coarsening/refinement 稳定性。零模型是每个预注册 \((X,w,\mathcal N)\) 下，所有 residual 都落入“近零、近 rank-1、随机轴不可区分、尺度不稳定”四类之一。快杀测试是：只要 residual 不能同时越过 noise、rank、random-axis、coarsening 四门，就判不存在。定理目标是一个存在性/不存在性命题：是否存在稳定非平凡商残差对象。它是最纯的底层问题，因为其他所有对象都只是它的特殊化、函子化或几何化。fileciteturn7file0L30-L44 fileciteturn20file0L15-L23 fileciteturn21file0L61-L66

**候选对象三：多尺度自然性缺陷 \(N_{\rho,t}\)。**
形式定义：
\[
N_{\rho,t}=C_\rho \Pi_{\mathcal A_f^\perp,w_f}K_t-\Pi_{\mathcal A_c^\perp,w_c}C_\rho K_t,
\]
其中 \(\rho:X_f\to X_c\) 是由同一 raw 派生的 coarse map，例如 \(q8\to q4\to q2\) 或 `tokenpos8→4→2`。环境空间是 coarse/fine Hilbert 空间之间的算子差。nuisance quotient 是 fine/coarse 两侧各自的 prereg nuisance。可观测统计量是 \(\|N_{\rho,t}\|_{w_c}\)、主子空间旋转角、粗化后符号是否翻转。零模型是：真实结构若存在，应近似满足自然性；随机分箱与后验坐标通常不满足。快杀测试是：只要粗化后残差消失、翻号或与粗尺度 residual 不可对齐，就判为 partition artifact。定理目标是一个**自然性或非自然性定理**：何时粗化与投影对易，何时必然不对易。这个对象是把“多尺度一致性”从口号变成算子命题。fileciteturn20file0L25-L36 fileciteturn21file0L32-L34 fileciteturn9file0L91-L99

**候选对象四：张量残差与秩阴影商。**
形式定义：若未来 full panel 存在，令
\[
R\in \mathbb R^{S\times G\times Q\times B},
\]
或其 flattening \(M\in\mathbb R^{(S G)\times (Q B)}\)。不是只看 \(R\) 本身，而是看它在“rank-1 标量阴影”上的商类：真实问题不是 residual 是否非零，而是 residual 是否超过“固定 cell 模板 \(\times\) 单一标量轨道”的解释能力。环境空间是四阶张量空间或其 flattenings；nuisance quotient 是先做 \(\Pi_{\mathcal N^\perp,w}\)，再考虑 rank-1 控制模板。可观测统计量是 \(\sigma_2/\sigma_1\)、CP/Tucker rank proxy、rms amplitude 与 rank-1 control 的比较。零模型是 residual 仅为 \(c_t u\) 型单模板缩放。快杀测试是 \(\sigma_2/\sigma_1\) 低且幅度不过 noise/rank1 floor。定理目标是：若 flattening rank 为 1，则任何所谓“复杂动态”都退化为单模板标量轨道。仓库 smoke 审计中 \(\sigma_2/\sigma_1\approx 0.132\) 的现象，正是这个 no-go 方向的原型。fileciteturn20file0L38-L42 fileciteturn20file0L82-L90 fileciteturn13file0L46-L62

**候选对象五：投影—演化对易子 \(C=[\Pi,T]\)。**
形式定义：
\[
C=\Pi T-T\Pi,
\]
其中 \(T\) 是 generation 演化算子，\(\Pi=\Pi_{\mathcal N^\perp,w}\) 是 prereg nuisance 去除投影。环境空间是 \(H_w\) 上的线性或局部线性算子代数。nuisance quotient 已经嵌入 \(\Pi\) 之中。可观测统计量是 \(\|C K_t\|_w\)、谱半径、主特征方向，或“先残差化再推进”与“先推进再残差化”的差。零模型是 additive/separable dynamics，其下 \(T\) 保持 nuisance 子空间及其正交补，从而 \(C=0\)。快杀测试是：若经验上 \(C\) 始终接近零，且所有效应都被 \(\Pi\) 后的标量轨道吸收，则 commutator 方向失去意义。定理目标是给出 preservation 条件与非对易障碍。它对应哲学中的“motion 不是加在对象外部，而是在 quotient 后仍留下来的不兼容性”。fileciteturn20file0L92-L97

**候选对象六：局部模型的 gluing obstruction。**
形式定义：取一组局部 chart \(U_\alpha\)，在每个 chart 上拟合局部 nuisance-quotiented residual \(R_\alpha\)，并在重叠区定义
\[
\delta_{\alpha\beta}=R_\alpha|_{U_\alpha\cap U_\beta}-R_\beta|_{U_\alpha\cap U_\beta}.
\]
若进一步在三重交上出现非平凡 cocycle mismatch，则得到真正的 gluing obstruction。环境空间不是单个向量空间，而是一个带 restriction maps 的局部模型系统。nuisance quotient 是 chart 内局部 nuisance；真正问题在于局部剥离后能否拼成一个全局对象。可观测统计量是 overlap mismatch、consistency radius、以及局部—全局残差差值。零模型是 sheaf-like 一致拼接：若所有局部残差可在重叠处一致 glue，则此方向没有独立信息。快杀测试是：若所谓 obstruction 完全被扩大一点 स्थानीय nuisance 就吸收掉，则 sheaf 语言空转。定理目标是：证明“局部看似可解释，不蕴含全球可解释”，并且把失败具体定位在 overlap 上，而不是回到隐喻。fileciteturn20file0L44-L48 fileciteturn21file0L21-L24

## 最佳底层对象

最佳底层对象不是 \(I_t\)，也不是 tensor rank，更不是 sheaf 或 commutator。最佳对象是：

\[
\boxed{R_t=\Pi_{\mathcal N^\perp,w}K_t}
\]

也就是**预注册有限带权乘积空间上的一般 nuisance 商残差族**。fileciteturn7file0L30-L44 fileciteturn21file0L61-L66

理由很简单，而且是严格的。

第一，它是**最小而充分**的对象。若直接选 \(I_t=\Pi_{\mathcal A^\perp,w}K_t\)，你已经偷偷承诺了“真实 nuisance 只有加性主效应”；可现实里仓库自己已经要求更广的 nuisance：q4 slope、generation smooth trend、matched mean/slope、decode confounds、随机同维控制。于是 \(I_t\) 只是某个 particular quotient；\(R_t\) 才是 quotient 原理本身。fileciteturn20file0L15-L23 fileciteturn21file0L7-L24

第二，它对 yes/no 两个方向都同样有力。若未来 \(R_t\) 在噪声、rank、random-axis、coarsening 四重门槛后仍存活，那么你得到的不是“玻璃盒被打破”，而是一个更克制、也更强的事实：存在某个**不能被预注册 nuisance 吸收**的非平凡对象。若未来所有 admissible \((X,w,\mathcal N)\) 都失败，那么负结论将比“没找到阳性”更强：它将构成一个统一 no-go，表明复杂 collapse narrative 只是 scalar projection、low-rank shadow 或 coordinate artifact。这个否定性力量，正是 Mode A 真正应追求的结果。fileciteturn21file0L61-L66 fileciteturn20file0L99-L102

第三，它把其他对象全部变成**派生结构**。加权 interaction field 是取特定 \(\mathcal N=\mathcal A\) 的特例；多尺度自然性缺陷是给 \(R_t\) 再施加 coarse/fine functor 的比较；tensor-rank 是把 \(\{R_t\}\) 堆成 panel 张量；projection-evolution commutator 是研究 \(R_t\) 与时间推进的不相容；gluing obstruction 则是研究 \(R_t\) 的局部—全局一致性。换言之，\(R_t\) 不是六个对象中的一个“选择题答案”，它是五个对象的母对象。fileciteturn20file0L15-L48

因此，我的结论非常明确：**Mode A 的底层问题不应写成“是否存在 interaction field”，而应写成“在固定的 \(X,w,\mathcal N\) 下，商残差族 \(R_t\) 是否存在为稳定、非标量、非随机、非 rank-1、非 partition-dependent 的对象”**。interaction field 只是第一层、最便宜的试金石。真正的 bottom level，是 quotient residual existence problem。fileciteturn7file0L30-L44 fileciteturn21file0L61-L66

## 定理与否定性定理方向

**方向一：加权可加—交互分解唯一性定理。**
对任意有限 \(Q\times B\) 与正权重 \(w\)，任意 \(K\in H_w\) 唯一分解为
\[
K=\mu+\alpha(q)+\beta(b)+I,\qquad I\in\mathcal A^\perp.
\]
而且 \(I=0\) 当且仅当 \(K\) 在带权意义下完全可加。这个命题看似基础，实际上价值很高：它把“contradiction = non-additive interaction”从隐喻变成了严格的投影残差判断。对 \(4\times4\) 情形，\(\dim \mathcal A^\perp=9\) 直接给出对象的自由度上限。fileciteturn20file0L69-L80

**方向二：rank-1 阴影否定性定理。**
设 \(M\) 为 checkpoint×cell 的 residual flattening。若 \(\operatorname{rank}(M)=1\)，则 \(R_t=c_tu\)；任何跨 checkpoint 的复杂叙事，都等价于一个标量路径 \(c_t\) 乘上固定模板 \(u\)。这应被视为**禁止使用“多方向结构”措辞**的 no-go 定理，而不是“弱阳性”。在当前 smoke 数据上，低的 uncentered \(\sigma_2/\sigma_1\) 已经把这个方向变成最应优先准备的反证器。fileciteturn20file0L82-L90 fileciteturn13file0L52-L62

**方向三：自然性—分箱依赖二分定理。**
若
\[
C_\rho\Pi_f=\Pi_c C_\rho,
\]
则细尺度 residual 才可合法称为粗尺度对象的 refinement；若此式系统性失败，则对象不是“更细的同一结构”，而是 partition artifact。这个方向的价值在于：它不要你先证明对象存在，它先检查对象是否**跨尺度有同一性**。如果连这一点都没有，讨论任何 higher-order interaction 都是浪费。fileciteturn20file0L25-L36

**方向四：随机同维子空间不可区分 no-go 定理。**
这是我建议新增的真正“残忍”定理方向：若对预注册真子空间 \(\mathcal N^\perp\) 的统计量，经验上并不优于随机同维子空间或随机等规模分箱的零分布，那么任何声称“该对象抓住了真实结构”的说法都不再有坐标不变意义。形式上，这是一个**不可识别性定理**：对象只在人工选坐标下显现，而不在 registered-vs-random 的比较中显现，于是它不是结构，而是自由度消费。仓库 kill suite 已经把这一思想写入 `same-dimension subspace guard` 与 `random equal-size partition null`，只是还没有被提升成理论主命题。fileciteturn21file0L13-L20 fileciteturn9file0L84-L95

**方向五：投影—演化非对易障碍定理。**
若 \(T\) 保持 nuisance 子空间与其正交补，则 \([\Pi,T]=0\)；反之，持久的 \([\Pi,T]\neq 0\) 说明“先去 nuisance 再演化”与“先演化再去 nuisance”不可交换。这里的关键不是把非对易性神秘化，而是把它降到一个最基础的判准：动力学是否会把 nuisance 混回 residual。若会，那么任何静态 residual 解释都不完整；若不会，那么 motion 只是在静态对象上拖动一个坐标。fileciteturn20file0L92-L97

## 预注册击杀套件

真正好的对象，必须先设计出让自己死掉的条件。仓库已经给出了雏形：未来 interaction 脚本只应接受 provenance-checked full-panel aggregate；缺少 aggregate、旧 rare/freq 行、缺少 null blocks 都要 fail closed；noise floor、rank-shadow、random-axis、coarsening 都必须进入 verdict。q4 residual 现有阈值也给出了一个最低参考：`delta_r2 >= 0.02`、单侧 permutation `p <= 0.10`、稳定符号比例至少 `0.70` 且 `|z| >= 2.58`、`sigma2/sigma1 >= 0.25`，并要求幅度高于 `2 × max(seed-bootstrap p90, rank1-control p90)`。fileciteturn10file0L293-L306 fileciteturn21file0L7-L24 fileciteturn16file0L13-L33 fileciteturn16file0L111-L160 fileciteturn16file0L193-L240 fileciteturn17file0L22-L41

我建议把 interaction 线的 prereg kill suite 固定为下面这套，而且比 skeleton 更严格，而不是更松：

| 门槛 | 核心统计 | 失败动作 | 解释 |
|---|---|---|---|
| provenance / schema / hash 完整性 | schema id、repo head、builder sha256、raw sha256、source-only weights | `invalid_artifact` | 工件不合法，直接退回 |
| 真实 full panel 完整性 | 必须是 `5 seeds × 10 generations = 50 checkpoints`，且 null test blocks 齐全 | `insufficient_artifact` | 数据不够，不准“半分析” |
| 严格加性湮灭 | \(\operatorname{median}_t \|I_t\|_w / \text{noise}_t\) | \(\le 1\) 时 `killed_by_noise_floor` | 连噪声都越不过 |
| matched mean / slope | 在匹配全局均值与 q4 slope 后的方向稳定度 | 若 residual 只剩 slope-shadow 或符号不稳，则 `killed_by_rank1_shadow` | 排除“标量加斜率”伪影 |
| rank / amplitude | \(\sigma_2/\sigma_1\)、rms amplitude、rank1-control floor | 低于 prereg floor 则 `killed_by_rank1_shadow` | 排除单模板阴影 |
| random equal-size partition | 真 position 轴 vs 随机等规模分箱 | 真轴不优于 null 则 `killed_by_random_axis` | 排除自选分箱 |
| within-q shuffle | q 内位置标签打乱后统计下降幅度 | 不下降则 `killed_by_random_axis` | 排除 cell 算法结构 |
| bad-axis control | `audit_block_id` 等坏轴 | 坏轴也能出同等级信号，则 `killed_by_random_axis` | 排除自由度膨胀 |
| same-dimension subspace guard | 真实 9 维残差子空间 vs 随机 9 维子空间 | 不优于随机则 `killed_by_random_axis` | 排除坐标偶然性 |
| coarsen/refine naturality | \(\|C_\rho\Pi_fK-\Pi_cC_\rho K\|\) | 消失、翻号或主子空间剧转则 `killed_by_coarsening` | 排除 partition artifact |
| principal-angle stability | 跨 seed / generation held-out 的主子空间角 | 若只在局部或少数 seed 成立，则通常回到 `killed_by_random_axis` 或 `insufficient_artifact` | 排除 seed-local 偶然性 |
| gluing sanity | overlap mismatch 是否可被局部 nuisance 吸收 | 可完全吸收则 `insufficient_artifact` | 防止 sheaf 语言空转 |

这套击杀不是为了“刁难对象”，而是为了把数学对象与 dashboard 残差彻底分开。通过全部门槛以后，允许的最强结论依然只是 `eligible_for_next_design_review_only`，而不是 observed field，更不是机制发现。仓库的 prereg design 与 future-only 脚本都已经把这一点写死。fileciteturn9file0L79-L99 fileciteturn9file0L100-L147 fileciteturn10file0L35-L53 fileciteturn11file0L45-L56

## 谨慎回译到 MaoField Mode B

现在只准用允许的 verdict 说话。

对**今天**这包材料，关于“稳定非标量结构是否已被证立”的 Mode B 结论，只能是：

\[
\boxed{\texttt{insufficient\_artifact}}
\]

原因不在于“smoke 完全没有东西”，而在于：没有 PI 批准的 50-checkpoint full panel；没有 interaction full-panel aggregate；没有 prereg null blocks；没有 held-out seed / generation-block leave-out；没有 random equal-size partition、within-q shuffle、same-dimension random subspace、coarsening/refinement 这些必要控制。未来脚本本来就是为这种情况定义 `insufficient_artifact` 的。fileciteturn9file0L41-L45 fileciteturn10file0L275-L306 fileciteturn11file0L17-L29

对**旧 rare/freq aggregate**、schema/hash 不匹配、source-only weights 不匹配、缺顶层字段等情形，结论应是：

\[
\boxed{\texttt{invalid\_artifact}}
\]

因为 interaction prereg skeleton 已明确拒绝旧 q4 rare/freq aggregate 作为 `q4 × tokenpos4` full-panel 输入，并对 metadata、rows、schema weights、digest 进行 fail-closed 校验。fileciteturn10file0L132-L178 fileciteturn11file0L21-L29

如果未来真的有合格 full-panel aggregate，那么 verdict 分岔应当是机械的，而不是解释性的。median interaction/noise ratio 若 \(\le 1\)，就应当是 `killed_by_noise_floor`；若 spectrum 近 rank-1、matched mean/slope 以后只剩单模板阴影，则应当是 `killed_by_rank1_shadow`；若真轴不优于随机分箱、bad axis、随机同维子空间，则应当是 `killed_by_random_axis`；若对象无法在 \(q2/q4/q8\) 与 `tokenpos2/4/8` 的 prereg coarsening/refinement 下保持自然性，则应当是 `killed_by_coarsening`。只有这些都过，而且 strict review 过，才配得上 `eligible_for_next_design_review_only`。fileciteturn10file0L293-L306 fileciteturn9file0L84-L111 fileciteturn17file0L22-L41

对当前 smoke hint，我的谨慎回译是：它**不是** observed field；它在 Mode B 里仍然只配 `insufficient_artifact`。但它同时暴露了一个高度具体的未来失败模式：由于当前 smoke 的 uncentered \(\sigma_2/\sigma_1\approx 0.132\)，而且三点形状相关又极高，它很可能在真正 full-panel 审计中被判成 `killed_by_rank1_shadow`。这不是现阶段的正式 verdict，因为正式 verdict 仍被 full-panel 缺失所支配；但它是最值得优先准备的 no-go 路线。fileciteturn13file0L46-L62 fileciteturn8file0L73-L89 fileciteturn8file0L91-L117

最后，把问题压成一句完全去品牌化的话：

在固定的有限带权乘积空间 \(X\)、固定的 prereg nuisance \(\mathcal N\)、固定的负对照与随机轴零模型下，是否存在一个商残差族
\[
R_t=\Pi_{\mathcal N^\perp,w}K_t
\]
同时高于噪声地板、不是 rank-1 scalar shadow、优于随机同维子空间与随机分箱、并在 prereg coarsening/refinement 下稳定？若答案是**有**，它揭示的不是“已进入玻璃盒”，而是一个不能被主效应、标量轨道、平滑 nuisance 或坐标重命名吸收的结构限制。若答案是**无**，那就不是“暂时没发现”，而是一条更强的 no-go：复杂 collapse narrative 不过是 scalar projection、low-rank template 或 coordinate artifact。就目前 MaoField 的证据而言，答案仍然是后者尚未被彻底证明、前者更没有被证立；因此最正确的仓库内裁定仍然是 **Mode A 继续，Mode B 从严，当前不越过 `insufficient_artifact`**。fileciteturn21file0L61-L66 fileciteturn7file0L39-L44 fileciteturn8file0L44-L55