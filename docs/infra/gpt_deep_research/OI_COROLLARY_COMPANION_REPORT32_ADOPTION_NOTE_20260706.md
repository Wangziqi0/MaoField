# OI Corollary Companion Report32 Adoption Note

Date verified: 2026-07-06 21:16:29 CST on node36.

Source attachment:

```text
/home/amd/.codex/attachments/2aab21c2-bd6b-45c2-8cd7-df93f82ab367/deep-research-report (2).md
```

Archived report:

```text
docs/infra/gpt_deep_research/deep_research_oi_corollary_companion_report32_20260706.md
```

Source attachment sha256:

```text
78874b19a1927aa09589ac864c23e4b70946b03772bf8dd129dc0649a0828546
```

Archived normalized report sha256:

```text
16983dce63d992ec8573ddc6e8e458b8ea70524ed4f332c32a3b1dc826e359c9
```

## Pro Verdict

Adopt the report's exact final action:

```text
DRAFT_ONE_PAGE_OI_COROLLARY_COMPANION
```

The report validates the bounded corollary candidate:

```text
OI^{op}_{N_add}(w) = 0 iff w is product form
```

under the finite positive weighted two-way table setting of v1.3.

## Local Adoption

Node36 action:

```text
ACCEPT_REPORT32_AND_WRITE_BOUNDED_OI_COROLLARY_COMPANION
```

Implemented note:

```text
docs/infra/debranded_residual_transport/FORMAL_NOTE_OI_COROLLARY_COMPANION_20260706.md
```

This is a one-page corollary companion to v1.3. It is not a patch to the
current Zenodo V2.5 preprint and it does not merge the separate v1.5 GQ-FCR
note into the order-defect theorem spine.

## Proof Dependency

The corollary depends on:

- v1.3 Proposition 1: product weights iff `A` is orthogonal to `B0`;
- v1.3 Proposition 2: `D_w=0` iff product weights;
- v1.3 Proposition 3: non-product weights admit an existential pure
  main-effect witness in `N_add` with zero true additive residual but nonzero
  wrong-order sequential output;
- the elementary finite-dimensional fact that a restricted operator norm is
  zero iff the restricted operator is the zero map.

## Local Verification

No new empirical experiment was run. Node36 reran exact-support scripts in SSD
scratch only:

```text
/home/amd/codex-node36/tmp/oi_corollary_companion_20260706_2015/verify/
```

Results:

```text
v1.4 exact witness all_checks_passed=True
v1.4 exact JSON sha256=0a786eff756f6e61ed00d9f236e3dbe05d7f9341ac082fbb159e2ae3a94dc0b6
v1.5 GQ-FCR all_checks_passed=True
v1.5 exact JSON sha256=01d3d452da17b0b7d1d1ad7b169c30a2b26d9098a4d1060703cc51cf9a856231
```

The v1.4/v1.5 exact JSON outputs match canonical files byte-for-byte. These
scripts are support checks only; the corollary is carried by the analytic proof
and v1.3 propositions, not by JSON or deterministic harness output.

## Boundary

No current action may claim:

- MaoField empirical positive result;
- full panel, training, inference, checkpoint loading, new loss, F3 positive,
  LOSO passed, or glass-box success;
- observed residual, interaction, transport, holonomy, or gluing field;
- broad new ANOVA, dependent-input, projection, sheaf, contextuality,
  consistency-radius, or dynamic-collapse theory;
- proof by deterministic harness or JSON floats;
- paper-ready, peer-reviewed, arXiv-submitted, or journal-submitted status.

Mode B remains:

```text
insufficient_artifact
```

Duplicate risk remains:

```text
MEDIUM
```
