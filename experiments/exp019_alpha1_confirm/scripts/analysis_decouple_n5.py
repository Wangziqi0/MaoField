#!/usr/bin/env python3
"""
analysis_decouple_n5.py — exp019 副实验「多样性-PPL 解耦」N=5 落盘判定脚本.

存在理由 (D617, Linux 姐姐):
  6/13 audit-exp019-decouple 审出: 解耦线 [A-] 的开奖判定**无落盘 trace**
  (无判定脚本 / 无结果文件 / 无 STATE 记) = D-1 纪律 1 违反。报告数 (verdict
  「4/5」, audit「5/5」) 谁都无法复现。本脚本 = **首个落盘可复现判定**, 闭合
  问题 #1 (seed4 4/5 vs 5/5) + #2 (无落盘 trace)。

预注册判据 (prereg_exp019_draft_v1.md §6.2, verbatim):
  D1 总降:     d2(g9) - d2(g0) <= -0.10   (s42 先验 -0.201)
  D2 恢复期续降: d2(g9) - d2(g2) <= -0.05   (s42 先验 ~-0.13)
  D3 重复率:    rep4(g9) - rep4(g0) >= +0.05 (s42 先验 +0.132)
  单链解耦 = D1 ∧ D2 ∧ D3
  N=5 群体 (seeds {1,2,3,4,42}): 5/5 -> [A]; 4/5 -> [A-] 保级; <=3/5 -> [B,seed 依赖]

方法论选择 (显式记录, 差异日志 D-1 纪律 5):
  [M1] CPU fp32 (非原始 GPU fp16): CPU 无良好 fp16; beam-search argmax 可能因
       精度微异 -> 生成 token 不必逐位等同原始 22-GPU syndata。但 D1/D2/D3 判据
       是**链内 delta (g9-g0)**, 所有代用同一 CPU-fp32 口径 -> 崩溃趋势稳健,
       绝对值或异于任何 GPU 参考, 链内 delta 一致可比。
  [M2] N=128 prompts = train 前 128 块 (确定性)。原 "n=128 seed 选择" 未落盘,
       此为 documented 选择; 同一组 128 prompt 用于一条链所有代 -> delta 良定义。
  [M3] rep-4 = 1 - distinct-4 (corpus)。项目 metrics.py 无 rep-4 定义; 此为
       text-degeneration 文献标准口径 (1 - distinct-n), 显式记录。
  [M4] distinct-n = metrics.compute_distinct_n (项目自身 fb_metric, 不另造)。
  [M5] 生成 = generate_synthetic.generate_synthetic_dataset (项目自身管线,
       5-way beam-search, prompt_length=64, max_new_tokens=64; 同 s42 run 口径)。

用法:
  HF_HUB_OFFLINE=1 python analysis_decouple_n5.py [--gens 0,2,9] [--n 128] [--out DIR]
"""
from __future__ import annotations
import sys, os, json, time, argparse, hashlib
sys.path.insert(0, "/media/amd/raid1/canonical/projects/MaoField/experiments/exp018_cat/src")
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

import torch
from transformers import AutoTokenizer
from data_pipeline import load_wikitext2, tokenize_and_block
from generate_synthetic import generate_synthetic_dataset
from metrics import compute_distinct_n

CKPT_ROOT = "/media/amd/raid1/canonical/projects/MaoField/experiments/exp018_cat/data/checkpoints_armb/alpha0.0"
TOK_ID = "facebook/opt-125m"
SEEDS = [1, 2, 3, 4, 42]
BLOCK = 64

# 预注册阈值 (硬编码 = prereg §6.2, 不可改; 改 = 作废重注册)
THR_D1 = -0.10   # d2(g9)-d2(g0) <= THR_D1
THR_D2 = -0.05   # d2(g9)-d2(g2) <= THR_D2
THR_D3 = +0.05   # rep4(g9)-rep4(g0) >= THR_D3


def measure_ckpt(ckpt, tok, prompts, n_beams=5, rep_penalty=3.0):
    """加载 ckpt, 对 prompts 生成, 返回 corpus distinct-2/3/4 / rep-4。
    rep_penalty=3.0 = cat_arm_b.yaml / shumailov_official.yaml 配置值 (Shumailov
    官方 Zenodo), 必须匹配链生成口径, 否则不忠实。"""
    syn = generate_synthetic_dataset(
        ckpt, TOK_ID, prompts,
        num_beams=n_beams, prompt_length=64, max_new_tokens=64,
        batch_size=32, fp16=False, device="cpu", repetition_penalty=rep_penalty,
    )
    texts = [tok.decode(r, skip_special_tokens=True) for r in syn["input_ids"]]
    d2 = compute_distinct_n(texts, 2)
    d3 = compute_distinct_n(texts, 3)
    d4 = compute_distinct_n(texts, 4)
    # sha256 over decoded syndata (确定性指纹; Column 不可 JSON 序列化, 用 text)
    sha = hashlib.sha256("\x1f".join(texts).encode("utf-8")).hexdigest()[:16]
    return {"distinct_2": d2, "distinct_3": d3, "distinct_4": d4,
            "rep_4": 1.0 - d4, "syndata_sha256": sha}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gens", default="0,2,9")
    ap.add_argument("--n", type=int, default=128)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                   "..", "decouple_verdict_20260617"))
    args = ap.parse_args()
    gens = [int(g) for g in args.gens.split(",")]
    out_dir = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)

    t0 = time.time()
    raw = load_wikitext2()
    tok = AutoTokenizer.from_pretrained(TOK_ID)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    train = tokenize_and_block(raw["train"], tok, BLOCK)
    prompts = train.select(range(args.n))
    print(f"[setup] train={len(train)} blocks, prompts=N={args.n}, gens={gens}, "
          f"seeds={SEEDS}, {time.time()-t0:.1f}s", flush=True)

    results = {}   # seed -> {gen -> metrics}
    for s in SEEDS:
        results[s] = {}
        for g in gens:
            ckpt = f"{CKPT_ROOT}/no_preserve_seed{s}/generation_{g}"
            t1 = time.time()
            m = measure_ckpt(ckpt, tok, prompts)
            results[s][g] = m
            print(f"[seed{s} g{g}] d2={m['distinct_2']:.4f} d4={m['distinct_4']:.4f} "
                  f"rep4={m['rep_4']:.4f} ({time.time()-t1:.0f}s) sha={m['syndata_sha256']}",
                  flush=True)

    # 判据 (需 g0,g2,g9 都在 gens 中)
    need = {0, 2, 9}
    verdict = {"criteria": {"D1": THR_D1, "D2": THR_D2, "D3": THR_D3},
               "methodology": "CPU fp32 / N=%d first-train-blocks / rep4=1-distinct4 / "
                              "metrics.compute_distinct_n / 5-way beam" % args.n,
               "per_seed": {}, "n_decoupled": 0, "N": len(SEEDS)}
    if need.issubset(set(gens)):
        for s in SEEDS:
            d2_0, d2_2, d2_9 = results[s][0]["distinct_2"], results[s][2]["distinct_2"], results[s][9]["distinct_2"]
            r4_0, r4_9 = results[s][0]["rep_4"], results[s][9]["rep_4"]
            D1 = (d2_9 - d2_0) <= THR_D1
            D2 = (d2_9 - d2_2) <= THR_D2
            D3 = (r4_9 - r4_0) >= THR_D3
            dec = bool(D1 and D2 and D3)
            verdict["per_seed"][s] = {
                "d2_g0": d2_0, "d2_g2": d2_2, "d2_g9": d2_9,
                "rep4_g0": r4_0, "rep4_g9": r4_9,
                "delta_d2_90": d2_9 - d2_0, "delta_d2_92": d2_9 - d2_2,
                "delta_rep4_90": r4_9 - r4_0,
                "D1": D1, "D2": D2, "D3": D3, "decoupled": dec,
            }
            verdict["n_decoupled"] += int(dec)
            print(f"[VERDICT seed{s}] D1={D1} D2={D2} D3={D3} -> decoupled={dec} "
                  f"(Δd2_90={d2_9-d2_0:+.4f} Δd2_92={d2_9-d2_2:+.4f} Δrep4={r4_9-r4_0:+.4f})",
                  flush=True)
        n = verdict["n_decoupled"]
        verdict["grade"] = "[A]" if n == 5 else ("[A-]" if n == 4 else "[B,seed-dep]")
        verdict["sign_test_p"] = 1/32 if n == 5 else None
        print(f"\n[N=5 VERDICT] {n}/5 decoupled -> grade {verdict['grade']}", flush=True)
    else:
        print(f"[warn] gens {gens} 不含 {need}, 跳过判据 (仅落盘原始测量)", flush=True)

    out = {"raw": {str(s): {str(g): results[s][g] for g in results[s]} for s in results},
           "verdict": verdict, "elapsed_s": round(time.time()-t0, 1)}
    with open(os.path.join(out_dir, "decouple_n5_result.json"), "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\n[done] -> {out_dir}/decouple_n5_result.json  total={time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
