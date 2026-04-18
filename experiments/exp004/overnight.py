"""
MaoField Exp004: Overnight Tasks
==================================
1. Extended Exp D: 20 query-doc pairs
2. Fixed Exp C: full sentences
3. Parameter sweep: D sensitivity
4. Save all results
"""

import numpy as np
import json
import time
import os

from simulator_ac import AllenCahn3D
from source import build_source_physical as build_source
from fusion import evolve_text_to_steady, iterative_fusion
from config import GRID_SIZE, ANALYSIS_DIR

D = 0.1
DT = 0.1
DX = 1.0
N = GRID_SIZE
STEPS = 5000


def field_stats(u):
    return {
        "pos_frac": float((u > 0.5).mean()),
        "neg_frac": float((u < -0.5).mean()),
        "wall_frac": float((np.abs(u) < 0.5).mean()),
        "mean": float(u.mean()),
        "std": float(u.std()),
    }


# ── Task 1: Extended Experiment D (20 pairs) ──

TEST_PAIRS = [
    # (query, doc_match, doc_mismatch)
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


def task1_extended_exp_d():
    print("\n" + "=" * 60)
    print("TASK 1: Extended Experiment D (10 pairs)")
    print("=" * 60)

    results = []
    correct = 0

    for idx, (query, doc_match, doc_mismatch) in enumerate(TEST_PAIRS):
        print(f"\n  Pair {idx+1}/10: '{query[:10]}...'")

        # Build source fields
        S_q = build_source(query, N)
        S_m = build_source(doc_match, N)
        S_mm = build_source(doc_mismatch, N)

        # Evolve each to steady state
        u_q, _ = evolve_text_to_steady(S_q, D=D, dt=DT, dx=DX, grid_size=N, max_steps=STEPS)
        u_m, _ = evolve_text_to_steady(S_m, D=D, dt=DT, dx=DX, grid_size=N, max_steps=STEPS)
        u_mm, _ = evolve_text_to_steady(S_mm, D=D, dt=DT, dx=DX, grid_size=N, max_steps=STEPS)

        # Fusion: query + match
        rounds_m, energy_m, hist_m = iterative_fusion(
            u_q.copy(), u_m.copy(), S_q, S_m,
            D=D, dt=DT, dx=DX, grid_size=N, verbose=False)

        # Fusion: query + mismatch
        rounds_mm, energy_mm, hist_mm = iterative_fusion(
            u_q.copy(), u_mm.copy(), S_q, S_mm,
            D=D, dt=DT, dx=DX, grid_size=N, verbose=False)

        is_correct = energy_m < energy_mm
        if is_correct:
            correct += 1

        delta_pct = (energy_mm - energy_m) / abs(energy_mm) * 100 if energy_mm != 0 else 0

        print(f"    Match E={energy_m:.1f} ({rounds_m}r) | Mismatch E={energy_mm:.1f} ({rounds_mm}r) | {'✓' if is_correct else '✗'} Δ={delta_pct:.1f}%")

        results.append({
            "idx": idx,
            "query": query,
            "doc_match": doc_match[:30],
            "doc_mismatch": doc_mismatch[:30],
            "match_energy": float(energy_m),
            "match_rounds": rounds_m,
            "mismatch_energy": float(energy_mm),
            "mismatch_rounds": rounds_mm,
            "correct": is_correct,
            "energy_delta_pct": float(delta_pct),
        })

    accuracy = correct / len(TEST_PAIRS)
    avg_delta = np.mean([r["energy_delta_pct"] for r in results])

    print(f"\n  === Task 1 Summary ===")
    print(f"  Accuracy: {correct}/{len(TEST_PAIRS)} ({accuracy:.0%})")
    print(f"  Avg energy delta: {avg_delta:.1f}%")
    print(f"  {'✓ PASSED (>70%)' if accuracy > 0.7 else '✗ FAILED (<70%)'}")

    return {"pairs": results, "accuracy": float(accuracy), "avg_delta": float(avg_delta)}


# ── Task 2: Fixed Experiment C ──

def task2_exp_c_sentences():
    print("\n" + "=" * 60)
    print("TASK 2: Experiment C with Full Sentences")
    print("=" * 60)

    base = "我想和他离婚"
    quant = "房子和车子怎么分割"
    qual = "因为他经常打我"
    quant_qual = "房子怎么分他还经常打我"

    # Base steady state
    S_base = build_source(base, N)
    u_base, _ = evolve_text_to_steady(S_base, D=D, dt=DT, dx=DX, grid_size=N, max_steps=STEPS)
    stats_base = field_stats(u_base)
    print(f"\n  Base '{base}': +1={stats_base['pos_frac']:.1%} -1={stats_base['neg_frac']:.1%}")

    contexts = {
        "quant": quant,
        "qual": qual,
        "quant_qual": quant_qual,
    }

    results = {"base": stats_base}

    for name, ctx_text in contexts.items():
        S_ctx = build_source(base + ctx_text, N)
        sim = AllenCahn3D(grid_size=N, D=D, dt=DT, dx=DX)
        sim.u = u_base.copy()
        sim.S = S_ctx
        if sim.S.max() > 0:
            sim.S = sim.S / sim.S.max()
        sim.run(STEPS, snapshot_interval=STEPS, verbose=False)
        stats = field_stats(sim.u)
        shift = abs(stats['pos_frac'] - stats_base['pos_frac'])
        print(f"  + '{ctx_text}': +1={stats['pos_frac']:.1%} -1={stats['neg_frac']:.1%} shift={shift:.4f}")
        results[name] = {**stats, "shift": float(shift), "context": ctx_text}

    # Analysis
    q_shift = results.get("quant", {}).get("shift", 0)
    ql_shift = results.get("qual", {}).get("shift", 0)
    qq_shift = results.get("quant_qual", {}).get("shift", 0)

    print(f"\n  Quant shift: {q_shift:.4f}")
    print(f"  Qual shift:  {ql_shift:.4f}")
    print(f"  Q+Q shift:   {qq_shift:.4f}")
    if ql_shift > q_shift:
        print(f"  ✓ Qualitative > Quantitative ({ql_shift/max(q_shift,1e-10):.1f}x)")
    else:
        print(f"  ✗ Quantitative ≥ Qualitative")

    return results


# ── Task 3: Parameter Sweep ──

def task3_param_sweep():
    print("\n" + "=" * 60)
    print("TASK 3: D Parameter Sensitivity")
    print("=" * 60)

    query = "他打我要怎么判"
    doc_match = "故意伤害他人身体的处三年以下有期徒刑拘役或者管制"
    doc_mismatch = "用人单位应当按照劳动合同约定和国家规定向劳动者及时足额支付劳动报酬"

    S_q = build_source(query, N)
    S_m = build_source(doc_match, N)
    S_mm = build_source(doc_mismatch, N)

    results = []

    for D_test in [0.05, 0.08, 0.1, 0.12, 0.15]:
        print(f"\n  D={D_test}...")

        u_q, _ = evolve_text_to_steady(S_q, D=D_test, dt=DT, dx=DX, grid_size=N, max_steps=STEPS)
        u_m, _ = evolve_text_to_steady(S_m, D=D_test, dt=DT, dx=DX, grid_size=N, max_steps=STEPS)
        u_mm, _ = evolve_text_to_steady(S_mm, D=D_test, dt=DT, dx=DX, grid_size=N, max_steps=STEPS)

        _, e_m, _ = iterative_fusion(
            u_q.copy(), u_m.copy(), S_q, S_m,
            D=D_test, dt=DT, dx=DX, grid_size=N, verbose=False)

        _, e_mm, _ = iterative_fusion(
            u_q.copy(), u_mm.copy(), S_q, S_mm,
            D=D_test, dt=DT, dx=DX, grid_size=N, verbose=False)

        delta = (e_mm - e_m) / abs(e_mm) * 100 if e_mm != 0 else 0
        correct = e_m < e_mm

        print(f"    Match E={e_m:.1f} Mismatch E={e_mm:.1f} Δ={delta:.1f}% {'✓' if correct else '✗'}")

        results.append({
            "D": D_test,
            "match_energy": float(e_m),
            "mismatch_energy": float(e_mm),
            "delta_pct": float(delta),
            "correct": correct,
        })

    return results


def main():
    print("=" * 60)
    print("MaoField Exp004: Overnight Tasks")
    print("=" * 60)
    t0 = time.time()

    t1_results = task1_extended_exp_d()
    t2_results = task2_exp_c_sentences()
    t3_results = task3_param_sweep()

    # Save all
    all_results = {
        "meta": {"date": "2026-04-10", "D": D, "grid": N, "steps": STEPS},
        "task1_extended_D": t1_results,
        "task2_exp_C_sentences": t2_results,
        "task3_param_sweep": t3_results,
    }

    for name, data in [
        ("exp_D_extended.json", t1_results),
        ("exp_C_sentences.json", t2_results),
        ("exp_D_param_sweep.json", t3_results),
    ]:
        with open(os.path.join(ANALYSIS_DIR, name), "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

    with open(os.path.join(ANALYSIS_DIR, "overnight_results.json"), "w") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)

    # Text summary
    total_time = time.time() - t0
    summary = f"""MaoField Exp004 Overnight Summary
==================================
Date: 2026-04-10
Total time: {total_time:.0f}s ({total_time/60:.1f}min)

Task 1 - Extended Exp D (10 pairs):
  Accuracy: {t1_results['accuracy']:.0%}
  Avg energy delta: {t1_results['avg_delta']:.1f}%

Task 2 - Exp C Sentences:
  Base: +1={t2_results['base']['pos_frac']:.1%}
  Quant shift: {t2_results.get('quant', {}).get('shift', 0):.4f}
  Qual shift: {t2_results.get('qual', {}).get('shift', 0):.4f}

Task 3 - D Sensitivity:
"""
    for r in t3_results:
        summary += f"  D={r['D']}: delta={r['delta_pct']:.1f}% {'✓' if r['correct'] else '✗'}\n"

    with open(os.path.join(ANALYSIS_DIR, "overnight_summary.txt"), "w") as f:
        f.write(summary)

    print(f"\n\n{'='*60}")
    print(summary)
    print(f"{'='*60}")
    print(f"All saved to {ANALYSIS_DIR}")


if __name__ == "__main__":
    main()
