# Canonical Classification

Node36 import from GPT/PRO attachment on 2026-06-22.
Classification: claim-source / external math-framework audit, not primary
MaoField evidence. The report explicitly says the auditor could not publicly
access the private `Wangziqi0/MaoField` repository; all repository-specific
facts in the report are therefore blocked unless verified against local
canonical code, JSON, logs, or verdict files. Its useful contribution is the
proposed mathematical framework and stricter artifact schema for the next
zero-GPU gate.

# MaoField 数学转向审计报告

## 审计边界与可核验证据

按题面要求，我把这次工作当作一次**零上下文的数学审计**：凡是不能由仓库代码、JSON、日志、verdict，或一级数学文献支持的断言，一律记为 **blocked**。在本次公开核验中，`Wangziqi0` 的 GitHub 公开主页显示当前只有 **1 个公开仓库**，页面可见的仓库是 `Shape-CFD`；对 `https://github.com/Wangziqi0/MaoField` 的直接抓取返回 **404 Not Found**。这意味着：题面所列 `STATE.md`、`GPT55_PRO_RESEARCH_INDEX_20260622.md`、`math_turn_loso_audit_result_20260622.json`、`scripts/math_turn_loso_audit.py` 等文件，我**无法独立公开核验其内容**；因此，所有依赖这些文件内部细节的具体结论，在本次报告中都只能标记为 **blocked**。citeturn3view0turn1view0

所以，下面给出的不是对 MaoField 当前仓库结论的“包装”，而是一个**可以直接杀死或拯救下一步的数学框架**。凡涉及题面中“exp019 无剩余正结论”“aggregate zero-GPU audit verdict = insufficient_artifact”“F3 LOSO delta 弱存活”等状态，我只把它们当作**你在本题中给出的前提**来组织分析，不把它们当作我已用仓库文件独立验证过的事实。仓库级实证断言仍然是 **blocked**。citeturn3view0turn1view0

最核心的审计判断先写在前面：如果 MaoField 的下一步想从“负向测量审计”转向“向量场/训练信号”，那它必须先解决一个比工程更高一级的问题——**从标量 KL 到均值为零的切片向量场，并不存在自然唯一的提升；要得到唯一对象，必须先固定切片结构、投影空间、正交性与决定论性的评分规则**。如果做不到这一点，所谓“mean-null vector KL field”在数学上只是一个可选坐标化，不是证据。这个判断直接来自 I-投影/Bregman 几何、Hoeffding 型投影分解、以及多维 functional elicitation 的文献。citeturn11search0turn12search0turn14search0turn14search1

## 定理与反例地图

### 标量 KL 到均值为零切片向量场

最可救的严谨框架，不是“从一个标量 KL 发明一个向量”，而是先固定一个切片 σ-代数或分区 \(\mathcal G\)，再把对数似然比 \(\ell(x)=\log \frac{dP}{dQ}(x)\) 在 \(L^2(P)\) 中做条件期望投影：  
\[
m = E_P[\ell],\qquad v_{\mathcal G}(x)=E_P[\ell\mid \mathcal G](x)-m,\qquad r_{\mathcal G}(x)=\ell(x)-E_P[\ell\mid \mathcal G](x).
\]
这样得到的是一个**唯一依赖于 \(\mathcal G\)** 的均值为零切片场 \(v_{\mathcal G}\)，并且有正交分解 \(\ell = m + v_{\mathcal G}+r_{\mathcal G}\)。这与 Hoeffding 分解的精神一致：一旦投影子空间给定，分量才具有唯一性；而在 KL/I-divergence 的几何下，投影与“Pythagorean”型分解才有严谨含义。换句话说，**真正的对象不是“向量化后的 KL”本身，而是“对数似然比在预先规定切片空间上的正交投影”**。citeturn12search0turn11search0

反例也很直接，而且足以杀死大量叙事：若不先固定 \(\mathcal G\) 或等价的坐标系统，则对任意均值为零的 \(\delta\in L^2(P)\)，都可以写成  
\[
\ell = m + (v+\delta) + (r-\delta),
\]
于是同一个标量 KL 对应无穷多个“均值为零向量场”。这不是哲学问题，而是**非识别性**：标量泛函本身不决定向量提升。因而，“把 scalar KL 投影成 mean-null vector field”这一步，只有在**切片规则、参考测度、内积、正规化、以及剩余项定义**全部写死时，才配称为数学对象；否则是 **blocked**。这一点是从 Hoeffding/投影框架作出的直接推论。citeturn12search0turn11search0

因此，若 MaoField 真想救这个方向，最强也最克制的说法只能是：**在给定切片空间 \(\mathcal G\) 后，研究 \(v_{\mathcal G}\) 是否携带超出均值、PPL、mean-logprob 阴影以外的稳定信息**。如果目前仓库工件还没有把 \(\mathcal G\) 的定义写成一个确定的、可重算的 schema，那么“vector turn”在数学上没有起点。该点目前对我而言是 **blocked**，因为仓库文件未可见。citeturn3view0turn1view0

### 残差不是 nuisance shadow

要证明某个残差不是 mean-logprob / PPL / perplexity 阴影，最低级别只能靠**部分回归**；更高一级则必须进入**半参数正交化**。在线性 nuisance 类里，Frisch–Waugh–Lovell 说明：对 nuisance 变量 \(Z\) 先做残差化，再用残差回归，得到的目标系数与完整回归相同。Robinson 的双残差部分线性模型进一步说明：如果 nuisance 是未知函数 \(g(Z)\)，则需要先估 \(E[Y\mid Z]\) 和 \(E[X\mid Z]\)，再在残差上做估计。Chernozhukov 等与 Foster–Syrgkanis 的框架把这件事写成 **Neyman orthogonality / orthogonal statistical learning**：目标矩条件对 nuisance 的一阶扰动必须局部不敏感，否则“残差幸存”只是 nuisance 估计误差的副产品。citeturn19search1turn19search5turn15search11turn15search8

这给出一个严格的杀伤标准：如果 MaoField 现在的“残差 survives”只是在**线性 partial-out**、或只在某个特定 residualizer 下成立，它并不足以说明存在新结构。反例很简单：设信号 \(S=g(N)+\varepsilon\)，其中 \(N\) 是 mean-logprob/PPL 之类 nuisance，\(g\) 是非线性单调函数；在线性 partial-out 后，\(S\) 仍可能留下看似稳定的残差，而这种残差依然完全是 nuisance shadow。进一步地，若做 rank transform，也只能杀死部分线性/单调关系，不能自动杀死一般函数阴影。因此，**“rank survives”“residual survives”都不是充分条件**；充分条件应当是：在一个明确声明的 nuisance 函数类下，目标 moment 对 nuisance 的 Gateaux 导数为零，且经过 cross-fitting 后仍然在各环境里稳定非零。否则结论仍是 **blocked**。citeturn19search5turn15search11turn15search8

如果要救这个方向，最紧的数学表述不是“这个残差和 PPL 不一样”，而是：**存在一个预注册的 score / moment \(\psi(W;\theta,\eta)\)，其中 \(\theta\) 是向量场效应参数，\(\eta\) 是 nuisance，且 \(\partial_\eta E[\psi(W;\theta_0,\eta_0)][h]=0\) 对允许的扰动方向 \(h\) 成立**。只有这种局部正交性，才配讨论“不是 shadow”。所有低于这一级的说法，在训练前都不够。citeturn15search11turn15search8

### LOSO、matched-mean、rank/residual 与 factor gates

LOSO 只能回答“是否主要由某一个 source 驱动”，不能回答“是否具有可迁移的结构稳定性”。更高一级的框架是 **Invariant Causal Prediction**：当数据来自多个环境时，真正稳定的结构应在环境变换下保持预测关系或条件分布不变；不稳定的伪信号会随环境移动。因而，若 MaoField 目前唯一“弱存活”的东西是 LOSO delta，那么它最多说明“不是单源伪影”的证据尚未彻底消失；它**不能**单独支持训练改动。只有当同一预注册方向在不同 source-held-out 环境下都保号、保量级、并且误差模型稳定时，才有资格继续。citeturn12search2turn12search5

`matched-mean` 的地位非常高。因为一旦一个候选 observable 在均值匹配后消失，最先该怀疑的不是“更深结构被抹平了”，而是它本来就主要依赖均值层面的 nuisance。这里的反例也很清楚：如果统计量本质上是 \(T(P)=\phi(E_P[X])\) 或被均值强控制，那么 matched-mean 直接把它送到零；相反，真正分布性、形状性、切片性的信息，应当允许**同均值异分布**下仍可存活。于是，若目前汇总工件显示 F3 在 LOSO 下弱存活，但 matched-mean 失败，那么对“新向量结构”的默认判决就应是**不成立**，除非你能在更细颗粒度的切片层面证明：匹配均值后仍有稳定的非均值分量。按题面给定的状态，这一点目前没有被充分工件支持。该仓库级事实本身对我仍是 **blocked**，但数学含义是明确的。citeturn12search2turn12search5

`rank/residual` 与 `factor-model gate` 应当视为两个不同层级。前者处理的是已声明 nuisance 类下的局部阴影；后者处理的是**低秩共因子**。Bai–Ng 给出了大维度近似因子模型中因子个数的一致估计；Bai 给出了大维度因子模型的推断理论；Fan 等的 POET 框架则明确：去掉公共因子后，剩余协方差可被当作 principal orthogonal complement 中的结构对象来研究。对 MaoField 而言，这意味着一个很尖锐的 gate：若候选向量场只是顶层几个公共难度/频率/长度因子的线性或近线性装扮，那么它在 factor removal 之后应当塌缩。反过来，只有当信号在 principal orthogonal complement 中仍存活，才配说它不是“公共难度因子”的影子。citeturn13search0turn13search1turn13search2

## 混合滞回与频率分层塌缩

题面中的 “mixture hysteresis / frequency-stratified collapse” 只有一半已经有成熟数学对象，另一半目前仍应标 **blocked**。成熟的那一半是：**混合、分层与坍缩后的反转**。Simpson 早就说明，分层后同向的关系在聚合后可能反转；Greenland 等把这件事系统化为 confounding 与 non-collapsibility 的区分；Teicher 证明过有限混合识别性需要额外条件。对 MaoField 的直接含义是：一个 aggregate delta 的符号与大小，都可能只是当前语料频率权重 \(w\) 下的产物，而不是组分级机制本身。于是，只要 effect 可以写成 \(\Delta(w)=\sum_k w_k \Delta_k\)，就存在权重区域使其换号；如果各 stratum 的 \(\Delta_k\) 异号，aggregate 的“微弱幸存”几乎没有解释权。citeturn17search5turn17search13turn11search3

所以，真正该做的不是继续盯 aggregate，而是对一个固定的 common-weight reference measure \(w^\star\) 做**频率标准化传输**：先在每个频率/长度/难度 stratum 中估 effect，再把各环境都运输到同一个 \(w^\star\) 上比较。只有当 transported effect 在多环境下仍稳定，同号且不被均值与公共因子解释，才说明不是 frequency-stratified collapse。若 transported effect 一旦换权重就塌或翻号，那么 MaoField turn 应立即停止。这个结论是 Simpson/可坍缩性与混合识别文献的直接审计化应用。citeturn17search5turn17search13turn11search3

至于题面中的 **hysteresis** 这半边，我必须更严格：如果没有仓库日志展示“沿不同训练路径、不同重加权路径、不同 curriculum path 到达不同稳定分支”，那“滞回”只是一个比喻，不是一个已被工件支持的数学现象。对 hysteresis 的任何强断言，在本次公开审计中都应标 **blocked**。citeturn3view0turn1view0

## 哪些先验框架最可能贴近 MaoField

最贴近、也最可能真正有用的框架，其实不是一个，而是五个彼此嵌套的框架。

第一层是 **I-divergence / Bregman 投影几何**。它给出的不是“新信号存在”，而是**什么叫做合法投影、什么叫做合法剩余、什么时候有 Pythagorean 型分解**。如果下一步还想保留 “KL” 这个词，这是唯一不空泛的母框架。citeturn11search0

第二层是 **Hoeffding 型正交分解**。它把“切片向量场”从叙事对象变成投影对象：先给定切片空间，再讨论一阶分量、交互分量和正交剩余。若没有这层，所谓 slice field 没有唯一性。citeturn12search0

第三层是 **partialling-out 与 orthogonal statistical learning**。FWL/Robinson 处理一般残差化问题；Chernozhukov 与 Foster–Syrgkanis 则给出“对 nuisance 一阶不敏感”的现代条件。只要 MaoField 的论证里还带着 “不是 PPL shadow”“不是 mean-logprob shadow” 这一类句子，这一层就是刚需，而不是参考文献摆设。citeturn19search1turn19search5turn15search11turn15search8

第四层是 **多环境不变性与近似因子模型**。前者回答“跨 source 是否稳定”；后者回答“是否只是公共低秩因子”。这两层合起来，才构成你题面里所谓 LOSO / factor gates 的真正数学版本。citeturn12search2turn13search0turn13search1turn13search2

第五层是 **elicitation / proper scoring**。这层决定一个 observable 能不能升格为训练损失。Savage、Gneiting–Raftery、Dawid、Fissler–Ziegel 的共同结论是：一个功能量若想成为严肃的优化目标，至少要能被一个严格一致的 score 识别；对多维 functional，还需要 joint elicitability 或等价的识别结构。没有这层，就不能从“可测”跳到“可训”。citeturn14search2turn14search0turn14search3turn14search1

## 什么才算真实的数学推进

真正的推进，不是再提出一个名字更响的向量场，而是把下面这组对象一次性钉死。

首先，要**严格定义功能量**。最自然的候选不是“mean-null vector KL field”这个口号，而是  
\[
T_{\mathcal G}(P,Q)=E_P[\ell\mid \mathcal G]-E_P[\ell],
\]
其中 \(\ell=\log(dP/dQ)\)，\(\mathcal G\) 是预注册的切片结构。这个对象的好处是：均值为零是构造内生的；切片唯一性由投影给出；剩余项 \(r_{\mathcal G}\) 有明确意义。若做不到这一步，就谈不上理论推进。citeturn11search0turn12search0

其次，要**证明它不是 nuisance shadow**，而且证明方式必须升级到正交矩条件。最低要求是：对明确定义的 nuisance 类 \(\eta\)（至少包括 mean-logprob、PPL、高阶 PPL、length、frequency、source-level common factors），你的目标 score 对 \(\eta\) 的一阶扰动为零，或等价地，在 cross-fitted orthogonalization 之后仍有稳定非零参数。否则只是“某种残差在某个 residualizer 下幸存”。citeturn19search5turn15search11turn15search8

再次，要**证明它在环境与重加权下稳定**。这不是“多做几个 ablation”能替代的。你需要的是：在 leave-one-source-out 环境、以及 transported common weights 下，\(T_{\mathcal G}\) 的方向和效应都基本不变；同时，在去掉估计公共因子后的 orthogonal complement 中仍保留。否则，它要么是环境偶然性，要么是低秩公共难度影子。citeturn12search2turn13search0turn13search1turn13search2

最后，若想把它升格到训练层，必须**给出严格一致的评分函数或可识别 moment**。对多维 functional，这一步不是可选项。若拿不出 \(S(a,y)\) 使得 \(a=T(P)\) 是 \(E_P S(a,Y)\) 的唯一极值，或者拿不出对应 identification function，那么优化它只是“优化一个代理坐标”，并无决策论担保。只有到了这一步，才配讨论 training loss。citeturn14search2turn14search0turn14search3turn14search1

## 立即停止条件与训练前必须要有的下一份工件

有五个条件，任何一个满足，MaoField turn 都应**立即停止**。

其一，若切片结构 \(\mathcal G\) 不能被写成确定的、可重算的 schema，那么从 scalar KL 到 vector field 的提升非唯一，项目在对象定义层面即失败。其二，若在 cross-fitted orthogonalization 后，目标效应消失，或只在线性 residualizer 下幸存，则“不是 shadow”的说法失败。其三，若 transported common-weight effect 在频率/长度/难度分层后显著翻号或塌缩，则 signal 只是 mixture/frequency artifact。其四，若 factor removal 后效应消失，则它只是公共低秩因子。其五，若不存在严格一致的 scoring rule / identification function，则该 observable 不应进入训练目标。citeturn12search0turn15search11turn15search8turn17search13turn11search3turn13search0turn13search1turn13search2turn14search0turn14search1

在任何训练改动之前，**唯一合格的下一份实证工件**不应再是 aggregate JSON，而必须是一份**切片级、环境级、可重算的面板工件**。最低规格应当是：每一行对应一个 `(example_id, source_id, fold_id, stratum_id, slice_id)`；列中至少包含原始 logprob、mean-logprob、PPL/high-order PPL、scalar KL、切片投影 \(v_{\mathcal G}\) 的各分量、source 标签、频率/长度/难度 strata、匹配前后权重、以及用于 factor gate 的低秩表示或残差表示。只有这种面板，才允许你同时跑 FWL/Robinson 正交化、ICP 风格环境稳定性检验、Bai–Ng 因子数选择、POET/orthogonal complement 检查、以及 common-weight transport。缺少这份面板，题面所说的“aggregate zero-GPU audit verdict insufficient_artifact”在数学上就没有出路，训练改动应继续冻结。这个要求是由上述文献共同逼出来的，而不是额外加码。citeturn19search5turn15search11turn12search2turn13search0turn13search1turn13search2turn17search13turn11search3

更尖锐地说，训练前的最小通过标准应写成一句话：**至少存在一个预注册切片方向，在 cross-fitted nuisance orthogonalization、common-weight transport、以及 factor removal 之后，仍在各 LOSO 环境中保号、保量级，并且对应一个可识别的严格一致 score。** 只要这句话目前不能被仓库工件逐项支撑，结论就只能是：**不准训练，不准升级成 loss，不准宣称 vector turn 得证。** 当前公开可核验证据不足以让我判断这句话已经成立，因此仓库层面的正面结论仍是 **blocked**。citeturn3view0turn1view0turn15search11turn12search2turn13search0turn14search1
