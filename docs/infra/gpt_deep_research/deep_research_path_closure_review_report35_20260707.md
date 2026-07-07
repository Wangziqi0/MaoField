# MaoField 路径闭合审查报告

## 核心裁决

**裁决：`PATCH_DEFINITIONS_THEN_RECHECK`。**

基于上传 ZIP 的当前状态，我的判断不是“方向错误”，也不是“已经可以直接宣称形成完整 bounded formal note”，而是：**这条线已经足够窄，能够成为一个 bounded formal note；但在正式进入 note 之前，必须先把 chart/path/cycle 的类型、合成规则、范数约定与路径缺陷的组合恒等式写成明确的有限维线性代数定义。** 这一步做完后，再进入 Pro 复核，路线是稳的。

更具体地说，仓库里现有的 v1.3 order-defect spine、D706 OI corollary、D707 v1.6 quantitative OI，已经形成一个真正可依赖的有限维数学骨架；而 `Material-Relation Path Closure for Finite Metric Objects` 目前仍处在 programme brief / next-proof-task source 级别，尚未升格为干净的 formal note。这个判断与仓库中对“programme framing 不是 theorem”“禁止把 JSON / harness 当证明”“禁止过早 NMI-ready 声明”的边界控制是一致的。fileciteturn0file0

因此，本报告的主结论是：

- **v1.6 quantitative OI：可保留，且应当保留为“有限正权二向表上的 two-projection commutator geometry”**，不要把它升级成广义 dependent-input theory 或大而化之的 projection theory。
- **finite chart / cycle defect：定义雏形是对的，但还需要最小补丁**，尤其是路径合成、空路径恒等元、路径缺陷的端点依赖、范数空间结构。
- **finite telescoping identity：在补完合成定义后是可证的，而且证明很短，不需要任何经验性内容。**
- **压缩后的 programme distinct contribution，如果还能成立，只能是非常窄的那一块：**  
  **finite metric-object identity audit**，即“声明 chart operators 与 declared transports 后，检查 path-closure / intertwining，给出 exact defect certificates，并研究 finite cycle-iteration defect propagation”。它不是一般 validity theory，不是一般 benchmark critique，不是 judge-bias 发现，不是 IRT 标定理论，也不是 model collapse 理论。后者都有强先行工作。citeturn11view0turn12view2turn12view7turn12view9turn10academia2turn7academia0

## 数学审查

### v1.6 quantitative OI 的状态

仓库中的 v1.6 结果可以维持为一个**边界清楚的 bounded companion note**。它的数学对象仍然是 v1.3 的同一个有限正权二向表对象：`X=Q×B`、加权 Hilbert 空间 `L2(w)`、中心常数空间 `C`、两条中心主效应空间 `A` 与 `B0`、以及 `D_w=[P_B0,P_A]` 的受限算子范数。现有公式

`OI^{op}_{N_add}(w)=max_j rho_j sqrt(1-rho_j^2)`

作为两正交投影交换子范数的有限维专用化，是可接受的。这里的 `rho_j` 是 `A` 与 `B0` 的 canonical correlations / principal-angle cosines；`Z_w=(w-w_Q⊗w_B)/sqrt(w_Q w_B)` 的非零奇异值与这些 `rho_j` 对应，这一写法也与标准的双子空间几何兼容。仓库里的 v1.6 note 已经明确把它限定为“standard finite Hilbert-space two-projection commutator formula 的专门化”，这条边界是正确的。  

我建议保留它，但在正式稿中把下面几个接口点写得更硬一些：

| 接口点 | 结论 | 需要的处理 |
|---|---|---|
| `A=0` 或 `B0=0` | 没问题 | 明写“若一方零维，则最大值约定为 0” |
| `rho=1` 公共子空间块 | 在当前对象中不会造成歧义 | 明写 `A∩B0={0}` 来自 fully supported `Q×B` 与双中心化，因此不会藏着 commuting-but-nonorthogonal 的公共块 |
| `N_add` 的限制 | 没问题 | 明写 `D_w` 杀死 `C`，因此对 `N_add` 的范数可等价压到 `A+B0` 来处理 |
| 与 v1.4 witness norm 的关系 | 已有 guard，但必须强化 | 正文保留“operator norm after input normalization ≠ one fixed witness output norm” 的 normalization guard |
| `Z_w` 的奇异值约定 | 基本没问题 | 明写“取 full matrix 的非零奇异值；零奇异值贡献 0；对应 centered cross-Gram map” |

这类限定与当代 AI evaluation validity 文献的一个大方向是相容的：**分数或排名本身不是自解释对象，关键在于你到底在测什么、如何聚合、如何定义推断目标。** Binette 与 Reiter 明确主张把 AI/ML evaluation 写成 estimands 框架，否则容易发生 rank reversal；相关 construct validity 论文也强调，benchmark 若不能真正对应其声称的现实任务，就会在推断上出问题。citeturn11view0turn12view2turn12view3

### finite chart / cycle defect 的最小补丁

仓库里的 programme brief 已经给出了正确的雏形：

- chart `c` 有 `H_c, O_c, Phi_c`
- edge transport 有 `U_{c->c'}`, `T_{c->c'}`
- edge defect 为 `Delta_{c->c'} = T_{c->c'} Phi_c - Phi_{c'} U_{c->c'}`

但若要把它变成 formal note，至少要补上以下四条：

**第一条，是类型补丁。**  
必须明确：对每个 chart `c`，`H_c` 与 `O_c` 都是**有限维实赋范线性空间**，最稳妥写法是有限维实 Hilbert 空间；`Phi_c`、`U_{c->c'}`、`T_{c->c'}` 都是线性算子。否则 `||·||`、restriction、operator norm 都无从安放。

**第二条，是路径补丁。**  
对任意可合成路径  
`alpha: c0 -> c1 -> ... -> ck`  
定义

- `U_alpha = U_{c_{k-1}->c_k} ... U_{c_0->c_1}`
- `T_alpha = T_{c_{k-1}->c_k} ... T_{c_0->c_1}`

并规定空路径 `id_c` 具有 `U_{id_c}=I_{H_c}`、`T_{id_c}=I_{O_c}`。  
然后**统一定义一般路径缺陷**

`Delta_alpha = T_alpha Phi_{c_0} - Phi_{c_k} U_alpha : H_{c_0} -> O_{c_k}`。

这样，cycle defect 只是 `c_k=c_0` 的特例，而不是先写 cycle 再回头补 path。这个改动很小，但会让整个 note 变干净很多。

**第三条，是 operator norm 补丁。**  
`CID_gamma(S)=||Delta_gamma|_S||` 与 `CIC_N(gamma,S)=max_{1<=n<=N} ||Delta_{gamma,n}|_S||` 必须说明：

- `S ⊆ H_{c_0}` 是有限维子空间；
- `Delta_gamma|_S : S -> O_{c_0}`；
- 使用的是由 `H_{c_0}` 与 `O_{c_0}` 给出的 operator norm。  

这里**不需要**预先要求 `S` 对 `U_gamma` 不变；只有在要写更漂亮的增长界时，才可能另外假定不变性或统一范数上界。

**第四条，是组合律补丁。**  
把下面这个引理写进 note：

> 若 `alpha: c0->c1`、`beta: c1->c2` 可合成，则  
> `Delta_{beta∘alpha} = T_beta Delta_alpha + Delta_beta U_alpha`。

这是整个 cycle-iteration 结构的真正基础。没有它，后面的 telescoping 只是一个“看起来像真”的式子；有了它，telescoping 就是直接归纳。

### finite telescoping identity 的证明

在上述补丁加上后，仓库 brief 中的 telescoping identity 是**正确的**：

`Delta_{gamma,n}=sum_{j=0}^{n-1} T_gamma^{n-1-j} Delta_gamma U_gamma^j`.

证明很短。

先记
`Delta_{gamma,n}=T_gamma^n Phi_{c0} - Phi_{c0} U_gamma^n`。

由路径缺陷组合律，取 `alpha=gamma^n`、`beta=gamma`，得

`Delta_{gamma,n+1} = T_gamma Delta_{gamma,n} + Delta_gamma U_gamma^n`.

这就是递推式。  
当 `n=1` 时，右边退化为 `Delta_gamma`，成立。  
假设对 `n` 成立，则

`Delta_{gamma,n+1}`
`= T_gamma [sum_{j=0}^{n-1} T_gamma^{n-1-j} Delta_gamma U_gamma^j] + Delta_gamma U_gamma^n`
`= sum_{j=0}^{n-1} T_gamma^{n-j} Delta_gamma U_gamma^j + Delta_gamma U_gamma^n`
`= sum_{j=0}^{n} T_gamma^{n-j} Delta_gamma U_gamma^j`.

归纳完成。

这表明：

- **若 `Delta_gamma=0`，则所有 `n` 都有 `Delta_{gamma,n}=0`。**
- **若 `Delta_gamma ≠ 0`，则 finite-horizon defect propagation 可以做，但只能在显式范数假设下做。**

例如若 `||T_gamma||<=a`、`||U_gamma||<=b`，则有

`||Delta_{gamma,n}|_S|| <= sum_{j=0}^{n-1} a^{n-1-j} b^j ||Delta_gamma||`

进一步在 `a=b=1` 时给出线性上界，在 `max(a,b)<1` 时给出几何级数上界。这里已经足够形成一个 bounded linear-algebra corollary；**绝不需要**往“dynamic-collapse 大理论”方向扩写。这个边界也与仓库 prompt kit 对 forbidden claims 的约束一致。fileciteturn0file0

## 压缩重构完整 chain

仓库现在最需要的不是再造一条更长的叙事，而是把现有链条压缩成**“哪一环是 theorem，哪一环是 support artifact，哪一环是 empirical hypothesis，哪一环只是 programme framing”**。压缩后可以写成下表。

| 链条环节 | 当前地位 | 应如何表达 |
|---|---|---|
| 最初预印本中的 metric-object identity obstruction | **theorem + programme framing 的混合** | 已证明的硬核部分其实是“有限加权 nuisance-removal chart 下，residual-like quantity 可因处理顺序而变成程序性 artifact”；把它推广到 black-box evaluation 只应写成 programme motivation |
| finite order-defect / OI | **theorem / corollary** | v1.3 与 D706 已足够稳定：`D_w=0 iff product form`，`OI^{op}_{N_add}(w)=0 iff product form` |
| quantitative OI | **theorem** | v1.6 保留为 bounded quantitative companion，不升级为大理论 |
| “同一性不是命名，而是物质关系中的路径闭合” | **programme framing** | 这是总纲，不是证明来源 |
| cycle-iteration defect | **definition + theorem candidate** | 在补完 path composition 与 telescoping 后，可升格为 bounded note 的核心新段落 |
| black-box evaluation audit | **method schema / empirical hypothesis** | 这是将来如何把 chart、transport、defect certificate 用到真实评测上的方法论，不是数学已完成的黑箱理论 |
| NMI 路线 | **roadmap only** | 只能写 gate-based presubmission route，不得写 ready |

如果把这条链压缩成一句话，最稳的版本不是“数学证明了全部哲学”，而是：

**v1.3/D706/D707 已经给出一个有限维 exact spine，说明 evaluation-derived object 的同一性不能只靠名字授权；若要跨 chart 认同一对象，必须声明 transport，并检验 path closure / intertwining。**

这与最近关于 AI evaluation 的多个相邻方向是同向的：construct validity 论文强调 benchmark 必须真正对应声称的能力目标；estimands 框架强调 measurement、scope、data acquisition、aggregation 必须事先定义；benchmark sensitivity 研究说明换 benchmark、换样本、换表述就可能改变相对排名。MaoField 不能把这些一般性元命题当作独创。citeturn11view0turn12view2turn13academia0turn12view11

## 与相邻学术工作的比较

### 高重叠区

与 **AI evaluation validity / construct validity / estimands** 的重叠是最高的。Binette 与 Reiter 直接把 AI/ML evaluation 写成 estimands 问题，强调 measurement、population/scope、data acquisition、aggregation 若不明确，甚至会出现 rank reversals。医学 LLM benchmark construct validity 论文进一步指出：若 benchmark 不能代表现实任务，benchmark 上的“进步”不等于现实能力上的进步。BetterBench 也把 benchmark 质量问题系统化，提出 46 条 best practices，并指出很多 benchmark 缺少显著性报告与可复现性。**所以，“分数不是透明对象”“评测设计会改变结果”这一层，MaoField 绝不能声称新。** citeturn11view0turn12view2turn12view0

与 **benchmark sensitivity / contamination** 的重叠也很高。“The Benchmark Lottery” 早已说明不同 benchmark 选择本身会明显改变算法或模型的相对优劣；关于 contamination 的工作则说明，简单字符串去重不够，rephrasing 仍可泄漏测试信息并污染 benchmark。**因此，任何“指标对象受具体评测路径影响”的宽泛说法，都已经处在拥挤地带。** citeturn13academia0turn5academia0

与 **judge / rubric drift** 的重叠同样不小。LLM-as-a-judge 的位置偏置、judge-level/task-level 偏差，和 rubric 编辑虽通过 benchmark 校验却仍能在目标域产生系统性 preference drift，这些工作已经把“同一个 judge 名称或 rubric 名称不意味着同一个 evaluation object”展示得相当清楚了。**如果 MaoField 想靠“judge 会漂移”来立新，是站不住的。** citeturn12view9turn12view10turn1academia1

与 **IRT calibration** 的重叠属于方法层面的中高重叠。ATLAS 这类工作已经把 item discrimination、ability calibration、rank shift、adaptive testing 引入 LLM evaluation；“Growing Pains” 进一步用 anchor items 和固定参数校准来保持新增 benchmark 与旧 benchmark 的可比性。**所以，“跨测试形式比较需要 declared comparability machinery” 也不是 MaoField 独有。** citeturn10academia2turn12view5turn12view6

与 **referential security** 的概念重叠则是**最需要正面承认的高风险先行艺术**。这篇 2026 工作的核心就是：评测必须绑定到稳定可识别的对象；公开名称不变，但权重、prompt、retrieval、serving 等可以悄悄变，导致“同名系统”并不真的是同一系统。MaoField 的“同一性不是命名”在这里有明显近邻。**如果不主动承认这点，会显得在 novelty 上回避现成先行工作。** citeturn12view7turn12view8

### 低重叠但高误伤风险区

与 **model collapse** 的真正内容重叠反而不高。Shumailov 及后续工作讨论的是：在递归训练、尤其以生成数据替代真实数据时，分布尾部信息消失、性能退化、甚至出现 collapse；同时也有工作指出，在真实数据持续累积时 collapse 不一定不可避免。**这与 MaoField 这里的 cycle-iteration defect 不是同一个问题。** 前者是训练数据生态的递归动力学；后者是**已声明 chart / transport 下的有限维路径缺陷传播**。  

但是，一旦把 `CIC_N` 说成“collapse theory”或“dynamic-collapse foundation”，就会立刻撞上已有文献，而且是强行跨题。**这一块不能碰。** citeturn7academia0turn7academia1

### 剩余的窄贡献

如果在充分承认先行工作的前提下，还要问 MaoField 剩下什么可以成立，我的答案是：

**剩下的窄贡献，的确可以收束为 finite metric-object identity audit。**

它的差异点不在于再说一遍“benchmark 有问题”，而在于把这个问题写成一个**有限维、可声明对象、可写 defect、可做 witness、可迭代 propagation** 的 audit calculus：

- chart 不是口头上的“evaluation setting”，而是有 `H_c, O_c, Phi_c` 的有限对象；
- comparability 不是口头上的“对齐”，而是声明 `U` 与 `T`；
- identity 不是靠名字，而是检查 `T Phi = Phi U`；
- failure 不是泛泛而谈，而是给出 exact defect certificate `Delta`；
- repeated loop 的问题不是宏大叙事，而是 `Delta_{gamma,n}` 的有限迭代公式与上界。

这个剩余贡献很窄，但也正因为窄，反而能避免与 construct validity、estimands、IRT、judge bias、referential security、model collapse 这些大块领域正面重叠。它更像一个**可嵌入这些框架的局部 audit calculus**，而不是要取代它们的总理论。citeturn11view0turn12view7turn12view9turn10academia2

## 多会话推进架构

上传的 prompt kit 已经把多会话结构、forbidden claims、Mode A / Mode B 分离写得比较清楚；我的建议是保留这个总体框架，但把当前最关键的数学补丁插入到 Loop 3 之前，形成一个更稳的推进节奏。fileciteturn0file0

### 总架构

| 会话 | 角色 | 只做什么 | 不做什么 | 主要输出 |
|---|---|---|---|---|
| Codex 主会话 | 编排器 | 锁状态、发 loop、收工件、维护 claim ledger | 不证明定理；不代替各 loop 做全部工作 | `STATE_LOCK`、`CLAIM_LEDGER`、`LOOP_MANIFEST`、`ARTIFACT_INDEX`、`NMI_GATE_STATUS` |
| 隔离 loop Codex 会话 | 单任务执行 | 只处理单个 loop 的窄任务 | 不改 unrelated files；不越界升级 claim | `LOCAL_README_LOOPX`、`ARTIFACT_MANIFEST_LOOPX`、`LOOP_STATUS_LOOPX` |
| 主 Pro | 总审稿 | 综合数学、实现、方法、风险 | 不写代码主实现；不跳 gate | `MAIN_PRO_SYNTHESIS`、`NEXT_CODEX_TASKBOOK`、`NMI_READINESS_DECISION` |
| 子 Pro A | 有限数学 referee | 审 v1.3/v1.6/chart/cycle/telescoping | 不管经验 ambition | 审核 verdict |
| 子 Pro B | 实现审计 | 类型、数值、 exact arithmetic、negative controls | 不把代码当证明 | 审核 verdict |
| 子 Pro C | 经验设计 referee | synthetic / real audit 方案 | 不放行 capability claim | 审核 verdict |
| 子 Pro D | framing referee | manuscript type、field positioning | 不放大成总理论 | 审核 verdict |
| 子 Pro E | adversarial red-team | prior art、triviality、overclaim、readiness exaggeration | 不做 optimistic merge | 审核 verdict |

### loop 路线图

| Loop | 任务 | 关键工件 | 审查 gate | 主要失败模式 |
|---|---|---|---|---|
| Loop 0 | state freeze 与 claim hygiene | `STATE_LOCK`、`CLAIM_LEDGER`、`FORBIDDEN_CLAIMS_CHECKLIST` | 不得出现 overclaim | 把 programme framing 写成 theorem；把 artifact 写成 proof |
| Loop 1 | v1.3 / D706 spine 清稿 | 投影定义、`D_w`、existential witness 摘要页 | 只依赖 v1.3 chain | 混淆 true residual 与 wrong-order output |
| Loop 2 | v1.6 quantitative OI 清稿 | principal-angle note、`Z_w` interface guard、2×2 exact appendix | 只能是 finite two-projection geometry | 把 fixed witness norm 混成 operator norm；忘记空维约定 |
| Loop 3 | **chart/path typed definitions 补丁** | `H_c,O_c,Phi_c,U,T` 的 typed note；一般路径 `Delta_alpha`；composition lemma | 类型一致、端点一致 | 没写空路径恒等元；没写 path composition；范数未定义 |
| Loop 4 | **cycle defect formal note** | `Delta_gamma`、`CID_gamma`、`Delta_{gamma,n}`、`CIC_N`、telescoping proof | telescoping 由 Pro A 过关 | 直接跳到 collapse theory；把经验语句灌进 theorem |
| Loop 5 | metric-object audit schema | declared chart / transport / witness / defect-certificate 模板 | schema 可复用 | transport 未声明；gauge 未固定；输出不可审计 |
| Loop 6 | synthetic validation | negative controls、ablations、expected labels | 只能验证 pipeline，不得当 proof | synthetic result 被写成 empirical-positive |
| Loop 7 | real black-box audit | 若有 raw evaluation tables，则产 defect matrices 与 witnesses；若无则 blocked | 必须能区分 defect 与噪声/variance | 原始表缺失；chart ownership 不清；过早作强结论 |
| Loop 8 | NMI gate review | math / method / empirical / reproducibility gate matrix | 四门全过才可谈 readiness | math 未净化、data 不全、claims 超过 artifacts |

### 当前最合适的即时顺序

当前不应直接冲 Loop 6 或 Loop 7。  
**正确顺序是：Loop 0 → Loop 3 → Loop 4 → 主 Pro 复核 → 再决定是否继续。**

原因很简单：你现在最需要补的是**定义与证明接口**，不是再找更多故事。

## 可复制提示词

下面给出的是**当前版本可直接复制**的提示词。它们遵守仓库 prompt kit 的边界：禁止 empirical-positive、禁止 proof-by-JSON、禁止 observed transport/holonomy/gluing/collapse field、禁止 dynamic-collapse 大理论、禁止过早 NMI-ready。fileciteturn0file0

### Codex 主会话提示词

> 你是 MaoField 的 Codex 主编排器。只使用当前冻结状态包与上传 ZIP 中已有事实。你不证明定理，你只负责编排。请创建或更新：`STATE_LOCK_YYYYMMDD.md`、`CLAIM_LEDGER_YYYYMMDD.md`、`LOOP_MANIFEST_YYYYMMDD.md`、`FORBIDDEN_CLAIMS_CHECKLIST_YYYYMMDD.md`、`ARTIFACT_INDEX_YYYYMMDD.md`、`NMI_GATE_STATUS_YYYYMMDD.md`。  
> 把工作拆成完全隔离的 loop 会话。保持 Mode A exact math 与 Mode B empirical audit 分离。JSON、harness、deterministic scripts 只能记作 support artifacts。不得声称 NMI readiness。当前优先级是：先发 Loop 0，再发 Loop 3，再发 Loop 4。输出下一条 loop prompt、所需输入文件、阻塞项、以及不应说出的 claims。

### 通用隔离 loop Codex 提示词

> 你处于 MaoField 的一个隔离 loop 会话。你只能处理 `<LOOP_NAME>`。输入仅限 `<FILES>`。必须产出 `<ARTIFACTS>`、`LOCAL_README_<LOOP>.md`、`ARTIFACT_MANIFEST_<LOOP>.md`、`LOOP_STATUS_<LOOP>.md`。  
> 计算与脚本只作为 support artifact，不构成 proof。若涉及经验验证，必须加入 negative controls，并明确说明“这些输出不能证明什么”。如果缺少关键文件，返回 `BLOCKED_MISSING_FILES`，不得猜测。

### Loop 3 专用提示词

> 你正在执行 MaoField Loop 3。目标不是写大理论，而是把 finite chart/path/cycle defect 框架补成 typed finite-dimensional note。  
> 任务：  
> 一，显式定义每个 chart 的 `H_c`、`O_c`、`Phi_c`，并给出所用范数。  
> 二，显式定义边 `U_{c->c'}`、`T_{c->c'}` 的域、陪域与线性性。  
> 三，先定义一般路径 `alpha` 的 `U_alpha`、`T_alpha` 与 `Delta_alpha = T_alpha Phi_{c0} - Phi_{ck} U_alpha`，再把 cycle 作为特例。  
> 四，写出并核对组合引理 `Delta_{beta∘alpha}=T_beta Delta_alpha + Delta_beta U_alpha`。  
> 五，给出 `CID` 与 `CIC_N` 的 operator-norm 定义。  
> 禁止输出：经验正结果、proof-by-JSON、observed field、dynamic-collapse 叙事。输出必须注明哪些只是 definition patch，哪些已被证明。

### Loop 4 专用提示词

> 你正在执行 MaoField Loop 4。目标是把 finite cycle defect 写成 bounded formal note，而不是推广成 collapse theory。  
> 请在已冻结的 Loop 3 typed definitions 上：  
> 一，证明 `Delta_{gamma,n}=T_gamma^n Phi - Phi U_gamma^n` 的 telescoping identity；  
> 二，写出递推式；  
> 三，给出有限视窗 `CIC_N` 的基础上界；  
> 四，明确哪些额外假设才允许更强增长界。  
> 禁止把循环 defect 称为经验观察到的 collapse。禁止把有限维迭代上界扩写为一般动力系统理论。

### 主 Pro 提示词

> 你是 MaoField 的主 Pro reviewer。只依据上传 ZIP 与各 loop 工件进行审稿。保持四分法：THEOREM、SUPPORT_ARTIFACT、EMPIRICAL_HYPOTHESIS、PROGRAMME_FRAMING。  
> 你必须输出：  
> 一，当前主 verdict；  
> 二，哪些定义仍需补；  
> 三，哪些 theorem 已经足够；  
> 四，哪些边界必须重申；  
> 五，下一轮允许 Codex 做什么，不允许做什么。  
> 你不得宣称 NMI readiness，除非 math、method、empirical、reproducibility 四门全部过关。

### 子 Pro A 提示词

> 你是有限数学 referee。只审 v1.3、D706、v1.6、chart/path/cycle typed definitions、composition lemma、telescoping proof。  
> 请逐条标记：`THEOREM_ACCEPT`、`PATCH_REQUIRED`、`REJECT_AS_STATED`。  
> 忽略经验 ambition，重点检查类型、端点、范数、限制算子、零维边界、以及是否偷偷把 framing 充当 proof。

### 子 Pro E 提示词

> 你是 adversarial red-team。请优先寻找：  
> 先行艺术重叠、平凡化风险、概念偷换、proof gap、artifact masquerading as proof、过早 readiness、以及把 cycle iteration 夸成 model collapse / general black-box theory 的冲动。  
> 你的默认立场应是：能 patch 就要求 patch，不能 patch 就拒绝。

## 最窄的可成立贡献与下一步

把所有比较放在一起之后，我的判断是：

**MaoField 目前不应声称自己的独特性在于“发现评测会受条件影响”。这个命题已经被 validity、construct validity、estimands、benchmark sensitivity、IRT calibration、referential security、judge/rubric drift 等多条文献线充分覆盖。** citeturn11view0turn12view2turn12view0turn12view6turn12view7turn12view9turn12view10

**如果还有一个窄而真实的剩余贡献，它只能是：**

**一个有限维 metric-object identity audit calculus**，其最小核心包括：

- declared chart operators `Phi_c`
- declared raw/object transports `U,T`
- path-closure / intertwining 条件
- exact defect certificates `Delta`
- finite cycle-iteration defect propagation 与 telescoping identity

而且这套东西必须保持如下边界：

- 不宣称 empirical-positive；
- 不把 JSON / harness 当 proof；
- 不声称 observed transport / holonomy / gluing / collapse field；
- 不发展 dynamic-collapse 大理论；
- 不作 NMI-ready 过早声明。fileciteturn0file0

**最准确的 exact next action 是：**

由 node36 先实施 **Loop 0** 的 state freeze 与 claim hygiene；随后立刻启动一个**隔离的 Loop 3**，只做 typed chart/path definitions 与 composition lemma；在此基础上再发 **Loop 4** 证明 telescoping identity 与写 cycle note 草稿；之后交给主 Pro + 子 Pro A/E 复审。  
在这一步完成前，**不要**启动 real black-box audit，**更不要**推进任何 NMI-ready 叙述。