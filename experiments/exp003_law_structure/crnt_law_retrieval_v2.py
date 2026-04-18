"""
MaoField Exp003 V2: 修复版 CRNT 法律检索
==========================================

修复：query 和 doc 物种分开，用 min 操作计算匹配量。
不再合并浓度——避免 doc 结构丰富度劫持分数。

score = match_score + 0.2 * complement_score - 0.05 * penalty
match_i = min(x_q[i], x_d[i])  # 两者都有才算
complement_i = x_d[i] * (1 - min(x_q[i], 1))  # doc 有 query 没有
penalty = sum(x_d)  # 惩罚"什么都有"的通用法条

match 部分可选 CRNT 演化（让匹配物种之间反应合成）。
"""

import sqlite3
import numpy as np
import json
import time
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from extract_species import extract_species

DB_PATH = "/home/amd/HEZIMENG/legal-assistant/knowledge_base/legal_data.db"
OUT_DIR = "/home/amd/HEZIMENG/MaoField/experiments/exp003_law_structure/results"

SPECIES_KEYS = ["subject", "action", "object", "condition", "consequence", "legal_basis"]

# Colloquial → legal term mapping for queries
COLLOQUIAL_MAP = {
    "辞退": ["解除", "终止"], "开除": ["解除"], "炒鱿鱼": ["解除"],
    "打人": ["伤害", "殴打"], "打": ["伤害", "殴打"],
    "偷": ["盗窃"], "偷东西": ["盗窃"],
    "骗": ["诈骗"], "骗钱": ["诈骗"],
    "杀": ["杀害", "故意杀人"],
    "抢": ["抢劫", "抢夺"],
    "赔": ["赔偿"], "赔偿": ["赔偿"],
    "判": ["判处"], "判刑": ["判处"],
    "分": ["分割"], "分财产": ["分割"],
    "还": ["返还", "偿还"], "还钱": ["返还", "偿还"],
    "告": ["起诉", "诉讼"], "起诉": ["起诉"],
    "拘留": ["行政拘留", "拘留"],
    "离婚": ["离婚"], "结婚": ["结婚"],
    "加班": ["加班"], "工资": ["工资", "报酬"],
    "合同": ["合同"], "押金": ["押金", "保证金"],
    "房子": ["房屋", "不动产", "财产"],
    "醉驾": ["醉酒驾驶", "危险驾驶", "醉酒"],
    "未成年": ["未成年人"],
    "工伤": ["工伤", "职业病"],
    "遗产": ["遗产", "继承"],
    "交通事故": ["交通事故"],
    "违约": ["违约"],
    "申诉": ["申诉", "复议"],
}


def extract_query_species(query_text):
    """Extract species from user query with colloquial mapping"""
    species, concentrations = extract_species(query_text)

    # Expand with colloquial mappings
    for colloquial, legal_terms in COLLOQUIAL_MAP.items():
        if colloquial in query_text:
            for lt in legal_terms:
                if lt not in species["action"] and lt not in species["subject"]:
                    species["action"].append(lt)

    # Also add query words directly as potential matching targets
    # (for subject/object detection in short queries)
    for pattern_word in ["公司", "单位", "老板", "房东", "借", "欠"]:
        if pattern_word in query_text:
            if pattern_word in ["公司", "单位", "老板", "房东"]:
                if pattern_word not in species["subject"]:
                    species["subject"].append(pattern_word)

    # Recalculate concentrations
    for key in SPECIES_KEYS:
        concentrations[key] = float(len(species[key])) if species[key] else 0.0

    return species, concentrations


def match_score_v2(q_conc, d_conc):
    """
    V2 scoring: min-based matching + complement + penalty
    Core insight: same as PQ-Chamfer's min — only mutual presence counts.
    """
    match = 0.0
    complement = 0.0
    total_doc = 0.0

    for key in SPECIES_KEYS:
        qc = q_conc.get(key, 0.0)
        dc = d_conc.get(key, 0.0)

        # Match: min of both (only what both have)
        match += min(qc, dc)

        # Complement: doc has but query doesn't
        if qc == 0 and dc > 0:
            complement += dc

        total_doc += dc

    # Penalty for overly rich docs
    penalty = total_doc * 0.05

    score = match + 0.2 * complement - penalty
    return score, match, complement, penalty


def crnt_match_evolve(q_conc, d_conc, dt=0.01, max_steps=200):
    """
    CRNT evolution on match-only species.
    Initial state = min(q, d) for each species.
    Reactions: matched species synthesize into "understanding".
    """
    # Initial: only the matched part
    x = np.zeros(8)  # 6 species + legal_fact + synthesis
    for i, key in enumerate(SPECIES_KEYS):
        x[i] = min(q_conc.get(key, 0.0), d_conc.get(key, 0.0))

    # Indices
    IDX_SUBJ, IDX_ACT, IDX_OBJ, IDX_COND, IDX_CONS, IDX_BASIS = 0, 1, 2, 3, 4, 5
    IDX_FACT = 6
    IDX_SYNTH = 7

    for step in range(max_steps):
        dx = np.zeros(8)

        # R0: subject + action → legal_fact
        r0 = 0.5 * x[IDX_SUBJ] * x[IDX_ACT]
        dx[IDX_FACT] += r0

        # R1: legal_fact + condition → synthesis
        r1 = 0.5 * x[IDX_FACT] * x[IDX_COND]
        dx[IDX_SYNTH] += r1

        # R2: legal_fact + consequence → synthesis
        r2 = 0.3 * x[IDX_FACT] * x[IDX_CONS]
        dx[IDX_SYNTH] += r2

        # R3: action + object → synthesis (direct match)
        r3 = 0.4 * x[IDX_ACT] * x[IDX_OBJ]
        dx[IDX_SYNTH] += r3

        # R4: legal_basis adds credibility
        r4 = 0.2 * x[IDX_BASIS]
        dx[IDX_SYNTH] += r4

        x = x + dx * dt
        x = np.maximum(x, 0)

        if np.max(np.abs(dx * dt)) < 1e-8:
            break

    return float(x[IDX_SYNTH])


def keyword_baseline(query_text, doc_text, query_keywords):
    """Simple keyword matching baseline"""
    score = 0
    for kw in query_keywords:
        if kw in doc_text:
            score += 1
    return score


def compute_ndcg(scores_and_ids, relevant_ids, k=10):
    ranked = sorted(scores_and_ids, key=lambda x: x[1], reverse=True)[:k]
    dcg = 0
    for i, (doc_id, _) in enumerate(ranked):
        rel = 1 if doc_id in relevant_ids else 0
        dcg += rel / np.log2(i + 2)
    n_rel = min(len(relevant_ids), k)
    idcg = sum(1 / np.log2(i + 2) for i in range(n_rel))
    return dcg / idcg if idcg > 0 else 0


def main():
    print("=" * 60)
    print("MaoField Exp003 V2: Fixed CRNT Law Retrieval")
    print("score = match(min) + 0.2*complement - 0.05*penalty")
    print("=" * 60)
    t0 = time.time()

    # Load law species
    print("\nLoading law species...")
    with open(os.path.join(OUT_DIR, "law_species.json"), encoding="utf-8") as f:
        law_data = json.load(f)
    print(f"  {len(law_data)} law articles")

    # Load test queries
    with open(os.path.join(OUT_DIR, "test_queries.json"), encoding="utf-8") as f:
        test_queries = json.load(f)
    print(f"  {len(test_queries)} queries")

    results = []

    for qi, query in enumerate(test_queries):
        print(f"\n--- {query['id']}: {query['query']} ---")

        q_species, q_conc = extract_query_species(query["query"])
        active = [f"{k}={v:.0f}" for k, v in q_conc.items() if v > 0]
        print(f"  Query: {', '.join(active)}")
        print(f"  Query actions: {q_species['action']}")

        # Score all docs
        v2_scores = []
        v2_crnt_scores = []
        kw_scores = []

        for doc in law_data:
            d_conc = doc["concentrations"]

            # V2 simple scoring
            score, match, comp, pen = match_score_v2(q_conc, d_conc)
            v2_scores.append((doc["id"], score))

            # V2 + CRNT evolution
            crnt_synth = crnt_match_evolve(q_conc, d_conc)
            v2_crnt_score = score + 0.5 * crnt_synth
            v2_crnt_scores.append((doc["id"], v2_crnt_score))

            # Keyword baseline
            kw = keyword_baseline(query["query"], doc["content"], query["relevant_keywords"])
            kw_scores.append((doc["id"], kw))

        # Relevant docs (keyword score >= 2)
        relevant_ids = set(d for d, s in kw_scores if s >= 2)
        if not relevant_ids:
            relevant_ids = set(d for d, s in kw_scores if s >= 1)

        # NDCG
        v2_ndcg = compute_ndcg(v2_scores, relevant_ids, k=10)
        v2_crnt_ndcg = compute_ndcg(v2_crnt_scores, relevant_ids, k=10)
        kw_ndcg = compute_ndcg(kw_scores, relevant_ids, k=10)

        # Hit@5
        v2_top5 = set(d for d, _ in sorted(v2_scores, key=lambda x: x[1], reverse=True)[:5])
        v2c_top5 = set(d for d, _ in sorted(v2_crnt_scores, key=lambda x: x[1], reverse=True)[:5])
        kw_top5 = set(d for d, _ in sorted(kw_scores, key=lambda x: x[1], reverse=True)[:5])

        print(f"  Relevant: {len(relevant_ids)}")
        print(f"  V2      NDCG@10={v2_ndcg:.4f}  Hit@5={'Y' if v2_top5 & relevant_ids else 'N'}")
        print(f"  V2+CRNT NDCG@10={v2_crnt_ndcg:.4f}  Hit@5={'Y' if v2c_top5 & relevant_ids else 'N'}")
        print(f"  KW      NDCG@10={kw_ndcg:.4f}  Hit@5={'Y' if kw_top5 & relevant_ids else 'N'}")

        # Show V2 top 3
        top3 = sorted(v2_scores, key=lambda x: x[1], reverse=True)[:3]
        for doc_id, score in top3:
            doc = next(d for d in law_data if d["id"] == doc_id)
            rel = "✓" if doc_id in relevant_ids else " "
            print(f"    {rel} [{doc['law'][:12]} {doc['article']}] s={score:.2f} {doc['content'][:50]}")

        results.append({
            "query_id": query["id"],
            "query": query["query"],
            "n_relevant": len(relevant_ids),
            "v2_ndcg10": float(v2_ndcg),
            "v2_crnt_ndcg10": float(v2_crnt_ndcg),
            "kw_ndcg10": float(kw_ndcg),
            "v2_hit5": bool(v2_top5 & relevant_ids),
            "v2_crnt_hit5": bool(v2c_top5 & relevant_ids),
            "kw_hit5": bool(kw_top5 & relevant_ids),
        })

    # Summary
    print(f"\n{'='*60}")
    print("  Exp003 V2 Summary")
    print(f"{'-'*60}")

    for method in ["v2", "v2_crnt", "kw"]:
        ndcgs = [r[f"{method}_ndcg10"] for r in results]
        hits = sum(1 for r in results if r[f"{method}_hit5"])
        print(f"  {method:10s} NDCG@10={np.mean(ndcgs):.4f}  Hit@5={hits}/{len(results)}")

    print(f"{'='*60}")

    # Save
    out_path = os.path.join(OUT_DIR, "exp003_v2_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "meta": {"date": "2026-04-10", "version": "v2_min_match"},
            "per_query": results,
            "summary": {
                m: {
                    "mean_ndcg10": float(np.mean([r[f"{m}_ndcg10"] for r in results])),
                    "hit5": sum(1 for r in results if r[f"{m}_hit5"])
                }
                for m in ["v2", "v2_crnt", "kw"]
            }
        }, f, ensure_ascii=False, indent=2)
    print(f"\nSaved: {out_path}")
    print(f"Total: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
