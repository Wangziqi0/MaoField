from __future__ import annotations
from dataclasses import dataclass
import json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from .canonical import (
    canonical_json_bytes,
    fisher_yates,
    hkdf_expand,
    hkdf_extract,
    hmac_sha256,
    sha256_bytes,
)

ARMS = ("DN", "UF", "X", "CO", "N0")
CELLS = ("S", "C", "R0", "R1")
LABELS = tuple((arm, cell) for arm in ARMS for cell in CELLS)
SALT = b"MAOFIELD/GLM53/V2/HKDF-SALT"
CONTEXTS = {
    "assignment_main": b"MAOFIELD/GLM53/V2/ASSIGNMENT/MAIN96",
    "assignment_sealed": b"MAOFIELD/GLM53/V2/ASSIGNMENT/SEALED32",
    "assignment_sibling": b"MAOFIELD/GLM53/V2/ASSIGNMENT/A_SIB_R_SHARED",
    "world_main": b"MAOFIELD/GLM53/V2/WORLD/MAIN96",
    "world_sealed": b"MAOFIELD/GLM53/V2/WORLD/SEALED32",
    "renderer": b"MAOFIELD/GLM53/V2/RENDERER",
    "evidence": b"MAOFIELD/GLM53/V2/EVIDENCE",
}


def derive_keys(
    root_secret: bytes,
    candidate_zip_sha256: str,
    formal_pi_adoption_sha256: str,
    pi_nonce_hex: str,
) -> dict[str, bytes]:
    if len(root_secret) != 32:
        raise ValueError("ROOT_SECRET_LENGTH")
    if len(pi_nonce_hex) != 64:
        raise ValueError("PI_NONCE_LENGTH")
    try:
        nonce = bytes.fromhex(pi_nonce_hex)
    except ValueError as exc:
        raise ValueError("PI_NONCE_HEX") from exc
    ikm = (
        root_secret
        + candidate_zip_sha256.upper().encode("ascii")
        + formal_pi_adoption_sha256.upper().encode("ascii")
        + nonce
    )
    prk = hkdf_extract(SALT, ikm)
    return {name: hkdf_expand(prk, context, 32) for name, context in CONTEXTS.items()}


def _mapping(key: bytes, domain: str, superblock: int) -> dict[str, dict[str, str]]:
    labels = fisher_yates(
        LABELS, key, f"{domain}\0{superblock}".encode("ascii")
    )
    return {
        str(slot): {"arm": arm, "cell": cell}
        for slot, (arm, cell) in enumerate(labels, start=1)
    }


def build_private_ledger(keys: dict[str, bytes]) -> dict:
    ledger = {
        "schema": "maofield.glm53.private_assignment_ledger.v2",
        "behavior_main": {},
        "behavior_sealed": {},
        "siblings": {},
    }
    for superblock in range(1, 97):
        ledger["behavior_main"][str(superblock)] = _mapping(
            keys["assignment_main"], "BEHAVIOR_MAIN96", superblock
        )
    for superblock in range(97, 129):
        ledger["behavior_sealed"][str(superblock)] = _mapping(
            keys["assignment_sealed"], "BEHAVIOR_SEALED32", superblock
        )
    for superblock in range(1, 65):
        ledger["siblings"][str(superblock)] = _mapping(
            keys["assignment_sibling"], "A_SIB_R_SHARED", superblock
        )
    validate_ledger(ledger)
    return ledger


def validate_ledger(ledger: dict) -> None:
    expected = set(LABELS)
    for domain in ("behavior_main", "behavior_sealed", "siblings"):
        for superblock, mapping in ledger.get(domain, {}).items():
            observed = {(row["arm"], row["cell"]) for row in mapping.values()}
            if observed != expected or len(mapping) != 20:
                raise ValueError(f"ASSIGNMENT_CARTESIAN:{domain}:{superblock}")
    if len(ledger["behavior_main"]) != 96:
        raise ValueError("MAIN96_COUNT")
    if len(ledger["behavior_sealed"]) != 32:
        raise ValueError("SEALED32_COUNT")
    if len(ledger["siblings"]) != 64:
        raise ValueError("SIBLING_COUNT")


def assignment_for(schedule_row: dict, ledger: dict) -> dict | None:
    channel = schedule_row["channel"]
    superblock = schedule_row["superblock"]
    slot = str(schedule_row["opaque_slot"])
    if channel == "BEHAVIOR":
        domain = "behavior_main" if superblock <= 96 else "behavior_sealed"
    elif channel in ("STRUCTURE", "ACTION_SIBLING"):
        domain = "siblings"
    else:
        return None
    assigned = ledger[domain][str(superblock)][slot]
    return {
        **assigned,
        "assignment_domain": domain,
        "pairing_id": (
            f"SIB-{superblock:03d}-{int(slot):02d}" if domain == "siblings" else None
        ),
    }


def encrypt_ledger(ledger: dict, key: bytes, public_binding: dict) -> dict:
    plaintext = canonical_json_bytes(ledger)
    aad = canonical_json_bytes(public_binding)
    nonce = hmac_sha256(
        key, b"LEDGER-NONCE\0" + bytes.fromhex(sha256_bytes(plaintext))
    )[:12]
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, aad)
    return {
        "algorithm": "AES-256-GCM",
        "nonce_hex": nonce.hex().upper(),
        "aad_sha256": sha256_bytes(aad),
        "plaintext_sha256": sha256_bytes(plaintext),
        "ciphertext_hex": ciphertext.hex().upper(),
        "ciphertext_sha256": sha256_bytes(ciphertext),
    }


def decrypt_ledger(envelope: dict, key: bytes, public_binding: dict) -> dict:
    aad = canonical_json_bytes(public_binding)
    if sha256_bytes(aad) != envelope["aad_sha256"]:
        raise ValueError("ASSIGNMENT_AAD")
    plaintext = AESGCM(key).decrypt(
        bytes.fromhex(envelope["nonce_hex"]),
        bytes.fromhex(envelope["ciphertext_hex"]),
        aad,
    )
    if sha256_bytes(plaintext) != envelope["plaintext_sha256"]:
        raise ValueError("ASSIGNMENT_PLAINTEXT")
    ledger = json.loads(plaintext)
    validate_ledger(ledger)
    return ledger
