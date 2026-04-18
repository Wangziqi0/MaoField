# arXiv v1 LaTeX Baseline + Phase B Exp 1 Appendix (T6)

**Built 2026-04-15 via pandoc + pdflatex**

## Status: baseline + appendix both compiled

| Artifact | Pages | Size | Source |
|---|---:|---:|---|
| `arxiv_v1_raw.pdf` (main paper) | 55 | 573 KB | `../arxiv_v1_full.md` |
| `phase_b_exp1_appendix.pdf` (companion) | 9 | 267 KB | `../phase_b_exp1/phase_b_exp1_appendix.md` |

Sources:
- `arxiv_v1_raw.tex` — main-paper pandoc output (184 KB)
- `phase_b_exp1_appendix.tex` — appendix pandoc output
- `arxiv_v1_with_appendix.md` — concatenation (currently fails integrated compile — appendix and main compile fine individually; integrated compile needs manual header merge, deferred)
- `*.log` — pdflatex transcripts

## Known issues (deferred to post-v0.1.1 release polish)

1. **CJK characters** (矛盾论, 实践论, etc. in references/footnotes) render as missing glyphs in pdflatex. Fix: switch to `xelatex` with `\usepackage{ctex}` or `\usepackage{xeCJK}` + a CJK font.
2. **Long tables** warn `Table widths have changed. Rerun LaTeX.` Cosmetic, resolved by re-running pdflatex 2-3 times.
3. **Labels may have changed** — cross-references need 2-3 pdflatex passes to stabilize.
4. **Math symbols**: Unicode math (ℂ, ψ, ∇, ∂, etc.) mostly render OK under pdflatex but some symbols may need explicit `$$` wrapping. Check math blocks in §2.3 / §3 / §4.

## Recommended production pipeline (post-release, T6 polish)

```bash
# With CJK support and proper math rendering:
xelatex -interaction=nonstopmode arxiv_v1_raw.tex
bibtex arxiv_v1_raw
xelatex arxiv_v1_raw.tex
xelatex arxiv_v1_raw.tex
```

Preamble additions needed:
```latex
\usepackage{ctex}         % Chinese typesetting
\usepackage{unicode-math} % Unicode math symbols (ℂ, ψ, ∇)
\setmathfont{Latin Modern Math}
```

## What the baseline proves

- arxiv_v1_full.md is **LaTeX-convertible in principle** — structural markdown (headings, tables, math, footnotes) survives pandoc → LaTeX roundtrip.
- 55-page PDF compiles without fatal errors.
- Suitable for arXiv submission after one round of CJK + bibtex polish (deferred to post-v0.1.1).

## Not done here

- arXiv submission prep (bibtex, arXiv template class, figures as PDF not PNG)
- Figure placement tuning
- Footnote numbering verification
- Cross-ref completeness check
