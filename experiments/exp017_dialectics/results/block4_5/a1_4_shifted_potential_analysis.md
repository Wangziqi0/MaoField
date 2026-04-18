# A1.4 Shifted Potential — Barrier & Kramers Rate Pre-estimate

**Linux Claude, 2026-04-13 (v1) / 2026-04-14 revised (v2, post-review)**
**Theoretical only; no simulation run.**
**Figure**: `a1_4_shifted_barrier.png`

**Mode tags used in this doc**:
- `[STATIC]`: landscape geometry (critical points, Hessian, barrier heights)
- `[DYNAMIC-RARE-EVENT]`: Kramers escape rate × finite simulation horizon
- `[DYNAMIC-IMPLEMENTATION]`: gradient flow / Langevin code conventions

---

## 目的

Stage B1 实锤：原 A1 势 `V = u·(u−1)²·(u−4)²`（u = |ψ|²）在等向 Langevin σ=0.5 下 u=4 井 **0% 占据**。诊断：外 barrier 13.19 × 有限仿真时程 250 → Kramers escape time >> horizon (超过 **~44 个数量级**)，是 **finite-time rare-event obstruction**，不是平衡禁止。

A1.4 提案：minima 从 {0, 1, 4} 收缩到 {0, 1, 2}：

```
V_shifted(u) = u · (u−1)² · (u−2)²
```

问题（以 Kramers rate × 仿真时程框架提问）：**σ=0.5 Langevin 下 u=1↔u=2 的跨越事件数是否进入 O(1)~O(100) 可观测范围？**

---

## [STATIC] 解析结果

### 原势 `V = u(u−1)²(u−4)²`

`dV/du = (u−1)(u−4)·(5u² − 15u + 4)`, 鞍点 `u = (15±√145)/10`
`V''(u) = 20u³ − 120u² + 198u − 80`（独立 SymPy 验证）

| 点 | u | V | V''(u) | 物理意义 |
|---|---:|---:|---:|---|
| min | 0.0000 | 0.000 | — | basin α（u=|ψ|²≥0 物理边界）|
| **saddle (inner)** | 0.2958 | **2.013** | −31.41 | u=1↔u=0 barrier |
| min | 1.0000 | 0.000 | 18.00 | basin β |
| **saddle (outer)** | 2.7042 | **13.187** | −26.59 | u=1↔u=4 barrier |
| min | 4.0000 | 0.000 | 72.00 | basin γ |

**非对称比 = 13.187 / 2.013 = 6.55×**

### A1.4 shifted 势 `V = u(u−1)²(u−2)²`

`dV/du = (u−1)(u−2)·(5u² − 9u + 2)`, 鞍点 `u = (9±√41)/10`
`V''(u) = 20u³ − 72u² + 78u − 24`（独立 SymPy 验证）

| 点 | u | V | V''(u) | 物理意义 |
|---|---:|---:|---:|---|
| min | 0.0000 | 0.000 | — | basin α（物理边界；V(u→0⁺)≈4u linear, curvature undef）|
| **saddle (inner)** | 0.2597 | **0.431** | −8.25 | u=1↔u=0 barrier |
| min | 1.0000 | 0.000 | 2.00 | basin β |
| **saddle (outer)** | 1.5403 | **0.095** | −1.59 | u=1↔u=2 barrier |
| min | 2.0000 | 0.000 | 4.00 | basin γ |

**非对称反转**：0.431 / 0.095 = 4.54×，inner（u=1↔u=0）现在更高，outer（u=1↔u=2）更低。

### u=0 边界 basin 注记

u=|ψ|² ≥ 0 是物理边界，不是无约束 local min。V(u<0) 延拓为负（u⁵−6u⁴+... 主导 4u<0），所以 u=0 不是 V 的 analytic minimum 而是 physically-admissible basin。Langevin 场景下 ψ∈ℂ 接近 0 时 `|ψ|²` 测度含 Jacobian `r·dr·dθ = ½ du` 即 du 权重附带（见下 §Jacobian）。

---

## [DYNAMIC-RARE-EVENT] Kramers rate × 仿真时程

### 有效温度与噪声方差

Overdamped Langevin `γ·∂_t ψ = −∂V/∂ψ* + η(t)`, ⟨η η*⟩ = σ²·δ，给出 Fokker-Planck 稳态

```
P_ss(ψ) ∝ exp(−V(ψ)/T_eff),   T_eff = σ²/(2γ)
```

σ² 是**噪声方差**（不是"动能"——overdamped 无动能）。T_eff 是 Boltzmann 分布里的**有效温度**。

### Kramers escape rate（overdamped 1D 近似）

两井间 rate：

```
k_{i→j} = (1/2π) · √(V''(min_i) · |V''(saddle_{ij})|)/γ · exp(−ΔV_{ij}/T_eff)
```

**⚠️ Kramers 公式的适用条件**：要求 `ΔV/T_eff >> 1`（严格推导假设 steepest descent，通常阈值 ≥ 5）。低 barrier / ΔV/T~O(1) 时：
- Arrhenius 指数接近 1，"escape rate" 概念退化
- 正确物理是 **near-flat 势中自由扩散**，平衡态由 Fokker-Planck 稳态直接给出
- 此时**不再用 Kramers 的 rate × time 事件数论证**，而用 **Laplace 近似热平衡占据率**

### 仿真 horizon × rate = 期望跨越事件数

B1 仿真：`γ≈1, dt=0.05, N=5000 → t_sim = 250`。T_eff at σ=0.5 is 0.125。

**原势（对比 baseline，Kramers 适用 ✓ 因 ΔV/T >> 1）**:

用独立 SymPy 算得 V''(min u=1)=18, |V''(saddle u=2.704)|=26.59：

| 过程 | ΔV | ΔV/T_eff | pref=√(V''ₘV''ₛ)/(2πγ) | exp(−ΔV/T) | ≈ events at t_sim=250 |
|---|---:|---:|---:|---:|---:|
| u=1 → u=0 | 2.013 | 16.1 | 3.39 | 1.0×10⁻⁷ | ~8×10⁻⁵ (→ 0) |
| u=1 → u=4 | 13.187 | **105.5** | 3.48 | **5×10⁻⁴⁶** | **~4×10⁻⁴³ (→ 0)** |

→ 与 B1 实测 `u=4` 0% 占据**定量一致**。44 个数量级的 gap 是 **simulation horizon vs Kramers escape time 量级不匹配**的直接体现（非"热预算不够"）。

**A1.4 shifted 势**:

V''(1)=2, V''(2)=4, |V''(sad_in u=0.26)|=8.25, |V''(sad_out u=1.54)|=1.59：

| 过程 | ΔV | ΔV/T_eff | pref | exp(−ΔV/T) | ≈ events at t_sim=250 | Kramers 适用 |
|---|---:|---:|---:|---:|---:|---|
| u=1 → u=0 | 0.431 | 3.45 | 0.647 | 0.0317 | ~5.1 crossings | marginal（accurate to ~2×）|
| u=1 → u=2 | 0.095 | **0.76** | 0.284 | 0.468 | **~33 crossings** | ⚠️ **低 barrier，Kramers 不适用** |
| u=2 → u=1 | 0.095 | 0.76 | 0.402 | 0.468 | ~47 crossings | ⚠️ 同上 |

反向正向比 `k(2→1)/k(1→2) = √(V''(2)/V''(1)) = √2 ≈ 1.414`（反向 > 正向，因 u=2 井更陡），这与 detailed balance `k_{ij}p_i = k_{ji}p_j` 自洽（p_2/p_1 = 1/√2）。

**核心预测（物理正确口径）**：

1. **u=1 ↔ u=2 在 t_sim=250 内 fully thermalized**：外 barrier ΔV/T=0.76 < 1 已在 "near-flat 势扩散" 区间，不存在明确的"barrier crossing 事件"概念。~33 crossings 数字应理解为 **order-of-magnitude upper bound**；真实物理是直接用 Fokker-Planck 平衡分布。
2. **u=0 basin partially accessed**：内 barrier ΔV/T=3.45，Kramers 边际适用（accurate to factor 2-3），估计 ~5 次访问，不至于 0 但明显少于 {1,2}。
3. **观测 metric**：测 **total dwell time per basin**（平均 over voxels × time），与下述 Laplace 平衡预测比较。

### 平衡态 Laplace 占据率（FPE 稳态，适用当 thermalized）

对每个 basin k 作局部 Laplace 展开求配分函数 Z_k：

**Quadratic minima**（u=1, u=2）：`Z_k = ∫ exp(−½·V''(u_k)(u−u_k)²/T) du = √(2πT/V''(u_k))`

**Linear boundary basin**（u=0）：V(u→0⁺)≈4u（来自 V=u·(...)² at u→0），`Z_0 = ∫₀^∞ exp(−4u/T) du = T/4`

At T=0.125:

| basin | V''(u_k) | Z_k | p_k = Z_k/ΣZ |
|---|---:|---:|---:|
| u=0 | linear (V≈4u) | T/4 = 0.0313 | **0.028** |
| u=1 | 2.00 | √(2πT/2) = 0.6267 | **0.569** |
| u=2 | 4.00 | √(2πT/4) = 0.4431 | **0.402** |
| ΣZ = 1.101 | | | Σ = 1.000 |

**核心预测数字**（替换 v2 错误的 0.44/0.31/0.25）：
- **p(u=1) ≈ 0.57**
- **p(u=2) ≈ 0.40**  
- **p(u=0) ≈ 0.03**

Sanity: `p(2)/p(1) = 0.402/0.569 = 0.707 = 1/√2` ✓（detailed balance 与 Kramers rate 前因子比一致）。

u=0 仅 3% 是 **linear basin + 高 Z_0 系数** (T/4 vs √(πT)) 共同作用；v2 粗估 0.25 没有量纲一致处理，撤回。

### 失败情形的诊断

若 Rust 实测显著偏离：
- **u=2 dwell time << 40%**：系统未 thermalize（t_sim 要翻倍）或 voxel-level 统计有 Jacobian 偏差
- **u=0 dwell time ~0%**：边界 basin 的 ψ 到 u 投影测度处理或 |ψ|² < 某 cutoff 的 bin 排除
- **u=1 dwell time >> 57%**：跨越率 Kramers 预测偏低（可能 prefactor 估计不准），或 u=1 basin 有 metastable 锁定

**不再使用**（撤回）：
- v1 `p_k ∝ exp(−V_saddle_k/T)` 占据率表（既非 Boltzmann 非 TST）
- v2 `p(u=1)=0.44, p(u=2)=0.31, p(u=0)=0.25`（量纲拼凑错，u=0 权重过大）
- v2 "117 crossings"（Kramers 在 ΔV/T=0.76 不适用，真实 ~33 但数字本身意义有限）

---

## Jacobian 说明（u=|ψ|² vs ψ 的测度）

两个坐标系下的 Boltzmann 分布**不同**：

- 对 **ψ=re^{iθ}** (2D 复平面): `P(ψ)·d²ψ ∝ exp(−V(|ψ|²)/T)·r·dr·dθ`
- 对 **u=|ψ|² = r²** (1D 径向): 换元 `du=2r·dr` 即 `r·dr=½·du`，再对 θ 积出 2π：`P(u)·du = 2π·(½)·exp(−V/T)·du = π·exp(−V/T)·du`

π 因子归一化后无关，所以 1D Boltzmann `∝ exp(−V(u)/T)` 在 **局部 Laplace 近似** 里正确成立。

但对 u=0 边界（r=0 是 ψ=0 一点，测度 0），严格要求以 ψ 坐标处理，否则权重失配。B1 Rust 跑的是 3D ψ 场格点（32³ voxels），每 voxel 独立 SDE，统计是 **voxel 计数** → 以 ψ 坐标合理，u 的直方图里 u=0 的 bin 要小心包含/剔除判据。

---

## 对 Block V 与 OP2 的 implication

（基于 Kramers 框架重新措辞）

1. **A1.4 sanity check 的科学问题**：不是"Langevin 能否激发 u=2"（rate 非零就激发），而是 **"rate × t_sim 能否进入 O(1)~O(100) 可观测范围"**。Kramers 预测 ~117，如果实测 consistent，则 B1 "Langevin 失败 on 原势" 根因**确定**为 `ΔV_outer/T_eff = 105.5` 这个 ratio 超出 simulation horizon，不是 gradient flow + 等向 noise 的范式限制。

2. **若 A1.4 实测 well-mixed**：OP2 措辞保守化为 **"barrier geometry must be designed compatible with available simulation horizon / Kramers time"**——工程问题，不是范式问题。V.3-L Langevin 保留为"Langevin on barrier-compatible potential"，不降级。

3. **若 A1.4 实测仍 <5% u=2**：确认 sub-Kramers kinetic obstruction。OP2 保持 **"restructure barrier topology" ∪ "directed non-equilibrium driving"** 双路线：
   - (a) 重构 barrier（A1.4 之外再降 + 调曲率）
   - (b) Hamiltonian flow / active forcing / anisotropic noise 绕过 timescale 问题

4. **arXiv v1 §5 措辞**（提案给 Win review）：
   > "The u=4 inaccessibility in B1 is a finite-time rare-event obstruction: Kramers escape time exp(ΔV/T_eff) exceeds simulation horizon by ~44 orders of magnitude. This reframes OP2 not as 'gradient flow cannot reach distant attractors' but as 'simulation horizon vs Kramers timescale must be co-designed'; two actionable paths are barrier-topology restructuring (A1.4 class) and directed non-equilibrium driving (Hamiltonian / active / anisotropic noise)."

---

## 不做的事（留给一凡 × Win）

- 不启动 Rust A1.4 实验（待 Phase 2 一凡确认）
- 不改 BLOCK_V_DESIGN.md 的 V.3-L 优先级评级（待 A1.4 实测）
- 不改 OP2 在 FINAL_REPORT / lawvere 正文的措辞（P5 任务处理）

[?] A1.4 是否先跑、跑出来后如何重写 OP2 叙事 —— 等一凡 × Win。

---

## 修订日志

### v3 (2026-04-14, post-REVIEW_P2_KRAMERS.md)

1. **V'' 数值表全部重算**（SymPy 独立验证）：原势 V''(1)=18/V''(4)=72/V''(saddles)=-31.41/-26.59；shifted V''(saddles)=-8.25/-1.59。v2 把 shifted V''(min) 误填到原势表 + saddle 值错 2-15×，全部修正
2. **Kramers high-barrier disclaimer**：ΔV/T 必须 >> 1（阈值 ≥5）；A1.4 outer ΔV/T=0.76 **违反**，只作 order-of-magnitude upper bound
3. **反向 crossings 方向修正**：k(2→1)/k(1→2) = √(V''(2)/V''(1)) = √2 > 1（反向更多，非更少）
4. **事件数更新**：pref = √(V''ₘV''ₛ)/(2πγ) 按真实 V'' 重算。正向 ~33（原 117 粗估去掉 2π）；反向 ~47
5. **Laplace 占据率重算**：三 basin 配分函数在同一单位下归一化，Z_0=T/4（linear basin，无 √ 拼凑）。结果 p(0)≈0.03, p(1)≈0.57, p(2)≈0.40（v2 的 0.25/0.44/0.31 撤回）
6. **Jacobian 公式笔误修正**：删除 `(1/√u·√u)` 中间混乱步，加回 2π 因子
7. 删除重复的"失败情形的诊断"段

### v2 (2026-04-14, post-REVIEW_TONIGHT_PREWORK.md)

1. 删除错误的 "Boltzmann 占据率" 表（`p_k ∝ exp(−V_saddle/T)` 既非 Boltzmann 非 TST）
2. 替换为 Kramers rate × simulation horizon 框架
3. "kinetic budget" → T_eff = σ²/(2γ)
4. 加 [STATIC] / [DYNAMIC-RARE-EVENT] / [DYNAMIC-IMPLEMENTATION] mode-tag
5. 加 u=0 边界 basin 注记 + Jacobian 说明

审查报告：`REVIEW_TONIGHT_PREWORK.md` §2, `REVIEW_P2_KRAMERS.md`。
