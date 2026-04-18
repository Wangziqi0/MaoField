"""
MaoField Exp004: Binary Source Field — Full Experiment
=======================================================
Tasks: source verification + 10-pair fusion + C sentences + bit analysis
"""

import numpy as np
import json
import time
import os

from simulator_ac import AllenCahn3D
from source_binary import build_source_binary, text_to_bits
from fusion import evolve_text_to_steady, iterative_fusion
from config import GRID_SIZE, ANALYSIS_DIR

D = 0.1; DT = 0.1; DX = 1.0; N = GRID_SIZE; STEPS = 5000

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


def main():
    print("=" * 60)
    print("MaoField Exp004: Binary Source Field")
    print("=" * 60)
    t0 = time.time()

    # ── Task 1: Source field verification ──
    print("\n--- Task 1: Source Verification ---")
    texts = {
        "criminal": "故意伤害",
        "labor": "解除劳动合同",
        "divorce": "离婚后财产分割",
        "criminal_heavy": "故意伤害致人重伤",
        "traffic": "交通事故责任认定",
    }

    for name, text in texts.items():
        bits = text_to_bits(text)
        ratio = sum(bits) / len(bits)
        print(f"  {name:16s}: {len(bits):3d} bits, 1-ratio={ratio:.3f}, first24={''.join(map(str,bits[:24]))}")

    print("\n  Source field correlations:")
    fields = {n: build_source_binary(t) for n, t in texts.items()}
    names = list(texts.keys())
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            corr = np.corrcoef(fields[names[i]].flat, fields[names[j]].flat)[0, 1]
            print(f"    {names[i]:16s} vs {names[j]:16s}: corr={corr:.4f}")

    # ── Task 2: 10-pair fusion ──
    print(f"\n--- Task 2: 10-pair Fusion ---")
    results = []
    correct = 0

    for idx, (query, doc_m, doc_mm) in enumerate(TEST_PAIRS):
        print(f"\n  Pair {idx+1}: '{query[:12]}...'")
        S_q = build_source_binary(query, N)
        S_m = build_source_binary(doc_m, N)
        S_mm = build_source_binary(doc_mm, N)

        u_q, _ = evolve_text_to_steady(S_q, D=D, dt=DT, dx=DX, grid_size=N, max_steps=STEPS)
        u_m, _ = evolve_text_to_steady(S_m, D=D, dt=DT, dx=DX, grid_size=N, max_steps=STEPS)
        u_mm, _ = evolve_text_to_steady(S_mm, D=D, dt=DT, dx=DX, grid_size=N, max_steps=STEPS)

        _, e_m, _ = iterative_fusion(u_q.copy(), u_m.copy(), S_q, S_m,
                                      D=D, dt=DT, dx=DX, grid_size=N, verbose=False)
        _, e_mm, _ = iterative_fusion(u_q.copy(), u_mm.copy(), S_q, S_mm,
                                       D=D, dt=DT, dx=DX, grid_size=N, verbose=False)

        ok = e_m < e_mm
        if ok: correct += 1
        delta = (e_mm - e_m) / abs(e_mm) * 100 if e_mm != 0 else 0
        print(f"    Match E={e_m:.1f} | Mismatch E={e_mm:.1f} | {'✓' if ok else '✗'} Δ={delta:.1f}%")
        results.append({"query": query, "e_match": float(e_m), "e_mismatch": float(e_mm),
                         "correct": ok, "delta": float(delta)})

    acc = correct / len(TEST_PAIRS)
    avg_d = np.mean([r["delta"] for r in results])
    print(f"\n  Accuracy: {correct}/{len(TEST_PAIRS)} ({acc:.0%})")
    print(f"  Avg delta: {avg_d:.1f}%")

    # ── Task 3: Exp C sentences ──
    print(f"\n--- Task 3: Exp C Sentences ---")
    base_text = "我想和他离婚"
    S_base = build_source_binary(base_text, N)
    u_base, _ = evolve_text_to_steady(S_base, D=D, dt=DT, dx=DX, grid_size=N, max_steps=STEPS)
    base_pos = (u_base > 0.5).mean()
    print(f"  Base '{base_text}': +1={base_pos:.1%}")

    for ctx_name, ctx_text in [("quant", "房子和车子怎么分割"),
                                ("qual", "因为他经常打我"),
                                ("both", "房子怎么分他还经常打我")]:
        S_ctx = build_source_binary(base_text + ctx_text, N)
        sim = AllenCahn3D(grid_size=N, D=D, dt=DT, dx=DX)
        sim.u = u_base.copy()
        sim.S = S_ctx
        mx = max(abs(sim.S.max()), abs(sim.S.min()))
        if mx > 0: sim.S = sim.S / mx
        sim.run(STEPS, snapshot_interval=STEPS, verbose=False)
        pos = (sim.u > 0.5).mean()
        shift = abs(pos - base_pos)
        print(f"  +'{ctx_text}': +1={pos:.1%} shift={shift:.4f}")

    # ── Task 4: Bit analysis ──
    print(f"\n--- Task 4: Bit Analysis ---")
    all_texts = list(texts.values()) + [p[0] for p in TEST_PAIRS]
    for t in all_texts[:8]:
        bits = text_to_bits(t)
        print(f"  '{t[:10]}': {len(bits):3d}bits 1-ratio={sum(bits)/len(bits):.3f}")

    # Save
    out = {
        "meta": {"date": "2026-04-10", "source": "binary_utf8"},
        "task2_pairs": results,
        "task2_accuracy": float(acc),
        "task2_avg_delta": float(avg_d),
    }
    with open(os.path.join(ANALYSIS_DIR, "exp004_binary_results.json"), "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"\n\nTotal: {time.time()-t0:.1f}s")
    print(f"Saved to {ANALYSIS_DIR}/exp004_binary_results.json")


if __name__ == "__main__":
    main()
