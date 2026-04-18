# EXPLORATION_PHASE_B_EXP1.md — 2026-04-15 Silent Block 1

## Summary

- Signal A (exp ≡ control_whiten): **resolved**. Three mechanisms conspire; dominant is a combination of hypothesis (d) — BGE S0 mean is O(10^-3) vs saturated |δS|~1.0 — and hypothesis (c) — the feedback channel is structurally mean-invariant. Fields are **not** byte-identical (per-doc ds_dt trajectories differ by up to 84%) but aggregated observables are statistically identical because mean(S0) enters only through uniform DC modes that the feedback cannot amplify.
- Signal B (O3 dt=1.0 outlier): **resolved mechanistically, theoretically suggestive**. dt=1.0 crosses both the diffusion CFL stability bound AND the middle-tick time scale, collapsing multi-scale structure. Not a clean RG fixed-point signature; more likely explicit-Euler stiffness driving the system to a degenerate homogeneous attractor.
- Signal C (multi-scale necessary for localization): **confirmed, paper-level implication**. Feedback alone saturates uniformly; block-averaging is the spatial seed that breaks translational degeneracy. Axioms 1 and 5 are coupled not independent.
- Signal D (power-law vs plateau): **genuine non-zero asymptote**, c ≈ 9.4e-7 (median), 100% of docs have c > 1e-7. Q2 verdict D (quasi-stationary) is technically correct; the slow decay is a transient superimposed on a real plateau.

---

## Signal A: exp ≡ control_whiten

### Setup recall

From `main.rs` lines 107-128: whitening subtracts the spatial mean of s0a, s0b.
From `engine.rs` line 273-274: effective source is
`S(x) = S0(x) + α · (ψ − ⟨ψ⟩) + β · δS_history`
where `δS_history` is built from `Δψ = ψ − ⟨ψ⟩` (line 258).

### Hypothesis test results

**(c) Feedback channel is structurally mean-invariant — CONFIRMED (theoretical)**

The feedback terms α·Δψ and β·δS_history are both constructed from `ψ − ⟨ψ⟩`, which is by definition zero-mean. So the feedback channel carries zero DC mode at every timestep, regardless of `⟨S0⟩`. The only place S0's mean enters the dynamics is:
1. Direct additive term in S (line 273)
2. Through ⟨ψ⟩ evolution, which then couples back into Δψ via the constraint that Δψ is mean-subtracted.

By linearity of the zero-mode sector and periodic BC, ⟨ψ⟩ obeys a closed ODE:
`d⟨ψ⟩/dt = −2⟨(|ψ|²−v²)ψ⟩ + ⟨S0⟩`
(because ∫∇²ψ = 0 and ∫Δψ = 0). The feedback α·Δψ and β·δS_history **do not enter the mean equation at all**. So ⟨S0⟩ only shifts ⟨ψ⟩; it cannot drive spatial structure.

**(d) BGE mean too small — CONFIRMED (numerical)**

Measured t=0 source_l2 difference between exp and control_whiten for 5 sample docs: ~2e-5. Since L2² differs by 2·L2·ΔL2 and L2 ≈ 0.036, we get (mean-of-S0)² ≈ 1.5e-6, i.e. |⟨S0⟩| ≈ 0.0012. Compared to saturated |S| ≈ 1.02, the mean is 0.12% of RMS. The "17σ BGE drift" is a z-score over the embedding distribution — it says mean ≠ 0 with extreme statistical significance, NOT that the mean is large in L2 terms.

**(a) Initial transient washout — PARTIAL**

Within ~1 time unit the feedback term reaches O(1) magnitude (by t=1, source_l2 jumps from 0.036 to ~0.04). So the S0 direct term becomes negligible (0.1% of total) within the first dozen steps. This is a secondary effect on top of (c) and (d).

**(b) Block-averaging removes mean — FALSE**

Block-averaging with periodic BC preserves the global mean (it's just coarse sampling of the mean). Not the mechanism. Ruled out.

### Test / Decision

Per-doc trajectories of ds_dt differ by up to 84% between exp and control_whiten (see inspection of 5 MED docs), but all aggregate observables converge to within 0.3% because differences are essentially phase noise in the same attractor. The 17σ BGE drift is real statistically but its norm contribution is tiny — feedback dynamics operate on the fluctuation field, which is shared.

**Verdict**: exp and control_whiten should indeed produce near-identical aggregate observables. The 17σ claim was a mis-framing — it documents that BGE embeddings violate one statistical test (zero-mean Gaussian null), not that the mean dominates dynamics.

### Implication for paper

**Strong positive evidence for §3.2 Axiom 4**. The framing should shift from "partial relaxation tolerates BGE drift" to "the feedback architecture is *constructively* mean-invariant: Δψ and δS_history carry no DC mode, so upstream embedding idiosyncrasies in the mean channel can never drive nontrivial field dynamics". This is a much stronger claim — it's a theorem about the PDE, not an empirical robustness. Paper gain: reframe Axiom 4 as a guarantee rather than a permission.

---

## Signal B: O3 dt=1.0 outlier

### Two candidate explanations

**(1) Explicit-Euler stability failure (more likely primary cause)**

Diffusion term on a unit-spacing lattice: stable Euler step requires `dt · D · (2d) < 1`, i.e. `dt < 1/(6·0.1) ≈ 1.67` in 3D. At dt=1.0 we're at ~60% of CFL; borderline but not over. However, the potential term `−2(|ψ|²−v²)·ψ` has effective stiffness ≈ 4v² = 4 when |ψ|² ≈ v². Stability of the combined step requires `dt · (6D + 4v²) < 2` → `dt < 2/4.6 ≈ 0.43`. At dt=1.0 we are **well above** this bound. The clamp at |ψ| ≤ 3 (engine.rs line 80) prevents blow-up but the dynamics degenerate into clamp-dominated bang-bang oscillation → no scale structure survives, η → 0.

**(2) Middle-tick cutoff coincidence (weaker)**

`middle_every × dt_inner_baseline = 10 × 0.01 = 0.1`. Extending this as "RG cutoff above which self-similarity breaks" is seductive but the RG analogy is imperfect here: in a genuine RG flow, exceeding the cutoff would produce a different but still scale-invariant coarse theory, not eta → 0. Observed behavior (scaling *eliminated*) is more consistent with numerical pathology than RG fixed-point crossing.

### Test / Decision

The log-log Pearson between dt=1.0 and dt=0.01 is 0.98 — waveforms still correlated — because the spatial pattern of `|ψ|²` is dictated by the clamped attractor, which inherits large-scale features from S. But the scaling exponent collapses because the fine-scale structure is wiped by the clamp. This is stiffness + saturation, not RG.

**Recommendation**: in O3 writeup, label dt=1.0 as "beyond explicit-Euler stability for potential term" and restrict the scaling-collapse verdict to dt ∈ {0.01, 0.1} where stability holds. η=0.30 vs η=0.31 is an excellent 3% spread — this is the real O3 pass within the stability window.

### Implication for paper

Do not claim "RG fixed point holds across all dt". Claim: "within stable integration range, scaling exponent is dt-invariant to 3%" (a narrower, defensible statement). Mention the stability bound explicitly. [?] A future Exp could try an implicit or IMEX integrator at dt=1.0 to disentangle numerical from physical cutoff.

---

## Signal C: multi-scale necessary for localized structure

### Observation

- control_single: feedback on, block-averaging off → mean|ψ|² = 1.02 (near bare v²=1), N_struct = 0, final free energy −2403
- exp: feedback on, block-averaging on → mean|ψ|² = 1.42 (42% above v²), N_struct = 49.8, final free energy −36305 (15× deeper)

### Mechanism

Block-averaging creates **piecewise-constant S on 2³ blocks** (16³ = 4096 macro-cells on 32³ lattice). This is an explicit spatial symmetry-breaking pattern frozen into S. Once S has block structure, the gradient-flow attractor for ψ inherits that structure as local |ψ| wells at block boundaries. Without block structure, S is smooth (3x smoothing kernel, line 116-117) and the system relaxes to a near-uniform minimum of V with small fluctuations around |ψ|=v.

Critically, the α·Δψ feedback cannot break translational symmetry by itself: it is spatially symmetric in its coupling and only reinforces existing modulations. Block-averaging plays the role of a **symmetry-breaking field** at the 2-cell scale. Once domains nucleate there, feedback amplifies. Without the seed, nothing breaks.

### Test / Decision

This is the structure-formation analog of the classic "you need an asymmetry to grow asymmetry" principle. The 15× deepening of free energy and 42% |ψ|² amplification confirm the multi-scale mode enters a completely different free-energy basin. control_single does NOT enter this basin because the only available broken-symmetry seed (thermal fluctuation from init_psi_near_minimum) is too small (init amplitude 0.1).

### Implication for paper

**Axioms 1 (field excitation = particle) and 5 (multi-scale synchronization) are not independent — they are a coupled proposition**: particle-like localized excitations *exist* in this model only because multi-scale coarse-graining breaks translational symmetry. Reframe as:

> "Localized excitations emerge iff the source admits a scale-separated coarse structure; in that case, feedback amplifies block-scale seeds into coherent domains."

This actually *strengthens* the philosophical story: it operationalizes "quantitative → qualitative" transition as a function of spatial RG depth. Paper should merge Axiom 1 narrative with Axiom 5 evidence into a single section "From scale separation to localization".

---

## Signal D: dS/dt power-law vs plateau

### Fits on extended trajectory (t=30–200, 101 points, 70 docs)

- Two-parameter pure power law `dS/dt = A·t^(-α)` on t≥50: **median α = 0.61**
- Three-parameter `dS/dt = c + A·t^(-α)` on t≥30: **median c = 9.4e-7, median α = 1.20**
- 100% of docs have fitted c > 1e-7; 30% have c > 1e-6

### Interpretation

A pure power law with α = 0.61 is unphysically slow for a dissipative system (no known universality class predicts it on 3D lattice). The `c + A·t^(-α)` fit with α ≈ 1.2 is much more natural: it is consistent with transient relaxation toward a true **non-equilibrium steady state**. The asymptotic c ≈ 1e-6 represents genuine continuous entropy production sustained by the open source S0 (which continuously injects energy through the feedback channel).

The exponent α ≈ 1 to 1.5 is consistent with generic dissipative relaxation to a driven steady state (e.g., O(N) model with random field). Not a universal class but plausible.

Last 5 extended points (t=200 single-doc): 2.905e-6 → 2.827e-6 (2.7% decay over last 1% of trajectory). At this rate, decay time constant is ~4000 units, so we're seeing a genuine slow approach to a plateau at c ~ 9e-7, not ongoing decay to zero.

### Test / Decision

Q2 verdict **D (quasi-stationary) is correct**. The system is in a true NESS, not approaching equilibrium. The naming "plateau" is slightly loose — more precisely, it is a slowly-decaying transient on top of a non-zero asymptote.

### Implication for paper

Use language: "quasi-stationary NESS with residual dissipation ~10^-6 relative to initial transient 10^-1 (5 orders of magnitude suppressed)". This is much stronger than "plateau": it claims an *open-system fixed point*, which is exactly the dialectical-materialist prediction (contradiction persists at reduced intensity, never vanishes).

---

## Synthesis: 5 Wins × Yifan's 5 Axioms

| Win | Axiom | Evidence status | New framing |
|---|---|---|---|
| W1 partial relaxation | A4 | confirmed but **reframed**: not robustness, it's structural mean-invariance of feedback channel | Theorem-level guarantee (Signal A) |
| W2 feedback closes loop | A2 contradiction | confirmed (null has no NESS, exp has c > 0) | Signal D asymptote is direct evidence |
| W3 scaling/RG | A5 multi-scale | confirmed in dt-stable window (Signal B) | narrow claim: "scale-invariant within CFL" |
| W4 localized structures | A1 particle = excitation | confirmed but **coupled to W3/A5** (Signal C) | Axioms 1+5 merge; localization requires scale-separated seed |
| W5 open NESS | A3 becoming | confirmed (Signal D: c ≈ 9e-7, genuine asymptote) | 5-order-of-magnitude dissipation suppression |

**Re-ranking**: 
1. Signal A promotes W1 from "robustness observation" to "architectural theorem" — biggest paper upgrade.
2. Signal C demotes A1's independence but strengthens the combined A1+A5 claim.
3. Signals B and D are quantitative refinements of existing claims.

---

## Recommendations for Day 3 verdict language

- **Q1 (Axiom 4 partial relaxation)**: "Self-feedback architecture is constructively mean-invariant; upstream embedding mean drift cannot enter the PDE through the feedback channel (proven from Δψ zero-mode identity). Empirical exp ≡ control_whiten matches this theorem to 0.3% in all aggregate observables."
- **Q2 (quasi-stationarity)**: "Verdict D. Extended trajectory admits asymptote fit dS/dt = c + A·t^(-1.2) with c ≈ 10^-6 > 0 on 100% of docs, consistent with open-system NESS."
- **Q3 (O1 localized structures)**: "Confirmed, **coupled to multi-scale mode**. Without block-averaging seed (control_single), feedback alone produces uniform saturation. Report Axioms 1 and 5 as conjoined."
- **Q4 (O3 scaling)**: "Scaling exponent η = 0.30 ± 0.01 across dt ∈ {0.01, 0.1} (log-log Pearson > 0.9999). dt = 1.0 is beyond explicit-Euler stability for the potential term (bound dt ≲ 0.43); its η ≈ 0 is a numerical artifact, not a physical cutoff. Restrict scaling claim to stable window."
- **Caveat to surface**: Axioms 1 and 5 are empirically coupled in this model. Honest narrative acknowledges this coupling as a feature (operationalizing quantitative→qualitative transition) rather than hiding it.

## Open items [?]

- Whether an implicit integrator at dt=1.0 would restore scaling (would distinguish numerical vs RG cutoff).
- Whether the α ≈ 1.2 decay exponent matches any known universality class; parameter sweep needed.
- Whether Signal C survives at different block sizes (block=4, block=8) — would test if multi-scale seed is parameter-robust or a knife-edge.
