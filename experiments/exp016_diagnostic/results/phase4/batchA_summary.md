# Phase 4 Batch A: 四 scorer nDCG@10 对比

统一候选池 = BM25 top-100，四 scorer 均在该 100 内重排。

| dataset | n_q | BM25 nDCG@10 | S1 (byte-cos) | S4 (3gram-jac) | MaoField |
|---|---:|---:|---:|---:|---:|
| nfcorpus | 323 | 0.3063 | 0.1366 | 0.2401 | 0.0565 |
| scifact | 300 | 0.6594 | 0.1920 | 0.4110 | 0.0403 |

## P@10

| dataset | BM25 | S1 | S4 | MaoField |
|---|---:|---:|---:|---:|
| nfcorpus | 0.2173 | 0.1173 | 0.1783 | 0.0582 |
| scifact | 0.0853 | 0.0320 | 0.0590 | 0.0097 |

## 三个诊断问题

- **nfcorpus**:
  - MaoField vs S1: -8.01 pp
  - MaoField vs BM25: -24.99 pp
  - S4 vs BM25: -6.62 pp
- **scifact**:
  - MaoField vs S1: -15.18 pp
  - MaoField vs BM25: -61.92 pp
  - S4 vs BM25: -24.85 pp