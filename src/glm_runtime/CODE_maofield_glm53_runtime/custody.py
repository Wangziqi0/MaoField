from __future__ import annotations
from pathlib import Path
import ctypes
import json
import os
import sys
from ctypes import wintypes
from .canonical import canonical_json_bytes, sha256_bytes


def atomic_new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def append_wal(path: Path, event: dict, previous: str | None = None) -> dict:
    if previous is None:
        previous = "0" * 64
        if path.exists():
            lines = path.read_text(encoding="utf-8").splitlines()
            if lines:
                previous = json.loads(lines[-1])["event_sha256"]
    row = {**event, "prev_event_sha256": previous}
    row["event_sha256"] = sha256_bytes(canonical_json_bytes(row))
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "ab", buffering=0) as handle:
        handle.write(canonical_json_bytes(row))
        os.fsync(handle.fileno())
    return row


def custody_blob(root: Path, attempt: int, kind: str, data: bytes) -> dict:
    path = root / "RAW_CUSTODY" / f"{attempt:05d}_{kind}.bin"
    atomic_new(path, data)
    return {
        "path": str(path.relative_to(root)).replace("\\", "/"),
        "bytes": len(data),
        "sha256": sha256_bytes(data),
    }


class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]


def _blob(data: bytes):
    buffer = ctypes.create_string_buffer(data)
    return DATA_BLOB(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_byte))), buffer


def dpapi_protect(data: bytes, description: str) -> bytes:
    if sys.platform != "win32":
        raise RuntimeError("DPAPI_WINDOWS_FORMAL_ONLY")
    source, source_buffer = _blob(data)
    target = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptProtectData(
        ctypes.byref(source), description, None, None, None, 0, ctypes.byref(target)
    ):
        raise ctypes.WinError()
    try:
        return ctypes.string_at(target.pbData, target.cbData)
    finally:
        ctypes.windll.kernel32.LocalFree(target.pbData)


def dpapi_unprotect(data: bytes) -> bytes:
    if sys.platform != "win32":
        raise RuntimeError("DPAPI_WINDOWS_FORMAL_ONLY")
    source, source_buffer = _blob(data)
    target = DATA_BLOB()
    description = wintypes.LPWSTR()
    if not ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(source), ctypes.byref(description), None, None, None, 0, ctypes.byref(target)
    ):
        raise ctypes.WinError()
    try:
        return ctypes.string_at(target.pbData, target.cbData)
    finally:
        ctypes.windll.kernel32.LocalFree(target.pbData)
