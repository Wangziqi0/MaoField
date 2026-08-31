from __future__ import annotations
import json
from pathlib import Path
from .family_rules import test_solution_a


def score(root: Path, private_world: dict) -> dict:
    state = json.loads((root / "state.json").read_text(encoding="utf-8"))
    solution = json.loads((root / "solution.json").read_text(encoding="utf-8"))
    tests = test_solution_a(state, solution)
    return {
        "schema": "maofield.glm53.objective_scorer_a.v2",
        "scorer": "A",
        "tests": tests,
        "U": sum(int(test["pass"]) for test in tests) / len(tests),
    }
