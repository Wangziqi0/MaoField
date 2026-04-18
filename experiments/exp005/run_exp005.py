"""
MaoField Exp005: Adjoint Functor-Driven Demand Practice
=========================================================

5 conditions:
  A. Vacuum (no practice)
  B. Blind 50 (random 50 from pool, no G)
  C. Demand-driven (1 round of G selection)
  D. Demand-driven (full adjoint iteration, up to 5 rounds)
  E. Demand-driven + random pool (control: content matters?)
"""

import sqlite3
import numpy as np
import json
import time
import os
import random as pyrandom

from simulator_ac import evolve_steps, compute_energy, compute_residual, compute_energy_density
from source_binary import build_source_binary
from adjoint import adjoint_iteration, blind_practice, select_practice_targets, compute_coupling_energy, compute_coupling_residual
from config import *


# ===== Test pairs (same as exp004 for comparability) =====
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
    """Load n law articles from database (fixed seed for reproducibility)."""
    db = sqlite3.connect(DB_PATH)
    rows = db.execute("SELECT content FROM law_chunks ORDER BY RANDOM() LIMIT ?", (n,)).fetchall()
    db.close()
    # Re-shuffle with fixed seed for reproducibility
    texts = [r[0] for r in rows]
    rng = pyrandom.Random(seed)
    rng.shuffle(texts)
    return texts


def generate_random_chinese(n, seed=42):
    """Generate n random Chinese text strings."""
    rng = pyrandom.Random(seed)
    return [''.join(chr(rng.randint(0x4e00, 0x9fff)) for _ in range(rng.randint(30, 80))) for _ in range(n)]


def precompute_source_fields(texts, grid_size=GRID_SIZE):
    """Precompute source fields for all corpus texts."""
    return [build_source_binary(t, grid_size) for t in texts]


def init_field(S, grid_size=GRID_SIZE, init_steps=INIT_STEPS):
    """Initialize field from noise and evolve to initial equilibrium."""
    u = np.random.uniform(-0.01, 0.01, (grid_size, grid_size, grid_size))
    u = evolve_steps(u, S, D, DT, DX, init_steps)
    return u


def fuse_and_score(u_q, u_d, S_q, S_d, fusion_steps=FUSION_STEPS):
    """Fuse query and doc fields, return fusion energy."""
    u_fused = 0.5 * (u_q + u_d)
    S_fused = S_q + S_d
    mx = max(abs(S_fused.max()), abs(S_fused.min()))
    if mx > 0:
        S_fused = S_fused / mx
    u_fused = evolve_steps(u_fused, S_fused, D, DT, DX, fusion_steps)
    return compute_energy(u_fused, S_fused, D, DX)


# ===== Diagnostic: check r(x) and e(x) magnitudes =====
def run_diagnostic(S_corpus_list, corpus_texts):
    """Round-0 diagnostic: check if residual and energy density are usable."""
    print("\n" + "=" * 60)
    print("  DIAGNOSTIC: Checking r(x) and e(x) magnitudes")
    print("=" * 60)

    query = TEST_PAIRS[0][0]
    S_q = build_source_binary(query, GRID_SIZE)
    u = init_field(S_q)

    r = compute_residual(u, S_q, D, DX)
    e = compute_energy_density(u, S_q, D, DX)

    r_norm = float(np.sqrt(np.sum(r**2)))
    e_total = float(np.sum(e))
    e_std = float(np.std(e))

    print(f"  ‖r(x)‖ = {r_norm:.6f}")
    print(f"  E_total = {e_total:.2f}")
    print(f"  e_std   = {e_std:.6f}")
    print(f"  r_max   = {float(np.max(np.abs(r))):.6f}")
    print(f"  e_max   = {float(np.max(e)):.6f}")

    # Coupling with residual
    c_r = np.array([float(np.sum(r * S_i)) for S_i in S_corpus_list[:20]])
    print(f"\n  Residual couplings (first 20):")
    print(f"    max |c_r| = {np.max(np.abs(c_r)):.6f}")
    print(f"    mean |c_r| = {np.mean(np.abs(c_r)):.6f}")
    print(f"    std |c_r| = {np.std(np.abs(c_r)):.6f}")

    # Coupling with energy density
    c_e = np.array([float(np.sum(e * S_i)) for S_i in S_corpus_list[:20]])
    print(f"\n  Energy density couplings (first 20):")
    print(f"    max |c_e| = {np.max(np.abs(c_e)):.6f}")
    print(f"    mean |c_e| = {np.mean(np.abs(c_e)):.6f}")
    print(f"    std |c_e| = {np.std(np.abs(c_e)):.6f}")

    # Recommendation
    if r_norm < 1e-4:
        print(f"\n  WARNING: ‖r‖ = {r_norm:.2e} is very small.")
        print(f"  → Using energy density e(x) for coupling (recommended).")
        recommended = 'energy'
    else:
        print(f"\n  ‖r‖ = {r_norm:.4f} is usable.")
        # Check if energy gives better discrimination
        if np.std(np.abs(c_e)) > np.std(np.abs(c_r)) * 2:
            print(f"  → Energy density has better discrimination. Using 'energy'.")
            recommended = 'energy'
        else:
            print(f"  → Residual is usable. Using 'residual'.")
            recommended = 'residual'

    print("=" * 60)
    return recommended


# ===== Condition runners =====

def run_condition_A(test_pairs):
    """Condition A: Vacuum (no practice)."""
    print("\n  --- Condition A: Vacuum (no practice) ---")
    correct = 0
    results = []

    for idx, (query, doc_m, doc_mm) in enumerate(test_pairs):
        S_q = build_source_binary(query, GRID_SIZE)
        S_m = build_source_binary(doc_m, GRID_SIZE)
        S_mm = build_source_binary(doc_mm, GRID_SIZE)

        u_q = init_field(S_q)
        u_m = init_field(S_m)
        u_mm = init_field(S_mm)

        e_m = fuse_and_score(u_q, u_m, S_q, S_m)
        e_mm = fuse_and_score(u_q, u_mm, S_q, S_mm)

        ok = e_m < e_mm
        if ok: correct += 1
        delta = (e_mm - e_m) / abs(e_mm) * 100 if e_mm != 0 else 0
        print(f"    Pair {idx+1}: E_m={e_m:.0f} E_mm={e_mm:.0f} {'✓' if ok else '✗'} Δ={delta:.1f}%")
        results.append({"query": query[:15], "e_match": float(e_m),
                        "e_mismatch": float(e_mm), "correct": ok, "delta": float(delta)})

    acc = correct / len(test_pairs)
    avg_d = np.mean([r["delta"] for r in results])
    print(f"\n  Condition A: Accuracy={acc:.0%} Avg Δ={avg_d:.1f}%")
    return {"accuracy": float(acc), "avg_delta": float(avg_d), "pairs": results}


def run_condition_B(test_pairs, S_corpus_list, blind_indices):
    """Condition B: Blind practice (50 random from pool, no G)."""
    print(f"\n  --- Condition B: Blind {len(blind_indices)} (no G) ---")
    correct = 0
    results = []

    for idx, (query, doc_m, doc_mm) in enumerate(test_pairs):
        S_q = build_source_binary(query, GRID_SIZE)
        S_m = build_source_binary(doc_m, GRID_SIZE)
        S_mm = build_source_binary(doc_mm, GRID_SIZE)

        print(f"    Pair {idx+1}: '{query[:10]}...'")
        u_q = init_field(S_q)
        u_q = blind_practice(u_q, S_q, S_corpus_list, blind_indices)

        u_m = init_field(S_m)
        u_m = blind_practice(u_m, S_m, S_corpus_list, blind_indices)

        u_mm = init_field(S_mm)
        u_mm = blind_practice(u_mm, S_mm, S_corpus_list, blind_indices)

        e_m = fuse_and_score(u_q, u_m, S_q, S_m)
        e_mm = fuse_and_score(u_q, u_mm, S_q, S_mm)

        ok = e_m < e_mm
        if ok: correct += 1
        delta = (e_mm - e_m) / abs(e_mm) * 100 if e_mm != 0 else 0
        print(f"      E_m={e_m:.0f} E_mm={e_mm:.0f} {'✓' if ok else '✗'} Δ={delta:.1f}%")
        results.append({"query": query[:15], "e_match": float(e_m),
                        "e_mismatch": float(e_mm), "correct": ok, "delta": float(delta)})

    acc = correct / len(test_pairs)
    avg_d = np.mean([r["delta"] for r in results])
    print(f"\n  Condition B: Accuracy={acc:.0%} Avg Δ={avg_d:.1f}%")
    return {"accuracy": float(acc), "avg_delta": float(avg_d), "pairs": results}


def run_condition_CD(test_pairs, S_corpus_list, corpus_texts,
                     max_rounds, coupling_mode, condition_name):
    """Condition C (1 round) or D (multi-round adjoint iteration)."""
    print(f"\n  --- Condition {condition_name}: Demand-driven (max_rounds={max_rounds}, mode={coupling_mode}) ---")
    correct = 0
    results = []
    all_histories = []

    for idx, (query, doc_m, doc_mm) in enumerate(test_pairs):
        S_q = build_source_binary(query, GRID_SIZE)
        S_m = build_source_binary(doc_m, GRID_SIZE)
        S_mm = build_source_binary(doc_mm, GRID_SIZE)

        print(f"    Pair {idx+1}: '{query[:10]}...'")

        # Query adjoint iteration
        print(f"      Query adjoint:")
        u_q = init_field(S_q)
        u_q, hist_q = adjoint_iteration(
            u_q, S_q, S_corpus_list, corpus_texts,
            max_rounds=max_rounds, k=TOP_K, coupling_mode=coupling_mode
        )

        # Match doc adjoint iteration
        print(f"      Match doc adjoint:")
        u_m = init_field(S_m)
        u_m, hist_m = adjoint_iteration(
            u_m, S_m, S_corpus_list, corpus_texts,
            max_rounds=max_rounds, k=TOP_K, coupling_mode=coupling_mode
        )

        # Mismatch doc adjoint iteration
        print(f"      Mismatch doc adjoint:")
        u_mm = init_field(S_mm)
        u_mm, hist_mm = adjoint_iteration(
            u_mm, S_mm, S_corpus_list, corpus_texts,
            max_rounds=max_rounds, k=TOP_K, coupling_mode=coupling_mode
        )

        e_m = fuse_and_score(u_q, u_m, S_q, S_m)
        e_mm = fuse_and_score(u_q, u_mm, S_q, S_mm)

        ok = e_m < e_mm
        if ok: correct += 1
        delta = (e_mm - e_m) / abs(e_mm) * 100 if e_mm != 0 else 0
        print(f"      E_m={e_m:.0f} E_mm={e_mm:.0f} {'✓' if ok else '✗'} Δ={delta:.1f}%")

        results.append({"query": query[:15], "e_match": float(e_m),
                        "e_mismatch": float(e_mm), "correct": ok, "delta": float(delta)})
        all_histories.append({"query": query[:15], "q_hist": hist_q,
                              "m_hist": hist_m, "mm_hist": hist_mm})

    acc = correct / len(test_pairs)
    avg_d = np.mean([r["delta"] for r in results])
    print(f"\n  Condition {condition_name}: Accuracy={acc:.0%} Avg Δ={avg_d:.1f}%")
    return {"accuracy": float(acc), "avg_delta": float(avg_d),
            "pairs": results, "adjoint_histories": all_histories}


def main():
    print("=" * 60)
    print("MaoField Exp005: Adjoint Functor-Driven Demand Practice")
    print("=" * 60)
    t0 = time.time()

    # === Load corpus pools ===
    print("\nLoading corpus...")
    law_corpus = load_corpus(CORPUS_SIZE)
    random_corpus = generate_random_chinese(CORPUS_SIZE)
    print(f"  Law corpus: {len(law_corpus)} texts")
    print(f"  Random corpus: {len(random_corpus)} texts")

    # === Precompute source fields ===
    print("\nPrecomputing source fields...")
    t_pre = time.time()
    S_law_list = precompute_source_fields(law_corpus)
    S_random_list = precompute_source_fields(random_corpus)
    print(f"  Done in {time.time()-t_pre:.1f}s")

    # === Diagnostic ===
    recommended_mode = run_diagnostic(S_law_list, law_corpus)

    # === Random indices for condition B ===
    rng = pyrandom.Random(123)
    blind_indices = rng.sample(range(CORPUS_SIZE), BLIND_SIZE)

    all_results = {}

    # === Condition A: Vacuum ===
    all_results["A_vacuum"] = run_condition_A(TEST_PAIRS)

    # === Condition B: Blind 50 ===
    all_results["B_blind50"] = run_condition_B(TEST_PAIRS, S_law_list, blind_indices)

    # === Condition C: Demand-driven, 1 round ===
    all_results["C_demand_1round"] = run_condition_CD(
        TEST_PAIRS, S_law_list, law_corpus,
        max_rounds=1, coupling_mode=recommended_mode, condition_name="C"
    )

    # === Condition D: Demand-driven, full iteration ===
    all_results["D_demand_full"] = run_condition_CD(
        TEST_PAIRS, S_law_list, law_corpus,
        max_rounds=MAX_ROUNDS, coupling_mode=recommended_mode, condition_name="D"
    )

    # === Condition E: Demand-driven + random pool ===
    all_results["E_demand_random"] = run_condition_CD(
        TEST_PAIRS, S_random_list, random_corpus,
        max_rounds=MAX_ROUNDS, coupling_mode=recommended_mode, condition_name="E"
    )

    # === Summary ===
    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'-'*60}")
    for cond, res in all_results.items():
        print(f"  {cond:25s}: {res['accuracy']:.0%}  avg_Δ={res['avg_delta']:.1f}%")

    print(f"\n  Key comparisons:")
    acc_a = all_results["A_vacuum"]["accuracy"]
    acc_b = all_results["B_blind50"]["accuracy"]
    acc_c = all_results["C_demand_1round"]["accuracy"]
    acc_d = all_results["D_demand_full"]["accuracy"]
    acc_e = all_results["E_demand_random"]["accuracy"]

    print(f"    C ({acc_c:.0%}) vs B ({acc_b:.0%}): G selection {'WORKS' if acc_c > acc_b else 'no effect'}")
    print(f"    D ({acc_d:.0%}) vs C ({acc_c:.0%}): Iteration {'WORKS' if acc_d > acc_c else 'no effect'}")
    print(f"    C ({acc_c:.0%}) vs E ({acc_e:.0%}): Content {'MATTERS' if acc_c > acc_e else 'irrelevant'}")
    print(f"    D ({acc_d:.0%}) vs A ({acc_a:.0%}): Overall {'IMPROVEMENT' if acc_d > acc_a else 'no improvement'}")
    print(f"{'='*60}")

    # === Save ===
    out_path = os.path.join(RESULTS_DIR, "exp005_results.json")
    with open(out_path, "w") as f:
        json.dump({
            "meta": {
                "date": "2026-04-10",
                "experiment": "exp005_adjoint_practice",
                "coupling_mode": recommended_mode,
                "params": {
                    "grid_size": GRID_SIZE, "D": D, "dt": DT,
                    "init_steps": INIT_STEPS, "interact_steps": INTERACT_STEPS,
                    "relax_steps": RELAX_STEPS, "fusion_steps": FUSION_STEPS,
                    "max_rounds": MAX_ROUNDS, "top_k": TOP_K,
                    "corpus_size": CORPUS_SIZE, "blind_size": BLIND_SIZE,
                }
            },
            "results": all_results
        }, f, indent=2, default=str, ensure_ascii=False)

    summary_path = os.path.join(RESULTS_DIR, "exp005_summary.txt")
    with open(summary_path, "w") as f:
        f.write("Exp005: Adjoint Functor-Driven Demand Practice\n")
        f.write(f"Coupling mode: {recommended_mode}\n\n")
        for c, r in all_results.items():
            f.write(f"{c}: {r['accuracy']:.0%} avg_Δ={r['avg_delta']:.1f}%\n")
        f.write(f"\nTotal time: {time.time()-t0:.0f}s ({(time.time()-t0)/60:.1f}min)\n")

    print(f"\nSaved to {RESULTS_DIR}")
    print(f"Total time: {time.time()-t0:.0f}s ({(time.time()-t0)/60:.1f}min)")


if __name__ == "__main__":
    main()
