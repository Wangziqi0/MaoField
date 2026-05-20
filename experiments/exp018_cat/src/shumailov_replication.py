"""
shumailov_replication.py — Shumailov 2024 baseline 自迭代崩溃 main entry.

CLI:
  python shumailov_replication.py --condition no_preserve --seed 42
  python shumailov_replication.py --condition preserve_10pct --seed 1337
  python shumailov_replication.py --condition no_preserve --seed 42 --smoke-test

主流程 (与 paper §5.2 严格对齐):
  Step 1: 加载 OPT-125m + tokenizer + wikitext-2 (block_size=64)
  Step 2: 在 real wikitext-2 上 fine-tune → "generation 0 model"
          (paper: "Training for each of the generations starts with generation
                   from the original training data ... best performing model
                   on the original task")
  Step 3: For g in [1, 2, ..., 9]:
            (a) 用 generation 0 model (or 上代 model) 5-way beam-search 生成下代训练数据
            (b) (按 condition) 全替换 / 10% 真实 + 90% 合成
            (c) 从 generation 0 model 重新 fine-tune (epochs 取决于 condition)
            (d) 在 wikitext-2 test set 上算 perplexity
  Step 4: 输出 jsonl 日志 + falsification check.

paper 严格 cite (§5.2):
  "Training for each of the generations starts with generation from the
   original training data."
  → 每代 fine-tune 都从 generation 0 重新出发 (不在前一代 checkpoint 上 continue).

  "to be as realistic as possible, we use the best performing model on the
   original task, evaluated using the original wikitext2 validation set, as
   the base model"
  → generation 0 在 wikitext-2 val 上评估, 取 best epoch 的 model 作下代 base.
  (我们简化: 单次 fine-tune save final epoch — sub-agent 默认 paper 多 epoch
   都跑完 take last; 复杂 best-epoch 选择留给后续优化)
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path

import torch
from datasets import Dataset
from transformers import AutoTokenizer

# 项目内 imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import load_config, resolve_path, ShumailovConfig, IterationConditionConfig
from data_pipeline import (
    load_wikitext2,
    tokenize_and_block,
    build_mixed_generation_dataset,
    get_text_strings_from_blocks,
)
from train_one_generation import fine_tune_one_generation
from generate_synthetic import generate_synthetic_dataset
from metrics import (
    compute_perplexity_on_dataset,
    compute_per_sequence_perplexity,
    compute_distinct_n,
    falsification_check,
)


def setup_logging(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_path, mode="a", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def get_condition(cfg: ShumailovConfig, name: str) -> IterationConditionConfig:
    for c in cfg.self_iteration.conditions:
        if c.name == name:
            return c
    raise ValueError(f"未知 condition: {name}, 可选 = "
                     f"{[c.name for c in cfg.self_iteration.conditions]}")


def write_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Shumailov 2024 OPT-125m 自迭代崩溃 baseline 复现"
    )
    parser.add_argument("--config", type=str, default=None,
                        help="yaml 配置路径 (默认 configs/shumailov_baseline.yaml)")
    parser.add_argument("--condition", type=str, required=True,
                        choices=["no_preserve", "preserve_10pct"],
                        help="paper §5.2 末段的 2 种 condition")
    parser.add_argument("--seed", type=int, required=True,
                        help="随机种子 (multi-seed run 用 42 / 1337 / 2024)")
    parser.add_argument("--output-base", type=str, default="data/checkpoints",
                        help="checkpoint + 合成数据输出根目录")
    parser.add_argument("--smoke-test", action="store_true",
                        help="smoke 模式: 数据集子采 32 行, 1 generation, 1 epoch (验证 pipeline)")
    parser.add_argument("--num-generations-override", type=int, default=None,
                        help="覆盖 yaml 的 num_generations (debug 用)")
    args = parser.parse_args()

    cfg_path = args.config if args.config else None
    cfg = load_config(cfg_path) if cfg_path else load_config()
    condition = get_condition(cfg, args.condition)

    n_generations = args.num_generations_override or cfg.self_iteration.num_generations
    if args.smoke_test:
        n_generations = 1

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    log_path = resolve_path(
        f"logs/shumailov_{args.condition}_seed{args.seed}_{timestamp}.log"
    )
    jsonl_path = resolve_path(
        f"logs/shumailov_{args.condition}_seed{args.seed}_{timestamp}.jsonl"
    )
    setup_logging(log_path)
    logger = logging.getLogger(__name__)

    logger.info("=" * 60)
    logger.info("Shumailov 2024 baseline 复现")
    logger.info("paper: %s", cfg.paper_cite)
    logger.info("condition=%s seed=%d n_generations=%d smoke=%s",
                args.condition, args.seed, n_generations, args.smoke_test)
    logger.info("device=%s", "cuda" if torch.cuda.is_available() else "cpu")
    logger.info("=" * 60)

    # ----- Step 1: 加载数据 + tokenizer -----
    tokenizer = AutoTokenizer.from_pretrained(cfg.model.hf_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    raw_ds = load_wikitext2(
        hf_id=cfg.dataset.hf_id,
        hf_config=cfg.dataset.hf_config,
        cache_dir=resolve_path(cfg.dataset.cache_dir),
    )
    train_blocks = tokenize_and_block(raw_ds["train"], tokenizer, cfg.dataset.block_size)
    val_blocks = tokenize_and_block(raw_ds["validation"], tokenizer, cfg.dataset.block_size)
    test_blocks = tokenize_and_block(raw_ds["test"], tokenizer, cfg.dataset.block_size)

    if args.smoke_test:
        logger.info("smoke-test: 截断 train→32 行, val→16 行, test→16 行")
        train_blocks = train_blocks.select(range(min(32, len(train_blocks))))
        val_blocks = val_blocks.select(range(min(16, len(val_blocks))))
        test_blocks = test_blocks.select(range(min(16, len(test_blocks))))

    # ----- Step 2: generation 0 fine-tune (real wikitext-2) -----
    output_base = resolve_path(args.output_base)
    gen0_dir = output_base / f"{args.condition}_seed{args.seed}" / "generation_0"
    gen0_epochs = condition.epochs_per_generation if not args.smoke_test else 1

    logger.info(">>> Generation 0: fine-tune on real wikitext-2 (epochs=%d)", gen0_epochs)
    gen0_result = fine_tune_one_generation(
        base_model_path=cfg.model.hf_id,
        train_dataset=train_blocks,
        val_dataset=val_blocks,
        tokenizer_id=cfg.model.hf_id,
        output_dir=gen0_dir,
        epochs=gen0_epochs,
        learning_rate=cfg.fine_tune.learning_rate,
        per_device_train_batch_size=cfg.fine_tune.per_device_train_batch_size,
        gradient_accumulation_steps=cfg.fine_tune.gradient_accumulation_steps,
        weight_decay=cfg.fine_tune.weight_decay,
        warmup_ratio=cfg.fine_tune.warmup_ratio,
        lr_scheduler_type=cfg.fine_tune.lr_scheduler_type,
        fp16=cfg.fine_tune.fp16,
        gradient_checkpointing=cfg.fine_tune.gradient_checkpointing,
        seed=args.seed,
        logging_steps=cfg.fine_tune.logging_steps,
    )

    # 评估 generation 0 在 wikitext-2 test 上的 perplexity
    test_ppl = compute_perplexity_on_dataset(
        model_path=str(gen0_dir),
        tokenizer_id=cfg.model.hf_id,
        dataset=test_blocks,
        block_size=cfg.dataset.block_size,
        batch_size=cfg.fine_tune.per_device_train_batch_size,
        fp16=cfg.fine_tune.fp16,
    )
    logger.info("Generation 0: val_ppl=%.2f test_ppl=%.2f",
                gen0_result.val_perplexity, test_ppl["mean_perplexity"])

    write_jsonl(jsonl_path, {
        "stage": "generation_done",
        "generation": 0,
        "condition": args.condition,
        "seed": args.seed,
        "val_perplexity": gen0_result.val_perplexity,
        "test_perplexity": test_ppl["mean_perplexity"],
        "test_loss": test_ppl["mean_loss"],
        "epochs": gen0_epochs,
        "n_train_blocks": len(train_blocks),
        "model_path": str(gen0_dir),
    })

    gen0_test_ppl = test_ppl["mean_perplexity"]
    last_test_ppl = gen0_test_ppl

    # paper §5.2: "Training for each of the generations starts with generation
    #              from the original training data"
    # 每代都从 gen0 model 出发 (而非前一代), 所以 base 锁定为 gen0_dir
    base_model_for_subsequent = str(gen0_dir)

    # ----- Step 3: 自迭代 generation 1..N-1 -----
    for g in range(1, n_generations):
        logger.info(">>> Generation %d", g)
        gen_dir = output_base / f"{args.condition}_seed{args.seed}" / f"generation_{g}"
        gen_dir.mkdir(parents=True, exist_ok=True)

        # 3(a) 用上一代 model 生成合成数据
        # paper 不完全清楚: 是 generation g-1 model 生 g, 还是固定 generation 0 生?
        # paper §5.2 文字: "model 1 was trained on the data produced by model 0;
        #                   model 2 was trained on data ..." (Figure 10 caption)
        # → 上代 model 生下代数据 (而非 gen0 永远生)
        prev_model_path = (
            output_base / f"{args.condition}_seed{args.seed}" / f"generation_{g-1}"
        )
        synth_ds = generate_synthetic_dataset(
            model_path=str(prev_model_path),
            tokenizer_id=cfg.model.hf_id,
            real_train_blocks=train_blocks,
            num_beams=cfg.generation.num_beams,
            prompt_length=cfg.generation.prompt_length,
            max_new_tokens=cfg.generation.max_new_tokens,
            batch_size=cfg.generation.per_device_generation_batch_size,
            fp16=cfg.fine_tune.fp16,
            repetition_penalty=cfg.generation.repetition_penalty,
        )
        synth_save_dir = gen_dir / "synthetic_train"
        synth_ds.save_to_disk(str(synth_save_dir))

        # 3(b) 按 condition 决定下代训练 dataset
        gen_train_ds = build_mixed_generation_dataset(
            real_train=train_blocks,
            synthetic_train=synth_ds,
            original_fraction=condition.original_data_fraction,
            seed=args.seed + g,
        )

        # 3(c) 从 gen0_dir base model 重新 fine-tune
        # paper 严格 cite: "Training for each of the generations starts with
        #                   generation from the original training data."
        gen_result = fine_tune_one_generation(
            base_model_path=base_model_for_subsequent,
            train_dataset=gen_train_ds,
            val_dataset=val_blocks,
            tokenizer_id=cfg.model.hf_id,
            output_dir=gen_dir,
            epochs=condition.epochs_per_generation if not args.smoke_test else 1,
            learning_rate=cfg.fine_tune.learning_rate,
            per_device_train_batch_size=cfg.fine_tune.per_device_train_batch_size,
            gradient_accumulation_steps=cfg.fine_tune.gradient_accumulation_steps,
            weight_decay=cfg.fine_tune.weight_decay,
            warmup_ratio=cfg.fine_tune.warmup_ratio,
            lr_scheduler_type=cfg.fine_tune.lr_scheduler_type,
            fp16=cfg.fine_tune.fp16,
            gradient_checkpointing=cfg.fine_tune.gradient_checkpointing,
            seed=args.seed + g,
            logging_steps=cfg.fine_tune.logging_steps,
        )

        # 3(d) 评估 wikitext-2 test perplexity
        test_ppl = compute_perplexity_on_dataset(
            model_path=str(gen_dir),
            tokenizer_id=cfg.model.hf_id,
            dataset=test_blocks,
            block_size=cfg.dataset.block_size,
            batch_size=cfg.fine_tune.per_device_train_batch_size,
            fp16=cfg.fine_tune.fp16,
        )
        last_test_ppl = test_ppl["mean_perplexity"]
        logger.info("Generation %d: val_ppl=%.2f test_ppl=%.2f",
                    g, gen_result.val_perplexity, last_test_ppl)

        # distinct-n on 合成数据 (mode coverage proxy)
        synth_texts = get_text_strings_from_blocks(synth_ds, tokenizer, max_samples=2000)
        d_metrics = {
            f"distinct_{n}": compute_distinct_n(synth_texts, n)
            for n in cfg.metrics.distinct_n["n"]
        }

        write_jsonl(jsonl_path, {
            "stage": "generation_done",
            "generation": g,
            "condition": args.condition,
            "seed": args.seed,
            "val_perplexity": gen_result.val_perplexity,
            "test_perplexity": last_test_ppl,
            "test_loss": test_ppl["mean_loss"],
            "epochs": condition.epochs_per_generation,
            "n_train_blocks": len(gen_train_ds),
            "n_synthetic_blocks": len(synth_ds),
            "model_path": str(gen_dir),
            **d_metrics,
        })

    # ----- Step 4: falsification check -----
    fc = falsification_check(
        gen0_ppl=gen0_test_ppl,
        gen9_ppl=last_test_ppl,
    )
    logger.info("=" * 60)
    logger.info("falsification check:")
    for k, v in fc.items():
        logger.info("  %s: passed=%s details=%s", k, v["passed"], v)

    write_jsonl(jsonl_path, {
        "stage": "falsification_check",
        "condition": args.condition,
        "seed": args.seed,
        "result": fc,
    })

    logger.info("complete. log=%s jsonl=%s", log_path, jsonl_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
