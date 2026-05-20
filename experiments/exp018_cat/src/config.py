"""
config.py — Shumailov 2024 baseline 复现的默认 hyperparameter + YAML 加载器.

加载 configs/shumailov_baseline.yaml 并提供 dataclass 封装.
所有 paper 引用见 yaml 文件注释.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = PROJECT_ROOT / "configs" / "shumailov_baseline.yaml"


@dataclass
class ModelConfig:
    hf_id: str
    dtype: str
    cache_dir: str


@dataclass
class DatasetConfig:
    hf_id: str
    hf_config: str
    block_size: int
    splits: dict[str, str]
    cache_dir: str


@dataclass
class FineTuneConfig:
    optimizer: str
    learning_rate: float
    per_device_train_batch_size: int
    gradient_accumulation_steps: int
    weight_decay: float
    warmup_ratio: float
    lr_scheduler_type: str
    fp16: bool
    gradient_checkpointing: bool
    save_strategy: str
    evaluation_strategy: str
    logging_steps: int
    seed: int | None


@dataclass
class GenerationConfig:
    strategy: str
    num_beams: int
    do_sample: bool
    prompt_length: int
    max_new_tokens: int
    per_device_generation_batch_size: int
    output_size: str
    repetition_penalty: float = 1.0  # Shumailov official Zenodo: 3.0 (paper §5.2 typo 写 2.0)


@dataclass
class IterationConditionConfig:
    name: str
    epochs_per_generation: int
    original_data_fraction: float
    synthetic_data_fraction: float


@dataclass
class SelfIterationConfig:
    num_generations: int
    conditions: list[IterationConditionConfig]
    base_model_for_each_generation: str
    base_model_selection_metric: str


@dataclass
class MetricsConfig:
    perplexity: dict[str, Any]
    per_sequence_perplexity_histogram: dict[str, Any]
    distinct_n: dict[str, Any]


@dataclass
class MultiSeedConfig:
    seeds: list[int]


@dataclass
class LoggingConfig:
    log_dir: str
    jsonl_per_run: str
    use_wandb: bool
    use_tensorboard: bool


@dataclass
class CATYamlConfig:
    """contradiction-aware training yaml 配置 (cat: section in yaml)."""
    enabled: bool = False
    alpha_scan: list[float] = field(default_factory=lambda: [0.0])
    kl_update_every: int = 10
    val_subset_size: int = 256
    val_max_length: int = 64
    beta_model: float = 0.999
    beta_kl: float = 0.9
    lambda_1: float = 1.0
    lambda_2: float = 1.0
    lambda_3: float = 1.0
    enable_grad_norm_monitor: bool = True
    # 5/10 凌晨 dialectical upgrade (Linux dispatch §4 + 3 sub-agent verdict pass)
    T_2_form: str = "relu_dpp"          # "relu_dpp" 旧 mechanical / "quadratic" 新 dialectical
    kl_history_K: int = 1               # 1 = Markov 旧 / 9 = Volterra 新
    m_eff: float = 1.0                  # χ kernel 参数; v2_dialectical = 0.212


@dataclass
class ShumailovConfig:
    experiment_name: str
    paper_cite: str
    goal: str
    model: ModelConfig
    dataset: DatasetConfig
    fine_tune: FineTuneConfig
    generation: GenerationConfig
    self_iteration: SelfIterationConfig
    metrics: MetricsConfig
    multi_seed: MultiSeedConfig
    logging: LoggingConfig
    cat: CATYamlConfig | None = None


def load_config(path: str | Path = DEFAULT_CONFIG) -> ShumailovConfig:
    """加载 yaml 配置, 返回 dataclass."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    exp = raw["experiment"]
    cond = [IterationConditionConfig(**c) for c in raw["self_iteration"]["conditions"]]

    return ShumailovConfig(
        experiment_name=exp["name"],
        paper_cite=exp["paper_cite"],
        goal=exp["goal"],
        model=ModelConfig(**raw["model"]),
        dataset=DatasetConfig(**raw["dataset"]),
        fine_tune=FineTuneConfig(**raw["fine_tune"]),
        generation=GenerationConfig(**raw["generation"]),
        self_iteration=SelfIterationConfig(
            num_generations=raw["self_iteration"]["num_generations"],
            conditions=cond,
            base_model_for_each_generation=raw["self_iteration"]["base_model_for_each_generation"],
            base_model_selection_metric=raw["self_iteration"]["base_model_selection_metric"],
        ),
        metrics=MetricsConfig(**raw["metrics"]),
        multi_seed=MultiSeedConfig(**raw["multi_seed"]),
        logging=LoggingConfig(**raw["logging"]),
        cat=CATYamlConfig(**raw["cat"]) if "cat" in raw and raw["cat"] is not None else None,
    )


def resolve_path(rel: str, project_root: Path = PROJECT_ROOT) -> Path:
    """相对路径转绝对路径 (相对项目根)."""
    p = Path(rel)
    if p.is_absolute():
        return p
    return project_root / p


if __name__ == "__main__":
    cfg = load_config()
    print(f"实验: {cfg.experiment_name}")
    print(f"模型: {cfg.model.hf_id}")
    print(f"数据集: {cfg.dataset.hf_id}/{cfg.dataset.hf_config}")
    print(f"代数: {cfg.self_iteration.num_generations}")
    print(f"种子数: {len(cfg.multi_seed.seeds)} ({cfg.multi_seed.seeds})")
    print(f"条件数: {len(cfg.self_iteration.conditions)}")
    for c in cfg.self_iteration.conditions:
        print(f"  - {c.name}: {c.epochs_per_generation} epochs, "
              f"original={c.original_data_fraction:.1%}")
