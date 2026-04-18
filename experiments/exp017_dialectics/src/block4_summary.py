#!/usr/bin/env python3
"""Render block4_summary.md with markdown tables (no conclusions)."""
import json, csv, time
from pathlib import Path

OUT = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4")

def md_table_from_csv(path):
    rows = list(csv.reader(open(path)))
    if not rows: return ""
    header = rows[0]
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    for r in rows[1:]:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def main():
    parts = []
    parts.append(f"# Block IV summary (auto-generated {time.strftime('%Y-%m-%d %H:%M:%S')})\n")
    parts.append("Four-way comparison of dialectical materialism vs idealism methods on three BEIR datasets.\n")
    parts.append("Groups:\n- IV-A 唯物动态: UTF-8 byte source -> Ginzburg-Landau PDE (FUSION_STEPS=0)\n- IV-B 唯心动态: BGE-M3 1024-d embedding source -> identical PDE\n- IV-C 唯心静态: BGE-M3 cosine reranking (no PDE)\n- IV-D 唯物静态: UTF-8 byte-frequency cosine (no PDE)\n")
    parts.append("Pool: BM25 top-20 per query (`exp017_dialectics/inputs_block1_top20/*.json`).\n")
    parts.append("\n## Core matrix `block4_matrix.csv`\n")
    parts.append(md_table_from_csv(OUT/"block4_matrix.csv"))

    # dim3
    parts.append("\n\n## Dim 3 robustness `dim3_robustness.csv`\n")
    p3 = OUT/"dim3_robustness.csv"
    if p3.exists():
        parts.append(md_table_from_csv(p3))
        d3 = json.load(open(OUT/"dim3_robustness.json"))
        parts.append(f"\n\nSubset: SciFact first {d3['subset_n']} queries; perturbation: ~{int(d3['frac']*100)}% WordNet substitution on content words.")
    else:
        parts.append("not run")

    # dim4
    parts.append("\n\n## Dim 4 attractor count `dim4_attractor_k.csv`\n")
    p4 = OUT/"dim4_attractor_k.csv"
    if p4.exists():
        parts.append(md_table_from_csv(p4))
        parts.append("\n\nSilhouette scan k=2..20 over three representations (raw_ab, amplitude, phase_cos_sin); k* picked at max silhouette.")
        parts.append("\nMatched 100-doc subset from NFCorpus top-20 pool.")

    # dim5
    parts.append("\n\n## Dim 5 cross-lingual\n")
    parts.append("**SKIPPED.** mMARCO Chinese requires downloading multi-GB collections (`unicamp-dl/mmarco/data/google/collections/{chinese,english}_collection.tsv`) and constructing zh_query x en_doc test set. Network and time constraints; per spec dim5 is skippable.")

    # files
    parts.append("\n\n## Files (absolute paths)\n")
    for f in sorted((OUT).glob("*")):
        parts.append(f"- `{f}`")

    out_path = OUT/"block4_summary.md"
    open(out_path, "w").write("\n".join(parts))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
