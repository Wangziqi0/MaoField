# Rebuilding the presentation (no new scientific sampling)

Install the pinned packages in requirements-lock.txt in a separately managed environment. The analysis uses the same saved scientific inputs; figure 2 is an analytical illustration.

```bash
python BUILD/figures.py --root .
python BUILD/build_documents.py
```

The document builder also needs Pandoc. It emits editable native Office Math and applies `BUILD/math_rendering.py` to repair OOXML delimiter property order. LibreOffice or Microsoft Word is then needed to render DOCX to PDF; the authoring run used LibreOffice through the supplied environment's document renderer. No font binaries are distributed. Figures use Arimo, an Arial-metric-compatible sans-serif font installed in the authoring environment; a standard sans-serif font can be installed separately and the figure constant changed before rebuilding. Math glyphs use appropriate font fallback. PDF text is embedded, SVG text remains editable.

Default scientific reanalysis is independent of the presentation builder:
```bash
python REPRODUCIBILITY/reproduce.py --out WORK/offline
```

No command above invokes a model or attempts a Lean proof replay. The saved-candidate replay remains a separate, explicitly enabled, dependency-bound procedure. Public reviewer archives include the figure source; editable manuscript/SI and the document builder are supplied in the private master/submission directories.
