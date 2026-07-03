# Bibliography Final Metadata Audit

Date verified on node36: 2026-07-03 14:32 CST
Scope: V2.4 final Pro review package
Status: `LOCAL_METADATA_SPOT_CHECK_COMPLETE_WITH_MEDIUM_DUPLICATE_RISK`

## Method

Metadata was checked from local command output against:

- Crossref API for DOI records;
- arXiv API for arXiv version/authors/title records;
- local repository files for MaoField release-state evidence.

This audit is not a claim that the literature search is exhaustive.
Duplicate-risk status remains:

```text
MEDIUM duplicate risk
```

## High-Risk Name Spelling

Use the TeX-safe accented spelling:

```text
B\"ottcher, A.
```

The DOI record for `10.1016/j.laa.2009.11.002` reports author spelling
`A. Böttcher` and coauthor `I.M. Spitkovsky`. Do not silently replace this
with plain `Bottcher` in a final bibliography. `Boettcher` is an ASCII fallback
only when accents are impossible.

Corrected V2.4 entry:

```text
B\"ottcher, A. and Spitkovsky, I. M. A gentle guide to the basics of two projections theory. Linear Algebra and its Applications 432(6), 1412--1459 (2010). doi:10.1016/j.laa.2009.11.002.
```

## DOI Metadata Spot Checks

### Lamboni 2026

- DOI: `10.1137/24M1712680`
- Title: `On ANOVA-Type Decompositions of Functions with Non-independent Variables: Sensitivity Analysis`
- Author: `Matieyendou Lamboni`
- Journal: `SIAM/ASA Journal on Uncertainty Quantification`
- Published online: 2026-06-16
- Published print metadata in Crossref: 2026-06-30
- Volume/issue/pages: `14(2), 691--710`

Corrected V2.4 entry:

```text
Lamboni, M. On ANOVA-Type Decompositions of Functions with Non-independent Variables: Sensitivity Analysis. SIAM/ASA Journal on Uncertainty Quantification 14(2), 691--710 (2026). doi:10.1137/24M1712680.
```

Do not imply that this paper was already formally printed before its publisher
metadata existed. On 2026-07-03, Crossref reports print metadata.

### Il Idrissi et al. 2025

- DOI: `10.1016/j.jmva.2025.105444`
- Title: `Hoeffding decomposition of functions of random dependent variables`
- Journal: `Journal of Multivariate Analysis`
- Volume/article: `208, 105444`
- Authors: Marouane Il Idrissi, Nicolas Bousquet, Fabrice Gamboa, Bertrand
  Iooss, Jean-Michel Loubes

Corrected V2.4 entry uses volume `208`, not `206`.

### Other DOI Floor

- Hooker 2007: `10.1198/106186007X237892`, JCGS 16(3), 709--732.
- Chastaing, Gamboa, Prieur 2012: `10.1214/12-EJS749`, Electronic Journal of Statistics 6.
- Chastaing, Gamboa, Prieur 2015: `10.1080/00949655.2014.960415`, JSCS 85(7), 1306--1333; online record 2014.
- Owen and Prieur 2017: `10.1137/16M1097717`, SIAM/ASA JUQ 5(1), 986--1002.
- Iooss and Prieur 2019: `10.1615/INT.J.UNCERTAINTYQUANTIFICATION.2019028372`, IJUQ 9(5), 493--514.
- Halmos 1969: `10.1090/S0002-9947-1969-0251519-5`, Transactions of the AMS 144, 381--389.

## arXiv Version Spot Checks

The V2.4 bibliography uses explicit version suffixes:

- `arXiv:2206.04615v3`: Srivastava et al., `Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models`.
- `arXiv:2211.09110v2`: Liang et al., `Holistic Evaluation of Language Models`.
- `arXiv:2109.07958v2`: Lin, Hilton, Evans, `TruthfulQA: Measuring How Models Mimic Human Falsehoods`.
- `arXiv:2303.08896v3`: Manakul, Liusie, Gales, `SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models`.
- `arXiv:2303.16634v3`: Liu et al., `G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment`.
- `arXiv:2306.05685v4`: Zheng et al., `Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena`.
- `arXiv:2306.11698v5`: Wang et al., `DecodingTrust: A Comprehensive Assessment of Trustworthiness in GPT Models`.
- `arXiv:2307.03109v9`: Chang et al., `A Survey on Evaluation of Large Language Models`.
- `arXiv:2406.04244v1`: Xu, Guan, Greene, Kechadi, `Benchmark Data Contamination of Large Language Models: A Survey`.
- `arXiv:2311.04850v2`: Yang, Chiang, Zheng, Gonzalez, Stoica, `Rethinking Benchmark and Contamination for Language Models with Rephrased Samples`.
- `arXiv:1011.5237v1`: Corach and Maestripieri, `Products of orthogonal projections and polar decompositions`.

## Duplicate-Risk Position

The V2.4 note remains a compact finite illustrative artifact:

- finite positive weighted two-way table;
- product-weight iff centered main-effect orthogonality;
- order-independence iff product weights;
- existential non-product pure-main-effect witness;
- exact rational 2 x 2 certificate.

It must not claim to supersede or originate broad functional ANOVA,
dependent-input decomposition, sensitivity-analysis, or two-projection theory.
The safest public wording is:

```text
The duplicate-risk status is MEDIUM duplicate risk; no claim is made that no close work exists.
```
