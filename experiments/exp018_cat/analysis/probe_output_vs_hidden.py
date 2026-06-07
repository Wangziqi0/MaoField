#!/usr/bin/env python
"""probe_output_vs_hidden.py — E0 gen0 vs gen1: 输出端 vs 隐层端 (检验假说②张力).
假说②: 崩溃中 输出收缩(pred entropy↓/top1↑) vs 隐层发散(末层 PR↑) 反向?
⚠️ caveat: pred_entropy = held-out 预测不确定性, NON 生成多样性. 真"model collapse 输出收缩"
   (generation diversity↓) 需额外 autoregressive gen 测. N=1 gen-step. 便宜 sanity 非判决.
忠实复现 val 子集 (wikitext-2 validation, block64, numpy shuffle seed42, 256).
"""
from __future__ import annotations
import os, time, json
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np, torch
CKPT = "/media/amd/raid1/maofield_ckpt_backup_20260529/5060_desktop/5060/E0_disentangle_S3/checkpoints/alpha0.0/no_preserve_seed42"
GEN0 = f"{CKPT}/generation_0"; GEN1 = f"{CKPT}/generation_1"; TOK = "facebook/opt-125m"
BLOCK = 64; SUBSET = 256; SEED = 42; BATCH = 16

def log(*a): print(f"[{time.strftime('%H:%M:%S')}]", *a, flush=True)

def build_val(tokenizer):
    from datasets import load_dataset
    for name in ["wikitext-2-raw-v1", "wikitext-2-v1"]:
        try: ds = load_dataset("wikitext", name, split="validation"); break
        except Exception as e: log("load fail", name, e)
    else: raise RuntimeError("no wikitext")
    text = "\n\n".join(t for t in ds["text"] if t.strip())
    ids = tokenizer(text, return_tensors=None)["input_ids"]
    nb = len(ids) // BLOCK; blocks = [ids[i*BLOCK:(i+1)*BLOCK] for i in range(nb)]
    rng = np.random.default_rng(SEED); perm = rng.permutation(len(blocks))
    sel = perm[:min(SUBSET, len(blocks))]
    return torch.tensor([blocks[i] for i in sel], dtype=torch.long)

@torch.no_grad()
def metrics(model, val):
    model.eval(); H = model.config.hidden_size
    ent = 0.0; top1 = 0.0; nll = 0.0; n = 0
    outer = np.zeros((H, H)); Nt = 0
    for i in range(0, val.size(0), BATCH):
        b = val[i:i+BATCH]
        out = model(input_ids=b, output_hidden_states=True, return_dict=True)
        lg = out.logits.float()                       # [B,T,V]
        logp = torch.log_softmax(lg, dim=-1); p = logp.exp()
        e = -(p * logp).sum(-1)                        # [B,T] predictive entropy (nats)
        t1 = p.max(-1).values                          # [B,T] top-1 prob (peakiness)
        tgt = b[:, 1:]; lp = logp[:, :-1, :].gather(-1, tgt.unsqueeze(-1)).squeeze(-1)
        nll += float(-lp.sum())
        ent += float(e.sum()); top1 += float(t1.sum()); n += e.numel()
        h = out.hidden_states[-1].reshape(-1, H).double().numpy()
        outer += h.T @ h; Nt += h.shape[0]
        log(f"  fwd {min(i+BATCH,val.size(0))}/{val.size(0)}")
    second = outer / Nt; eig = np.linalg.eigvalsh((second + second.T)/2); ec = np.clip(eig, 0, None)
    PR = float((ec.sum()**2) / (ec*ec).sum())
    ntok = val.size(0) * (val.size(1) - 1)
    return {"ppl_proxy": float(np.exp(nll/ntok)), "mean_pred_entropy_nats": ent/n,
            "mean_top1_prob": top1/n, "last_layer_PR_raw": PR}

if __name__ == "__main__":
    from transformers import AutoTokenizer, AutoModelForCausalLM
    t0 = time.time(); tok = AutoTokenizer.from_pretrained(TOK)
    val = build_val(tok); log("val", tuple(val.shape))
    R = {}
    for g, pth in [("gen0", GEN0), ("gen1", GEN1)]:
        log("load", g); m = AutoModelForCausalLM.from_pretrained(pth, torch_dtype=torch.float32)
        R[g] = metrics(m, val); del m; log(g, R[g])
    print("\n===== E0 gen0→gen1: 输出端 vs 隐层端 =====")
    for k in ["ppl_proxy", "mean_pred_entropy_nats", "mean_top1_prob", "last_layer_PR_raw"]:
        g0 = R["gen0"][k]; g1 = R["gen1"][k]; ar = "↑" if g1 > g0 else ("↓" if g1 < g0 else "=")
        print(f"  {k:26s} gen0={g0:.4f} gen1={g1:.4f}  {ar}")
    R["_meta"] = {"caveat": "pred_entropy=held-out 预测不确定性 NON 生成多样性; 真输出收缩需 autoregressive gen 测",
                  "N_gen_step": 1, "seed": SEED, "date": "2026-06-06",
                  "hypothesis2": "输出收缩(entropy↓/top1↑) vs 隐层发散(PR↑) 反向?"}
    out = "/home/amd/.claude/jobs/616da7b6/tmp/probe_output_vs_hidden_result.json"
    json.dump(R, open(out, "w"), indent=2, ensure_ascii=False)
    print(f"\ndone {time.time()-t0:.1f}s → {out}")
