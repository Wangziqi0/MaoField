from __future__ import annotations
from pathlib import Path
from collections import defaultdict
import json
import os
from .canonical import canonical_json_bytes, hkdf_expand, hkdf_extract, sha256_bytes
from .statistics import (
    ALPHA,
    BOOTSTRAPS,
    PERMUTATIONS,
    equivalence_test,
    holm,
    iut,
    linear_missing_bounds,
    simultaneous_bootstrap,
    superiority_test,
)

CELLS = ("S", "C", "R0", "R1")
ENDPOINTS = ("U", "A_FT", "P", "ORDERED_O", "NON_TARGET")
CONTRASTS = (
    ("S_DN_UF", "equivalence", {("DN", "S"): 1, ("UF", "S"): -1}, 0.10),
    ("C_DN_UF", "superiority", {("DN", "C"): 1, ("UF", "C"): -1}, 0.15),
    ("C_MINUS_S", "superiority", {("DN", "C"): 1, ("UF", "C"): -1, ("DN", "S"): -1, ("UF", "S"): 1}, 0.15),
    ("R0_DN_UF", "equivalence", {("DN", "R0"): 1, ("UF", "R0"): -1}, 0.10),
    ("R1_DN_UF", "superiority", {("DN", "R1"): 1, ("UF", "R1"): -1}, 0.15),
    ("R1_MINUS_R0", "superiority", {("DN", "R1"): 1, ("UF", "R1"): -1, ("DN", "R0"): -1, ("UF", "R0"): 1}, 0.15),
    ("C_DN_X", "superiority", {("DN", "C"): 1, ("X", "C"): -1}, 0.15),
    ("R1_DN_X", "superiority", {("DN", "R1"): 1, ("X", "R1"): -1}, 0.15),
    ("C_DN_CO", "superiority", {("DN", "C"): 1, ("CO", "C"): -1}, 0.10),
    ("R1_DN_CO", "superiority", {("DN", "R1"): 1, ("CO", "R1"): -1}, 0.10),
    ("C_DN_N0", "superiority", {("DN", "C"): 1, ("N0", "C"): -1}, 0.10),
    ("R1_DN_N0", "superiority", {("DN", "R1"): 1, ("N0", "R1"): -1}, 0.10),
)


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def _analysis_keys(root_key: bytes) -> tuple[bytes, bytes]:
    prk = hkdf_extract(b"MAOFIELD/GLM53/V2/ANALYSIS-SALT", root_key)
    return (
        hkdf_expand(prk, b"MAOFIELD/GLM53/V2/PERMUTATION", 32),
        hkdf_expand(prk, b"MAOFIELD/GLM53/V2/BOOTSTRAP", 32),
    )


def _block_values(rows: list[dict], endpoint: str) -> dict[int, dict[tuple[str, str], float | None]]:
    output: dict[int, dict[tuple[str, str], float | None]] = defaultdict(dict)
    for row in rows:
        assignment = row.get("assignment")
        if not assignment:
            continue
        value = None
        if row.get("status") == "EVALUABLE":
            value = row.get("endpoints", {}).get(endpoint)
        output[row["superblock"]][(assignment["arm"], assignment["cell"])] = value
    return output


def _contrast_vector(blocks: dict, coefficients: dict) -> tuple[list[float], dict]:
    complete: list[float] = []
    grouped = {group: [] for group in coefficients}
    for superblock in sorted(blocks):
        mapping = blocks[superblock]
        values = [mapping.get(group) for group in coefficients]
        for group in coefficients:
            grouped[group].append(mapping.get(group))
        if all(value is not None for value in values):
            complete.append(sum(coefficients[group] * mapping[group] for group in coefficients))
    bounds = linear_missing_bounds(grouped, coefficients)
    return complete, bounds


def analyze_endpoint(rows: list[dict], endpoint: str, permutation_key: bytes, bootstrap_key: bytes, label: str) -> dict:
    blocks = _block_values(rows, endpoint)
    tests: dict[str, dict] = {}
    matrix_rows: list[list[float]] = []
    matrix_ids: list[str] = []
    vectors: dict[str, list[float]] = {}
    for contrast_id, kind, coefficients, threshold in CONTRASTS:
        differences, bounds = _contrast_vector(blocks, coefficients)
        vectors[contrast_id] = differences
        context = f"{label}/{endpoint}/{contrast_id}".encode("utf-8")
        if not differences:
            test = {"p": 1.0, "estimate": None, "n": 0, "status": "NOT_IDENTIFIED_NO_COMPLETE_BLOCKS"}
        elif kind == "equivalence":
            test = equivalence_test(differences, threshold, permutation_key, context)
        else:
            test = superiority_test(differences, threshold, permutation_key, context)
        tests[contrast_id] = {**test, "missing_bounds": bounds, "kind": kind}
    # Simultaneous intervals use the common minimum number of complete blocks; every contrast is paired by sorted block order.
    common_n = min((len(values) for values in vectors.values()), default=0)
    intervals = {}
    if common_n >= 2:
        matrix = [[vectors[cid][index] for cid, *_ in CONTRASTS] for index in range(common_n)]
        ci_rows = simultaneous_bootstrap(matrix, bootstrap_key, f"{label}/{endpoint}".encode("utf-8"))
        intervals = {contrast[0]: ci for contrast, ci in zip(CONTRASTS, ci_rows)}
    constituents = {contrast_id: tests[contrast_id] for contrast_id, *_ in CONTRASTS}
    return {
        "endpoint": endpoint,
        "blocks_registered": len(blocks),
        "tests": tests,
        "simultaneous_intervals": intervals,
        "full_signature": iut(constituents),
    }


def ordinary_calibration(rows: list[dict]) -> dict:
    result = {}
    for endpoint in ("P", "ORDERED_O", "A_FT", "U"):
        values = [row.get("endpoints", {}).get(endpoint) if row.get("status") == "EVALUABLE" else None for row in rows]
        successes = sum(value == 1 or value == 1.0 for value in values)
        result[endpoint] = {"successes": successes, "n": 32, "valid": successes >= 22, "threshold": 22}
    return result


def structure_calibration(rows: list[dict]) -> dict:
    values = [row.get("STRUCTURE_CRITERION") if row.get("status") == "EVALUABLE" else None for row in rows]
    successes = sum(value == 1 for value in values)
    paired = defaultdict(dict)
    for row in rows:
        paired[row.get("criterion_case")][row.get("renderer")] = row.get("STRUCTURE_CRITERION")
    mismatches = sum(pair.get("A") != pair.get("B") for pair in paired.values() if set(pair) == {"A", "B"})
    return {"successes": successes, "n": 32, "renderer_mismatches": mismatches, "valid": successes >= 29 and mismatches == 0, "threshold": 29}


def analyze_run(run_root: Path, analysis_root_key: bytes, output_root: Path) -> dict:
    if output_root.exists():
        raise RuntimeError("ANALYSIS_OUTPUT_EXISTS")
    output_root.mkdir(parents=True)
    permutation_key, bootstrap_key = _analysis_keys(analysis_root_key)
    main_path = run_root / "PRIVATE_ENDPOINTS_MAIN96.jsonl"
    sealed_path = run_root / "PRIVATE_ENDPOINTS_SEALED32.jsonl"
    auxiliary_path = run_root / "PRIVATE_ENDPOINTS_AUXILIARY.jsonl"
    main_rows = _read_jsonl(main_path)
    main_results = {endpoint: analyze_endpoint(main_rows, endpoint, permutation_key, bootstrap_key, "MAIN96") for endpoint in ENDPOINTS}
    freeze = {"schema":"maofield.glm53.analysis_main96_freeze.v2","main_endpoint_sha256":sha256_bytes(main_path.read_bytes()),"main_analysis_sha256":sha256_bytes(canonical_json_bytes(main_results)),"sealed32_read":False}
    freeze_path = output_root / "ANALYSIS_MAIN96_FREEZE_RECEIPT.json"
    with open(freeze_path, "xb") as handle:
        handle.write(canonical_json_bytes(freeze)); handle.flush(); os.fsync(handle.fileno())
    sealed_rows = _read_jsonl(sealed_path)
    freeze["sealed32_read"] = True
    sealed_results = {endpoint: analyze_endpoint(sealed_rows, endpoint, permutation_key, bootstrap_key, "SEALED32") for endpoint in ENDPOINTS}
    auxiliary = _read_jsonl(auxiliary_path)
    ordinary = ordinary_calibration([row for row in auxiliary if row["channel"] == "ORDINARY_CONTROL"])
    structure_criterion = structure_calibration([row for row in auxiliary if row["channel"] == "STRUCTURE_CRITERION"])
    sibling_main = [row for row in auxiliary if row["channel"] in ("ACTION_SIBLING", "STRUCTURE") and row["superblock"] <= 48]
    sibling_sealed = [row for row in auxiliary if row["channel"] in ("ACTION_SIBLING", "STRUCTURE") and row["superblock"] > 48]
    sibling = {"main48": _analyze_siblings(sibling_main, permutation_key, bootstrap_key, "SIB_MAIN48"), "sealed16": _analyze_siblings(sibling_sealed, permutation_key, bootstrap_key, "SIB_SEALED16")}
    p1_candidate = bool(ordinary["U"]["valid"] and main_results["U"]["full_signature"]["pass"] and sealed_results["U"]["full_signature"]["pass"])
    p5_candidate = any(
        ordinary.get(endpoint if endpoint != "ORDERED_O" else "ORDERED_O", {"valid": False})["valid"]
        and main_results[endpoint]["full_signature"]["pass"]
        and sealed_results[endpoint]["full_signature"]["pass"]
        for endpoint in ("U", "A_FT", "P", "ORDERED_O")
    )
    def all_zero_region(result):
        cis=result.get("simultaneous_intervals",{})
        return bool(cis) and all(row["lower"] >= -0.10 and row["upper"] <= 0.10 for row in cis.values())
    bounded_zero_candidate = bool(ordinary["U"]["valid"] and all_zero_region(main_results["U"]) and all_zero_region(sealed_results["U"]))
    p2_candidate = bool(structure_criterion["valid"] and ordinary["A_FT"]["valid"] and sibling["main48"].get("P2",{}).get("pass") and sibling["sealed16"].get("P2",{}).get("pass"))
    p3_candidate = bool(structure_criterion["valid"] and ordinary["A_FT"]["valid"] and sibling["main48"].get("P3",{}).get("pass") and sibling["sealed16"].get("P3",{}).get("pass"))
    behavior_family={endpoint:max(main_results[endpoint]["full_signature"]["p"],sealed_results[endpoint]["full_signature"]["p"]) for endpoint in ("A_FT","P","ORDERED_O")}
    holm_families={
        "U_PRIMARY":holm({"U":max(main_results["U"]["full_signature"]["p"],sealed_results["U"]["full_signature"]["p"])}),
        "BEHAVIOR_SECONDARY":holm(behavior_family),
        "DISSOCIATION_DIRECTION":holm({"P2":max(sibling["main48"]["A_MINUS_R"]["p"],sibling["sealed16"]["A_MINUS_R"]["p"]),"P3":max(sibling["main48"]["R_MINUS_A"]["p"],sibling["sealed16"]["R_MINUS_A"]["p"])})
    }
    any_behavior_complete=any(main_results[e]["blocks_registered"]>0 for e in ("U","A_FT","P","ORDERED_O"))
    if p1_candidate:
        terminal = "P1_DIRECT_BEHAVIORAL_HFI_CANDIDATE"
    elif p5_candidate:
        terminal = "P5_FINITE_INTERVENTIONAL_NONCLOSURE_WITNESS_CANDIDATE"
    elif bounded_zero_candidate:
        terminal = "BOUNDED_OBJECTIVE_ZERO_CANDIDATE"
    elif p2_candidate:
        terminal = "P2_CANDIDATE"
    elif p3_candidate:
        terminal = "P3_CANDIDATE"
    elif not any_behavior_complete:
        terminal = "OBJECTIVE_BEHAVIOR_NON_EVALUABLE"
    elif not all(row["valid"] for row in ordinary.values()):
        terminal = "CROSS_PROVIDER_MEASUREMENT_BOUNDARY_REPLICATION; NO_FURTHER_EXPERIMENT"
    else:
        terminal = "MIXED_OR_INCONCLUSIVE"
    result = {"schema":"maofield.glm53.formal_scientific_result.v2","main96":main_results,"sealed32":sealed_results,"ordinary_criterion":ordinary,"structure_criterion":structure_criterion,"siblings":sibling,"holm_families":holm_families,"claims":{"P1":p1_candidate,"P5":p5_candidate,"BOUNDED_ZERO":bounded_zero_candidate,"P2":p2_candidate,"P3":p3_candidate},"terminal_label":terminal,"statistics":{"permutations":PERMUTATIONS,"bootstraps":BOOTSTRAPS,"alpha":ALPHA},"automatic_next_round":False}
    (output_root / "FORMAL_RESULT.json").write_bytes(canonical_json_bytes(result))
    return result


def _analyze_siblings(rows: list[dict], permutation_key: bytes, bootstrap_key: bytes, label: str) -> dict:
    by_channel = {"ACTION_SIBLING": [], "STRUCTURE": []}
    for row in rows:
        by_channel[row["channel"]].append(row)
    # Normalize A_SIB and R into the same [0,1] scale and use the frozen C DN-UF contrast as the main gap witness.
    def values(channel, endpoint):
        mapped=defaultdict(dict)
        for row in by_channel[channel]:
            assignment=row.get("assignment"); value=row.get(endpoint) if row.get("status")=="EVALUABLE" else None
            mapped[row["superblock"]][(assignment["arm"],assignment["cell"])]=value
        diffs=[]
        for sb in sorted(mapped):
            a=mapped[sb].get(("DN","C")); b=mapped[sb].get(("UF","C"))
            if a is not None and b is not None: diffs.append(a-b)
        return diffs
    a=values("ACTION_SIBLING","A_SIB"); r=values("STRUCTURE","R")
    n=min(len(a),len(r)); gap=[a[i]-r[i] for i in range(n)]
    if n:
        a_test=superiority_test(a,.15,permutation_key,(label+"/A").encode())
        r_pos=superiority_test(r,.15,permutation_key,(label+"/R_POS").encode())
        r_null=equivalence_test(r,.10,permutation_key,(label+"/R_NULL").encode())
        a_null=equivalence_test(a,.10,permutation_key,(label+"/A_NULL").encode())
        p2_gap=superiority_test(gap,.05,permutation_key,(label+"/P2_GAP").encode())
        p3_gap=superiority_test([-x for x in gap],.05,permutation_key,(label+"/P3_GAP").encode())
    else:
        blank={"p":1.0,"estimate":None,"n":0}; a_test=r_pos=r_null=a_null=p2_gap=p3_gap=blank
    return {"A_SIB_C_DN_UF":a_test,"R_C_DN_UF_POS":r_pos,"R_C_DN_UF_NULL":r_null,"A_SIB_C_DN_UF_NULL":a_null,"A_MINUS_R":p2_gap,"R_MINUS_A":p3_gap,"P2":{"pass":a_test["p"]<=ALPHA and r_null["p"]<=ALPHA and p2_gap["p"]<=ALPHA},"P3":{"pass":r_pos["p"]<=ALPHA and a_null["p"]<=ALPHA and p3_gap["p"]<=ALPHA},"n_paired":n}
