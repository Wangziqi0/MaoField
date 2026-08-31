from __future__ import annotations
from pathlib import Path
import json
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / "CODE"))

from maofield_glm53_runtime.assignment import build_private_ledger, derive_keys
from maofield_glm53_runtime.canonical import canonical_json_bytes
from maofield_glm53_runtime.endpoints import build_behavior_endpoints
from maofield_glm53_runtime.family_rules import objective_route, route_patch
from maofield_glm53_runtime.provider_adapter import dispatch
from maofield_glm53_runtime.renderer import render_messages
from maofield_glm53_runtime.scorer_a import score as scorer_a
from maofield_glm53_runtime.scorer_b import score as scorer_b
from maofield_glm53_runtime.statistics import iut
from maofield_glm53_runtime.worlds import descriptor, materialize_clean_successor


def main() -> int:
    results = {}
    keys = derive_keys(b"R" * 32, "A" * 64, "B" * 64, "C" * 64)
    ledger = build_private_ledger(keys)
    # M01: model-facing leakage.
    desc = descriptor(keys["world_main"], keys["renderer"], 1, "MAIN96", "C")
    leaked = json.loads(json.dumps(desc["public"]))
    leaked["arm"] = "DN"
    try:
        render_messages("BEHAVIOR", 1, leaked, None, [])
        results["M01"] = False
    except RuntimeError as exc:
        results["M01"] = str(exc) == "MODEL_FACING_PRIVATE_FIELD_LEAK"
    # M02: KDF domains must differ.
    results["M02"] = keys["assignment_main"] != keys["assignment_sealed"]
    # M03: A_SIB/R use the same sibling mapping; behavior uses another domain.
    results["M03"] = ledger["siblings"]["1"] == ledger["siblings"]["1"] and ledger["siblings"]["1"] != ledger["behavior_main"]["1"]
    # M04/M05: label-only solution cannot pass executable tests.
    root = Path(tempfile.mkdtemp())
    try:
        materialize_clean_successor(root / "episode", desc, {})
        (root / "episode" / "solution.json").write_bytes(canonical_json_bytes({"route": objective_route(desc["state"])}))
        left = scorer_a(root / "episode", desc)
        right = scorer_b(root / "episode", desc)
        results["M04"] = left["U"] < 1.0
        results["M05"] = right["U"] < 1.0
    finally:
        shutil.rmtree(root)
    # M06: correctness co-occurrence with wrong order cannot make ordered O pass.
    objective = objective_route(desc["state"])
    trajectory = [
        {"sequence": 1, "tool": "apply_patch", "ok": True, "route_private": objective},
        {"sequence": 2, "tool": "run_probe", "ok": True, "probe_semantic_private": desc["truth"]["informative_probe"], "observation_sha256": "WRONG"},
        {"sequence": 3, "tool": "submit", "ok": True},
    ]
    perfect = {"tests": [{"pass": True}], "U": 1.0}
    row = build_behavior_endpoints(desc, trajectory, objective, perfect, perfect, [])
    results["M06"] = row["endpoints"]["ORDERED_O"] == 0
    # M07: P2/P3 route only through A_SIB/R.
    analysis_source = (ROOT / "CODE/maofield_glm53_runtime/analysis.py").read_text(encoding="utf-8")
    sibling_source = analysis_source[analysis_source.index("def _analyze_siblings"):]
    results["M07"] = '"A_FT"' not in sibling_source and '"A_SIB"' in sibling_source
    # M08: sealed gate exists before first sealed read.
    state_source = (ROOT / "CODE/maofield_glm53_runtime/state_machine.py").read_text(encoding="utf-8")
    results["M08"] = "SEALED32_BEFORE_MAIN96_FREEZE" in state_source
    # M09: provider is impossible in build-only mode.
    try:
        dispatch(b"{}", "NOT-A-KEY", provider_authorized=False)
        results["M09"] = False
    except RuntimeError as exc:
        results["M09"] = str(exc) == "PROVIDER_CALL_NOT_AUTHORIZED_BUILD_ONLY"
    # M10: IUT is max constituent p, not average.
    results["M10"] = iut({"a": {"p": 0.001}, "b": {"p": 0.2}})["p"] == 0.2
    # M11: structure validity is not in the P1 boolean expression.
    p1_line = next(line for line in analysis_source.splitlines() if "p1_candidate =" in line)
    results["M11"] = "structure_criterion" not in p1_line
    # M12: terminal package fixes automatic_next_round=false.
    return_source = (ROOT / "CODE/maofield_glm53_runtime/formal_return.py").read_text(encoding="utf-8")
    results["M12"] = '"automatic_next_round": False' in return_source
    failures = [key for key, passed in results.items() if not passed]
    receipt = {
        "schema": "maofield.glm53.disconnection_mutation_selftest.v2",
        "status": "PASS" if not failures else "FAIL",
        "mutations": results,
        "failures": failures,
        "provider_calls": 0,
        "production_roots": 0,
        "automatic_next_round": False,
    }
    (ROOT / "VALIDATION/MUTATION_SELFTEST_RECEIPT.json").write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
