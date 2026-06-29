# GPT-5.5 Pro Zero-Context Prompt: Order-Defect Paper Draft v1.6

Use the uploaded zip as the primary evidence bundle for local repository facts.
Do not use public GitHub, raw GitHub URLs, search-engine snippets, or model
memory as evidence for local files. If a local file is absent from the bundle,
say so. You may use external scholarly search only for bibliography metadata,
duplicate-risk checking, and citation cleanup; cite stable records such as DOI,
arXiv, publisher pages, MathSciNet, zbMATH, or Crossref. Treat chat-internal
citation handles as non-evidence.

Repository/project context inside the bundle: MaoField is only the storage
container for this debranded Mode A finite-dimensional mathematics line. This
task is not MaoField empirical validation.

## Mission

Act as a strict mathematics professor, proof auditor, and academic-compliance
reviewer. The goal is to produce a short paper draft only if the v1.6
wording-lock gate passes.

First run the gate below. Do not draft the paper until the gate passes.

## Gate 1 -- v1.6 Wording Lock

Verify that the following sentence appears word-for-word in all five target
locations:

```text
The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats.
```

Required target files:

```text
from_repo/docs/infra/debranded_residual_transport/README.md
from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md
from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md
from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json
from_repo/scripts/debranded_residual_transport_harness_v1_3.py
```

If any target file fails, stop and return:

```text
gate_failed_wording_cleanup_incomplete
```

Then list missing files or line references. Do not write the paper in that
case.

## Gate 2 -- Evidence And Scope

If Gate 1 passes, verify that the bundle still preserves these boundaries:

- finite positive weighted two-way table only;
- product-weight iff centered main-effect orthogonality;
- order-independence iff product weights;
- non-product weights give an existential pure-main-effect witness, not a
  universal claim about every input;
- wrong-order nonzero output is a sequential stripping artifact, not a true
  interaction residual;
- exact `2 x 2` rational witness remains the certificate-level example;
- floating-point harness is deterministic regression support only;
- local ceiling remains `definitions_and_harness_viable_only`;
- Mode B MaoField empirical status remains `insufficient_artifact`.

If any boundary fails, stop and return:

```text
gate_failed_scope_or_evidence_boundary
```

Do not write the paper in that case.

## Primary Files To Inspect

```text
from_repo/STATE.md
from_repo/MD_CATALOG.md
from_repo/docs/infra/debranded_residual_transport/README.md
from_repo/docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md
from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md
from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md
from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md
from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md
from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json
from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md
from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json
from_repo/scripts/debranded_residual_transport_harness_v1_3.py
from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_v1_5_final_gate_audit_20260629.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_V1_5_FINAL_GATE_AUDIT_ADOPTION_NOTE_20260629.md
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_v1_4_exact_bibliography_audit_20260629.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_V1_4_EXACT_BIBLIOGRAPHY_AUDIT_ADOPTION_NOTE_20260629.md
from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_preprint_rigor_audit_20260629.md
from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_PREPRINT_RIGOR_AUDIT_ADOPTION_NOTE_20260629.md
```

## If Both Gates Pass: Draft The Short Note

Draft a self-contained 4-6 page short note in LaTeX-style Markdown. Use the
working title:

```text
A Finite Weighted Two-Way Projection-Order Artifact with an Exact 2 x 2 Witness
```

Required structure:

1. Abstract.
2. Introduction and narrow motivation.
3. Finite weighted setup: `X=Q x B`, positive probability weights, weighted
   Hilbert space, constant subspace `C`, centered row subspace `A`, centered
   column subspace `B0`, additive nuisance space `N=C+A+B0`.
4. Product-weight iff theorem for `A ⟂ B0`; include proof in finite sums.
5. Ordered stripping theorem for `R_Q_then_B` and `R_B_then_Q`; state exactly
   when they agree and why non-product weights imply only an existential
   witness.
6. Pure-main-effect no-go example: exact `2 x 2` rational witness, including
   `w`, `K`, `(I-P_N)K=0`, `R_B_then_Q K=0`, `R_Q_then_B K`, and
   `||R_Q_then_B K||_w^2 = 61/177408`.
7. A short harness paragraph containing the canonical harness sentence exactly
   once.
8. Related work paragraph: dependent-variable ANOVA/Hoeffding/Sobol/Shapley
   neighbors and two-projection background. Emphasize that this is not a new
   ANOVA theory, not a new dependent-input decomposition theory, and not a new
   noncommuting projection theory. For Lamboni 2026, verify citation metadata;
   if print metadata is after 2026-06-29, cite DOI/online record without
   implying a print date that has not happened.
9. Limitations and evidence boundary.
10. References with stable DOI/arXiv identifiers.

## Required Bibliography Floor

Position against at least:

```text
Hooker 2007, DOI 10.1198/106186007x237892
Chastaing, Gamboa, Prieur 2012, DOI 10.1214/12-ejs749
Chastaing, Gamboa, Prieur 2014/2015, DOI 10.1080/00949655.2014.960415
Owen and Prieur 2017, DOI 10.1137/16m1097717
Iooss and Prieur 2019, DOI 10.1615/int.j.uncertaintyquantification.2019028372
Il Idrissi et al. 2025, DOI 10.1016/j.jmva.2025.105444
Lamboni 2026, DOI 10.1137/24m1712680
Bottcher and Spitkovsky 2010, DOI 10.1016/j.laa.2009.11.002
Corach and Maestripieri, arXiv:1011.5237
Halmos 1969, DOI 10.1090/S0002-9947-1969-0251519-5
```

## Forbidden Claims

Do not claim:

- MaoField empirical positive result;
- full panel has run;
- 16-cell aggregate exists;
- checkpoint loading, inference, training, or new loss is authorized;
- MaoField residual / interaction / quotient-residual / transport / holonomy
  field has been observed;
- glass box broken;
- F3 positive or LOSO passed;
- completed formal system;
- broad new ANOVA theory;
- broad new dependent-input decomposition theory;
- broad new noncommuting projection theory;
- holonomy, gluing, sheaf, or curvature result;
- JSON floats or the deterministic harness prove the theorem.

## Output Format

Return in this order:

1. `gate_verdict`: PASS or FAIL for Gate 1 and Gate 2.
2. If any gate fails: blocker list only.
3. If both gates pass: the full paper draft.
4. After the draft: a short “claim boundary audit” listing exactly what the
   draft does and does not claim.

Be severe. Prefer a smaller correct note over a broader impressive one.
