# Experiment Audit Report

**Date:** 2026-09-23  
**Project:** MaoField presubmission manuscript, proof-completion record and coefficient-successor record  
**Auditor:** GPT-5.6-Sol ultra, fresh Codex reviewer subagent (`/root/final_experiment_integrity`), read-only  
**Review route:** `review_independence: same-family`; `acceptance_status: provisional`  
**Overall verdict:** **WARN**  
**Integrity status:** **warn**

The primary scientific records support the manuscript's bounded claims. I found no fake ground truth, prediction-derived reference, self-normalised performance score, phantom result, uncalled metric, or deletion/reclassification of failed, stopped, empty, truncated or unknown records. A fresh deterministic run completed all four offline paths with zero model calls and zero Lean compilations. The warning is for two traceability defects in the presubmission package: the figure-input identity table contains stale manuscript/SI hashes and figure stems that do not agree with the figure-source map; and one historical-unknown label in the successor audit output is hard-coded rather than derived from the preserved primary receipts. The underlying historical claim is nevertheless supported by the newly supplied full coefficient archive.

Positive findings remain provisional because the fresh reviewer is from the same Codex/OpenAI model family as the executor. This audit did not rerun a model experiment, Lean, an independent kernel, or any external service.

## Evidence path aliases

Every line citation below uses one of these exact absolute paths:

- `M` = `/home/amd/下载/MAOFIELD_NATURE_RESTORED_V8_R2_20260923/SUBMISSION/manuscript.md`
- `SI` = `/home/amd/下载/MAOFIELD_NATURE_RESTORED_V8_R2_20260923/SUBMISSION/supplementary_information.md`
- `RR` = `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/REPRODUCIBILITY/reproduce.py`
- `AH` = `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/REPRODUCIBILITY/experiment/audit_hclose.py`
- `AS` = `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/REPRODUCIBILITY/successor/audit_successor.py`
- `DT` = `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/INTERNAL/RAW_HCLOSE/20_TASK_AND_RUNNER/direct_task.py`
- `RD` = `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/INTERNAL/RAW_HCLOSE/20_TASK_AND_RUNNER/run_direct.py`
- `PT` = `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/INTERNAL/RAW_HCLOSE/20_TASK_AND_RUNNER/PROOF_TEMPLATE.lean.txt`
- `PL` = `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/INTERNAL/RAW_HCLOSE/10_CURRENT_RUN/PLAN.json`
- `HR` = `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/INTERNAL/RAW_HCLOSE/10_CURRENT_RUN/history/submissions/20260920T114931908693/RESULT.json`
- `HS` = `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/INTERNAL/RAW_HCLOSE/10_CURRENT_RUN/history/submissions/20260920T114931908693/compile/stdout.bin`
- `SR` = `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/INTERNAL/RAW_HCLOSE/10_CURRENT_RUN/standard/requests/0000/receipt.json`
- `SF` = `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/INTERNAL/RAW_HCLOSE/10_CURRENT_RUN/standard/submissions/20260920T121411892800/compile/stdout.bin`
- `AT` = `/home/amd/下载/MAOFIELD_NATURE_RESTORED_V8_R2_20260923/SOURCE_DATA/attempts.csv`
- `MC` = `/home/amd/下载/MAOFIELD_NATURE_RESTORED_V8_R2_20260923/SOURCE_DATA/successor/main_contrasts.csv`
- `CS` = `/home/amd/下载/MAOFIELD_NATURE_RESTORED_V8_R2_20260923/SOURCE_DATA/successor/cohort_status.json`
- `VI` = `/home/amd/下载/MAOFIELD_NATURE_RESTORED_V8_R2_20260923/SOURCE_DATA/successor/version_identity.json`
- `FI` = `/home/amd/下载/MAOFIELD_NATURE_RESTORED_V8_R2_20260923/SOURCE_DATA/FIGURE_INPUT_IDENTITIES.csv`
- `FM` = `/home/amd/下载/MAOFIELD_NATURE_RESTORED_V8_R2_20260923/SOURCE_DATA/FIGURE_SOURCE_MAP.csv`
- `CAT` = `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/REPRODUCIBILITY/successor/inputs/catalog.json`
- `ZA` = `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/ZENODO_CANDIDATES/03_FULL_SCIENTIFIC_RECORDS/SUCCESSOR/_ARCHIVE_README.md`
- `ZM` = `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/ZENODO_CANDIDATES/03_FULL_SCIENTIFIC_RECORDS/SUCCESSOR/_ARCHIVE_MEMBER_MANIFEST.json`
- `ZP` = `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/ZENODO_CANDIDATES/03_FULL_SCIENTIFIC_RECORDS/FILE_PROVENANCE.json`
- `ZU` = `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/ZENODO_CANDIDATES/03_FULL_SCIENTIFIC_RECORDS/SUCCESSOR/rounds/20260918_ns_r6_ab_execution/supplement_a_r3/analysis_view/science_A/pre_supplement_failure/P01_s1_W2/STATUS.json`
- `ZT` = `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/ZENODO_CANDIDATES/03_FULL_SCIENTIFIC_RECORDS/SUCCESSOR/rounds/20260918_ns_r6_ab_execution/supplement_a_r3/analysis_view/science_A/pre_supplement_failure/P01_s1_W2/request_01/parent_timeout.json`
- `ZC` = `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/ZENODO_CANDIDATES/03_FULL_SCIENTIFIC_RECORDS/SUCCESSOR/rounds/20260918_ns_r6_ab_execution/supplement_a_r3/remote_raw/COMPLETE.json`
- `DR` = `/data/MaoField/coordination/20260923_presubmission_final_audit/experiment/deterministic_reproduction/STATUS.json`
- `DA` = `/data/MaoField/coordination/20260923_presubmission_final_audit/experiment/deterministic_reproduction/records/audit_summary.json`
- `DS` = `/data/MaoField/coordination/20260923_presubmission_final_audit/experiment/successor_raw_reanalysis/audit_result.json`

## Audited input identities

| Input | SHA-256 |
|---|---|
| Manuscript | `1284d72b97dada6188e7e205c64e6f1b0dd9cd9351a007356c996b696f899d09` |
| Supplementary Information | `7b0cfd72c8148c5430606c98f8a98815abfa6d56b4a8f82663d73e220860471a` |
| `RAW_HCLOSE/PACKAGE_MANIFEST.json` | `5569bdabed031a8667ad9ec2d13d909645707b82acf329d843c721b99cf56db0` |
| Successor source-map `catalog.json` | `aa054ae57ff3c59395001fc28c7165617fd850c82ddc956c0f14c1fc039a9cc6` |
| Full successor `_ARCHIVE_MEMBER_MANIFEST.json` | `649a2cde1f3b4c4dc0245ee571fce0e49994a88368871db035fe39ad79b343c8` |
| Full-record `FILE_PROVENANCE.json` | `02dae2586ff01dfa3c985e639c2bb1cbfe3b37ded9ee5bbbf6ac9597dad73628` |
| `REPRODUCIBILITY/reproduce.py` | `f0df1946fa1affa191734949a6d7d1e5853c56e3ed468d4d60c595653b41cdb0` |
| `experiment/audit_hclose.py` | `e4c748459befcc670eb2e25447746e5904664a6e70a401bfe81cd50c40d17506` |
| `successor/audit_successor.py` | `c51b0d1e730629b534ab4c824522d2c0d23aea8b620404565436736b934b32ac` |
| `direct_task.py` | `ad9f299ef67aab0ebf6c94438348868a085892e668f772c9b396a1ddd38463b9` |
| `run_direct.py` | `b2ac7283b3c1eaa9363f1026189ea80634205267f67e60d2d2b84b861ba24d1d` |
| Proof template | `7650a1567c10f61e29bc0f761ac715c8dff13572cd8e4a8a7486eec41ddbca9c` |
| Historical run plan | `79b8405a3dcc55a6e4d2418f2048cd99a544e3d571ef7a7d339a28e222c42524` |
| Accepted proof body | `7b0d085eb5d1dae4ce730422adfaabcf7b9844d96e3c55a6f6f33508d334d927` |
| Accepted result record | `b8c1d5e9c020af0d8554f10adbe0d8b3b6e7addc96c5bf989fce14d62a349b6c` |
| `FIGURE_INPUT_IDENTITIES.csv` | `dc3918585d91c12d689574beb4079b1eb67a87c3202a3172ae03c3cd3fe2fc7b` |
| `FIGURE_SOURCE_MAP.csv` | `46e821457abf64a6e53ba5a4802b48d13e6a6dd2a3db761a55afeb5beea89fdd` |

Directory identities use SHA-256 over sorted records of `relative_path NUL byte_count NUL file_sha256 newline`: `SOURCE_DATA/` has 23 files and tree digest `8af9f6a8e1b2ec5256cf02b180cd9c17b2c7237b792d2853b1ef6de3ec0be1c8`; `REPRODUCIBILITY/` has 444 files and tree digest `52524d2482aee61961287caed6d80b6f90fccc50637d8bcfb6ce9f33d609c21f`.

## A. Ground-truth provenance: PASS

The proof-completion endpoint is a retained formal-checker observation, not a model-generated reference. The runner rejects placeholders, builds the mechanically inserted body and accepts only a zero-return build whose printed axioms are a subset of the permitted set (`DT:45-70`). The accepted receipt records `BUILD_COMPLETED` and the permitted axiom list (`HR:2-11`, `HR:108-121`), while the complete saved output contains the exact enclosing type, printed dependencies and successful build line (`HS:1-46`). The source-only final body has a real type mismatch (`SF:1-10`), so rejected and accepted candidates are distinguished by compiler evidence.

For the successor study, the evaluation is simulation-only: targets, states and generated programmes are retained workbench records, and residuals are recomputed arithmetically rather than compared against a model-produced pseudo-reference (`AS:44-90`). The source-map lists the original archive and explicit privacy transformations (`CAT:2512-2520`). A fresh export from the newly supplied full archive reproduced all 419 supplied source-mapped files byte-for-byte. The full archive manifest declares 5,582 payloads (`ZM:1-6`), and this audit independently verified closure, byte counts and all hashes. Relevant full-record provenance rows are byte-identical, including the historical unknown status (`ZP:109030-109040`) and supplement completion receipt (`ZP:124188-124198`).

The historical unknown and later supplement are preserved as distinct events. The original stage is `HALTED_UNRESOLVED` (`ZU:1-4`) after a no-replay parent timeout (`ZT:1-5`); the archive explicitly states that the later acquisition is new and does not resolve the old unknown (`ZA:5-8`); and the supplement receipt records 41 cumulative sends, 40 completes, one original unknown and `old_unknown_resolved: false` (`ZC:1-17`).

## B. Score normalisation: PASS

No reported performance score is divided by the model's own maximum, minimum, mean or output statistic. The proof endpoint is raw compile acceptance plus axiom readout. The successor contrasts are unnormalised treatment-minus-control differences of absolute residuals, averaged over fixed complete denominators (`AS:95-109`; `MC:1-16`). The only normalised quantity in the successor code is a numerical reconstruction tolerance, `abs(recomputed-stored)/(1+abs(recomputed))`, used to assert byte-carried arithmetic consistency (`AS:68-73`, `AS:119-126`); it is not a performance score and is not used in the manuscript's contrasts. The SI explicitly reports negative, positive and zero contrasts and explains the outer-region domination rather than rescaling it away (`SI:577-596`).

## C. Result existence and number matching: WARN

The scientific result files exist and their numbers match. Fresh reanalysis recovered six complete proof streams, five compiled candidates, one accepted guided attempt, the exact arm token totals and all 859 manifested HClose payload identities (`DA:2-42`; `AT:2-7`). The accepted body hash matches the historical result; the first declarations-only request records `finish_reason=length`, 32,768 completion tokens and an empty visible-body hash (`SR:2-19`). Fresh raw-archive reanalysis recovered 52 stages, 104 complete requests, 18,720 effects, 40 parent-state links, nine selected coordinates and seven unchanged adoption versions (`DS:2-12`), consistent with `CS:1-20`, `MC:1-16` and `VI:1-98`. These match the manuscript's bounded descriptions (`M:87-97`, `M:120-126`, `M:215-225`) and the SI's exact request and successor counts (`SI:214-225`, `SI:563-589`).

The warning is a figure-provenance drift, not a mismatch in the scientific numbers:

1. `FI:2` and `FI:6` record manuscript hash `31e935dd...`, but the audited final manuscript hash is `1284d72b...`. `FI:5` records SI hash `2ec02544...`, but the audited final SI hash is `7b0cfd72...`.
2. The identity table labels proof-completion inputs as `figure3_hclose_application` and successor inputs as `figure4_recorded_attempts` (`FI:6-10`), whereas the source map assigns successor evidence to Figure 3 and HClose evidence to Figure 4, with different stems (`FM:4-5`). Figure 1 and 2 stems also differ between the two ledgers (`FI:2-5`; `FM:2-3`).

This breaks exact figure-to-input traceability after the final manuscript/SI revision. It does not alter the independently matched result values.

## D. Dead code and executed-path tracing: PASS

All metric/check functions on the executed default path are called. The top-level reproduction route invokes exact algebra, HClose record checking, HClose algebra and successor checking (`RR:6-15`). The HClose audit verifies package closure, SSE reconstruction, request/visible-body identity, candidate insertion, compiler outcomes, prompt equality and shared workspaces (`AH:42-145`). The successor audit verifies catalog hashes, terminal programmes, all residual rows, parent-state inheritance, fixed-denominator contrasts, selected programme evaluation and symbolic expansions (`AS:44-149`). Static call tracing found no uncalled metric function in these executed scripts. Assembly and replay are explicit optional routes rather than hidden contributors, and the SI records replay and independent-kernel checking as not run (`SI:541-554`).

One traceability weakness remains outside the dead-code criterion: `A_historical_unknown_request` is inserted as a literal string in the audit result (`AS:143-149`) rather than checked from the primary unknown and supplement receipts. This audit checked those receipts directly and found the statement correct, but the machine audit should derive or validate it.

The historical runner also preserves failure paths: it records a returned length-limit body without compiling it, writes every compiler feedback object and appends every submission status (`RD:101-129`); its final readout includes both arms, token totals and unknown-request counts (`RD:135-147`).

## E. Scope assessment: PASS

The evidence is narrow and the prose says so. HClose is one post-selected local obligation, one seed block, two conditions and up to three requests each; the plan records those limits and the post-selection boundary (`PL:19-22`, `PL:59-64`). The manuscript calls the six requests and five candidates one bounded comparison, rejects success-rate and causal-efficiency inference, and names unequal information, feedback and realised computation (`M:120-126`, `M:215-217`).

The successor record comprises four assistance formation histories and eight adoption histories, with repeated coordinates rather than independent participants. The SI keeps all fixed denominators, empty finals, unchanged versions, mixed signs and extreme outer-region effects, and explicitly denies a stable average benefit (`SI:565-596`). Post-selected traces are labelled explanatory rather than confirmatory (`SI:598-623`). I found no empirical use of “comprehensive”, “extensive” or “robust” that exceeds this scope.

## F. Evaluation types: PASS

- **HClose proof completion:** `real_gt` as a formal-checker analogue. Ground truth is the retained Lean build return code, exact type and axiom readout. Claim ceiling: saved local compilation acceptance only; no fresh or independent kernel certification (`M:201-205`).
- **Coefficient successor studies:** `simulation_only`. The coefficient workbench uses fixed simulated targets, stored programme outputs and inherited numerical state. Claim ceiling: process, arithmetic, revision and reuse within this workbench; no physical NS or general causal-performance claim (`SI:563-596`).
- **Finite separation and compact repair:** non-empirical analytic proof, outside the five empirical labels in the base checklist. Its plotted curve is a deterministic `simulation_only` illustration, while the all-quantifier claim rests on the written piecewise proof (`SI:51-73`; `M:183-187`).

## Preservation of negative and interrupted outcomes

| Outcome | Direct evidence | Audit conclusion |
|---|---|---|
| Two guided compiler rejections | `AT:2-3` | Preserved and counted |
| Guided third acceptance | `AT:4`; `HS:1-46` | Preserved with exact type/axioms |
| Declarations-only length termination with no body | `AT:5`; `SR:2-19` | Preserved as truncation, not relabelled as Lean rejection |
| Two declarations-only compiler rejections | `AT:6-7`; `SF:1-10` | Preserved and counted |
| Five empty successor terminal programmes | `CS:2-18`; `SI:589-596` | Included in original denominators and no-update semantics |
| Seven unchanged adoption versions | `VI:1-98` | Included, not filtered out |
| Historical unknown request | `ZU:1-4`; `ZT:1-5` | Preserved as unknown/no replay |
| Separately authorised supplement | `ZC:1-17` | Kept separate; does not resolve original unknown |

## Deterministic derivation of the unknown/supplement distinction

The release-candidate audit can derive this distinction from the following primary receipts, all below `/home/amd/下载/MAOFIELD_NATURE_PRESUBMISSION_V8_20260922/ZENODO_CANDIDATES/03_FULL_SCIENTIFIC_RECORDS/SUCCESSOR/rounds/20260918_ns_r6_ab_execution/supplement_a_r3/`:

1. `analysis_view/science_A/ANALYSIS_VIEW_PROVENANCE.json`: require `kind == "DERIVED_OVERLAY_NOT_AN_ORIGINAL_EXECUTION_ROOT"`, `new_acquisition_id == "PI_R3_01"`, `old_unknown_root == "pre_supplement_failure/P01_s1_W2"`, `original_unknown_resolved is false`, `replaced_terminal_request == 1`, `replacement_stage == "P01_s1_W2"`, `requests_all_acquisitions_sent == 41`, `requests_known_complete == 40`, and `requests_unknown_completion == 1` (lines 2-14).
2. `analysis_view/science_A/pre_supplement_failure/P01_s1_W2/STATUS.json`: require `reason == "UNKNOWN_COMPLETION"` and `status == "HALTED_UNRESOLVED"` (lines 1-4).
3. `analysis_view/science_A/pre_supplement_failure/P01_s1_W2/request_01/parent_timeout.json`: require `no_replay is true`, `status == "UNKNOWN_COMPLETION"`, and the retained timeout value `seconds == 1200` (lines 1-5).
4. `analysis_view/science_A/pre_supplement_failure/P01_s1_W2/RETURNED_NOT_APPLIED.json`: require `effect_applied is false`, top-level `reason == "UNKNOWN_COMPLETION"`, and preserve the late `raw_result` rather than promoting it into the original endpoint (lines 1-4 and 20-22). The late raw result may itself have `finish_reason == "stop"`; that does not rewrite the frozen no-replay outcome.
5. `remote_raw/COMPLETE.json`: require `status == "COMPLETE_ONE_PI_AUTHORIZED_SUPPLEMENT"`, `new_generation_requests == 1`, `original_unknown_requests == 1`, `old_unknown_resolved is false`, `supplement_supplies_missing_terminal_for_separate_analysis is true`, `cumulative_A_sent == 41`, `cumulative_A_complete == 40`, `original_attempt == 1`, and `stage == "P01_s1_W2"` (lines 1-17).
6. `remote_raw/stages/P01_s1_W2/STATUS.json`: require `acquisition == "PI_AUTHORIZED_R3_SUPPLEMENT"`, `capture == "CAPTURED_NOT_MATH_CERTIFIED"`, and `status == "FINITE_STAGE_ENDED"` (lines 1-5).
7. Bind the supplement to the original request without treating it as the original return: SHA-256 of both `analysis_view/science_A/pre_supplement_failure/P01_s1_W2/request_01/request.json` and `remote_raw/request_01/request.json` is `31a4224b06fb4fdb7624c077daa473718c2378a6124578ada7781edd6551f55a`; the files are byte-identical, and this value equals `remote_raw/COMPLETE.json.payload_sha256` (line 14). The corresponding tokenizer request files are also byte-identical with SHA-256 `7f48213fbd3b05882074c8432ceabc4bab841ab12d7f60746cfa79f1b29724c3`.
8. `PI_SUPPLEMENT_AUTHORITY.txt` is the human-authority receipt. Its third line limits authority to one new call, requires preservation of the original timeout uncertainty, prohibits replay of other requests, and states that the original unknown usage remains unknown.

A derived machine result is valid only if all predicates above hold. The appropriate output is: original request `UNKNOWN_COMPLETION/HALTED_UNRESOLVED`, `effect_applied=false`, `no_replay=true`; supplement `COMPLETE_ONE_PI_AUTHORIZED_SUPPLEMENT`, separately captured, with `old_unknown_resolved=false`. Do not infer the distinction solely from the literal string currently emitted at `AS:148`.

## Action items

1. Regenerate `SOURCE_DATA/FIGURE_INPUT_IDENTITIES.csv` after freezing the final manuscript and SI so its recorded hashes equal `1284d72b...` and `7b0cfd72...`.
2. Reconcile `figure_file_stem` values in `FIGURE_INPUT_IDENTITIES.csv` and `FIGURE_SOURCE_MAP.csv` with the actual final figure assets. In particular, successor evidence should map to Figure 3 and HClose evidence to Figure 4.
3. Change `audit_successor.py` so the historical-unknown/supplement distinction is verified from the preserved `STATUS.json`, `parent_timeout.json`, request identity and supplement `COMPLETE.json`, rather than emitted as a literal statement. The present claim is supported; this change makes that support reproducible through the default audit path.

## Claim impact

- **Saved HClose local acceptance:** supported within the stated historical saved-compilation scope.
- **Six requests, five candidates, exact token counts and failure sequence:** supported.
- **52 stages, 104 completed successor returns, 18,720 rows, 40 inheritance links, five empty finals and seven unchanged adoption versions:** supported for the simulation/workbench record.
- **Selected residual decompositions, symbolic orders and complete-denominator contrasts:** supported as deterministic reanalysis of preserved records.
- **Stable average assistance/adoption benefit or a general history effect:** unsupported by design and correctly disclaimed.
- **Fresh Lean replay, independent kernel certification, full Navier–Stokes proof or physical validation:** not established and correctly not claimed.
- **Exact final figure-input provenance:** needs correction before the package is treated as internally frozen.

## Fresh deterministic verification receipt

The fresh offline run completed `math`, `records`, `hclose_math` and `successor` with return code 0 and recorded zero new model calls and zero new Lean compilations (`DR:1-22`). A second run exported the source-mapped successor inputs directly from the full primary archive, reproduced all 419 supplied files byte-for-byte, and produced the same successor counts and values (`DS:1-13`). These checks establish deterministic record consistency; they do not convert the same-family review into independent acceptance or create a new experiment.
