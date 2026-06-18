#!/usr/bin/env python3
"""
run_arm_b_alpha_scan.py — arm B (system emergent contradiction) α scan launcher

复用 shumailov_replication.py 的 self-iteration 框架, 加 CAT (Contradiction-Aware Training)
hook 在 fine_tune_one_generation 阶段, α scan 看 collapse 是否减弱.

跑法:
  python run_arm_b_alpha_scan.py --alpha 0.0 --seed 42 --num-generations 1 --smoke-test
  python run_arm_b_alpha_scan.py --alpha 10.0 --seed 42 --num-generations 10

输出:
  data/checkpoints_armb_alpha{alpha}/no_preserve_seed{seed}/generation_{n}/  (model checkpoints)
  logs/armb_alpha{alpha}_seed{seed}_<timestamp>.jsonl                       (per-gen perplexity + contradiction metrics)
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import torch
from datasets import Dataset
from transformers import AutoTokenizer

# 复用 shumailov_replication 的 helpers
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import load_config, resolve_path, CATYamlConfig
from data_pipeline import load_wikitext2, tokenize_and_block, build_mixed_generation_dataset as _build_mixed
from train_one_generation import fine_tune_one_generation, CATConfig
from generate_synthetic import generate_synthetic_dataset
from metrics import compute_perplexity_on_dataset


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def build_mixed_generation_dataset(
    real_train: Dataset,
    synthetic: Dataset,
    original_fraction: float,
    seed: int,
) -> Dataset:
    """按 condition 混 real + synthetic data — 复用 data_pipeline 的 helper."""
    return _build_mixed(real_train, synthetic, original_fraction, seed)


def cat_config_from_yaml(yaml_cat: CATYamlConfig, alpha: float) -> CATConfig:
    """从 yaml CATYamlConfig + 单 alpha → train_one_generation 的 CATConfig."""
    return CATConfig(
        enabled=alpha > 0,  # alpha=0 等价 baseline 不启用 CAT
        alpha=alpha,
        kl_update_every=yaml_cat.kl_update_every,
        val_subset_size=yaml_cat.val_subset_size,
        val_max_length=yaml_cat.val_max_length,
        beta_model=yaml_cat.beta_model,
        beta_kl=yaml_cat.beta_kl,
        lambda_1=yaml_cat.lambda_1,
        lambda_2=yaml_cat.lambda_2,
        lambda_3=yaml_cat.lambda_3,
        enable_grad_norm_monitor=yaml_cat.enable_grad_norm_monitor,
        # 5/10 凌晨 dialectical fields (yaml 缺则用 dataclass default — 旧 framework safe)
        T_2_form=getattr(yaml_cat, "T_2_form", "relu_dpp"),
        kl_history_K=getattr(yaml_cat, "kl_history_K", 1),
        m_eff=getattr(yaml_cat, "m_eff", 1.0),
    )


def main():
    parser = argparse.ArgumentParser(description="arm B emergent contradiction α scan")
    parser.add_argument("--config", type=str,
                        default="configs/cat_arm_b.yaml")
    parser.add_argument("--alpha", type=float, required=True,
                        help="ℒ_total = ℒ_LM + α * ℒ_contradiction")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--condition", type=str, default="no_preserve",
                        choices=["no_preserve", "preserve_10pct"])
    parser.add_argument("--num-generations", type=int, default=None,
                        help="覆盖 yaml 默认 generation 数")
    parser.add_argument("--smoke-test", action="store_true",
                        help="只跑 1 generation × 1 epoch × 32 train sentences (~5 min)")
    parser.add_argument("--output-base", type=str, default="data/checkpoints_armb")
    parser.add_argument("--base-mode", type=str, default="gen0", choices=["gen0","prev"], help="gen0=每代重置回gen0(原版canonical); prev=continue上一代(消融:剥base-reset外锚)")
    parser.add_argument("--prompt-mode", type=str, default="real", choices=["real","synthetic"], help="real=真wikitext前缀(原版); synthetic=用上一代合成数据作prompt(消融:剥real-prompt外锚)")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cfg_path = resolve_path(args.config)
    logger.info("=" * 60)
    logger.info("arm B α scan — alpha=%.4f seed=%d condition=%s smoke=%s",
                args.alpha, args.seed, args.condition, args.smoke_test)
    logger.info("config %s", cfg_path)
    logger.info("=" * 60)

    cfg = load_config(cfg_path)
    if cfg.cat is None or not cfg.cat.enabled:
        logger.error("yaml cat section missing 或 enabled=false; abort")
        return 1

    cat_cfg = cat_config_from_yaml(cfg.cat, args.alpha)
    logger.info("CATConfig: enabled=%s alpha=%.4f kl_update_every=%d",
                cat_cfg.enabled, cat_cfg.alpha, cat_cfg.kl_update_every)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info("device=%s", device)

    # ----- Step 1: 加载 + tokenize 数据 -----
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
        logger.info("smoke-test: 截断 train→32 行, val→32 行, test→16 行")
        train_blocks = train_blocks.select(range(min(32, len(train_blocks))))
        val_blocks = val_blocks.select(range(min(32, len(val_blocks))))
        test_blocks = test_blocks.select(range(min(16, len(test_blocks))))

    # ----- 选 condition -----
    condition = next(c for c in cfg.self_iteration.conditions if c.name == args.condition)
    n_generations = args.num_generations or (1 if args.smoke_test else cfg.self_iteration.num_generations)

    # ----- jsonl logging -----
    log_dir = resolve_path(cfg.logging.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = log_dir / f"armb_alpha{args.alpha}_seed{args.seed}_{timestamp}.jsonl"
    log_jsonl = open(jsonl_path, "a", encoding="utf-8")

    def log_record(rec: dict):
        log_jsonl.write(json.dumps(rec, ensure_ascii=False) + "\n")
        log_jsonl.flush()

    log_record({
        "stage": "run_start",
        "alpha": args.alpha,
        "seed": args.seed,
        "condition": args.condition,
        "n_generations": n_generations,
        "smoke_test": args.smoke_test,
        "kl_update_every": cat_cfg.kl_update_every,
    })

    # ----- Step 2: generation 0 fine-tune (real wikitext-2, **no CAT** 因为 g0 无 prior model) -----
    output_base = resolve_path(args.output_base) / f"alpha{args.alpha}"
    seed_base = output_base / f"{args.condition}_seed{args.seed}"
    gen0_dir = seed_base / "generation_0"
    gen0_epochs = condition.epochs_per_generation if not args.smoke_test else 1

    # ----- 5/10 RESUME LOGIC (PI binding caveat 1: resume not restart, audit trail) -----
    # Auto-detect first non-completed generation by checking checkpoint dirs
    def _ckpt_complete(g_dir):
        return (g_dir / "model.safetensors").exists() or (g_dir / "pytorch_model.bin").exists()

    resume_from = 0
    for n in range(0, n_generations):
        g_dir = seed_base / f"generation_{n}"
        if _ckpt_complete(g_dir):
            resume_from = n + 1
        else:
            break

    if resume_from > 0:
        logger.info(">>> RESUME mode: detected %d completed generations (gen 0..%d), skipping",
                    resume_from, resume_from - 1)
        log_record({
            "stage": "resume_detected",
            "resumed_from_gen": resume_from,
            "completed_gens": list(range(resume_from)),
            "ckpt_base": str(seed_base),
        })
    else:
        logger.info(">>> No completed generations found, starting from gen 0")

    logger.info(">>> Generation 0: fine-tune real wikitext-2 (epochs=%d, CAT disabled — no prior gen)", gen0_epochs)

    if resume_from >= 1:
        # gen 0 already done — re-eval test_ppl from existing ckpt for jsonl completeness
        logger.info("[resume] skip gen 0 fine-tune, re-eval test_ppl from existing ckpt")
        from train_one_generation import TrainResult
        # 用 dummy result; test_ppl 重 eval 下面
        gen0_result = TrainResult(
            output_dir=str(gen0_dir),
            final_train_loss=float("nan"),
            val_perplexity=float("nan"),
            val_loss=float("nan"),
            epoch_done=gen0_epochs,
        )
    else:
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
            cat_config=None,  # gen 0 没有 prior generation, CAT 不启用
        )
    test_ppl_dict_g0 = compute_perplexity_on_dataset(
        model_path=str(gen0_dir),
        tokenizer_id=cfg.model.hf_id,
        dataset=test_blocks,
        block_size=cfg.dataset.block_size,
        batch_size=cfg.fine_tune.per_device_train_batch_size,
        fp16=cfg.fine_tune.fp16,
    )
    test_ppl_g0 = float(test_ppl_dict_g0["mean_perplexity"])
    logger.info("Generation 0: val_ppl=%.2f test_ppl=%.2f", gen0_result.val_perplexity, test_ppl_g0)
    log_record({
        "stage": "generation_done",
        "generation": 0,
        "alpha": args.alpha,
        "seed": args.seed,
        "val_perplexity": gen0_result.val_perplexity,
        "test_perplexity": test_ppl_g0,
        "test_loss": gen0_result.val_loss,
        "epochs": gen0_epochs,
        "n_train_blocks": len(train_blocks),
        "model_path": str(gen0_dir),
        "cat_enabled": False,  # gen 0 无 CAT
    })

    # ----- Step 3: gen 1..N self-iteration with CAT enabled -----
    prev_synth_ds = None  # ABLATION A: prompt-mode synthetic 存上一代合成数据
    for g in range(1, n_generations):
        if g < resume_from:
            # 5/10 RESUME: gen g 已有 ckpt, 重 eval test_ppl 写 jsonl, 跳过 fine-tune + generate
            existing_gen_dir = seed_base / f"generation_{g}"
            logger.info("[resume] skip gen %d fine-tune (ckpt exists), re-eval test_ppl", g)
            try:
                test_ppl_dict_resume = compute_perplexity_on_dataset(
                    model_path=str(existing_gen_dir),
                    tokenizer_id=cfg.model.hf_id,
                    dataset=test_blocks,
                    block_size=cfg.dataset.block_size,
                    batch_size=cfg.fine_tune.per_device_train_batch_size,
                    fp16=cfg.fine_tune.fp16,
                )
                test_ppl_resume = float(test_ppl_dict_resume["mean_perplexity"])
            except Exception as e:
                logger.warning("[resume] gen %d test_ppl re-eval failed: %s", g, e)
                test_ppl_resume = float("nan")
            log_record({
                "stage": "generation_done",
                "generation": g,
                "alpha": args.alpha,
                "seed": args.seed,
                "val_perplexity": float("nan"),
                "test_perplexity": test_ppl_resume,
                "test_loss": float("nan"),
                "epochs": condition.epochs_per_generation,
                "n_train_blocks": len(train_blocks),
                "model_path": str(existing_gen_dir),
                "cat_enabled": args.alpha > 0,
                "cat_alpha": args.alpha,
                "resume_skip": True,
            })
            continue
        logger.info(">>> Generation %d (epochs=%d, CAT alpha=%.4f)", g, condition.epochs_per_generation, args.alpha)
        prev_gen_dir = output_base / f"{args.condition}_seed{args.seed}" / f"generation_{g-1}"
        gen_dir = output_base / f"{args.condition}_seed{args.seed}" / f"generation_{g}"

        # 3a generate synthetic data 用 prev model
        synth_ds = generate_synthetic_dataset(
            model_path=str(prev_gen_dir),
            tokenizer_id=cfg.model.hf_id,
            real_train_blocks=(prev_synth_ds if (args.prompt_mode=="synthetic" and prev_synth_ds is not None) else train_blocks),  # ABLATION A: prompt-mode
            num_beams=cfg.generation.num_beams,
            prompt_length=cfg.generation.prompt_length,
            max_new_tokens=cfg.generation.max_new_tokens,
            batch_size=cfg.generation.per_device_generation_batch_size,
            fp16=cfg.fine_tune.fp16,
            repetition_penalty=cfg.generation.repetition_penalty,
        )
        prev_synth_ds = synth_ds  # ABLATION A: 供下一代作 prompt
        # 3b 按 condition 混 real + synthetic
        gen_train_ds = build_mixed_generation_dataset(
            real_train=train_blocks,
            synthetic=synth_ds,
            original_fraction=condition.original_data_fraction,
            seed=args.seed + g,
        )
        # 3c fine-tune with CAT enabled (gen ≥ 1)
        epochs_g = condition.epochs_per_generation if not args.smoke_test else 1
        # paper: 每代 base 是 generation_0 (real wikitext-2 model), 不在前一代 continue
        gen_result = fine_tune_one_generation(
            base_model_path=str(gen0_dir if args.base_mode=="gen0" else prev_gen_dir),  # ABLATION B: base-mode (prev=剥 base-reset)
            train_dataset=gen_train_ds,
            val_dataset=val_blocks,
            tokenizer_id=cfg.model.hf_id,
            output_dir=gen_dir,
            epochs=epochs_g,
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
            cat_config=cat_cfg,  # ←←← arm B 关键: CAT 启用
        )
        # eval test ppl
        test_ppl_dict = compute_perplexity_on_dataset(
            model_path=str(gen_dir),
            tokenizer_id=cfg.model.hf_id,
            dataset=test_blocks,
            block_size=cfg.dataset.block_size,
            batch_size=cfg.fine_tune.per_device_train_batch_size,
            fp16=cfg.fine_tune.fp16,
        )
        test_ppl = float(test_ppl_dict["mean_perplexity"])
        # diversity skip — 留给 paper §4 写作 post-hoc 加, smoke 阶段不算
        distinct = {"distinct_1": None, "distinct_2": None, "distinct_3": None}
        logger.info("Generation %d: val_ppl=%.2f test_ppl=%.2f", g, gen_result.val_perplexity, test_ppl)
        log_record({
            "stage": "generation_done",
            "generation": g,
            "alpha": args.alpha,
            "seed": args.seed,
            "val_perplexity": gen_result.val_perplexity,
            "test_perplexity": test_ppl if test_ppl is not None else float("inf"),
            "test_loss": gen_result.val_loss,
            "epochs": epochs_g,
            "n_train_blocks": len(gen_train_ds),
            "n_synthetic_blocks": len(synth_ds),
            "model_path": str(gen_dir),
            "cat_enabled": True,
            "cat_alpha": args.alpha,
            **distinct,
        })

    log_jsonl.close()
    logger.info("=" * 60)
    logger.info("arm B α=%.4f seed=%d 完成. jsonl=%s", args.alpha, args.seed, jsonl_path)
    logger.info("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
