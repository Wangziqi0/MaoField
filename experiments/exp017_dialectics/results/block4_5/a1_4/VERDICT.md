# A1.4 Verdict — Shifted Potential as OP2 Diagnostic

**Authors**: Linux Claude × Win Claude (cross-reviewed by independent paper-review subagents)
**Date**: 2026-04-14
**Position**: diagnostic refinement of OP2 (Axiom 3 non-equilibrium extensions), **not** a success/failure binary on MaoField paradigm.

---

## 0. TL;DR

A1.4 shifted potential `V(u) = u(u−1)²(u−2)²` was proposed to test whether lowering the outer barrier from `V(saddle u=2.704)=13.187` (original A1 势) to `V(saddle u=1.540)=0.095` (A1.4 shifted) would bring the previously-unreachable outer basin (now at u=2) into Kramers-accessible range under σ=0.5 Langevin, thereby validating **OP2 (a) "barrier-topology engineering"** as a workable path.

**Finding**: A1.4 Laplace-predicted occupancy `p(0)=0.03, p(1)=0.57, p(2)=0.40` was **not recovered** under any tested σ∈{0.0, 0.1, 0.3, 0.5, 0.7} or wall configuration (λ∈{1, 10}, k=4, u_max=2.5). Observed regimes:

- σ≤0.1: **kinetically frozen** at init + deterministic drift → 85% u=2 (not Laplace)
- σ=0.3: **partial mixing** (k·t_sim≈10 for outer, insufficient ergodic) → p₁/p₂ direction **reversed** from Laplace prediction
- σ=0.5/0.7: **boundary-artifact dominated** (53%/98% voxels clamped at u=18, Kramers regime ΔV/T<1 invalid)

**Decomposition**: the failure to recover Laplace equilibrium is **not** attributable to any single cause; it is a **three-fold co-design problem** in which three independent obstructions must be addressed jointly:

1. **Source drift** — BGE embedding's imaginary component Sb has mean `−1.5×10⁻³` (`t=−17.1, p<10⁻²⁵`), violating Laplace's mean-zero source assumption. σ=0 deterministic baseline shows **66% u=2 occupancy without any noise** — init+gradient-flow drift alone suffices to break equilibrium.
2. **Potential tail geometry** — V_shifted decays as `u⁵` for `u>2`, insufficient to confine |ψ|² against Langevin noise `σ√dt=0.112` per step at σ=0.5. Simple polynomial walls V_wall=λ(u−u_max)⁴ do not cure this because k=4 is C³-smooth at the wall onset.
3. **Numerical scheme incompatibility** — explicit Euler at dt=0.05 is unstable (`dt·|J_wall| ≫ 2`) for any meaningful wall stiffness; λ=10 actively makes the problem worse (clamp residency +5.9pp vs λ=1).

**Verdict**: A1.4 reframes OP2 from a barrier-geometry single-axis problem to a **three-axis co-design** (source statistics × potential shape × integrator/BC). This is a **refinement of the open problem**, not a resolution. The reframed roadmap is Block V Phase A-1 (source bias), A-2 (potential design), A-3 (numerical scheme) in the updated `BLOCK_V_DESIGN.md`.

**Explicitly not claimed**:
- "OP2 is unreachable" (A1.4 tests one narrow path, not the solution space)
- "Allen-Cahn framework is broken" (σ=0 baseline confirms framework-internal dynamics are correct; the issue is boundary/source coupling)
- "Barrier engineering fails as a category" (it fails in **isolation**; may succeed jointly with source whitening + implicit integrator)

---

## 1. Experimental setup

### 1.1 Configuration (shared across σ-scan and walled experiments)

- Source: BGE-M3 1024-dim embeddings, tiled to 32³ grid, smoothed, max-normalized
- Documents: NFCorpus, 100 docs (70 with cached embeddings used in final stats)
- Init: `init_u_nonzero` — a ∈ [0.7, 1.3] uniform, b ∈ [−0.3, 0.3] uniform → u∈[0.49, 1.78]
- Integrator: explicit Euler, dt=0.05, steps=5000, horizon t_sim=250
- Clamp: `|a|, |b| ≤ 3.0` → u_max=18
- Potential A1.4 shifted: `V(u) = u(u−1)²(u−2)²`
- Langevin: `γ ∂_t ψ = −∂V/∂ψ* + S(x) + η(t)`, `⟨η η*⟩ = σ²δ`, effective temperature `T_eff = σ²/2` (γ=1)

### 1.2 Landscape geometry [STATIC]

Independent SymPy verification:

| Point | u | V | V''(u) |
|---|---:|---:|---:|
| min (boundary) | 0.0000 | 0.000 | — (linear `V≈4u`) |
| **saddle inner** | 0.2597 | **0.431** | −8.25 |
| min | 1.0000 | 0.000 | +2.00 |
| **saddle outer** | 1.5403 | **0.095** | −1.59 |
| min | 2.0000 | 0.000 | +4.00 |

Asymmetry ratio: `0.431 / 0.095 = 4.54×` (inner > outer, **reversed** from A1 original where ratio was 6.55× outer > inner).

### 1.3 Analytical predictions [DYNAMIC-EQUILIBRIUM]

Laplace partition functions (Boltzmann approximation, valid when thermalized):
- `Z_0 = T/4` (linear boundary basin, V≈4u)
- `Z_1 = √(2πT/2)` (quadratic minimum)
- `Z_2 = √(2πT/4)` (quadratic minimum)

At σ=0.5 (T=0.125): p(0)≈0.028, p(1)≈0.569, p(2)≈0.402. Prediction ratio `p(1)/p(2) = √(V''(2)/V''(1)) = √2 ≈ 1.414` (u=1 basin **wider** → more populated; independent (a,b)∈ℝ² rejection-sampling of 4×10⁶ points confirms this ratio at all σ).

---

## 2. Phase 2 + 2.5 data

### 2.1 σ-scan [4 σ values, + σ=0 deterministic baseline]

| σ | T_eff | u_max | u_mean | p(u=0) | p(u=1) | **p(u=2)** | **p(clamped)** | p(mid) | phase ⟨R⟩ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **0.0** | — | 2.13 | 1.72 | 0.000 | 0.340 | **0.660** | 0.000 | 0.000 | — |
| 0.1 | 0.005 | 2.41 | 1.88 | 0.000 | 0.146 | **0.853** | 0.000 | 0.001 | 0.190 |
| 0.3 | 0.045 | 18.00 | 1.61 | 0.012 | 0.363 | **0.408** | 0.004 | 0.212 | 0.184 |
| 0.5 | 0.125 | 18.00 | 9.90 | 0.054 | 0.246 | 0.041 | **0.525** | 0.134 | 0.053 |
| 0.7 | 0.245 | 18.00 | 17.65 | 0.003 | 0.008 | 0.001 | **0.979** | 0.008 | 0.003 |
| — **Laplace** | | | | 0.028 | **0.569** | **0.402** | 0 | 0 | — |

### 2.2 Walled (V_wall = λ·max(0, u−2.5)⁴, k=4)

| λ | σ | u_mean | p(u=1) | p(u=2) | **p(clamped)** | p(>2.5) | Δ vs no-wall (clamp) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.5 | 10.04 | 0.242 | 0.040 | **0.534** | 0.535 | +0.9pp (null) |
| 10 | 0.5 | 11.04 | 0.209 | 0.031 | **0.593** | 0.594 | **+6.8pp (worse)** |
| 1 | 0.3 (control) | 1.62 | 0.363 | 0.407 | 0.005 | 0.008 | +0.1pp (null, wall inactive) |

### 2.3 Baseline observations

**BGE source statistical bias** (independent t-test on 70 docs, per-doc mean of 512 Sb components before normalization):
- `mean(Sb) = −1.48×10⁻³, std=7.2×10⁻⁴, t=−17.12, p<10⁻²⁵`
- `mean(Sa) = 5×10⁻⁵, p=0.54` (consistent with zero)
- **Sb has statistically extreme non-zero mean; Sa is mean-zero**

**σ=0 deterministic (no Langevin)**:
- `u_max=2.13, u_mean=1.72`
- `p(u=1) = 0.340, p(u=2) = 0.660, p(clamped) = 0`
- **init+gradient+source drift alone produces 66% u=2** (vs Laplace prediction 0.40)

### 2.4 Kramers escape rates × horizon (independent computation)

| σ | T | `k_{1→2}·t_sim` | `k_{2→1}·t_sim` | `k_{1→0}·t_sim` | ΔV/T outer | ΔV/T inner | Regime |
|---|---:|---:|---:|---:|---:|---:|---|
| 0.1 | 0.005 | 4.0×10⁻⁷ | 5.6×10⁻⁷ | 5.9×10⁻³⁶ | 19.0 | 86.2 | **frozen** (both valid, no crossings) |
| 0.3 | 0.045 | 8.6 | 12.2 | 1.1×10⁻² | 2.1 | 9.6 | outer marginal, inner valid; **partial mixing** |
| 0.5 | 0.125 | 33.2† | 46.9† | 5.1† | 0.76 | 3.45 | outer **Kramers invalid**, inner marginal |
| 0.7 | 0.245 | 48.2† | 68.1† | 27.8† | 0.39 | 1.76 | both invalid; **Kramers breakdown** |

† rate values shown for reference; `ΔV/T < 5` renders standard Kramers formula inaccurate (prefactor uncertainty 2-3×) or invalid (ΔV/T<1, requires Mel'nikov-Meshkov correction).

Kramers formula `k = √(V''_min·|V''_saddle|)/(2πγ) · exp(−ΔV/T)` applicable only when `ΔV/T ≫ 1` (typically ≥ 5).

---

## 3. Three-fold co-design diagnosis

### 3.1 Axis A: Source statistics [DYNAMIC-IMPLEMENTATION]

**Evidence**:
- σ=0 deterministic produces 66% u=2 (Laplace predicts 40%): a **26pp gap** with no noise contribution possible
- BGE Sb t=−17.1 (p<10⁻²⁵): statistically ruled out as mean-zero

**Mechanism**: BGE embeddings are learned from MLM-style objectives optimizing distributional properties of token co-occurrence, with no constraint on the mean of individual dimensions. When such an embedding is used directly as PDE source term `S(x)` in `γ ∂_t ψ = −∂V/∂ψ* + S(x) + η`, the non-gradient component of S (Helmholtz-decomposition solenoidal part) produces persistent probability current in Fokker-Planck steady state. A **nonzero global mean** `⟨S⟩ ≠ 0` is one diagnostic — it guarantees that S cannot be written as `∇φ` of a single-valued potential with matching mean, so standard Boltzmann form `ρ ∝ exp(−V/T)` fails. Our BGE source violates `⟨Sb⟩=0` by 17σ (stronger test of non-gradient character would decompose S via Hodge or compute `∮ S·dl` on test loops; deferred to Block V Phase A-1).

**Cumulative forcing vs barrier scale**: with `|S| ~ O(0.1)` after smoothing + max-normalization, cumulative forcing over horizon `|S|·t_sim ~ 0.1 · 250 = 25`, **far exceeding** the outer saddle ΔV=0.095 in A1.4. Hence deterministic source-pull across the outer saddle is energetically available even at σ=0, confirming the σ=0 baseline observation (66% u=2).

Laplace equilibrium derivation assumes detailed balance, i.e. the full force `−∇V + S` is gradient. Our source violates this irrespective of how one interprets the mean.

**Implication**: any barrier-geometry experiment without source mean-subtraction / whitening is confounded by this drift. A1.4's failure to hit Laplace is **partially caused by source drift**, not solely by potential shape.

### 3.2 Axis B: Potential tail geometry [STATIC]

**Evidence**:
- Shifted V scales as `u⁵` for u≫2 (`V(u=3)=12, V(u=4)=144, V(u=10)=52000`)
- Compare A1 original `u⁹` (V(u=3)=48, V(u=10)=5×10⁵) — one polynomial order shallower
- Noise step at σ=0.5: `σ√dt = 0.112` on (a,b); displacement of u per step ≈ `2|ψ|·0.112 ≈ 0.22` for |ψ|~1

**Mechanism**: potential tail must provide restoring force exceeding noise-driven drift per step. `u⁵` tail in u-space (equivalently `|ψ|¹⁰` in ψ-space, two polynomial orders shallower than A1 original `|ψ|¹⁸`) satisfies this only in the regime u ~ 2–3 (force ~ 1–10); beyond, `dt·f` overshoots and explicit Euler destabilizes. Voxels that escape to u>3 enter a regime where noise σ√dt and deterministic force |V'(u)·ψ|·dt are comparable, producing random walk with weak restoring bias — eventually hitting the clamp.

Soft wall `λ(u−u_max)⁴` with `k=4` is **C³-smooth at u=u_max**, meaning wall force is identically zero at the boundary and grows cubically afterward. Voxels transit the (u_max, u_max+δ) region in O(δ/σ√dt) steps without appreciable deceleration.

**Implication**: confining |ψ|² requires either (i) higher polynomial degree in the original potential, (ii) logarithmic/exponential confinement, or (iii) discontinuous wall (reflecting BC). `k=4` soft walls are insufficient.

### 3.3 Axis C: Numerical scheme [DYNAMIC-IMPLEMENTATION]

**Evidence** (independent SymPy verification at u=10, a²=b²=5, isotropic case):
- `f_wall(u) = λ·k·(u−u_max)^{k−1} = λ·4·(7.5)³ = 1687.5·λ`
- `f'_wall(u) = λ·k(k−1)·(u−u_max)^{k−2} = 12·(7.5)² = 675·λ`
- 2×2 Jacobian block `[J11=2a²·f'+f, J12=2ab·f'; J12, J22=2b²·f'+f]`
- Spectral radius at a²=b²=5: `J_max = 2a²·f' + f + 2ab·f' = 8437.5 + 6750 = 15187.5·λ`
- **Wall Jacobian at u=10**: `J ≈ 1.5×10⁴` (λ=1) / `1.5×10⁵` (λ=10)
- Explicit Euler stability `dt·|J| < 2` → `dt_max,c1 ≈ 1.3×10⁻⁴`, `dt_max,c2 ≈ 1.3×10⁻⁵`
- Experimental dt = 0.05 → **violates stability by ~380× (c1) / ~3800× (c2)**

**Mechanism**: explicit Euler with large force gradient produces oscillatory overshoot. Without clamp, solution would diverge numerically (NaN). With clamp at ±3, the overshoot is absorbed into boundary residency. This makes the clamp statistics **integrator artifact** rather than physical steady-state.

λ=10 worse than λ=1 (53.4% → 59.3% clamped) is the **direct signature** of this effect: stiffer wall → larger J → more severe CFL violation → more clamp events, even though the wall is "supposed to" push voxels back.

**Implication**: wall treatment requires implicit or IMEX integration (wall term treated implicitly, rest explicit). Or: drop wall entirely and use reflecting boundary condition at some `|ψ|=R_max`. Or: reduce dt to `<6.7×10⁻⁵`, increasing cost 750×.

### 3.4 Axes coupling

The three axes are **not independent**: fixing any one in isolation does not restore Laplace equilibrium.

| Fix | Still fails because |
|---|---|
| Source whitening only | Potential tail still u⁵, integrator still CFL-violating at σ=0.5 |
| Potential only (deeper tail) | Source drift still breaks detailed balance; integrator stiffness worsens with deeper potential |
| Integrator only (implicit) | Source drift still 17σ non-zero; shallow tail still allows escape beyond basins |

A1.4 **cannot resolve OP2** as presented because it varies only axis B (potential shape) while leaving A and C at values that independently preclude Laplace. **Block V Phase A must address all three axes in coordinated experiments** — this is the refined OP2 roadmap in `BLOCK_V_DESIGN.md`.

---

## 4. Refinement of OP2 wording

### 4.1 Previous wording (B1-era, pre-A1.4)

> "OP2: gradient flow + isotropic Langevin fails to populate distant attractor basins. Non-equilibrium extensions (Langevin, Hamiltonian, active driving) are needed."

### 4.2 Current wording (post-A1.4)

> "OP2 (refined): populating non-gradient-connected attractor basins under finite simulation horizon requires **co-designed**:
>
> (i) **Source-field statistics** satisfying detailed-balance prerequisites (mean-zero or explicit non-equilibrium steady-state analysis);
>
> (ii) **Potential geometry** with confinement exceeding noise step size across accessible field-space domain (tail polynomial order ≥ 6 empirically; logarithmic/exponential preferable);
>
> (iii) **Numerical scheme** with stability margin for potential gradient's Lipschitz constant (implicit treatment of stiff terms, or sub-CFL dt, or reflecting BC).
>
> B1 Stage (A1 original potential, σ=0.5 Langevin) yielded two simultaneous findings under this refined lens: the inner barrier (ΔV/T=16) showed Kramers-like crossing (85% u=0 occupancy at t_sim=250); the outer barrier (ΔV/T=105) yielded Kramers escape time exceeding horizon by ~43 orders of magnitude. A1.4 Stage tested path (ii) in isolation and revealed the necessity of the co-design. Block V Phase A examines paths (i), (ii), (iii) jointly."

### 4.3 What A1.4 does **not** resolve

- A1.4 is a diagnostic for axis-coupling structure; it does not identify the thermodynamically-correct joint configuration
- A1.4 does not test whether directed (anisotropic, non-gradient) driving can bypass all three axes at once — that is OP2 path (b), deferred to V.3-H (Hamiltonian) and V.3-A (active) sub-blocks

---

## 5. Open methodological questions flagged

### 5.1 A1 inner barrier Kramers discrepancy (factor ~10⁴, i.e. ~4 orders of magnitude)

B1 Stage observed 85% u=0 occupancy at σ=0.5 on A1 original potential. Note `ΔV/T=16` is marginal for 1D Kramers validity (rule of thumb `ΔV/T ≥ 5`) but the 1D prefactor's absolute calibration in 3D lattice field theory is unverified. Kramers rate for inner barrier (ΔV=2.0, T=0.125):

`k_{1→0} = (1/(2πγ))·√(V''(1)·|V''(0.296)|) · exp(−16) ≈ 3.4·1.12×10⁻⁷ ≈ 3.8×10⁻⁷ per time unit`

Expected events at `t_sim=250`: ~`9.5×10⁻⁵` per voxel. Observed fraction having crossed: `0.85`.

**Factor ~10⁴ (i.e. ~4 orders of magnitude)** between prediction and observation — a significant quantitative gap but **not** a 10^10000 discrepancy.

Possible explanations:
- 1D Kramers prefactor underestimates escape rate in 3D field-theoretic setting (collective voxel interactions)
- Boundary basin (u=0) has linear-V attractor (`V ≈ 4u` as u→0⁺) rather than quadratic — standard Kramers prefactor derived for quadratic wells does not apply
- `ΔV/T=16` is marginal: ratio must be ≫ 1 but the constant is not well-calibrated for our system

This is flagged as an **open methodological question** for the arXiv §4 submission: the qualitative conclusion (outer barrier unreachable at ~43 orders-of-magnitude log-gap) is robust, but quantitative rate matching for lower barriers requires further work (measure prefactor empirically from σ-scan, or derive field-theoretic Kramers analog).

Note: the Giry-monad lift connection relevant to this Kramers analysis is deferred to `lawvere_monad_draft.md`; the current verdict focuses on A1.4 empirical refinement of OP2.

### 5.2 σ=0.1 kinetic-trapped 85% u=2 (not at Laplace)

Even at very low noise (T=0.005, `k·t_sim≈10⁻⁷` in all directions), system trapped in u=2 basin. Decomposition: 12% from init overlap with BoA(u=2), remaining **73pp** from BGE source drift deterministic pull. σ=0 baseline confirms 66% u=2 without noise. **This is evidence for axis A (source drift) being the dominant failure mode for this potential, not a new obstruction**.

### 5.3 σ=0.3 Laplace direction reversal

Predicted `p(1)/p(2) = √2 = 1.41`. Observed `0.363/0.408 = 0.89` (direction reversed). Rate ratio `k_{1→2}/k_{2→1} = 0.704 ≈ 1/√2` is correct (detailed balance of rates), but reaction not completed; init bias (u>1.54 ~ 12% straight to u=2) + BGE drift together carry more into u=2 than Kramers rate can return to u=1 within horizon. **Partial mixing snapshot, not equilibrium.**

---

## 6. Updates to downstream documents

### 6.1 `FINAL_REPORT.md` §5 (OP2 status)
Update OP2 from "conjecture + Langevin failed" to "refined three-axis co-design; A1.4 falsifies single-axis barrier-engineering; Block V Phase A addresses jointly."

### 6.2 `BLOCK_V_DESIGN.md`
Expand Phase A into A-1 / A-2 / A-3 (see updated document).

### 6.3 `open_problems_followup.md` OP2 section
Promote from position-paper conjecture to structured three-axis subsidiary open problems, each with experimental sub-plan.

### 6.4 `a1_4_shifted_potential_analysis.md` v3
Already contains Kramers + Laplace double framework and `[STATIC]/[DYNAMIC-*]` mode tags. Add cross-reference to this verdict.

---

## 7. Explicitly **not** claimed

- **Not claimed**: OP2 is unsolvable. A1.4 tests one narrow path (barrier shape), not the solution space.
- **Not claimed**: MaoField paradigm is disproven. σ=0 baseline confirms gradient-flow framework internal dynamics are correct; the failure is in source-coupling and boundary.
- **Not claimed**: Langevin is the wrong non-equilibrium mechanism. Phase 2.5 shows Langevin **works** (inner barrier crossing in B1) when barrier ratio ≤ horizon-appropriate; it fails at ΔV/T≪1 due to boundary artifact, not paradigm.
- **Not claimed**: barrier engineering is categorically wrong. It is wrong **in isolation**; it may succeed jointly with source whitening + implicit integrator.
- **Not claimed**: BGE embeddings are unsuitable for MaoField. They are unsuitable **as-is for Laplace**; whitening / mean-subtraction may restore suitability.

---

## 8. Take-away

A1.4 is the most informative experiment in the exp017 campaign to date because it **fails in a decomposable way**. The decomposition identifies three orthogonal obstructions (source statistics, potential tail, numerical scheme) each with a concrete engineering remedy. The refined OP2 is not more unreachable than before — it is **more precisely scoped**.

Whether the three-axis co-design restores Laplace equilibrium is a **Block V Phase A empirical question**. Whether it is sufficient for directed non-equilibrium driving (OP2 path b) is a **Block V Phase B open question**. Neither is resolved here.

This verdict treats A1.4 as diagnostic refinement, not success/failure binary. The diagnostic value is high; the engineering value is zero (no configuration tested gives usable OP2 performance). These coexist without contradiction.

---

*References*: `REVIEW_PHASE2_5_SIGMA_SCAN.md`, `REVIEW_PHASE2_5_WALLED.md`, `a1_4_shifted_potential_analysis.md` v3, `WIN_NARRATIVE_REVIEW_20260414.md` §一.
