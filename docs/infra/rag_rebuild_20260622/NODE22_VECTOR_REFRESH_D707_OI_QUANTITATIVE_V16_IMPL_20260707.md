# Node22 Vector Refresh -- D707 Quantitative OI Norm v1.6 Implementation

Date verified on node36: 2026-07-07 09:31 CST.

Status:

```text
PROMOTED_AND_NODE22_STOPPED_OI_QUANTITATIVE_V16_IMPL
```

This RAG-sync record covers the local implementation of Pro report33 as a
bounded v1.6 quantitative OI norm companion:

```text
PROVE_QUANTITATIVE_OI_NORM_RESULT
IMPLEMENT_BOUNDED_QUANTITATIVE_OI_NORM_COMPANION
```

The refresh makes the following newly promoted or modified files discoverable:

```text
STATE.md
MD_CATALOG.md
docs/infra/debranded_residual_transport/README.md
docs/infra/debranded_residual_transport/METRIC_OBJECT_IDENTITY_EXACT_NOTES_INDEX_20260706.md
docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_6_QUANTITATIVE_OI_NORM_20260707.md
docs/infra/debranded_residual_transport/EXACT_OI_QUANTITATIVE_V1_6_20260707.md
docs/infra/debranded_residual_transport/exact_oi_quantitative_v1_6_20260707.json
scripts/debranded_residual_transport_exact_oi_quantitative_v1_6.py
docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_D707_OI_QUANTITATIVE_V16_IMPL_20260707.md
```

The implemented finite theorem is:

```text
OI^{op}_{N_add}(w)
  = max_j rho_j sqrt(1-rho_j^2),
```

where `rho_j` are the principal-angle / canonical-correlation invariants
between `A` and `B0`, equivalently the nonzero singular values of
`Z_w=(w-w_Q otimes w_B)/sqrt(w_Q w_B)`.

Exact support checks:

```text
witness rho^2 = 1/672
(OI^{op}_{N_add})^2 = 671/451584
product control = 0
ratio to old v1.4 fixed-witness artifact norm = 121/28
```

To avoid self-referential hash drift, exact live hashes, scope counts,
candidate verification, node22 start/stop logs, and smoke output are stored in
non-Markdown sidecars with this tag:

```text
20260707_0931_oi_quantitative_v16_impl
```

Required checks:

- node22 is used only as a temporary embedding worker;
- node36 owns scope, build logs, verification, promotion, and smoke queries;
- node22 temporary service is stopped after use;
- smoke locates the v1.6 formal note, exact support artifact, script, exact
  `671/451584` value, and the principal-angle formula.

RAG remains a locator only. The mathematical claim is carried by the analytic
finite-dimensional proof in the v1.6 formal note. The exact JSON and Markdown
support artifacts are not proof authority.

## Claim Boundary

This refresh supports discovery of the v1.6 quantitative OI norm companion
only. It does not authorize:

- current Zenodo V2.5 preprint patching;
- broad ANOVA, dependent-input, projection, sheaf, contextuality,
  consistency-radius, or dynamic-collapse theory;
- MaoField empirical positive claims;
- full panel, checkpoint loading, inference, training, or new loss;
- observed residual, transport, holonomy, interaction, or gluing fields;
- proof-by-JSON or proof-by-deterministic-harness wording.

Mode B MaoField empirical status remains:

```text
insufficient_artifact
```
