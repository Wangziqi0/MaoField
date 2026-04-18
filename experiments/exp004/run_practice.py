"""
MaoField Exp004: Corpus as Practice Partner (Sequential Interaction)
=====================================================================

Each law article = one practice session.
Query field interacts with each article sequentially, then relaxes.
Key control: law corpus vs random text.
"""

import sqlite3
import numpy as np
import json
import time
import os
import random as pyrandom

from simulator_ac import AllenCahn3D, laplacian_3d_periodic
from source_binary import build_source_binary, text_to_bits
from config import GRID_SIZE, ANALYSIS_DIR
from scipy.ndimage import gaussian_filter

DB_PATH = "/home/amd/HEZIMENG/legal-assistant/knowledge_base/legal_data.db"
D = 0.1; DT = 0.1; DX = 1.0; N = GRID_SIZE

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


def load_law_corpus(n):
    db = sqlite3.connect(DB_PATH)
    rows = db.execute("SELECT content FROM law_chunks ORDER BY RANDOM() LIMIT ?", (n,)).fetchall()
    db.close()
    return [r[0] for r in rows]


def generate_random_chinese(n, avg_len=50):
    rng = pyrandom.Random(42)
    return [''.join(chr(rng.randint(0x4e00, 0x9fff)) for _ in range(rng.randint(30, 80))) for _ in range(n)]


def evolve_steps(u, S, D, dt, dx, n_steps):
    """Run Allen-Cahn n_steps with source S"""
    for _ in range(n_steps):
        lap = laplacian_3d_periodic(u, dx)
        coupling = (1.0 - 3.0 * u * u) * S
        u = u + dt * (D * lap - u**3 + u + coupling)
        u = np.clip(u, -2, 2)
    return u


def compute_energy(u, S, D, dx):
    gx = np.roll(u, -1, 0) - u
    gy = np.roll(u, -1, 1) - u
    gz = np.roll(u, -1, 2) - u
    return float(np.sum(0.5*D*(gx**2+gy**2+gz**2) + 0.25*(u**2-1)**2 - (1-u**2)*u*S))


def practice_with_corpus(u, S_self, corpus_texts, interact_steps=300, relax_steps=100):
    """Sequential practice: interact with each text then relax"""
    for i, text in enumerate(corpus_texts):
        S_law = build_source_binary(text, N)
        S_combined = S_self + S_law
        mx = max(abs(S_combined.max()), abs(S_combined.min()))
        if mx > 0:
            S_combined = S_combined / mx

        # Interact
        u = evolve_steps(u, S_combined, D, DT, DX, interact_steps)
        # Relax (remove law, keep only self)
        u = evolve_steps(u, S_self, D, DT, DX, relax_steps)

        if (i + 1) % 10 == 0:
            e = compute_energy(u, S_self, D, DX)
            print(f"      Practice {i+1}/{len(corpus_texts)}: E={e:.0f}")

    return u


def run_condition(condition_name, corpus_texts):
    """Run 10 test pairs with given corpus practice"""
    print(f"\n  --- {condition_name} ({len(corpus_texts)} texts) ---")
    correct = 0
    results = []

    for idx, (query, doc_m, doc_mm) in enumerate(TEST_PAIRS):
        S_q = build_source_binary(query, N)
        S_m = build_source_binary(doc_m, N)
        S_mm = build_source_binary(doc_mm, N)

        # Init query from noise, evolve to initial shape
        u_q = np.random.uniform(-0.01, 0.01, (N, N, N))
        u_q = evolve_steps(u_q, S_q, D, DT, DX, 1000)

        # Init docs
        u_m = np.random.uniform(-0.01, 0.01, (N, N, N))
        u_m = evolve_steps(u_m, S_m, D, DT, DX, 1000)

        u_mm = np.random.uniform(-0.01, 0.01, (N, N, N))
        u_mm = evolve_steps(u_mm, S_mm, D, DT, DX, 1000)

        # Practice with corpus
        print(f"    Pair {idx+1}: '{query[:10]}...'")
        print(f"      Query practice...")
        u_q = practice_with_corpus(u_q, S_q, corpus_texts)
        print(f"      Match doc practice...")
        u_m = practice_with_corpus(u_m, S_m, corpus_texts)
        print(f"      Mismatch doc practice...")
        u_mm = practice_with_corpus(u_mm, S_mm, corpus_texts)

        # Fusion: query + match
        u_fm = 0.5 * (u_q + u_m)
        S_fm = S_q + S_m
        mx = max(abs(S_fm.max()), abs(S_fm.min()))
        if mx > 0: S_fm = S_fm / mx
        u_fm = evolve_steps(u_fm, S_fm, D, DT, DX, 2000)
        e_m = compute_energy(u_fm, S_fm, D, DX)

        # Fusion: query + mismatch
        u_fmm = 0.5 * (u_q + u_mm)
        S_fmm = S_q + S_mm
        mx = max(abs(S_fmm.max()), abs(S_fmm.min()))
        if mx > 0: S_fmm = S_fmm / mx
        u_fmm = evolve_steps(u_fmm, S_fmm, D, DT, DX, 2000)
        e_mm = compute_energy(u_fmm, S_fmm, D, DX)

        ok = e_m < e_mm
        if ok: correct += 1
        delta = (e_mm - e_m) / abs(e_mm) * 100 if e_mm != 0 else 0
        print(f"      E_m={e_m:.0f} E_mm={e_mm:.0f} {'✓' if ok else '✗'} Δ={delta:.1f}%")

        results.append({"query": query[:15], "e_match": float(e_m),
                         "e_mismatch": float(e_mm), "correct": ok, "delta": float(delta)})

    acc = correct / len(TEST_PAIRS)
    avg_d = np.mean([r["delta"] for r in results])
    print(f"\n  {condition_name}: Accuracy={acc:.0%} Avg Δ={avg_d:.1f}%")
    return {"accuracy": float(acc), "avg_delta": float(avg_d), "pairs": results}


def main():
    print("=" * 60)
    print("MaoField Exp004: Corpus as Practice Partner")
    print("=" * 60)
    t0 = time.time()

    all_results = {}

    # Condition 1: 50 law articles
    law_corpus = load_law_corpus(50)
    print(f"\nLoaded {len(law_corpus)} law articles")
    all_results["law_50"] = run_condition("Law 50", law_corpus)

    # Condition 2: 50 random Chinese texts (control)
    random_corpus = generate_random_chinese(50)
    all_results["random_50"] = run_condition("Random 50", random_corpus)

    # Summary
    print(f"\n{'='*60}")
    print("  Summary: Practice Partner Experiment")
    print(f"{'-'*60}")
    print(f"  Vacuum (no practice):  70% (known baseline)")
    for cond, res in all_results.items():
        print(f"  {cond:20s}: {res['accuracy']:.0%}  avg_Δ={res['avg_delta']:.1f}%")

    law_acc = all_results["law_50"]["accuracy"]
    rand_acc = all_results["random_50"]["accuracy"]
    if law_acc > rand_acc:
        print(f"\n  ✓ Law ({law_acc:.0%}) > Random ({rand_acc:.0%}) → Social practice works!")
    elif law_acc == rand_acc:
        print(f"\n  = Law = Random → Content doesn't matter")
    else:
        print(f"\n  ✗ Random > Law → Unexpected")
    print(f"{'='*60}")

    # Save
    out_path = os.path.join(ANALYSIS_DIR, "exp004_practice.json")
    with open(out_path, "w") as f:
        json.dump({"meta": {"date": "2026-04-10"}, "results": all_results}, f, indent=2, default=str)

    summary_path = os.path.join(ANALYSIS_DIR, "practice_summary.txt")
    with open(summary_path, "w") as f:
        f.write(f"Practice Partner Experiment\n")
        f.write(f"Vacuum: 70%\n")
        for c, r in all_results.items():
            f.write(f"{c}: {r['accuracy']:.0%} avg_Δ={r['avg_delta']:.1f}%\n")
        f.write(f"Total time: {time.time()-t0:.0f}s\n")

    print(f"\nSaved. Total: {time.time()-t0:.0f}s ({(time.time()-t0)/60:.1f}min)")


if __name__ == "__main__":
    main()
