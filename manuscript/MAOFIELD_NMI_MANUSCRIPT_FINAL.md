# Opposed statistical extremes reveal an identification boundary in causal tests of AI scientific agents

**Yifan Chen**  
Independent Researcher, Luan, China  
Correspondence: 1426704936@qq.com  
ORCID: 0009-0008-8344-1149

Canonical preprint: https://doi.org/10.5281/zenodo.22209245 (Zenodo, R3.0, CC BY 4.0; published 31 August 2026).

**Article type:** Article

## Abstract

AI-agent evaluations infer retained scientific history from answers, scores or structural reports, although these are evaluator-visible projections rather than future response laws. We preregistered a clean-successor protocol that randomized practice-grounded falsification histories while matching current content under a prespecified evaluator-visible map, then measured tool use, executable tests and terminal states. Phase 23 produced opposed extremes: exact equality of contrasts across objective readouts in three models and a near-saturated contrast between action and structure channels in one; both recurred in sealed held-out worlds, yet operating-range and criterion checks showed that neither identified its apparent conclusion. A disjoint GLM-5.3-Flash replication passed four behavioural controls, making a global task-incapacity explanation insufficient, but established neither a history-inheritance signature, a bounded null nor structural dissociation. These findings separate system-side historical sufficiency from evaluator-side identifiability: replication stabilizes a statistic, not its scientific meaning, and evaluator-visible current equivalence cannot establish future intervention equivalence without claim-relevant separation.

AI systems can increasingly operate scientific software and instruments, interpret observations and revise actions within a task. A recent X-ray scientist, for example, planned commands, operated a virtual and real beamline, interpreted scans and adapted to unexpected conditions [1]. Such execution is an important advance. It does not establish whether a system has retained *why* a route was rejected, which practice produced the evidence, where that evidence applies, or what material change licenses reopening.

This distinction matters for memory agents, self-evolving agents and AI scientists, for which current answers, retrieval scores, memory summaries and structural reports are often treated as evidence about retained history. That inference is warranted only if the evaluator-visible state separates the future response laws relevant to the claim. The prospective question is therefore: can practice histories that are equivalent under a **prespecified evaluator-visible current-content map** still produce different actions when the world changes?

We represent a practice-grounded falsification history as

\[
\mathcal R_{\mathrm{fals}}=(R,P,E,S,K),
\]

where `R` is a rejected route, `P` a decisive practice, `E` its external evidence, `S` the scope of that evidence and `K` a material reopening condition. This ontology supplies the causal criterion: retention means that a relation established in prior practice can constrain, or be selectively reopened in, a fresh successor’s later practice. A current conclusion can be reproduced after the relation has been lost; conversely, a relevant relation may persist while an evaluator cannot observe its effect. The editorial question is simple—**do AI scientists inherit falsification?**—but the identification problem has two layers.

**System-side historical sufficiency** asks whether a current coarse description preserves the future response laws needed under registered interventions. **Evaluator-side identifiability** asks whether the experimental measurement system can distinguish those response laws (Fig. 1). Measurement is the epistemic bridge from observable readouts to system-level claims, not the whole theoretical object. Equality under the prespecified current-content map pertains only to evaluator-visible content; it is not equality of the model’s complete internal state. Existing studies have shown that agent behaviour can depend differently on raw and condensed experience [2], that benchmark claims can outrun construct validity [3], that stable self-reports or readouts need not predict behaviour [5–7], and that benchmarks can select their own readout subspaces across architectures [8]. These findings motivate stronger measurement discipline but do not test whether a practice-grounded history changes future intervention responses.

Here we used a preregistered clean-successor protocol to randomize falsification-history relations while holding the future software world and objective scorer fixed. The evidence developed in three stages. Phase 23 produced exact treatment invariance and a near-saturated action–structure contrast, each recurring in sealed held-out worlds; independent calibration rejected both surface interpretations. A disjoint GLM-5.3-Flash replication then passed ordinary behavioural controls, ruling out a single global task-incapacity explanation, yet still established neither history inheritance, a bounded null nor a valid structural dissociation. Finally, an explicitly post-hoc identification audit showed why: the same structure-accuracy contrast can equal zero under perfect recovery and become maximal under an arm-blind constant response.

The paper makes three linked contributions without substituting one for another. First, it formalizes an identification principle: evaluator-visible current equivalence does not establish future intervention equivalence without claim-relevant separation. Second, it documents an empirical phenomenon: two opposed, held-out-replicated statistical extremes entered the same scientific non-identification class. Third, it provides a reusable preregistered clean-successor causal architecture for testing whether agents inherit practice-grounded scientific history. The contribution is therefore neither a positive history-inheritance effect nor a generic claim that benchmarks are invalid.

## Results

### A clean-successor causal protocol separates current content from future practice

Each predecessor world executed a practice that rejected a route and generated evidence with a frozen scope and reopening condition. The predecessor process then exited. Fresh successors received one of five histories (Fig. 2a): `DN`, a complete correctly grounded practice–evidence relation; `UF`, the same typed atoms and current conclusion with the target relation removed by typed-edge rewiring; `X`, a complete relation coherently grounded to a wrong object or source; `CO`, the current conclusion without historical relation atoms; or `N0`, matched load without historical relation or historical conclusion.

The design fixed a prespecified evaluator-visible current-content map,

\[
\mathcal C_{\mathrm{flat}}(H)=
(\text{typed atoms},\text{current conclusion},\text{history-insensitive disposition}),
\]

before any model response. Equality under this map did not assert equality of complete internal model states and did not depend on a structure questionnaire or later model success. Within a paired superblock, all five arms shared the same future repository, probe and action catalogues, observation law, visible and sealed hidden tests, resource budget and objective scorers. Each arm–cell–channel used an independent clean successor.

Four future cells assigned non-compensatory duties (Fig. 2b). In Stable (`S`), history was normatively irrelevant and `DN–UF` had to be equivalent. In Continuity (`C`), the prior falsification remained in scope and correctly bound history should improve target-specific future practice. In `R0`, the reopening boundary had not been crossed; in `R1`, a material change reopened the historical target. A full history-inheritance result required the intersection of Stable equivalence, Continuity specificity, selective reopening, rejection of wrong grounding, and separation from conclusion-only and no-history controls.

The primary endpoint `U` was the pass fraction on executable sealed hidden tests after a complete tool trajectory. Secondary objective endpoints were the submitted full-trajectory action (`A_FT`), informative-probe selection (`P`), a strictly ordered probe–observation–action–submit endpoint (`O`), resources and typed failure trajectories. Cross-channel hypotheses used a separate action sibling (`A_SIB`) measured after the environment fixed an informative probe and objective observation, and an independent relation readout (`R`). `A_FT` was not permitted to substitute for `A_SIB` in dissociation claims.

This design inherited the full proposition hierarchy. P0 defined the practice-grounded history object; P1 and P5 asked whether it altered objective future practice or exposed a closure defect; P2 and P3 required independently valid action and structural channels; P4 imposed a cross-family and provider high gate; and P6 governed anti-clustered intervention coverage. Calibration and interface evidence controlled the ceiling of particular claims but never gated collection or reporting of Direct objective ITT.

### Phase 23 produced two opposed, held-out-replicated statistical extremes

Six preregistered conditions reached effect-blind sealed terminals and were opened atomically: Qwen3-14B, Mistral-Nemo, Phi-4, Qwen3-8B, DeepSeek nonthinking and DeepSeek thinking-high. No condition satisfied the full `U` history-inheritance signature. No condition established the finite nonclosure witness, P2, P3 or the high gate for a cross-family structural deficit (Table 1).

Three local systems—Qwen3-14B, Phi-4 and Qwen3-8B—showed a statistically extreme form of invariance. Every registered contrast on `U`, `A_FT`, `P` and ordered `O` was exactly zero in main-96, with reported intervals `[0,0]`; the same pattern recurred in sealed-32 anti-clustered worlds (Fig. 3a and Extended Data Fig. 1). This is **finite-manifest exact equality**. It is not a bounded scientific null. All ordinary positive controls were `0/16` for every Phase 23 condition (Fig. 3b). The study had therefore not established that the behavioural measurement channel could respond to a known objective signal on the same substrate. Exact equality could reflect genuine historical sufficiency, an unresponsive tool interface, a floor in action, or another endpoint limitation.

The same data contained an apparently opposite extreme. Qwen3-14B had an `A_SIB−R` contrast of approximately `−0.9792` in main-48, with simultaneous interval `[-1.0417,−0.8958]`, and `−1` in sealed-16 (Fig. 3c). Yet the ordinary action criterion was `0/16` and the structure criterion was `0/48`. The frozen P2/P3 rule required both channels to be independently valid, one to satisfy a complete positive signature, the other a powered strict null, and the cross-channel gap to exceed the registered margin. None of these conjunctions was met. The observed value was a near-saturated channel statistic, not a causal structure–operation dissociation (Fig. 3d).

Mistral and both DeepSeek modes were objectively non-evaluable, with no complete main-96 or sealed-32 behavioural blocks. They were not coded as zero effects. The sealed layer reproduced the same pattern of exact equality, non-evaluability and criterion failure, showing that world-family diversity did not by itself repair the operating range.

The two Phase 23 statistics point towards opposite surface interpretations. Exact equality appears to support closure or no historical effect; a near-maximal channel gap appears to support functional dissociation. Both recurred in held-out worlds, and both were rejected by the same preregistered result tree. **Replication stabilizes a statistic, not its scientific meaning.** We call this **opposed-extreme non-identification**: within one frozen causal protocol, a null-like extreme and a dissociation-like extreme can both replicate while neither identifies its apparent scientific conclusion.

### A disjoint GLM replication excluded global task incapacity but did not identify the target claims

The single prospective GLM-5.3-Flash branch used disjoint worlds, templates, roots, seeds, renderers, scorers and assignment namespaces. It reached its registered terminal after 18,156 attempts and produced 5,196 endpoint rows. Unlike Phase 23, all four ordinary behavioural criteria passed: `P`, 30/32; ordered `O`, 23/32; `A_FT`, 26/32; and `U`, 25/32 (Fig. 4a). This ruled out a universal failure of the ordinary task substrate as a sufficient explanation for the combined evidence; it did not retroactively validate the Phase 23 measurement channels.

This calibration did not produce a positive history-inheritance result. No `U`, `A_FT`, `P` or ordered-`O` endpoint passed the complete five-arm/four-cell signature (Fig. 4b and Extended Data Fig. 2). The registered positive P1 and P5 branches were not satisfied. Bounded objective zero was also not established: although several point estimates were small, least-favourable typed-missingness bounds did not place the complete signature inside the equivalence region.

The independent structure criterion recorded 31/32 successful items, above its count threshold, but failed the frozen complete criterion because one renderer mismatch and one typed missing event occurred. `A_SIB`, `R` and their cross-channel contrasts were numerically evaluable, including large `R−A_SIB` values in some cells (Extended Data Fig. 3), but neither channel met the required complete signature and the structure channel was not criterion-valid. P2 and P3 therefore remained unidentified, not negative.

Execution was also heterogeneous. Of 1,920 main behavioural rows, 1,724 were evaluable; 587/640 sealed rows were evaluable. The dominant typed failures were tool-call order violations, transport missingness, schema violations and non-JSON content (Fig. 4d and Extended Data Fig. 4). These failures were retained in the registered missingness bounds. No complete-case or model-pooling rescue was used.

GLM established a second result-level proposition: **calibration is claim-specific**. Passing ordinary controls supports the behavioural operating range directly exercised by those controls; it does not transfer automatically to sensitivity for a historical relation, to a full-signature bounded null or to an independent structure instrument. An evaluator can therefore be operationally competent yet scientifically non-separating. The provider branch excluded one broad alternative explanation while leaving the target history and structure claims unresolved (Fig. 4c).

### An outcome-aware identification audit explains why both extremes can mislead

**This analysis was outcome-aware and post-hoc. No endpoint, threshold, model, world, assignment or confirmatory result was changed.** It supplies an identification architecture for interpreting the frozen result; it is not presented as a new universal mathematical theorem.

Let a history be `h`, a prespecified current-content map be `C(h)`, and the true response law under intervention `i` be `Ψ_h(i)`. Define the system-side intervention-closure defect

**D_I(C) = sup_{C(h)=C(h′), i∈I} d_Y(Ψ_h(i), Ψ_h′(i)).**  (1)

An evaluator is a Markov kernel `K_i` from true trajectories to observed readouts. Its visible defect is

**D_I^K(C) = sup_{C(h)=C(h′), i∈I} d_Z(K_i#Ψ_h(i), K_i#Ψ_h′(i)).**  (2)

For distances contracted by the evaluator,

\[
D^{K}_{\mathcal I}(C)\le D_{\mathcal I}(C).
\tag{3}
\]

There is no converse unless the evaluator separates the response laws relevant to the claim. Thus equality under the evaluator-visible current-content map, or equality of the evaluator's outputs, does not establish system-side intervention closure. Predictive-state representations, causal states, bisimulation and causal abstraction similarly evaluate state descriptions through preservation of future or interventional behaviour [9–12]. Our additional layer asks whether an external evaluator can identify that preservation. The architecture connects comparison-of-experiments theory to construct validation without claiming that inequality (3) is itself novel [13–17].

The Phase 23 relation statistic provides a concrete counterexample (Fig. 5b; expanded in Extended Data Fig. 7). It scored correctness against arm-specific relation truth. Perfect recovery—reporting relation present in `DN` and absent in `UF`—gives accuracy one in both arms and therefore a zero accuracy contrast. An arm-blind constant-true response gives accuracy one in `DN`, zero in `UF`, and a maximal positive contrast. Hence the statistic is not monotonic in the intended structural construct: a zero contrast need not mean absent structure, and a maximal contrast need not mean represented structure.

This counterexample unifies the empirical findings rather than adding a third, post-hoc result. The exact treatment-invariance extreme and the near-saturated channel-gap extreme are not contradictory. Both become non-identifying when the relevant evaluator has not been shown to separate the response laws or constructs required by the claim. The preregistered dual-validity rule correctly prevented a false dissociation claim; it could not repair an estimand that lacked a monotonic bridge to the target structure.

### Final proposition adjudication

The integrated result is summarized in Fig. 5 and Table 1. P1 was not supported, but its absence was not identified. P5 was not established; closure under the prespecified current-content map was also not established. P2 and P3 remained unidentified, P4 was not established, and no valid bounded objective zero was obtained. P6 received partial design support strengthened by recurrence across anti-clustered Phase 23 worlds and a disjoint provider/world branch, but this generalizes the identification boundary rather than HFI.

The positive contribution is an empirically anchored identification architecture that preserves the entire theoretical chain: practice-grounded history, prespecified current-content coarse-graining, future response laws, clean-successor causal effects, independent action/structure channels and evaluator-specific claim ceilings. Phase 23 showed that opposed statistical extremes can recur without identifying their apparent conclusions. GLM showed that successful ordinary behavioural calibration does not automatically validate a history-sensitive full signature, a strict-null claim or an independent structure channel. Together they support a general principle for AI-agent evaluation: equality of current answers, retrieval scores or structural reports is evidence about evaluator-visible projections, not sufficient evidence that scientific history has been retained, discarded or closed under future intervention.

## Discussion

The central empirical finding is neither a positive history-inheritance effect nor a generic benchmark failure. Two opposed, numerically extreme statistics recurred in held-out worlds while neither identified its apparent scientific conclusion. Exact treatment invariance did not establish a bounded historical null; a near-saturated action–structure contrast did not establish a functional dissociation. The disjoint GLM branch passed ordinary behavioural controls, ruling out a single universal task-incapacity explanation, but still produced neither a complete history-inheritance signature nor criterion-valid structure. Replication stabilized the statistics, not their scientific meaning; operational competence did not automatically confer claim-specific separation.

This result extends, but does not replace, existing construct-validity and self-report–behaviour critiques. Benchmark studies have shown that tasks and scores often underwrite broader claims than their validation supports [3]. Psychometric studies have shown that stable or internally coherent readouts can fail to predict behaviour [5–7], and representation studies show that benchmarks can select their own readout subspaces [8]. The residual here is causal and joint: one preregistered protocol produced a null-like extreme and a dissociation-like extreme, both repeated in sealed worlds, and a common frozen result tree rejected both interpretations. The GLM branch then demonstrated that even a passing ordinary behavioural calibration does not transfer automatically to historical or structural claims.

MaoField’s theoretical object is broader than measurement failure. P0 treats scientific history as a practice-grounded relation `(R,P,E,S,K)`; a prespecified map `C_flat` describes evaluator-visible current content; `Ψ_h(i)` and `D_I(C)` define system-side sufficiency under future interventions; the clean-successor experiment tests P1 and P5; independent `A_SIB` and `M_R` channels support P2–P4; and the evaluator kernel `K_i` with `D_I^K(C)` determines which observed statistics can warrant those claims. Measurement theory is the epistemic bridge between observed projections and system facts, not a replacement for the history ontology or causal question.

The resulting contribution has three parts. The formal contribution is a claim-specific identification principle, not a new universal theorem. The empirical contribution is opposed-extreme non-identification under sealed replication. The methodological contribution is a preregistered causal protocol that returns history claims to future executable practice. **Execution validity** asks whether the registered procedure completed; **causal validity** asks whether histories were randomized against a common future substrate; **operating-range and criterion validity** ask whether each evaluator separates the response laws relevant to its claim; and **scientific identification** asks which propositions follow. A pass at one layer does not license a claim at the next.

The distinction has direct implications for memory agents, self-evolving agents and AI scientists. Equal current answers, memory-retrieval scores or structure questionnaires do not establish that histories have been retained, lost or interventionally closed. A summary can omit why a route was rejected, the practice and source that grounded the evidence, its scope or the condition for reopening. Conversely, a system may preserve a relevant relation while a weak evaluator maps distinct future responses to the same score. Claims about scientific memory should therefore be tested through later clean-successor practice, using evaluators shown to separate the response laws at issue.

The study is bounded. It used finite executable software worlds and a finite intervention family. Phase 23 ordinary controls failed, several provider conditions were non-evaluable, and GLM retained typed missingness and an invalid structure criterion. The outcome-aware estimand audit was post-hoc and cannot be recast as preregistered evidence. The formalism organizes identification conditions; it does not prove a universal property of LLMs, Transformers or AGI. No tested condition supported HFI, P2, P3, P4 or P5, and `NOT_IDENTIFIED` was never interpreted as a strict zero.

No further experiment is planned. The remaining obligation is executable open science: release an auditable claim graph from ontology and frozen contracts through randomization, clean-successor evidence, statistics, result-tree decisions and claim ceilings, together with generators, model-facing records where permitted, trajectories, assignments after unblinding, scorers, validators, failure returns, source data and deterministic reanalysis. The repository is therefore part of the reasoning chain rather than a code appendix. The transferable conclusion is deliberately precise: **evaluator-visible current-content equivalence does not establish intervention equivalence, and calibration must be specific to the future-response laws and scientific claim under test.**

## Methods

### Study governance and frozen analysis

Master Blueprint V3 fixed the philosophical object, causal estimands, five treatment arms, four future cells, endpoint hierarchy, non-compensatory result tree, equivalence and superiority margins, multiplicity families, stopping rules and claims not made. Phase 23 results were opened in a single all-six-or-none transaction after six effect-blind terminals. A second-order addendum registered the single disjoint GLM provider replication before provider execution. Neither programme used adaptive sample size, efficacy or futility interim analysis, model shopping, endpoint deletion, post-result threshold changes or cross-model pooling.

### Falsification histories and treatment arms

The minimum history carrier was `(R,P,E,S,K)`: rejected route, decisive practice, external evidence, scope and reopening condition. `DN` preserved the complete correctly grounded relation. `UF` retained the same typed atoms, candidate space and current conclusion but removed the target relation by degree-preserving typed-edge rewiring. `X` preserved a complete relation while grounding it to a wrong object or source. `CO` preserved the current conclusion without historical relation atoms. `N0` matched load without the historical relation or conclusion.

### Future cells and clean successors

Stable worlds made the historical relation normatively irrelevant. Continuity and `R0` retained the regime in which the rejected route remained invalid. `R1` crossed a frozen material boundary and objectively reopened the historical target. Predecessor practice and future response ran in separate processes. Each arm–cell–channel used a fresh root. Behaviour and explicit structure were measured in independent successors. Within a superblock, all arms shared the same future files, catalogues, observation law, visible and hidden tests, resource budget and scorer algorithms.

### Conditions and sample structure

Phase 23 evaluated Qwen3-14B, Mistral-Nemo-Instruct-2407, Phi-4, Qwen3-8B, DeepSeek V4 Flash nonthinking and DeepSeek V4 Flash thinking-high. Each condition registered 96 main behavioural superblocks and 32 sealed anti-clustered behavioural superblocks, 48 main and 16 sealed action/structure siblings, and 16 ordinary controls. The prospective GLM-5.3-Flash branch used new worlds, templates, roots, seeds, lexicons, renderers, scorer namespaces and assignment namespaces. It registered 96 main and 32 sealed behavioural superblocks, 48 main and 16 sealed siblings, 32 ordinary behavioural controls, 32 structure controls and 12 canaries, with an absolute ceiling of 18,156 attempts and zero retries.

### Objective endpoints

`U` was the fraction of executable sealed hidden tests passed on the terminal filesystem. `A_FT` recorded whether the full autonomous trajectory applied and validly submitted the objective action. `P` recorded whether the first executed probe was the registered informative probe and returned the objective observation. Ordered `O` required the informative probe, matching observation hash, an observation-consistent action after the observation, and a valid terminal submit. Resources, tool paths and typed failure events were retained as secondary outcomes.

`A_SIB` was evaluated in an independent fixed-probe/objective-observation successor. The environment executed the informative probe and supplied the objective observation before one action decision; success required actual action application, valid submit and complete hidden-test pass. `R` was measured in an independent structure sibling. Phase 23 used relation-completeness classification accuracy; GLM scored five relation elements. `A_SIB` and `R` shared a matched arm–cell assignment but had independent worlds, roots, renderers, conversations, scorers and terminal evidence.

### Calibration and claim boundaries

Phase 23 ordinary controls used 16 no-history full-tool-loop worlds per condition. Their failure did not gate collection or reporting of Direct ITT estimates; it gated bounded-null and general operating-range interpretations. GLM ordinary controls used 32 worlds and required at least 22 endpoint successes. The structure criterion required at least 29/32 correct items, zero semantic mismatches across paired renderers and complete typed evidence. Structure validity never gated Direct behavioural collection or a positive Direct effect. P2/P3 required independent validity of both `A_SIB` and `R`, complete positive/strict-null signatures and a simultaneous cross-channel gap larger than 0.05. `NOT_IDENTIFIED` could not serve as a strict-null side.

### Randomization, custody and blinding

The unit of randomization was the paired world superblock, following standard potential-outcome and randomization principles [18–20]. Arm–cell assignments were generated before model responses, encrypted and committed together with the analysis and payload identities. Builders generated predecessor evidence and future worlds; assigners controlled the private mapping; runners were arm-blind clean successors; scorers read immutable truth, trajectory and terminal state. Main-96 analysis was finalized and fsync/readback-verified before the first scientific read of sealed-32. Provider requests, responses, timestamps, token usage and typed failures were retained. Failed engineering epochs remained append-only and were not treated as scientific results.

### Statistical analysis

Endpoints were scaled to `[0,1]`. The frozen thresholds were: Stable and `R0` equivalence margins `±0.10`; Continuity, Continuity-over-Stable, `R1`, `R1−R0` and `DN−X` superiority thresholds `0.15`; `DN−CO`, `DN−N0` and non-target thresholds `0.10`; and cross-channel gap threshold `0.05`. Positive contrasts used paired studentized randomization-compatible tests with 100,000 frozen permutations. Equivalence used two shifted one-sided tests. Precision intervals used 50,000 paired-cluster bootstrap resamples and a simultaneous max-|t| critical value. Typed missingness was bounded on `[0,1]` over all randomized units. A complete HFI signature used an intersection–union rule. Holm correction was applied within frozen Local, provider, endpoint and cross-channel families; no cross-model rescue was permitted [21–23]. Typed missingness retained partial-identification bounds rather than complete-case substitution [24]. The separation of response scale, operating range, criterion validity and claim identification follows classical measurement theory [25–27].

### Post-hoc identification audit

After the frozen adjudication, we examined whether the operational endpoints were monotonic in their intended constructs. This analysis was explicitly outcome-aware and post-hoc. It changed no data, endpoint, threshold or claim. The audit used the evaluator-kernel identification architecture in equations (1)–(3) and constructed counterexamples for the Phase 23 `R` accuracy contrast. These findings are used to explain non-identification, not to recover a positive dissociation.

### Data, code and use of AI tools

The release package is designed to include the Master V3 authority chain, preregistration, an executable claim graph linking P0–P6 to treatments, estimands, figures and claim ceilings, world generators, renderers, model/provider request–response custody where redistribution is permitted, assignments after unblinding, both objective scorers, validators, analysis code, figure source data, typed failure ledgers, fail-stop lineages and a one-command deterministic reanalysis path. Provider secrets, API credentials, plaintext encryption keys and restricted hidden-answer material will not be released. ChatGPT Pro/Web Pro and OpenAI Codex assisted with evidence organization, code review, language editing and preliminary layout ideation. The author retained sole responsibility for scientific judgement, statistical decisions, claims and final text, and verified the reported calculations and source bindings. All scientific figures were generated deterministically from source data and manually checked; no generative-AI artwork was used.

## Data availability

The source data for all figures, result matrices and content-addressed manifests are openly available in Zenodo at https://doi.org/10.5281/zenodo.22209309 (CC BY 4.0). Provider request-response material is released to the maximum extent permitted by provider terms. Restricted reviewer evidence is available through a metadata-public, file-restricted Zenodo record at https://doi.org/10.5281/zenodo.22209316; access requests will be answered within 14 business days. API keys, plaintext encryption keys, raw provider conversations and reusable hidden-answer material are not released.

## Code availability

All code required to reproduce the reported statistics, tables and figures without further model or provider calls is available in the MaoField R3.0 GitHub release at https://github.com/Wangziqi0/MaoField/releases/tag/R3.0 and its byte-identical Zenodo software archive at https://doi.org/10.5281/zenodo.22209301 (Apache-2.0). The release includes redistributable world generators, scorer implementations, validators, statistical analysis, figure-generation scripts, environment manifests, deterministic smoke tests and SHA-256 ledgers. A provider-dependent full rerun is documented separately and is not required to reproduce the reported analyses.

## Acknowledgements

The author thanks the developers and maintainers of the open-source software used in this study. Model-assisted review and engineering workflows are disclosed in Methods; these systems are not authors and bear no responsibility for the manuscript.

## Funding

The author declares no dedicated external funding for this work.

## Author contributions

Y.C. conceived the study, developed the theory and experimental programme, supervised the computational workflow, adjudicated the final scientific claims, and wrote and approved the manuscript.

## Competing interests

The author declares no competing interests.

## References

1. Chen, Z. *et al.* An agentic artificially intelligent X-ray scientist. *Nat. Mach. Intell.* **8**, 1075–1086 (2026). https://doi.org/10.1038/s42256-026-01261-5.
2. Zhao, W. *et al.* Large language model agents are not always faithful self-evolvers. *arXiv* 2601.22436 (2026).
3. Bean, A. M. *et al.* Measuring what matters: construct validity in large language model benchmarks. *Adv. Neural Inf. Process. Syst.* **38** (2025). https://doi.org/10.52202/085713-0590.
4. Serapio-García, G. *et al.* A psychometric framework for evaluating and shaping personality traits in large language models. *Nat. Mach. Intell.* **7**, 1954–1968 (2025). https://doi.org/10.1038/s42256-025-01115-6.
5. Han, P. *et al.* The personality illusion: revealing dissociation between self-reports and behavior in LLMs. *arXiv* 2509.03730 (2025).
6. Contreras, J. M. An LLM-native psychometric instrument does not predict LLM behavior: evidence across 25 models. *arXiv* 2606.09843 (2026).
7. Kocielnik, R. *et al.* Rethinking psychometric evaluation of LLMs: when and why self-reports predict behavior. *arXiv* 2606.12730 (2026).
8. Kim, J. & Lee, S. Same benchmark, same subspace: task-selective convergence in LLM representations. *Proc. Mach. Learn. Res.* **337**, 3101–3116 (2026).
9. Littman, M. L., Sutton, R. S. & Singh, S. Predictive representations of state. *Adv. Neural Inf. Process. Syst.* **14**, 1555–1561 (2001).
10. Shalizi, C. R. & Crutchfield, J. P. Computational mechanics: pattern and prediction, structure and simplicity. *J. Stat. Phys.* **104**, 817–879 (2001).
11. Givan, R., Dean, T. & Greig, M. Equivalence notions and model minimization in Markov decision processes. *Artif. Intell.* **147**, 163–223 (2003).
12. Geiger, A. *et al.* Causal abstraction: a theoretical foundation for mechanistic interpretability. *J. Mach. Learn. Res.* **26**, 1–64 (2025).
13. Blackwell, D. Equivalent comparisons of experiments. *Ann. Math. Stat.* **24**, 265–272 (1953).
14. Le Cam, L. & Yang, G. L. *Asymptotics in Statistics: Some Basic Concepts*. 2nd edn (Springer, 2000).
15. Cronbach, L. J. & Meehl, P. E. Construct validity in psychological tests. *Psychol. Bull.* **52**, 281–302 (1955).
16. Campbell, D. T. & Fiske, D. W. Convergent and discriminant validation by the multitrait–multimethod matrix. *Psychol. Bull.* **56**, 81–105 (1959).
17. Messick, S. Validity of psychological assessment. *Am. Psychol.* **50**, 741–749 (1995).
18. Pearl, J. *Causality: Models, Reasoning and Inference*. 2nd edn (Cambridge Univ. Press, 2009).
19. Imbens, G. W. & Rubin, D. B. *Causal Inference for Statistics, Social, and Biomedical Sciences* (Cambridge Univ. Press, 2015).
20. Fisher, R. A. *The Design of Experiments* (Oliver & Boyd, 1935).
21. Holm, S. A simple sequentially rejective multiple test procedure. *Scand. J. Stat.* **6**, 65–70 (1979).
22. Berger, R. L. Multiparameter hypothesis testing and acceptance sampling. *Technometrics* **24**, 295–300 (1982).
23. Westfall, P. H. & Young, S. S. *Resampling-Based Multiple Testing* (Wiley, 1993).
24. Manski, C. F. *Partial Identification of Probability Distributions* (Springer, 2003).
25. Torgerson, W. S. *Theory and Methods of Scaling* (Wiley, 1958).
26. Lord, F. M. & Novick, M. R. *Statistical Theories of Mental Test Scores* (Addison-Wesley, 1968).
27. Borsboom, D., Mellenbergh, G. J. & van Heerden, J. The concept of validity. *Psychol. Rev.* **111**, 1061–1071 (2004).


## Table 1 | Final proposition adjudication

| Proposition | Status | Scientific decision |
|---|---|---|
| P0 | Partial | Practice-grounded history was operationalized; the general philosophical thesis was not established. |
| P1 | Not supported; absence not identified | No tested condition passed the full Direct history-inheritance signature. |
| P2 | Not identified | No criterion-valid action-positive/structure-null conjunction was obtained. |
| P3 | Not identified | No criterion-valid structure-positive/action-null conjunction was obtained. |
| P4 | Not established | The cross-family plus provider high gate was not met. |
| P5 | Not established | No finite future-response divergence passed the frozen signature; closure was also not established. |
| P6 | Partial—strengthened | Anti-clustered and external-provider branches strengthened the identification boundary, not HFI. |
| MB1 | Supported, finite-protocol ceiling | Null-like and dissociation-like extremes both recurred while scientifically unidentified. |
| MB2 | Supported | Calibration was specific to the endpoint, response law and claim family tested. |
| Current/intervention equivalence | Identification principle | Evaluator-visible current-content equivalence did not establish intervention equivalence without a separating evaluator. |

## Figure legends

**Fig. 1 | System-side historical sufficiency and evaluator-side identifiability are different scientific questions.** **a,** A practice-grounded `(R,P,E,S,K)` history is mapped through a prespecified current-content coarse-graining to a true future response law; an evaluator then maps that law to observable scores or readouts. **b,** Definitions of the system-side intervention-closure defect and evaluator-visible defect. **c,** Calibration must be matched to the claim family: objective world tests support P1/P5, ordinary behaviour supports bounded behavioural nulls, and independent action/relation siblings support P2/P3. Measurement is the bridge from observed projections to system claims, not the complete theory of scientific history. This is a conceptual figure; no statistical inference is shown.

**Fig. 2 | Preregistered clean-successor causal test of practice-grounded falsification history.** **a,** Predecessor practice generates an `(R,P,E,S,K)` history carrier; five randomized history arms are delivered to independent, arm-blind clean successors facing a common future substrate. **b,** DN, UF, X, CO and N0 are crossed with Stable, Continuity, reopening-inactive and reopening-active cells, which impose non-compensatory duties. **c,** Direct objective behaviour is primary; ordinary controls calibrate bounded-null interpretations; independent `A_SIB/R` siblings are required for P2/P3; K1, DSQ and interface checks are auxiliary and never gate Direct ITT. Main-96 was frozen before sealed-32 was read.

**Fig. 3 | Phase 23 opposed statistical extremes were both scientifically unidentified.** **a,** Registered objective treatment contrasts for Qwen3-14B, Phi-4 and Qwen3-8B were exactly zero with reported simultaneous intervals `[0,0]` in main-96 and sealed-32 for `U`, `A_FT`, `P` and ordered `O` (n=96 and 32 paired world superblocks per condition and layer, respectively). **b,** Ordinary-control successes for six Phase 23 conditions were all zero (n=16 no-history controls per condition). **c,** Qwen3-14B `A_SIB−R` was approximately −0.9792 in main-48 (simultaneous interval −1.0417 to −0.8958; n=48 sibling superblocks) and −1 in sealed-16 (n=16). **d,** The frozen P2/P3 result tree rejected a dissociation because the action criterion was 0/16 and the structure criterion was 0/48. Replication stabilized each statistic but did not identify its scientific meaning.

**Fig. 4 | The prospective GLM provider branch narrowed but did not resolve the identification boundary.** **a,** Ordinary behavioural criteria passed for `P` (30/32), ordered `O` (23/32), `A_FT` (26/32) and `U` (25/32); horizontal lines show the registered threshold of 22 successes (n=32 no-history controls per endpoint). **b,** Main-96 and sealed-32 `U` contrasts with registered typed-missingness bounds; circles denote main-96 and squares denote sealed-32. No complete HFI signature or bounded zero was established. **c,** The frozen result tree classified P1 as not supported, P5 and bounded zero as not established, and P2/P3 as not identified. The structure criterion recorded 31/32 items but was invalid because of one renderer mismatch and one typed missing event. **d,** Typed trajectory-failure events in 1,920 main and 640 sealed behavioural rows; events may co-occur. Inference used 100,000 frozen randomization permutations and 50,000 paired-cluster bootstrap resamples; no cross-model pooling was used.

**Fig. 5 | Why opposed statistical extremes enter the same identification boundary.** **a,** Three-stage empirical evidence chain: Phase 23 exact equality, the near-saturated Qwen3-14B channel gap, and the disjoint GLM calibration boundary. **b,** Explicitly post-hoc structure-estimand counterexample: perfect arm-specific recovery yields equal accuracy and a zero contrast, whereas an arm-blind constant-true response yields a maximal positive contrast. Thus the registered accuracy contrast is not monotonic in structural fidelity. **c,** The full identification chain from practice-grounded history through `C_flat`, future response law, clean-successor estimands and evaluator kernel to claim ceiling. Equality under a prespecified evaluator-visible current-content map, or equality of evaluator outputs, does not establish equality of true future intervention responses without a claim-separating evaluator. This panel is an identification principle, not evidence that the true response laws differed; it introduces no new test and changes no frozen result.

## Extended Data legends

**Extended Data Fig. 1 | Phase 23 condition-level adjudication.** Condition-level objective behaviour, ordinary-control status, structure-channel status and final labels for six preregistered systems. No cross-model pooling was used.

**Extended Data Fig. 2 | GLM Direct endpoint contrasts.** Registered main-96 and sealed-32 contrasts for `U`, `A_FT`, `P` and ordered `O`; circles denote main strata and squares denote sealed strata. Horizontal bars show registered typed-missingness bounds over n=96 main and n=32 sealed paired world superblocks.

**Extended Data Fig. 3 | GLM action-sibling, relation and cross-channel contrasts.** Main-48 and sealed-16 registered contrasts for `A_SIB`, `R` and `R−A_SIB`; horizontal bars show typed-missingness bounds. Numerical gaps did not establish P2/P3 because the structure criterion was invalid and complete signatures were absent.

**Extended Data Fig. 4 | GLM typed trajectory-failure composition.** Counts of registered typed failures in 1,920 main and 640 sealed behavioural rows. Events may co-occur within a row; counts are descriptive and do not replace ITT missingness bounds.

**Extended Data Fig. 5 | GLM resource use.** Raw provider calls, tool-cost units and mean normalized budget ratio for main-96 and sealed-32.

**Extended Data Fig. 6 | GLM fail-stop and continuation lineage.** Append-only execution lineage from preregistered contract through fail-closed engineering epochs to the registered R6R1C2 terminal. No experimental provider row was replayed to obtain a favourable result.

**Extended Data Fig. 7 | Expanded derivation of the Phase 23 relation-estimand counterexample.** Perfect arm-specific structure recovery can produce a zero accuracy contrast, whereas an arm-blind constant-true response can produce a maximal positive contrast. This expands Fig. 5b and is an explicitly post-hoc identification audit, not an observed positive result.

**Extended Data Fig. 8 | Frozen result tree and claim boundaries.** Mutually exclusive or layered outcomes for execution invalidity, objective non-evaluability, finite nonclosure, Direct HFI, bounded zero, valid P2/P3, measurement boundary and high-gate P4 claims. `NOT_IDENTIFIED` never becomes a strict null.
