# MaoField Experiment Convergence And Math-Turn Gate

> Node36 canonical note, 2026-06-22 16:10 CST.
> Classification: wip/core research planning.
> This file closes the current evidence round and defines the next
> zero-GPU mathematical gate. It is not a new experimental result and
> does not promote any GPT/PRO report to primary evidence.

## 0. Evidence Boundary

This convergence note uses:

- `STATE.md` as the volatile project truth source.
- `GPT55_PRO_RESEARCH_INDEX_20260622.md` as repository-local navigation.
- `docs/infra/gpt_deep_research/` as GPT/PRO claim-source only.
- `experiments/exp019_alpha1_confirm/` verdicts and JSON as primary exp019 evidence.
- `experiments/exp020_metric_stress_test/` verdicts, scripts, and JSON as primary exp020 evidence.
- RAG query on 2026-06-22:
  `MaoField current experiment convergence SES exp020 F3 weak exception mean-null vector LOSO math turn`.

PRO report (3) is a proposed-method audit. The mean-null vector field,
LOSO, matched-mean, and rank/residual gates are not yet observed training
results.

## 1. Current Round Closure

The current experimental round is closed as a negative-centered synthesis:

1. `exp019 alpha=1` confirmatory endpoints are all FALSE. C1/C2/C3 remain
   withdrawn and must not be revived.
2. The exp019 decoupling safety line is dead as a positive claim:
   faithful N=5 recomputation gives `0/5` chains satisfying the preregistered
   decoupling criterion.
3. Recovery geometry is a PPL-synchronized hump/projection, not an independent
   collapse signal.
4. exp020 closes at C(meta-pattern): candidate collapse measures meant to be
   independent of PPL mostly reduce to PPL/logit siblings, seed-noise floor, or
   decode sensitivity.
5. F3 slice-gap is the only weak exception. It is worth pursuing, but it is
   not a positive finding and not a glass-box break.
6. The historical chain-actual training object is a sparse, two-term scalar
   KL/EMA smoother:

   ```text
   L_cont_chain = (D_n - D_{n-1})^2 + (D_n - D_ema)^2
   D_n = KL(q_EMA || p_current)
   ```

   Volterra, GradNorm, F1/F3, and LOSO are metrics or post-hoc audits in the
   current evidence set, not optimizer-level constraints.

Allowed closing sentence:

```text
MaoField currently has a clean negative-centered measurement-audit result:
the historical method has not broken the glass box, and the only surviving
technical lead is a weak, post-hoc F3/slice residual that must pass stricter
zero-GPU gates before any new training is justified.
```

Forbidden closing upgrades:

- "glass box broken"
- "positive F3 finding"
- "first dialectical materialism / first reflexive AI / paradigm shift"
- "vector KL field survives"
- "LOSO passed" unless a primary artifact is written and reviewed
- "current contradiction loss is anti-collapse barrier"

## 2. Why The Math Turn Is Necessary

The current loss can become blind to any bad state that enters a scalar
KL platform. If `D_n = D*` after some update, then:

```text
(D_n - D_{n-1})^2 -> 0
(D_n - D_ema)^2 -> 0
```

because the scalar EMA catches up geometrically. This is the smallest
mathematical reason the old object cannot carry the highest goal.

The next turn must refuse scalar completion. It should ask whether there is a
stable residual in a mean-null subspace, not whether another dashboard metric
looks interesting.

## 3. Next Mathematical Object

Start from the existing scalar KL and minimally lift it to fixed slices:

```text
k_n[j] = mean tokenwise KL on fixed slice B_j
D_n    = w^T k_n
u_n    = P_perp k_n
P_perp = I - 1 w^T
```

`u_n` removes the mean KL mode. If a candidate structure disappears after this
projection or is predictable from low-order nuisance coordinates, it is not the
new carrier.

A possible later training loss may be:

```text
L_field =
  lambda_s ||u_n||^2
+ lambda_v ||u_n - u_{n-1}||^2
+ lambda_m ||u_n - EMA(u)||^2
```

But this is not authorized as a training objective yet. It first has to pass
the audit below.

## 4. Zero-GPU Gate Before Any New Training

Stage A: artifact closure.

- Re-read `locked_verdict.json`, `decouple_n5_result.json`,
  `highorder_result.json`, `MATH_LINE_VERDICT_20260619.md`, and
  `C_metapattern_evidence_base_20260618.md`.
- Re-run only cheap CPU scripts when useful, using `/home/amd/venv/bin/python`.
- Persist any new audit result as JSON/MD before promoting it to STATE.

Stage B: LOSO-first high-order audit.

- Treat the old cubic gate as broken.
- Report F1/F3 through LOSO, matched-mean, and permutation/null controls.
- Keep the conclusion at "weak exception" unless the new artifact proves
  otherwise.

Stage C: mean-null slice audit.

- Compute fixed-slice `k_n` or a surrogate from existing checkpoint/eval
  artifacts.
- Project to `u_n = P_perp k_n`.
- Test whether projected structure survives nuisance-only prediction.

Kill conditions:

- nuisance-only LOSO explains nearly all projected signal;
- matched-mean pairs have unstable or random sign;
- projected matrix is effectively rank-1 or below noise floor;
- result depends on unregistered slice choices.

Survival conditions:

- at least one preregistered projection leaves residual energy above noise;
- matched-mean contrast has stable direction;
- LOSO does not collapse the signal into mean/PPL/generation nuisance;
- slice definition is fixed before reading the outcome.

Only after Stage C survives should the project design a new training run.

## 5. Immediate Next Step

Do not start GPU training.

The next executable step is a small audit package:

```text
scripts/math_turn_loso_audit.py
docs/infra/math_turn_20260622/
```

It should consume existing JSON first and write a machine-readable verdict.
If the result kills F3/mean-null residuals, the project should accept the
stronger negative paper path. If it survives, then and only then define the
vector-field training patch.
