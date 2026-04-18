"""Block III: Attractor count analysis via clustering on final ψ states.
Load 100 docs' (a, b) fields (32³ each), cluster by multiple distance metrics,
silhouette scan k=2..20 to find effective attractor count k*."""
import json
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

RESULTS = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results")
G = 32; N = G**3

meta = json.load(open(RESULTS/"block3_meta.json"))
doc_ids = meta["doc_ids"]
n = meta["n_docs"]

# Load binary: for each doc: [a f32×N] [b f32×N]
raw = np.fromfile(RESULTS/"block3_states.bin", dtype=np.float32)
raw = raw.reshape(n, 2, N)
a = raw[:, 0, :]  # (n, N)
b = raw[:, 1, :]

print(f"Loaded {n} docs, a.shape={a.shape}, b.shape={b.shape}")
print(f"a stats: mean={a.mean():.4f} std={a.std():.4f} range=[{a.min():.3f},{a.max():.3f}]")
print(f"b stats: mean={b.mean():.4f} std={b.std():.4f} range=[{b.min():.3f},{b.max():.3f}]")

# Derived fields
amp = np.sqrt(a**2 + b**2)       # (n, N) amplitude
phase = np.arctan2(b, a)          # (n, N) phase in [-pi, pi]

# Representations for clustering
reps = {
    "raw_ab":       np.concatenate([a, b], axis=1),     # (n, 2N)
    "amplitude":    amp,                                 # (n, N)
    "phase_cos_sin": np.concatenate([np.cos(phase), np.sin(phase)], axis=1),  # (n, 2N) circular
}

# Mean-center and optionally normalize each rep for fair cosine-like clustering
rows = []
for name, X in reps.items():
    # Normalize each sample to unit L2 (so k-means on normalized ≈ spherical k-means ≈ cosine)
    Xn = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)
    print(f"\n--- representation: {name}, dim={Xn.shape[1]} ---")
    for k in range(2, 21):
        km = KMeans(n_clusters=k, n_init=10, random_state=20260412).fit(Xn)
        labels = km.labels_
        if len(set(labels)) < 2:
            sil = -1.0
        else:
            sil = silhouette_score(Xn, labels, metric="cosine")
        rows.append({"representation": name, "k": k, "silhouette": float(sil),
                     "inertia": float(km.inertia_)})
        print(f"  k={k:2d}  sil={sil:+.4f}  inertia={km.inertia_:.3f}")

# Save CSV
import csv
with open(RESULTS/"block3_cluster_k_search.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["representation", "k", "silhouette", "inertia"])
    w.writeheader(); [w.writerow(r) for r in rows]

# Best k per representation
best = {}
for name in reps:
    rs = [r for r in rows if r["representation"] == name]
    bk = max(rs, key=lambda r: r["silhouette"])
    best[name] = (bk["k"], bk["silhouette"])
    print(f"\nbest k for {name}: k*={bk['k']} sil={bk['silhouette']:.4f}")

# Visualization: PCA 2D per representation, with best-k labels
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, (name, X) in zip(axes, reps.items()):
    Xn = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)
    k_star = best[name][0]
    km = KMeans(n_clusters=k_star, n_init=10, random_state=20260412).fit(Xn)
    labels = km.labels_
    pca = PCA(n_components=2).fit(Xn)
    pts = pca.transform(Xn)
    for c in range(k_star):
        m = labels == c
        ax.scatter(pts[m, 0], pts[m, 1], s=30, label=f"basin {c}", alpha=0.7)
    ax.set_title(f"{name}  k*={k_star}  sil={best[name][1]:.3f}")
    ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
    ax.legend(fontsize=7, loc="best")
fig.suptitle("Block III: Effective Attractor Basins (NFCorpus 100 docs)", fontsize=13)
plt.tight_layout()
plt.savefig(RESULTS/"block3_basin_visualization.png", dpi=120)
print(f"\nSaved PCA visualization -> {RESULTS/'block3_basin_visualization.png'}")

# Summary MD
summary = f"""# Block III：Attractor 数量诊断

**方法**：100 NFCorpus docs，exp015 E 变体配置独立 evolve 5000 步，对 final ψ 状态做 3 种表征的 k-means + silhouette（k=2..20）。

## 表征 × 最优 k*

| 表征 | 维度 | k* | silhouette |
|---|---|---|---|
"""
for name in reps:
    X = reps[name]
    summary += f"| {name} | {X.shape[1]} | {best[name][0]} | {best[name][1]:.4f} |\n"

summary += f"""

## 判读（H2：矛盾主次质变假说）

**H2 成立条件**：有效 attractor 数 < 10

**结论**："""
k_values = [best[n][0] for n in reps]
median_k = int(np.median(k_values))
summary += f"三表征 k* = {k_values}（中位 {median_k}）。"
if median_k < 10:
    summary += "**H2 成立**：MaoField 的动力学 basin 容量 <10，当候选池 >20 时超过 basin 容量，矛盾主次结构发生质变，这解释了 top-20→top-100 的 nDCG 坍塌（exp016 发现的 +183% 退化）。"
elif median_k < 20:
    summary += f"H2 部分成立：basin 容量 {median_k} 介于 10-20 之间，候选池 >60 (3×{median_k}) 时发生坍塌。与 exp016 top-100 失败数据一致。"
else:
    summary += f"**H2 证伪**：basin 容量 ≥{median_k}，top-100 坍塌另有机制。"

summary += f"""

## 可视化
![basin_visualization](block3_basin_visualization.png)

PCA 2D 投影显示各表征下的 attractor basin 结构。

## 下一步含义
"""
if median_k < 10:
    summary += (f"- Block II（耦合 g 扫描）应该在 ≤{median_k*3} 的候选池上最有效\n"
                f"- Block IV 唯心组如果仍集中在 {median_k} 个 basin 内，可推论矛盾容量是 PDE 算子性质，不是源场性质\n"
                f"- 工程含义：MaoField reranker 的候选池上限 ~ 3·k* ≈ {median_k*3}")
else:
    summary += "- basin 容量看似较大，候选池瓶颈可能不是 attractor 数量。Block II/IV 需要重新考虑 H1/H3 的判读。"

(RESULTS/"block3_summary.md").write_text(summary)
print(f"\nWrote {RESULTS/'block3_summary.md'}")
