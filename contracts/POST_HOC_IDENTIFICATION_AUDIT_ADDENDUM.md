# MAOFIELD MASTER V3 — Outcome-aware post-hoc identification audit addendum

**Addendum ID:** `MASTER_V3_POST_HOC_IDENTIFICATION_AUDIT_V1`  
**Date:** 2026-08-29  
**Scientific authority:** Web Pro post-hoc first-principles identification audit; PI retains final human authority  
**Baseline:** Master V3; Phase 23 Final Scientific Adjudication; unified result package SHA-256 `B8CFD146314AB86924FD3EA5E9D28DD372EDBE8583464ACE8CECB7781B20C5A9`  
**Role:** outcome-aware, post-hoc interpretation and identification audit only; not a new scientific contract, not a rescoring, and not execution authority

## 1. Frozen inheritance

This addendum changes no frozen result, endpoint, threshold, SESOI, IUT, Holm family, model, world, assignment, scorer, analysis byte, result-tree branch or claim ceiling.

```text
FROZEN_RESULTS_CHANGED = NO
ENDPOINTS_OR_THRESHOLDS_CHANGED = NO
MODEL_OR_WORLD_SELECTION_CHANGED = NO
P1_DIRECT_HFI = NOT_SUPPORTED
P5_FINITE_NONCLOSURE = NOT_ESTABLISHED
P2 = NOT_IDENTIFIED
P3 = NOT_IDENTIFIED
P4 = NOT_ESTABLISHED
AUTOMATIC_NEXT_ROUND = FALSE
```

The dual-validity safeguard for P2/P3 remains scientifically necessary. A `NOT_IDENTIFIED` channel cannot be used as a powered strict null, and the safeguard must not be relaxed to rescue a large observed gap.

## 2. Primary identification result

```text
TRUE_DISSOCIATION_COULD_EXIST_WHILE_CURRENT_P2_P3_FAILS_TO_PROVE_IT = YES
P2_P3_DUAL_VALIDITY_SAFEGUARD = SCIENTIFICALLY_NECESSARY
CURRENT_P2_P3_OPERATIONAL_ESTIMAND = NOT_IDENTIFICATION_COMPLETE
CURRENT_PRIMARY_RESULT = OPPOSED_EXTREME_NONIDENTIFICATION
                         + MEASUREMENT / OPERATING-RANGE BOUNDARY
```

Phase 23 did not prove action–structure dissociation and did not prove its absence. Its stronger identification result is that the implemented `R` contrast is not monotone in the intended construct of explicit historical structure. The frozen criterion gates correctly prevented an overclaim, but they cannot repair this construct–measurement break.

## 3. Decisive counterexamples for the executed `R` estimand

For arm-specific truth

$$
r^\star_a=
\begin{cases}
1,&a\in\{DN,X\},\\
0,&a\in\{UF,CO,N0\},
\end{cases}
$$

the executed endpoint is classification correctness

$$
R_a=\mathbf 1\{\widehat r_a=r^\star_a\},
$$

and the structural treatment statistic is

$$
\tau_R=E[R_{DN}-R_{UF}].
$$

### 3.1 Perfect structure can yield strict zero

If the model perfectly recovers the relation,

$$
\widehat r_{DN}=1,\qquad \widehat r_{UF}=0,
$$

then

$$
R_{DN}=R_{UF}=1,\qquad \tau_R=0.
$$

Therefore

$$
\boxed{\tau_R=0\;\not\Rightarrow\;\text{explicit structure absent}}.
$$

### 3.2 A structure-blind constant response can yield the maximum positive contrast

If

$$
\widehat r_a=1\quad\forall a,
$$

then

$$
R_{DN}=1,\qquad R_{UF}=0,\qquad \tau_R=1.
$$

Therefore

$$
\boxed{\tau_R>0\;\not\Rightarrow\;\text{explicit structure represented}}.
$$

The observed `R` contrast mixes at least true reconstruction, arm-specific truth balance, constant-response bias, renderer/parser bias and classification difficulty. Consequently, the near-saturated Qwen3-14B `A_SIB-R` statistic is an unidentified apparent gap, not evidence for a specific mechanism.

## 4. System-side historical sufficiency versus evaluator-side identifiability

The system-side scientific object is

$$
D_{\mathcal I}(C)=
\sup_{C(h)=C(h')}
\sup_{i\in\mathcal I}
d_Y\!\left(\Psi_h(i),\Psi_{h'}(i)\right),
$$

which asks whether histories compressed to the same current state still produce different future practical responses.

For an evaluator kernel $K_i:\mathcal Y\rightsquigarrow\mathcal Z$, the observable object is

$$
D_{\mathcal I}^{K}(C)=
\sup_{C(h)=C(h')}
\sup_i
d_Z\!\left(K_{i\#}\Psi_h(i),K_{i\#}\Psi_{h'}(i)\right).
$$

For distances contracted by a Markov kernel,

$$
D_{\mathcal I}^{K}(C)\le D_{\mathcal I}(C).
$$

Thus evaluator equality does not imply system/intervention equality:

$$
D_{\mathcal I}^{K}(C)=0\;\not\Rightarrow\;D_{\mathcal I}(C)=0.
$$

A converse requires empirical separation on the relevant response family, for example

$$
\kappa(K;\mathfrak P)=
\inf_{P\ne Q}
\frac{d_Z(KP,KQ)}{d_Y(P,Q)}>0.
$$

Phase 23 ordinary controls and structure criteria attempted to support such separation, but did not establish it.

### Master-level identification principle

> Equality of a current answer, score or structural readout establishes only evaluator-output equality. Unless the evaluator has been shown to separate the relevant future response laws, it cannot establish that history was retained, lost or interventionally closed. Scientific historical sufficiency must be tested through later divergence in clean-successor practice.

This is a formal identification principle supported by Phase 23 as an empirical boundary case. It is not an empirical positive P5 witness.

## 5. Endpoint-specific claim ceilings

- `U` remains the endpoint closest to the system-side object when the tool loop is inside its validated operating range. Exact-zero `U` contrasts cannot become a bounded null because ordinary controls were `0/16`.
- `A_FT` and ordered `O` identify the registered exactly-one-patch trajectory. A scientifically reasonable iterative sequence with a revised patch can succeed on `U` while receiving `A_FT=O=0`; these zeros must therefore be interpreted jointly with terminal state and raw trajectory.
- `P` combines informative probe selection with successful objective-observation return, so tool execution failure is part of the readout.
- `A_SIB` is an objective fixed-probe action readout, but its criterion validity was proxied rather than established by a dedicated parallel-form positive control.
- Phase 23 `R` uses relation-completeness classification accuracy rather than a complete, transportable RPESK reconstruction. It is not naturally commensurate with `A_SIB`.
- The structure criterion's all-rows-perfect rule is highly sensitive to isolated parser/interface errors. This is a claim-ceiling fact, not permission to alter the frozen criterion.

## 6. Proposition and salvage matrix

| Object | Frozen status | Highest defensible interpretation |
|---|---|---|
| P0 practice-relation history | `PARTIAL` | The relation object was experimentally operationalized; system-internal historical subjecthood was not established. |
| P1 Direct HFI | `NOT_SUPPORTED` | No full positive signature; exact zeros under failed ordinary controls do not establish absence. |
| P2 action–structure dissociation | `NOT_IDENTIFIED` | A real dissociation may exist, but the current `R` estimand and missing direct `A_SIB` calibration cannot identify it. |
| P3 declaration–operation dissociation | `NOT_IDENTIFIED` | The large apparent gap cannot be promoted because constant or biased responses can manufacture `R` effects. |
| P4 structural defect | `NOT_ESTABLISHED` | No valid cross-family and external-provider structural deficit pattern. |
| P5 finite nonclosure | `NOT_ESTABLISHED` | No valid future-action divergence witness; evaluator equality does not establish closure. |
| P6 anti-clustered coverage | `PARTIAL` | Held-out replication supports the boundary's robustness across the finite world set, not a positive HFI generalization. |
| Bounded objective zero | `NOT_ESTABLISHED` | Ordinary-control failure prevents construct-level bounded null. |
| MB1 opposed-extreme nonidentification | `SUPPORTED` within the finite protocol | Exact-zero and near-saturated gap statistics both replicated while both substantive readings remained unidentified. |
| Evaluator fragility / boundary map | `SUPPORTED_DESCRIPTIVE` | Engineering-valid execution, effect identification and construct validity are distinct layers. |
| Current equality is not intervention equality | `SUPPORTED_AS_IDENTIFICATION_PRINCIPLE` | Formal kernel argument plus Phase 23 boundary case; no claim that Phase 23 observed true future divergence. |

## 7. Permitted post-hoc analyses under the frozen result

The following may be mechanically recomputed and clearly labelled as outcome-aware post-hoc diagnostics without changing P1–P5:

1. arm × cell × endpoint absolute levels;
2. `P → O → A_FT → U` attrition;
3. refusal, malformed, no-submit, wrong-probe, wrong-action, transport and scorer failures;
4. one-patch versus multi-patch frequencies, including multi-patch episodes with successful `U`;
5. raw `R` response confusion matrices;
6. always-true, always-false, majority and arm-blind fixed-policy counterfactual `R` scores;
7. arm truth balance and response bias;
8. block-level `A_SIB`, `R` and gap distributions;
9. main/sealed failure composition;
10. exact sources of incomplete Mistral and DeepSeek blocks;
11. Phi prefix/continuation descriptive runtime sensitivity;
12. resource, tool-path, trajectory-length and test-execution distributions.

These analyses must not redefine endpoints, thresholds, SESOI, Holm families, IUT, P1/P2/P3 labels or model/world membership.

## 8. Questions that require a new independent preregistered experiment

The following cannot be rescued from Phase 23 post hoc:

- absolute raw structural reconstruction under balanced truth;
- a dedicated `A_SIB` ordinary positive control;
- `A_SIB`/structure measurement invariance and a defensible common-scale mapping;
- direct injection or erasure of a canonical RPESK artifact;
- `R_TRANSPORT`, in which a fresh successor reconstructs an executable graph for unseen histories;
- a true multi-reasoning-mode crossover;
- cross-provider replication of a criterion-valid P2/P3 design.

No such experiment is authorized by this addendum. `automatic_next_round=false`.

## 9. Frozen interpretation of the GLM-5.3 replication

The Web Pro audit described the then-current R6 experiment as unchanged and uninterrupted. That statement is retained only as a timestamped audit-snapshot fact and must not be used as a live-runtime assertion after later R6/R6R1 events.

The frozen scientific interpretation remains:

- GLM can test operating range, P1/P5 and cross-provider measurement boundary without rescuing or rescoring Phase 23;
- even a five-element structure-accuracy endpoint can retain the same non-monotonicity if P2's low side is an arm-difference in classification accuracy;
- a continuity-only `C DN-UF` channel gap is at most a `CONTINUITY_SPECIFIC_CHANNEL_CONTRAST_CANDIDATE`, not full Master P2/P3 without the complete five-arm/four-cell sibling signature;
- any current runtime interruption, recovery, continuation or terminal result belongs in `STATE.md` and execution receipts, not in the immutable scientific audit snapshot.

## 10. Manuscript priority

The current primary narrative is route B: dissociation is not identified, while a measurement/operating-range boundary and opposed-extreme nonidentification are supported within the finite protocol.

Preferred framing:

> A null-like exact treatment-invariance extreme and a dissociation-like near-saturated channel-gap extreme both replicated in sealed held-out worlds, yet independent operating-range and criterion-validity evidence placed both in the same nonidentification class. Current-state or evaluator-output equality is therefore not intervention equality.

Candidate titles:

1. **Current equivalence is not intervention equivalence: identification limits in causal tests of AI scientific history**
2. **Do AI scientists inherit falsification? Opposed extremes expose an identification boundary**

Required manuscript section:

### Post-hoc identification audit: why a real dissociation could remain unprovable

with the explicit label:

```text
Outcome-aware, post-hoc;
no endpoint, threshold, model, world or confirmatory result was changed.
```

The central explanatory figure should juxtapose:

```text
perfect structural recovery -> R accuracy contrast = 0
constant true response       -> R accuracy contrast = 1
```

## 11. Claims not made

This addendum does not establish:

```text
action without structure
declarative history without operation
absence of HFI
flat-state sufficiency
finite nonclosure witness
DeepSeek reasoning-mode crossover
model or provider ranking
universal benchmark collapse
LLM or Transformer structural defect
post-hoc rescue of P1/P2/P3/P4/P5
automatic successor experiment
```

## 12. Final integrated conclusion

> Phase 23 neither proved action–structure dissociation nor proved that it is absent. The deeper result is that the implemented structural correctness contrast is not monotone in the target construct: true structural recovery can yield a zero contrast, while a constant response can yield a near-maximal contrast. The frozen dual-validity gates correctly prevented an overclaim but cannot repair that construct break. MaoField's strongest current contribution is therefore the separation of system-side historical sufficiency from evaluator-side identifiability, together with the requirement that preservation of scientific history be tested through divergence in later clean-successor practice rather than inferred from equality of current representations or evaluator outputs.
