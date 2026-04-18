# Z_n Angular Potential — Detailed Mathematical Analysis

**Linux Claude, 2026-04-13 evening. Drop-in math ammunition for Block V sub-block V.1-A.**
**Figure**: `block4_5/zn_angular_slices.png`

## 问题

Block V 设计文档将 **Z_n angular 势**（Mexican hat + explicit symmetry-breaking term）列为第一优先对称群候选。本文给出其完整数学形式：临界点、鞍点、势垒高度、Hessian 曲率、两极限行为，以及对 `k*=n` attractor 数量的理论预测。这些结果可以在 Block V 启动时直接填入 FINAL_REPORT.md 或 arXiv v1 appendix，无需额外推导。

## 势函数形式

```
V(ψ) = (|ψ|² − v²)² + ε · Re(C · ψⁿ)
```

- `ψ ∈ ℂ`，复数标量场
- `v > 0`：Mexican hat 底部半径
- `n ∈ ℤ₊, n ≥ 2`：破缺群阶数（对应 Z_n）
- `C = |C|·e^{iφ_C} ∈ ℂ`：symmetry-breaking 幅值 + 相位，`|C|>0`
- `ε > 0`：破缺强度（通常 ε·|C|·vⁿ ≪ v⁴，小破缺近似）

对应「整体 U(1) 被显式破缺到 Z_n 循环群」的 Landau 展开：Mexican hat 的 U(1) flat direction 被 cos(nθ) 摺皱成 n 个谷。

### 极坐标展开

令 `ψ = r·e^{iθ}`，`r ≥ 0`, `θ ∈ [0, 2π)`：

```
V(r, θ) = (r² − v²)²  +  ε · |C| · rⁿ · cos(n·θ + φ_C)
         └── radial (U(1) sym) ─┘   └── angular breaking ──┘
```

## 临界点

### 角度方向

```
∂V/∂θ = −n · ε · |C| · rⁿ · sin(n·θ + φ_C) = 0
  ⟹  n·θ + φ_C = k·π,   k = 0, 1, ..., 2n−1
```

**极小点**（`cos(n·θ+φ_C) = −1`，角向势最低）：

```
θₖ_min = ((2k+1)·π − φ_C) / n,   k = 0, 1, ..., n−1
```

共 **n 个等间距离散极小**，环上相邻极小角度间隔 `2π/n`。

**鞍点**（`cos(n·θ+φ_C) = +1`，角向势最高，位于相邻极小中点）：

```
θₖ_saddle = (2k·π − φ_C) / n,   k = 0, 1, ..., n−1
```

### 径向方向（在角度极小处，`cos=−1`）

```
∂V/∂r |_{cos=-1} = 4r(r²−v²) − n·ε·|C|·r^{n−1} = 0
```

隐方程。令 `r = v·(1+δ)`，到 `O(ε)` 一阶：

`4r(r²−v²) = 4v(1+δ)·v²·(2δ+δ²) ≈ 8v³·δ`（leading order in δ）
`n·ε·|C|·r^{n−1} ≈ n·ε·|C|·v^{n−1}`

平衡 `8v³δ = n·ε·|C|·v^{n−1}` → `δ = +n·ε·|C|·v^{n−4}/8`：

```
r_min ≈ v · [1 + n·ε·|C|·v^{n−4} / 8]   (cos=−1 方向，径向向外扩)
```

直觉 check：cos=−1 方向 V_ang = −ε|C|rⁿ 为负贡献，把能量曲面往下拉，径向最优位置略**偏外**（能量进一步降低），不是偏内。对角度鞍点，`cos=+1`：

```
r_saddle ≈ v · [1 − n·ε·|C|·v^{n−4} / 8]  (cos=+1 方向，径向向内缩)
```

### 在角度鞍点之外：还有没有"径向逃逸"路径？

沿 θ=θ_min 固定，令 `r → ∞`：`V → r⁴ + ε|C|·(−1)·rⁿ`，对 `n < 4` 仍被 `r⁴` 主导，势沿径向单调升，不存在径向逃逸路径。对 `n ≥ 4` 需更细分析（`n=4` 临界、`n>4` unstable，Block V 不讨论）。**Block V 聚焦 n ∈ {2, 3, 4}，径向稳定**。

## 势垒高度（adjacent-minima barrier）

在 `r ≈ v` 的环上，从一个极小跨过相邻鞍点：

```
ΔV_angular = V(r=v, cos=+1) − V(r=v, cos=−1)
            = [0 + ε|C|·vⁿ·(+1)] − [0 + ε|C|·vⁿ·(−1)]
            = 2 · ε · |C| · vⁿ          (to leading order in ε, O(ε²) corrections from radial shift)
```

这是**跨越单个 Z_n 破缺的能量成本**。对 Langevin 有效温度 `T_eff = σ²/(2γ)`，相邻极小间 Arrhenius 跨越率 `∝ exp(−2ε|C|vⁿ / T_eff)`（前提 `2ε|C|vⁿ/T_eff >> 1`，否则 Kramers 不适用见 a1_4 文档 §Kramers）。

## Hessian 曲率（稳定性）

在极小点 `(r_min, θ_min)`，`cos(n·θ+φ_C) = −1`：

```
∂V/∂r    = 4r(r²−v²) + n·ε|C|·r^{n−1}·cos(nθ+φ_C)

∂²V/∂r²  = 4(3r²−v²) + n(n−1)·ε|C|·r^{n−2}·cos(nθ+φ_C)
         = 8v² − n(n−1)·ε|C|·v^{n−2}              (leading + O(ε) 修正 at cos=−1)
         ≈ 8v²                                     (正定 → 径向稳定)

∂²V/∂θ²  = −n²·ε·|C|·rⁿ·cos(nθ+φ_C)
         = +n²·ε·|C|·vⁿ                           (正定 → 切向稳定 at cos=−1)

∂²V/∂r∂θ = −n²·ε·|C|·r^{n−1}·sin(nθ+φ_C)
         = 0   at minimum (sin=0)
```

→ Hessian **对角**，极小稳定。曲率特征值：

```
λ_r ≈ 8v²                (径向硬，与 GL baseline 同)
λ_θ ≈ n² · ε · |C| · vⁿ    (切向软，∝ n²ε)
```

**[DYNAMIC-IMPLEMENTATION] 时间尺度分离**（overdamped Langevin 规约）：

Overdamped 弛豫时间 `τ = γ/λ`（不是欠阻尼振荡 `√(λ/m)`——无动量）：

```
τ_r = γ/λ_r ≈ γ/(8v²)
τ_θ = γ/λ_θ ≈ γ/(n²·ε|C|·vⁿ)

τ_θ / τ_r ≈ 8/(n²·ε|C|·v^{n−2})   (一般情形)
         ≈ 8/(n²·ε)                (v=|C|=1)
```

**保留系数 8 很重要**：对 n=3, ε=0.05，真实 τ_θ/τ_r ≈ 17.8，而不是省略 8 的 ~2.2。这个差一个数量级，直接影响仿真 horizon 估计（Block V 实验需 `t_sim ≫ τ_θ` 才能采样 angular attractor）。

相比欠阻尼估计 `1/(n·√ε) = 1/3·√0.05 ≈ 1.5` (n=3, ε=0.05)，overdamped 的 `8/(n²ε) ≈ 17.8` 绝热分离更强一个量级——一致地，overdamped 无动量惯性反弹，弛豫纯耗散，慢尺度更慢。

## Attractor 数量预测

```
k* = n
```

对应 Z_n 离散破缺后的基态数目。具体：

| n | 群 | 极小数 | 几何 | 对 exp017 k*=2 解释 |
|---|---|---:|---|---|
| 2 | Z₂ | 2 | 对跖 | 与 baseline GL (φ → −φ Ising-like) **重合**；若 BGE Z₂ bistability 源自 n=2 angular breaking（而非幅值 bistability），则两种机制可等价 |
| 3 | Z₃ | 3 | 正三角 | 第一个非平凡的 U(1) 离散破缺；k*=3 是首选判别实验 |
| 4 | Z₄ | 4 | 正方 | clock model; Z₄ 循环群，唯一真子群 Z₂ |

### ε → 0 极限：恢复 U(1)

`V → (r²−v²)²`，环上 flat，整条 Mexican hat 圆 S¹ 均为 degenerate ground state。Standard cluster silhouette 会在这种情况下给 `k* → 1` 或随机（退化），但 **persistent homology Betti₁ = 1** 会稳定检测到 S¹ 拓扑 —— 这是为什么 Block V evaluation 必须升级 PH 的关键原因之一。

### ε → ∞（或 ε|C|·v^{n−4} >> 1）极限

径向稳定性判据：在 cos=−1 方向 `V = (r²−v²)² − ε|C|rⁿ`，`r→∞` 时：

- **n < 4**：`r⁴` 主导 → V → +∞，径向恒稳定，任意 ε
- **n = 4**：`V ~ (1−ε|C|)·r⁴`，稳定当 **`ε|C| < 1`**；超过则 V→−∞
- **n > 4**：`rⁿ` 主导 → 任意 ε>0 都 V→−∞，非物理

注意：**关键在 n 与 4 的大小关系 + ε|C| 系数**，**与 n 奇偶无关**（奇 n=3 的 cos=−1 方向也负贡献）。v1 归因于"n 偶"是错的，v2 纠正。

**合理工作区**：`ε · |C| · vⁿ ≤ 0.1 · v⁴`（破缺项 < 10% Mexican hat 深度）。例如 v=1, n=3, |C|=1：`ε ≤ 0.1`。

## 与 Block V V.1-A 的工程对接

V.1-A sub-block 在 Rust 端只需改 `potential.rs` 的 `grad_V` 实现：

```rust
// in potential.rs, add enum variant ZnAngular { v: f64, n: u32, eps_c: Complex64 }
// eps_c 编码 ε·C（ε 实数，C 复数幅值相位）
fn grad_V_Zn(psi: Complex64, v: f64, n: u32, eps_c: Complex64) -> Complex64 {
    // 返回 ∂V/∂ψ* （Wirtinger 导数），gradient flow 驱动力 = −this
    let r2 = psi.norm_sqr();
    // Mexican hat: V_mex = (|ψ|²−v²)², ∂/∂ψ* = 2(|ψ|²−v²)·ψ
    let mexican = 2.0 * (r2 - v*v) * psi;
    // Angular: V_ang = (ε/2)·[Cψⁿ + C*(ψ*)ⁿ],  ∂/∂ψ* = (n/2)·ε·C*·(ψ*)^{n−1}
    //                                            = (n/2) · eps_c.conj() · ψ*^{n−1}
    let angular = 0.5 * (n as f64) * eps_c.conj() * psi.conj().powu(n - 1);
    mexican + angular
}

// 构造处约束（Z_1 平凡非物理，且 u32 下溢会 panic）
// ZnAngular::new(v, n, eps_c) { debug_assert!(n >= 2); ... }
```

**Wirtinger derivation（为什么是 ψ* 不是 ψ，为什么带 ½）**：

把 `Re(Cψⁿ) = ½·[Cψⁿ + C*(ψ*)ⁿ]` 展开。在 Wirtinger 演算里 `ψ` 与 `ψ*` 视作独立变量，`∂ψⁿ/∂ψ* = 0`（不含 ψ*），`∂(ψ*)ⁿ/∂ψ* = n·(ψ*)^{n−1}`。所以

```
∂V_ang/∂ψ* = (ε/2) · [0 + C* · n · (ψ*)^{n−1}] = (n/2) · ε · C* · (ψ*)^{n−1}
```

Gradient flow 方程 `γ·∂_t ψ = −∂V/∂ψ*` 对应力学上的"ψ 沿能量负梯度演化"，使用 ψ* 而非 ψ 是复变量耗散系统的标准规约（实数情形 ψ=ψ* 退化重合，这是 n=2 时 bug 碰巧无可见效应的原因）。

**对 n 的差异**：
- n=2：正确项 ∝ (ψ*)¹ = r·e^{−iθ}，错误项 ∝ ψ = r·e^{+iθ}。V_ang 本身不变（V 是实数），但 gradient flow 方向反了。**统计不可分辨的根因**：Z_2 极小集 {θ=0, π} 在复共轭 θ→−θ 下自映射（0↔0, π↔π），所以正确 / 错误代码给出的 attractor 分布完全重合——不是"U(1) 平均掩盖"，而是 Z_2 极小集的复共轭对称
- n=3：`(ψ*)² ≠ ψ²`（相位翻倍且符号相反），错写会把 `e^{i2θ}` 写成 `e^{−i2θ}`，attractor 旋向反转 → 实测 angular histogram 会呈"镜像 Z_n"而不是正 Z_n，但仍 k*=n，容易误判"代码正确"
- n=4：同理，镜像效应但 Z_4 对称掩盖更深——**最隐蔽的 bug**

### 诊断 checklist（V.1-A 实测应当看到的）

1. **极小数** = n（phase histogram 应有 n 个峰，等间距 2π/n）
2. **幅值分布**窄且单峰在 ~v（不是 bistable）
3. **silhouette k-search** 给出 `k* = n`（若不是，说明 ε 太小、或系统未收敛）
4. **跨极小切换率** `∝ exp(−2ε|C|vⁿ · dt · N_steps / σ²)`，可用来校准 ε 和 σ 配合
5. **persistent homology Betti₀ → n, Betti₁ → 0**（对比 U(1) ε=0 时 Betti₁=1）

### 推荐 Block V V.1-A 扫描网格（MVP）

```
n ∈ {2, 3, 4}
ε|C| ∈ {0.01, 0.05, 0.1}  (3 级破缺强度)
σ (gradient flow ε=0 / Langevin σ=0.1 / σ=0.5)  如果 Q3 要联合
固定: v=1.0, dt=0.05, evolve=5000, lattice=32³
```

共 9 参数点（纯 gradient flow）或 27（含 Langevin）。每点 ~3 min Rust，可在 0.5–1.5h 内完成 MVP 扫描。

## 不下的结论

1. n ∈ {2,3,4} 哪个应该 **优先**跑 —— Block V 设计已建议 n=3（first nontrivial），但最终哲学位阶等一凡 × Win。
2. ε 和 σ 的哲学解释（"symmetry-breaking strength" vs "thermal noise"）是否对应辩证法某概念 —— 不碰。
3. Z_n 与 source-density regime 的联系（Stage C 的 byte Z_1 / BGE Z_2 是否就是"自发到 n=1 or n=2 不同 group"的表现）—— 留给一凡。

[?] 上述这些推理好不好 —— 等一凡看了决定。

---

**附：参考文献 pointers**（Block V 写作时可直接引）

- Ginzburg-Landau + explicit Z_n breaking：任何 Landau-Ginzburg textbook 的 Potts/clock model 章节
- Non-abelian 扩展（SU(2)）：Goldstone theorem + Anderson-Higgs mechanism 文献
- Persistent homology on complex order-parameter fields：Adams et al. giotto-tda 2021
- Langevin on Mexican hat with explicit breaking：Bray, Adv. Phys. 2002（coarsening dynamics）

本文不包含外部引用验证，是数学推导本身。外部文献 citation 由 Win 主导 arXiv v1 时确认。
