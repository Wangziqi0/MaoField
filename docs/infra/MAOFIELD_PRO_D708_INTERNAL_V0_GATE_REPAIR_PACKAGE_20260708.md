# MaoField Pro Package - D708 Internal V0 Gate Repair

- Date verified: `2026-07-08 11:45 CST` on node36
- Package source scratch:
  `/home/amd/codex-node36/tmp/package_20260708_1130_d708_repair/`
- Durable package output:
  `docs/infra/package_outputs/d708_internal_v0_gate_repair_20260708_1130/`

## Purpose

Prepare a repair/recheck package after Main Pro report39 returned:

```text
REQUEST_NODE36_FILES
```

Report39 did not reject the mathematical body. It found that the previous D708
package was not provenance-closed: loop status files, D708 records, and rule
file mappings were omitted from the zip.

This package closes those package/provenance gaps and asks Pro to recheck the
same internal v0 finite chart/path/cycle defect note.

## Main Prompt

```text
docs/infra/gpt_deep_research/GPT55_PRO_D708_INTERNAL_V0_GATE_REPAIR_RECHECK_PROMPT_20260708.md
```

Packaged convenience copy:

```text
START_HERE_D708_REPAIR_RECHECK_PROMPT_20260708_1130.md
```

## Final Node19 Desktop Files

```text
MaoField_PRO_D708_InternalV0GateRepair_20260708_1130.zip
START_HERE_D708_REPAIR_RECHECK_PROMPT_20260708_1130.md
SHA256SUMS_20260708_1130_d708_repair.txt
```

## SHA256

```text
b3206ecf59b636d2eb17ba3a510ea1b348fa518a60668d714d87c455d1729b52  MaoField_PRO_D708_InternalV0GateRepair_20260708_1130.zip
7b29b8eef5770ca05a7a83e47542cbd72349cd218db4c3db26f8db3d5253ac78  START_HERE_D708_REPAIR_RECHECK_PROMPT_20260708_1130.md
```

## Package Size And Manifest

```text
zip size: 234112 bytes
prompt size: 6467 bytes
manifest entries: 67 payload/control entries
zip total entries: 84 files/directories
unzip -t: PASS
```

## Report39 Blockers Addressed

The repair package includes the three loop status files:

```text
docs/infra/recovery/d707_split_loop_outputs/loop0/LOOP_STATUS_LOOP0_20260707.md
docs/infra/recovery/d707_split_loop_outputs/loop3/LOOP_STATUS_LOOP3_20260707.md
docs/infra/recovery/d707_split_loop_outputs/loop4/LOOP_STATUS_LOOP4_20260707.md
```

Their canonical hashes are:

```text
d3993191822d430b25832d7c9c82ee9b0bff182efa004bbca18ba873d5abc038  docs/infra/recovery/d707_split_loop_outputs/loop0/LOOP_STATUS_LOOP0_20260707.md
d73d2a317ae96572fcd622dcd9e7e58d519238997dbb2877b3e4063ea50bda43  docs/infra/recovery/d707_split_loop_outputs/loop3/LOOP_STATUS_LOOP3_20260707.md
07a623ffb333e639b8a0ce6a8aa45632ac759daea0234633cd2afab329dd15bb  docs/infra/recovery/d707_split_loop_outputs/loop4/LOOP_STATUS_LOOP4_20260707.md
```

The repair package also includes:

- `docs/infra/MAOFIELD_PRO_D708_INTERNAL_V0_PROMOTION_GATE_PACKAGE_20260708.md`
- `docs/infra/MAOFIELD_PRO_D708_INTERNAL_V0_PROMOTION_GATE_NODE19_DELIVERY_20260708.md`
- `docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_D708_INTERNAL_V0_GATE_PACKAGE_20260708.md`
- `PACKAGE_PROVENANCE_D708_REPAIR_20260708.md`
- `rules/PROJECT_AGENTS.md`
- `rules/CANONICAL_AGENTS.md`
- `rules/CLAUDE.md`
- report39 archive and adoption note.

## Self-Reference Note

The package includes `PACKAGE_PROVENANCE_D708_REPAIR_20260708.md`, which tells
Pro not to fail the repair package merely because `STATE.md` does not contain
the final SHA256 of the repair zip. A zip cannot contain a file that already
knows the final hash of the zip containing it.

Use the external `SHA256SUMS_20260708_1130_d708_repair.txt`, internal payload
checksums, and node19 delivery readback for package integrity.

## Boundary

This package is for internal v0 promotion-gate repair/recheck only.

Still forbidden:

- public-ready, paper-ready, submission-ready, or NMI-ready claims;
- MaoField empirical-positive claims;
- observed residual, interaction, transport, holonomy, gluing, or collapse field;
- black-box mechanism solved;
- dynamic-collapse theory;
- broad ANOVA, dependent-input, projection, sheaf, contextuality, or path-closure
  theory;
- proof-by-RAG, proof-by-JSON, proof-by-harness, proof-by-prompt,
  proof-by-package, or proof-by-handoff.

Mode B remains `insufficient_artifact`. Duplicate risk remains `MEDIUM`.
