import json, numpy as np
d=json.load(open('highorder_ppl_20260618/highorder_result.json'))
rows=d['rows']
mlp=np.array([r['mean_lp'] for r in rows]); gen=np.array([r['gen'] for r in rows],float)
print(f"mean-lp ↔ gen 共线性: pearson r={np.corrcoef(mlp,gen)[0,1]:+.3f}  spearman-ish(rank)={np.corrcoef(np.argsort(np.argsort(mlp)),np.argsort(np.argsort(gen)))[0,1]:+.3f}")
def polyR2(y,x,deg):
    X=np.vander(x,deg+1); b,_,_,_=np.linalg.lstsq(X,y,rcond=None); r=y-X@b
    return 1-r.var()/y.var()
def pcorr_cubic(F,g,x):  # 锁定的 cubic 控制
    X=np.vander(x,4)
    rF=F-X@np.linalg.lstsq(X,F,rcond=None)[0]; rg=g-X@np.linalg.lstsq(X,g,rcond=None)[0]
    return np.corrcoef(rF,rg)[0,1] if rF.std()>1e-12 and rg.std()>1e-12 else 0.0
print("\n=== 护栏(c): F 是不是 mean-lp 的高阶函数(曲率混叠) vs 真正交 ===")
for f in ['F1_var','F1_tail','F3_slice_gap']:
    F=np.array([r[f] for r in rows])
    r2=[polyR2(F,mlp,k) for k in [1,2,3,4,5,6]]
    print(f"{f}: R²(F~mean-lp) deg1-6 = {['%.4f'%x for x in r2]}  cubic残差={1-r2[2]:.4f} → 6阶残差={1-r2[5]:.4f}")
print("\n=== 更强 null: 纯 mean-lp 高阶函数 过【锁定cubic门A】是否也假阳 ===")
for name,h in [('mlp^2',mlp**2),('mlp^4',mlp**4),('mlp^6',mlp**6),('exp(mlp)',np.exp(mlp)),('1/(-mlp)',1/(-mlp)),('mlp^5',mlp**5)]:
    print(f"  null {name}: cubic-门A partial_r={pcorr_cubic(h,gen,mlp):+.3f}")
print("\n=== 对比: 真 F 的 cubic-门A partial_r (锁定值) ===")
for f in ['F1_var','F1_tail','F3_slice_gap']:
    F=np.array([r[f] for r in rows]); print(f"  {f}: {pcorr_cubic(F,gen,mlp):+.3f}")
