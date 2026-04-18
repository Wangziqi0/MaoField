---
name: OP1 / OP2 严格化尝试（诚实记录）
date: 2026-04-13
author: Linux Claude
status: mathematical follow-up, honest recording of what worked / what didn't
purpose: supply rigor attempts for arXiv v1 Open Problems section
---

# Open Problems 严格化尝试

本文档记录对 exp017 FINAL_REPORT 中标识的两个 Open Problems 的严格化尝试。诚实列 what worked / what didn't / what remains open。**不做哲学判读**。

---

## OP1 — Axiom 6 (matching = self-training) 的严格数学形式

### OP1.0 目标

寻找 Axiom 6 "匹配即自我训练" 的严格数学对应。候选方向：M2 iteration 的 Banach contraction property 或其他 fixed-point / self-similarity 结构。

### OP1.1 M2 iteration 回顾

From `exp015/rust_solver/src/engine.rs::update_source_m2_complex`：

```
S_k ← normalize_∞(S_k · conj(ψ_k))
```

逐点复数乘法后归一到 ∞-norm。展开：
```
S · conj(ψ) |_k = (sa_k + i·sb_k) · (a_k − i·b_k)
              = (sa_k·a_k + sb_k·b_k) + i·(sb_k·a_k − sa_k·b_k)
```

### OP1.2 尝试：M2 是否是 Banach contraction？

**Setup**: 给定固定 `ψ ∈ ℂ^N`，定义 map

```
T_ψ : ℂ^N → ℂ^N,  T_ψ(S) = (S ⊙ conj(ψ)) / ‖S ⊙ conj(ψ)‖_∞
```

其中 `⊙` 是 Hadamard 积。

**Claim 1 — 不是 ℂ^N 上的 Banach contraction**：
原因：normalize 算子在 `S → 0` 处奇异；任意 S 都被 map 到单位球面 `‖T_ψ(S)‖_∞ = 1`，所以 `‖T_ψ(S) − T_ψ(S')‖` 与 `‖S − S'‖` 没有线性压缩关系。

**Claim 2 — 可以研究 T_ψ 在 projective space ℂP^{N−1} 上的动力学**：

把 `T_ψ` 视为作用在 unit ∞-sphere (或 equivalently `ℂP^{N−1}`) 上的迭代。由于 `S → S ⊙ conj(ψ)` 是 **对角线性算子**（本征值 `{conj(ψ_k)}_{k=1}^N`），standard Perron-Frobenius-like analysis 适用：

**Proposition (Convergence of M2 on ℂP)**:
设 `ψ ∈ ℂ^N` 满足 `|ψ_{k*}| > |ψ_k|` for all k ≠ k*（严格最大），则对任意 initial `S^{(0)}` with `S^{(0)}_{k*} ≠ 0`：

```
T_ψ^n (S^{(0)}) ----→ e_{k*}  as  n → ∞
```

其中 `e_{k*}` 是第 k* 个标准基向量（one-hot）。收敛速率：
```
‖T_ψ^n(S^{(0)}) − e_{k*}‖ ≤ C · (|ψ_k2| / |ψ_{k*}|)^{2n}
```
其中 `k2` 是次大 |ψ_k| 的 index。

**Proof sketch**：
`(S^{(0)} ⊙ conj(ψ)^n)_k = S^{(0)}_k · conj(ψ_k)^n`。Max coordinate is 在 k* 处（由于 `|ψ_{k*}|^n` 指数 dominant）。Normalization 让这个 coordinate → 1，其他 coordinates → 0 exponentially。QED.

### OP1.3 结论：M2 **可收敛，但收敛到退化 one-hot 态**

这是**严格的数学结论**，但也是**物理上无意义的形式**：
- 如果 Axiom 6 的数学对应真是 M2 iteration，那"匹配即自我训练"的稳态是 "source 集中到单一 voxel"——所有空间结构被消除。
- 这**不符合** Axiom 6 哲学直觉（"匹配应该 refine source 而非 degrade 它"）。

**诚实的 OP1 verdict**：

> M2 iteration 在 projective space 上是 contraction（收敛到 dominant eigenvector），但 fixed point 退化。**因此 M2 不是 Axiom 6 的满意严格形式**。Axiom 6 需要别的数学框架。

### OP1.4 候选替代框架（尝试但未成功）

**Attempt A: Gradient descent on matching loss**
```
S_{n+1} = S_n − α · ∇_S L(ψ_evolved(S_n), qrels_positive)
```
- 问题：需要 supervised signal `qrels_positive`，违反 Axiom 4（语料是实践记录，不监督）
- **Rejected on axiomatic grounds**

**Attempt B: Co-evolution (teacher-student pair)**
```
(S^{(t)}, S^{(s)}) 并行演化，S^{(s)} ← update toward S^{(t)} 若 t 胜出
```
- 需要定义 "胜出" 标准 — 这又回到 Attempt A 的监督问题
- **Rejected**

**Attempt C: 双场耦合不动点**
```
(S, ψ) 满足联立方程 S = G(ψ), ψ = F(S) + D∇²ψ − (|ψ|²−1)ψ
```
- 形式上是不动点方程，但 `G` 的具体形式未定
- 候选：`G(ψ) = proj_Λ(ψ)` 其中 Λ 是某种 "compressed representation space"
- **需要额外结构（Λ 的选择），留作未来工作**

**Attempt D: Information-theoretic formulation**
```
S_{n+1} = argmin_S { ‖S − S_n‖² : H[ψ_evolved(S)] ≥ H_min }
```
- 通过最大熵约束避免 one-hot degeneracy
- 数学上干净，但实现需要 variational machinery
- **Viable but heavy, not for position paper**

### OP1.5 arXiv v1 的建议措辞

```
"Axiom 6 (matching-as-self-training) currently lacks a rigorous 
mathematical formalization. We considered M2 source-field 
iteration (exp007) as a candidate; analysis (Appendix X) shows M2 
converges on projective space ℂP^{N−1} to a one-hot limit state, 
which fails to capture the refinement intent of Axiom 6. Gradient-
based and co-evolutionary alternatives were rejected on axiomatic 
or infrastructural grounds. A satisfactory formalization—likely 
requiring a maximum-entropy-constrained iteration or a 
two-field fixed-point system on a structured representation 
space—remains open."
```

---

## OP2 — Δ_OP2 的 topos / Kan extension 扩展

### OP2.0 目标

Lawvere 草稿 §2.3.3 给出的 `Δ_OP2 := |T-Alg_T| ⊖ |T-Alg_T^{(η, p_0)}|` 是 **discrete category 下的 cardinality complement**。em 在 2026-04-13 review 中承诺"topos 设定下的泛化" 作为 future work。本节尝试具体化这个泛化。

### OP2.1 Setup：topos-enriched version

假设 category `C` 升级为一个 **elementary topos** `𝓔`（例如 `Set`、`Sh(X)`、`[C^op, Set]`）。`F ⊣ G` 升级为 topos-morphism adjunction。

- `T := G∘F : 𝓔 → 𝓔` 仍是 monad
- `𝓔^T` = Eilenberg-Moore category of T-algebras
- `p_0` 从 `supp(p_0)` 的离散集升级为 `𝓔` 中的 object（比如 "initial condition subobject"）

在 topos 中，subobjects 形成 Heyting algebra `Sub(X)`。因此：

### OP2.2 尝试：Δ_OP2 作为 Heyting-algebraic complement

**Definition**:
```
Δ_OP2^topos := Sub(T-Alg_T)  /  Sub(T-Alg_T^{(η, p_0)})
```

**问题**：在 Heyting algebra 中，`¬a` 一般不满足 `a ∨ ¬a = 1`（没有 double negation）。所以 `Sub(T-Alg_T^{(η, p_0)})` 的补不是唯一确定的。

**Tentative fix**: 用 closed/open subobject 区分。若 `T-Alg_T^{(η, p_0)}` 是 closed subobject (一个 closure point of the monad action)，其 open complement 有定义，Δ_OP2 作为 open subobject measure 可以 quantify。

**Verdict**: 需要 **specify whether `T-Alg_T^{(η, p_0)}` is closed**。这个没有先验答案；依 topos 的选择而定。**留作 open**。

### OP2.3 尝试：Δ_OP2 作为 Kan extension obstruction

**Setup**: inclusion `ι : T-Alg_T^{(η, p_0)} ↪ T-Alg_T`

**Left Kan extension** `Lan_ι (Id)` 存在 iff 对 every object in `T-Alg_T`，"canonical shape" 从 `T-Alg_T^{(η, p_0)}` 可以形式地 extend 到它。

如果 `Lan_ι (Id) ≃ Id_{T-Alg_T}` (via counit of Kan adjunction)，则 inclusion 是 "essentially surjective"，Δ_OP2 为零。

否则，Δ_OP2 非零，且可以量化为：
```
Δ_OP2^Kan := "obstruction class"  ∈  Ext^1(Q, Id)
```
其中 `Q = cokernel` of `Lan_ι(Id) → Id_{T-Alg_T}` in a chain-complex enrichment.

**问题**: `Ext^1` 需要 abelian enrichment。`Cat` 本身不是 abelian。只有在特定 enrichment (如 `Ab-Cat` 或 `Chain-Cat`) 下，Ext 有定义。

**Verdict**: 这个方向需要选择一个 **specific enrichment**（stable ∞-category / dg-category / simplicial category），每种选择给不同的 Δ_OP2^Kan。非唯一，但 **qualitatively 仍对应 "reachable vs existent"**。

### OP2.4 尝试：persistent homology quantification

最具体、物理上最可测的方向：

**Setup**: 固定 initial distribution `p_0`，在 phase space 里 run many trajectories 的 gradient flow（可与 Langevin noise 组合），collect fixed-point sample set `X_realized ⊂ ℝ^{2N}` (a, b 场的 fixed points)。

独立地，在 `V(ψ)` 的所有 critical points 解析/数值计算 `X_theory ⊂ ℝ^{2N}` (理论 attractor set)。

**Δ_OP2^PH**: persistent homology 的 **Betti 数差**：
```
Δ_OP2^PH := PH_*(X_theory) − PH_*(X_realized)
```

具体每个 Betti:
- `ΔB_0` = realized 中 "丢失" 的连通分量数
- `ΔB_1` = realized 中 "丢失" 的 1-cycles
- ...

**优点**：
- 完全经验可算（giotto-tda 支持）
- 直接链接 Block V 的 evaluation metric upgrade（§5 of BLOCK_V_DESIGN.md）
- Physical meaning 清晰

**Verdict**: **PH-based quantification 是最务实的 Δ_OP2 formal measure**。推荐作为 arXiv v1 的 "concrete quantification" 候选。

### OP2.5 arXiv v1 的建议措辞

```
"Δ_OP2 as defined in §2.3 is a symbolic placeholder (cardinality 
complement) in the discrete-category setting. Several enriched 
formulations are possible:
  - Heyting-algebraic complement in a topos enrichment 
    (requires closure of T-Alg_T^{(η,p_0)})
  - Kan extension obstruction in an abelian/∞-category 
    enrichment (choice-dependent)
  - Persistent-homology Betti difference 
    (empirically measurable, recommended for Block V evaluation)

The qualitative content—dialectical structures that exist in 
T-Alg_T but are unreachable under the dynamics defined by η 
and p_0—is stable across formalizations. Full mathematical 
rigor for Δ_OP2 is future work."
```

---

## 总结（Open Problems 当前状态）

| 问题 | 状态 | 贡献 |
|---|---|---|
| **OP1** (Axiom 6 严格化) | **证伪 M2 为满意形式**；其他 candidates 或违反 axioms 或需要额外基础设施 | Paper 需诚实标注；留 Attempt C/D 作 future 方向 |
| **OP2 topos** | 半工作；Heyting complement 需要 closed subobject 假设 | 标为 "conditional formalization" |
| **OP2 Kan** | 需要 enrichment 选择；每种给不同 Δ_OP2^Kan | 标为 "choice-dependent" |
| **OP2 PH** | **推荐具体方向**；经验可算，Block V 可直接实验 | **首选 concrete quantification**，纳入 Block V evaluation metrics |

### 对 exp017 FINAL_REPORT 的回补

建议 FINAL_REPORT §4.5 (Open Problems) 增加一条：
- "A persistent-homology-based quantification of Δ_OP2 is proposed as the most empirically grounded formalization (see open_problems_followup.md and BLOCK_V_DESIGN.md §5)."

---

## 附录：M2 projective convergence 的详细推导

### A.1 Setup
- `ψ ∈ ℂ^N`, `S^{(0)} ∈ ℂ^N`, `S^{(0)} ≠ 0`
- Map: `T_ψ(S)_k := S_k · conj(ψ_k) / max_j |S_j · conj(ψ_j)|`

### A.2 Without normalization
```
(T̃_ψ^n(S^{(0)}))_k = S^{(0)}_k · conj(ψ_k)^n
```
Magnitude: `|S^{(0)}_k| · |ψ_k|^n`。

### A.3 With normalization
Assume `k* = argmax |ψ_k|` unique. Then:
```
(T_ψ^n(S^{(0)}))_{k*} = S^{(0)}_{k*} · conj(ψ_{k*})^n / (|S^{(0)}_{k*}| · |ψ_{k*}|^n) · (1/c_n)
                    = (S^{(0)}_{k*}/|S^{(0)}_{k*}|) · (conj(ψ_{k*})/|ψ_{k*}|)^n · (1/c_n)
```
其中 `c_n` 是 normalization 因子。由 max condition，`c_n → 1`。

对 k ≠ k*：
```
|(T_ψ^n(S^{(0)}))_k| = |S^{(0)}_k| · |ψ_k|^n / (|S^{(0)}_{k*}| · |ψ_{k*}|^n)
                   = C · (|ψ_k|/|ψ_{k*}|)^n → 0
```

### A.4 Rate
Second-order convergence in `(|ψ_k2|/|ψ_{k*}|)^n` for the second-largest coordinate。

### A.5 Phase rotation artifact
注意 `(conj(ψ_{k*})/|ψ_{k*}|)^n` 在 `n → ∞` 时 **不收敛**——它是单位圆上的旋转。但由于 `ℂP` 把 phase 等价掉，这在 projective 意义下仍收敛到 `[e_{k*}] ∈ ℂP^{N−1}`。

这是一个 **subtle point**：M2 在 ℂ^N 上不收敛（相位旋转），只在 ℂP^{N−1} 上收敛。

这个 subtlety 在 exp015 实现里被 normalize 隐藏了（normalize 把每步 output 投到单位球面，相当于取 ℂP 代表）。

---

*End of follow-up. Status: OP1 rigorously analyzed and M2 falsified as its formalization; OP2 given three candidate quantifications with PH recommended as most concrete. Both ready for arXiv v1 Open Problems section.*
