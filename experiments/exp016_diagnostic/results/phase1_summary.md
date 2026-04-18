# Phase 1 诊断 AUC 矩阵 (exp016)

总耗时: 428.1s  seed=20260412  workers=64

## AUC 矩阵 (每 query 正例 vs 99 负例平均 AUC)

| dataset | n_q | s1_byte_cos | s2_char_jac | s3_2gram_jac | s4_3gram_jac | s5_lev | s6_bm25 | best |
|---|---|---|---|---|---|---|---|---|
| nfcorpus | 323 | 0.6107 | 0.5186 | 0.5931 | 0.6770 | 0.4867 | 0.6851 | **s6_bm25** |
| scifact | 300 | 0.7687 | 0.5677 | 0.6529 | 0.9120 | 0.5571 | 0.9771 | **s6_bm25** |
| fiqa | 648 | 0.7219 | 0.4402 | 0.5883 | 0.8229 | 0.3471 | 0.9313 | **s6_bm25** |
| arguana | 1000 | 0.7370 | 0.6555 | 0.8258 | 0.9127 | 0.7233 | 0.9704 | **s6_bm25** |
| trec-covid | 50 | 0.6814 | 0.5282 | 0.6046 | 0.7686 | 0.4396 | 0.8758 | **s6_bm25** |
| quora | 1000 | 0.9712 | 0.9700 | 0.9986 | 0.9989 | 0.9712 | 0.9997 | **s6_bm25** |
| codesearchnet | 1000 | 0.8643 | 0.8890 | 0.9893 | 0.9995 | 0.8352 | 1.0000 | **s6_bm25** |

## d' 矩阵

| dataset | n_q | s1_byte_cos | s2_char_jac | s3_2gram_jac | s4_3gram_jac | s5_lev | s6_bm25 ||
|---|---|---|---|---|---|---|---|
| nfcorpus | 323 | 0.047 | 0.012 | 0.091 | 0.364 | -0.022 | 0.737 |
| scifact | 300 | 0.348 | 0.160 | 0.304 | 1.061 | 0.044 | 1.761 |
| fiqa | 648 | 0.256 | -0.148 | 0.211 | 0.848 | -0.399 | 1.381 |
| arguana | 1000 | 0.523 | 0.545 | 1.036 | 1.251 | 0.559 | 0.903 |
| trec-covid | 50 | 0.397 | 0.050 | 0.322 | 0.656 | -0.181 | 1.074 |
| quora | 1000 | 2.076 | 2.437 | 3.536 | 3.347 | 2.601 | 3.080 |
| codesearchnet | 1000 | 0.534 | 1.105 | 1.877 | 2.376 | 1.000 | 1.469 |

## 每数据集最高 AUC 判读

| dataset | best metric | AUC | 判读 |
|---|---|---|---|
| nfcorpus | s6_bm25 | 0.6851 | weak |
| scifact | s6_bm25 | 0.9771 | strong |
| fiqa | s6_bm25 | 0.9313 | strong |
| arguana | s6_bm25 | 0.9704 | strong |
| trec-covid | s6_bm25 | 0.8758 | strong |
| quora | s6_bm25 | 0.9997 | strong |
| codesearchnet | s6_bm25 | 1.0000 | strong |

## 判读阈值

- AUC<0.55: 几乎无区分度 (near-random)
- [0.55,0.70): 弱 (weak)
- [0.70,0.85): 中 (medium)
- >=0.85: 强 (strong)


## 跳过/异常

- nfcorpus: skipped_no_neg=0
- scifact: skipped_no_neg=0
- fiqa: skipped_no_neg=0
- arguana: skipped_no_neg=0
- trec-covid: skipped_no_neg=0
- quora: skipped_no_neg=0
- codesearchnet: skipped_no_neg=0