# 审查报告 Phase 2.5 σ-scan — A1.4 Shifted Potential

**审查员**：独立 paper-review subagent, 2026-04-14
**范围**：σ∈{0.1, 0.3, 0.5, 0.7} Langevin on V_shifted = u(u-1)²(u-2)²
**判定**：**Release-ready = 否**。框架数学正确，数据处于多个非-Laplace regime（kinetic freezing / partial mixing / boundary artifact）。

---

## §1 数值验证

### Init u 分布（独立 Monte Carlo, N=2e6）

`init_u_nonzero`: a=1.0+0.3·(2r−1), b=0.3·(2r−1), u=a²+b² ∈ [0.49, 1.78]

| 指标 | 值 |
|---|---|
| P(init u < 0.15) | **0** (init 不接触 u=0 basin) |
| P(init 0.6≤u≤1.4) | 0.692 |
| P(init 1.7≤u≤2.3) | 0.014 |
| **P(init u > 1.540, outer saddle)** | **0.119** |
| P(init in u=1 BoA) | 0.881 |

**关键**：11.9% voxels 起步已在 outer saddle 右侧，gradient flow 直接拉向 u=2（无需跨越）。

### Kramers rate × horizon (H=250)

| σ | T_eff | k₁₂·H | k₂₁·H | k₁₀·H |
|---|---|---|---|---|
| 0.1 | 0.005 | 4.0e-7 | 5.6e-7 | 5.9e-36 |
| 0.3 | 0.045 | **8.6** | **12.2** | 1.1e-2 |
| 0.5 | 0.125 | 33.2 | 46.9 | 5.1 |
| 0.7 | 0.245 | 48.2 | 68.1 | 27.8 |

**Regime 分类**：
- σ=0.1: kinetically frozen at init (k·H ≪ 1)
- σ=0.3: partial mixing (k·H ~10, 未 ergodic)
- σ=0.5: Kramers 失效（ΔV_outer/T=0.76 < 1），boundary artifact 主导
- σ=0.7: 纯噪声

### Laplace p₁/p₂ = √2 的独立蒙卡验证（(a,b)∈ℝ² rejection sampling, N=4e6）

| σ | p₀ | p₁ | p₂ | p_mid | **p₁/p₂** |
|---|---|---|---|---|---|
| 0.1 | 0.006 | 0.580 | 0.414 | 0.000 | **1.40** |
| 0.3 | 0.017 | 0.541 | 0.384 | 0.058 | **1.41** |
| 0.5 | 0.031 | 0.478 | 0.339 | 0.151 | **1.41** |

**Laplace 预测 p₁/p₂ = √2 = 1.414（u=1 占据多）**在所有 σ 下严格保持。我 a1_4 文档 v3 的数字 (0.569, 0.402) 也给出 0.569/0.402=1.415 ✓ 数字对，**但前文解读把它当作"equilibrium 可达"是错的**。

---

## §2 σ=0.1 实测 u=2 占据 0.853 vs Laplace 0.412 — **严重失配 73 pp**

**正确解释**：
1. **Kinetic freezing 主导**：T=0.005, k·H≈5e-7 → 零 Kramers crossing。系统冻结在 init 落入的 basin。
2. **Init bias 只解释 12%**：gradient flow 把 init u>1.54 的 11.9% 拉向 u=2，剩 88.1% 应留 u=1。**缺口 73 pp 无法由 init 解释**。
3. **第三机制候选**（未验证）：
   - (a) BGE 源场正向偏置（ψ drift to large |ψ|）
   - (b) gradient flow 把 u∈(1.4, 1.7) 的 voxels（init 占 ~10%）也向 u=2 倾倒（in-between=0.1% 暗示清空）
   - (c) dt=0.05 overshoot（outer well 浅 0.095，可能跳过）

**σ=0.1 不能作为 "验证 Laplace" 的证据**。

---

## §3 σ=0.3 "Goldilocks" 破灭

实测 p₁/p₂ = 0.363/0.408 = **0.889**，Laplace 预测 **1.414**。**比值方向反**。

**机制**：
- Rate 比正确：k₁₂·H/k₂₁·H = 8.6/12.2 = 0.704 ≈ 1/√2 ✓（detailed balance 数值一致）
- 但 reaction 未完成：21% in-between 是 transient
- **Init u=2 direct pull 11.9% + Kramers partial mixing = 不够翻转 Laplace 方向**
- 需要 horizon×10 (steps=50000) 或 uniform init 才能验证是否真收敛

**σ=0.3 是 "partial mixing snapshot" 不是 "thermal equilibrium"**。

---

## §4 σ=0.5 / 0.7 blow-up 机制

**σ=0.5 (52% clamped)**：
- ΔV_outer/T_eff = 0.76 < 1，Kramers 公式失效
- shifted V(u) ~ u⁵ 在 u>2 太浅
- Langevin step σ√dt = 0.112 连续多步可推 a→3 (clamp)
- clamp = reflecting-like wall + 持续 noise pressure → boundary 停留时间人为放大

**σ=0.7 (98% clamped)**：纯噪声，phase |R|=0.003 (uniform random)。

**这两个数据不是势函数物理，是 integrator + boundary artifact**。

---

## §5 对 a1_4 文档 v3 的修订建议

| 位置 | 问题 | 建议 |
|---|---|---|
| Laplace 预测表 | 公式正确但未声明假设 | 加 disclaimer: "(i) k·H≫1 for all transitions; (ii) 源场 mean-zero; (iii) boundary 不可达" |
| σ=0.1 解读 | 现暗示"低温好" | 改 "**kinetically frozen + init bias，不是 equilibrium**" |
| σ=0.3 解读 | "Goldilocks" 误导 | 改 "**partial mixing, horizon 不足**，p₁/p₂ 方向反" |
| σ=0.5/0.7 | 暗示势函数物理 | 改 "**boundary artifact，Kramers 失效，应排除物理结论集**" |

---

## §6 Release Gate

**补充对照实验优先级**：

1. **σ=0 deterministic-only**（同 init，无噪声）→ 隔离 init+gradient pull
2. **BGE 源场统计**（mean(F), ⟨F·ψ⟩ 是否 mean-zero）→ 验证 Laplace 假设 (ii)
3. **Uniform init on (a,b)∈[-3,3]² + σ=0.3, steps=50000** → 检查是否真收敛
4. **Walled potential**（一凡 Phase 2.5 实验组 2）→ 解决 boundary artifact
5. **dt=0.01 at σ=0.1** → 排除 overshoot

**核心结论**：
- **理论框架（Kramers + Laplace）数学正确**
- **当前数据不在 Laplace 适用区域**
- σ-scan 可作 "kinetic diagnostic" 发布，**不可作 "equilibrium validation"**

---

## Bottom line

σ-scan 交出硬数据但故事复杂：σ=0.1 kinetic trap、σ=0.3 partial mixing、σ=0.5/0.7 artifact。Laplace 方向在全部 σ 下均被实测违反。必须补 σ=0 deterministic 和 BGE 源场统计两项 baseline（低成本、不违反 init/clamp 禁令），再进 walled。
