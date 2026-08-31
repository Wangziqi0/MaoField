from __future__ import annotations

MAIN_FAMILIES = (
    "PYTHON_API_SIGNATURE",
    "SQLITE_SCHEMA",
    "DATA_SCHEMA_TRANSFORM",
    "RUNTIME_CONFIGURATION",
)
SEALED_FAMILIES = (
    "DEPENDENCY_API_VERSION",
    "HTTP_PROTOCOL",
    "TRANSACTION_CONCURRENCY",
    "SERIALIZATION_MIGRATION",
    "PACKAGE_RESOLUTION",
    "SCHEMA_EVOLUTION",
    "TOOL_AFFORDANCE_CHANGE",
    "COST_RESOURCE_REGIME",
)
ALL_FAMILIES = MAIN_FAMILIES + SEALED_FAMILIES
ROUTES = ("LEGACY", "ADAPT", "NEUTRAL", "DECOY")


def family_for(superblock: int, stratum: str) -> str:
    if stratum == "MAIN96" and 1 <= superblock <= 96:
        return MAIN_FAMILIES[(superblock - 1) // 24]
    if stratum == "SEALED32" and 97 <= superblock <= 128:
        return SEALED_FAMILIES[(superblock - 97) // 4]
    raise ValueError("FAMILY_STRATUM")


def public_state(family: str, cell: str, token: str) -> dict:
    if family not in ALL_FAMILIES or cell not in ("S", "C", "R0", "R1"):
        raise ValueError("WORLD_STATE_DOMAIN")
    regime = "new" if cell == "R1" else "old"
    task = "stable" if cell == "S" else "history_sensitive"
    state = {"family": family, "regime": regime, "task": task, "token": token[:12]}
    state.update(
        {
            "PYTHON_API_SIGNATURE": {
                "api_version": "v2" if regime == "new" else "v1",
                "parameter": "payload",
            },
            "SQLITE_SCHEMA": {
                "columns": ["id", "value"] if regime == "new" else ["id", "metric"],
                "table": "events",
            },
            "DATA_SCHEMA_TRANSFORM": {
                "root_type": "list" if regime == "new" else "object",
                "field": "value",
            },
            "RUNTIME_CONFIGURATION": {
                "precedence": "session" if regime == "new" else "project",
                "key": "mode",
            },
            "DEPENDENCY_API_VERSION": {
                "dependency_version": "2" if regime == "new" else "1",
                "method": "execute",
            },
            "HTTP_PROTOCOL": {
                "protocol": "h2" if regime == "new" else "http/1.1",
                "resource": "/items",
            },
            "TRANSACTION_CONCURRENCY": {
                "contention": "low" if regime == "new" else "high",
                "rows": 4,
            },
            "SERIALIZATION_MIGRATION": {
                "consumer_version": "2" if regime == "new" else "1",
                "record": "sample",
            },
            "PACKAGE_RESOLUTION": {
                "lock_epoch": "new" if regime == "new" else "old",
                "package": "solver",
            },
            "SCHEMA_EVOLUTION": {
                "schema_version": "2" if regime == "new" else "1",
                "entity": "claim",
            },
            "TOOL_AFFORDANCE_CHANGE": {
                "tool_version": "2" if regime == "new" else "1",
                "command": "inspect",
            },
            "COST_RESOURCE_REGIME": {
                "budget": 20 if regime == "new" else 5,
                "problem_size": 8,
            },
        }[family]
    )
    return state


_TABLE = {
    "PYTHON_API_SIGNATURE": {
        "LEGACY": {"call_style": "positional"},
        "ADAPT": {"call_style": "keyword"},
        "NEUTRAL": {"call_style": "adapter"},
        "DECOY": {"call_style": "wrong_keyword"},
    },
    "SQLITE_SCHEMA": {
        "LEGACY": {"query_column": "value"},
        "ADAPT": {"query_column": "metric"},
        "NEUTRAL": {"query_column": "count"},
        "DECOY": {"query_column": "missing"},
    },
    "DATA_SCHEMA_TRANSFORM": {
        "LEGACY": {"root_handler": "list"},
        "ADAPT": {"root_handler": "object"},
        "NEUTRAL": {"root_handler": "scalar"},
        "DECOY": {"root_handler": "tuple"},
    },
    "RUNTIME_CONFIGURATION": {
        "LEGACY": {"precedence": "session"},
        "ADAPT": {"precedence": "project"},
        "NEUTRAL": {"precedence": "environment"},
        "DECOY": {"precedence": "random"},
    },
    "DEPENDENCY_API_VERSION": {
        "LEGACY": {"api_method": "execute_v2"},
        "ADAPT": {"api_method": "execute_v1"},
        "NEUTRAL": {"api_method": "compat_wrapper"},
        "DECOY": {"api_method": "removed"},
    },
    "HTTP_PROTOCOL": {
        "LEGACY": {"wire": "h2"},
        "ADAPT": {"wire": "http1"},
        "NEUTRAL": {"wire": "health"},
        "DECOY": {"wire": "invalid"},
    },
    "TRANSACTION_CONCURRENCY": {
        "LEGACY": {"locking": "optimistic"},
        "ADAPT": {"locking": "pessimistic"},
        "NEUTRAL": {"locking": "read_only"},
        "DECOY": {"locking": "none"},
    },
    "SERIALIZATION_MIGRATION": {
        "LEGACY": {"encoding": "v2"},
        "ADAPT": {"encoding": "v1"},
        "NEUTRAL": {"encoding": "json"},
        "DECOY": {"encoding": "corrupt"},
    },
    "PACKAGE_RESOLUTION": {
        "LEGACY": {"resolution": "latest"},
        "ADAPT": {"resolution": "pinned"},
        "NEUTRAL": {"resolution": "vendored"},
        "DECOY": {"resolution": "missing"},
    },
    "SCHEMA_EVOLUTION": {
        "LEGACY": {"shape": "v2_minimal"},
        "ADAPT": {"shape": "v1_compatible"},
        "NEUTRAL": {"shape": "identity"},
        "DECOY": {"shape": "invalid"},
    },
    "TOOL_AFFORDANCE_CHANGE": {
        "LEGACY": {"mode": "json_flag"},
        "ADAPT": {"mode": "text_parse"},
        "NEUTRAL": {"mode": "status"},
        "DECOY": {"mode": "unsupported"},
    },
    "COST_RESOURCE_REGIME": {
        "LEGACY": {"algorithm": "exhaustive"},
        "ADAPT": {"algorithm": "heuristic"},
        "NEUTRAL": {"algorithm": "constant"},
        "DECOY": {"algorithm": "wasteful"},
    },
}


def route_patch(family: str, route: str) -> dict:
    try:
        return dict(_TABLE[family][route])
    except KeyError as exc:
        raise ValueError("ROUTE_PATCH_DOMAIN") from exc


def informative_probe(family: str) -> str:
    if family not in ALL_FAMILIES:
        raise ValueError("PROBE_FAMILY")
    return "PROBE_REGIME"


def probe_output(state: dict, probe_semantic: str) -> dict:
    if probe_semantic == "PROBE_METADATA":
        return {"family": state["family"], "token": state["token"]}
    if probe_semantic == "PROBE_COST":
        return {"budget": state.get("budget", 6)}
    if probe_semantic == "PROBE_NONE":
        return {"status": "NO_INFORMATION"}
    if probe_semantic != "PROBE_REGIME":
        raise ValueError("PROBE_SEMANTIC")
    key_map = {
        "PYTHON_API_SIGNATURE": ("api_version",),
        "SQLITE_SCHEMA": ("columns",),
        "DATA_SCHEMA_TRANSFORM": ("root_type",),
        "RUNTIME_CONFIGURATION": ("precedence",),
        "DEPENDENCY_API_VERSION": ("dependency_version",),
        "HTTP_PROTOCOL": ("protocol",),
        "TRANSACTION_CONCURRENCY": ("contention",),
        "SERIALIZATION_MIGRATION": ("consumer_version",),
        "PACKAGE_RESOLUTION": ("lock_epoch",),
        "SCHEMA_EVOLUTION": ("schema_version",),
        "TOOL_AFFORDANCE_CHANGE": ("tool_version",),
        "COST_RESOURCE_REGIME": ("budget",),
    }
    return {key: state[key] for key in key_map[state["family"]]}


def objective_route(state: dict) -> str:
    if state["task"] == "stable":
        return "NEUTRAL"
    return "LEGACY" if state["regime"] == "new" else "ADAPT"


def resource_cost(family: str, solution: dict) -> int:
    value = next(iter(solution.values()), "")
    return {
        "exhaustive": 18,
        "wasteful": 99,
        "heuristic": 4,
        "constant": 1,
        "optimistic": 8,
        "pessimistic": 4,
    }.get(value, 2)


def resource_budget(state: dict) -> int:
    return int(state.get("budget", 10))


def test_solution_a(state: dict, solution: dict) -> list[dict]:
    expected = route_patch(state["family"], objective_route(state))
    tests = [
        {"id": f"A:{state['family']}:{key}", "pass": solution.get(key) == value}
        for key, value in expected.items()
    ]
    tests.append(
        {"id": f"A:{state['family']}:schema", "pass": set(solution) == set(expected)}
    )
    tests.append(
        {
            "id": f"A:{state['family']}:resource",
            "pass": resource_cost(state["family"], solution) <= resource_budget(state),
        }
    )
    return tests


def test_solution_b(state: dict, solution: dict) -> list[dict]:
    family = state["family"]
    stable = state["task"] == "stable"
    new = state["regime"] == "new"
    expected_value, expected_key = {
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
    return [
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
