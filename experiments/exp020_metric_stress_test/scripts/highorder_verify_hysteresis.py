import json, numpy as np
rows=json.load(open('highorder_ppl_20260618/highorder_result.json'))['rows']
print("=== 迟滞核实: per-gen 均值 (across 5 seed) ===")
print(f"{'gen':>3} {'mean_lp':>9} {'F3_gap':>8} {'F3_rare':>8} {'F3_freq':>8} {'F1_var':>8}")
pg={}
for g in range(10):
    sub=[r for r in rows if r['gen']==g]
    mlp=np.mean([r['mean_lp'] for r in sub]); gap=np.mean([r['F3_slice_gap'] for r in sub])
    rare=np.mean([r['F3_slice_rare'] for r in sub]); freq=np.mean([r['F3_slice_freq'] for r in sub])
    var=np.mean([r['F1_var'] for r in sub]); pg[g]=(mlp,gap,rare,freq,var)
    print(f"{g:>3} {mlp:>9.3f} {gap:>8.3f} {rare:>8.3f} {freq:>8.3f} {var:>8.2f}")
print("\n=== gen1 vs gen4 (第二通道 decisive claim) ===")
g1,g4=pg[1],pg[4]
print(f"gen1: mean_lp={g1[0]:.3f} F3_gap={g1[1]:.3f}")
print(f"gen4: mean_lp={g4[0]:.3f} F3_gap={g4[1]:.3f}")
print(f"Δmean_lp={abs(g1[0]-g4[0]):.3f} (近似相等?)  ΔF3_gap={abs(g1[1]-g4[1]):.3f} (纯mean_lp函数应≈0)")
# t-test gen1 vs gen4 on F3_gap (5 seed each)
from statistics import mean,pstdev
gap1=[r['F3_slice_gap'] for r in rows if r['gen']==1]; gap4=[r['F3_slice_gap'] for r in rows if r['gen']==4]
mlp1=[r['mean_lp'] for r in rows if r['gen']==1]; mlp4=[r['mean_lp'] for r in rows if r['gen']==4]
import math
def welch(a,b):
    ma,mb=mean(a),mean(b); va,vb=pstdev(a)**2*len(a)/(len(a)-1),pstdev(b)**2*len(b)/(len(b)-1)
    se=math.sqrt(va/len(a)+vb/len(b)); return (ma-mb)/se if se>0 else float('inf')
print(f"\nF3_gap gen1 vs gen4: t={welch(gap1,gap4):.1f}  | mean_lp gen1 vs gen4: t={welch(mlp1,mlp4):.1f}")
print(f"seed CV: mean_lp gen1 = {pstdev(mlp1)/abs(mean(mlp1))*100:.1f}% , F3_gap gen1 = {pstdev(gap1)/abs(mean(gap1))*100:.1f}% (近确定性复本?)")
