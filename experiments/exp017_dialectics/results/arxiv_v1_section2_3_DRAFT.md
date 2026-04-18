# Section 2.3 — Adjunction, Monad, and the Categorical Structure of Dialectical Motion

*arXiv v1 first draft, 2026-04-14. Win Claude. Cross-review by Linux + independent paper-review subagent.*

**Position**: position-paper-level identification. The bare endofunctor picture on `Meas` is rigorous; the monad lift via Giry is conjectured and reserved for follow-up work. All `Z_n` labels follow the loose-sense convention defined in §3.5 and footnote `[^zn-loose]`.

---

## 2.3.1 From Adjunction to Monad: The Closure of Dialectical Operation

An adjoint pair `F ⊣ G` between categories `C` and `D` expresses a primitive form of dialectical opposition: `F` *proposes* objects of `C` into `D` (the moment of **thesis**, "立"), while `G` *returns* objects of `D` back into `C` (the moment of **antithesis**, "破"). The adjunction is constituted by two natural transformations — the **unit** `η: Id_C ⇒ G∘F` and the **counit** `ε: F∘G ⇒ Id_D` — satisfying the triangle identities, which encode the **closure** of the propose-return cycle.

The composition `T := G∘F : C → C` is, when fully formalized, a **monad** with multiplication `μ := G·ε·F : T² ⇒ T`. Whereas the adjunction alone describes a single dialectical oscillation, the monad `T` internalizes the *iterative* dialectical process entirely within `C`. A **T-algebra** `(X, α: TX → X)` is precisely an object that has reached a self-consistent state under this iteration — it is the categorical form of the **synthesis**¹: not a third point adjoined, but a structural invariant of the propose-return-reintegrate cycle. The Kleisli and Eilenberg-Moore categories of `T` stratify the algebras by their mode of realization.

> ¹ *Synthesis* (Aufhebung in Hegelian terminology, capturing the dual sense of cancellation and preservation; often mistranslated as "combination", which loses the negation-of-negation structure). The T-algebra formalization preserves this dual structure: the algebra map `α: TX → X` both *absorbs* (cancels) the monadic iteration and *retains* (preserves) its action as an endomorphism.

This framing is due to Lawvere (1969); our contribution is to **propose** a physical realization of the structure under PDE dynamics and to **identify** two subtleties that pure categorical abstraction elides: the **decomposition of the operator F by source density** (§2.3.2), and the **failure of deterministic gradient flow to satisfy monad axioms** (§2.3.3). We do not claim our realization is the unique or the canonical one; we claim it is rigorous at the endofunctor level and that its open problems organize a coherent research program.

## 2.3.2 Two Paths, Two Endofunctors: The Source-Density Decomposition

MaoField implements the functor `F` via a source-field construction `Text → Field ∈ ℂ^N`. Our experiments reveal that this construction **is not unique**, and that the specific realization determines the algebraic structure.

Let `F_sparse : Text → Field` denote the byte-frequency construction (UTF-8 bits scattered over the 32³ grid, ~10% occupancy), and let `F_dense : Text → Field` denote the dense construction via a pretrained embedding (here BGE-M3, tiled to full grid coverage). With a common `G : Field → Score-ready representation` (Ginzburg-Landau gradient flow to fixed point), the composition `G∘F_•` properly spans three distinct layers (Text, Field, Score-ready). To discuss categorical structure, we embed all three as subcategories of an ambient category `Meas` of measurable spaces, extending `F_•, G` by identity outside their natural domains so that `G∘F_• : Meas → Meas` becomes a well-defined endofunctor. Under this embedding we obtain two composite **endofunctors** (the lift to genuine monads is reserved for §2.3.3 and footnote ⁵):

- `T_sparse := G∘F_sparse`: phase concentrated (`|R|_per-doc = 0.84`), U(1) broken in the empirical distribution but not antipodally split — `Z_2` not realized in the phase sector. Phase concentration to a narrow band (kmeans-2 center distance 26.2°). See §4.6 for full diagnostics.
- `T_dense := G∘F_dense`: amplitude bimodal at `|ψ|∈{0,1}`, phase much less concentrated (`|R|_per-doc = 0.20`, still non-uniform vs uniform-baseline 0.006). `V=¼(|ψ|²−1)²` admits only `|ψ|=1` as a true minimum; `|ψ|=0` is an unstable fixed point with `V(0)=¼ ≠ V(1)=0`, so no `Z_2` group action interchanges the two basins. The "amplitude bistability" is a **distributional pattern, not a group-theoretic claim**.

Numerically both yield `k*=2`. **Categorically they correspond to distinct endofunctors**: `T_sparse`'s candidate Kleisli category is phase-degenerate; `T_dense`'s is amplitude-stratified.² The claim that "dialectical closure is determined by the operator alone" is refuted by this decomposition — **the source-field functor `F` co-determines the algebra structure**. This is a categorical formulation of the materialist thesis that *practice (the mode of source-field construction) conditions the forms of cognitive closure*.

> ² This is a *conjectured* categorical interpretation based on the experimental phase/amplitude observations; a fully rigorous functorial treatment (e.g., explicit functors to `Z_n`-equivariant categories indexed by the broken symmetry pattern) is left to future work.

## 2.3.3 Why Deterministic Gradient Flow Is Not a Monad — and What This Reveals

A subtlety arises when one attempts to upgrade the endofunctor `T_• := G∘F_•` to a genuine monad in the Lawvere sense. The composition `G∘F_•` is an endofunctor of `Meas` once embedded as in §2.3.2, but the multiplication `μ : T² ⇒ T` requires that the iterative composition `T∘T` admit a canonical natural transformation back to `T`. For **deterministic** dynamics — gradient flow `∂_t ψ = −δH/δψ*` — this is **not the case**.

### The Categorical Diagnosis

Deterministic gradient flow is naturally an `R⁺`-monoid action on field space — equivalently, an **F-coalgebra** for the time-translation endofunctor (`X → F(X)` describing how state evolves under one time-step). It is not a monad: there is no canonical multiplication `μ: F∘F → F` satisfying the monad coherence axioms (associativity and unit) in the deterministic regime. The standard categorical lift to a genuine monad goes through **stochastic extension**: replacing deterministic flows with Markov kernels yields the **Giry monad** `P` on `Meas` (Giry 1982; Jacobs 2010). We conjecture that the source-attractor endofunctor `T_•` admits a Giry-monad lift `P ∘ T_•` inheriting (η, μ) from the underlying stochastic dynamics. Rigorous formalization of `P ∘ T_•` is an open problem.

### The Physical Diagnosis

The same stochastic extension required for the categorical monad lift is **also the physical mechanism** required to overcome the Kramers timescale obstruction observed in Stage B1 (§4.8). Under deterministic gradient flow alone, our system cannot escape any single basin of attraction (`F` is monotone non-increasing along trajectories); under isotropic Langevin, escape is possible but the Kramers rate `∝ exp(−ΔV/T_eff)` makes high-barrier crossings unreachable within finite simulation horizons. **Closing OP2 (Axiom 3's open problem of non-equilibrium extensions) requires moving beyond pure gradient flow to genuinely stochastic / non-equilibrium dynamics** — which is the same operation that supplies the Giry-monad multiplication `μ` for the categorical lift.

### Three Faces of One Open Problem

The categorical structure (§2.3.1–2.3.2), the OP2 physical roadmap (§5.2), and the Stage B1 phenomenology (§4.8) are not three independent open problems — they are **three faces of a single conjectured stochastic extension**:

```
  Categorical face        Physical face          Phenomenological face
  ───────────────         ─────────────          ─────────────────────
  Endofunctor T_•   ⟶    Gradient flow:    ⟶   B1: Inner barrier 
  not a monad             monotone, no            crossed (Kramers
  in deterministic        escape from any         marginal); outer
  regime                  basin                   barrier at 43-orders-
                                                  of-magnitude gap
                                                  
                          ┃                       ┃
                          ┃                       ┃
                          ┃ requires same         ┃
                          ┃ stochastic            ┃
                          ┃ extension             ┃
                          ┃                       ┃
                          ▼                       ▼

               ╔══════════════════════════════════════════╗
               ║ Conjectured stochastic structure:         ║
               ║                                           ║
               ║  Categorical:  Giry monad lift P ∘ T_•   ║
               ║  Physical:     directed non-equilibrium  ║
               ║                driving (OP2 path b)       ║
               ║  Phenom.:      barrier-and-confinement   ║
               ║                co-design (OP2 path a)     ║
               ╚══════════════════════════════════════════╝
```

This **convergence of three apparently independent open problems** onto a single conjectured stochastic structure is, in our reading, the **most coherent organizing conjecture currently visible** for MaoField as a research program. The dialectical-materialist principle that "categorical formalization, physical mechanism, and empirical observation should converge" (compatible with Axiom 4's materially-grounded epistemology) is **suggested**, not proven, by the framework's open problems lining up this way; rigorous demonstration of the convergence is itself part of the open problem.

> ⁵ Concretely, `Meas` is the category of measurable spaces with measurable maps; Text, Field, and Score-ready objects are embedded via their natural σ-algebras (discrete for Text, Borel for the ℂ^N Field, Borel for Score). Deterministic maps `F_•, G` extend to identity on the complement, so `T_• := G∘F_•` is a bona fide endofunctor of `Meas`. The Giry monad `P` is the standard probability-measure monad on `Meas` (Giry 1982; Jacobs 2010): for measurable space `(X, Σ_X)`, `P(X)` is the space of probability measures on `(X, Σ_X)` with the σ-algebra generated by evaluation maps `μ ↦ μ(A)` for `A ∈ Σ_X`; the unit `η_X : X → P(X)` is the Dirac map `x ↦ δ_x`; the multiplication `μ_X : P(P(X)) → P(X)` is the marginalization `Π ↦ ∫ν dΠ(ν)`. The conjectured lift `P ∘ T_•` of our endofunctor would carry the (η, μ) of `P` provided the natural-transformation diagrams compose; verifying or disproving this is OP1's category-theoretic component, related to but distinct from the M2-falsification of OP1's analytic component (see §5.1).

## 2.3.4 Reachability: The Categorical Measure of Open Problem 2

The source-density decomposition in §2.3.2 locates the choice of algebra structure at the functor `F`. A second, independent axis of constraint emerges from the **dynamics**: even when the target algebraic structure is in-principle present in `T-Alg_T` (the category of T-algebras under the conjectured monad lift), the dynamics of MaoField may fail to reach it. Stage A1 of our diagnostic cascade (§4.7) makes this concrete.

When `V(ψ)` is extended from the double-well `¼(|ψ|²−1)²` to a triple-well `|ψ|²(|ψ|²−1)²(|ψ|²−4)²`, the would-be T-algebra category gains additional objects corresponding to the `|ψ|=2` basin. However, under gradient-flow dynamics initialized from `|ψ|_init ≈ 1.0 ± 0.3`, the observed occupancy of the `|ψ|=2` basin is **0.00%** (99.15% at `|ψ|=1`, 0.85% at `|ψ|=0`). The `u=4` algebras exist in the theory but are not realized in the experiment.

This motivates the following refinement. Define the **reachable subcategory** under a unit `η` and an initial distribution `p_0`:

> `T-Alg_T^{(η, p_0)} := { (X, α) ∈ T-Alg_T | ∃ x_0 ∈ supp(p_0), η_{x_0} generates a Kleisli-reachable path to (X, α) via μ }`

In general `T-Alg_T^{(η, p_0)} ⊊ T-Alg_T`. We propose the **categorical gap**

> `Δ_{OP2} := |T-Alg_T| ⊖ |T-Alg_T^{(η, p_0)}|`

as the **formal measure of Open Problem 2**: the unrealized algebraic potential of dialectical structures that are *mathematically present* in the (conjectured) monad but *dynamically unreachable* under descending-only (gradient-flow) evolution.³

Two technical caveats are required for `Δ_{OP2}` to be well-defined:

(i) **The notation `⊖`** denotes full-subcategory complement: `Δ_{OP2}` is intended as the (essentially small) full subcategory of `T-Alg_T` whose objects do **not** lie in `T-Alg_T^{(η, p_0)}`, equipped with the inherited morphisms. `|·|` is then the cardinality (or, for proper-class issues, the cardinality after restriction to a Grothendieck universe), or — preferably — a coarser invariant such as groupoid cardinality `Σ 1/|Aut|` over isomorphism classes.

(ii) **`T-Alg_T` may be a proper class** in the absence of a small-set ambient universe; we restrict attention to `T-Alg_T ∩ U` for a suitable universe `U` containing all algebra structures of finite presentation under the conjectured monad lift, and treat the cardinality of the complement within this restricted setting. Footnote ³ acknowledges that other quantifications (categorical entropy, persistent-homology dimension of the unreached manifold, Kan extension obstructions) are equally valid and conjecturally agree in a common limit; the cardinality complement is a symbolic first pass.

The "Kleisli-reachable path" condition in the definition of `T-Alg_T^{(η, p_0)}` should be read as: there exists a finite composition of Kleisli morphisms (under the conjectured monad lift; see §2.3.3) starting from a unit of an element in `supp(p_0)` and reaching the algebra `(X, α)` as an object. This is a categorical translation of the dynamical reachability condition; rigorous formulation requires the Kleisli composition `g ∘_K f := μ ∘ Tg ∘ f` of the conjectured Giry-monad lift and is reserved for follow-up work.

> ³ `Δ_{OP2}` as defined above uses cardinality complement as a symbolic first pass; alternative quantifications — categorical entropy, persistent-homology dimension of the unreached manifold (Adams et al., giotto-tda 2021), Kan extension obstructions — remain follow-up work. The qualitative invariant — the gap between *existent* and *realizable* T-algebras — is conjectured (not proven) to be stable across these choices. Closing this gap is one component of OP2 (§5.2); the other component is the empirical co-design refinement identified in §4.9 (A1.4 verdict).

In dialectical-materialist language: the existence of multi-polar contradiction structure (the full would-be `T-Alg_T`) is not identical with its realization in historical practice (the reachable `T-Alg_T^{(η, p_0)}`). The ascending phase of dialectical motion — the *negation of negation* that produces qualitatively new synthesis — requires material conditions beyond those of pure gradient descent. This provides experimental and categorical grounding for Axiom 3's OP2.

---

## Appendix 2.3.A: Numerical Barrier Computation for A1

Independent SymPy verification of all critical-point quantities for `V(u) = u(u−1)²(u−4)²`:

- Minima at `u ∈ {0, 1, 4}` with `V = 0`
- Inner saddle at `u = (15 − √145)/10 ≈ 0.296`, `V(u_s_in) = 2.013`
- Outer saddle at `u = (15 + √145)/10 ≈ 2.704`, `V(u_s_out) = 13.187`
- `V''(u)` at minima: `V''(1) = 18.00`, `V''(4) = 72.00`; at saddles: `V''(0.296) = −31.41`, `V''(2.704) = −26.59`

Under A1's initialization (`|ψ|_init ≈ 1.0 ± 0.3`), `u_init ∈ [0.49, 1.69]`. The inner saddle `u_s_in = 0.296` is strictly below this range and the outer saddle `u_s_out = 2.704` strictly above; **the entire init support lies in the basin of attraction of `u=1`**. Under L²-gradient flow of the free-energy functional `F[ψ] = ∫ V(|ψ|²) + |∇ψ|² dx` (monotone `dF/dt ≤ 0`; first-order dissipative; **no kinetic-energy term**), every trajectory relaxes to `u=1` without crossing any saddle. Observed `u_max = 1.199` confirms.

Static energy ratio for reference: `V(u_s_out) / V(u_init_max) = 13.187 / 4.293 ≈ 3.07×` (linear ratio; **not** to be confused with the dynamical log-probability gap below).

Under overdamped Langevin (`γ ∂_t ψ = −∂V/∂ψ* + η`, `⟨ηη*⟩ = σ²δ`, `T_eff = σ²/(2γ)`), escape becomes a Kramers rare-event process. For `σ=0.5, γ=1 → T_eff=0.125`, the outer barrier gives `ΔV/T_eff = 105.5`; Kramers escape time `∝ exp(105.5)` exceeds the simulation horizon (`t_sim=250`) by `log₁₀(exp(105.5)/250) ≈ 43.4` — i.e. **~43 orders of magnitude (logarithmic gap, not linear ratio)**. The B1 Stage `0%` occupancy of `u=4` is therefore a **finite-time rare-event obstruction**, not an equilibrium prohibition.

For the inner barrier (`ΔV=2.013, ΔV/T_eff=16.1`), Kramers prediction yields `~9.5×10⁻⁵` expected crossings per voxel over `t_sim=250`. Observed crossing fraction is `0.85`, a discrepancy of factor `~10⁴` (i.e. ~4 orders of magnitude). This open methodological question is flagged in §4.8.3 and discussed in detail in the A1.4 verdict (`block4_5/a1_4/VERDICT.md` §5.1).

---

*Forward references*. §3 develops the explicit PDE realization of the adjunction `F ⊣ G` for MaoField's source-field construction and Ginzburg-Landau dynamics; Axioms 1–7 are realized as specific structural constraints on that realization (§3.2), and the open problems OP1 (M2 fixed-point formalization, falsified in §5.1) and OP2 (non-equilibrium extensions, refined in §5.2) are reformulated in the concrete PDE setting. The categorical vocabulary introduced here — `T-algebra`, `T-Alg_T^{(η, p_0)}`, `Δ_OP2`, the three-faces convergence of §2.3.3 — is referenced throughout §§3–5 whenever the distinction between *existent* and *realizable* structure matters.
