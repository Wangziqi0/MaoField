#!/usr/bin/env python
"""exp020 round3 消融 launcher — 剥外通道, 测 collapse 是否变单调更深(无自愈)。
承 ARMA_FINDINGS_20260618: 自迭代 setup 含两条常驻真实锚 (真 prompt + gen0 base 重置);
消融测它们的因果作用。本 launcher = exp019_launch_chain 同款 manual-LN patch 包装。

应用: (1) manual-LN patch (gfx1201 native_layer_norm_backward race, torch2.12+rocm7.2,
binding: 22 上任何 ROCm 训练必须经此 patch); (2) HIP_VISIBLE_DEVICES=0 (排 iGPU);
(3) 跑 run_arm_b_ablation.py 的 --base-mode {gen0|prev}。

用法 (cwd=exp018_cat):
  HIP_VISIBLE_DEVICES=0 .venv/bin/python exp020_ablation_launch.py \
    --seed 1 --base-mode prev --output-base data/checkpoints_armb_ABL_baseprev \
    [--num-generations 10] [--smoke]
"""
import os, sys, json, time, socket, argparse

assert os.environ.get("HIP_VISIBLE_DEVICES") == "0", "HIP_VISIBLE_DEVICES=0 required (iGPU exclusion)"
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("HF_DATASETS_OFFLINE", "1")

import torch
import torch.nn.functional as F
assert "rocm" in torch.__version__, "ROCm torch required, got %s" % torch.__version__

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
print("[exp020-abl] manual-LN patch active", flush=True)

ap = argparse.ArgumentParser()
ap.add_argument("--seed", required=True)
ap.add_argument("--base-mode", required=True, choices=["gen0", "prev"])
ap.add_argument("--output-base", required=True)
ap.add_argument("--num-generations", default="10")
ap.add_argument("--config", default="configs/cat_arm_b.yaml")
ap.add_argument("--smoke", action="store_true")
ap.add_argument("--manifest-dir", default="../exp020_metric_stress_test/round3_ablation_manifests")
a = ap.parse_args()

os.makedirs(a.manifest_dir, exist_ok=True)
man = {"exp": "exp020_round3_ablation", "seed": a.seed, "base_mode": a.base_mode,
       "output_base": a.output_base, "ts_start": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
       "host": socket.gethostname(), "torch": torch.__version__, "ln_patch": "manual_v1",
       "num_generations": a.num_generations, "smoke": a.smoke}
mpath = os.path.join(a.manifest_dir, "manifest_abl_%s_s%s.jsonl" % (a.base_mode, a.seed))
with open(mpath, "a") as f: f.write(json.dumps(man) + "\n")
print("[exp020-abl] seed=%s base_mode=%s out=%s smoke=%s" % (a.seed, a.base_mode, a.output_base, a.smoke), flush=True)

argv = ["run_arm_b_ablation.py", "--alpha", "0.0", "--seed", a.seed,
        "--condition", "no_preserve", "--num-generations", a.num_generations,
        "--config", a.config, "--base-mode", a.base_mode, "--output-base", a.output_base]
if a.smoke: argv.append("--smoke-test")
sys.argv = argv

import runpy
t0 = time.time(); rc = 0
try:
    runpy.run_path("src/run_arm_b_ablation.py", run_name="__main__")
except SystemExit as e:
    rc = e.code or 0
with open(mpath, "a") as f:
    f.write(json.dumps({"seed": a.seed, "base_mode": a.base_mode,
                        "ts_end": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                        "elapsed_sec": round(time.time()-t0, 1), "exit": rc}) + "\n")
print("[exp020-abl] done rc=%s elapsed=%.0fs" % (rc, time.time()-t0), flush=True)
