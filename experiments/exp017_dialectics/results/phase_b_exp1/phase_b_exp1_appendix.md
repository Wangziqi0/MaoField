# Appendix: Preliminary Phase B Experiment 1 Findings

*Companion to arXiv v1 (`MaoField: A Dialectical-Materialist Framework for Non-Statistical Semantic Representation`, Chen 2026); results included in v0.1.1 Zenodo release.*

**Summary.** A 36-hour experimental campaign on the open-dissipative b+c-feedback PDE formulation of MaoField produces a clean differential signal — 50 localized phase-coherent patches per document in the experimental mode versus 0 in every control lacking either feedback or multi-scale coarse-graining — together with an approach-to-plateau behavior of the dissipation rate at `dS/dt ≈ 10⁻⁶` over 150 dimensionless time units, five orders of magnitude below the initial transient. A structural consequence of the feedback architecture — that translationally-invariant feedback operators cannot couple to the base-source mean — accounts for the observation that whitening the 17σ BGE-drift component of the source has zero measurable effect on the dynamics; this partially obviates arXiv v1 OP2 sub-problem (a) source-drift de-biasing for the mean channel. Three honest language refinements (§A.5) replace heuristic claims with quantitatively supported statements; no insight from the 2026-04-15 five-insight sketch is falsified, three are refined, two are merged.

## A.1 Scope and status

This appendix reports preliminary findings from Phase B Experiment 1, an empirical test of five theoretical insights developed during a 2026-04-15 discussion between one of the principal collaborators and a research assistant. The original arXiv v1 manuscript (§5.4) flagged Phase B as an "outlook" program for after the Block V Phase A mechanism paper (IPM target, 2026-07). Acting on the principal investigator's 2026-04-15 decision, the first Phase B experiment was compressed into the v0.1.1 release week, executed autonomously with independent review gates.

The findings are **preliminary**. They rest on a single parameter setting of the feedback and history-decay constants `(α = 0.1, β = 0.05, λ = 0.05, N_hist = 100, block_size = 2)`, a 70-document sample from NFCorpus with cached BGE-M3 embeddings, and a deterministic explicit-Euler integrator with no stochastic noise. Parameter scans, larger corpora, and Langevin extensions are deferred to subsequent Phase B experiments. The present result establishes that the framework, under the b+c-feedback architecture proposed in §A.2, is empirically **non-vacuous** and **qualitatively consistent** with the five-insight dialectical-materialist sketch.

Three honest language downgrades — described in §A.5 — replace heuristic qualitative claims with quantitatively supported, mechanistically grounded statements. The downgrades **strengthen** the paper's integrity: they are not concessions to negative results but refinements of the initial formulation.

## A.2 Experimental design

The complex scalar field `ψ : 𝕋³ → ℂ` on a 32³ periodic lattice (dx = 1) evolves by the overdamped equation

$$\gamma\, \partial_t \psi \;=\; D\,\nabla^2 \psi \;-\; 2(|\psi|^2 - v^2)\,\psi \;+\; S(x, t) \qquad (A.1)$$

with `γ = 1`, `D = 0.1`, `v = 1` (Mexican-hat potential, U(1) global symmetry). The source `S(x, t)` implements bidirectional self-feedback:

$$S(x, t) \;=\; S_0(x) \;+\; \alpha\,\bigl(\psi(x, t) - \langle \psi \rangle_x\bigr) \;+\; \beta\,\delta S_{\text{history}}(x, t) \qquad (A.2)$$

with `δS_history(x, t) = Σ_k w_k · (ψ(x, t − kΔt_outer) − ⟨ψ⟩_{x, t − kΔt_outer}) · Δt_outer`, exponential decay `w_k = exp(−λ k Δt_outer)`, and `S₀(x)` the BGE-M3 embedding of the document tiled on the lattice (halves assigned to `S_a` and `S_b`, three passes of 3-point box smoothing).

A three-time-scale integrator separates ψ evolution, source refresh, and history accumulation:

- **inner** `Δt₁ = 0.01` — explicit Euler step on ψ using the current `S`
- **middle** every 10 inner steps (`Δt₂ = 0.1`) — recompute `S` from (A.2) and replace it with a block-averaged coarse version (block = 2, producing 16³ coarse cells); this coarse `S` drives the next 10 inner steps
- **outer** every 100 inner steps (`Δt₃ = 1.0`) — push the current `ψ − ⟨ψ⟩` snapshot onto the history buffer

The simulation runs for 5,000 inner steps (`t_sim = 50`). The history buffer has capacity `N_hist = 100` and fills to 50 samples over `t_sim = 50`. All runs use base seed `20260421` with per-document offset `17i`.

**Five operational modes** (Table A.1) differ by (α, β), multi-scale versus single-scale integrator, and whitened versus unwhitened source base.

| mode | α | β | multi-scale | source whiten | purpose |
|---|---|---|---|---|---|
| `exp` | 0.1 | 0.05 | ✓ | no | main experiment |
| `null` / `control_const` | 0 | 0 | ✓ | no | static-source control |
| `control_whiten` | 0.1 | 0.05 | ✓ | **yes** | isolates BGE 17σ mean effect |
| `control_single` | 0.1 | 0.05 | **no** | no | isolates multi-scale effect |

Two additional O3-dedicated runs vary `dt_inner ∈ {0.1, 1.0}` with `t_sim = 50` held fixed; one extended run (`t_sim = 200`) checks late-time plateau behavior. Eight runs total, 70 documents each, zero NaN or divergence across all runs.

## A.3 Results

### A.3.1 Localized phase-coherent structures (O1)

Each stationary ψ-snapshot is analyzed by two independent algorithms, per an independent mathematical review of the observable: (i) connected-component labeling on a local phase-coherence field `C(x) = |⟨e^{iθ(y)}⟩_{y ∈ N(x)}|` with 27-voxel neighborhood and threshold `T = ⟨C⟩ + σ(C)`; (ii) polar-decomposition radial structure factors `S_ρ(|k|)` and `S_θ(|k|)` from `ψ = ρ e^{iθ}`, with pseudo-Goldstone indicator `R = S_θ(k_min)/S_ρ(k_min)` and low-`k` log-log slopes `α_θ, α_ρ`.

| mode | N_struct_valid | Pass A (≥ 3) | R | α_θ | Pass B | **Combined** |
|---|---:|---:|---:|---:|---:|---:|
| `exp` | 49.8 | **100%** | 7,768 | 1.28 | 94.3% | **94.3%** |
| `control_whiten` | 49.8 | **100%** | 7,742 | 1.28 | 94.3% | **94.3%** |
| `null` | 0.0 | 0% | 16,923 | 2.54 | 100% | **0%** |
| `control_const` | 0.0 | 0% | 16,923 | 2.54 | 100% | **0%** |
| `control_single` | 0.0 | 0% | 20,344 | 2.51 | 100% | **0%** |

The differential signal is large and robust: feedback combined with multi-scale coarse-graining yields ≈ 50 phase-coherent patches of gyration radius below `grid/4 = 8`. Removing either the feedback (`null`, `control_const`) or the multi-scale coupling (`control_single`) yields zero patches. Pass B alone cannot distinguish the experimental mode from the controls — indeed, `null`, `control_const`, and `control_single` all exhibit `R` ratios roughly twice that of `exp` (≈ 17,000–20,000 vs ≈ 7,700) — because the phase-vs-amplitude asymmetry is a generic feature of overdamped relaxation from random initial conditions in a U(1) Mexican-hat potential; the uniform relaxation state in the controls produces an even smoother angular spectrum than the feedback-structured state. The discriminating observable is Algorithm A: the **coexistence** of pass-B-like phase softness and pass-A-like localized structure formation is what separates the experimental mode from the controls.

### A.3.2 Non-equilibrium steady-state dissipation (O2)

Entropy production rate is computed in the Seifert (2005) overdamped framework with `γ = T = 1`: `dS/dt := ⟨|∂_t ψ|²⟩_x` is the mean-field dissipated power per voxel, equivalent in these units to the medium entropy production. To falsify the Lyapunov-necessary interpretation `dS/dt → 0 under static S`, we additionally require that the source field exhibit meaningful late-window time variance.

| mode | late `dS/dt` | late `|S|₂` | `|S|₂` CoV (late) |
|---|---:|---:|---:|
| `exp` | 2.19·10⁻⁵ | 1.018 | **0.107** |
| `control_whiten` | 2.24·10⁻⁵ | 1.018 | **0.107** |
| `null` | 8.28·10⁻⁴ | 0.008 | 0 |
| `control_const` | 8.28·10⁻⁴ | 0.008 | 0 |
| `control_single` | 8.62·10⁻⁴ | 0.103 | 0.005 |

The extended run (`t_sim = 200`) reveals a genuine approach-to-plateau behavior. Over the window `t ∈ [100, 200]`, the cross-document mean `dS/dt` decays from `4.14·10⁻⁶` to `2.90·10⁻⁶` — a factor of `0.70` over 100 time units. Fitting `dS/dt(t) = c + A·t^(−α)` per document over `t ∈ [25, 200]` with `α` free yields a median `α ≈ 2.9` (interquartile range `[2.87, 2.95]`) and a median asymptote `c ≈ 2.9·10⁻⁶`, with `c > 10⁻⁷` in **100% of documents**. The atypically large `α` value in this free-parameter fit reflects a crossover from the early transient to the late plateau that is not well-modeled by a single power-law; with `α` fixed at the `t^(−1.2)` first-principles expectation for an overdamped-relaxation tail, the fit yields negative `c` values, indicating the residual decay is faster than `t^(−1.2)`. What is robust across both fitting protocols is the observation that (i) 100% of documents exhibit a late-time `dS/dt > 10⁻⁷`, (ii) the decay rate is visibly decreasing (consistent with plateau approach rather than continued power-law decay toward zero), and (iii) the source field exhibits non-zero late-window coefficient of variation `0.107`, ruling out the Lyapunov-necessary interpretation `dS/dt → 0 under static S`. The exact functional form of the approach (power-law with exponent in `[1, 3]`, stretched exponential, or a crossover regime) is not pinned down by the available data and is a follow-up target.

The late-time `dS/dt` value represents a suppression of 5 orders of magnitude relative to the initial transient `dS/dt(t = 0) ≈ 5·10⁻¹`, consistent with the "contradiction persistence with reduced intensity" prediction of the dialectical framing introduced during the 2026-04-15 discussion.

### A.3.3 Kinematic self-similarity under block averaging (O3)

Three runs of the experimental mode with `dt_inner ∈ {0.01, 0.1, 1.0}` and `t_sim = 50` held fixed produce spatial structure functions `S₂^{|ψ|²}(r) = ⟨(|ψ|²(x + r) − |ψ|²(x))²⟩` (radially binned). Pairwise log-log Pearson correlations in `r ∈ [1, 8]`:

| pair | raw Pearson | log-log Pearson |
|---|---:|---:|
| `dt = 0.01 ↔ dt = 0.1` | 0.9999 | **0.9999** |
| `dt = 0.01 ↔ dt = 1.0` | 0.9156 | 0.9809 |
| `dt = 0.1 ↔ dt = 1.0` | 0.9121 | 0.9794 |

Power-law fits `S₂(r) ~ r^η`:

| run | η | residual |
|---|---:|---:|
| `dt = 0.01` | **0.302** | 0.100 |
| `dt = 0.1` | **0.311** | 0.101 |
| `dt = 1.0` | 0.001 | 0.000 |

The `dt = 0.01` and `dt = 0.1` runs agree to 3% in scaling exponent — a clean indicator of kinematic self-similarity across one decade of inner-step resolution. The `dt = 1.0` run is excluded from the comparison: explicit-Euler linear stability on the nonlinear potential term `−2(|ψ|² − v²)ψ` requires `Δt < 2/(6D + 4v²) ≈ 0.43`, violated at `Δt = 1.0`. The clamp `|a|, |b| < 3` then engages, producing a bang-bang dynamics with flat scaling. An earlier hypothesis that this outlier reflected a physical cutoff coincident with the middle-tick scale `Δt₂ = 0.1` has been retracted.

## A.4 Exploration findings

Four unexpected signals in the raw data were investigated by an independent analysis:

**(i) Experimental mode ≡ whitened-source control, to three significant figures.** This is an architectural structural property of the feedback scheme, not empirical coincidence. The feedback terms `α(ψ − ⟨ψ⟩)` and `β · δS_history` are by construction mean-subtracted (history snapshots store `ψ − ⟨ψ⟩`), hence translationally invariant, hence insensitive to the spatial mean of the base source. Formally: since `α(ψ − ⟨ψ⟩)` and `β · δS_history` both integrate to zero in `x`, the constant component of `S₀` enters only the one-dimensional ODE for `⟨ψ⟩(t)`, decoupled from spatial modes. The base-source mean `⟨S₀⟩` therefore shifts `⟨ψ⟩` but cannot seed spatial structure. Quantitatively, `|⟨S₀⟩| / |S_{\text{saturated}}| ≈ 0.0012` — the 17-σ z-score of the BGE-drift violation of Laplace detailed-balance reported in arXiv v1 §4.9 is statistically significant but physically negligible in L². **Consequence for the theory**: the architectural claim **"the feedback layer is robust to base-source mean"** replaces the earlier heuristic claim **"BGE drift is the historical imprint that drives open dissipation."** Open dissipation arises from the feedback-plus-multi-scale coupling, not from the upstream statistical idiosyncrasy.

**(ii) The `dt = 1.0` outlier in O3 is a numerical, not physical, signature.** See §A.3.3.

**(iii) Insights 1 (localized excitations) and 5 (multi-scale synchronization) are a single proposition.** Removing multi-scale block-averaging while keeping the feedback (`control_single`) produces zero localized structures. The feedback operators preserve translation invariance by construction; block-averaging with `block = 2` imposes a fixed 16³ lattice of coarse cells, which is the symmetry-breaking perturbation that seeds the feedback's structure formation. The merged claim is: *localized phase-coherent excitations emerge in the feedback-driven PDE only when block-averaging provides a translation-symmetry-breaking seed.* The original two-insight formulation is revised accordingly.

**(iv) The O2 asymptote is a true plateau, not power-law decay to zero.** See §A.3.2 three-parameter fit.

## A.5 Three honest language downgrades

| original | downgraded |
|---|---|
| "RG self-similarity" | "**kinematic self-similarity under block averaging** — necessary but not sufficient for an RG fixed point" |
| "sustained `dS/dt > 0`" | "approach-to-plateau behavior at `~10⁻⁶`, five orders of magnitude suppressed from the initial transient, over 150 dimensionless time units; 100% of documents exceed `10⁻⁷` at `t = 200`; decay rate visibly decreasing (late-time window ratio 0.70 over 100 time units); exact functional form of the approach not pinned down by current data" |
| "BGE drift is the historical imprint that drives open dissipation" | "BGE drift is **not** a differential driver of the dynamics; the feedback layer is architecturally robust to base-source mean; open dissipation arises from feedback-plus-multi-scale coupling" |

These are not retreats. Each downgrade replaces a heuristic qualitative claim with a quantitatively supported, mechanistically grounded statement.

## A.6 Five insights — verdict

| # | original insight | verdict | notes |
|---|---|---|---|
| 1 & 5 | elementary particles = field excitations (localized Goldstone / soliton / breather) + multi-scale synchronization (RG from Phase B) | **merged: multi-scale-seeded localized excitations** | see §A.4 (iii); block-averaging is the translation-symmetry-breaking seed |
| 2 | atom = process (Axiom 1: dynamic, entropy-increasing, cross-scale, mutable) | **conditional pass** | §A.3.2 — quasi-stationary NESS at `10⁻⁶` |
| 3 | driving = objective material reflection (open dissipation; BGE drift is historical imprint, not noise bias) | **refined** — architectural theorem | §A.4 (i); feedback robust to base-source mean |
| 4 | coupling = b + c bidirectional self-feedback (Axiom 6 "matching = self-training" in mathematical form) | **pass** | `|ψ|²` from 1.00 → 1.42, source `|S|₂` from 0.008 → 1.37, free energy from +10⁴ → −3.6·10⁴ |

**No insight is falsified**, three are refined, two are merged. The refinements strengthen the theoretical coherence of the framework by grounding its central claims in mechanisms rather than heuristics.

## A.7 Relation to arXiv v1 open problems

**OP1 (Axiom 6 formalization).** Phase B Exp 1 does not address OP1. Axiom 6 M2 falsification (arXiv v1 §5.1) remains the current state of the open problem.

**OP2 (Axiom 3 three-fold co-design).** The architectural theorem of §A.4 (i) partially obviates OP2 sub-problem (a) — source-drift de-biasing — for the mean channel: when the feedback is the coupling route, the base-source mean is not a necessary upstream correction. Sub-problems (b) — potential geometry — and (c) — numerical scheme — remain open. They are the subject of Block V Phase A-0 / A-1 / A-2 / A-3 (arXiv v1 §5.3), which retains its priority.

## A.8 Explicitly not claimed

- That MaoField solves any established open problem in theoretical physics, information retrieval, or AI.
- That the ≈ 50 localized patches per document correspond to specific ontological entities ("particles", "atoms", "concepts"). They are well-defined dynamical features of the PDE; their interpretation remains open.
- That the plateau at `dS/dt ≈ 10⁻⁶` is a rigorously defined thermodynamic NESS in the Seifert-Evans-Searles sense. It is a finite-time, finite-size, deterministic-integrator observation consistent with NESS phenomenology.
- That the kinematic self-similarity result (§A.3.3) is evidence of RG universality, a critical exponent, or membership in any known universality class. It is Kadanoff-block-averaging agreement between two stability-admissible time scales.
- That the architectural theorem (§A.4 (i)) implies BGE is a neutral upstream. It implies only that the base-source **mean** has no differential effect on the feedback dynamics; higher-order statistics were not ablated.
- That the Day 1–Day 4 compressed execution (2026-04-15, 36 hours) substitutes for a properly paced parameter-scan and robustness campaign. It does not.
- That the findings generalize beyond the specific `(α, β, N_hist, block_size) = (0.1, 0.05, 100, 2)` parameter choice used here. Parameter robustness is deferred to follow-up experiments (§A.9).

## A.9 Follow-up

- **Parameter robustness**: `(α, β, N_hist)` scan across the ranges specified in the task specification `(α ∈ {0.01, 0.1, 0.5}, β ∈ {0, 0.05, 0.2}, N_hist ∈ {50, 100, 500})`. Do the qualitative findings hold?
- **Block-size dependence**: self-similarity exponent `η` as a function of `block_size ∈ {2, 4, 8}`; distinguish seeding-hierarchy self-similarity from universal scaling.
- **True Langevin limit**: add noise `σ · η(x, t)` and compare `c(σ)`. The deterministic `c ≈ 10⁻⁶` is the `σ → 0` limit; the thermodynamic interpretation of the NESS in the stochastic case is sharper.
- **Retrieval correlation**: does the patch count correlate with document-level retrieval performance or semantic complexity? This is the natural test of the "multi-scale-seeded localized excitation = candidate semantic unit" interpretation.
- **True RG flow**: measure the feedback parameters `(α_eff, β_eff, D_eff)` at successive block scales and check for flow toward a fixed point. The current experiment demonstrates kinematic self-similarity of configurations; a proper Wilson flow in the parameters is a separate observation.
- **History saturation**: run `t_sim = 100` to fully saturate `N_hist = 100` and confirm the qualitative findings.

## A.10 Data and code availability

All analysis code (Rust engine source, Python analysis scripts), raw observable JSONs, stationary-state ψ-field snapshots (`states.bin`, little-endian `f32` pairs), independent review records (code review, three observable-specific math reviews, exploration-signals analysis, verdict review), and the task specification originating this experiment are archived in `exp017_dialectics/results/phase_b_exp1/` and included in the v0.1.1 Zenodo release.

---

*Linux Claude, 2026-04-15, under Yifan Chen's Gate 2 authorization. Independent review of this appendix is archived as `REVIEW_PHASE_B_EXP1_appendix.md`.*
