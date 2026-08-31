from __future__ import annotations
from .canonical import canonical_json_bytes, hmac_sha256


def _identifier(key: bytes, kind: str, world_id: str, index: int = 0) -> str:
    return kind[:1] + hmac_sha256(
        key, f"{kind}\0{world_id}\0{index}".encode("utf-8")
    ).hex().upper()[:15]


def build_cards(key: bytes, desc: dict, source_receipt: dict) -> dict[str, dict]:
    world_id = desc["world_id"]
    route_atoms = {
        route: _identifier(key, "ROUTE", world_id, index)
        for index, route in enumerate(("LEGACY", "ADAPT", "NEUTRAL", "DECOY"))
    }
    action_for_route = {
        route: alias for alias, route in desc["action_alias_private"].items()
    }
    practice = _identifier(key, "PRACTICE", world_id)
    evidence = _identifier(key, "EVIDENCE", world_id)
    scope = _identifier(key, "SCOPE", world_id)
    reopen = _identifier(key, "REOPEN", world_id)
    obj = _identifier(key, "OBJECT", world_id)
    source = _identifier(key, "SOURCE", world_id)
    decoy_obj = _identifier(key, "DECOY_OBJECT", world_id)
    decoy_source = _identifier(key, "DECOY_SOURCE", world_id)
    atoms = [
        *[
            {"id": atom, "type": "route", "candidate_action_id": action_for_route[route]}
            for route, atom in route_atoms.items()
        ],
        {"id": practice, "type": "practice", "value": "decisive executable test"},
        {"id": evidence, "type": "evidence", "value": "nonzero predecessor test failure"},
        {"id": scope, "type": "scope", "value": source_receipt["scope"]},
        {"id": reopen, "type": "reopening", "value": source_receipt["reopening_condition"]},
        {"id": obj, "type": "object", "value": desc["family"]},
        {"id": source, "type": "source", "value": "predecessor-practice receipt"},
    ]
    correct = [
        [route_atoms["LEGACY"], practice, "route_tested_by"],
        [practice, evidence, "practice_produced"],
        [evidence, scope, "evidence_scoped_by"],
        [scope, reopen, "scope_reopened_by"],
        [practice, source, "practice_grounded_in"],
        [route_atoms["LEGACY"], obj, "route_targets"],
    ]
    rewired = [
        [route_atoms["LEGACY"], evidence, "route_tested_by"],
        [practice, reopen, "practice_produced"],
        [evidence, route_atoms["ADAPT"], "evidence_scoped_by"],
        [scope, practice, "scope_reopened_by"],
        [practice, obj, "practice_grounded_in"],
        [route_atoms["LEGACY"], source, "route_targets"],
    ]
    conclusion = {
        "status": "REJECTED_UNDER_SCOPE",
        "route_atom": route_atoms["LEGACY"],
        "scope": source_receipt["scope"],
        "reopening_condition": source_receipt["reopening_condition"],
    }
    cards = {
        "DN": {
            "typed_atoms": atoms,
            "typed_edges": correct,
            "current_conclusion": conclusion,
            "grounding": {"object": obj, "source": source},
        },
        "UF": {
            "typed_atoms": atoms,
            "typed_edges": rewired,
            "current_conclusion": conclusion,
            "grounding": {"object": obj, "source": source},
        },
        "X": {
            "typed_atoms": atoms,
            "typed_edges": correct,
            "current_conclusion": conclusion,
            "grounding": {"object": decoy_obj, "source": decoy_source},
        },
        "CO": {
            "typed_atoms": [],
            "typed_edges": [],
            "current_conclusion": conclusion,
            "grounding": None,
        },
        "N0": {
            "typed_atoms": [],
            "typed_edges": [],
            "current_conclusion": {
                "status": "UNSET",
                "scope": source_receipt["scope"],
                "reopening_condition": source_receipt["reopening_condition"],
            },
            "grounding": None,
        },
    }
    for card in cards.values():
        card.update(
            {
                "schema": "maofield.glm53.history_card.v2",
                "route_action_map": {
                    atom: action_for_route[route]
                    for route, atom in route_atoms.items()
                },
                "padding": "",
            }
        )
    _balance(cards)
    return cards


def _balance(cards: dict[str, dict]) -> None:
    for _ in range(16):
        sizes = {arm: len(canonical_json_bytes(card)) for arm, card in cards.items()}
        target = max(sizes.values())
        if len(set(sizes.values())) == 1:
            return
        for arm, card in cards.items():
            card["padding"] += "." * (target - sizes[arm])
    if len({len(canonical_json_bytes(card)) for card in cards.values()}) != 1:
        raise RuntimeError("HISTORY_BYTE_BALANCE")
