#!/usr/bin/env python
"""recovery_geometry_panel.py — exp019 12 链 gen0-9 末层表示几何, 对齐 PPL 驼峰.

检验 fresh-eyes 盲点: E0「崩溃→升维」测的是 gen0→gen1 (= PPL U 型上升边/峰前一步);
恢复相 (gen2→gen9, PPL 回落) 的隐层几何从没测过. 问题:
  几何在恢复相 反转(→ 升维=驼峰峰瞬态, E0 核心 claim 被削)
  还是 继续散(→ 几何 vs PPL 第二个解耦, 叠在 多样性 vs PPL 上)?

复用 rerun_e0_metric_panel 的口径 (同 val 子集 + 同 layer_metrics), 不另造, 防口径漂移.
口径自检: α0 s101 gen1 的 PR_centered 应 ≈ pairs.json E1["101"][0]=200.638.
"""
from __future__ import annotations
import os, sys, json, glob, time
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
import numpy as np, torch
sys.path.insert(0, "/media/amd/raid1/canonical/projects/MaoField/experiments/exp018_cat/analysis")
import rerun_e0_metric_panel as e0   # 复用 build_val_blocks / accumulate / layer_metrics 口径

RAW = "/media/amd/raid1/canonical/wip/exp019_alpha1_confirm_run/raw"
ARMS = ["alpha0.0", "alpha1.0"]
SEEDS = [101, 102, 103, 104, 105, 106]
GENS = list(range(10))
LAST = 11  # L12 末层 index (E0/exp019-E1 同)
OUT = "/home/amd/.claude/jobs/71b26205/tmp/recovery_geometry_panel_result.json"

def log(*a): print(f"[{time.strftime('%H:%M:%S')}]", *a, flush=True)

def load_ppl():
    ppl = {}
    for arm in ARMS:
        for seed in SEEDS:
            fs = glob.glob(f"{RAW}/armb_{arm}_seed{seed}_*.jsonl")
            if not fs: continue
            seq = {}
            for line in open(fs[0]):
                line = line.strip()
                if not line: continue
                try: d = json.loads(line)
                except Exception: continue
                g = d.get("generation", d.get("gen"))
                p = d.get("test_perplexity", d.get("test_ppl"))
                if g is not None and p is not None:
                    try: seq[int(g)] = float(p)
                    except Exception: pass
            if seq: ppl[f"{arm}_s{seed}"] = seq
    return ppl

if __name__ == "__main__":
    t0 = time.time()
    pilot = len(sys.argv) > 1 and sys.argv[1] == "pilot"
    arms = ["alpha0.0"] if pilot else ARMS
    seeds = [101] if pilot else SEEDS
    from transformers import AutoTokenizer, AutoModelForCausalLM
    tok = AutoTokenizer.from_pretrained(e0.TOKENIZER_ID)
    val, variant = e0.build_val_blocks(tok)
    log(f"val {tuple(val.shape)} variant={variant} | mode={'PILOT' if pilot else 'FULL'}")
    geom = {}
    for arm in arms:
        for seed in seeds:
            chain = f"{arm}_s{seed}"
            for g in GENS:
                path = f"{RAW}/ckpt_{arm}/no_preserve_seed{seed}/generation_{g}"
                if not os.path.exists(f"{path}/model.safetensors"):
                    log(f"  MISSING {path}"); continue
                m = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.float32)
                N, sv, svn, oo, H = e0.accumulate(m, val)
                lm = e0.layer_metrics(N, sv[LAST], svn[LAST], oo[LAST], H)
                geom.setdefault(chain, {})[str(g)] = lm
                del m
                log(f"  {chain} g{g}: PR_raw={lm['PR_raw_uncentered']:.2f} "
                    f"PR_cen={lm['PR_centered']:.2f} iso={lm['isotropy_1_minus']:.4f} "
                    f"effR={lm['eff_rank_centered']:.2f} rogue={lm['rogue_coord_share']:.3f}")
    res = {
        "date": "2026-06-15", "mode": "pilot" if pilot else "full",
        "what": "exp019 12链 gen0-9 末层(L12)几何, 对齐 PPL 驼峰; 检验恢复相几何反转 vs 继续散",
        "koujing": "复用 rerun_e0_metric_panel: wikitext-2 val/block64/numpy-shuffle42/前256, 末层 L12",
        "sanity": "α0 s101 g1 PR_centered 应 ≈ pairs.json E1['101'][0]=200.638",
        "geometry_L12": geom, "ppl": load_ppl(),
    }
    json.dump(res, open(OUT, "w"), indent=2, ensure_ascii=False)
    log(f"=== done {time.time()-t0:.1f}s → {OUT} ===")
    # 人读: 每链几何轨迹 (PR_centered) vs PPL
    print("\n===== 末层 PR_centered 轨迹 (对齐 PPL) =====")
    ppl = res["ppl"]
    for chain, gg in geom.items():
        prc = [gg.get(str(g), {}).get("PR_centered", float("nan")) for g in GENS]
        pl = [ppl.get(chain, {}).get(g, float("nan")) for g in GENS]
        print(f"  {chain}")
        print(f"    PR_cen: " + " ".join(f"{x:6.1f}" for x in prc))
        print(f"    PPL   : " + " ".join(f"{x:6.1f}" for x in pl))
