# [9070XT surface — D21 桌面 cascade crash binary diagnose]

**真实今日日期** (`date '+%Y-%m-%d %H:%M:%S %Z'`): `2026-05-21 13:50 CST` (D21)

**Surface**: 9070XT Claude Desktop (Remote Control by Win 9955HX)

**对象**: 7B13 Linux 姐姐主会话 + (待 一凡 决) 反题 sub-agent verdict B audit iteration

**协议**: D-PPL 桥 verify D21 prompt 之 scope 外, **9070XT OS-level surface** — verdict B (5/11 ROCm RDNA 4 driver bug) 之 **scope 扩展** binary 抓 input

**状态**: 一凡 D21 13:48 surface "现在登陆进桌面过一会就黑屏回登陆界面"。9070XT Claude 之 read-only diagnose 抓到 root cause + 时间窗口 align。

---

## §1 一凡 之 报告 (binary verbatim)

一凡 D21 13:48 在 9070XT Claude Desktop (Remote Control session) 内 surface:

> 现在登陆进桌面过一会就黑屏回登陆界面

含义: 一凡 物理 在 9070XT 之 显示器前 (or ssh -X) 登陆 GDM 之 桌面 session, 几秒至几十秒后 桌面 collapse, 回到 gdm 之 login screen。多次 reproduce。

---

## §2 read-only diagnose binary 抓 root cause

### §2.1 顶层 verbatim quote (journalctl --user -b)

```
5月 21 13:42:27 amd-ONDA-B650M-W gnome-shell[152085]: amdgpu: The CS has cancelled because the context is lost. This context is innocent.
5月 21 13:42:27 amd-ONDA-B650M-W gnome-shell[152085]: GNOME Shell crashed with signal 6
5月 21 13:42:27 amd-ONDA-B650M-W gnome-shell[152085]: == Stack trace for context 0x5da98260e650 ==
5月 21 13:42:27 amd-ONDA-B650M-W gnome-shell[152085]: #0   5da9826d9df8 i   resource:///org/gnome/shell/ui/init.js:21 (27d4ad670bf0 @ 48)
5月 21 13:42:28 amd-ONDA-B650M-W snapd-desktop-i[152920]: Lost connection to Wayland compositor.
5月 21 13:42:28 amd-ONDA-B650M-W systemd[1745]: org.gnome.Shell@wayland.service: Main process exited, code=dumped, status=6/ABRT
5月 21 13:42:28 amd-ONDA-B650M-W systemd[1745]: org.gnome.Shell@wayland.service: Failed with result 'core-dump'.
5月 21 13:42:28 amd-ONDA-B650M-W systemd[1745]: Stopped target gnome-session-wayland@ubuntu.target - GNOME Wayland Session
```

### §2.2 binary 解读

| 字段 | 含义 |
|---|---|
| `amdgpu: The CS has cancelled because the context is lost.` | amdgpu kernel driver 之 message: GPU command submission (CS) 被 cancel, GPU context state lost (driver 之 reset 触发) |
| `This context is innocent` | mutter (gnome-shell) 自己没做错 — **其他 process 之 GPU op 触发 GPU-wide reset**, mutter 受 cascading 影响 |
| `signal 6 = SIGABRT` | mutter 无法 recover context, abort |
| `Lost connection to Wayland compositor` | 整个 桌面 session collapse → 回 gdm login screen |
| `code=dumped, status=6/ABRT` | gnome-shell @wayland.service 之 systemd unit fail with core-dump |

---

## §3 时间窗口 binary align (我之 GPU op → cascading crash)

```
13:21:36 我跑 HSA_OVERRIDE_GFX_VERSION=11.0.0 matmul
          → GPU Hang HW Exception (exit 134 SIGABRT, core dump)
          → amdgpu driver 之 GPU reset (driver self-recovered, 但 context state 之 stable 性 是否真清 待 audit)

13:30:22 pip uninstall + 跑 rocm7.2 wheel install (matmul gfx1201 native ✓)

13:37:17 [4/5] verify GPU matmul (rocm7.2 wheel, 无 HSA_OVERRIDE) ✓ 无 hang
13:37:32 [5/5] OPT-125m 加载 ✓

13:42:00 我跑 supervisorctl stop qwen8emib:qwen8emib_00
          → llama-server SIGTERM, cleanup 14.4 GB VRAM teardown

13:42:09 amd 物理 登陆 9070XT 桌面 (pam_unix session opened)
13:42:11 gnome-session 启动 + 子进程 dead 之 第一 warning
13:42:17-23 一凡 开 3 个 gnome-terminal (mutter 之 stacking 之 assertion warning, 不致命)
13:42:27 ★ amdgpu CS cancelled, context lost → gnome-shell SIGABRT ★
13:42:28 桌面 session collapse → 回 gdm login screen
```

**时间精度**:
- 我之 supervisorctl stop 13:42:00 → mutter crash 13:42:27 = **27 秒间隔**
- 中间 一凡 13:42:09 物理 登陆 + 13:42:17 起 开 terminal (mutter 重用 GPU context)

**致命窗口推测**:
- 13:21 之 HSA_OVERRIDE hang 之 GPU driver state 累计 (~21 min 仍 不完全 clean)
- 13:42:00 之 llama-server kill 时刻 触发 amdgpu 之 driver 二次 reset
- mutter 之 GPU context 在 reset 时刻 同步 invalidate, `context lost`
- mutter 之 ~13:42:17 之 terminal 渲染 + ~13:42:27 之 渲染 op 触碰 lost context → SIGABRT

---

## §4 verdict B 之 scope 扩展 (binary surface)

**之前 verdict B** (5/11 binary 判定, 9070XT CLAUDE.md 记):

> 5/11 alpha=10 hang **已 binary 判定 = ROCm RDNA 4 driver bug (verdict B)**, 不是 framework boundary

**之前 verdict B 之 scope** = "alpha=10 chain 长跑 hang" (single trigger class)

**D21 binary surface 之 scope 扩展** (新 binary 抓):

| trigger class | 之前 verdict B | D21 抓 |
|---|---|---|
| chain 长跑 alpha=10 (5/11 baseline) | ✓ 已 binary 判定 | — |
| **install verify cold-start matmul (HSA_OVERRIDE=11.0.0)** | 不在 之前 scope | ✓ D21 13:21 抓 (verdict B-2) |
| **GUI 桌面 (mutter Wayland compositor) cascading crash** | 不在 之前 scope | ✓ D21 13:42:27 抓 (verdict B-3) |

**实质 = RDNA 4 之 amdgpu kernel driver 之 不稳定** (Ubuntu 24.04 之 kernel 6.x + mesa + amdgpu 之 RDNA 4 driver), 即使 ROCm 7.2 之 user-space (rocm-smi / rocminfo / torch wheel) 之 matmul 跑 OK, **kernel-level amdgpu driver 之 context reset 之 cascading 仍 影响所有 GPU consumer** (chain 实验 + Wayland compositor 同 受害)。

---

## §5 9070XT Claude 之 honest mitigation 选项 (一凡 / Linux 姐姐 决)

| 选项 | binary action | trade-off | recommend tier |
|---|---|---|---|
| **(M-1)** | 一凡 **不在 9070XT 物理 显示器登陆 GUI**, 改 Win 端 ssh terminal 接 9070XT (跟 Remote Control Claude 之 path 同) | 不 用 GUI = mutter 不跑 = 没 cascading 受害, 完全避桌面 crash 循环。**这条已是 D20 三机架构 之 design intent (一凡 = Win interactive 端, 9070XT = GPU 执行节点, 不应 物理 用 9070XT GUI)** | **★★ 短期 best** |
| (M-2) | GDM 切到 **X11 session** (不 Wayland), Xorg 之 GPU dep 比 mutter 少 | 可能 less affected (X11 之 GPU rendering 通过 amdgpu DRM 不 直接 attach context, less 受 reset 影响), 但需 test, 不 guaranteed | ★ |
| (M-3) | Linux 姐姐 / 一凡 决 OS-level upgrade: kernel 6.14+ (Ubuntu 24.10/25.04) + amdgpu firmware update + ROCm 7.3+ stable | OS-level, **不在 9070XT Claude scope**, 但 是 长期 fix RDNA 4 driver 之 path. paper timeline 之 cloud A100 fallback 之 替代 path | **★★★ 长期** |
| (M-4) | Win 之 SSHFS-Win mount 7B13 (一凡 paper deep read 路径 — D20 self-action #3 装 WinFsp) | 完全避开 9070XT GUI, 一凡 只在 Win 之 native GUI 工作, 9070XT 是 headless GPU 节点 | ★★ 长期 |

### §5.1 推荐 path

**短期** (今 D21 内 立即 actionable): **M-1** — 一凡 不在 9070XT 物理 GUI, 用 Win 端 ssh / Remote Control 全部 操作。9070XT 之 boot 之后 不登陆 GUI (但 gdm 之 login screen 一直在, 不影响 driver state)。

**长期** (D60+): **M-3** — kernel + amdgpu firmware upgrade。M-4 之 SSHFS-Win + WinFsp 是 一凡 D20 self-action #3 + #4 之 已 plan, 升级 后 一凡 物理 设备完全 移到 Win, 9070XT headless。

---

## §6 与 D-PPL 桥 verify scope 之 implication

### §6.1 直接 implication (不阻塞 §5 pilot fix)

- 桌面 cascade crash 不直接 block §5 pilot (pilot 之 python script 跑在 terminal / ssh, 不 require GUI)
- 但 一凡 物理 在 9070XT 显示器前 之 体验受影响 (一凡 必须 切到 Win 端 ssh 路径)
- 若 一凡 接受 M-1 = 立即 OK proceed, 不影响 D-PPL pipeline timeline

### §6.2 间接 implication (verdict B audit input 扩展)

- 反题 sub-agent verdict B audit (5/11 之 H 反题 sub-agent 之 后续 iteration) 应 spawn 新一轮, **input 含 D21 新抓 之 verdict B-2 + B-3 scope 扩展 evidence** (即 install matmul + GUI cascading)
- 之 audit 之 结果 可能 影响 paper v8.1 之 footnote — 之前 v8 footnote 描述 verdict B = "alpha=10 chain hang only", 应 expand 为 "RDNA 4 amdgpu driver 之 kernel-level context reset cascading 之 unstable, 影响 chain hang + cold-start matmul + GUI compositor"
- 但 这是 7B13 Linux 姐姐 / 一凡 / 反题三方 决, **9070XT Claude 不 propose paper v8 final lock 之 重开** (D-1 binding 严守)

### §6.3 关卡 4 之 implication (PI + DS + 反题 三方决)

- 之前 paper v8 final lock 之 47/47 manifest 含 verdict B 之 description = "5/11 alpha=10 chain hang only"
- D21 binary surface 之 verdict B-2 + B-3 之 evidence 是否 触发 paper v8 之 footnote update? — **PI + DS + 反题 三方决, 不在 9070XT Claude scope**
- 9070XT Claude 仅 surface evidence, 不 propose paper level change

---

## §7 9070XT Claude 之 binding 严守

- ✗ 不擅自 reboot 9070XT (会 disrupt llama-server stop 之 state, 影响 D-PPL pipeline)
- ✗ 不擅自 改 OS config (kernel boot params / amdgpu module params / mesa config)
- ✗ 不擅自 关 / 切 GDM 之 session 类型 (Wayland → X11 是 user-config, 需 一凡 物理 在 9070XT 之 GDM login screen 切)
- ✗ 不擅自 trigger GPU op 之 verdict B 之 repro test (避免 第三次 hang 累计)
- ✗ 不 propose paper v8 final lock 重开 (D-1 binding §8.1)
- ✓ read-only diagnose: `loginctl` + `systemctl status` + `journalctl --user -b` (amd in adm group, 不 sudo)
- ✓ 占位符 ✓ — 所有 timestamp binary verbatim 引用 journal, 所有 PID binary trace

---

## §8 9070XT 端 当前 state (相关)

```
display manager:       GDM3 (gdm.service active since 5/19 20:10 CST)
session type:          gnome-session-wayland@ubuntu.target (mutter Wayland compositor)
amd user groups:       amd adm cdrom sudo dip video plugdev users lpadmin render

当前 sessions (loginctl):
  Session 277 (amd, pts/0, active)            ← Bash terminal (我 跑 在的 session)
  Session 344 (amd, no TTY, active)            ← 可能 systemd user manager OR 残留 gnome-session
  Session c2  (gdm, tty1, idle 1min 50s)      ← gdm 之 login screen tty1 (一凡 刚 crash 出来)

GPU [Device 0]:        RX 9070 XT 16 GB gfx1201
ROCm runtime:          7.2.0
amdgpu driver:         (kernel 6.x, Ubuntu 24.04, 之 RDNA 4 driver 不稳定 = verdict B)

dmesg access:          ✗ "不允许的操作" — kernel.dmesg_restrict=1, amd in adm group 但 read 失败
                       (workaround: sudo dmesg, 但 9070XT Claude 不擅自 sudo, 一凡 ssh self-action 可读)

verdict B 之 D21 binary surface 之 2 次 GPU 之 OS-level 受害:
  1. 13:21:36 HSA_OVERRIDE=11.0.0 之 matmul → GPU Hang HW Exception (B-2)
  2. 13:42:27 gnome-shell 之 amdgpu context lost → SIGABRT (B-3)
```

---

## §9 next 之 binary 期望

### §9.1 一凡 之 short-term action

- (M-1 推荐) **一凡 不再 在 9070XT 物理 显示器 登陆 GUI**, 改 Win 端 ssh + Remote Control 全部 操作 (跟 D20 三机架构 design intent align)
- 9070XT 之 gdm login screen 一直 显示在 9070XT 物理 显示器 OK (不消耗 GPU rendering, 不 crash), 一凡 不需 切

### §9.2 Linux 姐姐 之 action option

- 决 是否 spawn 反题 sub-agent verdict B audit iteration (input = 本份 surface markdown 之 D21 新 evidence)
- 决 是否 paper v8 之 footnote 之 verdict B description 应 update (PI + DS + 反题三方决 scope, 9070XT Claude 不 propose)
- 决 长期 OS-level upgrade path (kernel 6.14+ + amdgpu firmware) 之 timeline + ownership

### §9.3 不阻塞 §5 pilot fix

桌面 cascade crash 是 **GUI scope, 不直接阻塞 §5 pilot**。一凡 决 R3 之 (R3-i)/(R3-ii)/(R3-iii) 之 任一 path 后, §5 pilot 可继续 (在 ssh terminal 内, 不 require GUI)。

---

**生成**: 9070XT Claude Desktop (Remote Control session by Win 9955HX 一凡接管)
**surface file path** (9070XT 本地): `/tmp/dppl_bridge_verify/output/SURFACE_D21_DESKTOP_CASCADE_CRASH.md`
**rsync target** (7B13): `amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/`

**附**: journal 之 verbatim quote 全部 在 §2.1 内, log 文件 (journalctl --user -b) 之 export 是 巨大 (~MB 级别), 不一同 push。若 7B13 Linux 姐姐 / 反题 sub-agent 需要 完整 journal export, 一凡 ssh self-action: `ssh amd@192.168.31.22 'journalctl --user -b > /tmp/journal_user_d21.log' && rsync ...`
