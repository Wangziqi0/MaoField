# Block I baseline table  (5 datasets x 6 scorers)

Pool = BM25 top-100 per query. All scorers rerank within this pool.

Metric below: **nDCG@10** (mean over queries with non-empty qrels).

| dataset | bm25 | s1 | s4 | bge | maofield_baseline | maofield_E |
|---|---:|---:|---:|---:|---:|---:|
| nfcorpus | 0.3063 | 0.1366 | 0.2401 | 0.3104 | 0.0565 | 0.2026 |
| scifact | 0.6594 | 0.1920 | 0.4110 | 0.6223 | 0.0403 | 0.3002 |
| fiqa | 0.2167 | 0.0686 | 0.1163 | - | - | - |
| arguana | - | - | - | - | - | - |
| trec-covid | - | - | - | - | - | - |

## P@10

| dataset | bm25 | s1 | s4 | bge | maofield_baseline | maofield_E |
|---|---:|---:|---:|---:|---:|---:|
| nfcorpus | 0.2173 | 0.1173 | 0.1783 | 0.2223 | 0.0582 | 0.1746 |
| scifact | 0.0853 | 0.0320 | 0.0590 | 0.0830 | 0.0097 | 0.0690 |
| fiqa | 0.0619 | 0.0222 | 0.0369 | - | - | - |
| arguana | - | - | - | - | - | - |
| trec-covid | - | - | - | - | - | - |

## MRR@10

| dataset | bm25 | s1 | s4 | bge | maofield_baseline | maofield_E |
|---|---:|---:|---:|---:|---:|---:|
| nfcorpus | 0.5061 | 0.2418 | 0.4286 | 0.5301 | 0.1295 | 0.3210 |
| scifact | 0.6292 | 0.1684 | 0.3788 | 0.5898 | 0.0260 | 0.2068 |
| fiqa | 0.2703 | 0.0741 | 0.1479 | - | - | - |
| arguana | - | - | - | - | - | - |
| trec-covid | - | - | - | - | - | - |

## Core observations

- **nfcorpus**:  MaoField-E vs S1 = +48.3%  MaoField-E - BGE = -10.78 pp  E - baseline = +14.62 pp
- **scifact**:  MaoField-E vs S1 = +56.3%  MaoField-E - BGE = -32.21 pp  E - baseline = +25.99 pp
- **fiqa**:
- **arguana**:
- **trec-covid**: