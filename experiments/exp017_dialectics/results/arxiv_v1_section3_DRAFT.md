# Section 3 — Mathematical Formulation

*arXiv v1 first draft, 2026-04-14. Win Claude. Cross-review by Linux + independent paper-review subagent.*

**Position**: structured statement of the field-theoretic formalism, the seven framework axioms, the source-attractor adjunction, and the two meta-problems (OP1, OP2). Includes a dedicated subsection (§3.5) on the use of symmetry-breaking language under finite-lattice settings — a concession to mathematical rigor that the empirical sections (§4) require.

---

## 3.1 Field-Theoretic Setup

We model semantic information via a complex scalar field `ψ : Ω → ℂ` over a discrete spatial domain `Ω = [N]³` (default `N=32`, `|Ω| = 32³ = 32768` voxels) with periodic boundary conditions. The field evolves under a generalized Ginzburg-Landau / Allen-Cahn dynamics:

```
γ · ∂_t ψ(x, t) = D · ∇²ψ(x, t) − ∂V/∂ψ*(ψ(x, t)) + S(x) + η(x, t)         (3.1)
```

with parameters and quantities:

- `γ > 0`: damping coefficient (default `γ=1`, units fixing convention)
- `D > 0`: diffusion coefficient (default `D=0.1`)
- `∇²`: discrete Laplacian on the toroidal lattice (`dx=1`)
- `V : ℝ_{≥0} → ℝ`: scalar potential as a function of `u = |ψ|² = |a|² + |b|²` where `ψ = a + ib`. The Wirtinger derivative `∂V/∂ψ* = V'(u) · ψ` provides the field-theoretic gradient (see Appendix 3.A for sign conventions and derivation)
- `S : Ω → ℂ`: a deterministic source term encoding the input text. Two canonical constructions are studied:
  - `S_sparse(x)`: byte-frequency construction (UTF-8 codepoints scattered across the 32³ grid; ~10% nonzero occupancy)
  - `S_dense(x)`: BGE-M3 1024-dim embedding tiled across the grid, smoothed and max-normalized
- `η : Ω × ℝ_{≥0} → ℂ`: complex Gaussian noise satisfying `⟨η(x,t) η*(x',t')⟩ = σ²·δ_{xx'}·δ(t−t')`, parametrized by noise intensity `σ ≥ 0`. The case `σ=0` recovers deterministic gradient flow

The default potential is the standard double-well GL form `V(u) = ¼·(u − 1)²` (admitting `|ψ|=1` as the unique minimum on the U(1) orbit of vacua, and `ψ=0` as an unstable fixed point). For diagnostic experiments (Blocks IV.5, V) we substitute richer `V(u)`; the explicit forms are stated in §4 at point of use.

The dynamics (3.1) admits the L² free-energy functional

```
F[ψ] := ∫_Ω [ D·|∇ψ|² + V(|ψ|²) − (S·ψ* + S*·ψ) ] dx                       (3.2)
```

so that `γ ∂_t ψ = −δF/δψ* + η`. We adopt the no-½ convention in (3.2) — equivalent to using the Wirtinger derivative `δ/δψ*` directly without inserting the canonical Wirtinger factor of 2 — so that the Euler-Lagrange equation `γ ∂_t ψ = −δF/δψ* + η` reproduces (3.1) without rescaling. See Appendix 3.A for the Wirtinger conventions in detail.

In the noiseless limit `σ=0`, `dF/dt = −γ⁻¹ ∫ |δF/δψ*|² ≤ 0`, exhibiting **monotone descent** — a fact we use repeatedly in §4 to diagnose what gradient flow alone cannot reach (see §4.7, §4.8).

**Numerical scheme**. Equation (3.1) is integrated by explicit Euler with timestep `dt=0.05` for `5000` steps (simulation horizon `t_sim = 250`) unless noted. A clamp `|a|, |b| ≤ 3.0` is applied for numerical safety; in some experiments (notably §4.9 with `σ ≥ 0.5`) this clamp is reached and the resulting voxel occupancy at the boundary is a `[DYNAMIC-IMPLEMENTATION]` artifact rather than a physical steady state. We flag these cases explicitly throughout §4.

---

## 3.2 Seven Framework Axioms

The MaoField framework rests on seven axioms supplied by the principal author. These are not derived; they are postulates whose consequences (and limits) the paper explores. Each axiom is stated, followed by its concrete realization in the formalism of §3.1, and (where applicable) its connection to an open meta-problem (OP1 or OP2).

**Axiom 1** — *A particle is a dynamic process, not a static definition*.

  **Realization**: The unit of representation is the field configuration `ψ(x, t)` together with its evolution under (3.1), not a static vector. The "meaning" of an input text is the trajectory of `ψ` under the dynamics, evaluated at convergence (or at finite horizon).

**Axiom 2** — *Understanding equals the equilibrium state of internal-external opposition unified*.

  **Realization**: Score-ready representation is the fixed point of (3.1) under given source `S` and potential `V`. Adjunction `F ⊣ G` between Text and Field categories formalizes this opposition (§2.3.1); T-algebras (objects fixed by `T = G∘F`) are the categorical form of this equilibrium (§2.3.1).

**Axiom 3** — *The driving force is the data's intrinsic regularity, not an externally imposed objective*.

  **Realization**: No external loss function or training signal. The dynamics (3.1) is autonomous — driven only by the source `S` (encoding input regularity) and the potential `V` (encoding intrinsic field structure). **Open Problem 2 (OP2)**: the fully autonomous case (`η=0`, gradient flow only) is descending-phase only and cannot realize the *ascending* phase of dialectical motion (§4.7, §4.8 demonstrate the empirical limits; §5.2 reformulates OP2).

**Axiom 4** — *The corpus is a record of practice, not a fit to a statistical distribution*.

  **Realization**: Source `S` is constructed deterministically from each input text (no learned compression at the inference-time framework boundary). `S_sparse` (byte-level, fully transparent) is the strict realization. `S_dense` (BGE-M3, learned upstream and fixed at inference time) is included as a **partial relaxation of Axiom 4 used for ablation purposes**, not as an embodiment of the axiom — and the resulting source drift in §4.9 (`⟨S_b⟩ = -1.5×10⁻³, t = -17.1, p < 10⁻²⁵`) provides **quantitative evidence for the necessity of the strict reading**: a learned embedding violates the mean-zero source assumption underlying our Laplace prediction by 17σ, and this violation is the dominant source of OP2's source-statistics axis (§5.2.2 (a)). The paper studies both realizations precisely to expose this contrast.

**Axiom 5** — *Composite structures are the superposition of simpler structures*.

  **Realization**: Composite source fields `V_{A∪B}(ψ) = V_A(ψ) + V_B(ψ)` (potential addition, not field addition — GL non-linearity prevents the latter from preserving the GL form). Sources superpose linearly: `S_{A∪B}(x) = S_A(x) + S_B(x)`. Compositional benchmarks (e.g., SCAN-style) are reserved for Block V Phase B.

**Axiom 6** — *Matching is itself self-training*.

  **Realization**: Given a query field `ψ_q` and a candidate document field `ψ_d`, the matching score is computed by an iteration that is jointly self-consistent — not by a fixed encoder. **Open Problem 1 (OP1)**: a candidate iteration `S_{n+1} = normalize(S_n · ψ*_q · ψ_d)` (M2) was proposed as a Banach contraction giving the unique fixed point. We **falsify** this candidate in §5.1: M2 is 0-homogeneous and trivially fails Banach contraction in `ℂ^N`; the question of contraction in projective `ℂP^{N-1}` under Fubini-Study metric remains open, but no rigorous fixed-point theorem is currently in hand. Axiom 6 thus has **no known canonical mathematical formalization** as of this writing.

**Axiom 7** — *Reaction rules are dynamically shaped by input and state, not fixed*.

  **Realization**: In current MaoField, `V(ψ)` is fixed across the run; the dynamics (3.1) is the only mechanism by which input shapes outcome. A **future direction** (Block V Phase C sub-block C-V, dynamic-potential, see §5.4) replaces fixed `V` with `V(ψ, t, history)`, where the potential itself is evolved by an outer loop reflecting accumulated field history. This is consistent with Axiom 7 but not yet implemented.

**Tension points**. We note three places where the strict reading of an axiom comes into tension with our current implementation:

1. Axiom 4 vs. BGE source: BGE is a learned (statistically fitted) embedding, a partial concession against "no statistical fit." We treat BGE as a **trained reflection of practice** — i.e. the upstream training is itself a practice-record — but flag this as a concession with empirical consequences (the source drift in §4.9).
2. Axiom 3 vs. Langevin noise: introducing `η` is an external (thermal) driving in tension with "no externally imposed objective." We treat `η` as **quasi-material** (representing finite-temperature physical noise rather than a designed gradient signal) and use it only diagnostically to expose OP2's structure (§4.8, §4.9). Future *directed* driving (anisotropic noise, active forcing) would require more careful axiomatic justification.
3. Axiom 7 vs. fixed `V`: as noted, full Axiom 7 implementation is deferred to Block V V.5.

---

## 3.3 Source-Attractor Adjunction

The dynamics (3.1) implements an adjunction `F ⊣ G` between a category of inputs and a category of attractors:

- `F : Text → Field` is the source construction `Text(s) ↦ S(x)` extending to the initial field configuration `ψ_0(x)`. Two implementations are studied: `F_sparse` and `F_dense` (defined in §3.1).
- `G : Field → Score-ready` is the time-evolution map `(ψ_0, V, σ) ↦ ψ_∞`, the fixed point (or finite-horizon snapshot) of (3.1).

The composition `T_• := G∘F_•` becomes a well-defined endofunctor of the ambient category `Meas` (§2.3.2). We do **not** claim `T_•` is a monad in the deterministic case; the lift to a Giry-monad `P ∘ T_•` is conjectured and reserved for follow-up work (§2.3.3 and footnote ⁵ thereof). For the present paper, all categorical statements involving `T_•` are read as endofunctorial; statements requiring monad axioms (T-algebras, Kleisli, EM) are flagged "conjectured under monad lift."

A T-algebra (under the conjectured lift) `(X, α: TX → X)` corresponds to a self-consistent attractor of the dynamics: an object that is fixed by the iterated source-evolution-readout cycle. The reachability question — which T-algebras are *dynamically* attainable from a given initial distribution — is the categorical form of OP2 (see §2.3.4 and §5.2).

---

## 3.4 Open Problems as Meta-Theoretic Constraints

Two open problems organize the framework's relationship to its own incompleteness. Both are explicitly identified, neither is resolved here, and both are central to the forward roadmap.

**OP1 (Axiom 6 formalization)**. Axiom 6 ("matching is self-training") asserts the existence of a self-consistent iteration that produces the matching score directly from the field representations of query and document, without an external loss. The natural candidate iteration

```
M2:    S_{n+1} = normalize(S_n · ψ*_q · ψ_d)                                (3.3)
```

was proposed as a Banach contraction giving a unique fixed point. We falsify M2 as a contraction in §5.1. The status of OP1 is therefore: **Axiom 6 is asserted; no known canonical mathematical formalization exists**. The honest position is that Axiom 6 currently functions as a *physical intuition* awaiting mathematical capture, not a theorem.

**OP2 (Axiom 3 non-equilibrium extension)**. Axiom 3 ("intrinsic regularity drives, no external objective") under the strict reading — pure gradient flow with no external driving — is descending-phase only: the system relaxes to the local basin of attraction of its initial configuration and cannot realize qualitatively new synthesis (§4.7). Closing OP2 requires extending the dynamics beyond pure gradient descent. Section 4.9's A1.4 diagnostic refines OP2 from "needs non-equilibrium" to a **three-fold co-design** problem, formalized in §5.2.

These two open problems are **not failures of the framework but constitutive of its research program**. A framework that announced "all axioms have rigorous formalization" while implementing them in a finite-lattice numerical experiment would be over-claiming; explicit OP-tagging is the alternative to implicit overstatement.

---

## 3.5 On the Use of Symmetry-Breaking Language [^zn-loose]

A recurring formal concern arises from our repeated use of group-theoretic labels (`U(1)`, `Z_n`, "spontaneous symmetry breaking") in describing finite-lattice simulation outputs. We address this concern explicitly to forestall both reader confusion and reviewer objection.

**Strict-sense spontaneous symmetry breaking** in the Anderson-Goldstone-Nambu framework requires five conditions:

1. An **order parameter** `O[ψ]` whose expectation value distinguishes symmetry sectors
2. A **symmetry group** `G` acting on field space (continuous or discrete)
3. The **Hamiltonian / action** is invariant under `G`
4. The **ground state** breaks `G` (existence of non-`G`-invariant minima)
5. The **thermodynamic limit**: the symmetry breaking is sharp (no tunneling between symmetry-related ground states) **only in the limit of infinite system size** (`N → ∞`)

Condition (5) is **not satisfied** by our experiments: we work at `N = 32³ = 32768` voxels, finite simulation time `t_sim = 250`, and finite document corpus (per-domain BEIR scale, `O(10² – 10³)` documents). Strict-sense SSB **does not apply**; symmetry-related sectors always have finite tunneling rate at our scale.

**What we do mean**. We use SSB language in the **empirical distributional sense**: a field-theoretic observable (e.g., per-document `|R|` for phase concentration in §4.6, amplitude bistability in §4.6) exhibits a distribution that, at our finite lattice and finite simulation horizon, is **statistically distinguishable from the symmetric (uniform / monomodal) baseline** — established by formal `χ²` tests in §4 with degrees of freedom and significance levels reported.

Discrete-group labels (`Z_n`) attached to specific regimes (e.g., "byte `Z_1` regime" in §4.6, "BGE `Z_2` regime" in §4.6) are **labels of empirical distributional pattern**, not assertions of rigorous group action on a thermodynamically-broken vacuum. Where we state `Z_n` we mean: "the empirical distribution is consistent with the residual symmetry pattern that strict-sense SSB to `Z_n` would produce at infinite system size, modulo finite-size corrections we have not characterized."

We acknowledge this distinction explicitly because conflation between **empirical pattern** and **rigorous SSB** has historically led to overstatement when physics formalism is applied to non-physical (information-theoretic, biological, social) systems. **We do not claim our finite-lattice observations have the mathematical status of thermodynamic SSB**; we claim they are well-defined empirical regularities under our explicit experimental protocol, suggestive of the structural symmetry patterns we name.

**Mode-tagging convention** (used throughout §4 to reduce the static-to-dynamic confusion that we identified internally as a recurrent error class):

- `[STATIC]`: landscape geometry — critical points, Hessian, barrier heights, energy ratios. No reference to time or noise
- `[DYNAMIC-EQUILIBRIUM]`: Boltzmann / Laplace stationary distribution predictions assuming thermalization within `t_sim`
- `[DYNAMIC-RARE-EVENT]`: Kramers escape rate, horizon comparisons, `ΔV/T_eff` regime indicators
- `[DYNAMIC-IMPLEMENTATION]`: numerical scheme (CFL stability, integrator choice), boundary conditions, source statistics

This tagging discipline is a methodological precaution — it makes explicit which regime each statement belongs to and prevents the silent conflation of, e.g., a static energy ratio with a dynamic log-probability gap (a confusion we caught and corrected internally; see §4.8 for the corrected statements with both quantities given side-by-side).

> [^zn-loose] All `Z_n` symbols in this paper are used in the empirical distributional sense defined in §3.5: they describe the residual pattern observed in the finite-lattice simulation, and are consistent with — but not proof of — strict-sense Anderson-Goldstone-Nambu spontaneous symmetry breaking. Strict-sense SSB requires the thermodynamic limit (`N → ∞`), which is violated by our `N = 32` lattice. This footnote applies wherever `Z_n` appears in §4 and beyond.

---

## Appendix 3.A: Wirtinger Derivative Convention

For a complex field `ψ = a + ib`, the Wirtinger derivatives are

```
∂/∂ψ  = ½ (∂/∂a − i ∂/∂b)
∂/∂ψ* = ½ (∂/∂a + i ∂/∂b)
```

For a real-valued potential `V(u)` with `u = |ψ|² = a² + b²`,

```
∂V/∂ψ* = V'(u) · ψ
```

This is the convention used throughout the paper.

**Factor consistency between (3.1) and (3.2)**. The Wirtinger derivative `δ/δψ*` of the no-½ free energy `F = ∫[D|∇ψ|² + V − (Sψ* + S*ψ)] dx` (equation 3.2) is

```
δF/δψ* = −D∇²ψ + V'(u)·ψ − S
```

so that `γ ∂_t ψ = −δF/δψ* = D∇²ψ − V'(u)·ψ + S` reproduces (3.1) **without** any factor-of-2 rescaling. We adopt this no-½ convention to make (3.1) and (3.2) directly compatible. The alternative convention — `F̃ = ∫[½D|∇ψ|² + V − ½(Sψ* + S*ψ)] dx` (with ½'s on the kinetic and source terms) — requires the Wirtinger-canonical relation `γ ∂_t ψ = −2 · δF̃/δψ*` and gives the same (3.1); we choose the no-½ convention for notational economy. The L²-gradient flow gives, for `V(u) = ¼(u−1)²`:

```
γ ∂_t ψ = D∇²ψ − (u − 1)·ψ + S + η
```

A common implementation pitfall is to use `∂V/∂ψ` (without conjugate) in the gradient-descent direction. For radially symmetric `V(u)`, this difference is invisible at static critical points (where `sin` and `cos` factors of phase derivatives both vanish) but produces incorrect dynamics in the Z_n angular potentials proposed for Block V (§5.3); we have verified the convention against SymPy and against the explicit gradient of `F` defined in (3.2).

---

*Forward references*. §4 reports the experimental evidence under the formalism above. Block I (§4.2) establishes baseline retrieval performance; Block II (§4.3) tests Kuramoto coupling; Block III (§4.4) enumerates attractors; Block IV (§4.5) studies source-density × operator interactions; Block IV.5 (§§4.6–4.9) decomposes `k*=2` into byte and BGE regimes (Stage C), tests gradient-flow reachability of multi-well minima (Stage A1), tests Langevin noise as an OP2 mechanism (Stage B1), and refines OP2 to a three-fold co-design problem (Stage A1.4). §5 then formalizes the refined open problems and lays out Block V's experimental program.
