# Scripts

Reproduction and utility scripts for MaoField experiments.

## Planned scripts (v0.1.0)

| Script | Purpose |
|---|---|
| `setup.sh` | One-time setup: install Rust crates, Python deps, download BEIR datasets, build BGE embeddings cache |
| `reproduce_exp016.sh` | Full reproduction of exp016 (fusion × candidate-pool diagnostic) |
| `reproduce_exp017.sh` | Full reproduction of exp017 (four-block dialectical comparison + Stage C/A1) |
| `verify_results.sh` | Sanity check: run a small experiment subset, compare to expected results |
| `clean.sh` | Clean cache and temporary files |

## Design

Scripts are written for **POSIX shell** (compatible with Linux, macOS, WSL, Git Bash on Windows).

Each reproduction script:
1. Validates environment (Rust version, Python version, deps)
2. Reports estimated time and disk usage
3. Asks for confirmation before destructive operations
4. Logs all output to `logs/<timestamp>_<exp>.log`
5. Exits with clear success / failure status
6. Prints final result summary

## Hardware expectations

- **exp016 / exp017**: CPU only, ~3-15 hours wall time depending on dataset count
- **exp018+** (planned): may benefit from GPU for embedding computation

## Status

Scripts are being finalized for v0.1.0 release. Core experiment binaries
(`rust_core/target/release/...`) work standalone but the wrapper shell
scripts add reproducibility verification and logging.
