# GPT-5.5 Pro Zero-Context Prompt: OI Corollary Companion Review

You are GPT-5.5 Pro acting as a strict mathematical referee and rescue editor.
Use the uploaded package as your source of truth. Do not use public GitHub,
search-engine snippets, model memory, or assumptions about private repository
state. If a needed file is missing, request it from node36 explicitly.

Repository/project context:

```text
Project: MaoField
Author: Yifan Chen
Current public formal preprint DOI: 10.5281/zenodo.21190475
Current public repo/software DOI: 10.5281/zenodo.21157578
Current local status: Mode A exact finite mathematics only; Mode B empirical
MaoField status remains insufficient_artifact.
```

Your task is not to validate a MaoField empirical claim. Your task is to decide
whether the following bounded exact-math candidate can be written as a one-page
corollary companion to the existing v1.3 finite order-defect note:

```text
OI^{op}_{N_add}(w) = 0 iff w is product form
```

Use this definition unless you find a flaw:

```text
OI^{op}_{N_add}(w) := ||D_w restricted to N_add||_{L2(w)->L2(w)}
```

where the base object is a finite positive weighted two-way table
`X = Q x B`, with weighted Hilbert space `R^{Q x B}`, subspaces `C`, `A`,
`B0`, additive nuisance space `N_add = C direct-sum A direct-sum B0`, ordered
stripping maps `R_Q_then_B`, `R_B_then_Q`, and order-defect operator
`D_w = R_Q_then_B - R_B_then_Q`.

Read these files first:

```text
from_repo/STATE.md
from_repo/MD_CATALOG.md
from_repo/docs/infra/recovery/MAOFIELD_D706_OI_COROLLARY_COMPANION_TASKBOOK_20260706.md
from_repo/docs/infra/recovery/D706_OI_COROLLARY_NEXT_PRO_RAG_STATUS_SYNTHESIS_20260706.md
from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md
from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md
from_repo/docs/infra/debranded_residual_transport/METRIC_OBJECT_IDENTITY_EXACT_NOTES_INDEX_20260706.md
from_repo/docs/infra/gpt_deep_research/deep_research_metric_identity_oi_corollary_decision_report31_20260706.md
from_repo/docs/infra/gpt_deep_research/METRIC_IDENTITY_OI_COROLLARY_DECISION_REPORT31_ADOPTION_NOTE_20260706.md
```

Then consult report30/report25/report26 only for programme-language
provenance, not for proof authority. The v1.5 GQ-FCR files are included only
as boundary context and must not be merged into this corollary unless you
explicitly argue for a separate future task.

Check the proof chain strictly:

1. v1.3 Proposition 1: finite positive product weights iff `A` is orthogonal
   to `B0` under the weighted inner product.
2. v1.3 Proposition 2: `D_w=0` iff product weights, and the ordered stripping
   maps are equal iff product weights.
3. v1.3 Proposition 3: if weights are non-product, there exists a pure
   main-effect witness in `A` or `B0` whose true additive residual is zero but
   the wrong ordered stripping output is nonzero.
4. Verify whether these imply the restricted operator corollary:

```text
OI^{op}_{N_add}(w)=0 iff w is product form.
```

Be especially alert to these failure modes:

- turning an existential witness into a universal statement;
- treating a wrong-order sequential output as a true interaction residual;
- confusing `I-P_N` with ordered stripping products;
- treating deterministic harnesses or JSON floats as proofs;
- broadening a finite corollary into a general ANOVA, dependent-input,
  projection, sheaf, contextuality, or dynamic-collapse theory;
- making any MaoField empirical-positive claim.

You must choose exactly one final action:

```text
DRAFT_ONE_PAGE_OI_COROLLARY_COMPANION
PATCH_DEFINITION_THEN_RECHECK
REJECT_OR_DEFER_DUE_TO_PROOF_GAP
REQUEST_NODE36_FILES
```

If you choose `DRAFT_ONE_PAGE_OI_COROLLARY_COMPANION`, output:

1. a short verdict saying why the corollary is valid;
2. a clean definition of `OI^{op}_{N_add}(w)`;
3. a theorem statement in finite positive weighted two-way tables;
4. a proof of both directions using only v1.3 propositions and elementary
   finite-dimensional facts;
5. a boundary paragraph stating what this does not prove;
6. a note on whether it should be a separate one-page companion rather than a
   patch to the current Zenodo V2.5 preprint.

If you choose any other action, give the smallest exact blocker list and do
not draft the corollary.

Forbidden claims:

```text
MaoField empirical positive result
full panel has run
checkpoint loading / inference / training / new loss
observed residual / interaction / transport / holonomy / gluing field
glass box broken
F3 positive or LOSO passed
broad new ANOVA / dependent-input / projection / sheaf / contextuality theory
JSON floats prove theorem
deterministic harness proves theorem
paper-ready, peer-reviewed, arXiv-submitted, or journal-submitted
```

Remember: the desired output is a rigorous go/no-go decision for one small
finite corollary. If you can make it elegant, do so by making it narrower, not
larger.
