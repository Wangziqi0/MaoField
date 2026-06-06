#!/usr/bin/env python
"""
rerun_e0_metric_panel.py — 干净复跑 E0 fp32 gen0-vs-gen1 度量 panel (额外 agent, D-?? 2026-06-06)

目的: 厘清 ultracode 无-trace "PR↑(升维)" vs 归档有-trace "a2 anisotropy↑(更集中)" 的打架,
     并锁死 frame(a)「崩溃→更低维→更可解释」的"低维"到底指哪个口径 (rogue-dim 是否 artifact)。

严于 ultracode 三条:
  1. 归档 jsonl trace (本脚本输出带 metric 定义 + ckpt sha256 + val 子集 recipe)
  2. 控 outlier-dim (raw PR / centered PR / 去 top-k coordinate PR)
  3. 多度量交叉 (raw-anisotropy + isotropy + 各种 PR + mean-share + rogue 占比 + eff-rank + d90)

忠实复现 candidate_c_runner.py:325-326 的 val 子集: wikitext-2 validation → block_size=64
  → shuffle(seed=42) → 前 256 block. a2 公式 = multi_layer_hook.compute_a2_anisotropy
  的 raw mean_pairwise_cos = ‖mean(normalized)‖² (注: 归档存的是 raw 值 NON 1-it; canonical
  代码 return 的是 1-abs(it)=isotropy, 二者符号翻转 = 本次要 flag 的 drift).

不下 frame 结论 / 不替 PI 决. 只输出 raw 数 + 三结局(a/b/c) 的判据,留 PI.
"""
from __future__ import annotations
import os, sys, json, hashlib, math, time
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np
import torch

CKPT_DIR = "/media/amd/raid1/maofield_ckpt_backup_20260529/5060_desktop/5060/E0_disentangle_S3/checkpoints/alpha0.0/no_preserve_seed42"
GEN0 = f"{CKPT_DIR}/generation_0"
GEN1 = f"{CKPT_DIR}/generation_1"
TOKENIZER_ID = "facebook/opt-125m"
BLOCK_SIZE = 64
VAL_SUBSET = 256
SEED = 42
BATCH = 16
ARCHIVED_A2_GEN0 = [0.7349,0.7441,0.7748,0.7996,0.8304,0.8593,0.8828,0.8955,0.9065,0.9116,0.9072,0.8754]
ARCHIVED_A2_GEN1 = [0.7380,0.7404,0.7733,0.7993,0.8334,0.8635,0.8889,0.9060,0.9216,0.9322,0.9366,0.9283]

def log(*a): print(f"[{time.strftime('%H:%M:%S')}]", *a, flush=True)

def sha256(path):
    h = hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda: f.read(1<<20), b""): h.update(c)
    return h.hexdigest()

def build_val_blocks(tokenizer):
    """wikitext-2 validation → 64-token blocks → shuffle(seed=42) → 前 256. 复现 runner."""
    from datasets import load_dataset
    last_err = None
    for name in ["wikitext-2-raw-v1", "wikitext-2-v1"]:
        try:
            ds = load_dataset("wikitext", name, split="validation")
            log(f"  loaded wikitext/{name} validation: {len(ds)} rows")
            variant = name
            break
        except Exception as e:
            last_err = e; log(f"  load wikitext/{name} fail: {e}")
    else:
        raise RuntimeError(f"无法离线加载 wikitext-2 validation: {last_err}")
    # concat 全文 → 单一 token 流 → 切 64 block (标准 LM blocking, 无 pad)
    text = "\n\n".join(t for t in ds["text"] if t.strip())
    ids = tokenizer(text, return_tensors=None)["input_ids"]
    n_blocks = len(ids)//BLOCK_SIZE
    blocks = [ids[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE] for i in range(n_blocks)]
    log(f"  total tokens={len(ids)} → {n_blocks} blocks of {BLOCK_SIZE}")
    rng = np.random.default_rng(SEED)
    perm = rng.permutation(len(blocks))  # 注: HF .shuffle(seed) 用别的 RNG, 顺序未必逐一致
    sel = perm[:min(VAL_SUBSET, len(blocks))]
    val = torch.tensor([blocks[i] for i in sel], dtype=torch.long)
    log(f"  val subset: {val.shape} (variant={variant})")
    return val, variant

@torch.no_grad()
def accumulate(model, val_ids):
    """流式累积 per-layer: N, sum_v[H], sum_vn[H], outer[H,H]=Σ v vᵀ (float64)."""
    L = 12
    H = model.config.hidden_size
    N = 0
    sum_v  = [np.zeros(H, dtype=np.float64) for _ in range(L)]
    sum_vn = [np.zeros(H, dtype=np.float64) for _ in range(L)]
    outer  = [np.zeros((H,H), dtype=np.float64) for _ in range(L)]
    model.eval()
    for i in range(0, val_ids.size(0), BATCH):
        batch = val_ids[i:i+BATCH]
        out = model(input_ids=batch, output_hidden_states=True, return_dict=True)
        hs = out.hidden_states[1:]  # skip embedding, 取 12 transformer 层
        for li, h in enumerate(hs):
            v = h.reshape(-1, H).double().numpy()        # [b*64, H] raw
            nrm = np.linalg.norm(v, axis=1, keepdims=True); nrm[nrm<1e-12]=1e-12
            vn = v / nrm
            sum_v[li]  += v.sum(0)
            sum_vn[li] += vn.sum(0)
            outer[li]  += v.T @ v
        N += val_ids[i:i+BATCH].shape[0]*val_ids.shape[1]
        log(f"    fwd {min(i+BATCH,val_ids.size(0))}/{val_ids.size(0)} seqs")
    return N, sum_v, sum_vn, outer, H

def pr(eigs):
    e = np.clip(eigs, 0, None); s = e.sum()
    return float((s*s)/(e*e).sum()) if (e*e).sum()>0 else float("nan")

def eff_rank(eigs):
    e = np.clip(eigs,0,None); s=e.sum()
    if s<=0: return float("nan")
    p = e/s; p = p[p>0]
    return float(np.exp(-(p*np.log(p)).sum()))

def d_frac(eigs, frac=0.9):
    e = np.sort(np.clip(eigs,0,None))[::-1]; s=e.sum()
    if s<=0: return float("nan")
    c = np.cumsum(e)/s
    return int(np.searchsorted(c, frac)+1)

def layer_metrics(N, sum_v, sum_vn, outer, H):
    """每层全 panel."""
    mean_v  = sum_v / N                     # [H] raw 均值
    mean_vn = sum_vn / N                    # [H] 归一化均值
    second  = outer / N                     # [H,H] 二阶矩 (un-centered)
    cov     = second - np.outer(mean_v, mean_v)  # centered 协方差
    cov     = (cov + cov.T)/2
    second  = (second + second.T)/2
    a2_raw  = float(mean_vn @ mean_vn)      # = 归档 a2 (raw anisotropy, higher=更集中)
    isotropy= 1.0 - abs(a2_raw)             # = canonical 代码 return 的口径
    eig_raw = np.linalg.eigvalsh(second)
    eig_cen = np.linalg.eigvalsh(cov)
    diagv   = np.clip(np.diag(cov),0,None)  # 各坐标方差 (rogue-dim 用)
    order   = np.argsort(diagv)[::-1]
    def pr_drop_coords(k):
        keep = np.sort(order[k:])
        sub = cov[np.ix_(keep,keep)]
        return pr(np.linalg.eigvalsh(sub))
    total_energy = float(np.trace(second))
    mean_energy  = float(mean_v @ mean_v)
    return {
        "a2_raw_anisotropy": a2_raw,           # 归档口径; ↑=更集中
        "isotropy_1_minus": isotropy,          # canonical 代码口径; ↑=更散
        "PR_raw_uncentered": pr(eig_raw),      # ultracode 大概率这个; ↑=升维
        "PR_centered": pr(eig_cen),            # 去均值后
        "PR_drop_top1_coord": pr_drop_coords(1),
        "PR_drop_top2_coord": pr_drop_coords(2),
        "PR_drop_top5_coord": pr_drop_coords(5),
        "mean_share": mean_energy/total_energy if total_energy>0 else float("nan"),  # 均值占二阶矩能量比; ↑=更 mean-主导=更各向异性
        "rogue_coord_share": float(diagv.max()/diagv.sum()) if diagv.sum()>0 else float("nan"),  # 最大单坐标方差占比 (Timkey rogue-dim)
        "lambda_max_share_centered": float(np.clip(eig_cen,0,None).max()/np.clip(eig_cen,0,None).sum()),
        "eff_rank_centered": eff_rank(eig_cen),
        "d90_centered": d_frac(eig_cen,0.9),
    }

def run_ckpt(path):
    from transformers import AutoModelForCausalLM
    log(f"  load {path}")
    model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.float32)
    sha = sha256(f"{path}/model.safetensors")
    N, sv, svn, oo, H = accumulate(model, VAL_IDS)
    layers = [layer_metrics(N, sv[i], svn[i], oo[i], H) for i in range(12)]
    del model
    return {"ckpt": path, "safetensors_sha256": sha, "N_tokens": N, "per_layer": layers}

if __name__ == "__main__":
    t0=time.time()
    log("=== rerun E0 metric panel (gen0 vs gen1, fp32, CPU) ===")
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(TOKENIZER_ID)
    log("tokenizer ok")
    VAL_IDS, VARIANT = build_val_blocks(tok)
    res = {"date":"2026-06-06","val_subset":{"source":"wikitext-2 validation","variant":VARIANT,
            "block_size":BLOCK_SIZE,"subset_size":int(VAL_IDS.size(0)),"seed":SEED,
            "note":"shuffle 用 numpy RNG, 与 HF .shuffle(seed=42) 顺序未必逐一致 → a2 复现若略偏属此因, 看方向+量级"},
           "metric_defs":{
             "a2_raw_anisotropy":"‖mean(L2-normalized token)‖² = 归档 jsonl 存的口径; higher=更各向异性=更集中",
             "isotropy_1_minus":"1-abs(a2_raw) = canonical multi_layer_hook.py:78 return 口径; higher=更散=less collapse (与归档差符号翻转=本次 flag 的 drift)",
             "PR_raw_uncentered":"participation ratio of un-centered 2nd-moment eigs; ultracode '升维' 大概率此口径",
             "PR_centered":"PR of mean-centered covariance eigs",
             "PR_drop_topk_coord":"去掉方差最大的 k 个坐标后 centered PR (Timkey rogue-dim 控制)",
             "mean_share":"‖mean_v‖²/trace(2nd-moment); 共同均值占能量比, ↑=更 mean-主导",
             "rogue_coord_share":"max 单坐标方差/总; Timkey rogue-dimension 指纹",
           },
           "archived_a2_gen0":ARCHIVED_A2_GEN0,"archived_a2_gen1":ARCHIVED_A2_GEN1}
    res["gen0"]=run_ckpt(GEN0)
    res["gen1"]=run_ckpt(GEN1)
    # 验证: 我复现的 a2 vs 归档
    repro0=[res["gen0"]["per_layer"][i]["a2_raw_anisotropy"] for i in range(12)]
    repro1=[res["gen1"]["per_layer"][i]["a2_raw_anisotropy"] for i in range(12)]
    res["a2_repro_check"]={
        "gen0_mean_repro":float(np.mean(repro0)),"gen0_mean_archived":float(np.mean(ARCHIVED_A2_GEN0)),
        "gen1_mean_repro":float(np.mean(repro1)),"gen1_mean_archived":float(np.mean(ARCHIVED_A2_GEN1)),
        "gen0_max_abs_layer_diff":float(np.max(np.abs(np.array(repro0)-np.array(ARCHIVED_A2_GEN0)))),
        "gen1_max_abs_layer_diff":float(np.max(np.abs(np.array(repro1)-np.array(ARCHIVED_A2_GEN1)))),
    }
    # gen0→gen1 关键 Δ (last layer + mean) 给三结局判据
    def col(g,k): return [res[g]["per_layer"][i][k] for i in range(12)]
    summary={}
    for k in ["a2_raw_anisotropy","isotropy_1_minus","PR_raw_uncentered","PR_centered",
              "PR_drop_top2_coord","mean_share","rogue_coord_share","eff_rank_centered"]:
        g0=np.array(col("gen0",k)); g1=np.array(col("gen1",k))
        summary[k]={"gen0_mean":float(np.nanmean(g0)),"gen1_mean":float(np.nanmean(g1)),
                    "delta_mean":float(np.nanmean(g1-g0)),
                    "gen0_last":float(g0[-1]),"gen1_last":float(g1[-1])}
    res["gen0_to_gen1_summary"]=summary
    out="/home/amd/.claude/jobs/40589e44/tmp/rerun_e0_panel_result.json"
    with open(out,"w") as f: json.dump(res,f,indent=2,ensure_ascii=False)
    log(f"=== done in {time.time()-t0:.1f}s → {out} ===")
    # 人读摘要
    print("\n===== A2 复现验证 (pipeline 可信度) =====")
    print(json.dumps(res["a2_repro_check"],indent=2,ensure_ascii=False))
    print("\n===== gen0→gen1 关键度量 (mean over 12 层) =====")
    for k,v in summary.items():
        arrow = "↑" if v["delta_mean"]>0 else ("↓" if v["delta_mean"]<0 else "=")
        print(f"  {k:24s} gen0={v['gen0_mean']:.4f} gen1={v['gen1_mean']:.4f}  Δ={v['delta_mean']:+.4f} {arrow}")
