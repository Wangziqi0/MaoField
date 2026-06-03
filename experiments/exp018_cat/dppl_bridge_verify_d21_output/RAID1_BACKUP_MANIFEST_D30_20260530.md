# RAID1 备份清单 — 22 端 dppl_bridge_verify ckpt 抢救 (留 7B13 主会话执行)

> **署名**: [额外 agent] (来自 Win 端, 现 Linux 7B13 secondary session, 严格 read-only 清点通道)。
> **对象**: 7B13 Linux 姐姐主会话 (持 git 单点写权 + ssh/rsync 执行权)。
> **指令源**: 一凡 dispatch — "在数据丢失之前守住 paper v8 负结果所依赖的底层 ckpt"。
> **本文件 = read-only 准备好的执行计划**, 不是已执行的备份。本通道全程 0 写 / 0 删 / 0 rsync 实跑 / 0 git。
>
> **⚠️ 文件头日期 binary 自检 (D-1 纪律 5 sub-rule)**: dispatch 要求文件名 `_D30_20260530` + D30 署名。但本通道 `date` binary 实测 (7B13 currentDate + 22 端 SSH) = **2026-05-31 CST**, 即真实日期 **D31**, 非 D30。按 dispatch 保留 D30 文件名, 但 honest disclose 实测 D31, 不静默用错日期 (反 5/16 forward-dated 教训)。

---

## ⛔ 0. 最重要结论 (binary, 颠覆 dispatch 前提)

**dispatch 前提 = "ckpt 还躺在 22 的 `/tmp/dppl_bridge_verify/` (ephemeral, 一重启就没), 趁早备份。"**

**实测第一手 binary 事实: 该目录在 22 上不存在。**

```
$ ssh amd@192.168.31.22 'ls -ld /tmp/dppl_bridge_verify/'
ls: 无法访问 '/tmp/dppl_bridge_verify/': 没有那个文件或目录
```

→ **dispatch 设想的"备份哪些 ckpt 目录"清单无法给出 —— 目标路径已不存在。**
→ paper v8 的 "从 ckpt 重验 sha256 / 重算 D-PPL" 这条复现路径, 在 22 的这个路径上已经不可用 (后果留 PI + 关卡 3, 见 §4)。

**⚠️ 本文件 scope 诚实声明 (D-1 纪律 1, 不编造)**: 本通道在确认上述 binary 事实后, 准备做更深的 read-only forensics (整盘 `find` safetensors / `du` / `bash_history` 还原删除时间线 / 其他路径是否有副本), 但 **本机 Bash 工具中途陷入 stall, 这批深度扫描的输出未能可靠取回**。因此本文件**只 commit 已 100% 取回的第一手事实** (§1 机器身份 + §2 目标目录不存在), 其余标 `[未完成-需 7B13 续查]`, **绝不**写未经实证返回的数字 / 文件大小 / 删除记录。这是 D-1 纪律 1 占位符禁令 + 纪律 5 不静默的要求。

---

## §1 机器身份 binary 核实 (已取回)

| 项 | dispatch / 文档说法 | 实测 (ssh read-only, 已取回) | 判定 |
|---|---|---|---|
| 192.168.31.22 host | 9070XT GPU 节点 | hostname = `amd-ONDA-B650M-W` | — |
| IP | 192.168.31.22 | `hostname -I` 含 192.168.31.22 (+ docker 172.17/172.18/198.18 bridge) | ✓ |
| GPU[0] | RX 9070XT | `rocm-smi`: **AMD Radeon RX 9070 XT**, SKU `G295BP00`, GFX `gfx1201` | ✓ 与文档一致 |
| GPU[1] | — | `Raphael` 核显 (CPU iGPU), 非独显 | (附带信息) |

机器身份与三机架构文档一致 (22 = 9070XT GPU 节点)。✓

---

## §2 `/tmp/dppl_bridge_verify/` 不存在 (已取回, binary)

- `ls -ld /tmp/dppl_bridge_verify/` → **没有那个文件或目录** (见 §0 verbatim)。

这是本次清点的核心 binary 事实, 已可靠取回。**dispatch 要备份的目标在该路径上不存在。**

---

## §3 [未完成 — 需 7B13 续查] 深度 read-only forensics

以下问题本通道**未能取回可靠输出** (Bash stall), 全部移交 7B13 主会话用 read-only 命令补查。**不要**信任任何本文件之外、声称是本通道给出的这些数字 —— 本通道没 commit 任何未实证返回的具体值。

7B13 主会话建议跑 (全 read-only):

```bash
# (a) 整盘是否还有任何 ckpt / safetensors (确认是否真的全没了, 还是挪到别处)
ssh amd@192.168.31.22 'find / -maxdepth 7 -name "*.safetensors" 2>/dev/null | head; \
  find /home /tmp /data /mnt /media /opt /var -maxdepth 6 \
    \( -iname "*dppl*" -o -iname "*bridge_verify*" -o -iname "*candidate_c*" \
       -o -iname "*armb*" -o -name "*.safetensors" -o -name "pytorch_model*" \) 2>/dev/null'

# (b) 目录是被 rm 删的, 还是 /tmp 被重启清掉的? (还原时间线 + 删前有没有备份动作)
ssh amd@192.168.31.22 'uptime -s; cat -n ~/.bash_history 2>/dev/null | \
  grep -nE "dppl|bridge_verify|rm -rf|rsync|scp |raid|backup|cp -r|tar "'

# (c) 还剩什么 maofield 相关数据 (jsonl / log 等非 ckpt)
ssh amd@192.168.31.22 'du -sh ~/maofield_* 2>/dev/null; \
  find ~/maofield_* -maxdepth 6 -type f \
    \( -name "*.jsonl" -o -name "*.log" \) -printf "%s\t%p\n" 2>/dev/null | sort -rn | head -30'
```

**判据**:
- (a) 若全盘 0 个 safetensors → ckpt 确实已丢, 22 无法做 sha256/D-PPL 重验 → 触发 §4。
- (b) 若 history 见 `rm -rf` 且其前无 rsync/scp/backup → 是手动删且删前无备份 (最坏情况); 若是 `/tmp` 重启清掉 → dispatch 的 ephemeral 担心成真。两者后果都指向 §4。
- (c) 若只剩 jsonl + log (无权重) → 这些是 partial 文本佐证, 见下方"还能抢救什么"。

---

## §4 给 7B13 主会话的实际可执行项 (改写后的"备份清单")

dispatch 要的"备份 v8-basis early-armb ckpt 到 RAID1": **目标路径已不存在, 该 action 无法按原样执行**。退而求其次:

### A. 【先确认 §3, 再决定】若 §3(c) 发现还剩 jsonl / log → 抢救到 RAID1

落点 = RAID1 repo 外 (零 git 风险, 不碰 `archive/v1.0_release_*` v8 锁定 manifest)。**模板, 先 dry-run** (具体源路径以 §3(c) 实查结果为准):

```bash
mkdir -p /media/amd/raid1/maofield_ckpt_backup_20260530/22_residual_NO_CKPT
# 以 §3(c) 查到的真实残留路径替换 <SRC>, 先 dry-run
rsync -av --dry-run amd@192.168.31.22:<SRC>/ \
  /media/amd/raid1/maofield_ckpt_backup_20260530/22_residual_NO_CKPT/
# 核对传输清单 (应只有 log/jsonl, 无 *.safetensors) → 去掉 --dry-run 实跑
```

**注意**: 目录命名特意带 `_NO_CKPT`, 以免日后误以为里面有权重。log/jsonl **不能**替代 ckpt 做 sha256 / D-PPL 重验, 只是 partial 文本级佐证。

### B. 【必须升级到 PI + 关卡 3】v8 ckpt 复现路径的后果评估 (超本通道判定权)

这是本次清点最该上报的一条:

- **已确认事实**: dispatch + D29 handoff §1.2 把 early-armb (2026-05-08~05-12) 真训练 ckpt 当作 v8 可复算性的物质基础。**这批 ckpt 所在的 22 `/tmp/dppl_bridge_verify/` 路径已不存在。** (是否全盘还有副本 → 待 §3(a) 确认)。
- **后果 (留 PI + 关卡 3 反题三方决, 本通道严格不 declare)**:
  1. 若投稿后被要求 "提供 ckpt 重验 sha256 / 重算 D-PPL", 22 这条路 (在该路径) 已不可行。
  2. D29 handoff §1.2 "v8 建在真训练数据、可字节级复算" 的表述, 在 ckpt 已不在该路径的前提下, 是否需要在 paper / data-availability statement 如实标注 (例: "raw checkpoints not retained at original path; training logs + jsonl traces available") —— **paper-level / venue-level 判定, 本通道不擅。**
  3. 是否需从别处 (19 桌面 `Desktop\5060\`? 一凡 / 9070XT 实操者别处副本?) 找回 early-armb 主链 ckpt → 留 PI 核实。D29 §2 提到 19 桌面有一批 5060 数据, 但那是 fp16/fp32 smoke + E0, `[?]` 是否含 early-armb **主链** ckpt 需 PI 确认。

---

## §5 binding 严守 (本通道全程遵守)

- ✅ **全程 READ-ONLY**: 22 上只跑 `ls` / `rocm-smi` / `hostname` 等只读命令, **0 写 / 0 改 / 0 删 / 0 rsync 实跑 / 0 launch / 0 实验**。深度 forensics 因工具 stall 未完成 (非因写操作)。
- ✅ **未碰** repo `archive/` 或 `v1.0_release_20260516` v8 锁定 manifest。
- ✅ **未 git add/commit/push** (git 单点写权 = 7B13 主会话)。
- ✅ 唯一写操作 = 本 md 一个文件 (落 dispatch 指定路径)。
- ✅ **不编造**: §3 未取回的数据明确标 `[未完成-需 7B13 续查]`, 不写任何未实证返回的具体值 (D-1 纪律 1)。
- ✅ paper v8 final 47/47 D17 锁定**不动**; 12 NOT-claim 撤回**不复活**; venue/paper/tier/reproducibility 后果判定**全留 PI + 关卡 3 反题三方决**。
- ⚠️ 日期 honest disclose: 文件名 D30 (按 dispatch), 实测真实日期 D31。

---

## §6 一句话给 7B13 + PI

**已确认 (binary)**: 22 = 9070XT 节点身份对; 但 dispatch 要守的 `/tmp/dppl_bridge_verify/` 在 22 上**已不存在**, 这条 ckpt 复现路径在该路径上断了。
**未确认 (工具 stall, 需 7B13 续查 §3)**: 整盘是否还有 safetensors 副本 / 目录是被 `rm` 删还是重启清掉 / 删前有无备份 / 还剩哪些 jsonl·log。
**最该决的 (留 PI + 关卡 3)**: paper v8 "建在真训练 ckpt + 可字节级复算" 的物质基础在 22 该路径已不在 —— 是否需在 paper / data-availability 如实标注, 或从别处找回。(D-1 纪律 1 + 5: 不静默, 如实 surface。)

---

**生成**: [额外 agent] read-only 清点通道, 真实日期 2026-05-31 (文件名 stamp D30 按 dispatch)。本文件只 commit 已可靠取回的第一手事实, 未取回部分标 `[未完成-需 7B13 续查]`。rsync/git 执行由 7B13 主会话; reproducibility/paper/venue 后果判定留 PI + 关卡 3 反题三方决。一凡 priority 1 健康优先, hotline 010-82951332 / 400-161-9995 standing。

---

## ⊕ APPENDIX · 2026-06-03 D34 更正 (append-only, 原记录不动)

> **署名**: 子协作者 (Linux 主会话 36 派遣)。**本段只追加, 上方 §0–§6 原记录一字不改** (D-1 纪律 5: 浮现不静默修正, 差异留痕)。
> **性质**: 对本文件 §0 / §2 / §4 / §6 「`/tmp/dppl_bridge_verify/` ckpt 断路/丢失 → v8 ckpt 复现路径断了」这一**前提**的**实证更正**。

### 1. 更正结论 (binary)

D30/D31 本文件基于 22 上 `/tmp/dppl_bridge_verify/`（ephemeral 路径）已不存在, 推断 paper v8 主链 ckpt 复现路径"断了"。**该推断的前提路径确已不存在, 但结论被后续实证推翻**:

**paper v8 主链 ckpt 未丢。** D34 前完整存活在 22 的**持久**路径
`~/HEZIMENG/MaoField_static_backup_20260520/.../checkpoints_armb`（**111 ckpt**），
而非已被清掉的 `/tmp/` ephemeral 路径。即: 当初看的是错的（临时）路径, 真权重一直在静态备份里。

### 2. 实证证据 (sha256 二通道, 已取回)

- **132/132 ckpt sha256 ≡ `canonical/projects/MaoField`**（D34 主会话 + migrate-22 二通道验证）。
- 本子协作者**独立复核**抢救暂存区 `/media/amd/raid1/from_22/_VERIFICATION/` 内两份 sha 清单:
  - `22_static_backup_132ckpt_sha256.txt`（22 静态备份, 132 行）
  - `canonical_132ckpt_sha256.txt`（canonical, 132 行）
  - `diff`（sha+path 双字段排序后）= **空 = 132/132 逐行 identical**。
  - 其中 `checkpoints_armb/` = **111**, 普通 `checkpoints/` = 11, 合计 132（与"111 ckpt"一致）。
- 该 22 静态备份副本**验证后已删**, canonical 留权威（durable RAID1 [UU]）。

### 3. 对本文件原结论的影响

- §0「ckpt 复现路径在 22 该路径上断了」: **路径前提仍成立**（`/tmp/...` 确不在）, **但"v8 ckpt 丢失/不可复算"的引申不成立** —— 权重在静态备份完整, 且字节级 ≡ canonical。
- §4.B / §6「v8 建在真训练 ckpt + 可字节级复算的物质基础在 22 已不在」: **被推翻**。物质基础在 canonical + （D34 前）22 静态备份**完整存在且 sha 一致**, 可字节级复算路径**未断**。

### 4. 边界 (本子协作者严守)

- **不下 paper 结论 / 不下 venue / reproducibility / tier 判定** —— 全留 PI + 关卡 3 反题三方决。
- 本段仅校正"ckpt 是否物理存活 + sha 是否一致"这一**可二值实证的事实层**, 不触碰 paper v8 战略判定。
- paper v8 final 47/47 + D17 锁定**不动**; 12 NOT-claim 撤回**不复活**。
- 0 删 canonical ckpt; 本次唯一写 = 本 append 段。git 执行留 Linux 主会话（单点写权 36）。

**一句话**: 当初判"丢"看的是 ephemeral `/tmp` 路径; 真权重在静态备份, 132/132 sha ≡ canonical, **未丢、可复算**。事实层更正于此, paper 级后果留 PI / 关卡 3。
