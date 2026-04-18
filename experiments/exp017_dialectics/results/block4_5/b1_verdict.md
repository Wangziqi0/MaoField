# Block IV.5 Stage B1: Langevin σ Scan — Results

## Config
- A1 multi-well potential V = |ψ|²(|ψ|²−1)²(|ψ|²−4)²
- BGE-M3 embedding source (20 NFC docs, same as Stage A1 subset)
- DT=0.05, steps=5000, clamp_hi=3.0, init |ψ|≈1.0±0.3
- σ ∈ {0.0, 0.1, 0.5, 1.0, 2.0}

## Occupancy table (% of voxels within basin boundary)

| σ | u_max_all | u_mean_all | near u=0 | near u=1 | **near u=4** | clamped |
|---|---|---|---|---|---|---|
| 0.0 | 1.19 | 1.01 | 0.8% | 99.2% | **0.0%** | 0.0% |
| 0.1 | 1.34 | 1.00 | 1.3% | 98.7% | **0.0%** | 0.0% |
| 0.5 | 18.00 | 0.17 | 85.0% | 13.4% | **0.0%** | 0.0% |
| 1.0 | 18.00 | 17.21 | 1.9% | 1.8% | **0.0%** | 95.4% |
| 2.0 | 18.00 | 18.00 | 0.0% | 0.0% | **0.0%** | 100.0% |

## Data-layer observations (no philosophy)

- σ=0 (pure gradient flow): u=1 basin dominates at 99.2%; u=4 basin occupancy 0.0% (reproduces Stage A1 finding).
- σ=0.1 (weak noise): u=1 98.7% (Δ-0.5pp); u=4 0.0%. Noise too weak to cross barrier V≈13.2.
- σ=0.5 (moderate noise): u=1 collapses to 13.4%; u_max_all=18.0 hits clamp ceiling; bulk of voxels (85.0% at u=0) scattered. NOT a clean u=1↔u=4 transition.
- σ=1.0: u_mean_all=17.2 near clamp ceiling (|ψ|²≈18); 95.4% voxels clamped. System entirely dominated by noise, potential structure is erased.
- σ=2.0: u_mean_all=18.0 near clamp ceiling (|ψ|²≈18); 100.0% voxels clamped. System entirely dominated by noise, potential structure is erased.

## Barrier asymmetry diagnostic (key insight)

V(u) = u(u−1)²(u−4)² has two barriers originating from u=1 basin:

| Direction | Barrier location | Barrier height |
|---|---|---|
| u=1 → u=0 | u ≈ 0.296 | V ≈ **2.0** |
| u=1 → u=4 | u ≈ 2.704 | V ≈ **13.2** |

**Ratio ~ 6.55×** (precise analytic: 13.187/2.013). The σ=0.5 result makes this asymmetry visible through the Kramers lens:

- Overdamped Langevin `γ ∂_t ψ = −∂V/∂ψ* + η`, `⟨η η*⟩ = σ²δ`; stationary Gibbs distribution at effective temperature `T_eff = σ²/(2γ) = σ²/2` (γ=1 normalization). **No kinetic-energy concept** in first-order dissipative dynamics.
- Kramers inter-basin escape rate `k ∝ exp(−ΔV/T_eff)`:
  - **u=1 → u=0** (inner, ΔV=2.013): `ΔV/T_eff = 16.1`, `exp(−16.1) ≈ 1.0×10⁻⁷`. Note `u_init ∈ [0.49, 1.69] ⊂ basin-of-attraction(u=1)` (inner saddle u_s_in=0.296 lies *left* of init range, not inside it), so gradient flow alone cannot reach u=0. The observed 85% u=0 occupancy at σ=0.5 is therefore **Langevin-driven Kramers crossing** of the inner barrier, amortized over 32³ voxels × 5000 steps.
  - **u=1 → u=4** (outer, ΔV=13.187): `ΔV/T_eff = 105.5`, `exp(−105.5) ≈ 5×10⁻⁴⁶`. Kramers escape time exceeds horizon by **~43 orders of magnitude** → u=4 strictly unreachable in t_sim=250.

**Physical reading**: isotropic Langevin noise gives Boltzmann-like Kramers rates; asymmetric barriers mean inner basin (u=0) is Kramers-reachable at σ=0.5 while outer basin (u=4) is not. Increasing σ to compensate 44-orders-of-magnitude gap requires σ² such that σ²/2 ~ 13.2/ln(N·t·volume), but the lattice clamp at |ψ|²=18 hits first.

## Verdict against OP2 hypothesis

**H_OP2_Langevin**: Adding Langevin noise to gradient flow should populate the u=4 basin unreachable under pure gradient flow.

**Result**: No σ in tested range yields clean u=4 basin occupancy (>1%).
- σ ≤ 0.1: too weak → stuck in u=1 basin (expected, V_barrier≈13.2 > noise kinetic ~σ²·dt = 0.0005)
- σ ≥ 0.5: too strong → field explodes to clamp ceiling (|ψ|²≈18, unphysical) rather than populating u=4
- No 'Goldilocks zone' found in tested σ range where tunneling is clean.

**Interpretation (data-layer only, no philosophy)**: 
Naive Langevin on top of gradient flow in this V(ψ) is unlikely to realize 'ascent phase' of dialectical motion cleanly. The potential landscape is too steep (V grows as |ψ|^10 far from wells) — noise either insufficient or destructive, no balanced regime.

## Implications for Block V design

1. **Langevin alone is NOT OP2 answer** — not in this V(ψ) form. Options:
   - Redesign V(ψ) with lower barriers (e.g., wells at u∈{0,1,2} instead of {0,1,4})
   - Combine with active driving or Hamiltonian structure
   - Use metadynamics / adaptive biasing to flatten barrier
2. **The triple-well A1 potential V ~ |ψ|^10 may be unsuitable** for noise-based exploration — too steep. A1.4 shifted minima u∈{0,1,2} (from FINAL_REPORT §3.2 future directions) has V ~ |ψ|^6, may be more noise-tolerant.
3. This result argues for **V.3-H (Hamiltonian)** or **V.3-A (structured active driving)** as more promising Q2 candidates than naive Langevin.

**Overall**: Stage B1 provides a concrete data point supporting the claim 'gradient flow + simple noise ≠ OP2'. The ascending phase requires more structured non-equilibrium mechanisms.

---

## Decision points for em × Win [?]

1. Is this result enough to rule out Langevin route entirely, or should we retry on lower-barrier potential (A1.4, u∈{0,1,2})?
2. Should Block V shift V.3-L priority down (currently 1st) and elevate V.3-H (Hamiltonian)?
3. Does this support reframing OP2 from 'add noise' to 'restructure barrier topology'?