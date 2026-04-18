# REVIEW_PHASE_B_EXP1_math_O1.md — 2026-04-15

**Reviewer**: Independent paper-review subagent (Opus, Silent Block 1)
**Scope**: Win taskbook §2 O1 — "局域相干结构谱" + Goldstone 软模判据

## Summary verdict

**存疑（Conditional Pass）** — Win O1 判据在 *physical intuition* 上对（Mexican-hat + U(1) + Goldstone 是教科书级 SSB 场景），但作为 Day 2 下午可执行判据，存在 **三处非 trivial 歧义**：

1. "Localized structures" 的算法 + 阈值未指定 → 需要补一个 concrete operational definition
2. "Gapless dispersion" 在 **overdamped + 单 stationary snapshot** 场景下严格不可测；需要替代 proxy
3. U(1) 被 source S(x,t) 显式破坏，严格 Goldstone 模**不存在**；应降级为 "pseudo-Goldstone / soft radial-vs-angular asymmetry"

若接受下文 Algorithm A+B 作为 concrete spec，O1 可在 Day 2 下午 2–3 小时内跑完。**Blocking 级别：非 blocking，但必须替换判据文字**。

---

## Judgment criteria audit

### 1. Localized structure detection — 判据含糊 [P0 修正]

Taskbook "real-space clustering on |ψ|" + "至少 3 个，size < grid/4" 无算法、无阈值、无 size 定义。严格审核：

- **"Localized" 的物理定义**：在 Mexican hat 里，若 ψ 是 vortex/soliton，|ψ|(x) 在 core 处 dip 到 0，远场趋于 v；若是 domain（相畴），|ψ| ≈ v 均匀，phase θ 分块。因此 **"|ψ| 的局部极大" 不是好 indicator**（vortex core 是极小）。应改为 **"phase coherence 的 connected patch"**。
- **"至少 3 个"**：数字 3 没有 principled 出处。保留为 qualitative heuristic。
- **"size < grid/4 = 8"**：保证 structure 不 wrap 周期 BC。物理合理 ✓
- **size 定义**：建议 **gyration radius** 而非 bounding box。

### 2. Goldstone 软模 / gapless dispersion — 定义在本系统不成立 [P0 修正]

- **Overdamped dynamics** (model A Hohenberg-Halperin)：ω(k)→0 退化为 **λ(k)→0 as k→0** (phase 扩散慢模)
- **单 snapshot 不能测 dispersion**：dispersion 需要 time FT
- **Operational 替代**: equal-time **structure factor** S_θ(k) = ⟨|θ(k)|²⟩。Goldstone 预言 S_θ(k) ∝ 1/k² as k→0（massless）; radial S_ρ(k) saturate 到 1/m_ρ²（有 gap）
- 对比 S_θ vs S_ρ 比 dispersion 更 tractable

### 3. U(1) + external S(x,t) 下的 pseudo-Goldstone

**关键漏洞**: S(x,t) 直接耦合 (a, b)，不是 U(1)-invariant 耦合（invariant 应只依赖 |ψ|² 或 Re[ψ* J]）。显式破缺 → 严格 Goldstone 失效，角向模获得 mass m_θ² ∝ ⟨|S_perp|⟩。

**修正**:
- 声明 "approximate/pseudo-Goldstone"
- Operational test: m_θ / m_ρ < 0.3 即可（不要求 m_θ=0）
- Pass 条件: **m_θ² / m_ρ² < 0.1** 或等价 **S_θ(k_min) / S_ρ(k_min) > 10**

### 4. FFT conventions — 细节需 lock

- 32³ 周期 + dx=1：k_n = 2π n/32
- **关键**：不要直接 FFT 复 ψ。应先做 **polar decomposition** ψ(x) = ρ(x) e^{iθ(x)}
- 或 cos/sin 替代避免 branch cut
- Power spectrum 分别 S_ρ(k), S_θ(k)
- Radial binning: |k| 球壳平均

---

## Concrete proposals for Day 2 implementation

### Algorithm A: Localized structures (connected-component on phase coherence)

```
1. 计算 θ(x) = angle(ψ(x))
2. Local phase-coherence order parameter:
     C(x) = | (1/|N(x)|) Σ_{y ∈ N(x)} e^{iθ(y)} |
   其中 N(x) 是 x 的 27 voxel 立方邻居
3. 阈值：T = mean(C) + 1.0·std(C)
4. Mask M = {x : C(x) > T}
5. 3D connected-component labeling (scipy.ndimage.label, 26-connectivity)
6. 对每个 component:
     - r_g = sqrt( (1/N_i) Σ |x − x_com|² )
     - 要求 r_g < 8 (= grid/4)
     - 丢弃 size < 3 voxel 的 noise
7. N_struct = 符合 (r_g < 8) 的 component 数
Pass: N_struct ≥ 3
```

**Physical motivation**: Goldstone/soliton/vortex 都表现为 **phase-coherent patch**（连续的 θ 区域）。trivial uniform ground state → C ≈ 1 everywhere → 一个 component → N_struct = 1 → 不 pass ✓

### Algorithm B: Goldstone indicator (stationary snapshot)

```
1. Polar decomp: ρ(x)=|ψ(x)|, θ(x)=angle(ψ(x))
2. 减均值: δρ = ρ − mean(ρ), δθ_c = cos(θ) − mean(cos θ), δθ_s = sin(θ) − mean(sin θ)
3. 3D FFT: δρ̂(k), δθ̂_c(k), δθ̂_s(k)
4. Radial-binned power:
     S_ρ(|k|) = ⟨|δρ̂|²⟩_{shell}
     S_θ(|k|) = ⟨|δθ̂_c|² + |δθ̂_s|²⟩_{shell}
5. 取 low-k bins (|k| ∈ [2π/32, 4·2π/32]) 的 log-log 斜率:
     S_θ(k) ~ k^{−α_θ}, S_ρ(k) ~ k^{−α_ρ}
6. Goldstone indicator:
     R = S_θ(k_min) / S_ρ(k_min)
     Δα = α_θ − α_ρ
Pass (pseudo-Goldstone): R > 5 AND α_θ > 1.0 (gapless-like scaling)
```

**Theoretical basis**: Free massless scalar S(k) = T/k² (α=2); massive S(k) = T/(k²+m²) (low-k saturate, α=0). α_θ > α_ρ 即角向更 soft。R > 5 是 1σ 级信号。

### 组合 pass: O1 通过 iff (Algorithm A ≥3 structures) AND (Algorithm B R>5, α_θ>1.0)

---

## Blocking / non-blocking 分类

| Issue | Level | Action |
|---|---|---|
| Localized detection algorithm 未指定 | Non-blocking | 采用 Algorithm A |
| Dispersion 在 stationary snapshot 不可测 | Non-blocking | 替换为 Algorithm B 的 structure factor ratio |
| U(1) 被 S 显式破缺 | Non-blocking theoretical | 降级为 pseudo-Goldstone, R>5 |
| FFT convention (polar decomp first) | Non-blocking | lock 到 Algorithm B step 1-2 |
| "至少 3 个" 的 3 无原则 | Acknowledged heuristic | 保留，标注 qualitative |

**无 P0 blocking**：Day 2 下午 2-3 小时可实施。

---

## References

1. Goldstone, Salam, Weinberg, *Phys. Rev.* 127, 965 (1962) — Goldstone 定理原版
2. Hohenberg & Halperin, *Rev. Mod. Phys.* 49, 435 (1977) — Model A overdamped λ(k) = Γ k²
3. Chaikin & Lubensky, *Principles of Condensed Matter Physics* Ch. 6-8 — SSB + structure factor S(k) ∝ 1/k²
4. Zurek, *Phys. Rep.* 276, 177 (1996) — defect detection via phase coherence
5. Watanabe, *Ann. Rev. Cond. Mat. Phys.* 11, 169 (2020) — Goldstone in non-relativistic
