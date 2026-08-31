from __future__ import annotations
from pathlib import Path
import hashlib
import json
import os
import zipfile
from .canonical import canonical_json_bytes, sha256_bytes

FIXED_ZIP_TIME = (2026, 8, 28, 0, 0, 0)


def build_formal_return(
    output_zip: Path,
    run_root: Path,
    analysis_root: Path,
    binding: dict,
) -> dict:
    if output_zip.exists():
        raise RuntimeError("FORMAL_RETURN_EXISTS")
    files: list[tuple[str, bytes]] = []
    for base_name, base in (("RUN", run_root), ("ANALYSIS", analysis_root)):
        for path in sorted(base.rglob("*")):
            if path.is_file():
                relative = str(path.relative_to(base)).replace("\\", "/")
                files.append((f"{base_name}/{relative}", path.read_bytes()))
    files.append(("BINDING.json", canonical_json_bytes(binding)))
    manifest_rows = [
        {"path": name, "bytes": len(data), "sha256": sha256_bytes(data)}
        for name, data in files
    ]
    manifest = {
        "schema": "maofield.glm53.formal_return_manifest.v2",
        "payloads": manifest_rows,
        "automatic_next_round": False,
    }
    files.append(("PACKAGE_MANIFEST.json", canonical_json_bytes(manifest)))
    sha_lines = "".join(f"{row['sha256']}  {row['path']}\n" for row in manifest_rows).encode("utf-8")
    files.append(("SHA256SUMS.txt", sha_lines))
    with zipfile.ZipFile(output_zip, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files):
            info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(output_zip) as archive:
        if archive.testzip() is not None:
            raise RuntimeError("FORMAL_RETURN_CRC")
    return {
        "schema": "maofield.glm53.formal_return_receipt.v2",
        "bytes": output_zip.stat().st_size,
        "sha256": sha256_bytes(output_zip.read_bytes()),
        "members": len(files),
        "automatic_next_round": False,
    }
