"""
data_pipeline.py — wikitext-2 加载 + tokenize + 64-token block 化.

paper 严格 cite (Shumailov 2024 §5.2):
  "We block training sequences to be 64 tokens long; then for each token
   sequence in the training set, we ask the model to predict the next 64 tokens."

接口:
  load_wikitext2(cfg) -> DatasetDict (train / validation / test)
  tokenize_and_block(dataset, tokenizer, block_size) -> Dataset
  build_mixed_generation_dataset(real, synthetic, original_fraction, seed) -> Dataset
"""
from __future__ import annotations

import logging
import random
from pathlib import Path

from datasets import Dataset, DatasetDict, load_dataset
from transformers import PreTrainedTokenizerBase

logger = logging.getLogger(__name__)


def load_wikitext2(
    hf_id: str = "wikitext",
    hf_config: str = "wikitext-2-raw-v1",
    cache_dir: str | Path | None = None,
) -> DatasetDict:
    """
    加载 wikitext-2 raw v1.
    paper 严格 cite: "wikitext2 dataset" — §5.2
    [paper 未明示 raw vs v1 — sub-agent 默认 raw-v1; 与 OPT-125m BPE tokenizer 兼容性最高]

    返回 train / validation / test 三个 split.
    """
    logger.info("加载 wikitext-2 (%s/%s) cache_dir=%s", hf_id, hf_config, cache_dir)
    ds = load_dataset(hf_id, hf_config, cache_dir=str(cache_dir) if cache_dir else None)
    for k in ("train", "validation", "test"):
        if k not in ds:
            raise ValueError(f"split {k} 缺失, 实际 splits = {list(ds.keys())}")
        logger.info("  %s: %d 行", k, len(ds[k]))
    return ds


def _tokenize_function(examples: dict, tokenizer: PreTrainedTokenizerBase) -> dict:
    """逐行 tokenize, 不加 padding (block 化阶段处理)."""
    return tokenizer(examples["text"], add_special_tokens=False)


def _group_into_blocks(examples: dict, block_size: int) -> dict:
    """
    将连续 tokenize 结果切成 block_size 长度块.
    paper 严格 cite: "We block training sequences to be 64 tokens long" — §5.2
    标准 HF run_clm.py group_texts 实现.
    """
    concatenated = {k: sum(examples[k], []) for k in examples.keys()}
    total_length = len(concatenated[list(examples.keys())[0]])
    total_length = (total_length // block_size) * block_size
    result = {
        k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
        for k, t in concatenated.items()
    }
    result["labels"] = [list(ids) for ids in result["input_ids"]]
    return result


def tokenize_and_block(
    dataset: Dataset,
    tokenizer: PreTrainedTokenizerBase,
    block_size: int = 64,
    num_proc: int = 4,
) -> Dataset:
    """
    Tokenize + block 化. 输出每条样本是 (input_ids, attention_mask, labels)
    各长度 = block_size.
    """
    logger.info("tokenize 数据集 (%d 行) block_size=%d", len(dataset), block_size)
    tokenized = dataset.map(
        lambda ex: _tokenize_function(ex, tokenizer),
        batched=True,
        num_proc=num_proc,
        remove_columns=dataset.column_names,
    )
    blocked = tokenized.map(
        lambda ex: _group_into_blocks(ex, block_size),
        batched=True,
        num_proc=num_proc,
    )
    logger.info("  block 化后: %d 块", len(blocked))
    return blocked


def build_mixed_generation_dataset(
    real_train: Dataset,
    synthetic_train: Dataset,
    original_fraction: float,
    seed: int,
) -> Dataset:
    """
    paper 严格 cite (§5.2 末段, preserve_10pct condition):
      "every new generation of training, a random 10% of the original
       data points are sampled. The overall original [size preserved]"

    参数:
      real_train: 原始 wikitext-2 train (block 化后)
      synthetic_train: 上一代 model 生成的合成 train (block 化后)
      original_fraction: 0.0 (no_preserve) 或 0.10 (preserve_10pct)
      seed: 子样本采样种子

    返回 mix 后 dataset, 总量 = synthetic_train 大小 (paper:
      "produce an artificial dataset of the same size") + 加 random 10% 真实
      = 1.0 倍 + 0.10 倍 ≈ 1.10 倍? 还是 90% 合成 + 10% 真实 = 1.0 倍?
      paper §5.2 末: "10% of the original data points are sampled. The overall
      original" — 文字截断, 我们 default 解为
        总量保持 = 原 train 大小, 其中 10% 真实 + 90% 合成
      [paper 未完全明示, sub-agent 默认 总量 = synthetic 大小, 真实 10% 替换合成 10%]
    """
    rng = random.Random(seed)
    if original_fraction == 0.0:
        return synthetic_train

    target_total = len(synthetic_train)
    n_real = int(target_total * original_fraction)
    n_synth = target_total - n_real

    real_indices = rng.sample(range(len(real_train)), min(n_real, len(real_train)))
    synth_indices = rng.sample(range(len(synthetic_train)), min(n_synth, len(synthetic_train)))

    real_sub = real_train.select(real_indices)
    synth_sub = synthetic_train.select(synth_indices)

    from datasets import concatenate_datasets

    mixed = concatenate_datasets([real_sub, synth_sub]).shuffle(seed=seed)
    logger.info(
        "mix dataset: real=%d (%.1f%%) + synthetic=%d (%.1f%%) = %d 总",
        len(real_sub),
        100 * len(real_sub) / len(mixed),
        len(synth_sub),
        100 * len(synth_sub) / len(mixed),
        len(mixed),
    )
    return mixed


def get_text_strings_from_blocks(
    blocked: Dataset,
    tokenizer: PreTrainedTokenizerBase,
    max_samples: int | None = None,
) -> list[str]:
    """把 block 化的 input_ids 解码回字符串 (用于 distinct-n 计算)."""
    n = len(blocked) if max_samples is None else min(max_samples, len(blocked))
    return [tokenizer.decode(blocked[i]["input_ids"], skip_special_tokens=True)
            for i in range(n)]
