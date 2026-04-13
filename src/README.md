# Source Code

This directory hosts the MaoField implementation.

## Structure

```
src/
├── rust_core/              # Performance-critical PDE evolution + retrieval engine
│   ├── Cargo.toml
│   ├── src/
│   │   ├── lib.rs
│   │   ├── allen_cahn.rs           # Allen-Cahn bistable dynamics
│   │   ├── ginzburg_landau.rs      # Complex GL field evolution
│   │   ├── coupling.rs             # Kuramoto-style coupling (Block II)
│   │   ├── multiwell.rs            # Multi-well potentials (Block V, planned)
│   │   └── reranking.rs            # Top-K reranking with energy-difference scoring
│   └── tests/
├── python_scripts/         # Analysis, visualization, baseline comparisons
│   ├── beir_evaluation.py          # BEIR benchmark harness
│   ├── bge_baseline.py             # BGE cross-encoder reference
│   ├── attractor_analysis.py       # k* via k-means + silhouette + TDA (planned)
│   ├── phase_diagnostics.py        # |R| and χ² uniformity tests
│   └── visualize.py                # Figure generation
└── README.md
```

## Design principles

**Rust core for physics**:
- PDE evolution is the hot path; SIMD and parallelism matter
- All variants share a common interface for reproducibility
- No Python in the inner loop

**Python for analysis**:
- Scientific computing ergonomics (numpy, scipy, scikit-learn)
- BEIR integration (rank_bm25, sentence-transformers)
- Figure generation (matplotlib, seaborn)

**Strict separation**: physics (Rust) produces raw field states → Python consumes for analysis. Intermediate artifacts are serialized to .npz / .bin with documented schemas.

## Dependencies

See `rust_core/Cargo.toml` and `python_scripts/requirements.txt`.

Key runtime: Rust 1.70+, Python 3.10+, scientific Python stack.

## Status

Code cleanup and documentation in progress for v0.1.0 release. Core exp016/017
experiments are reproducible via `experiments/*/src/`; public-facing library
crate is being factored from those.
