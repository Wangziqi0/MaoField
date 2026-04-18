# Block IV.5 Stage A1: Multi-well Amplitude Potential

## Config
DT=0.05000000074505806  steps=5000  clamp=3.0  n_docs=70

Potential: `A1_multiwell: V=|psi|^2*(|psi|^2-1)^2*(|psi|^2-4)^2`

Init: `init_u_nonzero: |psi|=1.0+-0.3`

## Stability
- u_max (field) = 1.199224591255188
- u_mean (field) = 1.008676528930664
- n_nan = 0

## Amplitude distribution
- |psi| range: [0.0147, 1.0951]  mean 1.0005
- u=|psi|^2 range: [0.0002, 1.1992]  mean 1.0087
- peaks (pos,height): [(np.float64(1.012499988079071), 563386.5558024341)]
- well occupancy fraction [u=0, u=1, u=4]: [0.0085, 0.9915, 0.0]

## Phase diagnostic
| metric | value |
|---|---|
| global \|R\| | 0.1586 |
| chi2 / 72 | 3773.71 |
| per-doc \|R\| mean | 0.1851 +- 0.0865 |
| kmeans-2 antipodal | 57.9 deg |

## k-means k=2..5

| repr | k | silhouette | inertia |
|---|---|---|---|
| raw_ab | 2 | 0.0544 | 1.325e+06 |
| raw_ab | 3 | 0.0403 | 1.280e+06 |
| raw_ab | 4 | 0.0510 | 1.220e+06 |
| raw_ab | 5 | 0.0387 | 1.182e+06 |
| amplitude | 2 | 0.1502 | 1.682e+04 |
| amplitude | 3 | 0.0489 | 1.651e+04 |
| amplitude | 4 | 0.0723 | 1.622e+04 |
| amplitude | 5 | 0.0713 | 1.584e+04 |
| phase_cos_sin | 2 | 0.0551 | 1.310e+06 |
| phase_cos_sin | 3 | 0.0407 | 1.264e+06 |
| phase_cos_sin | 4 | 0.0515 | 1.204e+06 |
| phase_cos_sin | 5 | 0.0392 | 1.167e+06 |

### Best k* per representation

- raw_ab: k*=2  silhouette=0.0544
- amplitude: k*=2  silhouette=0.1502
- phase_cos_sin: k*=2  silhouette=0.0551

## Data rules (no philosophy)
- k*>=3 AND |R| < 0.3 -> multi-well clusters resolved by kmeans, phase stays uniform
- k*=2 AND |R| < 0.3 -> multi-well may exist in amplitude space but kmeans doesn't split; need manifold-aware eval
- |R| >= 0.3 -> phase uniformity broken by multi-well (counter-example)
