from __future__ import annotations
import math
import numpy as np
from .canonical import HmacStream

PERMUTATIONS = 100_000
BOOTSTRAPS = 50_000
ALPHA = 0.05


def _mean(values) -> float:
    return float(np.mean(np.asarray(values, dtype=float)))


def _se(values) -> float:
    array = np.asarray(values, dtype=float)
    if len(array) < 2:
        return math.inf
    return float(np.std(array, ddof=1) / math.sqrt(len(array)))


def _tstat(values) -> float:
    estimate = _mean(values)
    standard_error = _se(values)
    if standard_error == 0:
        if estimate > 0:
            return math.inf
        if estimate < 0:
            return -math.inf
        return 0.0
    if not math.isfinite(standard_error):
        return 0.0
    return estimate / standard_error


def _sign_vectors(key: bytes, context: bytes, n: int, repetitions: int):
    stream = HmacStream(key, context)
    for _ in range(repetitions):
        yield np.asarray(
            [1.0 if stream.randbelow(2) else -1.0 for _ in range(n)], dtype=float
        )


def superiority_test(
    differences,
    threshold: float,
    key: bytes,
    context: bytes,
    *,
    repetitions: int = PERMUTATIONS,
) -> dict:
    values = np.asarray(differences, dtype=float)
    shifted = values - threshold
    observed = _tstat(shifted)
    count = 0
    for signs in _sign_vectors(key, context, len(shifted), repetitions):
        count += _tstat(shifted * signs) >= observed
    return {
        "estimate": _mean(values),
        "threshold": threshold,
        "statistic": observed,
        "p": (count + 1) / (repetitions + 1),
        "n": len(values),
        "permutations": repetitions,
    }


def equivalence_test(
    differences,
    margin: float,
    key: bytes,
    context: bytes,
    *,
    repetitions: int = PERMUTATIONS,
) -> dict:
    values = np.asarray(differences, dtype=float)
    lower_shift = values + margin
    upper_shift = margin - values
    lower_observed = _tstat(lower_shift)
    upper_observed = _tstat(upper_shift)
    lower_count = upper_count = 0
    for signs in _sign_vectors(key, context + b"/LOWER", len(values), repetitions):
        lower_count += _tstat(lower_shift * signs) >= lower_observed
    for signs in _sign_vectors(key, context + b"/UPPER", len(values), repetitions):
        upper_count += _tstat(upper_shift * signs) >= upper_observed
    lower_p = (lower_count + 1) / (repetitions + 1)
    upper_p = (upper_count + 1) / (repetitions + 1)
    return {
        "estimate": _mean(values),
        "margin": [-margin, margin],
        "lower_p": lower_p,
        "upper_p": upper_p,
        "p": max(lower_p, upper_p),
        "n": len(values),
        "permutations": repetitions,
    }


def simultaneous_bootstrap(
    contrast_matrix,
    key: bytes,
    context: bytes,
    *,
    repetitions: int = BOOTSTRAPS,
) -> list[dict]:
    matrix = np.asarray(contrast_matrix, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] < 2:
        raise ValueError("BOOTSTRAP_MATRIX")
    n, k = matrix.shape
    estimates = np.mean(matrix, axis=0)
    standard_errors = np.std(matrix, axis=0, ddof=1) / math.sqrt(n)
    stream = HmacStream(key, context)
    maxima: list[float] = []
    for _ in range(repetitions):
        indices = np.asarray([stream.randbelow(n) for _ in range(n)])
        sample = matrix[indices]
        means = np.mean(sample, axis=0)
        sample_se = np.std(sample, axis=0, ddof=1) / math.sqrt(n)
        studentized = np.divide(
            np.abs(means - estimates),
            sample_se,
            out=np.zeros_like(means),
            where=sample_se > 0,
        )
        maxima.append(float(np.max(studentized)))
    critical = float(np.quantile(np.asarray(maxima), 0.95, method="higher"))
    return [
        {
            "estimate": float(estimates[index]),
            "se": float(standard_errors[index]),
            "lower": float(estimates[index] - critical * standard_errors[index]),
            "upper": float(estimates[index] + critical * standard_errors[index]),
            "critical": critical,
            "bootstraps": repetitions,
        }
        for index in range(k)
    ]


def holm(pvalues: dict[str, float], alpha: float = ALPHA) -> dict[str, dict]:
    ordered = sorted(pvalues.items(), key=lambda item: (item[1], item[0]))
    total = len(ordered)
    running_adjusted = 0.0
    stopped = False
    result: dict[str, dict] = {}
    for index, (name, pvalue) in enumerate(ordered):
        remaining = total - index
        threshold = alpha / remaining
        adjusted = min(1.0, remaining * pvalue)
        running_adjusted = max(running_adjusted, adjusted)
        reject = (not stopped) and pvalue <= threshold
        if not reject:
            stopped = True
        result[name] = {
            "raw_p": pvalue,
            "adjusted_p": running_adjusted,
            "rank": index + 1,
            "threshold": threshold,
            "reject": reject,
        }
    return result


def linear_missing_bounds(
    grouped_values: dict[tuple[str, str], list[float | None]],
    coefficients: dict[tuple[str, str], float],
) -> dict:
    lower = upper = 0.0
    for group, coefficient in coefficients.items():
        values = grouped_values[group]
        observed = [value for value in values if value is not None]
        missing = len(values) - len(observed)
        denominator = len(values)
        group_lower = (sum(observed) + 0.0 * missing) / denominator
        group_upper = (sum(observed) + 1.0 * missing) / denominator
        if coefficient >= 0:
            lower += coefficient * group_lower
            upper += coefficient * group_upper
        else:
            lower += coefficient * group_upper
            upper += coefficient * group_lower
    return {"lower": lower, "upper": upper}


def iut(constituents: dict[str, dict], alpha: float = ALPHA) -> dict:
    pvalues = {name: row["p"] for name, row in constituents.items()}
    maximum = max(pvalues.values()) if pvalues else 1.0
    return {
        "p": maximum,
        "pass": bool(pvalues) and maximum <= alpha,
        "constituent_pvalues": pvalues,
        "rule": "MAX_CONSTITUENT_P_NO_COMPENSATORY_SCORE",
    }
