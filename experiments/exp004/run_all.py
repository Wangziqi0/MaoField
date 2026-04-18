"""
MaoField Exp004: Run Experiments B-E
=====================================

B: Single text injection → different patterns?
C: Quantitative vs qualitative change
D: Iterative fusion (same domain = faster?)
E: Multi-scale spectral analysis
"""

import numpy as np
import json
import time
import os

from simulator_ac import AllenCahn3D
from source import build_source_physical as build_source, TEXTS, QUERY_TEXTS, EXP_C, EXP_E
from fusion import evolve_text_to_steady, iterative_fusion
from config import SNAPSHOTS_DIR, ANALYSIS_DIR

D = 0.1
DT = 0.1
DX = 1.0
N = 32
STEPS = 5000


def field_stats(u):
    return {
        "pos_frac": float((u > 0.5).mean()),
        "neg_frac": float((u < -0.5).mean()),
        "wall_frac": float((np.abs(u) < 0.5).mean()),
        "mean": float(u.mean()),
        "std": float(u.std()),
    }


def spectral_analysis(u, grid_size=N):
    """3D FFT power spectrum, split into frequency bands"""
    F = np.fft.fftn(u)
    P = np.abs(F) ** 2

    # Frequency magnitude grid
    freqs = np.fft.fftfreq(grid_size)
    kx, ky, kz = np.meshgrid(freqs, freqs, freqs, indexing='ij')
    k_mag = np.sqrt(kx**2 + ky**2 + kz**2)

    # Frequency bands
    low = k_mag < 4.0 / grid_size
    mid = (k_mag >= 4.0 / grid_size) & (k_mag < 10.0 / grid_size)
    high = k_mag >= 10.0 / grid_size

    return {
        "low": float(P[low].sum()),
        "mid": float(P[mid].sum()),
        "high": float(P[high].sum()),
        "total": float(P.sum()),
        "P": P,
    }


def spectral_correlation(P1, P2, mask):
    """Correlation of power spectra in a frequency band"""
    a = P1[mask].flatten()
    b = P2[mask].flatten()
    ac = a - a.mean()
    bc = b - b.mean()
    num = np.dot(ac, bc)
    den = np.sqrt(np.dot(ac, ac) * np.dot(bc, bc))
    return float(num / (den + 1e-15))


# ── Experiment B ──

def experiment_b():
    print("\n" + "=" * 60)
    print("EXPERIMENT B: Single Text Injection")
    print("=" * 60)

    results = {}
    fields = {}

    for name, text in TEXTS.items():
        print(f"\n  --- {name}: '{text}' ---")
        S = build_source(text, N)
        u_final, sim = evolve_text_to_steady(S, D=D, dt=DT, dx=DX, grid_size=N, max_steps=STEPS)
        stats = field_stats(u_final)
        print(f"  +1={stats['pos_frac']:.1%} -1={stats['neg_frac']:.1%} wall={stats['wall_frac']:.1%} std={stats['std']:.4f}")

        fields[name] = u_final
        results[name] = {"text": text, **stats}
        np.save(os.path.join(SNAPSHOTS_DIR, f"exp_b_{name}.npy"), u_final)

    # Cross-compare: are different texts distinguishable?
    print("\n  Cross-field distances:")
    names = list(fields.keys())
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            d = np.sqrt(np.mean((fields[names[i]] - fields[names[j]])**2))
            c = np.corrcoef(fields[names[i]].flat, fields[names[j]].flat)[0, 1]
            print(f"    {names[i]:16s} vs {names[j]:16s}: dist={d:.4f} corr={c:.4f}")

    return results, fields


# ── Experiment C ──

def experiment_c():
    print("\n" + "=" * 60)
    print("EXPERIMENT C: Quantitative vs Qualitative Change")
    print("=" * 60)

    # Step 1: Base "离婚" to steady state
    S_base = build_source(EXP_C["base"], N)
    u_base, _ = evolve_text_to_steady(S_base, D=D, dt=DT, dx=DX, grid_size=N, max_steps=STEPS)
    stats_base = field_stats(u_base)
    print(f"\n  Base '{EXP_C['base']}': +1={stats_base['pos_frac']:.1%} -1={stats_base['neg_frac']:.1%}")

    # Step 2: Quantitative context
    S_quant = build_source(EXP_C["quant"], N)
    sim_q = AllenCahn3D(grid_size=N, D=D, dt=DT, dx=DX)
    sim_q.u = u_base.copy()
    sim_q.S = S_quant  # Full text source (includes base)
    if sim_q.S.max() > 0:
        sim_q.S = sim_q.S / sim_q.S.max()
    sim_q.run(STEPS, snapshot_interval=STEPS, verbose=False)
    stats_quant = field_stats(sim_q.u)
    print(f"  + '{EXP_C['quant']}': +1={stats_quant['pos_frac']:.1%} -1={stats_quant['neg_frac']:.1%}")

    # Step 3: Qualitative context
    S_qual = build_source(EXP_C["qual"], N)
    sim_ql = AllenCahn3D(grid_size=N, D=D, dt=DT, dx=DX)
    sim_ql.u = u_base.copy()
    sim_ql.S = S_qual
    if sim_ql.S.max() > 0:
        sim_ql.S = sim_ql.S / sim_ql.S.max()
    sim_ql.run(STEPS, snapshot_interval=STEPS, verbose=False)
    stats_qual = field_stats(sim_ql.u)
    print(f"  + '{EXP_C['qual']}': +1={stats_qual['pos_frac']:.1%} -1={stats_qual['neg_frac']:.1%}")

    # Analysis
    quant_shift = abs(stats_quant['pos_frac'] - stats_base['pos_frac'])
    qual_shift = abs(stats_qual['pos_frac'] - stats_base['pos_frac'])
    print(f"\n  Quantitative shift: {quant_shift:.4f}")
    print(f"  Qualitative shift:  {qual_shift:.4f}")
    print(f"  Ratio (qual/quant): {qual_shift/(quant_shift+1e-10):.2f}x")

    return {
        "base": stats_base,
        "quantitative": stats_quant,
        "qualitative": stats_qual,
        "quant_shift": float(quant_shift),
        "qual_shift": float(qual_shift),
    }


# ── Experiment D ──

def experiment_d():
    print("\n" + "=" * 60)
    print("EXPERIMENT D: Iterative Fusion (Same vs Cross Domain)")
    print("=" * 60)

    # Evolve each to steady state
    S_query = build_source(QUERY_TEXTS["query_hit"], N)
    S_match = build_source(QUERY_TEXTS["doc_match"], N)
    S_mismatch = build_source(QUERY_TEXTS["doc_mismatch"], N)
    print(f"  Source field stats:")
    print(f"    query nnz={(S_query>0.01).sum()}, match nnz={(S_match>0.01).sum()}, mismatch nnz={(S_mismatch>0.01).sum()}")

    print("\n  Evolving query '他打我怎么判'...")
    u_query, _ = evolve_text_to_steady(S_query, D=D, dt=DT, dx=DX, grid_size=N, max_steps=STEPS)

    print("  Evolving doc_match '故意伤害他人身体处三年以下'...")
    u_match, _ = evolve_text_to_steady(S_match, D=D, dt=DT, dx=DX, grid_size=N, max_steps=STEPS)

    print("  Evolving doc_mismatch '解除劳动合同经济补偿'...")
    u_mismatch, _ = evolve_text_to_steady(S_mismatch, D=D, dt=DT, dx=DX, grid_size=N, max_steps=STEPS)

    # Fusion: query + match
    print("\n  Fusing query + matching doc:")
    rounds_m, energy_m, hist_m = iterative_fusion(
        u_query.copy(), u_match.copy(), S_query, S_match,
        D=D, dt=DT, dx=DX, grid_size=N, verbose=True)

    # Fusion: query + mismatch
    print("\n  Fusing query + mismatching doc:")
    rounds_mm, energy_mm, hist_mm = iterative_fusion(
        u_query.copy(), u_mismatch.copy(), S_query, S_mismatch,
        D=D, dt=DT, dx=DX, grid_size=N, verbose=True)

    print(f"\n  === Result ===")
    print(f"  Match:    {rounds_m} rounds, E={energy_m:.1f}")
    print(f"  Mismatch: {rounds_mm} rounds, E={energy_mm:.1f}")
    if rounds_m < rounds_mm:
        print(f"  ✓ Match fuses FASTER ({rounds_m} < {rounds_mm})")
    elif rounds_m > rounds_mm:
        print(f"  ✗ Mismatch fuses faster ({rounds_mm} < {rounds_m})")
    else:
        print(f"  = Same rounds, checking energy...")
        if energy_m < energy_mm:
            print(f"  ✓ Match has LOWER energy ({energy_m:.1f} < {energy_mm:.1f})")
        else:
            print(f"  ✗ No discrimination")

    return {
        "match": {"rounds": rounds_m, "energy": float(energy_m), "history": [float(e) for e in hist_m]},
        "mismatch": {"rounds": rounds_mm, "energy": float(energy_mm), "history": [float(e) for e in hist_mm]},
        "correct": rounds_m < rounds_mm or (rounds_m == rounds_mm and energy_m < energy_mm)
    }


# ── Experiment E ──

def experiment_e():
    print("\n" + "=" * 60)
    print("EXPERIMENT E: Multi-Scale Spectral Analysis")
    print("=" * 60)

    # Evolve all texts
    fields = {}

    for name, text in EXP_E.items():
        S = build_source(text, N)
        u, _ = evolve_text_to_steady(S, D=D, dt=DT, dx=DX, grid_size=N, max_steps=STEPS)
        fields[name] = u
        print(f"  {name}: +1={(u>0.5).mean():.1%} -1={(u<-0.5).mean():.1%}")

    # Spectral analysis
    spectra = {name: spectral_analysis(u) for name, u in fields.items()}

    # Frequency grid for band masks
    freqs = np.fft.fftfreq(N)
    kx, ky, kz = np.meshgrid(freqs, freqs, freqs, indexing='ij')
    k_mag = np.sqrt(kx**2 + ky**2 + kz**2)
    low = k_mag < 4.0 / N
    mid = (k_mag >= 4.0 / N) & (k_mag < 10.0 / N)
    high = k_mag >= 10.0 / N

    # Same-domain pair: criminal_1 vs criminal_2
    print("\n  Same-domain (criminal_1 vs criminal_2):")
    for band_name, mask in [("low", low), ("mid", mid), ("high", high)]:
        corr = spectral_correlation(spectra["criminal_1"]["P"], spectra["criminal_2"]["P"], mask)
        print(f"    {band_name}: corr={corr:.4f}")

    # Cross-domain pair: criminal_1 vs labor_1
    print("\n  Cross-domain (criminal_1 vs labor_1):")
    for band_name, mask in [("low", low), ("mid", mid), ("high", high)]:
        corr = spectral_correlation(spectra["criminal_1"]["P"], spectra["labor_1"]["P"], mask)
        print(f"    {band_name}: corr={corr:.4f}")

    return {
        "same_domain": {
            band: float(spectral_correlation(spectra["criminal_1"]["P"], spectra["criminal_2"]["P"], m))
            for band, m in [("low", low), ("mid", mid), ("high", high)]
        },
        "cross_domain": {
            band: float(spectral_correlation(spectra["criminal_1"]["P"], spectra["labor_1"]["P"], m))
            for band, m in [("low", low), ("mid", mid), ("high", high)]
        }
    }


def main():
    print("=" * 60)
    print("MaoField Exp004: Allen-Cahn Semantic Field B-E")
    print("=" * 60)
    t0 = time.time()

    b_results, b_fields = experiment_b()
    c_results = experiment_c()
    d_results = experiment_d()
    e_results = experiment_e()

    # Save
    all_results = {
        "meta": {"date": "2026-04-10", "D": D, "grid": N, "steps": STEPS},
        "exp_b": b_results,
        "exp_c": c_results,
        "exp_d": d_results,
        "exp_e": e_results,
    }

    out_path = os.path.join(ANALYSIS_DIR, "exp004_bce_results.json")
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\n\nSaved: {out_path}")
    print(f"Total: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
