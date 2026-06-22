# MaoField q4 Panel Multi-Checkpoint Smoke Record

> Generated on node36 at 2026-06-22 21:49 CST.
> This is a multi-point smoke record, not a full panel verdict.

## Boundary

- Three single-checkpoint CPU fp32 smokes were checked.
- No 50-checkpoint panel was generated.
- No training, backward pass, optimizer step, EMA update, text generation, or
  new loss was run.
- These smokes only reduce the risk that the generator path is hard-coded to
  seed1/gen0.

## Result

- Overall status: **pass**
- All three points have `old_aggregate_reproduction = pass`.
- New v3 manifests include `builder_script_sha256` and
  `generator_script_sha256`.

## Points

| seed | generation | manifest artifact version | reproduction | n_tokens | global_ppl | primary_projection_P |
|---:|---:|---|---|---:|---:|---:|
| 1 | 0 | `2026-06-22.d622.generator.v1` | pass | 8064 | 23.626112493679635 | 1.4694237198551585 |
| 2 | 5 | `2026-06-22.d622.generator.v3` | pass | 8064 | 38.61973032596258 | 1.6308561208667203 |
| 42 | 9 | `2026-06-22.d622.generator.v3` | pass | 8064 | 30.566837397951986 | 1.5595813393211577 |

## Raw Rows

Raw token rows remain outside git under:

```text
/media/amd/raid1/canonical/wip/maofield_panel_primary_20260622/raw/
```

SHA256:

```text
seed1/gen0   90e5104f714306f7e1eaa7c14b26aa8333f4c42ad0e684521e757efa992d5dbe
seed2/gen5   3449396dc2378c939d8ae10f8fa95d6b3e786f68c0fc307f7bdbbd10c6b440cc
seed42/gen9  6f434848b7024e20c01c1a401a15b09145e3e0c103f4d4a7dc544b478b090338
```

## Remaining Blockers

This record does not approve full panel generation. Remaining blockers before
any 50-checkpoint launch:

- full-panel generator mode is not implemented;
- separate fold-local q4 analysis path is not implemented;
- PI/PRO has not approved 50-checkpoint generation.
