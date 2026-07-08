# D708 Internal V0 Gate Repair Package Taskbook

- Date verified on node36: `2026-07-08 11:27 CST`
- Project root: `/media/amd/raid1/canonical/projects/MaoField`
- Current HEAD before repair package edits: `e8ef5c0`
- Report39 verdict: `REQUEST_NODE36_FILES`

## Purpose

Prepare a repair/recheck package for the D708 internal-v0 promotion gate after
Report39 found package/provenance gaps.

The repair target is not a new mathematical theory. The target is to close the
evidence-package gap and ask Pro to recheck the same narrow object:

```text
docs/infra/debranded_residual_transport/FORMAL_NOTE_D707_CHART_PATH_CYCLE_DEFECT_V0_20260707.md
```

## Report39 Blockers To Close

The repair package must include:

1. `docs/infra/recovery/d707_split_loop_outputs/loop0/LOOP_STATUS_LOOP0_20260707.md`
2. `docs/infra/recovery/d707_split_loop_outputs/loop3/LOOP_STATUS_LOOP3_20260707.md`
3. `docs/infra/recovery/d707_split_loop_outputs/loop4/LOOP_STATUS_LOOP4_20260707.md`
4. `docs/infra/MAOFIELD_PRO_D708_INTERNAL_V0_PROMOTION_GATE_PACKAGE_20260708.md`
5. `docs/infra/MAOFIELD_PRO_D708_INTERNAL_V0_PROMOTION_GATE_NODE19_DELIVERY_20260708.md`
6. `docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_D708_INTERNAL_V0_GATE_PACKAGE_20260708.md`
7. project rule files or explicit package mappings:
   - `AGENTS.md`
   - `/media/amd/raid1/canonical/AGENTS.md`
   - `CLAUDE.md`
8. report39 archive and adoption note.

## Important Self-Reference Rule

The repair package must not require `STATE.md` to contain the zip's own final
SHA256. A zip cannot contain a file that already knows the final hash of the zip
that contains it.

For package integrity, use:

- external `SHA256SUMS_...txt` delivered alongside the zip;
- internal payload checksum file;
- node19 delivery readback;
- canonical package/delivery records.

## Required Pro Recheck

Pro should answer:

1. Did the repair package close the Report39 package/provenance blockers?
2. Does the internal v0 mathematical body remain correct and bounded?
3. Are any new package inconsistencies present?
4. Is the correct next action `KEEP_INTERNAL_ONLY`, `PATCH_AND_RECHECK`,
   `STOP_PARK`, or `REQUEST_MORE_FILES`?

## Allowed Verdicts

Pro must choose exactly one:

```text
ACCEPT_INTERNAL_V0_AS_LOCAL_NOTE_ONLY
PATCH_INTERNAL_V0_THEN_RECHECK
REJECT_OR_STOP_PARK
REQUEST_NODE36_FILES
```

## Forbidden Outputs

Pro must not:

- write a paper;
- claim public-ready, paper-ready, submission-ready, or NMI-ready status;
- upgrade Mode B beyond `insufficient_artifact`;
- claim MaoField empirical-positive results;
- claim observed residual, interaction, transport, holonomy, gluing, or collapse
  fields;
- claim black-box mechanism solved;
- claim dynamic-collapse theory;
- claim broad ANOVA, dependent-input, projection, sheaf, contextuality, or
  path-closure theory;
- treat RAG, JSON, harness, prompt, handoff, package, or model output as proof.
