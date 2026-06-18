import json
dc=json.load(open('../exp019_alpha1_confirm/decouple_verdict_20260617/decouple_n5_result.json'))['raw']
r2=json.load(open('armA_round2_20260618/armA_round2_result.json'))['measures']
seeds=['1','2','3','4','42']; gens=[0,2,9]
xs=[]; ys=[]  # x=eff_supp, y=distinct_2
print("seed gen  eff_supp  distinct2")
for s in seeds:
    for g in gens:
        d2=dc[s][str(g)]['distinct_2']
        es=r2[f'traj_s{s}_g{g}']['eff_supp']
        xs.append(es); ys.append(d2)
        print(f"  {s:>3} {g}   {es:6.1f}   {d2:.4f}")
# Pearson r + R²
n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
sxy=sum((xs[i]-mx)*(ys[i]-my) for i in range(n))
sxx=sum((xs[i]-mx)**2 for i in range(n)); syy=sum((ys[i]-my)**2 for i in range(n))
r=sxy/(sxx*syy)**0.5
print(f"\n=== distinct-2 vs eff_supp (n={n}, all gens) ===")
print(f"Pearson r={r:.3f}  R²={r*r:.3f}  (判据b: R²<0.5=不共线=过; >0.5=共线=死)")
# 方向: per-gen 均值
import statistics as st
print("\nper-gen means:")
for g in gens:
    es=st.mean(r2[f'traj_s{s}_g{g}']['eff_supp'] for s in seeds)
    d2=st.mean(dc[s][str(g)]['distinct_2'] for s in seeds)
    print(f"  g{g}: eff_supp={es:.1f}  distinct2={d2:.4f}")
# down-leg vs up-leg
print("\ndown-leg g0→g2: eff_supp↓ distinct2 ?  up-leg g2→g9: eff_supp↑ distinct2 ?")
