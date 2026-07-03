# Order-Defect Bibliography And Positioning v1.5

Date: 2026-06-29 CST
Status: local bibliography / positioning record, not an external submission
Classification: core/wip bridge

## Purpose

This file closes the immediate bibliography and novelty-wording gap identified
by the v1.4 exact/bibliography Pro audit. It is a local reference record for
the narrow order-defect preprint placeholder:

```text
docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md
```

The safe claim is deliberately small:

```text
a compact finite weighted projection-order artifact note with an exact 2 x 2 witness
```

It is not:

```text
new ANOVA theory
new dependent-input Hoeffding decomposition theory
new Sobol/Shapley sensitivity theory
new noncommuting projection theory
MaoField empirical evidence
```

## Verified Bibliography Floor

The following records were checked by DOI/Crossref or arXiv metadata on
2026-06-29 CST before being added to the local positioning record.

| Role | Record | Stable id | Positioning effect |
|---|---|---|---|
| dependent-variable functional ANOVA diagnostics | Giles Hooker, "Generalized Functional ANOVA Diagnostics for High-Dimensional Functions of Dependent Variables", Journal of Computational and Graphical Statistics, 2007 | DOI `10.1198/106186007x237892` | Forces the note to avoid claiming broad novelty over weighted/dependent-variable ANOVA diagnostics. |
| dependent-variable Hoeffding-Sobol decomposition | Gaelle Chastaing, Fabrice Gamboa, Clementine Prieur, "Generalized Hoeffding-Sobol decomposition for dependent variables - application to sensitivity analysis", Electronic Journal of Statistics, 2012 | DOI `10.1214/12-ejs749` | Forces the note to avoid claiming a new dependent-input Hoeffding decomposition. |
| dependent-variable numerical sensitivity methods | G. Chastaing, F. Gamboa, C. Prieur, "Generalized Sobol sensitivity indices for dependent variables: numerical methods", Journal of Statistical Computation and Simulation, 2014/2015 | DOI `10.1080/00949655.2014.960415` | Forces the note to avoid presenting itself as a general numerical decomposition method. |
| dependent-input importance | Art B. Owen, Clementine Prieur, "On Shapley Value for Measuring Importance of Dependent Inputs", SIAM/ASA Journal on Uncertainty Quantification, 2017 | DOI `10.1137/16m1097717` | Forces the note to distinguish order-artifact diagnosis from dependent-input importance allocation. |
| correlated-input sensitivity | Bertrand Iooss, Clementine Prieur, "Shapley effects for sensitivity analysis with correlated inputs: comparisons with Sobol' indices, numerical estimation and applications", International Journal for Uncertainty Quantification, 2019 | DOI `10.1615/int.j.uncertaintyquantification.2019028372` | Forces the note to avoid claiming a Sobol/Shapley alternative. |
| dependent random variables Hoeffding decomposition | Marouane Il Idrissi, Nicolas Bousquet, Fabrice Gamboa, Bertrand Iooss, Jean-Michel Loubes, "Hoeffding decomposition of functions of random dependent variables", Journal of Multivariate Analysis, 2025 | DOI `10.1016/j.jmva.2025.105444` | Very close broad-theory neighbor; forces explicit "not a new dependent-variable Hoeffding theory" wording. |
| non-independent ANOVA-type decompositions | Matieyendou Lamboni, "On ANOVA-Type Decompositions of Functions with Non-independent Variables: Sensitivity Analysis", SIAM/ASA Journal on Uncertainty Quantification, DOI / publisher online record status only for current drafting | DOI `10.1137/24m1712680` | New near-neighbor; forces the note to frame itself as a finite weighted projection-order artifact, not an ANOVA-type decomposition program. Do not rely on this local record as final camera-ready print metadata. |
| two projections background | A. Boettcher, I. M. Spitkovsky, "A gentle guide to the basics of two projections theory", Linear Algebra and its Applications, 2010 | DOI `10.1016/j.laa.2009.11.002` | Forces the note to avoid claiming new two-projections theory. |
| products of orthogonal projections | Gustavo Corach, Alejandra Maestripieri, "Products of orthogonal projections and polar decompositions", 2010 | arXiv `1011.5237` | Projection-product background; not an exact duplicate. |
| classical two-subspace theory | P. R. Halmos, "Two subspaces", Transactions of the American Mathematical Society, 1969, 144, 381-389 | DOI `10.1090/S0002-9947-1969-0251519-5` | Classical projection/subspace background; not an exact duplicate. |

## Positioning Paragraph For Drafting

Closest antecedents lie in dependent-variable ANOVA-Hoeffding decompositions
and in the classical theory of two noncommuting orthogonal projections. This
note does not propose a new ANOVA, Sobol, Shapley, dependent-input
decomposition, or projection theory. It isolates a finite weighted
projection-order artifact in a two-way table: under non-product cell weights,
sequential nuisance stripping can produce a nonzero wrong-order residual from
a pure main-effect signal even though the true additive residual is zero.

## Harness Boundary

The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats.

## Duplicate-Risk Status

No exact duplicate is identified by the current Pro audit or the local DOI/arXiv
record checks above. The risk is instead overclaiming into already occupied
broad theory. The draft must keep the contribution at this level:

```text
finite positive weighted two-way table
product-weight iff main-effect orthogonality
order-independence iff product weights
existential non-product pure-main-effect witness
exact 2 x 2 rational certificate
```

Do not promote this into continuous measures, general dependent-input
decompositions, a completed formal system, or MaoField empirical evidence.
