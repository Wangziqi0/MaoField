# Block IV summary (auto-generated 2026-04-13 10:40:24)

Four-way comparison of dialectical materialism vs idealism methods on three BEIR datasets.

Groups:
- IV-A 唯物动态: UTF-8 byte source -> Ginzburg-Landau PDE (FUSION_STEPS=0)
- IV-B 唯心动态: BGE-M3 1024-d embedding source -> identical PDE
- IV-C 唯心静态: BGE-M3 cosine reranking (no PDE)
- IV-D 唯物静态: UTF-8 byte-frequency cosine (no PDE)

Pool: BM25 top-20 per query (`exp017_dialectics/inputs_block1_top20/*.json`).


## Core matrix `block4_matrix.csv`

| dimension | dataset | IV-A | IV-B | IV-C | IV-D |
|---|---|---|---|---|---|
| 总体nDCG10 | nfcorpus | 0.2026 | 0.2495 | 0.3089 | 0.2159 |
| 总体nDCG10 | scifact | 0.3002 | 0.3814 | 0.6143 | 0.3555 |
| 总体nDCG10 | fiqa | 0.1082 | 0.1901 | 0.2774 | 0.1309 |
| 长尾nDCG10(n=227) | nfcorpus | 0.2117 | 0.2608 | 0.3149 | 0.2264 |
| 长尾nDCG10(n=3) | scifact | 0.6667 | 0.4206 | 0.2854 | 0.2477 |
| 长尾nDCG10(n=29) | fiqa | 0.1404 | 0.1551 | 0.2199 | 0.1341 |
| 鲁棒性drop_nDCG10(扰动-原) | scifact | -0.0102 | 0.0112 | -0.0150 | 0.0309 |
| attractor_k* (kmeans silhouette) | nfcorpus_doc100 | 2 | 2 | NA | NA |


## Dim 3 robustness `dim3_robustness.csv`

| group | orig_nDCG10 | pert_nDCG10 | drop_nDCG10 |
|---|---|---|---|
| IV-A | 0.2855 | 0.2956 | -0.0102 |
| IV-B | 0.3766 | 0.3654 | 0.0112 |
| IV-C | 0.6212 | 0.6362 | -0.0150 |
| IV-D | 0.3568 | 0.3259 | 0.0309 |


Subset: SciFact first 200 queries; perturbation: ~30% WordNet substitution on content words.


## Dim 4 attractor count `dim4_attractor_k.csv`

| group | n_docs | best_representation | k_star | silhouette |
|---|---|---|---|---|
| IV-A | 100 | phase_cos_sin | 2 | 0.1285 |
| IV-B | 100 | raw_ab | 2 | 0.0571 |


Silhouette scan k=2..20 over three representations (raw_ab, amplitude, phase_cos_sin); k* picked at max silhouette.

Matched 100-doc subset from NFCorpus top-20 pool.


## Dim 5 cross-lingual

**SKIPPED.** mMARCO Chinese requires downloading multi-GB collections (`unicamp-dl/mmarco/data/google/collections/{chinese,english}_collection.tsv`) and constructing zh_query x en_doc test set. Network and time constraints; per spec dim5 is skippable.


## Files (absolute paths)

- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/IV-A_nfcorpus_out.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/IV-A_scifact_out.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/IV-B_fiqa_out.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/IV-B_nfcorpus_out.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/IV-B_nfcorpus_states.bin`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/IV-B_nfcorpus_states_meta.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/IV-B_scifact_out.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/IV-C_fiqa.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/IV-C_nfcorpus.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/IV-C_scifact.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/IV-D_fiqa.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/IV-D_nfcorpus.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/IV-D_scifact.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/block4_matrix.csv`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/dim3_IV-A_perturbed_out.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/dim3_IV-B_perturbed_out.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/dim3_robustness.csv`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/dim3_robustness.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/dim3_scifact_perturbed_embeddings.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/dim3_scifact_perturbed_input.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/dim4_IV-A_meta.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/dim4_IV-A_states.bin`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/dim4_IV-B_meta.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/dim4_IV-B_states.bin`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/dim4_attractor_k.csv`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/dim4_attractor_k.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/dim4_attractor_scan.csv`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/dim4_input100.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/dim5_crosslingual.csv`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/embeddings_fiqa.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/embeddings_fiqa.npz`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/embeddings_nfcorpus.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/embeddings_nfcorpus.npz`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/embeddings_scifact.json`
- `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/embeddings_scifact.npz`