# Cross-Section Consistency Pass

**Auditor**: Win Claude
**Date**: 2026-04-14
**Scope**: 8 sections (§1, §2.1-2.2, §2.3, §3, §4, §5, §6) + references
**Judgment**: **pass** after 4 cross-reference fixes applied

---

## Issues Found and Fixed

| # | Issue | Location | Fix |
|---|---|---|---|
| 1 | "Section 3.X" dangling ref (SSB section) | §4 line 5 | → "Section 3.5" |
| 2 | "(Section 3.X; footnote [^zn-loose])" | §4 line 424 | → "(Section 3.5; footnote [^zn-loose])" |
| 3 | "See Section 3.X footnote or FINAL_REPORT.md" | §4 line 460 ([^zn-loose] definition) | → "See Section 3.5 (`[^zn-loose]` footnote) for full text" (dropped external ref since arXiv paper should be self-contained) |
| 4 | "BLOCK_V_DESIGN.md §3.6" (A-3.b Jacobian ref) | §5.3 A-3.b | → "BLOCK_V_DESIGN.md §4.5.3 Phase A-3" (§3.6 is non-equilibrium priority, IMEX Jacobian is §4.5.3) |

All 4 fixes applied and re-scp'd to Linux.

## Consistency Verified (no fix needed)

### Numbers
- Block I range: `+14.7%` to `+172.3%` consistent in §1.5, §1.7 (fixed earlier), §4.2 Table 4.1 ✓
- BGE-reranker gap: `−11 pp to −32 pp` in §1.5, `−10.8 to −32.2 pp` in §4.2 Table (rounding OK) ✓
- BGE source drift: `t = −17.1, p < 10⁻²⁵` consistent in §1, §3.2 Axiom 4, §4.9, §5.2, §6 ✓
- A1 outer barrier: `13.187 / T_eff=0.125 = 105.5; ~43 orders log-gap` consistent in §2.3 App., §4.8, §5.2 ✓
- A1 inner barrier discrepancy: `factor ~10⁴ (~4 orders of magnitude)` consistent in §2.3 App., §4.8.3, §4.11.1, §6.2.3 ✓
- Static ratio: `3.07×` consistent in §2.3 App., §4.7.3, §5 ✓
- CFL violation: `380× (λ=1) / 3800× (λ=10)` consistent in §4.9.3 Axis C and §5.2.2 (c) (fixed earlier) ✓
- A1.4 Laplace prediction: `p(0)=0.028, p(1)=0.569, p(2)=0.402` consistent in §4.9, §5 ✓
- A1.4 clamp residency: `52.5% (σ=0.5 no wall), 53.4% (λ=1), 59.3% (λ=10)` consistent in §4.9.2 Table 4.11, §5.2.2 ✓

### Naming
- "Phase C sub-block C-V" consistent in §3.2 Axiom 7 (fixed earlier), §5.4 ✓
- "Block V Phase A-0/A-1/A-2/A-3/A-joint" consistent in §3, §5.3, §6 ✓
- "three-fold co-design" consistent terminology across §3, §4, §5, §6 ✓
- "three-faces convergence" consistent across §2.3.3, §5.2.4, §6 (softened to "most coherent organizing conjecture currently visible" in both §2.3 and §5.2.4) ✓
- Z_n labels `[^zn-loose]` convention: footnote defined in §3.5, cross-referenced by §2.3, §4, §5, §6 — all use "empirical distributional sense" phrasing ✓

### Cross-references
- §1.8 outline matches §2–§6 actual content ✓
- §2.3 forward-refs to §3.2 (axioms), §3.3 (adjunction), §4.7, §4.8, §5.1, §5.2 all land correctly ✓
- §3 forward-refs to §4.9 (A1.4), §5.1 (OP1), §5.2 (OP2) ✓
- §5 back-refs to §2.3.3, §4.9, §4.11.1 ✓
- §6 integrates all sections correctly ✓

### OP1 / OP2 Status (cross-document integrity)
- OP1 (Axiom 6 formalization): stated in §3.2 Axiom 6, §3.4, referenced in §1.6, falsified in §5.1, summarized in §6.1. **All consistent: M2 excluded, Axiom 6 remains without canonical formalization.** ✓
- OP2 (Axiom 3 non-equilibrium extension): stated in §3.2 Axiom 3, §3.4, refined in §4.9, §5.2 three-fold co-design, summarized in §6.1. **All consistent: refined from single-axis to three-axis problem.** ✓

### Citation integrity
- Lawvere 1969 "Adjointness in Foundations" Dialectica 23: cited in §1.3, §2.2, §2.3.1, references.bib ✓
- Giry 1982, Jacobs 2010/2017: cited in §2.3 footnote ⁵, §2.3.3, references.bib ✓
- Lenin 1909, Mao 1937 (×2), Engels 1873-83/1925: cited in §1.2, §2.1, references.bib ✓
- Ginzburg-Landau 1950, Allen-Cahn 1979, Kramers 1940, Anderson 1963, Goldstone 1961, Nambu 1961: all in references.bib ✓
- BEIR 2021, BGE-M3 2024: in §4.1, references.bib ✓
- MaoField self-ref: Zenodo DOI `10.5281/zenodo.19550341` consistent in §1.8, references.bib ✓
- Shape-CFD: IPM-D-26-02154 cited in §6 (not in body — OK, it's separate work); in references.bib ✓

### Footnote integrity
- `[^zn-loose]` defined in §3.5, referenced correctly from §2.3, §4 (3 places after fix), §5 ✓
- Numbered footnotes ¹²³⁴⁵ in §2.3 all resolve to in-section content ✓

## Remaining Non-Issues

The following could be "improved" but are not inconsistencies:

- §4.1 mentions "+CodeSearchNet" in datasets list, but Table 4.1 reports only 5 datasets. This is **OK** because CodeSearchNet is configured but results-missing; §1.5 correctly says "five reported BEIR benchmarks"
- §2.3 Appendix 2.3.A numbering overlaps §3.A. The paper has both 2.3.A and 3.A appendices; reader context disambiguates. Acceptable for position paper
- `⊖` symbol in Δ_OP2 is now defined in §2.3.4 main text + footnote ³ (after P1 fix). Acceptable

## Bottom Line

**arXiv v1 paper is cross-section consistent after 4 fixes applied**. No remaining P0 or P1 inconsistencies. Ready for §1 + §2.1-2.2 agent review (rate-limited to 3pm Asia/Shanghai) and final integration pass tomorrow morning.

*End of consistency pass.*
