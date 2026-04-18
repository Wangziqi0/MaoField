# arXiv v1 Figures & Captions (T7 preliminary)

*Linux Claude, 2026-04-14. For arXiv v1 figure placement. Captions drafted; LaTeX conversion (T6) deferred to Win/一凡.*

---

## Figure assignment

### §4.4 Block III — Attractor enumeration

**Fig 4.4** `fig4_4_block3_basin.png`
Basin visualization for NFCorpus 100 documents under byte source + standard double-well potential. Three representations (raw_ab, amplitude, phase cos/sin) independently converge on `k*=2` with silhouette 0.214 / 0.037 / 0.223 respectively. Weak-to-moderate cluster separation (all < 0.25); see §4.11.2 for methodological caveats.

### §4.6 Stage C — Phase diagnostic (two source-density regimes)

**Fig 4.6** `fig4_6_stageC_phase_diag.png`
Phase distribution for IV-A (byte) vs IV-B (BGE) 100-document runs. Top: per-document phase concentration `|R|` distribution — byte `⟨|R|⟩=0.84` (strong concentration, narrow 26° fan) vs BGE `⟨|R|⟩=0.20` (near-uniform, 81° separation). Bottom: k-means cluster separation on 100-document circular means — byte two-center 26.2° (not antipodal) vs BGE 81.4° (not antipodal either). See §4.6.3 for interpretation ([^zn-loose]).

### §4.7 Stage A1 — Multi-well amplitude intervention

**Fig 4.7a** `fig4_7_a1_amp_hist.png`
Amplitude `|ψ|` histogram for 70 documents × 32³ voxels under triple-well potential `V = u(u-1)²(u-4)²` (minima at u ∈ {0, 1, 4}). 99.15% of voxels at |ψ|≈1, 0.85% at |ψ|=0, **0.00% at |ψ|=2 (u=4 basin)**. `u_max=1.199` confirms no trajectory escapes u=1 basin under pure gradient flow.

**Fig 4.7b** `fig4_7_a1_phase_diag.png`
Phase diagnostic for Stage A1 vs control IV-B (both BGE source). Adding amplitude wells does not induce phase degeneracy: global `|R|=0.159` (A1) vs `0.165` (IV-B); per-doc `⟨|R|⟩=0.185` vs `0.197`.

### §4.8 Stage B1 — Langevin σ-scan

**Fig 4.8** `fig4_8_b1_sigma_scan.png`
Amplitude histograms across σ ∈ {0, 0.1, 0.5, 1.0, 2.0} on A1 triple-well potential. σ=0.1 frozen (98.7% u=1). σ=0.5 Langevin-driven inner-barrier crossing gives 85% u=0 (qualitative Kramers behavior, though quantitative rate differs from 1D prediction by factor ~10⁴ — §4.11.1). σ ≥ 1.0 noise overwhelms potential → clamp boundary artifact.

### §4.9 Stage A1.4 — OP2 three-fold co-design diagnostic

**Fig 4.9a** `fig4_9_a1_4_shifted_barrier.png`
Comparison of A1 original potential `V=u(u-1)²(u-4)²` (outer barrier 13.187 at u=2.704) vs A1.4 shifted `V=u(u-1)²(u-2)²` (outer barrier 0.095 at u=1.540). Static energy ratio reduced by factor ~140. Hessian structure at minima: `V''(1)=2, V''(2)=4` (shifted) vs `V''(1)=18, V''(4)=72` (original).

**Fig 4.9b** `fig4_9b_sigma0p5_u_hist.png`
Observed `u=|ψ|²` distribution at σ=0.5 on shifted potential (log scale) vs Laplace equilibrium prediction. Massive deviation: 52.5% clamp residency at u=18 vs Laplace prediction 0%. Marks the origin point of the three-fold co-design refinement.

**Fig 4.9c** `fig4_9c_sigma_scan_occupancy.png`
Basin occupancy vs σ stacked bar chart. σ=0 baseline 66% u=2 (deterministic drift, no noise needed). σ=0.3 partial mixing (36% u=1 / 41% u=2 / 21% in-between). σ=0.5+ progressive clamp dominance. Observed never matches Laplace `(0.028, 0.569, 0.402)` at any σ, motivating three-axis diagnosis.

### §5.3 Block V Phase A — Potential design candidates

**Fig 5.2** `fig5_2_zn_angular_slices.png`
Illustrative Z_n angular potential slices (Mexican hat + `Re(Cψⁿ)` term) for n ∈ {3, 4, 6}, showing the n discrete minima on `|ψ|=v` orbit and angular saddle structure. Candidate for Block V Phase A-2 potential-design axis; see `BLOCK_V_DESIGN.md` §2.3 for full mathematical analysis.

---

## LaTeX conversion (T6, deferred)

All figures are in PNG format, resolution 130 dpi, suitable for arXiv submission via `\includegraphics`. Conversion to LaTeX format:

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=0.8\textwidth]{fig4_9b_sigma0p5_u_hist.png}
  \caption{Observed $u=|\psi|^2$ distribution at $\sigma=0.5$ on the shifted
  potential vs Laplace equilibrium prediction. Log-scale y-axis. The 52.5\%
  clamp residency at $u=18$ (vs Laplace prediction 0\%) motivates the
  three-fold co-design refinement of OP2 in §5.2.}
  \label{fig:sigma0p5-u-hist}
\end{figure}
```

Deferred to Win/一凡 for final arXiv LaTeX assembly.
