# [9070XT Claude Desktop ack — D-PPL 桥 verify D21 prerequisites]

**真实今日日期** (D-1 纪律 5, `date '+%Y-%m-%d %H:%M:%S %Z'` binary print): `2026-05-21 11:34:50 CST` → D21 (D-day anchor 2026-05-01)

**Surface 时间**: 2026-05-21 11:45 CST

**来源**: 9070XT Claude Desktop (192.168.31.22, amd-ONDA-B650M-W), Remote Control session 由 Win 9955HX (192.168.31.19) 接管

**对象**: 7B13 主会话 Linux 姐姐 + 第十三波派遣 sub-agent A

**协议**: D-PPL 桥 verify D21 prompt §10 之 ack format (file rsync 通道, 非 conversation relay)

---

## §1 §2 prerequisites binary verify 结果

| 项 | 状态 | binary detail |
|---|---|---|
| §2.1 真实日期 | ✓ | `date` 输出 `2026-05-21 11:34:50 CST` = D21, 与 prompt 期望 match |
| §2.2 hostname | ✓ | `amd-ONDA-B650M-W` |
| §2.2 GPU | ✓ | `rocm-smi` Device 0 = RX 9070 XT 16 GB (idle low-power state, 14W power, SCLK 53MHz; Used VRAM% 84% 是 stale read 来自 llama-server 占用, §3.4 stop 之后 re-verify) |
| §2.2 / free | ✓ | `df -h /` → `/dev/nvme0n1p1` 1.9T 总 / 228G used / **1.6T free** (远超 install 6 GB 需求) |
| §2.3 checkpoint dir | ✓ | `.../alpha10.0/no_preserve_seed1/generation_5/` 存在 |
| §2.3 model.safetensors | ✓ | `500,979,600 bytes ≈ 477.8 MB` (期望 478 MB ✓ ballpark, mtime 2026-05-11 17:50) |
| §2.3 含 config.json + tokenizer.json + merges.txt + vocab.json + training_args.bin | ✓ | 全 ✓ |
| **§2.4 venv (.venv)** | **✗ 阻塞** | `.venv` 不存在; system `python3` (`/usr/bin/python3`) `import torch` / `import transformers` / `import datasets` 全 fail `ModuleNotFoundError` |

---

## §2 §2.4 阻塞之 冲突 instruction surface

按 D-1 binding §8.3 (不擅自决策性操作) + 9070XT CLAUDE.md "不擅自启动 GPU 长跑 (watchdog + checkpoint script ready + 一凡 confirm 后)" — install ~30 min + ~6 GB 是 决策性 操作, **9070XT Claude 不擅自 跑**。

### 冲突 detail (binary verbatim 引用)

**install_rocm_torch.sh head line 3-5** (sub-agent A 写之 install script 之 自身禁令):

```
# **重要**: 这个脚本 sub-agent **不主动跑**, 留给主 Linux 姐姐 + PI 一凡在场时决.
# 单次 install ~30min + 占 ~6GB 磁盘, 是 "决策性" 操作.
```

**D-PPL 桥 verify D21 prompt §2.4 line 80** (sub-agent A 写之 D-PPL prompt 之 同段, 推 sub-agent 跑):

```
若 不装 venv: `cd /home/amd/HEZIMENG/MaoField/experiments/exp018_cat && bash scripts/install_rocm_torch.sh` (per archive 之 install script)
```

**两者矛盾存活** — 同一 sub-agent A 之 install script head 禁令 vs D-PPL prompt 推 install。9070XT Claude **不擅自 决** 走哪条, surface 给 一凡 + 7B13 主会话 binary 决。

---

## §3 待 一凡 / 7B13 binary 决之 三选

| 选项 | binary action | trade-off |
|---|---|---|
| **A** | 9070XT 跑 `bash scripts/install_rocm_torch.sh` | ~30 min 阻塞 pilot, ~6 GB 占盘 (1.6 T free 富余), 解 §2.4 |
| **B** | 7B13 主会话 spawn debug sub-agent 改 D-PPL prompt clarify "install 是 sub-agent scope" + 重发 | 协议 binding 修正, ~hour 级延迟 |
| **C** | 7B13 端 venv (若已构建) rsync push 至 9070XT | ROCm wheel 与 driver / GPU arch (gfx1201) bind, 大概率 不直接 transferable (7B13 无 GPU + ROCm) |

**9070XT Claude 之 honest recommendation**: 选 **A** 之概率高 (B 之 protocol 修正与 实质 install 等价, C 之 binary 不可达 — 7B13 无 ROCm 不会有 9070XT 兼容 venv)。但 binary 决 仍 留 一凡 / 7B13。

---

## §4 file source binary trace (D-1 纪律 4 子协作者验证)

prompt 文件 (`DPPL_BRIDGE_9070XT_PROMPT_D21_20260521.md`) 之来源 binary verify:

- **没** 走 sshfs / NFS / ssh 直读 7B13 (`mount | grep 31.36` 空)
- 走 **git mirror**: 7B13 主仓 commit `69c4d2bc15ba7352b1c5b7539b1da4b9389b701d` "Add D-PPL 桥 verify D21 launch package (Sub-agent A)" 之 2026-05-21 11:31:40 → 9070XT git pull 同步 2026-05-21 11:31:45 (5 秒同步延迟)
- 9070XT 本地 working tree 之 副本与 7B13 原文 **同一 hash, binary 等价**
- `/home/amd/HEZIMENG/MaoField` 在 9070XT 是 本地 git clone (设备 `259,1` = `/dev/nvme0n1p1` 1.9T NVMe), 不是 sshfs mount
- git remote: `origin = amd@192.168.31.36:.../MaoField` (7B13 LAN) + `github = Wangziqi0/MaoField.git` (异地 fallback, D20 evening 配)

---

## §5 §3-§6 之 blocked status

| step | status | reason |
|---|---|---|
| §3 stop llama-server | 未跑 | blocked on §2.4 决 + 需 一凡 9070XT sudo password OR NOPASSWD verify |
| §4 rsync pull `dppl_bridge_verify/` | 未跑 | blocked on §2.4 决 |
| §5 pilot | 未跑 | blocked on §3, §4 |
| §6 main | 未跑 | blocked on §5 + 关卡 2 一凡 confirm |

---

## §6 D-1 binding 严守 ack

- 不擅自 跑 决策性 install (§2.4 A 选项) ✓
- 不擅自 declare "P0★-F close" / "实验 success" ✓
- 不擅自 inflate ballpark / 占位符 ✓ (所有数字 binary traced 到 shell 输出)
- 真实日期 binary 自检 ✓ (`date` 输出 verbatim print)
- 不擅自 修 launch script ✓ (尚未 rsync pull, 无 script 可改)
- D-1 纪律 4 子协作者验证: 本份 ack 由 9070XT Claude Desktop 单点 write, **不绑 7B13 主协作者**, 仅 surface 数字 + 阻塞 + 选项, 不下战略决

---

## §7 next 之 binary 期望

等 一凡 / 7B13 主会话 输 **A** / **B** / **C** 之一, 形式可:

1. 一凡 在 9070XT Claude Desktop (Remote Control) 之 conversation 内 binary 输 `install A ✓` / `B` / `C`
2. **或** 7B13 主会话 rsync push 一份 `LINUX_DECISION_D21.md` 至 `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/` (9070XT 端 git pull 或 ssh-poll 接收)

收到决之后 9070XT Claude **不二次 confirm**, 直接 binary execute (per D-PPL prompt §0 line 5)。

---

**生成**: 9070XT Claude Desktop (Remote Control session, Win 9955HX 一凡接管中)
**ack file path** (9070XT 本地): `/tmp/dppl_bridge_verify/output/ACK_D21_PREREQ.md`
**rsync target** (7B13): `amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/ACK_D21_PREREQ.md`
