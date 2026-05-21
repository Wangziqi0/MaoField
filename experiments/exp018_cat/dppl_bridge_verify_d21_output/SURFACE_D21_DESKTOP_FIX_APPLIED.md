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

---

## §9 [Linux 姐姐 D21 14:50 append — D22-D60+ 完整实验 handoff 给 9070XT]

**真实日期** (`date '+%Y-%m-%d %H:%M:%S %Z'`): `2026-05-21 14:50 CST` (D21)
**生成**: 7B13 主会话 Linux 姐姐
**对象**: 9070XT Claude Desktop (Remote Control by Win 9955HX 一凡接管)
**触发**: 一凡 D21 14:45 explicit 指令 "你在9070xt给你发的那个md末尾加上你要交接给他完成的所有实验, 把对应实验有关的7b13这边的文件位置 哲学数学物理实验 的md信息地址 交接过去 他负责完成现阶段我们需要的所有实验, 记得告诉他 三机协作 数据同步7b13 大数据放raid1, 还有让他派agent多次校验数据 随时多机合作"

---

### §9.1 总体 framing (一凡 14:30 commit 之 dialectical materialism 反映论)

研究方法 = **实践先行 + 实践 carry 哲学之高级组成 + model 映射出物质映像之数学** (毛之实践论 + 矛盾论 + 认识论 + 列宁反映论)

- 实践 (binary 跑 chain) 不是 pure empirical, carry 内因 (sub-agent 之 self-testing 矩阵 + chain config 之 design intent) + 外因 (9070XT 硬件 / ROCm runtime / Wikitext-2 / Llama-8B 之实际 state) 之 unified
- 数学 (D^code / m_eff / J_S / Pearson r / etc) **反映** model 之 物质映像, 不是 first-principles axiom-first derive
- 9070XT 之 binary deliverable 之 form 应符合此 framing: 跑 + 数据 + 反映, 不是 hypothesis-driven verify

paper v8 final lock (D17, 47/47 manifest) **不动**. 投稿 D29 arXiv + TMLR + KBS, cumulative 30-40% **不动**.

9070XT 之 scope = **chain 跑 + GPU 实验 + sub-agent 派遣 + 数据 push 7B13**, 不在 paper 写 / paper 战略 / 哲学判读 / 投稿决策.

---

### §9.2 三机协作 protocol (binding, 严守)

| 机器 | 角色 | 数据 |
|---|---|---|
| **7B13** (192.168.31.36, EPYC 64-core, 499 GB RAM, 4T SSD + 15T RAID1) | 数据中枢 + Linux 姐姐主会话 + 数学 derive + sub-agent 派遣 + **git 写权单点** | 主数据 `/home/amd/HEZIMENG/MaoField/` (4T SSD) + 大文件归档 `/media/amd/raid1/` (15T RAID1) |
| **9070XT** (192.168.31.22, RX 9070 XT 16 GB, 6-core, 30 GB RAM, 1.9T NVMe + 4T HDD) | **GPU 执行节点** + chain 实验 + sub-agent 多次校验 + ack rsync push 7B13 | chain log / checkpoint / venv 本地, 大数据 rsync 推 7B13 |
| **Win 9955HX** (192.168.31.19, RTX 5060, Ryzen 9 16-core, 32 GB RAM) | 一凡 interactive 端 + paper deep read + Claude Code 跟 Linux 姐姐 talk + 反题 spawn 之触发 | SSHFS-Win mount 7B13 (一凡 D20 self-action pending WinFsp) |

**核心 binding (3 条 + 1 数据策略)**:

1. **数据主同步 7B13** = chain log jsonl + sub-agent ack md + 实验数字 全部 rsync push 7B13 之 同目录 + git track. 不在 9070XT 本地 静默 保存 之独立 dataset.
2. **大数据放 RAID1** = 单文件 > 1 GB OR 总 dir > 5 GB 之 dataset (HF 模型 cache / Llama-8B checkpoint / chain log 历史归档 / 等), 一凡 + Linux 姐姐 决之 后 rsync 推 7B13 之 `/media/amd/raid1/` (15T) 不在 `/home/` 4T SSD.
3. **git 写权单点 = 7B13**. 9070XT 之 binary deliverable 之 commit + push 由 Linux 姐姐 (我) 单点完成. 9070XT 端 `git pull github main` 之 read-only, 不 `git push`.
4. **备份**: 7B13 → RAID1 每 2h hardlink incremental + 7B13 → 9070XT 4T HDD 每日 03:00 daily (待 一凡 D20-D21 self-action 之后 enable cron).

---

### §9.3 D22-D60+ 实验任务清单 (按 priority 排序)

#### §9.3.1 第一关键 — Phase 5 Llama-8B chain (D22-D26, $50 cloud A100 80GB)

**paper-level 价值**: paper v8.1 之 add 跨规模 systematic empirical pilot, 直接 close single-arch OPT-125M limitation 之一部分. 反映论 instantiate = 8B 之 chain training 实践 (carry 跨规模哲学组成) 之 数学 反映.

**timeline**: 一凡 D22 早 prep (1-2h) + D23 launch + D23-D26 跑 4 天

**资源**:
- $50 cost (RunPod A100 80GB spot $1.89/h × ~26h)
- HF Llama-3.1-8B-base license accept (一凡 D22 早 self-action)
- RunPod $60 credit + S3 backup bucket (一凡 D22 早 self-action)
- A100 80GB 必须 (不能用 A100 40GB — EMA 16 GB + activations + optimizer 之 footprint > 40 GB)

**9070XT 之 deliverable**:
1. **D22 早 之 sub-agent A spawn**: 写 `experiments/exp018_cat/scripts/phase5_llama8b/` 之 cloud launch script (chain config Llama-8B 版 cat_arm_b.yaml + 单 seed N=1 + 5-10 代 + α=10 二项 form). 用 RunPod CLI / API 之 schedule
2. **D23-D26 sub-agent A monitor**: 每 ~6h check + ack md push 7B13 + 大 checkpoint 之 rsync 策略 (S3 → 7B13 RAID1, 每代 checkpoint ~16 GB × 10 代 = ~160 GB → RAID1)
3. **D26 完成 之 ack md** + chain log jsonl rsync push 7B13

**7B13 端 reference 文件 (9070XT 先 git pull 拿到)**:
- `experiments/exp018_cat/literature/paper_v8_final_20260516.md` (162 KB, paper v8 final lock — chain config 之 source of truth, §3.5 之 binding form + §6.1 之 D^paper definition)
- `experiments/exp018_cat/literature/MAOFIELD_PROJECT_FULL_STATE_D17_20260517.md` (Phase 5 prep 之 5/19 一凡 final 决之 spec: $50 / 4 天 / A100 80GB / Llama-3.1-8B-base / SFT-only Wikitext-2)
- `experiments/exp018_cat/literature/ANTITHESIS_LAYER_PAPER_V8_FINAL_AUDIT_20260516.md` (反题 6 P0★ 之 P0★-B / P0★-C 候选 之 Phase 5 之 implication)
- `experiments/exp018_cat/cat_arm_b.yaml` (OPT-125M chain config baseline, Llama-8B 版 之 reference)
- `experiments/exp018_cat/scripts/train_one_generation.py` (chain training 主 script, EMA save 之 line 197 lacuna 需 fix for path A D60+, Phase 5 之 single chain 不需 fix)

**sub-agent 多次校验 mandate**:
- 9070XT 之 spawn Y 第二通道 pre-flight verify: cloud launch script 之 dry-run on 9070XT 之 local (CPU mode + tiny seed) → verify no PosixPath / SIGPIPE / 其他 first-line crash
- 每 checkpoint 之 数据 (D^code per gen + PPL per gen + EMA β 验证) 之 sub-agent 校验 → 写 verify ack md push 7B13

#### §9.3.2 第二关键 — D-PPL 桥主跑 (D22-D24, 在跑, 等 一凡 D22 早 `main launch ✓` 决)

**已部分 done**: D21 试运行 ✓ (D^code_B = 0.2962, D^code_C = 0.5900, factor-of-2 范围内)

**9070XT 之 deliverable** (D22 早 一凡 input `main launch ✓` 之后 9070XT 不二次 confirm execute):
- main run: `nohup bash watchdog.sh python3 launch_dppl_bridge.py --mode main --ckpt-root ... --alphas 0,10 --seeds 1,2,3,4 --gens 0,1,...,9 --paths B,C ...` 之 160 tuples × ~10 sec = ~25-30 min GPU + watchdog buffer
- 跑完 写 `MAIN_VERDICT_D22.md` + `main_D22_*.jsonl` rsync push 7B13

**7B13 端 reference 文件**:
- `experiments/exp018_cat/literature/DPPL_BRIDGE_VERIFY_EXPERIMENT_DESIGN_BRIEF_D21_20260521.md` (50 KB, sub-agent X 实验设计)
- `experiments/exp018_cat/literature/DPPL_BRIDGE_MATH_VERIFY_D21_20260521.md` (24 KB, sub-agent B 数学验证 — Pearson r 4 档阈值 + 真 binary close P0★-F 需 D60+ 路径 A 之 honest disclose)
- `experiments/exp018_cat/literature/DPPL_BRIDGE_9070XT_PROMPT_D21_20260521.md` (22 KB, prompt 详)
- `experiments/exp018_cat/scripts/dppl_bridge_verify/{launch_dppl_bridge.py, watchdog.sh, analyze_pearson.py, README.md}`

**main 跑完 之后 7B13 端 我 跑** `analyze_pearson.py` 之 Pearson r + bootstrap CI 95% (D24-D27).

#### §9.3.3 第三关键 — N≥8 multi-seed extension (D27-D40, P0★-C close 候选)

**paper-level 价值**: P0★-C ★★ FATAL close 候选 (v3→v8 之 PPL drift 43→54→48→48→55 之 post-hoc curve fitting 嫌疑 — 加 N=4 → N≥8 之 统计 power 之 增之 verify). 反映论 instantiate = 多种子 dialectical multi-instantiation.

**timeline**: D27 launch + ~1-2 周跑 (9070XT sequential to D-PPL 桥)

**9070XT 之 deliverable**:
1. **sub-agent A spawn 写 chain config**: 扩 `cat_arm_b.yaml` 之 seed=5/6/7/8 (4 个新 seed × α=0/10 × 10 代 = 80 chain run) 之 sequential launch script + watchdog 之 hang retry budget
2. **chain log + checkpoint push 7B13**: chain log jsonl 直接 推 7B13 之 `experiments/exp018_cat/data/checkpoints_armb_n8/` (主数据 7B13), checkpoint > 1 GB / dir > 5 GB 推 RAID1
3. **sub-agent 多次校验**: D-1 纪律 4 之 子协作者验证 = spawn Y 第二通道 之 chain log 之 sanity check (PPL gen 0 baseline ✓, α=10 plateau pattern 之 reproduce ✓, 之 dual-trace 之 confirm)

**7B13 端 reference 文件**:
- `experiments/exp018_cat/literature/paper_v8_final_20260516.md` (paper §6.1 之 关键数字 lock: α=10 plateau 55.97 SD 2.13 多种子 N=4, 之 N≥8 extension 之 power 增之 verify target)
- `experiments/exp018_cat/literature/ANTITHESIS_LAYER_PAPER_V8_FINAL_AUDIT_20260516.md` (反题 P0★-C 之 PPL drift 43→54→48→48→55 之 5 次 prediction reversal 之 honest disclose — N≥8 之 close target)

#### §9.3.4 第四关键 — Family 1b/1c/4/4' ablation (D27-D45, P0★-D deferred close 候选)

**paper-level 价值**: P0★-D 之 close (deferred) + Family 1a not unique 之 binary verify (5 family tied 4.5/5 partial C5).

**timeline**: D27-D45 (9070XT sequential to N≥8 OR parallel 第二 chain)

**9070XT 之 deliverable**:
1. **sub-agent A spawn 写 4 个 family variant config**: Family 1b (Σ_2 nested) / 1c (Σ_3 nested) / 4 (Volterra 三项 K=2) / 4' (Volterra 三项 K=3), 各 N=4 × α=10 × 10 代
2. chain log + checkpoint push 7B13
3. sub-agent 多次校验

**7B13 端 reference 文件**:
- `experiments/exp018_cat/literature/paper_v8_final_20260516.md` §4 (5 alternative families catalog 之 form spec)
- `experiments/exp018_cat/literature/MAOFIELD_PROJECT_FULL_STATE_D17_20260517.md` (Family ablation 之 5/19 PI plan)

#### §9.3.5 第五档 — 数学方向 first reproduce (D28-D60, paper v9/v10 之 起点)

**paper-level 价值**: 数学层 之 first substantive 反映 instantiate, 工具 5 Hartree LLM 域 first principles. 不在 D29 投稿 scope, 是 D60+ 之 paper v9 / v10 之 contribution.

按 priority:

1. **Banach LLM (Gauthier-Bach-Jordan 2026) reproduce** — P0★-A 候选 close, 数学 反映 model 之 Banach 算子之物质映像
2. **Mean-field transformer (Rigollet 2025) reproduce** — 数学 反映 transformer mean-field 行为
3. **Hartree LLM 12-layer transformer (Mei-Montanari 2018 instantiate)** — first LLM-domain Hartree closure 反映 instantiate
4. **NESS LLM (Liu-Tegmark 2025) reproduce** — 数学 反映 model NESS 实际行为

**9070XT 之 deliverable**:
- 9070XT 不 数学 derive (那是 7B13 我之 work), 9070XT 跑 reproduce 实验之 GPU instantiate verify (numerical match 之 binary)
- 7B13 端 我 spawn sub-agent 数学层 derive + push 给 9070XT 之 verify spec

**7B13 端 reference 文件 (待 D28 之时 spawn 数学 sub-agent 之产 之 detail derive)**:
- arxiv:2403.xxxxx Gauthier-Bach-Jordan 2026 (Banach LLM)
- arxiv:2502.xxxxx Liu-Tegmark 2025 (NESS LLM)
- arxiv:2501.xxxxx Rigollet 2025 (Mean-field transformer)
- arxiv:1806.10374 Mei-Montanari 2018 (Hartree mean-field NN, instantiate to transformer 之 D60+)

#### §9.3.6 第六档 — D60+ 长期工作 (不在 D29 投稿 scope, paper v10+ 起点)

- **D-PPL 桥 path A** (33 GPU-时 重训 EMA 之 SGD 回放, L1 严, P0★-F binary close)
- **F-1 阶段 2 剩 7 family** (Chern-Simons / Wess-Zumino / Ostrogradsky / Lifshitz / MSR / EFT / TQFT, 2-4 月)
- **multi-architecture** (Llama / Pythia / GPT-2 之 跨 arch chain)
- **multi-dataset** (Wikitext-2 + C4 + OpenWebText)
- **RLHF axis 真实证** (Constitutional AI, 2-3 月)
- **评估范式重定义** (本体论 dialectical reflective practice metric, 6-12 月 + Win 哲学协作)

---

### §9.4 7B13 reference 文件完整 mapping (按 layer)

#### 哲学 layer (一凡 14:30 commit 之 反映论 framing 之 source)

- `experiments/exp018_cat/literature/RESEARCH_LENIN_MAO_D19_20260519.md` (103 KB, 16 work, Lenin + Mao 之 反映论 + 实践论 + 矛盾论 + 认识论 source)
- `experiments/exp018_cat/literature/RESEARCH_MARX_ENGELS_D19_20260519.md` (88 KB, 8 work)
- `experiments/exp018_cat/literature/RESEARCH_ACADEMIC_D19_20260519.md` (42 KB, 30+ paper)
- `experiments/exp018_cat/literature/RESEARCH_MARXIST_D19_20260519.md` (44 KB, 8 work)
- `experiments/exp018_cat/literature/paper_v8_final_20260516.md` §1.3 (axiom 0 反映论) + §3.1 (axiom 1-7 矛盾 loss) + §7 (12 NOT-claim retract)

#### 数学 layer

- `experiments/exp018_cat/literature/paper_v8_final_20260516.md` §3 (axiom 1-7) + §4 (5 family catalog) + §5 (主定理) + §6 (m_eff 0.300±0.066 + J_S 三方法 0.772/0.535/0.329 + F3 -0.42 p=0.818 d=-0.125 + Reading 2 z=0.46σ)
- `experiments/exp018_cat/literature/DPPL_BRIDGE_MATH_VERIFY_D21_20260521.md` (24 KB, sub-agent B 之 D-PPL 桥 数学验证, β_θ^1460 ≈ 0.232 + Pearson r 4 档阈值 + 真 binary close 需 D60+ 路径 A 之 honest)
- `experiments/exp018_cat/literature/ANTITHESIS_LAYER_PAPER_V8_FINAL_AUDIT_20260516.md` (反题 6 P0★, 3 ★★ FATAL: B no-framework 等价 + C v3→v8 PPL drift + F D^code/D^paper mismatch)

#### 物理 layer (F-1 阶段 2 family uniqueness verify)

- `experiments/exp018_cat/literature/paper_v8_final_20260516.md` §4.2 (F-1 阶段 2 之 9 family universal uniqueness verify, U(1) Higgs + SU(N) YM 已 0/5 严格, 剩 7 family 推 D60+)

#### 实验 layer

- `experiments/exp018_cat/literature/MAOFIELD_PROJECT_FULL_STATE_D17_20260517.md` (D17 full state, chain 实验 之 5/11 partial D4 5/5 PASS STRONG ROBUST + 5/12 m_eff 多种子 + 5/17 code-first finding)
- `experiments/exp018_cat/cat_arm_b.yaml` (chain 实际跑之 二项 form config, λ_i=1 m_eff=1 K=1 β_kl=0.9 kl_update_every=10)
- `experiments/exp018_cat/scripts/train_one_generation.py` (chain training 主 script)
- `MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb/alpha{0.0,10.0}/no_preserve_seed{1,2,3,4}/generation_{0..9}/model.safetensors` (111 files ~63 GB, 现 N=4 chain checkpoints)

#### chain config / checkpoint layer

- `experiments/exp018_cat/data/checkpoints_armb/` (N=4 chain 跑过之 checkpoint, 主 7B13 数据 / 9070XT 静态副本)
- (待) `experiments/exp018_cat/data/checkpoints_llama8b/` (Phase 5 之 Llama-8B chain checkpoint, ~160 GB → RAID1)
- (待) `experiments/exp018_cat/data/checkpoints_armb_n8/` (N≥8 chain checkpoint)
- (待) `experiments/exp018_cat/data/checkpoints_family_ablation/` (Family 1b/1c/4/4' ablation checkpoint)

#### audit / sub-agent surface layer (本目录之 之前 D21 之 sub-agent 之 ack + escalate + surface 之全 audit trail)

- `experiments/exp018_cat/dppl_bridge_verify_d21_output/` (本目录, D21 共 17 文件: ACK_PREREQ + ESCALATE + DIRECTIVE + ACK_INSTALL_DONE + ESCALATE_R2 + ESCALATE_R3 + DIRECTIVE_R3 + PILOT_VERDICT + SURFACE_DESKTOP_CASCADE + SURFACE_DESKTOP_FIX_APPLIED + jsonl + log 等)

#### project-level binding layer

- `CLAUDE.md` (313 行, D-1 五条 + D-2 三线 + D-1 纪律 5 真实日期自检 + 三机超级协作架构, git tracked 三机一致)
- `/home/amd/CLAUDE.md` (用户级, 一凡 PI 规则 1-7 + 健康 binding + 学术严谨度)
- `/home/amd/.claude/CLAUDE.md` (全局, 中文严格执行)

---

### §9.5 sub-agent 多次校验 mandate (D-1 纪律 4 expand candidate, 一凡 14:45 explicit)

**9070XT 必 spawn sub-agent (类我 7B13 spawn X/Y/A/B) 多次校验数据**:

1. **每个 deliverable 之 pre-flight self-test**: launch script / chain config / data 之 binary dry-run on 9070XT 之 local 之 short epoch verify (e.g. Llama-8B cloud script 之 9070XT CPU mode + tiny seed dry-run, verify no first-line crash 之类 install line 19 SIGPIPE / launch line 63 PosixPath JSON 之 typo bug)
2. **每个 chain run 之 第二通道 verify**: spawn Y 之 sub-agent 之 chain log jsonl 之 sanity check (gen 0 PPL baseline ✓ + α=10 plateau pattern ✓ + 之 dual-trace 之 confirm + 之 异常 surface 即 escalate)
3. **每个数字之 binary jsonl trace**: 任何 surface 之数字 (D^code / PPL / m_eff / J_S / Pearson r / 等) 必 binary jsonl source 之 line 之 verbatim 引用. 无 placeholder. 无 ballpark approximation. 占位符禁令 严守.
4. **每个 ack md 之 7B13 rsync push** + git commit 之 audit trail. 全 D21 之 17 文件之 pattern 沿用.

**特别 D21 之教训** (sub-agent A 3 次 deliverable bug pattern, 见 PILOT_VERDICT_D21.md §10.2):
- install line 19 SIGPIPE (sub-agent A 没 真跑过 install script on 9070XT)
- install line 44 wheel ROCm version mismatch (sub-agent A 没 verify 9070XT 之 ROCm runtime 版本)
- launch line 63 PosixPath JSON (sub-agent A 没 真跑过 pilot mode first 10 line)

D21 教训 = sub-agent A 之 self-testing 矩阵之 expand mandate. 9070XT 之 后续 sub-agent A spawn 必 自带 pre-flight self-test report (类我之 D21 dry-run awk 校验之 pattern), 不交付未自跑过之 script.

---

### §9.6 多机合作 trigger protocol (D-2 三线 parallel 之 instantiate)

随时 cross-tension surface 之触发规则:

| trigger | 实时 ping |
|---|---|
| **数学 gap** (9070XT 之 sub-agent 跑数据 之后 之 catch — 与 paper §3 之 axiom 之 不一致) | 立即 rsync push surface md 至 7B13, ping Linux 姐姐 (我) 数学 derive layer 重算 (mean-field / NESS / Hartree / Banach) |
| **实验 unexpected** (9070XT 之 chain 跑出之数字 与 paper §6 之 lock 数字之 binary surface 不一致) | 立即 rsync push surface, ping 7B13 (我) → 7B13 (我) 之 ping Win (一凡 + Win 哲学层) |
| **哲学 reframe candidate** (chain 跑出之 实际行为 surface 之 dialectical 新组成 candidate) | rsync push 给 7B13, 7B13 (我) 之 ping Win (Win 之 work), 不 propose 自决 |
| **桌面 / OS-level instability** (类 D21 之 verdict B-3) | rsync push surface 给 7B13, 一凡 + Linux 姐姐 决之 mitigation, 不擅自 reboot |
| **资源 / cost surface** (类 cloud A100 spot 价波动 / 9070XT 显存 不够 / 等) | rsync push surface, ping 7B13 + 一凡 决之 |

**triggering 之 form**:
- 9070XT 之 surface md 之 file naming: `{TYPE}_{D-day-anchor}_{topic}.md` (e.g., `ACK_D22_PHASE5_LAUNCH.md`, `ESCALATE_D23_PHASE5_OOM.md`, `SURFACE_D27_MULTISEED_UNEXPECTED.md`)
- rsync target: `amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d{D-day-anchor}_output/` (or 新建之 per-stage output dir, e.g., `phase5_output/`)
- 7B13 (我) background monitor 该目录, 看到新 file 即 read + process + git commit + push + memory update + surface 一凡 (若 critical) or async work (若 routine)

---

### §9.7 9070XT 端 D-1 binding 严守 ack (refresh)

| binding | binary | 9070XT 严守 |
|---|---|---|
| D-1 纪律 1 (不等数据 不写声明) | 每数字 binary jsonl traced | ✓ |
| D-1 纪律 2 (48h 反馈真空 不存活) | 每 stage ~15-30 min surface 给 7B13 + 一凡 | ✓ |
| D-1 纪律 3 (代码 form 先于 paper form, 实践先于理论) | chain config 之 实际跑之 form > paper §3 之 form-borrow tier (D17 catch 之 instantiate) | ✓ (任何 chain run 之 数字 之 form 与 paper 之 不一致 surface 给 7B13, 不 隐藏) |
| D-1 纪律 4 (子协作者验证) | sub-agent 多次校验 (§9.5) | ✓ (D21 之教训 expand, 自带 pre-flight self-test report) |
| D-1 纪律 5 (错误 surface 不静默修正 + 真实日期自检) | 每 surface md 之 head 之 binary `date` 输出 verbatim + 全 错误 git track 不 hide | ✓ |
| 不擅自 reboot 9070XT | (一凡 explicit 之外不 reboot) | ✓ |
| 不擅自 sudo 决策性 op | (一凡 explicit 之外不 sudo, 一凡 ssh self-action OR explicit 之 password relay 例外) | ✓ |
| 不擅自 paper 写 / paper 战略 / 哲学判读 / 投稿决策 | 9070XT scope 之外, surface 给 7B13 + 一凡 + Win | ✓ |
| 不擅自 git push 7B13 单点写权 | (9070XT 仅 git pull github main, 不 push) | ✓ |
| 不擅自 launch 主跑 / Phase 5 / N≥8 / Family 之 各实验 (除非 一凡 explicit `main launch ✓` / `phase5 launch ✓` / 等之 binary input) | (9070XT 端 sub-agent 之 deliverable 之 chain launch 待 一凡 之 binary 决) | ✓ |

---

### §9.8 D22 早 一凡 之 双 input (期待 9070XT binary execute)

- (1) `main launch ✓` → 9070XT 立即 launch D-PPL 桥主跑 (160 tuples ~25-60 min)
- (2) `phase5 prep` (一凡 之后) + `phase5 launch ✓` → 9070XT spawn sub-agent A 写 cloud launch script + 一凡 verify 之后 RunPod launch

9070XT 之 standby 是 active (Remote Control conversation 保留, 不 exit). 一凡 D22 早 input 任一即 立即 execute.

---

### §9.9 一凡 14:30 之 framing 之 9070XT instantiate (binding)

实践 (binary 跑) + 哲学之高级组成 + model 映射出物质映像之数学 之 三层 unity 之 9070XT 端 instantiate:

- **chain 跑** (实践) carry sub-agent 之 self-testing 矩阵 (内因) + 9070XT 硬件 / ROCm runtime / cloud A100 之实际 state (外因) 之 unified
- **chain output 数字** (D^code / PPL / m_eff / 等) **反映** model 之 物质映像, 不是 first-principles axiom-first derive 之 verify
- **6 次 D21 实践纠正认识** (PILOT_VERDICT_D21.md §10 + 反映论 之 dialectical 之 D21 instantiate, 一凡 14:30 reframe) 之 pattern 沿用到 D22-D60+ — 不是 mechanical 之 "实践 vs 认识 二元 opposition", 是 unified dialectical 之 reflexive surface + 物质化 (git track + 记忆 + audit artifact)

---

### §9.10 当前 git state binary verify (D21 14:50)

| 机器 | git HEAD | 状态 |
|---|---|---|
| 7B13 (本机, 我跑此 handoff 之 mainline) | `ccaf80c` (本份 handoff append 之后 之 commit pending) | 写之时点 ✓ |
| 9070XT | `5be864d` | 滞后 2 个 commit (`28e8639` 试运行通过 + `ccaf80c` 桌面 fix). 9070XT 端 `git pull github main` 拿到 handoff 之后 ✓ sync |
| Win | (一凡 D22 早 自检) | 一凡 之 端不暴露 ssh server, 之 git pull github main 由 一凡 D22 早 self-action |

**重要**: 9070XT 拿到本 handoff 之 path = 一凡 D22 早 input `main launch ✓` 之前 OR 之后 之 9070XT 端 `git pull github main` (将 fast-forward 至 commit `c... pending` 之 latest).

---

**§9 生成**: 7B13 主会话 Linux 姐姐, D21 14:50 CST append
**触发**: 一凡 D21 14:45 explicit 指令
**git push 之后 9070XT 端 sync path**: `git pull github main` (fetch + fast-forward), 之后 `cat experiments/exp018_cat/dppl_bridge_verify_d21_output/SURFACE_D21_DESKTOP_FIX_APPLIED.md` 之 §9 含本 handoff content
