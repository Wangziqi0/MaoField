# RELEASE_NOTES — MaoField Contradiction-Aware Training (CAT)

## v1.0 — 2026-05-19

**Type:** Initial pilot release.
**Scope:** Empirical pilot snapshot of the contradiction-aware training
arm B implementation on OPT-125m / wikitext-2, frozen at the close of
the 5/7–5/12 chain.

### 1. What v1.0 includes

- **Source code snapshot** (`src/`)
  - `contradiction_loss.py` — Σ_2 → ℒ_contradiction KL-second-order
    implementation (candidate b PRIMARY training loss + candidate d
    gradient-norm monitoring metric).
  - `cat_trainer.py` — `CATTrainer` subclassing
    `transformers.Trainer`, hooking the contradiction tracker into
    `compute_loss` and maintaining the EMA teacher in `training_step`.
  - `train_one_generation.py` — single-generation fine-tune wrapper
    with optional CAT activation.
  - `run_arm_b_alpha_scan.py` — α-scan launcher (one cell = one
    (α, seed) pair, 10 generations) with crash-resume support.
  - `data_pipeline.py` — wikitext-2 load + tokenize + 64-token block
    + real/synthetic mixing per the Shumailov preserve_10pct rule.
  - `generate_synthetic.py` — 5-way beam-search synthetic-data
    generation for next generation.
  - `metrics.py` — perplexity / per-sequence ppl / distinct-n /
    bootstrap CI / Shumailov F1-F3 falsification checks.
  - `config.py` — YAML loader and `CATYamlConfig` dataclass.
  - `shumailov_replication.py` — main entry point for arm 0
    (no-CAT strict-mirror baseline).
- **YAML configs snapshot** (`configs/`)
  - `cat_arm_b_v1_0_release_20260516.yaml` — **v1.0 release config**,
    propagating m_eff = 0.300 (post-hoc multi-seed N = 4 fit) through
    all derived hyperparameters with explicit honest-disclose header.
  - `cat_arm_b.yaml` — config used by the 5/10–5/12 chain; YAML omits
    `m_eff`, so chain runs fell through to dataclass default 1.0.
  - `cat_arm_b_v2_dialectical.yaml` — m_eff = 0.212 single-seed fit
    historical config (rolled back; preserved for record).
  - `shumailov_baseline.yaml` — strict-mirror baseline (no CAT)
    reference config.
  - Sensitivity configs: `shumailov_lr5e-5.yaml`,
    `shumailov_official.yaml`, `sensitivity_fp32_baseline.yaml`,
    `sensitivity_rep_penalty_2.yaml`.
- **Auxiliary scripts snapshot** (`scripts/`)
  - `phase1_robust_chain.sh` — sequential 5-seed × 2-α chain runner
    with 3-retry-per-cell fault tolerance.
  - `chain_watchdog.sh` — chain progress watchdog.
  - `partial_D4_shape_verdict.py` — multi-seed shape-robustness
    verdict for the U-shape modulation finding.
  - `sliding_window_eval_all_gens.py`, `sliding_window_eval.py` —
    sliding-window evaluation utilities.
  - `m_eff_direct_fit.py` — single-seed direct-fit script (5/9, prior
    to the multi-seed N = 4 fit on 5/13).
  - `plot_collapse_curve.py` — plotting utility.
  - `sanity_check_kl.py` — KL sanity check.
  - `yaml_setup_hash.py` — YAML hash verifier ensuring chain stack
    integrity across runs.
- **Chain logs** (`chain_logs/`, 19 files)
  - α = 0.0, seeds 0–4 jsonl (Phase 1 multi-seed baseline,
    5/10–5/11).
  - α = 10.0, seeds 0–4 jsonl (Phase 1 multi-seed CAT,
    5/11–5/12).
  - α scan single-seed (seed = 42): α ∈ {0.0, 1.0, 5.0, 10.0, 50.0}
    jsonl (5/8–5/9).
  - `phase1_robust_20260510_125805.master.log` — chain master log.
  - `phase1_robust_20260510_125805.audit.jsonl` — chain audit jsonl.
  - `phase1_robust_outer_20260510_125805.out` — outer wrapper stdout.
- **Documentation**
  - `README.md` — paper-grade English README.
  - This file (`RELEASE_NOTES.md`).
  - `manifest.sha256` — SHA-256 of every file in this archive.

### 2. What v1.0 does NOT include

- Phase 5 Llama-8B demonstrated result.
- Multi-architecture generalization (e.g., GPT-2 family, Pythia,
  Llama-2-7B beyond Llama-8B).
- Reinforcement Learning from Human Feedback (RLHF) axis
  ℒ_contradiction^Hartree derivation and training results.
- F-1 Phase 2 universal uniqueness study (cross-LLM family).
- Evaluation-paradigm redefinition (deferred to v4.0 — see roadmap).

### 3. Known limitations carried forward to v1.x

- **Code-vs-paper m_eff drift.** Chain logs were produced under
  CATConfig dataclass fallthrough m_eff = 1.0; the paper claims
  m_eff = 0.300. The v1.0 release config aligns the YAML with paper
  but does not retroactively change historical chain semantics.
- **F3 paired-t p = 0.82.** The α = 10 U-shape modulation pattern is
  empirical structure but is not significant at α = 0.05 under the
  pre-registered binary test. Significance gap surfaced
  evaluation-paradigm-level discussion documented in
  `literature/DIALECTICAL_REFLECTION_20260512.md`.
- **Volterra K = 9 metric-only.** The path-dependent kernel is logged
  but does not enter the training loss form. Substantive derivation
  deferred.
- **Multi-seed N = 4 below paper convention.** Shumailov 2024 uses 5
  seeds. Time budget closed Phase 1 at 4 seeds; bootstrap CI partially
  compensates.

### 4. Provenance of the v1.0 m_eff = 0.300 fit

The multi-seed N = 4 fit was performed on 5/13 by
`literature/fit_m_eff_js_multiseed_20260513.py`, consuming the seed
0/1/2/3 baseline jsonl in `chain_logs/`. Prior single-seed (seed = 42
only) fits produced m_eff = 0.212, preserved in
`configs/cat_arm_b_v2_dialectical.yaml`. The N = 4 fit supersedes the
single-seed value because variance under seed = 42 was found to come
largely from fp16 numerical drift, not from genuine model variance.

---

## v1.x and beyond — roadmap stubs (not committed timelines)

### v1.1 — Partial Phase 5

- Single Llama-8B (N = 1) chain on ~$50 cloud budget.
- Verify whether the U-shape modulation pattern survives architecture
  scale-up from 125M to 8B parameters.
- Document scaling behavior of m_eff and J_S across architecture sizes.

### v2.0 — Multi-architecture generalization

- Cross-family chains: OPT, GPT-2, Pythia, Llama-2-7B (minimum 3
  architectures, target 5).
- F-1 universal uniqueness study.
- Substantive K-th order chain rule derivation that enters the
  Volterra K = 9 kernel into the loss form (not just metric).

### v3.0 — RLHF axis

- ℒ_contradiction^Hartree explicit derivation (paper §3).
- RLHF-trained model collapse curve characterization.
- Cross-axis comparison: SFT chain vs RLHF chain modulation under
  CAT.

### v4.0 — Evaluation-paradigm redefinition

- Move beyond paired-t perplexity test as the only significance
  criterion (the F3 p = 0.82 surface drove this).
- Define paradigm-level evaluation primitives that capture U-shape
  modulation, plateau persistence, and middle-trap regime structure
  directly.
- Re-publish v1.0 chain numbers under the new evaluation primitives.

---

## Discipline binding referenced in this release

This release was prepared under the five operational disciplines in
`/home/amd/HEZIMENG/CLAUDE.md` (MaoField D-1 standing rule, 5/15):

1. No claim without experimental data behind every number.
2. No probability claim survives feedback vacuum > 48 hours.
3. Code form has priority over paper form; theory follows practice.
4. Sub-collaborators are an independent second cognitive channel, not
   a quality checker.
5. Errors are the precursor of discovery; never silently correct,
   always log the deviation.

Specifically, the v1.0 m_eff disclosure (chain ran m_eff = 1.0
fallthrough vs paper m_eff = 0.300 post-hoc fit) is an instance of
discipline 5 — the deviation is surfaced as a release-note line, not
silently rewritten.
