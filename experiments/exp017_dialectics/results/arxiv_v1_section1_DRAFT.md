# Section 1 — Introduction

*arXiv v1 first draft, 2026-04-14. Win Claude. Cross-review by Linux + independent paper-review subagent.*

---

## 1.1 The Paradigm Question

Modern artificial intelligence is overwhelmingly built on statistical pattern-matching at scale: gradient-descent training of high-parameter neural networks against large data corpora. The empirical successes are unprecedented, and we do not contest them. We do, however, observe that the same successes have not produced certain qualitatively distinct capacities — robust compositional generalization, structural transparency, sample-efficient adaptation, and explanatory reasoning over the field's own outputs — and that incremental engineering on the existing paradigm has not closed these gaps. Whether this is a temporary contingency of architecture, a fundamental limit of statistical pattern-matching, or a third possibility neither of these characterizations exhausts is, in our view, an open paradigm question.

This paper takes the third position seriously. We propose a candidate alternative paradigm — not as a replacement for statistical deep learning, but as a complementary framework for problems where structural understanding rather than predictive accuracy is the operative goal. The candidate is **field-theoretic, axiom-driven, and rooted in the methodology of dialectical materialism**.

We anticipate two skeptical reactions. First: dialectical materialism, in 20th-century practice, became a state ideology and is now widely treated as either museum-piece philosophy or politicized rhetoric — neither posture suited to mathematical or empirical work. Second: applying physics formalism to non-physical systems carries notorious risks of over-claim. We address both objections directly throughout this paper. The first by **using dialectical materialism as a methodological framework**, not a slogan, and by being explicit about which axioms are postulated and which are derived (§3.2). The second by **explicit attention to the gap between empirical pattern and rigorous physics** (§3.5, mode-tagging convention), and by foregrounding open problems rather than concealing them (§5).

## 1.2 Why a Dialectical-Materialist Method

The dialectical-materialist tradition — as developed by Marx, Engels, Lenin, and most pertinently for our purposes in the Maoist contributions of *On Contradiction* and *On Practice* — supplies four methodological commitments that directly inform the framework's design:

1. **Reflection theory** (反映论, Lenin): cognition is a structural correspondence to objective reality, not a statistical fit to observation distributions. *Realization in MaoField*: the source field `S(x)` is a deterministic encoding of the input text, not a learned compression — every voxel is interpretable in principle (Axiom 4, §3.2)
2. **Theory of contradiction** (矛盾论, Mao): internal opposition is the engine of dynamics, not external imposition. *Realization*: the field dynamics (Eq. 3.1) are autonomous; no loss function or external objective is supplied (Axiom 3)
3. **Theory of practice** (实践论, Mao): cognition deepens through practice; the corpus is a record of practice, not a sample from a population. *Realization*: the corpus is treated as practice-record (Axiom 4)
4. **Quantity-to-quality transition** (质量互变, Engels): quantitative changes can produce qualitative shifts that are not predictable from extrapolation alone. *Realization*: the framework explicitly admits and studies regime transitions (Block IV.5 Stage A1.4 in §4.9 is a direct experimental instance of this principle: a quantitative reduction in barrier height produced a qualitative loss of well structure)

These are not mere analogies. Each commitment maps to a concrete structural choice that distinguishes MaoField from a generic field-theoretic AI proposal. We argue that the convergence of these commitments produces a framework whose properties cannot be replicated by adding any single one of them to a standard pipeline.

## 1.3 The Categorical Bridge

A persistent concern with dialectical-materialist approaches has been the perceived absence of a precise mathematical infrastructure. We adopt **Lawvere's 1969 identification of adjoint functors with the Hegelian unity of opposites** (Lawvere, *Adjointness in foundations*) as the categorical bridge between dialectical motion and rigorous mathematics. An adjoint pair `F ⊣ G` formalizes the propose-return structure of thesis-antithesis; the induced monad `T = G∘F` (when fully formalized — see §2.3.3 for current status) internalizes the synthesis as a T-algebra; the Eilenberg-Moore and Kleisli categories stratify the modes of dialectical realization.

This categorical infrastructure is **not** decoration. In §2.3 we show that it carries genuine predictive content: it identifies the **source-density decomposition** (two distinct endofunctors arising from sparse vs. dense source constructions, §2.3.2), the **reachability gap** as a categorical measure of one of our open problems (§2.3.4), and the **three-faces convergence** that unifies categorical, physical, and phenomenological open problems under a single conjectured stochastic structure (§2.3.3).

## 1.4 The PDE Realization: MaoField

The framework's concrete instantiation is a Ginzburg-Landau / Allen-Cahn dynamics on a complex scalar field `ψ : Ω → ℂ` over a discrete 3D lattice (32³ voxels):

```
γ ∂_t ψ = D ∇²ψ − ∂V/∂ψ* + S(x) + η(x, t)
```

The functor `F : Text → Field` is the source-construction map (two implementations studied: byte-frequency `F_sparse` and dense embedding `F_dense`); the functor `G : Field → Score-ready` is the time-evolution to fixed point. Their composition `T = G∘F` is the source-attractor endofunctor whose categorical structure §2.3 analyzes.

The framework rests on seven axioms supplied by the principal author (§3.2). Two of these axioms remain at the level of physical intuition without canonical mathematical formalization (Axiom 6, OP1) or with refined formulation but unresolved (Axiom 3, OP2). We treat both as **open problems prominently signposted**, not as failures or evasions. A research-stage framework that conceals its own open problems is a misrepresentation of its status; we choose the alternative.

## 1.5 Empirical Status (Summary)

We report experiments on five BEIR retrieval benchmarks (NFCorpus, SciFact, FiQA, ArguAna, TREC-COVID). Key findings, detailed in §4:

- **Block I**: MaoField as PDE-based reranker yields **+14.7% to +172.3%** improvement over byte-frequency baselines across all five datasets (Table 4.1, §4.2), while underperforming SOTA cross-encoders (BGE-reranker-v2-m3) by `−11 pp` to `−32 pp`. The framework establishes its empirical envelope: meaningfully above naïve baselines, below trained SOTA, with structural advantages absent from both
- **Block II**: Kuramoto diffusive coupling (a candidate for replacing explicit fusion) is **weakly falsified** (max +18.7% gain, below pre-registered 20% threshold)
- **Block III**: Attractor enumeration converges on `k* = 2` across three independent representations, identifying a structural ceiling
- **Block IV.5**: The `k* = 2` ceiling decomposes into **two distinct mechanisms** under sparse vs. dense source fields (Stage C, §4.6); pure gradient flow cannot populate distant attractor basins (Stage A1, §4.7); isotropic Langevin succeeds for inner barriers but fails for outer barriers under finite simulation horizon (Stage B1, §4.8); the OP2 program is refined from "directed driving needed" to a three-axis co-design problem (Stage A1.4, §4.9)

The empirical contribution is **not** a SOTA performance claim. It is the **structural decomposition of a multi-attractor dynamics problem in a setting where every step admits direct mechanistic interpretation** — a property absent from the dominant paradigm.

## 1.6 Open Problems Prominently Foregrounded

Two open problems organize the framework's relationship to its own incompleteness:

- **OP1 (Axiom 6 formalization)**: the principal candidate iteration (M2) is **falsified** by 0-homogeneity (§5.1). Axiom 6 currently has no known canonical mathematical formalization. We do not claim Axiom 6 is wrong; we claim our best candidate for its mathematical capture is excluded
- **OP2 (Axiom 3 non-equilibrium extension)**: the empirical refinement from "needs non-equilibrium" to "three-fold co-design — source statistics, potential geometry, numerical scheme" (§5.2) is the central methodological contribution of this paper. Block V Phase A (§5.3) is the experimental program designed to address it

We foreground OP1 and OP2 because the contributions of §4 and §2.3 make sense only against a scaffold that includes these problems explicitly — and because the **dialectical-materialist epistemology that motivates the framework demands that "open contradictions are the engine of motion"**, a methodological self-application of Axiom 1.

## 1.7 Contributions

Five main contributions:

1. **Categorical structure** for dialectical motion in PDE-based AI: Lawvere endofunctor on `Meas` with conjectured Giry-monad lift; T-algebra reachability subcategory `T-Alg^{(η, p_0)}` as the formal measure of OP2; the **three-faces convergence** of categorical / physical / phenomenological open problems onto a single conjectured stochastic extension (§2.3)

2. **PDE-based retrieval** without retrieval-specific training: `+14.7%` to `+172.3%` improvement over byte baselines across five BEIR datasets, structurally interpretable end-to-end (§4.2)

3. **Mechanism for the `k* = 2` retrieval ceiling**: source-density decomposition reveals two distinct distributional regimes (sparse byte = phase concentration; dense BGE = amplitude bistability) under one numerical attractor count (§4.6)

4. **OP2 three-fold co-design framework**: experimental refinement of Axiom 3's open problem from a single-axis "needs non-equilibrium" formulation to a three-axis (source statistics, potential geometry, numerical scheme) problem with concrete sub-problem statements and an experimental program (§4.9, §5.2)

5. **Honest research-stage methodology**: explicit OP1/OP2 signposting, [^zn-loose] convention for finite-lattice symmetry-breaking language, mode-tagging discipline, paper-review-subagent quality assurance protocol used throughout this campaign (§3.5; the 11 errors caught and corrected by independent subagent review during the 2026-04-13–14 campaign are documented in the project's `REVIEW_*.md` files, archived alongside this paper)

## 1.8 Outline

- **§2** *Categorical Structure*: §2.1 dialectical-materialist foundation; §2.2 adjoint functors as the categorical form of opposition; §2.3 Lawvere endofunctor on `Meas`, conjectured Giry monad lift, three-faces convergence
- **§3** *Mathematical Formulation*: PDE setup, the seven framework axioms with realizations and tension points, source-attractor adjunction, OP1/OP2 statements, **§3.5 on the use of symmetry-breaking language under finite-lattice settings**
- **§4** *Experimental Evidence*: Blocks I-IV (baseline retrieval, Kuramoto coupling, attractor enumeration, source-density × operator quadrants); Block IV.5 (Stage C source-density mechanism, Stage A1 reachability failure, Stage B1 Langevin and Kramers timescale, Stage A1.4 OP2 three-fold diagnostic)
- **§5** *Roadmap*: §5.1 OP1 M2 falsification; §5.2 OP2 refined to three-fold co-design; §5.3 Block V Phase A program (A-0 reachability pre-check, A-1 source statistics, A-2 potential geometry, A-3 numerical scheme, A-joint capstone); §5.4 Phase B/C outlook; §5.5 three-stage publication plan
- **§6** *Discussion*: limitations, implications, and the methodological position of this work in relation to the broader dialectical-materialist tradition

A companion repository (https://github.com/Wangziqi0/MaoField) provides the v0.1.0 code and data release (Zenodo concept DOI `10.5281/zenodo.19550341`); reproducibility scripts are in `paper/reproduce/`.
