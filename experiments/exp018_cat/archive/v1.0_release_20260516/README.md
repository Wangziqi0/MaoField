# MaoField Contradiction-Aware Training — v1.0 Release

**Release date:** 2026-05-19
**Status:** Empirical pilot study (systematic, not yet fully verified)
**Scope:** OPT-125m on wikitext-2, self-iteration collapse mitigation via KL-derived contradiction loss

This release packages the code, configs, and chain logs used to run the
contradiction-aware training (CAT) pilot study on top of a strict-mirror
Shumailov et al. 2024 self-iteration baseline. It corresponds to the
state of the codebase on 2026-05-19, freezing the empirical pilot phase
before larger-architecture follow-ups (Llama-8B, multi-arch, RLHF axis).

The release is intended as an honest snapshot — including code-vs-paper
divergences, partial isomorphism caveats, and limited multi-seed coverage —
not as a polished framework.

---

## 1. What this is

We study whether augmenting standard language-model fine-tuning with a
second-order KL contradiction penalty modulates the model-collapse curve
reported by Shumailov et al. 2024 *Nature* 631:755-759.

The total loss in arm B is

    L_total = L_LM + α · L_contradiction

where L_contradiction is built from the time-series of validation KL
divergence between the current model and an EMA teacher,

    L_contradiction = λ_1 (ΔD_n)^2 + λ_2 (D_n − D̄_n^EMA)^2 + λ_3 T_2(D_n).

Two T_2 forms are implemented (`T_2_form` in the config):
- `quadratic` — symmetric D^2 / 2 (v1.0 release default).
- `relu_dpp`  — punitive single-side ReLU(D''_n) (legacy, used in 5/8 alpha
  scan with seed=42).

The Klein-Gordon-style propagation of (λ_1, λ_2, λ_3, β_kl, β_model)
from a single effective mass m_eff is form-borrowing (Tauber 2014 §4.2),
**not** a first-principles derivation. See §6 of the paper for explicit
disclose of the 25–40 % partial structural correspondence claim.

## 2. Why

- Shumailov et al. 2024 (Nature) report unexplained mean-perplexity
  divergence under self-iteration on OPT-125m / wikitext-2.
- Borji 2024 (arXiv) reports related anomalies across other generative
  setups.
- No existing intervention that we are aware of targets the KL second-order
  trajectory directly as a regularizer. This release provides a minimal
  empirical probe.

## 3. Key empirical numbers (v1.0 reference)

All numbers below are from the chain logs in `chain_logs/`. They are
provided as reference points, not as final published claims.

| Quantity                                             | Value                              | Source                                                  |
|------------------------------------------------------|------------------------------------|---------------------------------------------------------|
| Strict-mirror baseline gen 0 ppl (α = 0)             | ≈ 36                               | `armb_alpha0.0_seed*` jsonl, generation 0 record         |
| Strict-mirror baseline gen 9 ppl (α = 0)             | ≈ 53                               | `armb_alpha0.0_seed*` jsonl, generation 9 record         |
| Multi-seed N = 4 baseline std at gen 0               | 0.22 %                             | Partial D4 5/5 PASS STRONG ROBUST (5/11)                |
| Sliding-window eval std                              | 0.08 %                             | `sliding_window_eval_all_gens.py`                       |
| m_eff (Klein-Gordon mass coefficient)                | **0.300 ± 0.066**                  | post-hoc multi-seed N = 4 fit (5/13)                    |
| J_S (Jensen-Shannon nat / token / generation)        | **0.33 – 0.77**                    | three estimator methods, 5/13 multi-seed fit            |
| α = 10 plateau effect                                | −4.2 % vs α = 0 (gen 6 – 9)         | `armb_alpha10.0_seed{1,2,3,4}` jsonl                     |
| F3 paired-t p-value (α = 10 vs α = 0)                | 0.82                                | `partial_D4_shape_verdict.py`                           |

**Single-seed (seed = 42 only) prior fit gave m_eff = 0.212.** That value is
preserved in `configs/cat_arm_b_v2_dialectical.yaml` for historical record,
but the v1.0 release config (`configs/cat_arm_b_v1_0_release_20260516.yaml`)
uses the multi-seed N = 4 value m_eff = 0.300.

## 4. How to reproduce the chain

### 4.1 Environment

- OS: Linux 6.x (tested on Ubuntu 22.04 derivative)
- GPU: AMD Radeon RX 9070 XT (gfx1201, RDNA 4)
- ROCm: 7.2 (tested) — earlier ROCm 6.2/6.3 with
  `HSA_OVERRIDE_GFX_VERSION=11.0.0` may also work
- Python: 3.10+
- Key Python packages (pinned versions in `requirements_pinned.txt` if
  present; otherwise current versions used during 5/7–5/12 chain):
  - `torch` with ROCm wheel
  - `transformers` ≥ 4.40
  - `datasets` ≥ 2.18
  - `tqdm`, `numpy`, `pyyaml`

ROCm install helper: `scripts/install_rocm_torch.sh` (from upstream
exp018_cat scripts directory, not copied into this archive).

### 4.2 Run a single (α, seed) cell

    cd /home/amd/HEZIMENG/MaoField/experiments/exp018_cat
    env HF_ENDPOINT=https://hf-mirror.com \
        HIP_VISIBLE_DEVICES=0 \
        CUDA_VISIBLE_DEVICES=0 \
        .venv/bin/python src/run_arm_b_alpha_scan.py \
            --config archive/v1.0_release_20260516/configs/cat_arm_b_v1_0_release_20260516.yaml \
            --alpha 10.0 \
            --seed 0 \
            --num-generations 10

Each (α, seed) cell takes roughly 4–6 GPU-hours on RX 9070 XT
(10 generations × 5 epochs of OPT-125m fine-tune + 10 beam-search
synthetic-data generations).

### 4.3 Run the full Phase 1 chain (5 seeds × 2 alphas)

    bash scripts/phase1_robust_chain.sh

This launches the cross-product `alphas ∈ {0.0, 10.0} × seeds ∈ {0..4}`
sequentially with up to 3 retries per cell on failure. It writes:

- `logs/phase1_robust_<ts>.master.log` — human-readable progress log
- `logs/phase1_robust_<ts>.audit.jsonl` — JSON-line machine-readable audit
- `logs/phase1_robust_alpha<α>_seed<s>_attempt<n>_<ts>.log` — per-cell stdout

The corresponding production jsonl per cell is
`logs/armb_alpha<α>_seed<s>_<ts>.jsonl`.

### 4.4 Expected output structure (jsonl)

Each `armb_alpha<α>_seed<s>_<ts>.jsonl` contains one record per generation
plus a run-start header. Generation records have shape:

    {
      "stage": "generation_done",
      "generation": 7,
      "alpha": 10.0,
      "seed": 2,
      "val_perplexity": 51.3,
      "test_perplexity": 50.8,
      "test_loss": 3.93,
      "epochs": 5,
      "n_train_blocks": 36284,
      "n_synthetic_blocks": 36284,
      "model_path": "data/checkpoints_armb/alpha10.0/no_preserve_seed2/generation_7",
      "cat_enabled": true,
      "cat_alpha": 10.0
    }

Resume support: if a generation's checkpoint directory already contains
`model.safetensors`, `run_arm_b_alpha_scan.py` will re-evaluate test
perplexity from disk and skip fine-tuning + generation for that cell
(see the `RESUME` block in the script).

## 5. Cross-references

- Paper: `paper_v6_emergency_fix_20260518.md` (or latest `paper_v*.md` in
  `literature/`). v1.0 release corresponds to paper v6 / v7 numbers.
- Appendix D (Partial D4 shape robustness verdict):
  `literature/EXP_RIGOROUS_VERIFY_20260512.md` and
  `scripts/partial_D4_shape_verdict.py`.
- Appendix E (multi-seed fit of m_eff and J_S):
  `literature/fit_m_eff_js_multiseed_20260513.py` and
  `literature/MATH_100_PERCENT_RIGOROUS_20260513.md`.
- m_eff direct fit single-seed history:
  `literature/m_eff_direct_fit_verdict_20260510.md`.

## 6. Caveats (must remain visible)

1. **Pilot scale.** OPT-125m only; one architecture family; wikitext-2 only.
   Generalization beyond this setup is not claimed.
2. **Partial isomorphism.** The KL second-order training loss is
   form-borrowing from Klein-Gordon Lagrangian density structure with
   25–40 % structural correspondence (5 dimensions: 2 full, 2 partial,
   1 weak). It is not a first-principles derivation.
3. **Code-vs-paper drift on m_eff.** Chain logs in `chain_logs/` were
   produced with m_eff = 1.0 (CATConfig dataclass fallthrough; see
   `configs/cat_arm_b_v1_0_release_20260516.yaml` disclose header).
   The paper analysis uses the post-hoc multi-seed N = 4 fit m_eff = 0.300.
   Re-runs with v1.0 release config will propagate m_eff = 0.300 through
   λ_i / β_kl / β_model / χ kernel.
4. **Volterra K = 9 kernel is metric-only.** The K-th order
   path-dependent accumulator Σ_{k=1..9} χ(k) D_{n−k} is logged in
   `volterra_sum_K` but does not enter the training loss. Entering it
   requires K-th order chain rule + T_H Markov kernel substantive
   derivation, deferred to v2.0+.
5. **F3 paired-t p = 0.82 is not significant at α = 0.05.** The α = 10
   modulation pattern is empirical structure (U-shape middle-trap +
   plateau-persist), not statistically significant under the
   pre-registered binary test. Significance triggered a paradigm-evaluation
   reframe documented in `literature/DIALECTICAL_REFLECTION_20260512.md`.
6. **Multi-seed N = 4 is below paper convention.** Shumailov 2024 reports
   5-seed runs; this release stopped at N = 4 due to time budget.
   Bootstrap CI in `metrics.py` partially compensates.

## 7. Not included in v1.0

- Phase 5 Llama-8B demonstrated result (D60+).
- Multi-architecture generalization (D60+).
- Reinforcement Learning from Human Feedback (RLHF) axis derivation
  (D60+).
- F-1 Phase 2 universal uniqueness study (D60+).

See `RELEASE_NOTES.md` for the v1.1 / v2.0 / v3.0 / v4.0 roadmap stubs.

## 8. License

MIT License. See repository-level LICENSE file if present, or treat the
contents of this release as MIT-licensed for academic reproduction.

## 9. Citation

If you reference the contradiction-aware training pilot directly, please
cite the corresponding MaoField paper draft (latest version in
`literature/paper_v*.md`). If you reference the Shumailov baseline that
this study builds on, please cite the original Shumailov et al. 2024
*Nature* article.

## 10. Honest contact

This release is a 16-year-old independent researcher's pilot study under
discipline binding (see `CLAUDE.md` at `/home/amd/HEZIMENG/CLAUDE.md`).
Issues, reproduction failures, and falsification attempts are welcome.
