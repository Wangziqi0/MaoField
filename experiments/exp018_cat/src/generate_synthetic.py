"""
generate_synthetic.py — 用 fine-tune 后的 model 5-way beam-search 生成下代训练数据.

paper 严格 cite (§5.2):
  - "For data generation from the trained models we use a 5-way beam-search."
  - "for each token sequence in the training set, we ask the model to predict
    the next 64 tokens."
  - "We go through all of the original training dataset and produce an
    artificial dataset of the same size."
  - "Since we go though all of the original dataset and predict all of the
    blocks, if the model had 0.0 error it would produce the original
    wikitext2 dataset."

实现:
  - 输入: fine-tune 后的 model + 原 train block 化数据 (block_size=64)
  - 对每个 block, 用前 64 token 作 prompt, beam_search 生成下 64 token
  - 拼成 (prompt + generated) 组成下代训练数据 (依然 64-token block)

注意:
  paper 措辞 "for each token sequence ... predict the next 64 tokens" 含义微妙:
  解 1: 取每个 block 作 prompt, 生成下 64 tokens, 用 64 generated 作下代 sample
        (block_in → 64 generated → 1 new block)
  解 2: prompt + generated 拼起来 128 长度, 然后切回 64-block (产生 2 个 block)
  [paper 未完全明示, sub-agent 默认 解 1 — 与 "produce an artificial dataset
  of the same size" 一致 (input N blocks → output N synthetic blocks)]
"""
from __future__ import annotations

import logging
from pathlib import Path

import torch
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedTokenizerBase
from tqdm import tqdm

logger = logging.getLogger(__name__)


@torch.no_grad()
def generate_synthetic_dataset(
    model_path: str,
    tokenizer_id: str,
    real_train_blocks: Dataset,
    *,
    num_beams: int = 5,
    prompt_length: int = 64,
    max_new_tokens: int = 64,
    batch_size: int = 32,
    fp16: bool = True,
    device: str | None = None,
    repetition_penalty: float = 1.0,
) -> Dataset:
    """
    用 model_path 加载的 model 对 real_train_blocks 每个 block 跑 beam-search,
    返回 Dataset (input_ids, attention_mask, labels, 各 64-token block).

    paper 严格 cite: 5-way beam-search, prompt 64, predict next 64.
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info("device=%s 加载 model %s", device, model_path)

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    dtype = torch.float16 if fp16 else torch.float32
    model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=dtype).to(device)
    model.eval()

    n_total = len(real_train_blocks)
    logger.info("生成下代数据集 n_blocks=%d batch=%d num_beams=%d",
                n_total, batch_size, num_beams)

    synthetic_input_ids: list[list[int]] = []
    synthetic_attention: list[list[int]] = []

    for batch_start in tqdm(range(0, n_total, batch_size), desc="generate"):
        batch_end = min(batch_start + batch_size, n_total)
        batch_blocks = real_train_blocks[batch_start:batch_end]

        # 取前 prompt_length tokens 作 prompt
        prompts_ids = [
            torch.tensor(ids[:prompt_length], dtype=torch.long)
            for ids in batch_blocks["input_ids"]
        ]
        # left-pad 对齐
        max_p = max(p.shape[0] for p in prompts_ids)
        pad_id = tokenizer.pad_token_id
        padded_prompts = torch.full((len(prompts_ids), max_p), pad_id, dtype=torch.long)
        attn_mask = torch.zeros((len(prompts_ids), max_p), dtype=torch.long)
        for i, p in enumerate(prompts_ids):
            padded_prompts[i, max_p - p.shape[0]:] = p
            attn_mask[i, max_p - p.shape[0]:] = 1

        padded_prompts = padded_prompts.to(device)
        attn_mask = attn_mask.to(device)

        outputs = model.generate(
            input_ids=padded_prompts,
            attention_mask=attn_mask,
            num_beams=num_beams,
            do_sample=False,            # paper: beam-search, 非 sampling
            max_new_tokens=max_new_tokens,
            min_new_tokens=max_new_tokens,
            num_return_sequences=1,
            pad_token_id=pad_id,
            early_stopping=False,
            repetition_penalty=repetition_penalty,  # Shumailov official Zenodo code: 3.0 (paper §5.2 写 2.0 是 typo)
        )
        # outputs shape (B, max_p + max_new_tokens)
        # paper 解 1: 取 generated 部分作下代 block
        for i in range(outputs.shape[0]):
            gen_part = outputs[i, max_p:].tolist()
            # 防 generate 输出短于 max_new_tokens (early stop bug 兜底)
            if len(gen_part) < max_new_tokens:
                gen_part = gen_part + [pad_id] * (max_new_tokens - len(gen_part))
            else:
                gen_part = gen_part[:max_new_tokens]
            synthetic_input_ids.append(gen_part)
            synthetic_attention.append([1] * max_new_tokens)

    del model
    if device.startswith("cuda"):
        torch.cuda.empty_cache()

    synthetic_ds = Dataset.from_dict({
        "input_ids": synthetic_input_ids,
        "attention_mask": synthetic_attention,
        "labels": [list(ids) for ids in synthetic_input_ids],
    })
    logger.info("合成数据集生成完毕: %d blocks", len(synthetic_ds))
    return synthetic_ds


def save_synthetic_to_disk(ds: Dataset, save_dir: str | Path) -> Path:
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    ds.save_to_disk(str(save_dir))
    logger.info("合成数据保存到 %s", save_dir)
    return save_dir
