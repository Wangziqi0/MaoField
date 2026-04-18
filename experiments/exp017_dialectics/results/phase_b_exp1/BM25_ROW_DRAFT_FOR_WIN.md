# BM25 对比行草稿 — Linux 给 Win 审修辞

**写于**: 2026-04-15 晚, Linux 姐姐
**触发**: 反题姐姐路径 1 独立 verify 完全成立
**scope**: 只给草稿候选，**不 commit 到 arxiv_v1_full.md**。Win 睡醒定修辞 + 一凡批战略
**紧急度**: P0 for Zenodo 4/20 release（不改的话 4/20 发出去被公开 spot 概率高）

---

## 事实摘要

Table 4.1 实算 5/5 数据集 BM25 胜 MaoField_E：

| Dataset | BM25 | MaoField_E | Δ |
|---|---:|---:|---:|
| NFCorpus | 0.3063 | 0.2026 | **−10.4 pp** |
| SciFact | 0.6594 | 0.3002 | **−35.9 pp** |
| FiQA | 0.2167 | 0.1082 | **−10.9 pp** |
| ArguAna | 0.2838 | 0.1514 | **−13.2 pp** |
| TREC-COVID | 0.5589 | 0.4932 | **−6.6 pp** |

此外 §4.1 line 575 明确："Candidate pool: BM25 top-K, K ∈ {6, 20, 100}" → MaoField_E 是 BM25 top-K reranker，rerank 完 **恶化** BM25 原排序。

当前 §4.2 Observations 4 条 + Status 段**未显式呈现此事实**。这是反题姐姐的核心 claim。

---

## 草稿 1：§4.2 Observations 新增一条（Linux 倾向方案）

在现有 Obs 4 之后，新增 Obs 5：

> 5. **MaoField_E vs BM25 (standard sparse reference)**: MaoField_E operates as a reranker on BM25 top-K candidates (§4.1). On 5/5 datasets, the reranked output underperforms the original BM25 ranking: NFCorpus `−10.4`, SciFact `−35.9`, FiQA `−10.9`, ArguAna `−13.2`, TREC-COVID `−6.6` pp. Within this operating regime MaoField_E cannot be recommended as a retrieval method; its empirical utility, reported throughout §4, lies in the structural-diagnostic dimension (§4.4–§4.10) rather than in retrieval performance.

---

## 草稿 2：§4.2 Status 段改写

**现在**：
> **Status**: MaoField_E represents a working PDE-based reranker, significantly above naïve byte baselines and below SOTA. This establishes the empirical envelope within which subsequent Block analyses operate.

**候选改法**：
> **Status**: Within the BM25 top-K operating regime, MaoField_E does not outperform BM25 itself as a retrieval reranker. The empirical envelope established by §4.2 is therefore: **above naïve byte n-gram baselines, below the standard sparse reference (BM25), and below SOTA cross-encoders (BGE-reranker-v2-m3)**. The framework's contribution reported throughout the remainder of §4 is not retrieval performance but the structural-diagnostic apparatus built on this envelope (§4.4 attractor enumeration, §4.6 source-density decomposition, §4.8–§4.10 Langevin / Kramers analysis of OP2).

---

## 草稿 3：Abstract 第四段修改候选

**现在（line 22）**：
> On five BEIR retrieval benchmarks, the framework improves over a byte-level lexical baseline by **+14.7% to +172.3%** while lagging SOTA cross-encoders by 10.8–32.2 pp.

**候选 A（最诚实，可能偏削弱）**：
> On five BEIR retrieval benchmarks, the framework's reranker form (MaoField_E) operates on BM25 top-K candidates, exceeding a byte-level lexical baseline by +14.7% to +172.3% but underperforming both BM25 itself (by 6.6–35.9 pp) and SOTA cross-encoders (by 10.8–32.2 pp). Retrieval is used as a tractable empirical domain; the paper's claim is structural interpretability, not SOTA performance.

**候选 B（节奏更平）**：
> On five BEIR retrieval benchmarks, MaoField_E exceeds a byte-level lexical baseline by +14.7% to +172.3%, while operating below the standard sparse reference (BM25, −6.6 to −35.9 pp) and below SOTA cross-encoders (−10.8 to −32.2 pp). The empirical claim is not retrieval performance; retrieval is the tractable testbed for the structural-diagnostic apparatus developed in §4.4–§4.10.

**Linux 建议**：候选 A 或 B 皆可，两者都比现状诚实。Win 选修辞节奏。

---

## 不动的东西（Linux 纪律）

- **§1.5 Contribution 5 不改**: 这是 Win 修辞领地；如果改 Abstract 和 §4.2 已足够覆盖，Contribution 5 可不动。若 Win 觉得需要对齐，由 Win 改
- **§1.7 / §6.1 / §6.4 等修辞段**: 全部归 Win
- **§2.3 范畴论 tag / §5 falsification pre-registration**: 路径 3 / 路径 4 的 action，分开处理，今晚不动

---

## 一凡决定清单

| 选项 | 动作 | 修辞风险 |
|---|---|---|
| **1. 全采纳草稿 1+2+3A** | Abstract + Obs + Status 全改 | 最诚实，但 abstract 开头第四段变得 defensive |
| **2. 采纳草稿 1+2 (不改 abstract)** | Obs + Status 改，Abstract 不动 | 中度诚实；快读 abstract 者仍可能被 spot，但 table + §4.2 一致 |
| **3. 只采纳草稿 1 (最小改动)** | 只加 Obs 5 | 满足"Table 里都有"的最低诚实度；修辞工程 charge 仍成立 |
| **4. 全暂停，Win 睡醒后定** | Linux standby | 最保守 |

**Linux 倾向**: 选项 2（改 Obs + Status，abstract 留给 Win 决定）。理由：Table 下方的 Observations 和 Status 是 **技术正文**，Linux 改合规；abstract 是修辞第一窗口，归 Win。

**但这是一凡 + Win 的战略决定。我草稿止于此，不 commit。**

🌙
