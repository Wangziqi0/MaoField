"""Phase 3 aggressive variant: force high substitution rate (target 60-80%).
Same 200 SciFact pairs; pick content words sorted by length desc and exhaust WordNet."""
import json, random, re
import numpy as np
from pathlib import Path

SEED = 20260412
random.seed(SEED); np.random.seed(SEED)

import nltk
from nltk.corpus import wordnet as wn
from nltk import pos_tag, word_tokenize
from rapidfuzz.distance import Levenshtein as Lev
from rank_bm25 import BM25Okapi

TOKEN_RE = re.compile(r"\w+", re.UNICODE)
def tokens_lower(s): return TOKEN_RE.findall(s.lower())

def s1(a,b):
    va = np.bincount(np.frombuffer(a.encode('utf-8'), dtype=np.uint8), minlength=256).astype(np.float32)
    vb = np.bincount(np.frombuffer(b.encode('utf-8'), dtype=np.uint8), minlength=256).astype(np.float32)
    na, nb = np.linalg.norm(va), np.linalg.norm(vb)
    return float(va @ vb/(na*nb)) if na>0 and nb>0 else 0.0
def s2(a,b):
    sa,sb=set(a),set(b); u=sa|sb; return len(sa&sb)/len(u) if u else 0.0
def _ng(s,n): return {s[i:i+n] for i in range(len(s)-n+1)} if len(s)>=n else {s}
def s3(a,b):
    sa,sb=_ng(a,2),_ng(b,2); u=sa|sb; return len(sa&sb)/len(u) if u else 0.0
def s4(a,b):
    sa,sb=_ng(a,3),_ng(b,3); u=sa|sb; return len(sa&sb)/len(u) if u else 0.0
def s5(a,b):
    a=a[:2000];b=b[:2000]; L=max(len(a),len(b))
    return 1.0-Lev.distance(a,b)/L if L else 1.0

WN_POS = {"NN":"n","NNS":"n","NNP":"n","NNPS":"n",
          "VB":"v","VBD":"v","VBG":"v","VBN":"v","VBP":"v","VBZ":"v",
          "JJ":"a","JJR":"a","JJS":"a","RB":"r","RBR":"r","RBS":"r"}

def get_synonyms(word, pos):
    wnpos = WN_POS.get(pos)
    if not wnpos: return []
    out=[]
    for syn in wn.synsets(word, pos=wnpos):
        for lem in syn.lemmas():
            name = lem.name().replace("_"," ")
            if name.lower() != word.lower() and " " not in name and name.isalpha():
                out.append(name)
    return list(dict.fromkeys(out))  # unique, ordered

def substitute_aggressive(text, target_frac=0.7):
    toks = word_tokenize(text); tagged = pos_tag(toks)
    candidates = [(i,w,p) for i,(w,p) in enumerate(tagged)
                  if p in WN_POS and w.isalpha() and len(w)>=3]
    # sort by word length desc (prioritize content-heavy words)
    candidates.sort(key=lambda x: -len(x[1]))
    n_target = max(1, int(len(candidates) * target_frac))
    out = list(toks); replaced = 0
    for i,w,p in candidates:
        if replaced >= n_target: break
        syns = get_synonyms(w, p)
        if syns:
            out[i] = random.choice(syns[:3])  # pick among top-3
            replaced += 1
    return " ".join(out), replaced, len(candidates)

SCIFACT = Path("/home/amd/HEZIMENG/legal-assistant/beir_data/scifact")
corpus={}
with open(SCIFACT/"corpus.jsonl") as f:
    for line in f:
        d=json.loads(line); corpus[d["_id"]]=(d.get("title","")+" "+d.get("text","")).strip()
queries={}
with open(SCIFACT/"queries.jsonl") as f:
    for line in f:
        d=json.loads(line); queries[d["_id"]]=d["text"]
qrels={}
with open(SCIFACT/"qrels"/"test.tsv") as f:
    next(f)
    for line in f:
        q,d,s=line.strip().split("\t")
        if int(s)>0: qrels.setdefault(q,{})[d]=int(s)

qids=[q for q in qrels if q in queries]
random.shuffle(qids); qids=qids[:200]

doc_ids=list(corpus.keys())
bm25=BM25Okapi([tokens_lower(corpus[d]) for d in doc_ids])
id_to_idx={d:i for i,d in enumerate(doc_ids)}

def score_all(q, cand_texts, cand_ids):
    qtoks=tokens_lower(q)
    bm=bm25.get_scores(qtoks)
    return {
        "s1_byte": [s1(q,t) for t in cand_texts],
        "s2_char": [s2(q,t) for t in cand_texts],
        "s3_2g":   [s3(q,t) for t in cand_texts],
        "s4_3g":   [s4(q,t) for t in cand_texts],
        "s5_lev":  [s5(q,t) for t in cand_texts],
        "s6_bm25": [float(bm[id_to_idx[c]]) for c in cand_ids],
    }

metrics=["s1_byte","s2_char","s3_2g","s4_3g","s5_lev","s6_bm25"]
delta_p={m:[] for m in metrics}
auc_o={m:[] for m in metrics}; auc_s={m:[] for m in metrics}
sub_stats=[]

def rank_auc(scores):
    pos=scores[0]; negs=scores[1:]
    below=sum(1 for x in negs if x<pos); tie=sum(1 for x in negs if x==pos)
    return (below+0.5*tie)/99.0

for qi,qid in enumerate(qids):
    orig=queries[qid]
    pos_id=max(qrels[qid], key=lambda d:qrels[qid][d])
    if pos_id not in corpus: continue
    neg_pool=[d for d in doc_ids if d not in qrels[qid]]
    negs=random.sample(neg_pool, 99)
    cand_ids=[pos_id]+negs
    cand_texts=[corpus[c] for c in cand_ids]

    so=score_all(orig, cand_texts, cand_ids)
    sub_q, n_sub, n_cand = substitute_aggressive(orig, target_frac=0.7)
    sub_stats.append((n_sub, n_cand))
    ss=score_all(sub_q, cand_texts, cand_ids)

    delta_p["s1_byte"].append(s1(orig,sub_q))
    delta_p["s2_char"].append(s2(orig,sub_q))
    delta_p["s3_2g"].append(s3(orig,sub_q))
    delta_p["s4_3g"].append(s4(orig,sub_q))
    delta_p["s5_lev"].append(s5(orig,sub_q))
    to1,to2=set(tokens_lower(orig)),set(tokens_lower(sub_q))
    delta_p["s6_bm25"].append(len(to1&to2)/len(to1|to2) if to1|to2 else 1.0)

    for m in metrics:
        auc_o[m].append(rank_auc(so[m]))
        auc_s[m].append(rank_auc(ss[m]))

    if (qi+1)%50==0: print(f"  [{qi+1}/{len(qids)}]")

frac_mean=np.mean([s[0]/max(1,s[1]) for s in sub_stats])
n_sub_mean=np.mean([s[0] for s in sub_stats])
n_cand_mean=np.mean([s[1] for s in sub_stats])
print(f"frac_mean={frac_mean:.3f} avg_subs={n_sub_mean:.2f}/{n_cand_mean:.2f}")

rows=[]
for m in metrics:
    rows.append({"metric":m,
        "delta_pair":float(np.mean(delta_p[m])),
        "auc_orig":float(np.mean(auc_o[m])),
        "auc_sub":float(np.mean(auc_s[m])),
        "drop_auc":float(np.mean(auc_o[m])-np.mean(auc_s[m]))})

import csv
OUT=Path("/home/amd/HEZIMENG/MaoField/experiments/exp016_diagnostic/results")
with open(OUT/"synonym_sensitivity_aggressive.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["metric","delta_pair","auc_orig","auc_sub","drop_auc"])
    w.writeheader()
    for r in rows: w.writerow(r)

lines=[f"# 阶段 3 (aggressive)：SciFact 激进同义词扰动",
       f"- 目标替换率 70%，优先换长实词",
       f"- 实际替换：{n_sub_mean:.2f}/{n_cand_mean:.2f} = {frac_mean*100:.1f}%",
       "",
       "| 度量 | Δ(原,替换) | AUC(原) | AUC(替换) | drop_AUC |",
       "|---|---|---|---|---|"]
for r in rows:
    lines.append(f"| {r['metric']} | {r['delta_pair']:.3f} | {r['auc_orig']:.3f} | {r['auc_sub']:.3f} | {r['drop_auc']:+.3f} |")
(OUT/"phase3_aggressive_summary.md").write_text("\n".join(lines))
print("DONE")
