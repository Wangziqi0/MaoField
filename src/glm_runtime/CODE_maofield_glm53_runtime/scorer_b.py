from __future__ import annotations
import json
from pathlib import Path
from .family_rules import resource_budget, resource_cost


def _expected(state: dict) -> tuple[str, str]:
    family = state["family"]
    stable = state["task"] == "stable"
    new = state["regime"] == "new"
    return {
        "PYTHON_API_SIGNATURE": (
            "adapter" if stable else ("positional" if new else "keyword"),
            "call_style",
        ),
        "SQLITE_SCHEMA": (
            "count" if stable else ("value" if new else "metric"),
            "query_column",
        ),
        "DATA_SCHEMA_TRANSFORM": (
            "scalar" if stable else ("list" if new else "object"),
            "root_handler",
        ),
        "RUNTIME_CONFIGURATION": (
            "environment" if stable else ("session" if new else "project"),
            "precedence",
        ),
        "DEPENDENCY_API_VERSION": (
            "compat_wrapper" if stable else ("execute_v2" if new else "execute_v1"),
            "api_method",
        ),
        "HTTP_PROTOCOL": (
            "health" if stable else ("h2" if new else "http1"),
            "wire",
        ),
        "TRANSACTION_CONCURRENCY": (
            "read_only" if stable else ("optimistic" if new else "pessimistic"),
            "locking",
        ),
        "SERIALIZATION_MIGRATION": (
            "json" if stable else ("v2" if new else "v1"),
            "encoding",
        ),
        "PACKAGE_RESOLUTION": (
            "vendored" if stable else ("latest" if new else "pinned"),
            "resolution",
        ),
        "SCHEMA_EVOLUTION": (
            "identity" if stable else ("v2_minimal" if new else "v1_compatible"),
            "shape",
        ),
        "TOOL_AFFORDANCE_CHANGE": (
            "status" if stable else ("json_flag" if new else "text_parse"),
            "mode",
        ),
        "COST_RESOURCE_REGIME": (
            "constant" if stable else ("exhaustive" if new else "heuristic"),
            "algorithm",
        ),
    }[family]


def score(root: Path, private_world: dict) -> dict:
    state = json.loads((root / "state.json").read_text(encoding="utf-8"))
    solution = json.loads((root / "solution.json").read_text(encoding="utf-8"))
    expected_value, expected_key = _expected(state)
    family = state["family"]
    tests = [
        {
            "id": f"B:{family}:value",
            "pass": solution.get(expected_key) == expected_value,
        },
        {
            "id": f"B:{family}:schema",
            "pass": sorted(solution) == [expected_key],
        },
        {
            "id": f"B:{family}:resource",
            "pass": resource_cost(family, solution) <= resource_budget(state),
        },
    ]
    return {
        "schema": "maofield.glm53.objective_scorer_b.v2",
        "scorer": "B",
        "tests": tests,
        "U": sum(int(test["pass"]) for test in tests) / len(tests),
    }
