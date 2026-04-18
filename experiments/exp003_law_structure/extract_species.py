"""
MaoField Exp003 Step 1: 法条结构提取
=====================================

从 23,853 条法条中提取 6 类结构化物种（CRNT 的"物种"）。
纯规则/正则提取，不用任何神经网络。

物种: Subject, Action, Object, Condition, Consequence, LegalBasis
浓度: 结构存在强度（0.0/0.5/1.0/1.5+），不是统计量
"""

import sqlite3
import re
import json
import time
import os

DB_PATH = "/home/amd/HEZIMENG/legal-assistant/knowledge_base/legal_data.db"
OUT_DIR = "/home/amd/HEZIMENG/MaoField/experiments/exp003_law_structure/results"

# ── 提取规则 ──

SUBJECT_PATTERNS = [
    r"(用人单位|劳动者|工人|职工|雇主|雇员)",
    r"(公民|自然人|法人|非法人组织)",
    r"(当事人|双方当事人|一方当事人)",
    r"(被告人|犯罪嫌疑人|罪犯|被告|原告|第三人)",
    r"(债务人|债权人|保证人|抵押人|质权人)",
    r"(国家机关|人民法院|人民检察院|公安机关|司法行政机关)",
    r"(国务院|地方各级人民政府|县级以上人民政府)",
    r"(企业|公司|合伙企业|个人独资企业|个体工商户)",
    r"(未成年人|限制民事行为能力人|无民事行为能力人|完全民事行为能力人)",
    r"(夫妻双方|夫妻|父母|子女|继承人|被继承人|监护人|被监护人)",
    r"(消费者|经营者|生产者|销售者)",
    r"(承租人|出租人|买受人|出卖人|委托人|受托人)",
    r"(侵权人|被侵权人|受害人|加害人)",
    r"(申请人|被申请人|上诉人|被上诉人)",
    r"(行政机关|行政相对人)",
    r"(纳税人|扣缴义务人)",
]

ACTION_WORDS = [
    "解除", "终止", "变更", "签订", "订立", "履行", "违反", "违约",
    "侵害", "损害", "伤害", "杀害", "盗窃", "抢劫", "抢夺", "诈骗",
    "敲诈勒索", "绑架", "拐卖", "非法拘禁", "强奸", "猥亵",
    "贪污", "受贿", "行贿", "挪用", "滥用职权", "玩忽职守",
    "拘留", "逮捕", "起诉", "公诉", "自诉", "判决", "裁定", "执行",
    "赔偿", "补偿", "返还", "恢复", "撤销", "变更", "确认",
    "支付", "给付", "交付", "转让", "继承", "赠与", "租赁",
    "申请", "审查", "批准", "许可", "登记", "备案",
    "没收", "罚款", "吊销", "暂扣", "查封", "扣押", "冻结",
    "调解", "仲裁", "诉讼", "上诉", "申诉", "复议",
    "生产", "销售", "运输", "储存", "使用", "排放", "处置",
]

CONDITION_TRIGGERS = [
    "有下列情形之一", "有下列行为之一", "具有下列条件",
    "有下列情况之一", "符合下列条件",
    "在下列情况下", "在以下情形下",
    "如果", "若", "当", "在.*情况下", "在.*条件下",
    "经.*同意", "经.*批准", "经.*许可", "经.*授权",
    "未经", "未取得", "未依法",
    "违反.*规定", "违反.*约定",
    "因.*原因", "由于",
    "除.*外", "除非",
    "情节严重", "情节特别严重", "情节较轻", "情节恶劣",
    "数额较大", "数额巨大", "数额特别巨大",
    "造成严重后果", "造成重大损失",
]

CONSEQUENCE_TRIGGERS = [
    "处.*有期徒刑", "处.*拘役", "处.*管制", "处.*罚金",
    "判处.*有期徒刑", "判处.*无期徒刑", "判处.*死刑",
    "处以.*罚款", "罚款.*元",
    "应当赔偿", "应当补偿", "应当支付", "应当返还",
    "可以赔偿", "可以减轻", "可以免除",
    "给予.*处分", "给予.*处罚",
    "责令.*改正", "责令.*停止", "责令.*赔偿", "责令.*恢复",
    "没收.*财产", "没收.*违法所得",
    "吊销.*许可证", "吊销.*执照", "吊销.*资格",
    "撤销.*资格", "撤销.*登记",
    "不得.*", "禁止.*",
]

CONSEQUENCE_KEYWORDS = [
    "有期徒刑", "无期徒刑", "死刑", "拘役", "管制",
    "罚金", "罚款", "没收财产",
    "赔偿损失", "支付违约金", "经济补偿",
    "行政拘留", "治安拘留",
    "吊销", "撤销", "暂扣",
    "警告", "记过", "记大过", "降级", "撤职", "开除",
]

LEGAL_BASIS_PATTERNS = [
    r"依照本法第(\S+?)条",
    r"依照第(\S+?)条",
    r"依据本法第(\S+?)条",
    r"按照本法第(\S+?)条",
    r"参照(\S+?)的规定",
    r"根据《(.+?)》",
    r"依照《(.+?)》",
    r"适用《(.+?)》",
    r"按照《(.+?)》",
    r"依照.*第(\d+)条",
]


def extract_subjects(text):
    found = []
    for pattern in SUBJECT_PATTERNS:
        matches = re.findall(pattern, text)
        found.extend(matches)
    return list(set(found))


def extract_actions(text):
    found = []
    for word in ACTION_WORDS:
        if word in text:
            found.append(word)
    return found


def extract_conditions(text):
    found = []
    for trigger in CONDITION_TRIGGERS:
        if re.search(trigger, text):
            # Extract the matching part
            match = re.search(trigger, text)
            if match:
                found.append(match.group(0))
    return list(set(found))


def extract_consequences(text):
    found = []
    # Pattern-based
    for trigger in CONSEQUENCE_TRIGGERS:
        match = re.search(trigger, text)
        if match:
            found.append(match.group(0))
    # Keyword-based
    for kw in CONSEQUENCE_KEYWORDS:
        if kw in text:
            found.append(kw)
    return list(set(found))


def extract_legal_basis(text):
    found = []
    for pattern in LEGAL_BASIS_PATTERNS:
        matches = re.findall(pattern, text)
        found.extend(matches)
    return list(set(found))


def extract_objects(text, actions):
    """Extract objects: noun phrases after action verbs"""
    found = []
    for action in actions:
        # Find text after the action verb (up to punctuation)
        pattern = re.escape(action) + r"(.{1,20}?)(?:[，。；、,.]|$)"
        match = re.search(pattern, text)
        if match:
            obj = match.group(1).strip()
            if obj and len(obj) <= 15:
                found.append(obj)
    return list(set(found))


def compute_concentration(items, is_implicit=False):
    """
    Concentration = structural presence strength
    0.0 = not present
    0.5 = implicit
    1.0 = one explicit
    n = n explicit items
    """
    if not items:
        return 0.5 if is_implicit else 0.0
    return float(len(items))


def extract_species(text, law_name="", article=""):
    """Extract all 6 species from a single law article"""
    subjects = extract_subjects(text)
    actions = extract_actions(text)
    objects = extract_objects(text, actions)
    conditions = extract_conditions(text)
    consequences = extract_consequences(text)
    legal_basis = extract_legal_basis(text)

    # Implicit subject: if no explicit subject but has action, someone is doing it
    subject_implicit = (len(subjects) == 0 and len(actions) > 0)

    species = {
        "subject": subjects,
        "action": actions,
        "object": objects,
        "condition": conditions,
        "consequence": consequences,
        "legal_basis": legal_basis,
    }

    concentrations = {
        "subject": compute_concentration(subjects, is_implicit=subject_implicit),
        "action": compute_concentration(actions),
        "object": compute_concentration(objects),
        "condition": compute_concentration(conditions),
        "consequence": compute_concentration(consequences),
        "legal_basis": compute_concentration(legal_basis),
    }

    return species, concentrations


def main():
    print("=" * 60)
    print("MaoField Exp003 Step 1: 法条结构提取")
    print("=" * 60)
    t0 = time.time()

    # Load all law articles
    print("\nLoading law articles...")
    db = sqlite3.connect(DB_PATH)
    rows = db.execute(
        "SELECT id, law, article, content, category FROM law_chunks ORDER BY id"
    ).fetchall()
    db.close()
    print(f"  Loaded {len(rows)} law articles")

    # Extract species for each article
    print("\nExtracting species...")
    results = []
    stats = {
        "total": len(rows),
        "has_subject": 0,
        "has_action": 0,
        "has_object": 0,
        "has_condition": 0,
        "has_consequence": 0,
        "has_legal_basis": 0,
        "has_3plus": 0,  # Articles with >=3 species types
        "has_0": 0,  # Articles with no species
    }

    for i, (row_id, law, article, content, category) in enumerate(rows):
        species, concentrations = extract_species(content, law, article)

        result = {
            "id": row_id,
            "law": law,
            "article": article or "",
            "category": category or "",
            "content": content,
            "species": species,
            "concentrations": concentrations,
        }
        results.append(result)

        # Stats
        n_types = sum(1 for v in species.values() if len(v) > 0)
        if species["subject"]: stats["has_subject"] += 1
        if species["action"]: stats["has_action"] += 1
        if species["object"]: stats["has_object"] += 1
        if species["condition"]: stats["has_condition"] += 1
        if species["consequence"]: stats["has_consequence"] += 1
        if species["legal_basis"]: stats["has_legal_basis"] += 1
        if n_types >= 3: stats["has_3plus"] += 1
        if n_types == 0: stats["has_0"] += 1

        if (i + 1) % 5000 == 0:
            print(f"  {i+1}/{len(rows)}...")

    elapsed = time.time() - t0
    print(f"  Done ({elapsed:.1f}s)")

    # Print stats
    print(f"\n{'='*60}")
    print("  Species Extraction Statistics")
    print(f"{'-'*60}")
    for key in ["has_subject", "has_action", "has_object",
                "has_condition", "has_consequence", "has_legal_basis"]:
        name = key.replace("has_", "")
        count = stats[key]
        pct = count / stats["total"] * 100
        print(f"  {name:15s} {count:6d} / {stats['total']}  ({pct:.1f}%)")
    print(f"{'-'*60}")
    print(f"  {'>=3 species':15s} {stats['has_3plus']:6d} / {stats['total']}  ({stats['has_3plus']/stats['total']*100:.1f}%)")
    print(f"  {'0 species':15s} {stats['has_0']:6d} / {stats['total']}  ({stats['has_0']/stats['total']*100:.1f}%)")
    print(f"{'='*60}")

    # Show some examples
    print("\n  Sample extractions:")
    for r in results[:5]:
        print(f"\n  [{r['law']} {r['article']}]")
        print(f"  内容: {r['content'][:80]}...")
        for sp_name, sp_items in r['species'].items():
            if sp_items:
                print(f"    {sp_name}: {sp_items[:3]}")

    # Category breakdown
    print(f"\n{'='*60}")
    print("  Coverage by Category")
    print(f"{'-'*60}")
    cat_stats = {}
    for r in results:
        cat = r["category"] or "未分类"
        if cat not in cat_stats:
            cat_stats[cat] = {"total": 0, "has_3plus": 0}
        cat_stats[cat]["total"] += 1
        n_types = sum(1 for v in r["species"].values() if len(v) > 0)
        if n_types >= 3:
            cat_stats[cat]["has_3plus"] += 1

    for cat in sorted(cat_stats.keys()):
        s = cat_stats[cat]
        pct = s["has_3plus"] / s["total"] * 100 if s["total"] > 0 else 0
        print(f"  {cat:20s} {s['has_3plus']:5d}/{s['total']:5d} ({pct:.1f}%)")

    # Save
    out_path = os.path.join(OUT_DIR, "law_species.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nSaved {len(results)} articles to {out_path}")

    # Also save stats
    stats_path = os.path.join(OUT_DIR, "extraction_stats.json")
    with open(stats_path, "w") as f:
        json.dump({"stats": stats, "category_stats": cat_stats}, f, indent=2)
    print(f"Saved stats to {stats_path}")
    print(f"\nTotal time: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
