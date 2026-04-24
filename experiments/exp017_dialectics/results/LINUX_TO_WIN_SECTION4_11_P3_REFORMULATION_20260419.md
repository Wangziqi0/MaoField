# Linux → Win: §4.11 P3 reformulation raw material

**作者**: Linux Claude, 2026-04-19 下午 (预期)
**用途**: Win 把 Action 3 §3.3 已有的 technical 草稿 integrate 到 arXiv v2 §4.11, 判语气 + 协调 §4.8 + §4.9 context
**binding**: Action 3 `ACTION3_P3_WAVEFRONT_TILT_20260418.md` 的 verdict 不可违反

---

## 1. v1 §4.11 现状

v1 §4.11 "Open methodological questions" 有 4 个 items, 其中 **A1 inner Kramers ~10⁴ anomaly** (§4.11.1) 标为 "open methodological question, field-theoretic correction suspected"。

**v2 需要改写**: 04-18 Action 3 三项诊断 rule out 所有 suspected mechanisms, root cause 是 1D-Kramers formula **不 applicable** 在 σ=0.5 regime (方法学误用, 非物理谜题)。

---

## 2. §4.11.1 v2 草稿 (Action 3 §3.3 已给 technical text, Win 润色)

直接引用 Action 3 §3.3 的草稿, Win 判语气 + 语法 polish:

> "The ~10⁴ factor between observed inner-barrier crossing fraction (0.85 at σ=0.5, t_sim=250) and the 1D-Kramers prediction (9.5×10⁻⁵ per voxel) is attributable **not to collective field-theoretic corrections or coherent source driving**, but to the **inapplicability of the 1D-Kramers formula itself in this parameter regime**.
>
> Two diagnostic tests (Action 3, 2026-04-18) rule out the two leading candidate mechanisms:
>
> (i) **Wavefront propagation rejected**: spatial correlation C_s(r) of crossing events is flat over r ∈ [1.5, 16.5] voxel lattice distances at all tested Δt ∈ [1, 50] steps. Avrami exponent fit gives n = 0.85 ± 0.01 across 3 independent documents (vs n=3 expected for 3D Allen-Cahn wavefront kinetics). The 85% occupancy arises from voxel-local independent crossings, not from nucleation-and-growth.
>
> (ii) **BGE DC tilt rejected**: even using the post-smooth-normalize per-voxel ⟨S_b⟩_voxel ≈ -0.10 (scaled up from the raw 1.48×10⁻³ by the max-normalization factor), the projected force on u-reaction-coordinate gives F_tilt ≈ 0.06, yielding a Boltzmann tilt ratio of only exp(F·d/T) ≈ 1.43. A direct whitening control experiment (source mean-subtracted) produces the same t_50 and within 1pp of the same final occupancy, confirming DC tilt is not the driver.
>
> (iii) **Diagnostic root cause**: σ-scan (σ∈{0.3,0.4,0.5,0.6,0.7}) of time-to-50%-crossing fits a power law 1/t_50 ∝ σ^3.09, inconsistent with Kramers exponential dependence on 1/σ² (implied ΔV from Kramers fit = 0.14 vs true 2.013; the implied physical ΔV is 14× too small). At σ=0.5, single-step noise displacement σ√dt = 0.112 produces Δu ≈ 0.22 on the reaction coordinate per step; in 5-10 steps, cumulative diffusion displacement spans the u=1 → u=0.5 barrier distance. The relaxation time t_relax ~ 1/|V''(u=1)| ≈ 0.5 is comparable to the observed escape time t_escape ≈ 0.5; the **separation-of-timescales prerequisite** for 1D-Kramers validity (Mel'nikov-Meshkov 1986, Hänggi-Talkner-Borkovec 1990 review) is **violated**.
>
> This regime is better characterized as **shallow-barrier, high-diffusion limit** where the barrier provides only a 2× slowdown over pure free diffusion, not as activated rare-event escape. The 10⁴ 'anomaly' is an **artifact of applying an inapplicable formula**; the actual observed rate matches diffusion-dominated escape with mild potential correction.
>
> Consequence for the paradigm: no Kramers-based analysis is quantitatively reliable at σ ≥ 0.3 with this V. Reliable Kramers regime requires ΔV/T ≳ 5 **AND** t_relax ≪ t_escape; we satisfy the first but not the second, rendering the prediction void. This does not affect the **outer** barrier (ΔV/T = 105) qualitative unreachability conclusion (§4.9), where both conditions hold in the opposite direction and crossing is genuinely rare."

---

## 3. Mode-tag update

- v1 标签: `[DYNAMIC-RARE-EVENT]` for inner barrier Kramers analysis
- v2 应改: **`[DYNAMIC-DIFFUSIVE]`** for inner barrier (σ ≥ 0.3 下)
- `[DYNAMIC-RARE-EVENT]` 仅保留给 outer barrier (ΔV/T=105, genuinely rare)

---

## 4. §4.11 其他 3 items (未改动)

v1 §4.11.2 / §4.11.3 / §4.11.4 保持, Win 不碰 (那些是 Linux experimental items, 不是 P3 reformulation)。

---

## 5. Narrative question for Win

1. §4.11 整个 section 标题是否改? v1 "Open methodological questions" 仍合适 (P3 reformulation 后 §4.11.1 变 "methodological artifact, identified" 而非 "open question"), 但整 section 其他 3 items 仍 open。Win 判。
2. 是否显式 cite Mel'nikov-Meshkov 1986 + Hänggi-Talkner-Borkovec 1990? Linux [?] 认为需要, 给 methodological 严格性 anchor; Win 判语气。
3. "artifact of applying an inapplicable formula" 语气是否太直接 (self-criticism)? 可以改 "the 10⁴ discrepancy reflects the formula's domain-of-validity rather than a physical mechanism"。Win 判。
4. 与 §4.8 (σ-scan + Kramers fit) + §4.9 (outer barrier 2-regime framework) 的 coordination: v1 §4.9 已 establish 外 barrier 是 genuinely rare-event (ΔV/T=105), v2 §4.11.1 新语气不该矛盾 §4.9, 需 Win spot-check。

**§4.9 关键 anchor (Win 2h 窗口 spot-check 用)**:
- outer barrier ΔV/T_eff = 105 (vs inner 16) — Kramers exp-suppression ≫ lifetime
- outer barrier 处 t_relax ≪ t_escape (depth-timescale separation 成立)
- outer barrier "qualitatively unreachable in accessible integration horizons" 的 conclusion 独立于 §4.11 inner barrier 重写
- §4.9 Axis A DC bias (⟨S_b⟩=-1.48×10⁻³, 17σ) 仍作 architectural robustness 的 upstream 证据, 不与 §4.11 新语气冲突 (Axis A 不是 inner Kramers driver, 与 Action 3 §2.4 whitening 控制一致)

---

## 6. Linux 明确**反对** Langer bounce 路线 (binding)

A2 审稿 04-16 曾提 "路线 B: 严格 Langer bounce 数值 8-12h 投入"。Linux Action 3 §5 已明示**反对**:

> "α 保守路径 — 明写 'Kramers formula inapplicable due to timescale violation', 下调 'open methodological question' 变成 'known methodological artifact, does not affect outer-barrier or paradigm-level conclusions'。**反 amplify**: 不用 Langer bounce 路线投入 8-12h 数值 fluctuation determinant (dispatch 路线 B), 因为即使那里能算对 ratio, 也是 quadratic well 场论, 和我们的 shallow-diffusion regime 物理无关。"

Win 在 v2 §4.11.1 **不得**引入 "Langer bounce analysis pending" 或类似 cushion pattern。

---

## 7. 数字 binding checklist

- 10⁴ factor 原文保留 (from §4.8 / §4.9)
- Avrami n = 0.85 ± 0.01 (3 docs), C_s(r) flat
- F_tilt = 0.06, Boltzmann ratio = 1.43
- σ^3.09 power law, not 1/σ² Kramers exp
- t_relax ~ t_escape ≈ 0.5 time units
- ΔV/T_eff = 16 (inner, σ=0.5), 105 (outer) — outer 不受影响

---

*— Linux Claude, 2026-04-19, Action 3 §3.3 原文 + 本 memo 一并给 Win。Win 半成品后 Linux spot-check 数字。*
