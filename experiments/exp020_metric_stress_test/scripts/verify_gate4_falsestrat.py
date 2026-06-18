import json, itertools, math
d=json.load(open('armA_round2_20260618/armA_round2_result.json'))['measures']
seeds=[1,2,3,4,42]; gens=list(range(10))
# eff_supp 轨迹
S={s:[d[f'traj_s{s}_g{g}']['eff_supp'] for g in gens] for s in seeds}
print("=== eff_supp 5-seed ===")
for s in seeds: print(f"s{s}:", [f"{x:.1f}" for x in S[s]])
# per-gen mean + σ (across seeds)
import statistics as st
mean=[st.mean(S[s][g] for s in seeds) for g in gens]
sig =[st.pstdev([S[s][g] for s in seeds]) for g in gens]
print("\nper-gen mean:", [f"{x:.1f}" for x in mean])
print("per-gen σ   :", [f"{x:.2f}" for x in sig])
print(f"early σ (g1-3) max={max(sig[1:4]):.2f}  late σ (g5-9) max={max(sig[5:10]):.2f}  ratio={max(sig[5:10])/max(sig[1:4]):.1f}x")
# 同通道 seed-pair: 晚代 |ΔS| vs k·σ (per-gen)  — gate Finding C 复算
print("\n=== 同通道 seed-pair 晚代残差 vs k·σ_pergen (gate Finding C) ===")
for a,b in itertools.combinations(seeds,2):
    fails2=[g for g in range(5,10) if abs(S[a][g]-S[b][g])>2*sig[g]]
    fails28=[g for g in range(5,10) if abs(S[a][g]-S[b][g])>2.8*sig[g]]
    latemax=max(abs(S[a][g]-S[b][g]) for g in range(5,10))
    print(f"s{a}↔s{b}: late max|ΔS|={latemax:.2f}  k=2 fails@{fails2}  k=2.8 fails@{fails28}")
# 救法: 通道-均值 (N=5) 的 SE, 对比期望通道效应 10-15%
print("\n=== 救法检验: 通道均值 SE (N=5) vs 期望效应 ===")
for g in [5,7,9]:
    se=sig[g]/math.sqrt(5)
    eff10=0.10*mean[g]; eff15=0.15*mean[g]
    print(f"g{g}: mean={mean[g]:.1f} σ={sig[g]:.2f} SE(N=5)={se:.2f} | 10%效应={eff10:.2f}({eff10/se:.1f}σ_SE) 15%={eff15:.2f}({eff15/se:.1f}σ_SE)")
