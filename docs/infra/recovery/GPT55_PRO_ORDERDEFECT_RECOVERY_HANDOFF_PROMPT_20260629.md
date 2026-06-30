# GPT-5.5 Pro Zero-Context Prompt: MaoField / Order-Defect Recovery Handoff

You are receiving a local evidence bundle prepared on node36:

```text
MaoField_OrderDefect_Recovery_20260625_20260629.zip
```

Do not use public GitHub, public web browsing, search snippets, or model memory
as substitutes for the files inside the bundle. Treat the bundle contents as
the only local evidence source. If a fact is not in the bundle, say
`insufficient_artifact`.

Your task is not to write a paper immediately. First perform a strict recovery
audit of the 2026-06-25 through 2026-06-29 MaoField / Order-Defect / Mode A
finite-dimensional mathematics line.

Read these files first:

```text
docs/infra/recovery/HANDOFF_TO_GPT55PRO_20260629.md
docs/infra/recovery/GATE_RESCUE_AUDIT_20260629.md
docs/infra/recovery/MATH_PROOF_RESCUE_AUDIT_20260629.md
docs/infra/recovery/BIBLIOGRAPHY_RESCUE_AUDIT_20260629.md
docs/infra/recovery/FORBIDDEN_CLAIMS_SCAN_20260629.md
docs/infra/recovery/EVIDENCE_INDEX_SINCE_20260625.md
docs/infra/recovery/RECOVERY_TIMELINE_SINCE_20260625.md
STATE.md
```

Important current status:

- Gate 1, the v1.6 wording lock, is reported as PASS.
- Gate 2, the evidence/scope boundary, is reported as PASS.
- The forbidden-claims scan reports zero automated BLOCKER lines, but many
  WARNING lines that must be treated as risk locators.
- `STATE.md` contains an external-model emergency lock: current OpenAI/Pro
  output is `non_authoritative_scratch` / `gate_only_audit` only until a human
  explicitly lifts that lock.

Therefore your recommended action must remain one of:

```text
STOP_AND_FIX_GATES
DRAFT_SHORT_NOTE_WITH_BOUNDARIES
DO_NOT_DRAFT_EVIDENCE_INSUFFICIENT
```

But under the current emergency lock, do not choose
`DRAFT_SHORT_NOTE_WITH_BOUNDARIES` unless you explicitly explain that the lock
has been lifted by the user or that your output is only a non-authoritative
drafting sketch, not proof authority, bibliography authority, or posting
authority.

Minimal safe mathematical object:

In a finite positive weighted two-way table `X = Q x B`, centered row and
column main-effect subspaces are orthogonal exactly when the cell weights
factor as product weights. The two sequential nuisance-stripping maps are
order-independent exactly in the product-weight case. Under non-product
weights, there exists a pure main-effect witness whose true additive residual
is zero but whose wrong-order sequential stripping residual is nonzero. That
nonzero output is a sequential stripping artifact, not a true interaction
residual and not a product-measure Hoeffding interaction. The current exact
witness is a `2 x 2` rational example; the floating-point harness is
deterministic regression support only.

Forbidden claims:

- MaoField empirical positive result.
- full panel or 16-cell aggregate completed.
- checkpoint loading, inference, training, or new loss authorization.
- observed MaoField residual / interaction / quotient-residual / transport /
  holonomy field.
- glass box broken, F3 positive, or LOSO passed.
- completed formal system.
- broad new ANOVA, dependent-input decomposition, or noncommuting projection
  theory.
- JSON floats or deterministic harness prove the theorem.

Required output:

1. State whether the bundle is internally coherent.
2. State whether Gate 1 and Gate 2 are truly supported by the included files.
3. Identify any proof gaps, citation risks, stale files, or claim-boundary
   risks.
4. Decide whether the next action is `STOP_AND_FIX_GATES`,
   `DRAFT_SHORT_NOTE_WITH_BOUNDARIES`, or `DO_NOT_DRAFT_EVIDENCE_INSUFFICIENT`.
5. If you recommend drafting later, give only a guarded outline and exact
   required fixes. Do not write the paper body unless the user separately lifts
   the emergency lock and explicitly asks for a draft.
