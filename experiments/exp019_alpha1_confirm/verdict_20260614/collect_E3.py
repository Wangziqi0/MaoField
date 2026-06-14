import sys, json, os
os.environ.setdefault("HF_HUB_OFFLINE","1"); os.environ.setdefault("HF_DATASETS_OFFLINE","1")
sys.path.insert(0, "/media/amd/raid1/canonical/wip/maofield_armb_deepdive_20260610")
import torch; torch.set_num_threads(16)
import launch_dppl_bridge as L
CK = "/media/amd/raid1/canonical/wip/exp019_alpha1_confirm_run/raw"
VAL_SEEDS = [1, 7, 42]
batchsets = {vs: L.reproduce_val_batch(vs, 256, 64, 8, None)[0] for vs in VAL_SEEDS}
print("val batches ready", flush=True)
out = {}
for A in ["0.0","1.0"]:
    for S in [101,102,103,104,105,106]:
        base = "%s/ckpt_alpha%s/no_preserve_seed%d" % (CK, A, S)
        models = {g: L.load_model("%s/generation_%d" % (base,g), "fp32", None) for g in [1,2,3,4,5]}
        tmeans = []
        for n in [2,3,4,5]:
            kls = [L.compute_kl_q_to_p(models[n], models[n-1], batchsets[vs], None)[0] for vs in VAL_SEEDS]
            tmeans.append(sum(kls)/len(kls))
        r = sum(tmeans)/len(tmeans)
        out["a%s_s%d" % (A,S)] = r
        print("a%s_s%d pathB_window_r=%.4f" % (A,S,r), flush=True)
        for g in list(models): del models[g]
json.dump(out, open("/tmp/exp019_collect/E3.json","w"))
print("E3_DONE", flush=True)
