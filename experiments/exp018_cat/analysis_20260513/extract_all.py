"""
exp018_cat MaoField framework 实证数据 100% 落地脚本
2026-05-13 重新算 framework 全部实验数字 + bootstrap CI
所有数字从 jsonl 实读 + 重新算,禁止引用任何报告数字
"""
import json
import os
import math
from pathlib import Path

# 主目录
LOGS = Path('/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/logs')
BACKUP = LOGS / 'host22_backup_20260512'

def load_jsonl(path):
    """加载 jsonl,返回 list of dicts;只保留 generation_done 行"""
    gens = []
    run_start = None
    with open(path) as f:
        for line in f:
            try:
                d = json.loads(line)
                if d.get('stage') == 'run_start':
                    run_start = d
                if d.get('stage') == 'generation_done':
                    gens.append(d)
            except json.JSONDecodeError:
                continue
    return run_start, gens

def get_ppl(d):
    """从 generation_done dict 中提取 test_perplexity (float)
    test_perplexity 可能是 float,也可能是 dict (smoke_test) ;返回 float 或 None"""
    tp = d.get('test_perplexity')
    if tp is None:
        return None
    if isinstance(tp, dict):
        return tp.get('mean_perplexity')
    if isinstance(tp, float) and math.isinf(tp):
        return None  # Infinity
    if isinstance(tp, float) and math.isnan(tp):
        return None
    return tp

def extract_ppl_series(gens):
    """提取 PPL 序列 (gen 0 - gen 9),返回 list of (gen, val_ppl, test_ppl)"""
    by_gen = {}
    for d in gens:
        g = d.get('generation')
        if g is None:
            continue
        valp = d.get('val_perplexity')
        if isinstance(valp, float) and (math.isinf(valp) or math.isnan(valp)):
            valp = None
        testp = get_ppl(d)
        by_gen[g] = (valp, testp, d.get('distinct_3'))
    return by_gen

# === 组一:Shumailov 严格镜像 ===
print('=' * 80)
print('组一:Shumailov 严格镜像基线')
print('=' * 80)

shu_file = LOGS / 'shumailov_no_preserve_seed42_20260508_092730.jsonl'
rs, gens = load_jsonl(shu_file)
series = extract_ppl_series(gens)
print(f"文件: {shu_file.name}")
print(f"  gens 数: {len(gens)}")
print(f"  字段: condition={rs.get('condition','?') if rs else '?'} seed={rs.get('seed','?') if rs else '?'}")
print()
print(f"  {'gen':<4} {'val_ppl':<12} {'test_ppl':<12} {'distinct_3':<12}")
for g in range(10):
    if g in series:
        valp, testp, d3 = series[g]
        d3s = f"{d3:.4f}" if d3 is not None else "None"
        valps = f"{valp:.3f}" if valp else "None"
        testps = f"{testp:.3f}" if testp else "None/Inf"
        print(f"  {g:<4} {valps:<12} {testps:<12} {d3s:<12}")
