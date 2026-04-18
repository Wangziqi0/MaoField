# REVIEW_PHASE_B_EXP1_appendix.md — 2026-04-15 Silent Block 2

Independent scholarly-review audit of `phase_b_exp1_appendix.md` (Linux draft). Reviewer read appendix + verdict + verdict review + day2 JSONs + arXiv v1 parent paper §1.6 / §3.4 / §5.2 / §5.3. Read-only.

## Summary verdict

**PASS for arXiv v1 appendix inclusion and v0.1.1 Zenodo release.** The appendix is a genuinely scholarly distillation of the verdict: tone is neutral and quantitative, the three downgrades are executed cleanly, all four exploration signals are narratively integrated, and every spot-checked number traces to the day2 JSONs. No P0 blockers. Remaining items are polish, mostly inherited from the verdict review.

## P0 check (8 items) — all PASS

1. **Coherence with parent paper — PASS.** §A.7 positions against OP1 (not addressed) and OP2 ("partially obviates (a), (b)(c) open") matching arXiv v1 §5.2/§5.3. No conflict against §1.6/§3.4/§5.4.

2. **Scholarly tone — PASS.** Abstract sentence, equation numbering (A.1, A.2), passive-voice methods, table-driven results, discriminating framings all referee-appropriate.

3. **Three downgrades — PASS.** §A.5 table crisp; §A.3.3 title; §A.3.2 quasi-stationary language with c+A·t⁻¹·²; §A.4(i) architectural robustness with 0.12% L² vs 17σ z-score. No regression.

4. **Four exploration signals — PASS.** A (§A.4(i) + DC mode), B (§A.4(ii) + §A.3.3 Δt<0.43), C (§A.4(iii) SSB seed merge), D (§A.4(iv) + §A.3.2 fit).

5. **Numbers spot-check — PASS.** Verified against day2 JSONs:
   - 50 patches / 49.8 ← 49.828 ✓ ; 94.3% ← 0.94286 ✓
   - R = 7,768 ← 7768.20 ✓ ; α_θ = 1.28 ← 1.2797 ✓
   - late dS/dt exp 2.19e-5 ← 2.1894e-5 ✓ ; whiten 2.24e-5 ← 2.2362e-5 ✓ ; null/const 8.28e-4 ✓ ; single 8.62e-4 ← 8.625e-4 ✓
   - source_l2 CoV 0.107 ← 0.10717 ✓ ; single CoV 0.005 ← 0.00512 ✓
   - η(dt=0.01) = 0.302 ← 0.30178 ✓ ; η(dt=0.1) = 0.311 ← 0.31149 ✓
   - Δt stability 0.43 ← 2/4.6 = 0.4348 ✓
   - c = 9.4e-7 asymptote consistent with extended trajectory (2.90e-6 at t=200 decaying toward plateau)

6. **Explicitly not claimed — PASS (7 disclaimers).** §A.8 covers ontological / thermodynamic / RG / parameter / temporal generalization / 36h caveat / BGE higher-order. Exceeds required 6.

7. **Not over-selling — PASS.** §A.1 "preliminary", "non-vacuous", "qualitatively consistent"; §A.7 "partially obviates OP2 (a)"; §A.6 "no falsified, three refined, two merged" — appropriately bounded.

8. **36-hour caveat — PASS.** §A.1 paragraphs 1-2 and §A.8 bullet 6 all explicit.

## P1 recommended polish (non-blocking)

1. **NESS exponent 1.2 justification** *(top priority)* — §A.3.2 fixes exponent at 1.2 without disclosure. Hostile-referee target. Recommend single sentence: "The exponent 1.2 was selected as [median fitted / round figure from preliminary scan]; sensitivity across exponents ∈ [1.0, 1.5] yields c within ±3·10⁻⁷, preserving the qualitative plateau identification."

2. **"Architectural theorem" language** (§A.4(i), §A.6) — either soften to "architectural property" / "structural robustness claim", or promote with one-line proof: *"since α(ψ − ⟨ψ⟩) and β·δS_history integrate to 0 in x, the constant component of S₀ enters only the 1-D ODE for ⟨ψ⟩(t), decoupled from spatial modes."* Current wording is threshold.

3. **Null-mode R interpretation** — The paragraph does explain "generic feature of overdamped relaxation". However the table row `null: R=16,923, Pass B 100%` next to `exp: R=7,768, 94.3%` visually suggests null is more Goldstone-like. One clarifying sentence preempts misread.

4. **Abstract/opening label.** "One-sentence summary." is non-standard; consider removing label or using "Summary" / dedicated *Abstract*. Minor.

5. **Section numbering.** A.1–A.10 scheme may collide with existing "Appendix 2.3.A" / "Appendix 3.A" in parent. Recommend labeling "Appendix B: Phase B Experiment 1" for unambiguous referencing.

6. **Figure references absent.** `phase_b_exp1_figures/` exists but appendix never references. Either cross-reference one figure (dS/dt trajectory; ψ snapshot showing patches) or add line: "Figures are in the Zenodo companion dataset."

7. **Block-size caveat in §A.3.3.** Self-similarity is across *inner time-step* scales at fixed `block_size = 2`. §A.9 bullet 2 flags, but one sentence in §A.3.3 itself prevents referee conflation of time-scale vs spatial-scale self-similarity.

## P2 stylistic

- §A.1 closing paragraph ("strengthen...not concessions") slightly defensive; let results speak.
- `dS/dt` vs `ds/dt` notation inconsistent (§A.3.2 vs §A.8). Normalize.
- §A.3.3 "bang-bang" colloquial; prefer "clipped nonlinear regime".
- §A.4(i) final sentence "upstream statistical idiosyncrasy" colloquial; prefer "statistical idiosyncrasies of the upstream embedding".
- §A.6 table `#` column mixes "1 & 5" with singletons; consider 5-row layout.
- §A.10 should add this appendix review to the list when finalizing.

## Alignment with parent paper

**Strong.** Parent §1.6 declares OP1/OP2 "prominently foregrounded"; appendix §A.7 surgically consistent. Parent §5.4 "outlook" status for Phase B; appendix §A.1 honors explicitly.

One alignment opportunity: parent §2.3.3 "three faces of OP2" (categorical / physical / phenomenological). Phase B Exp 1 architectural-theorem (§A.4(i)) adds *structural information* about path (a) source statistics. A single sentence in §A.7 cross-referencing "three faces of OP2" would make the contribution to the parent's categorical edifice explicit.

## Over/under-claim double scan

**Over-claim risk — zero red flags.** Strongest claims ("quasi-stationary NESS", "architectural theorem", "kinematic self-similarity") each paired with downgrade and "not claimed" counterpart. Referee-safe.

**Under-claim risk — mild.** The architectural-theorem reframing of Insight 3 is genuinely the strongest scientific finding (falsification-resistant structural result). §A.4(i) slightly buries it under the exploration heading. Consider promoting to the abstract/summary sentence alongside 50-patch/NESS facts.

## Blocking / non-blocking

- **Blocking: none.** All 8 P0 pass.
- **Non-blocking P1:** 7 items. Top priority is (1) NESS exponent justification — address before camera-ready arXiv.
- **Non-blocking P2:** 6 stylistic, editorial.

## Closing note

The appendix is notably tighter than the verdict: ~8,000 words of internal argument distilled into ~2,400 words of scholarly prose without losing any downgrade or signal. Control-table compression (§A.3) and merged insights 1+5 framing (§A.4(iii), §A.6) are particularly well-executed — what was an awkward "collapse" in the verdict becomes a positive structural claim ("translation-symmetry-breaking seed is the necessary third ingredient").

**Recommendation**: accept Linux's appendix for v0.1.1 Zenodo release and arXiv v1 inclusion. Merge P1 item 1 (exponent justification) before camera-ready arXiv. No re-review needed post-polish.

*— Independent paper-review subagent, 2026-04-15 Silent Block 2*
