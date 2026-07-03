# GPT-5.5 Pro Zero-Context Prompt: MaoField Formal Preprint V2.2 Strict Review

You are GPT-5.5 Pro acting as a severe mathematical referee and scientific
editor. You are reviewing a local MaoField draft under lock:

```text
docs/infra/debranded_residual_transport/PREPRINT_DRAFT_PROGRAMMATIC_V2_2_UNDER_LOCK_20260703.tex
```

Use only the attached package files as project evidence. Do not use public
GitHub, previous chat memory, or unprovided repository assumptions for project
facts. You may use external academic sources only to verify bibliography and
related-work metadata.

## Required Verdict

Choose exactly one:

```text
PASS_TO_PI_FINAL_LOCAL_REVIEW_UNDER_LOCK
REQUEST_MATHEMATICAL_PATCH_BEFORE_PI_REVIEW
REQUEST_BIBLIOGRAPHY_PATCH_BEFORE_PI_REVIEW
REQUEST_BOUNDARY_WORDING_PATCH_BEFORE_PI_REVIEW
STOP_DO_NOT_PREPRINT
```

`PASS_TO_PI_FINAL_LOCAL_REVIEW_UNDER_LOCK` is not release, posting, submission,
paper-ready, or preprint-ready authorization.

## Core Mathematical Claims To Check

- finite positive weighted two-way table;
- weighted Hilbert space `L^2(w)`;
- constant subspace `C`;
- centered row-main-effect space `A`;
- centered column-main-effect space `B0`;
- additive nuisance space `N_add = C + A + B0`;
- product weights iff `A` is orthogonal to `B0`;
- order-independence iff product weights;
- non-product weights give an existential pure-main-effect witness, not a
  universal statement about every input;
- wrong-order nonzero output is a sequential stripping artifact, not a true
  interaction residual;
- exact 2 x 2 rational witness with
  `||R_{Q->B}K||_w^2 = 61/177408`.

## Mandatory Boundary Sentence

The following sentence must appear verbatim:

```text
The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats.
```

## Bibliography Floor

Verify that the draft includes and correctly positions:

- Hooker 2007, DOI `10.1198/106186007X237892`;
- Chastaing, Gamboa, Prieur 2012, DOI `10.1214/12-EJS749`;
- Chastaing, Gamboa, Prieur 2015, DOI `10.1080/00949655.2014.960415`;
- Owen and Prieur 2017, DOI `10.1137/16M1097717`;
- Iooss and Prieur 2019, DOI
  `10.1615/INT.J.UNCERTAINTYQUANTIFICATION.2019028372`;
- Il Idrissi et al. 2025, DOI `10.1016/j.jmva.2025.105444`;
- Lamboni DOI record `10.1137/24M1712680`, without overclaiming print status
  if uncertain;
- Boettcher and Spitkovsky 2010, DOI `10.1016/j.laa.2009.11.002`;
- Corach and Maestripieri, arXiv `1011.5237`;
- Halmos 1969, DOI `10.1090/S0002-9947-1969-0251519-5`;
- LLM evaluation context: HELM, BIG-bench, LLM-as-judge, contamination,
  hallucination/truthfulness, and trustworthiness evaluations.

The exact duplicate-risk status must remain:

```text
MEDIUM duplicate risk
```

## Forbidden Claims

Reject the draft if it claims any of:

- paper-ready, preprint-ready, public-postable, posted, submitted, accepted, or
  submission-authorized;
- broad new ANOVA theory;
- broad new dependent-input decomposition theory;
- broad new noncommuting-projection theory;
- completed formal system;
- MaoField empirical positive result;
- full panel has run;
- checkpoint inference;
- training;
- new loss;
- observed MaoField residual, interaction, transport, or holonomy field;
- glass box broken;
- F3 positive;
- LOSO passed;
- JSON floats prove theorem;
- harness proves theorem.

Mode B MaoField empirical status remains:

```text
insufficient_artifact
```

## Output

Return:

1. final verdict;
2. concise theorem/proof audit;
3. exact witness arithmetic audit;
4. bibliography metadata audit;
5. forbidden-claim scan;
6. required patch list, if any;
7. whether the draft may proceed to PI final local review under lock.
