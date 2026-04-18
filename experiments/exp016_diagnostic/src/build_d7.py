"""Build D7 CodeSearchNet Python subset in BEIR-like format.
docstring -> func_code_string retrieval. 10k pairs sampled from test+valid."""
import json, random, os
from datasets import load_dataset

random.seed(20260412)
OUT = "/home/amd/HEZIMENG/MaoField/experiments/exp016_diagnostic/data/codesearchnet"
os.makedirs(os.path.join(OUT, "qrels"), exist_ok=True)

ds_test = load_dataset("code_search_net", "python", split="test")
ds_val = load_dataset("code_search_net", "python", split="validation")

pool = []
for ds in (ds_test, ds_val):
    for ex in ds:
        doc = ex["func_documentation_string"]
        code = ex["func_code_string"]
        if not doc or not code: continue
        doc = doc.strip()
        if len(doc) < 20 or len(doc) > 1000: continue
        if len(code) < 50 or len(code) > 4000: continue
        pool.append((doc, code))

random.shuffle(pool)
pool = pool[:10000]
print(f"selected {len(pool)} pairs")

with open(os.path.join(OUT,"corpus.jsonl"),"w") as f:
    for i,(doc,code) in enumerate(pool):
        f.write(json.dumps({"_id": f"C{i}", "text": code, "title": ""}) + "\n")
with open(os.path.join(OUT,"queries.jsonl"),"w") as f:
    for i,(doc,code) in enumerate(pool):
        f.write(json.dumps({"_id": f"Q{i}", "text": doc}) + "\n")
with open(os.path.join(OUT,"qrels/test.tsv"),"w") as f:
    f.write("query-id\tcorpus-id\tscore\n")
    for i in range(len(pool)):
        f.write(f"Q{i}\tC{i}\t1\n")
print("done")
