# Paper Claim Audit Report

**Date:** 23 September 2026  
**Paper:** *Why can equal results lead to different scientific futures*  
**Audit route:** fresh zero-context Codex review; same-family; provisional  
**Overall verdict:** **WARN**

The current scientific numbers reconcile. I found no inflated result, wrong denominator, arithmetic error, cherry-picked value presented as an average, caption/value discrepancy, or comparison assembled from incompatible configurations. The warning is caused by two stale figure-provenance files and by several historical-only SI statements whose exact counts cannot be traced to admissible primary records in the supplied evidence set.

## Claim accounting

Fifty consolidated claim groups cover the distinct quantitative and empirical assertions in the manuscript and Supplementary Information. Repeated statements of the same result were consolidated but every location is recorded in [CLAIM_EVIDENCE_TABLE.csv](/data/MaoField/coordination/20260923_presubmission_final_audit/claims/CLAIM_EVIDENCE_TABLE.csv).

| Status | Count |
|---|---:|
| exact_match | 34 |
| rounding_ok | 8 |
| ambiguous_mapping | 1 |
| missing_evidence | 5 |
| config_mismatch | 2 |
| number_mismatch | 0 |
| scope_overclaim | 0 |

Bibliographic metadata and citation numbering were left to the separate citation audit. Equation, figure, table and note numbers were treated as structural labels. Earlier audits, narrative reports, experiment trackers, STATE/STATUS and executor summaries were not accepted as claim evidence.

## Actionable findings

### 1. Figure provenance hashes and stems are stale

[FIGURE_INPUT_IDENTITIES.csv](/home/amd/下载/MAOFIELD_NATURE_RESTORED_V8_R2_20260923/SOURCE_DATA/FIGURE_INPUT_IDENTITIES.csv) still names the former stems `figure1_practice_cycle`, `figure2_finite_separation`, `figure3_hclose_application` and `figure4_recorded_attempts`. The current build emits `figure1_core_non_sufficiency`, `figure2_minimax_and_domain`, `figure3_successor_continuation` and `figure4_hclose_application`.

The same CSV records:

- manuscript SHA-256 `31e935dd…`, while the audited R2 manuscript is `1284d72b97dada6188e7e205c64e6f1b0dd9cd9351a007356c996b696f899d09`;
- SI SHA-256 `2ec02544…`, while the audited R2 SI is `7b0cfd72c8148c5430606c98f8a98815abfa6d56b4a8f82663d73e220860471a`.

Regenerate this identity table from the current R2 build and submission sources.

### 2. A second figure-source table retains the prior Fig. 3/Fig. 4 numbering

[source_data_figures.csv](/home/amd/下载/MAOFIELD_NATURE_RESTORED_V8_R2_20260923/SOURCE_DATA/source_data_figures.csv) maps six proof requests to Figure 3 and final tactics/compiler mismatch to Figure 4. In the current paper, Figure 3 is successor continuation and Figure 4 is the `hclose` application. [FIGURE_SOURCE_MAP.csv](/home/amd/下载/MAOFIELD_NATURE_RESTORED_V8_R2_20260923/SOURCE_DATA/FIGURE_SOURCE_MAP.csv) has the current mapping.

Replace the stale file with the current mapping or remove the redundant table. This is a provenance defect; the actual Figure 3 and Figure 4 values and captions are correct.

### 3. Four older-history rows lack admissible primary records

Supplementary Table 5 gives exact counts for A′ V1 (`4` lineages, `48` stages), A″ (`9` submitted, `1` no-submission stop, `1` interruption, `21` unrun), E1/E3 (`8` stages, `56` coordinates, `4` discrepant E3 accounts), and an earlier finite-scalar/R4 comparison. No immutable raw episode ledger or result export for those studies is present in the declared evidence roots. The available support is confined to excluded historical summaries or state records.

These values are not contradicted, but this audit cannot independently verify them. Add the relevant raw ledgers/results or qualify the rows as historical-report statements without reproducing exact counts. The later pre-`hclose` workflow counts in Supplementary Table 6 and Extended Data Table 1 do have direct raw backing and all reconcile.

### 4. The exact model name needs a primary alias mapping

The manuscript names `Qwen/Qwen3.8-27B-FP8`. The final run records contain the served identifier `qwen3.8-27b-fp8-a256k-nomtp-c1` and a local model-root basename `Qwen3.8-27B-FP8`, but not the exact namespaced string. Use the served identifier or add a primary receipt linking the served alias to the namespaced repository/model identity.

### 5. The later replay-probe reason is not in the admissible raw set

Historical compilation under Lean 4.34.0-rc2 is fully evidenced. The later statement that saved-candidate replay was not run because a compatible toolchain/container was unavailable is not backed by a raw probe receipt in the declared evidence roots. Add that receipt, or shorten the claim to “not rerun in this revision.”

## Main results verified

- The HClose package manifest has **859 entries**, and all **859/859** file hashes verify. There are **6** returned request streams, **5** compiled candidates, and **243** byte-identical workspace files outside the differing candidate module.
- Guided outcomes are rejected, rejected, accepted; declarations-only outcomes are token-limit/no body, rejected, rejected. The accepted record has return code `0` and dependencies `propext`, `Classical.choice` and `Quot.sound`.
- The six request token pairs and totals are exact. Guided totals are **25,757 input / 20,781 output**; declarations-only totals are **12,124 / 41,009**. The initial prompt difference is exactly **332** tokens.
- Runtime and sampling values match the raw run configuration: context `262,144`, input allowance `196,608`, output limit `32,768`, tensor parallelism `2`, half precision, `turboquant_k8v4`, PIECEWISE capture `[4]`, no speculative configuration, temperature `1`, top-p `0.95`, top-k `20`, presence penalty `0`, repetition penalty `1`, EOS active and medium reasoning.
- The successor export catalog has **418/418** valid exported-file hashes; with `catalog.json`, this is a **419-file** analysis input tree.
- Assistance contains **4** formation episodes from **2** archived ancestors, **20** stages and **40** complete returns. Adoption contains **8** new episodes, **32** stages and **64** returns. Totals are **52 stages / 104 returns**; all 104 recorded returns end with `stop`.
- Direct raw inspection confirms **5** empty terminal programmes, **7/8** identical adoption version pairs, **18,720** terminal rows and **40/40** exact predecessor-state links.
- Every Supplementary Table 8 contrast was independently recomputed from raw effect rows with denominators **144**, **144** and **288**. All 15 displayed values are correct to the shown precision.
- The selected P00 and P07 programmes, residual decompositions, stored round-off values, symbolic series and changed-target reuse all match the raw stage files. The Fig. 3 value `1.811136 × 10^-71` is valid rounding of `1.811135815765… × 10^-71`.
- The mathematical identities, minimax bound, counterexample and compact-repair domain check exactly. The Figure 2 curve is correctly labelled as an analytic illustration rather than an empirical sample.
- Quantitative captions for Figures 2–4 and Extended Data Fig. 1 agree with both the rendered SVGs and raw records. No caption-table number mismatch was found.

## Assurance boundary

This is a fresh same-family Codex audit, so `review_independence` is `same-family` and `acceptance_status` is `provisional`. The substantive verdict remains **WARN**: the scientific result numbers are clean, while the provenance tables and historical evidence gaps should be resolved before treating the package as fully submission-ready.

Machine-readable details, hashes and the issue list are in [PAPER_CLAIM_AUDIT.json](/data/MaoField/coordination/20260923_presubmission_final_audit/claims/PAPER_CLAIM_AUDIT.json).
