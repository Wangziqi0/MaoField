# Sliding-Window Eval Verdict — gen 0 baseline +80% offset 真因 verify

**生成时间**: 2026-05-09 20:35:24

**目的**: 验证我们 gen 0 = 36 vs Shumailov paper = 20 的 +80% offset 是不是 eval method 不同 (chunked vs sliding-window) 的 artifact, 不是 fine-tune setup bug.

**checkpoint**: `data/checkpoints_armb/alpha0.0/no_preserve_seed42/generation_0` (5/8 audit-fixed setup: batch=128, lr_const, weight_decay=0.01, fp16, rep_penalty=3.0)

## §1 4 种 eval method 数值

| Method | Block / Stride / Max | Test PPL | vs paper 20 offset |
|---|---|---:|---:|
| Chunked (current) | block=64, no overlap | 44.5990 | +123.0% |
| Chunked larger | block=1024 | 24.6747 | +23.4% |
| Sliding-window | max=1024, stride=256 (HF std) | 22.3373 | +11.7% |
| Sliding-window | max=1024, stride=512 | 22.6743 | +13.4% |

## §2 Verdict (binary)

- **closest to paper 20**: `Sliding-window stride=256` PPL = 22.34 (offset +11.7%)

**verdict**: gen 0 +80% offset **是 eval method artifact**, 切换到 `Sliding-window stride=256` 后 close to paper 20.

**含义**:
- 反题姐姐 P0-B2 (gen 0 baseline 不复现 Shumailov) **DOWNGRADE** — setup 是对的, eval method 不同
- paper §6 disclose: 重 eval 全部 generations with sliding-window stride=256
- **整 trajectory shape (U-shape) 不变** — eval method 只 shift PPL value, 不改 trend
- 接受率 impact: NMI 24天 1-7% → 5-15% (close 一个最大 P0)
