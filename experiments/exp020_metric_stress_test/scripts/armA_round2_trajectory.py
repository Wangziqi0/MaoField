#!/usr/bin/env python3
"""
armA_round2_trajectory.py — exp020 臂A round2 (全轨迹熵 + 从 g2 干预 + seed42 复制).

round1 发现 (armA_firstlook): 分布层熵是"谷"(g2 最深), 链 g2→g9 自训练自愈~58%,
g9 残余 gap 内部不可逆。本 round 把这钉实:
  (1) 全轨迹 g0-g9 × 5 seed: 谷在哪 / 自愈多少 / g9 是否 flatten(g8→g9 delta).
  (2) 从 g2(真谷)内部干预: 最深塌缩能否内部恢复(对照链自身自愈).
  (3) seed42 复制 round1 g9 干预 (稳健).
全 CPU fp32, decode-free (logits 直接算熵), 无训练。
预注册预测承 prereg_exp020_draft_v1 §A.5 (committed 先于数据)。
"""
from __future__ import annotations
import sys, os, json, time
sys.path.insert(0, "/media/amd/raid1/canonical/projects/MaoField/experiments/exp018_cat/src")
os.environ.setdefault("HF_HUB_OFFLINE","1"); os.environ.setdefault("TOKENIZERS_PARALLELISM","false")
import torch, numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from data_pipeline import load_wikitext2, tokenize_and_block

ROOT="/media/amd/raid1/canonical/projects/MaoField/experiments/exp018_cat/data/checkpoints_armb/alpha0.0"
TOK="facebook/opt-125m"; N_CTX=128; BLOCK=64; BATCH=32; SEEDS=[1,2,3,4,42]
OUT="/media/amd/raid1/canonical/projects/MaoField/experiments/exp020_metric_stress_test/armA_round2_20260618"
def ckpt(s,g): return f"{ROOT}/no_preserve_seed{s}/generation_{g}"

@torch.no_grad()
def measure(model, blocks):
    Hs,n90s=[],[]
    for i in range(0,len(blocks),BATCH):
        ids=torch.tensor(blocks[i:i+BATCH]["input_ids"],dtype=torch.long)
        logits=model(input_ids=ids).logits.float()
        logp=torch.log_softmax(logits,-1); p=logp.exp()
        Hs.append((-(p*logp).sum(-1)).reshape(-1))
        ps,_=torch.sort(p,-1,descending=True); cdf=torch.cumsum(ps,-1)
        n90s.append(((cdf<0.9).sum(-1)+1).reshape(-1).float())
    Hbar=torch.cat(Hs).mean().item()
    return {"H_nats":Hbar,"eff_supp":float(np.exp(Hbar)),"n90":torch.cat(n90s).mean().item()}

def load(p): return AutoModelForCausalLM.from_pretrained(p,dtype=torch.float32).to("cpu").eval()
def soup(pa,pb,w=0.5):
    ma,mb=load(pa),load(pb); sa,sb=ma.state_dict(),mb.state_dict()
    for k in sa:
        if sa[k].dtype.is_floating_point: sa[k]=w*sa[k]+(1-w)*sb[k]
    ma.load_state_dict(sa); del mb; return ma.eval()
def add_noise(p,sr):
    m=load(p); sd=m.state_dict(); g=torch.Generator().manual_seed(0)
    for k in sd:
        if sd[k].dtype.is_floating_point and sd[k].numel()>1:
            sd[k]=sd[k]+torch.randn(sd[k].shape,generator=g)*(sr*sd[k].std().item())
    m.load_state_dict(sd); return m.eval()

def main():
    os.makedirs(OUT,exist_ok=True); t0=time.time()
    raw=load_wikitext2(); tok=AutoTokenizer.from_pretrained(TOK)
    if tok.pad_token is None: tok.pad_token=tok.eos_token
    blocks=tokenize_and_block(raw["train"],tok,BLOCK).select(range(N_CTX))
    print(f"[setup] ctx={N_CTX} {time.time()-t0:.1f}s",flush=True)
    res={}
    def run(label,model):
        t1=time.time(); m=measure(model,blocks); del model; res[label]=m
        print(f"[{label}] H={m['H_nats']:.4f} eff_supp={m['eff_supp']:.1f} ({time.time()-t1:.0f}s)",flush=True)

    # (1) 全轨迹
    for s in SEEDS:
        for g in range(10): run(f"traj_s{s}_g{g}", load(ckpt(s,g)))
    # (2) 从 g2 内部干预 (seed1)
    run("g2iv_noise_0.05_s1", add_noise(ckpt(1,2),0.05))
    run("g2iv_soup_g2s1_g2s42", soup(ckpt(1,2),ckpt(42,2)))    # 纯内部: 两深谷
    run("g2iv_soup_g2s1_g0s1",  soup(ckpt(1,2),ckpt(1,0)))     # control+: 注健康
    # (3) seed42 复制 round1 g9 干预
    run("g9iv_noise_0.05_s42", add_noise(ckpt(42,9),0.05))
    run("g9iv_soup_g9s42_g9s1", soup(ckpt(42,9),ckpt(1,9)))

    # 分析: 每 seed 谷位置 / 自愈 frac / g8->g9 flatten
    analysis={}
    for s in SEEDS:
        H={g:res[f"traj_s{s}_g{g}"]["H_nats"] for g in range(10)}
        trough_g=min(range(10),key=lambda g:H[g])
        g0,gt,g9=H[0],H[trough_g],H[9]
        selfheal=(g9-gt)/(g0-gt) if abs(g0-gt)>1e-9 else float("nan")
        residual=(g0-g9)/g0
        flatten=H[9]-H[8]
        analysis[s]={"trough_gen":trough_g,"H_g0":g0,"H_trough":gt,"H_g9":g9,
                     "selfheal_frac":selfheal,"residual_frac_of_g0":residual,"g8_to_g9_delta":flatten}
        print(f"[seed{s}] 谷@g{trough_g}(H={gt:.3f}) g0={g0:.3f} g9={g9:.3f} | 自愈={selfheal:+.1%} 残余={residual:.1%}of g0 | g8->g9 Δ={flatten:+.4f}",flush=True)
    # g2 内部恢复
    g0s1=res["traj_s1_g0"]["H_nats"]; g2s1=res["traj_s1_g2"]["H_nats"]; gap_g2=g0s1-g2s1
    g2rec={k:(res[k]["H_nats"]-g2s1)/gap_g2 for k in ["g2iv_noise_0.05_s1","g2iv_soup_g2s1_g2s42","g2iv_soup_g2s1_g0s1"]}
    analysis["g2_internal_recovery_frac"]=g2rec
    print(f"[g2 内部恢复 vs g0-g2 gap]: noise={g2rec['g2iv_noise_0.05_s1']:+.1%} soup2深谷={g2rec['g2iv_soup_g2s1_g2s42']:+.1%} soup健康={g2rec['g2iv_soup_g2s1_g0s1']:+.1%}",flush=True)

    json.dump({"measures":res,"analysis":analysis,"elapsed_s":round(time.time()-t0,1)},
              open(f"{OUT}/armA_round2_result.json","w"),indent=2,ensure_ascii=False)
    print(f"[done] → {OUT}/armA_round2_result.json ({time.time()-t0:.0f}s)",flush=True)

if __name__=="__main__": main()
