"""
MaoField Exp003 Step 3+4: CRNT 法律检索 + 评估
=================================================

对每个 (query, doc) 对：
1. 提取 query 的物种浓度
2. 合并 query + doc 浓度为初始状态
3. CRNT ODE 演化
4. 得分 = 合成量（对立面统一的程度）+ 互补激活
5. 和 baseline（关键词匹配）对比
"""

import sqlite3
import numpy as np
import json
import time
import os
import re

DB_PATH = "/home/amd/HEZIMENG/legal-assistant/knowledge_base/legal_data.db"
OUT_DIR = "/home/amd/HEZIMENG/MaoField/experiments/exp003_law_structure/results"

# Import species extraction from step 1
import sys
sys.path.insert(0, os.path.dirname(__file__))
from extract_species import extract_species


def extract_query_species(query_text):
    """Extract species from a user query (shorter, less structured than law articles)"""
    species, concentrations = extract_species(query_text)

    # Query-specific: map colloquial terms to legal terms
    colloquial_map = {
        "辞退": ["解除", "终止"],
        "开除": ["解除"],
        "打人": ["伤害", "殴打"],
        "偷": ["盗窃"],
        "骗": ["诈骗"],
        "杀": ["杀害", "故意杀人"],
        "抢": ["抢劫", "抢夺"],
        "赔": ["赔偿"],
        "判": ["判处"],
        "分": ["分割"],
        "还": ["返还", "偿还"],
        "告": ["起诉", "诉讼"],
        "拘留": ["行政拘留", "拘留"],
    }

    for colloquial, legal_terms in colloquial_map.items():
        if colloquial in query_text:
            for lt in legal_terms:
                if lt not in species["action"]:
                    species["action"].append(lt)

    # Recalculate concentrations
    for key in concentrations:
        if species[key]:
            concentrations[key] = float(len(species[key]))
        # Keep implicit 0.5 for subject if no explicit

    return species, concentrations


def define_reactions():
    """
    Define CRNT reaction rules for legal reasoning.
    Each reaction: reactants → products, with rate constant k
    """
    reactions = [
        # R0: Subject + Action → LegalFact (基础法律事实成立)
        {
            "name": "R0_legal_fact",
            "reactants": {"subject": 1, "action": 1},
            "products": {"legal_fact": 1},
            "k": 0.5
        },
        # R1: LegalFact + Object → LegalRelation (具体法律关系)
        {
            "name": "R1_legal_relation",
            "reactants": {"legal_fact": 1, "object": 1},
            "products": {"legal_relation": 1},
            "k": 0.5
        },
        # R2: LegalRelation + Condition → Trigger (触发后果)
        {
            "name": "R2_trigger",
            "reactants": {"legal_relation": 1, "condition": 1},
            "products": {"trigger": 1},
            "k": 0.5
        },
        # R3: Trigger → Consequence (产生法律后果)
        {
            "name": "R3_consequence",
            "reactants": {"trigger": 1},
            "products": {"consequence_activated": 1},
            "k": 0.5
        },
        # R4: Synthesis — query + doc species combine
        {
            "name": "R4_synthesis",
            "reactants": {"query_signal": 1, "doc_signal": 1},
            "products": {"synthesis": 1},
            "k": 1.0
        },
        # R5: Complementary — doc fills what query lacks
        {
            "name": "R5_complementary",
            "reactants": {"doc_extra": 1},
            "products": {"complementary": 1},
            "k": 0.8
        },
    ]
    return reactions


def crnt_evolve(query_conc, doc_conc, dt=0.01, max_steps=500, eps=1e-8):
    """
    CRNT ODE evolution for a (query, doc) pair.

    State vector: 6 original species + 5 derived species
    dx/dt = S · v(x) where S is stoichiometry, v(x) is reaction rate

    Returns: (synthesis_score, complementary_score, opposition_score)
    """
    # Species: subject, action, object, condition, consequence, legal_basis,
    #          legal_fact, legal_relation, trigger, consequence_activated,
    #          synthesis, complementary
    SPECIES = [
        "subject", "action", "object", "condition", "consequence", "legal_basis",
        "legal_fact", "legal_relation", "trigger", "consequence_activated",
        "synthesis", "complementary"
    ]
    N = len(SPECIES)
    idx = {s: i for i, s in enumerate(SPECIES)}

    # Initial state: merge query and doc concentrations
    x = np.zeros(N)
    q_keys = ["subject", "action", "object", "condition", "consequence", "legal_basis"]

    # Query signal: how much query covers each species
    query_signal = 0.0
    doc_signal = 0.0
    doc_extra = 0.0

    for key in q_keys:
        qc = query_conc.get(key, 0.0)
        dc = doc_conc.get(key, 0.0)

        # Merge: take max (both present = reinforcement)
        x[idx[key]] = max(qc, dc)

        # Track overlap and complement
        if qc > 0 and dc > 0:
            query_signal += min(qc, dc)
            doc_signal += min(qc, dc)
        elif qc == 0 and dc > 0:
            doc_extra += dc  # Doc has what query lacks

    # Add derived species initial values
    x[idx["synthesis"]] = 0.0
    x[idx["complementary"]] = 0.0

    # Simplified ODE: mass action kinetics
    for step in range(max_steps):
        dx = np.zeros(N)

        # R0: subject + action → legal_fact
        r0 = 0.5 * x[idx["subject"]] * x[idx["action"]]
        dx[idx["subject"]] -= r0 * 0.1  # Consume slowly
        dx[idx["action"]] -= r0 * 0.1
        dx[idx["legal_fact"]] += r0

        # R1: legal_fact + object → legal_relation
        r1 = 0.5 * x[idx["legal_fact"]] * x[idx["object"]]
        dx[idx["legal_fact"]] -= r1 * 0.1
        dx[idx["object"]] -= r1 * 0.1
        dx[idx["legal_relation"]] += r1

        # R2: legal_relation + condition → trigger
        r2 = 0.5 * x[idx["legal_relation"]] * x[idx["condition"]]
        dx[idx["legal_relation"]] -= r2 * 0.1
        dx[idx["condition"]] -= r2 * 0.1
        dx[idx["trigger"]] += r2

        # R3: trigger → consequence_activated
        r3 = 0.5 * x[idx["trigger"]]
        dx[idx["trigger"]] -= r3 * 0.1
        dx[idx["consequence_activated"]] += r3

        # R4: Synthesis from overlap
        r4 = 1.0 * query_signal * doc_signal / (query_signal + doc_signal + eps)
        dx[idx["synthesis"]] += r4 * dt

        # R5: Complementary from doc_extra
        r5 = 0.8 * doc_extra
        dx[idx["complementary"]] += r5 * dt

        # Update
        x = x + dx * dt
        x = np.maximum(x, 0)  # Non-negative concentrations

        # Check convergence
        if np.max(np.abs(dx * dt)) < eps:
            break

    synthesis = x[idx["synthesis"]]
    complementary = x[idx["complementary"]]
    consequence_match = x[idx["consequence_activated"]]

    return synthesis, complementary, consequence_match


def keyword_baseline_score(query_text, doc_text, query_keywords):
    """Simple keyword matching baseline"""
    score = 0
    for kw in query_keywords:
        if kw in doc_text:
            score += 1
    # Also count query word overlap
    for word in query_text:
        if word in doc_text:
            score += 0.1
    return score


def compute_ndcg(scores_and_ids, relevant_ids, k=10):
    """Compute NDCG@k given scored results and relevant IDs"""
    ranked = sorted(scores_and_ids, key=lambda x: x[1], reverse=True)[:k]
    dcg = 0
    for i, (doc_id, _) in enumerate(ranked):
        rel = 1 if doc_id in relevant_ids else 0
        dcg += rel / np.log2(i + 2)
    # Ideal
    n_rel = min(len(relevant_ids), k)
    idcg = sum(1 / np.log2(i + 2) for i in range(n_rel))
    return dcg / idcg if idcg > 0 else 0


def main():
    print("=" * 60)
    print("MaoField Exp003: CRNT Law Retrieval")
    print("=" * 60)
    t0 = time.time()

    # Load law species
    print("\nLoading law species...")
    with open(os.path.join(OUT_DIR, "law_species.json"), encoding="utf-8") as f:
        law_data = json.load(f)
    print(f"  {len(law_data)} law articles")

    # Load test queries
    print("Loading test queries...")
    with open(os.path.join(OUT_DIR, "test_queries.json"), encoding="utf-8") as f:
        test_queries = json.load(f)
    print(f"  {len(test_queries)} queries")

    # For each query, find relevant docs by keyword matching (ground truth approximation)
    # Since we don't have human annotations for specific law IDs, we use keyword matching
    # to identify "relevant" articles, then compare CRNT ranking vs keyword ranking

    results = []

    for qi, query in enumerate(test_queries):
        print(f"\n--- Query {query['id']}: {query['query']} ---")

        # Extract query species
        q_species, q_conc = extract_query_species(query["query"])
        print(f"  Query species: {', '.join(f'{k}={v}' for k, v in q_conc.items() if v > 0)}")

        # Score all docs with CRNT
        crnt_scores = []
        keyword_scores = []

        for doc in law_data:
            doc_conc = doc["concentrations"]

            # CRNT score
            synthesis, complementary, consequence_match = crnt_evolve(q_conc, doc_conc)
            crnt_score = synthesis + 0.5 * complementary + 0.3 * consequence_match
            crnt_scores.append((doc["id"], crnt_score))

            # Keyword baseline
            kw_score = keyword_baseline_score(
                query["query"], doc["content"], query["relevant_keywords"])
            keyword_scores.append((doc["id"], kw_score))

        # Find "relevant" docs (keyword score > 0 as proxy for relevance)
        relevant_ids = set(
            doc_id for doc_id, score in keyword_scores if score >= 2
        )

        if not relevant_ids:
            # Relax threshold
            relevant_ids = set(
                doc_id for doc_id, score in keyword_scores if score >= 1
            )

        # Compute NDCG
        crnt_ndcg = compute_ndcg(crnt_scores, relevant_ids, k=10)
        kw_ndcg = compute_ndcg(keyword_scores, relevant_ids, k=10)

        # Hit rate: is there at least one relevant doc in top 5?
        crnt_top5 = set(doc_id for doc_id, _ in sorted(crnt_scores, key=lambda x: x[1], reverse=True)[:5])
        kw_top5 = set(doc_id for doc_id, _ in sorted(keyword_scores, key=lambda x: x[1], reverse=True)[:5])
        crnt_hit = len(crnt_top5 & relevant_ids) > 0
        kw_hit = len(kw_top5 & relevant_ids) > 0

        print(f"  Relevant docs: {len(relevant_ids)}")
        print(f"  CRNT  NDCG@10={crnt_ndcg:.4f}  Hit@5={'✓' if crnt_hit else '✗'}")
        print(f"  KW    NDCG@10={kw_ndcg:.4f}  Hit@5={'✓' if kw_hit else '✗'}")

        # Show CRNT top 3
        crnt_top3 = sorted(crnt_scores, key=lambda x: x[1], reverse=True)[:3]
        print(f"  CRNT top 3:")
        for doc_id, score in crnt_top3:
            doc = next(d for d in law_data if d["id"] == doc_id)
            print(f"    [{doc['law']} {doc['article']}] score={score:.4f}  {doc['content'][:60]}")

        results.append({
            "query_id": query["id"],
            "query": query["query"],
            "domain": query["domain"],
            "n_relevant": len(relevant_ids),
            "crnt_ndcg10": float(crnt_ndcg),
            "kw_ndcg10": float(kw_ndcg),
            "crnt_hit5": crnt_hit,
            "kw_hit5": kw_hit,
        })

    # Summary
    print(f"\n{'='*60}")
    print("  Exp003 Summary — CRNT vs Keyword Baseline")
    print(f"{'-'*60}")

    crnt_ndcgs = [r["crnt_ndcg10"] for r in results]
    kw_ndcgs = [r["kw_ndcg10"] for r in results]
    crnt_hits = sum(1 for r in results if r["crnt_hit5"])
    kw_hits = sum(1 for r in results if r["kw_hit5"])

    print(f"  CRNT   mean NDCG@10={np.mean(crnt_ndcgs):.4f}  Hit@5={crnt_hits}/{len(results)}")
    print(f"  KW     mean NDCG@10={np.mean(kw_ndcgs):.4f}  Hit@5={kw_hits}/{len(results)}")

    if np.mean(kw_ndcgs) > 0:
        delta = (np.mean(crnt_ndcgs) - np.mean(kw_ndcgs)) / np.mean(kw_ndcgs) * 100
        print(f"  Delta: {delta:+.2f}%")

    print(f"{'='*60}")

    # Save
    out_path = os.path.join(OUT_DIR, "exp003_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "meta": {"date": "2026-04-09", "n_queries": len(results), "n_docs": len(law_data)},
            "per_query": results,
            "summary": {
                "crnt_mean_ndcg10": float(np.mean(crnt_ndcgs)),
                "kw_mean_ndcg10": float(np.mean(kw_ndcgs)),
                "crnt_hit5": crnt_hits,
                "kw_hit5": kw_hits,
            }
        }, f, ensure_ascii=False, indent=2)
    print(f"\nSaved: {out_path}")
    print(f"Total time: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
