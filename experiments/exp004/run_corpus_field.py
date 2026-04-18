"""
MaoField Exp004: Corpus as Background Field
=============================================

语料不是数据源——语料是场的环境。
法律语料构建背景场 → query在背景上演化 → 匹配。

关键对照：法律背景 vs 随机文本背景。
"""

import sqlite3
import numpy as np
import json
import time
import os
import random

from simulator_ac import AllenCahn3D, laplacian_3d_periodic
from source_binary import build_source_binary, text_to_bits
from config import GRID_SIZE, ANALYSIS_DIR
from scipy.ndimage import gaussian_filter

DB_PATH = "/home/amd/HEZIMENG/legal-assistant/knowledge_base/legal_data.db"
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


def load_corpus(n_articles):
    """Load n random law articles from LawVein"""
    db = sqlite3.connect(DB_PATH)
    rows = db.execute("SELECT content FROM law_chunks ORDER BY RANDOM() LIMIT ?", (n_articles,)).fetchall()
    db.close()
    return [r[0] for r in rows]


def generate_random_chinese(n_texts, avg_len=50):
    """Generate random Chinese text (control group)"""
    rng = random.Random(42)
    texts = []
    # Common CJK range
    for _ in range(n_texts):
        length = rng.randint(avg_len // 2, avg_len * 2)
        text = ''.join(chr(rng.randint(0x4e00, 0x9fff)) for _ in range(length))
        texts.append(text)
    return texts


def build_corpus_background(corpus_texts, grid_size=N, sigma=1.5):
    """Build background field from corpus bit patterns"""
    S_bg = np.zeros((grid_size, grid_size, grid_size))
    total_cells = grid_size ** 3

    for text in corpus_texts:
        bits = text_to_bits(text)
        for i, bit in enumerate(bits):
            idx = i % total_cells
            x = idx % grid_size
            y = (idx // grid_size) % grid_size
            z = (idx // (grid_size * grid_size)) % grid_size
            S_bg[x, y, z] += (2 * bit - 1)

    S_bg = gaussian_filter(S_bg, sigma=sigma)

    mx = max(abs(S_bg.max()), abs(S_bg.min()))
    if mx > 0:
        S_bg = S_bg / mx * 0.5  # Background limited to [-0.5, 0.5]

    return S_bg


def evolve_to_steady(u_init, S, D=D, dt=DT, dx=DX, n_steps=STEPS):
    """Evolve Allen-Cahn to steady state"""
    u = u_init.copy()
    for step in range(n_steps):
        lap = laplacian_3d_periodic(u, dx)
        coupling = (1.0 - 3.0 * u * u) * S
        dudt = D * lap - u**3 + u + coupling
        u = u + dt * dudt
        u = np.clip(u, -2, 2)
    return u


def run_pairs_with_background(S_bg, u_bg, label=""):
    """Run 10 test pairs with given background field"""
    correct = 0
    results = []

    for idx, (query, doc_m, doc_mm) in enumerate(TEST_PAIRS):
        S_q = build_source_binary(query, N)
        S_m = build_source_binary(doc_m, N)
        S_mm = build_source_binary(doc_mm, N)

        # Evolve query on background
        S_q_total = S_bg + S_q * 0.3
        u_q = evolve_to_steady(u_bg.copy(), S_q_total, n_steps=3000)

        # Evolve match doc on background
        S_m_total = S_bg + S_m * 0.3
        u_m = evolve_to_steady(u_bg.copy(), S_m_total, n_steps=3000)

        # Evolve mismatch doc on background
        S_mm_total = S_bg + S_mm * 0.3
        u_mm = evolve_to_steady(u_bg.copy(), S_mm_total, n_steps=3000)

        # Fusion energy: merge and evolve briefly
        u_fuse_m = 0.5 * (u_q + u_m)
        S_fuse_m = S_bg + (S_q + S_m) * 0.15
        u_fuse_m = evolve_to_steady(u_fuse_m, S_fuse_m, n_steps=2000)

        u_fuse_mm = 0.5 * (u_q + u_mm)
        S_fuse_mm = S_bg + (S_q + S_mm) * 0.15
        u_fuse_mm = evolve_to_steady(u_fuse_mm, S_fuse_mm, n_steps=2000)

        # Energy
        def energy(u, S):
            gx = np.roll(u, -1, 0) - u
            gy = np.roll(u, -1, 1) - u
            gz = np.roll(u, -1, 2) - u
            return float(np.sum(0.5*D*(gx**2+gy**2+gz**2) + 0.25*(u**2-1)**2 - (1-u**2)*u*S))

        e_m = energy(u_fuse_m, S_fuse_m)
        e_mm = energy(u_fuse_mm, S_fuse_mm)

        ok = e_m < e_mm
        if ok: correct += 1
        delta = (e_mm - e_m) / abs(e_mm) * 100 if e_mm != 0 else 0

        print(f"    P{idx+1}: E_m={e_m:.0f} E_mm={e_mm:.0f} {'✓' if ok else '✗'} Δ={delta:.1f}%")
        results.append({"e_match": float(e_m), "e_mismatch": float(e_mm),
                         "correct": ok, "delta": float(delta)})

    acc = correct / len(TEST_PAIRS)
    avg_d = np.mean([r["delta"] for r in results])
    print(f"  {label}: Accuracy={acc:.0%} Avg Δ={avg_d:.1f}%")
    return {"accuracy": float(acc), "avg_delta": float(avg_d), "pairs": results}


def main():
    print("=" * 60)
    print("MaoField Exp004: Corpus as Background Field")
    print("=" * 60)
    t0 = time.time()

    all_results = {}

    # ── Condition 0: Vacuum (no background) ── already known: 70%
    print("\n--- Condition 0: Vacuum (baseline from binary) ---")
    print("  Known: 70% accuracy, 0.9% avg delta")
    all_results["vacuum"] = {"accuracy": 0.7, "avg_delta": 0.9, "note": "from run_binary.py"}

    # ── Condition 1-3: Law corpus backgrounds ──
    for n_articles in [50, 100, 500]:
        print(f"\n--- Condition: Law corpus ({n_articles} articles) ---")
        corpus = load_corpus(n_articles)
        print(f"  Loaded {len(corpus)} articles, total chars={sum(len(t) for t in corpus)}")

        S_bg = build_corpus_background(corpus, N)
        print(f"  Background field: min={S_bg.min():.3f} max={S_bg.max():.3f} std={S_bg.std():.4f}")

        # Evolve background to ground state
        print("  Evolving background to ground state...")
        u_bg = np.random.uniform(-0.01, 0.01, (N, N, N))
        u_bg = evolve_to_steady(u_bg, S_bg, n_steps=STEPS)
        pos = (u_bg > 0.5).mean()
        neg = (u_bg < -0.5).mean()
        print(f"  Ground state: +1={pos:.1%} -1={neg:.1%}")

        print("  Running 10 pairs...")
        result = run_pairs_with_background(S_bg, u_bg, label=f"law_{n_articles}")
        all_results[f"law_{n_articles}"] = result

    # ── Condition 4: Random Chinese text (control) ──
    print(f"\n--- Condition: Random Chinese text (100 texts, control) ---")
    random_corpus = generate_random_chinese(100, avg_len=50)
    S_bg_rand = build_corpus_background(random_corpus, N)
    print(f"  Background field: min={S_bg_rand.min():.3f} max={S_bg_rand.max():.3f}")

    u_bg_rand = np.random.uniform(-0.01, 0.01, (N, N, N))
    u_bg_rand = evolve_to_steady(u_bg_rand, S_bg_rand, n_steps=STEPS)
    print(f"  Ground state: +1={(u_bg_rand>0.5).mean():.1%} -1={(u_bg_rand<-0.5).mean():.1%}")

    print("  Running 10 pairs...")
    result_rand = run_pairs_with_background(S_bg_rand, u_bg_rand, label="random_100")
    all_results["random_100"] = result_rand

    # ── Summary ──
    print(f"\n{'='*60}")
    print("  Summary: Corpus Background Field Experiment")
    print(f"{'-'*60}")
    for cond, res in all_results.items():
        acc = res["accuracy"]
        delta = res["avg_delta"]
        print(f"  {cond:20s}: accuracy={acc:.0%} avg_Δ={delta:.1f}%")
    print(f"{'='*60}")

    # Key comparison
    law_100 = all_results.get("law_100", {}).get("accuracy", 0)
    rand_100 = all_results.get("random_100", {}).get("accuracy", 0)
    if law_100 > rand_100:
        print(f"\n  ✓ Law corpus ({law_100:.0%}) > Random ({rand_100:.0%}) → Social practice matters!")
    elif law_100 == rand_100:
        print(f"\n  = Law = Random → Content doesn't matter (background structure only)")
    else:
        print(f"\n  ✗ Random ({rand_100:.0%}) > Law ({law_100:.0%}) → Unexpected")

    # Save
    out_path = os.path.join(ANALYSIS_DIR, "exp004_corpus_field.json")
    with open(out_path, "w") as f:
        json.dump({"meta": {"date": "2026-04-10"}, "results": all_results}, f, indent=2, default=str)
    print(f"\nSaved: {out_path}")
    print(f"Total: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
