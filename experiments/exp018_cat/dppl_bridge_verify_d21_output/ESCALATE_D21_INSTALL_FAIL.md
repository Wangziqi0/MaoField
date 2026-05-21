# [9070XT escalate — D-PPL 桥 verify D21 install fail]

**真实今日日期** (`date '+%Y-%m-%d %H:%M:%S %Z'`): `2026-05-21 12:00 CST` (D21)

**Surface**: 9070XT Claude Desktop (Remote Control by Win 9955HX, 一凡接管)

**对象**: 7B13 Linux 姐姐主会话 + 第十三波派遣 sub-agent A

**协议**: D-PPL 桥 verify D21 prompt §7 之 escalate flag 路径 (file rsync, 非 conversation)

**状态**: install_rocm_torch.sh **2 次跑均 fail exit 141 (SIGPIPE)** — venv 仍 不存在, §2.4 阻塞 unsolved

---

## §1 fail 之 binary detail

### §1.1 attempt 1 (11:54 CST)

- 命令: `nohup bash scripts/install_rocm_torch.sh > install_rocm_torch.log 2>&1 &`
- log 内容: 仅 line 1-12 (ROCm 检查 rocminfo grep 输出 10 行)
- venv: 未创建
- 进程: 早 disappear

### §1.2 attempt 2 (11:55 CST, no nohup, run_in_background 直跟踪)

- 命令: `bash scripts/install_rocm_torch.sh > log 2>&1`
- exit code: **141 = SIGPIPE**
- log 同 attempt 1 (line 1-12 ROCm 输出后 stop)

### §1.3 attempt 3 (12:00 CST, bash -x 完整 trace)

- 命令: `bash -x scripts/install_rocm_torch.sh > install_trace.log 2>&1`
- exit code: **141** (确证 SIGPIPE)
- trace log 完整 23 行, 见下

---

## §2 bash -x trace 之 last lines (root cause 定位)

```
+ set -euo pipefail
+ echo '[0/5] 检查 22 主机 ROCm 环境'
[0/5] 检查 22 主机 ROCm 环境
+ command -v rocminfo
+ rocminfo
+ grep -E 'Name:|gfx'
+ head -10
  Name:                    AMD Ryzen 5 9600X 6-Core Processor       ← (CPU agent)
  Marketing Name:          AMD Ryzen 5 9600X 6-Core Processor
  Vendor Name:             CPU
  Name:                    gfx1201
  Marketing Name:          AMD Radeon RX 9070 XT
  Vendor Name:             AMD
      Name:                    amdgcn-amd-amdhsa--gfx1201
      Name:                    amdgcn-amd-amdhsa--gfx12-generic
  Name:                    gfx1036
  Marketing Name:          AMD Radeon Graphics
++ rocminfo
++ grep -m1 'Marketing Name'
++ awk -F: '{print $2}'
++ xargs
+ GPU_NAME='AMD Ryzen 5 9600X 6-Core Processor'       ← ★ (CPU 名字, 不是 GPU, sub-agent A 之 second bug)
                                                       ← (line 20 之 echo "GPU: $GPU_NAME" 没执行, exit 在此)
```

---

## §3 root cause binary 分析

### §3.1 主 fail (致命)

install_rocm_torch.sh line 19:

```bash
GPU_NAME=$(rocminfo | grep -m1 "Marketing Name" | awk -F: '{print $2}' | xargs)
```

- `grep -m1` 找到第 1 个 `Marketing Name` match 之后 **立即 exit 0**
- rocminfo 继续写 stdout 给已 close 之 grep stdin → rocminfo 收 **SIGPIPE → exit 141**
- `set -o pipefail` (script line 10) 让整个 pipeline 之 exit code = pipeline 内 max non-zero = **141**
- `GPU_NAME=$(failed_pipeline)` 之 assignment exit code = substitution exit code = **141**
- `set -e` 在 simple assignment with failing command substitution 触发 → script exit 141, 不跑后续

### §3.2 次 bug (非致命但 latent)

`grep -m1 "Marketing Name"` 之结果 = `AMD Ryzen 5 9600X 6-Core Processor` (CPU agent 之 Marketing Name, 第一个 match), **不是** GPU 名字。即使主 fail fix 之后, 第 22 行之 echo 会输出 `GPU: AMD Ryzen 5 9600X 6-Core Processor` 是 misleading prose, 但 install script 后续不依赖 $GPU_NAME, 不阻塞 install 实质流程。

### §3.3 sub-agent A 之 install script design 偏差

- `set -euo pipefail` 严格但与 `grep -m1` 之 早 exit 行为 不兼容
- 应写为 `... || true` 屏蔽 SIGPIPE, 或 `awk '/Marketing Name/{print $2; exit}'` 之 single-pass form

---

## §4 9070XT Claude 之 D-1 binding 严守 ack

- ✗ **不擅自 修 install_rocm_torch.sh** (D-1 binding §8.3 "不擅自 修 launch script", install script 属于 sub-agent A 产出之 同份 deliverable scope)
- ✗ **不擅自 bypass install script 跑 venv + pip install 手动序列** (违反 §8.3 同一 binding, 即使 venv 创建 + pip install 命令本身 deterministic)
- ✓ surface escalate 给 7B13 + 一凡 决之, 等 binary 决

---

## §5 待 一凡 / 7B13 binary 决之 三选

| 选项 | binary action | trade-off |
|---|---|---|
| **(i)** 7B13 sub-agent A 之 debug iteration: rewrite install script line 19 (add `\|\| true` 或 改 awk 写法) + commit + push, 9070XT git pull + rerun install | ~30 min sub-agent + ~30 min install = ~1h | D-1 binding 之 protocol fix, 之后 install script 可重用 |
| **(ii)** 7B13 直接 push fix-patch (sed -i 之 one-liner) 至 9070XT, 我 apply + rerun install | ~10 min patch + ~30 min install = ~40 min | 不 commit, 仅 9070XT 本地 patch, 之后 7B13 git 仓库仍 buggy |
| **(iii)** 一凡 explicit override 给 9070XT Claude 授权: "bypass install script, 跑 venv + pip install 手动序列" | ~30 min install | 违反 D-1 binding §8.3, 但一凡 PI 权限 可 override, surface 之后 7B13 sub-agent fix script 之 latent dep 仍要补 |

**9070XT Claude 之 honest recommendation**: **(i) > (ii) > (iii)**

- (i) 是协议 cleanest 之路径, sub-agent A 自己 debug 自己 buggy script, 之后整套 install pipeline reusable
- (ii) 是 fast-track, 但 7B13 仓库仍 latent buggy
- (iii) 是 PI override, 越线但 actionable; 9070XT Claude 不主动 propose 此选项, 仅 surface 给 一凡 之 option 用

但 binary 决 留 一凡 / 7B13 主会话。

---

## §6 9070XT 端 当前状态 (binary, jsonl-traced)

```bash
# venv
/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/.venv  →  不存在

# system python3
/usr/bin/python3 → python 3.x (具体 version 不重要)
import torch          → ModuleNotFoundError
import transformers   → ModuleNotFoundError
import datasets       → ModuleNotFoundError

# rocminfo (host ROCm ok)
gfx1201 (RX 9070 XT) 之 ROCm runtime 可见

# 9070XT 进程 (relevant)
llama-server (root, PID 2080, port 8080) 仍跑, VRAM 占用 ~14.4 GB (待 §3 stop)
install_rocm_torch.sh 进程 → 已 exit (3 次均 fail)

# log 文件
/tmp/dppl_bridge_verify/output/install_rocm_torch.log     (673 bytes, attempt 2)
/tmp/dppl_bridge_verify/output/install_trace.log          (~1.5 KB, attempt 3 bash -x)

# rocminfo grep 之 实际 match 行数
13 行 (验证 head -10 之 SIGPIPE 边界, 之外 install script line 19 之 grep -m1 才是 fail point)
```

---

## §7 §3-§6 之 blocked status

| step | status | reason |
|---|---|---|
| §2.4 venv install | ✗ fail 3x (exit 141) | 此 escalate 之 主因 |
| §3 stop llama-server | 未跑 | blocked on §2.4 |
| §4 rsync pull dppl_bridge_verify/ | 未跑 | blocked on §2.4 |
| §5 pilot | 未跑 | blocked on §2.4 + §3 + §4 |
| §6 main | 未跑 | blocked on §5 + 关卡 2 |

---

## §8 next 之 binary 期望

等 一凡 / 7B13 主会话 输 **(i)** / **(ii)** / **(iii)** 之一, 形式:

1. 一凡 在 9070XT Claude Desktop (Remote Control) 之 conversation 内 binary 输 `(i)` / `(ii)` / `(iii)` + (若 ii 或 iii) 之具体 patch 或 override 文本
2. **或** 7B13 主会话 rsync push fix-patch 或 修过之 install script 至 9070XT, 我 接收 + rerun
3. **或** 7B13 主会话 commit 修过之 install script + git push, 9070XT 自动 (或 我 手动) git pull + rerun

收到决之后 9070XT Claude **不二次 confirm**, 直接 binary execute (per D-PPL prompt §0 line 5)。

---

**生成**: 9070XT Claude Desktop (Remote Control session)
**escalate file path** (9070XT 本地): `/tmp/dppl_bridge_verify/output/ESCALATE_D21_INSTALL_FAIL.md`
**rsync target** (7B13): `amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/`
