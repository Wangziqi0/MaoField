# Block I baseline table  (5 datasets x 6 scorers)

Pool = BM25 top-100 per query. All scorers rerank within this pool.

Metric below: **nDCG@10** (mean over queries with non-empty qrels).

| dataset | bm25 | s1 | s4 | bge | maofield_baseline | maofield_E |
|---|---:|---:|---:|---:|---:|---:|
| nfcorpus | 0.3063 | 0.1366 | 0.2401 | 0.3104 | 0.0565 | 0.2026 |
| scifact | 0.6594 | 0.1920 | 0.4110 | 0.6223 | 0.0403 | 0.3002 |
| fiqa | 0.2167 | 0.0686 | 0.1163 | 0.2992 | 0.0294 | 0.1082 |
| arguana | 0.2838 | 0.0556 | 0.2085 | 0.4560 | 0.0289 | 0.1514 |
| trec-covid | 0.5589 | 0.4299 | 0.3962 | 0.7257 | 0.3553 | 0.4932 |

## P@10

| dataset | bm25 | s1 | s4 | bge | maofield_baseline | maofield_E |
|---|---:|---:|---:|---:|---:|---:|
| nfcorpus | 0.2173 | 0.1173 | 0.1783 | 0.2223 | 0.0582 | 0.1746 |
| scifact | 0.0853 | 0.0320 | 0.0590 | 0.0830 | 0.0097 | 0.0690 |
| fiqa | 0.0619 | 0.0222 | 0.0369 | 0.0793 | 0.0131 | 0.0444 |
| arguana | 0.0604 | 0.0127 | 0.0452 | 0.0711 | 0.0068 | 0.0347 |
| trec-covid | 0.6340 | 0.5100 | 0.4700 | 0.7980 | 0.4300 | 0.5780 |

## MRR@10

| dataset | bm25 | s1 | s4 | bge | maofield_baseline | maofield_E |
|---|---:|---:|---:|---:|---:|---:|
| nfcorpus | 0.5061 | 0.2418 | 0.4286 | 0.5301 | 0.1295 | 0.3210 |
| scifact | 0.6292 | 0.1684 | 0.3788 | 0.5898 | 0.0260 | 0.2068 |
| fiqa | 0.2703 | 0.0741 | 0.1479 | 0.3828 | 0.0375 | 0.1142 |
| arguana | 0.1836 | 0.0344 | 0.1329 | 0.3755 | 0.0172 | 0.0937 |
| trec-covid | 0.7825 | 0.6917 | 0.6212 | 0.8957 | 0.6397 | 0.7030 |

## Core observations

- **nfcorpus**:  MaoField-E vs S1 = +48.3%  MaoField-E - BGE = -10.78 pp  E - baseline = +14.62 pp
- **scifact**:  MaoField-E vs S1 = +56.3%  MaoField-E - BGE = -32.21 pp  E - baseline = +25.99 pp
- **fiqa**:  MaoField-E vs S1 = +57.7%  MaoField-E - BGE = -19.10 pp  E - baseline = +7.88 pp
- **arguana**:  MaoField-E vs S1 = +172.3%  MaoField-E - BGE = -30.46 pp  E - baseline = +12.25 pp
- **trec-covid**:  MaoField-E vs S1 = +14.7%  MaoField-E - BGE = -23.25 pp  E - baseline = +13.78 pp