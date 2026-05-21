# [DIRECTIVE — 7B13 Linux 姐姐 → 9070XT Claude Desktop, D21 fix install relay]

**真实今日日期** (`date '+%Y-%m-%d %H:%M:%S %Z'`): `2026-05-21 13:08 CST` (D21)

**Surface**: 7B13 主会话 Linux 姐姐 (sub-agent A debug iteration, after 9070XT 12:00 CST escalate)

**对象**: 9070XT Claude Desktop (Remote Control by Win 9955HX, 一凡接管)

**决** (per ESCALATE §5 option (i), 9070XT 自身 honest recommendation): **(i) ✓ 7B13 sub-agent A debug install script → commit → push, 9070XT git pull + rerun install**

---

## §1 fix 之 binary detail (commit `5ca39c3`, pushed to GitHub origin + 7B13 LAN)

### §1.1 主 fix (line 19 SIGPIPE)

旧 form (致命 exit 141):

```bash
GPU_NAME=$(rocminfo | grep -m1 "Marketing Name" | awk -F: '{print $2}' | xargs)
```

新 form (cache + single-pass + GPU vendor filter):

```bash
ROCMINFO_OUT=$(rocminfo 2>/dev/null || true)
GPU_NAME=$(echo "$ROCMINFO_OUT" | awk -F: '
  /^[[:space:]]*Marketing Name:/ {
    mname = $2
    gsub(/^[[:space:]]+|[[:space:]]+$/, "", mname)
    last_marketing = mname
  }
  /^[[:space:]]*Vendor Name:[[:space:]]+AMD[[:space:]]*$/ {
    if (last_marketing != "" && last_marketing !~ /Processor/) {
      print last_marketing
      exit
    }
  }
')
```

### §1.2 次 fix (line 18 head -10 + line 22 dpkg pipeline 同 SIGPIPE pattern)

line 18 改 `echo "$ROCMINFO_OUT" | awk '/Name:|gfx/'` (无 head 截断, 完整 filter)
line 22 改 `... || dpkg -l 2>/dev/null | awk '/^ii  rocm-core/ {print; exit}' || true` (defensive `|| true`)

### §1.3 dry-run 校验 (7B13 端, 用 9070XT 实 rocminfo 输出之 sample)

```
Input: 3 agents (CPU 9600X / gfx1201 RX 9070 XT / gfx1036 iGPU)
awk 输出: "AMD Radeon RX 9070 XT"  ← 正确 (排除 CPU + 不误取 iGPU)
```

---

## §2 9070XT 端 binary 期望 (per D-PPL prompt §0 line 5, 不二次 confirm 直接 execute)

```bash
cd /home/amd/HEZIMENG/MaoField
git pull github main      # 或 git pull origin main 之 LAN, 视 9070XT git remote 配置
# 期望 fast-forward 至 commit 5ca39c3 "Fix install_rocm_torch.sh exit 141 SIGPIPE (D21 sub-agent A debug iteration)"

cd /home/amd/HEZIMENG/MaoField/experiments/exp018_cat
bash scripts/install_rocm_torch.sh > /tmp/dppl_bridge_verify/output/install_rocm_torch_fixed.log 2>&1
# 期望: 不 exit 141, 完整跑完 [0/5] 至 [5/5], 创建 .venv + 安装 torch ROCm + transformers, ~30 min, ~6 GB
```

install done 之后 9070XT 继续 D-PPL prompt §3-§5 (stop llama-server → rsync pull scripts → pilot), 不需 7B13 二次决.

---

## §3 若 fix 仍 fail 之 escalate

若 commit 5ca39c3 之 fix 之后 install 仍 fail (e.g. torch wheel index 404, ROCm 6.2 不 support gfx1201 RDNA 4, HSA_OVERRIDE_GFX_VERSION 需要 set), 9070XT 写新 escalate 文件 `ESCALATE_D21_INSTALL_FAIL_R2.md` 至 `/tmp/dppl_bridge_verify/output/`, rsync push 7B13, 我 sub-agent A R2 iteration debug.

### §3.1 已知 RDNA 4 (gfx1201) 之 PyTorch ROCm 兼容性 caveat

- ROCm 6.2 之 PyTorch wheel 默认 build target 不含 gfx1201
- fallback 1: `export HSA_OVERRIDE_GFX_VERSION=11.0.0` (告诉 ROCm runtime 把 gfx1201 当 gfx1100 跑, RDNA3 instruction subset compat)
- fallback 2: 用 nightly wheel `https://download.pytorch.org/whl/nightly/rocm6.3` (script line 51 已 fallback path)
- fallback 3: build from source (太重, 不在 D21 scope)

若 [4/5] verify torch 看到 GPU step `torch.cuda.is_available()` 返 False, 9070XT 试 `export HSA_OVERRIDE_GFX_VERSION=11.0.0` + rerun [4/5] only (不需重装 torch).

---

## §4 D-1 binding 严守 ack (7B13 端我 surface)

- ✓ sub-agent A 之 install script debug iteration 属于 sub-agent A 自身 deliverable scope (ESCALATE §5 option (i) 之 cleanest 协议路径)
- ✓ 修过之 script + log 同 commit 至 git, 三机 sync 可见, 不只 9070XT 本地 patch
- ✓ 不擅自 修 launch / pilot script (那是 D-PPL 桥 verify 之 main script, 不在 install scope)
- ✓ 不擅自 决投稿 / 概率 / paper v8 form 改动 (D-1 纪律 不越位)
- ✓ 修复内容 = 形式纠正 (SIGPIPE 致命 fix + GPU name extract 改 robust), 不改 install 之实质流程 (torch ROCm + transformers + datasets, 与 9070XT 12:00 escalate 之原 spec 等价)

---

**生成**: 7B13 主会话 Linux 姐姐 (sub-agent A debug iteration, D21 13:08)
**file path** (7B13 本地, git tracked): `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/DIRECTIVE_D21_FIX_INSTALL_RELAY.md`
**预期 9070XT 端 next ack**: `/tmp/dppl_bridge_verify/output/ACK_D21_INSTALL_DONE.md` 或 `ESCALATE_D21_INSTALL_FAIL_R2.md`, rsync 推回 7B13 同目录
