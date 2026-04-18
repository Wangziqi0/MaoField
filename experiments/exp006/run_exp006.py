"""
MaoField Exp006: Multi-Component Field Verification
=====================================================

Does increasing collision dimensionality help?

Conditions:
  A:  1-comp, no coupling          (baseline, reproduce exp005-D)
  B1: 2-comp, lambda=0.0           (pure dimension increase)
  B2: 2-comp, lambda=+0.1          (struggle/repulsion)
  B3: 2-comp, lambda=-0.1          (identity/attraction)
  C:  3-comp, lambda=+0.1 (all)    (more components)
"""

import sqlite3
import numpy as np
import json
import time
import os
import random as pyrandom

from simulator_mc import evolve_steps_mc, compute_energy_mc
from source_binary_mc import build_source_mc
from adjoint_mc import adjoint_iteration_mc
from config import *


# ===== Test pairs (same as exp004/exp005) =====
TEST_PAIRS = [
    ("他打我要怎么判",
     "故意伤害他人身体的处三年以下有期徒刑拘役或者管制",
     "用人单位应当按照劳动合同约定和国家规定向劳动者及时足额支付劳动报酬"),
    ("偷东西会怎么样",
     "盗窃公私财物数额较大的或者多次盗窃的处三年以下有期徒刑",
     "离婚时夫妻共同财产由双方协议处理"),
    ("醉酒开车怎么处罚",
     "醉酒驾驶机动车的由公安机关交通管理部门约束至酒醒吊销机动车驾驶证",
     "承揽人应当以自己的设备技术和劳力完成主要工作"),
    ("杀人判几年",
     "故意杀人的处死刑无期徒刑或者十年以上有期徒刑",
     "当事人对合同条款的理解有争议的应当按照合同所使用的词句"),
    ("诈骗怎么判",
     "诈骗公私财物数额较大的处三年以下有期徒刑拘役或者管制并处或者单处罚金",
     "婚姻关系存续期间所得的工资奖金劳务报酬为夫妻共同财产"),
    ("离婚后房子怎么分",
     "离婚时夫妻共同财产由双方协议处理协议不成的由人民法院判决",
     "故意伤害他人身体的处三年以下有期徒刑拘役或者管制"),
    ("借钱不还怎么办",
     "借款人应当按照约定的期限返还借款",
     "盗窃公私财物数额较大的处三年以下有期徒刑"),
    ("租房合同到期房东不退押金",
     "租赁期限届满承租人应当返还租赁物出租人应当退还押金",
     "醉酒驾驶机动车的由公安机关吊销机动车驾驶证"),
    ("买到假货怎么维权",
     "经营者提供商品或者服务有欺诈行为的应当按照消费者的要求增加赔偿",
     "故意杀人的处死刑无期徒刑或者十年以上有期徒刑"),
    ("被公司辞退怎么赔偿",
     "用人单位违法解除劳动合同的应当按照经济补偿标准的二倍向劳动者支付赔偿金",
     "离婚时夫妻共同财产由双方协议处理"),
]


def load_corpus(n, seed=42):
    """Load n law articles from database."""
    db = sqlite3.connect(DB_PATH)
    rows = db.execute("SELECT content FROM law_chunks ORDER BY RANDOM() LIMIT ?", (n,)).fetchall()
    db.close()
    texts = [r[0] for r in rows]
    rng = pyrandom.Random(seed)
    rng.shuffle(texts)
    return texts


def precompute_source_fields_mc(texts, n_components, grid_size=GRID_SIZE):
    """Precompute multi-component source fields for all texts."""
    return [build_source_mc(t, n_components, grid_size) for t in texts]


def init_field_mc(S_list, lambdas, grid_size=GRID_SIZE, init_steps=INIT_STEPS):
    """Initialize multi-component field and evolve to initial equilibrium."""
    n_comp = len(S_list)
    u_list = [np.random.uniform(-0.01, 0.01, (grid_size, grid_size, grid_size))
              for _ in range(n_comp)]
    u_list = evolve_steps_mc(u_list, S_list, D, DT, DX, init_steps, lambdas)
    return u_list


def fuse_and_score_mc(u_q_list, u_d_list, S_q_list, S_d_list, lambdas,
                       fusion_steps=FUSION_STEPS):
    """Fuse query and doc fields per component, return total energy."""
    n_comp = len(u_q_list)
    u_fused = [0.5 * (u_q_list[i] + u_d_list[i]) for i in range(n_comp)]
    S_fused = []
    for i in range(n_comp):
        sf = S_q_list[i] + S_d_list[i]
        mx = max(abs(sf.max()), abs(sf.min()))
        if mx > 0:
            sf = sf / mx
        S_fused.append(sf)
    u_fused = evolve_steps_mc(u_fused, S_fused, D, DT, DX, fusion_steps, lambdas)
    return compute_energy_mc(u_fused, S_fused, D, DX, lambdas)


def make_lambdas(n_components, lam_value):
    """Build lambda dict for uniform coupling."""
    lambdas = {}
    for i in range(n_components):
        for j in range(i + 1, n_components):
            lambdas[(i, j)] = lam_value
    return lambdas


def run_condition(test_pairs, S_corpus_mc_list, corpus_texts,
                  n_components, lam_value, condition_name):
    """Run a single experimental condition with adjoint iteration."""
    lambdas = make_lambdas(n_components, lam_value)
    lam_str = f"lambda={lam_value}" if n_components > 1 else "N/A"
    print(f"\n  --- Condition {condition_name}: {n_components}-comp, {lam_str} ---")

    correct = 0
    results = []
    all_histories = []

    for idx, (query, doc_m, doc_mm) in enumerate(test_pairs):
        S_q = build_source_mc(query, n_components, GRID_SIZE)
        S_m = build_source_mc(doc_m, n_components, GRID_SIZE)
        S_mm = build_source_mc(doc_mm, n_components, GRID_SIZE)

        print(f"    Pair {idx+1}: '{query[:10]}...'")

        # Query: init + adjoint iteration
        print(f"      Query adjoint:")
        u_q = init_field_mc(S_q, lambdas)
        u_q, hist_q = adjoint_iteration_mc(
            u_q, S_q, S_corpus_mc_list, lambdas, corpus_texts,
            max_rounds=MAX_ROUNDS, k=TOP_K)

        # Match doc
        print(f"      Match doc adjoint:")
        u_m = init_field_mc(S_m, lambdas)
        u_m, hist_m = adjoint_iteration_mc(
            u_m, S_m, S_corpus_mc_list, lambdas, corpus_texts,
            max_rounds=MAX_ROUNDS, k=TOP_K)

        # Mismatch doc
        print(f"      Mismatch doc adjoint:")
        u_mm = init_field_mc(S_mm, lambdas)
        u_mm, hist_mm = adjoint_iteration_mc(
            u_mm, S_mm, S_corpus_mc_list, lambdas, corpus_texts,
            max_rounds=MAX_ROUNDS, k=TOP_K)

        e_m = fuse_and_score_mc(u_q, u_m, S_q, S_m, lambdas)
        e_mm = fuse_and_score_mc(u_q, u_mm, S_q, S_mm, lambdas)

        ok = e_m < e_mm
        if ok:
            correct += 1
        delta = (e_mm - e_m) / abs(e_mm) * 100 if e_mm != 0 else 0
        print(f"      E_m={e_m:.0f} E_mm={e_mm:.0f} {'✓' if ok else '✗'} Δ={delta:.1f}%")

        results.append({
            "query": query[:15], "e_match": float(e_m),
            "e_mismatch": float(e_mm), "correct": ok, "delta": float(delta)
        })
        all_histories.append({
            "query": query[:15],
            "q_hist": hist_q, "m_hist": hist_m, "mm_hist": hist_mm
        })

    acc = correct / len(test_pairs)
    avg_d = np.mean([r["delta"] for r in results])
    print(f"\n  Condition {condition_name}: Accuracy={acc:.0%} Avg Δ={avg_d:.1f}%")
    return {
        "n_components": n_components, "lambda": lam_value,
        "accuracy": float(acc), "avg_delta": float(avg_d),
        "pairs": results, "adjoint_histories": all_histories
    }


def main():
    print("=" * 60)
    print("MaoField Exp006: Multi-Component Field Verification")
    print("=" * 60)
    t0 = time.time()

    # Load corpus
    print("\nLoading corpus...")
    law_corpus = load_corpus(CORPUS_SIZE)
    print(f"  Law corpus: {len(law_corpus)} texts")

    # Precompute source fields for each component count
    print("\nPrecomputing source fields...")
    t_pre = time.time()
    S_corpus_1 = precompute_source_fields_mc(law_corpus, 1)
    S_corpus_2 = precompute_source_fields_mc(law_corpus, 2)
    S_corpus_3 = precompute_source_fields_mc(law_corpus, 3)
    print(f"  Done in {time.time()-t_pre:.1f}s")

    all_results = {}

    # Condition A: 1-component baseline (reproduce exp005-D)
    all_results["A_1comp"] = run_condition(
        TEST_PAIRS, S_corpus_1, law_corpus,
        n_components=1, lam_value=0.0, condition_name="A")

    # Condition B1: 2-component, no coupling
    all_results["B1_2comp_lam0"] = run_condition(
        TEST_PAIRS, S_corpus_2, law_corpus,
        n_components=2, lam_value=0.0, condition_name="B1")

    # Condition B2: 2-component, lambda=+0.1 (repulsion/struggle)
    all_results["B2_2comp_lam+"] = run_condition(
        TEST_PAIRS, S_corpus_2, law_corpus,
        n_components=2, lam_value=0.1, condition_name="B2")

    # Condition B3: 2-component, lambda=-0.1 (attraction/identity)
    all_results["B3_2comp_lam-"] = run_condition(
        TEST_PAIRS, S_corpus_2, law_corpus,
        n_components=2, lam_value=-0.1, condition_name="B3")

    # Condition C: 3-component, lambda=+0.1
    all_results["C_3comp"] = run_condition(
        TEST_PAIRS, S_corpus_3, law_corpus,
        n_components=3, lam_value=0.1, condition_name="C")

    # === Summary ===
    elapsed = time.time() - t0
    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'-'*60}")
    for cond, res in all_results.items():
        print(f"  {cond:20s}: {res['accuracy']:.0%}  avg_Δ={res['avg_delta']:.1f}%  "
              f"({res['n_components']}-comp, λ={res['lambda']})")

    acc_a = all_results["A_1comp"]["accuracy"]
    acc_b1 = all_results["B1_2comp_lam0"]["accuracy"]
    acc_b2 = all_results["B2_2comp_lam+"]["accuracy"]
    acc_b3 = all_results["B3_2comp_lam-"]["accuracy"]
    acc_c = all_results["C_3comp"]["accuracy"]

    print(f"\n  Key comparisons:")
    print(f"    B1 ({acc_b1:.0%}) vs A ({acc_a:.0%}): "
          f"Pure dimension {'HELPS' if acc_b1 > acc_a else 'no effect'}")
    print(f"    B2 ({acc_b2:.0%}) vs A ({acc_a:.0%}): "
          f"Repulsive coupling {'HELPS' if acc_b2 > acc_a else 'no effect'}")
    print(f"    B3 ({acc_b3:.0%}) vs A ({acc_a:.0%}): "
          f"Attractive coupling {'HELPS' if acc_b3 > acc_a else 'no effect'}")
    print(f"    B2 ({acc_b2:.0%}) vs B3 ({acc_b3:.0%}): "
          f"Struggle vs Identity {'DIFFERENT' if acc_b2 != acc_b3 else 'same'}")
    print(f"    C ({acc_c:.0%}) vs B2 ({acc_b2:.0%}): "
          f"More components {'HELPS' if acc_c > acc_b2 else 'no effect'}")
    if acc_a == acc_b1 == acc_b2 == acc_b3 == acc_c:
        print(f"    ALL EQUAL → problem is NOT collision dimension, it's source field")
    print(f"{'='*60}")

    # Save
    out_path = os.path.join(RESULTS_DIR, "exp006_results.json")
    with open(out_path, "w") as f:
        json.dump({
            "meta": {
                "date": "2026-04-11",
                "experiment": "exp006_multicomponent",
                "params": {
                    "grid_size": GRID_SIZE, "D": D, "dt": DT,
                    "init_steps": INIT_STEPS, "interact_steps": INTERACT_STEPS,
                    "relax_steps": RELAX_STEPS, "fusion_steps": FUSION_STEPS,
                    "max_rounds": MAX_ROUNDS, "top_k": TOP_K,
                    "corpus_size": CORPUS_SIZE,
                }
            },
            "results": all_results
        }, f, indent=2, default=str, ensure_ascii=False)

    summary_path = os.path.join(RESULTS_DIR, "exp006_summary.txt")
    with open(summary_path, "w") as f:
        f.write("Exp006: Multi-Component Field Verification\n\n")
        for c, r in all_results.items():
            f.write(f"{c}: {r['accuracy']:.0%} avg_Δ={r['avg_delta']:.1f}% "
                    f"({r['n_components']}-comp, λ={r['lambda']})\n")
        f.write(f"\nTotal time: {elapsed:.0f}s ({elapsed/60:.1f}min)\n")

    print(f"\nSaved to {RESULTS_DIR}")
    print(f"Total time: {elapsed:.0f}s ({elapsed/60:.1f}min)")


if __name__ == "__main__":
    main()
