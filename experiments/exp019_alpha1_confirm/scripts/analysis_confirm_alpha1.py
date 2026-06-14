#!/usr/bin/env python3
"""exp019 locked analysis — thresholds hardcoded per prereg v1.1. Do not edit post-LOCK.
Gatekeeping: E1(geometry,g1) -> E2(PPL,g2) -> E3(pathB log-ratio, g1->g2..g4->g5 window).
Paired sign-flip exact permutation (2^n), one-sided (alpha1 < alpha0), alpha=0.05.
Three-zone verdict per endpoint: CONFIRMED / INCONCLUSIVE / FALSE.
Modes:
  --pairs-json FILE   {"E1": {"101": [a0_val, a1_val], ...}, "E2": {...}, "E3": {...}}
                      E1/E2 raw per-arm values; E3 per-arm window means (ratio taken as ln(a1/a0))
  --null-sim N        type-I error simulation (N reps, n=6 pairs, N(0,1) diffs)
  --sanity-s42        run pipeline on historical s42 single pair (descriptive only)
"""
import json, math, argparse, itertools, random

TH = {"E1": -6.3, "E2": -9.4, "E3": -0.0513}
ALPHA = 0.05

def signflip_p(diffs):
    n = len(diffs); T = sum(diffs)/n
    cnt = 0; tot = 2**n
    for signs in itertools.product((1,-1), repeat=n):
        Tp = sum(d*s for d,s in zip(diffs,signs))/n
        if Tp <= T + 1e-15: cnt += 1
    return cnt/tot

def verdict(ep, diffs):
    n = len(diffs); mean = sum(diffs)/n
    if n >= 5:
        p = signflip_p(diffs)
    else:
        p = None  # fallback t handled manually per prereg if n==4
    conf = TH[ep]
    if p is not None and mean <= conf and p < ALPHA: zone = "CONFIRMED"
    elif mean >= 0: zone = "FALSE"
    else: zone = "INCONCLUSIVE"
    return {"endpoint": ep, "n": n, "mean_diff": round(mean,5), "p_signflip": (round(p,5) if p is not None else None), "threshold": conf, "zone": zone}

def run_confirm(pairs):
    out = {"order": ["E1","E2","E3"], "results": [], "gate_stopped_at": None}
    proceed = True
    for ep in ["E1","E2","E3"]:
        d = pairs.get(ep, {})
        if ep == "E3":
            diffs = [math.log(v[1]/v[0]) for v in d.values()]
        else:
            diffs = [v[1]-v[0] for v in d.values()]
        r = verdict(ep, diffs)
        r["gated"] = proceed
        if not proceed: r["note"] = "exploratory (gate stopped earlier)"
        out["results"].append(r)
        if proceed and r["zone"] != "CONFIRMED":
            out["gate_stopped_at"] = ep; proceed = False
    return out

def null_sim(N):
    random.seed(42)
    rej = 0
    for _ in range(N):
        diffs = [random.gauss(0,1) for _ in range(6)]
        # one-sided test at ALPHA, ignore effect threshold (pure type-I of the test)
        if signflip_p(diffs) < ALPHA: rej += 1
    return {"reps": N, "empirical_type_I": rej/N, "expected_band": [0.03, 0.05]}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs-json"); ap.add_argument("--null-sim", type=int)
    ap.add_argument("--sanity-s42", action="store_true")
    a = ap.parse_args()
    if a.null_sim:
        print(json.dumps(null_sim(a.null_sim), indent=1))
    elif a.sanity_s42:
        pairs = {"E1": {"42": [202.39, 189.80]}, "E2": {"42": [108.396, 89.521]}, "E3": {"42": [0.2181, 0.1929]}}
        out = run_confirm(pairs)
        out["note"] = "SANITY ONLY: n=1 historical s42, no inference"
        print(json.dumps(out, indent=1))
    elif a.pairs_json:
        pairs = json.load(open(a.pairs_json))
        print(json.dumps(run_confirm(pairs), indent=1))
