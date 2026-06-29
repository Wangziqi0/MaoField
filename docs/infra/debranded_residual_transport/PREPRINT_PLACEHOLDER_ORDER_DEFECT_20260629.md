# Preprint Placeholder -- Order Defects in Finite Weighted Residual Decompositions

Date: 2026-06-29 CST
Status: local preprint placeholder, not an external submission
Classification: wip/core bridge

## Working Title

Order Defects in Finite Weighted Residual Decompositions

## One-Sentence Claim

In a finite weighted two-way array/table, sequentially stripping centered
main-effect subspaces is order-independent exactly in the product-weight case;
under non-product weights, a pure main-effect signal can produce a nonzero
wrong-order residual even though its true additive residual is zero.

## Abstract Placeholder

Many diagnostic pipelines decompose a finite array into mean effects,
axis-wise main effects, and a residual that is then interpreted as an
interaction-like signal.  This note records a finite-dimensional caution for
such decompositions.  Let `X=Q x B` be finite, let `w(q,b)>0` be a probability
weight, and let `C`, `A`, and `B0` denote the constant, centered `q`-only, and
centered `b`-only subspaces in the weighted Hilbert space `L^2(X,w)`.  We show
that the two centered main-effect subspaces are orthogonal if and only if
`w(q,b)=w_Q(q)w_B(b)`.  Consequently, the two ordered nuisance-stripping maps

```text
R_Q_then_B = (I-P_B0)(I-P_A)(I-P_C)
R_B_then_Q = (I-P_A)(I-P_B0)(I-P_C)
```

agree if and only if the weight is product form.  If the weight is not product
form, there exists a pure main-effect witness whose orthogonal additive
residual `(I-P_N)K` is zero, while one wrong-order sequential residual is
nonzero.  The nonzero output is therefore a sequential stripping artifact, not
a true interaction residual and not a product-measure Hoeffding interaction.

The note is intentionally finite, elementary, and implementation-oriented.  It
does not introduce a new theory of functional ANOVA, Sobol indices, Shapley
effects, or dependent-input decompositions. This note isolates a finite
weighted projection-order artifact in a two-way table; it is not proposed as a
new dependent-input ANOVA or Hoeffding decomposition theory. Its purpose is
narrower: to give a minimal rational witness and deterministic regression
checks for detecting when a finite weighted-table residual has been created by
the order of nuisance removal rather than by a true non-additive component.

## Narrow Contribution To Preserve

1. Product-weight iff theorem for the orthogonality of centered row/column
   main-effect subspaces in the finite positive-weight case.
2. Exact equivalence between product weights and order independence of the
   two sequential residual-stripping maps above.
3. Existential non-product no-go: a pure main-effect witness can have zero
   true additive residual but nonzero wrong-order residual.
4. Minimal `2 x 2` rational witness:

```text
w = (1/11) [[1,2],
            [3,5]]
K = (7/11, -4/11, 7/11, -4/11) in B0
(I-P_N)K = 0
R_B_then_Q K = 0
R_Q_then_B K = (1/32, 5/168, -1/96, -1/84)
||R_Q_then_B K||_w^2 = 61/177408
```

5. Exact rational witness certificate:
   `docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md`
   and
   `docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json`.
6. Deterministic zero-GPU regression harness boundary:
   `docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md`
   and
   `docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json`.
   This harness is deterministic regression support only; the mathematical
   claims are carried by the analytic proof and exact rational certificate, not
   by JSON floating-point outputs.

## Related Work Boundary

This placeholder must not claim broad novelty over dependent-input ANOVA,
sensitivity analysis, or noncommuting projection theory. Before any external
draft, durable bibliography records must replace any chat-internal citation
handles. Closest antecedents lie in dependent-variable ANOVA-Hoeffding
decompositions and in the classical theory of two noncommuting orthogonal
projections. At minimum, cite and position against:

- Hooker, "Generalized Functional ANOVA Diagnostics for High-Dimensional
  Functions of Dependent Variables", 2007. DOI:
  https://doi.org/10.1198/106186007x237892
- Chastaing, Gamboa, and Prieur, "Generalized Hoeffding-Sobol decomposition
  for dependent variables - application to sensitivity analysis", Electronic
  Journal of Statistics, 2012. DOI: https://doi.org/10.1214/12-ejs749
- Chastaing, Gamboa, and Prieur, "Generalized Sobol sensitivity indices for
  dependent variables: numerical methods", Journal of Statistical Computation
  and Simulation, 2015. DOI: https://doi.org/10.1080/00949655.2014.960415
- Owen and Prieur, "On Shapley Value for Measuring Importance of Dependent
  Inputs", SIAM/ASA Journal on Uncertainty Quantification, 2017. DOI:
  https://doi.org/10.1137/16m1097717
- Iooss and Prieur, "Shapley effects for sensitivity analysis with correlated
  inputs", International Journal for Uncertainty Quantification, 2019. DOI:
  https://doi.org/10.1615/int.j.uncertaintyquantification.2019028372
- Il Idrissi, Bousquet, Gamboa, Iooss, and Loubes, "Hoeffding decomposition
  of functions of random dependent variables", Journal of Multivariate
  Analysis, 2025. DOI: https://doi.org/10.1016/j.jmva.2025.105444
- Lamboni, "On ANOVA-Type Decompositions of Functions with Non-independent
  Variables: Sensitivity Analysis", SIAM/ASA Journal on Uncertainty
  Quantification, 2026. DOI: https://doi.org/10.1137/24M1712680
- Böttcher and Spitkovsky, "A gentle guide to the basics of two projections
  theory", Linear Algebra and its Applications, 2010. DOI:
  https://doi.org/10.1016/j.laa.2009.11.002
- Corach and Maestripieri, "Products of orthogonal projections and polar
  decompositions", arXiv: https://arxiv.org/abs/1011.5237
- Halmos, "Two subspaces", Transactions of the American Mathematical Society,
  1969. DOI: https://doi.org/10.1090/S0002-9947-1969-0251519-5

The formal bibliography/positioning record for this local placeholder is:
`docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md`.

The safe novelty framing is not "new ANOVA", not a new dependent-input
decomposition theory, and not a new noncommuting projection theory. It is a
compact finite weighted projection-order artifact note with an exact `2 x 2`
witness: if an empirical pipeline uses non-product cell weights and removes
nuisance axes sequentially, the resulting residual can be an order artifact.

## Forbidden Claims

Do not claim:

- a MaoField empirical positive result;
- an observed MaoField residual, interaction, quotient-residual, transport, or
  holonomy field;
- full panel completion, 16-cell aggregate, LOSO pass, F3 positive, glass-box
  breakage, training authorization, or new-loss authorization;
- a completed formal system;
- that every non-product-weight input shows order dependence.

Allowed ceiling:

```text
definitions_and_harness_viable_only
```

Mode B MaoField empirical status:

```text
insufficient_artifact
```

## Preprint-Safe Next Step

Revise first. The current placeholder is not yet an external submission
candidate. Before posting, turn `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md`
into a short standalone note of 4-6 pages and complete:

1. finite weighted setup;
2. product-weight iff theorem;
3. ordered stripping theorem;
4. pure-main-effect no-go;
5. `2 x 2` witness;
6. exact rational appendix/certificate;
7. short related-work paragraph emphasizing that this is a finite weighted
   projection-order artifact note, not a new ANOVA theory, not a replacement
   for dependent-input ANOVA or Shapley sensitivity analysis, and not a new
   theory of noncommuting projections;
8. final gate confirmation that all harness references are deterministic
   regression support only, not proof artifacts.
