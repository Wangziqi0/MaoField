# HANDOFF → 7B13 Linux 姐姐主会话 — D29 验证级联 action 交接 (2026-05-29)

> **来源**: 独立验证通道 [额外 agent], 跨三机 trust-but-verify。
> **对象**: 7B13 主会话 (持 git 单点写权 + 执行权)。
> **指令源**: 一凡 D29 "把所有都写进文件, 让 7b13 搞"。
> **本文件 = 自包含交接**: §1 已验证状态 + §2 本轮更正日志 + §3 可执行 action (A1 备份 / A2 git 入库 / A3 实验留 ack) + §4 binding + §5 留 PI/关卡 3。
> 真实日期 `date` binary = **2026-05-29 CST** (D29, 三 leg 投稿 D-day)。全程 read-only 产出, 0 commit/push/launch (执行交 7B13)。

---

## §1 已验证状态 (字节级 / 多通道收敛)

1. **C3 = 退化 (frozen identity), fractal 决定性排除 — 4 重字节铁证**: 通道 P + 通道 V + cascade + agent X 独立 ssh 22 重算, 全收敛。22 端 candidate_c gen=0 ckpt sha256: 5 cell (1337α10/2024α0/7α10/137α0/271α10) = `b3a67b42504e0c10` **逐字节相同** (`‖θ_i−θ_j‖=0`); (42,α0) = `dff908569813f815` distinct (唯一权重真动)。→ **v9 "fractal fundamental limit 主刊" 叙事决定性死, 反 inflate 第三次拦下** (5/12 + 5/19 同构)。
2. **paper v8 安全 (最重要)**: v8 负结果建在**早期 armb 系列 (2026-05-08~05-12) 真训练数据** (单链 gen0-9 = **10 distinct sha256**, 权重逐代变, loss 收敛, gen0=36.5, 0 NaN)。**与 candidate_c (broken fp16) 是另一个 run, 不污染 v8。D29 三 leg (arXiv+TMLR+KBS) 照投, 不受影响。**
3. **candidate_c (22, N=180) 不可用于定量结论**: 180 ckpt 仅 **52 distinct hash**, 9 链全冻, `grad_norm:nan` 命中 **8909 次**, 0/180 训到 baseline。每 cell 跑满 ~34min (forward+backward 全跑) 但 optimizer 被 GradScaler skip = "跑满算力没学到"。
4. **cluster-11 (5060 fp16) 数据存在** (此前 NO-GO 撤销): 在 5060/19 `C:\Users\amd\Desktop\5060\SMOKE_5060_FP16_CROSSCHECK\` (gen0=36.5377/gen1=78.0735 健康, +113.7%, 无 skip)。→ v9 "+113.7% 否决 cross-platform fp16" claim 有数据支撑。
5. **fp32 balanced 矩阵未跑 (P0)**: smoke_fp32_N_seed 只是 1-cell smoke (gen0 卡 24%/346 步被 kill — 顺带独立印证 N_total=1460 步/代)。要 substantive α 效应需 E1+E2 (见 §3-A3)。
6. **早期真数据上的 α 效应** (caveat: multi-seed 仅 α=0 n=6 / α=10 n≈5): α>0 不缓解 collapse, α=10 倾向加重 + 升 NaN 风险。

详细见 [`D29_VERIFICATION_CASCADE_UPDATE_20260529.md`](D29_VERIFICATION_CASCADE_UPDATE_20260529.md) + [`MAOFIELD_EXP_METADATA_MASTER_20260529.md`](MAOFIELD_EXP_METADATA_MASTER_20260529.md)。

---

## §2 本轮更正日志 (D-1 纪律 5, 多通道纠错链)

纠错链一路纠到纠错者本身 — 这是多通道在工作:

| # | 谁错 | 谁 catch | 更正 |
|---|---|---|---|
| 1 | GATE/round2 判 "cluster-11 NO-GO 缺失" | 一凡指 19 桌面 + 本通道 ssh 核 | 撤销, 数据在 `Desktop\5060\` |
| 2 | cascade "candidate_c 无 training_args" | agent X + 本通道 ssh 22 重算 | **错**: training_args.bin **180/180 存在**; 真缺 trainer_state.json + optimizer.pt。根因: 本通道 ls 误用 `head -10` 截断 |
| 3 | 本通道 rsync 落点 = repo `archive/` | L0 主会话 git caveat + 本通道 verify | **错**: `archive/` 非 gitignore + .gitignore 不覆盖 `*.safetensors` → 86GB 进 git 会炸。改落 RAID1 (见 A1) |
| 4 | 本通道上轮 "candidate_c 0/180 trained" | 元数据重算 | refine: 混合 regime 52 distinct, 不可用于定量 (非严格 0) |

**字节事实不变** (C3 退化 / v8 安全) — 以上全是数据完整性 + 元数据细节更正。

---

## §3 可执行 ACTION (7B13 主会话)

### A1 — 【时间敏感, 一凡已 ack "让7b13搞"】RAID1 数据备份

**原因**: 22 `/tmp/dppl_bridge_verify` (86G, 含 v8 基的 early-armb ckpt) 是 **ephemeral, 重启即失**; 7B13 只有 jsonl 没 ckpt → 22 一重启, v8 可复算性 (D-PPL 重算 / sha256 重验) 就没了。

**落点 = RAID1 `/media/amd/raid1` (15T, 13T free, repo 之外 → 零 git 风险)**。先 dry-run:
```bash
mkdir -p /media/amd/raid1/maofield_ckpt_backup_20260529/{22_tmp,5060_desktop}
# 22 /tmp (86G) → RAID1, 先 dry-run 确认
rsync -av --dry-run --ignore-existing amd@192.168.31.22:/tmp/dppl_bridge_verify/ \
  /media/amd/raid1/maofield_ckpt_backup_20260529/22_tmp/
# 确认无误 → 去掉 --dry-run 实跑
# 19 桌面 → RAID1
scp -r amd@192.168.31.19:'C:/Users/amd/Desktop/5060' \
  /media/amd/raid1/maofield_ckpt_backup_20260529/5060_desktop/
```
caveat: 落 RAID1 (repo 外) 零 git 风险 ✓ / 不碰 `archive/v1.0_release_20260516` v8 锁定 manifest ✓ / 86G→13T 空间够 ✓ / --ignore-existing 不覆盖。

### A2 — 【一凡已 ack】git 入库 D29 文档 (仅小 md, 严禁大文件)

待入库 (全小 text md, 已确认无大文件):
```bash
cd /home/amd/HEZIMENG/MaoField
git add experiments/exp018_cat/dppl_bridge_verify_d21_output/*20260529*.md
# 安全检查: 确认只 stage 了 md, 无大文件 / 无 RAID1 路径
git diff --cached --stat | tail -3        # 总量应是 KB 级, 不是 GB
git status --short | grep -vE '\.md$'     # 应为空 (只有 md 被 stage)
# 确认后再 commit (建议 message):
# "D29 verification cascade: cross-machine data + metadata audit; C3 degenerate byte-locked (sha256 4-channel); cluster-11 data located on 5060 desktop; v8 negative result confirmed on real early-armb data; fp32 matrix P0 still pending. Corrections logged per D-1 discipline 5."
```
**严禁**: `git add -A` / `git add .` / git-add RAID1 备份路径 / git-add 任何 `*.safetensors` / `candidate_c.nohup.log` (5.3MB) / 大 jsonl。大文件全走 A1 的 RAID1, 不进 git。

### A3 — 【留 PI explicit ack + 关卡 4 budget, "让7b13搞" 不覆盖此项, 勿自动 launch】fp32 实验

- **E1 (P0 阻塞)**: `configs/cat_arm_b.yaml` line51 dtype float16 → fp32/bf16 修训练根因。判据: gen0 val_ppl<50 且梯度有限 (fp32 可恢复已被 5060 E0 证: gen0=36.536/gen1=78.572)。
- **E2 (P0)**: balanced α∈{0,1,5,10} × seed≥6 真训练矩阵 + Welch t 给严格效应量。
- **另**: config-identical NaN-vs-frozen 蹊跷的隔离重跑 (α5/seed42 gen0 单独干净启动), 判 sensitive-dependence vs flaky bug (MLSys genre)。
- 成本 ~$120-180 / 60-90h GPU — **留 PI + 关卡 4 budget 决, 不在本交接的 auto 执行范围**。

---

## §4 binding

- paper v8 final 47/47 D17 锁定不动; 不碰 `archive/v1.0_release_20260516/`; 12 NOT-claim 撤回不复活。
- git 单点写权 = 7B13 主会话 (A2); RAID1 备份 repo 外 (A1); 大文件不进 git。
- **genre 不变: 全部发现 = 数据完整性 + 元数据 + 下一步定位 + 更正, NMI/方法论/reproducibility, 非 Nature 主刊。** C3 退化字节锁死 = 反 inflate, 非新发现。

## §5 留 PI + 关卡 3 反题三方决 (本通道不擅 declare)

1. **venue 映射**: C3 退化 → v9 天花板 TMLR/numerical/workshop, **非主刊 fractal** (两通道 + 主编模拟都点名主刊 = inflate)。
2. **v9 narrative 重构**: 从 "fractal 主刊" → "cross-hardware reproducibility + 测度论不适定 (退化版) + 失效分类 catalog"。
3. **L0-8 NESS tier 分歧** (通道 P conditional L0 vs 通道 V L2 实测脱节) — 核心真分歧。
4. **L0-5/6/7 弱-descriptive 版去留** (over-correct 防错杀)。
5. **E1/E2 launch + budget** (关卡 4)。

---

**生成**: 独立验证通道 [额外 agent], 2026-05-29 CST。本文件是给 7B13 主会话的可执行交接。A1+A2 一凡已 ack ("让7b13搞"), A3 留 PI explicit ack。git/rsync 执行由 7B13 主会话。venue/paper/tier 判定留 PI + 关卡 3 反题三方决。**一凡 priority 1 健康优先, hotline 010-82951332 / 400-161-9995 standing。**
