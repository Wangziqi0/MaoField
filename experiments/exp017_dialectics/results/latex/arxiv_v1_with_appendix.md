# MaoField: A Dialectical-Materialist Framework for Non-Statistical Semantic Representation

**Author**: Yifan Chen (Chen Yifan)
**Affiliation**: Independent Researcher
**ORCID**: [0009-0008-8344-1149](https://orcid.org/0009-0008-8344-1149)
**Repository**: https://github.com/Wangziqi0/MaoField
**Concept DOI** (v0.1.0): [10.5281/zenodo.19550341](https://doi.org/10.5281/zenodo.19550341)
**Version DOI** (v0.1.1 / this paper): [10.5281/zenodo.19550342](https://doi.org/10.5281/zenodo.19550342)
**Date**: 2026-04-20
**License**: Apache 2.0 (code); CC BY 4.0 (paper)

---

## Abstract

Deep-learning systems trained by gradient descent on statistical objectives have achieved unprecedented predictive performance, yet certain qualitatively distinct capacities — compositional generalization, structural interpretability, and autonomous semantic dynamics — remain out of reach of this paradigm. We propose **MaoField**, a candidate *complementary* framework for problems where structural understanding rather than predictive accuracy is the operative goal.

The framework's methodology is **dialectical-materialist**: four commitments from the Marx–Engels–Lenin–Mao tradition (reflection theory, theory of contradiction, practice, quantity-to-quality transition) supply non-optional structural constraints rather than slogans, and are mapped to concrete design choices (deterministic source construction, autonomous dynamics, practice-record corpus handling, regime-transition-aware evaluation).

A **categorical bridge** to rigorous mathematics is provided by Lawvere's (1969) identification of adjoint functors with the Hegelian unity of opposites; we develop the source-attractor map as an endofunctor `T_• = G∘F_•` on the category `Meas` of measurable spaces, with a conjectured Giry-monad lift `P∘T_•` as the stochastic formalization of synthesis.

MaoField's PDE realization is a Ginzburg-Landau / Allen-Cahn dynamics on a complex scalar field over a `32³` lattice. On five BEIR retrieval benchmarks, the framework improves over a byte-level lexical baseline by **+14.7% to +172.3%** while lagging SOTA cross-encoders by 10.8–32.2 pp. A four-stage diagnostic cascade reveals that a single numerical attractor count `k*=2` hides **two distinct source-density regimes** (sparse byte / dense BGE), and refines the open problem of dialectical ascent (OP2) from a single-axis "non-equilibrium extension needed" to a **three-axis co-design problem** — source statistics, potential geometry, numerical scheme.

One candidate formalization of Axiom 6 (Banach contraction M2) is **falsified**; the axiom itself remains open. We present this as a **research-stage position paper** with open problems explicitly foregrounded, not a completed theory.

**Keywords**: dialectical materialism, Ginzburg-Landau, category theory, information retrieval, position paper, Lawvere adjunction, Giry monad, Kramers rate, spontaneous symmetry breaking, complex scalar field.

**arXiv categories**: `cs.IR` (primary), `cs.AI`, `math.CT`, `cond-mat.dis-nn`.

---

## Contents

- §1 Introduction
- §2 Categorical Structure
  - §2.1 Dialectical-Materialist Foundation
  - §2.2 Adjoint Functors as the Categorical Form of Opposition
  - §2.3 Adjunction, Monad, and the Categorical Structure of Dialectical Motion
- §3 Mathematical Formulation
- §4 Experimental Evidence
- §5 Roadmap: Refined Open Problems and Block V Program
- §6 Discussion
- References
- Appendix 2.3.A: Numerical Barrier Computation for A1
- Appendix 3.A: Wirtinger Derivative Convention

---

# 1. Introduction

---

## 1.1 The Paradigm Question

Modern artificial intelligence is overwhelmingly built on statistical pattern-matching at scale: gradient-descent training of high-parameter neural networks against large data corpora. The empirical successes are unprecedented, and we do not contest them. We do, however, observe that the same successes have not produced certain qualitatively distinct capacities — robust compositional generalization, structural transparency, sample-efficient adaptation, and explanatory reasoning over the field's own outputs — and that incremental engineering on the existing paradigm has not closed these gaps. Whether this is a temporary contingency of architecture, a fundamental limit of statistical pattern-matching, or a third possibility neither of these characterizations exhausts is, in our view, an open paradigm question.

This paper takes the third position seriously. **This is a position paper**: we articulate a methodological stance and a concrete candidate framework, with open problems explicitly foregrounded, rather than asserting full formalization or SOTA performance. We propose a **complementary candidate framework** — not a replacement for statistical deep learning, but a framework for problems where structural understanding rather than predictive accuracy is the operative goal. The candidate is **field-theoretic, axiom-driven, and rooted in the methodology of dialectical materialism**. We do not seek SOTA retrieval performance; our claim is structural interpretability at useful-above-baseline performance (see §4.2).

**A note on scope**: the paper's ambition is **a methodologically distinct paradigm for artificial intelligence**, not a contribution to information retrieval per se. Retrieval is chosen as the *initial empirical domain* because it is **tractable**: query–document matching admits a well-posed fixed-point formulation, benchmarks with established baselines are available, and every step in the pipeline admits direct mechanistic interpretation. The framework's intended application scope extends well beyond retrieval — scientific hypothesis generation, safety-critical decision systems, educational / explanatory applications, and more broadly any setting where autonomous structural dynamics is the operative goal (§6.4, §6.5). Retrieval results in §4 are evidence that the framework is **empirically non-vacuous**, not the ceiling of what the framework is for.

We anticipate two skeptical reactions. First: dialectical materialism, in 20th-century practice, became a state ideology and is now widely treated as either museum-piece philosophy or politicized rhetoric — neither posture suited to mathematical or empirical work. Second: applying physics formalism to non-physical systems carries notorious risks of over-claim. We address both objections directly throughout this paper. The first by **using dialectical materialism as a methodological framework**, not a slogan, and by being explicit about which axioms are postulated and which are derived (§3.2). The second by **explicit attention to the gap between empirical pattern and rigorous physics** (§3.5, mode-tagging convention), and by foregrounding open problems rather than concealing them (§5).

## 1.2 Why a Dialectical-Materialist Method

The dialectical-materialist tradition — as developed by Marx, Engels, Lenin, and most pertinently for our purposes in the Maoist contributions of *On Contradiction* and *On Practice* — supplies four methodological commitments that directly inform the framework's design:

1. **Reflection theory** (反映论, Lenin): cognition is a structural correspondence to objective reality, not a statistical fit to observation distributions. *Realization in MaoField*: the source field `S(x)` is a deterministic encoding of the input text, not a learned compression — every voxel is interpretable in principle (Axiom 4, §3.2)
2. **Theory of contradiction** (矛盾论, Mao): internal opposition is the engine of dynamics, not external imposition. *Realization*: the field dynamics (Eq. 3.1) are autonomous; no loss function or external objective is supplied (Axiom 3)
3. **Theory of practice** (实践论, Mao): cognition deepens through practice; the corpus is a record of practice, not a sample from a population. *Realization*: the corpus is treated as practice-record (Axiom 4)
4. **Quantity-to-quality transition** (质量互变, Engels): quantitative changes can produce qualitative shifts that are not predictable from extrapolation alone. *Realization*: the framework explicitly admits and studies regime transitions (Block IV.5 Stage A1.4 in §4.9 is a direct experimental instance of this principle: a quantitative reduction in barrier height produced a qualitative loss of well structure)

These are not mere analogies. Each commitment maps to a concrete structural choice that distinguishes MaoField from a generic field-theoretic AI proposal. We conjecture that the convergence of these commitments produces a framework whose properties are not trivially replicable by adding any single one of them to a standard pipeline.

## 1.3 The Categorical Bridge

A persistent concern with dialectical-materialist approaches has been the perceived absence of a precise mathematical infrastructure. We adopt **Lawvere's 1969 identification of adjoint functors with the Hegelian unity of opposites** (Lawvere, *Adjointness in foundations*) as the categorical bridge between dialectical motion and rigorous mathematics. An adjoint pair `F ⊣ G` formalizes the propose-return structure of thesis-antithesis; the induced monad `T = G∘F` (when fully formalized — see §2.3.3 for current status) internalizes the synthesis as a T-algebra; the Eilenberg-Moore and Kleisli categories stratify the modes of dialectical realization.

This categorical infrastructure is **not** decoration. In §2.3 we show that it carries conjectural structural content: it identifies the **source-density decomposition** (two distinct endofunctors arising from sparse vs. dense source constructions, §2.3.2), the **reachability gap** as a categorical measure of one of our open problems (§2.3.4), and the **three-faces convergence** that unifies categorical, physical, and phenomenological open problems under a single conjectured stochastic structure (§2.3.3).

## 1.4 The PDE Realization: MaoField

The framework's concrete instantiation is a Ginzburg-Landau / Allen-Cahn dynamics on a complex scalar field `ψ : Ω → ℂ` over a discrete 3D lattice (32³ voxels):

```
γ ∂_t ψ = D ∇²ψ − ∂V/∂ψ* + S(x) + η(x, t)
```

The functor `F : Text → Field` is the source-construction map (two implementations studied: byte-frequency `F_sparse` and dense embedding `F_dense`); the functor `G : Field → Score-ready` is the time-evolution to fixed point. Their composition `T = G∘F` is the source-attractor endofunctor whose categorical structure §2.3 analyzes.

The framework postulates seven axioms (§3.2). Two of these axioms remain at the level of physical intuition without canonical mathematical formalization (Axiom 6, OP1) or with refined formulation but unresolved (Axiom 3, OP2). We treat both as **open problems prominently signposted**, not as failures or evasions. A research-stage framework that conceals its own open problems is a misrepresentation of its status; we choose the alternative.

## 1.5 Empirical Status (Summary)

We report experiments on five BEIR retrieval benchmarks (NFCorpus, SciFact, FiQA, ArguAna, TREC-COVID). Key findings, detailed in §4:

- **Block I**: MaoField as PDE-based reranker yields **+14.7% to +172.3%** improvement over a byte-level lexical baseline across all five datasets (Table 4.1, §4.2), while underperforming SOTA cross-encoders (BGE-reranker-v2-m3) by `−10.8 pp` to `−32.2 pp`. Additionally, removing explicit fusion yields +7.9 to +26.0 pp vs. MaoField_base on the same datasets, corroborating the Block II finding that fusion erodes discriminative signal (§4.3). The framework establishes its empirical envelope: meaningfully above naïve baselines, below trained SOTA, with structural advantages absent from both
- **Block II**: Kuramoto diffusive coupling (a candidate for replacing explicit fusion) is **weakly falsified** (max +18.7% gain, below pre-registered 20% threshold)
- **Block III**: Attractor enumeration converges on `k*=2` as a **local silhouette optimum** across three independent representations; statistical separation is weak-to-moderate (silhouette 0.037–0.223, all below the 0.25 conventional-substantive threshold), so `k*=2` is a candidate structural ceiling subject to the methodological caveats in §4.11.2
- **Block IV.5**: The `k* = 2` ceiling decomposes into **two distinct mechanisms** under sparse vs. dense source fields (Stage C, §4.6); pure gradient flow cannot populate distant attractor basins (Stage A1, §4.7); isotropic Langevin succeeds for inner barriers but fails for outer barriers under finite simulation horizon (Stage B1, §4.8; this is a timescale-vs-horizon mismatch rather than a paradigm obstruction — the two-regime framework is formalized in §4.10); the OP2 program is refined from "directed driving needed" to a three-axis co-design problem (Stage A1.4, §4.9)

The empirical contribution is **not** a SOTA performance claim. It is the **structural decomposition of a multi-attractor dynamics problem in a setting where every step admits direct mechanistic interpretation** — a property absent from the dominant paradigm.

## 1.6 Open Problems Prominently Foregrounded

Two open problems organize the framework's relationship to its own incompleteness:

- **OP1 (Axiom 6 formalization)**: the principal candidate iteration (M2) is **falsified** by 0-homogeneity (§5.1). Axiom 6 currently has no known canonical mathematical formalization. We do not claim Axiom 6 is wrong; we claim our best candidate for its mathematical capture is excluded
- **OP2 (Axiom 3 non-equilibrium extension)**: the empirical refinement from "needs non-equilibrium" to "three-fold co-design — source statistics, potential geometry, numerical scheme" (§5.2) is the central methodological contribution of this paper. Block V Phase A (§5.3) is the experimental program designed to address it

We foreground OP1 and OP2 because the contributions of §4 and §2.3 make sense only against a scaffold that includes these problems explicitly — and because the **dialectical-materialist epistemology that motivates the framework demands that "open contradictions are the engine of motion"**, a methodological self-application of Axiom 1.

## 1.7 Contributions

Five paper-level contributions. Each is a substantive finding (categorical, empirical, or methodological-foundational) rather than a pipeline-level quality-assurance practice; the latter is discussed in §6.3.

1. **Categorical structure** for dialectical motion in PDE-based AI: Lawvere endofunctor on `Meas` with conjectured Giry-monad lift as the categorical route around deterministic monad obstruction; T-algebra reachability subcategory `T-Alg^{(η, p_0)}` as the formal measure of OP2; the **three-faces convergence** of categorical / physical / phenomenological open problems onto a single conjectured stochastic extension (§2.3)

2. **Source-density mechanism for the `k*=2` retrieval ceiling**: the decomposition reveals **two structurally distinct distributional regimes** under one numerical attractor count — sparse byte = phase concentration vs. dense BGE = amplitude bistability (empirical distributional labels, finite-lattice caveat in §3.5 and footnote [^zn-loose]). A quantitative by-product central to the result: the dense BGE source mean is non-zero at `t = −17.1` (`p < 10⁻²⁵`), a **17σ violation of Laplace's detailed-balance precondition** that is both the cause of the dense-regime bistability and a concrete obstruction to naïve composition of learned embeddings with PDE-based frameworks (§4.6, §4.9; re-addressed in §6.4)

3. **OP2 refined from single-axis to three-fold co-design**: experimental refinement of Axiom 3's open problem from a single-axis "needs non-equilibrium" formulation to a three-axis (source statistics, potential geometry, numerical scheme) problem with concrete sub-problem statements and an experimental program. The refinement rests on two further findings: **(i) an inner-succeeds/outer-timescale-mismatch reframe** — isotropic Langevin succeeds on the inner barrier (`ΔV/T = 16`, observed 85% crossing at `t_sim = 250`) but fails on the outer barrier (`ΔV/T = 105.5`, Kramers escape time exceeds horizon by **~43 orders of magnitude** log-gap), establishing that the `u = 4` 0% occupancy is a **timescale–horizon mismatch** rather than a paradigm limitation; **(ii) A1 inner-barrier anomaly** — the same inner crossing exceeds the 1D Kramers prefactor prediction by **factor ~10⁴ (~4 orders)**, flagged as an open methodological question concerning field-theoretic rate theory (§4.8, §4.9, §4.10, §4.11, §5.2)

4. **OP1 M2 falsification**: the principal candidate iteration (M2) of Axiom 6's mathematical formalization is **excluded by 0-homogeneity obstruction** (§5.1). We do not claim Axiom 6 is wrong; we claim our best current candidate for its canonical mathematical capture is ruled out, and we signpost the remaining search space rather than paper over the failure. This is the framework's most explicit instance of an open problem that the research program commits to carrying forward

5. **PDE-based retrieval as empirical non-vacuity** (test-bed result, not ambition): without retrieval-specific training, `+14.7%` to `+172.3%` improvement over a byte-level lexical baseline across five BEIR datasets, `−10.8 pp` to `−32.2 pp` below SOTA cross-encoders, structurally interpretable end-to-end. The result establishes that the paradigm-level claims of contributions 1–4 are operative on a concrete dataset and not purely formal; retrieval is the test bed, not the target (§4.2, §6.4)

## 1.8 Outline

- **§2** *Categorical Structure*: §2.1 dialectical-materialist foundation; §2.2 adjoint functors as the categorical form of opposition; §2.3 Lawvere endofunctor on `Meas`, conjectured Giry monad lift, three-faces convergence
- **§3** *Mathematical Formulation*: PDE setup, the seven framework axioms with realizations and tension points, source-attractor adjunction, OP1/OP2 statements, **§3.5 on the use of symmetry-breaking language under finite-lattice settings**
- **§4** *Experimental Evidence*: Blocks I-IV (baseline retrieval, Kuramoto coupling, attractor enumeration, source-density × operator quadrants); Block IV.5 (Stage C source-density mechanism, Stage A1 reachability failure, Stage B1 Langevin and Kramers timescale, Stage A1.4 OP2 three-fold diagnostic)
- **§5** *Roadmap*: §5.1 OP1 M2 falsification; §5.2 OP2 refined to three-fold co-design; §5.3 Block V Phase A program (A-0 reachability pre-check, A-1 source statistics, A-2 potential geometry, A-3 numerical scheme, A-joint capstone); §5.4 Phase B/C outlook; §5.5 three-stage publication plan
- **§6** *Discussion*: limitations, implications, and the methodological position of this work in relation to the broader dialectical-materialist tradition

A companion repository (https://github.com/Wangziqi0/MaoField) provides the v0.1.0 code and data release (Zenodo concept DOI `10.5281/zenodo.19550341`); reproducibility scripts are in `paper/reproduce/`.



# 2. Categorical Structure

This section develops the categorical infrastructure that bridges dialectical-materialist methodology (§2.1) with rigorous mathematics via Lawvere's adjoint-functor identification (§2.2) and the source-attractor endofunctor on `Meas` (§2.3).



**Position**: §2.1 grounds the dialectical-materialist methodological commitments in the philosophical tradition; §2.2 introduces the categorical apparatus (adjoint functors) as the bridge from dialectical motion to rigorous mathematics. §2.3 formalizes the source-attractor structure as an endofunctor on `Meas`.

---

## 2.1 The Dialectical-Materialist Methodological Foundation

The methodological commitments stated in §1.2 do not float free of a tradition. They derive from a coherent body of philosophical work — Marx, Engels, Lenin, and the Maoist contributions in *On Contradiction* (1937) and *On Practice* (1937) — and they have specific structural implications for any framework that takes them seriously. We summarize the four most operative for MaoField, with explicit forward references to the formalism of §3.

### 2.1.1 Reflection Theory (反映论, Lenin)

The Leninist *Materialism and Empirio-Criticism* (1909) defends the position that cognition is a **structural correspondence between subjective representation and objective reality**, and that this correspondence is achieved through the historical practice of testing representation against reality. The implication for our framework: representation should not be a *fit* to a statistical distribution of observations (which is loss-function-driven and produces compression artifacts), but a **deterministic encoding** that preserves the structure of the input.

**Realization in MaoField**: the source field `S(x)` is constructed deterministically from each input text — `S_sparse` is byte-frequency scattering (every voxel corresponds to a specific UTF-8 byte value; position information is collapsed to frequency, so the construction is injective at the histogram level but lossy at the sequence level); `S_dense` is BGE-M3 embedding tiled (every channel directly traceable to an embedding component, even if the embedding itself was learned upstream). We do not claim sequence-level positional reconstruction; we claim every voxel value is interpretable with respect to the input. This is the structural realization of Reflection Theory at the encoding boundary.

### 2.1.2 Theory of Contradiction (矛盾论, Mao)

Mao's 1937 *On Contradiction* identifies the **internal opposition within a system as the source of its motion**. External factors are conditions; internal contradictions are causes. This implies that a dynamical system's evolution should be driven by structure intrinsic to the system, not by an externally imposed objective function.

**Realization in MaoField**: the dynamics (Eq. 3.1) are autonomous in the strict sense — the system contains no loss function, no training signal, no externally imposed gradient. The drives are: (i) the source field `S` (encoding input regularity), (ii) the potential `V` (encoding intrinsic field structure), and (iii) under non-equilibrium extension, the noise term `η` (representing thermal coupling, though see §3.2 Tension Point 2). The convergence to a fixed point is the working-out of internal contradictions among `S`, `V`, and the field's own configuration — not optimization toward a specified target.

### 2.1.3 Theory of Practice (实践论, Mao)

Mao's 1937 *On Practice* posits that **cognition deepens through repeated practice**, and that knowledge accumulates not as a static accumulation but as an iterative refinement of the practice-cognition cycle. This implies that the corpus on which a framework operates is not a *sample from a population* (the framing implicit in standard statistical learning) but a **record of practice** — and the framework's job is to extract structural invariants from this record, not to fit a generative model of how the record was sampled.

**Realization in MaoField**: the corpus is treated as practice-record (Axiom 4, §3.2). The framework's evaluation on retrieval benchmarks (Block I, §4.2) measures structural invariants (basin assignment consistency, attractor enumeration) rather than generative likelihood. We do not train an upstream model on the BEIR corpus; we treat each query-document pair as a single instance of the practice of matching, and the dynamics' fixed point as the structural outcome of that practice.

### 2.1.4 Quantity-to-Quality Transition (质量互变, Engels)

Engels's *Dialectics of Nature* (1873–1883, posthumously published 1925) and the subsequent Marxist tradition develop the principle that **quantitative changes can produce qualitative shifts that are not predictable from extrapolation alone**. The implication for system design: regime transitions must be admitted as a structural possibility, not glossed over by smoothing.

**Realization in MaoField**: the framework explicitly admits and studies regime transitions. The single most direct experimental instance is Stage A1.4 (§4.9): an engineered quantitative reduction of the potential's outer barrier — undertaken to probe whether continuity of parameter change would yield continuity of behavior — instead triggered a qualitative regime shift in which the field explored amplitudes orders of magnitude larger than the original potential admitted. §4.9.3 decomposes this regime shift into three coupled axes (source statistics, potential geometry, numerical scheme); the quantitative-qualitative discontinuity is the phenomenon, and the three-axis decomposition is its mechanism. The barrier reduction was not a continuous-improvement engineering attempt — it was an experimental probe of the regime-transition principle, and its outcome (the three-fold co-design refinement of §5.2) is precisely the kind of qualitative restructuring that quantity-to-quality transition predicts.

### 2.1.5 Three Methodological Implications

The four commitments above jointly imply three positions that distinguish MaoField from a generic field-theoretic AI proposal:

1. **No statistical fitting at the framework boundary**: source construction is deterministic; there is no end-to-end gradient that adjusts the framework's parameters against an objective. Statistical methods may appear *internally* (e.g., BGE embeddings are learned) but only as inputs that the framework subsequently subjects to its own non-statistical dynamics
2. **Open problems are constitutive of the research program**: the Theory of Contradiction implies that a closed framework — one with no internal contradictions — would be one with no source of motion. We expose OP1 and OP2 prominently (§5) because their persistence is the framework's evidence of life
3. **Regime transitions are first-class objects**: Stage A1.4 (§4.9) is not an "experimental error" or a "failed attempt"; it is the framework's own demonstration of the quantity-to-quality principle in action. The three-fold co-design refinement of OP2 is the framework's response to this transition

These three positions — together with Lawvere's categorical bridge (§2.2) — define the operational space within which MaoField's specific choices (PDE form, axioms, source constructions) can be evaluated.

---

## 2.2 Adjoint Functors as the Categorical Form of Opposition

A persistent obstacle to the mathematical respectability of dialectical methods has been the perceived absence of a formal apparatus that captures the structure of opposition without collapsing into either idealist abstraction or rhetorical analogy. This obstacle was substantially addressed by **Lawvere's 1969 identification of adjoint functors with the Hegelian unity of opposites** (*Adjointness in foundations*, Dialectica 23:281–296). We adopt this identification as the categorical foundation of our framework.

### 2.2.1 Adjunctions Recall

For categories `C` and `D`, an **adjunction** `F ⊣ G` consists of functors `F : C → D` and `G : D → C` together with a natural bijection

```
Hom_D(F(c), d) ≅ Hom_C(c, G(d))                                       (2.1)
```

for all objects `c ∈ C` and `d ∈ D`. Equivalently, an adjunction is specified by two natural transformations — the **unit** `η : Id_C ⇒ G∘F` and the **counit** `ε : F∘G ⇒ Id_D` — satisfying the **triangle identities**:

```
(εF) ∘ (Fη) = id_F          and          (Gε) ∘ (ηG) = id_G            (2.2)
```

The triangle identities encode the **closure** of the propose-return cycle: composing the propose (`F`) with the unit (`η`) and the counit (`ε`) recovers `F`; symmetrically for `G`.

### 2.2.2 Lawvere's Identification

Lawvere's contribution was to identify the structure (2.1)–(2.2) with the Hegelian dialectical structure of *unity of opposites*:

- `F` is the **propose** functor (the moment of *thesis*, "立"): it sends each object of `C` to its image in `D`. In dialectical-materialist language, `F` is the practice that actively constitutes a representation
- `G` is the **return** functor (the moment of *antithesis*, "破"): it sends each object of `D` back to `C`. In dialectical-materialist language, `G` is the reflection that re-grounds the proposed representation in its source category
- The **unit** `η : Id_C ⇒ G∘F` captures the **non-trivial return**: an object `c ∈ C`, after being proposed into `D` and returned to `C`, is in general *not* identical to `c`. The discrepancy `c → (G∘F)(c)` encodes how the propose-return cycle changes the original
- The **counit** `ε : F∘G ⇒ Id_D` symmetrically captures the discrepancy on the `D` side
- The **triangle identities** encode the **closure of the dialectical cycle**: the propose-return-propose composition recovers the original propose, and symmetrically. This closure is the categorical form of dialectical determinism — the cycle is internal, not arbitrary

This identification is **rigorous**: each element of the dialectical structure (thesis, antithesis, closure) maps to a precise categorical element (functor, natural transformation, identity). It is also **non-trivial**: not every adjunction is a useful dialectical structure (most are degenerate; the structure becomes substantive only when `F`, `G` are non-isomorphism functors), and the dialectical reading constrains which adjunctions are physically meaningful.

### 2.2.3 The Monad as Internalized Dialectic

The composite `T := G∘F : C → C` is, when fully formalized as a **monad**, the internalization of the entire dialectical cycle within `C`. The monad multiplication `μ := G·ε·F : T² ⇒ T` collapses two iterations of the propose-return cycle into one, formalizing the *iterative deepening* of dialectical motion. A **T-algebra** `(X, α: TX → X)` is an object of `C` that is fixed under the iterated cycle — the categorical form of **synthesis** (Aufhebung), in which the propose-return motion has stabilized into a self-consistent structure.

§2.3 develops this construction for MaoField's source-attractor dynamics, identifying:

- the explicit functors `F_sparse, F_dense, G` for the byte and dense source constructions,
- the conjectured Giry-monad lift required to upgrade the deterministic endofunctor `T_•` to a genuine monad (§2.3.3),
- the **reachability subcategory** `T-Alg^{(η, p_0)}` that distinguishes existent from realizable dialectical structures (§2.3.4),
- and the **three-faces convergence** that links our categorical, physical, and phenomenological open problems under a single conjectured stochastic structure (§2.3.3).

### 2.2.4 What the Categorical Bridge Buys Us

We close §2.2 with an explicit statement of what the categorical bridge accomplishes — and what it does not.

**It does provide**: a precise vocabulary for describing dialectical motion (`F ⊣ G`, `η`, `ε`, `T`-algebra) that is shared with other branches of mathematics; a language in which the framework's structural commitments can be checked against well-understood categorical theorems (e.g., the existence of T-algebras under the Eilenberg-Moore construction, the compositional behavior of adjunctions); and a setting in which open problems can be precisely formulated (§2.3.4's `Δ_OP2` as cardinality complement is one such formulation).

**It does not provide**: a guarantee that the dialectical-materialist commitments of §2.1 are uniquely realized by the categorical formalism (other categorical structures may admit dialectical readings); a substitute for empirical work (the categorical structure must be *realized* in a concrete dynamics, and §3 onward make this realization explicit); or a complete formalization of the framework's open problems (§2.3.3 explicitly notes that the monad structure is conjectured, not proven, in the deterministic case).

The categorical bridge is **a methodological instrument**, not a foundational guarantee. In §2.3 we show that it is sharp enough to identify structural decompositions (source-density), reachability gaps (`Δ_OP2`), and convergences across apparently independent open problems (three-faces) — these are the deliverables we claim. The bridge is **not** a proof that MaoField is the unique categorical realization of dialectical materialism, and we do not claim it is.

---

*Forward reference*. §2.3 below develops the explicit monad-theoretic structure of MaoField's source-attractor dynamics, including the source-density decomposition into two endofunctors `T_sparse` and `T_dense` (§2.3.2), the explanation of why deterministic gradient flow does not admit a monad structure and what stochastic extension is required (§2.3.3), and the categorical formalization of OP2 as a reachability gap in the T-algebra category (§2.3.4).

## 2.3 Adjunction, Monad, and the Categorical Structure of Dialectical Motion



**Position**: position-paper-level identification. The bare endofunctor picture on `Meas` is rigorous; the monad lift via Giry is conjectured and reserved for follow-up work. All `Z_n` labels follow the loose-sense convention defined in §3.5 and footnote `[^zn-loose]`.

---

## 2.3.1 From Adjunction to Monad: The Closure of Dialectical Operation

An adjoint pair `F ⊣ G` between categories `C` and `D` expresses a primitive form of dialectical opposition: `F` *proposes* objects of `C` into `D` (the moment of **thesis**, "立"), while `G` *returns* objects of `D` back into `C` (the moment of **antithesis**, "破"). The adjunction is constituted by two natural transformations — the **unit** `η: Id_C ⇒ G∘F` and the **counit** `ε: F∘G ⇒ Id_D` — satisfying the triangle identities, which encode the **closure** of the propose-return cycle.

The composition `T := G∘F : C → C` is, when fully formalized, a **monad** with multiplication `μ := G·ε·F : T² ⇒ T`. Whereas the adjunction alone describes a single dialectical oscillation, the monad `T` internalizes the *iterative* dialectical process entirely within `C`. A **T-algebra** `(X, α: TX → X)` is precisely an object that has reached a self-consistent state under this iteration — it is the categorical form of the **synthesis**[^aufhebung]: not a third point adjoined, but a structural invariant of the propose-return-reintegrate cycle. The Kleisli and Eilenberg-Moore categories of `T` stratify the algebras by their mode of realization.

[^aufhebung]: *Synthesis* (Aufhebung in Hegelian terminology, capturing the dual sense of cancellation and preservation; often mistranslated as "combination", which loses the negation-of-negation structure). The T-algebra formalization preserves this dual structure: the algebra map `α: TX → X` both *absorbs* (cancels) the monadic iteration and *retains* (preserves) its action as an endomorphism.

This framing is due to Lawvere (1969); our contribution is to **propose** a physical realization of the structure under PDE dynamics and to **identify** two subtleties that pure categorical abstraction elides: the **decomposition of the operator F by source density** (§2.3.2), and the **failure of deterministic gradient flow to satisfy monad axioms** (§2.3.3). We do not claim our realization is the unique or the canonical one; we claim it is rigorous at the endofunctor level and that its open problems organize a coherent research program.

## 2.3.2 Two Paths, Two Endofunctors: The Source-Density Decomposition

MaoField implements the functor `F` via a source-field construction `Text → Field ∈ ℂ^N`. Our experiments reveal that this construction **is not unique**, and that the specific realization determines the algebraic structure.

Let `F_sparse : Text → Field` denote the byte-frequency construction (UTF-8 bits scattered over the 32³ grid, ~10% occupancy), and let `F_dense : Text → Field` denote the dense construction via a pretrained embedding (here BGE-M3, tiled to full grid coverage). With a common `G : Field → Score-ready representation` (Ginzburg-Landau gradient flow to fixed point), the composition `G∘F_•` properly spans three distinct layers (Text, Field, Score-ready). To discuss categorical structure, we embed all three as subcategories of an ambient category `Meas` of measurable spaces, extending `F_•, G` by identity outside their natural domains so that `G∘F_• : Meas → Meas` becomes a well-defined endofunctor. Under this embedding we obtain two composite **endofunctors** (the lift to genuine monads is reserved for §2.3.3 and footnote [^giry-monad]):

- `T_sparse := G∘F_sparse`: phase concentrated (`|R|_per-doc = 0.84`), U(1) broken in the empirical distribution but not antipodally split — `Z_2` not realized in the phase sector. Phase concentration to a narrow band (kmeans-2 center distance 26.2°). See §4.6 for full diagnostics.
- `T_dense := G∘F_dense`: amplitude bimodal at `|ψ|∈{0,1}`, phase much less concentrated (`|R|_per-doc = 0.20`, still non-uniform vs uniform-baseline 0.006). `V=¼(|ψ|²−1)²` admits only `|ψ|=1` as a true minimum; `|ψ|=0` is an unstable fixed point with `V(0)=¼ ≠ V(1)=0`, so no `Z_2` group action interchanges the two basins. The "amplitude bistability" is a **distributional pattern, not a group-theoretic claim**.

Numerically both yield `k*=2`. **Categorically they correspond to distinct endofunctors**: `T_sparse`'s candidate Kleisli category is phase-degenerate; `T_dense`'s is amplitude-stratified.[^functor-future] The claim that "dialectical closure is determined by the operator alone" is refuted by this decomposition — **the source-field functor `F` co-determines the algebra structure**. This is a categorical formulation of the materialist thesis that *practice (the mode of source-field construction) conditions the forms of cognitive closure*.

[^functor-future]: This is a *conjectured* categorical interpretation based on the experimental phase/amplitude observations; a fully rigorous functorial treatment (e.g., explicit functors to `Z_n`-equivariant categories indexed by the broken symmetry pattern) is left to future work.

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

[^giry-monad]: Concretely, `Meas` is the category of measurable spaces with measurable maps; Text, Field, and Score-ready objects are embedded via their natural σ-algebras (discrete for Text, Borel for the ℂ^N Field, Borel for Score). Deterministic maps `F_•, G` extend to identity on the complement, so `T_• := G∘F_•` is a bona fide endofunctor of `Meas`. The Giry monad `P` is the standard probability-measure monad on `Meas` (Giry 1982; Jacobs 2010): for measurable space `(X, Σ_X)`, `P(X)` is the space of probability measures on `(X, Σ_X)` with the σ-algebra generated by evaluation maps `μ ↦ μ(A)` for `A ∈ Σ_X`; the unit `η_X : X → P(X)` is the Dirac map `x ↦ δ_x`; the multiplication `μ_X : P(P(X)) → P(X)` is the marginalization `Π ↦ ∫ν dΠ(ν)`. The conjectured lift `P ∘ T_•` of our endofunctor would carry the (η, μ) of `P` provided the natural-transformation diagrams compose; verifying or disproving this is OP1's category-theoretic component, related to but distinct from the M2-falsification of OP1's analytic component (see §5.1).

## 2.3.4 Reachability: The Categorical Measure of Open Problem 2

The source-density decomposition in §2.3.2 locates the choice of algebra structure at the functor `F`. A second, independent axis of constraint emerges from the **dynamics**: even when the target algebraic structure is in-principle present in `T-Alg_T` (the category of T-algebras under the conjectured monad lift), the dynamics of MaoField may fail to reach it. Stage A1 of our diagnostic cascade (§4.7) makes this concrete.

When `V(ψ)` is extended from the double-well `¼(|ψ|²−1)²` to a triple-well `|ψ|²(|ψ|²−1)²(|ψ|²−4)²`, the would-be T-algebra category gains additional objects corresponding to the `|ψ|=2` basin. However, under gradient-flow dynamics initialized from `|ψ|_init ≈ 1.0 ± 0.3`, the observed occupancy of the `|ψ|=2` basin is **0.00%** (99.15% at `|ψ|=1`, 0.85% at `|ψ|=0`). The `u=4` algebras exist in the theory but are not realized in the experiment.

This motivates the following refinement. Define the **reachable subcategory** under a unit `η` and an initial distribution `p_0`:

> `T-Alg_T^{(η, p_0)} := { (X, α) ∈ T-Alg_T | ∃ x_0 ∈ supp(p_0), η_{x_0} generates a Kleisli-reachable path to (X, α) via μ }`

In general `T-Alg_T^{(η, p_0)} ⊊ T-Alg_T`. We propose the **categorical gap**

> `Δ_{OP2} := |T-Alg_T| ⊖ |T-Alg_T^{(η, p_0)}|`

as the **formal measure of Open Problem 2**: the unrealized algebraic potential of dialectical structures that are *mathematically present* in the (conjectured) monad but *dynamically unreachable* under descending-only (gradient-flow) evolution.[^delta-op2-alt]

Two technical caveats are required for `Δ_{OP2}` to be well-defined:

(i) **The notation `⊖`** denotes full-subcategory complement: `Δ_{OP2}` is intended as the (essentially small) full subcategory of `T-Alg_T` whose objects do **not** lie in `T-Alg_T^{(η, p_0)}`, equipped with the inherited morphisms. `|·|` is then the cardinality (or, for proper-class issues, the cardinality after restriction to a Grothendieck universe), or — preferably — a coarser invariant such as groupoid cardinality `Σ 1/|Aut|` over isomorphism classes.

(ii) **`T-Alg_T` may be a proper class** in the absence of a small-set ambient universe; we restrict attention to `T-Alg_T ∩ U` for a suitable universe `U` containing all algebra structures of finite presentation under the conjectured monad lift, and treat the cardinality of the complement within this restricted setting. Footnote [^delta-op2-alt] acknowledges that other quantifications (categorical entropy, persistent-homology dimension of the unreached manifold, Kan extension obstructions) are equally valid and conjecturally agree in a common limit; the cardinality complement is a symbolic first pass.

The "Kleisli-reachable path" condition in the definition of `T-Alg_T^{(η, p_0)}` should be read as: there exists a finite composition of Kleisli morphisms (under the conjectured monad lift; see §2.3.3) starting from a unit of an element in `supp(p_0)` and reaching the algebra `(X, α)` as an object. This is a categorical translation of the dynamical reachability condition; rigorous formulation requires the Kleisli composition `g ∘_K f := μ ∘ Tg ∘ f` of the conjectured Giry-monad lift and is reserved for follow-up work.

[^delta-op2-alt]: `Δ_{OP2}` as defined above uses cardinality complement as a symbolic first pass; alternative quantifications — categorical entropy, persistent-homology dimension of the unreached manifold (Adams et al., giotto-tda 2021), Kan extension obstructions — remain follow-up work. The qualitative invariant — the gap between *existent* and *realizable* T-algebras — is conjectured (not proven) to be stable across these choices. Closing this gap is one component of OP2 (§5.2); the other component is the empirical co-design refinement identified in §4.9 (A1.4 verdict).

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

# 3. Mathematical Formulation

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

The MaoField framework postulates seven axioms. These are not derived; they are postulates whose consequences (and limits) the paper explores. Each axiom is stated, followed by its concrete realization in the formalism of §3.1, and (where applicable) its connection to an open meta-problem (OP1 or OP2).

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

The composition `T_• := G∘F_•` becomes a well-defined endofunctor of the ambient category `Meas` (§2.3.2). We do **not** claim `T_•` is a monad in the deterministic case; the lift to a Giry-monad `P ∘ T_•` is conjectured and reserved for follow-up work (§2.3.3 and footnote [^giry-monad] thereof). For the present paper, all categorical statements involving `T_•` are read as endofunctorial; statements requiring monad axioms (T-algebras, Kleisli, EM) are flagged "conjectured under monad lift."

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

# 4. Experimental Evidence

**Scope**: this section reports all empirical evidence for MaoField's core claims, organized around the four canonical hypotheses (H1–H3 + OP1/OP2 diagnostic) introduced in Section 3. All `Z_n` symbols are used in the **empirical distributional sense** defined in footnote [^zn-loose]; finite-lattice caveats (Section 3.5) apply throughout.

**Mode tags** (after Linux internal convention, following a documented bug-prevention protocol):
- `[STATIC]`: landscape geometry (critical points, Hessian, barrier heights)
- `[DYNAMIC-EQUILIBRIUM]`: Boltzmann / Laplace stationary distribution predictions
- `[DYNAMIC-RARE-EVENT]`: Kramers escape rate, horizon comparisons
- `[DYNAMIC-IMPLEMENTATION]`: numerical scheme, CFL, boundary conditions, source statistics

---

## 4.1 Setup and notation

**Common configuration** across Blocks I–V.5:

- PDE engine: `ComplexEngine` (exp015), Ginzburg-Landau Allen-Cahn form `γ·∂_t ψ = D ∇²ψ − ∂V/∂ψ* + S(x) + η(t)`, `γ=1`, `D=0.1`
- Default potential: `V(ψ) = ¼·(|ψ|² − 1)²` (standard GL double-well)
- Grid: 3D toroidal lattice, `32³ = 32768` voxels, periodic BC, `dx=1`
- Integrator: explicit Euler, `dt=0.05` (unless noted), steps=5000 for reranker or 2000 for Block II
- Candidate pool: BM25 top-K, K ∈ {6, 20, 100}
- Clamp: `|a|, |b| ≤ 3.0` (i.e. `|ψ|² ≤ 18`) as numerical safeguard; flagged as `[DYNAMIC-IMPLEMENTATION]` artifact where it contributes
- Datasets: BEIR subset `{NFCorpus, SciFact, FiQA, ArguAna, TREC-COVID}`; mMARCO and CodeSearchNet experiments exist in the exp017 archive but are not reported in this paper as the five-BEIR set already covers the hypothesis space relevant to §4
- Evaluation: `nDCG@10, P@10, MRR@10`, BEIR standard
- Hardware: EPYC 7B13 256-core CPU, RX 9070 XT for embeddings (bge-m3, bge-reranker-v2-m3 via llama.cpp)
- Random seeds: 20260412 / 20260413

**Notation**:
- `u ≡ |ψ|²` (scalar amplitude-square radial coordinate)
- `T_eff ≡ σ²/(2γ) = σ²/2` (effective temperature under Langevin noise)
- `⟨·⟩_k` denotes ensemble mean over (documents × voxels) in basin *k*

---

## 4.2 Block I — Baseline retrieval across 5 BEIR datasets

We report `nDCG@10` for six scorers on five datasets to locate MaoField's position in the retrieval performance landscape. Scorers: BM25 (sparse), S1 (byte-ngram baseline), S4 (trigram baseline), BGE-reranker-v2-m3 (SOTA cross-encoder), MaoField_base (PDE with fusion), MaoField_E (PDE without fusion, reranker-only).

**Table 4.1**: `nDCG@10` matrix, 5 datasets × 6 scorers.

| Dataset | BM25 | S1 byte | S4 3-gram | BGE-reranker | MaoField_base | MaoField_E |
|---|---:|---:|---:|---:|---:|---:|
| NFCorpus | 0.3063 | 0.1366 | 0.2401 | 0.3104 | 0.0565 | **0.2026** |
| SciFact | 0.6594 | 0.1920 | 0.4110 | 0.6223 | 0.0403 | **0.3002** |
| FiQA | 0.2167 | 0.0686 | 0.1163 | 0.2992 | 0.0294 | **0.1082** |
| ArguAna | 0.2838 | 0.0556 | 0.2085 | 0.4560 | 0.0289 | **0.1514** |
| TREC-COVID | 0.5589 | 0.4299 | 0.3962 | 0.7257 | 0.3553 | **0.4932** |

**Observations**:

1. MaoField_E vs S1 (byte baseline): 5/5 datasets positive gain, **+14.7% to +172.3%** relative improvement
2. MaoField_E vs BGE-reranker: 5/5 datasets lag behind SOTA by −10.8 to −32.2 pp
3. MaoField_E vs MaoField_base: consistent +7.9 to +26.0 pp improvement from removing fusion (see §4.3 below)
4. BGE-reranker underperforms BM25 on SciFact by −3.7 pp, confirming SOTA cross-encoders have weak domains

**Status**: MaoField_E represents a working PDE-based reranker, significantly above naïve byte baselines and below SOTA. This establishes the empirical envelope within which subsequent Block analyses operate.

---

## 4.3 Block II — Kuramoto diffusive coupling (H1 test)

**Hypothesis H1** (*movement to fusion*): Replacing explicit fusion with Kuramoto-type diffusive coupling `∂_t ψ_q = GL(ψ_q) + g·(ψ_d − ψ_q)` (co-evolving query and document fields for 2000 steps) should improve performance by ≥20%.

**Table 4.2**: `nDCG@10` at coupling-scan optimum `g_best`.

| Dataset | Pool | `g=0` | `g_best` | best `g` | Relative gain |
|---|---|---:|---:|---:|---:|
| NFCorpus | top-6 | 0.2201 | 0.2252 | 1.0 | +2.3% |
| NFCorpus | top-20 | 0.1712 | 0.1712 | 0.0 | 0.0% |
| SciFact | top-6 | 0.4082 | 0.4362 | 0.05 | +6.9% |
| SciFact | top-20 | 0.1836 | 0.2179 | 0.05 | **+18.7%** |

**H1 verdict (weak falsification)**: Maximum observed gain 18.7%, below the pre-registered 20% threshold. `g_c` does not coincide across datasets (NFC 1.0 vs SciFact 0.05). Coupling helps modestly but does not replace fusion as hypothesized.

**Independent confirmation from Block I**: MaoField_E (no fusion) outperforms MaoField_base (with fusion) by +7.9 to +26.0 pp. **Fusion actively degrades signal** on 5/5 datasets, consistent with the hypothesis that evolving query-document fields together erodes discriminative information.

---

## 4.4 Block III — Attractor enumeration (H2 test)

**Hypothesis H2** (*contradiction, primary/secondary, qualitative change*): The number of effective attractors `k*` is bounded and small; this explains the top-20 vs top-100 performance ceiling.

**Methodology**: For NFCorpus 100 docs, evolve each independently for 5000 steps with byte source, cluster final `(a, b)` fields via k-means over three representations. Select `k*` as the silhouette-optimal cluster count over `k ∈ {2,...,5}`.

**Table 4.3**: Silhouette-optimal attractor count.

| Representation | Dimension | `k*` | Silhouette |
|---|---:|---:|---:|
| `raw_ab` | 65536 | **2** | 0.214 |
| amplitude `|ψ|` | 32768 | **2** | 0.037 |
| phase `(cosφ, sinφ)` | 65536 | **2** | 0.223 |

**H2 verdict (confirmed, with statistical caveat)**: All three representations converge on `k*=2`. However, silhouette values `0.037–0.223` are weak-to-moderate; `< 0.25` is conventionally interpreted as "no substantial cluster structure." We thus claim `k*=2` as the **local silhouette optimum** rather than a strongly-separated attractor count. See §4.11 for open statistical questions.

The invariance of `k*=2` across representations motivates the Section 4.6 diagnostic: if amplitude and phase both give `k*=2`, the underlying symmetry-breaking mechanism may yet differ.

---

## 4.5 Block IV — Source-density × operator-symmetry (H3 test)

**Hypothesis H3** (*material starting point*): Under the same PDE operator, byte sources (materialist) and learned embedding sources (idealist) produce different attractor structures.

**Four-quadrant setup**: byte or BGE source × PDE-dynamic or static-cosine evaluation.

**Table 4.4**: `nDCG@10` and diagnostics across four quadrants.

| Dimension | Dataset | IV-A byte+PDE | IV-B BGE+PDE | IV-C BGE cos | IV-D byte cos |
|---|---|---:|---:|---:|---:|
| Overall `nDCG@10` | NFCorpus | 0.2026 | 0.2495 | **0.3089** | 0.2159 |
| Overall `nDCG@10` | SciFact | 0.3002 | 0.3814 | **0.6143** | 0.3555 |
| Overall `nDCG@10` | FiQA | 0.1082 | 0.1901 | **0.2774** | 0.1309 |
| Long-tail `nDCG@10` | NFC (n=227) | 0.2117 | 0.2608 | **0.3149** | 0.2264 |
| Long-tail `nDCG@10` | FiQA (n=29) | 0.1404 | 0.1551 | **0.2199** | 0.1341 |
| Robustness drop | SciFact ±200 | −0.010 | +0.011 | −0.015 | +0.031 |
| Attractor `k*` (raw-ab only)† | NFC 100 docs | **2** (sil 0.13) | **2** (sil 0.06) | N/A | N/A |

† These silhouette values are for the `raw_ab`-only clustering in a paired IV-A vs IV-B comparison on NFCorpus 100 docs; they are numerically lower than the Block III §4.4 triple-representation scan (`raw_ab` 0.214, `amplitude` 0.037, `phase` 0.223) because Block III reports each representation independently with per-representation optimization, while Block IV uses a common feature space to enable cross-source comparison. Both analyses confirm `k*=2`; only the silhouette magnitudes differ by cluster-space choice.

‡ SciFact long-tail (n=3) row omitted from this table due to insufficient sample; see `FINAL_REPORT.md` §2.4 for the raw numbers if needed.

**Observations**:

1. Overall ranking consistent across three datasets: `IV-C > IV-B > IV-D > IV-A`
2. Within-source-type: IV-A (byte+PDE) underperforms IV-D (byte cos) by −1.3 to −5.5 pp; IV-B (BGE+PDE) underperforms IV-C (BGE cos) by −5.9 to −23.3 pp
3. **`k*=2` holds in both IV-A and IV-B**, across source-density extremes
4. Robustness drops all `|Δ| < 0.04` — within noise

**H3 verdict (partial support)**: Source-density does affect retrieval scores but does **not** produce different `k*`. The surface-level `k*=2` identity across byte and BGE raises a mechanistic question: does the `Z_2` structure arise from the *same* or *different* symmetry breaking in the two source regimes? Stage C (§4.6) addresses this.

---

## 4.6 Stage C — Two regimes of `k*=2`

**Motivation**: `k*=2` holds for both byte and BGE sources. If the underlying mechanism differs, Stage C's phase diagnostic will resolve it.

### 4.6.1 Method

Compute for both IV-A and IV-B final states:
- Global phase circular mean resultant `|R|` (0 = uniform on S¹, 1 = full lock)
- Per-document `⟨|R|⟩` (average over documents of within-document phase concentration)
- 100-document circular-mean phases, k-means on sine/cosine, measure antipodal separation angle (expected 180° for pure `Z_2` phase inversion)

### 4.6.2 Results [STATIC]

**Table 4.5**: Phase diagnostic for IV-A vs IV-B.

|  | Global `|R|` | χ²/72 | Per-doc `⟨|R|⟩` | k-means centroid separation |
|---|---:|---:|---:|---:|
| **IV-A (byte)** | **0.807** | 94989.7 | **0.840** | **26.2°** (not antipodal) |
| **IV-B (BGE)** | 0.165 | 4879.9 | 0.197 | 81.4° (not antipodal) |

### 4.6.3 Interpretation [STATIC]

**IV-A (byte, sparse source)**: `⟨|R|⟩=0.84` indicates strong phase concentration within each document. The 100-document circular means fall into a narrow 26.2° fan. **The U(1) phase symmetry is empirically broken** in the sense that the observed `arg(ψ)` distribution is statistically distinguishable from uniform (χ² ≫ 1). However, the absence of antipodal separation (26° ≠ π rad) **rules out rigorous `Z_2 ⊂ U(1)` phase inversion** as the operative mechanism. The pattern is better described as "phase concentration to one preferred direction" — a broken U(1) without a surviving discrete subgroup.

**IV-B (BGE, dense source)**: `⟨|R|⟩=0.20` indicates much weaker phase concentration (still non-uniform; χ² = 4880 rejects uniformity strongly, but the phase modulation is weak relative to byte). Amplitude exhibits a bimodal distribution at `|ψ|∈{0,1}`. Note that `V=¼(|ψ|²−1)²` admits only `|ψ|=1` as a true minimum; `|ψ|=0` is a critical point with negative-definite Hessian (unstable fixed point, since `V(0)=¼ ≠ V(1)=0`). Hence `|ψ|=0` and `|ψ|=1` **do not lie on the same U(1) orbit** and cannot be interchanged by any `Z_2` group action respecting the potential. The "amplitude bistability" is a bimodal distributional pattern, not a strict `Z_2` amplitude symmetry breaking [^zn-loose].

### 4.6.4 `k*=2` in two regimes

The `k*=2` identity across IV-A and IV-B hides **two distinct distributional regimes**:

- Byte: phase concentration into a narrow fan; amplitude roughly unimodal
- BGE: amplitude bimodal at `|ψ|∈{0,1}`; phase weakly modulated

We label these "byte Z₁ regime" and "BGE Z₂ regime" in the loose sense of footnote [^zn-loose], but emphasize the labels are **distributional descriptors, not group-theoretic claims**. The empirical finding — that a single silhouette-optimal `k*=2` conceals two physically distinct mechanisms — is robust independent of labelling convention.

**Status**: H3 receives refined support. Source density does affect the *mechanism* of attractor structure while preserving the *count*.

---

## 4.7 Stage A1 — Multi-well amplitude intervention

**Intervention hypothesis**: If BGE's `k*=2` arises from amplitude bistability, introducing additional amplitude wells in `V` should increase `k*`.

**Setup**: Replace default `V=¼(|ψ|²−1)²` with triple-well `V(u) = u(u−1)²(u−4)²`, minima at `u = |ψ|² ∈ {0, 1, 4}` (i.e., `|ψ|∈{0, 1, 2}`). BGE-M3 embedding source, NFCorpus 100 docs (70 with cached embeddings), init `|ψ|_init ≈ 1.0 ± 0.3`, all other parameters matching IV-B.

**Stability**: 0 NaN, `u_max=1.20`, `u_mean=1.01`, 5000 steps fully stable.

### 4.7.1 Amplitude occupancy

**Table 4.6**: Observed occupancy across three wells.

| Well | `|ψ|` | `u=|ψ|²` | Observed occupancy |
|---|---|---|---:|
| Inner | 0 | 0 | **0.85%** |
| Middle | 1 | 1 | **99.15%** |
| Outer | 2 | 4 | **0.00%** |

The outer well is **not populated** under gradient flow from this initialization.

### 4.7.2 Barrier analysis [STATIC]

**Table 4.7**: Critical-point structure of the triple-well potential (independent SymPy verification).

| Point | `u` | `V` | `V''(u)` |
|---|---:|---:|---:|
| Min (boundary) | 0.0000 | 0.000 | — (linear `V≈4u`) |
| Saddle (inner) | 0.2958 | **2.013** | −31.41 |
| Min | 1.0000 | 0.000 | +18.00 |
| Saddle (outer) | **2.7042** | **13.187** | −26.59 |
| Min | 4.0000 | 0.000 | +72.00 |

**Barrier asymmetry**: `V(saddle outer) / V(saddle inner) = 13.187 / 2.013 = 6.55×`.

### 4.7.3 Gradient-flow inaccessibility of `u=4` [DYNAMIC-EQUILIBRIUM]

Under pure gradient flow (`γ · du/dt = −∂V/∂u`, first-order dissipative, **no kinetic-energy term**), `V` is monotonically non-increasing along trajectories. Initialization `u_init ∈ [0.49, 1.69]` lies **entirely within the basin of attraction of `u=1`** (inner saddle `u_s_in=0.296` is left of init range, outer saddle `u_s_out=2.704` is right). Hence no trajectory can reach the `u=4` basin under gradient flow alone. Observed `u_max=1.199` confirms.

For reference, the **static energy ratio** is `V(saddle outer) / V(u_init_max) = 13.187 / V(1.69) = 13.187 / 4.293 ≈ 3.07×`. Since gradient flow is monotonically non-increasing in V and `V(u_init_max) < V(saddle)`, the `u=4` basin is **analytically unreachable** under pure gradient flow — not an experimental surprise but a direct consequence of the static energy landscape geometry.

**A1 verdict**: Adding wells to `V` does not mechanically add attractors in the observed distribution. Populating the new wells requires either (i) initialization spanning multiple basins, (ii) a non-equilibrium mechanism (Langevin, Hamiltonian, active), or (iii) a structural change to `V` that brings the new minima into the gradient-connected region. This motivates Stage B1.

---

## 4.8 Stage B1 — Langevin σ-scan with Kramers timescale analysis

**Motivation**: Test whether adding isotropic Gaussian noise (`η(t)` with `⟨ηη*⟩ = σ²δ`) enables barrier crossing to the `u=4` basin.

**Setup**: same as A1 but with Langevin SDE `γ ∂_t ψ = −∂V/∂ψ* + S + η`. Scan `σ ∈ {0, 0.1, 0.5, 1.0, 2.0}`.

### 4.8.1 Observed occupancy

**Table 4.8**: Basin occupancy across σ-scan on triple-well `V = u(u-1)²(u-4)²`.

| σ | `u_max_all` | `u_mean_all` | near `u=0` | near `u=1` | near `u=4` | clamped |
|---|---:|---:|---:|---:|---:|---:|
| 0.0 | 1.19 | 1.01 | 0.8% | 99.2% | **0.0%** | 0.0% |
| 0.1 | 1.34 | 1.00 | 1.3% | 98.7% | **0.0%** | 0.0% |
| 0.5 | 18.00 | 0.17 | **85.0%** | 13.4% | **0.0%** | 0.0% |
| 1.0 | 18.00 | 17.21 | 1.9% | 1.8% | 0.0% | 95.4% |
| 2.0 | 18.00 | 18.00 | 0.0% | 0.0% | 0.0% | 100.0% |

### 4.8.2 Kramers timescale analysis [DYNAMIC-RARE-EVENT]

**Two-regime analytical framework**: we apply the Kramers rate formula for overdamped Langevin in 1D,

```
k_{i→j} = (1/(2π·γ))·√(V''(min_i) · |V''(saddle_ij)|) · exp(−ΔV_ij / T_eff)
```

valid when `ΔV/T_eff ≫ 1` (typically ≥ 5). The *expected number of crossings* over the simulation horizon `t_sim = steps · dt = 5000 · 0.05 = 250` is `k × t_sim`.

**Table 4.9**: Kramers analysis at σ=0.5 (`T_eff = 0.125`), triple-well `V`.

| Transition | ΔV | ΔV/`T_eff` | Prefactor | `k·t_sim` | Status |
|---|---:|---:|---:|---:|---|
| `u=1 → u=0` | 2.013 | **16.1** | ~3.4 | ~8·10⁻⁵ | Kramers marginal (inner barrier) |
| `u=1 → u=4` | 13.187 | **105.5** | ~3.5 | ~4·10⁻⁴³ | Kramers strongly valid, **43 orders below horizon** |

### 4.8.3 Reframe — *Langevin works for inner, fails for outer* (#7)

The σ=0.5 observation (85% `u=0`, 0% `u=4`) should be read as **two simultaneous outcomes under one noise level**:

1. **Inner barrier** (ΔV/T_eff = 16): Langevin-driven crossing is qualitatively observed. 85% of voxels transit from the `u=1` basin across the inner saddle to the `u=0` basin within `t_sim=250`. Note however that Kramers prediction gives only ~`8·10⁻⁵` expected crossings per voxel — an **observed/predicted ratio ≈ 1.1·10⁴ (i.e. about 4 orders of magnitude)** discrepancy between 1D-Kramers and observation (see §4.11).

2. **Outer barrier** (ΔV/T_eff = 105.5): Kramers escape time exceeds the simulation horizon by `log₁₀(exp(105.5) / 250) ≈ 43.4` — **~43 orders of magnitude** log-gap. The 0% `u=4` occupancy is a **finite-time rare-event obstruction**, not an equilibrium prohibition.

This reframes the original interpretation ("Langevin fails on A1") to a more precise dual statement:

> **Langevin succeeds where the simulation horizon is adequate for the Kramers timescale; it fails where the horizon is too short.** The apparent "failure" to populate `u=4` is a timescale mismatch, not a paradigm limitation.

**Implication for OP2**: resolving OP2 (populating distant attractors) requires either (a) **barrier-topology engineering** to bring Kramers timescales within horizon, or (b) **directed non-equilibrium driving** (Hamiltonian, active, anisotropic noise) to bypass the Kramers bottleneck entirely.

### 4.8.4 High-σ regime [DYNAMIC-IMPLEMENTATION]

At σ ≥ 1.0, the noise amplitude dominates the potential structure. Voxels random-walk to the clamp boundary `|ψ|=3` (i.e. `u=18`), producing `u_max=18` and `u_mean ≈ 17` at σ=2.0. This is **not a physical steady state** but a `[DYNAMIC-IMPLEMENTATION]` artifact of the explicit-Euler + clamp boundary condition combined with ΔV/T_eff ≤ 1. See §4.11 for methodological notes.

---

## 4.9 Stage A1.4 — OP2 three-fold co-design diagnostic

**Hypothesis**: If the outer barrier in A1 is too high for the simulation horizon, lowering it should restore Laplace equilibrium under moderate σ. Test via shifted potential `V_shifted(u) = u(u−1)²(u−2)²`, minima at `u∈{0,1,2}`, outer barrier reduced from 13.187 (A1) to `V(saddle u=1.540) = 0.095`.

**Setup**: same as A1 but with shifted `V`, σ-scan `{0, 0.1, 0.3, 0.5, 0.7}` + soft-wall experiments `V_wall = λ·max(0, u−u_max)⁴` with `λ ∈ {1, 10}`, `u_max=2.5`, and a `λ=1, σ=0.3` control.

**Laplace prediction at σ=0.5, T_eff=0.125** [DYNAMIC-EQUILIBRIUM]:

- `Z_0 = T/4 = 0.0313` (linear boundary basin `V≈4u` near `u=0`)
- `Z_1 = √(2πT/V''(1)) = √(πT) = 0.6267` (quadratic minimum `V''=2`)
- `Z_2 = √(2πT/V''(2)) = √(πT/2) = 0.4431` (quadratic minimum `V''=4`)

Normalization: `p_k = Z_k / Σ_j Z_j` with `Σ_j Z_j = 0.0313 + 0.6267 + 0.4431 = 1.1010`. Predicted occupancy: `p(0) ≈ 0.028, p(1) ≈ 0.569, p(2) ≈ 0.402` (sum = 1.000). Ratio `p(1)/p(2) = √2 ≈ 1.414` (wider basin has higher weight). Independent rejection-sampling on `(a,b) ∈ ℝ²` with 4·10⁶ points confirms this ratio.

### 4.9.1 σ-scan results

**Table 4.10**: Observed occupancy under σ-scan on shifted potential (70 docs × 32³ voxels = 2.3·10⁶ samples per σ).

| σ | `T_eff` | `u_max` | `u_mean` | p(0) | p(1) | p(2) | p(clamp) | Kramers regime |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 0.0 | — | 2.13 | 1.72 | 0.000 | 0.340 | **0.660** | 0.000 | (deterministic baseline) |
| 0.1 | 0.005 | 2.41 | 1.88 | 0.000 | 0.146 | **0.853** | 0.000 | frozen (k·H≈10⁻⁷) |
| 0.3 | 0.045 | 18.00 | 1.61 | 0.012 | 0.363 | 0.408 | 0.004 | partial (k·H≈10, outer marginal) |
| 0.5 | 0.125 | 18.00 | 9.90 | 0.054 | 0.246 | 0.041 | **0.525** | ΔV/T=0.76 < 1: **Kramers invalid** |
| 0.7 | 0.245 | 18.00 | 17.65 | 0.003 | 0.008 | 0.001 | **0.979** | ΔV/T=0.39 < 1: breakdown |
| — **Laplace** | | | | 0.028 | **0.569** | **0.402** | 0 | — |

**None of the σ values yield Laplace-consistent occupancy**. Specifically:

1. **σ=0 deterministic baseline** already deviates from Laplace: 66% `u=2` (not 40%) even with no noise. Gradient flow plus source driving alone suffices to disrupt equilibrium.
2. **σ=0.1**: 85% trapped in `u=2` basin. Below thermal mixing timescale (`k · t_sim ≈ 10⁻⁷` for inter-well rates).
3. **σ=0.3**: ratio `p(1)/p(2) = 0.363/0.408 = 0.89`, **reversed** from Laplace prediction `1.41`. Detailed-balance rate ratio `k_{12}/k_{21} = 0.704 ≈ 1/√2` is correct, but system has not thermalized (21% "in-between"; init bias and source drift exceed mixing within horizon).
4. **σ=0.5, 0.7**: noise exceeds potential confinement; 52% / 98% of voxels hit the clamp boundary at `u=18`.

### 4.9.2 Soft-wall intervention (walled experiments)

Adding `V_wall = λ·max(0, u−2.5)⁴` should confine voxels away from the clamp.

**Table 4.11**: Walled experiments at shifted potential.

| λ | σ | `u_mean` | p(u=1) | p(u=2) | p(clamp) | Δ(clamp) vs no-wall |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 0.5 | 10.04 | 0.242 | 0.040 | 0.534 | +0.9 pp (no help) |
| 10 | 0.5 | 11.04 | 0.209 | 0.031 | **0.593** | **+6.8 pp (worse)** |
| 1 | 0.3 (control) | 1.62 | 0.363 | 0.407 | 0.005 | +0.1 pp (wall passive) |

**Walls of this form do not restore Laplace equilibrium**. The σ=0.3 control confirms the wall is appropriately passive when not needed (wall active fraction 0.75%).

### 4.9.3 Three-fold diagnosis

Decomposition of why the intervention fails:

#### Axis A — Source statistics [DYNAMIC-IMPLEMENTATION]

BGE embedding's imaginary component has a **statistically extreme non-zero mean**:

- Per-doc mean of 512 `Sb` components across 70 docs: `⟨Sb⟩ = −1.48·10⁻³`, `std = 7.2·10⁻⁴`
- 1-sample t-test: `t = −17.12, p < 10⁻²⁵`
- For `Sa`: `t = 0.62, p = 0.54` (consistent with zero)

A nonzero mean of `S` implies the force `−∇V + S` is **not pure-gradient** (or at least cannot take Boltzmann form without modification); detailed balance is broken, and the system evolves toward a non-equilibrium steady state (NESS) rather than a Boltzmann distribution.

Cumulative forcing scale: `|S|·t_sim ~ 0.1 · 250 = 25`, far exceeding the shifted outer barrier `ΔV_outer = 0.095`. Deterministic source-pull across the outer saddle is energetically available even at σ=0. The σ=0 baseline observation (66% `u=2`) confirms this mechanism operates *without any noise contribution*.

#### Axis B — Potential tail geometry [STATIC]

Shifted `V(u)` scales as `u⁵` for large `u` (equivalently `|ψ|¹⁰` in ψ-space; two polynomial orders shallower than A1 original `u⁹`/`|ψ|¹⁸`). For `σ=0.5`, per-step noise displacement is `σ√dt = 0.112` in `(a, b)` coordinates, producing per-step `Δu ≈ 2|ψ|·0.112 ≈ 0.22` near basins. The `u⁵` tail restoring force exceeds this only in a narrow band `u ∈ [2, 3]`; beyond, `dt·|f|` overshoots and voxels random-walk to the clamp.

Soft wall `V_wall = λ·(u−u_max)⁴` is `C³`-smooth at `u=u_max` — `V=V'=V''=V'''=0`, `V''''=24λ`. Wall force at `u=2.6` is only `4λ·(0.1)³ = 4·10⁻³·λ` (essentially zero); voxels transit the `u ∈ [u_max, u_max + δ]` region in `O(δ/σ√dt) ~ 5` steps without appreciable deceleration before reaching the clamp at `u=18`.

#### Axis C — Numerical scheme [DYNAMIC-IMPLEMENTATION]

Explicit Euler stability requires `dt·|J| < 2`, where `J` is the local Jacobian spectral radius.

At `u=10, a²=b²=5` (isotropic case), for `V_wall = λ·(u−2.5)⁴`:
- `f_wall(u) = λ · 4 · (7.5)³ = 1687.5·λ`
- `f'_wall(u) = λ · 12 · (7.5)² = 675·λ`
- 2×2 block `[[J11=2a²·f' + f, J12=2ab·f'], [J12, J22=2b²·f' + f]]`
- At `a²=b²=5`: `J_max = (2a²·f'+f) + 2ab·f' = 8437.5 + 6750 = 15187.5·λ`

Hence:
- λ=1: `J ≈ 1.5·10⁴`, `dt_max ≈ 1.3·10⁻⁴`, experimental `dt=0.05` exceeds stability by **~380×**
- λ=10: `J ≈ 1.5·10⁵`, `dt_max ≈ 1.3·10⁻⁵`, exceeds by **~3800×**

This **directly explains** why the stronger wall (`λ=10`) *worsens* clamp residency: larger Jacobian violates CFL more severely; the clamp absorbs the instability. Explicit Euler at `dt=0.05` is fundamentally incompatible with any meaningful wall stiffness in this geometry.

#### Axes are coupled

**No single-axis fix restores Laplace** (verified by elimination):

| Fix axis | Remaining obstruction |
|---|---|
| Source whitening only | Potential tail still `u⁵`; integrator still CFL-violating at σ=0.5 |
| Potential shape only (deeper tail) | Source drift still breaks DB; stiffer potential worsens integrator stability |
| Integrator only (implicit) | Source drift still `17σ` from mean-zero; shallow tail still allows escape |

A1.4 **refines** OP2 from a single-axis barrier-engineering problem to a three-axis co-design problem. The three axes are empirically orthogonal in the sense that each is an independent necessary (not sufficient) condition for Laplace equilibrium under this class of physics setup.

### 4.9.4 A1.4 verdict

A1.4 is best read as a **diagnostic refinement**, not a success/failure binary:

- It **falsifies** the naive interpretation "lowering barriers alone enables OP2 access"
- It **does not falsify** the broader OP2 program, which still admits joint source/potential/integrator co-design (Block V Phase A)
- It **does falsify** the specific instance (shifted potential + explicit Euler + BGE raw source + simple soft wall)
- It provides three orthogonal engineering targets for future work

**Explicitly not claimed**: (i) OP2 is unsolvable, (ii) the Allen-Cahn framework is broken (σ=0 baseline confirms internal dynamics are correct), (iii) BGE embeddings are unsuitable (only their raw use as source; whitening or gradient-projection may restore suitability).

Full details in `block4_5/a1_4/VERDICT.md` (companion repository).

---

## 4.10 Two-regime analytical framework

The preceding Block IV.5 analyses make explicit use of a **two-regime dichotomy** for occupancy prediction:

**Regime 1 — Rare-event (Kramers) limit** (`ΔV/T_eff ≫ 1`):
- Occupancy evolves slowly via barrier crossings
- Relevant quantity: `k·t_sim` (expected number of crossings)
- Applicable: A1 outer barrier at σ=0.5 (`ΔV/T = 105.5`, `k·t_sim ≈ 4·10⁻⁴³` → 0 crossings)

**Regime 2 — Thermalized (Laplace) limit** (`ΔV/T_eff ≲ few`, system fully mixes within `t_sim`):
- Occupancy given by equilibrium Boltzmann partition function
- `p_k ∝ Z_k = √(2πT/V''(u_k))` for quadratic minima; boundary basins require case-by-case treatment (e.g., linear-V gives `Z ∝ T/|V'(0+)|`)
- Applicable: A1.4 at σ=0.5 if detailed balance held (which it does not, per §4.9.3)

**Regime selection is dictated by the dimensionless quantity `ΔV/T_eff`**, not by modeling choice. Boundary regimes (`ΔV/T_eff ∈ [1, 5]`) require either longer simulation or explicit Kramers-prefactor measurement. For `ΔV/T_eff ≤ 1`, Kramers formula is invalid and system dynamics approach free diffusion with weak potential modulation — in the presence of boundary clamps, this produces `[DYNAMIC-IMPLEMENTATION]` artifacts rather than physical steady states.

Both regimes assume `⟨S⟩ = 0` (mean-zero source) and standard Boltzmann form. **§4.9.3 Axis A shows BGE violates this assumption by `17σ`** — a systematic caveat applicable to all MaoField experiments in this paper that use raw BGE embeddings as source.

---

## 4.11 Open methodological questions

### 4.11.1 A1 inner barrier ~10⁴ Kramers-observation discrepancy

In §4.8.3, the 1D Kramers prefactor for `u=1 → u=0` gave `k·t_sim ≈ 8·10⁻⁵` expected crossings per voxel, while observation shows 85% of voxels have crossed. The ratio between prediction and observation is **factor ~10⁴ (i.e. ~4 orders of magnitude)**, not 10^10000.

Candidate explanations (not tested):
1. **1D Kramers prefactor underestimates** escape rate in 3D field-theoretic setting due to collective voxel-voxel interactions (the voxels are coupled through the Laplacian `D∇²ψ`). To our knowledge, no closed-form field-theoretic Kramers analog is tabulated for this geometry; empirical calibration via σ-scan is the most direct route.
2. **Boundary basin at `u=0`** has linear-V attractor `V≈4u` rather than quadratic; standard Kramers prefactor derivation assumes quadratic saddles and quadratic minima
3. `ΔV/T_eff = 16` is marginal: although above the conventional `≥ 5` threshold for Kramers validity, the *absolute calibration* of the 1D prefactor in 3D lattice field theory is not established in the literature we surveyed

**Status**: flagged as an open methodological question. The **qualitative conclusion** (outer barrier unreachable at `~43 orders` log-gap) is robust regardless, but quantitative rate matching for lower barriers requires further work — either empirical prefactor measurement from σ-scan, or derivation of a field-theoretic Kramers analog.

### 4.11.2 Silhouette values `< 0.25`

Block III's `k*=2` finding rests on silhouette coefficients `0.037–0.223`, below the conventional `0.25` threshold for "substantial cluster structure". We report `k*=2` as the *local* silhouette optimum rather than as a strongly-separated attractor count. Future work should use alternative cluster-validation metrics (gap statistic, bootstrap-stability) and ideally persistent-homology diagnostics to distinguish between "truly k-cluster structure" and "k-optimum of weakly-structured point cloud".

### 4.11.3 Finite-lattice caveat

All SSB-like claims in this paper hold in the *empirical distributional sense* on a 32³ lattice within finite simulation horizons. Strict-sense spontaneous symmetry breaking requires thermodynamic-limit treatments (Section 3.5; footnote [^zn-loose]). The pattern separation observed at N=32³ is suggestive of mechanism but does not constitute proof of symmetry-sector existence in the Anderson-Goldstone-Nambu sense.

### 4.11.4 Missing controls

The following ablations were not performed and would strengthen the empirical case:
1. σ=0 gradient-flow-only experiments for *every* σ-scan (not just A1.4)
2. Source whitening (`Sb − ⟨Sb⟩`) baseline to separate drift from mixing effects
3. Integrator-convergence test with `dt=0.01` to rule out numerical artifacts in σ-scan regimes
4. mMARCO cross-lingual runs (original H3 dimension, currently SKIPPED due to download failure)

---

## 4.12 Experimental status summary

**Confirmed** (empirical evidence supports):

- [H1 falsified, weak] Kuramoto coupling improves retrieval by max `+18.7%`, below the 20% threshold
- [H2 confirmed, statistically weak] `k*=2` across three representations and two source types
- [H3 partially confirmed] Source density affects the mechanism (byte vs BGE regimes) while preserving `k*`
- [Fusion] Explicit query-document fusion degrades signal by `+7.9 to +26.0 pp` across 5 datasets

**Refined open problems**:

- [OP1] M2 iteration (Axiom 6 candidate) falsified in prior work; Axiom 6 formalization remains open
- [OP2] Reframed from "non-equilibrium extensions needed" to **three-fold co-design**: source statistics (mean-zero or NESS treatment), potential geometry (confining tail + stability-compatible shape), numerical scheme (implicit or sub-CFL-dt for stiff terms). A1.4 diagnostic supplies all three axes; Block V Phase A is scheduled to test them jointly.

**Methodological** (see §4.11):

- A1 inner barrier Kramers prediction differs from observation by factor ~10⁴
- Silhouette values support `k*=2` only in local-optimum sense
- BGE raw source violates mean-zero assumption of Laplace framework

---

[^zn-loose]: See Section 3.5 (`[^zn-loose]` footnote) for full text. Summary: `Z_n` labels in this paper denote **empirical distributional remaining-symmetry patterns**, not rigorous group actions on a thermodynamically-broken vacuum. Strict SSB requires (1) group `G` acting on field space, (2) `V` invariant under `G`, (3) ground-state manifold is `G`-orbit, (4) non-trivially-transforming order parameter `⟨ψ⟩ ≠ 0`, (5) thermodynamic limit `N → ∞`. Conditions (3)–(5) are not verified on our `N=32³` lattice; `Z_n` is a compact descriptor for convenience.

# 5. Roadmap: Refined Open Problems and Block V Program

**Position**: this section formalizes the two open problems (OP1, OP2) in their post-experiment refined form, lays out Block V's three-axis co-design experimental program (Phase A-0/A-1/A-2/A-3), and states the three-stage publication strategy that organizes follow-up work.

---

## 5.1 OP1: Axiom 6 Formalization — M2 Falsification

Axiom 6 asserts that matching is self-training: the matching score between query and document fields should be the fixed point of a self-consistent iteration. The natural candidate

```
M2:   S_{n+1} = normalize(S_n · ψ_q* · ψ_d)                                  (reproduced from Eq. 3.3)
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

# 6. Discussion

---

## 6.1 Summary of What This Paper Claims and Does Not Claim

MaoField is a research-stage framework, not a completed theory. We summarize explicitly.

**Claimed**:
- A categorical structure (Lawvere endofunctor on `Meas`, conjectured Giry-monad lift) that formalizes dialectical motion in PDE-based AI (§2.3)
- A source-density decomposition that explains the `k* = 2` retrieval ceiling via two distinct distributional regimes (§4.6)
- A refined formulation of OP2 (Axiom 3's non-equilibrium extension) from a single-axis "directed driving" problem to a three-axis co-design problem with concrete sub-problem statements (§5.2)
- A working PDE-based retrieval reranker that exceeds byte-level lexical baselines by `+14.7% to +172.3%` across five BEIR datasets while lagging SOTA cross-encoders by `−10.8 to −32.2 pp` (§4.2)
- An exclusion result for Axiom 6: the principal candidate iteration (M2) of Axiom 6's mathematical formalization is falsified as a Banach contraction in `ℂ^N` by 0-homogeneity (§5.1). The axiom itself remains open (OP1); methodological pragmatics (mode-tagging discipline, spawn-agent review pipeline, [^zn-loose] convention) are discussed separately in §6.3 as working commitments, not as paper-level claims

**Not claimed**:
- That MaoField replaces or competes with deep-learning-based retrieval on SOTA benchmarks
- That dialectical materialism is *uniquely* realized by our categorical formalism; other formalisms may admit dialectical readings
- That OP1 or OP2 is solved; we report one candidate excluded (M2 in OP1) and one problem scope refined (OP2 three-fold), nothing stronger
- That the Giry-monad lift conjectured in §2.3.3 is proven; it is the most coherent organizing conjecture currently visible, not a theorem
- That our finite-lattice (`N = 32³`) observations have the status of thermodynamic-limit spontaneous symmetry breaking; they are well-defined empirical patterns consistent with — but not proof of — strict-sense SSB (§3.5)

The distinction between these two lists is, in our view, the operative integrity check for a research-stage paper. Papers that conflate them — claiming the former while implicitly asserting the latter — are the recurring failure mode in over-ambitious framework work. We have tried to keep the two lists separate.

## 6.2 Limitations

The framework's current limitations fall into four categories.

### 6.2.1 Empirical Limitations

Our retrieval evaluation is limited to five BEIR datasets at modest scale (per-domain `O(10² – 10³)` documents). We have not tested:
- Compositional generalization (SCAN-style benchmarks)
- Long-context coherence (beyond single-document scoring)
- Cross-lingual performance
- Adversarial / out-of-distribution robustness

Block V (§5.3–5.4) is designed in part to address these, but the results are not in this paper. A reader seeking a full empirical envelope should read this paper as establishing the **mechanism** and awaiting the follow-up IPM paper (§5.5 Stage 2) for broader performance validation.

### 6.2.2 Scale Limitations

All field-theoretic simulations run on `32³ = 32768` voxels per document field. Strict-sense symmetry breaking requires `N → ∞` (§3.5); at our scale, symmetry-related sectors have finite tunneling rates that we have not fully characterized. Whether the observed phenomena (notably the `k* = 2` mechanism decomposition in §4.6) are stable under scale increase is an empirical question that this paper does not resolve. Block V Phase A-0 (§5.3) includes a reachability pre-check that partially addresses scale-related artifacts; a systematic finite-size scaling study is reserved for follow-up work.

### 6.2.3 Methodological Limitations

The A1 inner barrier Kramers discrepancy (observed/predicted ratio ~10⁴, §4.8.3 and A1.4 VERDICT §5.1) indicates that our 1D Kramers rate predictions may systematically underestimate escape rates in 3D lattice field theory. We flag this as an open methodological question; our qualitative conclusions (outer barrier at 43-orders-of-magnitude log-gap) are robust, but quantitative rate matching for near-Kramers-regime barriers requires a field-theoretic analog to the 1D Kramers formula. This is potentially addressable via empirical prefactor calibration from the σ-scan, deferred to Block V Phase A-1.

### 6.2.4 Formal Limitations

The Lawvere-monad framing in §2.3 is **position-paper-level, not formalization-level**. Three gaps are explicit:

1. The endofunctor `T_•` on `Meas` is rigorous, but the Giry-monad lift `P ∘ T_•` is conjectured (§2.3.3 footnote [^giry-monad])
2. The reachable-subcategory definition `T-Alg^{(η, p_0)}` uses a "Kleisli-reachable path" notion that requires the conjectured monad lift for full rigor (§2.3.4)
3. `Δ_OP2 := |T-Alg| ⊖ |T-Alg^{(η, p_0)}|` uses cardinality complement as a symbolic first pass; alternative quantifications (categorical entropy, persistent-homology dimension, Kan extension obstructions) may disagree in finer regimes

A follow-up paper dedicated to the categorical formalization — one in which (1), (2), (3) are either resolved or their independence is precisely characterized — is the natural sequel to the present work.

## 6.3 Methodological Reflection

This paper was produced via a workflow that deserves explicit methodological reflection, because the workflow itself embodies commitments that the framework argues for.

**Spawn-agent review pipeline.** During the 2026-04-13–14 campaign in which this paper was drafted, the author working with two AI assistants instituted a standing rule: every significant deliverable (mathematical derivation, experimental verdict, paper section) is submitted to an **independent paper-review subagent** before being finalized. The reviewer is a separate instance without the drafting agent's context, prompted with explicit review criteria (P0 must-fix, P1 recommended, P2 suggested weakening, P3 already-honest).

Under this protocol, **11 substantive errors** were caught and corrected during Phase 1 (Kramers formulation errors, Wirtinger-derivative bugs, over-claimed symmetry-breaking labels, Kramers vs. Boltzmann regime conflation, and others). A further **pass of reviews** on the arXiv v1 section drafts (the present paper) caught additional issues (factor-of-2 inconsistency between field equation and free energy, Axiom 4 softening that undercut quantitative evidence, cross-reference naming drift, CFL violation number inconsistency). Each of these would have been noticed by a careful human reviewer; the protocol makes the noticing **systematic rather than contingent on reviewer attention**.

We offer this as a concrete practice compatible with the framework's epistemology: **the dialectical-materialist insistence on practice-driven cognition maps directly onto a "review-as-practice" discipline for paper production**. The reviewer is not a decorative safety net; it is the practice that tests the drafting agent's claims against independent analysis.

**Mode-tagging discipline.** Throughout the experimental sections we tag statements as `[STATIC]` (landscape geometry), `[DYNAMIC-EQUILIBRIUM]` (Boltzmann / Laplace predictions), `[DYNAMIC-RARE-EVENT]` (Kramers escape), or `[DYNAMIC-IMPLEMENTATION]` (integrator, boundary, source statistics). This discipline was introduced in response to a recurring error class identified during Phase 1 review: **static analysis tools (critical-point geometry, Hessian analysis) being silently transported to dynamic prediction tasks (occupancy, escape rates) without changing toolkit**. Tagging makes the regime explicit, forcing the author to consciously choose the appropriate formula (Kramers rate vs. Laplace equilibrium vs. finite-time simulation) rather than reach for the most convenient.

**Explicit OP-signposting.** Axioms 3 and 6 are maintained as open problems (OP2 and OP1 respectively) rather than being implicitly asserted or silently weakened. This is, again, a dialectical-materialist methodological commitment: open contradictions should be made visible rather than papered over, because their resolution is the engine of the research program's motion.

## 6.4 Implications for the AI Paradigm Discussion

We do not claim that MaoField refutes, replaces, or dominates statistical deep learning. We claim that a **second paradigm** — distinct in motivation, mathematical infrastructure, and implementation details — is viable at a research-stage level and produces properties that the first paradigm has not produced (end-to-end structural interpretability, autonomous dynamics, explicit attractor enumeration). The paradigm-level scope is deliberate: retrieval is the **tractable test bed** on which §4 demonstrates non-vacuity, but the framework's target domain is any setting where autonomous structural dynamics rather than statistical prediction is the operative goal.

**The paradigms are complementary, not competitive**. Statistical deep learning is the correct approach when the goal is predictive performance at scale on tasks where structure is implicit and data is abundant. Field-theoretic dialectical frameworks may be the correct approach when the goal is **structural understanding of attractor dynamics in low-data or interpretability-critical settings** (scientific hypothesis generation, safety-critical decision systems, educational / explanatory applications). Neither paradigm subsumes the other.

**The long-term question** is whether the two paradigms can be composed — statistical deep learning providing the upstream embedding (as in our `F_dense` construction with BGE-M3) and the field-theoretic framework providing the downstream structural analysis. Our empirical results suggest this composition is **non-trivial**: BGE's statistical structure violates Laplace's mean-zero source assumption by 17σ (§4.9), a quantitative obstruction to naïve composition. Addressing this obstruction is OP2 sub-problem (a) (§5.2.2) and Block V Phase A-1 (§5.3). The outcome will substantively inform how the two paradigms can interoperate.

## 6.5 Implications for the Dialectical-Materialist Tradition

This paper is an explicit attempt to **re-activate dialectical materialism as a working method** for 21st-century problems in artificial intelligence, beyond its 20th-century applications to political economy and social theory. We take seriously three commitments from that tradition:

1. That **practice is the criterion of truth** (On Practice, Mao 1937). Our spawn-agent review pipeline, our mode-tagging discipline, and our explicit OP-signposting are all practical instruments, not rhetorical positions; they are the framework's working-out of the practice criterion at the level of paper production
2. That **contradictions internal to a system drive its motion** (On Contradiction, Mao 1937). We have been explicit about the framework's internal contradictions (Axiom 4 vs. BGE, Axiom 3 vs. Langevin, Axiom 7 vs. fixed V) rather than resolving them by fiat; their persistence is what the framework needs to continue developing
3. That **quantitative changes can produce qualitative transitions** (Engels, posthumously 1925). Stage A1.4 (§4.9) is the framework's own direct experimental instance of this principle; the "failure" of A1.4 — its 52.5% clamp residency — is not an engineering setback but a quality-transition observation that refines OP2 into its three-fold form

We do not claim to speak for the tradition beyond our specific use of it. Other dialectical-materialist thinkers have developed different methodological emphases (structuralism, historical sociology, critical theory); our use is technical and instrument-focused, not programmatic.

**On the broader project**. We hold the position, defensible against critical examination, that dialectical materialism is a methodological tradition with substantial unresolved potential for application to 21st-century problems — specifically, that the tradition's analytical tools for understanding how systems evolve through internal contradiction may be more applicable to AI and complex systems than to the primarily social-scientific applications that dominated 20th-century practice. This paper is an experiment in testing that position; the results are, as the paper shows, partial but substantive.

We do not expect this framing to be universally welcomed. We include it to be honest about the paper's motivation — and because the reader who knows the motivation can more accurately calibrate what to believe and what to question.

## 6.6 Concluding Statement

A framework whose research program is entirely in its open problems is not an evasion of responsibility. It is the honest representation of a research stage in which the most important claims are **what we have not proven** rather than **what we have proven**. We have:

- Proposed a categorical structure with explicit conjectural limits
- Reported empirical findings with explicit finite-lattice caveats
- Identified two open problems with concrete experimental programs
- Established a three-stage publication plan that separates mechanism from integration

The next paper in the series (the IPM mechanism paper, Stage 2, target 2026-07–08 month) will report Block V Phase A outcomes. The capstone paper (Stage 3, target 2027 Q1–Q2) will integrate across Phases A, B, and C with whatever state the research has reached. Neither is promised.

The framework's ultimate target is **not a benchmark victory**. The target is **the re-activation of dialectical materialism as a working methodology for 21st-century productive forces** — a target measured in years to decades, not quarters, and one whose success criterion is the emergence of a community that finds the framework useful, not any single empirical result. We believe the work reported here is a coherent first anchor toward that target; we do not believe it is the target. The distinction matters.

---

# References

**Primary references cited in text** (full bibliographic details in `references.bib` in the companion repository; reproducibility scripts in `paper/reproduce/`):

- Lawvere, F. W. (1969). *Adjointness in foundations*. Dialectica, 23:281–296.
- Mao Zedong (1937). *On Contradiction* (矛盾论).
- Mao Zedong (1937). *On Practice* (实践论).
- Lenin, V. I. (1909). *Materialism and Empirio-Criticism*.
- Engels, F. (posthumously 1925). *Dialectics of Nature*.
- Giry, M. (1982). *A categorical approach to probability theory*. In Categorical Aspects of Topology and Analysis, LNM 915, Springer.
- Jacobs, B. (2010). *Convexity, duality and effects*. In Theoretical Computer Science, Springer.
- Adams, H., et al. (2021). *giotto-tda: A Topological Data Analysis Toolkit for Machine Learning and Data Exploration*. JMLR.
- Bossy, M., & Talay, D. (2005). *Reflected Langevin dynamics and related schemes*. Stochastic Analysis and Applications.
- Anderson, P. W. (1972). *More Is Different*. Science 177:393–396.
- Kramers, H. A. (1940). *Brownian motion in a field of force and the diffusion model of chemical reactions*. Physica 7:284–304.

**Supporting methodology documents** (in this repository):

- `FINAL_REPORT.md` — Full exp017 experimental archive (Block I–IV + Stage C/A1)
- `block4_5/a1_4/VERDICT.md` — A1.4 shifted-potential verdict (Phase 2/2.5)
- `BLOCK_V_DESIGN.md` — Phase A/B/C experimental roadmap
- `REVIEW_*.md` files — Spawn-agent review records (P1–P5 + Phase 2.5 + §4 + verdicts)

---
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
