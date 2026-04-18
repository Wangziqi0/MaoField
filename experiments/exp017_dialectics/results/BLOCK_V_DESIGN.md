---
name: Block V 实验设计书
date: 2026-04-13
author: Linux Claude（初稿，待 em × Win review）
status: design only — NO experiments launched until em explicit authorization
based_on: exp017 FINAL_REPORT Sections 3 + 5 (Stage C 两路径分裂 / Stage A1 reachability failure)
---

# Block V 实验设计书

## 0. 前言与守则

本文档仅为设计。**不启动任何实验，除非 em 明确授权**。所有数学推导尽可能严格，所有哲学对应标 **[?]** 交 em × Win 判读。

所有 `[?]` 标记表示本文件作者（Linux Claude）无权决定、需人类判读的点。

---

## 1. 问题陈述

### 1.1 exp017 留下的三个未解问题

基于 Stage C 和 Stage A1 的诊断结论，Block V 必须回答：

**Q1（对称群问题）**：What symmetry group should V(ψ) break to achieve k\*≥3 and support compositional semantic structure?

- 背景：exp017 确认 double-well GL 下 k\*=2 via 两种 Z_n 机制（byte Z_1 phase collapse / BGE Z_2 amplitude bistability）
- 核心：不是 "加多少个井"，是 "选什么对称群"（em × Win 2026-04-13 design principle）

**Q2（动力学问题）**：Is gradient flow alone enough to reach new basins, or does OP2 require non-equilibrium extension?

- 背景：Stage A1 证实即使 V(ψ) 数学定义了 u=4 井，pure gradient flow 下 u=4 井 occupancy = 0.00%（gradient flow 单调下降 F[ψ]；init u∈[0.49,1.69] ⊂ basin-of-attraction(u=1)，任何 trajectory 被 confined）
- 核心：动力学类型本身是独立于势函数的第二轴

**Q3（联合/解耦问题）**：Do Q1 and Q2 need to be addressed jointly, or can they be decoupled?

- 如果解耦 → 两个独立实验线
- 如果联合 → 需要 symmetric group × dynamics type 的乘积实验设计
- 预判 [?]：A1 已暗示**联合**（即使选对对称群，gradient flow 仍不可达 disjoint basins）。但需要 Block V 的对照实验证实

### 1.2 Block V 不做什么

- **不做 SCAN benchmark 接入**：等对称群 + 动力学设计成熟后再选下游
- **不做 full 5-dataset sweep**：Block V 是 mechanism study，用 1-2 数据集 + 100 docs 诊断即可
- **不做 Kuramoto / diffusive 耦合变体**：Block II 已弱证伪，不回溯

---

## 2. 对称群候选分析

### 2.1 候选矩阵总览

| 对称群 | V(ψ) 候选形式 | 稳态结构 | 预期 k\* | 数学复杂度 | Block V 编号 |
|---|---|---|---|---|---|
| **Z_2 (baseline)** | `¼(|ψ|²−1)²` | `{0} ∪ S^1_{|ψ|=1}` (AC 破缺后 ≈ 2 点) | 2 | 低 | (对照组) |
| **Z_n radial** | `∏_k (|ψ|²−a_k)²` (A1 形式) | n 个同心圆 | n (理论) / 1-2 (实测，见 A1) | 中 | V.1-R |
| **Z_n angular** | Mexican hat + `Re(C·ψ^n)` | n 个离散点 on `|ψ|=1` | n | 中 | V.1-A |
| **U(1) 保持** | Mexican hat only | `{0} ∪ S^1_{|ψ|=1}` (连续流形) | 1 + manifold | 低 | V.2 |
| **SU(2) / 2-component** | `−|Ψ|² + |Ψ|⁴`, Ψ ∈ ℂ² | `S^3` (3-sphere) | 1 + 3-manifold | 高 | V.5 |

### 2.2 Z_n radial (V.1-R)

**势函数形式**：
```
V(u) = ∏_{k=0}^{n-1} (u − a_k)^{m_k},   u = |ψ|²,   a_k 升序
```

A1 是 `n=3, a=(0,1,4), m=(1,2,2)`。

**Euler-Lagrange**：
```
∂ψ/∂t = D∇²ψ − F(u)·ψ + S
F(u) = dV/du
```

**稳态**：u ∈ {a_0, a_1, ..., a_{n-1}} 为 minima。

**Predicted attractor manifold**：每个 minima 对应一个 U(1) 对称的圆轨 `|ψ|² = a_k`，合计 n 个同心圆。但 AC discretization 会破 U(1) → 每圆坍缩为孤立点（参照 Stage C IV-B）。

**Stage A1 实测**：`n=3, a=(0,1,4)` 下 gradient flow 只激发 1 个井。其他 n 值在 gradient flow 下预期同样受 barrier 约束。**Z_n radial 单独不足**。

### 2.3 Z_n angular (V.1-A)

**势函数形式**（this is the key alternative we haven't tried）：
```
V(ψ) = −A·|ψ|² + B·|ψ|⁴ + C·Re(ψ^n)
     = −A·|ψ|² + B·|ψ|⁴ + C·|ψ|^n·cos(n·θ)
```
其中 `θ = arg(ψ)`。

**Euler-Lagrange**：
```
δV/δψ* = −A·ψ + 2B·|ψ|²·ψ + n·C·(ψ*)^{n-1}
∂ψ/∂t = D∇²ψ − (−A·ψ + 2B·|ψ|²·ψ + n·C·(ψ*)^{n-1}) + S
      = D∇²ψ + A·ψ − 2B·|ψ|²·ψ − n·C·(ψ*)^{n-1} + S
```

**稳态**：
- `|ψ|` 由 `−A + 2B|ψ|²` 决定（radial），给出 `|ψ|² = A/(2B)`
- `θ` 由 `cos(nθ)` 的 minima 决定，即 `θ_k = (2k+1)π/n` （若 C>0）或 `θ_k = 2kπ/n` （若 C<0）
- 合计 **n 个离散 minima** 在同一 radial manifold 上

**Predicted basins**：n 个 discrete points（不是流形），受 C 强度调制。
- C → 0：退化为 U(1)（连续流形）
- C 适中：n 个清晰离散 basin
- C → ∞：单一 basin（C 项完全主导）

**优势 vs Z_n radial**：
- Basin 是 **离散点**（而非同心圆），k-means 能 cleanly 分出
- 对 gradient flow 更友好（所有 minima 在同一 `|ψ|` shell 上，barrier 只在 angular 方向）
- 势垒高度由 C 参数控制，可精细调节

**劣势**：
- C·Re(ψ^n) 显式破坏 U(1)，PDE 形式含 `(ψ*)^{n-1}` 非局部项
- n≥3 时实现复杂度上升（n=3 就有 ψ̄² 项）

**[?]**：em × Win 判读 —— angular 形式（离散 phase 点）在哲学上是否对应 "n 种不同的矛盾形态"？还是 radial 形式（n 个同心圆）更像 "矛盾的层次结构"？

### 2.4 U(1) 保持 (V.2)

**势函数**：Mexican hat `V = −½|ψ|² + ¼|ψ|⁴`（等价于 `¼(|ψ|²−1)²` up to const）。

**关键：不加 U(1) 破缺项**。需要消除 AC discretization 的 U(1) 破坏：
- 用 **continuous Fourier basis**（而非 32³ cubic grid），或
- 加一个 Lagrange multiplier 强制 `|ψ|²` 守恒

**稳态**：`|ψ| = 1` 的整个 `S^1`（circle of vacua）。

**Goldstone 模**：phase θ 成为 massless mode。

**Predicted attractor**：连续 1-manifold。

**k-means 会失败**（流形不是点云）；需要 persistent homology 或 diffusion maps 做 evaluation（见 §5）。

**[?]**：em × Win 判读 —— 连续流形 attractor 对应 "矛盾的连续谱"，比离散 n-basin 是不是更 "辩证"（因为它本身就是对立统一的连续变形）？

### 2.5 SU(2) 非 Abelian (V.5)

**场**：`Ψ = (ψ_1, ψ_2) ∈ ℂ²`

**势函数**：
```
V(Ψ) = −A·|Ψ|² + B·|Ψ|⁴,   |Ψ|² = |ψ_1|² + |ψ_2|²
```

**SU(2) 不变性**：对任意 U ∈ SU(2)，`Ψ → UΨ` 保 V 不变。

**稳态 manifold**：`|Ψ|² = A/(2B)`，即 `ℂ² \ {0}` 中的一个 `S^3`（3-sphere）。

**Hopf fibration**：`S^3 → S^2`（纤维 = `U(1)`），即每个 S^2 上的点对应 S^1 的 phase 自由度。

**Predicted attractor**：带纤维结构的 3-manifold。

**数学复杂度**：
- Euler-Lagrange 是 2-component，耦合
- Discrete AC 会破 SU(2) → 需要 special discretization 保对称
- Evaluation 需要 manifold-with-fiber 的拓扑工具

**[?]**：em × Win 判读 —— Hopf fibration 的 "bundle 上一个纤维" 结构是否是 "主要矛盾 + 次要矛盾" 的自然数学形式？（如果是，SU(2) 可能是整个 Block V 的 crown jewel 目标）

### 2.6 对称群候选的优先级建议（Linux 视角）

**[?] 以下为数学可行性排序，不是哲学优先级**：

1. **V.1-A (Z_n angular)** — **第一优先**：数学干净 + 预期离散 basin + gradient-flow 可能直接 work（同 radial shell 内无大 barrier）
2. **V.2 (U(1) 保持)** — 第二优先：连续流形是干净的"扬弃"候选，但需要 manifold evaluation
3. **V.1-R (Z_n radial)** — 第三优先：A1 已示 gradient flow 不够，单独做意义有限，但可以作为 V.1-A 的对照
4. **V.5 (SU(2))** — 最后：数学复杂度最高，风险/回报比最高但时间成本也最高

---

## 3. Non-equilibrium 扩展候选 (Q2)

### 3.1 候选矩阵

| 扩展 | 方程形式 | 物理对应 | 数学稳定性 | 辩证法对应 | 编号 |
|---|---|---|---|---|---|
| **Langevin** | `∂ψ/∂t = −δE/δψ* + η(t,x)` | 热浴 | 高（FP 方程有解） | [?] 偶然性/历史具体性 | V.3-L |
| **Hamiltonian** | `∂ψ/∂t = −i·δH/δψ*` | 保能量振荡 | 高（守恒系统） | [?] 保结构转化 | V.3-H |
| **Active driving** | `∂ψ/∂t = −δE/δψ* + f(ψ,t)` | 非平衡稳态 | 中（依赖 f） | [?] 实践持续介入 | V.3-A |
| **Metropolis overlay** | `PDE + MC accept/reject` | 全局最优搜索 | 中（需离散化） | [?] 质变的随机触发 | V.3-M |

### 3.2 Langevin (V.3-L)

**完整方程**：
```
∂ψ/∂t = D∇²ψ − δV/δψ* + S + η(t,x)
<η(t,x) η*(t',x')> = 2·σ²·δ(t−t')·δ(x−x')
```
σ = noise intensity (相当于 `√(k_B T)`)

**Fokker-Planck 对应**：
```
∂P[ψ]/∂t = ∇·(P·∇(δE/δψ*)) + σ²·∇²P
```
稳态分布 `P_ss(ψ) ∝ exp(−E[ψ]/σ²)`。

**关键性质**：可以以非零概率翻越势垒。对 A1 势函数，u=4 basin 被占据的概率为
```
P(u=4) / P(u=1) ∝ exp(−(V(u=2.7) − V(u=1)) / σ²) = exp(−13.2/σ²)
```
所以 σ² ≳ 13.2 时 u=4 basin 会显著被占据。但过大 σ 会让系统完全 decohered。

**实验提议**：σ ∈ {0.1, 0.5, 1.0, 2.0, 4.0} 扫描，对 A1 势函数固定，看 |ψ|=2 basin 占据率 vs σ。

**辩证对应 [?]**：Langevin noise = "历史具体性 / 偶然性" 的物理对应。凝结成辩证法 = "必然在偶然中实现"。em × Win 定。

### 3.3 Hamiltonian (V.3-H)

**完整方程**（复场一阶形式）：
```
i·∂ψ/∂t = −D∇²ψ + δV/δψ*  (Schrödinger-like)
```
或二阶形式（wave equation）：
```
∂²ψ/∂t² = D∇²ψ − δV/δψ*
```

**关键性质**：能量守恒。从初始高能态（kinetic energy 足够）可以 oscillate 穿过势垒。

**稳态结构**：没有唯一稳态——系统在恒能 manifold 上振荡。真正 "访问" 的 basin 由初始能量决定。

**评估**：不是 fixed-point，而是 **time-averaged distribution** 或 **Poincaré section**。需要改 metric。

**辩证对应 [?]**：Hamiltonian = "保结构转化" 的物理对应。凝结成辩证法 = "矛盾的同一性（两面不断转化但整体不变）"。

**风险**：数值 damping 会让 Hamiltonian 退化为 gradient。需要 symplectic integrator。实现成本中。

### 3.4 Active driving (V.3-A)

**完整方程**：
```
∂ψ/∂t = D∇²ψ − δV/δψ* + S + f(ψ, t)
```

`f` 的形式多样：
- **Periodic**：`f = A·cos(ωt)·e^{iφ}`
- **State-dependent**：`f = γ·(ψ_target − ψ)`（向 target 驱动）
- **Stochastic + deterministic 混合**：`f = f_det + η`

**物理例子**：主动物质（活细胞、生物膜）。

**辩证对应 [?]**：Active driving = "实践的持续介入"。最直接对应 "实践决定认识" 的辩证唯物主义立场。

**实现风险**：`f` 的选择有无穷多种。需要先从**最简**开始（periodic constant）。

### 3.5 Metropolis overlay (V.3-M)

在 PDE evolve 每 k 步后，对场做一次 Metropolis 接受/拒绝判断：
- 提议更新 ψ → ψ + δψ
- 计算 ΔE
- 接受概率 `min(1, exp(−ΔE/T))`

**关键**：允许 uphill moves，全局最优搜索。

**辩证对应 [?]**：Metropolis = "质变的随机触发"，对应 "量变到质变的偶然跃迁"。

**实现**：简单，可叠加到 gradient flow 上。

### 3.6 Non-equilibrium 候选优先级建议（Linux 视角）

**[?] 数学可行性排序**：

1. **V.3-L (Langevin)** — **第一优先**：数学最完整（Fokker-Planck），实验最简单（加 random noise），直接回答 "gradient flow 是否够"
2. **V.3-H (Hamiltonian)** — 第二优先：如果 Langevin 能 work，Hamiltonian 可以给 "无损翻越" 的对照
3. **V.3-M (Metropolis)** — 第三优先：实现简单，但物理意义与 Langevin 重叠
4. **V.3-A (Active)** — 最后：无穷多选择，需要先定 f 形式

---

## 4. 实验矩阵 Proposal

### 4.1 Sub-block 结构

| Sub-block | 变量 | 目的 | 估时 |
|---|---|---|---|
| **V.0** | 复现 A1 + baseline | sanity check（0 变化） | 0.5 h |
| **V.1-A** | Z_n angular, n ∈ {3,4,5,6} | Q1 主实验：离散 basin 能否达到 k\*=n | 3 h |
| **V.1-R** | Z_n radial (A1 系列 + A1.2/A1.3) | Q1 对照：radial 是否不如 angular | 2 h |
| **V.2** | U(1) 保持 + manifold eval | Q1 第二候选：连续流形 | 3 h |
| **V.3-L** | Langevin σ ∈ {0, 0.1, 0.5, 1.0, 2.0, 4.0} on A1 | Q2 主实验：noise 能否达 u=4 basin | 2 h |
| **V.3-L × V.1-A** | Langevin on Z_n angular | Q3 联合：symmetry × dynamics 交互 | 4 h |
| **V.3-H** | Hamiltonian on A1 | Q2 对照 | 3 h |
| **V.5** | SU(2) 2-component | 远期 stretch goal | 8+ h |

**总预算**：~20-25 小时（含 buffer）。分 3-4 个工作日。

### 4.2 每 sub-block 的评估标准

**Q1 候选评估（V.0, V.1-A, V.1-R, V.2）**：
- k\* via k-means silhouette（k=2..10）
- amplitude distribution histogram
- phase distribution（global + per-doc |R|）
- **persistent homology**（for V.2 连续流形）
- 可选：nDCG@10 on NFCorpus top-20（reranker 性能）

**Q2 候选评估（V.3-L, V.3-H）**：
- basin occupancy vs 驱动强度（σ for Langevin, 初始能量 for Hamiltonian）
- **关键指标**：|ψ|=2 basin occupancy 从 0% 提升到了多少？
- 相图：noise vs barrier height

**Q3 联合评估（V.3-L × V.1-A）**：
- k\* 曲线：n × σ
- 最优 (n, σ) 组合

### 4.3 数据集和规模

- 主数据集：**NFCorpus 100 docs**（和 Stage C / A1 一致，保持可比）
- 次数据集：**SciFact 100 docs**（如需验证 generalization）
- 候选池：top-20（和 Block IV / IV.5 一致）
- 源场：**BGE-M3 embedding tile to 32³**（A1 conventions）

### 4.4 编号与交付

```
results/block_v/
├── v0_sanity/                   # V.0 对照
├── v1a_zn_angular/              # V.1-A
├── v1r_zn_radial/               # V.1-R（含 A1.2/A1.3/A1.4）
├── v2_u1_preserved/             # V.2
├── v3l_langevin/                # V.3-L
├── v3h_hamiltonian/             # V.3-H
├── v3l_x_v1a/                   # 联合 sub-block
├── v5_su2/                      # 远期（optional）
└── BLOCK_V_FINAL_REPORT.md      # 汇总
```

---

## 4.5 Phase A — Three-axis OP2 co-design (post-A1.4 refinement, added 2026-04-14, revised after review)

**Background**: A1.4 σ-scan + walled experiments (`block4_5/a1_4/VERDICT.md`) refined OP2 from a single-axis barrier-engineering problem to a **three-axis co-design**:
- **Axis A** — Source statistics (`⟨Sb⟩ ≠ 0` breaks detailed balance; BGE raw embeddings violate by 17σ)
- **Axis B** — Potential geometry (shifted `V~u⁵` tail too shallow to confine against σ√dt noise)
- **Axis C** — Numerical scheme (explicit Euler + soft wall + dt=0.05 violates CFL by ~380×)

Single-axis fixes do not restore Laplace equilibrium (proven by elimination, `VERDICT.md` §3.4). Block V Phase A tests each axis independently then jointly, preceded by a Phase A-0 feasibility check.

### 4.5.0 Phase A-0: Reachability pre-check (prerequisite, ~1h)

**Objective**: Before any intervention, verify Laplace target is reachable within simulation horizon.

**Computations**:
1. Kramers barrier crossing times on shifted potential (`ΔV=0.095` outer, `V''(1)=2`, `|V''(saddle)|=1.59`):
   - σ=0.3, `T_eff=0.045`: `k ≈ 0.28·exp(−2.11) ≈ 0.034`, `τ_cross ≈ 29` — well below `t_sim=250` ✓
   - σ=0.5, `T_eff=0.125`: `k ≈ 0.28·exp(−0.76) ≈ 0.133`, `τ_cross ≈ 7.5` (marginal; Kramers invalid at ΔV/T<1)
   - Conclusion: inter-basin mixing timescale is adequate for σ∈{0.3, 0.5} at outer barrier. Inner barrier `ΔV=0.431` gives `τ_cross ≈ 1/0.032 = 31` at σ=0.5, also adequate.
2. Deterministic σ=0 baseline prediction (init + gradient flow, no noise): Monte Carlo the init distribution and propagate deterministically. Expected: voxels in `u_init ∈ [0.49, 1.69]` roll to `u=1` basin (majority) with a small fraction `P(u_init > u_saddle_outer=1.54) ≈ 12%` drifting to `u=2`. Observed σ=0 A1.4 baseline shows 66% `u=2`, of which ~12% is from init + 54pp from source drift (Axis A).
3. Success gate for Phase A: `p(k)_predicted` from Monte Carlo must agree with Laplace `p(k) ∝ Z_k` to within `KL(p_obs ∥ p_Laplace) < 0.05` after source debiasing.

**Deliverable**: `a_0_reachability.json` with `τ_cross` for outer+inner barriers at σ∈{0.3, 0.5} and deterministic Monte Carlo baseline occupancy estimates. If `τ_cross > t_sim` at target σ, extend `t_sim` or broaden init before proceeding.

### 4.5.1 Phase A-1: Source bias mitigation

**Objective**: Eliminate `⟨S⟩ ≠ 0` drift; restore Laplace assumption (i).

**Sub-experiments** (MVP, ~2h total):
- **A-1.a** (mean-subtraction baseline): `S' = S − ⟨S⟩_global`, re-run A1.4 shifted potential σ=0.3 and σ=0. Compare p(1)/p(2) ratio vs Laplace √2 prediction. If recovers → Axis A is necessary and sufficient under this potential+integrator.
- **A-1.b** (per-doc mean-subtraction): `S' = S − ⟨S⟩_doc`, check if residual drift survives (would indicate non-gradient curl component beyond mean).
- **A-1.c** (whitening: `S' = Σ^{-1/2}(S − ⟨S⟩)`): stronger decorrelation. Tests whether other covariance structure of BGE contributes to drift.

**Success criterion** (quantitative): σ=0 deterministic baseline gives occupancy matching Phase A-0 Monte Carlo prediction (init + pure gradient flow) to within `max_k |p_obs(k) − p_A-0(k)| < 0.05`. This is the testable "no residual drift" threshold.

**Key data to produce**:
- `a_1_occupancy.csv`: 3 interventions × σ∈{0, 0.3} = 6 rows × basin occupancy
- `a_1_source_stats.json`: t-stat on `⟨Sb⟩` post-intervention
- Verdict: which intervention level is sufficient

### 4.5.2 Phase A-2: Potential geometry design

**Objective**: Construct `V` that confines `|ψ|²` against `σ√dt = 0.11` noise scale without Axis-C integrator instability.

**Sub-experiments** (MVP, ~3h total):
- **A-2.a** (additive quartic confining tail): `V(u) = V_shifted(u) + α·(u − u_c)⁴·[u > u_c]` with `u_c=2.5`, `α ∈ {0.1, 1, 10}`. **Additive** form is used to keep `u⁴` tail independent of the base `V_shifted`'s `u⁵` decay; multiplicative modification `V·(1+α(u-3)²)` leaves tail polynomial order at `u^7` still shallower than desired. `[u>u_c]` is Heaviside; `(u−u_c)⁴` has `V=V'=V''=V'''=0` at the junction, so `C³`-smooth.
- **A-2.b** (logarithmic + quartic safety): `V(u) = V_shifted(u) + κ·log(1 + (u-u_c)²)·[u > u_c] + λ·(u - u_c_hard)⁴·[u > u_c_hard]`, with `u_c=2.5`, `κ ∈ {1, 5}`, `u_c_hard=3.5`, `λ = 10`. The log term provides gentle confinement in the transit region; the quartic safety net prevents unbounded excursion in long tails (addressing the `f' → 0` issue of pure log confinement).
- **A-2.c** (reflecting BC via Skorokhod projection): *moved to Phase A-3 (see A-3.c)*. Hard BC is a numerical-scheme choice, not a potential shape; treating it as a potential form produces spurious Axis-C failures.

**Success criterion**: `p(clamp) < 1%` at σ=0.5 **under two conditions simultaneously reported**: (i) Axis A fix from A-1 applied, and (ii) Axis A not applied. Reporting both columns allows Axis B's independent contribution to be evaluated even if A-1 is not fully sufficient.

**Key data to produce**:
- `a_2_scan.csv`: 3 potential forms × 3 parameter values × basin occupancy
- `a_2_stability.json`: per-config u_max trajectory time-series (confirm steady-state)

### 4.5.3 Phase A-3: Numerical scheme upgrade

**Objective**: Resolve explicit Euler + soft-wall CFL incompatibility. Produce integrator that handles stiff wall force at `dt=0.05` without blow-up.

**Sub-experiments** (MVP, ~3h total):
- **A-3.a** (reduce dt to `5×10⁻⁵`): brute-force sub-CFL. Cost: 1000× slower per step. Test on 10 docs × σ=0.5 to verify Axis B confining wall stops blow-up.
- **A-3.b** (IMEX Euler with per-voxel diagonal Jacobian): implicit treatment of wall term `f_wall(u)·ψ`, explicit for Laplacian + source + noise. The wall force is **local** (depends only on `|ψ_k|²` at voxel `k`), so `J` is **block-diagonal with 2×2 blocks per voxel**. Linearization for complex `ψ=a+ib`: `F(ψ) = f(|ψ|²)·ψ`, giving per-voxel real 2×2 Jacobian `J_{2×2} = f(u)·I_2 + 2f'(u)·[[a², ab], [ab, b²]]`. Implicit step solved by closed-form 2×2 matrix inverse — `O(N)` cost, same order as explicit. This is the recommended production integrator.
- **A-3.c** (Skorokhod reflecting BC): replace soft wall with hard radial reflection at `|ψ| = R_max` (`R_max=√3.5 ≈ 1.87`, matching A-2.b `u_c_hard`). Since the SDE is **overdamped (first-order, no velocity)**, "reflection" is implemented as radial projection: `if |ψ_{n+1}| > R_max then ψ_{n+1} ← R_max · ψ_{n+1}/|ψ_{n+1}|`. This is the Skorokhod scheme for overdamped SDE on a bounded domain (Bossy-Talay 2005); preserves stationary distribution asymptotically. Tests whether pure projection suffices without any wall potential.

**Success criterion**: at σ=0.5 + potential from A-2 (known to confine under Axis B) + integrator from A-3, `p(clamp) = 0` AND `p(>2.5) < 5%`. This isolates Axis C.

**Key data to produce**:
- `a_3_scan.csv`: 3 integrators × σ ∈ {0.3, 0.5} × occupancy + wall-clock time
- Verdict: cheapest integrator that works; dt scaling of each

### 4.5.4 Phase A-joint: Three-axis simultaneous test

**Objective**: Verify the three axes are sufficient jointly. MVP decisive experiment.

**Framing**: *confirmatory, not optimization*. We pick one configuration based on physics intuition (A-1.a mean-subtraction + A-2.b log+quartic + A-3.b IMEX) and test whether it works. Full (A-1 × A-2 × A-3) grid is 3×3×3 = 27 points; if single confirmatory config fails, proceed to 2-stage 2×2×2 = 8-point grid search (~+3h) picking top-2 from each axis's MVP.

**Configuration** (~2h):
- Axis A: **A-1.a** (global mean-subtraction)
- Axis B: **A-2.b** (log + quartic safety)
- Axis C: **A-3.b** (IMEX Euler, per-voxel diagonal Jacobian)
- σ ∈ {0.3, 0.5}
- 70 docs × 32³ voxels (same as A1.4)

**Laplace prediction** (unchanged): `p(0)=0.028, p(1)=0.569, p(2)=0.402` at σ=0.5.

**Success criterion** (KL-based to avoid the ±5pp narrowness on small p(0)):
`KL(p_obs ∥ p_Laplace) < 0.05` at σ=0.5, computed as `Σ_k p_obs(k)·log(p_obs(k) / p_Laplace(k))`.

**If success**: OP2 path (a) "barrier-topology engineering" validated as workable. Advance to Phase B (OP2 path b, directed non-equilibrium driving via V.3-H / V.3-A).

**If failure**: new axis D suspected. Candidates:
- **D-1**: field-theoretic correction to 1D Kramers prefactor (collective voxel-voxel coupling)
- **D-2**: Laplacian coupling `D∇²` produces non-trivial spatial correlations not captured in single-voxel analysis
- **D-3**: init-distribution sensitivity (addressed by Phase A-0 Monte Carlo prediction; if A-0 predicts failure this is pre-caught)
- **D-4**: `t_sim = 250` insufficient for Kramers timescale; extend to 2500 or 25000 steps

Phase A-4 diagnostic scoped to distinguish D-1/D-2/D-3/D-4 via: (i) single-voxel decoupled simulation to isolate field-theory correction; (ii) longer `t_sim` run with one axis-varied config to isolate horizon issue; (iii) broader init to isolate sensitivity.

### 4.5.5 Phase A time budget

| Sub-phase | Time (MVP) | Time (full) |
|---|---:|---:|
| **A-0 (reachability pre-check)** | **1h** | **1h** |
| A-1 (source bias) | 2h | 4h |
| A-2 (potential, now additive form) | 3h | 6h |
| A-3 (numerical, with IMEX + Skorokhod) | 4h | 8h |
| A-joint (confirmatory) | 2h | 2h |
| A-grid (if joint fails, 2×2×2 search) | — | 3h |
| **Total** | **12h** | **24h** |

Phase A MVP (~12h) fits within 1.5 focused workdays. Full Phase A (~24h) requires 3 days.

### 4.5.6 Phase A → Phase B gate

Phase A resolves (or maps) OP2 path (a). Phase B (V.3-H / V.3-A / V.3-L × V.1-A, directed driving) is **gated on Phase A-joint result**:
- Phase A-joint success → Phase B tests whether directed driving **adds capabilities** beyond Laplace equilibrium (e.g., accessing attractors not connected by gradient flow even with horizon-adequate thermal driving)
- Phase A-joint failure → Phase B must diagnose axis-D before proceeding

---

## 5. Evaluation Metric Upgrade

### 5.1 为什么需要升级

k-means + silhouette 假设 attractor 是**离散点云**。V.2 (U(1)) 和 V.5 (SU(2)) 的 attractor 是**连续流形**，k-means 会 misjudge：
- 在 1-manifold 上做 k-means 会得到 k 个任意划分，silhouette 虚高或虚低
- k\* 数值没有物理意义

### 5.2 候选工具

| 工具 | 输入 | 输出 | 适用场景 |
|---|---|---|---|
| **Persistent homology** (Vietoris-Rips) | 点云距离矩阵 | Betti numbers + persistence diagram | 连续流形拓扑 |
| **UMAP + HDBSCAN** | 点云 | density-based 聚类 | 任意几何 |
| **Diffusion maps** | 点云 + kernel | 流形 embedding | geodesic 结构 |
| **Mapper** (TDA) | 点云 + filter function | 流形 skeleton graph | 流形上下文对比 |

### 5.3 推荐工具链

**对 Q1 candidates**（不同 symmetry group）：
1. 先跑 **UMAP** 可视化（快速直观）
2. 跑 **persistent homology** 算 Betti 数：
   - `β_0` = 连通分量数（离散 basin 的数目）
   - `β_1` = 1-holes（S^1 流形 count）
   - `β_2` = 2-holes（S^2 流形 count）
3. 根据 Betti 数判断 attractor 结构：
   - `β_0 = n, β_1 = 0`：n 个离散点 basin（Z_n angular 预期）
   - `β_0 = 1, β_1 = 1`：一个连续 S^1 流形（U(1) 预期）
   - `β_0 = 1, β_1 = 0, β_2 = 1`：S^2 流形
   - `β_0 = 1, β_1 = 1, β_2 = 1, β_3 = 1`：S^3 流形（SU(2) 预期）

**对 Q2 candidates**（不同 dynamics）：
- 主要看 **basin occupancy vs 驱动强度** 曲线
- 不需要拓扑工具（还是在同一势函数 V 下）

### 5.4 实现

```python
# 推荐库
from giotto.topology import VietorisRipsPersistence
import umap
import hdbscan
from sklearn.preprocessing import StandardScaler
```

`giotto-tda` 是最成熟的 TDA 库，支持 PD + Betti。

---

## 6. 不可知清单 [?]

Block V 设计中，以下决策 Linux 无权下，等 em × Win 判读：

1. **对称群哲学优先级 [?]**：Z_n angular vs U(1) vs SU(2) 在辩证法上各对应什么？"n 个离散点" vs "连续流形" vs "带纤维的 3-sphere" 哪个最 aligns 七公理？

2. **Non-equilibrium 哲学对应 [?]**：
   - Langevin = 偶然性？
   - Hamiltonian = 保结构转化？
   - Active = 实践介入？
   - Metropolis = 质变触发？
   这些是 suggestive，需哲学 Endorsement。

3. **Q3 联合/解耦 [?]**：是否采用"先独立调 Q1 + Q2 再联合"策略，还是一开始就做 Q1 × Q2 网格？成本不同。

4. **V.5 (SU(2)) 是否纳入 Block V 范围 [?]**：数学复杂度高，实现时间 2-3 天。如果 V.1-A / V.3-L 已足够给 paper，V.5 可以推到 Block VI（但 paper 丢一个 Hopf fiber 的故事）。

5. **Evaluation metric 选择 [?]**：persistent homology 需要引入新依赖（giotto-tda, ~100MB）。是否接受？

6. **下游任务选择 [?]**：Block V 跑完后，是选 SCAN / COGS / HINT 做 compositional generalization，还是 continual learning benchmark？这是 exp019 的事，但 Block V 的设计会影响下游选择（Z_n angular 偏 compositional，U(1) 偏 continuity）。

7. **Σ_OP2 的 canonical 量化 [?]**：Lawvere 草稿留了 persistent homology dimension 作 future quantification。Block V 是否顺便做这个？

---

## 7. 总结（Block V 设计的一页概括）

**Block V 的目标**：回答 Q1（对称群）、Q2（动力学）、Q3（联合/解耦）三个核心问题。

**Block V 的最小可行方案（MVP）**：
- V.0 sanity check（0.5h）
- V.1-A Z_n angular, n=3,4（2h）
- V.3-L Langevin σ scan on A1（2h）

**总 ~4.5 小时，回答 Q1 + Q2 的第一版数据**。

**Block V 的完整方案**：所有 sub-blocks，~20-25 小时。

**em × Win 决策点**：
- 是 MVP 还是 完整？
- 哲学对应 [?] 清单的判读？
- V.5 SU(2) 纳入还是推迟？

---

## 8. Appendix：A1 barrier 的数值校正

基于 §2.2 和 FINAL_REPORT §3.2：

V_A1(u) = u·(u−1)²·(u−4)²，minima at u∈{0,1,4}

- Inner barrier: `dV/du=0` 在 u=(15+√145)/10 ≈ **2.704**
- Barrier height at u=2.704: `V(2.704) ≈ **13.18**`
- Midpoint estimate: `V(u=2) = 2·1·4 = 8`

A1 gradient-flow 下 `u_init ∈ [0.49, 1.69] ⊂ basin-of-attraction(u=1)`（inner saddle u_s=0.296 在 init range 左侧；outer saddle u_s=2.704 在右侧）。Gradient flow 是 L² monotone descent of F[ψ]，无法跨 saddle，u=4 basin 不可达。

两个物理量分开报（不可混用同一 "44" 数字）：
- **静态比**（gradient flow 可达性）：V_saddle/V_init_max = 13.187/4.29 ≈ **3.07×**（V(1.69)=4.29 是 init range 上 V 上界）
- **动力学 log-gap**（Langevin Kramers @ σ=0.5, T_eff=σ²/2=0.125）：log10(exp(ΔV/T_eff)/horizon) = 45.82 − 2.40 = **~43 orders of magnitude**

**对 V.3-L Langevin 需要的 σ 估计**：
`P(escape) ∝ exp(−13.18/σ²)`
- σ²=1 → P ∝ exp(−13.18) ≈ 2e-6 （很低）
- σ²=4 → P ∝ exp(−3.30) ≈ 0.037
- σ²=10 → P ∝ exp(−1.32) ≈ 0.27
- σ²=20 → P ∝ exp(−0.66) ≈ 0.52

所以 σ ∈ {1, 2, 3, 4, 5}（σ² ∈ {1, 4, 9, 16, 25}）是合理扫描范围。

---

*Draft v1 — 2026-04-13. Status: design only. NO experiments launched. Waiting em × Win review on [?] decision points.*
