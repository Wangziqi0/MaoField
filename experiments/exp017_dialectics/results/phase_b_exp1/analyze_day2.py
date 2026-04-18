#!/usr/bin/env python3
"""Phase B Exp 1 — Day 2 observable analysis.

Reads observables_{mode}.json from each of the 6 runs and computes:
  - O2 primary:    late-window dS/dt statistics (t ∈ [25, 50])
  - O2 source-var: source_l2(t) late-window coefficient of variation (CoV)
                   — per dS/dt math review P0-3: if CoV is ~0 then dS/dt→0 is
                   Lyapunov-necessary (does NOT falsify insight 2-3); only if
                   CoV is non-trivial AND dS/dt still → 0 does insight 2-3 fail.
  - O2 extended:   exp_extended (t_sim=200) plateau test (per Q2: 10⁻⁶ vs 10⁻¹⁰)
  - mode comparison: exp vs controls on (mean_mod2, std_mod2, free_energy,
                     source_l2 late mean, dS/dt late mean, source CoV)
"""
import json
import math
import statistics
from pathlib import Path

DAY2 = Path("results/phase_b_exp1/day2")
MODES = ["exp", "null", "control_const", "control_whiten", "control_single"]
EXTENDED = "exp_extended"


def load_obs(mode: str, dir_name: str | None = None):
    d = dir_name if dir_name is not None else mode
    path = DAY2 / d / f"observables_{mode}.json"
    return json.loads(path.read_text())


def late_window_stats(rows, key, t_from=25.0):
    vals = [r[key] for r in rows if r["t"] >= t_from]
    if not vals:
        return None
    m = statistics.mean(vals)
    sd = statistics.stdev(vals) if len(vals) > 1 else 0.0
    return {"n": len(vals), "mean": m, "std": sd, "cov": sd / abs(m) if m else float("inf")}


def trajectory_at(rows, times):
    """Return values at approximately the requested times."""
    out = []
    for t in times:
        nearest = min(rows, key=lambda r: abs(r["t"] - t))
        out.append(nearest)
    return out


def mode_summary(mode, dir_name=None):
    obs = load_obs(mode, dir_name)
    # aggregate across docs (take per-doc late stats, then average)
    per_doc_late_ds = []
    per_doc_late_src = []
    per_doc_src_cov = []
    per_doc_final = []
    for doc in obs:
        rows = doc["rows"]
        s_ds = late_window_stats(rows, "ds_dt", t_from=25.0)
        s_src = late_window_stats(rows, "source_l2", t_from=25.0)
        if s_ds is None or s_src is None:
            continue
        per_doc_late_ds.append(s_ds["mean"])
        per_doc_late_src.append(s_src["mean"])
        per_doc_src_cov.append(s_src["cov"])
        per_doc_final.append(rows[-1])
    n = len(per_doc_late_ds)
    if n == 0:
        return None
    def agg(xs):
        return {"mean": statistics.mean(xs), "std": statistics.stdev(xs) if len(xs) > 1 else 0.0,
                "min": min(xs), "max": max(xs)}
    return {
        "mode": mode,
        "n_docs": n,
        "late_ds_dt": agg(per_doc_late_ds),
        "late_source_l2": agg(per_doc_late_src),
        "source_l2_CoV_late": agg(per_doc_src_cov),
        "final_mean_mod2": agg([r["mean_mod2"] for r in per_doc_final]),
        "final_std_mod2": agg([r["std_mod2"] for r in per_doc_final]),
        "final_free_energy": agg([r["free_energy"] for r in per_doc_final]),
    }


def main():
    print("=" * 96)
    print("Phase B Exp 1 — Day 2 Observable Analysis")
    print("=" * 96)

    summaries = {}
    for m in MODES:
        s = mode_summary(m)
        summaries[m] = s
        if s is None:
            print(f"\n{m}: NO DATA")
            continue
        print(f"\n### Mode: {m}  ({s['n_docs']} docs)")
        print(f"  late dS/dt mean   = {s['late_ds_dt']['mean']:.3e}   (doc-range: {s['late_ds_dt']['min']:.3e} → {s['late_ds_dt']['max']:.3e})")
        print(f"  late source_l2    = {s['late_source_l2']['mean']:.3e}")
        print(f"  source_l2 CoV     = {s['source_l2_CoV_late']['mean']:.3e}   (time-variance in late window; CoV=std/mean)")
        print(f"  final mean |ψ|²    = {s['final_mean_mod2']['mean']:.4f} ± {s['final_mean_mod2']['std']:.4f}")
        print(f"  final std  |ψ|²    = {s['final_std_mod2']['mean']:.4f} ± {s['final_std_mod2']['std']:.4f}")
        print(f"  final free energy = {s['final_free_energy']['mean']:.3e}")

    # Extended exp (t_sim=200, Q2 plateau test)
    print("\n" + "=" * 96)
    print("### Extended exp (t_sim=200, 20000 inner steps, Q2 plateau check)")
    print("=" * 96)
    obs_ext = load_obs("exp", "exp_extended")
    print(f"  n_docs = {len(obs_ext)}")
    # Cross-doc average dS/dt at specific times
    times_probe = [10, 25, 50, 100, 150, 200]
    for t_probe in times_probe:
        ds_at_t = []
        src_at_t = []
        for doc in obs_ext:
            nearest = min(doc["rows"], key=lambda r: abs(r["t"] - t_probe))
            ds_at_t.append(nearest["ds_dt"])
            src_at_t.append(nearest["source_l2"])
        print(f"  t ≈ {t_probe:4d}:  dS/dt = {statistics.mean(ds_at_t):.3e}   source_l2 = {statistics.mean(src_at_t):.4e}")

    # Q2 verdict: plateau 10^-6 → D branch (quasi-stationary pass); 10^-10 → A branch (fail insight 2-3)
    final_ds_ext = [doc["rows"][-1]["ds_dt"] for doc in obs_ext]
    final_ds_mean = statistics.mean(final_ds_ext)
    print(f"\n  ==> t=200 final dS/dt mean = {final_ds_mean:.3e}")
    if final_ds_mean > 1e-7:
        print(f"  ==> QUASI-STATIONARY at ≳10⁻⁶ level (pass D — insight 2-3 survives weakly)")
        q2_verdict = "D_quasi_stationary"
    elif final_ds_mean < 1e-9:
        print(f"  ==> COLLAPSING to ≲10⁻⁹ (fail A — insight 2-3 falsified, equilibrium attractor)")
        q2_verdict = "A_fail"
    else:
        print(f"  ==> AMBIGUOUS 10⁻⁷–10⁻⁸ range; verdict intermediate")
        q2_verdict = "intermediate"

    # Source variance check (review P0-3 gate): does source in late window ACTUALLY vary over time?
    # If CoV ~0, dS/dt → 0 is Lyapunov necessary; if CoV > threshold, dS/dt → 0 is meaningful.
    print("\n" + "=" * 96)
    print("### dS/dt math review P0-3 gate: source_l2(t) late-window CoV")
    print("=" * 96)
    print("Interpretation: if source is (nearly) constant in late window, dS/dt → 0")
    print("is Lyapunov-necessary — dS/dt magnitude alone cannot falsify insight 2-3.")
    print("Only the COMBINATION (dS/dt small AND source CoV non-trivial) is meaningful.")
    threshold_cov = 1e-3  # informative threshold; below this, S is essentially constant
    print(f"Threshold: CoV > {threshold_cov} ⇒ source meaningfully time-varying\n")
    for m in MODES + [EXTENDED]:
        if m == EXTENDED:
            obs = load_obs("exp", EXTENDED)
        else:
            obs = load_obs(m)
        covs = []
        for doc in obs:
            s = late_window_stats(doc["rows"], "source_l2", t_from=max(25.0, doc["rows"][-1]["t"]/2))
            if s:
                covs.append(s["cov"])
        if covs:
            mean_cov = statistics.mean(covs)
            gate = "✓ time-varying" if mean_cov > threshold_cov else "✗ (near) constant"
            print(f"  {m:20s}  CoV={mean_cov:.3e}  {gate}")

    # Also output machine-readable JSON
    out = {
        "modes": summaries,
        "extended": {
            "n_docs": len(obs_ext),
            "final_dSdt_mean": final_ds_mean,
            "q2_verdict": q2_verdict,
            "trajectory": [
                {
                    "t": t,
                    "dSdt_mean": statistics.mean([min(doc["rows"], key=lambda r: abs(r["t"] - t))["ds_dt"] for doc in obs_ext]),
                    "source_l2_mean": statistics.mean([min(doc["rows"], key=lambda r: abs(r["t"] - t))["source_l2"] for doc in obs_ext]),
                }
                for t in [10, 25, 50, 100, 150, 200]
            ],
        },
    }
    Path("results/phase_b_exp1/day2/day2_summary.json").write_text(json.dumps(out, indent=2, default=str))
    print("\nwrote results/phase_b_exp1/day2/day2_summary.json")


if __name__ == "__main__":
    main()
