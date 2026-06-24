# Residual Transport / Holonomy Adoption Note

Date: 2026-06-24 CST

## Source

Archived GPT/PRO report (23):

```text
docs/infra/gpt_deep_research/deep_research_residual_transport_holonomy_split_project_20260624.md
```

Attachment SHA256:

```text
78ae75a38c5b0a1c8bd2ad2297abf8382ff13550ade972f06cac4eaa779d2de7
```

Canonical archive SHA256 after trailing-whitespace normalization:

```text
3025217867b1a70f226ed77f5f22ac4297e1eea4768f5e8613f98a16613753f5
```

This note is the node36 interpretation layer. Treat the report as a
claim-source Mode A mathematical proposal, not as new MaoField evidence.

## Local Decision

Adopt report (23) as the strongest current recommendation for the Mode A line:

```text
split the mathematics into a debranded finite-dimensional operator/no-go
project; keep MaoField empirical Mode B at insufficient_artifact /
smoke_conjecture_only.
```

Do not treat the report as a request or authorization to create a new repository
yet. It is a direction proposal pending PI decision.

## Adopted Mathematical Object

Adopt the proposed refinement of the mother object. The single-scale quotient
residual

```text
R_t = Pi_{N_perp,w} K_t
```

is still useful, but report (23) correctly identifies it as too easy to confuse
with rank-1 shadows, random same-dimension subspaces, or scale-choice artifacts.

The cleaner Mode A object is a finite scale-lattice residual transport system:

```text
scale s in Sigma
admissible triple (X_s, w_s, N_s)
weighted projection P_s = Pi_{N_s_perp,w_s}
coarsening map C_rho: H_s -> H_s'
local residual R_s(K) = P_s K_s
edge defect D_rho(K) = C_rho P_s K - P_s' C_rho K
square holonomy defect H_square(K) = difference between two coarsening /
projection paths around a refinement square
```

The proposed bottom-level question becomes:

```text
When do all edge defects and square holonomy defects vanish, while the residual
subspaces remain distinguishable from rank-1 shadows and random same-dimension
subspaces?
```

Positive answer: a transport-stable, gluable, non-random residual object exists.
Negative answer: the apparent structure was coordinate, scale, nuisance, or
projection artifact.

## Adopted No-Go Agenda

Adopt these Mode A theorem / counterexample targets:

- rank-1 shadow vacuity: principal-angle stability is meaningless until
  `sigma2/sigma1` clears the rank-shadow floor;
- square holonomy no-go: if every coarsening edge commutes with projection, all
  refinement-square holonomy defects vanish; nonzero holonomy proves at least
  one non-functorial nuisance or failed coarsening naturality condition;
- local gluing absorption: local mismatch is not an obstruction if allowed
  pre-registered local nuisance can absorb it;
- random same-dimension no-go: a residual subspace that does not beat random
  same-dimensional subspaces has no coordinate-invariant structural meaning;
- transport-stable rank: classify minimal effective residual rank under
  coarsening, holonomy, random-subspace, and rank-shadow guards.

## Mode B Boundary

The MaoField-specific verdict remains unchanged:

```text
stable non-scalar residual object: insufficient_artifact
existing interaction smoke: smoke_conjecture_only
```

Blocked claims remain blocked:

- no full panel has run;
- no 16-cell full-panel aggregate exists;
- no hypercube residual / interaction / quotient-residual field has been
  observed;
- no LOSO pass, F3 positive, or glass-box breakthrough is authorized;
- no training or new loss work is authorized;
- current smoke remains smoke-only and is below the D624 rank-shadow
  design-review floor (`sigma2/sigma1 >= 0.25`).

## Local Consequence

Use report (23) to guide the next decision conversation:

1. Keep current MaoField empirical line negative-centered and evidence-gated.
2. Consider a separate, debranded mathematical project around finite
   scale-lattice residual transport, holonomy defects, and no-go classification.
3. Before any real aggregate or GPU work, first write a zero-GPU synthetic
   theorem/counterexample harness for:
   `scale_square_holonomy`, `nuisance_functoriality_digest`,
   `rank1_angle_vacuity_guard`, and `random_same_dim_angle_gap`.
4. Do not add these as empirical requirements to MaoField until PI explicitly
   decides whether to split the line or keep it as a MaoField subprogram.

## Non-Adoption

Do not adopt report (23)'s "split into a new project" line as an already-made
project-management decision. Adopt it only as the current best mathematical
recommendation to present to PI.

Do not create, train, or run a full-panel path from this report alone.
