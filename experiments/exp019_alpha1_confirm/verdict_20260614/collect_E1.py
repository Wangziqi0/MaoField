import sys, json, os
os.environ.setdefault("HF_HUB_OFFLINE","1"); os.environ.setdefault("HF_DATASETS_OFFLINE","1")
sys.path.insert(0, "/media/amd/raid1/canonical/wip/maofield_e0_isotropy_rerun_20260606")
import torch; torch.set_num_threads(16)
import rerun_e0_metric_panel as P
from transformers import AutoTokenizer, AutoModelForCausalLM
tok = AutoTokenizer.from_pretrained(P.TOKENIZER_ID)
val_ids, _v = P.build_val_blocks(tok)
CK = "/media/amd/raid1/canonical/wip/exp019_alpha1_confirm_run/raw"
out = {}
for A in ["0.0","1.0"]:
    for S in [101,102,103,104,105,106]:
        p = "%s/ckpt_alpha%s/no_preserve_seed%d/generation_1" % (CK, A, S)
        m = AutoModelForCausalLM.from_pretrained(p, torch_dtype=torch.float32)
        N, sv, svn, outer, H = P.accumulate(m, val_ids)
        met = P.layer_metrics(N, sv[11], svn[11], outer[11], H)
        out["a%s_s%d" % (A,S)] = met["PR_centered"]
        print("a%s_s%d L11_PR_centered=%.3f" % (A,S,met["PR_centered"]), flush=True)
        del m
json.dump(out, open("/tmp/exp019_collect/E1.json","w"))
print("E1_DONE", flush=True)
