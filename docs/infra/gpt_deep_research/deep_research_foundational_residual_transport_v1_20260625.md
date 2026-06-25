# A. 一页裁决 🧪

**裁决：保留数学项目，杀掉经验阳性叙事。**

这里有一个严肃的有限维数学对象：**finite weighted residual transport / holonomy / operator no-go package**。它不是“已经观察到的 MaoField 场”，而是一套可定义、可反驳、可证明 no-go、可做合成控制的投影—传输算子框架。仓库当前也把该方向明确放在 debranded 数学线内，而不是 MaoField empirical upgrade：formal-start 目录写明 MaoField 仍是负中心 measurement-audit case，本目录只研究有限加权残差传输/holonomy/operator no-go；toy harness 通过也不等于观察到 MaoField residual field，且不授权 full panel、checkpoint loading、training 或 new loss。

**最强可说结论仍然只有：**

```text
definitions_and_harness_viable_only
```

这在仓库 README、harness summary、JSON 里一致出现；含义是“定义可在 toy finite systems 上执行，并有正/反控”，不是经验发现。

**严格答案：**

* **Mode A 数学线：保留。** 它有清楚母对象：加权有限 Hilbert 空间、预结果 nuisance 子空间、加权正交残差、固定尺度传输、edge defect、square holonomy defect。Formal Note v0 已经把核心投影、边缺陷、edge no-go、square no-go、rank-1 guard、random subspace guard、gluing absorption、product-weight boundary 写成初版。
* **Mode B MaoField 证据线：不升级。** 当前不允许说 full panel、16-cell aggregate、residual/interaction/transport/holonomy field、LOSO、F3、glass-box、training、new loss。
* **最好的 v1 方向：不是“证明有场”，而是写成 operator/no-go note。** 如果结构被 random axes、rank guard、coarsening/refinement、gluing absorption 杀死，那不是失败，而是项目成功地产生了 projection artifact/no-go 分类。仓库 core description 也明确：项目可通过定义、no-go theorem、counterexample、rank/random/coarsening/gluing artifact 分类而成功，不需要 MaoField positive result。

我的严格判断：**数学对象成立；经验对象未成立。**
应继续写 Formal Note v1，但写法必须是“定义—命题—反例—kill gates”，不是“发现—命名—装饰”。

---

# B. Formal definitions

## B1. Admissible finite weighted system

一个尺度 (s) 上的 admissible system 是三元组

[
\mathcal A_s=(X_s,w_s,N_s)
]

其中：

[
X_s \text{ finite},\qquad
w_s:X_s\to \mathbb R_{>0},\qquad
H_s=L^2(X_s,w_s),
]

[
\langle f,g\rangle_s=\sum_{x\in X_s} w_s(x)f(x)g(x),
]

[
N_s\le H_s
]

是**pre-outcome / outcome-independent nuisance subspace**。Formal Note v0 已定义这一层，并给出 weighted projection formula。

若 (A_s) 是 (N_s) 的列基矩阵，(W_s=\operatorname{diag}(w_s))，则 nuisance projection 为

[
Q_s=A_s(A_s^\top W_s A_s)^+A_s^\top W_s,
]

residual projection 为

[
P_s=I-Q_s=\Pi_{N_s^{\perp},w_s}.
]

对 (K_s\in H_s)，定义 residual representative：

[
R_s(K)=P_sK_s.
]

它是商类 (K_s+N_s\in H_s/N_s) 的唯一 (N_s^\perp) 代表，也是最小范数代表。

## B2. Nuisance admissibility

(N_s) 可包含：

[
\text{constant, main effects, registered slopes, smooth trends, matched mean/slope templates, coarse pullbacks}
]

但不得包含由 (K_s) 后验拟合出来的方向。Formal-note outline 已把 nuisance 允许项和禁止 outcome-derived directions 写清。

**v1 建议写成定义：**

[
N_s=\operatorname{span}{\phi_{s,1},\dots,\phi_{s,d_s}},
]

其中每个 (\phi_{s,i}) 必须由 schema、axis、weight、pre-registered template、或 transport structure 生成，而非由 outcome (K) 生成。

## B3. Scale graph and raw transports

一个 residual transport system 是

[
\mathfrak S=(G,{\mathcal A_s}*{s\in V(G)},{C*\rho}_{\rho\in E(G)}),
]

其中 (G) 是有限有向尺度图；每条边

[
\rho:s\to t
]

配一个预先固定的线性映射

[
C_\rho:H_s\to H_t.
]

典型合法例子：weighted block average、pullback、显式 weighted adjoint。Formal Note v0 已要求 (C_\rho) 在 outcome 之前固定。

## B4. Edge defect

结构算子：

[
E_\rho=C_\rho P_s-P_tC_\rho.
]

对信号 (K_s)：

[
D_\rho(K)=E_\rho K_s
= C_\rho P_sK_s-P_tC_\rho K_s.
]

解释：它精确测量“先去 nuisance 再传输”与“先传输再去 nuisance”的不交换。Formal Note v0 已定义该式。

应同时记录：

[
|D_\rho(K)|*t,
\qquad
|E*\rho|*{s\to t},
\qquad
\frac{|D*\rho(K)|*t}{\max(|C*\rho P_sK|*t,|P_tC*\rho K|_t,\epsilon)}.
]

## B5. Projected path transport

给定路径

[
p:s_0\xrightarrow{\rho_1}s_1\xrightarrow{\rho_2}\cdots
\xrightarrow{\rho_m}s_m,
]

定义 raw path transport

[
C_p=C_{\rho_m}\cdots C_{\rho_1},
]

定义 projected path transport

[
\widehat C_p
============

P_{s_m}C_{\rho_m}P_{s_{m-1}}\cdots P_{s_1}C_{\rho_1}P_{s_0}.
]

## B6. Square holonomy defect

若 (p,q:s_0\to s_2) 是同端点的两条路径，则

[
\Omega_{p,q}=\widehat C_p-\widehat C_q,
]

[
H_{p,q}(K)=\Omega_{p,q}K_{s_0}.
]

这才是合法 holonomy defect：一个终点 Hilbert space (H_{s_2}) 里的明确差向量。Formal Note v0 已把 square holonomy 定义为两条 projected path 的差，并强调它不是任意 discrepancy 的美名。

## B7. Equivalences

### 1. Nuisance-gauge equivalence

[
K\sim_N K'
\quad\Longleftrightarrow\quad
K_s-K'_s\in N_s
\quad \forall s.
]

于是：

[
P_sK_s=P_sK'_s.
]

### 2. Transport-isomorphism equivalence

两个系统 (\mathfrak S,\widetilde{\mathfrak S}) 等价，若存在 weighted isometries

[
U_s:H_s\to \widetilde H_s
]

满足：

[
U_sN_s=\widetilde N_s,
\qquad
U_tC_\rho=\widetilde C_\rho U_s.
]

Formal-note outline 已列出这两层 equivalence，并要求只使用 equivalence-invariant claims。

## B8. Invariants

合法 invariant families：

[
{|R_s(K)|_s}_s,
]

stacked residual singular spectrum,

[
\sigma_1\ge\sigma_2\ge\cdots,
]

principal-angle profile,

[
{\theta_i(E_s,E_t)},
]

edge defect profile,

[
{|D_\rho(K)|*t}*\rho,
]

square holonomy profile,

[
{|H_{p,q}(K)|*{s_2}}*{p,q},
]

random same-dimensional subspace capture quantile,

[
\operatorname{Quantile}_{E\sim \mathrm{Gr}(r,N_s^\perp)}
\big(\operatorname{capture}(E;K)\big),
]

and transport-stable rank.

仓库 adoption note 已把 residual norms、singular values、principal angles、edge/square defects、random subspace quantiles、transport-stable rank 列为 accepted invariant families。

---

# C. Theorem / no-go / counterexample agenda

按优先级排序。

## 1. Edge commutation lemma

**Statement.** For one edge (\rho:s\to t),

[
C_\rho P_s=P_tC_\rho
]

if and only if

[
C_\rho(N_s)\subseteq N_t
]

and

[
C_\rho(N_s^\perp)\subseteq N_t^\perp.
]

**Proof sketch.**
For (n\in N_s), (P_sn=0). Commutation gives (P_tC_\rho n=0), so (C_\rho n\in N_t).
For (r\in N_s^\perp), (P_sr=r). Commutation gives (C_\rho r=P_tC_\rho r), so (C_\rho r\in N_t^\perp).
Conversely decompose (v=n+r), apply both inclusions.

Formal Note v0 states this lemma already; v1 should promote it to a full lemma with weighted Hilbert-space notation.

## 2. Square holonomy no-go

**Statement.** Suppose (p,q:s_0\to s_2) are two paths in a square. If every edge on both paths commutes with endpoint residual projections and

[
C_p=C_q,
]

then

[
\widehat C_p=\widehat C_q
]

and hence

[
H_{p,q}(K)=0
\quad \forall K.
]

**Meaning.** Nonzero holonomy can only appear when raw transport differs, projections/nuisance are non-functorial, or some edge leaks nuisance into residual. Formal Note v0 states the no-go in this form.

## 3. Rank-1 shadow vacuity theorem

**Statement.** Let residuals across conditions/checkpoints be stacked as rows of (M). If

[
\operatorname{rank}(M)=1,
]

then

[
R_i=c_i u
]

for one template (u). All apparent stability is scalar brightness along one direction.

**Kill gate.**

[
\sigma_2/\sigma_1 < 0.25
\quad\Rightarrow\quad
\texttt{killed_by_rank1_shadow}.
]

Formal Note v0 correctly says the 0.25 floor is a guardrail, not a discovery threshold.

## 4. Random same-dimensional subspace indistinguishability

**Statement.** Fix residual ambient space (V=N_s^\perp) and dimension (r). If a named subspace (E\le V) does not exceed the empirical/null distribution of

[
E_{\mathrm{rand}}\sim \mathrm{Gr}(r,V)
]

under the same weighted geometry, then (E) has no coordinate-invariant content.

**Precise test.**

[
\operatorname{capture}(E;K)

>

Q_{0.95}{\operatorname{capture}(E_{\mathrm{rand}};K)}.
]

Failing this does not prove absence of all structure, but it kills the named coordinate claim.

## 5. Gluing absorption no-go

**Statement.** For local models on (U_i,U_j) with overlap mismatch (m_{ij}\in H_{ij}), let (N_{ij}^{\mathrm{allow}}) be the allowed overlap nuisance. If

[
\Pi_{(N_{ij}^{\mathrm{allow}})^\perp}m_{ij}=0,
]

then the mismatch is gauge/nuisance, not a gluing obstruction.

**Meaning.** Do not rename local nuisance mismatch as sheaf content.

## 6. Non-product-weight counterexample to naive Hoeffding language

**Counterexample.** Let (X={0,1}\times{0,1}), order cells as (00,01,10,11), and use observed weight

[
w=(0.2,0.2,0.2,0.4).
]

Its product-of-marginals reference is

[
w^\Pi=(0.16,0.24,0.24,0.36).
]

Let additive nuisance be

[
N=\operatorname{span}{1,q,b},
]

and signal

[
K=(1,-1,-1,1).
]

Weighted residual under observed (w):

[
P_wK=(1.142857,-1.142857,-1.142857,0.571429)
\propto (2,-2,-2,1).
]

Product-reference residual:

[
P_{w^\Pi}K=(1.44,-0.96,-0.96,0.64)
\propto (2.25,-1.5,-1.5,1).
]

They differ. Therefore, non-product weighted projection residual is not canonical product-measure Hoeffding interaction. This matches the repository boundary: current q4×tokenpos4 weights are verified non-product, and current legal language is “non-product weighted hierarchical projection / residual program.”

This is also aligned with the broader ANOVA literature: dependent/non-product measures require generalized decomposition or projection language, not naive independent/product Hoeffding language. Rahman’s generalized ANOVA decomposition explicitly addresses dependent probability measures and notes that dependence can alter component functions and sensitivity rankings.([arXiv][1])

## 7. Projection/evolution commutator leakage theorem

Let (P=\Pi_{N^\perp,w}) and (T:H\to H) be a linearized evolution operator.

**Statement.**

[
[P,T]=0
]

if and only if

[
T(N)\subseteq N
\quad\text{and}\quad
T(N^\perp)\subseteq N^\perp.
]

If not, (T) leaks nuisance into residual or residual into nuisance.

**Kill rule.** Nonzero commutator is not automatically structure. It becomes interesting only if it survives random-axis, rank, matched-template, and gluing controls.

## 8. Multiscale non-naturality counterexamples

Construct (4\times4\to2\times2) examples where:

1. raw block averaging is fixed;
2. fine-scale nuisance includes all additive effects;
3. coarse nuisance omits one pullback/main-effect component.

Then

[
C_\rho P_s\ne P_tC_\rho.
]

This proves that stable-looking fine residuals can fail to define a natural scale object.

## 9. Outcome-derived nuisance trivialization no-go

**Statement.** If (N_s) may be chosen after seeing (K_s), then any residual claim is vacuous: choose (N_s\ni K_s), then (P_sK_s=0); choose (N_s\perp K_s), then (P_sK_s=K_s).

Therefore nuisance must be fixed pre-outcome.

## 10. Product-reweighting separation lemma

If one introduces a product reference (\widetilde w=\bigotimes_j \widetilde w_j), the resulting residual object lives in

[
L^2(X,\widetilde w),
]

not in

[
L^2(X,w_{\mathrm{observed}}).
]

So product-reweighted Hoeffding analysis may be mathematically legal, but it is a different geometry. It cannot be reported as the observed weighted residual object.

---

# D. Review of Formal Note v0

## What v0 gets right

1. **Core triple is correct.**
   ((X,w,N)), (H=L^2(X,w)), weighted projection, residual representative: sound finite-dimensional construction.

2. **Edge defect is the right commutator.**
   (D_\rho(K)=C_\rho P_sK_s-P_tC_\rho K_s) is exactly the meaningful edge object.

3. **Edge no-go lemma is correct.**
   The two-inclusion characterization is mathematically valid.

4. **Square holonomy no-go is conceptually right.**
   Holonomy only means path-dependence after raw transports, projections, nuisance, weights, and equivalences are fixed.

5. **Product-weight warning is essential.**
   v0 correctly blocks canonical Hoeffding language for non-product weights.

## Gaps and required v1 fixes

| Area                    | v0 gap                                                                            | v1 fix                                                                                                      |
| ----------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Projection theorem      | Projection formula stated, but not proved as (W)-orthogonal idempotent            | Add lemma: (Q_N^2=Q_N), (\operatorname{im}Q_N=N), (Q_N) is self-adjoint under (\langle\cdot,\cdot\rangle_w) |
| Quotient representative | “minimum-norm representative” stated but quotient norm/equivalence not formalized | Define (H/N), prove (P_NK) minimizes (|K+n|_w)                                                              |
| Nuisance admissibility  | “pre-outcome” said, but no allowed-information sigma-algebra                      | Define allowed source structure: axes, weights, templates, transports; ban outcome-derived directions       |
| Scale graph             | Finite graph stated, but path/category composition not formalized                 | Treat (G) as finite directed graph with composable paths; define (C_p), (\widehat C_p)                      |
| Transport maps          | (C_\rho) allowed arbitrary linear maps                                            | Split admissible coarsening, refinement, adjoint/pullback; require source-fixed and type-compatible         |
| Edge defect             | Only signal-level defect                                                          | Add structural operator (E_\rho=C_\rho P_s-P_tC_\rho) and operator norm                                     |
| Square holonomy         | Path notation too compressed                                                      | Define two paths (p,q), raw equality (C_p=C_q), projected equality (\widehat C_p=\widehat C_q)              |
| Equivalence             | v0 lacks full equivalence section                                                 | Add nuisance-gauge and transport-isomorphism equivalence from outline                                       |
| Invariants              | v0 lists guards but not invariant families                                        | Add residual norm, singular spectrum, angles, edge/square profiles, random quantiles, transport-stable rank |
| Rank floor              | 0.25 stated                                                                       | Say explicitly: design-review floor, not universal theorem                                                  |
| Random guard            | No capture statistic/null law specified                                           | Define weighted Grassmann sampling, statistic, seed, split, multiplicity handling                           |
| Gluing                  | (P_{N_{\text{overlap}}}) notation risks confusion                                 | Use (P^{\mathrm{res}}*{ij}=\Pi*{(N_{ij}^{allow})^\perp})                                                    |
| Product weights         | Correct warning but no counterexample                                             | Insert 2×2 counterexample above                                                                             |
| Dynamic paths           | Mentioned in project prompt, absent in v0                                         | Add (T_g), ([P,T_g]), principal angles over generation                                                      |
| Kill gates              | v0 says modest deliverable, but no fail-closed contract                           | Add explicit verdict map: invalid / killed / insufficient / eligible-only                                   |

---

# E. Review of the seven-block synthetic harness

## What it proves

The harness proves exactly this:

```text
Small finite weighted operator definitions are executable.
The seven toy positive/negative controls are separable.
The JSON schema records seed, random draws, blocked claims, and verdict.
```

The repo summary says this is a zero-GPU toy harness and explicitly not a MaoField empirical result; strongest allowed verdict remains `definitions_and_harness_viable_only`.

The seven blocks all pass:

```text
non_product_weighted_projection
edge_defect
square_holonomy
rank_shadow_guard
random_subspace_guard
gluing_absorption
commutator_obstruction
```

with key metrics such as non-product residual difference (0.0271), bad edge defect (0.4636), bad square holonomy (1.1944), rank-1 (\sigma_2/\sigma_1\approx 9.7e{-17}), multidirectional (\sigma_2/\sigma_1\approx0.2529), random p95 (0.5859), and bad commutator (0.4062).

I also reran the uploaded script locally. Excluding `created_utc`, the rerun JSON matches the archived JSON exactly. The different full-file hash is only timestamp-driven.

## What it does **not** prove

It does **not** prove:

```text
residual_field_observed
interaction_field_observed
quotient_residual_field_observed
transport_field_observed
holonomy_field_observed
glass_box_broken
training_authorized
new_loss_authorized
```

These blocked claims are explicitly listed in the JSON.

It also does not prove:

* robustness to high dimension;
* real q2/q4/q8 or tokenpos2/4/8 stability;
* empirical MaoField aggregate existence;
* random-axis superiority on real axes;
* seed/generation holdout;
* product Hoeffding legality;
* theorem correctness;
* threshold universality.

## Missing positive controls

Add:

1. **Exact product-weight equality control**
   If (w=w_Q\otimes w_B), product-Hoeffding interaction and weighted projection residual should match.

2. **Known transport-stable multidirectional object**
   Construct a residual family with two independent directions that survives (4\times4\to2\times2).

3. **Known raw path equality square**
   Assert (C_p=C_q) numerically before measuring projected holonomy.

4. **Known nonzero gluing obstruction not absorbable by nuisance**
   Current checkerboard is good; add a larger cover with multiple overlaps.

5. **Evolution block-diagonal positive control**
   A (T) preserving (N\oplus N^\perp) should have ([P,T]=0).

## Missing negative controls

Add:

1. **Outcome-derived nuisance invalidation**
   Deliberately include (K) in (N); harness must label artifact invalid, not pass.

2. **Random equal-cell-count axes**
   Same dimensions, same occupancy, random labels.

3. **Within-axis shuffles**
   Shuffle token-position labels or frequency bins while preserving counts.

4. **Bad audit axis**
   Use `audit_block_id`-style axis; named axis must not beat this trivially.

5. **Rank-1 plus noise floor**
   (R_t=c_tu+\epsilon_t); ensure small noise does not fake (\sigma_2/\sigma_1).

6. **Product-reweighting separation**
   Show reweighted product geometry yields a different object and must be labeled separately.

7. **Coarsening non-naturality trap**
   Fine residual coherent, coarse nuisance incompatible; edge defect must kill.

---

# F. Formal Note v1 outline

## Title

```text
Finite Weighted Residual Transport:
Definitions, No-Go Lemmas, and Synthetic Kill Gates
```

## 0. Boundary

State at top:

```text
This is Mode A mathematics.
It is not MaoField empirical evidence.
Strongest current verdict: definitions_and_harness_viable_only.
```

Cite current repository boundary.

## 1. Finite weighted Hilbert systems

Definitions:

[
(X_s,w_s,N_s),\quad H_s=L^2(X_s,w_s),\quad Q_s,\quad P_s.
]

Lemma 1:

[
Q_s=A(A^\top W_sA)^+A^\top W_s
]

is the (w_s)-orthogonal projection onto (N_s).

Lemma 2:

[
P_sK_s
]

is the minimum-norm representative of (K_s+N_s).

## 2. Admissible nuisance

Definition: (N_s) must be source-fixed and pre-outcome.

Proposition:

```text
If nuisance may be outcome-derived, residual claims are vacuous.
```

Proof: choose (N_s\ni K_s) to kill or (N_s\perp K_s) to preserve.

## 3. Scale graph and transports

Define (G), (C_\rho), (C_p), (\widehat C_p).

Add admissible transport classes:

* weighted conditional expectation / block average;
* pullback;
* weighted adjoint;
* explicitly registered arbitrary linear map, labeled non-natural.

## 4. Edge defect

Definition:

[
E_\rho=C_\rho P_s-P_tC_\rho.
]

Theorem:

[
E_\rho=0
\iff
C_\rho(N_s)\subseteq N_t
\text{ and }
C_\rho(N_s^\perp)\subseteq N_t^\perp.
]

Proof as above.

## 5. Square holonomy

Definition:

[
\Omega_{p,q}=\widehat C_p-\widehat C_q.
]

Theorem:

If all edge defects vanish and (C_p=C_q), then (\Omega_{p,q}=0).

Counterexample:

Construct square with (C_p=C_q) but one middle nuisance non-functorial; (\Omega\ne0).

## 6. Product and non-product weights

Definition of product carrier:

[
w(x_1,\dots,x_d)=\prod_jw_j(x_j).
]

Theorem:

Classical product-measure Hoeffding decomposition is legal only in product geometry.

Counterexample:

Insert 2×2 example above.

Academic note: generalized/dependent ANOVA exists, but it is not the same as naive product Hoeffding. Rahman’s dependent-measure ANOVA and later generalized polynomial decomposition make this distinction explicit.([arXiv][1])

## 7. Rank and random-subspace guards

Theorem:

Rank-1 residual stacks are scalar brightness paths.

Definition:

[
\operatorname{capture}(E,K)
===========================

\frac{|\Pi_EK|}{|K|}.
]

No-go:

If named (E) does not beat Grassmann null, no coordinate-free claim.

## 8. Gluing

Define finite cover ({U_i}), restriction maps, local residual sections (r_i), overlap mismatch

[
m_{ij}=r_i|*{ij}-r_j|*{ij}.
]

Absorption lemma:

[
\Pi_{(N_{ij}^{allow})^\perp}m_{ij}=0
\Rightarrow
\text{no obstruction}.
]

Only non-absorbed mismatch can be called gluing obstruction. This is consistent with the sheaf-theoretic idea that obstruction claims concern failure of local data to extend/glue globally, not arbitrary local disagreement.([arXiv][2])

## 9. Evolution commutator

Define linearized evolution (T_g).

Theorem:

[
[P,T]=0
\iff
T(N)\subseteq N
\text{ and }
T(N^\perp)\subseteq N^\perp.
]

Interpret nonzero ([P,T]) only after kill gates.

## 10. Synthetic harness contract

List seven blocks plus added controls.

Verdict map:

```text
invalid_artifact
killed_by_rank1_shadow
killed_by_random_axis
killed_by_coarsening
killed_by_gluing_absorption
insufficient_artifact
definitions_and_harness_viable_only
eligible_for_next_design_review_only
```

No harness result may produce `observed_field`.

---

# G. Forbidden statements

Do **not** say:

```text
A full MaoField panel has run.
A 16-cell full-panel aggregate exists.
A hypercube residual field has been observed.
An interaction field has been observed.
A quotient-residual field has been observed.
A residual transport field has been observed.
A holonomy field has been observed.
LOSO passed.
F3 is positive.
The glass box was broken.
Training is authorized.
A new loss is authorized.
The seven-block harness is empirical evidence.
The q4 x tokenpos4 carrier is canonical product-measure Hoeffding.
Passing random-subspace/rank/coarsening toy checks means object observed.
Philosophical language can substitute for definitions or proof.
```

The repo status file lists the main forbidden upgrades directly.

Also do **not** say current q4×tokenpos4 is classical product Hoeffding unless a future exact product measure or explicit product reweighting is introduced and labeled as a different geometry.

---

# H. 初中版解释 🧩

想象你有很多张小表格。旧故事说：“这些表格里有一个很深的形状。”

现在更严格的做法是：先把所有容易骗人的痕迹擦掉。

擦掉什么？

```text
平均数
主效应
平滑趋势
分箱造成的假形状
随机坐标轴
低秩模板
只是一条亮暗变化的方向
局部 patch 可以吸收掉的错位
```

擦完以后问一句：

> 还剩下一个真正的形状吗？

如果剩下，而且它在换尺度、换路径、换随机轴、做 rank guard、做 gluing test 后还保持同一身份，那它才是一个值得研究的数学对象。

如果不剩下，也不是白做。那就证明：以前看起来复杂的东西，其实只是平均数、坐标选择、分箱、低秩影子或投影伪影。

**目前结论：**

```text
MaoField 数据里的“真实形状”还没有被证明存在。
但“如何严格判断有没有真实形状”的数学工具，已经值得继续 formalize。
```

这就是最干净的方向：
**不是救旧 claim，而是建立一个能杀死弱 claim 的有限维残差传输数学框架。**

[1]: https://arxiv.org/abs/1408.0722?utm_source=chatgpt.com "A Generalized ANOVA Dimensional Decomposition for Dependent Probability Measures"
[2]: https://arxiv.org/abs/1805.08927?utm_source=chatgpt.com "Assignments to sheaves of pseudometric spaces"
