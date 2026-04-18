"""Phase 3: Synonym sensitivity on SciFact (200 pairs).
Measure how each of S1-S6 degrades under WordNet synonym substitution of 30-50% content words."""
import json, random, re, os
import numpy as np
from pathlib import Path
from collections import Counter

SEED = 20260412
random.seed(SEED); np.random.seed(SEED)

import nltk
from nltk.corpus import wordnet as wn
from nltk import pos_tag, word_tokenize

# ---- metrics (copy from phase1_auc.py, kept identical) ----
from rapidfuzz.distance import Levenshtein as Lev
from rank_bm25 import BM25Okapi

TOKEN_RE = re.compile(r"\w+", re.UNICODE)
def tokens_lower(s): return TOKEN_RE.findall(s.lower())

def s1_byte_cos(a, b):
    va = np.bincount(np.frombuffer(a.encode('utf-8'), dtype=np.uint8), minlength=256).astype(np.float32)
    vb = np.bincount(np.frombuffer(b.encode('utf-8'), dtype=np.uint8), minlength=256).astype(np.float32)
    na, nb = np.linalg.norm(va), np.linalg.norm(vb)
    return float(va @ vb / (na*nb)) if na>0 and nb>0 else 0.0

def s2_char_jac(a, b):
    sa, sb = set(a), set(b)
    u = sa | sb
    return len(sa & sb)/len(u) if u else 0.0

def _ngrams(s, n):
    return {s[i:i+n] for i in range(len(s)-n+1)} if len(s)>=n else {s}

def s3_2gram(a, b):
    sa, sb = _ngrams(a, 2), _ngrams(b, 2)
    u = sa | sb
    return len(sa & sb)/len(u) if u else 0.0

def s4_3gram(a, b):
    sa, sb = _ngrams(a, 3), _ngrams(b, 3)
    u = sa | sb
    return len(sa & sb)/len(u) if u else 0.0

def s5_lev(a, b):
    a = a[:2000]; b = b[:2000]
    L = max(len(a), len(b))
    if L == 0: return 1.0
    return 1.0 - Lev.distance(a, b)/L

# ---- load SciFact ----
SCIFACT = Path("/home/amd/HEZIMENG/legal-assistant/beir_data/scifact")
corpus = {}
with open(SCIFACT/"corpus.jsonl") as f:
    for line in f:
        d = json.loads(line)
        corpus[d["_id"]] = (d.get("title","") + " " + d.get("text","")).strip()
queries = {}
with open(SCIFACT/"queries.jsonl") as f:
    for line in f:
        d = json.loads(line)
        queries[d["_id"]] = d["text"]

qrels = {}  # qid -> {doc_id: score}
with open(SCIFACT/"qrels"/"test.tsv") as f:
    next(f)
    for line in f:
        q,d,s = line.strip().split("\t")
        if int(s) > 0:
            qrels.setdefault(q, {})[d] = int(s)

# sample 200 queries with at least one positive
qids = [q for q in qrels if q in queries]
random.shuffle(qids)
qids = qids[:200]
print(f"SciFact sampled {len(qids)} queries")

# BM25 over full corpus
doc_ids = list(corpus.keys())
doc_toks = [tokens_lower(corpus[d]) for d in doc_ids]
bm25 = BM25Okapi(doc_toks)
id_to_idx = {d:i for i,d in enumerate(doc_ids)}

# ---- synonym replacement ----
WN_POS = {"NOUN":"n","VERB":"v","ADJ":"a","ADV":"r",
          "NN":"n","NNS":"n","NNP":"n","NNPS":"n",
          "VB":"v","VBD":"v","VBG":"v","VBN":"v","VBP":"v","VBZ":"v",
          "JJ":"a","JJR":"a","JJS":"a","RB":"r","RBR":"r","RBS":"r"}

def get_synonym(word, pos):
    wnpos = WN_POS.get(pos)
    if not wnpos: return None
    syns = wn.synsets(word, pos=wnpos)
    for syn in syns:
        for lemma in syn.lemmas():
            name = lemma.name().replace("_", " ")
            if name.lower() != word.lower() and " " not in name:
                return name
    return None

def substitute(text, frac_low=0.3, frac_high=0.5):
    toks = word_tokenize(text)
    tagged = pos_tag(toks)
    content_idx = [i for i,(w,p) in enumerate(tagged) if p in WN_POS and w.isalpha() and len(w)>=3]
    if not content_idx:
        return text, 0, 0
    n_sub = max(1, int(len(content_idx) * random.uniform(frac_low, frac_high)))
    pick = random.sample(content_idx, min(n_sub, len(content_idx)))
    replaced = 0
    out = list(toks)
    for i in pick:
        w, p = tagged[i]
        syn = get_synonym(w, p)
        if syn:
            out[i] = syn
            replaced += 1
    return " ".join(out), replaced, len(content_idx)

# ---- compute ----
metrics = ["s1_byte","s2_char","s3_2g","s4_3g","s5_lev","s6_bm25"]
delta_accum = {m: [] for m in metrics}

# For drop_AUC: need original AUC and replaced AUC using 1-vs-99 sampling
def metric_scores_on_candidates(query, cand_texts, cand_toks):
    """Return dict: metric -> list of scores over candidates"""
    out = {}
    out["s1_byte"] = [s1_byte_cos(query, t) for t in cand_texts]
    out["s2_char"] = [s2_char_jac(query, t) for t in cand_texts]
    out["s3_2g"]   = [s3_2gram(query, t) for t in cand_texts]
    out["s4_3g"]   = [s4_3gram(query, t) for t in cand_texts]
    out["s5_lev"]  = [s5_lev(query, t) for t in cand_texts]
    qtoks = tokens_lower(query)
    # bm25 scores via recomputing over cand set (not global) would change meaning;
    # use global bm25 model but restrict to cand indices
    global_scores = bm25.get_scores(qtoks)
    out["s6_bm25"] = [float(global_scores[id_to_idx[cid]]) for cid in cand_ids_ref[0]]
    return out

auc_orig = {m: [] for m in metrics}
auc_sub  = {m: [] for m in metrics}
sub_stats = []  # (n_sub, n_content)

cand_ids_ref = [None]  # hack for metric fn access

for qi, qid in enumerate(qids):
    orig_q = queries[qid]
    pos_ids = list(qrels[qid].keys())
    if not pos_ids: continue
    # pick the highest-scored positive
    pos_id = max(pos_ids, key=lambda d: qrels[qid][d])
    if pos_id not in corpus: continue
    # 99 random negatives
    neg_pool = [d for d in doc_ids if d not in qrels[qid]]
    negs = random.sample(neg_pool, 99)
    cand_ids = [pos_id] + negs
    cand_texts = [corpus[c] for c in cand_ids]
    cand_ids_ref[0] = cand_ids

    # original query scores
    scores_orig = metric_scores_on_candidates(orig_q, cand_texts, None)

    # synonym-substituted query
    sub_q, n_sub, n_content = substitute(orig_q)
    sub_stats.append((n_sub, n_content))
    scores_sub = metric_scores_on_candidates(sub_q, cand_texts, None)

    # Delta(orig,sub) = similarity between orig and substituted query texts
    delta_accum["s1_byte"].append(s1_byte_cos(orig_q, sub_q))
    delta_accum["s2_char"].append(s2_char_jac(orig_q, sub_q))
    delta_accum["s3_2g"].append(s3_2gram(orig_q, sub_q))
    delta_accum["s4_3g"].append(s4_3gram(orig_q, sub_q))
    delta_accum["s5_lev"].append(s5_lev(orig_q, sub_q))
    # bm25 between two short strings: use a pair-based bm25 is awkward; use s4 as proxy? No:
    # define bm25 Delta as token overlap count weighted—simpler: use Jaccard of token sets as "S6 Delta"
    # But we want a consistent "pair-similarity" metric. For BM25 we skip meaningful pair-Delta.
    # Report NA — use token Jaccard as a BM25-flavored proxy
    to1, to2 = set(tokens_lower(orig_q)), set(tokens_lower(sub_q))
    delta_accum["s6_bm25"].append(len(to1&to2)/len(to1|to2) if to1|to2 else 1.0)

    # AUC for each metric: positive rank among 100
    for m in metrics:
        def rank_auc(s):
            pos_s = s[0]
            neg_s = s[1:]
            # fraction of negs below pos (ties split)
            n_below = sum(1 for x in neg_s if x < pos_s)
            n_tie = sum(1 for x in neg_s if x == pos_s)
            return (n_below + 0.5*n_tie) / 99.0
        auc_orig[m].append(rank_auc(scores_orig[m]))
        auc_sub[m].append(rank_auc(scores_sub[m]))

    if (qi+1) % 50 == 0:
        print(f"  [{qi+1}/{len(qids)}] processed")

# ---- aggregate & write ----
n_sub_mean = np.mean([s[0] for s in sub_stats])
n_content_mean = np.mean([s[1] for s in sub_stats])
frac_mean = np.mean([s[0]/max(1,s[1]) for s in sub_stats])
print(f"substitution stats: avg_subs={n_sub_mean:.2f} avg_content={n_content_mean:.2f} frac={frac_mean:.3f}")

rows = []
for m in metrics:
    rows.append({
        "metric": m,
        "delta_pair_mean": float(np.mean(delta_accum[m])),
        "delta_pair_std": float(np.std(delta_accum[m])),
        "auc_orig": float(np.mean(auc_orig[m])),
        "auc_sub": float(np.mean(auc_sub[m])),
        "drop_auc": float(np.mean(auc_orig[m]) - np.mean(auc_sub[m])),
    })

import csv
OUT = Path("/home/amd/HEZIMENG/MaoField/experiments/exp016_diagnostic/results")
OUT.mkdir(exist_ok=True)
with open(OUT/"synonym_sensitivity.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=["metric","delta_pair_mean","delta_pair_std","auc_orig","auc_sub","drop_auc"])
    w.writeheader()
    for r in rows: w.writerow(r)

# summary md
lines = ["# 阶段 3：SciFact 同义词敏感性\n",
         f"- 样本：200 queries，WordNet 同义替换实词 30-50%",
         f"- 实际替换均值：{n_sub_mean:.2f} / {n_content_mean:.2f} 实词 ({frac_mean*100:.1f}%)",
         "",
         "| 度量 | Δ(原,替换) | AUC(原) | AUC(替换) | drop_AUC |",
         "|---|---|---|---|---|"]
for r in rows:
    lines.append(f"| {r['metric']} | {r['delta_pair_mean']:.3f} | {r['auc_orig']:.3f} | {r['auc_sub']:.3f} | {r['drop_auc']:+.3f} |")
lines.append("")
lines.append("**判读**：drop_AUC > 0.15 = 该度量对同义词严重敏感（源场盲）；Δ(原,替换) 越接近 1 = 该度量把替换前后看作等价文本。")
lines.append("")
lines.append("**S6 BM25 的 Δ 用 token Jaccard 代替**（BM25 本身是 query-doc 打分函数，不直接定义 query-query 相似度）。")

(OUT/"phase3_summary.md").write_text("\n".join(lines))
print("DONE. Wrote", OUT/"synonym_sensitivity.csv", "and", OUT/"phase3_summary.md")
