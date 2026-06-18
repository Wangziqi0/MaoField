#!/usr/bin/env python3
"""
armA_testB_pseudoflux.py — exp020 臂A test B (廉价版): decode 是否注入伪通量。

假说 (承讨论 + round2): g2→g9 熵自愈极可能是 decode 伪影 —— beam+rep_penalty=3.0
强制生成出比模型自身分布更杂的训练数据, 这股"通量"不是内生的, 是 decode 塞进去的。
通量=本质、内/外/decode=通道 框架的第一个硬证。

test: 在 g2(谷), 用 beam rep_penalty∈{1.0, 3.0} 生成 128-block 训练语料,
测语料的 unigram 熵 + distinct-2。
预测: rep=3.0 语料多样性 ≫ rep=1.0 → rep_penalty 注入伪通量(源存在);
      ≈ → 无伪通量, 自愈是真内生(通量假说不全=新发现)。
对照: g0(健康)rep=3.0 语料作 reference。
注: 本 test 证"伪通量源存在", 不证"它驱动了自愈"(后者=round3 剥 decode 重训整链, GPU)。
全 CPU fp32。
"""
from __future__ import annotations
import sys, os, json, time, math
sys.path.insert(0, "/media/amd/raid1/canonical/projects/MaoField/experiments/exp018_cat/src")
os.environ.setdefault("HF_HUB_OFFLINE","1"); os.environ.setdefault("TOKENIZERS_PARALLELISM","false")
import torch
from collections import Counter
from transformers import AutoTokenizer
from data_pipeline import load_wikitext2, tokenize_and_block
from generate_synthetic import generate_synthetic_dataset
from metrics import compute_distinct_n

ROOT="/media/amd/raid1/canonical/projects/MaoField/experiments/exp018_cat/data/checkpoints_armb/alpha0.0"
TOK="facebook/opt-125m"; N=128; BLOCK=64
OUT="/media/amd/raid1/canonical/projects/MaoField/experiments/exp020_metric_stress_test/armA_testB_20260618"
def ckpt(s,g): return f"{ROOT}/no_preserve_seed{s}/generation_{g}"

def unigram_entropy(texts):
    """生成语料的 token unigram 分布熵 (nats), 衡量训练数据有多杂。"""
    c=Counter()
    for t in texts:
        for w in t.split(): c[w]+=1
    tot=sum(c.values())
    if tot==0: return 0.0
    return -sum((n/tot)*math.log(n/tot) for n in c.values())

def gen_corpus(ck, tok, prompts, rep):
    syn=generate_synthetic_dataset(ck, TOK, prompts, num_beams=5, prompt_length=64,
                                   max_new_tokens=64, batch_size=32, fp16=False,
                                   device="cpu", repetition_penalty=rep)
    return [tok.decode(r, skip_special_tokens=True) for r in syn["input_ids"]]

def main():
    os.makedirs(OUT,exist_ok=True); t0=time.time()
    raw=load_wikitext2(); tok=AutoTokenizer.from_pretrained(TOK)
    if tok.pad_token is None: tok.pad_token=tok.eos_token
    prompts=tokenize_and_block(raw["train"],tok,BLOCK).select(range(N))
    print(f"[setup] N={N} {time.time()-t0:.1f}s",flush=True)

    res={}
    def run(label, s, g, rep):
        t1=time.time(); txt=gen_corpus(ckpt(s,g),tok,prompts,rep)
        ue=unigram_entropy(txt); d2=compute_distinct_n(txt,2)
        res[label]={"unigram_H":ue,"distinct_2":d2}
        print(f"[{label}] unigram_H={ue:.4f} distinct2={d2:.4f} ({time.time()-t1:.0f}s)",flush=True)

    # g2 谷: rep 1.0 vs 3.0 (seed1+42 复制)
    for s in [1,42]:
        run(f"g2_s{s}_rep1.0", s, 2, 1.0)
        run(f"g2_s{s}_rep3.0", s, 2, 3.0)
    # g0 健康 reference (rep3.0)
    run("g0_s1_rep3.0", 1, 0, 3.0)

    # 裁定: rep3 语料是否比 rep1 更杂 (= rep_penalty 注伪通量)
    verdict={}
    for s in [1,42]:
        r1=res[f"g2_s{s}_rep1.0"]; r3=res[f"g2_s{s}_rep3.0"]
        dH=r3["unigram_H"]-r1["unigram_H"]; dd2=r3["distinct_2"]-r1["distinct_2"]
        verdict[f"seed{s}"]={"d_unigramH_rep3_minus_rep1":dH,"d_distinct2":dd2,
                             "rep3_injects_flux": bool(dH>0.1 and dd2>0.02)}
        print(f"[verdict s{s}] rep3−rep1: ΔunigramH={dH:+.4f} Δdistinct2={dd2:+.4f} → 注伪通量={verdict[f'seed{s}']['rep3_injects_flux']}",flush=True)
    json.dump({"measures":res,"verdict":verdict,"elapsed_s":round(time.time()-t0,1)},
              open(f"{OUT}/armA_testB_result.json","w"),indent=2,ensure_ascii=False)
    print(f"[done] → {OUT}/armA_testB_result.json ({time.time()-t0:.0f}s)",flush=True)

if __name__=="__main__": main()
