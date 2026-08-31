from __future__ import annotations
from pathlib import Path
import json
from .canonical import canonical_json_bytes, hmac_sha256, sha256_bytes
from .family_rules import (
    ROUTES,
    family_for,
    informative_probe,
    objective_route,
    probe_output,
    public_state,
    route_patch,
    test_solution_a,
)

PROBES = ("PROBE_REGIME", "PROBE_METADATA", "PROBE_COST", "PROBE_NONE")


def _opaque(key: bytes, kind: str, semantic: str, world_id: str) -> str:
    return kind[:1] + hmac_sha256(
        key, f"{kind}\0{world_id}\0{semantic}".encode("utf-8")
    ).hex().upper()[:15]


def descriptor(
    world_key: bytes,
    renderer_key: bytes,
    superblock: int,
    stratum: str,
    cell: str,
    namespace: str = "BEHAVIOR",
) -> dict:
    if stratum in ("MAIN96", "SEALED32"):
        family = family_for(superblock, stratum)
    elif stratum == "INDEPENDENT64":
        from .family_rules import MAIN_FAMILIES, SEALED_FAMILIES
        family = MAIN_FAMILIES[(superblock - 1) // 12] if superblock <= 48 else SEALED_FAMILIES[(superblock - 49) // 2]
    elif stratum == "CONTROL32":
        from .family_rules import MAIN_FAMILIES, SEALED_FAMILIES
        family = MAIN_FAMILIES[(superblock - 1) // 6] if superblock <= 24 else SEALED_FAMILIES[superblock - 25]
    else:
        raise ValueError("WORLD_STRATUM")
    world_id = sha256_bytes(
        hmac_sha256(world_key, f"WORLD\0{namespace}\0{stratum}\0{superblock}".encode("ascii"))
    )
    state = public_state(family, cell, world_id)
    action_alias_private = {
        _opaque(renderer_key, "ACTION", route, world_id): route for route in ROUTES
    }
    probe_alias_private = {
        _opaque(renderer_key, "PROBE", probe, world_id): probe for probe in PROBES
    }
    action_public = []
    for alias, route in sorted(action_alias_private.items()):
        action_public.append(
            {
                "id": alias,
                "candidate_patch": route_patch(family, route),
                "cost_units": {"LEGACY": 5, "ADAPT": 4, "NEUTRAL": 2, "DECOY": 8}[route],
            }
        )
    probe_public = []
    descriptions = {
        "PROBE_REGIME": "execute a diagnostic of the current material/interface regime",
        "PROBE_METADATA": "read static project metadata only",
        "PROBE_COST": "read the current resource budget only",
        "PROBE_NONE": "return no diagnostic information",
    }
    for alias, semantic in sorted(probe_alias_private.items()):
        probe_public.append({"id": alias, "description": descriptions[semantic]})
    public = {
        "world_id": world_id,
        "family": family,
        "repository_files": ["README.txt", "state.json", "solution.json"],
        "state": state,
        "actions": action_public,
        "probes": probe_public,
        "resource_budget": state.get("budget", 10),
        "maximum_tool_turns": 6,
    }
    return {
        "schema": "maofield.glm53.world_descriptor.v2",
        "namespace": namespace,
        "world_id": world_id,
        "family": family,
        "stratum": stratum,
        "superblock": superblock,
        "cell_private": cell,
        "state": state,
        "public": public,
        "action_alias_private": action_alias_private,
        "probe_alias_private": probe_alias_private,
        "truth": {
            "objective_route": objective_route(state),
            "informative_probe": informative_probe(family),
        },
    }


def materialize_source_practice(root: Path, desc: dict) -> dict:
    root.mkdir(parents=True, exist_ok=False)
    source_state = public_state(
        desc["family"], "C", desc["world_id"] + "-SOURCE-PREDECESSOR"
    )
    historical_solution = route_patch(desc["family"], "LEGACY")
    tests = test_solution_a(source_state, historical_solution)
    receipt = {
        "schema": "maofield.glm53.predecessor_practice.v2",
        "world_id": desc["world_id"],
        "route": "LEGACY",
        "command": "python -I source_decisive_test.py",
        "stdout": json.dumps(tests, sort_keys=True, separators=(",", ":")),
        "stderr": "",
        "exit_code": 0 if all(test["pass"] for test in tests) else 1,
        "tests": tests,
        "scope": {"family": desc["family"], "regime": "old"},
        "reopening_condition": {"regime": "new"},
    }
    if receipt["exit_code"] == 0:
        raise RuntimeError("SOURCE_PRACTICE_DID_NOT_FALSIFY_LEGACY")
    (root / "SOURCE_PRACTICE.json").write_bytes(canonical_json_bytes(receipt))
    return receipt


def materialize_clean_successor(root: Path, desc: dict, history_card: dict) -> Path:
    root.mkdir(parents=True, exist_ok=False)
    (root / "README.txt").write_text(
        "MaoField GLM-5.3-Flash clean-successor executable world.\n",
        encoding="utf-8",
        newline="\n",
    )
    (root / "state.json").write_bytes(canonical_json_bytes(desc["state"]))
    (root / "solution.json").write_bytes(canonical_json_bytes({}))
    (root / "WORLD_PUBLIC.json").write_bytes(canonical_json_bytes(desc["public"]))
    (root / "HISTORY_CARD.json").write_bytes(canonical_json_bytes(history_card))
    return root


def execute_probe(desc: dict, probe_id: str) -> dict:
    semantic = desc["probe_alias_private"].get(probe_id)
    if semantic is None:
        raise ValueError("PROBE_NOT_IN_CATALOGUE")
    observation = probe_output(desc["state"], semantic)
    return {
        "probe_id": probe_id,
        "observation": observation,
        "observation_sha256": sha256_bytes(canonical_json_bytes(observation)),
        "semantic_private": semantic,
    }


def apply_action(root: Path, desc: dict, action_id: str) -> dict:
    route = desc["action_alias_private"].get(action_id)
    if route is None:
        raise ValueError("ACTION_NOT_IN_CATALOGUE")
    patch = route_patch(desc["family"], route)
    (root / "solution.json").write_bytes(canonical_json_bytes(patch))
    return {
        "action_id": action_id,
        "route_private": route,
        "patch_sha256": sha256_bytes(canonical_json_bytes(patch)),
    }
