# MaoField / Open-MaoField：指标对象同一性、指标形式拜物教与真正解决纲领

生成日期：2026-07-04
用途：把本轮连续讨论中形成的核心判断、项目宗旨、数学楔子、查重邻域与马列毛理论支撑压缩成一份可继续用于 README、论文导言、roadmap、内部纲领的 Markdown 文档。
状态：研究纲领笔记；不是论文终稿；不是经验正结果声明。

---

## 0. 一句话总判断

MaoField 的核心不是指出当前 LLM evaluation 有问题，然后进行外部批判；它要做的是一种真正意义上的解决：建立一套底层理论，证明一个指标输出什么时候有资格被当作“同一个测量对象”，什么时候只是异质测量关系被 score-form 伪装成了同一模型属性。

更压缩地说：

> LLM evaluation 的黑箱性不只是模型内部不可见，而是指标形式把非同一的测量关系生产成同一的模型属性；MaoField 要做的不是喊这个属性是假，而是证明它什么时候有资格为真。

---

## 1. 当前对“解决”的重新定义

这里的“解决”不是形容词，也不是口号式的“批判旧范式”。它至少包含四层：

1. **定义对象**：先说明一个 score / residual / ranking / capability claim 到底是什么测量对象。
2. **给出同一性条件**：说明在 prompt、judge、rubric、decoding、weighting、aggregation、residualization chart 改变时，它什么时候仍然是同一个对象。
3. **给出 defect certificate**：当同一性失败时，不只说“不可靠”，而是给出可计算、可证明、可复现的非同一性证书。
4. **再允许 empirical audit**：只有在对象、条件、缺陷形式都清楚之后，经验测量才不会重蹈旧项目的坑。

这意味着 MaoField 的任务不是：

```text
benchmark 有问题 → 进行批判
```

而是：

```text
metric object 未被证明 → 建立同一性判据 → 给出 defect / invariance 证明 → 再进入审计
```

---

## 2. Open-MaoField 当前数学结果的真实地位

当前公开的 Open-MaoField 不是 MaoField 总理论，不是旧 MaoField empirical line 的公开证明版，也不是 LLM 内部机制解释。它是一个很小、很锋利的数学工具：

```text
finite positive weighted two-way residual audit chart
+ projection-order defect theorem
+ exact rational 2x2 certificate
```

当前定理的核心形式：

```text
product weights
⇔ A ⟂ B₀
⇔ D_w = 0
⇔ R_{Q→B} = R_{B→Q}
```

其中：

```text
R_{Q→B} = (I - P_{B₀})(I - P_A)(I - P_C)
R_{B→Q} = (I - P_A)(I - P_{B₀})(I - P_C)
D_w      = R_{Q→B} - R_{B→Q}
         = P_{B₀}P_A - P_AP_{B₀}
```

在 non-product weights 下，存在 pure main-effect witness `K`，使得：

```text
true additive residual = (I - P_{N_add})K = 0
```

但错误顺序的 sequential stripping output 非零。因此非零 output 不是 true interaction，也不是 true residual，而是 procedure artifact。

当前 exact rational certificate：

```text
w = (1/11) * [[1, 2], [3, 5]]
K = [7/11, -4/11, 7/11, -4/11]
R_{B→Q}K = 0
R_{Q→B}K = [1/32, 5/168, -1/96, -1/84]
||R_{Q→B}K||²_w = 61/177408
```

这把小刀说明：

> 指标对象的同一性不是自动给定的；即使在最小有限加权残差审计表中，measurement procedure 也能制造 residual-like object。

---

## 3. 旧项目踩过的坑与新路线的区别

旧 MaoField 的经验线不能作为 positive result。它更适合作为 deflated empirical material 和 conceptual ore。旧线反复踩到的坑包括：

```text
scalar smoothers
PPL shadows
decode artifacts
noise floors
insufficient artifacts
coordinate freedom
low-rank shadows
aggregation artifacts
```

因此新路线不能再是：

```text
先观察 residual-like signal，再尝试解释它是什么。
```

新路线必须是：

```text
先定义可解释对象，再证明同一性条件，再给出 defect certificate，最后才进入经验审计。
```

也就是说：

| 旧路线 | 新路线 |
|---|---|
| empirical residual first | identity condition first |
| 先找信号 | 先定义对象 |
| 信号容易被 smoother / PPL / decode artifact 吞掉 | 先形式化 nuisance 与 chart |
| 容易过度解释 | claim boundary 内置 |
| “我们看到了某个场” | “我们证明某类 residual object 何时不成立 / 何时成立” |
| 失败后很难回收 | 失败变成 defect certificate 或 boundary condition |

---

## 4. 核心概念一：Measurement-Object Identity Problem

建议术语：

```text
measurement-object identity problem
测量对象同一性问题
```

或：

```text
metric individualization problem
指标个体化问题
```

问题不是“score 有噪声”，而是：

> 你以为不同 chart 下的 score / residual / ranking 都是在测同一个对象，但这个同一性并没有被证明。

当前 LLM evaluation 中，常见默认假设是：

```text
score = model 的某个属性
```

MaoField 要改写为：

```text
score = model + prompt distribution + task axis + judge + rubric
        + decoding + weighting + aggregation + coordinate chart
        + residualization procedure
```

因此要问：

```text
这些不同 score expressions 为什么可以被当作同一个 metric object？
如果没有证明，它们是否只是不同对象？
```

---

## 5. 核心概念二：Metric-Form Fetishism / 指标形式拜物教

建议定义：

> **Metric-form fetishism**：异质测量关系通过 score-form 表现为模型自身客观属性的过程。

形式上：

```text
(model, prompt distribution, task, judge, rubric, decoding, weighting, aggregation, chart)
→ score
→ 被误认为 model-property
```

它不是简单的“指标错了”。更深层是：

```text
measurement relation → model property
```

这与马克思的商品拜物教结构相似：

```text
commodity fetishism:
social relation → thing-property

metric-form fetishism:
measurement relation → model-property
```

因此 MaoField 不是只做外部批判，而是要问：

```text
这种 score-form 表象什么时候有资格成立？
什么时候只是形式造成的虚假同一性？
```

---

## 6. 黑箱性的重新定义

旧理解：

```text
LLM black box = model internals opaque
```

MaoField 的更深理解：

```text
LLM evaluation black box
= model internals opaque
+ measurement apparatus opaque
+ metric identity unproven
```

也就是说，黑箱不只是“看不见模型内部”，还包括：

```text
prompt distribution 如何塑造 score
judge protocol 如何塑造 score
rubric 如何塑造 score
decoding 如何塑造 score
weights 如何塑造 score
aggregation chart 如何塑造 ranking
residualization order 如何制造 residual-like output
```

最终最危险的黑箱是：

> 指标形式把非同一的测量关系生产为同一的模型属性。

---

## 7. 马克思：从商品拜物教到指标形式拜物教

### 7.1 可用理论点

马克思在《资本论》第一卷第一章中分析商品形式和商品拜物教。他指出，商品的神秘性不来自 use-value，而来自商品形式本身；社会关系会表现为物与物之间的关系。

可转译为 MaoField：

```text
商品形式：人的社会关系表现为物的属性。
指标形式：异质测量关系表现为模型属性。
```

### 7.2 MaoField 转译

当前 score / leaderboard / benchmark claim 的问题不只是数值误差，而是形式问题：

```text
score-form 把 measurement relation 物化为 model-property。
```

这不是哲学硬加，因为 Open-MaoField 的数学对象中，`w(q,b)`、projection subspaces、residualization order、aggregation chart 都是物质测量结构。它们可以直接决定 residual-like output 是否成立。

### 7.3 链接

- Marx, *Capital Volume One*, Chapter One: Commodities
  https://www.marxists.org/archive/marx/works/1867-c1/ch01.htm

关键定位：

```text
value-form / commodity-form 分析
fetishism of commodities
social relation appearing as relation between things
```

---

## 8. 列宁：同一性不是静态相等，而是有条件的对立统一

### 8.1 可用理论点

列宁在《谈谈辩证法问题》中强调：

```text
一个统一体分裂为互相排斥的对立方面，是辩证法的核心之一。
对立面的同一 / 统一是有条件的、暂时的、相对的。
对立面的斗争是绝对的。
```

### 8.2 MaoField 转译

旧范式常默认：

```text
score A 和 score B 都叫 reasoning score，因而它们是同一个对象。
```

MaoField 要说：

```text
名称相同 ≠ 对象同一
标量形式相同 ≠ 对象同一
benchmark category 相同 ≠ 对象同一
```

真正需要的是：

```text
在指定 chart transformation 下证明 invariance / transport / equivalence。
```

### 8.3 链接

- Lenin, *On the Question of Dialectics*
  https://www.marxists.org/archive/lenin/works/1915/misc/x02.htm

关键定位：

```text
splitting of a single whole
identity / unity of opposites
conditional, temporary, transitory, relative unity
absolute struggle of opposites
```

---

## 9. 毛泽东：《矛盾论》给出的最关键补充

### 9.1 同一性只在必要条件下成立

毛在《矛盾论》中说明，同一性、统一、互相依存、互相联结，至少包含两点：

```text
1. 矛盾双方以对方存在为条件，并共处于一个统一体；
2. 在一定条件下，矛盾双方可以向对方转化。
```

最关键的转译是：

> 没有必要条件，就没有真实同一性。

MaoField 对应为：

```text
没有 product weights / orthogonality / order-independence，
sequential residual outputs 就不能自动被认作同一个 true residual object。
```

当前 Open-MaoField 小定理就是这个原则的一个有限数学实现。

### 9.2 差异本身就是矛盾

毛还批评只看到差异、看不到矛盾的观点，并指出：

```text
每一个差异已经包含矛盾；差异本身就是矛盾。
```

MaoField 转译：

```text
prompt difference 不是中性差异；可能是 metric object 的内部矛盾。
judge difference 不是中性差异；可能改变对象身份。
rubric difference 不是中性差异；可能制造非同一性。
weighting difference 不是中性差异；可能改变 residual / ranking 的性质。
aggregation difference 不是中性差异；可能发生量变到质变。
```

### 9.3 特殊矛盾防止空泛哲学

毛强调，必须研究具体事物的特殊矛盾；每一种运动形式、每一个具体过程，都有其特殊矛盾和特殊本质。

MaoField 因此不能只说：

```text
所有指标都有矛盾。
```

而必须说：

```text
每个 metric object 有自己的特殊矛盾，需要具体审计。
```

例如：

| metric object | 特殊矛盾 / audit axis |
|---|---|
| reasoning score | prompt-form reasoning vs answer-form grading |
| hallucination rate | factuality source vs judge threshold vs retrieval exposure |
| safety score | refusal vs helpfulness vs policy boundary vs rubric |
| leaderboard rank | model score vs task mixture vs weighting chart |
| LLM-as-judge score | position bias vs verbosity bias vs self-preference |
| contamination audit | memorization vs paraphrase exposure vs fresh-item condition |

### 9.4 主要矛盾与主要方面

毛关于主要矛盾的观点也可直接用于 MaoField：复杂过程有多重矛盾，其中一个矛盾会决定或影响其他矛盾的发展。

MaoField 转译：

```text
一个 evaluation pipeline 可能有 prompt contradiction、judge contradiction、rubric contradiction、weight contradiction、decoding contradiction、aggregation contradiction。
但某一阶段的 principal contradiction 可能是：
- judge-axis instability
- prompt-distribution shift
- weight non-productness
- contamination coupling
- aggregation chart instability
```

找到 principal contradiction 后，audit 才不会散掉。

### 9.5 链接

- Mao Zedong, *On Contradiction*
  https://www.marxists.org/reference/archive/mao/selected-works/volume-1/mswv1_17.htm

关键定位：

```text
identity and struggle of contradiction
necessary given conditions
no identity without necessary conditions
difference itself is contradiction
particularity of contradiction
principal contradiction and principal aspect
```

---

## 10. 恩格斯：量变到质变与 weight / aggregation

恩格斯在《自然辩证法》中把辩证法的一般规律之一概括为：

```text
quantity → quality
quality → quantity
```

MaoField 中最直接的对应不是抽象套用，而是：

```text
small weight changes
→ score changes
→ ranking changes
→ residual object changes
→ qualitative interpretation changes
```

因此未来方向包括：

```text
near-product perturbation bounds
commutator norm instability index
weight-sensitive rank stability
aggregation chart equivalence classes
```

### 链接

- Engels, *Dialectics of Nature*, Chapter 2
  https://www.marxists.org/archive/marx/works/1883/don/ch02.htm

关键定位：

```text
transformation of quantity into quality
interpenetration of opposites
negation of negation
```

---

## 11. 毛泽东：《实践论》防止纲领变成纯解释

MaoField 不能只停留在“指标拜物教”这一理论解释上。毛在《实践论》中强调，认识从实践中来，也要回到实践中去，并且通过实践检验和发展真理。

MaoField 转译：

```text
哲学概念
→ 数学对象
→ exact certificate
→ audit protocol
→ empirical boundary
→ 再修正理论
```

也就是说：

```text
不是哲学硬加，必须落成 theorem / certificate / audit。
```

### 链接

- Mao Zedong, *On Practice*
  https://www.marxists.org/reference/archive/mao/selected-works/volume-1/mswv1_16.htm

关键定位：

```text
practice → knowledge → practice
verify and develop truth through practice
```

---

## 12. 为什么这不是“哲学硬加”

它不是把马列毛术语外部贴到 LLM evaluation 上，而是存在结构同构与可形式化落点：

| 马列毛范畴 | MaoField 中的技术落点 |
|---|---|
| 商品拜物教 | metric-form fetishism |
| 社会关系表现为物的属性 | measurement relation 表现为 model-property |
| 对立统一 | prompt / judge / rubric / weight / aggregation 等 measurement axes 的内部矛盾 |
| 同一性有条件 | metric identity 需要 invariance / transport / projection 条件 |
| 差异就是矛盾 | prompt/judge/weight differences 不是中性 noise，而可能改变对象身份 |
| 特殊矛盾 | 每类 metric object 要有自己的 audit chart |
| 主要矛盾 | 每个 evaluation pipeline 要找 principal instability axis |
| 量变到质变 | weight / aggregation 小变动可能导致 ranking / residual object 质变 |
| 实践论 | theorem 和 certificate 必须进入可复现 audit protocol |

因此这条理论线不是装饰，而是项目的深层问题意识：

> 指标形式生产虚假同一性；MaoField 要证明指标同一性成立或失败的物质条件。

---

## 13. 查重 / 邻域结论

第一轮查重和邻域扫描得到的判断：

```text
直接重名或近重名：暂未发现明显同名近邻。
概念 / 数学 / LLM-eval 邻居：很多，必须正面处理。
```

### 13.1 高风险数学邻居

1. **Dependent-input ANOVA / Sobol / Hoeffding decomposition**
   - 研究输入相关时的函数分解、方差归因、sensitivity indices。
   - MaoField 不能声称开创 dependent-input decomposition。
   - 差异：MaoField 研究 finite weighted residual audit chart 中的 projection-order artifact。

2. **Shapley effects for dependent inputs**
   - 研究 dependent inputs 下变量重要性归因。
   - MaoField 不做 Shapley attribution，而是做 residual object identity / order-defect certificate。

3. **Two-projection / projection-product theory**
   - `D_w = P_{B₀}P_A - P_AP_{B₀}` 直接邻接投影乘积与 commutator 理论。
   - MaoField 不能声称是 broad projection-product theory。
   - 差异：MaoField 把 finite two-projection obstruction 放进 residual metric audit 和 black-box evaluation measurement apparatus。

### 13.2 LLM evaluation 邻居

1. **HELM / holistic evaluation**
   - 多场景、多指标评估框架。
   - MaoField 不是新 benchmark，而是审计 metric complexes 是否有 invariant residual object。

2. **LLM-as-a-judge bias**
   - position bias、verbosity bias、self-preference、judge-human agreement 等。
   - 这些是 MaoField `B` 轴或 judge-axis audit 的实证邻居。

3. **Benchmark contamination / rephrased samples**
   - contamination、paraphrase exposure、fresh-item condition 可成为 contamination-axis audit。

4. **Benchmark distributional assumptions / ranking robustness**
   - prompt distribution、correlations、aggregation weights 可能改变 rankings。
   - 是 weight-sensitive rank stability 的直接桥。

### 13.3 MaoField 的真正空位

不是：

```text
LLM evaluation is flawed
```

也不是：

```text
dependent inputs break ANOVA
```

也不是：

```text
two projections may not commute
```

而是：

```text
finite weighted residual metric audit
+ exact rational order-defect certificate
+ metric object identity problem
+ black-box LLM measurement apparatus framing
```

更短：

> 把 dependent-weight projection noncommutativity 变成 LLM evaluation residual-audit discipline。

---

## 14. 可引用的邻域论文 / 方向链接

这些不是全部，只是本轮讨论中最关键的邻居：

### Open-MaoField

- GitHub repository:
  https://github.com/Wangziqi0/Open-MaoField
- Preprint DOI:
  https://doi.org/10.5281/zenodo.21190475
- Repository/software DOI:
  https://doi.org/10.5281/zenodo.21157578

### Dependent-input decomposition / sensitivity

- Chastaing, Gamboa, Prieur — *Generalized Hoeffding-Sobol decomposition for dependent variables*
  https://arxiv.org/abs/1112.1788
- Chastaing, Gamboa, Prieur — *Generalized Sobol sensitivity indices for dependent variables: numerical methods*
  https://arxiv.org/abs/1303.4372
- Owen, Prieur — *On Shapley value for measuring importance of dependent inputs*
  https://arxiv.org/abs/1610.02080

### Projection theory

- Corach, Maestripieri — *Products of orthogonal projections and polar decompositions*
  https://arxiv.org/abs/1011.5237
- General two-projection / Halmos-neighbor search anchor:
  https://arxiv.org/search/math?query=two+projections+Halmos&searchtype=all

### LLM evaluation / measurement apparatus

- HELM — *Holistic Evaluation of Language Models*
  https://arxiv.org/abs/2211.09110
- MT-Bench / Chatbot Arena — *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*
  https://arxiv.org/abs/2306.05685
- Benchmark contamination — *Rethinking Benchmark and Contamination for Language Models with Rephrased Samples*
  https://arxiv.org/abs/2311.04850
- Benchmark distributional assumptions — *Examining the robustness of LLM evaluation to the distributional assumptions of benchmarks*
  https://arxiv.org/abs/2404.16966

---

## 15. 建议的理论形式化骨架

### 15.1 Evaluation chart

定义一个 chart：

```text
c = (P, T, J, R, D, w, A_g, S)
```

其中：

```text
P   = prompt distribution
T   = task / benchmark axis
J   = judge / evaluator
R   = rubric
D   = decoding rule
w   = weight table
A_g = aggregation chart
S   = residualization / nuisance-stripping scheme
```

指标输出：

```text
M_c(model) = score / residual / ranking / diagnostic
```

### 15.2 Metric identity condition

要说两个 chart 下的 outputs 是“同一个测量对象”，需要证明某种 invariance / transport：

```text
T_{c→c'} ρ_c(K) = ρ_{c'}(T_{c→c'}K)
```

否则不能默认：

```text
ρ_c(K) and ρ_{c'}(K') are the same object
```

### 15.3 Defect certificate

当同一性失败：

```text
D(c,c';K) ≠ 0
```

当前 Open-MaoField 的第一类 certificate：

```text
D_w(K) = R_{Q→B}K - R_{B→Q}K
```

如果：

```text
(I - P_{N_add})K = 0
```

但：

```text
R_{Q→B}K ≠ 0
```

则得到：

```text
wrong-order residual-like artifact
```

---

## 16. 建议的下一步技术对象

### 16.1 Audit Instability Index

定义：

```text
OI(w) = ||D_w||
```

或对具体 metric table `K`：

```text
OI_w(K) = ||R_{Q→B}K - R_{B→Q}K||_w
```

解释：

```text
procedural residual sensitivity
```

不是 capability score。

### 16.2 Metric-Form Fetishism 定义段

可写入 future paper：

```text
Metric-form fetishism is the process by which a heterogeneous measurement relation
(model, prompt distribution, task, judge, rubric, decoding, weighting, aggregation, chart)
appears as an objective property of the model itself.
```

中文：

```text
指标形式拜物教，是异质测量关系
（模型、提示分布、任务、评判者、评分规程、解码、权重、聚合、坐标图）
通过 score-form 表现为模型自身客观属性的过程。
```

### 16.3 Exact Certificate Library

建议目录：

```text
certificates/
  2x2_minimal_order_defect/
  2x3_product_control/
  2x3_near_product_small_defect/
  3x3_large_commutator/
  contamination_weight_coupling/
  judge_order_defect/
  ranking_instability_toy/
```

每个 certificate 包括：

```text
weights
marginals
basis
projection matrices
D_w
witness K
true additive residual
two sequential outputs
weighted norms
claim boundary
```

### 16.4 Residual Metric Audit Protocol v0.1

第一版 protocol 可包括：

```text
1. Weight-form audit
2. Order-defect audit
3. Projection audit
4. Judge-axis audit
5. Contamination-axis audit
6. Aggregation audit
7. Ranking stability audit
```

---

## 17. 写作边界：必须避免的过度声明

不要说：

```text
MaoField 已经发现 deployed model residual field
MaoField 已经解释 hallucination / reasoning / alignment mechanism
MaoField 已经证明 model collapse / recovery 的非标量结构
MaoField 已经完成 broad ANOVA / dependent-input / projection theory
Open-MaoField 是 LLM empirical positive result
harness JSON 证明 theorem
```

应该说：

```text
Open-MaoField gives a finite exact certificate that residual-like metric outputs can be procedurally non-identical under non-product weighted audit charts.
```

中文：

```text
Open-MaoField 给出一个有限精确证书：在非乘积加权审计图表中，residual-like metric output 可能在程序上并不定义同一个 residual object。
```

---

## 18. 可用的项目宗旨表述

### 18.1 中文短版

```text
MaoField 研究的是：在什么物质条件下，不同黑箱评估图表中的指标输出可以被当作同一个测量对象。它批判的核心不是某个 benchmark，而是指标形式拜物教：异质测量关系被转化为看似内在的模型属性。
```

### 18.2 中文强版

```text
MaoField 不是要指出 LLM 评估有问题再进行批判，而是要建立指标对象同一性的证明理论：当 prompt、judge、rubric、decoding、weighting、aggregation 和 residualization chart 改变时，一个 score / residual / ranking 何时仍然是同一个对象，何时已经是 measurement apparatus 生产出的另一个对象。
```

### 18.3 English version

```text
MaoField studies the material conditions under which metric outputs can be treated as identical objects across black-box evaluation charts. Its critical target is metric-form fetishism: the transformation of heterogeneous measurement relations into apparently intrinsic model properties.
```

### 18.4 Open-MaoField 定位句

```text
Open-MaoField v1.0.0 is the first finite exact certificate for this programme: even in a minimal weighted two-way residual audit chart, metric identity is conditional; without product-weight orthogonality, a sequential procedure can manufacture a residual-like object whose true additive residual is zero.
```

---

## 19. 结论

本轮讨论后的项目主线应当是：

```text
不是：批判旧测量范式。
而是：解决指标对象同一性问题。
```

也就是说：

```text
1. 指标形式会把异质测量关系物化为模型属性。
2. 这种属性是否成立，不应被默认，而应被证明。
3. 当前 Open-MaoField 的小定理证明：这种同一性至少在 residual audit chart 中不是免费的。
4. 后续 MaoField 要建立一套从 metric-form critique 到 theorem / certificate / audit protocol 的底层理论。
```

最终一句：

> MaoField 的目标不是把“旧指标有问题”说得更漂亮，而是给出一个能判定、证明和修复指标对象同一性的理论与工具系统。
