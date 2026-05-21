# [9070XT surface — D21 桌面 cascade crash fix applied]

**真实今日日期** (`date '+%Y-%m-%d %H:%M:%S %Z'`): `2026-05-21 14:38 CST` (D21)

**Surface**: 9070XT Claude Desktop (Remote Control by Win 9955HX)

**对象**: 7B13 Linux 姐姐主会话 + 一凡 之后 read 之 anchor (一凡 D21 14:30 explicit 让 我 修, 后 跟 Linux 姐姐 讨论 数学 + 哲学)

**协议**: 9070XT OS-level 之 sub-agent action, **不在 D-PPL 桥 verify scope**, 但 verdict B-3 之 mitigation 是 paper-relevant

**状态**: 一凡 explicit "更新驱动或者别的" 之 PI authorization → 我 binary execute, package upgrade 不 actionable, GDM config + session type 改 2 项 已 apply ✓

---

## §1 一凡 之 instruction (binary verbatim)

D21 14:30 一凡 在 9070XT Claude Desktop conversation 内:

> 你现在去修桌面闪退的问题 更新驱动或者别的 我去跟linux 探讨下一步实验和数学哲学研究

**Scope authorization 含**:
- ✓ 更新驱动 (mesa / firmware / amdgpu / libdrm 之 package upgrade)
- ✓ 或者别的 (config 改 / system service 调整 / 之类)
- ✗ 不 explicit 含 reboot (conservative interpretation, 一凡 不在 现场 之 reboot recover 风险 high)

---

## §2 read-only diagnose (D21 14:34-14:37, binary)

### §2.1 system state

| 项 | 值 | 评价 |
|---|---|---|
| kernel | `6.17.0-29-generic` | 较新 (Ubuntu 24.04 default 6.8, 6.17 是 HWE OR 升级 之) |
| mesa | `25.2.8-0ubuntu0.24.04.1` | **latest** (mesa 25.2 是 2026 之 release) |
| libdrm | `2.4.125-1ubuntu0.1~24.04.1` | **latest** |
| libdrm-amdgpu1 | `2.4.125` | latest |
| linux-firmware (RDNA 4) | `/lib/firmware/amdgpu/gc_12_0_*.bin.zst` 存在 (imu/me/mec/mes1/mes/pfp/rlc/toc/uni_mes) | ✓ RDNA 4 firmware **已 deploy** |
| amdgpu module | dynamic load (modinfo 不 list 全 firmware) | normal |

### §2.2 pending package upgrade

```
$ apt list --upgradable | grep -iE "mesa|libdrm|firmware|amdgpu|xorg|gnome-shell|mutter|wayland"
(空 — 无 pending upgrade)
```

**driver / firmware / mesa 之 latest 已 deploy**, **package upgrade 这条 path 不 actionable** (即 verdict B-3 之 root cause 不是 package version 过期, 是 RDNA 4 之 amdgpu kernel driver 之 latest 本身 仍 trigger context lost)。

### §2.3 GDM config + session type

| 项 | 改前 | 改后 (apply) |
|---|---|---|
| `/etc/gdm3/custom.conf` `AutomaticLoginEnable` | `true` ★ 关键 issue ★ | **`false`** ✓ |
| `/etc/gdm3/custom.conf` `AutomaticLogin` | `amd` | `amd` (保留, 但 enable=false 不 effective) |
| `/var/lib/AccountsService/users/amd` `Session` | `ubuntu` (Wayland default) | **`ubuntu-xorg`** (X11) ✓ |

### §2.4 backup files (可 restore)

```
/etc/gdm3/custom.conf.bak_d21                       (改前 state)
/var/lib/AccountsService/users/amd.bak_d21          (改前 state)
```

restore command (一凡 ssh self-action 若 需要):

```bash
ssh amd@192.168.31.22
sudo cp /etc/gdm3/custom.conf.bak_d21 /etc/gdm3/custom.conf
sudo cp /var/lib/AccountsService/users/amd.bak_d21 /var/lib/AccountsService/users/amd
```

---

## §3 改 之 期望 effect (binary 假设, 待 一凡 verify)

### §3.1 fix 1 (AutomaticLogin = false) 之 expected behavior

```
之前 (AutomaticLogin=true):
  boot → gdm 启动 → 自动 login amd → gnome-session-wayland 启动 → mutter trigger amdgpu cascade
  → gnome-shell SIGABRT → 桌面 collapse → 回 gdm → 自动 login amd → 循环

之后 (AutomaticLogin=false):
  boot → gdm 启动 → 显示 GDM login screen (idle, GUI 不占 GPU rendering)
  → 一凡 物理 选 amd + 输 password + 选 session + 进 桌面 (若 一凡 explicit 需要 GUI)
  OR
  → 一凡 不进 桌面, ssh terminal 全程, 9070XT 物理 显示器 显示 gdm login screen 永久 idle
  → **mutter 不跑 = amdgpu cascade 不 trigger = 不闪退**
```

### §3.2 fix 2 (Session=ubuntu-xorg) 之 expected behavior

一凡 一旦 物理 在 GDM login screen 输 password 进 amd, 之 default session 是 **X11 (Xorg)**, 不是 Wayland mutter。Xorg 之 GPU dep:

- X11 之 GPU rendering 通过 amdgpu DRM 之 KMS, **更 stateless** (与 GPU context tightly bound 之 mutter Wayland 不同)
- 即使 amdgpu kernel driver trigger reset, Xorg 之 client 之 redraw 是 explicit + 之 context recovery 更 robust
- 大概率 less affected (**但 不 guaranteed** — RDNA 4 driver 之 不稳定 之 cascading 仍 可能 hit Xorg)

### §3.3 D-1 binding 严守 之 binary assumption caveat

- ✗ 不 declare "fix 解决 桌面闪退" (没 reboot, 没 测试, binary verify pending 一凡 之 实测)
- ✓ 仅 surface "fix apply ✓, expected behavior described, 待 一凡 之 binary verify"
- ✗ 不 declare X11 session 之 stability 之 guarantee (RDNA 4 driver bug 之 cascading 之 scope 仍 active hypothesis)

---

## §4 一凡 之 binary verify path (D-1 纪律 2 之 48h 反馈真空 不存活)

### §4.1 immediate verify (无需 reboot)

```bash
# 一凡 ssh 9070XT (Win 端):
ssh amd@192.168.31.22

# logout 之后 之 GDM lock screen 之 view (但 logout 是 GUI action, 一凡 物理 在 9070XT OR Win 端 不直接 logout)

# 或 GDM restart (一凡 ssh 跑, 会断 9070XT 物理 GUI 之 当前 session):
sudo systemctl restart gdm3
# 跑 之 后, 9070XT 物理 显示器 显示 fresh GDM login screen (不 自动 login)
# 一凡 在 9070XT 物理 显示器前 选 amd + 输 password + 进 桌面 → verify X11 session 之 stability
```

### §4.2 next reboot 之 verify (一凡 explicit reboot, 不 我 跑)

```bash
# 一凡 explicit 之后:
ssh amd@192.168.31.22 'sudo reboot'

# boot 之后, 9070XT 物理 显示器 显示 GDM login screen (不 自动 login)
# 一凡 选 amd + 输 password + 进 X11 session
# verify 桌面 之 stability (~10-30 min idle / 之 简单 GUI op)
```

### §4.3 verify 之 binary check

| check | binary | pass criterion |
|---|---|---|
| boot 之 后 不 自动 进 桌面 | gdm-x-session crash 之 absence (journal --user) | login screen idle persist > 5 min |
| 一凡 manual login 之后 之 session type | `echo $XDG_SESSION_TYPE` (在 gnome-terminal 内) | `x11` (不是 `wayland`) |
| 桌面 idle 之 stability | `journalctl --user --since "session start" 2>&1 \| grep -iE "amdgpu\|crash\|SIGABRT"` | 0 amdgpu cascade entry |
| GUI op 之 stability | 开 Firefox / Files / Terminal, 拖窗口, 等 ~10 min | 0 桌面 collapse |

---

## §5 长期 fix path (D60+ scope, 不在 我 当前 scope)

| path | binary action | timeline |
|---|---|---|
| (a) kernel 6.18+ (Ubuntu 24.10 / 25.04 HWE kernel) | 一凡 / Linux 姐姐 决之 + 一凡 物理 reboot | D60+ |
| (b) ROCm 7.3+ stable runtime upgrade | 一凡 ssh self-action 之 ROCm SDK update + 之 venv torch wheel 之 reinstall (rocm7.3 wheel 之 verify, 之 wheel index 是否 published) | D45+ |
| (c) amdgpu firmware 之 之 dev branch (linux-firmware-amdgpu-dkms OR git pull from kernel.org) | 风险 high, 不在 production scope | D90+ |
| (d) 完全 移 GUI 到 Win 9955HX (D20 三机架构 之 design intent) | 一凡 之 default operating mode 改 (D20 self-action #3 之 WinFsp 装 + SSHFS-Win mount) | D21-D30 (一凡 D20 之 self-action) |

**9070XT Claude 之 honest recommendation**:
- 短期 (本 D21 末): 当前 fix 已 apply, 一凡 next physical login 之 verify
- 中期 (D30 内): **(d)** 一凡 之 D20 self-action 之 WinFsp + SSHFS-Win 完成, 之后 9070XT 是 headless GPU node, **完全 不用 9070XT 物理 桌面**
- 长期 (D60+): **(a)** + **(b)** 之 OS-level upgrade, 之 PI + Linux 姐姐 决 timeline

---

## §6 9070XT Claude 之 D-1 binding 严守 ack

| binding | binary verify |
|---|---|
| 不擅自 reboot | ✓ (PI authorization "别的" 之 scope 不 explicit 含 reboot, conservative interpretation) |
| 不擅自 修 OS kernel boot params | ✓ (不 改 grub config) |
| 不擅自 disable / mask GDM service | ✓ (仅 改 AutomaticLogin 设置, 不 mask service) |
| 不擅自 install / remove package | ✓ (apt list --upgradable 无 pending, 不 install / 不 remove) |
| backup 之 reversibility | ✓ (custom.conf.bak_d21 + amd.bak_d21 保留) |
| 占位符 ✓ | ✓ (所有 改 之 diff binary verbatim, 所有 verify command binary listable) |
| 真实日期 binary print | ✓ (head line `date` 输出 verbatim) |

---

## §7 9070XT 端 当前 state (post-fix, binary)

```
GDM:
  AutomaticLoginEnable:        false ✓
  AutomaticLogin:              amd (保留, 但 enable=false 不 effective)
  
AccountsService /amd:
  Session:                     ubuntu-xorg ✓ (X11, 不 Wayland)
  Icon:                        /home/amd/.face (不动)
  SystemAccount:               false (不动)
  InputSource0:                ibus=libpinyin (不动)
  InputSource1:                xkb=cn (不动)

backup files:
  /etc/gdm3/custom.conf.bak_d21                       ✓
  /var/lib/AccountsService/users/amd.bak_d21          ✓

kernel:                        6.17.0-29-generic (不动)
mesa:                          25.2.8-0ubuntu0.24.04.1 (latest, 不动)
libdrm:                        2.4.125-1ubuntu0.1~24.04.1 (latest, 不动)
amdgpu firmware (RDNA 4):      gc_12_0_*.bin.zst ✓ 已 deploy (不动)

GDM3 service:
  Active:                      ✓ (since 5/19 20:10 CST, 之 不动)
  当前 session 之 stop 之 时刻:  仅 sudo systemctl restart gdm3 OR reboot 之 时刻 effective

verdict B-3 之 risk (mutter Wayland):
  trigger probability:         应大幅 降低 (mutter Wayland 之 default 之 user 不再 一凡 amd)
  alternative path:            X11 (less GPU-dep) — 但 不 binary guaranteed less-affected, 待 一凡 之 实测 verify
```

---

## §8 与 D-PPL 桥 verify pipeline 之 关系

### §8.1 不阻塞 §6 main run

- 桌面 fix 是 OS-level 之 mitigation, 不在 D-PPL pipeline critical path
- main run 跑 之 时刻, 9070XT 之 GUI session 之 状态 不 affect Python pilot / main 之 GPU compute (chain 之 Python 跑在 ssh terminal pty, 不依赖 mutter)
- AutomaticLogin=false 之 改 之 后, 即使 9070XT reboot, 不再 自动 启动 桌面 GUI session → 减少 amdgpu cascading 之 risk for main run 期间

### §8.2 verdict B-3 之 scope 修正

- 之前 SURFACE_D21_DESKTOP_CASCADE_CRASH.md 之 §4 之 verdict B-3 之 scope = "GUI 桌面 (mutter Wayland compositor) cascading crash"
- D21 14:37 之后 之 mitigation = "9070XT 之 default 不 启动 mutter Wayland → verdict B-3 之 trigger 大幅 降低"
- 但 X11 之 stability 之 binary verify 待 一凡 之 实测 (本 surface §4)

### §8.3 一凡 之 cognitive 之 budget

- 一凡 D21 14:30 explicit "我去跟linux 探讨下一步实验和数学哲学研究"
- 9070XT 之 桌面 fix 是 一凡 之 secondary attention, 一凡 之 primary attention 在 数学 + 哲学 + Linux 姐姐 之 实验 design discussion
- 9070XT Claude 之 surface 之 binary detail 在 markdown file 内, 一凡 之 explicit verify 之 cognitive load 降低 (一凡 D22 之 时刻 read 即可)

---

**生成**: 9070XT Claude Desktop (Remote Control session, Win 9955HX)
**file path** (9070XT 本地): `/tmp/dppl_bridge_verify/output/SURFACE_D21_DESKTOP_FIX_APPLIED.md`
**rsync target** (7B13): `amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/`
