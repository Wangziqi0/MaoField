# 审查报告 Phase 2.5 walled — A1.4 Soft Wall 三配置

**审查员**：独立 paper-review subagent, 2026-04-14
**范围**：V_wall = λ·max(0, u−2.5)^4 on shifted potential, 3 配置
**判定**：**Release-ready = 否；Verdict-ready = 是（with revised framing）**

---

## §1 三配置数值正确性

| Config | u_mean | p(u=0) | p(u=1) | p(u=2) | p(clamped) | p(>2.5) |
|---|---:|---:|---:|---:|---:|---:|
| no wall σ=0.5 | 9.90 | 0.054 | 0.246 | 0.041 | 0.525 | — |
| **walled c1** λ=1 σ=0.5 | 10.04 | 0.054 | 0.242 | 0.040 | **0.534** | 0.535 |
| **walled c2** λ=10 σ=0.5 | 11.04 | 0.052 | 0.209 | 0.031 | **0.593** | 0.594 |
| no wall σ=0.3 | 1.61 | 0.012 | 0.363 | 0.408 | 0.004 | — |
| **walled c3** λ=1 σ=0.3 | 1.62 | 0.012 | 0.363 | 0.407 | 0.005 | 0.008 |

一致性 check：c1 / c2 的 `p_clamped` 仅比 `p_above_2.5` 小 0.15% / 0.11% → voxels 在 (2.5, 3) 区间 transit 但不 reside。c3 `p_above_2.5 − p_clamped = 0.30%` → wall passive 确认。✅

## §2 walled 为何没救 σ=0.5（机制）

正确三条原因 + review 补一条：

**(i)** BGE source Sb 偏置 `mean=-0.00148, t=-17.1, p<1e-25` → 非平衡 drift。Wall 不修复 drift。
**(ii)** ΔV_outer/T_eff=0.76 < 1 → basin escape rate 由 noise 主导，wall 只换"escape 后去哪"。
**(iii)** Wall 仅作为 |ψ|² 上界，basin 间 traffic 不变。
**(iv, 新)** clamp 是 **hard absorbing** wall (不是 reflecting)：clamp 后 phase info 丢失，一旦 53% clamped-pool 形成，**detailed balance 被破坏**；wall 只能延缓不能消除这个 sink。

`k=4` 在 `u→2.5+` 斜率为 0（C³-smooth），wall force 在 `u=2.6` 仅 4e-5，`u=3.0` 才 0.5。voxel 用 ~5 步 noise (0.5/σ√dt=4.5) 穿越 [2.5, 3.0] transit 区到 clamp。实测 c1 中 (2.5, 3.0) 只占 0.15% 证实为 transit 而非 reside。

## §3 λ=10 比 λ=1 更糟：explicit Euler CFL 违反

Wall Jacobian at u=10, |ψ|=3.16：
- c1 (λ=1): `J ≈ 12·(7.5)²·(6.32)² + 4·(7.5)³·2 ≈ 30,000`
- c2 (λ=10): `J ≈ 300,000`

explicit Euler stability `dt·|J| < 2` → `dt_max,c1 ≈ 6.7e-5`, `dt_max,c2 ≈ 6.7e-6`。
实测 dt=0.05 **超 stable 上限 750× (c1) / 7500× (c2)**。

不稳定被 clamp 吸收：λ ↑10 → 单步 overshoot ↑10 → 反弹更猛 → clamp event 更频 → stationary clamp probability ↑。实测 0.534 → 0.593 (+5.9 pp) 与此一致。

**工程 take-away**：explicit Euler + dt=0.05 + 任何 meaningful wall 不兼容，要 implicit/IMEX 或 dt=1e-4 或 reflecting BC（超出当前 Phase 2.5 范围）。

## §4 σ=0.3 control 验证

c3 vs no-wall σ=0.3 四指标差异 < 0.05 pp（远在 2.3M sample 的 1σ=0.03% 内）。`P(u>2.5)=0.75%` → wall 99.25% 时间 inactive。**walled c3 与 no-wall σ=0.3 统计等价 ✓**。

此 control 正向验证：
- wall 按需启动符合设计
- σ=0.3 的非-Laplace 行为 (p₁/p₂=0.89 vs 预测 1.41) **不是 wall artifact**，是 source drift + partial mixing 本身

**c3 是 Phase 2.5 唯一 unambiguous positive control**。

## §5 对 a1_4 v3 / arXiv §5 OP2 措辞修订

### a1_4 文档
- Phase 2.5 wall 段：改 "soft wall (k=4, λ∈{1,10}) **未能** 阻止 σ=0.5 下 53-59% clamp。Wall 在 basin 区域 passive (σ=0.3 control 验证)；boundary 区域被 explicit Euler instability 吸收为 clamp residency。"
- OP2 出路诊断：**三要素并列**
  1. Source drift（BGE Sb mean ≠ 0, t=-17）需源场端 mean-subtraction/whitening
  2. Shifted V 在 u>2 衰减为 u⁵ 太浅，需 quartic-cap 或 log-confinement
  3. Explicit Euler + soft wall 不可同存，需 implicit or reflecting BC
- Verdict 段加："A1.4 证伪 'lower barrier alone enables OP2 access'；OP2 不是 barrier 问题，是 source-drift × tail-shape × integrator-BC 三体耦合。"

### arXiv §5 OP2 建议段落
> "Phase 2.5 systematically tests OP2 access via (a) σ-scan on shifted V = u(u-1)²(u-2)² and (b) soft-wall regularization V_wall = λ(u-u_max)⁴. Neither recovers Laplace stationary. Diagnostic decomposition attributes the gap to three independent obstructions: (i) BGE source field statistically biased (mean Sb = -1.5e-3, t=-17.1, p<1e-25), violating Laplace mean-zero source assumption; (ii) shifted potential decays as u⁵ for u>2, insufficient confinement against σ√dt = 0.11 noise scale; (iii) explicit-Euler stability requires dt·∂f_wall/∂a < 2, violated by any meaningful wall stiffness at dt=0.05, producing artifactual clamp accumulation. **OP2 is not a barrier-geometry problem; it is a source-statistics × tail-shape × integrator-BC coupled problem, deferred to Block V.**"

**保留**诊断价值，**避免**承诺无法兑现的"OP2 工程通路"。

## §6 整体 Release Gate

### 已有材料
| 实验 | 用途 |
|---|---|
| σ-scan {0.1, 0.3, 0.5, 0.7} | kinetic regime 4-分类 |
| σ=0 deterministic baseline | init+gradient pull 隔离（66% u=2 已偏离 Laplace 0.412）|
| BGE source stats | Laplace 假设 (ii) 明确证伪 (t=-17.1) |
| walled σ=0.5 ×2 | OP2 simple-wall 出路证伪 |
| walled σ=0.3 control | wall passive 验证 |

### Verdict 能写的强命题
1. ✅ "shifted V + σ-scan + simple soft wall **不能** 在 BGE source 下复现 Laplace 平衡"
2. ✅ "OP2 三要素瓶颈：source drift / V tail 浅 / integrator-BC 不兼容"
3. ✅ "σ=0 baseline 66% u=2 已偏离 Laplace 0.412，**不需要噪声就证伪 'shifted V 给出 Laplace 平衡' 的 naive 期望**"
4. ✅ "BGE source mean Sb (t=-17) 是 Laplace 假设的硬证伪，与 V-shape 无关"

### 不可写
- ❌ "OP2 不可达"（只证伪这一路径）
- ❌ "Allen-Cahn 框架破产"（σ=0 baseline 显示框架内动力学正确）

### 可选补充（不阻塞 verdict）
Uniform init on (a,b)∈[-3,3]² + σ=0.3 + steps=10000：唯一能区分 "partial mixing snapshot" vs "true non-Laplace stationary"。对 source drift vs horizon 相对贡献定调。

## Bottom line

Phase 2.5 四组数据（σ-scan + walled ×3 + σ=0 + BGE stats）**够写 A1.4 verdict**。措辞必须从"OP2 通路探索"切到"OP2 工程难点诊断 + Block V roadmap"。负结果在论文叙事上比假阳性更有价值——A1.4 成为论文里**唯一**有完整 4 类诊断（kinetic / boundary / source / integrator）的 OP，可作方法学示范段。

**Win review 完成后可起笔 verdict。**
