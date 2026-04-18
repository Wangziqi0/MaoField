# Action 3 P3 wavefront 诊断 + BGE DC tilt 估

**作者**: Linux Claude Action 3 algo-verify subagent (Opus 4.7 xhigh), dispatch 2026-04-18
**任务**: 对 A2 审查 catch 的 Kramers factor 10⁴ anomaly 做两条低成本 route 诊断 — wavefront (路线 A) + BGE DC tilt (路线 C)
**诚实度**: 数据驱动, 不 inflate; verdict 见 §3

---

## 0. 数据 location verify

Phase B Exp 1 (σ=0 deterministic, 不含 Langevin trajectory) 对本任务无帮助。σ=0.5 Langevin 的 raw data 在 `block4_5/b1_langevin/s0.5_states.bin` (5.24 MB, **仅最终 state, 无 trajectory**)。

→ 决策: **重跑 1 doc σ=0.5 Langevin in Python with per-voxel t_cross tracking**。可复现 Rust engine 数学 (同样 dt, steps, seed 家族, BGE source tile+smooth+normalize, A1 原势 `V=u(u-1)²(u-4)²`, init `|ψ|=1.0±0.3`)。1 doc ~12s, 多 doc cross-validate ~40s 总。脚本: `action3_wavefront/wavefront_diag.py`, `wavefront_diag_deep.py`, `sigma_scan_v2.py`, `source_whitening_test.py`, `tilt_estimate.py`。

Python 重跑 reproduce 原 Rust 实验数字 (85% u<0.5 at t=250 → Python 87% u<0.5, 7pp 容差内, OK)。

---

## 1. 路线 A: Wavefront 诊断

### 1.1 setup + t_cross 计算

`[DYNAMIC-RARE-EVENT] → [DYNAMIC-DIFFUSIVE]` (mode tag 被数据重新归类)

- Grid: 32³ = 32768 voxels
- Langevin: γ·dψ/dt = D·∇²ψ − F(u)·ψ + S + η, σ=0.5, dt=0.05, 5000 steps → t_sim=250
- Inner saddle at u=0.2597, V=2.013 above u=1 well
- Crossing criterion: `t_cross(x) = min{step: u(x, step) < 0.5}` (0.5 是 u=1 well 和 inner saddle 中点, 兼容 A1 verdict 中 "85% u=0" 定义的 fraction)

3 doc 跨 seed 1000/1017/1034 cross-validate 全部 reproduce: 100% crossed at t_sim=50 (step 1000), median t_cross ≈ 10 steps, Avrami n ≈ 0.85 (std 0.009 across docs).

### 1.2 C_s(r) 空间相关

Spatial correlation of crossing events:
```
C_s(r) = ⟨1[|t_cross(x_i) − t_cross(x_j)| < Δt_thresh]⟩ | |x_i − x_j| = r
```

预测:
- **Independent Poisson**: C_s 近恒定, 不依赖 r (P(both cross within Δt) ≈ Δt/t_total, same at all r)
- **Wavefront**: C_s ∝ exp(−r/ξ_wave) 或 step at wall velocity · Δt_thresh (邻近 voxel 高度相关, 远距低相关)

**观察** (500k-1M pairs, bin width 1.0 voxel, Δt ∈ {1,2,3,5,10,20,50} steps):

| r (voxel) | C_s(Δt=1step) | C_s(Δt=5step) | C_s(Δt=20step) | C_s(Δt=50step) |
|---|---|---|---|---|
| 1.5 (nearest) | 0.054 | 0.244 | 0.700 | 0.950 |
| 4.5 | 0.057 | 0.261 | 0.687 | 0.949 |
| 8.5 | 0.053 | 0.256 | 0.709 | 0.950 |
| 16.5 (opposite) | 0.055 | 0.255 | 0.699 | 0.948 |

**C_s(r) 在所有 r ∈ [1.5, 16.5] voxel 上保持平坦** (相对变异 < 5%), 跨所有 Δt_thresh. 数值本身只反映 random pair overlap 在 time window 内的概率 (≈ Δt_thresh / t_total_dispersion, 确实 ~0.055 at Δt=1, ~0.25 at Δt=5).

**Verdict (1.2)**: **nearest-neighbor 和 opposite-corner 的 C_s 无差异**。**非 wavefront**。domain wall propagation 会给 r=1.5 显著高于 r=16.5 (wall 传 1 step 最多几 voxel), 观察到的完全平坦 → rejects wavefront.

### 1.3 N_crossed(t) Avrami fit

```
N_crossed(t) / N_total = 1 − exp(−(t/τ)^n)
```
- n ≈ 1: independent Poisson process
- n = 2-3: 1D-2D wall sweep
- n ≈ 3-4: 3D Allen-Cahn wall sweep (homogeneous nucleation + growth)

Fit (3 doc, skip f<5% and f>95%):

| Doc | Avrami n | τ (time unit) | R² |
|---|---|---|---|
| MED-961 | 0.840 | 0.675 | 0.9962 |
| MED-952 | 0.862 | 0.677 | 0.9962 |
| MED-942 | 0.848 | 0.676 | 0.9967 |

**Mean n = 0.850 ± 0.009** (across 3 independent seeds). **很接近 n=1 (independent Poisson)**, 远 < n=3 (3D wavefront).

τ ≈ 0.68 time units → 50% crossing 在 **0.68 time units** (13 steps) 内发生, 不是 250 time units。

### 1.4 wavefront vs independent verdict

**Verdict (路线 A)**: **NOT wavefront**.

- C_s(r) 平坦 (no spatial decay) — rejects wall propagation
- Avrami n ≈ 0.85 ≈ 1 — rejects 3D growth kinetics, consistent with independent Poisson
- **但是**: "independent" 不是 Kramers 意义上的 "rare-event independence", 而是 **voxel-local diffusion independence** (每 voxel 各自 diffuse 过 shallow barrier, 几乎 non-interacting)

---

## 2. 路线 C: BGE DC tilt 量级估

### 2.1 数字 input

| 量 | 值 | 来源 |
|---|---|---|
| ⟨S_b⟩ (raw 512-dim 级, 70 docs) | −1.48×10⁻³ | arXiv §4.9.3 Axis A |
| ⟨S_a⟩ (raw) | +5×10⁻⁵ | §4.9.3 |
| T_eff = σ²/2 (γ=1) | 0.125 | §4.8 |
| σ | 0.5 | §4.9 |
| ΔV (inner: u=1 → u=0.2597 saddle) | 2.013 | b1_verdict §barrier table |
| ΔV/T_eff | 16.10 | §4.9 |
| d_barrier (u-space, u=1 → u=0.2597) | 0.7403 | 几何 |
| u=1 well 处 typical |b| (init, $b \in [-0.3, 0.3]$ uniform) | 0.3 | init_u_nonzero |
| ⟨S_b⟩_voxel **post tile+smooth+normalize** (5 doc avg) | −0.101 | 本实验计算 |
| mean(|S_b|)_voxel post-normalize | 0.28 | 本实验 |

**注意**: `build_source_from_emb` 在 Rust engine 做 tile+smooth+max-normalize, 所以 per-voxel S_b 被放大 ~67× (|Sb|_raw ~ 1.5e-3 → post-normalize mean |Sb|_voxel ~ 0.1). 真实 tilt 用 post-normalize 值算 (否则严重低估 tilt)。A2 审稿给的 1.48e-3 是 raw, **应该用 post-normalize 数字**算 F_tilt。

### 2.2 F_tilt 计算 (严格处理)

Source 进入 equations of motion 是 `γ·dψ/dt ← S` 直接加到 ψ:
```
γ·∂_t a = D·∇²a − F(u)·a + S_a + η_a
γ·∂_t b = D·∇²b − F(u)·b + S_b + η_b
```
沿 u = a² + b² reaction coordinate:
```
du/dt = 2a·(∂_t a) + 2b·(∂_t b)
      = 2a·(D∇²a − F(u)a + S_a + η_a) + 2b·(... + S_b + η_b)
```

Source tilt 对 u-方向的贡献: **2a·⟨S_a⟩ + 2b·⟨S_b⟩**. 在 u=1 well (typical a~1, |b|~0.3 at init):
```
F_tilt(u-direction) = 2·1.0·5e-5 + 2·0.3·(−0.101) = 1.0e-4 − 6.06e-2 ≈ −6.05×10⁻² per time unit
```

即使如此 DC force, 从 u=1 to saddle u=0.26 的能量 "降低" 只有:
```
ΔV_tilt = |F_tilt| · d_barrier = 6.05e-2 × 0.7403 = 4.48×10⁻²
```

### 2.3 Boltzmann ratio (tilted-Kramers)

```
ratio = exp(−ΔV_eff/T_eff) / exp(−ΔV/T_eff) = exp(ΔV_tilt/T_eff)
      = exp(4.48×10⁻² / 0.125) = exp(0.358) ≈ 1.43
```

**要到 ratio = 10⁴ 需要**:
```
F_tilt · d_barrier / T_eff = ln(10⁴) = 9.21
F_tilt · d_barrier = 1.151
F_tilt = 1.55 per time unit  (with d_barrier = 0.74)
```
观察 F_tilt ≈ 0.06, **差 ~26×** — 单独 tilt 无法 explain 10⁴.

### 2.4 BGE tilt alone 是否解释 10⁴: **完全无法** (ratio ≈ 1.4, 差 ~10³×)

**重要对照** (源场 whitening test, `source_whitening_test.py`):

| Source | σ=0.5 t_50 (steps) | final u<0.5 fraction |
|---|---|---|
| Original BGE raw | 10 | 0.857 |
| **Whitened (mean=0)** | **10** | **0.864** |
| Zero source | 10 | 0.951 |

**移除 DC tilt 完全不改变 crossing rate**, t_50 完全一致。Zero source 反而增加 crossing (因 source 维持 ψ in u=1 well)。

→ BGE DC tilt **实验上证明不是 crossing driver**.

---

## 3. 组合 verdict

### 3.1 Scenario 判定

按 dispatch 表格:

| Scenario | Wavefront | BGE tilt |
|---|---|---|
| 观察 | Avrami n ≈ 0.85, C_s(r) 平坦 **→ NOT wavefront** | ratio = 1.43, whitening test 证明不是 driver **→ NOT tilt** |

落入 dispatch 第 4 行 "**都不够**"。

### 3.2 问题的真实根源: Kramers formula inapplicable in this regime

**不是 dispatch 预想的 scenarios 中任何一条**。通过 σ-scan 诊断 (5 σ 值, `sigma_scan_v2.py`):

| σ | T_eff | ΔV/T | Kramers t_half_1 | 观察 t_50 | 比值 |
|---|---|---|---|---|---|
| 0.3 | 0.045 | 44.73 | 5.5×10¹⁸ | 3.35 | 1.6×10¹⁸ |
| 0.4 | 0.080 | 25.16 | 1.7×10¹⁰ | 0.95 | 1.8×10¹⁰ |
| 0.5 | 0.125 | 16.10 | 2.0×10⁶ | 0.50 | 4.0×10⁶ |
| 0.6 | 0.180 | 11.18 | 1.5×10⁴ | 0.30 | 4.9×10⁴ |
| 0.7 | 0.245 | 8.22 | 7.5×10² | 0.25 | 3.0×10³ |

Kramers fit `log(1/t_50) = slope/σ² + const`: slope = 0.287. Kramers 预测 slope = 2·ΔV = 4.03. **观察 slope 只有 predicted 的 7%** — log 依赖 1/σ² 的 slope 极浅, implied ΔV = 0.14 (vs true 2.013, 差 14×).

Power-law fit `1/t_50 ∝ σ^p`: p = 3.09. Pure diffusion (free random walk) 预测 p=2. 观察 p 介于 2 和 Kramers-like exp-dependence 之间, **很接近 diffusion** (稍陡因 potential 给 slight restoring).

**物理解释**:
- σ=0.5 下单步 noise 位移 `σ·√dt = 0.112` on (a,b)-space; ψ=1 处 Δu ≈ 2|ψ|·0.112 = 0.224
- 5 步 累积 diffusion Δu ≈ 0.5 (= u=1 到 u=0.5 的距离)
- 观察 median t_cross = 10 steps (只 2× pure-diffusion 慢, 势阱 restoring 效应弱)
- **Crossing 不是 "barrier climb by thermal fluctuation" (Kramers), 而是 "thermal diffusion across shallow quasi-degenerate wells with comparable depth and noise scale"**

Kramers formula `k = ω₀/(2π)·exp(−ΔV/T)` 的前提 (Mel'nikov-Meshkov 1986):
1. `ΔV/T ≫ 1` — 满足 (16)
2. **`t_relax ≪ t_escape`** — **violated**: t_relax ~ 1/|V''(u=1)| ~ 0.5, t_escape 观察 ~ 0.5. 相当.
3. **quadratic well approximation** — 未严格 satisfied, V(u) = u(u-1)²(u-4)² 在 u=1 处四次方多项式, V''(1)=2 but 高阶项快速 dominate

条件 2 (即 "well-separated timescales") 被 违反, 使 Kramers 式不再 applicable. 1D-Kramers prefactor 假设从深 well 出发 thermalize 到 well bottom 然后缓慢 escape — 但我们的系统 在 1 relaxation time 内直接 diffuse 过 saddle, 没有 "thermalize and wait" 阶段.

### 3.3 §4.11.1 v2 草稿

按 dispatch 第 4 行 "都不够 → remains open methodological question, 但**更精确命名 root cause**":

> **§4.11.1 v2 草稿 (Linux Action 3 建议, 诚实下调 not upgrade)**
>
> "The ~10⁴ factor between observed inner-barrier crossing fraction (0.85 at σ=0.5, t_sim=250) and the 1D-Kramers prediction (9.5×10⁻⁵ per voxel) is attributable not to collective field-theoretic corrections or coherent source driving, but to the **inapplicability of the 1D-Kramers formula itself in this parameter regime**.
>
> Two diagnostic tests (Action 3, 2026-04-18) rule out the two leading candidate mechanisms:
>
> (i) **Wavefront propagation rejected**: spatial correlation C_s(r) of crossing events is flat over r ∈ [1.5, 16.5] voxel lattice distances at all tested Δt ∈ [1, 50] steps. Avrami exponent fit gives n = 0.85 ± 0.01 across 3 independent documents (vs n=3 expected for 3D Allen-Cahn wavefront kinetics). The 85% occupancy arises from voxel-local independent crossings, not from nucleation-and-growth.
>
> (ii) **BGE DC tilt rejected**: even using the post-smooth-normalize per-voxel ⟨S_b⟩_voxel ≈ -0.10 (scaled up from the raw 1.48×10⁻³ by the max-normalization factor), the projected force on u-reaction-coordinate gives F_tilt ≈ 0.06, yielding a Boltzmann tilt ratio of only exp(F·d/T) ≈ 1.43. A direct whitening control experiment (source mean-subtracted) produces the same t_50 and within 1pp of the same final occupancy, confirming DC tilt is not the driver.
>
> (iii) **Diagnostic root cause**: σ-scan (σ∈{0.3,0.4,0.5,0.6,0.7}) of time-to-50%-crossing fits a power law 1/t_50 ∝ σ^3.09, inconsistent with Kramers exponential dependence on 1/σ² (implied ΔV from Kramers fit = 0.14 vs true 2.013; Kramers-slope fit R²=0.99 but the *implied physical ΔV is 14× too small*). At σ=0.5, single-step noise displacement σ√dt = 0.112 produces Δu ≈ 0.22 on the reaction coordinate per step; in 5-10 steps, cumulative diffusion displacement spans the u=1 → u=0.5 barrier distance. The relaxation time t_relax ~ 1/|V''(u=1)| ≈ 0.5 is comparable to the observed escape time t_escape ≈ 0.5; the *separation-of-timescales* prerequisite for 1D-Kramers validity (Mel'nikov-Meshkov 1986, Hänggi-Talkner-Borkovec 1990 review) is violated.
>
> This regime is better characterized as **shallow-barrier, high-diffusion limit** where the barrier provides only a 2× slowdown over pure free diffusion, not as activated rare-event escape. The 10⁴ 'anomaly' is artefact of **applying an inapplicable formula**; the actual observed rate matches diffusion-dominated escape with mild potential correction.
>
> Consequence for the paradigm: no Kramers-based analysis is quantitatively reliable at σ ≥ 0.3 with this V. Reliable Kramers regime requires ΔV/T ≳ 5 AND t_relax ≪ t_escape; we satisfy the first but not the second, rendering the prediction void. This does not affect the *outer* barrier (ΔV/T = 105) qualitative unreachability conclusion (§4.9), where both conditions hold in the opposite direction and crossing is genuinely rare."

### 3.4 §4.11.1 与 dispatch scenarios 对照

| Dispatch scenario | 判定 |
|---|---|
| Wavefront 主导 | **Rejected** (Avrami, C_s(r)) |
| BGE tilt 主导 | **Rejected** (whitening test) |
| Mixed (both partial) | **Rejected** (两 mechanism 都被 control experiment 排除) |
| **都不够 → open methodological question** | **√ 这条, 但 root cause 被精确 identified**: Kramers formula inapplicable due to violated timescale separation (t_relax ~ t_escape) |

---

## 4. Python script + 可复现命令

所有脚本在 `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/action3_wavefront/`:

```
wavefront_diag.py         — 主 Langevin repro + t_cross tracking + C_s(r) + Avrami
wavefront_diag_deep.py    — 3 doc repro + finer Δt + pure-noise control
sigma_scan_v2.py          — σ∈{0.1..0.7} scan, t_50 → Kramers vs power-law fit
source_whitening_test.py  — original vs whitened vs zero source, σ=0 也测
tilt_estimate.py          — 路线 C 数字: F_tilt, ratio, BGE DC tilt alone 不够
```

**一键复现**:
```bash
cd /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/action3_wavefront
python3 wavefront_diag.py        # ~12s, generates wavefront_doc0.npz
python3 wavefront_diag_deep.py   # ~30s
python3 sigma_scan_v2.py         # ~15s, generates sigma_scan_v2.npz
python3 source_whitening_test.py # ~45s
python3 tilt_estimate.py         # ~5s
```

运行日志保存在同目录下 `run*.log`。

---

## 5. 剩余 open problems

1. **严格 Mel'nikov-Meshkov correction**: 若强行保留 Kramers, 应 apply inertial correction for moderate damping. 本系统 overdamped (γ=1, |V''|~2 → damping ratio strong), 但还需 check whether full Fokker-Planck first-passage solution matches observed t_50 quantitatively. 估计 ~4h 工作量.

2. **V 形状是否独特 inapplicable**: 三井 V=u(u−1)²(u−4)² 在 u=1 处 quadratic 但 globally quartic. 1D-Kramers 在 quadratic well + inverted quadratic saddle 严格推导. 非 quadratic 修正量级估计 (Landauer-Swanson) 约 O(1) prefactor, 不影响 4 orders of magnitude 结论.

3. **Larger σ-scan**: σ ∈ {0.05, 0.08, 0.1} 需要 跑 >10⁶ steps 看 Kramers regime 是否恢复 (σ=0.1 时 ΔV/T=400, 超 rare-event). 若跑到 σ=0.08 下仍 crossing fast → Kramers formula 彻底失效而非 marginal; 若 σ=0.08 下 crossing 变慢几个量级 → Kramers 在更低 σ 恢复 但 σ=0.5 已经 超出 applicable regime. 需 ~24h 长跑.

4. **3D → 1D reduction 问题**: 严格从 3D lattice ψ-field 到 1D u-reaction-coordinate 的投影需要积分掉所有横向 modes, 给 effective 1D 动力学. A2 审稿提的 zero-mode 贡献本是其中一部分, 但**在我们的 shallow-barrier regime, 这些修正都是 prefactor O(1), 不会改变 "Kramers inapplicable" 的定性结论**.

5. **arXiv §4.11.1 如何 update**: dispatch A5 的 3 scenarios (α保守 / β中庸 / γ激进) 需一凡 + Win 决策. 本 Action 建议走 **α保守** 路径 — 明写 "Kramers formula inapplicable due to timescale violation", 下调 "open methodological question" 变成 "known methodological artifact, does not affect outer-barrier or paradigm-level conclusions". **反 amplify**: 不用 Langer bounce 路线投入 8-12h 数值 fluctuation determinant (dispatch 路线 B), 因为即使那里能算对 ratio, 也是 quadratic well 场论, 和我们的 shallow-diffusion regime 物理无关.

---

## 6. 自检: assumption 清单

1. `[ASSUME]` U_THRESH=0.5 (u=1 well 到 u=0.2597 saddle 中点) 作 crossing 定义. 合理替代 U_THRESH ∈ [0.3, 0.7] 下 Avrami n 应 similar (检过 U_THRESH=0.5 稳定, 未做 [0.3, 0.7] scan, 承认).

2. `[ASSUME]` Python xorshift 替代为 numpy default_rng. 物理 statistics 等价 (大 N, large σ), 具体 seed-specific reproducibility 不一致但 **ensemble average reproduce 了 b1_langevin 85% u<0.5 的 observation** (Python 87%, 差 2pp 容差内).

3. `[ASSUME]` typical b = 0.3 at crossing time. 实际 b 随 σ·√(dt·steps) 增长. 在 crossing time (step ~10) b 只从 init 0.3 走到 ~0.35. 若改用 b=0.5 算 tilt, ratio = exp(F·d·(0.5/0.3)/T) = exp(0.597) = 1.82 — 仍 ≪ 10⁴. Robust.

4. `[ASSUME]` max-normalize 放大因子 ~67× 是 documented, 不 handwave. Source post-normalize 数字直接从 embedding 算出 (5 doc avg).

5. `[LIMIT]` 只跑 3 doc cross-validate, 不是 20 doc full set. 3 个跨 doc Avrami n 标准差 0.009 (1%) 表明 statistic 在 3 doc 已稳定.

6. `[LIMIT]` t_cross criterion 用 `u(x,t) < 0.5` (first passage). 若用更严格 "absorbing" (u 越过 saddle 后不返回), Avrami fit 可能 shift 但 n 定性 不变.

7. `[NOT DONE]` 未做 snapshot 可视化 (每 50 step 存 u-field 快照看 wall/cluster). 有 snapshot 数据在 `wavefront_doc0.npz` 若 Win / 一凡 要画 movie 可用. 本 Action 判定 n ≈ 0.85 + C_s(r) 平坦已足够拒绝 wavefront, 不需要额外可视化.

8. `[NOT CLAIMED]` 不声称 "Kramers formula 在所有参数域 inapplicable". 只声称 σ=0.5 + A1 potential 下 timescale 假设被违反. σ=0.1 下 t_escape 估计 ~10¹⁷⁵ time unit (Kramers), Kramers 可能真正 applicable 但不在我们 accessible 计算 horizon (此处无法 empirically verify, 只能按 theory 外推).

---

## 7. 04-20 exec summary (3 句)

1. **Wavefront 否定**: σ=0.5 A1-potential Langevin 下 C_s(r) 在 r∈[1.5, 16.5] voxel 完全平坦, Avrami n=0.85±0.01 (3 doc), 跨越事件 spatially independent 而非 wall sweep; Kramers factor 10⁴ anomaly **不是 Allen-Cahn propagation** 造成.
2. **BGE DC tilt 否定**: whitening 控制实验 (mean-subtract source) 下 t_50=10 steps 不变, final occupancy 差 0.7pp; F_tilt·d/T_eff = 0.36 → ratio exp(0.36)=1.43, 单独 tilt 只够 40% 修正, **差 10³**.
3. **真实 root cause 已识别**: σ-scan 拟合 1/t_50 ∝ σ^3.09 (Kramers 应 1/σ²), implied ΔV=0.14 vs true 2.013 (14× off), **1D-Kramers formula 在 σ=0.5 下 不 applicable** — 因 t_relax~t_escape ~ 0.5 time units, 违反 Mel'nikov-Meshkov timescale separation 前提. §4.11.1 **建议走 α保守 reformulation** ("Kramers methodological artifact, does not affect outer-barrier or paradigm conclusions"), 不投入 Langer bounce 数值 (A2 路线 B).

---

*— Action 3 algo-verify subagent (Opus 4.7 xhigh), 2026-04-18, ~40 min agent time*
