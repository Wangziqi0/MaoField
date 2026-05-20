# 代码体系封存 v1.0 release 总结 (2026-05-19)

子协作者: opus 4.7 (代码 release)
任务来源: 5/19 一凡 + DS 指令, Linux 姐姐数学层派遣
完成时间: 2026-05-19 burst session 内 (~90 min)

---

## 1. 归档路径

```
/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/archive/v1.0_release_20260519/
├── README.md                    # 英文 paper-grade README (10 章)
├── RELEASE_NOTES.md             # v1.0 内容 + v1.1/v2.0/v3.0/v4.0 roadmap
├── manifest.sha256              # 47 file SHA-256 全 checksum
├── chain_logs/                  # 19 file
├── configs/                     # 8 yaml (v1.0 release config + 7 historical)
├── src/                         # 9 py (snapshot from 22 主机)
└── scripts/                     # 9 file (chain runner + verdict + utility)
```

总大小: **496 KB** (含 47 files, manifest 行数 = 47 file)

---

## 2. 代码清理 binary 决策

**决策: 最小侵入式清理 + 单独追加 v1.0 release config**

理由 (纪律 5: 不静默修正,记录差异):
- 22 主机原 src/configs 不动 (保 historical truth)
- archive 内的 src/configs 是 5/19 snapshot (复制不改)
- 单独**新增** `configs/cat_arm_b_v1_0_release_20260519.yaml`,做 m_eff = 0.300 alignment
- 在新 config header **explicit disclose** chain 5/10-5/12 实际跑 m_eff = 1.0 fallthrough,paper 用 0.300 post-hoc N=4 fit

**不做的事** (binding):
- 不重命名变量 (会污染 historical chain log 对照能力)
- 不删 deprecated comment (5/9 ROLLBACK / 5/10 dialectical upgrade 注释全保留, 是 dev trace)
- 不改 framework 数学 form (binding 5)
- 不偏袒 PI 重写为 "看起来 clean" 的版本 (binding 6: 规则 5)

---

## 3. configs align m_eff = 0.300 binary 决策

**选项 A 选定**: 单独新写 v1.0 release config, 不动 historical configs.

**Honest disclose 写入** `cat_arm_b_v1_0_release_20260519.yaml` header:

```
HONEST DISCLOSE — chain historical vs v1.0 release alignment
The chain runs that produced logs/armb_alpha{0,10}_seed{0..4}_*.jsonl
(5/10-5/12) used cat_arm_b.yaml, in which the YAML omits the `m_eff` key.
In that case CATConfig at train_one_generation.py:54 falls through to its
dataclass default `m_eff: 1.0`. Therefore the Volterra kernel
    χ(k) = exp(-m_eff · k)
in the metric-only accumulator decays with m_eff = 1.0 in those logs.
...
v1.0 release alignment (this file) writes the post-hoc fit m_eff = 0.300
into the YAML explicitly so that:
  1. Re-runs starting 5/19 propagate the m_eff = 0.300 value through
     lambda_i, beta_kl, beta_model and the χ kernel.
  2. The paper's "m_eff = 0.300" claim has a corresponding YAML on disk.
  3. Historical chain logs retain their original m_eff = 1.0 semantics.
```

**v1.0 release config 的 derived 数值** (m_eff = 0.300 propagation):
- λ_1 = 1 / (2 m_eff) = **1.6667** (kinetic / velocity)
- λ_2 = m_eff / 2     = **0.1500** (mass / memory)
- λ_3 = m_eff         = **0.3000** (T_2 outer, option-β)
- β_kl    = exp(-m_eff)            = **0.7408**
- β_model = exp(-m_eff / 1406)     = **0.999787**
- T_2_form = "quadratic" (5/10 dialectical)
- kl_history_K = 9 (metric only)
- alpha_scan = [0.0, 1.0, 5.0, 10.0, 20.0]
- seeds = [0, 1, 2, 3, 4] (paper convention)

**保留的 fallback configs** (configs/):
- `cat_arm_b.yaml` — chain 5/10-5/12 用 (m_eff fallthrough 1.0)
- `cat_arm_b_v2_dialectical.yaml` — 5/9 single-seed fit (m_eff = 0.212)
- `shumailov_baseline.yaml` — no-CAT strict-mirror
- `shumailov_lr5e-5.yaml` / `shumailov_official.yaml` — sensitivity
- `sensitivity_fp32_baseline.yaml` / `sensitivity_rep_penalty_2.yaml`

---

## 4. chain logs 归档完成度

**19 file**(全部 from 22 主机或 host22_backup_20260512 双源 cross-check):

α scan single-seed (seed = 42) 5/8-5/9:
- α = 0.0  (gen 0-9 完整)
- α = 1.0  (gen 0-9 完整)
- α = 5.0  (gen 0-9 完整)
- α = 10.0 (gen 0-9 完整)
- α = 50.0 (numerical break, 仅 run_start record)

Phase 1 multi-seed 5/10-5/12:
- α = 0.0,  seed 0/1/2/3/4 (5 file, 各 gen 0-9 完整)
- α = 10.0, seed 0/1/2/3/4 (5 file)
  - seed 0 仅 first gen (5/11 hang, ROCm bug Verdict B per memory)
  - seed 1/2/3/4 各 gen 0-9 完整 → Partial D4 5/5 PASS STRONG ROBUST

Chain master + audit (5/10-5/12 robust chain):
- `phase1_robust_20260510_125805.master.log`
- `phase1_robust_20260510_125805.audit.jsonl`
- `phase1_robust_outer_20260510_125805.out`

---

## 5. README 完成度 (英文 paper-grade)

10 章节全部 done:
1. What this is (loss form explicit + Klein-Gordon form-borrowing disclose)
2. Why (Shumailov 2024 + Borji 2024 cite)
3. Key empirical numbers (m_eff / J_S / F3 p / Partial D4 / α=10 plateau)
4. How to reproduce (env + single cell + full chain + jsonl structure)
5. Cross-references (paper v6/v7 + Appendix D/E + literature dir)
6. Caveats (6 条 explicit, 含 pilot scale / partial isomorphism /
   code-vs-paper drift / Volterra metric-only / F3 p=0.82 NOT
   significant / multi-seed N=4 below paper convention)
7. Not included (Phase 5 / multi-arch / RLHF / F-1 Phase 2)
8. License (MIT)
9. Citation (paper draft + Shumailov 2024)
10. Honest contact (16 岁独立研究者 + discipline binding)

---

## 6. manifest.sha256

47 个 file 全部 SHA-256 hash 写入, 用 `find . -type f ! -name manifest.sha256 -print0 | sort -z | xargs -0 sha256sum` 生成 (排序后稳定, reproducible)。

verify 方法: `cd archive/v1.0_release_20260519 && sha256sum -c manifest.sha256`

---

## 7. 严守规则自检 (CLAUDE.md 5 纪律)

- **纪律 1 不等实验数据不写声明**: README/RELEASE_NOTES 每个数字标 source
  (chain_logs/jsonl 文件名 + 行 / fit script 路径). m_eff = 0.300 来源
  multi-seed N=4 fit (5/13 script). m_eff = 0.212 单 seed=42 explicit
  标 single-seed.
- **纪律 2 概率声明 48h verify**: 本 release 不下接受概率声明. 仅写实验
  结构与已验证数字.
- **纪律 3 代码 form 优先 paper form**: chain 历史 m_eff = 1.0 fallthrough
  vs paper m_eff = 0.300 explicit 拆分,不让 paper form 覆盖代码 form 历史.
  v1.0 release config 新写 align,不 retro 改 historical configs.
- **纪律 4 子协作者第二认识通道**: 本子协作者 = 代码 release 通道 (与
  Linux 主会话 + DS + 一凡 + 反题姐姐 + 实验/数学/叙事各通道并列). 不替代
  其他通道.
- **纪律 5 surface 错误不静默**: chain ran m_eff = 1.0 fallthrough → paper
  写 m_eff = 0.300 这件事, 在 v1.0 release config header + README §6
  caveat 3 + RELEASE_NOTES §3 三处 explicit disclose, 不静默重写.

---

## 8. 严守 6 binding 自检 (任务 prompt)

1. 严格中文 (README 英文): ✓ 本总结全中文,README 英文 prose 服务 international audience.
2. 不护短不夸大,二元判定: ✓ F3 p=0.82 explicit 写 "NOT significant".
3. 标 [?] 不确定: ✓ 本 release 数字全有 source, 未 surface 不确定项.
4. 代码 form 优先 (纪律 3): ✓ m_eff alignment 不 retro 改历史.
5. 不改 framework 数学: ✓ 仅清理 + 注释 + 归档, 数学 form 0 改.
6. 不偏袒 PI (规则 5): ✓ 不删 deprecated comment, 不重写为 clean version
   掩盖 dev trace.

---

## 9. 路径返回 Linux 姐姐主会话

完成路径:
```
/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/archive/v1.0_release_20260519/
├── README.md                                              # 英文 paper-grade
├── RELEASE_NOTES.md                                       # v1.0 + roadmap
├── manifest.sha256                                        # 47 file checksum
├── chain_logs/   (19 file)                                # 全 jsonl + master/audit
├── configs/      (8 yaml, 含 v1.0 release config + 7 historical)
├── scripts/      (9 file: chain runner + verdict + utility)
└── src/          (9 py: snapshot from 22 主机 5/9-5/10)
```

待 Linux 姐姐 + 一凡 review (5/19 burst 末段评审).
```
