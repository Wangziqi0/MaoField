# MaoField 去魅后的严格数学审计

## 执行裁决

以下仓库内证据引用统一写成 `路径:Lx-Ly`，均取自你上传的 bundle 当前快照；外部数学背景只用于支撑一般性定义，不用于替代 MaoField 证据。当前 bundle 对证据边界写得非常硬：项目总综合仍是 **negative-centered**；旧训练对象本质上是一个两项的标量 KL/EMA 平滑器；`F3` 只是“值得追的弱例外”而不是正发现；`Q_freq4 × B_tokenpos4` 目前只被允许进入 **zero‑GPU formal prereg feasibility**；而 interaction smoke 也只被允许进入 **smoke_conjecture_only**。`full panel`、`training`、`new loss`、`glass box broken` 等升级表述均被显式阻断。 【repo/STATE.md:L16-L27】【repo/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:L27-L68】【repo/docs/infra/math_turn_20260622/Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.md:L8-L18】【repo/docs/infra/gpt_deep_research/FUTURE_MATH_OBJECTS_INTERACTION_FIELD_ADOPTION_NOTE_20260623.md:L101-L117】

### Mode B 证据门槛裁决

严格按现有证据回答你的中心问题：**到目前为止，没有任何“稳定非标量结构已经存在”这一命题被 MaoField 证明。** 现有 bundle 最多支持这样一句话：把 `4×4` 的 cell-mean logprob 矩阵按加权常数项、q4 主效应、token-position 主效应剥离后，确实还剩下一个**小的、可复算的非加性余量**；但这个余量只在 3 个 smoke 点上出现，幅度大约只有 mean-null 尺度的 `10%–11%`，且三点合起来几乎接近单一主形状，因此它更像“值得被杀测的候选剩余”而不是“已识别的稳定对象”。仓库自己的正式裁定正是 `smoke_conjecture_only`，不是 observed field，更不是 scientific result。 【repo/docs/infra/math_turn_20260622/Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.md:L13-L19】【repo/docs/infra/math_turn_20260622/Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.md:L23-L65】【repo/docs/infra/gpt_deep_research/FUTURE_MATH_OBJECTS_INTERACTION_FIELD_ADOPTION_NOTE_20260623.md:L71-L99】

我还按 bundle 内脚本在本地对上传 raw JSONL 重新跑了一次 `scripts/q4_hypercube_interaction_smoke_audit.py`，复得与 adoption note/markdown audit 一致的数值：三个 smoke checkpoint 的 interaction/mean-null 比值分别约为 `0.1002`、`0.1116`、`0.1088`，两两加权相关约为 `0.948`、`0.947`、`0.969`，而未中心化的 `sigma2/sigma1` 约为 `0.132`（加权）与 `0.1465`（不加权），最终 verdict 仍是 `smoke_conjecture_only`。这说明“有一个小余量”是可复算事实；但同一组数也同时说明，这个余量目前极可能只是**低维模板 + 小幅度系数**，还远远谈不上稳定多方向结构。 【repo/scripts/q4_hypercube_interaction_smoke_audit.py:L97-L103】【repo/scripts/q4_hypercube_interaction_smoke_audit.py:L154-L176】【repo/scripts/q4_hypercube_interaction_smoke_audit.py:L179-L216】【local reproduction local_test.json:L14-L19】【local reproduction local_test.json:L20-L275】

因此，证据门槛下最严厉、也最准确的结论是：**现在只能说“还没把非标量结构杀干净，但更没有把它立起来”。** 这不是折中判断，而是边界判断。当前所有夸张叙事都还没有穿过：held-out seed、generation-block leave-out、matched mean/slope、random same-dimension guards、random partition null、coarsening/refinement 稳定性、rank/noise floor。仓库文档反复强调，未过这些 gate 之前，不得声称 `LOSO passed`、`residual field observed`、`mean-null vector field survives`、`glass box broken`、`training authorized`、`new loss authorized`。 【repo/STATE.md:L24-L27】【repo/docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md:L62-L90】【repo/scripts/q4_full_panel_foldlocal_analysis.py:L539-L558】【repo/scripts/q4_full_panel_foldlocal_analysis.py:L617-L625】

### Mode A 自由数学裁决

如果把 MaoField 当作已经去魅的失败试材，而不再当作“旧 claim 需要保全”的对象，那么它真正留下来的不是某个现成发现，而是一个更锋利的底层问题：

> **在一个预注册、带权、有限乘积划分空间里，去掉所有固定 nuisance 之后，余下的商空间残差是否存在、是否稳定、是否超出随机同维子空间与随机分箱的零模型？**

这是一个真正的数学问题，也是我认为唯一值得继续追的东西。若未来答案为 **是**，它揭示的限制不是“玻璃盒被打破”，而是：模型退化/恢复/控制中确有一个**不能被任何标量轨道、主效应、平滑 generation nuisance 或坐标重命名吸收**的低维非加性对象。若未来答案为 **否**，那么负面结论的力量反而更强：所谓复杂崩塌叙事，只不过是标量投影、低秩阴影或坐标制品。这个问题的形式与 functional ANOVA/Hoeffding 分解、张量低秩分解、子空间角、以及 sheaf 的 gluing 条件天然相连；但前提始终是**先固定参考权重或分布，再谈唯一分解**，否则对象本身没有数学同一性。 【repo/docs/infra/gpt_deep_research/FUTURE_MATH_OBJECTS_INTERACTION_FIELD_ADOPTION_NOTE_20260623.md:L27-L52】【repo/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:L72-L85】 citeturn2view0turn2view2turn2view3turn2view4

## 证据边界与当前仓库实际支持

先把仓库里**真正存在**的对象和**尚不存在**的对象分开。历史训练对象不是某个“场”，而是标量 KL/EMA 平滑器
\[
L_{\mathrm{cont\_chain}}
=(D_n-D_{n-1})^2+(D_n-D_{\mathrm{ema}})^2,\qquad
D_n=\mathrm{KL}(q_{\mathrm{EMA}}\|p_{\mathrm{current}}).
\]
仓库自己把这点写成了数学转向的最小理由：一旦坏状态进入同一个标量 KL 平台，EMA 会几何追上，旧对象就会失明，所以接下来必须“拒绝标量完成”，去问 mean-null 或 quotient 里还有没有剩余结构。 【repo/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:L41-L50】【repo/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:L70-L85】

当前带明文工件支持的“新对象”只有两层。第一层是 q4 线上的 slope-orthogonal residual field 候选
\[
r_i=u_i-\langle v,u_i\rangle_w\,v,
\]
它已经被写进当前仓库脚本 `scripts/q4_full_panel_foldlocal_analysis.py` 的对象定义和 gate 逻辑里；但注意，这个脚本只接受**未来的 q4 full-panel aggregate**，最强 verdict 也不过是 `eligible_for_next_design_review_only`，并且它仍不是现有 evidence，而是未来分析路径。第二层是 `Q_freq4 × B_tokenpos4` 上的 weighted product-partition interaction field 候选
\[
I_i=\Pi_{A^\perp,w}K_i,
\]
其中 `A` 去掉常数均值、q4 频率主效应和 token-position 主效应。这个对象在 adoption note 中被采纳为“最强 future candidate”，但同一份 note 也明确写道：`I_i\neq 0` 只证明在**选定 16 个 cell + 选定投影**下非加性没有被消掉，绝不等于机制、哲学结果或 glass-box access。 【repo/scripts/q4_full_panel_foldlocal_analysis.py:L1-L11】【repo/scripts/q4_full_panel_foldlocal_analysis.py:L30-L35】【repo/docs/infra/gpt_deep_research/FUTURE_MATH_OBJECTS_INTERACTION_FIELD_ADOPTION_NOTE_20260623.md:L23-L53】

当前 `Q_freq4 × B_tokenpos4` 作为坐标系统本身是完全真材实料的：schema builder 明确把第二轴定义为从 `token_pos` 通过 `position_bin = min(3,(token_pos-1)*4//63)` 派生的 outcome-independent 分箱；cell 权重来自 source-only 计数；`strict additive nuisance space` 的维数被固定为 \(1+(4-1)+(4-1)=7\)，所以残差补空间维数是 \(16-7=9\)。同一 schema 还把 `seed`、`generation`、post hoc axis 等列为 `forbidden_axes_for_primary_v1`，并把各种 overclaim 明文列入 `must_not_support`。这一步非常关键：它把“对象的 carrier、weights、nuisance、axis policy”第一次写死，使得“剩余”至少有可能成为数学对象，而不只是 dashboard 手工活。 【repo/scripts/build_hypercube_schema_20260623.py:L155-L179】【repo/scripts/build_hypercube_schema_20260623.py:L188-L265】

但仓库同样非常明确地说：当前能证明的也仅止于此。zero-GPU audit 只证明 `q4 × token_pos4` 在三份 smoke raw 上 `16/16` cell 非空，最小 cell 计数 `324`；同时还示范了一个坏轴：把 `audit_block_id` 当主轴会被判成 `rejected_sparse_high_dimensional_axis`。这正是一个负对照例子：**维度不是越高越好，越高越可能只是噪声与自由度膨胀。** 【repo/docs/infra/math_turn_20260622/Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.md:L15-L18】【repo/docs/infra/math_turn_20260622/Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.md:L22-L54】

还有一点必须说清：当前 bundle 的确已经包含 `scripts/q4_full_panel_foldlocal_analysis.py`，而且 `highorder_raw_logprob_panel.py` 也已经加入了 `--full-panel-dry-run` 与显式 PI approval token 守卫；但这只说明**工程闸门被搭好**，不说明 full panel 已运行。生成器要求 `--full-panel-approval-token PI_APPROVED_Q4_FULL_PANEL`，没有这个 token 会在载入 checkpoint 之前直接拒绝。dry-run 工件只会记录 `full_panel_generated=false`、`no_checkpoint_loaded=true`。因此，当前最强表述仍然只能是“已具备 future analysis path”，不能是“已有现象”。 【repo/docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md:L11-L22】【repo/docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md:L68-L90】【repo/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py:L272-L283】【repo/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py:L480-L500】

## 候选对象的形式化定义

### Mode A 自由数学定义

令 \(X=A_1\times\cdots\times A_d\) 是预注册的有限乘积空间，\(w:X\to(0,1]\) 是正权重且 \(\sum_{x\in X}w(x)=1\)。定义带权 Hilbert 空间
\[
H_w=\mathbb R^X,\qquad
\langle f,g\rangle_w=\sum_{x\in X}w(x)f(x)g(x).
\]
这是整个问题的 carrier。若 carrier、weights、nuisance 不是先固定的，那么后面的“剩余”都不具备对象同一性。对 functional ANOVA / Hoeffding 型分解来说，唯一性本来就要求参考分布先被指定；不先固定分布或权重，谈“哪个交互项是真的”在数学上就是偷换对象。 【repo/scripts/build_hypercube_schema_20260623.py:L182-L265】 citeturn2view0

对于两轴情形 \(X=Q\times B\)，定义严格加性 nuisance 子空间
\[
\mathcal A
=
\{\mu+\alpha(q)+\beta(b)\,:\,\mu\in\mathbb R,\ \alpha:Q\to\mathbb R,\ \beta:B\to\mathbb R\}.
\]
定义交互场
\[
I=\Pi_{\mathcal A^\perp,w}K.
\]
若 \(K\) 是 cell-mean 场，则 \(I\) 是“去掉所有带权可加主效应之后”的剩余。对 \(4\times4\) 情形，\(\dim \mathcal A=7\)，所以 \(\dim\mathcal A^\perp=9\)。这正是当前 schema 已经固定下来的 16-cell interaction carrier。若目标更保守，也可用仓库的 `mandatory_nuisance_space`，那会只去掉常数项、q4 slope 与 pure position main effects，留下 \(11\) 维残差；但如果你的哲学要求是“把标量、主效应与明显坐标自由度都剥掉”，那么这 \(11\) 维版本太松，应该优先用 \(9\) 维严格加性补空间。 【repo/scripts/build_hypercube_schema_20260623.py:L223-L240】

更一般地，对 \(d\)-维超立方体，真正严肃的对象不是原函数 \(K\)，而是商空间类
\[
[K]\in H_w/\mathcal N,
\]
其中 \(\mathcal N\) 是**看 outcome 之前就固定**的 nuisance 空间。一个足够严格的 \(\mathcal N\) 不仅应包含全局均值、各轴主效应，还应包含注册过的 generation 平滑项、seed baseline、matched mean/slope 模板、以及任何 decode-policy 诱导的伪结构模板。代表元的规范化选择是最小范数残差
\[
R=\Pi_{\mathcal N^\perp,w}K.
\]
如果 \(R\approx0\)，对象不存在；如果 \(R\neq0\) 但所有 checkpoint 只是在同一个固定模板上缩放，那么它仍然只是“单形状标量阴影”，不是真正多方向结构。这里的核心不是残差非零，而是**残差是否通过对象级稳定性审计**。这与 functional ANOVA 的“先固定分布，再唯一分解”的原则同源。 citeturn2view0turn4search4

多尺度稳定性必须被定义为算子，而不是口头直觉。若 \(\rho:X_f\to X_c\) 是粗化映射，定义带权条件期望型粗化算子
\[
(C_\rho f)(y)=\frac{1}{w_c(y)}\sum_{\rho(x)=y}w_f(x)f(x),\qquad
w_c(y)=\sum_{\rho(x')=y}w_f(x').
\]
真正严肃的问题不是“细网格上有非零残差吗”，而是
\[
C_\rho\,\Pi_{\mathcal A_f^\perp}K_f
\stackrel{?}{\approx}
\Pi_{\mathcal A_c^\perp}\,C_\rho K_f.
\]
若二者相差很大，说明所谓结构高度依赖分箱选择；若粗化后直接消失、翻号或主子空间大幅旋转，则那不是稳定对象，而是 partition artifact。你要的“多尺度 coarsening/refinement”本质上就是一个投影—粗化对易性问题。 【repo/docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md:L62-L66】

把 panel 整体看成张量最自然。若有全 panel，则令
\[
R\in \mathbb R^{S\times G\times Q\times B},
\]
其中 \(S\) 是 seed，\(G\) 是 generation，\((Q,B)\) 是结构轴。此时 CP 分解把张量表示为有限个 rank‑1 张量之和，Tucker 分解则是高阶 PCA。若实证中 \(R\) 基本就是 rank‑1 或某个固定 cell 模板乘上一个单一标量轨道，那么所有丰富叙事都应降格为一维幅度变化，而不应再讲“多向场”或“高阶矛盾动力学”。这类判别正适合用 CP/Tucker、矩阵 flattening 的奇异值谱、以及跨 seed 的 principal angles 来做。 citeturn2view1turn2view2turn2view3

若把局部解释看成覆盖 \(\{U_\alpha\}\) 上的局部截面，那么 sheaf 语言**只有在你真的定义了重叠一致性误差时**才有价值。具体可定义局部拟合残差 \(R_\alpha\)，在重叠处计算
\[
\delta_{\alpha\beta}=R_\alpha|_{U_\alpha\cap U_\beta}-R_\beta|_{U_\alpha\cap U_\beta},
\]
再在三重交上检查 cocycle 误差。若所有局部残差在重叠处都可一致 glue，那么 sheaf 语言没有增量；若在局部看似解释得很好，但 overlap 上持久不一致，那才叫 gluing obstruction。所谓“矛盾”若要脱离隐喻，最适合落在这里。Sheaf 的数学核心本来就是“局部相容数据能否唯一拼成全球对象”。 citeturn2view4

### Mode B 与 MaoField 当前工件相容的定义

与当前 bundle **直接相容** 的定义只有三类。第一类是 q4 mean-null / slope-orth residual：
\[
u_i=P_\perp k_i,\qquad
r_i=u_i-\langle v,u_i\rangle_w v.
\]
这在当前脚本中已经被正式写成 audited object，并配有 LOSO、matched-mean、rank/noise、random projection multiplicity gate。第二类是 16-cell strict-additive interaction：
\[
I_i=\Pi_{\mathcal A^\perp,w}K_i,
\]
其中 \(K_i\) 是一个 checkpoint 的 16-cell mean-logprob 向量。第三类才是更强的 panel-tensor / path-space 对象；但这些目前**没有真实 full-panel 工件**，只能作为未来定义。 【repo/scripts/q4_full_panel_foldlocal_analysis.py:L223-L247】【repo/scripts/q4_full_panel_foldlocal_analysis.py:L250-L558】【repo/docs/infra/gpt_deep_research/FUTURE_MATH_OBJECTS_INTERACTION_FIELD_ADOPTION_NOTE_20260623.md:L27-L44】

在 MaoField 证据边界里，以下五个“哲学着陆点”是可以 operationalize 的：**contradiction** = 非加性 interaction、非对易投影—演化或 gluing obstruction；**essence** = 商空间里 survive 的残差；**mediation** = outcome-independent 的轴或投影算子；**totality** = 固定产品空间、固定权重、固定 nuisance、固定负对照的整体 protocol；**motion** = quotient/tensor space 中的 generation path。任何超出这些的说法，在当前项目里都只能算隐喻，不能补证据缺口。 adoption note 已经把这一点写死：philosophical language 只能当 inspiration，不能当 proof。 【repo/docs/infra/gpt_deep_research/FUTURE_MATH_OBJECTS_INTERACTION_FIELD_ADOPTION_NOTE_20260623.md:L39-L53】

## 定理候选与可证伪命题

### 有限维事实

**命题甲：带权加性—交互分解存在且唯一。**
设 \(X=Q\times B\)，权重 \(w_{qb}>0\)。则任意 \(K\in H_w\) 都可唯一分解为
\[
K=\mu+\alpha(q)+\beta(b)+I,
\qquad I\in \mathcal A^\perp.
\]
并且 \(I=0\) 当且仅当 \(K\) 在带权意义下完全可加。对 \(|Q|=m,|B|=n\)，有
\[
\dim \mathcal A=m+n-1,\qquad
\dim \mathcal A^\perp=(m-1)(n-1).
\]
这不是哲学命题，只是有限维正交投影。对当前 `4×4` 情形，交互补空间维数正好是 \(9\)。 【repo/scripts/build_hypercube_schema_20260623.py:L223-L240】 citeturn2view0

**命题乙：若残差在 checkpoint×cell flattening 后是 rank‑1，则所有“复杂动态”都退化为单形状标量轨道。**
设 \(R_i\in \mathcal A^\perp\subset\mathbb R^{16}\)，把各 checkpoint 的 \(R_i\) 叠成矩阵 \(M\in\mathbb R^{N\times16}\)。如果 \(\mathrm{rank}(M)=1\)，则 \(R_i=c_i u\) 对某个固定模板 \(u\) 与标量系数 \(c_i\) 成立。于是任何与 cell basis 的正交更换无关的统计描述，最终都只能归结为系数路径 \(\{c_i\}\) 与固定模板 \(u\) 的稳定性。换言之，**rank‑1 不是“弱场”，而是“不够资格叫多方向结构”**。这就是为什么当前 smoke 的 \(\sigma_2/\sigma_1\) 低到约 `0.13` 时，最合理的默认解释是“几乎固定模板 + 小幅度变化”，而不是高维交互动力学。 【repo/docs/infra/math_turn_20260622/Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.md:L44-L60】【local reproduction local_test.json:L217-L255】 citeturn2view2

**命题丙：若粗化算子与投影算子近似对易，则细尺度残差才有资格称为粗尺度对象的 refinement。**
设 \(C_\rho:H_f\to H_c\) 是带权粗化算子，\(\Pi_f,\Pi_c\) 是 fine/coarse nuisance 空间的正交补投影。若
\[
C_\rho\Pi_f=\Pi_c C_\rho,
\]
则细尺度残差粗化后与粗尺度残差一致；若对易性失败，则失败本身就构成“分箱依赖”的证据。这个判别比单看细尺度非零更强，因为它把“对象是否跨分辨率同一”变成了可检验算子恒等式。仓库当前已经把 coarsening/refinement check 列为未来 hypercube analysis 的必需 gate，这个方向是完全对的。 【repo/docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md:L62-L66】

**命题丁：投影—演化对易子是“nuisance 是否被动力学混入”的最简证据。**
设 \(T\) 是 generation 演化算子，\(\Pi\) 是固定 nuisance 去除投影。若 \(T\) 保持 nuisance 子空间及其正交补不变，则
\[
[\Pi,T]=\Pi T-T\Pi=0.
\]
只要 \([\Pi,T]\neq0\)，就说明“先去 nuisance 再演化”与“先演化再去 nuisance”不是同一件事。这并不自动说明存在深刻结构；但它至少说明 dynamics 与 decomposition 不可分离，从而 scalar‑first 叙事不再充足。若将来要把“motion”做实，这个对象比口头谈“生成轨迹很复杂”强得多。 citeturn2view3

### 猜想与严格可证伪命题

**猜想戊：稳定非标量结构若存在，则必在某个 preregistered product partition 上同时通过四类门槛。**
它必须同时满足：残差幅度高于 noise floor；\(\sigma_2/\sigma_1\) 不低于 registered threshold；跨 seed 主子空间角稳定；并且优于 random equal-size partitions / within-q shuffles / same-dimension random subspaces 的经验零分布。缺一项都不算。当前 bundle 只支持把这些写成 future gate，不支持宣布它们已经通过。 【repo/docs/infra/gpt_deep_research/FUTURE_MATH_OBJECTS_INTERACTION_FIELD_ADOPTION_NOTE_20260623.md:L89-L117】【repo/scripts/q4_full_panel_foldlocal_analysis.py:L430-L536】

**猜想己：若所有 admissible residual 在这些门槛下都失败，则复杂崩塌叙事可被统一降格为投影或坐标制品。**
更严格地说，若对每个 preregistered \((X,w,\mathcal N)\)，残差 \(R=\Pi_{\mathcal N^\perp}K\) 都满足以下至少一条：\(R\approx0\)；低于 noise floor；flattening 近 rank‑1；不能优于 random-axis/null；在 coarsen/refine 下翻号或消失；则“复杂 collapse narrative”不再是被证据识别出来的对象，而只是某个 metric projection 或 coordinate artifact。这个猜想一旦证成，负面结果会比“没找到正结果”更强。它会给出一张**反对象存在性证明模板**。 【repo/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:L83-L85】【repo/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:L131-L153】

## 零GPU杀测套件与升格前数据要求

### 零GPU杀测套件

当前仓库已经为 q4 residual-field 提供了一个雏形：LOSO 弱增益门槛、matched-mean 稳定性、rank/noise、random mean-null projection guard。对你要求的 16-cell interaction field，我建议把它升级成**更残忍的 kill suite**，而不是更宽松的探索套件。q4 脚本里的现成阈值可作为最低参考：`delta_r2 >= 0.02`、单侧 permutation `p <= 0.10`、matched sign stability 至少 `0.70` 且 `|z| >= 2.58`、`sigma2/sigma1 >= 0.25`，并要求残差幅度高于 `2 × max(seed-bootstrap p90, rank1-control p90)`。这些阈值目前是对 q4 residual-field 的；interaction hypercube 若要升格，至少不能比它更松。 【repo/scripts/q4_full_panel_foldlocal_analysis.py:L250-L270】【repo/scripts/q4_full_panel_foldlocal_analysis.py:L348-L397】【repo/scripts/q4_full_panel_foldlocal_analysis.py:L430-L477】

我建议的 zero‑GPU kill suite 如下。它们不是“如果过了就算发现”，而是“不过就立刻杀”：

| 杀测 | 统计对象 | 直接 kill 条件 | 作用 |
|---|---|---|---|
| 严格加性湮灭 | \(I=\Pi_{\mathcal A^\perp,w}K\) | \(\|I\|_w\) 落入 noise floor | 先排除“只是主效应没减干净” |
| matched mean / matched slope 双匹配 | 配对残差方向 | 在匹配 \(D\) 与 slope 后方向不稳 | 排除标量与 slope 伪影 |
| random equal-size partition null | 随机 token-position 分箱 | 真轴不优于随机分箱 null | 排除分箱挑选偏差 |
| within-q shuffle null | q 内位置标签打乱 | 交互统计不显著下降 | 排除 cell 算法结构伪影 |
| bad-axis null | `audit_block_id`、随机等维轴 | 坏轴也能做出“信号” | 证明对象只是高维自由度 |
| same-dimension subspace guard | 随机 \(9\) 维残差子空间 | 真子空间不优于随机同维子空间 | 排除 multiplicity 游戏 |
| rank/noise gate | flattening 奇异值谱 | \(\sigma_2/\sigma_1\) 低、幅度低于 floor | 排除 scalar shadow |
| coarsen/refine gate | \(C_\rho\Pi_f - \Pi_c C_\rho\) | 残差在分辨率改变下消失或翻号 | 排除 partition artifact |
| principal-angle stability | seed 间主子空间角 | 角度大、方向翻转 | 排除 seed-local 偶然性 |
| gluing obstruction sanity | overlap 上局部残差差异 | 所谓障碍可被局部 nuisance 完全吸收 | 防止 sheaf 语言空转 |

这些 kill test 与仓库当前 claim boundary 完全一致：只要有一项失败，最强结论也只能是 `killed`、`invalid_artifact` 或 `insufficient_artifact`，不能偷渡成“弱阳性”。 【repo/docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md:L19-L22】【repo/docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md:L62-L66】【repo/scripts/q4_full_panel_foldlocal_analysis.py:L539-L558】

### 升格前的精确数据要求

在 moving beyond smoke feasibility 之前，我认为必须具备下列**精确工件**，否则一律不许升格。

第一，必须有**真实 full panel**，不是 dry-run，不是 smoke，不是 manifest-only。当前仓库已经把 full panel 计划固定为 `5 seeds × 10 generations = 50 checkpoints`，而且 dry-run 工件会记录 `checkpoint_count=50`、`full_panel_generated=false`、`no_checkpoint_loaded=true`。真正缺的不是“定义”，而是**已生成的 50 个 checkpoint 的 raw JSONL 与 aggregate**。 【repo/STATE.md:L16-L27】【repo/docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md:L111-L136】【repo/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py:L480-L500】

第二，必须保留 token-level raw 字段，而不是只留 cell means。仓库当前 q4/hypercube schema 已经把关键字段写得很清楚：`schema_id`、`seed`、`generation`、`source_split`、`audit_block_id`、`token_pos`、`flat_token_index`、`target_token_id`、`target_count_audit_blocks`、`slice_id`、`token_logprob`、`neg_logprob`。没有这些字段，就无法做 coarsening、within-q shuffle、cell variance/noise model、以及不同 partition 的 determinisitic re-aggregation。 【repo/scripts/q4_hypercube_zero_gpu_audit.py:L30-L43】【repo/docs/infra/gpt_deep_research/deep_research_q4_hypercube_extension_strict_math_audit_20260623.md:L164-L176】

第三，必须把多尺度对象做成**同一 raw 上的确定性派生**，而不是分别跑不同实验。也就是说，`q2/q4/q8` 与 `tokenpos2/4/8` 都必须由同一批 raw JSONL 经过 source-only builder 派生出来，从而让 coarsening/refinement 真正成为算子比较，而不是 cross-run 比较。否则“多尺度稳定性”根本无从定义。当前仓库已经在 hypercube extension gate 中把 coarsening/refinement 列成 future requirement，这一步不能省。 【repo/docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md:L62-L66】

第四，必须有一个**独立于生成器的 hypercube analysis 脚本**。现有 `q4_full_panel_foldlocal_analysis.py` 只处理 q4 residual-field，不处理 16-cell interaction field。它的存在说明“单独分析路径”这个工程哲学是对的，但 interaction hypercube 需要自己的版本，至少实现：fold-local projection、matched mean/slope、same-dimension random subspace guard、equal-size random partition null、within-q shuffle null、coarsen/refine commutator、rank/noise 与 subspace-angle 稳定性。没有这一步，interaction 线永远只有 smoke memo。 【repo/scripts/q4_full_panel_foldlocal_analysis.py:L1-L11】【repo/docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md:L62-L90】

第五，必须保留当前的 wording guard，并提前把所有 summary 模板锁死。因为这个项目最危险的不是“没数学”，而是“剩下一点小 residual 就被叙事抢跑”。从 STATE、implementation gate、zero-GPU audit 到 adoption note，仓库已经把这条线立得很直；继续研究时唯一正确的姿态不是“给对象留面子”，而是“先给对象准备刑具”。 【repo/STATE.md:L24-L27】【repo/docs/infra/math_turn_20260622/Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623.md:L55-L77】【repo/docs/infra/gpt_deep_research/FUTURE_MATH_OBJECTS_INTERACTION_FIELD_ADOPTION_NOTE_20260623.md:L101-L117】

## 反夸大表与去品牌化问题陈述

在当前 bundle 里，哪些说法被允许、哪些被阻断、哪些已经应当直接判假，边界其实非常清楚。下面这张表不是我的情绪，而是把仓库的 claim policy 翻成更严格的研究语言。 【repo/STATE.md:L16-L27】【repo/docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md:L123-L136】【repo/docs/infra/math_turn_20260622/Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.md:L56-L65】【repo/docs/infra/gpt_deep_research/FUTURE_MATH_OBJECTS_INTERACTION_FIELD_ADOPTION_NOTE_20260623.md:L101-L117】

| 句子 | 状态 | 严格判定 |
|---|---|---|
| “MaoField 目前是一个 negative-centered measurement-audit 结果。” | allowed | 对 |
| “旧对象是标量 KL/EMA smoother，因此数学转向必须拒绝 scalar completion。” | allowed | 对 |
| “`Q_freq4 × B_tokenpos4` 是一个已锁定的 formal-prereg coordinate system。” | allowed | 对 |
| “16-cell interaction residual 是目前最强的 future math candidate。” | allowed | 对，但仅限 design judgment |
| “现有 smoke raw 可复算出小的 interaction residual。” | allowed | 对，但只能说 smoke-derived calculation |
| “这已经证明了稳定非标量结构。” | false | 现证据不支持 |
| “hypercube interaction field observed。” | blocked / 现阶段等价于 false | adoption note 明示禁止 |
| “LOSO passed。” | blocked | 没有相应 primary artifact |
| “F3 positive。” | blocked | 仓库反复写明不是正发现 |
| “glass box broken。” | false | 现有综合结论明确否定 |
| “training authorized / new loss authorized。” | false | 工程与文档都明示未授权 |
| “哲学语言本身完成了证据桥接。” | false | adoption note 明示 philosophy 只能 inspiraton |

最终，去掉 MaoField 品牌、叙事、历史包袱之后，真正留下来的底层数学问题可以写成下面这句。我认为这才是这次研究的净产出。

**去品牌化的底层问题陈述：**
给定一个预注册的有限带权乘积划分 \(X=\prod_{j=1}^d A_j\)、一个正权重 \(w\)、以及一个在 outcome 观测前固定的 nuisance 子空间 \(\mathcal N\subset \mathbb R^X\)，再给定一组沿参数或时间索引 \(t\) 的观测场 \(K_t\in\mathbb R^X\)。判定是否存在一个非平凡对象
\[
R_t=\Pi_{\mathcal N^\perp,w}K_t
\]
使其同时满足：高于噪声地板、不是 rank‑1 scalar shadow、优于随机同维子空间与随机分箱的零模型、并在预注册 coarsening/refinement 下保持稳定。若不存在，则证明任何“复杂结构”叙事都可降格为标量投影、低秩模板或坐标制品；若存在，则刻画该对象揭示的限制究竟是非加性交互、非对易演化，还是局部解释无法 glue 成全局解释。这个问题与 MaoField 无关；MaoField 只是把它暴露出来的失败试验。 【repo/docs/infra/gpt_deep_research/FUTURE_MATH_OBJECTS_INTERACTION_FIELD_ADOPTION_NOTE_20260623.md:L27-L53】【repo/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:L83-L85】【repo/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:L131-L153】 citeturn2view0turn2view2turn2view3turn2view4