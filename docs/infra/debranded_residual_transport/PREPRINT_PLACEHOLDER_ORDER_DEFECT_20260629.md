# Preprint Placeholder -- Order Defects in Finite Weighted Residual Decompositions

Date: 2026-06-29 CST
Status: local preprint placeholder, not an external submission
Classification: wip/core bridge

## Working Title

Order Defects in Finite Weighted Residual Decompositions

## One-Sentence Claim

In a finite two-axis weighted diagnostic field, sequentially stripping centered
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
effects, or dependent-input decompositions.  Its purpose is narrower: to give a
minimal rational witness and a deterministic harness for detecting when a
weighted diagnostic residual has been created by the order of nuisance removal
rather than by a stable non-additive field.

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

5. Deterministic zero-GPU harness boundary:
   `docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md`
   and
   `docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json`.

## Related Work Boundary

This placeholder must not claim broad novelty over dependent-input ANOVA or
sensitivity analysis.  At minimum, cite and position against:

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

The safe novelty framing is not "new ANOVA".  It is a compact diagnostic
warning: if an empirical pipeline uses non-product cell weights and removes
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

Turn `FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` into a short standalone note
of 4-6 pages:

1. finite weighted setup;
2. product-weight iff theorem;
3. ordered stripping theorem;
4. pure-main-effect no-go;
5. `2 x 2` witness;
6. short related-work paragraph emphasizing that this is a diagnostic
   artifact note, not a replacement for dependent-input ANOVA or Shapley
   sensitivity analysis.

