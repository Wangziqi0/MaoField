# MaoField Math-Turn Zero-GPU Audit Verdict

- Generated: `2026-06-22 node36; rerun script for exact wall time`
- Input: `/media/amd/raid1/canonical/projects/MaoField/experiments/exp020_metric_stress_test/highorder_ppl_20260618/highorder_result.json`
- Verdict: **insufficient_artifact**

## Boundary

This audit consumes the existing aggregate `highorder_result.json` only.
It does not create new bins, load checkpoints, or prove the proposed
mean-null vector KL field.

## LOSO Delta

| metric | CV-R2 poly5(mean_lp) | CV-R2 + gen | delta | perm p | weak gate |
|---|---:|---:|---:|---:|---|
| F1_var | 0.9736 | 0.9959 | +0.0223 | 0.0005 | pass |
| F1_tail | 0.9824 | 0.9952 | +0.0128 | 0.0005 | fail |
| F3_slice_gap | 0.8964 | 0.9476 | +0.0513 | 0.0005 | pass |

## Matched-Mean Gate

| metric | tol | pairs | frac sign(delta F)=sign(delta gen) | z | stable gate |
|---|---:|---:|---:|---:|---|
| F1_var | 0.02 | 27 | 0.593 | +0.96 | fail |
| F1_var | 0.04 | 62 | 0.500 | +0.00 | fail |
| F1_tail | 0.02 | 27 | 0.593 | +0.96 | fail |
| F1_tail | 0.04 | 62 | 0.548 | +0.76 | fail |
| F3_slice_gap | 0.02 | 27 | 0.444 | -0.58 | fail |
| F3_slice_gap | 0.04 | 62 | 0.581 | +1.27 | fail |

## Rank/Residual Gate

- Status: `diagnostic_only_two_slice_aggregate`
- Available slices: `F3_slice_rare, F3_slice_freq`
- sigma2/sigma1: `3.27404e-17`
- Gate: `fail`
- Reason: The current highorder_result.json has only rare/freq aggregate slice means. This cannot certify the proposed fixed J>=4 mean-null vector field.

## Final

- Allowed claim: Current aggregate high-order artifact supports at most a weak F3 lead. It does not authorize training a new vector-field loss.
- Next step: If PI approves, build a raw-logprob/checkpoint mode with fixed pre-registered slices and write a new primary JSON before any training implementation.

Blocked claims:
- LOSO passed as primary artifact
- mean-null vector field survives
- glass box broken
- F3 is a positive finding
