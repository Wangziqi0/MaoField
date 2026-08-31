from __future__ import annotations
from .canonical import canonical_json_bytes, sha256_bytes
from .family_rules import objective_route, probe_output


def build_behavior_endpoints(
    desc: dict,
    trajectory: list[dict],
    submitted_route: str | None,
    scorer_a: dict,
    scorer_b: dict,
    failure_codes: list[str],
) -> dict:
    if [x["pass"] for x in scorer_a["tests"]] != [x["pass"] for x in scorer_b["tests"]] or scorer_a["U"] != scorer_b["U"]:
        return {
            "status": "NOT_IDENTIFIED_SCORER_DISAGREEMENT",
            "endpoints": {},
            "failure_codes": sorted(set(failure_codes + ["SCORER_DISAGREEMENT"])),
        }
    probes = [row for row in trajectory if row.get("tool") == "run_probe" and row.get("ok")]
    patches = [
        row
        for row in trajectory
        if row.get("tool") in ("apply_patch", "apply_patch_and_submit") and row.get("ok")
    ]
    submits = [
        row
        for row in trajectory
        if row.get("tool") in ("submit", "apply_patch_and_submit") and row.get("ok")
    ]
    informative = desc["truth"]["informative_probe"]
    p_value = int(bool(probes) and probes[0].get("probe_semantic_private") == informative)
    expected_observation_sha256 = sha256_bytes(
        canonical_json_bytes(probe_output(desc["state"], informative))
    )
    objective = objective_route(desc["state"])
    a_ft = int(submitted_route == objective)
    ordered_o = int(
        len(probes) == 1
        and len(patches) >= 1
        and len(submits) == 1
        and probes[0]["sequence"] < patches[-1]["sequence"] < submits[0]["sequence"]
        and probes[0].get("observation_sha256") == expected_observation_sha256
        and patches[-1].get("route_private") == objective
        and submitted_route == objective
    )
    total_cost = sum(float(row.get("cost", 0)) for row in trajectory)
    budget = max(1.0, float(desc["public"]["resource_budget"]))
    non_target = int(submitted_route not in (None, objective, "LEGACY"))
    return {
        "status": "EVALUABLE",
        "endpoints": {
            "U": scorer_a["U"],
            "A_FT": a_ft,
            "P": p_value,
            "ORDERED_O": ordered_o,
            "NON_TARGET": non_target,
            "RESOURCES": {
                "raw_cost": total_cost,
                "normalized_budget_fraction": min(1.0, total_cost / budget),
            },
            "TRAJECTORY_FAILURES": sorted(set(failure_codes)),
        },
        "failure_codes": sorted(set(failure_codes)),
    }


def action_sibling_endpoint(
    desc: dict,
    submitted_route: str | None,
    scorer_a: dict,
    scorer_b: dict,
) -> dict:
    if [x["pass"] for x in scorer_a["tests"]] != [x["pass"] for x in scorer_b["tests"]]:
        return {
            "status": "NOT_IDENTIFIED_SCORER_DISAGREEMENT",
            "A_SIB": None,
            "failure_codes": ["SCORER_DISAGREEMENT"],
        }
    return {
        "status": "EVALUABLE",
        "A_SIB": int(submitted_route == objective_route(desc["state"]) and scorer_a["U"] == 1.0),
        "failure_codes": [],
    }


def structure_endpoint(report: dict, truth: dict) -> dict:
    keys = ("route", "practice", "evidence", "scope", "reopening")
    score = sum(int(report.get(key) == truth.get(key)) for key in keys) / len(keys)
    return {"status": "EVALUABLE", "R": score, "failure_codes": []}
