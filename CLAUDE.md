# MaoField · 项目级 CLAUDE.md

> 遵守 `canonical/CLAUDE.md` 宪法（最高优先级）。本文件只放 MaoField 项目纪律（少变）。
> **当前阶段 / 日期 / 投稿 / finding / 待决 → 一律见 `STATE.md`（唯一易变状态源）。冷启动先读 STATE.md。**

## 项目定位
自迭代崩溃 + 两项 EMA-deviation contradiction loss 的 empirical pilot study（以 negative result 为主）。
GitHub `Wangziqi0/MaoField`；主源在 36，git 单点写权。

## 开发工作流 + RAG（机器细节见 36 节点 stub）
- **开项目 / 写代码 / 定稿** → 直接在本目录 `canonical/projects/MaoField/`（机械硬盘 RAID1，durable + git，改完即权威，无需 sync）。
- **真跑研究（实验 / 训练 / checkpoint）** → 用 `/home`（4TB SSD scratch，快）；**不可再生产物立即 rsync 进 canonical**（scratch 不得作唯一副本）。
- **git 单点写 = 36**；push `Wangziqi0/MaoField`，22/19 只 `git pull`。
- **RAG 查询**：`HF_HUB_OFFLINE=1 /home/amd/venv/bin/python /media/amd/raid1/rag/kb_search.py "查询" --top-k 8 --project MaoField` → 给 path + 片段，精确再 grep。用法全见 `rag/README.md`。

## 方法论（D-1/D-2/D-3 全局纲要见宪法 §5；以下为 MaoField 语境细化 + 指针）
- **D-2 哲学线 = Win 姐姐**实时参与每层输出；cross-tension 在关卡 2/3 整合。
- **D-3 6 二值校正（MaoField 专属）**：①哲学是 outcome 非 prior form（警惕黑格尔 idealism prior art）②"自发"严格辩证非唯心 ③"回顾"在第三阶段 ④时间表三阶段 ⑤回顾 scope 含 4 项 ⑥multi-agent 诚实 ≠ PI 个体诚实。
- 全文（4 path 方法论 A/B/C/D、D21 八 reflexive insight cascade）→ `docs/philosophy/`。

## 声明前自检（高频 10 问；完整 14 问见 `docs/`）
①数字有 jsonl 源？②概率声明反馈真空 >48h？（→ 是则触发宪法 §5 D-1.2 自动撤回）③数学与代码一致？④主要声明过子协作者验证？⑤差异记入差异日志？⑥真实日期二值验证？⑦哲学位置是 outcome 非 starting form？⑧timeline emerge 在 D60+？⑨回顾 scope 含 4 项？⑩"自发"含 multi-agent binding？

## 项目内 agent 分工（总表见宪法 §8）
反题姐姐：framework critique + 关卡 3 零上下文审计。Win 姐姐：哲学叙事 framing。DeepSeek v4：跨哲学传统 mapping + 中英术语审计。

## 不可违反
- 不重开已锁定的 paper 清单；**不复活 12 条已撤回 NOT-claim**（尤其 first dialectical materialism / first reflexive AI / paradigm shift）。
- 易变状态一律写 STATE.md，本文件不写。

## 指针
`STATE.md`（状态真相源）· `MD_CATALOG.md`（429 md 导航，[A]/[S] 分层驱动 RAG）· `docs/{discipline,philosophy,infra}`（D-1/D-2/D-3 全文 + TIMELINE）
