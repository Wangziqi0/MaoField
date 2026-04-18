# Section 4 — Experimental Evidence

*arXiv v1 first draft, 2026-04-14. Linux Claude. Cross-review by Win + independent paper-review subagent.*

**Scope**: this section reports all empirical evidence for MaoField's core claims, organized around the four canonical hypotheses (H1–H3 + OP1/OP2 diagnostic) introduced in Section 3. All `Z_n` symbols are used in the **empirical distributional sense** defined in footnote [^zn-loose]; finite-lattice caveats (Section 3.5) apply throughout.

**Mode tags** (after Linux internal convention, following a documented bug-prevention protocol):
- `[STATIC]`: landscape geometry (critical points, Hessian, barrier heights)
- `[DYNAMIC-EQUILIBRIUM]`: Boltzmann / Laplace stationary distribution predictions
- `[DYNAMIC-RARE-EVENT]`: Kramers escape rate, horizon comparisons
- `[DYNAMIC-IMPLEMENTATION]`: numerical scheme, CFL, boundary conditions, source statistics

---

## 4.1 Setup and notation

**Common configuration** across Blocks I–V.5:

- PDE engine: `ComplexEngine` (exp015), Ginzburg-Landau Allen-Cahn form `γ·∂_t ψ = D ∇²ψ − ∂V/∂ψ* + S(x) + η(t)`, `γ=1`, `D=0.1`
- Default potential: `V(ψ) = ¼·(|ψ|² − 1)²` (standard GL double-well)
- Grid: 3D toroidal lattice, `32³ = 32768` voxels, periodic BC, `dx=1`
- Integrator: explicit Euler, `dt=0.05` (unless noted), steps=5000 for reranker or 2000 for Block II
- Candidate pool: BM25 top-K, K ∈ {6, 20, 100}
- Clamp: `|a|, |b| ≤ 3.0` (i.e. `|ψ|² ≤ 18`) as numerical safeguard; flagged as `[DYNAMIC-IMPLEMENTATION]` artifact where it contributes
- Datasets: BEIR subset `{NFCorpus, SciFact, FiQA, ArguAna, TREC-COVID}` + CodeSearchNet; mMARCO skipped due to download failure
- Evaluation: `nDCG@10, P@10, MRR@10`, BEIR standard
- Hardware: EPYC 7B13 256-core CPU, RX 9070 XT for embeddings (bge-m3, bge-reranker-v2-m3 via llama.cpp)
- Random seeds: 20260412 / 20260413

**Notation**:
- `u ≡ |ψ|²` (scalar amplitude-square radial coordinate)
- `T_eff ≡ σ²/(2γ) = σ²/2` (effective temperature under Langevin noise)
- `⟨·⟩_k` denotes ensemble mean over (documents × voxels) in basin *k*

---

## 4.2 Block I — Baseline retrieval across 5 BEIR datasets

We report `nDCG@10` for six scorers on five datasets to locate MaoField's position in the retrieval performance landscape. Scorers: BM25 (sparse), S1 (byte-ngram baseline), S4 (trigram baseline), BGE-reranker-v2-m3 (SOTA cross-encoder), MaoField_base (PDE with fusion), MaoField_E (PDE without fusion, reranker-only).

**Table 4.1**: `nDCG@10` matrix, 5 datasets × 6 scorers.

| Dataset | BM25 | S1 byte | S4 3-gram | BGE-reranker | MaoField_base | MaoField_E |
|---|---:|---:|---:|---:|---:|---:|
| NFCorpus | 0.3063 | 0.1366 | 0.2401 | 0.3104 | 0.0565 | **0.2026** |
| SciFact | 0.6594 | 0.1920 | 0.4110 | 0.6223 | 0.0403 | **0.3002** |
| FiQA | 0.2167 | 0.0686 | 0.1163 | 0.2992 | 0.0294 | **0.1082** |
| ArguAna | 0.2838 | 0.0556 | 0.2085 | 0.4560 | 0.0289 | **0.1514** |
| TREC-COVID | 0.5589 | 0.4299 | 0.3962 | 0.7257 | 0.3553 | **0.4932** |

**Observations**:

1. MaoField_E vs S1 (byte baseline): 5/5 datasets positive gain, **+14.7% to +172.3%** relative improvement
2. MaoField_E vs BGE-reranker: 5/5 datasets lag behind SOTA by −10.8 to −32.2 pp
3. MaoField_E vs MaoField_base: consistent +7.9 to +26.0 pp improvement from removing fusion (see §4.3 below)
4. BGE-reranker underperforms BM25 on SciFact by −3.7 pp, confirming SOTA cross-encoders have weak domains

**Status**: MaoField_E represents a working PDE-based reranker, significantly above naïve byte baselines and below SOTA. This establishes the empirical envelope within which subsequent Block analyses operate.

---

## 4.3 Block II — Kuramoto diffusive coupling (H1 test)

**Hypothesis H1** (*movement to fusion*): Replacing explicit fusion with Kuramoto-type diffusive coupling `∂_t ψ_q = GL(ψ_q) + g·(ψ_d − ψ_q)` (co-evolving query and document fields for 2000 steps) should improve performance by ≥20%.

**Table 4.2**: `nDCG@10` at coupling-scan optimum `g_best`.

| Dataset | Pool | `g=0` | `g_best` | best `g` | Relative gain |
|---|---|---:|---:|---:|---:|
| NFCorpus | top-6 | 0.2201 | 0.2252 | 1.0 | +2.3% |
| NFCorpus | top-20 | 0.1712 | 0.1712 | 0.0 | 0.0% |
| SciFact | top-6 | 0.4082 | 0.4362 | 0.05 | +6.9% |
| SciFact | top-20 | 0.1836 | 0.2179 | 0.05 | **+18.7%** |

**H1 verdict (weak falsification)**: Maximum observed gain 18.7%, below the pre-registered 20% threshold. `g_c` does not coincide across datasets (NFC 1.0 vs SciFact 0.05). Coupling helps modestly but does not replace fusion as hypothesized.

**Independent confirmation from Block I**: MaoField_E (no fusion) outperforms MaoField_base (with fusion) by +7.9 to +26.0 pp. **Fusion actively degrades signal** on 5/5 datasets, consistent with the hypothesis that evolving query-document fields together erodes discriminative information.

---

## 4.4 Block III — Attractor enumeration (H2 test)

**Hypothesis H2** (*contradiction, primary/secondary, qualitative change*): The number of effective attractors `k*` is bounded and small; this explains the top-20 vs top-100 performance ceiling.

**Methodology**: For NFCorpus 100 docs, evolve each independently for 5000 steps with byte source, cluster final `(a, b)` fields via k-means over three representations. Select `k*` as the silhouette-optimal cluster count over `k ∈ {2,...,5}`.

**Table 4.3**: Silhouette-optimal attractor count.

| Representation | Dimension | `k*` | Silhouette |
|---|---:|---:|---:|
| `raw_ab` | 65536 | **2** | 0.214 |
| amplitude `|ψ|` | 32768 | **2** | 0.037 |
| phase `(cosφ, sinφ)` | 65536 | **2** | 0.223 |

**H2 verdict (confirmed, with statistical caveat)**: All three representations converge on `k*=2`. However, silhouette values `0.037–0.223` are weak-to-moderate; `< 0.25` is conventionally interpreted as "no substantial cluster structure." We thus claim `k*=2` as the **local silhouette optimum** rather than a strongly-separated attractor count. See §4.11 for open statistical questions.

The invariance of `k*=2` across representations motivates the Section 4.6 diagnostic: if amplitude and phase both give `k*=2`, the underlying symmetry-breaking mechanism may yet differ.

---

## 4.5 Block IV — Source-density × operator-symmetry (H3 test)

**Hypothesis H3** (*material starting point*): Under the same PDE operator, byte sources (materialist) and learned embedding sources (idealist) produce different attractor structures.

**Four-quadrant setup**: byte or BGE source × PDE-dynamic or static-cosine evaluation.

**Table 4.4**: `nDCG@10` and diagnostics across four quadrants.

| Dimension | Dataset | IV-A byte+PDE | IV-B BGE+PDE | IV-C BGE cos | IV-D byte cos |
|---|---|---:|---:|---:|---:|
| Overall `nDCG@10` | NFCorpus | 0.2026 | 0.2495 | **0.3089** | 0.2159 |
| Overall `nDCG@10` | SciFact | 0.3002 | 0.3814 | **0.6143** | 0.3555 |
| Overall `nDCG@10` | FiQA | 0.1082 | 0.1901 | **0.2774** | 0.1309 |
| Long-tail `nDCG@10` | NFC (n=227) | 0.2117 | 0.2608 | **0.3149** | 0.2264 |
| Long-tail `nDCG@10` | FiQA (n=29) | 0.1404 | 0.1551 | **0.2199** | 0.1341 |
| Robustness drop | SciFact ±200 | −0.010 | +0.011 | −0.015 | +0.031 |
| Attractor `k*` (raw-ab only)† | NFC 100 docs | **2** (sil 0.13) | **2** (sil 0.06) | N/A | N/A |

† These silhouette values are for the `raw_ab`-only clustering in a paired IV-A vs IV-B comparison on NFCorpus 100 docs; they are numerically lower than the Block III §4.4 triple-representation scan (`raw_ab` 0.214, `amplitude` 0.037, `phase` 0.223) because Block III reports each representation independently with per-representation optimization, while Block IV uses a common feature space to enable cross-source comparison. Both analyses confirm `k*=2`; only the silhouette magnitudes differ by cluster-space choice.

‡ SciFact long-tail (n=3) row omitted from this table due to insufficient sample; see `FINAL_REPORT.md` §2.4 for the raw numbers if needed.

**Observations**:

1. Overall ranking consistent across three datasets: `IV-C > IV-B > IV-D > IV-A`
2. Within-source-type: IV-A (byte+PDE) underperforms IV-D (byte cos) by −1.3 to −5.5 pp; IV-B (BGE+PDE) underperforms IV-C (BGE cos) by −5.9 to −23.3 pp
3. **`k*=2` holds in both IV-A and IV-B**, across source-density extremes
4. Robustness drops all `|Δ| < 0.04` — within noise

**H3 verdict (partial support)**: Source-density does affect retrieval scores but does **not** produce different `k*`. The surface-level `k*=2` identity across byte and BGE raises a mechanistic question: does the `Z_2` structure arise from the *same* or *different* symmetry breaking in the two source regimes? Stage C (§4.6) addresses this.

---

## 4.6 Stage C — Two regimes of `k*=2`

**Motivation**: `k*=2` holds for both byte and BGE sources. If the underlying mechanism differs, Stage C's phase diagnostic will resolve it.

### 4.6.1 Method

Compute for both IV-A and IV-B final states:
- Global phase circular mean resultant `|R|` (0 = uniform on S¹, 1 = full lock)
- Per-document `⟨|R|⟩` (average over documents of within-document phase concentration)
- 100-document circular-mean phases, k-means on sine/cosine, measure antipodal separation angle (expected 180° for pure `Z_2` phase inversion)

### 4.6.2 Results [STATIC]

**Table 4.5**: Phase diagnostic for IV-A vs IV-B.

|  | Global `|R|` | χ²/72 | Per-doc `⟨|R|⟩` | k-means centroid separation |
|---|---:|---:|---:|---:|
| **IV-A (byte)** | **0.807** | 94989.7 | **0.840** | **26.2°** (not antipodal) |
| **IV-B (BGE)** | 0.165 | 4879.9 | 0.197 | 81.4° (not antipodal) |

### 4.6.3 Interpretation [STATIC]

**IV-A (byte, sparse source)**: `⟨|R|⟩=0.84` indicates strong phase concentration within each document. The 100-document circular means fall into a narrow 26.2° fan. **The U(1) phase symmetry is empirically broken** in the sense that the observed `arg(ψ)` distribution is statistically distinguishable from uniform (χ² ≫ 1). However, the absence of antipodal separation (26° ≠ π rad) **rules out rigorous `Z_2 ⊂ U(1)` phase inversion** as the operative mechanism. The pattern is better described as "phase concentration to one preferred direction" — a broken U(1) without a surviving discrete subgroup.

**IV-B (BGE, dense source)**: `⟨|R|⟩=0.20` indicates much weaker phase concentration (still non-uniform; χ² = 4880 rejects uniformity strongly, but the phase modulation is weak relative to byte). Amplitude exhibits a bimodal distribution at `|ψ|∈{0,1}`. Note that `V=¼(|ψ|²−1)²` admits only `|ψ|=1` as a true minimum; `|ψ|=0` is a critical point with negative-definite Hessian (unstable fixed point, since `V(0)=¼ ≠ V(1)=0`). Hence `|ψ|=0` and `|ψ|=1` **do not lie on the same U(1) orbit** and cannot be interchanged by any `Z_2` group action respecting the potential. The "amplitude bistability" is a bimodal distributional pattern, not a strict `Z_2` amplitude symmetry breaking [^zn-loose].

### 4.6.4 `k*=2` in two regimes

The `k*=2` identity across IV-A and IV-B hides **two distinct distributional regimes**:

- Byte: phase concentration into a narrow fan; amplitude roughly unimodal
- BGE: amplitude bimodal at `|ψ|∈{0,1}`; phase weakly modulated

We label these "byte Z₁ regime" and "BGE Z₂ regime" in the loose sense of footnote [^zn-loose], but emphasize the labels are **distributional descriptors, not group-theoretic claims**. The empirical finding — that a single silhouette-optimal `k*=2` conceals two physically distinct mechanisms — is robust independent of labelling convention.

**Status**: H3 receives refined support. Source density does affect the *mechanism* of attractor structure while preserving the *count*.

---

## 4.7 Stage A1 — Multi-well amplitude intervention

**Intervention hypothesis**: If BGE's `k*=2` arises from amplitude bistability, introducing additional amplitude wells in `V` should increase `k*`.

**Setup**: Replace default `V=¼(|ψ|²−1)²` with triple-well `V(u) = u(u−1)²(u−4)²`, minima at `u = |ψ|² ∈ {0, 1, 4}` (i.e., `|ψ|∈{0, 1, 2}`). BGE-M3 embedding source, NFCorpus 100 docs (70 with cached embeddings), init `|ψ|_init ≈ 1.0 ± 0.3`, all other parameters matching IV-B.

**Stability**: 0 NaN, `u_max=1.20`, `u_mean=1.01`, 5000 steps fully stable.

### 4.7.1 Amplitude occupancy

**Table 4.6**: Observed occupancy across three wells.

| Well | `|ψ|` | `u=|ψ|²` | Observed occupancy |
|---|---|---|---:|
| Inner | 0 | 0 | **0.85%** |
| Middle | 1 | 1 | **99.15%** |
| Outer | 2 | 4 | **0.00%** |

The outer well is **not populated** under gradient flow from this initialization.

### 4.7.2 Barrier analysis [STATIC]

**Table 4.7**: Critical-point structure of the triple-well potential (independent SymPy verification).

| Point | `u` | `V` | `V''(u)` |
|---|---:|---:|---:|
| Min (boundary) | 0.0000 | 0.000 | — (linear `V≈4u`) |
| Saddle (inner) | 0.2958 | **2.013** | −31.41 |
| Min | 1.0000 | 0.000 | +18.00 |
| Saddle (outer) | **2.7042** | **13.187** | −26.59 |
| Min | 4.0000 | 0.000 | +72.00 |

**Barrier asymmetry**: `V(saddle outer) / V(saddle inner) = 13.187 / 2.013 = 6.55×`.

### 4.7.3 Gradient-flow inaccessibility of `u=4` [DYNAMIC-EQUILIBRIUM]

Under pure gradient flow (`γ · du/dt = −∂V/∂u`, first-order dissipative, **no kinetic-energy term**), `V` is monotonically non-increasing along trajectories. Initialization `u_init ∈ [0.49, 1.69]` lies **entirely within the basin of attraction of `u=1`** (inner saddle `u_s_in=0.296` is left of init range, outer saddle `u_s_out=2.704` is right). Hence no trajectory can reach the `u=4` basin under gradient flow alone. Observed `u_max=1.199` confirms.

For reference, the **static energy ratio** is `V(saddle outer) / V(u_init_max) = 13.187 / V(1.69) = 13.187 / 4.293 ≈ 3.07×`. Since gradient flow is monotonically non-increasing in V and `V(u_init_max) < V(saddle)`, the `u=4` basin is **analytically unreachable** under pure gradient flow — not an experimental surprise but a direct consequence of the static energy landscape geometry.

**A1 verdict**: Adding wells to `V` does not mechanically add attractors in the observed distribution. Populating the new wells requires either (i) initialization spanning multiple basins, (ii) a non-equilibrium mechanism (Langevin, Hamiltonian, active), or (iii) a structural change to `V` that brings the new minima into the gradient-connected region. This motivates Stage B1.

---

## 4.8 Stage B1 — Langevin σ-scan with Kramers timescale analysis

**Motivation**: Test whether adding isotropic Gaussian noise (`η(t)` with `⟨ηη*⟩ = σ²δ`) enables barrier crossing to the `u=4` basin.

**Setup**: same as A1 but with Langevin SDE `γ ∂_t ψ = −∂V/∂ψ* + S + η`. Scan `σ ∈ {0, 0.1, 0.5, 1.0, 2.0}`.

### 4.8.1 Observed occupancy

**Table 4.8**: Basin occupancy across σ-scan on triple-well `V = u(u-1)²(u-4)²`.

| σ | `u_max_all` | `u_mean_all` | near `u=0` | near `u=1` | near `u=4` | clamped |
|---|---:|---:|---:|---:|---:|---:|
| 0.0 | 1.19 | 1.01 | 0.8% | 99.2% | **0.0%** | 0.0% |
| 0.1 | 1.34 | 1.00 | 1.3% | 98.7% | **0.0%** | 0.0% |
| 0.5 | 18.00 | 0.17 | **85.0%** | 13.4% | **0.0%** | 0.0% |
| 1.0 | 18.00 | 17.21 | 1.9% | 1.8% | 0.0% | 95.4% |
| 2.0 | 18.00 | 18.00 | 0.0% | 0.0% | 0.0% | 100.0% |

### 4.8.2 Kramers timescale analysis [DYNAMIC-RARE-EVENT]

**Two-regime analytical framework**: we apply the Kramers rate formula for overdamped Langevin in 1D,

```
k_{i→j} = (1/(2π·γ))·√(V''(min_i) · |V''(saddle_ij)|) · exp(−ΔV_ij / T_eff)
```

valid when `ΔV/T_eff ≫ 1` (typically ≥ 5). The *expected number of crossings* over the simulation horizon `t_sim = steps · dt = 5000 · 0.05 = 250` is `k × t_sim`.

**Table 4.9**: Kramers analysis at σ=0.5 (`T_eff = 0.125`), triple-well `V`.

| Transition | ΔV | ΔV/`T_eff` | Prefactor | `k·t_sim` | Status |
|---|---:|---:|---:|---:|---|
| `u=1 → u=0` | 2.013 | **16.1** | ~3.4 | ~8·10⁻⁵ | Kramers marginal (inner barrier) |
| `u=1 → u=4` | 13.187 | **105.5** | ~3.5 | ~4·10⁻⁴³ | Kramers strongly valid, **43 orders below horizon** |

### 4.8.3 Reframe — *Langevin works for inner, fails for outer* (#7)

The σ=0.5 observation (85% `u=0`, 0% `u=4`) should be read as **two simultaneous outcomes under one noise level**:

1. **Inner barrier** (ΔV/T_eff = 16): Langevin-driven crossing is qualitatively observed. 85% of voxels transit from the `u=1` basin across the inner saddle to the `u=0` basin within `t_sim=250`. Note however that Kramers prediction gives only ~`8·10⁻⁵` expected crossings per voxel — an **observed/predicted ratio ≈ 1.1·10⁴ (i.e. about 4 orders of magnitude)** discrepancy between 1D-Kramers and observation (see §4.11).

2. **Outer barrier** (ΔV/T_eff = 105.5): Kramers escape time exceeds the simulation horizon by `log₁₀(exp(105.5) / 250) ≈ 43.4` — **~43 orders of magnitude** log-gap. The 0% `u=4` occupancy is a **finite-time rare-event obstruction**, not an equilibrium prohibition.

This reframes the original interpretation ("Langevin fails on A1") to a more precise dual statement:

> **Langevin succeeds where the simulation horizon is adequate for the Kramers timescale; it fails where the horizon is too short.** The apparent "failure" to populate `u=4` is a timescale mismatch, not a paradigm limitation.

**Implication for OP2**: resolving OP2 (populating distant attractors) requires either (a) **barrier-topology engineering** to bring Kramers timescales within horizon, or (b) **directed non-equilibrium driving** (Hamiltonian, active, anisotropic noise) to bypass the Kramers bottleneck entirely.

### 4.8.4 High-σ regime [DYNAMIC-IMPLEMENTATION]

At σ ≥ 1.0, the noise amplitude dominates the potential structure. Voxels random-walk to the clamp boundary `|ψ|=3` (i.e. `u=18`), producing `u_max=18` and `u_mean ≈ 17` at σ=2.0. This is **not a physical steady state** but a `[DYNAMIC-IMPLEMENTATION]` artifact of the explicit-Euler + clamp boundary condition combined with ΔV/T_eff ≤ 1. See §4.11 for methodological notes.

---

## 4.9 Stage A1.4 — OP2 three-fold co-design diagnostic

**Hypothesis**: If the outer barrier in A1 is too high for the simulation horizon, lowering it should restore Laplace equilibrium under moderate σ. Test via shifted potential `V_shifted(u) = u(u−1)²(u−2)²`, minima at `u∈{0,1,2}`, outer barrier reduced from 13.187 (A1) to `V(saddle u=1.540) = 0.095`.

**Setup**: same as A1 but with shifted `V`, σ-scan `{0, 0.1, 0.3, 0.5, 0.7}` + soft-wall experiments `V_wall = λ·max(0, u−u_max)⁴` with `λ ∈ {1, 10}`, `u_max=2.5`, and a `λ=1, σ=0.3` control.

**Laplace prediction at σ=0.5, T_eff=0.125** [DYNAMIC-EQUILIBRIUM]:

- `Z_0 = T/4 = 0.0313` (linear boundary basin `V≈4u` near `u=0`)
- `Z_1 = √(2πT/V''(1)) = √(πT) = 0.6267` (quadratic minimum `V''=2`)
- `Z_2 = √(2πT/V''(2)) = √(πT/2) = 0.4431` (quadratic minimum `V''=4`)

Normalization: `p_k = Z_k / Σ_j Z_j` with `Σ_j Z_j = 0.0313 + 0.6267 + 0.4431 = 1.1010`. Predicted occupancy: `p(0) ≈ 0.028, p(1) ≈ 0.569, p(2) ≈ 0.402` (sum = 1.000). Ratio `p(1)/p(2) = √2 ≈ 1.414` (wider basin has higher weight). Independent rejection-sampling on `(a,b) ∈ ℝ²` with 4·10⁶ points confirms this ratio.

### 4.9.1 σ-scan results

**Table 4.10**: Observed occupancy under σ-scan on shifted potential (70 docs × 32³ voxels = 2.3·10⁶ samples per σ).

| σ | `T_eff` | `u_max` | `u_mean` | p(0) | p(1) | p(2) | p(clamp) | Kramers regime |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 0.0 | — | 2.13 | 1.72 | 0.000 | 0.340 | **0.660** | 0.000 | (deterministic baseline) |
| 0.1 | 0.005 | 2.41 | 1.88 | 0.000 | 0.146 | **0.853** | 0.000 | frozen (k·H≈10⁻⁷) |
| 0.3 | 0.045 | 18.00 | 1.61 | 0.012 | 0.363 | 0.408 | 0.004 | partial (k·H≈10, outer marginal) |
| 0.5 | 0.125 | 18.00 | 9.90 | 0.054 | 0.246 | 0.041 | **0.525** | ΔV/T=0.76 < 1: **Kramers invalid** |
| 0.7 | 0.245 | 18.00 | 17.65 | 0.003 | 0.008 | 0.001 | **0.979** | ΔV/T=0.39 < 1: breakdown |
| — **Laplace** | | | | 0.028 | **0.569** | **0.402** | 0 | — |

**None of the σ values yield Laplace-consistent occupancy**. Specifically:

1. **σ=0 deterministic baseline** already deviates from Laplace: 66% `u=2` (not 40%) even with no noise. Gradient flow plus source driving alone suffices to disrupt equilibrium.
2. **σ=0.1**: 85% trapped in `u=2` basin. Below thermal mixing timescale (`k · t_sim ≈ 10⁻⁷` for inter-well rates).
3. **σ=0.3**: ratio `p(1)/p(2) = 0.363/0.408 = 0.89`, **reversed** from Laplace prediction `1.41`. Detailed-balance rate ratio `k_{12}/k_{21} = 0.704 ≈ 1/√2` is correct, but system has not thermalized (21% "in-between"; init bias and source drift exceed mixing within horizon).
4. **σ=0.5, 0.7**: noise exceeds potential confinement; 52% / 98% of voxels hit the clamp boundary at `u=18`.

### 4.9.2 Soft-wall intervention (walled experiments)

Adding `V_wall = λ·max(0, u−2.5)⁴` should confine voxels away from the clamp.

**Table 4.11**: Walled experiments at shifted potential.

| λ | σ | `u_mean` | p(u=1) | p(u=2) | p(clamp) | Δ(clamp) vs no-wall |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 0.5 | 10.04 | 0.242 | 0.040 | 0.534 | +0.9 pp (no help) |
| 10 | 0.5 | 11.04 | 0.209 | 0.031 | **0.593** | **+6.8 pp (worse)** |
| 1 | 0.3 (control) | 1.62 | 0.363 | 0.407 | 0.005 | +0.1 pp (wall passive) |

**Walls of this form do not restore Laplace equilibrium**. The σ=0.3 control confirms the wall is appropriately passive when not needed (wall active fraction 0.75%).

### 4.9.3 Three-fold diagnosis

Decomposition of why the intervention fails:

#### Axis A — Source statistics [DYNAMIC-IMPLEMENTATION]

BGE embedding's imaginary component has a **statistically extreme non-zero mean**:

- Per-doc mean of 512 `Sb` components across 70 docs: `⟨Sb⟩ = −1.48·10⁻³`, `std = 7.2·10⁻⁴`
- 1-sample t-test: `t = −17.12, p < 10⁻²⁵`
- For `Sa`: `t = 0.62, p = 0.54` (consistent with zero)

A nonzero mean of `S` implies the force `−∇V + S` is **not pure-gradient** (or at least cannot take Boltzmann form without modification); detailed balance is broken, and the system evolves toward a non-equilibrium steady state (NESS) rather than a Boltzmann distribution.

Cumulative forcing scale: `|S|·t_sim ~ 0.1 · 250 = 25`, far exceeding the shifted outer barrier `ΔV_outer = 0.095`. Deterministic source-pull across the outer saddle is energetically available even at σ=0. The σ=0 baseline observation (66% `u=2`) confirms this mechanism operates *without any noise contribution*.

#### Axis B — Potential tail geometry [STATIC]

Shifted `V(u)` scales as `u⁵` for large `u` (equivalently `|ψ|¹⁰` in ψ-space; two polynomial orders shallower than A1 original `u⁹`/`|ψ|¹⁸`). For `σ=0.5`, per-step noise displacement is `σ√dt = 0.112` in `(a, b)` coordinates, producing per-step `Δu ≈ 2|ψ|·0.112 ≈ 0.22` near basins. The `u⁵` tail restoring force exceeds this only in a narrow band `u ∈ [2, 3]`; beyond, `dt·|f|` overshoots and voxels random-walk to the clamp.

Soft wall `V_wall = λ·(u−u_max)⁴` is `C³`-smooth at `u=u_max` — `V=V'=V''=V'''=0`, `V''''=24λ`. Wall force at `u=2.6` is only `4λ·(0.1)³ = 4·10⁻³·λ` (essentially zero); voxels transit the `u ∈ [u_max, u_max + δ]` region in `O(δ/σ√dt) ~ 5` steps without appreciable deceleration before reaching the clamp at `u=18`.

#### Axis C — Numerical scheme [DYNAMIC-IMPLEMENTATION]

Explicit Euler stability requires `dt·|J| < 2`, where `J` is the local Jacobian spectral radius.

At `u=10, a²=b²=5` (isotropic case), for `V_wall = λ·(u−2.5)⁴`:
- `f_wall(u) = λ · 4 · (7.5)³ = 1687.5·λ`
- `f'_wall(u) = λ · 12 · (7.5)² = 675·λ`
- 2×2 block `[[J11=2a²·f' + f, J12=2ab·f'], [J12, J22=2b²·f' + f]]`
- At `a²=b²=5`: `J_max = (2a²·f'+f) + 2ab·f' = 8437.5 + 6750 = 15187.5·λ`

Hence:
- λ=1: `J ≈ 1.5·10⁴`, `dt_max ≈ 1.3·10⁻⁴`, experimental `dt=0.05` exceeds stability by **~380×**
- λ=10: `J ≈ 1.5·10⁵`, `dt_max ≈ 1.3·10⁻⁵`, exceeds by **~3800×**

This **directly explains** why the stronger wall (`λ=10`) *worsens* clamp residency: larger Jacobian violates CFL more severely; the clamp absorbs the instability. Explicit Euler at `dt=0.05` is fundamentally incompatible with any meaningful wall stiffness in this geometry.

#### Axes are coupled

**No single-axis fix restores Laplace** (verified by elimination):

| Fix axis | Remaining obstruction |
|---|---|
| Source whitening only | Potential tail still `u⁵`; integrator still CFL-violating at σ=0.5 |
| Potential shape only (deeper tail) | Source drift still breaks DB; stiffer potential worsens integrator stability |
| Integrator only (implicit) | Source drift still `17σ` from mean-zero; shallow tail still allows escape |

A1.4 **refines** OP2 from a single-axis barrier-engineering problem to a three-axis co-design problem. The three axes are empirically orthogonal in the sense that each is an independent necessary (not sufficient) condition for Laplace equilibrium under this class of physics setup.

### 4.9.4 A1.4 verdict

A1.4 is best read as a **diagnostic refinement**, not a success/failure binary:

- It **falsifies** the naive interpretation "lowering barriers alone enables OP2 access"
- It **does not falsify** the broader OP2 program, which still admits joint source/potential/integrator co-design (Block V Phase A)
- It **does falsify** the specific instance (shifted potential + explicit Euler + BGE raw source + simple soft wall)
- It provides three orthogonal engineering targets for future work

**Explicitly not claimed**: (i) OP2 is unsolvable, (ii) the Allen-Cahn framework is broken (σ=0 baseline confirms internal dynamics are correct), (iii) BGE embeddings are unsuitable (only their raw use as source; whitening or gradient-projection may restore suitability).

Full details in [`block4_5/a1_4/VERDICT.md`](block4_5/a1_4/VERDICT.md).

---

## 4.10 Two-regime analytical framework

The preceding Block IV.5 analyses make explicit use of a **two-regime dichotomy** for occupancy prediction:

**Regime 1 — Rare-event (Kramers) limit** (`ΔV/T_eff ≫ 1`):
- Occupancy evolves slowly via barrier crossings
- Relevant quantity: `k·t_sim` (expected number of crossings)
- Applicable: A1 outer barrier at σ=0.5 (`ΔV/T = 105.5`, `k·t_sim ≈ 4·10⁻⁴³` → 0 crossings)

**Regime 2 — Thermalized (Laplace) limit** (`ΔV/T_eff ≲ few`, system fully mixes within `t_sim`):
- Occupancy given by equilibrium Boltzmann partition function
- `p_k ∝ Z_k = √(2πT/V''(u_k))` for quadratic minima; boundary basins require case-by-case treatment (e.g., linear-V gives `Z ∝ T/|V'(0+)|`)
- Applicable: A1.4 at σ=0.5 if detailed balance held (which it does not, per §4.9.3)

**Regime selection is dictated by the dimensionless quantity `ΔV/T_eff`**, not by modeling choice. Boundary regimes (`ΔV/T_eff ∈ [1, 5]`) require either longer simulation or explicit Kramers-prefactor measurement. For `ΔV/T_eff ≤ 1`, Kramers formula is invalid and system dynamics approach free diffusion with weak potential modulation — in the presence of boundary clamps, this produces `[DYNAMIC-IMPLEMENTATION]` artifacts rather than physical steady states.

Both regimes assume `⟨S⟩ = 0` (mean-zero source) and standard Boltzmann form. **§4.9.3 Axis A shows BGE violates this assumption by `17σ`** — a systematic caveat applicable to all MaoField experiments in this paper that use raw BGE embeddings as source.

---

## 4.11 Open methodological questions

### 4.11.1 A1 inner barrier ~10⁴ Kramers-observation discrepancy

In §4.8.3, the 1D Kramers prefactor for `u=1 → u=0` gave `k·t_sim ≈ 8·10⁻⁵` expected crossings per voxel, while observation shows 85% of voxels have crossed. The ratio between prediction and observation is **factor ~10⁴ (i.e. ~4 orders of magnitude)**, not 10^10000.

Candidate explanations (not tested):
1. **1D Kramers prefactor underestimates** escape rate in 3D field-theoretic setting due to collective voxel-voxel interactions (the voxels are coupled through the Laplacian `D∇²ψ`). To our knowledge, no closed-form field-theoretic Kramers analog is tabulated for this geometry; empirical calibration via σ-scan is the most direct route.
2. **Boundary basin at `u=0`** has linear-V attractor `V≈4u` rather than quadratic; standard Kramers prefactor derivation assumes quadratic saddles and quadratic minima
3. `ΔV/T_eff = 16` is marginal: although above the conventional `≥ 5` threshold for Kramers validity, the *absolute calibration* of the 1D prefactor in 3D lattice field theory is not established in the literature we surveyed

**Status**: flagged as an open methodological question. The **qualitative conclusion** (outer barrier unreachable at `~43 orders` log-gap) is robust regardless, but quantitative rate matching for lower barriers requires further work — either empirical prefactor measurement from σ-scan, or derivation of a field-theoretic Kramers analog.

### 4.11.2 Silhouette values `< 0.25`

Block III's `k*=2` finding rests on silhouette coefficients `0.037–0.223`, below the conventional `0.25` threshold for "substantial cluster structure". We report `k*=2` as the *local* silhouette optimum rather than as a strongly-separated attractor count. Future work should use alternative cluster-validation metrics (gap statistic, bootstrap-stability) and ideally persistent-homology diagnostics to distinguish between "truly k-cluster structure" and "k-optimum of weakly-structured point cloud".

### 4.11.3 Finite-lattice caveat

All SSB-like claims in this paper hold in the *empirical distributional sense* on a 32³ lattice within finite simulation horizons. Strict-sense spontaneous symmetry breaking requires thermodynamic-limit treatments (Section 3.5; footnote [^zn-loose]). The pattern separation observed at N=32³ is suggestive of mechanism but does not constitute proof of symmetry-sector existence in the Anderson-Goldstone-Nambu sense.

### 4.11.4 Missing controls

The following ablations were not performed and would strengthen the empirical case:
1. σ=0 gradient-flow-only experiments for *every* σ-scan (not just A1.4)
2. Source whitening (`Sb − ⟨Sb⟩`) baseline to separate drift from mixing effects
3. Integrator-convergence test with `dt=0.01` to rule out numerical artifacts in σ-scan regimes
4. mMARCO cross-lingual runs (original H3 dimension, currently SKIPPED due to download failure)

---

## 4.12 Experimental status summary

**Confirmed** (empirical evidence supports):

- [H1 falsified, weak] Kuramoto coupling improves retrieval by max `+18.7%`, below the 20% threshold
- [H2 confirmed, statistically weak] `k*=2` across three representations and two source types
- [H3 partially confirmed] Source density affects the mechanism (byte vs BGE regimes) while preserving `k*`
- [Fusion] Explicit query-document fusion degrades signal by `+7.9 to +26.0 pp` across 5 datasets

**Refined open problems**:

- [OP1] M2 iteration (Axiom 6 candidate) falsified in prior work; Axiom 6 formalization remains open
- [OP2] Reframed from "non-equilibrium extensions needed" to **three-fold co-design**: source statistics (mean-zero or NESS treatment), potential geometry (confining tail + stability-compatible shape), numerical scheme (implicit or sub-CFL-dt for stiff terms). A1.4 diagnostic supplies all three axes; Block V Phase A is scheduled to test them jointly.

**Methodological** (see §4.11):

- A1 inner barrier Kramers prediction differs from observation by factor ~10⁴
- Silhouette values support `k*=2` only in local-optimum sense
- BGE raw source violates mean-zero assumption of Laplace framework

---

*Section 4 first draft. Written: 2026-04-14. Review: spawn paper-review subagent on `REVIEW_ARXIV_SECTION4.md`. Cross-review with Win Claude required before integration.*

[^zn-loose]: See Section 3.5 (`[^zn-loose]` footnote) for full text. Summary: `Z_n` labels in this paper denote **empirical distributional remaining-symmetry patterns**, not rigorous group actions on a thermodynamically-broken vacuum. Strict SSB requires (1) group `G` acting on field space, (2) `V` invariant under `G`, (3) ground-state manifold is `G`-orbit, (4) non-trivially-transforming order parameter `⟨ψ⟩ ≠ 0`, (5) thermodynamic limit `N → ∞`. Conditions (3)–(5) are not verified on our `N=32³` lattice; `Z_n` is a compact descriptor for convenience.
