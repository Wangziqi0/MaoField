from __future__ import annotations
import hashlib
import hmac
import json


def canonical_json_bytes(value: object) -> bytes:
    """UTF-8 sorted compact JSON with a single trailing LF."""
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_object(value: object) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def hmac_sha256(key: bytes, data: bytes) -> bytes:
    return hmac.new(key, data, hashlib.sha256).digest()


def hkdf_extract(salt: bytes, ikm: bytes) -> bytes:
    return hmac_sha256(salt, ikm)


def hkdf_expand(prk: bytes, info: bytes, length: int) -> bytes:
    if length < 0 or length > 255 * 32:
        raise ValueError("HKDF_LENGTH")
    output = b""
    block = b""
    counter = 1
    while len(output) < length:
        block = hmac_sha256(prk, block + info + bytes((counter,)))
        output += block
        counter += 1
    return output[:length]


class HmacStream:
    """Deterministic byte stream used only after a domain-separated key exists."""

    def __init__(self, key: bytes, context: bytes) -> None:
        self.key = key
        self.context = context
        self.counter = 0
        self.buffer = b""

    def read(self, length: int) -> bytes:
        if length < 0:
            raise ValueError("STREAM_LENGTH")
        while len(self.buffer) < length:
            self.counter += 1
            self.buffer += hmac_sha256(
                self.key, self.context + self.counter.to_bytes(8, "big")
            )
        result, self.buffer = self.buffer[:length], self.buffer[length:]
        return result

    def randbelow(self, upper: int) -> int:
        if upper <= 0:
            raise ValueError("RANDBELOW_UPPER")
        size = max(1, (upper.bit_length() + 7) // 8)
        span = 1 << (size * 8)
        cutoff = span - (span % upper)
        while True:
            value = int.from_bytes(self.read(size), "big")
            if value < cutoff:
                return value % upper


def fisher_yates(items: tuple | list, key: bytes, context: bytes) -> list:
    result = list(items)
    stream = HmacStream(key, context)
    for index in range(len(result) - 1, 0, -1):
        swap = stream.randbelow(index + 1)
        result[index], result[swap] = result[swap], result[index]
    return result
