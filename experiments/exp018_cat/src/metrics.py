"""
metrics.py — Shumailov baseline 复现的指标计算.

paper 引用项:
  - 主指标: perplexity on wikitext-2 test set (Figure 10)
  - Figure 11: per-sequence perplexity histogram, evaluated by generation 0 model
  - sub-agent 加 distinct-1/2/3 (mode coverage proxy, paper 未做)
  - bootstrap CI (paper 给 5-seed mean ± std, 我们 3 seed + bootstrap)
"""
from __future__ import annotations

import logging
import math
from collections import Counter

import numpy as np
import torch
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer

logger = logging.getLogger(__name__)


@torch.no_grad()
def compute_perplexity_on_dataset(
    model_path: str,
    tokenizer_id: str,
    dataset: Dataset,
    *,
    block_size: int = 64,
    batch_size: int = 8,
    fp16: bool = True,
    device: str | None = None,
) -> dict[str, float]:
    """
    在 dataset (block 化, input_ids 64-token) 上计算 mean perplexity.

    paper 严格 cite (Figure 10 caption):
      "Performance of OPT-125m models of different generations evaluated using
       the original wikitext2 test dataset."

    返回 {"mean_loss", "mean_perplexity", "n_blocks"}.
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    dtype = torch.float16 if fp16 else torch.float32
    model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=dtype).to(device)
    model.eval()

    losses = []
    n = len(dataset)
    for batch_start in range(0, n, batch_size):
        batch_end = min(batch_start + batch_size, n)
        batch = dataset[batch_start:batch_end]
        input_ids = torch.tensor(batch["input_ids"], dtype=torch.long).to(device)
        attention = torch.tensor(batch["attention_mask"], dtype=torch.long).to(device)
        labels = input_ids.clone()
        labels[attention == 0] = -100

        out = model(input_ids=input_ids, attention_mask=attention, labels=labels)
        # HF Trainer 计算的 loss 是 batch 平均 token loss; 我们累计 token-level
        n_tokens = (labels != -100).sum().item()
        losses.append((out.loss.item(), n_tokens))

    total_loss = sum(l * n for l, n in losses)
    total_tok = sum(n for _, n in losses)
    mean_loss = total_loss / total_tok if total_tok > 0 else float("inf")
    ppl = math.exp(mean_loss) if mean_loss < 20 else float("inf")

    del model
    if device.startswith("cuda"):
        torch.cuda.empty_cache()

    return {"mean_loss": mean_loss, "mean_perplexity": ppl, "n_blocks": n}


@torch.no_grad()
def compute_per_sequence_perplexity(
    model_path: str,
    tokenizer_id: str,
    dataset: Dataset,
    *,
    batch_size: int = 8,
    fp16: bool = True,
    device: str | None = None,
) -> np.ndarray:
    """
    paper Figure 11: 用 generation 0 model 评估每个生成 sequence 的 perplexity.
    返回 shape (n_blocks,) 的 numpy array (per-block ppl).
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    dtype = torch.float16 if fp16 else torch.float32
    model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=dtype).to(device)
    model.eval()

    per_seq_ppl = []
    n = len(dataset)
    for batch_start in range(0, n, batch_size):
        batch_end = min(batch_start + batch_size, n)
        batch = dataset[batch_start:batch_end]
        input_ids = torch.tensor(batch["input_ids"], dtype=torch.long).to(device)
        attention = torch.tensor(batch["attention_mask"], dtype=torch.long).to(device)

        # 单 sample 维度 loss: 跑 logits 然后手算 cross-entropy 不平均
        outputs = model(input_ids=input_ids, attention_mask=attention)
        logits = outputs.logits  # (B, T, V)
        # shift
        shift_logits = logits[:, :-1, :].contiguous()
        shift_labels = input_ids[:, 1:].contiguous()
        shift_attn = attention[:, 1:].contiguous()

        loss_fn = torch.nn.CrossEntropyLoss(reduction="none")
        per_token_loss = loss_fn(
            shift_logits.view(-1, shift_logits.size(-1)),
            shift_labels.view(-1),
        ).view(shift_labels.shape)
        per_token_loss = per_token_loss * shift_attn.float()

        n_tokens = shift_attn.sum(dim=1).clamp(min=1)
        seq_loss = per_token_loss.sum(dim=1) / n_tokens
        seq_ppl = torch.exp(seq_loss.clamp(max=20)).cpu().numpy()
        per_seq_ppl.extend(seq_ppl.tolist())

    del model
    if device.startswith("cuda"):
        torch.cuda.empty_cache()

    return np.array(per_seq_ppl)


def compute_distinct_n(texts: list[str], n: int) -> float:
    """
    distinct-n = unique n-grams / total n-grams.
    Mode coverage proxy: 越低表示 mode collapse 越严重 (paper §5.1 GMM 类比).
    [paper 未做 distinct-n, sub-agent 自加]
    """
    total = 0
    unique = Counter()
    for t in texts:
        tokens = t.split()
        if len(tokens) < n:
            continue
        for i in range(len(tokens) - n + 1):
            gram = tuple(tokens[i : i + n])
            unique[gram] += 1
            total += 1
    if total == 0:
        return 0.0
    return len(unique) / total


def bootstrap_ci(
    samples: np.ndarray,
    *,
    n_bootstrap: int = 1000,
    ci: float = 0.95,
    seed: int = 0,
) -> tuple[float, float, float]:
    """
    bootstrap CI: 返回 (mean, lower, upper).
    用于 3-seed 的 perplexity 聚合 (paper 用 5-seed mean±std, 我们 3-seed + bootstrap).
    """
    rng = np.random.default_rng(seed)
    n = len(samples)
    means = []
    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, size=n)
        means.append(samples[idx].mean())
    means = np.array(means)
    alpha = (1 - ci) / 2
    return (
        float(samples.mean()),
        float(np.quantile(means, alpha)),
        float(np.quantile(means, 1 - alpha)),
    )


def falsification_check(
    gen0_ppl: float,
    gen9_ppl: float,
    no_preserve_gen9: float | None = None,
    preserve_10pct_gen9: float | None = None,
) -> dict[str, dict]:
    """
    binary falsification check (Shumailov 2024 baseline 复现):

    F1: gen9_ppl < gen0_ppl + 5 → 自迭代崩溃未复现 → 反 paper.
    F2: no_preserve_gen9 不显著高于 preserve_10pct_gen9 → "10% 缓解" 未复现.
    F3: gen0_ppl > 50 → fine-tune setup 本身有问题 (paper baseline 34).
    """
    result = {
        "F1_collapse_reproduced": {
            "passed": gen9_ppl >= gen0_ppl + 5,
            "gen0_ppl": gen0_ppl,
            "gen9_ppl": gen9_ppl,
            "delta": gen9_ppl - gen0_ppl,
            "criterion": "gen9_ppl >= gen0_ppl + 5",
        },
        "F3_fine_tune_sanity": {
            "passed": gen0_ppl <= 50,
            "gen0_ppl": gen0_ppl,
            "criterion": "gen0_ppl <= 50 (paper: 34)",
        },
    }
    if no_preserve_gen9 is not None and preserve_10pct_gen9 is not None:
        result["F2_preserve_helps"] = {
            "passed": no_preserve_gen9 > preserve_10pct_gen9,
            "no_preserve_gen9": no_preserve_gen9,
            "preserve_10pct_gen9": preserve_10pct_gen9,
            "criterion": "no_preserve > preserve_10pct",
        }
    return result
