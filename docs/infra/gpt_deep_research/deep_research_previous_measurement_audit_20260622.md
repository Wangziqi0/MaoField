# MaoField 玻璃箱打破工具的严格数学审计

## 执行裁定

[LOCAL] 今天在严格审计下，**MaoField 当前能成立的数学对象，不是 unconditional theorem，也不是“辩证唯物主义本身给出数学工具”，而是一个可证伪的 measurement-audit operator family**：任何候选 collapse 指标，都必须先穿过 nuisance 轴的投影与残差审计，才有资格进入“独立结构”候选。这个结论与仓库当前绑定态一致：STATE 将 exp020 的收口明确写成 **C(meta-pattern)**，并把积极性 A 线判死；L0 总整合同时维持 **0 unconditional close**；PHILO 索引则把“物质+实践第一性、哲学+数学是 outcome 而不是 starting form”列为 D-3 的核心防线。fileciteturn2file1L20-L20 fileciteturn2file1L26-L31 fileciteturn8file5L108-L113 fileciteturn9file1L22-L25

[LOCAL] 当前允许的最高强度表述是：**在 MaoField 当前实验 regime 中，若干预注册/盲/敌意 gate 下的候选 PPL-independent collapse 指标，反复退化为 PPL/eff_supp shadow、seed-noise floor 或 decode sensitivity；F3 只是弱例外，不是独立 positive finding。** 这一点在 C 证据库、STATE 收口页和 T1/T2/T3 数学裁定里是一致的。fileciteturn4file0L11-L15 fileciteturn2file1L26-L30 fileciteturn5file0L20-L28

[INFERENCE] 因而，“玻璃箱打破工具”最准确的数学重述不是某个单一定理，而是一组**敌意审计算子**：**通道正交化 + 噪声地板 + decode 不变性 + 可识别性秩条件 + 迟滞残差 + η/T-response 判别器**。它的作用不是直接“证明 collapse 的本质”，而是先持续淘汰伪独立测度，再把仍然存活的残差压缩成最小可检验对象。

[WEB] 从外部 primary literature 看，这种保守定位也是诚实的：Shumailov 给出递归训练下 tails 消失与 irreversible defects 的早期主干；Guo 已系统研究 linguistic diversity 下降；Gerstgrasser 证明 replace 与 accumulate 两种工作流的结论可以完全不同；Schaeffer 进一步指出“model collapse”本身至少包含八种互相冲突的定义；Borji 则直接提醒距离度量不同会改变 collapse 结论。外部文献因此支持 MaoField 把重点放在“审计定义、度量、通道与可识别性”，但并不把 MaoField 自动升级为 theorem。citeturn5view1turn5view0turn4view2turn3view1turn3view0

## 形式定义

[INFERENCE] 令递归训练轨迹的索引集为
\[
I=\{(g,s,c,d)\},
\]
其中 \(g\) 是 generation，\(s\) 是 seed，\(c\) 是训练/实验 condition，\(d\) 是 decode protocol。令固定评测基座为 \(\mathcal E\)，对应模型诱导的评测分布或打分对象为 \(p_{g,s,c,d}\)。任何候选 collapse 指标都写成
\[
M:I\to\mathbb R,\qquad M(g,s,c,d)=\Phi(p_{g,s,c,d};\mathcal E).
\]
这里的 \(\Phi\) 可以是 PPL、mean-logprob、eff_supp、distinct-2、几何量、slice-gap，或任何新提出的函数。

[INFERENCE] 令 nuisance 坐标族为
\[
Z=(Z_1,\dots,Z_K),
\]
最小应包含：\(\bar\ell\) 或 PPL/mean-logprob、eff_supp、decode protocol、seed、base-reset 通道、\(\eta/T\)、以及已知 prior-art mechanisms 的摘要量。形式上可写为
\[
Z(g,s,c,d)=\big(\bar\ell,\mathrm{PPL},\mathrm{eff\_supp},d,s,w,\eta,T,K_1,\dots,K_m\big).
\]
这一步和仓库当前纪律一致：PHILO 索引明确要求数学起点必须落在 code、data、operator、measurement、identifiability、invariance、noise floor，而不是哲学先验；同时它也把“当前标准 ML evaluation 缺少 cross-layer interconnection 的可证伪测量工具”单列为方法论 catch。fileciteturn9file1L22-L25

[INFERENCE] 定义 nuisance-only 函数类 \(\mathcal H_Z\)，并把经验投影算子定义为
\[
\Pi_Z M \in \arg\min_{h\in\mathcal H_Z}\sum_{i\in I_{\rm obs}}\big(M_i-h(Z_i)\big)^2+\lambda \Omega(h),
\]
其中 \(\Omega\) 是对过拟合的正则，\(\mathcal H_Z\) 可以是线性族、样条、isotonic、LOO-kNN 或其联合。于是残差定义为
\[
R_M = M-\Pi_Z M.
\]
这正是 exp020 第二通道脚本在做的事：它先构造**纯 mean-lp null functions**，再用 flexible mean-lp fits、matched-mean_lp pairs 与 LOSO-CV 检查 F1/F3 是否真的带有 orthogonal-to-mean-logprob 的信息；其设计目标就是“纯 mean-lp function 不得 false-positive”。fileciteturn10file0L5-L15

[INFERENCE] 一个候选测度 “survives audit” 的必要条件，可压成以下五门：
\[
\mathfrak A(M)=
\mathbf 1\{\text{Gate}_{\rm resid}\wedge \text{Gate}_{\rm noise}\wedge \text{Gate}_{\rm decode}\wedge \text{Gate}_{\rm rank}\wedge \text{Gate}_{\rm subsume}\}.
\]
更具体地说：
\[
\text{Gate}_{\rm resid}: \exists\,\Delta_g \text{ s.t. } |\Delta_g R_M|>\epsilon_r,
\]
\[
\text{Gate}_{\rm noise}: |\Delta_g R_M|>\kappa\,N_M,\qquad N_M:=Q_{0.9}\big(\sigma_s(R_M\mid g,d^\*)\big),
\]
\[
\text{Gate}_{\rm decode}: \operatorname{sign}\Delta_g R_M^{(d)} \text{ 在允许的 } d \text{ 上不翻号},
\]
\[
\text{Gate}_{\rm rank}: \operatorname{rank}[1,Z,Q_M]>\operatorname{rank}[1,Z]\ \text{或 LOSO-CV 增益}>\epsilon_{\rm cv},
\]
\[
\text{Gate}_{\rm subsume}: \forall j,\ \|R_M-\Pi_{K_j}R_M\|>\epsilon_k.
\]
这里 \(Q_M\) 是“新通道”候选。它要么给 design matrix 增加秩，要么在 LOSO/pair-matching 下提供可复现的 out-of-nuisance 预测增益；否则不具备独立可识别性。

[INFERENCE] 在这个框架下，可以写出一个最小 no-survival 命题：**若 \(M=h(Z)\) 在观测分布上成立，且 \(\mathcal H_Z\) 含真函数 \(h\)，则 \(R_M=0\)，因此任何“独立测度”表述都不成立。** 这不是新定理，而是审计框架的定义性结论。它对应 MaoField 当前对 gate-1 到 gate-5 的理解：不是“collapse 不可测”，而是在当前测到的这些候选里，**独立性没有过关**。这一点由 C 证据库写得很清楚。fileciteturn4file0L12-L15

[INFERENCE] 这个框架也自带失败模式。第一，若 \(\mathcal H_Z\) 太弱，就会把 nuisance leakage 错认成结构残差；第二，若 \(\mathcal H_Z\) 太强且样本太小，也可能把真残差过拟合吸走；第三，若 decode 本身改变观测测度，decode-invariance gate 会把“观测协议差异”误判成“对象不存在”；第四，若 known mechanism 摘要变量 \(K_j\) 过粗，也会把 subsumption gate 做成伪空门。换句话说，这是一套**可证伪、可失败、可修订**的数学审计程序，而不是一劳永逸的理论封口。

## Claim table

| Claim | Allowed wording | Forbidden wording | Proof status | Required next check |
|---|---|---|---|---|
| [LOCAL] MaoField 当前的核心数学对象 | “一个可证伪的 measurement-audit operator family；新指标必须先穿过 nuisance 投影与残差审计。” fileciteturn2file1L26-L31 fileciteturn9file1L22-L25 | “MaoField 已给出 collapse 的 unconditional theorem” | [LOCAL] 支持强；[INFERENCE] 形式化可加固 | [LOCAL] 把 \(\Pi_Z\)、noise floor、rank gate 写进正式 design/appendix |
| [LOCAL] C(meta-pattern) 的强度 | “在当前实验 regime 中，已测试的若干 PPL-independent 候选测度反复塌回 PPL/eff_supp shadow、seed-noise floor 或 decode sensitivity。” fileciteturn4file0L11-L15 | “all collapse metrics reduce to mean-PPL” | [LOCAL] 现有最强表述 | [LOCAL] 用 T3 arbitrary-bin kill-test 检查是否还有廉价非标量残差 |
| [LOCAL] L0 数学层 | “0 unconditional close；只存在 conditional / negative / partial / FAIL。” fileciteturn8file4L66-L71 fileciteturn8file5L108-L113 | “L0 已闭合”“已经证明 collapse theorem” | [LOCAL] 强支持 | [LOCAL] 只对有新实证支撑的条目做 tier 升降 |
| [LOCAL] exp019 | “α=1 confirmatory 三 endpoint 全 FALSE；faithful decouple recompute 0/5；exp019 无 surviving positive。” fileciteturn6file0L13-L26 fileciteturn7file1L1-L7 | “exp019 仍保留 positive branch” | [LOCAL] 强支持 | [LOCAL] 若重审 α=10，必须全新交错 confirmatory |
| [LOCAL] F3 | “F3_slice_gap 是 weak exception / hysteresis residual / measurement instantiation，提示 mean-logprob 不是完备坐标。” fileciteturn4file0L15-L15 fileciteturn5file0L20-L24 | “F3 是独立 positive finding” | [LOCAL] 弱支持；[WEB] prior-art 高重叠 | [LOCAL] 补 T2 sufficient-side code；[LOCAL] 保留 raw per-token logprobs |
| [WEB] F3 的 prior-art 占用 | “tail/frequency differential collapse 与 irreversibility 在外部文献已有主干；MaoField 的 F3 更像对这些机制的测量学实例化。” citeturn5view1turn4view3turn7view0turn4view0 | “F3 首创 tail collapse / hysteresis” | [WEB] 支持中等到强 | [INFERENCE] 需继续区分‘tail differential’与‘literal hysteresis loop’ |
| [LOCAL] T3 arbitrary-bin 测试 | “它是最便宜的 refuse-the-scalar 载体；若 matched-mean 下线性差测度仍非零，可拒绝单坐标 sufficiency。” fileciteturn5file0L26-L36 | “T3 已经证明完整非线性结构” | [LOCAL] 候选强；尚未全跑 | [LOCAL] 用 persisted per-token logprobs 或 CPU 重算补上 |
| [LOCAL] base-reset vs Borkar | “标量静态 toy 中可约简；唯一仍可保留的是 η/T-response discriminator 与高维/operator wedge。” fileciteturn5file0L11-L18 | “base-reset 与 Borkar 在数学上已完全正交” | [LOCAL] 标量层强支持；高维层开放 | [LOCAL] 做 step-sweep；[INFERENCE] 设计多方向 operator-level fit |
| [WEB] Borji 对 D-PPL / 线性桥的覆盖 | “Borji 只支持 generic metric-dependence caution，不等于证明 MaoField-specific 线性桥。” citeturn3view0 | “Borji 已证明 MaoField 的 \( \tfrac12(B+C) \) 结构桥” | [WEB] 仅背景支持 | [LOCAL] 同源重算 \(D_{\rm code}\) 与 \(D_{\rm paper}\) 轨迹并打破秩亏 |
| [LOCAL] 哲学位置 | “哲学只能作 retrospective discipline，不得作数学起点。” fileciteturn9file1L22-L25 | “辩证唯物主义本身给出玻璃箱数学工具” | [LOCAL] 强支持 | [INFERENCE] paper 中哲学只写 discipline / discussion，不入 theorem body |

## Theorem candidates

| Candidate | Assumptions | Proof sketch | Counterexample attack | Failure condition |
|---|---|---|---|---|
| [INFERENCE] **Nuisance-sufficiency lemma**: 若 \(M=h(Z)\) 且 \(h\in\mathcal H_Z\)，则 \(R_M=0\) | \(\mathcal H_Z\) 包含真 nuisance map；样本足以识别 | 投影定义直接给出 \(\Pi_ZM=M\) | 若 \(\mathcal H_Z\) 过弱，\(R_M\neq0\) 只是 misspecification 漏差，不是真结构 | 只是一条定义性引理，不可外推到“所有未来指标” |
| [INFERENCE] **Noise-floor exclusion lemma**: 若 \(|\Delta_gR_M|\le \kappa N_M\)，则不得把 \(M\) 升格为稳定独立通道 | seed-noise floor 估计来自预注册 bootstrap / within-gen seed variance | 这是一个 decision-theoretic exclusion rule：信号未越过观测噪声上界时，正面结论不稳健 | 若 seed 本身过少、bootstrap 假设失真、或 noise floor 与 generation confounded，就会过严 | 这是审计门，不是对象定理；只能给“不得声称”，不能给“对象不存在” |
| [INFERENCE] **Two-slice determinant proposition**: 在线性 two-arm/two-slice toy 中，\(D=a_{fd}a_{ru}-a_{fu}a_{rd}\neq0\) 对产生 matched-mean hysteresis residual 充分，且在该 toy 中也 generically 必要 | 设 down/up 两臂分别只沿一个 arm coordinate 变化；freq/rare 响应矩阵为 \(A=\begin{pmatrix}a_{fd}&a_{fu}\\ a_{rd}&a_{ru}\end{pmatrix}\)；mean 取两 slice 的固定加权和，且两臂都可达到相同 mean | 若 down 臂 \(u=(t,0)\)，up 臂 \(u=(0,t')\)，在等权 mean 下可令 \(m_d(t)=m_u(t')\)。消去 \(t'\) 后，gap 差满足 \(\Delta g_{d,u\mid m}\propto D\)。因此 \(D\neq0\Rightarrow\) 同 mean 不同 gap，出现迟滞残差；\(D=0\Rightarrow A\) 秩 1，\((m,g)\) 均塌到单参数曲线 | 即便 \(D\neq0\)，如果真实轨迹只落在二维空间中的一条一维子流形上，或两臂永远到不了同 mean 区间，也观察不到 hysteresis | 该命题只对**线性 toy** 成立；离开 toy，只能保留为 mechanism possibility，不得写成 empirical theorem。它与本地 T2 裁定一致，但本地也明确承认 sufficient-side code 还没落盘。fileciteturn5file0L20-L24 |
| [INFERENCE] **T3 linear-functional proposition**: 定义 \(L_{B_1,B_2}(p)=\langle \log p,\ |B_1|^{-1}\mathbf 1_{B_1}-|B_2|^{-1}\mathbf 1_{B_2}\rangle\)。若 matched-mean pairs 上 \(L\) 仍系统性非零，则拒绝“单坐标 sufficiency” | 固定评测 token universe；bins 预注册；用 matched-mean 配对或 LOSO/p permutation 控制 nuisance | \(L\) 本质上就是两 bin 的平均 logprob 差。它比 cubic residual gate 干净，因为不需要假设三次多项式就能直接检验“同 mean 是否仍有结构差” | post-hoc bins、token frequency bins 与基线定义共用同一统计量、或上下文构成变化导致的伪 bin signal，都会给出 false positive | 若没有 raw per-token logprobs，只剩 aggregate rows/gates，就不能新增 bin，也不能做多重比较控制；此时**只能**报告预先聚合好的 F1/F3，不能把结果放大成“一般 refuse-the-scalar 定理”。本地数学线已把 T3 定为“最便宜 kill-test”，且把 cubic gateA 判 broken。fileciteturn5file0L26-L36 |
| [INFERENCE] **Scalar equivalence proposition**: 标量静态 Gaussian toy 中，base-reset ridge \(w=1/(\eta T)\) 与 Borkar mix \(c\) 在稳态层可由 \(c=w/(1+w)\) 双射等同 | 一维 Gaussian toy；只比较稳态分布层，不比较 transient response | 直接代入本地方程 \(v_A^\*=s/[w(w+2)]\) 与 \(v_B^\*=s(1-c)^2/[c(2-c)]\)，解得 \(c=w/(1+w)\) 后两式相同 | 若比较的是路径依赖、暂态、分层方向响应，而不是标量稳态方差，此等价未必保留 | 这条命题只能打掉“强结构正交性”主张，不能自动打掉高维/operator wedge；本地数学线也正是这样收口的。fileciteturn5file0L11-L18 |
| [INFERENCE] **Operator wedge candidate**: 若高维基座下 effective prior 是各向异性的矩阵/算子 \(W\)，而 Borkar 只给标量 mixture \(c\)，则除非 \(W\propto I\) 或只观测到一维 summary，否则不存在单个 \(c\) 同时匹配所有方向响应 | 线性化或局部二次近似；可观测至少两个独立方向/层；\(W\) 与 Hessian 不在同一标量子族 | mixture \(c\) 只能给各方向同尺度收缩；矩阵 prior 会给不同特征方向不同响应。若多方向观测需要不同 \(c_{\rm eff}\)，则 scalar-c 失败 | 如果实验只看一个标量 summary，任何各向异性都可能被“平均完”并伪装成某个 \(c_{\rm eff}\) | 这仍是 [GAP]：要靠 η/T step-sweep 与分层/分方向观测来关门或保留 |

[LOCAL] 上表里，真正已经被本地文件写进结论的只有三点：**T1 在标量静态层被证伪、T2 只保留到 weak mechanism possibility、T3 只到“廉价载体与 kill-test 候选”**。这正是当前仓库对数学强度的自我约束。fileciteturn5file0L11-L18 fileciteturn5file0L20-L28

[WEB] 外部文献对这些 theorem candidates 的作用主要是“限缩声称范围”，不是“替 MaoField 证明定理”：Shumailov 提供了 tails 消失与不可逆缺陷的大框架；Tale of Tails 把 model collapse 放进 scaling-law / tail 语言；Rate of Model Collapse 进一步给出离散词项忘却与原始频次的关系；Borkar 讨论的是 external-source presence 导致的两类极限行为；Schaeffer 则提醒“collapse”定义不稳固，因此任何 theorem 候选都必须把对象、工作流和度量写死。citeturn5view1turn4view3turn7view0turn4view0turn3view1

## Zero-GPU tasks and gaps

[LOCAL] **优先级最高的零 GPU / CPU 任务**有五项，而且它们都直接对应当前数学口子的开闭状态。第一，补跑 **T3 arbitrary-bin / linear-functional kill-test**；本地数学线已把它列为“最便宜 kill-test”。第二，补齐 **T2 two-component sufficient-side code artifact**；现在 toy 的 IFF 还停在一半。第三，把 **cubic gateA 降级，LOSO/permutation 升为主 gate**；数学线已写明 cubic gateA broken，而第二通道脚本的设计本来就是为防 pure mean-lp null functions 假阳性。第四，做 **M3 η/T-response step-sweep**，检验 \(c_{\rm eff}\) 是否真的跟 \(\eta,T\) 变化。第五，持久化 **raw per-token logprobs 或等价 masks/indices**，为 T3 和后续任意 bin 重算留底。fileciteturn5file0L27-L36 fileciteturn10file0L5-L15 fileciteturn11file0L9-L15 fileciteturn11file0L66-L79

[LOCAL] **trace hygiene** 方面，E10 的 source-name 风险是实锤：C 证据库表格把 E10 的来源写成 `verify_gate5b.py`，但仓库实际存在并可读取的脚本是 `scripts/verify_gate5_distinct2_collinear.py`，其内容直接计算 distinct-2 与 eff_supp 的 Pearson \(R^2\)，还把 “\(R^2<0.5\) 才算不共线、\(>0.5\) 就死” 写进注释。因此 paper 或审计正文里应按**实际脚本名**更正。fileciteturn4file1turn4file1 fileciteturn12file0L5-L23

[LOCAL] **E5 的可写范围必须收紧。** C 证据库对 E5 的原始信息是：晚代 seed 方差大幅放大，而在同通道 5-seed / k=2 阈值下出现 5/10 假分层，因此“outcome 噪声地板 > 期望通道效应(1v1)”。最稳妥的写法不是“所有通道效应都不可测”，而是“**在当前 1v1 / pairwise lambda 协议下，晚代 seed noise 足以刺穿这一量级的 channel claim**”。fileciteturn4file1turn4file1

[LOCAL] **E11 的措辞也必须收紧。** 仓库当前绑定态已经明说：C **不能**写成“全塌 mean-PPL”；F3 是弱真例外，而且 even this weak exception 也被 prior art 高度占用。因此 paper-safe wording 最多只能写“F1_var / F1_tail largely reconstruct mean-logprob-like structure, while F3_slice_gap leaves a weak hysteresis residual”。不宜写“98% mean-PPL reparameterization”这类过精确数字，除非补出直接、公开、同源的计算轨迹。fileciteturn4file0L15-L15 fileciteturn2file1L28-L30

[LOCAL] **raw per-token logprob persistence 目前确实是缺口。** `highorder_ppl_run.py` 在内存里收集了每个 \((s,g)\) 的 per-token `LP[(s,g)]` 数组与 token target，然后只把 `rows`、gateA、gateB、verdict 等聚合结果写入 `highorder_result.json`；而当前 `highorder_result.json` 公开保存的是 50 个聚合 row，每个 row 只有 `mean_lp`、`F1_var`、`F1_tail`、`F3_slice_rare/freq/gap` 等摘要字段。由此可知，**任意新 bin 的 T3 重算目前不能直接在现有 json 上完成**，除非重新 CPU 评估或补存原始 logprob 阵列。fileciteturn11file0L66-L79 fileciteturn13file0L1-L4 fileciteturn14file0L5-L14

[GAP] **v1.0 manifest completeness 仍需补对账。** 仓库 manifest 明确列出了 `./chain_logs/phase1_robust_20260510_125805.master.log`。因此研究-only bundle 若缺这一文件，就不是“可以忽略的细枝末节”，而是一个应单列的 archive completeness gap。fileciteturn15file0L21-L23

[LOCAL] **按任务附带的 migration audit 说明，E9 目前只能安全写成“seed1 / cell00 的 matched baseline 支持 hump 非旧链 artifact”，不能扩写成 full Stage-A 完成；同样，cubic gate 已 broken，因此所有高阶结论都应以 LOSO / permutation / matched-mean pair 为主写法。** 这些都属于当前 paper 文字层必须同步反映的降级条件。

## Literature map and paper-safe wording

[WEB] **Shumailov et al., arXiv:2305.17493**：覆盖“递归训练导致 tails 消失、并带来不可逆缺陷”的主干命题；**不覆盖** MaoField 的 F3 是否是独立坐标，也不覆盖 base-reset vs Borkar。citeturn5view1

[WEB] **Dohmatob et al., arXiv:2402.07043**：覆盖 tail-collapse / scaling-law change / synthetic-data-induced decay 的理论语言；**不覆盖** MaoField 的具体 slice-gap 定义或 matched-mean hysteresis 测度。citeturn4view3

[WEB] **Suresh et al., arXiv:2412.17646**：覆盖离散分布下“忘掉一个词的时间与原始出现频次近似线性相关”，因此对 rare/frequent differential collapse 有直接相关性；**不覆盖** MaoField 的 two-slice hysteresis 几何。citeturn7view0

[WEB] **Guo et al., arXiv:2311.09807**：覆盖 lexical / semantic / syntactic diversity 递归下降，并且明确讨论 distinct-\(n\) 类多样性指标；**不覆盖** MaoField 的 PPL-hump、decode sign flips、base-reset。citeturn5view0

[WEB] **Gerstgrasser et al., arXiv:2404.01413**：覆盖 replace 与 accumulate 两类 recursive-training workflow 的分野，并说明 accumulate real+synthetic data 可避免 collapse；**不覆盖** MaoField 的 channel-invariance、T3、F3。citeturn4view2

[WEB] **Schaeffer et al., arXiv:2503.03150**：覆盖 “model collapse” 至少有八种互相冲突定义，属于 metric / workflow / threat framing 的上位审计文献；**不覆盖** MaoField-specific 线性桥或 F3 toy。citeturn3view1

[WEB] **Borji, arXiv:2410.12954**：覆盖“collapse 结论会随 distance metric 改变”这一 generic caution；**不覆盖** MaoField 的 \(D\)-PPL 具体桥、\(\tfrac12(B+C)\) 这种项目内结构式。citeturn3view0

[WEB] **Borkar, arXiv:2506.09401**：覆盖“是否存在哪怕极小的 external source，会把递归训练带向两种不同 asymptotic behaviour”这一主命题；**不覆盖** MaoField base-reset 的 operator-level prior 结构，也没有直接给出 η/T-response 的 param-space 判别。citeturn4view0

[WEB] **Gu et al., arXiv:2601.03385**：覆盖 embedding Gram matrix 谱的 collapse metric，即 representation-space spectral monitor；**不覆盖** MaoField 的 grounded channel claims、T3 的 token-bin 线性函数、base-reset。citeturn4view1

[WEB] **Tong, arXiv:2511.20503**：覆盖 support/topology-oriented structural pathology metric；**不覆盖** MaoField 的 recursive text setup、F3、channel-invariance。citeturn2academia0

[LOCAL][INFERENCE] **可安全入 abstract 的最窄表述**可以写成：
“MaoField currently contributes a falsifiable measurement-audit program for recursive-training collapse rather than an unconditional theorem. In the regimes tested so far, multiple candidate collapse metrics proposed to be independent of perplexity repeatedly reduce to perplexity/mean-logprob or effective-support shadows, fall below late-generation seed-noise floors, or change sign under decoding choices. A weak residual exception remains in a slice-gap hysteresis statistic inside the log-probability object, but it is presently best treated as a measurement instantiation of mechanisms already close to prior tail-collapse and irreversibility literature, not as an independent positive finding. The main mathematical object is therefore an audit operator family based on nuisance projection, residual survival, noise-floor exclusion, decode invariance, identifiability/rank tests, and η/T-response discrimination.” 这段话与当前仓库绑定态一致。fileciteturn2file1L26-L31 fileciteturn4file0L11-L15 fileciteturn5file0L20-L40 fileciteturn8file5L108-L113

[LOCAL] **必须进入 blacklist 的表述**包括：
“unconditional theorem”；“all collapse metrics reduce to mean-PPL”；“F3 is an independent positive finding”；“first dialectical materialism / first reflexive AI / paradigm shift / universal solution / mitigation framework”；以及任何把哲学写成数学起点的句子。仓库当前 active binding 与 PHILO 索引都把这些表述列为撤回或禁止复活对象。fileciteturn2file1L33-L38 fileciteturn9file1L22-L27

[GAP] **仍未闭合的口子**只有在明确标 gap 的前提下才能写进正文：T2 sufficient-side code 尚缺；T3 arbitrary-bin kill-test 尚未跑通到可公开级；highorder 原始 per-token logprobs 未持久化；manifest completeness 需对账；E9/E10/E5/E11 的 trace hygiene 还要统一改写；Borkar vs base-reset 的高维/operator wedge 仍是 open discriminator，而不是已保留下来的 theorem。当前最好的策略不是再拔高 MaoField，而是继续把它压成一套**可失败、可复算、可被外部反例击穿的数学审计程序**。