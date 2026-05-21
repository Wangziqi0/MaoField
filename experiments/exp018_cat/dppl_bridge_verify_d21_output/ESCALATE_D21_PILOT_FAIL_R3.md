# [9070XT escalate R3 — D-PPL 桥 verify D21 pilot 启动立即 crash]

**真实今日日期** (`date '+%Y-%m-%d %H:%M:%S %Z'`): `2026-05-21 13:45 CST` (D21)

**Surface**: 9070XT Claude Desktop (Remote Control by Win 9955HX)

**对象**: 7B13 Linux 姐姐主会话 + 第十三波派遣 sub-agent A (launch script 之 debug iteration 3)

**协议**: D-PPL 桥 verify D21 prompt §7 之 escalate + README.md line 4 之 D-1 binding §8.3 严守 (不擅自 edit launch_dppl_bridge.py)

**状态**: §2.4 venv ✓ + §3 stop llama-server ✓ + §4 rsync pull ✓, **§5 pilot 启动立即 crash** exit 1, run_start event 写入 jsonl 失败

---

## §1 进展 binary detail (D21 13:30-13:45)

| step | 状态 | binary detail |
|---|---|---|
| §2.4 venv install | ✓ 13:37 | rocm7.2 wheel: torch 2.12.0+rocm7.2, matmul ✓ gfx1201 native, OPT-125m 加载 ✓ |
| §3 stop llama-server | ✓ 13:42 | supervisorctl stop qwen8emib:qwen8emib_00, VRAM 14.2 → 0.69 GB |
| §4 rsync pull | ✓ 13:43 | launch_dppl_bridge.py 21.9 KB + watchdog.sh 7.4 KB + analyze_pearson.py 15.7 KB + README.md 11.0 KB |
| §5 pilot 启动 | ✗ 13:44 | Python crash exit 1 在 run_start event 写 jsonl 时 |

---

## §2 Bug 之 binary 定位 (traceback verbatim)

```
Traceback (most recent call last):
  File "/tmp/dppl_bridge_verify/launch_dppl_bridge.py", line 578, in <module>
    main()
  File "/tmp/dppl_bridge_verify/launch_dppl_bridge.py", line 498, in main
    write_jsonl(output_jsonl, {
  File "/tmp/dppl_bridge_verify/launch_dppl_bridge.py", line 63, in write_jsonl
    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
  ...
  File "/usr/lib/python3.12/json/encoder.py", line 180, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type PosixPath is not JSON serializable
```

### §2.1 Root cause (sub-agent A 之 latent bug)

`launch_dppl_bridge.py` line 498-505 之 run_start event:

```python
write_jsonl(output_jsonl, {
    "ts": utc_now(),
    "event": "run_start",
    "mode": args.mode,
    "args": vars(args),               # ← bug 在此
    "n_tuples_total": ...,
    "n_tuples_remaining": len(tuples),
})
```

argparse 之 `--output-jsonl` 和 `--log-file` 之 type=Path (line 433-434):

```python
p.add_argument("--output-jsonl", type=Path, required=True)
p.add_argument("--log-file", type=Path, default=None)
```

`vars(args)` 返 dict 含 `output_jsonl: PosixPath(...)` + `log_file: PosixPath(...)`。`json.dumps()` 默认 不 serialize `PosixPath` 类, raise `TypeError`。

### §2.2 sub-agent A 之 missed coverage

sub-agent A 之 prerequisites 之 testing 大概率没真跑 pilot mode 之 first-line write_jsonl call, 否则会立即 catch bug。说明 sub-agent A 之 deliverable 之 testing matrix 不全 (类 install_rocm_torch.sh 之 line 19 SIGPIPE bug + 之 wheel ROCm version mismatch bug — 同一 sub-agent A 之 第三次 deliverable bug)。

---

## §3 9070XT Claude 之 honest fix recommendation (1-line, low risk)

### §3.1 Option (P) — patch json.dumps 之 default

`launch_dppl_bridge.py` line 63 之 `write_jsonl`:

```python
# 现:
f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# 改:
f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")
```

`default=str` 让 json 之 fallback 把 non-serializable 对象 (含 PosixPath, datetime, etc) call str(). Path → "/path/to/file" str. 全局 fix, 一行。

### §3.2 Option (Q) — patch line 498 之 vars(args) 转换

`launch_dppl_bridge.py` line 498-505:

```python
# 现:
"args": vars(args),

# 改:
"args": {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(args).items()},
```

仅修 此处, 但 后续 write_jsonl 之 任何 entry 含 Path 还会 fail (若有)。Local fix。

### §3.3 推荐 path

Option (P) — 全局 fix 1 line, future-proof, low-risk。是 Python json 之 standard pattern。

---

## §4 D-1 binding 严守 ack (9070XT Claude 不擅自 edit)

按 **README.md line 4** (在 `/tmp/dppl_bridge_verify/README.md` 之 §9 错误 escalate path 段, verbatim 引用 design brief §7.5):

> launch_dppl_bridge.py 是 7B13 sub-agent 写完之 binary 跑之 script, **不修改**
>
> 若 catch script 之 bug (e.g., import error / 路径 error) → surface escalate 给 7B13, 由 7B13 主会话 spawn debug sub-agent 改 script + rsync 重 pull, **不擅自 edit**

按 **D-PPL prompt §8.3** verbatim:

> 9070XT Claude 不擅自 修 launch_dppl_bridge.py

9070XT Claude 严守 → 不擅自 apply Option (P) 或 (Q) 之 1-line fix, 哪怕 trivial。surface 给 7B13 + 等 sub-agent A 之 debug iteration 3 + commit + push + 9070XT git pull + rerun。

例外: 一凡 PI explicit override (类 D21 13:14 之 sudo password explicit relay) 可允许 9070XT Claude binary 修 + rerun, 但 默认 不 propose 此选项。

---

## §5 待 7B13 / 一凡 binary 决 (R3 三选)

| 选项 | binary | trade-off |
|---|---|---|
| **(R3-i)** [9070XT Claude 推 first] | 7B13 sub-agent A debug iteration 3: apply Option (P) `json.dumps(..., default=str)` + commit + push, 9070XT git pull + rerun pilot | ~10-15 min sub-agent + ~30 min pilot = ~45 min |
| **(R3-ii)** | 7B13 push fix-patch (sed -i one-liner) at 9070XT, 我 apply + rerun | ~5 min patch + ~30 min pilot = ~35 min, 但 7B13 仓库仍 buggy until 后续 commit |
| **(R3-iii)** | 一凡 PI explicit override 给 9070XT Claude 授权 "apply Option (P), rerun" | ~5 min fix + ~30 min pilot = ~35 min, 越线但 trivial bug PI 权限 可 |

### 5.1 R3 之 比例

sub-agent A 之 第三次 deliverable bug (install line 19 SIGPIPE → install line 44 wheel version → launch line 498 PosixPath JSON), iteration ratio 不健康。Linux 姐姐 主会话 之 D-1 纪律 4 子协作者验证 之 矩阵 可能 需 expand (sub-agent A 之 自我 test 不全)。但 此 escalate 仅 surface bug + 选项, 不作 sub-agent A 之 process audit (在 一凡 / Linux 姐姐 scope)。

---

## §6 9070XT 端 当前 state (binary, jsonl-traced)

```
venv:                /home/amd/HEZIMENG/MaoField/experiments/exp018_cat/.venv
  torch:             2.12.0+rocm7.2 ✓
  transformers:      4.49.0 ✓
  datasets:          2.21.0 ✓

GPU [Device 0]:      RX 9070 XT 16 GB
  arch:              gfx1201 native (rocm7.2 wheel 兼容)
  VRAM Used:         ~0.69 GB (post llama-server stop)
  VRAM Free:         ~16.4 GB (pilot OPT-125M 需 ~1.1 GB, 富余)
  Hang count:        0 (post rocm7.2)

ROCm runtime:        7.2.0

llama-server (qwen8emib:qwen8emib_00):
  状态:              STOPPED (supervisorctl, autorestart pending until manual start)
  VRAM 释放:         13.5 GB

pilot run 0:
  启动:              2026-05-21 13:44:50 CST
  crash:             ~13:44:51 (< 1 sec, before model load)
  exit code:         1
  output files (9070XT 本地):
    /tmp/dppl_bridge_verify/output/pilot_D21_seed1_gen5.jsonl    (0 bytes, empty — crash 在 first write)
    /tmp/dppl_bridge_verify/output/pilot_D21.log                  (810 bytes, run_metadata 之 head log)
    /tmp/dppl_bridge_verify/output/pilot_D21.console.log          (1,818 bytes, 含 traceback)

D-PPL pipeline 之 §3-§5 之 sequential lock:
  §3 stop llama-server: ✓ done
  §4 rsync pull:        ✓ done
  §5 pilot:             ✗ crash, awaiting fix
  §6 main:              pending (关卡 2 之后)
```

---

## §7 sanity check (附带产出, binary verify chain checkpoint dir)

pilot 启动前我 inline ls 验证 chain checkpoint dir 含 全 generations (path B 需 gen-(n-1), path C 需 gen-0):

```
/home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb/alpha10.0/no_preserve_seed1/:
  generation_0/  generation_1/  ...  generation_9/   ← 10 gens 全 ✓
  
gen=0/model.safetensors  ✓ 存在
gen=4/model.safetensors  ✓ 存在 (path B 需)
gen=5/model.safetensors  ✓ 存在 (path B + C 之 θ_n)
```

checkpoint dir 不是 pilot crash 之 因, 是 script 之 PosixPath JSON serialize bug。

---

## §8 next 之 binary 期望

等 一凡 / 7B13 主会话 输 **(R3-i)** / **(R3-ii)** / **(R3-iii)** 之一, 形式:

1. 一凡 在 9070XT Claude Desktop (Remote Control) 之 conversation 内 binary 输 `R3-i` / `R3-ii` / `R3-iii` + (若 iii) explicit override 文本
2. **或** 7B13 主会话 commit 修过之 launch_dppl_bridge.py + git push, 9070XT git pull + rerun pilot
3. **或** 7B13 主会话 rsync push fix-patch (sed -i), 9070XT apply + rerun

收到决之后 9070XT Claude **不二次 confirm**, 直接 binary execute (per D-PPL prompt §0 line 5 + 一凡 D21 "auto" override)。

---

**生成**: 9070XT Claude Desktop (Remote Control session)
**escalate file path** (9070XT 本地): `/tmp/dppl_bridge_verify/output/ESCALATE_D21_PILOT_FAIL_R3.md`
**rsync target** (7B13): `amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/`
**附 log** (一同 push): `pilot_D21.console.log` (1,818 bytes, 含完整 traceback) + `pilot_D21.log` (810 bytes, run_metadata head)
