#!/usr/bin/env python3
"""
Independent second-channel adjudication of Branch 1 (high-order PPL structure).
Re-written from scratch; does NOT import highorder_ppl_run.py or guardrail_c.py.

Core question: do F1_var / F1_tail / F3_slice_gap carry崩溃 signal ORTHOGONAL
to mean-logprob, or is it curvature aliasing through the mean_lp<->gen collinearity?

Strategy for a test that does NOT false-positive on pure mean-lp functions:
  1. Build several PURE mean-lp functions (mlp^4, mlp^5, mlp^6, exp, |mlp|^p) that
     by construction carry ZERO independent gen info. A correct orthogonality test
     MUST give them ~null.
  2. Residualize F against a FLEXIBLE smooth/monotone fit of mean_lp (isotonic +
     high-deg poly + LOO k-NN-in-mean_lp), then test residual vs gen.
  3. matched-mean_lp paired contrast: pairs of (seed,gen) rows with near-equal
     mean_lp but different gen -> does F differ in a gen-consistent direction?
"""
import json, itertools
import numpy as np

np.random.seed(0)
P = "/media/amd/raid1/canonical/projects/MaoField/experiments/exp020_metric_stress_test/highorder_ppl_20260618/highorder_result.json"
d = json.load(open(P))
rows = d["rows"]
seed = np.array([r["seed"] for r in rows], float)
gen  = np.array([r["gen"]  for r in rows], float)
mlp  = np.array([r["mean_lp"] for r in rows], float)
F = {
    "F1_var":       np.array([r["F1_var"] for r in rows], float),
    "F1_tail":      np.array([r["F1_tail"] for r in rows], float),
    "F3_slice_gap": np.array([r["F3_slice_gap"] for r in rows], float),
}
F3_rare = np.array([r["F3_slice_rare"] for r in rows], float)
F3_freq = np.array([r["F3_slice_freq"] for r in rows], float)

N = len(rows)
print(f"N rows = {N}; seeds = {sorted(set(seed))}; gens 0-9")
print(f"corr(mean_lp, gen) = {np.corrcoef(mlp, gen)[0,1]:+.4f}")
print(f"corr(mean_lp^2, gen)= {np.corrcoef(mlp**2, gen)[0,1]:+.4f}")
print()

# --- PURE mean-lp null functions (zero independent gen info by construction) ---
nulls = {
    "mlp^2":  mlp**2,
    "mlp^4":  mlp**4,
    "mlp^5":  mlp**5,
    "mlp^6":  mlp**6,
    "exp(mlp)": np.exp(mlp),
    "|mlp|^2.5": np.abs(mlp)**2.5,
    "1/mlp":  1.0/mlp,
}

# =====================================================================
# helpers
# =====================================================================
def partial_corr_cubic(y, x_signal, x_ctrl):
    """partial corr(y, x_signal | cubic(x_ctrl)) -- replicates locked gate A."""
    # design for cubic of ctrl
    Xc = np.column_stack([np.ones_like(x_ctrl), x_ctrl, x_ctrl**2, x_ctrl**3])
    def resid(v):
        beta, *_ = np.linalg.lstsq(Xc, v, rcond=None)
        return v - Xc @ beta
    ry = resid(y); rs = resid(x_signal)
    if np.std(ry) < 1e-12 or np.std(rs) < 1e-12:
        return 0.0
    return np.corrcoef(ry, rs)[0,1]

def isotonic(x, y):
    """Pool-adjacent-violators isotonic regression of y on x (monotone fit).
    Returns fitted values aligned to original order. Auto-picks increasing/decreasing."""
    order = np.argsort(x)
    yo = y[order].astype(float).copy()
    n = len(yo)
    def pava(v):
        # increasing isotonic via PAVA
        val = v.copy(); w = np.ones(n)
        i = 0
        # standard stack-based PAVA
        lvl_val = []; lvl_w = []; lvl_cnt = []
        for k in range(n):
            cv = v[k]; cw = 1.0; cc = 1
            while lvl_val and lvl_val[-1] > cv:
                pv = lvl_val.pop(); pw = lvl_w.pop(); pc = lvl_cnt.pop()
                cv = (pv*pw + cv*cw)/(pw+cw); cw = pw+cw; cc = pc+cc
            lvl_val.append(cv); lvl_w.append(cw); lvl_cnt.append(cc)
        out = []
        for vv, cc in zip(lvl_val, lvl_cnt):
            out.extend([vv]*cc)
        return np.array(out)
    fit_inc = pava(yo)
    fit_dec = pava(yo[::-1])[::-1]  # decreasing = increasing on reversed
    # also try decreasing properly: isotonic on -y then negate
    fit_dec2 = -pava(-yo)
    sse_inc = np.sum((yo-fit_inc)**2)
    sse_dec = np.sum((yo-fit_dec2)**2)
    fit = fit_inc if sse_inc <= sse_dec else fit_dec2
    out = np.empty(n); out[order] = fit
    return out

def loo_knn_mlp(y, x, k=6):
    """Leave-one-out k-NN regression of y on scalar x (mean_lp).
    Flexible non-parametric fit; predicts each point from its k nearest mean_lp
    neighbours (excluding itself). Residual = y - prediction."""
    n = len(y); pred = np.empty(n)
    for i in range(n):
        dist = np.abs(x - x[i]); dist[i] = np.inf
        idx = np.argsort(dist)[:k]
        pred[i] = np.mean(y[idx])
    return y - pred

def resid_vs_gen_after_flexible(y):
    """Multiple flexible-mean_lp residualizations; report Spearman of residual vs gen.
    A pure mean_lp function should give ~0 here under ALL flex fits."""
    out = {}
    # poly deg up to 6
    for deg in (3,5,6):
        Xp = np.column_stack([mlp**p for p in range(deg+1)])
        beta,*_ = np.linalg.lstsq(Xp, y, rcond=None)
        r = y - Xp@beta
        out[f"poly{deg}"] = spearman(r, gen)
    # isotonic
    fit = isotonic(mlp, y); r = y - fit
    out["isotonic"] = spearman(r, gen)
    # LOO kNN
    for k in (4,6,8):
        r = loo_knn_mlp(y, mlp, k=k)
        out[f"knn{k}"] = spearman(r, gen)
    return out

def spearman(a, b):
    ra = rankdata(a); rb = rankdata(b)
    return np.corrcoef(ra, rb)[0,1]

def rankdata(a):
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a)); ranks[order] = np.arange(len(a))
    # average ties
    a_sorted = a[order]; i = 0; n=len(a)
    while i < n:
        j = i
        while j+1 < n and a_sorted[j+1]==a_sorted[i]:
            j+=1
        if j>i:
            ranks[order[i:j+1]] = np.mean(np.arange(i,j+1))
        i=j+1
    return ranks

# =====================================================================
# Q1 + Q3: calibrate gate A on pure nulls (is cubic enough?)
# =====================================================================
print("="*70)
print("Q1/Q3: GATE A (cubic partial-corr) on TRUE F vs PURE mean-lp nulls")
print("="*70)
print(f"{'function':<14} {'partial_r(cubic)':>16}")
for name,v in {**F, **nulls}.items():
    pr = partial_corr_cubic(v, gen, mlp)
    tag = " <-TRUE F" if name in F else " (pure-mlp null)"
    print(f"{name:<14} {pr:>16.4f}{tag}")
print()
print(">>> If pure-mlp nulls give |partial_r| >= true F, cubic gate A is BROKEN")
print("    (a pure function of mean_lp must NOT pass an orthogonality test).")

# =====================================================================
# Q1: FLEXIBLE-mean_lp residual test (must NOT false-positive on nulls)
# Spearman(residual, gen) after isotonic / high-poly / LOO-kNN fit of mean_lp.
# =====================================================================
print()
print("="*70)
print("Q1: residual-vs-gen AFTER flexible mean_lp fit (Spearman). ")
print("    A correct test gives ~0 for pure-mlp nulls under ALL fits.")
print("="*70)
allfns = {**F, **nulls}
hdr = ["poly3","poly5","poly6","isotonic","knn4","knn6","knn8"]
print(f"{'function':<14} " + " ".join(f"{h:>8}" for h in hdr) + "   tag")
for name,v in allfns.items():
    res = resid_vs_gen_after_flexible(v)
    tag = "TRUE F" if name in F else "null"
    print(f"{name:<14} " + " ".join(f"{res[h]:>8.3f}" for h in hdr) + f"   {tag}")

# =====================================================================
# Q2: matched-mean_lp PAIRED contrast (the cleanest orthogonality test)
# Find pairs of rows with near-equal mean_lp but different gen.
# If F differs in a gen-monotone direction across such pairs -> orthogonal signal.
# This CANNOT false-positive on a pure function of mean_lp (equal mlp -> equal F).
# =====================================================================
print()
print("="*70)
print("Q2: matched-mean_lp paired contrast (|Δmean_lp| small, Δgen != 0)")
print("="*70)

def matched_pairs_test(y, mlp_tol):
    """For all row pairs with |Δmlp|<tol and gen_i != gen_j, sign of (ΔF)*(Δgen).
    Returns: n_pairs, frac_F_increases_with_gen, mean Δgen-normalized ΔF."""
    pairs = []
    for i,j in itertools.combinations(range(N), 2):
        if abs(mlp[i]-mlp[j]) < mlp_tol and gen[i] != gen[j]:
            dg = gen[i]-gen[j]
            dF = y[i]-y[j]
            pairs.append((dg, dF))
    if not pairs:
        return 0, np.nan, np.nan, np.nan
    pairs = np.array(pairs)
    # sign agreement: does sign(dF) == sign(dg) consistently?
    s = np.sign(pairs[:,0]*pairs[:,1])
    frac_pos = np.mean(s>0)
    # slope: dF per unit dg (orient each pair so dg>0)
    oriented = np.where(pairs[:,0]>0, pairs[:,1], -pairs[:,1])
    oriented_dg = np.abs(pairs[:,0])
    slope = np.sum(oriented)/np.sum(oriented_dg)
    # binomial test (two-sided) approx via normal
    n = len(s); k = np.sum(s>0)
    p = 0.5
    z = (k - n*p)/np.sqrt(n*p*(1-p))
    return n, frac_pos, slope, z

print("mean_lp matched within tol; sign-consistency of ΔF with Δgen:")
print(f"{'function':<14} {'tol':>5} {'npairs':>7} {'frac_dF~dg':>11} {'slope/Δgen':>11} {'z':>7}")
for tol in (0.02, 0.04, 0.06):
    for name in ["F1_var","F1_tail","F3_slice_gap","mlp^4","mlp^6"]:
        v = F.get(name, nulls.get(name))
        n,fp,sl,z = matched_pairs_test(v, tol)
        print(f"{name:<14} {tol:>5.2f} {n:>7d} {fp:>11.3f} {sl:>11.4f} {z:>7.2f}")
    print()

# =====================================================================
# Q2-decisive: U-shape fold inspection + nested CV improvement test
# =====================================================================
print()
print("="*70)
print("Q2-decisive: per-gen means (averaged over 5 seeds) -- U-shape fold")
print("="*70)
print(f"{'gen':>3} {'mean_lp':>9} {'F1_var':>8} {'F1_tail':>8} {'F3_gap':>8} {'F3_rare':>8} {'F3_freq':>8}")
for g in range(10):
    m = gen==g
    print(f"{g:>3} {mlp[m].mean():>9.4f} {F['F1_var'][m].mean():>8.3f} "
          f"{F['F1_tail'][m].mean():>8.4f} {F['F3_slice_gap'][m].mean():>8.4f} "
          f"{F3_rare[m].mean():>8.3f} {F3_freq[m].mean():>8.3f}")

print()
print("Look for gens with NEAR-EQUAL mean_lp but DIFFERENT F (pure-mlp fn forbids this):")
gm = np.array([mlp[gen==g].mean() for g in range(10)])
f3m = np.array([F['F3_slice_gap'][gen==g].mean() for g in range(10)])
fvm = np.array([F['F1_var'][gen==g].mean() for g in range(10)])
ftm = np.array([F['F1_tail'][gen==g].mean() for g in range(10)])
for ga in range(10):
    for gb in range(ga+1,10):
        if abs(gm[ga]-gm[gb])<0.03:
            print(f"  gen{ga} vs gen{gb}: Δmean_lp={gm[ga]-gm[gb]:+.4f}  "
                  f"ΔF3_gap={f3m[ga]-f3m[gb]:+.4f}  ΔF1_var={fvm[ga]-fvm[gb]:+.4f}  "
                  f"ΔF1_tail={ftm[ga]-ftm[gb]:+.5f}")

# Nested cross-validated test: does adding gen improve prediction of F
# beyond a flexible mlp basis? Use LOSO (leave-one-seed-out) CV to be honest.
print()
print("="*70)
print("Q2: LOSO-CV -- does gen improve F prediction beyond flexible mlp basis?")
print("    Model A: F ~ poly5(mlp).  Model B: F ~ poly5(mlp) + gen + gen^2.")
print("    Report CV-R2. If B >> A, gen carries info orthogonal to (poly) mlp.")
print("="*70)
seeds_u = sorted(set(seed))
def cv_r2(y, use_gen):
    preds = np.empty(N); 
    for s in seeds_u:
        tr = seed!=s; te = seed==s
        cols = [mlp**p for p in range(6)]
        if use_gen:
            cols += [gen, gen**2]
        X = np.column_stack(cols)
        beta,*_ = np.linalg.lstsq(X[tr], y[tr], rcond=None)
        preds[te] = X[te]@beta
    ss_res = np.sum((y-preds)**2); ss_tot = np.sum((y-y.mean())**2)
    return 1 - ss_res/ss_tot
for name in ["F1_var","F1_tail","F3_slice_gap"]:
    v = F[name]
    ra = cv_r2(v, False); rb = cv_r2(v, True)
    print(f"{name:<14} CV-R2  poly5(mlp)={ra:>7.4f}   +gen={rb:>7.4f}   Δ={rb-ra:>+7.4f}")
for name in ["mlp^4","mlp^6"]:
    v = nulls[name]
    ra = cv_r2(v, False); rb = cv_r2(v, True)
    print(f"{name:<14} CV-R2  poly5(mlp)={ra:>7.4f}   +gen={rb:>7.4f}   Δ={rb-ra:>+7.4f}  (null)")

# =====================================================================
# Q2-F3 deep dive: differential collapse rare vs freq + permutation null
# =====================================================================
print()
print("="*70)
print("Q2-F3: F3_slice_gap deep dive (differential collapse rare vs freq)")
print("="*70)
# Is the gen-residual of F3 driven by rare-slice, freq-slice, or both?
# Residualize each slice's mean-logprob against flexible mlp, see which carries gen.
def loso_resid_spearman_vs_gen(y, deg=5):
    preds = np.empty(N)
    for s in seeds_u:
        tr = seed!=s; te=seed==s
        X = np.column_stack([mlp**p for p in range(deg+1)])
        beta,*_ = np.linalg.lstsq(X[tr], y[tr], rcond=None)
        preds[te] = X[te]@beta
    r = y - preds
    return spearman(r, gen), r
for nm, vv in [("F3_rare",F3_rare),("F3_freq",F3_freq),("F3_gap",F['F3_slice_gap'])]:
    sp, r = loso_resid_spearman_vs_gen(vv)
    print(f"  {nm:<9} LOSO-resid spearman vs gen = {sp:+.3f}")

# Permutation null on the LOSO ΔR2 for F3_gap: shuffle gen WITHIN nothing
# (full shuffle) -> distribution of ΔR2 under no gen-info.
print()
print("Permutation null for F3_gap LOSO ΔR2 (shuffle gen labels, 2000x):")
def cv_r2_perm(y, gperm):
    preds = np.empty(N)
    for s in seeds_u:
        tr=seed!=s; te=seed==s
        Xa = np.column_stack([mlp**p for p in range(6)])
        Xb = np.column_stack([mlp**p for p in range(6)]+[gperm, gperm**2])
        ba,*_=np.linalg.lstsq(Xa[tr],y[tr],rcond=None)
        bb,*_=np.linalg.lstsq(Xb[tr],y[tr],rcond=None)
        # store improvement via combined: use model B pred
        preds[te]=Xb[te]@bb
    ssb=np.sum((y-preds)**2)
    # model A pred
    predsa=np.empty(N)
    for s in seeds_u:
        tr=seed!=s; te=seed==s
        Xa=np.column_stack([mlp**p for p in range(6)])
        ba,*_=np.linalg.lstsq(Xa[tr],y[tr],rcond=None)
        predsa[te]=Xa[te]@ba
    ssa=np.sum((y-predsa)**2); sstot=np.sum((y-y.mean())**2)
    return (1-ssb/sstot)-(1-ssa/sstot)
obs = cv_r2_perm(F['F3_slice_gap'], gen)
rng=np.random.default_rng(1)
perm=[]
for _ in range(2000):
    gp = rng.permutation(gen)
    perm.append(cv_r2_perm(F['F3_slice_gap'], gp))
perm=np.array(perm)
pval=(np.sum(perm>=obs)+1)/(len(perm)+1)
print(f"  observed ΔR2 = {obs:+.4f};  perm-null mean={perm.mean():+.4f} sd={perm.std():.4f};  p={pval:.4f}")
for nm in ["F1_var","F1_tail"]:
    ob = cv_r2_perm(F[nm], gen)
    pm=np.array([cv_r2_perm(F[nm], rng.permutation(gen)) for _ in range(2000)])
    pv=(np.sum(pm>=ob)+1)/(len(pm)+1)
    print(f"  {nm}: observed ΔR2={ob:+.4f}; p={pv:.4f}")

# =====================================================================
# Q2-robustness: rows are NOT independent (5 near-replicate seeds x 10 gens).
# Honest test: collapse to per-gen means (10 quasi-independent points), then
# ask if F-residual-vs-mlp still tracks gen. Also block-permute by gen.
# =====================================================================
print()
print("="*70)
print("Q2-robustness: per-gen-mean analysis (10 points; respects dependence)")
print("="*70)
gm  = np.array([mlp[gen==g].mean() for g in range(10)])
gG  = np.arange(10.0)
for name in ["F1_var","F1_tail","F3_slice_gap"]:
    ym = np.array([F[name][gen==g].mean() for g in range(10)])
    # fit flexible mlp (use poly3 to avoid overfit on 10 pts) and check resid vs gen
    for deg in (2,3):
        X=np.column_stack([gm**p for p in range(deg+1)])
        beta,*_=np.linalg.lstsq(X,ym,rcond=None)
        r=ym-X@beta
        print(f"  {name:<13} poly{deg}(mlp) resid: spearman(resid,gen)={spearman(r,gG):+.3f}  "
              f"maxabs_resid={np.max(np.abs(r)):.4f}  range(F)={ym.max()-ym.min():.4f}")

# Direct U-shape fold non-monotonicity proof for F3_gap:
# mean_lp is U-shaped (min at gen2); if F3_gap were a function of mlp it must be
# symmetric across the fold. Compare descending arm (g0->2) vs ascending (g2->9)
# at matched mlp.
print()
print("F3_gap non-monotonicity vs mlp (hysteresis across the U-fold):")
order = np.argsort(gm)
print("  gens sorted by mean_lp:", [int(g) for g in np.argsort(gm)])
f3m=np.array([F['F3_slice_gap'][gen==g].mean() for g in range(10)])
print("  mean_lp ascending -> F3_gap (should be monotone if pure fn of mlp):")
for g in np.argsort(gm):
    print(f"    gen{int(g)}: mlp={gm[g]:+.4f}  F3_gap={f3m[g]:.4f}")

# Gate B sanity: cross-gen signal vs seed noise floor for F3_gap
print()
print("Gate B recompute (cross-gen range vs within-gen 5-seed sd):")
for name in ["F1_var","F1_tail","F3_slice_gap"]:
    perg_mean=np.array([F[name][gen==g].mean() for g in range(10)])
    perg_sd  =np.array([F[name][gen==g].std(ddof=1) for g in range(10)])
    cross=perg_mean.max()-perg_mean.min()
    floor=perg_sd.max()
    print(f"  {name:<13} cross-gen range={cross:.4f}  max within-gen sd={floor:.5f}  "
          f"ratio={cross/floor:.1f}x")

# =====================================================================
# FINAL: contrast F3 hysteresis vs F1 plateau-wobble; quantify "extra" signal
# =====================================================================
print()
print("="*70)
print("FINAL: matched-mlp arm contrast (gen1 vs gen4: near-equal mean_lp)")
print("="*70)
for ga,gb in [(1,4),(2,3),(0,7)]:
    print(f"  gen{ga} vs gen{gb}:")
    for nm,vv in [("mean_lp",mlp),("F1_var",F['F1_var']),("F1_tail",F['F1_tail']),
                  ("F3_gap",F['F3_slice_gap']),("F3_rare",F3_rare),("F3_freq",F3_freq)]:
        a=vv[gen==ga].mean(); b=vv[gen==gb].mean()
        print(f"     {nm:<9} {a:>9.4f} vs {b:>9.4f}   Δ={a-b:+.4f}")

# Fraction of F variance NOT explainable by any smooth mlp fn (per-gen, poly3 LOO)
print()
print("Unexplained-by-mlp fraction (per-gen means, poly3, LOO over 10 gens):")
gm  = np.array([mlp[gen==g].mean() for g in range(10)])
for name in ["F1_var","F1_tail","F3_slice_gap"]:
    ym=np.array([F[name][gen==g].mean() for g in range(10)])
    pred=np.empty(10)
    for i in range(10):
        tr=np.arange(10)!=i
        X=np.column_stack([gm**p for p in range(4)])
        beta,*_=np.linalg.lstsq(X[tr],ym[tr],rcond=None)
        pred[i]=X[i]@beta
    r=ym-pred
    # is residual gen-ordered? check serial structure (lag) - hysteresis signature
    sp=spearman(r,np.arange(10.0))
    print(f"  {name:<13} resid_sd/F_sd={r.std()/ym.std():.3f}  "
          f"LOO-resid maxabs={np.max(np.abs(r)):.4f}  spearman(resid,gen)={sp:+.3f}")

# Are gen1 vs gen4 F3 difference significant given 5-seed noise? (Welch-ish)
print()
def welch(a,b):
    ma,mb=a.mean(),b.mean(); va,vb=a.var(ddof=1),b.var(ddof=1); na,nb=len(a),len(b)
    t=(ma-mb)/np.sqrt(va/na+vb/nb)
    return t
print("Significance of matched-mlp F-differences (t over 5 seeds):")
for ga,gb in [(1,4),(2,3)]:
    print(f"  gen{ga}vs{gb}: Δmlp_t={welch(mlp[gen==ga],mlp[gen==gb]):+.1f}  "
          f"F3gap_t={welch(F['F3_slice_gap'][gen==ga],F['F3_slice_gap'][gen==gb]):+.1f}  "
          f"F1var_t={welch(F['F1_var'][gen==ga],F['F1_var'][gen==gb]):+.1f}  "
          f"F1tail_t={welch(F['F1_tail'][gen==ga],F['F1_tail'][gen==gb]):+.1f}")

# =====================================================================
# Seed-replicate determinism check (confound 5c): are the 5 seeds independent
# realizations, or near-deterministic replicates of one trajectory?
# =====================================================================
print()
print("="*70)
print("Confound 5c: per-(gen) across-seed coefficient of variation")
print("="*70)
for name in ["mean_lp","F1_var","F1_tail","F3_slice_gap"]:
    v = mlp if name=="mean_lp" else F[name]
    cvs=[]
    for g in range(10):
        m=v[gen==g]; cvs.append(abs(m.std(ddof=1)/m.mean()))
    print(f"  {name:<13} median across-seed CV = {np.median(cvs)*100:.2f}%  "
          f"(max {np.max(cvs)*100:.2f}%)")
print()
print("  -> If CV ~1% or less, seeds are near-deterministic replicates of ONE")
print("     trajectory; orthogonal 'signal' = the trajectory is a 2D+ manifold")
print("     in (mean_lp, F)-space, NOT 5 independent draws. Real structure but")
print("     'independent seed set复现' bar (a) is NOT met by these 5 seeds.")
