# 引用最终核验

核对 20 条编号参考文献及其全部已识别引用位置。当前未发现需要改写的作者、标题、年份、卷页或 DOI 错误。

采用 nature-ref-verifier 的编号文献流程；上下文判断是本执行者对照原始来源所得，不宣称另一模型家族的独立认证。

| 编号 | 结果 | 原始来源与核对说明 |
|---|---|---|
| 1 | 保留 | [Avila, A](https://mathandai.org/) — Declaration and DataCite agree on title, date and 25 initial authors. Used as an attributed concern and motivation, not as a measured general harm. |
| 2 | 保留 | [OpenAI](https://openai.com/index/navier-stokes-solution/) — Published process account supports Euler-result reuse, resource redirection, Codex consolidation and concurrent model update. The manuscript keeps its process-account status. |
| 3 | 保留 | [OpenAI](https://github.com/openai/codex/tree/a8964cb1bad67bc26a826fb07d1bef99c6a3f008) — Commit resolves; context handler and history-notes module fetched at the pin match supplied snapshots byte-for-byte. Concrete operations are supported; full future sufficiency is not inferred. |
| 4 | 保留 | [Rav, Y](https://academic.oup.com/philmat/article-abstract/7/1/5/1430602) — Publisher verifies Rav, 1999, volume 7, pages 5–41. Publisher abstract directly supports epistemic/methodological content beyond theorem statements; no stronger empirical claim is attributed. |
| 5 | 保留 | [Messeri, L](https://www.nature.com/articles/s41586-024-07146-0) — Authors, title, year, volume and pages match. Used for the conceptual distinction between productivity and understanding, not a causal result from this study. |
| 6 | 保留 | [Yang, K](https://proceedings.neurips.cc/paper_files/paper/2023/hash/4441469427094f8873d0fecb0c4e1cee-Abstract-Datasets_and_Benchmarks.html) — Published NeurIPS 36 and arXiv title/year/lead author agree. Premise retrieval/availability context is directly supported. More than five authors are correctly abbreviated et al. |
| 7 | 保留 | [Doyle, J](https://dspace.mit.edu/entities/publication/5377b306-4ecc-4687-b1f5-78cbb4a0543a) — MIT record verifies Doyle, AI Memo 521, 1979. Abstract directly states recording/maintaining reasons and revising beliefs. |
| 8 | 保留 | [Littman, M](https://proceedings.neurips.cc/paper/2001/file/1e4d36177d71bbb3558e43af9577d70e-Paper.pdf) — The primary PDF lists Littman, Sutton AND Singh; the HTML index omits Singh. Retain all three as currently written. Source supports action-conditional predictive state representation and recursive updates. |
| 9 | 保留 | [Arora, S](https://proceedings.mlr.press/v80/arora18a.html) — Primary proceedings match Arora/Cohen/Hazan, 2018, volume 80, pages 244–253. Linear overparameterisation separates optimisation effects from expressiveness, supporting the limited comparison cited. |
| 10 | 保留 | [Feldman, M](https://journals.sagepub.com/doi/10.2307/3556620) — Publisher and registry agree on two authors, 2003, volume 48, pages 94–118. Ostensive/performative relations support the cited situated-performance and stability/change discussion. |
| 11 | 保留 | [Ibrahim, L](https://www.nature.com/articles/s41586-026-10410-0) — Publisher verifies Ibrahim/Hafner/Rocher, Nature 652, 1159–1165, 2026. Warmth/accuracy dependence is contextual prior work, not evidence for the manuscript mechanism. |
| 12 | 保留 | [Shumailov, I](https://www.nature.com/articles/s41586-024-07566-y) — Publisher and Crossref agree. Recursively generated training data is used only as a relevant example of outputs changing later conditions. |
| 13 | 保留 | [Miao, J](https://www.nature.com/articles/s41586-026-11044-y) — Publisher lists the same five authors, title and DOI; published 16 September 2026, with no volume/pages displayed yet. Interactive executable paper agents support the stated related-work role. |
| 14 | 保留 | [Marx, K](https://www.marxists.org/archive/marx/works/1845/theses/theses.htm) — Edition header verifies 1845 composition, Engels editing, W. Lough translation, Progress Publishers Moscow 1969, pages 13–15. Thesis III directly supports educator/organiser inside the process; manuscript calls this a theoretical boundary, not mechanism proof. |
| 15 | 保留 | [Mao, Z](https://www.marxists.org/reference/archive/mao/selected-works/volume-1/mswv1_16.htm) — Title/date and selected-works identity match. The primary text discusses renewed practice, unforeseen circumstances and revision. Used as conceptual framing only. |
| 16 | 保留 | [OpenAI](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf) — Direct PDF has 166 pages, title Finite Time Blowup for Navier–Stokes and OpenAI authorship; fetched hash recorded. Covariance/primary-wave sections exist. This citation does not independently certify global NS closure; detailed mathematical use is separately audited. |
| 17 | 保留 | [OpenAI](https://github.com/OpenAI/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/NavierStokes/PrimaryCovarianceBounds.lean) — Commit and source file resolve. Fetched source SHA256 7417f840e9689a41504a1cc368acc04d565d2c5bac2cca3959675a9a86b97862 matches the recorded original-source identity. Modified study slice is separately disclosed in Methods. |
| 18 | 保留 | [de Moura, L](https://lean-lang.org/papers/lean4.pdf) — Lean official citation verifies de Moura/Ullrich, CADE 28, 2021, pages 625–635 and DOI. Appropriate tool/theorem-prover citation. |
| 19 | 保留 | [Lean Project](https://lean-lang.org/doc/reference/latest/ValidatingProofs/) — Official documentation explicitly distinguishes listed axioms, stored-proof checking and stronger trust layers. The cited standard-axiom discussion remains applicable; latest URL is dynamic and its current version is not substituted for the historical 4.34 toolchain. |
| 20 | 保留 | [Liu, N](https://aclanthology.org/2024.tacl-1.9/) — ACL and Crossref match Liu et al., TACL 12, 157–173 (2024). Position/context-use effects support plausible alternative explanations, not a demonstrated cause of this proof-pair contrast. |

特别记录：Crossref 的限流不被当作文献不存在；PSR 作者以原始 PDF 为准；Paper2Agent 的卷页不凭空补全；动态 Lean 文档不替代历史工具链身份。
完整引用上下文与行号见 CITATION_CONTEXTS.json，实时查询回执和固定源码哈希保存在同一审计目录。
