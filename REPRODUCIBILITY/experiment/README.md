# Recorded experiment and saved-candidate reproduction

One selected local `hclose` task, two bounded attempt sequences, six requests and five visible candidates. The recorded labels HISTORY and STANDARD are provenance labels; no historical retrieval/compaction intervention is claimed. H3 was historically accepted; S1 was truncated without a body; S2 and S3 produced the two standard candidates.

The private master stores all originals under `INTERNAL/RAW_HCLOSE`. Its full audit uses `audit_hclose.py`. The reviewer archive stores source-mapped copies under this directory's `raw/`; its `audit_shareable.py` independently reads visible stream chunks, usage, request messages, candidate insertions and saved compiler records. Read `SHAREABLE_MANIFEST.json` for each transformation; neither script interprets absence of private reasoning as absence of historical thinking.

`candidate_manifest.json` contains both visible-candidate ordinal and original request number. These are not interchangeable. `request_to_candidate.json` lists all six requests including the no-candidate request. Candidate file bytes are never corrected to improve a result.

Run `assemble_lean.py --out WORK/lean_project` from the archive root, followed by the probe or explicit isolated replay in `LEAN_ASSEMBLY.md`. Exact source identifiers, toolchain/archive hash and dependency locks come from retained provenance, not from a claim that remote binaries were reacquired here. Independent-kernel certification remains a separate unexecuted layer.

The historical generation protocol is documentation only. No default command connects to the former service or runs a new model. Weights/service availability and future repeat sampling require separate authorisation and an actually available model. Matching seeds alone do not promise identical output bytes.
