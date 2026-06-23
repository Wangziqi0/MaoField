# MaoField 之后值得追的数学对象

## 材料地图

**模式 A 自由发现。**
从材料的整体结构看，MaoField 现在最有价值的，不是某个“已成事实的突破”，而是一组被不断压缩、剥皮后留下来的问题骨架：怎样在一个固定的、可复核的离散划分上，把“标量平滑”“单调斜率”“坐标膨胀”“事后讲故事”全部剥掉之后，还能剩下一个真正的、可识别的非标量对象。换句话说，材料最强的启发不是“再加轴”，而是“找一个在商空间里仍然活着的剩余结构”。这正是后来 functional ANOVA / Hoeffding 型分解、交互项、以及更高阶的一致性/拼接障碍等语言最自然接入的位置。citeturn3search0turn3search15turn2search1

**模式 B 证据门禁。**
上传 bundle 自己已经把证据边界写得很死：它是可移植上下文包，不是新实验，不是正结果，不替代一手证据；RAG/index/digest 只能当定位器，代码、JSON/JSONL、verdict markdown、显式 logs 才是证据。bundle 明确包含 `STATE.md`、研究索引、markdown catalog、`docs/infra`、相关脚本、`exp019` 与 `exp020` 的记录，以及 **3 份** `wip_data/maofield_panel_primary_20260622/raw/*.jsonl` smoke token panel；并且明写当前 q4 hypercube 结果只允许 `formal_prereg_only`，不得声称 `glass box broken`、`residual field observed`、`LOSO passed`、`F3 positive`、`mathematical breakthrough`，也不得声称 full 50-checkpoint panel 已批准或已运行。 （本地档案：`README_FOR_GPT55_PRO_20260623.md:8-15,18-31,33-42,57-63`）

项目状态文件与研究索引把当前局面进一步压实了：MaoField 当前的总研究综合仍是 **negative-centered**；`exp020` 的收口是 **C(meta-pattern)**，即“想独立于 PPL 的候选 collapse 指标，大多又塌回 PPL/logit 兄弟、seed 噪声地板或 decode 混淆”；F3 只是“值得追的弱例外”，不是正发现；q4 线的当前状态是：已有 schema、smoke、implementation gate、zero-GPU hypercube feasibility audit，但 **没有** real q4 full panel、没有训练授权、没有 new loss 授权、也没有强数学 claim 的通过。`STATE.md` 还明确说 q4 hypercube extension 的本地 verdict 是 `formal_prereg_only`，只说明 `q4 × token_pos4` 的 16/16 cell 非空，最小 cell 计数是 324，而不是科学结果。 （本地档案：`repo/STATE.md:16-17,22-27,84-86`；`repo/GPT55_PRO_RESEARCH_INDEX_20260622.md:43-46,126-136,320-340,422-429`）

材料还分成几条不同性质的线。旧经验线属于 `exp019`/`exp020` 的 empirical pilot，当前只能支持“若干候选度量失败或被压扁”的负结果综合；q4 residual-field 线把“真正该审的对象”收紧到 `r_i = u_i - <v,u_i>_w v` 及其 fold-local 版本，但这是 **审计目标**，不是已观测结果；q4 hypercube 线则把该对象延伸到 `Q_freq4 × B_tokenpos4` 的有限乘积划分，会谈到 nuisance subspace、occupancy、source-only axis 等，但本地裁定仍只是零 GPU 的形式预注册可行性。哲学/辩证材料则主要位于 `README`、`README_zh`、早期 `exp017_dialectics` 档案与 philosophy 文档中；它们提供的是生成性直觉，不是证据。 （本地档案：`repo/README.md:12-16,32-42,90-91,152-152`；`repo/docs/infra/gpt_deep_research/Q4_RESIDUAL_FIELD_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md:17-34,58-73`；`repo/docs/infra/gpt_deep_research/Q4_HYPERCUBE_EXTENSION_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md:18-35,57-72`）

## 旧项目当前不能支持什么

**模式 A 自由发现。**
如果把“研究直觉”“项目叙事”“PI 愿望”全部放到一边，直接看对象层面，那么旧项目当前最鲜明的失败，其实是 **identification failure**：现有对象不是在问“有无新的结构”，而长期在问“某个标量影子能否被重讲为新的结构”。一旦把均值模、单调斜率、generation 趋势、mean-PPL 联动拿掉，旧 framing 很大概率只剩 dashboard 的坐标选择。这个失败不是坏消息，反而是最干净的出发点：它迫使我们寻找一个以“删尽主效应和弱 nuisance 后仍不消失”为定义的对象。 （本地档案：`repo/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:27-50,83-85,124-153`）

**模式 B 证据门禁。**
MaoField 当前**不能**支持的东西，材料写得极其明确：不能说 full q4 panel 已运行；不能说 training 已授权；不能说 new loss 已授权；不能说 `LOSO passed`、`F3 positive`、`mean-null vector field survives`、`residual field observed`、`glass box broken`。runbook 甚至规定：即使所有 gate 都通过，最强允许表述也只有 “eligible for next design review only”。这不是我额外加门槛，而是仓库自己锁死的上界。 （本地档案：`repo/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:15-24,210-241,255-315`；`repo/docs/infra/math_turn_20260622/Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.md:8-18,56-65`；`repo/docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md:86-99`）

更关键的是，当前 `Q_freq4 × B_tokenpos4` 还只是**坐标系对象**，不是现象对象。`build_hypercube_schema_20260623.py` 做的事，是固定 q4 频率轴、从 `token_pos` 派生出 4 个 coarse position bins、记录 16 个 cells 的 source-only occupancy、给出 mandatory nuisance space 与 claim policy；`q4_hypercube_zero_gpu_audit.py` 做的事，是在 **已有 3 份 smoke raw JSONL** 上检查字段、occupancy、cell counts 与不得复活的 blocked claims，最终只可能输出 `formal_prereg_only`。这些都是非常有价值的 **预注册工程**，但还不是“观察到某个 hypercube residual”的证据。 （本地档案：`repo/scripts/build_hypercube_schema_20260623.py:2-7,56-78,150-181,188-240,250-265`；`repo/scripts/q4_hypercube_zero_gpu_audit.py:2-6,30-53,165-241,316-343`）

同样，当前 q4 主对象本身也仍然非常瘦：`highorder_raw_logprob_panel.py` 生成的是每个 checkpoint 的 q4 切片均值 `k_j = mean_logprob(slice_j)`，然后计算加权均值模 `D`、mean-null 向量 `u` 以及单一有序频率斜率投影 `P`。它可以做 manifest-only、one-checkpoint smoke、full-panel dry-run，也可以在拿到 **PI approval token** 的前提下进入 guarded `--full-panel` 路径；但已有证据里并没有产生 real q4 full-panel aggregate。换言之，当前 MaoField 真实落地的是**观测管线和闸门**，不是证实了新数学结构。 （本地档案：`repo/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py:2-12,90-105,136-179,272-323,480-540`；`repo/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_SMOKE_20260622.md:8-17,125-148`；`repo/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_MULTI_SMOKE_20260622.md:9-11,51-53`）

## 对 PI 的超立方体与哲学直觉的重建

**模式 A 自由发现。**
我认为 PI 的原始直觉，如果用最强的数学愿望来重建，并不是“把 q4 变成 q4×q4×q4”，也不是“把辩证法翻译成更多坐标轴”。它更像是下面这个愿望：存在一个**非标量障碍**，它在全局平均、单调频率斜率、generation 光滑趋势、甚至某些主效应都被删去之后，仍然作为一个 **不能被加法分解、不能被单一路径吸收、不能被任意换坐标抹平** 的对象存在。这个对象如果是静态的，它会表现为加权乘积划分上的交互残差；如果是动态的，它会表现为 transport/path dependence/hysteresis；如果是范畴/层论语言，它会表现为 local models 的 gluing failure；如果是算子语言，它会表现为某两个“本应兼容”的操作不交换。 （本地档案：`repo/README.md:32-42,90-91,152-152`）

“Dialectical fusion should emerge from motion rather than be externally imposed” 这句话若做最节制的数学翻译，等于说：你不想把对象定义成一个先验加上去的 penalty，也不想把它定义成某种 pre-labeled contradiction score；你想要的是一个**从运动与比较中生成出来的剩余量**。这会自然排斥“纯标量完成”，也会自然偏向 residual、holonomy、gluing obstruction、non-commutation 等对象。也就是说，PI 直觉的核心不是多维，而是 **quotient 之后仍然不为零**。 （本地档案：`repo/README.md:152-152`；`repo/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:83-85,89-112`）

**模式 B 证据门禁。**
但从仓库证据能严格支持的层面说，当前材料真正已经写进本地约束的愿望更窄：`EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md` 明确要求“refuse scalar completion”，去问 mean-null subspace 里有没有稳定 residual；residual-field adoption note 则把 q4 的 true object 压实成 `r_i = u_i - <v,u_i>_w v` 以及其更严格的 fold-local scalar-slope residual；hypercube adoption note 又进一步要求：若延展到乘积划分，轴必须 outcome-independent，权重必须 source-only，nuisance subspace 必须在看 outcome 前就固定。于是，能从材料中合法重建出来的最强愿望不是“某种哲学真理已在代码中显现”，而是“请给我一个固定商空间里的剩余对象，并证明它不是坐标膨胀”。 （本地档案：`repo/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:83-85,131-153`；`repo/docs/infra/gpt_deep_research/Q4_RESIDUAL_FIELD_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md:17-34`；`repo/docs/infra/gpt_deep_research/Q4_HYPERCUBE_EXTENSION_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md:20-35`）

## 候选数学对象

**模式 A 自由发现。**
下面我不给“最好听”的对象，而给**彼此 genuinely 不同**的五类对象。它们共享一个标准：都试图把“非标量剩余量”做成明确的数学对象；但它们对 identifiability、falsifiability、与现有 MaoField 数据的贴合程度差别很大。功能 ANOVA/Hoeffding 型分解给出“主效应 vs 交互项”的自然商空间；sheaf 一致性半径给出“局部模型为什么拼不成全局模型”的语言；principal angles/Grassmann 距离给出“残差子空间随路径如何转动”的语言；信息几何给出“概率族与投影的曲率/联络”语言。citeturn3search0turn3search15turn4search2turn4search5turn2search7

**模式 B 证据门禁。**
表中的 “现有 MaoField 状态” 一栏严格区分三种情况：**可部分测试**、**仅能受现有数据启发**、**被当前数据阻断**。凡是需要 real full-panel 或需要当前脚本还未输出的新 aggregate 结构，我都不会写成“已观测结果”。 （本地档案：`repo/STATE.md:22-27`；`repo/docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md:7-23,97-99`）

| 方向 | 形式定义 | 环境空间 | nuisance / 不变性商 | 可观测或可估量 | 非平凡命题 | 快速杀死方式 | 现有 MaoField 状态 |
|---|---|---|---|---|---|---|---|
| **加权乘积划分交互场** | 对每个 checkpoint \(i\)，定义 \(K_i(q,b)\) 为 cell mean logprob；取 \(I_i=\Pi_{A^\perp_w}K_i\)，其中 \(A\) 为常数项 + 频率主效应 + 位置主效应的加权可加子空间 | \(\mathbb R^{Q\times B}\) 或 \(H_Q\otimes H_B\) | 去掉所有加权可加主效应；若 \(I_i\neq 0\)，则存在非加性耦合 | cell means、\(\|I_i\|_w\)、奇异值比、matched contrasts | 唯一加权分解存在，且 \(I_i=0\iff K_i\) 可加；若 panel 稳定，则可给出真正的交互定理 | 随机 position 分箱同样强；或 full-panel 下 \(\sigma_2/\sigma_1\) 很低、matched sign 不稳、LOSO 解释完 | **可部分测试**。现有 3 份 smoke raw JSONL 足以做占用与单点交互分解，但不足以做 panel 稳定性结论 |
| **q4 斜率正交残差场** | \(r_i=u_i-\langle v,u_i\rangle_w v\)；更严格的是 fold-local 版本，去掉 \(\alpha(D,g,g^2)v\) | q4 mean-null 子空间 \(\mathcal R\subset\mathbb R^4\) | 去掉均值模与锁定主斜率 | \(\|r_i\|_w\)、rank/noise、held-out residuals | 若在 fold-local 下仍有超噪声二维残差，则 q4 不是纯标量影子 | rank-1 control、mean-only control、matched-mean fail、random projection fail | **MaoField 现成审计方向**，但当前仍缺 real full-panel 结果来裁决 |
| **局部模型的 sheaf 拼接障碍** | 给每个 seed / generation / matched-pair 局部 chart 一个局部可加模型；若重叠处 restrictions 不一致，则得到 consistency radius / cohomological obstruction | 覆盖上的 sheaf of local additive models | 全局模型存在性按 gluing 判定；障碍非零即“局部可解释但全局不一致” | consistency radius、局部-全局残差差异 | 非零障碍即不存在统一全局可加解释；可解释“局部看似稳定，整体却拼不上” | 若所有局部 charts 可一致拼接，则此方向失去独立意义 | **仅受当前数据启发**。需要更完整 panel 与明确 overlap 设计。sheaf 语言本身是数学研究方向。 citeturn4search2turn2search6 |
| **交互子空间的 holonomy / hysteresis** | 取每个 generation 上 \(I_i\) 的主子空间 \(E_{s,g}\)，用 principal angles 比较 \(E_{s,g}\to E_{s,g+1}\)；回路面积或 holonomy 测 path dependence | Grassmann 流形上的子空间路径 | 对基底旋转不敏感，仅看子空间几何 | principal angles、loop area、seed-wise path mismatch | 若不同 seed 的路径几何稳定而非仅依赖 generation 标量，则出现真正 path-dependent object | 若所有路径都塌成单参数单调曲线，或角度完全被噪声主导 | **被当前数据阻断**。3 个 smoke 点远远不够。 citeturn4search5turn4search11 |
| **边缘化与演化的对易子** | 给定时间/代际预测算子 \(T\) 与结构投影 \(\Pi\)，定义 \(C=\Pi T-T\Pi\)；若 \(C\neq 0\)，则“先去 nuisance 再演化”与“先演化再去 nuisance”不同 | 有限维算子代数 | 对座标重参数化以共轭不变 | \(\|C\|\)、谱半径、特征向量 | 在 separable / additive 动力学下 \(C=0\)；持久非零意味着演化与结构分解不相容 | 若 fold-local 线性/多项式模型下 \(C\) 近零 | **仅受当前数据启发**。数学上漂亮，但现在太早 |
| **“加更多轴就更接近本质”的朴素超立方体** | 继续向 cell set 里堆轴 | 任意大离散乘积空间 | 几乎没有真正 quotient | 稀疏占用、更多坐标 | 没有好命题，只有自由度膨胀 | 任意随机轴也能“出东西” | **应拒绝**。这是坐标膨胀，不是对象 |

## 最佳候选

**模式 A 自由发现。**
我选的最佳候选不是最讨喜的 q4 residual field，也不是最华丽的 sheaf/holonomy 语言，而是 **加权乘积划分交互场**。原因很直接：它同时满足四个条件。第一，它比现有 q4 scalar carrier 深，因为它问的不是一个斜率，而是“可加主效应剥离后还剩什么”；第二，它比朴素 hypercube 干净，因为它把“增加坐标”重新定义为“进入商空间后是否仍有交互项”；第三，它比 sheaf/holonomy 更可识别，因为估计器就是加权最小二乘投影；第四，它与 MaoField 实际已有的 `Q_freq4 × B_tokenpos4` 原料贴得最近。它本质上是一个**有限产品划分上的、加权 Hoeffding/ANOVA 交互项**。citeturn3search0turn3search15turn2search1

**模式 B 证据门禁。**
我选它，不是因为 MaoField 已经证明了它，而是因为现有 bundle 至少已经提供了它所需的最小前提：固定 q4 频率轴、固定 `token_pos` 派生规则、16/16 非空 cells、明确禁止把 seed/generation 当结构轴、以及 source-only weights / nuisance policy 的初稿。相反，如果我现在选 holonomy 或 sheaf obstruction 作为最佳候选，那会明显超过现有数据支持度。 （本地档案：`repo/scripts/build_hypercube_schema_20260623.py:188-240,242-265`；`repo/docs/infra/math_turn_20260622/Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.md:17-18,22-53`；`repo/docs/infra/gpt_deep_research/Q4_HYPERCUBE_EXTENSION_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md:20-35`）

设 \(Q=\{0,1,2,3\}\) 是锁定的 q4 频率切片，\(B=\{0,1,2,3\}\) 是由 `token_pos` 通过
\[
b=\min\!\left(3,\left\lfloor \frac{(\text{token\_pos}-1)\cdot 4}{63}\right\rfloor\right)
\]
派生的 4 个位置桶。对每个 checkpoint \(i=(s,g)\)，定义 16-cell 张量
\[
K_i(q,b)=\text{checkpoint }i\text{ 在 cell }(q,b)\text{ 上的 mean logprob}.
\]
令 \(w_{qb}>0\) 为 source-only cell 权重，归一化到 \(\sum_{q,b}w_{qb}=1\)。环境空间是
\[
H:=\mathbb R^{Q\times B}
\]
并配加权内积
\[
\langle X,Y\rangle_w=\sum_{q,b}w_{qb}X(q,b)Y(q,b).
\]
定义可加 nuisance 子空间
\[
A=\Bigl\{\mu\mathbf 1 + a(q)+b(b)\ \bigm|\ \sum_q \bar w_q a(q)=0,\ \sum_b \bar w_b b(b)=0\Bigr\},
\]
其中 \(\bar w_q=\sum_b w_{qb}\), \(\bar w_b=\sum_q w_{qb}\)。最佳候选对象是
\[
I_i:=\Pi^{(w)}_{A^\perp}K_i.
\]
这是“频率主效应 + 位置主效应 + 常数项”全部删掉之后剩下的**交互场**。它比 MaoField 当前脚本里的 q4 slope residual 更狠，也因此更不 flattering。 （本地档案：`repo/scripts/build_hypercube_schema_20260623.py:56-78,150-181,188-240`；`repo/scripts/q4_hypercube_zero_gpu_audit.py:165-222`）

这个对象的最小定理和最小猜想可以分开说。**最小定理**：在所有 cell 权重均为正、轴分配与权重规则对所有 checkpoint 固定的前提下，每个 \(K_i\) 都有唯一的加权正交分解
\[
K_i=\mu_i\mathbf1 + a_i(q)+b_i(b)+I_i,\qquad I_i\in A^\perp_w.
\]
因此 \(I_i=0\) 当且仅当该 checkpoint 的 16-cell 结构在加权意义下完全可加。这个定理本身只是有限维线性代数，但它把“有无真正的非加性结构”变成了清晰的 yes/no 问题。**最小猜想**：如果 MaoField 在这个方向上真有值得继续追的非标量结构，那么在某个预注册乘积划分上，\(I_i\) 必须在 held-out seed 的 fold-local 审计下保持超噪声幅度，且不能被随机等 bucket-size 分箱、随机 mean-null 投影、或 generation-only nuisance 模型复制。 （本地推导；相关分解背景可类比 Hoeffding / ANOVA 交互项。 ） citeturn3search0turn3search15turn2search1

它的**零模型**应该写成
\[
K_i(q,b)=\mu_i+a_i(q)+b_i(b)+\varepsilon_i(q,b),
\]
并允许 \(\mu_i,a_i,b_i\) 进一步被 fold-local 的 \(D_i,g_i,g_i^2\) 或其他预注册 nuisance 参数化；也就是说，真实零假设不是“没有任何结构”，而是“所有结构都能被可加主效应与低阶 nuisance 吸收”。只有当 \(I_i\) 在这一零模型下仍然保留稳定、非 rank-1、非任意分箱的剩余部分时，这个方向才值得活下去。 （本地档案：`repo/scripts/q4_full_panel_foldlocal_analysis.py:250-330,430-475,496-557`）

它的**identifiability 条件**也很明确。必须同时满足：其一，所有 16 cells 在每个 checkpoint 上都有正计数；其二，轴规则 outcome-independent，不能事后根据效果重划 bin；其三，weights 固定为 source-only 计数权重；其四，seed/generation 保持 sample index 身份，不能被偷渡成结构轴；其五，full-panel 或其他足够重复的 panel 必须存在，才能做 fold-local 稳定性。少任何一条，这个对象都会退化成 dashboard 设计。 （本地档案：`repo/scripts/build_hypercube_schema_20260623.py:223-240,242-249`；`repo/docs/infra/gpt_deep_research/Q4_HYPERCUBE_EXTENSION_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md:20-35`）

它的**有限样本估计器**非常朴素：对每个 checkpoint，把 16 个 cell mean 组成向量 \(\hat K_i\)；对加权可加子空间 \(A\) 做加权最小二乘投影，得到
\[
\hat I_i=\hat K_i-\Pi^{(w)}_{A}\hat K_i.
\]
然后在 panel 上计算四个统计量：
\[
T_{\text{amp}}=\operatorname{RMS}(\hat I_i),\quad
T_{\text{rank}}=\sigma_2/\sigma_1\bigl([\hat I_i]_i\bigr),\quad
T_{\text{match}}=\text{matched-mean sign stability},\quad
T_{\text{rand}}=p\text{-value against random equal-size }B\text{ partitions}.
\]
只有当这四类指标一起过关，才允许进入 next design review；任何单项失败，都直接 kill。这个逻辑与现有 q4 residual-field 审计脚本已经使用的 LOSO、matched-mean、rank/noise、random projection guard 高度同构。 （本地档案：`repo/scripts/q4_full_panel_foldlocal_analysis.py:348-394,430-475,496-557,726-745`）

其**负控设计**我建议分成三层。第一层是 **随机位置分箱负控**：保持每个位置桶的格子大小不变，随机重排 `token_pos` 到 4 桶，检验真实 \(B_{tokenpos4}\) 的交互统计是否显著优于随机分箱。第二层是 **坏轴负控**：把 `audit_block_id` 作为候选新轴，应当由于稀疏高维而快速失败；现有 zero-GPU audit 已经把这点演示出来。第三层是 **局部打乱负控**：在每个 q slice 内随机打乱 `token_pos` 标签，若交互信号仍不降，则说明所谓“位置交互”只是 cell 数学伪影。 （本地档案：`repo/docs/infra/math_turn_20260622/Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.md:22-53`；`repo/scripts/q4_hypercube_zero_gpu_audit.py:165-222`）

它的**证明草图**很短：因为 \(H\) 是有限维加权内积空间，而 \(A\) 是线性子空间，所以 \(H=A\oplus A^\perp_w\) 唯一成立；于是 \(\hat I_i\) 是唯一的加权交互剩余项。真正的障碍不在数学定义，而在证据结构：MaoField 当前 full-panel q4 aggregate 脚本输出的是 4 个 q-slice，而不是 16 个 \((q,b)\)-cell；所以要真正测试这个最佳候选，需要的是**一个新的 full-panel hypercube aggregate artifact**，而不是拿旧 q4 aggregate 强拗。也就是说，理论对象很清楚，证据工件却还没生产出来。 （本地档案：`repo/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py:308-323,505-540`；`repo/scripts/build_hypercube_schema_20260623.py:188-240`）

我还做了一个**严格标注为派生、非正式**的小计算：直接读取 bundle 中现有三份 smoke raw JSONL，把每个 checkpoint 的 16-cell mean logprob 做成 \(4\times4\) 矩阵，并投影到“常数 + 频率主效应 + 位置主效应”的正交补。结果是：三个 checkpoint 的交互残差加权范数分别约为总 mean-null 16-cell 信号的 **10.0%**, **11.2%**, **10.9%**；三者的交互残差图样两两加权相关在 **0.95** 左右；但把三行 residual 堆成 \(3\times16\) 矩阵后，\(\sigma_2/\sigma_1\approx 0.15\)，显示它目前更像“形状相近但有效维度很低”的 smoke pattern，而不是 panel-level 稳定对象。这个结果对“有一点真实结构的可能性”是启发性的，但对“已经发现可生存交互场”是**不利的**。这恰好说明它是最佳候选：值得测，但不能吹。 （本地派生计算，原始数据文件：`wip_data/maofield_panel_primary_20260622/raw/smoke_seed1_generation0_token_panel.jsonl`、`smoke_seed2_generation5_token_panel.jsonl`、`smoke_seed42_generation9_token_panel.jsonl`；工件存在性见 `README_FOR_GPT55_PRO_20260623.md:28-29` 与 `repo/docs/infra/math_turn_20260622/Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.md:22-53`）

要真正测试它，所需的**精确数据工件**应当是下面二者之一。最理想的是一个新的
`q4_tokenpos4_full_panel_aggregate.json`，其中对每个 \((seed,generation)\) 行都保存：16 个 cells 的 `mean_logprob`、计数、方差、weights、raw JSONL hash、schema id、repo head、source hashes。次理想是 50 个 raw JSONL 文件加上固定 schema，然后在单独分析脚本里现场聚合。**现有**的 q4 aggregate 只有 4 个 q slices，不够测试这个对象。 （本地档案：`repo/scripts/q4_full_panel_foldlocal_analysis.py:128-141,175-199`；`repo/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py:505-540`）

## 不膨胀的哲学翻译

**模式 A 自由发现。**
如果一定要用哲学词，我建议只保留那些能被明确操作化的词。这里“矛盾”最好的数学对应不是“两个量反号”，而是**去掉全局主效应后仍然存在的非可加耦合**；“本质/现象”最好的对应不是神秘的深层结构，而是**主效应商空间与残余交互之间的区分**；“中介/媒介”最好的对应是**你通过哪个 outcome-independent 轴去检测某个频率效应是否发生非加性调制**；“总体性”最好的对应是**固定产品划分、固定 weights、固定负控与 fixed panel scope 的整体验证框架**；“过程”最好的对应是**这些对象如何随 generation/seed 路径演化**。如果这些词不能落实到上述操作层，那它们就应该退回隐喻。 （本地档案：`repo/README.md:32-42`）

**模式 B 证据门禁。**
更残酷地说，在当前 MaoField 证据状态下，绝不能把哲学语言当 proof。研究索引已经明确写了：philosophical / dialectical-materialist framing 由 Win + PI 保留，执行代理只能把它标成受限解释层；而仓库的 empirical 状态恰恰是负结果综合、meta-pattern、weak exception、blocked claims。也就是说，现在能严肃说的不是“辩证法得到了数学证实”，而是“某些哲学直觉启发了一个更干净的 residual/interaction 问题”。这两句话差得非常远。 （本地档案：`repo/GPT55_PRO_RESEARCH_INDEX_20260622.md:126-136`；`repo/STATE.md:16-17,22-27`）

若采用我上面的最佳候选，那么“矛盾”这一术语有且只有一个安全译法：**非可加交互项**。它并不自动意味着“深刻”“突破”或“dialectical motion 成立”；它只是说，频率与位置的作用不能被简单写成“频率项 + 位置项 + 常数项”。这很清晰，也很冷酷。类似地，“运动生成的融合”也只能被翻译成“对象应来自 panel 上的 transport / fold-local 比较，而不是先验用 loss 写死”；在没有 panel-level 稳定证据之前，这仍然只是研究方向，不是结果。 （本地档案：`repo/README.md:152-152`；`repo/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:83-85,102-112`）

## 具体下一步

**模式 A 自由发现。**
下一步不应当是“马上跑新 loss”，而应当是把这个最佳候选做成一个**零 GPU 就能被杀或被留下**的对象。真正好的对象，不怕被快速 kill；相反，它应该主动设计出 cheap negative controls、粗暴的 identifiability 审计和会让自己死掉的随机轴比较。 （本地档案：`README_FOR_GPT55_PRO_20260623.md:57-63`）

**模式 B 证据门禁。**
第一阶段应是**零 GPU 概念审计**。要做的不是跑模型，而是写清楚并锁死：`Q_freq4 × B_tokenpos4` 的 cell 定义、加权可加 nuisance 子空间 \(A\)、随机等 bucket-size 分箱负控、以及“什么情况下该方向直接判死”。这一阶段可以完全靠现有 bundle 和数学推导完成。它最多能产出“对象定义已锁、可进入现有数据 smoke 审计”，不能产出任何“结构已观测”口径。 （本地档案：`repo/scripts/build_hypercube_schema_20260623.py:188-240,250-265`；`repo/docs/infra/gpt_deep_research/Q4_HYPERCUBE_EXTENSION_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md:45-72`）

第二阶段应是**现有数据审计**。直接使用 bundle 里的 3 份 raw JSONL，写一个独立的 zero-GPU 脚本，输出 16-cell means、交互残差 \(\hat I_i\)、随机分箱负控、坏轴负控、以及 3 个 smoke checkpoints 之间的 pattern correlation。这里产生的最好结果，也只能叫做 **smoke-derived feasibility note** 或 **new conjectural direction supported by zero-GPU smoke calculations**。因为它仍然不是 full-panel，不存在 held-out seed 级别的稳定性结论。 （本地档案：`README_FOR_GPT55_PRO_20260623.md:28-29`；`repo/docs/infra/math_turn_20260622/Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.md:8-18,20-53`）

第三阶段才是**可能的 future full-panel audit**，而且只能在 **PI 明确批准** 的前提下。即便批准，也不应直接复用现有 q4 aggregate 路径，而应增加一个与当前 residual-field 脚本分离的新分析脚本，例如 `scripts/q4_hypercube_interaction_audit.py`，其输入必须是 16-cell full-panel aggregate，输出必须限定在 `invalid_artifact / killed / insufficient_artifact / eligible_for_next_design_review_only` 之内。现有 `Q4_IMPLEMENTATION_GATE_UPDATE` 已经对 q4 full-panel 生成加了 approval token guard；这一逻辑应当继续沿用，而不是绕过。 （本地档案：`repo/docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md:13-23,38-53,78-99`；`repo/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py:272-287,480-540`）

所需代码非常具体。首先，生成器需要新增一个**不影响旧 q4 primary path** 的 hypercube aggregate 分支，按 16 个 \((q,b)\) cells 产出每个 checkpoint 的 cell-level means/counts/vars/hash。其次，需要一个单独的 interaction audit 脚本，包含：fold-local additive projection、matched-mean / matched-slope 稳定性、rank/noise gate、random equal-size partition guard、坏轴 guard、以及 wording guard。再次，需要一个专门的 negative-control journal，把“随机分箱也能出类似结果”的坏消息明确落盘，而不是只记录成功情况。 （本地档案：`repo/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:285-315`；`repo/scripts/q4_full_panel_foldlocal_analysis.py:496-557,726-745`）

什么结果只会是“**有资格进入下一轮设计评审**”？答案是：未来某个 real full-panel hypercube audit 同时通过 fold-locality、matched stability、rank/noise 与 random-partition guards。什么结果仍然**不可能**声称？答案同样不变：training authorized、new loss authorized、glass box broken、residual field observed、philosophical breakthrough。这些上限已经被 bundle 多处明写锁死，不应再被任何新对象偷渡突破。 （本地档案：`repo/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:285-315`；`repo/docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md:88-99`；`repo/docs/infra/math_turn_20260622/Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623.md:56-65`）

## 最终决策表

**模式 A 自由发现。**
下表不是按“最华丽”排序，而是按“是否值得继续作为数学对象、是否值得进入 MaoField 审计、是否应退回隐喻”来裁决。

**模式 B 证据门禁。**
其中凡涉及“blocked pending data”的行，都不是说对象不好，而是说以 MaoField 当前工件结构，没法诚实地把它升级成仓库 claim。 （本地档案：`repo/STATE.md:22-27`）

| 方向 | 结论 | 理由 |
|---|---|---|
| 加权乘积划分交互场 | **保留为数学研究方向**；**保留为 MaoField 审计方向**；当前 **blocked pending data** | 数学上最干净，identifiability 最好，和现有 `Q_freq4 × B_tokenpos4` 最贴近；但真正裁决需要 16-cell full-panel aggregate |
| q4 斜率正交残差场 | **保留为 MaoField 审计方向** | 这是仓库当前已经明确 adopted 的对象；但仍未被现有工件观测为正结果 |
| sheaf 拼接障碍 | **保留为数学研究方向** | 很适合表达“局部可解释、全局拼不齐”；但当前数据结构还不够 |
| 交互子空间 holonomy / hysteresis | **保留为数学研究方向**；当前 **blocked pending data** | 极符合“运动生成对象”的 PI 直觉，但对 panel 密度要求高 |
| 边缘化–演化对易子 | **保留为远期数学方向** | 作为“矛盾算子”很漂亮，但现在太早，容易飘离现有工件 |
| “加更多轴就更接近本质”的朴素超立方体 | **压缩为隐喻**，并在 MaoField 审计里 **拒绝** | 没有强 quotient，就只是自由度膨胀；随机轴同样能讲故事 |
| 哲学语言本身作为证据 | **拒绝** | 可以启发定义，不能代替证明，也不能越过 blocked claims |

综合判断是：**旧 MaoField framing 应该被继续去魅，但不应被直接放弃。** 去魅之后留下来的最值得追的对象，不是“hypercube 已成立”，也不是“residual field 已观察到”，而是一个更严格、更会让自己死掉的对象：**加权乘积划分交互场**。它能够把 PI 的超立方体直觉、项目的 residual ambition、以及现有 bundle 的 source-only/product-cell 工件整合成一个可定义、可识别、可快速证伪的数学研究方向；同时，它也足够严苛，以至于当前 MaoField 证据只能说：**它被现有材料启发，并被现有 smoke 数据部分触碰，但远未被现有数据证明。** （本地档案：`README_FOR_GPT55_PRO_20260623.md:57-63`；`repo/STATE.md:22-27`；`repo/docs/infra/gpt_deep_research/Q4_HYPERCUBE_EXTENSION_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md:57-72`）