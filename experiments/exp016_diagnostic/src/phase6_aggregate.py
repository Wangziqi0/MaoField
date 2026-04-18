"""Aggregate ablation results; compute BM25 top-20 baseline nDCG@10."""
import json, math, csv, os

PHASE6 = '/home/amd/HEZIMENG/MaoField/experiments/exp016_diagnostic/results/phase6_ablation'
OUT_CSV = '/home/amd/HEZIMENG/MaoField/experiments/exp016_diagnostic/results/ablation_matrix.csv'

def ndcg_at_k(order, qrels, k=10):
    rels = []
    for d in order[:k]:
        rels.append(int(qrels.get(d, 0)) if qrels.get(d, 0) else 0)
    dcg = sum((2**r - 1) / math.log2(i + 2) for i, r in enumerate(rels) if r > 0)
    ideal_rels = sorted([v for v in qrels.values() if isinstance(v,(int,float)) and v > 0], reverse=True)[:k]
    ideal = sum((2**r - 1) / math.log2(i + 2) for i, r in enumerate(ideal_rels))
    return dcg / ideal if ideal > 0 else 0.0

def p_at_k(order, qrels, k=10):
    hits = sum(1 for d in order[:k] if int(qrels.get(d,0) or 0) > 0)
    return hits / k

# Compute BM25 top-20 baseline by reading top-20 input and using candidate order
TOP20_DIR = '/home/amd/HEZIMENG/MaoField/experiments/exp016_diagnostic/inputs_top20'
bm25_top20 = {}
for ds in ['nfcorpus','scifact']:
    data = json.load(open(f'{TOP20_DIR}/{ds}_top20_input.json'))
    ndcgs = []
    p10s = []
    for q in data:
        order = [c['doc_id'] for c in q['candidates']]
        ndcgs.append(ndcg_at_k(order, q['qrels'], 10))
        p10s.append(p_at_k(order, q['qrels'], 10))
    bm25_top20[ds] = {
        'n': len(data),
        'bm25_ndcg10': sum(ndcgs)/len(ndcgs),
        'bm25_p10': sum(p10s)/len(p10s),
    }
    print(f'BM25 top-20 {ds}: n={len(data)} nDCG@10={bm25_top20[ds]["bm25_ndcg10"]:.4f} P@10={bm25_top20[ds]["bm25_p10"]:.4f}')

# baseline top-100 from batchA
bm25_top100 = {
    'nfcorpus': {'bm25_ndcg10': 0.3063, 'bm25_p10': 0.2173},
    'scifact':  {'bm25_ndcg10': 0.6594, 'bm25_p10': 0.0853},
}

variants = [
    ('D', 'top-20 pool',           'top20'),
    ('A', 'FUSION_STEPS=0',        'top100'),
    ('C', 'EVOLVE_STEPS=500',      'top100'),
    ('B', 'ScalarEngine',          'top100'),
    ('E', 'top-20 + fusion=0',     'top20'),
]

rows = []
for v, desc, pool in variants:
    for ds in ['nfcorpus','scifact']:
        out_path = f'{PHASE6}/variant_{v}_{ds}_out.json'
        d = json.load(open(out_path))
        bm25_ref = bm25_top20[ds] if pool=='top20' else bm25_top100[ds]
        rows.append({
            'variant': v,
            'desc': desc,
            'pool': pool,
            'dataset': ds,
            'n_queries': d['n_queries'],
            'bm25_ndcg10': round(bm25_ref['bm25_ndcg10'],4),
            'bm25_p10':   round(bm25_ref['bm25_p10'],4),
            'maofield_ndcg10': round(d['mao_ndcg10'],4),
            'maofield_p10':    round(d['mao_p10'],4),
            'runtime_s': round(d['total_time_s'],1),
        })
        print(f'Variant {v} ({desc}) {ds} pool={pool}: mao_nDCG={d["mao_ndcg10"]:.4f}  mao_P={d["mao_p10"]:.4f} bm25_nDCG={bm25_ref["bm25_ndcg10"]:.4f}')

with open(OUT_CSV, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['variant','desc','pool','dataset','n_queries','bm25_ndcg10','bm25_p10','maofield_ndcg10','maofield_p10','runtime_s'])
    w.writeheader()
    w.writerows(rows)
print(f'\nWrote {OUT_CSV}')
