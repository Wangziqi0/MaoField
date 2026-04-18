# Block IV.5 Stage C: Phase Distribution Diagnostic

## Question
Is k*=2 from a hidden phase-locking mechanism (Z_2 via phase antipodes)?

## Method
Analyze phase φ = atan2(b,a) for IV-A (byte) and IV-B (BGE) final states.

## Metrics
- `|R|`: circular mean resultant length (0=uniform, 1=locked)
- `χ²/n_bins`: goodness-of-fit against uniform
- k=2 centers on (cos,sin) of per-doc mean phase: ~180° apart = Z_2 phase lock

## Numbers

| group | global |R| | χ²/72 | per-doc |R| mean | kmeans-2 center dist |
|---|---|---|---|---|
| IV-A (byte) | 0.8073 | 94989.68 | 0.8403 | 26.2° |
| IV-B (BGE)  | 0.1651 | 4879.91 | 0.1974 | 81.4° |

## Verdict

- IV-A: ambiguous (|R|=0.840, antipodal=26°). Need deeper test.
- IV-B: per-doc phase is NEARLY UNIFORM. k*=2 is NOT from phase locking.

## Next Step

Proceed to **Stage A**: add external field `+h·Re(ψ)` to Allen-Cahn, test if Z_2 breaks and k* changes.
