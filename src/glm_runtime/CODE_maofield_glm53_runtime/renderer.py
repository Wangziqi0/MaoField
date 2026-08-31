from __future__ import annotations
from .canonical import canonical_json_bytes

MAX_CANONICAL_MESSAGE_BYTES = 32768
MAX_OUTPUT_TOKENS = 256
SYSTEM_MESSAGE = (
    "You are operating an executable scientific-software world. "
    "Return exactly one JSON object and no prose. Use protocol MAOFIELD_TOOL/1. "
    "Select only listed probes/actions and obey the turn-specific tool grammar."
)
TOOL_ARGUMENTS = {
    "list_files": (),
    "read_file": ("path",),
    "run_probe": ("probe_id",),
    "apply_patch": ("action_id",),
    "run_visible_tests": (),
    "inspect_diff": (),
    "submit": ("action_id",),
    "apply_patch_and_submit": ("action_id",),
    "report_structure": ("route", "practice", "evidence", "scope", "reopening"),
    "report_criterion": ("relation_complete", "grounding_correct", "currently_applicable"),
    "canary_echo": ("nonce",),
}
BEHAVIOR_ALLOWED = {
    1: ("run_probe",),
    2: ("apply_patch",),
    3: ("run_visible_tests",),
    4: ("apply_patch", "inspect_diff"),
    5: ("run_visible_tests",),
    6: ("submit",),
}


def allowed_tools(channel: str, turn: int) -> tuple[str, ...]:
    if channel in ("BEHAVIOR", "ORDINARY_CONTROL"):
        return BEHAVIOR_ALLOWED[turn]
    if channel == "ACTION_SIBLING":
        return ("apply_patch_and_submit",)
    if channel == "STRUCTURE":
        return ("report_structure",)
    if channel == "STRUCTURE_CRITERION":
        return ("report_criterion",)
    if channel == "CANARY":
        return ("canary_echo",)
    raise ValueError("CHANNEL")


def _reject_private_keys(value):
    if isinstance(value, dict):
        forbidden={"arm","cell","objective_route","informative_probe","hidden_truth","private_assignment"}
        overlap=forbidden.intersection(value)
        if overlap:
            raise RuntimeError("MODEL_FACING_PRIVATE_FIELD_LEAK")
        for child in value.values(): _reject_private_keys(child)
    elif isinstance(value, list):
        for child in value: _reject_private_keys(child)


def render_messages(
    channel: str,
    turn: int,
    world_public: dict,
    history_card: dict | None,
    transcript: list[dict],
    fixed_objective_observation: dict | None = None,
) -> list[dict]:
    tools = allowed_tools(channel, turn)
    payload = {
        "protocol": "MAOFIELD-GLM53/2",
        "channel": channel,
        "turn": turn,
        "world": world_public,
        "history": history_card,
        "fixed_objective_observation": fixed_objective_observation,
        "allowed_tools": [
            {
                "tool": tool,
                "required_arguments": list(TOOL_ARGUMENTS[tool]),
                "additional_arguments": False,
            }
            for tool in tools
        ],
        "response": {
            "protocol": "MAOFIELD_TOOL/1",
            "exact_top_level_keys": ["protocol", "tool", "arguments"],
        },
    }
    _reject_private_keys(world_public)
    _reject_private_keys(history_card)
    _reject_private_keys(fixed_objective_observation)
    messages = [
        {"role": "system", "content": SYSTEM_MESSAGE},
        {
            "role": "user",
            "content": "MAOFIELD-GLM53/2\n"
            + canonical_json_bytes(payload).decode("utf-8"),
        },
    ]
    for event in transcript:
        messages.append(
            {"role": "assistant", "content": event["assistant_content"]}
        )
        messages.append(
            {
                "role": "user",
                "content": "TOOL_RESULT\n"
                + canonical_json_bytes(event["tool_result"]).decode("utf-8"),
            }
        )
    rendered = canonical_json_bytes(messages)
    if len(rendered) > MAX_CANONICAL_MESSAGE_BYTES:
        raise RuntimeError("RENDERED_INPUT_BYTE_BOUNDARY")
    forbidden = (b'"arm"', b'"cell"', b'"objective_route"', b'"informative_probe"')
    if any(token in rendered for token in forbidden):
        raise RuntimeError("MODEL_FACING_PRIVATE_FIELD_LEAK")
    return messages


def request_body(model: str, messages: list[dict]) -> bytes:
    return canonical_json_bytes(
        {
            "model": model,
            "messages": messages,
            "temperature": 1.0,
            "top_p": 0.95,
            "reasoning_effort": "max",
            "thinking": {"type": "enabled", "clear_thinking": False},
            "stream": False,
            "max_tokens": MAX_OUTPUT_TOKENS,
        }
    )
