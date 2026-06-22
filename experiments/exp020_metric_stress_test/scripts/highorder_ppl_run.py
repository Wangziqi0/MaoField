#!/usr/bin/env python3
"""
highorder_ppl_run.py — exp020 高阶 PPL 结构测试 (LOCKED v2, gate-6 修复).
决策规则锁于 highorder_ppl_structure_DESIGN sha256 733be69 (算前已 push 987ef21).
候选 3 泛函 (decode-free, 固定 Wikitext-2 train audit blocks, 禁触模型自生成):
  F1-var = per-token true-next-token logprob 方差
  F1-tail = logprob < τ 占比 (τ=g0 全seed logprob 5th pct, 锁一次)
  F3-slice = per-slice mean-logprob (稀有 vs 高频 target token, g0 unigram top/bottom20%)
门A=cubic 非线性 residualize(F,gen | mean-logprob); 门B=per-gen 5seed σ bootstrap 上界.
Branch1 ⟺ ≥1 F 过门A(cubic残差仍随gen,超null) AND 门B(跨gen信号>2·σ_upper). 否则 Branch2.
CPU fp32, 5-seed α=0 链 gen0-9 (在36).
"""
from __future__ import annotations
import sys, os, json, time
sys.path.insert(0,"/media/amd/raid1/canonical/projects/MaoField/experiments/exp018_cat/src")
os.environ.setdefault("HF_HUB_OFFLINE","1"); os.environ.setdefault("TOKENIZERS_PARALLELISM","false")
import torch, numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from data_pipeline import load_wikitext2, tokenize_and_block

ROOT="/media/amd/raid1/canonical/projects/MaoField/experiments/exp018_cat/data/checkpoints_armb/alpha0.0"
TOK="facebook/opt-125m"; N_CTX=128; BLOCK=64; BATCH=32
SEEDS=[1,2,3,4,42]; GENS=list(range(10))
OUT="/media/amd/raid1/canonical/projects/MaoField/experiments/exp020_metric_stress_test/highorder_ppl_20260618"
def ckpt(s,g): return f"{ROOT}/no_preserve_seed{s}/generation_{g}"

@torch.no_grad()
def get_logprobs(model, blocks):
    lps=[]; tgts=[]
    for i in range(0,len(blocks),BATCH):
        ids=torch.tensor(blocks[i:i+BATCH]["input_ids"],dtype=torch.long)
        logits=model(input_ids=ids).logits.float()
        logp=torch.log_softmax(logits,dim=-1)
        lp=logp[:,:-1,:].gather(-1,ids[:,1:].unsqueeze(-1)).squeeze(-1)
        lps.append(lp.reshape(-1)); tgts.append(ids[:,1:].reshape(-1))
    return torch.cat(lps).numpy(), torch.cat(tgts).numpy()

def load(p): return AutoModelForCausalLM.from_pretrained(p,dtype=torch.float32).to("cpu").eval()

def partial_corr_cubic(F, gen, meanlp):
    """partial-corr(F, gen | cubic(meanlp)): residualize both on cubic of meanlp, correlate."""
    X=np.vstack([meanlp**k for k in range(4)]).T  # cubic design
    def resid(y):
        beta,_,_,_=np.linalg.lstsq(X,y,rcond=None); return y-X@beta
    rF=resid(F.astype(float)); rg=resid(gen.astype(float))
    if rF.std()<1e-12 or rg.std()<1e-12: return 0.0
    return float(np.corrcoef(rF,rg)[0,1])

def boot_sigma_upper(vals, n=2000, q=0.90):
    """bootstrap 90% 上置信界 of std(vals) (5 seeds)."""
    vals=np.asarray(vals); g=np.random.default_rng(0)
    bs=[np.std(g.choice(vals,len(vals),replace=True),ddof=1) for _ in range(n)]
    return float(np.quantile(bs,q))

def main():
    os.makedirs(OUT,exist_ok=True); t0=time.time()
    raw=load_wikitext2(); tok=AutoTokenizer.from_pretrained(TOK)
    if tok.pad_token is None: tok.pad_token=tok.eos_token
    blocks=tokenize_and_block(raw["train"],tok,BLOCK).select(range(N_CTX))
    print(f"[setup] {N_CTX} blocks {time.time()-t0:.1f}s",flush=True)

    # pass 1: 收 per-(seed,gen) logprob 数组 + target
    LP={}; TG=None
    for s in SEEDS:
        for g in GENS:
            m=load(ckpt(s,g)); lp,tg=get_logprobs(m,blocks); del m
            LP[(s,g)]=lp;  TG=tg  # target 固定 (同 train audit blocks)
            print(f"  s{s}g{g}: n={len(lp)} mean_lp={lp.mean():.3f}",flush=True)

    # 锁: τ = g0 全seed logprob 5th pct; slice freq = audit target token 频率 top/bottom 20%
    g0_all=np.concatenate([LP[(s,0)] for s in SEEDS]); TAU=float(np.percentile(g0_all,5))
    uniq,cnt=np.unique(TG,return_counts=True); freq=dict(zip(uniq.tolist(),cnt.tolist()))
    tg_freq=np.array([freq[t] for t in TG])
    hi=np.percentile(tg_freq,80); lo=np.percentile(tg_freq,20)
    mask_rare=tg_freq<=lo; mask_freq=tg_freq>=hi
    print(f"[lock] τ(g0 5pct)={TAU:.3f}  slice rare<= {lo:.0f} freq>={hi:.0f} (n_rare={mask_rare.sum()} n_freq={mask_freq.sum()})",flush=True)

    # F per (seed,gen)
    rows=[]
    for s in SEEDS:
        for g in GENS:
            lp=LP[(s,g)]
            rows.append(dict(seed=s,gen=g,
                mean_lp=float(lp.mean()),
                F1_var=float(lp.var()),
                F1_tail=float((lp<TAU).mean()),
                F3_slice_rare=float(lp[mask_rare].mean()),
                F3_slice_freq=float(lp[mask_freq].mean()),
                F3_slice_gap=float(lp[mask_freq].mean()-lp[mask_rare].mean())))
    meanlp=np.array([r["mean_lp"] for r in rows]); gen=np.array([r["gen"] for r in rows])

    # 门A: cubic partial-corr(F,gen|meanlp); null = F0=meanlp^2 (纯 mean 函数)
    null_r=partial_corr_cubic(meanlp**2, gen, meanlp)
    Fnames=["F1_var","F1_tail","F3_slice_gap"]
    gateA={};
    for f in Fnames:
        Fv=np.array([r[f] for r in rows])
        gateA[f]=dict(partial_r=partial_corr_cubic(Fv,gen,meanlp),
                      raw_corr_gen=float(np.corrcoef(Fv,gen)[0,1]),
                      cubic_R2_on_meanlp=float(1-((Fv-np.vander(meanlp,4)@np.linalg.lstsq(np.vander(meanlp,4),Fv,rcond=None)[0]).var()/Fv.var())))
    # 门B: per-gen 5seed σ bootstrap 上界; 跨gen信号
    gateB={}
    for f in Fnames:
        per_gen_mean=[]; sig_up=[]
        for g in GENS:
            vals=[r[f] for r in rows if r["gen"]==g]
            per_gen_mean.append(np.mean(vals)); sig_up.append(boot_sigma_upper(vals))
        signal=float(max(per_gen_mean)-min(per_gen_mean)); floor=float(2*np.median(sig_up))
        gateB[f]=dict(cross_gen_signal=signal, k2_sigma_upper_floor=floor, passes=bool(signal>floor))

    # 判据
    verdict={}
    for f in Fnames:
        a=abs(gateA[f]["partial_r"])>abs(null_r)+0.15  # 超 null 上界 (留 margin)
        b=gateB[f]["passes"]
        verdict[f]=dict(gateA_pass=bool(a),gateB_pass=bool(b),branch1=bool(a and b))
    branch="Branch1" if any(verdict[f]["branch1"] for f in Fnames) else "Branch2"
    out=dict(locked_sha="733be69",tau=TAU,null_partialr=null_r,rows=rows,
             gateA=gateA,gateB=gateB,verdict=verdict,branch=branch,elapsed_s=round(time.time()-t0,1))
    json.dump(out,open(f"{OUT}/highorder_result.json","w"),indent=2,ensure_ascii=False)
    print(f"\n[null] cubic partial-r(meanlp^2,gen|meanlp)={null_r:+.3f}",flush=True)
    for f in Fnames:
        print(f"[{f}] 门A partial_r={gateA[f]['partial_r']:+.3f}(cubicR²_on_mean={gateA[f]['cubic_R2_on_meanlp']:.2f}) pass={verdict[f]['gateA_pass']} | 门B sig={gateB[f]['cross_gen_signal']:.4f} floor={gateB[f]['k2_sigma_upper_floor']:.4f} pass={verdict[f]['gateB_pass']} → branch1={verdict[f]['branch1']}",flush=True)
    print(f"\n[VERDICT] {branch}  (Branch2=C最强; Branch1=值得追尚非positive)  {time.time()-t0:.0f}s → {OUT}/highorder_result.json",flush=True)

if __name__=="__main__": main()
