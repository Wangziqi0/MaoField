"""
train_one_generation.py — 单代 fine-tune.

输入: 训练 dataset (block 化), 起点 model checkpoint 路径, 配置.
输出: fine-tune 后的 model (saved 到 output_dir), val perplexity.

paper 严格 cite (§5.2):
  - 5 epochs (no_preserve) / 10 epochs (preserve_10pct)
  - "Training for each of the generations starts with generation from the
    original training data."
    含义: 每代都从 generation_0_best 重新出发, 不在前一代上 continue.
  - "to be as realistic as possible, we use the best performing model on the
    original task, evaluated using the original wikitext2 validation set, as
    the base model"
"""
from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from pathlib import Path

import torch
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

logger = logging.getLogger(__name__)


# CAT (Contradiction-Aware Training) 选项 — 仅 arm B 用
@dataclass
class CATConfig:
    """contradiction-aware training 配置. 默认 None = 不启用 (baseline 跑)."""
    enabled: bool = False
    alpha: float = 0.1            # ℒ_total = ℒ_LM + alpha * ℒ_contradiction
    kl_update_every: int = 10
    val_subset_size: int = 256
    val_max_length: int = 64
    beta_model: float = 0.999
    beta_kl: float = 0.9
    lambda_1: float = 1.0
    lambda_2: float = 1.0
    lambda_3: float = 1.0
    enable_grad_norm_monitor: bool = True
    # 5/10 凌晨 dialectical upgrade (Linux dispatch §4 + 3 sub-agent verdict)
    T_2_form: str = "relu_dpp"          # "relu_dpp" 旧 mechanical / "quadratic" 新 dialectical
    kl_history_K: int = 1               # 1 = Markov (旧) / 9 = Volterra path-dependent (新)
    m_eff: float = 1.0                  # 用于 Volterra χ kernel; v2_dialectical = 0.212


@dataclass
class TrainResult:
    output_dir: str
    final_train_loss: float
    val_perplexity: float
    val_loss: float
    epoch_done: int


def fine_tune_one_generation(
    base_model_path: str,
    train_dataset: Dataset,
    val_dataset: Dataset,
    tokenizer_id: str,
    output_dir: str | Path,
    *,
    epochs: int,
    learning_rate: float,
    per_device_train_batch_size: int,
    gradient_accumulation_steps: int,
    weight_decay: float,
    warmup_ratio: float,
    lr_scheduler_type: str,
    fp16: bool,
    gradient_checkpointing: bool,
    seed: int,
    logging_steps: int = 50,
    cat_config: CATConfig | None = None,
) -> TrainResult:
    """
    单代 fine-tune. 严格按 yaml 配置传参.

    返回 TrainResult, 含 val_perplexity (用 wikitext2 val).
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info("fine-tune base=%s → out=%s epochs=%d seed=%d",
                base_model_path, output_dir, epochs, seed)

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 训练时 model 必须 FP32 加载, fp16 mixed precision 由 Trainer 自动管理.
    # 否则触发 "Attempting to unscale FP16 gradients" — autocast 对 FP16 model 不工作.
    # D22 candidate C add (Agent 4 catch): attn_implementation="eager" 必 explicit.
    # 避 OPT model SDPA default 之 output_attentions=True silent fallback 到 eager + warning.
    # multi-layer A3 attention 头熵 测量 需 output_attentions=True (Phase 1 candidate C binding).
    model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        torch_dtype=torch.float32,
        attn_implementation="eager",
    )

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=epochs,
        per_device_train_batch_size=per_device_train_batch_size,
        per_device_eval_batch_size=per_device_train_batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        learning_rate=learning_rate,
        weight_decay=weight_decay,
        warmup_ratio=warmup_ratio,
        lr_scheduler_type=lr_scheduler_type,
        fp16=fp16,
        gradient_checkpointing=gradient_checkpointing,
        evaluation_strategy="epoch",
        save_strategy="no",
        logging_steps=logging_steps,
        report_to="none",     # 不连 wandb / tensorboard
        seed=seed,
        data_seed=seed,
        load_best_model_at_end=False,
        remove_unused_columns=False,
    )

    # CAT (Contradiction-Aware Training) 选项 — arm B 用
    if cat_config is not None and cat_config.enabled:
        from cat_trainer import CATTrainer, build_val_loader_for_kl
        from contradiction_loss import (
            KLContradictionConfig, KLContradictionTracker,
            GradNormMonitor, GradNormMonitorConfig,
        )
        logger.info("CATTrainer enabled: alpha=%.4f kl_update_every=%d",
                    cat_config.alpha, cat_config.kl_update_every)
        kl_cfg = KLContradictionConfig(
            beta_model=cat_config.beta_model,
            beta_kl=cat_config.beta_kl,
            lambda_1=cat_config.lambda_1,
            lambda_2=cat_config.lambda_2,
            lambda_3=cat_config.lambda_3,
            kl_update_every=cat_config.kl_update_every,
            val_subset_size=cat_config.val_subset_size,
            val_max_length=cat_config.val_max_length,
            T_2_form=cat_config.T_2_form,
            kl_history_K=cat_config.kl_history_K,
            m_eff=cat_config.m_eff,
        )
        tracker = KLContradictionTracker(kl_cfg)
        # 取 val_dataset 子集作 KL val loader (256 句)
        val_subset = val_dataset.shuffle(seed=seed).select(
            range(min(cat_config.val_subset_size, len(val_dataset)))
        )
        val_loader = build_val_loader_for_kl(
            val_subset, tokenizer,
            batch_size=8, max_length=cat_config.val_max_length,
        )
        grad_monitor = GradNormMonitor(GradNormMonitorConfig()) if cat_config.enable_grad_norm_monitor else None

        trainer = CATTrainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            data_collator=data_collator,
            tokenizer=tokenizer,
            contradiction_tracker=tracker,
            val_loader_for_kl=val_loader,
            contradiction_alpha=cat_config.alpha,
            kl_update_every=cat_config.kl_update_every,
            grad_norm_monitor=grad_monitor,
        )
    else:
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            data_collator=data_collator,
            tokenizer=tokenizer,
        )

    train_output = trainer.train()
    eval_output = trainer.evaluate()

    val_loss = float(eval_output["eval_loss"])
    val_ppl = math.exp(val_loss) if val_loss < 20 else float("inf")
    final_train_loss = float(train_output.training_loss)

    # 保存 final model (供下代使用)
    trainer.save_model(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))

    logger.info(
        "fine-tune 完成: train_loss=%.4f val_loss=%.4f val_ppl=%.2f",
        final_train_loss, val_loss, val_ppl,
    )

    # 释放 GPU 内存
    del model, trainer
    torch.cuda.empty_cache() if torch.cuda.is_available() else None

    return TrainResult(
        output_dir=str(output_dir),
        final_train_loss=final_train_loss,
        val_perplexity=val_ppl,
        val_loss=val_loss,
        epoch_done=epochs,
    )
