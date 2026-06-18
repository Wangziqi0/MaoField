#!/usr/bin/env python3
"""
armA_reversal_distentropy.py — exp020 臂A 逆转实验 first-look (分布层直接测, decode-free).

预注册预测 (prereg_exp020_draft_v1.md §A.5, committed 2c2adcc 先于本数据):
  H_irreversible: 已塌缩 g9 在"无外部真实数据"的内部干预下, 分布层多样性
  (熵/有效支撑) 不可恢复; 信息须箱外来。
  falsify: 某纯内部廉价干预使恢复 ≥ ~50% (g0−g9 gap) ⇒ P1 死 = 新发现。

测度 (decode-free, 在固定真实 wikitext context 上 forward, 不生成):
  - H̄ = 逐 token next-token 分布熵, 在所有 position 均值 (nats)
  - eff_supp = exp(H̄) (有效词表大小, 几何均)
  - n90 = 达 0.9 累积概率所需 token 数, position 均值

模型: α=0 链 ckpt (alpha0.0/no_preserve_seed{s}/generation_{g}).
干预 (g9, seed1): 加噪 / souping (纯内部: g9+g9其他seed, g9+g2; control+: g9+g0).
方法: CPU fp32; 复用 metrics 口径精神, 但熵是 logits 直接算不经 decode。
"""
from __future__ import annotations
import sys, os, json, time, copy
sys.path.insert(0, "/media/amd/raid1/canonical/projects/MaoField/experiments/exp018_cat/src")
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
import torch
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from data_pipeline import load_wikitext2, tokenize_and_block

ROOT = "/media/amd/raid1/canonical/projects/MaoField/experiments/exp018_cat/data/checkpoints_armb/alpha0.0"
TOK = "facebook/opt-125m"
N_CTX = 128           # context blocks (前 N train 块; first-look)
BLOCK = 64
BATCH = 32
OUT = "/media/amd/raid1/canonical/projects/MaoField/experiments/exp020_metric_stress_test/armA_firstlook_20260618"

def ckpt(s, g): return f"{ROOT}/no_preserve_seed{s}/generation_{g}"

@torch.no_grad()
def measure(model, blocks):
    """返回 (H̄ nats, eff_supp=exp(H̄), n90)。decode-free: 直接 logits 算熵。"""
    Hs, n90s = [], []
    n = len(blocks)
    for i in range(0, n, BATCH):
        ids = torch.tensor(blocks[i:i+BATCH]["input_ids"], dtype=torch.long)
        out = model(input_ids=ids)
        logits = out.logits.float()                       # (B,T,V)
        logp = torch.log_softmax(logits, dim=-1)
        p = logp.exp()
        H = -(p * logp).sum(-1)                            # (B,T) nats
        Hs.append(H.reshape(-1))
        # n90: 排序累积到 0.9 所需 token 数
        ps, _ = torch.sort(p, dim=-1, descending=True)
        cdf = torch.cumsum(ps, dim=-1)
        n90 = (cdf < 0.9).sum(-1) + 1                      # (B,T)
        n90s.append(n90.reshape(-1).float())
    Hbar = torch.cat(Hs).mean().item()
    n90bar = torch.cat(n90s).mean().item()
    return {"H_nats": Hbar, "eff_supp": float(np.exp(Hbar)), "n90": n90bar}

def load(path):
    return AutoModelForCausalLM.from_pretrained(path, dtype=torch.float32).to("cpu").eval()

def soup(pa, pb, w=0.5):
    """权重平均 (model soup)。"""
    ma, mb = load(pa), load(pb)
    sa, sb = ma.state_dict(), mb.state_dict()
    for k in sa:
        if sa[k].dtype.is_floating_point:
            sa[k] = w * sa[k] + (1 - w) * sb[k]
    ma.load_state_dict(sa); del mb
    return ma.eval()

def add_noise(path, sigma_rel):
    """每参数加 N(0, sigma_rel * 该张量 std) 噪声。"""
    m = load(path); sd = m.state_dict()
    g = torch.Generator().manual_seed(0)
    for k in sd:
        if sd[k].dtype.is_floating_point and sd[k].numel() > 1:
            s = sd[k].std().item()
            sd[k] = sd[k] + torch.randn(sd[k].shape, generator=g) * (sigma_rel * s)
    m.load_state_dict(sd); return m.eval()

def main():
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    raw = load_wikitext2(); tok = AutoTokenizer.from_pretrained(TOK)
    if tok.pad_token is None: tok.pad_token = tok.eos_token
    train = tokenize_and_block(raw["train"], tok, BLOCK)
    blocks = train.select(range(N_CTX))
    print(f"[setup] ctx={N_CTX} blocks, {time.time()-t0:.1f}s", flush=True)

    res = {}
    def run(label, model):
        t1 = time.time(); m = measure(model, blocks); del model
        print(f"[{label}] H={m['H_nats']:.4f} eff_supp={m['eff_supp']:.1f} n90={m['n90']:.1f} ({time.time()-t1:.0f}s)", flush=True)
        res[label] = m

    # 轨迹 (seed1 + seed42): 确认分布层塌缩 + 曲线
    for s in [1, 42]:
        for g in [0, 2, 5, 9]:
            run(f"traj_s{s}_g{g}", load(ckpt(s, g)))

    # 干预 (g9 seed1)
    run("iv_noise_0.02", add_noise(ckpt(1, 9), 0.02))
    run("iv_noise_0.05", add_noise(ckpt(1, 9), 0.05))
    run("iv_soup_g9s1_g9s42", soup(ckpt(1, 9), ckpt(42, 9)))   # 纯内部: 两塌缩
    run("iv_soup_g9s1_g2s1",  soup(ckpt(1, 9), ckpt(1, 2)))    # 内部: 再注早代轨迹
    run("iv_soup_g9s1_g0s1",  soup(ckpt(1, 9), ckpt(1, 0)))    # control+: 注健康权重

    # 裁定 (对 seed1: 内部干预恢复了多少 g0-g9 gap)
    g0, g9 = res["traj_s1_g0"]["H_nats"], res["traj_s1_g9"]["H_nats"]
    gap = g0 - g9
    verdict = {"g0_H": g0, "g9_H": g9, "gap": gap, "recovery_frac": {}}
    for k in ["iv_noise_0.02","iv_noise_0.05","iv_soup_g9s1_g9s42","iv_soup_g9s1_g2s1","iv_soup_g9s1_g0s1"]:
        frac = (res[k]["H_nats"] - g9) / gap if abs(gap) > 1e-9 else float("nan")
        verdict["recovery_frac"][k] = frac
        print(f"[recovery] {k}: {frac:+.1%} of (g0-g9) gap", flush=True)
    internal = ["iv_noise_0.02","iv_noise_0.05","iv_soup_g9s1_g9s42","iv_soup_g9s1_g2s1"]
    max_internal = max(verdict["recovery_frac"][k] for k in internal)
    verdict["max_internal_recovery"] = max_internal
    verdict["P1_call"] = ("FALSIFIED(可逆=新发现)" if max_internal >= 0.50
                          else "SUPPORTED(内部不可逆)" if max_internal < 0.20
                          else "[?]中间区")
    print(f"\n[P1] max 内部恢复={max_internal:+.1%} → {verdict['P1_call']}", flush=True)

    json.dump({"measures": res, "verdict": verdict, "elapsed_s": round(time.time()-t0,1)},
              open(f"{OUT}/armA_firstlook_result.json","w"), indent=2, ensure_ascii=False)
    print(f"[done] → {OUT}/armA_firstlook_result.json  ({time.time()-t0:.0f}s)", flush=True)

if __name__ == "__main__":
    main()
