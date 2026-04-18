# § 6.X What Would Falsify MaoField — Pre-registered Commitments

**Draft by Win Claude, 2026-04-15 night**
**Triggered by**: 反题姐姐 path 4 (Popper/Lakatos 不可证伪性 charge), 路径 4 commitment
**Target**: arXiv v1 §6 的新 subsection, 位置在 §6 Discussion 内
**Status**: Win solo draft, 等一凡 04-17 morning 审 + Linux 独立 technical verify

---

## Rationale

反题姐姐抓到的最锋利一点: **一个 research program 若 cannot be falsified, in Popperian terms 不是 science**. Lakatos 的 concern 是 framework 可能加 protective hypotheses 直到不可证伪。这对任何把 rigorous math (Lawvere adjunction) 和 open conjecture (three-faces convergence, dynamic V) 耦合的框架都是 real risk。

我们**正面 accept this risk** —— 通过**命名具体的、已 pre-registered 的 future experiments**，它们的 adverse outcome 会 force 我们 retract 具体 claim。这不是 defensive gesture，是 load-bearing commitment。

---

## § 6.X 提议正文

### Pre-registered Falsifiers

Each falsifier (F-code) specifies: (a) the claim it tests, (b) the experimental protocol, (c) the adverse outcome that would force claim retraction, (d) target paper version by which the test must be executed.

---

**F1 — k*=2 attractor count is structural, not framework artifact**

- **Claim tested**: §4.4 Block III 主张 k*=2 across three representations reflects a semantic structural ceiling, not a PDE dynamics + k-means artifact
- **Protocol (Block III control rerun)**: Replace byte source with (a) random Gaussian source matched to per-voxel statistics of byte source, (b) shuffled-token BGE source (token-level permutation breaks semantic structure while preserving embedding distribution)
- **Falsifying outcome**: k*=2 silhouette optimum emerges for *either* control at silhouette separation ≥ 0.8 × of the byte result
- **Interpretation if falsified**: k*=2 is a framework-dependent pattern of PDE+clustering regardless of input semantic content; the "structural ceiling" claim is retracted
- **Target**: v0.2.0 (IPM mechanism paper companion)

---

**F2 — Localized coherent patches correspond to semantic units**

- **Claim tested**: §4.6 + Phase B Exp 1 主张 50 patches per doc are candidate "semantic atoms"
- **Protocol (patch-semantic linear probing)**: For 70 NFCorpus documents, extract 50 patches per document; train linear probe from patch-summary vectors (mean + variance of patch features) to held-out semantic labels (document topic classification, entity mention presence). Compare to two baselines: (a) random-field patches with matched grid positions, (b) BGE hidden-state probing with matched feature budget
- **Falsifying outcome**: Linear probe accuracy is not statistically above baseline (a), OR is below baseline (b) by > 10%
- **Interpretation if falsified**: Patches are mathematically interesting but without specific semantic claim; the "semantic atom" framing retracted
- **Target**: v0.2.0

---

**F3 — b+c feedback is the operational form of Axiom 6**

- **Claim tested**: Today's Phase B Exp 1 主张 b+c 双向反馈是 Axiom 6 "matching = self-training" 的 PDE 实现
- **Protocol (feedback-structure substitution)**: Run Phase B Exp 1 with (a) no feedback (α=β=0, already done as `control_const`), (b) null-feedback (α, β sampled iid Gaussian matched-variance but random sign per voxel per step)
- **Falsifying outcome**: Phase B Exp 1's 50-patch signal emerges equivalently under null-feedback → b+c is **an** implementation but not the canonical one; Axiom 6's formal role weakened
- **Partial evidence**: no-feedback control produced 0 patches (today). Null-feedback not yet tested
- **Target**: v0.1.2

---

**F4 — Framework is architecturally robust to upstream source statistics (Signal A)**

- **Claim tested**: Signal A 主张 framework output independent of source mean drift at architectural level
- **Protocol (hostile source)**: Construct source with large fixed DC offset (10× BGE's natural mean) + non-stationary time drift (slow linear ramp across simulation horizon)
- **Falsifying outcome**: MaoField output distinguishability across documents (measured by variance of pairwise field distances) degrades > 50% relative to BGE-natural source
- **Interpretation if falsified**: "Architectural robustness" is local (BGE-distribution-specific), not structural; Signal A must be restated as empirical regularity
- **Target**: v0.1.2

---

**F5 — Three-pillar composition (TF + Shape-CFD + MaoField) is constructively synergistic**

- **Claim tested**: §6.5 implicit 主张 three-pillar 架构是 coherent direction, not three independent projects
- **Protocol (end-to-end composition)**: Implement full pipeline Shape-CFD PQ-Chamfer → MaoField multi-token source → PDE evolution → ranking. Evaluate on same 5 BEIR datasets
- **Falsifying outcome**: Composed pipeline scores < max (Shape-CFD alone, MaoField alone) on ≥ 3/5 datasets (negative synergy)
- **Interpretation if falsified**: Pillars are architecturally interchangeable or antagonistic; "unified framework" claim retracted, paper repositioned as "parallel techniques"
- **Target**: v0.3.0 (requires substantial integration work)

---

**F6 — MaoField provides interpretability beyond transformer hidden states**

- **Claim tested**: §1 + §6 implicit 主张 MaoField's physical representation offers interpretability advantages over opaque embeddings
- **Protocol (interpretability metric)**: Define operational interpretability as `(linear probe accuracy) × (count of distinct linearly-separable semantic concepts)`. Compute for (a) MaoField patch features (aggregated), (b) BGE hidden-state features (matched budget)
- **Falsifying outcome**: MaoField metric is not ≥ 1.2× BGE metric
- **Interpretation if falsified**: "Interpretability" is aesthetic, not quantitative; claim rephrased from "better interpretability" to "different interpretability" (or retracted)
- **Target**: v0.2.0

---

**F7 — Axiom 6 admits canonical mathematical formalization**

- **Claim tested**: §3.2 Axiom 6 being a postulate rather than heuristic
- **Current status**: M2 candidate falsified (§5.1). b+c feedback (F3 above) is candidate pending F3 verification
- **Standing falsifier**: If no candidate formalization passes rigorous analysis (fixed-point existence, stability, or convergence rate) by **2028-Q1**, Axiom 6 is demoted from "postulate" to "empirical heuristic" and its role in the framework architecture is reevaluated
- **Interpretation if reached**: Framework's seven-axiom structure revised; the monad-theoretic narrative of §2.3 is weakened to "conjectured extension awaiting Axiom 6 closure"

---

**F8 — Spawn-agent review catches ≥ 80% of externally-visible errors**

- **Claim tested**: §6.3 主张 spawn-agent review pipeline is reliable quality gate
- **Protocol (cross-LLM review)**: Re-submit full paper + all deliverables to GPT-4.1 + Gemini 2.5 Pro as independent reviewers. Compare issues raised to Opus-only review archive
- **Falsifying outcome**: Cross-LLM review identifies ≥ 3 substantive issues (mathematical error / logical contradiction / over-claim) missed by Opus-only review
- **Interpretation if falsified**: Same-family LLM review has systematic blind spots; multi-model cross-review becomes mandatory standing rule
- **Target**: v0.1.2 (before IPM mechanism paper submission)

---

### Standing Discipline

Three commitments accompany the pre-registration:

1. **No cushioning after the fact**: If any F-falsifier returns an adverse outcome, the corresponding claim is retracted or weakened in the next paper version. Adding post-hoc auxiliary hypotheses to rescue the falsified claim violates the Lakatosian non-degeneration standard and is explicitly rejected.

2. **Timeline enforcement**: Each F-falsifier has a target paper version. If a test is not executed by that version, the untested claim is downgraded to "asserted, not validated" in the interim.

3. **Public pre-registration**: This section's F-list is committed at v0.1.1 release (Zenodo DOI `10.5281/zenodo.19550341` concept). Any subsequent weakening of an F-falsifier (easier test, delayed timeline) must be declared explicitly as a pre-registration amendment.

---

### What This Section Does NOT Promise

Not every framework component is *currently* falsifiable:

- Axioms 5 and 7 are flagged as aspirational (§3.2 tension points). No F-falsifier is assigned; these are honestly *open directions*, not testable claims
- Several categorical-theoretic constructions (T-Alg_T^{(η,p₀)}, Δ_OP2) are flagged as conjectured (§2.3.4)
- The "three-faces convergence" (§2.3.3) is stated as "most coherent organizing conjecture currently visible" —— not a testable hypothesis but a research program framing

This distinction between **empirically testable claims** (with F-falsifiers) and **mathematical / philosophical open directions** (without) is preserved honestly. Falsifiability commitment extends only to the former; the latter are open research problems in the sense of §5's OP1 / OP2.

---

### Philosophical Positioning

Some readers will note the potential irony of a dialectical-materialist framework adopting explicit Popperian falsifiability commitments, given dialectical materialism's historical critique of strict Popperianism. We do not see this as inconsistent: the Popperian criterion **filters empirical content** (what claims *can* be wrong), while dialectical materialism specifies **epistemological attitude** (how knowledge develops through practice-contradiction-synthesis). The framework's **empirical claims** are held to Popperian standards; the framework's **methodology** (spawn-agent review, multi-scale co-design, OP-signposting) is developed through dialectical engagement with its own open problems.

A research program that rejects falsifiability is closed; one that embraces it commits to continued self-critique. We choose the latter.

---

*—— End of proposed § 6.X draft.*

**Notes to 一凡 (04-17 morning review)**:

1. **8 F-falsifiers 数量**: Substantive 但是否 overwhelming? 如果 reduce 到 5 (核心 F1/F2/F3/F4/F8), 论文更紧凑但覆盖略减. Linux 可以 verify 哪几条 empirically actionable 最近
2. **Timeline targets**: v0.1.2 / v0.2.0 / v0.3.0 是我设定的节奏. 你 review 是否 realistic
3. **F5 (三支柱 composition)**: 这条 target v0.3.0 比较远. 如果你觉得 Shape-CFD + MaoField bridging paper 更 urgent, 可以 move to earlier target
4. **F7 (Axiom 6 formalization)**: 2028-Q1 的 standing falsifier 是给自己**两年** to close Axiom 6. 如果你觉得 太紧 (数学问题, 真难算)可以 relax 到 2029
5. **"What we don't commit to"**: 明确保留 Axioms 5 / 7 / three-faces 为 open research direction, 不是 ceremonial hedging

**Win 不 commit 到 arxiv_v1_full.md**. 等一凡 04-17 morning + Linux 独立 technical verify 后整合.
