"""Truncate candidates to top-20 per query from a BM25 top-100 stage1_input.json."""
import json, sys, os

TOP = 20
src_dir = '/home/amd/HEZIMENG/MaoField/experiments/exp016_diagnostic/results/phase4'
dst_dir = '/home/amd/HEZIMENG/MaoField/experiments/exp016_diagnostic/inputs_top20'
os.makedirs(dst_dir, exist_ok=True)

for ds in ['nfcorpus', 'scifact']:
    src = f'{src_dir}/{ds}_stage1_input.json'
    dst = f'{dst_dir}/{ds}_top20_input.json'
    d = json.load(open(src))
    for q in d:
        q['candidates'] = q['candidates'][:TOP]
    json.dump(d, open(dst, 'w'))
    print(f'{ds}: {len(d)} queries, each {len(d[0]["candidates"])} cands -> {dst}')

# Also a smoke-top20
src = f'{src_dir}/smoke_input.json'
dst = f'{dst_dir}/smoke_top20_input.json'
d = json.load(open(src))
for q in d:
    q['candidates'] = q['candidates'][:TOP]
json.dump(d, open(dst, 'w'))
print(f'smoke: {len(d)} queries, each {len(d[0]["candidates"])} cands')
