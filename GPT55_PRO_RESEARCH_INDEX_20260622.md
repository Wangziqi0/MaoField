# MaoField GPT-5.5 Pro Research Index

> Built on 2026-06-22 after a node-36 takeover audit, six-agent read-only review, RAG-assisted discovery, and direct source reads. This file is a **sanitized repository-local research index** for GitHub / web indexing. It does not replace `STATE.md`; volatile project status still belongs there.

> **D622 21:21 update.** PRO report (6) has been archived locally as a q4
> strict bundle audit. It did **not** approve full 50-checkpoint panel
> generation. Current q4 work is implementation-review eligible only after
> provenance cleanup, fail-fast negative smokes, multi-checkpoint smoke, and a
> separate fold-local q4 analysis path.

## 0. Scope And Evidence Boundary

**Purpose.** Give GPT-5.5 Pro a single repository-visible entry point that merges:

- Claude handoff math content.
- Actual code-level math.
- Current experiment verdicts.
- Superseded claims that must not be revived.
- RAG and file-navigation instructions.

**Not a public paper claim.** This is an internal research index. Treat claims by category:

| Category | Meaning in this index |
|---|---|
| observed | Directly read from code, JSON, git, or verdict files. |
| derived | Computed or logically derived from observed files. |
| claimed | Interpretation supported by evidence but not itself a raw measurement. |
| blocked | Missing artifact, missing independent validation, or reserved for PI / Win judgment. |

**Current git snapshot when this index was built.**

- Repo: `Wangziqi0/MaoField`
- Branch: `main`
- HEAD before this index: `ac9253a1b61a4da59e01961564709e9f1becf33f`
- Working tree before edits: tracked diff empty; untracked `AGENTS.md` and `.codex/config.toml`
- Important correction: D619 files `experiments/exp020_metric_stress_test/HANDOFF_TO_GPT_20260619.md` and `experiments/exp020_metric_stress_test/MATH_LINE_VERDICT_20260619.md` are already tracked as of commit `23c21bb`; older handoff text saying they were untracked is stale.

## 1. Read Order

Use this order for a cold start:

1. [STATE.md](STATE.md) for volatile state and current bindings.
2. [AGENTS.md](AGENTS.md) if present in the local checkout, plus [CLAUDE.md](CLAUDE.md) for legacy project method authority.
3. This index.
4. [交接索引_GPT_20260626.md](交接索引_GPT_20260626.md) for the broader GPT handoff pointer.
5. Core verdict files:
   - [MATH_LINE_VERDICT_20260619.md](experiments/exp020_metric_stress_test/MATH_LINE_VERDICT_20260619.md)
   - [C_metapattern_evidence_base_20260618.md](experiments/exp020_metric_stress_test/C_metapattern_evidence_base_20260618.md)
   - [DECOUPLE_VERDICT_20260617.md](experiments/exp019_alpha1_confirm/decouple_verdict_20260617/DECOUPLE_VERDICT_20260617.md)
   - [exp019_VERDICT.md](experiments/exp019_alpha1_confirm/verdict_20260614/exp019_VERDICT.md)
6. Method discipline:
   - [D-1-five-disciplines.md](docs/discipline/D-1-five-disciplines.md)
   - [D-2-parallel.md](docs/discipline/D-2-parallel.md)
   - [D-3-dialectical-reflection.md](docs/philosophy/D-3-dialectical-reflection.md)
   - [retracted_claims.md](docs/retracted_claims.md)
7. D622 q4 strict audit:
   - [deep_research_q4_panel_strict_audit_20260622.md](docs/infra/gpt_deep_research/deep_research_q4_panel_strict_audit_20260622.md)
   - [Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md](docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md)
   - [PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md](docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md)
   - [PANEL_PRIMARY_ARTIFACT_SMOKE_20260622.md](docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_SMOKE_20260622.md)

## 2. Current Scientific Position

**Observed / derived.**

- MaoField is now best treated as an empirical pilot study with negative-result center of gravity.
- exp019 alpha=1 confirmatory line failed all three locked endpoints; gate stopped at E1. See [locked_verdict.json](experiments/exp019_alpha1_confirm/verdict_20260614/locked_verdict.json).
- exp019 decoupling line is superseded by D617 recomputation: 0/5 chains met the preregistered decoupling criterion. See [DECOUPLE_VERDICT_20260617.md](experiments/exp019_alpha1_confirm/decouple_verdict_20260617/DECOUPLE_VERDICT_20260617.md).
- exp020 C(meta-pattern) is the current research synthesis: multiple candidate collapse measures intended to be independent of PPL either reduce to PPL/logit siblings, fall below late-generation seed noise, or are decode-confounded. See [C_metapattern_evidence_base_20260618.md](experiments/exp020_metric_stress_test/C_metapattern_evidence_base_20260618.md).

**Claimed but constrained.**

- C is a regime-limited, falsifiable meta-pattern, not a universal statement that collapse is unmeasurable.
- F3 slice-gap hysteresis is a weak real exception inside PPL-function space; it is **worth pursuing but not a positive finding**.
- "C explains why Shumailov / Gerstgrasser / Schaeffer disagree" is an interpretation / hypothesis, not an established result.

**Blocked / reserved.**

- Philosophical / dialectical-materialist framing is reserved for Win + PI; execution agents should mark it `[?]`.
- Multi-channel novelty is blocked as a novelty claim unless the full 2x2 / flux ablation evidence exists.
- T2 IFF sufficiency and T3 full nonlinear characterization remain open math tasks.

## 3. Actual Code Math: Contradiction Loss

The key historical trap is that project prose, paper drafts, and code comments mention a three-term form, but the chain actually analyzed in the main pilot reduced to a **two-term EMA-deviation form**.

### 3.1 Code-Level `D_n`

Primary code: [contradiction_loss.py](experiments/exp018_cat/archive/v1.0_release_20260516/src/contradiction_loss.py)

`compute_kl` computes a KL on a validation batch:

```text
D_n = KL(q_EMA || p_current)
```

Implementation anchors:

- Current model has gradients: [contradiction_loss.py:153](experiments/exp018_cat/archive/v1.0_release_20260516/src/contradiction_loss.py#L153)
- EMA model is no-grad: [contradiction_loss.py:155](experiments/exp018_cat/archive/v1.0_release_20260516/src/contradiction_loss.py#L155)
- `q = exp(log_q).detach()`: [contradiction_loss.py:164](experiments/exp018_cat/archive/v1.0_release_20260516/src/contradiction_loss.py#L164)
- KL scalar mask average: [contradiction_loss.py:172](experiments/exp018_cat/archive/v1.0_release_20260516/src/contradiction_loss.py#L172)

### 3.2 Generic Tracker Form In Code

`compute_loss` builds:

```text
L_cont = lambda_1 * (D_n - D_{n-1})^2
       + lambda_2 * (D_n - D_ema)^2
       + lambda_3 * T2_replace
```

Anchors:

- History branches and detached previous `D`: [contradiction_loss.py:204](experiments/exp018_cat/archive/v1.0_release_20260516/src/contradiction_loss.py#L204)
- Memory term: [contradiction_loss.py:218](experiments/exp018_cat/archive/v1.0_release_20260516/src/contradiction_loss.py#L218)
- T2 options: [contradiction_loss.py:227](experiments/exp018_cat/archive/v1.0_release_20260516/src/contradiction_loss.py#L227)
- Weighted loss: [contradiction_loss.py:239](experiments/exp018_cat/archive/v1.0_release_20260516/src/contradiction_loss.py#L239)
- Volterra accumulator is metric-only, not in loss: [contradiction_loss.py:245](experiments/exp018_cat/archive/v1.0_release_20260516/src/contradiction_loss.py#L245)
- KL EMA update is detached: [contradiction_loss.py:258](experiments/exp018_cat/archive/v1.0_release_20260516/src/contradiction_loss.py#L258)

### 3.3 Chain-Actual Form

Important distinction:

| Layer | What it means | Current status |
|---|---|---|
| Current code defaults | The defaults in `KLContradictionConfig` in the archived / current source tree | `beta_model=0.999849`, `beta_kl=0.8090`, `lambda_1=2.3585`, `lambda_2=0.1060`, `lambda_3=0.2120`, `T_2_form=quadratic`, `K=9`, `m_eff=0.212` |
| Historical chain actual | The configuration actually launched for the 5/10-5/12 chain analyzed by the pilot | Old YAML / launcher path; effectively uniform lambdas and `K=1` |

The code-first audit found that the actual 5/10-5/12 chain used old YAML overrides:

```text
lambda_1 = lambda_2 = lambda_3 = 1
T_2_form = relu_dpp
kl_history_K = 1
```

Because `K=1`, `D_doubleprime` is always zero in the branch that has only one history item. Therefore the actual training contradiction loss reduced to:

```text
L_cont_chain_actual(theta_n) = (D_n - D_{n-1})^2 + (D_n - D_ema)^2
```

Source:

- [CODE_FIRST_EXTRACT_DERIVE_ASSESS_20260517.md](experiments/exp018_cat/literature/CODE_FIRST_EXTRACT_DERIVE_ASSESS_20260517.md)
- Especially the chain-actual boxed form in section 1.4.

Do not use current defaults to reinterpret historical chain results unless the run logs prove those defaults were active.

### 3.4 Total Loss Integration

The trainer adds contradiction loss only every `kl_update_every` steps:

```text
L_total = L_LM + alpha * L_cont
```

Anchors:

- Should-compute condition: [cat_trainer.py:107](experiments/exp018_cat/archive/v1.0_release_20260516/src/cat_trainer.py#L107)
- Total loss addition: [cat_trainer.py:123](experiments/exp018_cat/archive/v1.0_release_20260516/src/cat_trainer.py#L123)
- Other steps fall back to LM only: [cat_trainer.py:140](experiments/exp018_cat/archive/v1.0_release_20260516/src/cat_trainer.py#L140)

### 3.5 Code/Paper Mismatch To Preserve

Do not conflate these:

| Quantity | Training code | Paper / evaluation metric |
|---|---|---|
| `D_n` in loss | KL between EMA model and current model on val batch | Often discussed as log PPL ratio or collapse metric |
| Gradient | Through current `D_n` only; history and EMA detached | No cross-generation gradient |
| Volterra / path term | Logged as metric only in this implementation | Appears in older math drafts |
| Chain actual loss | Two terms | Older prose may mention three terms |

If code and paper disagree, project discipline says paper should chase code unless a later experiment explicitly invalidates the code form.

## 4. Experiment Verdict Map

### 4.1 exp019 Alpha=1 Confirmatory

Primary verdict: [exp019_VERDICT.md](experiments/exp019_alpha1_confirm/verdict_20260614/exp019_VERDICT.md)

Machine-readable verdict: [locked_verdict.json](experiments/exp019_alpha1_confirm/verdict_20260614/locked_verdict.json)

Observed results:

| Endpoint | Mean diff | Sign-flip p | Zone |
|---|---:|---:|---|
| E1 geometry | +0.12352 | 0.625 | FALSE |
| E2 PPL | +0.85856 | 0.9375 | FALSE, exploratory after gate stop |
| E3 path B | +0.06194 | 1.0 | FALSE, exploratory after gate stop |

Interpretation: s42 was an idiosyncratic outlier; C1/C2/C3 are withdrawn and must not be revived.

### 4.2 exp019 Decouple Line: Superseding Verdict

Primary verdict: [DECOUPLE_VERDICT_20260617.md](experiments/exp019_alpha1_confirm/decouple_verdict_20260617/DECOUPLE_VERDICT_20260617.md)

Machine-readable result: [decouple_n5_result.json](experiments/exp019_alpha1_confirm/decouple_verdict_20260617/decouple_n5_result.json)

Script: [analysis_decouple_n5.py](experiments/exp019_alpha1_confirm/scripts/analysis_decouple_n5.py)

Observed:

- Preregistered single-chain decoupling = D1 and D2 and D3.
- D1 total distinct-2 drop passed 3/5.
- D2 recovery-phase continued drop passed 0/5.
- D3 repeat-rate increase passed 5/5.
- Net decoupled chains: 0/5.

Important supersession: older [exp019_VERDICT.md](experiments/exp019_alpha1_confirm/verdict_20260614/exp019_VERDICT.md) still says decouple `[A-]` survived; that line is superseded by D617 and must be treated as false.

### 4.3 Recovery Geometry

Primary verdict: [RECOVERY_GEOMETRY_FINDINGS_20260615.md](experiments/exp018_cat/analysis/RECOVERY_GEOMETRY_FINDINGS_20260615.md)

Observed:

- Geometry metrics are non-monotone humps synchronized with the PPL hump.
- E0 single-step geometry signal exaggerated steady-state change by roughly 2.2x.
- Geometry is not a second independent decoupling signal; it is likely a representation-space projection of the same PPL process.

### 4.4 exp020 ArmA / Multi-Channel Structure

Primary file: [ARMA_FINDINGS_20260618.md](experiments/exp020_metric_stress_test/ARMA_FINDINGS_20260618.md)

Observed code structure:

- Synthetic generation uses true `train_blocks` as prompts: [run_arm_b_alpha_scan.py:285](experiments/exp018_cat/src/run_arm_b_alpha_scan.py#L285)
- Mixed-generation dataset receives both real and synthetic inputs, with condition-controlled `original_fraction`: [run_arm_b_alpha_scan.py:296](experiments/exp018_cat/src/run_arm_b_alpha_scan.py#L296)
- Each generation fine-tunes from `gen0_dir`, not the previous generation: [run_arm_b_alpha_scan.py:305](experiments/exp018_cat/src/run_arm_b_alpha_scan.py#L305)

Allowed statement:

- The nominal no-preserve self-iteration runner still contains persistent true-prompt and gen0-reset channels.

Blocked upgrade:

- Do not claim causal proof that these channels drive recovery, nor that the novelty is open terrain, unless the locked 2x2 / flux ablation criteria are satisfied.

### 4.5 exp020 C Meta-Pattern

Primary file: [C_metapattern_evidence_base_20260618.md](experiments/exp020_metric_stress_test/C_metapattern_evidence_base_20260618.md)

Frame-neutral claim:

```text
Across five preregistered / blind / adversarial-gate attempts, candidate collapse measures intended to be independent of PPL either collapse back into PPL/logit siblings, fall under late-generation seed noise, or are decode-confounded.
```

Do not overstate:

- Not "collapse is unmeasurable."
- Not "everything is mean-PPL."
- Not "positive finding."
- Not "paradigm shift."

Source-path correction: older prose may mention `verify_gate5b.py`; the repository-visible gate-5 script is [verify_gate5_distinct2_collinear.py](experiments/exp020_metric_stress_test/scripts/verify_gate5_distinct2_collinear.py).

### 4.6 High-Order PPL / F3 Exception

Script: [highorder_ppl_run.py](experiments/exp020_metric_stress_test/scripts/highorder_ppl_run.py)

Result: [highorder_result.json](experiments/exp020_metric_stress_test/highorder_ppl_20260618/highorder_result.json)

Observed:

- Branch1 in result JSON.
- F1-var, F1-tail, and F3-slice-gap pass the script's gate A and gate B.
- F1-var and F1-tail are mostly reconstructible from mean log-probability.
- F3-slice-gap is the weak exception: a differential freq-vs-rare structure / hysteresis signal.

Constraint:

- F3 is "worth pursuing, not positive." It needs independent seeds, cross-condition sign-test, and primary-source prior-art verification.
- Old aggregate LOSO/permutation cleanup is now persisted under
  [docs/infra/math_turn_20260622/](docs/infra/math_turn_20260622/), but the
  final verdict remains `insufficient_artifact`: F3 weak LOSO delta passed,
  matched-mean failed, and rank/residual failed/blocked.
- Prior-art occupancy for F3 is not primary-source-verified in this index. Treat "already occupied" as claimed / needs Win+PI or direct paper verification.

### 4.7 D622 q4 Panel Strict Audit

Primary local interpretation:
[Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md](docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md)

External/bundle audit:
[deep_research_q4_panel_strict_audit_20260622.md](docs/infra/gpt_deep_research/deep_research_q4_panel_strict_audit_20260622.md)

Observed / adopted:

- q4 schema/runbook are locked.
- q8 was not repaired or promoted because it has an empty bin.
- Manifest-only plus seed1/gen0 one-checkpoint smoke passed and reproduced the
  old aggregate row with zero absolute diff.
- The smoke is generator-alignment evidence only, not a scientific signal.

Current decision:

- Full 50-checkpoint q4 panel generation is **not approved**.
- Current generator and q4 locked schema are eligible only for full-panel
  implementation review.

Must fix before launch:

- Add/record `builder_script_sha256` and exact artifact provenance.
- Resolve the old non-clean / multi-HEAD provenance issue in generated
  manifests or record artifact-generation commit and recording commit
  explicitly.
- Add fail-fast negative smokes for schema hash, source hash, and split wording.
- Add multi-checkpoint smoke coverage before any full panel.
- Implement a separate q4 full-panel analysis script with fold-local LOSO,
  pairing, projection, and control gates.

Still blocked:

- `LOSO passed`
- `F3 positive`
- `mean-null vector field survives`
- `glass box broken`
- training authorization
- new loss authorization

## 5. D619 Math-Line Verdict

Primary file: [MATH_LINE_VERDICT_20260619.md](experiments/exp020_metric_stress_test/MATH_LINE_VERDICT_20260619.md)

### T1

Verdict: base-reset vs Borkar `c * mu` strong static orthogonality is falsified at the scalar Gaussian toy layer.

Allowed:

- In toy scalar form, there is a bijection `c = w/(1+w) = 1/(eta*T + 1)` that makes steady-state distributions identical.
- M3 eta/T-response survives as a possible discriminator.

Blocked:

- Do not claim the true OPT-125m high-dimensional system is proven reducible to scalar Borkar `c`.

### T2

Verdict: F3 hysteresis has a weak mechanistic derivation in a two-component model.

Allowed:

- Hysteresis iff cross-rate determinant `D = a_fd*a_ru - a_fu*a_rd != 0` in the toy mechanism.

Blocked:

- The IFF sufficiency half lacks code artifact. This is an explicit queue item.

### T3

Verdict: "refuse the scalar" carrier is partly identified as linear difference measures in the orthogonal complement of the evaluation measure.

Blocked:

- Complete nonlinear characterization is open.
- Cubic gate A is broken; LOSO is the stronger material support.

### Zero-GPU Queue

1. Run the linear-difference kill-test on existing JSONL artifacts.
2. Implement the two-component mixture script for T2 sufficiency.
3. Replace cubic gate A with LOSO as the main gate and restate weak margins.

These are research tasks, not already completed facts.

## 6. L0 / Earlier Math Index

Useful entry points:

- [MAOFIELD_INDEX_MATH_PROP_20260529.md](experiments/exp018_cat/dppl_bridge_verify_d21_output/MAOFIELD_INDEX_MATH_PROP_20260529.md)
- [MAOFIELD_L0_ROUND2_INTEGRATION_20260529.md](experiments/exp018_cat/dppl_bridge_verify_d21_output/MAOFIELD_L0_ROUND2_INTEGRATION_20260529.md)

Conservative summary:

- 0 unconditional close is safe.
- Per-proof tier counts should be checked against the integration file before being quoted as a current claim.

## 7. Do-Not-Revive List

Authority: [retracted_claims.md](docs/retracted_claims.md)

Never revive:

- `paradigm-shift`
- `first dialectical materialism instantiation`
- `first reflexive AI`
- `first systematic empirical study`
- `axiom-first`
- `universal uniqueness`
- `mitigation framework`
- `universal solution across architectures`
- exp019 C1/C2/C3 alpha=1 positive claims
- exp019 decouple `[A-]` / 4-of-5 / 5-of-5 positive claims
- fractal / C3 frozen mainline narrative
- NMI / NeurIPS / NCS / Nature-main-paper target narrative

Safe replacement language:

- "empirical pilot study"
- "negative result"
- "regime-limited evidence"
- "falsifiable meta-pattern"
- "weak exception, not positive"
- "blocked / requires independent verification"

## 8. RAG And Search Procedure

Use RAG for semantic location only:

```bash
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py "query" --top-k 8 --project MaoField
```

Then verify with file reads:

```bash
rg "pattern" /media/amd/raid1/canonical/projects/MaoField
sed -n '1,220p' path/to/file.md
jq '.' path/to/result.json
```

Known coverage caveats:

- `MD_CATALOG.md` is useful but stale; it is a navigation map, not latest truth.
- `sessions/handoff-gpt-20260626/` is outside the MaoField repo and not reliably available to GitHub/web indexing.
- This file is the repository-local replacement for the research subset of that handoff.
- As of the D622 21:21 q4 strict-audit adoption, local RAG has not yet been
  rebuilt to include report (6). Use direct file reads for report (6) until the
  RAG index is regenerated.

## 9. GitHub / Web Indexing Package

For GPT-5.5 Pro via GitHub or web indexing, prefer this repository-local set:

- [GPT55_PRO_RESEARCH_INDEX_20260622.md](GPT55_PRO_RESEARCH_INDEX_20260622.md)
- [交接索引_GPT_20260626.md](交接索引_GPT_20260626.md)
- [STATE.md](STATE.md) if private/internal indexing is allowed.
- [MATH_LINE_VERDICT_20260619.md](experiments/exp020_metric_stress_test/MATH_LINE_VERDICT_20260619.md)
- [C_metapattern_evidence_base_20260618.md](experiments/exp020_metric_stress_test/C_metapattern_evidence_base_20260618.md)
- [DECOUPLE_VERDICT_20260617.md](experiments/exp019_alpha1_confirm/decouple_verdict_20260617/DECOUPLE_VERDICT_20260617.md)
- [CODE_FIRST_EXTRACT_DERIVE_ASSESS_20260517.md](experiments/exp018_cat/literature/CODE_FIRST_EXTRACT_DERIVE_ASSESS_20260517.md)
- [contradiction_loss.py](experiments/exp018_cat/archive/v1.0_release_20260516/src/contradiction_loss.py)
- [Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md](docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md)
- [PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md](docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md)

Do not commit or index raw operational handoff chapters that include local security / credential / proxy operations unless they are separately sanitized.

Repository-local evidence preferred for web indexing:

- Use committed Markdown, scripts, and small JSON files.
- Do not rely on `/media/.../canonical/wip/...` paths for GitHub indexing; those may contain large artifacts or machine-local run packages.
- If a wip artifact is scientifically necessary, summarize it in a sanitized tracked Markdown file with checksums and paths, then classify it before promotion.

## 10. Immediate Research Handoff

Best next steps for GPT-5.5 Pro research:

1. Do not launch full q4 panel yet; first review provenance, negative-smoke,
   multi-checkpoint smoke, and fold-local analysis implementation.
2. Treat q4 as a locked diagnostic carrier, not a pristine confirmatory proof.
3. If the q4 implementation gate is repaired, decide whether the 50-checkpoint
   panel is worth running before any training or new-loss work.
4. Keep the older zero-GPU T2 toy sufficiency script and linear-difference
   kill-test as secondary math tasks.
5. If PI wants external validity, design outward generalization to another collapse setup rather than another inward MaoField-only negative.
6. Keep philosophical interpretation `[?]` unless Win + PI promote it with evidence.

The main guardrail: do not let a cleaner index become a cleaner overclaim.
