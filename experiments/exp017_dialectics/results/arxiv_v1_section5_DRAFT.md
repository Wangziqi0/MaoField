# Section 5 — Roadmap: Refined Open Problems and Block V Program

*arXiv v1 first draft, 2026-04-14. Win Claude. Cross-review by Linux + independent paper-review subagent.*

**Position**: this section formalizes the two open problems (OP1, OP2) in their post-experiment refined form, lays out Block V's three-axis co-design experimental program (Phase A-0/A-1/A-2/A-3), and states the three-stage publication strategy that organizes follow-up work.

---

## 5.1 OP1: Axiom 6 Formalization — M2 Falsification

Axiom 6 asserts that matching is self-training: the matching score between query and document fields should be the fixed point of a self-consistent iteration. The natural candidate

```
M2:   S_{n+1} = normalize(S_n · ψ_q* · ψ_d)                                  (5.1)
```

was proposed as a Banach contraction giving a unique fixed point on the unit sphere of `ℂ^N`.

**Falsification**. The map `T_ψ : S ↦ normalize(S · ψ_q* · ψ_d)` is **0-homogeneous**: `T_ψ(λS) = T_ψ(S)` for any `λ > 0`. Hence

```
‖ T_ψ(S) − T_ψ(2S) ‖ = ‖ T_ψ(S) − T_ψ(S) ‖ = 0
‖ S − 2S ‖           = ‖ S ‖
```

The contraction coefficient is therefore identically zero between any two points on the same ray. The Banach contraction property requires `‖ T(x) − T(y) ‖ ≤ k · ‖ x − y ‖` with `k < 1` *uniformly* across the metric space; M2 trivially satisfies this between rays but cannot be a contraction in any sense that yields a unique fixed point in `ℂ^N` itself (since the entire ray is fixed setwise but no single point is fixed).

**Reformulation in `ℂP^{N-1}` (open)**. The 0-homogeneity means `M2` descends to a well-defined map on the projective space `ℂP^{N-1}`. Whether the descended map is a contraction in the **Fubini-Study metric** on `ℂP^{N-1}` is a meaningful question. Linear convergence rates suggested by power-iteration analysis (Appendix A.4 of `open_problems_followup.md`) are consistent with contraction-like behavior, but a rigorous Lipschitz estimate has not been established.

**Status**. Axiom 6 currently has **no known canonical mathematical formalization**. M2 is excluded as a candidate. Other candidates (M1, M3) considered in `open_problems_followup.md` either fail similar tests or are demonstrably non-converging on test cases. We **do not falsify Axiom 6 itself** — only its M2 candidate; the axiom remains as a physical intuition awaiting mathematical capture.

---

## 5.2 OP2: Refined to Three-Fold Co-Design

### 5.2.1 Pre-A1.4 Form

Prior to A1.4 (§4.9), OP2 was stated as:

> "Pure gradient flow + isotropic Langevin fails to populate distant attractor basins under finite simulation horizon. Non-equilibrium extensions (Langevin, Hamiltonian, active driving) are needed."

This wording treated OP2 as a single problem with potential single-axis solution paths. The A1.4 diagnostic (§4.9) reveals this framing as insufficient.

### 5.2.2 Post-A1.4 Refined Form

OP2 is a **three-axis co-design problem**. Resolution in any single axis, holding the others fixed, does not restore the predicted equilibrium or close the reachability gap.

**OP2 (a) — Source-field statistics**. Detailed-balance prerequisites for Boltzmann / Laplace equilibrium require either mean-zero sources or explicit non-equilibrium steady-state analysis. BGE-M3 source fields exhibit `t = -17.1, p < 10⁻²⁵` non-zero mean in the imaginary component (`⟨S_b⟩`), violating mean-zero. The deterministic baseline `σ=0` already produces `66% u=2` occupancy (vs. Laplace prediction `40%`) due to source drift alone — *no noise contribution possible*. Resolution requires either source whitening (mean-subtraction, possibly Hodge decomposition for solenoidal components) or an extended steady-state framework explicitly accounting for the non-equilibrium current.

**OP2 (b) — Potential geometry**. Confinement must exceed noise step size across the accessible field-space domain. The shifted potential `V(u) = u(u-1)²(u-2)²` has a `u⁵` tail at `u → ∞`, insufficient to confine `|ψ|²` against `σ √dt = 0.112` per-step displacement at `σ=0.5`. Voxels escaping the outer well random-walk to the clamp boundary (`53%` clamp residency in §4.9). Resolution requires either higher-order polynomial confinement (`tail ≥ u⁶`), logarithmic / exponential confinement, or — what we currently believe is the cleanest path — **non-polynomial closures** (e.g., piecewise constructions, reflecting boundary conditions at `|ψ| = R_max`) that decouple the inter-well barrier height from the outer confinement strength.

**OP2 (c) — Numerical scheme**. Stiff potential gradients require numerical integration with stability margin for the Lipschitz constant. Soft walls `λ · max(0, u - u_max)⁴` produce Jacobian spectral radius `J ≈ 1.5×10⁴ · λ` at `u≈u_max + 7.5`, requiring `dt_max,c1 ≈ 1.3×10⁻⁴` (λ=1) and `dt_max,c2 ≈ 1.3×10⁻⁵` (λ=10) under explicit Euler — **violations of ~380× (λ=1) to ~3800× (λ=10)** at our `dt = 0.05` (numbers from VERDICT.md §3.3). The result is integrator instability absorbed into the clamp (more clamp events with stiffer wall: `λ=10` gives `+6.8 pp` clamp residency vs `λ=1`). Resolution requires **implicit or IMEX integration** (wall term treated implicitly, rest explicit), or sub-CFL `dt`, or — what we currently believe is the cleanest path — **reflecting boundary conditions** (Skorokhod radial projection) in place of soft walls.

### 5.2.3 Coupling: The Three Axes Are Not Independent

**Fixing any axis in isolation does not restore equilibrium**:

| Fix attempted | Why still fails |
|---|---|
| Source whitening only | Potential tail still `u⁵`, integrator still CFL-violating at `σ ≥ 0.5` |
| Potential only (deeper tail) | Source drift still breaks detailed balance; deeper potential worsens integrator stiffness |
| Integrator only (implicit) | Source drift remains 17σ non-zero; shallow tail still allows escape beyond basins |

A1.4 was an attempt to vary axis (b) alone; it produced the diagnostic finding **precisely because** it isolated one axis and exposed the unaddressed interactions. Block V Phase A is the systematic co-design experimental program.

### 5.2.4 Connection to the Categorical Open Problem (§2.3.3)

The same conjectured stochastic extension required for the Giry-monad lift `P ∘ T_•` (§2.3.3) supplies the mathematical structure within which OP2's three axes are naturally addressed:

- Source-statistics axis (OP2 a) ↔ specifying the input measure on `Meas` for which `T_•` admits a Markov-kernel lift
- Potential-geometry axis (OP2 b) ↔ the support and confinement structure of the kernel
- Numerical-scheme axis (OP2 c) ↔ the discrete-time stochastic process approximating the continuous Markov dynamics

This identification — three apparently independent experimental refinements unified under a single conjectured categorical structure — is what we call the **three-faces convergence** of §2.3.3. Whether the convergence holds rigorously is, of course, an open question; we offer it as the most coherent organizing conjecture currently visible.

---

## 5.3 Block V Program: Phase A as Co-Design

Block V is the next experimental campaign. Its **Phase A** addresses OP2's three-axis structure via four sub-blocks: a reachability pre-check (A-0) followed by axis-specific interventions (A-1, A-2, A-3) and a joint-design evaluation (A-joint). All sub-blocks are mechanism studies on small datasets (NFCorpus, FiQA, ~100 docs); larger sweeps are deferred to Phase B.

### A-0 Reachability Pre-Check

**Purpose**: Verify that the chosen `(V, init, σ, t_sim)` configuration is reachable from the Boltzmann sense — i.e., that the predicted equilibrium distribution is consistent with the gradient-flow basin-of-attraction structure under the prescribed initialization. This precludes the "unreachable Laplace" trap exhibited by A1 (where the prediction was correct but the dynamics could never reach it under any finite `σ`).

**Method**: For each candidate `V`, compute `(BoA(V) ∩ supp(p_init))` for each minimum, verify that all minima have nonzero overlap with init support; compute Kramers `k_{i→j} · t_sim` across all saddle pairs and verify they are within a reasonable range (e.g., `[10⁻², 10²]`) to ensure thermalization is feasible within horizon.

**Output**: A pre-flight checklist for each `V` configuration before launching the σ-scan.

### A-1 Source-Field Statistics Axis

**Purpose**: Quantify and remediate source-field bias for the potentials studied.

**Method**: For each source construction `F_•` (sparse byte, dense BGE-M3, dense BGE-large, learned-but-whitened, principled-mean-zero):

1. Compute `⟨S⟩` and `t`-statistic for non-zero mean
2. Compute Hodge decomposition (gradient + solenoidal parts)
3. Test mean-subtracted variant `S' = S − ⟨S⟩` and re-run a baseline σ-scan
4. Compare equilibrium distributions to Laplace predictions across source variants

**Success criterion**: identify a source construction (or whitening procedure) for which the deterministic `σ=0` baseline falls within `±10 pp` of the gradient-flow basin-of-attraction-weighted Laplace prediction.

**Anti-claim to avoid**: "approaching init distribution" (this is not testable since init is itself a distribution).

### A-2 Potential Geometry Axis

**Purpose**: Find a potential family for which inter-well barrier and outer confinement can be independently tuned.

**Sub-experiments**:

- **A-2.a** (deeper polynomial tail, additive form): Compare `V_5(u) = u(u-1)²(u-2)²` (current A1.4) against `V_8(u) = V_5(u) + α·(u-u_outer)^k` with `k ≥ 6` and tunable `α, u_outer` adding a higher-order confining term — verify whether deeper polynomial *tail* helps without changing inter-well barrier (note: multiplicative tail forms like `(u-c)²` were considered and excluded, since they reshape inter-well barriers; see `BLOCK_V_DESIGN.md` Phase A v2 for the additive-quartic discussion)
- **A-2.b** (Z_n angular, full development): Implement `V(ψ) = -A|ψ|² + B|ψ|⁴ + C·Re(ψ^n)` for `n ∈ {3, 4, 6}`. Confining radial structure (Mexican hat) decouples from angular barriers (`ε · Re(ψ^n)`). See `BLOCK_V_DESIGN.md` §2.3 for full mathematical analysis (Linux Claude, 2026-04-14)

(Note: the piecewise / non-polynomial route originally considered as A-2.c has been merged into A-3.c — Skorokhod radial reflection — since reflecting BC is the cleanest non-PDE alternative and properly belongs to the numerical-scheme axis.)

**Success criterion**: identify a `V` family for which Laplace prediction matches σ=0.3 / σ=0.5 observation within `±15 pp` per basin **after** A-1 source whitening.

### A-3 Numerical Scheme Axis

**Purpose**: Implement integration scheme appropriate for stiff potentials.

**Sub-experiments**:

- **A-3.a** (IMEX): Treat wall term implicitly (Crank-Nicolson or backward Euler on the wall part), rest explicitly. Verify stability at `dt = 0.05` for `λ ∈ {1, 10, 100}`
- **A-3.b** (specify Jacobian structure): For implicit treatment, the Jacobian of `−V'(u)·ψ` is a 2×2 block per voxel; structure documented in `BLOCK_V_DESIGN.md` §4.5.3 Phase A-3 (Linux, 2026-04-14)
- **A-3.c** (Skorokhod radial reflection): Replace soft wall with a reflecting BC at `|ψ| = R_max` via Skorokhod radial projection (overdamped systems have no velocity to reflect; the projection is done on position). This is the structurally cleanest BC for confined diffusion

**Success criterion**: stable integration at `dt = 0.05` for arbitrary `V` configurations encountered in A-2.

### A-joint Phase A Capstone

**Purpose**: Demonstrate that the three axes addressed jointly recover a Laplace-predictable equilibrium.

**Method**: Take the **best A-1 source configuration** (mean-subtracted BGE or principled mean-zero), the **best A-2 potential** (selected from A-2 sub-experiments by success criterion), and the **best A-3 integrator** (validated stable in A-3). Run σ-scan on this joint configuration, compare to Laplace prediction.

**Success criterion**: at least one σ value yields all-basin occupancy within `±10 pp` of Laplace prediction *with* `[STATIC]` and `[DYNAMIC-EQUILIBRIUM]` mode tags consistent.

**Anti-claim to avoid**: "best of" combinatorial over all (A-1, A-2, A-3) variants would explode; A-joint commits to one variant per axis as decided by the per-axis success criteria.

### A-joint outcomes and their interpretation

- **A-joint succeeds** → OP2 is **confirmed solvable in the gradient-flow + isotropic-Langevin regime** with three-axis co-design. OP2 (b) directed-driving program becomes a generalization rather than a necessity. Block V can proceed to Phase B compositional benchmarks
- **A-joint partially succeeds** (e.g., 2 of 3 basins within tolerance) → OP2 has a **partial co-design solution**; the unresolved third axis identifies the remaining open question, which may require Phase B's directed-driving (Hamiltonian flow, anisotropic noise) approaches
- **A-joint fails** → strong evidence that gradient-flow + isotropic-Langevin is **structurally insufficient** for our class of problems; OP2 (b) becomes the only path forward; Block V Phase B becomes the central thrust

In all three cases, the outcome is informative — A-joint is a diagnostic, not a make-or-break engineering test.

---

## 5.4 Block V Phase B and C: Outlook

**Phase B** addresses OP2 path (b) — directed non-equilibrium driving:

- **B-H (Hamiltonian)**: Add symplectic structure `∂_t ψ = -i δH/δψ*` as an alternative to `-δH/δψ*`. Energy-conserving dynamics may explore the energy shell rather than descend
- **B-A (Active forcing)**: External drive `f(ψ, t)` representing "practical intervention" beyond thermal noise
- **B-N (Anisotropic noise)**: `⟨η η*⟩` with non-trivial spatial / spectral structure to bypass timescale problems via directed exploration

**Phase C** addresses Axiom 7 (dynamic potential) and compositionality:

- **C-V** (dynamic V): `V(ψ, t, history)`, the potential itself evolved by an outer loop reflecting field history
- **C-S** (SCAN-like compositional benchmarks): test whether MaoField's symbolic-composition properties scale to compositional generalization tests once Phase A or B has stabilized the underlying dynamics

Phases B and C are scoped at **2026-Q3 / Q4** in our internal planning; arXiv v1 documents Phase A only, with B and C signposted as future work.

---

## 5.5 Three-Stage Publication Plan

Internal scheduling, included for transparency:

**Stage 1 — arXiv v1 / Zenodo v0.1.0 (2026-04-13 / 2026-04-20)**

- v0.1.0 skeleton release on Zenodo (DOI `10.5281/zenodo.19550342`): repository structure, axioms, narrative, no paper PDF (already released)
- v0.1.1 paper PDF release: this paper (target 2026-04-20). Includes Block I-IV.5 experimental evidence, OP1 / OP2 statements, Phase A program

**Stage 2 — Mechanism Paper at IPM (target 2026-07–08 month)**

- Single-purpose paper: *"Why PDE-based retrieval scales poorly: an attractor-capacity analysis"*
- Focus: mechanism explanation of `k* = 2` ceiling and source-density coupling
- Audience: Information Processing & Management readership (IR / IR-adjacent ML)
- Builds on this arXiv v1's Block I-IV.5 results + Phase A outcomes (pending)

**Stage 3 — Capstone Paper at Generalist Top-Tier (target 2027 Q1-Q2)**

- Audience: `Nature Machine Intelligence` or equivalent
- Content: full framework synthesis, philosophical positioning, capstone results from Block V Phases A + B (and, if successful, C)
- Deliberately deferred to allow Block V experimental program to mature; deferral is a **methodological decision**, not a timeline slip

**Why three stages**. Releasing a generalist top-tier paper before the mechanism is empirically validated would either over-claim or under-claim. The arXiv v1 establishes the framework and open problems publicly; the IPM paper validates the central mechanism in a domain-specific venue; the generalist paper integrates after validation. This sequencing also reduces single-point publication risk (failure or delay of any one stage does not block the others).

---

## 5.6 Concluding Note on the Status of OP1 and OP2

We close with an explicit statement of the two open problems' present status, intended to forestall over-reading of the contributions claimed in this paper.

- **OP1 (Axiom 6 formalization)**: candidate iteration M2 falsified (§5.1). Axiom 6 remains as a physical intuition without canonical mathematical formalization. We do not claim OP1 is solved or refuted; we claim one candidate is excluded.
- **OP2 (Axiom 3 non-equilibrium extension)**: refined from "needs non-equilibrium" to a three-axis co-design problem (§5.2). Block V Phase A is the experimental program designed to address it (§5.3). We do not claim OP2 is solved; we claim its scope is more precisely identified than at the start of this campaign.

**A framework whose research program lies entirely in its open problems is not an evasion** — it is the honest representation of a research stage. We expose OP1 and OP2 prominently rather than concealed because (i) the contributions of §4 (empirical evidence) and §2 (categorical structure) make sense only against a scaffold that includes these problems explicitly, and (ii) the dialectical-materialist epistemology that motivates the framework demands that "open contradictions are the engine of motion" — a methodological self-application of Axiom 1.

The next paper in the series (the IPM mechanism paper, Stage 2) will report Block V Phase A's outcome under the success criteria stated in §5.3.
