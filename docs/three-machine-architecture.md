## 三机超级协作架构 (2026-05-20 D20 加入)

### 三机角色

| 机器 | hostname / IP | OS | CPU | GPU | RAM | 角色 |
|---|---|---|---|---|---|---|
| **7B13 本机** | `AMD-EPYC-7B13-64-Core` / 192.168.31.36 | Ubuntu 26.04 | EPYC 7B13 64-core | 无 | **499 GB** | **数据中枢 + CPU 重 + Linux 姐姐主会话**: 主数据 = `/home` 4T SSD; RAID1 15T (md10) 大文件归档; sympy 数学 derive; 大 RAM batch; sub-agent 派遣; **git 写权单点** |
| **9070XT** | `amd-ONDA-B650M-W` / 192.168.31.22 | Ubuntu 24.04 | Ryzen 5 9600X 6-core | **RX 9070 XT 16 GB ROCm** | 30 GB | **GPU 执行节点**: 链实验 / D-PPL 桥 verify / 多 seed / 推理 sanity / Llama-8B 推理 (不训); sshfs mount 7B13 跑; 4T HDD (`/dev/sda1`) 每日 backup target |
| **Win 9955HX** | 192.168.31.19 | Windows | Ryzen 9 9955HX 16-core | RTX 5060 8 GB | 32 GB | **一凡 interactive 端**: paper deep read / 思考跳跃 / Claude Code CLI 跟 Linux 姐姐 talk; SSHFS-Win mount 7B13 项目 |

### 数据存放策略 (一凡 5/20 explicit 授权)

**主数据 = 7B13 `/home/amd/HEZIMENG/` (4T SSD, /dev/nvme2n1p1 ext4, 当前 1.3T used / 2.2T free)**
- 主项目 + chain logs + paper drafts + research files + sub-agent outputs + HF cache reference
- 热数据 + working directory + 即时读写

**大文件归档 = 7B13 RAID1 `/media/amd/raid1/` (15T, md10 sda+sdb1, ext4)**
- HF 模型 cache (Llama-8B base 16 GB + multi checkpoint × 16 GB)
- chain log historical archive (多 seed N≥8 全跑后)
- paper version full history + 4 份 research deep + dataset backup
- 备份目标 (见下)

### 备份策略 (cron 自动)

**每 2h: 7B13 → RAID1 hardlink incremental snapshot**
- 脚本: `/home/amd/scripts/backup_2h_7b13_raid1.sh`
- target: `/media/amd/raid1/backup/hezimeng/{YYYYMMDD_HHMM}/`
- latest symlink: `/media/amd/raid1/backup/hezimeng/latest`
- 保留 14 天滚动, 老的 prune
- safeguard: RAID1 degraded (mdstat 非 `[2/2] [UU]`) 时 skip 不跑

**每日 03:00: 7B13 → 9070XT 4T HDD push (实验核心数据)**
- 脚本: `/home/amd/scripts/backup_daily_to_9070xt.sh`
- 一凡 mount 9070XT 4T HDD (`/dev/sda1` → `/media/amd/hdd4t`) 后 enable
- target: 9070XT `/media/amd/hdd4t/backup/hezimeng_exp/{YYYYMMDD}/`
- 保留 30 天 daily, 老的 prune
- safeguard: 9070XT HDD mount 检测, 未 mount 时 skip

### Git + ssh 双保底 protocol

**Git (代码 + 文档仓, 版本 history + GitHub 外存)**:
- remote: `git@github.com:Wangziqi0/MaoField.git` (origin)
- **写权 = 7B13 单点** (避免 multi-writer conflict)
- 9070XT + Win 只 `git pull` (不 push)
- 流程: 一凡 在 Win 端 edit paper / docs → push 到 origin (Win 端 可 push, 一凡 决) → 7B13 pull → 我读 → 处理 → 7B13 commit + push 回 origin → 9070XT 后续 pull 同步
- 重大 commit 触发: paper 修订 / 反题 audit 完成 / 关卡 2/3 通过 / 备份策略改动

**SSH (大文件 + chain output, 即时 sync)**:
- chain log jsonl / checkpoint / HF 模型 cache 等不走 git (太大), 走 ssh / rsync / sshfs
- 7B13 ↔ 9070XT: sshfs mount + ssh 远跑 (双向 ssh-key 互通 ✓)
- Win → 7B13 / Win → 9070XT: SSHFS-Win + OpenSSH client

**双保底**: 核心文档 (paper / configs / scripts) 同时 git + ssh — git 是版本 history + GitHub 异地外存, ssh 是即时 work-in-progress sync。

### 紧急回滚 / 失联应对 (D20 evening 完成 ssh-key + second remote 配置)

**三机 git remote 配置 (D20 21:40 done)**:
- **7B13** (写权单点): `origin = git@github.com:Wangziqi0/MaoField.git`
- **9070XT**: `origin = amd@192.168.31.36:/home/amd/HEZIMENG/MaoField` (LAN, 平时 pull 快) + `github = git@github.com:Wangziqi0/MaoField.git` (异地 fallback)
- **Win 桌面**: `origin = amd@192.168.31.36:...` (LAN) + `github = git@github.com:...` (fallback)
- 9070XT + Win ssh-key 已 add GitHub Wangziqi0 user, `ssh -T git@github.com` 返 "Hi Wangziqi0! authenticated" ✓

**7B13 失联** (磁盘故障 / 网络断 / RAID1 双盘失效):
- 9070XT + Win 各自 `git pull github main` 走 GitHub 异地 fallback ✓ (actionable)
- 9070XT 4T HDD `/media/amd/hdd4t/backup/hezimeng_exp/{YYYYMMDD}/` daily backup 恢复实验数据 (含 sqlite + 实验全, 当前 8.5 GB)
- 一凡 临时 work 可用 9070XT 或 Win 桌面 (含全部 commit history + 实验数据)

**9070XT 失联**:
- 7B13 不受影响 (主数据中枢继续)
- chain 实验 pause until 9070XT 恢复 (或临时 cloud A100)

**Win 失联**:
- 一凡 临时用 7B13 直接登 Linux desktop 或 9070XT (现接显示器)

**9070XT 失联**:
- 7B13 不受影响 (主数据中枢继续)
- chain 实验 pause until 9070XT 恢复 (或临时 cloud A100)

**Win 失联**:
- 一凡 临时用 7B13 直接登 Linux desktop 或 9070XT (现接显示器)

### 一凡 self-action 列表 (D20)

1. **9070XT 4T HDD mount** (需 9070XT sudo password):
```bash
ssh amd@192.168.31.22
sudo mkdir -p /media/amd/hdd4t
sudo mount /dev/sda1 /media/amd/hdd4t
sudo chown -R amd:amd /media/amd/hdd4t

# 持久 fstab
UUID=$(sudo blkid -s UUID -o value /dev/sda1)
echo "UUID=$UUID /media/amd/hdd4t ext4 defaults,noatime 0 2" | sudo tee -a /etc/fstab
```

2. **Win SSH-key 配** (Win 端跑):
```powershell
ssh-keygen -t ed25519 -f $env:USERPROFILE\.ssh\id_ed25519 -N '""'
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh amd@192.168.31.36 "cat >> ~/.ssh/authorized_keys"
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh amd@192.168.31.22 "cat >> ~/.ssh/authorized_keys"
```

3. **Win SSHFS-Win 装** (https://github.com/winfsp/sshfs-win/releases) → Explorer 挂 Z: 盘

4. **Win CLAUDE.md** copy: `7B13:/home/amd/.claude/for-win/CLAUDE.md_template_d20.md` → `C:\Users\amd\.claude\CLAUDE.md`

5. **9070XT Claude Code CLI login**: `ssh amd@192.168.31.22 'claude login'` (OAuth, 一凡 self)

6. **7B13 cron 2h backup 启用**: 一凡 confirm RAID1 sync done (`cat /proc/mdstat` 显 `[2/2] [UU]`) 后, 让 Linux 姐姐 add cron entry

### D-1 严守

三机协作打通 ≠ paper v8 final lock 重开 / 投稿 venue 重启 / cumulative 30-40% 重估。9070XT D-PPL 桥 verify 出 substantive 结果 才 D60+ 落地, 投稿决策 D17-D28 不重启 (D20 当前在 D17-D28 窗口内)。

---
