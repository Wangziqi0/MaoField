from __future__ import annotations
import json
from .canonical import canonical_json_bytes
from .family_rules import objective_route, probe_output
from .state_machine import _structure_truth


def _provider(content: dict) -> bytes:
    return canonical_json_bytes(
        {
            "id": "MOCK-NO-PROVIDER",
            "model": "glm-5.3-flash",
            "choices": [
                {
                    "finish_reason": "stop",
                    "message": {
                        "role": "assistant",
                        "content": json.dumps(
                            content,
                            sort_keys=True,
                            separators=(",", ":"),
                            ensure_ascii=False,
                        ),
                        "reasoning_content": "NO_PROVIDER_CONFORMANCE_FIXTURE",
                    },
                }
            ],
        }
    )


def oracle_adapter(request_body: bytes, metadata: dict) -> bytes:
    row = metadata["row"]
    context = metadata["context"]
    channel = context.channel
    turn = row["turn"]
    desc = context.desc
    action = {"protocol": "MAOFIELD_TOOL/1", "tool": "", "arguments": {}}
    if channel in ("BEHAVIOR", "ORDINARY_CONTROL"):
        if turn == 1:
            probe_id = next(
                alias
                for alias, semantic in desc["probe_alias_private"].items()
                if semantic == desc["truth"]["informative_probe"]
            )
            action.update(tool="run_probe", arguments={"probe_id": probe_id})
        elif turn == 2:
            action_id = next(
                alias
                for alias, route in desc["action_alias_private"].items()
                if route == desc["truth"]["objective_route"]
            )
            action.update(tool="apply_patch", arguments={"action_id": action_id})
        elif turn in (3, 5):
            action.update(tool="run_visible_tests", arguments={})
        elif turn == 4:
            action.update(tool="inspect_diff", arguments={})
        elif turn == 6:
            action_id = next(
                alias
                for alias, route in desc["action_alias_private"].items()
                if route == desc["truth"]["objective_route"]
            )
            action.update(tool="submit", arguments={"action_id": action_id})
    elif channel == "ACTION_SIBLING":
        action_id = next(
            alias
            for alias, route in desc["action_alias_private"].items()
            if route == desc["truth"]["objective_route"]
        )
        action.update(tool="apply_patch_and_submit", arguments={"action_id": action_id})
    elif channel == "STRUCTURE":
        action.update(tool="report_structure", arguments=_structure_truth(context.history_card))
    elif channel == "STRUCTURE_CRITERION":
        action.update(tool="report_criterion", arguments=desc["truth"])
    elif channel == "CANARY":
        action.update(tool="canary_echo", arguments={"nonce": desc["truth"]["canary_nonce"]})
    else:
        raise RuntimeError("MOCK_CHANNEL")
    return _provider(action)
