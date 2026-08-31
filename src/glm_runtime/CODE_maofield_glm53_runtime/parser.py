from __future__ import annotations
import json
from .renderer import TOOL_ARGUMENTS


class ParseFailure(ValueError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def parse_provider_response(raw: bytes, allowed: tuple[str, ...]) -> dict:
    try:
        response = json.loads(raw)
    except Exception as exc:
        raise ParseFailure("INVALID_PROVIDER_JSON") from exc
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        raise ParseFailure("NO_CHOICE")
    message = choices[0].get("message", {})
    content = message.get("content")
    if not isinstance(content, str):
        raise ParseFailure("NON_STRING_CONTENT")
    if content.strip() != content or content.startswith("```"):
        raise ParseFailure("NON_JSON_CONTENT")
    try:
        action = json.loads(content)
    except Exception as exc:
        raise ParseFailure("NON_JSON_CONTENT") from exc
    if set(action) != {"protocol", "tool", "arguments"}:
        raise ParseFailure("SCHEMA_VIOLATION")
    if action.get("protocol") != "MAOFIELD_TOOL/1":
        raise ParseFailure("SCHEMA_VIOLATION")
    tool = action.get("tool")
    arguments = action.get("arguments")
    if tool not in allowed:
        raise ParseFailure("TOOL_NOT_ALLOWED_THIS_TURN")
    if not isinstance(arguments, dict) or set(arguments) != set(TOOL_ARGUMENTS[tool]):
        raise ParseFailure("ARGUMENT_SCHEMA_VIOLATION")
    return {
        "action": action,
        "assistant_content": content,
        "reasoning_content": message.get("reasoning_content"),
        "finish_reason": choices[0].get("finish_reason"),
    }
