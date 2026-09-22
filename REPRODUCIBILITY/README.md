# Reproducibility: mathematical results and recorded continuation

All default commands are offline. They create new output directories, run no model, and do not execute archived shell scripts.

## Private master

```bash
python REPRODUCIBILITY/reproduce.py --out WORK/reproduction
python REPRODUCIBILITY/experiment/assemble_lean.py --out WORK/lean_project
python REPRODUCIBILITY/experiment/replay_lean.py --probe --prepared-project WORK/lean_project --out WORK/lean_probe
```

The first command verifies the 859 unmodified raw payloads in `INTERNAL/RAW_HCLOSE`, re-parses six streams and five compiler/candidate records, and runs the mathematical checks and the separate successor-record audit. Record reanalysis is not new sampling or kernel certification. Assembly mechanically merges the preserved workspace and public modules; it does not reconstruct an ideal candidate.

## Source-mapped reviewer copy

Unpack `MAOFIELD_REVIEW_SUPPORT.zip` to its own directory and run the same entry commands there. The reviewer record audit reads 553 mapped files with visible-only SSE, unchanged mathematical content and five unchanged candidates. Private hidden reasoning, host paths and unrelated correspondence are not copied. The full original remains in the private master; `PROVENANCE_MAP.json` identifies transformations.

## Mathematical proofs and limits

See `math/README.md`: minimax SI 2.3 (setup 2.2), state-aware repair SI 2.5, full residual counterexample SI 2.6. Symbolic checks support the displayed identities; the written proofs supply quantifiers and analysis. There is no complete-NS or population-effect claim.

## Lean assembly and replay

`experiment/LEAN_ASSEMBLY.md` lists the exact modified source slice, `Checkpoint/NodeGoal.lean`, toolchain source/hash, all locked dependencies, image requirements and isolated replay commands. Only explicit `--execute` invokes Docker/Lean. No host execution fallback or automatic model endpoint exists. STANDARD request 1 has no visible candidate and is not compiled; `standard_1.lean` is request 2 and `standard_2.lean` is request 3.

## Current execution status

Mathematical checks, full original-record reanalysis, mapped-record audit and source assembly have been run for this revision. Saved-candidate Lean compilation and independent-kernel checking have not been run: Lean/Lake/Docker and the exact built dependency environment are unavailable here. No new model sampling, agents, submission or publication took place. `REPRO_STATUS.json` and QA logs state the observed boundary.

## Actual successor records

```bash
python REPRODUCIBILITY/successor/audit_successor.py --inputs REPRODUCIBILITY/successor/inputs --out WORK/successor
```

This rereads 52 actual stages and 104 complete-request records, checks all 18,720 terminal arithmetic rows and 40 predecessor-state links, reconstructs the original complete-denominator contrasts, and independently evaluates nine illustrative programme/coordinate uses. Only the stored visible content and source-mapped mathematical records enter the reviewer copy. The unmodified compressed archive is retained privately. The two highlighted traces were selected after observing the data; they do not change the denominator or imply a stable treatment effect.
