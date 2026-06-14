#!/usr/bin/env python
"""exp019 unified offline PPL re-eval (runs on 36 CPU, fp32). Thin driver over
exp018_cat/src/metrics.compute_perplexity_on_dataset with the exact runner protocol:
wikitext-2-raw-v1 TEST split -> tokenize_and_block(64) -> batch 128.
Validated 2026-06-10: CPU-fp32 vs historical GPU values delta <= 0.011 PPL.
Usage: python ppl_reeval.py --ckpt PATH [PATH...] --out OUT.jsonl
"""
import os, sys, json, argparse, time
os.environ.setdefault("HF_HUB_OFFLINE","1"); os.environ.setdefault("HF_DATASETS_OFFLINE","1")
SRC = "/media/amd/raid1/canonical/projects/MaoField/experiments/exp018_cat/src"
sys.path.insert(0, SRC)
import torch; torch.set_num_threads(24)
from transformers import AutoTokenizer
from data_pipeline import load_wikitext2, tokenize_and_block
from metrics import compute_perplexity_on_dataset

ap = argparse.ArgumentParser()
ap.add_argument("--ckpt", nargs="+", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()
tok = AutoTokenizer.from_pretrained("facebook/opt-125m")
raw = load_wikitext2()
test_blocks = tokenize_and_block(raw["test"], tok, 64)
with open(a.out, "a") as f:
    for ck in a.ckpt:
        t0=time.time()
        d = compute_perplexity_on_dataset(model_path=ck, tokenizer_id="facebook/opt-125m",
            dataset=test_blocks, block_size=64, batch_size=128, fp16=False, device="cpu")
        rec = {"ckpt": ck, "test_perplexity": float(d["mean_perplexity"]), "elapsed": round(time.time()-t0,1)}
        f.write(json.dumps(rec)+"\n"); f.flush()
        print(rec, flush=True)
