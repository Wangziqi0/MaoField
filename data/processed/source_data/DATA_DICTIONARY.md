# Source Data dictionary

## CSV tables

### `Figure_5_Identification_Architecture.csv`

Rows (excluding header): 7

Columns: `section`, `scenario`, `dn_truth`, `uf_truth`, `dn_response`, `uf_response`, `dn_accuracy`, `uf_accuracy`, `contrast`, `source_or_status`

### `Final_Proposition_Matrix.csv`

Rows (excluding header): 10

Columns: `proposition`, `status`, `evidence`, `ceiling`

### `GLM_Direct_Contrasts.csv`

Rows (excluding header): 96

Columns: `stratum`, `endpoint`, `contrast`, `contrast_label`, `estimate`, `missing_lower`, `missing_upper`, `p_value`, `n_paired`, `kind`, `registered_threshold`, `least_favourable_pass`

### `GLM_Ordinary_Criteria.csv`

Rows (excluding header): 4

Columns: `endpoint`, `successes`, `registered_n`, `threshold`, `typed_missing`, `valid`

### `GLM_Resources.csv`

Rows (excluding header): 2

Columns: `stratum`, `elapsed_time_seconds_sum`, `evaluable_rows`, `normalized_budget_ratio_mean`, `raw_calls_sum`, `registered_rows`, `status`, `tool_cost_sum`

### `GLM_Sibling_Contrasts.csv`

Rows (excluding header): 88

Columns: `stratum`, `channel`, `contrast`, `contrast_label`, `estimate`, `missing_lower`, `missing_upper`, `p_value`, `n_paired`, `kind`, `registered_threshold`, `least_favourable_pass`

### `GLM_Structure_Criterion.csv`

Rows (excluding header): 1

Columns: `observed_rows`, `registered_n`, `renderer_mismatches`, `successes`, `threshold`, `typed_missing`, `valid`

### `GLM_Trajectory_Failures.csv`

Rows (excluding header): 16

Columns: `stratum`, `failure_code`, `count`, `registered_rows`, `rows_with_failure`

### `Phase23_Condition_Matrix.csv`

Rows (excluding header): 6

Columns: `condition`, `final`, `gap`, `objective`, `ordinary`, `structure`

### `Phase23_Exact_Equality.csv`

Rows (excluding header): 24

Columns: `condition`, `endpoint`, `stratum`, `estimate`, `ci_lower`, `ci_upper`

### `Phase23_Ordinary_Controls.csv`

Rows (excluding header): 6

Columns: `condition`, `ordinary_successes`, `ordinary_n`, `ordinary_valid`

### `Phase23_Qwen_Channel_Gap.csv`

Rows (excluding header): 2

Columns: `condition`, `stratum`, `A_SIB_minus_R`, `ci_lower`, `ci_upper`, `ordinary_successes`, `ordinary_n`, `structure_successes`, `structure_n`, `criterion_valid`

## Workbooks

### `Source_Data_Extended_Data_Figure_1_V3.xlsx`

- `Phase23_conditions`: ``

### `Source_Data_Extended_Data_Figure_2_V3.xlsx`

- `GLM_direct`: ``

### `Source_Data_Extended_Data_Figure_3_V3.xlsx`

- `GLM_siblings`: ``

### `Source_Data_Extended_Data_Figure_4_V3.xlsx`

- `GLM_failures`: ``

### `Source_Data_Extended_Data_Figure_5_V3.xlsx`

- `GLM_resources`: ``

### `Source_Data_Figure_3_V3.xlsx`

- `Exact_equality`: ``
- `Ordinary_controls`: ``
- `Qwen_gap`: ``

### `Source_Data_Figure_4_V3.xlsx`

- `Ordinary_criteria`: ``
- `Structure_criterion`: ``
- `Direct_contrasts`: ``
- `Trajectory_failures`: ``

### `Source_Data_Figure_5_V3.xlsx`

- `Identification_architecture`: ``
- `Claim_ceiling`: ``
