from __future__ import annotations
from pathlib import Path
import ast
import json
import sys

ROOT = Path(__file__).resolve().parents[1]


def symbols(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    result = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            result.add(node.name)
            if isinstance(node, ast.ClassDef):
                for child in node.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        result.add(node.name + "." + child.name)
    return result


def source(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> int:
    registry = json.loads((ROOT / "GOVERNANCE/NORMATIVE_REQUIREMENT_REGISTRY.json").read_text(encoding="utf-8"))
    failures = []
    for row in registry["entries"]:
        relative, symbol = row["production_locator"].split("::", 1)
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"MISSING_FILE:{row['id']}:{relative}")
            continue
        if symbol not in symbols(path):
            failures.append(f"MISSING_SYMBOL:{row['id']}:{symbol}")
        if relative.endswith("config.py"):
            failures.append(f"CONFIG_ONLY_LOCATOR:{row['id']}")
    edges = {
        "formal_runner_to_state_machine": ("CODE/maofield_glm53_runtime/formal_runner.py", "run_schedule("),
        "formal_runner_to_analysis": ("CODE/maofield_glm53_runtime/formal_runner.py", "analyze_run("),
        "formal_runner_to_return": ("CODE/maofield_glm53_runtime/formal_runner.py", "build_formal_return("),
        "state_to_assignment": ("CODE/maofield_glm53_runtime/state_machine.py", "assignment_for("),
        "state_to_world": ("CODE/maofield_glm53_runtime/state_machine.py", "descriptor("),
        "state_to_source_practice": ("CODE/maofield_glm53_runtime/state_machine.py", "materialize_source_practice("),
        "state_to_history": ("CODE/maofield_glm53_runtime/state_machine.py", "build_cards("),
        "state_to_renderer": ("CODE/maofield_glm53_runtime/state_machine.py", "render_messages("),
        "state_to_request": ("CODE/maofield_glm53_runtime/state_machine.py", "request_body("),
        "state_to_parser": ("CODE/maofield_glm53_runtime/state_machine.py", "parse_provider_response("),
        "state_to_tool_environment": ("CODE/maofield_glm53_runtime/state_machine.py", ".execute("),
        "state_to_scorer_A": ("CODE/maofield_glm53_runtime/state_machine.py", "scorer_a("),
        "state_to_scorer_B": ("CODE/maofield_glm53_runtime/state_machine.py", "scorer_b("),
        "state_to_endpoint": ("CODE/maofield_glm53_runtime/state_machine.py", "build_behavior_endpoints("),
        "analysis_to_permutation": ("CODE/maofield_glm53_runtime/analysis.py", "superiority_test("),
        "analysis_to_equivalence": ("CODE/maofield_glm53_runtime/analysis.py", "equivalence_test("),
        "analysis_to_bootstrap": ("CODE/maofield_glm53_runtime/analysis.py", "simultaneous_bootstrap("),
        "analysis_to_holm": ("CODE/maofield_glm53_runtime/analysis.py", "holm("),
        "analysis_to_IUT": ("CODE/maofield_glm53_runtime/analysis.py", "iut("),
    }
    edge_receipts = {}
    for edge, (relative, needle) in edges.items():
        present = needle in source(relative)
        edge_receipts[edge] = present
        if not present:
            failures.append("DISCONNECTED_EDGE:" + edge)
    mutation_registry = json.loads((ROOT / "VALIDATION/DISCONNECTION_MUTATION_REGISTRY.json").read_text(encoding="utf-8"))
    if mutation_registry["count"] != len(mutation_registry["mutations"]):
        failures.append("MUTATION_COUNT")
    receipt = {
        "schema": "maofield.glm53.runtime_reachability_receipt.v2",
        "status": "PASS" if not failures else "FAIL",
        "requirements": len(registry["entries"]),
        "production_edges": edge_receipts,
        "mutations": len(mutation_registry["mutations"]),
        "failures": failures,
        "provider_calls": 0,
        "production_roots": 0,
        "automatic_next_round": False,
    }
    output = ROOT / "VALIDATION/RUNTIME_REACHABILITY_RECEIPT.json"
    output.write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
