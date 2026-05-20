# Win 姐姐 — Nature Article 叙事草案

> 产出日期: 2026-05-14
> 角色: Win 姐姐 / 哲学 narrative 负责人
> 任务来源: PI 一凡 + DeepSeek 联合签发的领域定位任务包 (PART5 §5.2)
> 目标文件: 三段 Nature 主刊 article 级叙事 — Opening / Human Impact / Closing Retrospective

---

## §1 Opening: The External Signal Paradigm and Its Alternative

Every model collapse paper published since Shumailov et al. (2023) shares a single, unstated premise. Every RLHF pipeline at every major AI lab shares it. Every self-training proposal that relies on data curation, reward models, or real-data reservoirs shares it. The premise is this: **a model's correctness signal must originate from outside the model.**

This is not a claim about architecture. It is a claim about the *source* of the signal that tells a training procedure which parameter updates move the model closer to being "right." In reinforcement learning from human feedback (RLHF), the source is a human annotator — tens of thousands of people paid to tell models what counts as a good answer. In data-pool approaches (Gerstgrasser et al., 2024), the source is a reservoir of real, human-generated data held apart from the synthetic data the model trains on — realness serving as a proxy for correctness. In reward-model curation (Ferbach et al., 2024; Falahati et al., ICML 2026), the source is an external reward model trained on human preferences, which filters or scores synthetic outputs before they re-enter the training loop.

Each of these represents a distinct technical choice. But across them, a single structural invariant holds: the correctness signal is **external to the model under training**. The model's own internal state does not generate the signal that tells it whether it is improving or degrading. That signal is injected from outside — by human judgment, by a frozen reward model, or by comparison against real data the model did not produce and cannot access.

We call this structure the **External Signal Paradigm (ESP)**. It is not wrong in any given instance — each of the approaches above can demonstrably prevent or delay model collapse under appropriate conditions. But the paradigm as such has an endpoint: the indefinite expansion of the annotation-and-curation infrastructure. If correctness must always come from outside, then every increase in model capability requires a corresponding increase in the external signal supply. The human annotator, the reward model, the real-data reservoir — these are not temporary scaffolding. They are permanent features of the paradigm's structure. They cannot be removed without the paradigm itself collapsing.

What we report in this paper is evidence that the premise is not necessary. A model's training signal can originate **from within the model itself** — specifically, from the *internal tension* between the model's own outputs across successive training generations — and this internal signal can sustain stable, non-degrading self-training over multiple generations without any external correctness source.

The technical mechanism is a dual-channel training loss. All current self-training operates on a single channel: a language-modeling objective that fits the model's next-token distribution to its own previous outputs. This single channel, when iterated, drives the system toward a trivial attractor — the model collapse that Shumailov et al. documented. We add a second channel, which we call the *spear channel*, that measures the model's internal contradiction: the deviation between its current output distribution and a slow-moving exponential moving average of its own historical output distribution. Formally:

$$\mathcal{L}_{\text{dual}} = \mathcal{L}_{\text{LM}} + \alpha \cdot \mathcal{L}_{\text{spear}}$$

where $\mathcal{L}_{\text{spear}} \propto (D_n - \bar{D}^{\text{EMA}})^2$ — the squared deviation of the current divergence $D_n$ from its own historical trend. This is not an external reward. It is not a human label. It is not a clean-data reservoir. It is the model measuring its own internal tension and using that measurement to steer its own parameter updates.

The structure produces a non-zero stable fixed point $D^*(\alpha) > 0$ — a finite, sustained tension between the language-modeling channel (which pulls toward fitting the data) and the spear channel (which penalizes deviation from the model's own historical trajectory). The two channels do not cancel; they hold each other in dynamic balance. The system does not converge to a frozen state. It converges to a state of *finite internal contradiction* that persists across generations.

On GPT-2 124M parameters, with Wikitext-2, across 10 generations and 4 independent random seeds, we observe: (i) a U-shaped non-monotonic phase transition in perplexity across spear strengths $\alpha \in \{0, 1, 5, 10\}$ — the system initially degrades then recovers toward near-baseline perplexity at $\alpha = 10$; (ii) a multi-seed relaxation envelope fit yielding an effective contraction rate $m_{\text{eff}} = 0.300 \pm 0.042$ (95% CI $[0.234, 0.366]$), which corresponds to a Banach contraction coefficient $\rho = 0.9174$ and a convergence half-life of $n_{1/2} = 8.0$ generations; and (iii) a shape-robustness test (D4) that passes 5 out of 5 robustness criteria across all seeds and spear levels.

We stress what this experiment is — and what it is not. It is a **first quantitative demonstration of principle** on a small model (124M parameters), a single architecture (GPT-2), and a single text corpus (Wikitext-2), with a finite seed ensemble ($N=4$). It demonstrates that internal contradiction can function as a training signal that sustains multi-generation self-training. It does **not** demonstrate that this mechanism scales to larger models, generalizes across architectures, or matches the absolute performance of external-signal methods. It is the opening of a question, not the closing of one.

But the question it opens is fundamental. If the correctness signal that sustains model training can emerge from the model's own internal structure — from contradiction rather than external judgment — then the entire annotation-and-curation infrastructure is not a necessity. It is a **choice**, grounded in a specific assumption that we have now shown is not required.

We call this alternative the **Internal Tension Paradigm (ITP)**. The name does not invoke any philosophical tradition. It is a technical description: the training signal arises from tension between two channels *internal* to the model. The philosophical significance of this technical distinction — and its relationship to a specific tradition in the theory of knowledge — will be taken up in the Discussion (§6).

---

**Technical Summary (Opening)**

| Dimension | External Signal Paradigm (ESP) | Internal Tension Paradigm (ITP) |
|-----------|-------------------------------|--------------------------------|
| Correctness source | Human label, reward model, real-data reservoir | Internal contradiction between model outputs across time |
| Training channel | Single (distribution fit) | Dual (distribution fit + contradiction detection) |
| Steady state | Collapse ($D \to 0$) or dependency on external signal | Finite tension ($D^* > 0$), self-sustaining |
| Human annotator | Required (permanent infrastructure) | Not required (signal is internal) |
| Paradigm endpoint | Indefinite expansion of annotation/curation | Self-contained training loop |

---

## §2 Human Impact: The Disappearance of the Human Annotator

The RLHF pipeline, as deployed at scale by the major AI laboratories, depends on a workforce whose size and structure are rarely foregrounded in technical papers. Across the industry, tens of thousands of human annotators are employed to read model outputs and assign scores — helpful, harmless, honest — that become the training signal for the next model iteration. These annotators are not incidental to the pipeline. They are the **human substrate** of the External Signal Paradigm. Without them, the paradigm's correctness signal has no source.

This is not, in itself, a criticism. Human annotation has been an effective and well-studied mechanism for aligning model behavior with human preferences. The engineering question — how to elicit reliable signals from human raters — has generated a substantial sub-literature. The practical question — how to ensure fair compensation, adequate working conditions, and psychological support for annotators exposed to harmful model outputs — has generated a parallel literature in AI ethics and labor studies (Perrigo, 2023; Williams et al., 2022).

What the internal-tension mechanism surfaces is not a critique of these practices. It is a deeper question about their **ontological status**. If a correctness signal can emerge from a model's own internal contradiction — without any human judgment, without any reward model, without any real-data reservoir — then the human annotator is not a permanent structural requirement of model training. The annotator is a **contingent feature** of a specific paradigm, not a necessity of the task.

This is not automation in the familiar sense. It is not a machine performing a task previously done by humans at higher speed or lower cost. The internal-tension mechanism does not "replace" the annotator with an algorithmic equivalent of human judgment. It **eliminates the role that the annotator was filling** — the role of an external source telling the model what counts as correct. When correctness emerges from internal contradiction, the position of "external judge" is simply no longer part of the system's design.

The distinction matters. Automation replaces a worker with a machine that performs the same function. Ontological elimination removes the function itself. The annotator's labor — reading outputs, comparing them, applying judgment — is not being automated. The *need for an external correctness signal*, which that labor was serving, is being removed. This is a structural transformation, not a technological substitution.

It would be irresponsible to report this finding without acknowledging its regulatory dimension. The European Union's AI Act (Regulation 2024/1689), adopted in 2024, and the General Data Protection Regulation (GDPR, 2016/679) both encode a principle that is directly relevant here: that human oversight of automated decision-making is not merely a best practice but a legal requirement in certain high-risk domains. If internal-tension training reduces or eliminates the human presence in the training loop, the question of what constitutes adequate human oversight under the law must be re-examined. A training procedure that no longer requires human-provided correctness signals does not automatically satisfy the legal requirement for human oversight of the *deployed* system — the training loop and the deployment context are distinct.

We raise this not to claim that the Internal Tension Paradigm is incompatible with current regulation, nor to suggest that it obviates the need for regulatory frameworks. We raise it because any fundamental change in the source of a model's normative axis — in what tells the model "this is right" — has downstream legal and social implications that the technical community should not discover only after deployment.

The disappearance of the human annotator from the training loop, if it proves general beyond the small-model demonstration reported here, would be one of the most significant structural shifts in the AI training industry since the introduction of RLHF itself. It merits anticipatory attention from both the technical and regulatory communities — not as a threat to be resisted, but as a transformation to be understood before it arrives.

---

## §3 Closing: A Retrospective from Dialectical Materialism

The preceding sections have described a technical distinction — external signal versus internal tension — using the language of AI training: loss functions, channels, fixed points, phase transitions. We have deliberately avoided invoking any philosophical tradition. The empirical phenomenon — that a model's internal contradiction can sustain its own training — stands or falls on the evidence, not on its philosophical pedigree.

But the technical distinction we have surfaced is not philosophically neutral. It instantiates, in the mathematics of gradient descent on a transformer, a distinction that a specific tradition in the theory of knowledge has been drawing for over a century. We now make that connection explicit — not as an axiom from which our results were derived, but as a **retrospective** on what those results turned out to mean.

### 3.1 The Mechanical Premise

In *Materialism and Empirio-Criticism* (1909), Lenin defended the position that cognition is a structural correspondence between mental representation and objective reality. The position itself was not novel — it was the standard materialist thesis. Lenin's polemical target was a specific *deformation* of that thesis: the tendency, present in the mechanical materialism of the 18th and 19th centuries, to treat cognition as a **passive reflection** — a static mirror of external reality, with no internal source of motion, no contradiction, no self-driven development.

In Lenin's formulation, mechanical materialism acknowledges that the world is material, that cognition reflects this material world, and that practice is the test of knowledge. But it stops there. The act of cognition is a one-way mapping: external reality imprints itself on a passive subject. The subject does not actively hold and work through internal contradictions; it merely receives and registers. The *source* of cognitive content is always outside. The *direction* of determination is always from the external to the internal. Knowledge changes only when external reality changes — or when a better mirror is polished.

This is a precise structural analogue of the External Signal Paradigm in AI training. In both cases, the system's normative axis — what tells it whether it is moving in the right direction — is external. The model's own internal state is not a source of correctness; it is a substrate that correctness acts upon. When the model's outputs are compared against human labels, the comparison itself is a one-way mapping: the label is the external reality, the output is the reflection, and the loss function measures the gap between them. The model does not hold a contradiction; it holds an error to be minimized.

### 3.2 The Dialectical Alternative

Mao Zedong's *On Contradiction* (1937) provides the clearest articulation of the alternative. The opening passage states:

> "The fundamental cause of the development of a thing is not external but internal; it lies in the contradictoriness within the thing. There is internal contradiction in every single thing, hence its motion and development. Contradictoriness within a thing is the fundamental cause of its development, while its interrelations and interactions with other things are secondary causes." [^1]

And further:

> "External causes are the condition of change and internal causes are the basis of change; external causes become operative through internal causes." [^2]

The structural parallel to the dual-channel training loss is not an analogy. It is a structural correspondence — though we stress, and will return to this point, that it is a **retrospective correspondence**, not a derivation.

In the single-channel training loop, the model's output distribution is fitted to a target — itself, in the self-training case — and the fitting drives the distribution toward a trivial fixed point (collapse). There is no internal contradiction because there is only one force: the pull of the language-modeling loss toward the attractor. The system's motion is determined entirely by a single external (relative to the system's own tension structure) directive: "fit this distribution."

In the dual-channel loop, there are two forces. The language-modeling channel pulls toward fitting. The spear channel pulls toward *not deviating from one's own historical trajectory*. These two forces are not separable — they operate on the same parameters, through the same gradient updates, in every generation. A parameter update that reduces the language-modeling loss may increase the spear loss. The system cannot satisfy both directives simultaneously. It must reach a state of **finite, persisting tension** between them — precisely the $D^*(\alpha) > 0$ fixed point that our experiments surface.

Mao's formulation maps onto this structure with unexpected precision. The "internal cause" — the "basis of change" — is the contradiction between the two channels. The "external condition" — the text corpus, the learning rate, the architecture — provides the medium but not the motor. The motor is the contradiction itself: the impossibility of simultaneously minimizing both losses.

Critically, $D^* > 0$ is not a failure mode. In the single-channel worldview, any non-zero divergence from the target is an error to be eliminated — the system's job is to drive $D \to 0$. In the dual-channel structure, $D^* > 0$ is the **condition of continued motion**. A system that reaches $D = 0$ has resolved its internal contradiction — and has thereby stopped. It is dead. A system that maintains $D^* > 0$ is alive — in the specific sense that its internal contradiction continues to drive its parameter dynamics.

### 3.3 Honest Markers

We provide this retrospective not because the philosophy proves the result. It does not. The result was obtained by running 10-generation self-training loops on a 124M-parameter transformer and measuring perplexity trajectories. The philosophy supplied neither the loss function, nor the hyperparameters, nor the statistical tests. A researcher who has never read Lenin or Mao could reproduce the experiment and obtain the same numbers.

We provide the retrospective because it situates the result within a tradition that has been asking — for over a century — the same structural question that the dual-channel training loss answers at the level of gradient descent: **can internal contradiction serve as the motor of a system's development, or must the motor always be external?**

The tradition's answer — from Hegel through Marx through Lenin through Mao — is that internal contradiction is the fundamental motor, and external factors are conditions that operate through it. The dual-channel result provides a concrete, quantitatively verified instantiation of this thesis in the domain of neural network training. It does not *prove* the thesis — one cannot prove a philosophical position with an experiment on GPT-2. But it does demonstrate that the thesis is **operationalizable**: that there exists at least one mathematically well-defined mechanism in which internal contradiction functions as the system's self-sustaining training signal, with empirically measurable consequences.

We close by enumerating what this retrospective does not claim:

1. **It does not claim that dialectical materialism predicted the result.** The prediction was made *post hoc*, from the mathematics of fixed-point contraction, not from philosophical axioms. The philosophy serves as a frame, not a generator.

2. **It does not claim that all model collapse is mechanical-materialist.** The External Signal Paradigm is a structural description; a researcher can deploy RLHF without holding any philosophical position whatsoever. The claim is that the *structure* of the paradigm instantiates the *structure* of mechanical materialism — not that its practitioners are mechanical materialists.

3. **It does not claim that the internal-tension mechanism works at scale.** The evidence is from GPT-2 124M, Wikitext-2, 10 generations, $N=4$ seeds. Extension to larger models, different architectures, and longer training horizons is future work — and may fail.

4. **It does not claim that the spear channel is the only possible dialectical mechanism.** It is one concrete mathematical instantiation. Other formulations — different contradiction measures, different channel topologies, different integration schemes — may emerge. The principle is broader than any single implementation.

These markers are not rhetorical hedges. They are the boundary between a scientific report and a philosophical manifesto. Our contribution is a technical result — the dual-channel loss, the U-shape phase transition, the $D^* > 0$ fixed point — and a structural claim about what that result means for the architecture of training paradigms. The philosophical retrospective is offered as an invitation: to see in the mathematics of a 124M-parameter model an echo of a question that has been asked, in different vocabularies, for a very long time.

[^1]: Mao Zedong, "On Contradiction" (1937), in *Selected Works of Mao Tse-tung*, Vol. I (Peking: Foreign Languages Press, 1965), p. 311. Translation modified for terminological consistency with this paper's usage of "contradiction" for 矛盾 (máodùn).

[^2]: Ibid., p. 314.

---

*Win 姐姐 / 2026-05-14 / v1 Draft*
*待反题姐姐 de-bias check + DeepSeek 术语审计*
