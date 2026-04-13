# Experiments

This directory hosts all experimental campaigns underlying MaoField v0.1.0 and future versions.

## Structure

```
experiments/
├── exp016_diagnostic/          # Source-field capacity + fusion diagnostic
│   ├── README.md
│   ├── results/                # CSVs, figures, summary
│   └── src/                    # Reproduction scripts
├── exp017_dialectics/          # Four-block dialectical comparison + attractor analysis
│   ├── README.md
│   ├── results/
│   │   ├── FINAL_REPORT.md     # Complete archival report
│   │   ├── block4_matrix.csv
│   │   ├── dim4_attractor_k.csv
│   │   └── ...
│   └── src/
├── exp018_symmetry_design/     # (planned) Block V: symmetry group design
└── README.md                   # this file
```

## Experiment catalogue

| ID | Scope | Core finding | Status |
|---|---|---|---|
| exp011b | 4-candidate adversarial reranking | Complex-field GL achieves 90% on small pools | archived |
| exp016 | Fusion × candidate-pool diagnostic | Fusion step degrades signal; k*=2 first observed | archived |
| exp017 | Four-block dialectical comparison + Stage C/A1 | k*=2 via two distinct symmetry regimes; multi-well alone insufficient | archived (v0.1.0) |
| exp018 | Block V: symmetry group design | *planned for v0.2.0* | planned |
| exp019 | Non-equilibrium dynamics (OP2) | *planned* | planned |
| exp020 | Multi-step adjoint iteration (A-jump) | *planned* | planned |

## Reproducibility

Each experiment directory contains:
- `results/` — all output artifacts (CSVs, PNGs, logs, reports)
- `src/` — reproduction code (Rust + Python)
- `README.md` — experiment-specific documentation

All randomness is seeded. Hardware: EPYC 7B13 CPU (no GPU required for exp016–017).

## Data retention

Per-query output files (`IV-*_out.json`, etc.) are excluded from git due to size
but are fully regeneratable from the reproduction scripts. See `.gitignore`
at repository root.
