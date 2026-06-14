#!/usr/bin/env python
"""exp019 launcher wrapper — one chain. MUST be used for all 12 confirmatory chains.
Applies: (1) manual-LN patch (gfx1201 native_layer_norm_backward race, torch2.12+rocm7.2,
diagnosed 2026-06-11, see wip/maofield_armb_deepdive_20260610/exp019_stage0/);
(2) environment assertions; (3) run manifest (jsonl).
Usage: HIP_VISIBLE_DEVICES=0 python exp019_launch_chain.py --alpha {0.0|1.0} --seed S \
         --order-index K --manifest-dir DIR [--num-generations 10] [--config CONFIG]
"""
import os, sys, json, time, hashlib, subprocess, socket, argparse

# ---- assertions BEFORE torch import ----
assert os.environ.get("HIP_VISIBLE_DEVICES") == "0", "HIP_VISIBLE_DEVICES=0 required (iGPU exclusion)"
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("HF_DATASETS_OFFLINE", "1")

import torch
import torch.nn.functional as F
assert "rocm" in torch.__version__, "ROCm torch required, got %s (pip may have overwritten it)" % torch.__version__

def manual_layer_norm(x, normalized_shape, weight=None, bias=None, eps=1e-5):
    dims = tuple(range(-len(normalized_shape), 0))
    mu = x.mean(dims, keepdim=True)
    var = x.var(dims, keepdim=True, unbiased=False)
    xhat = (x - mu) / torch.sqrt(var + eps)
    if weight is not None: xhat = xhat * weight
    if bias is not None: xhat = xhat + bias
    return xhat
F.layer_norm = manual_layer_norm
torch.nn.functional.layer_norm = manual_layer_norm
print("[exp019] manual-LN patch active", flush=True)

ap = argparse.ArgumentParser()
ap.add_argument("--alpha", required=True)
ap.add_argument("--seed", required=True)
ap.add_argument("--order-index", required=True, type=int)
ap.add_argument("--manifest-dir", required=True)
ap.add_argument("--num-generations", default="10")
ap.add_argument("--config", default="configs/cat_arm_b.yaml")
a = ap.parse_args()

def sha256f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()

repo_root = os.path.expanduser("~/HEZIMENG/MaoField")
git_hash = subprocess.run(["git", "-C", repo_root, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip() or "no-git"
import transformers
man = {
    "chain_id": "a%s_s%s" % (a.alpha, a.seed), "alpha": a.alpha, "seed": a.seed,
    "order_index": a.order_index, "ts_start": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    "host": socket.gethostname(), "git_hash": git_hash,
    "config": a.config, "config_sha256": sha256f(a.config),
    "torch": torch.__version__, "transformers": transformers.__version__,
    "ln_patch": "manual_v1", "hip_visible_devices": os.environ.get("HIP_VISIBLE_DEVICES"),
}
os.makedirs(a.manifest_dir, exist_ok=True)
mpath = os.path.join(a.manifest_dir, "manifest_%s.jsonl" % man["chain_id"])
with open(mpath, "a") as f: f.write(json.dumps(man) + "\n")

sys.argv = ["run_arm_b_alpha_scan.py", "--alpha", a.alpha, "--seed", a.seed,
            "--num-generations", a.num_generations, "--config", a.config]
import runpy
t0 = time.time()
rc = 0
try:
    runpy.run_path("src/run_arm_b_alpha_scan.py", run_name="__main__")
except SystemExit as e:
    rc = e.code or 0
end = {"chain_id": man["chain_id"], "ts_end": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
       "elapsed_sec": round(time.time() - t0, 1), "exit": rc}
ckpt_base = "data/checkpoints_armb/alpha%s/no_preserve_seed%s" % (a.alpha, a.seed)
if os.path.isdir(ckpt_base):
    end["ckpt_sha256"] = {}
    for g in sorted(os.listdir(ckpt_base)):
        st = os.path.join(ckpt_base, g, "model.safetensors")
        if os.path.exists(st): end["ckpt_sha256"][g] = sha256f(st)
with open(mpath, "a") as f: f.write(json.dumps(end) + "\n")
print("[exp019] chain done rc=%s elapsed=%.0fs" % (rc, end["elapsed_sec"]), flush=True)
