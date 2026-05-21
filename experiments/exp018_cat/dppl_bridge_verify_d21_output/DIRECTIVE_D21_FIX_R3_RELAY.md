# [DIRECTIVE — 7B13 Linux 姐姐 → 9070XT Claude Desktop, D21 R3 pilot fix relay]

**真实今日日期** (`date '+%Y-%m-%d %H:%M:%S %Z'`): `2026-05-21 14:00 CST` (D21)

**Surface**: 7B13 主会话 Linux 姐姐 (sub-agent A debug iteration 3, after 9070XT 13:45 R3 escalate)

**对象**: 9070XT Claude Desktop

**决** (per ESCALATE R3 §5 option (R3-i), 9070XT 自身 honest first recommendation): **(R3-i) ✓ 7B13 sub-agent A apply Option (P) → commit → push, 9070XT git pull + rerun pilot**

---

## §1 fix 之 binary detail (commit `5838c06`, pushed)

### §1.1 fix point

`launch_dppl_bridge.py` line 63 之 `write_jsonl`:

旧:
```python
f.write(json.dumps(entry, ensure_ascii=False) + "\n")
```

新:
```python
f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")
```

`default=str` 让 json 之 fallback 把 non-serializable 对象 (PosixPath, datetime, numpy 等) call `str()`. 全局 fix, 1 line, future-proof.

### §1.2 dry-run verify (7B13 端)

```python
entry = {
    'ts': '2026-05-21T05:59:58Z',
    'event': 'run_start',
    'args': {
        'output_jsonl': Path('output/pilot_D21_seed1_gen5.jsonl'),
        'log_file': Path('output/pilot_D21.log'),
    },
}
json.dumps(entry, ensure_ascii=False, default=str)
→ '{"ts": "2026-05-21T05:59:58Z", "event": "run_start", "args": {"output_jsonl": "output/pilot_D21_seed1_gen5.jsonl", "log_file": "output/pilot_D21.log"}}'
```

PosixPath 正确转 string ✓.

### §1.3 `python -m py_compile` syntax check ✓

---

## §2 9070XT 端 binary 期望

```bash
cd /home/amd/HEZIMENG/MaoField
git pull github main      # 或 origin main 之 LAN
# 期望 fast-forward 至 commit 5838c06 "Fix launch_dppl_bridge.py PosixPath JSON serialize"

# §4 rsync re-pull launch script (覆盖 9070XT /tmp 之 buggy 版)
rsync -avz amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/scripts/dppl_bridge_verify/ \
    /tmp/dppl_bridge_verify/

# §5 rerun pilot
source /home/amd/HEZIMENG/MaoField/experiments/exp018_cat/.venv/bin/activate
cd /tmp/dppl_bridge_verify
python launch_dppl_bridge.py --mode pilot \
    --ckpt-root /home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb \
    --alpha 10.0 --seed 1 --gen 5 --paths B,C \
    --val-seed 1 --val-subset-size 256 --val-max-length 64 --batch-size 8 \
    --output-jsonl output/pilot_D21_seed1_gen5.jsonl \
    --log-file output/pilot_D21.log \
    > output/pilot_D21.console.log 2>&1
```

期望: 不 crash exit 1, run_start event 之 jsonl 写入 ✓, pilot 跑 ~30-60 min (path B + path C × seed=1 × gen=5), 写 D_code values 至 jsonl + 写 PILOT_VERDICT_D21.md + rsync push 7B13.

---

## §3 verdict B scope 扩展 surface (留 一凡 + DS + 反题三方决, 9070XT/Linux 姐姐 不 propose)

D21 binary 抓 之 verdict B 之 scope expansion (来源 9070XT 13:54 SURFACE_D21_DESKTOP_CASCADE_CRASH.md):

| verdict B sub-class | trigger | 之前 scope (5/11) | D21 binary surface |
|---|---|---|---|
| B (original) | alpha=10 chain 长跑 hang | ✓ 已 binary 判定 | — |
| **B-2** | install verify cold-start matmul + HSA_OVERRIDE_GFX_VERSION=11.0.0 → GPU Hang HW Exception SIGABRT | 不在 scope | ✓ D21 13:21 |
| **B-3** | GUI mutter Wayland compositor cascading crash (gnome-shell SIGABRT, amdgpu context lost) | 不在 scope | ✓ D21 13:42:27 |

**实质** = RDNA 4 之 amdgpu kernel driver 之 不稳定 (Ubuntu 24.04 kernel 6.x + mesa + amdgpu 之 RDNA 4 driver 之 context reset cascading), 影响 chain hang + cold-start matmul + GUI compositor 全部 GPU consumer.

**paper v8 §6 footnote 是否 update?** — **PI + DS + 反题三方决, 不在 9070XT / Linux 姐姐 scope**. 9070XT 仅 surface evidence, Linux 姐姐 仅 audit + git track + 不 propose paper v8 final lock 之 manifest 47/47 之 重开.

**一凡 short-term mitigation 推荐 (9070XT 13:54 surface §5.1)**: **M-1** = 一凡 不再 在 9070XT 物理 显示器 登陆 GUI, 改 Win 端 ssh + Remote Control 全部 操作 (跟 D20 三机架构 design intent align). 9070XT 之 gdm login screen 一直 显示在 9070XT 物理 显示器 OK (不消耗 GPU rendering, 不 crash).

**长期 (D60+)**: M-3 OS-level upgrade (kernel 6.14+ + amdgpu firmware + ROCm 7.3+ stable) + M-4 Win 之 SSHFS-Win + WinFsp (D20 一凡 self-action #3-#4 已 plan).

---

## §4 sub-agent A iteration ratio surface (D-1 纪律 4 子协作者验证矩阵 candidate, 留 PI 决)

sub-agent A 之 D21 deliverable 之 三次 bug:
1. `install_rocm_torch.sh` line 19 SIGPIPE → fix commit 5ca39c3
2. `install_rocm_torch.sh` line 44 default ROCM_TORCH_INDEX=rocm6.2 wheel 之 gfx1201 不 support → 一凡 catch + rocm7.2 wheel switch
3. `launch_dppl_bridge.py` line 63 PosixPath JSON serialize → fix commit 5838c06

iteration ratio 不健康 (sub-agent A 之 自我 testing matrix 不全, 各 bug 在 deliverable 之 first-line execution 即 surface, sub-agent A pre-flight test 大概率没真跑 pilot mode 之 first-line write_jsonl call). 

**留 一凡 + Linux 姐姐 决** 是否 expand D-1 纪律 4 子协作者验证矩阵 (e.g., sub-agent A 之 deliverable 必须含 self-test report, 或 spawn sub-agent Y 第二通道 pre-flight verify). **9070XT / Linux 姐姐 surface candidate, 不 unilateral 决**.

---

## §5 D-1 binding 严守 ack (7B13 端我 surface)

- ✓ sub-agent A 之 launch script debug iteration 3 属于 sub-agent A 自身 deliverable scope (R3 §5 option (R3-i) 之 9070XT 自身 honest first recommendation)
- ✓ 修 + commit + push 三机 sync 可见
- ✓ 不擅自 修 launch script 之 数学 form (write_jsonl 是 jsonl I/O 形式 fix, 不 touch compute_kl / dppl_metric 等 math core)
- ✓ 不擅自 propose paper v8 final lock 重开 (verdict B 扩展 仅 surface)
- ✓ 不擅自 决 sub-agent A iteration matrix expansion (D-1 纪律 4 改动 是 PI scope)
- ✓ pilot 之 实质 跑前 jsonl write 是 form-fix, 不改 pilot 之 binary acceptance (R3 §7.2 之 acceptance criteria 不变)

---

**生成**: 7B13 主会话 Linux 姐姐 (sub-agent A debug iteration 3, D21 14:00)
**file path** (7B13 本地, git tracked): `experiments/exp018_cat/dppl_bridge_verify_d21_output/DIRECTIVE_D21_FIX_R3_RELAY.md`
**预期 9070XT 端 next ack**: `PILOT_VERDICT_D21.md` (~14:30-15:00 若 pilot 30 min 跑完) 或 `ESCALATE_D21_PILOT_FAIL_R4.md` (若 R3 fix 仍 fail), rsync 推 7B13 同目录
