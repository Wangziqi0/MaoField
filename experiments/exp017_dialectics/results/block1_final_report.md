# Block I complete (2026年 04月 12日 星期日 21:21:22 CST)

## Files produced
- block1_baselines.csv (final, 5x6 = 30 rows)
- block1_summary.md (final)
- block1_partial_baselines.csv / block1_partial_summary.md (early snapshot, 15 rows)

## BGE HTTP stats
  [arguana/bge] done 3438.8s fails=0.0% -> /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block1/arguana_bge_ranks.json
  [trec-covid/bge] done 41.6s fails=0.0% -> /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block1/trec-covid_bge_ranks.json
  [nfcorpus/bge] done 288.2s fails=0.0% -> /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block1/nfcorpus_bge_ranks.json
  [scifact/bge] done 310.7s fails=0.0% -> /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block1/scifact_bge_ranks.json
  [fiqa/bge] done 574.3s fails=0.0% -> /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block1/fiqa_bge_ranks.json

## MaoField runtimes
-rw-rw-r-- 1 amd amd 35633569  4月 12 19:23 /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block1/arguana_maofield_baseline_out.json
-rw-rw-r-- 1 amd amd  8661890  4月 12 20:14 /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block1/arguana_maofield_E_out.json
-rw-rw-r-- 1 amd amd 10058856  4月 12 17:50 /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block1/fiqa_maofield_baseline_out.json
-rw-rw-r-- 1 amd amd  2149322  4月 12 18:14 /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block1/fiqa_maofield_E_out.json
-rw-rw-r-- 1 amd amd  1373947  4月 12 20:16 /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block1/trec-covid_maofield_baseline_out.json
-rw-rw-r-- 1 amd amd   737773  4月 12 20:18 /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block1/trec-covid_maofield_E_out.json

## block1_baselines.csv
dataset,scorer,n_queries,ndcg10,p10,mrr10,runtime_s
nfcorpus,bm25,323,0.30632221168269674,0.21733746130030962,0.5061243795763919,0.0025959014892578125
nfcorpus,s1,323,0.13660502801123323,0.11733746130030959,0.24176495159467296,0.5268614292144775
nfcorpus,s4,323,0.2401175654016554,0.178328173374613,0.42862671384343204,4.261425018310547
nfcorpus,bge,323,0.3104434723992524,0.22229102167182666,0.5300850164627255,288.2131013870239
nfcorpus,maofield_baseline,323,0.056456567794185446,0.05820433436532508,0.12946704997788586,937.664341894
nfcorpus,maofield_E,323,0.20261068092472242,0.17461300309597524,0.3210329745933461,701.626141548
scifact,bm25,300,0.6594488905317624,0.08533333333333332,0.6291931216931217,0.0023720264434814453
scifact,s1,300,0.19202033082059464,0.03200000000000001,0.16835582010582012,0.4967637062072754
scifact,s4,300,0.4109924192649119,0.059,0.3788452380952381,4.131507635116577
scifact,bge,300,0.6222744887850911,0.08299999999999999,0.5898095238095238,310.6618676185608
scifact,maofield_baseline,300,0.040265774019484946,0.009666666666666667,0.026030423280423282,856.357965489
scifact,maofield_E,300,0.30020025350625096,0.06899999999999999,0.20682407407407408,668.410506883
fiqa,bm25,648,0.21668445500943226,0.06188271604938272,0.27028586125808346,0.002856731414794922
fiqa,s1,648,0.06860666799533154,0.022222222222222223,0.07411204193611601,0.4436502456665039
fiqa,s4,648,0.11634169910418359,0.036882716049382716,0.14787073780129337,5.026148557662964
fiqa,bge,648,0.2992415717099509,0.079320987654321,0.3827632030178326,574.268392086029
fiqa,maofield_baseline,648,0.02942197226937069,0.013117283950617283,0.03745100921026846,1874.02398354
fiqa,maofield_E,648,0.10819505917606086,0.04444444444444445,0.11415527630805408,1419.176767294
arguana,bm25,1406,0.283768622138595,0.0603840682788051,0.18359468491047437,0.009388923645019531
arguana,s1,1406,0.05558957164452322,0.012731152204836414,0.034429542324279166,1.0766820907592773
arguana,s4,1406,0.20854026300588058,0.04516358463726884,0.13289247894511053,14.630795001983643
arguana,bge,1406,0.45602944812039653,0.07105263157894737,0.3754812142970037,3438.7642855644226
arguana,maofield_baseline,1406,0.028899715868995656,0.006827880512091039,0.017203481677165885,4116.992072644
arguana,maofield_E,1406,0.15138406794408463,0.03470839260312944,0.09371796608638713,3059.830323089
trec-covid,bm25,50,0.5588999629852218,0.634,0.7825238095238096,0.00027108192443847656
trec-covid,s1,50,0.4298544122697421,0.5100000000000001,0.6917460317460318,0.03688311576843262
trec-covid,s4,50,0.3961754384129806,0.47,0.6211587301587301,0.3218839168548584
trec-covid,bge,50,0.7256565445970119,0.7979999999999999,0.8956666666666666,41.56570267677307
trec-covid,maofield_baseline,50,0.3553447417725055,0.43,0.6396666666666667,147.930268777
trec-covid,maofield_E,50,0.49318536338014773,0.5780000000000001,0.7030238095238096,110.287798554

## block1_summary.md
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