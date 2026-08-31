from __future__ import annotations
from pathlib import Path
import json
import os
import urllib.request

BASE_URL = "https://api.z.ai/api/paas/v4"
CHAT_PATH = "/chat/completions"
MODEL = "glm-5.3-flash"


def load_api_key() -> str:
    inline = os.environ.get("ZAI_API_KEY")
    key_file = os.environ.get("ZAI_API_KEY_FILE")
    if bool(inline) == bool(key_file):
        raise RuntimeError("EXACTLY_ONE_SECRET_SOURCE_REQUIRED")
    value = inline if inline is not None else Path(key_file).read_text(encoding="utf-8").strip()
    if not value or any(character in value for character in "\r\n"):
        raise RuntimeError("SECRET_FORMAT_INVALID")
    return value


def dispatch(
    request_body: bytes,
    api_key: str,
    *,
    provider_authorized: bool = False,
    transport=None,
) -> bytes:
    if not provider_authorized:
        raise RuntimeError("PROVIDER_CALL_NOT_AUTHORIZED_BUILD_ONLY")
    if transport is not None:
        return transport(BASE_URL + CHAT_PATH, request_body, api_key)
    request = urllib.request.Request(
        BASE_URL + CHAT_PATH,
        data=request_body,
        method="POST",
        headers={
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json",
            "Accept-Language": "en-US,en",
        },
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        return response.read()
