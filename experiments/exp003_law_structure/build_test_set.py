"""
MaoField Exp003: 构造测试集
============================

手工构造 15 个法律 query + 相关法条标注。
覆盖刑法、民法、劳动法、行政法等领域。
"""

import json
import os

OUT_DIR = "/home/amd/HEZIMENG/MaoField/experiments/exp003_law_structure/results"

test_queries = [
    {
        "id": "q01",
        "query": "被公司辞退了怎么赔偿",
        "domain": "劳动法",
        "relevant_keywords": ["解除", "劳动合同", "经济补偿", "赔偿金", "用人单位"],
        "expected_species": {
            "subject": ["公司", "用人单位"],
            "action": ["辞退", "解除"],
            "object": [],
            "condition": [],
            "consequence": ["赔偿"],
            "legal_basis": []
        }
    },
    {
        "id": "q02",
        "query": "故意伤害别人判几年",
        "domain": "刑法",
        "relevant_keywords": ["故意伤害", "有期徒刑", "拘役", "身体"],
        "expected_species": {
            "subject": [],
            "action": ["故意伤害", "伤害"],
            "object": ["别人"],
            "condition": [],
            "consequence": ["有期徒刑"],
            "legal_basis": []
        }
    },
    {
        "id": "q03",
        "query": "离婚后房子怎么分",
        "domain": "民商法",
        "relevant_keywords": ["离婚", "财产", "分割", "夫妻", "共同财产"],
        "expected_species": {
            "subject": ["夫妻"],
            "action": ["离婚"],
            "object": ["房子", "财产"],
            "condition": [],
            "consequence": [],
            "legal_basis": []
        }
    },
    {
        "id": "q04",
        "query": "借钱不还怎么起诉",
        "domain": "民商法",
        "relevant_keywords": ["借款", "债务", "还款", "起诉", "诉讼", "债权人", "债务人"],
        "expected_species": {
            "subject": ["债务人", "债权人"],
            "action": ["起诉"],
            "object": ["借款"],
            "condition": ["不还"],
            "consequence": [],
            "legal_basis": []
        }
    },
    {
        "id": "q05",
        "query": "醉驾怎么处罚",
        "domain": "刑法",
        "relevant_keywords": ["醉酒", "驾驶", "危险驾驶", "拘役", "罚金", "机动车"],
        "expected_species": {
            "subject": [],
            "action": ["驾驶"],
            "object": ["机动车"],
            "condition": ["醉酒"],
            "consequence": ["拘役", "罚金"],
            "legal_basis": []
        }
    },
    {
        "id": "q06",
        "query": "公司不给加班费怎么办",
        "domain": "劳动法",
        "relevant_keywords": ["加班", "工资", "报酬", "用人单位", "劳动者", "支付"],
        "expected_species": {
            "subject": ["公司", "用人单位"],
            "action": ["支付"],
            "object": ["加班费"],
            "condition": [],
            "consequence": ["支付"],
            "legal_basis": []
        }
    },
    {
        "id": "q07",
        "query": "被人骗了钱怎么报案",
        "domain": "刑法",
        "relevant_keywords": ["诈骗", "公私财物", "数额较大", "有期徒刑", "罚金"],
        "expected_species": {
            "subject": [],
            "action": ["诈骗"],
            "object": ["钱", "财物"],
            "condition": [],
            "consequence": ["有期徒刑"],
            "legal_basis": []
        }
    },
    {
        "id": "q08",
        "query": "房东不退押金怎么办",
        "domain": "民商法",
        "relevant_keywords": ["租赁", "押金", "返还", "承租人", "出租人", "合同"],
        "expected_species": {
            "subject": ["房东", "出租人"],
            "action": ["返还"],
            "object": ["押金"],
            "condition": [],
            "consequence": ["返还"],
            "legal_basis": []
        }
    },
    {
        "id": "q09",
        "query": "未成年人犯罪怎么判",
        "domain": "刑法",
        "relevant_keywords": ["未成年人", "刑事责任", "从轻", "减轻", "十四周岁", "十六周岁"],
        "expected_species": {
            "subject": ["未成年人"],
            "action": ["犯罪"],
            "object": [],
            "condition": ["未成年"],
            "consequence": ["从轻", "减轻"],
            "legal_basis": []
        }
    },
    {
        "id": "q10",
        "query": "工伤怎么认定和赔偿",
        "domain": "社会法",
        "relevant_keywords": ["工伤", "认定", "赔偿", "劳动者", "用人单位", "工伤保险"],
        "expected_species": {
            "subject": ["劳动者", "用人单位"],
            "action": ["认定"],
            "object": ["工伤"],
            "condition": [],
            "consequence": ["赔偿"],
            "legal_basis": []
        }
    },
    {
        "id": "q11",
        "query": "偷东西会判刑吗",
        "domain": "刑法",
        "relevant_keywords": ["盗窃", "公私财物", "数额较大", "有期徒刑", "拘役"],
        "expected_species": {
            "subject": [],
            "action": ["盗窃"],
            "object": ["东西", "财物"],
            "condition": [],
            "consequence": ["有期徒刑", "拘役"],
            "legal_basis": []
        }
    },
    {
        "id": "q12",
        "query": "遗产怎么继承",
        "domain": "民商法",
        "relevant_keywords": ["继承", "遗产", "继承人", "被继承人", "法定继承", "遗嘱"],
        "expected_species": {
            "subject": ["继承人", "被继承人"],
            "action": ["继承"],
            "object": ["遗产"],
            "condition": [],
            "consequence": [],
            "legal_basis": []
        }
    },
    {
        "id": "q13",
        "query": "交通事故责任怎么划分",
        "domain": "行政法",
        "relevant_keywords": ["交通事故", "责任", "赔偿", "机动车", "行人", "公安机关"],
        "expected_species": {
            "subject": ["公安机关"],
            "action": ["划分"],
            "object": ["责任"],
            "condition": ["交通事故"],
            "consequence": ["赔偿"],
            "legal_basis": []
        }
    },
    {
        "id": "q14",
        "query": "合同违约要赔多少钱",
        "domain": "民商法",
        "relevant_keywords": ["违约", "赔偿", "违约金", "损失", "合同", "当事人"],
        "expected_species": {
            "subject": ["当事人"],
            "action": ["违约"],
            "object": ["合同"],
            "condition": [],
            "consequence": ["赔偿", "违约金"],
            "legal_basis": []
        }
    },
    {
        "id": "q15",
        "query": "被行政拘留了怎么申诉",
        "domain": "行政法",
        "relevant_keywords": ["行政拘留", "申诉", "复议", "行政处罚", "公安机关"],
        "expected_species": {
            "subject": ["公安机关"],
            "action": ["拘留", "申诉"],
            "object": [],
            "condition": ["行政拘留"],
            "consequence": [],
            "legal_basis": []
        }
    },
]

def main():
    out_path = os.path.join(OUT_DIR, "test_queries.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(test_queries, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(test_queries)} test queries to {out_path}")

    # Summary
    domains = {}
    for q in test_queries:
        d = q["domain"]
        domains[d] = domains.get(d, 0) + 1
    print("\nDomain distribution:")
    for d, c in sorted(domains.items()):
        print(f"  {d}: {c}")


if __name__ == "__main__":
    main()
