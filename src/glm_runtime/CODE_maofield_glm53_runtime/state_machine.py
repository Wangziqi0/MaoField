from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import json
import os
import shutil
from typing import Callable

from .assignment import assignment_for
from .canonical import canonical_json_bytes, sha256_bytes
from .custody import append_wal, atomic_new, custody_blob
from .endpoints import (
    action_sibling_endpoint,
    build_behavior_endpoints,
    structure_endpoint,
)
from .family_rules import objective_route, probe_output
from .history import build_cards
from .parser import ParseFailure, parse_provider_response
from .renderer import allowed_tools, render_messages, request_body
from .scorer_a import score as scorer_a
from .scorer_b import score as scorer_b
from .schedule import load_schedule
from .tool_environment import Environment
from .worlds import (
    apply_action,
    descriptor,
    execute_probe,
    materialize_clean_successor,
    materialize_source_practice,
)

Adapter = Callable[[bytes, dict], bytes]


@dataclass
class EpisodeContext:
    channel: str
    stratum: str
    superblock: int
    opaque_slot: int
    assignment: dict | None
    desc: dict
    history_card: dict | None
    root: Path
    environment: Environment | None
    transcript: list[dict] = field(default_factory=list)
    endpoint_finalized: bool = False


def _episode_key(row: dict) -> tuple:
    return (
        row["channel"],
        row["stratum"],
        row["superblock"],
        row["opaque_slot"],
    )


def _structure_truth(history_card: dict) -> dict:
    edges = history_card.get("typed_edges", [])
    if not edges:
        return {
            "route": "NONE",
            "practice": "NONE",
            "evidence": "NONE",
            "scope": "NONE",
            "reopening": "NONE",
        }
    relation = {edge[2]: (edge[0], edge[1]) for edge in edges}
    route, practice = relation.get("route_tested_by", ("NONE", "NONE"))
    practice2, evidence = relation.get("practice_produced", ("NONE", "NONE"))
    evidence2, scope = relation.get("evidence_scoped_by", ("NONE", "NONE"))
    scope2, reopening = relation.get("scope_reopened_by", ("NONE", "NONE"))
    if practice != practice2 or evidence != evidence2 or scope != scope2:
        return {
            "route": "NONE",
            "practice": "NONE",
            "evidence": "NONE",
            "scope": "NONE",
            "reopening": "NONE",
        }
    return {
        "route": route,
        "practice": practice,
        "evidence": evidence,
        "scope": scope,
        "reopening": reopening,
    }


def _structure_criterion(superblock: int) -> tuple[dict, dict]:
    state = (superblock - 1) // 2
    truth = {
        "relation_complete": bool(state & 1),
        "grounding_correct": bool(state & 2),
        "currently_applicable": bool(state & 4),
    }
    renderer = "A" if superblock % 2 else "B"
    public = {
        "criterion_case": state + 1,
        "renderer": renderer,
        "facts": [
            "A route is connected to a practice and evidence" if truth["relation_complete"] else "The chain is incomplete",
            "The evidence belongs to the stated object" if truth["grounding_correct"] else "The evidence belongs to a decoy object",
            "The current material state remains in scope" if truth["currently_applicable"] else "The material state is outside the registered scope",
        ],
    }
    return public, truth


def _create_context(
    row: dict,
    run_root: Path,
    keys: dict[str, bytes],
    ledger: dict,
    source_cache: dict,
) -> EpisodeContext:
    channel = row["channel"]
    assignment = assignment_for(row, ledger)
    cell = assignment["cell"] if assignment else "C"
    namespace = channel
    if channel == "STRUCTURE_CRITERION":
        public, truth = _structure_criterion(row["superblock"])
        desc = {
            "schema": "maofield.glm53.structure_criterion_world.v2",
            "namespace": channel,
            "world_id": sha256_bytes(canonical_json_bytes(public)),
            "family": "STRUCTURE_CRITERION",
            "stratum": row["stratum"],
            "superblock": row["superblock"],
            "cell_private": None,
            "state": {},
            "public": public,
            "truth": truth,
            "action_alias_private": {},
            "probe_alias_private": {},
        }
        return EpisodeContext(
            channel, row["stratum"], row["superblock"], row["opaque_slot"], None,
            desc, None, run_root / "EPISODES" / f"CRITERION-{row['superblock']:03d}", None,
        )
    if channel == "CANARY":
        public = {"canary_nonce": f"CANARY-{row['superblock']:02d}"}
        desc = {
            "schema": "maofield.glm53.canary_world.v2",
            "namespace": channel,
            "world_id": sha256_bytes(canonical_json_bytes(public)),
            "family": "CANARY",
            "stratum": row["stratum"],
            "superblock": row["superblock"],
            "cell_private": None,
            "state": {},
            "public": public,
            "truth": public,
            "action_alias_private": {},
            "probe_alias_private": {},
        }
        return EpisodeContext(
            channel, row["stratum"], row["superblock"], row["opaque_slot"], None,
            desc, None, run_root / "EPISODES" / f"CANARY-{row['superblock']:03d}", None,
        )
    stratum = row["stratum"]
    desc = descriptor(
        keys["world_main"] if stratum != "SEALED32" else keys["world_sealed"],
        keys["renderer"],
        row["superblock"],
        stratum,
        cell,
        namespace=namespace,
    )
    source_key = (namespace, row["stratum"], row["superblock"])
    if source_key not in source_cache:
        source_root = run_root / "SOURCES" / f"{namespace}-{row['stratum']}-{row['superblock']:03d}"
        source_cache[source_key] = materialize_source_practice(source_root, desc)
    cards = build_cards(keys["renderer"], desc, source_cache[source_key])
    history_card = cards[assignment["arm"]] if assignment else None
    episode_root = run_root / "EPISODES" / (
        f"{channel}-{stratum}-{row['superblock']:03d}-{row['opaque_slot']:02d}"
    )
    materialize_clean_successor(episode_root, desc, history_card or {})
    environment = Environment(episode_root, desc)
    return EpisodeContext(
        channel,
        stratum,
        row["superblock"],
        row["opaque_slot"],
        assignment,
        desc,
        history_card,
        episode_root,
        environment,
    )


def run_schedule(
    schedule_path: Path,
    run_root: Path,
    keys: dict[str, bytes],
    ledger: dict,
    adapter: Adapter,
    *,
    model: str = "glm-5.3-flash",
    provider_authorized: bool = False,
) -> dict:
    """The sole production/rehearsal state machine.

    A future formal PI adoption must set provider_authorized=True outside this
    build-only package. This package's tests always use an in-process mock adapter.
    """
    rows = load_schedule(schedule_path)
    if run_root.exists():
        raise RuntimeError("RUN_ROOT_ALREADY_EXISTS")
    run_root.mkdir(parents=True)
    wal = run_root / "WAL.jsonl"
    main_endpoints_path = run_root / "PRIVATE_ENDPOINTS_MAIN96.jsonl"
    sealed_endpoints_path = run_root / "PRIVATE_ENDPOINTS_SEALED32.jsonl"
    auxiliary_endpoints_path = run_root / "PRIVATE_ENDPOINTS_AUXILIARY.jsonl"
    contexts: dict[tuple, EpisodeContext] = {}
    source_cache: dict = {}
    main_behavior_finalized: set[tuple] = set()
    sealed_started = False
    attempt_started = 0
    attempt_terminal = 0
    endpoint_rows = 0
    wal_previous = "0" * 64

    def write_endpoint(row: dict) -> None:
        nonlocal endpoint_rows
        if row.get("stratum") == "MAIN96":
            target = main_endpoints_path
        elif row.get("stratum") == "SEALED32":
            target = sealed_endpoints_path
        else:
            target = auxiliary_endpoints_path
        with open(target, "ab", buffering=0) as handle:
            handle.write(canonical_json_bytes(row))
            os.fsync(handle.fileno())
        endpoint_rows += 1

    for row in rows:
        # The state machine owns the single append-only WAL chain.
        if row["attempt"] > 18156:
            raise RuntimeError("ATTEMPT_CEILING_EXCEEDED")
        if row["channel"] == "BEHAVIOR" and row["stratum"] == "SEALED32" and not sealed_started:
            if len(main_behavior_finalized) != 96 * 20:
                raise RuntimeError("SEALED32_BEFORE_MAIN96_FREEZE")
            freeze = {
                "schema": "maofield.glm53.main96_freeze.v2",
                "complete_behavior_episodes": len(main_behavior_finalized),
                "endpoint_tree_sha256": sha256_bytes(main_endpoints_path.read_bytes()),
                "sealed_assignment_opened": False,
            }
            atomic_new(run_root / "MAIN96_FREEZE_RECEIPT.json", canonical_json_bytes(freeze))
            sealed_started = True
        key = _episode_key(row)
        if key not in contexts:
            contexts[key] = _create_context(row, run_root, keys, ledger, source_cache)
        context = contexts[key]
        wal_row = append_wal(wal, {"event": "ATTEMPT_STARTED", "attempt": row["attempt"], "episode": key}, wal_previous)
        wal_previous = wal_row["event_sha256"]
        attempt_started += 1
        fixed_observation = None
        if context.channel == "ACTION_SIBLING":
            semantic = context.desc["truth"]["informative_probe"]
            fixed_observation = probe_output(context.desc["state"], semantic)
        messages = render_messages(
            context.channel,
            row["turn"],
            context.desc["public"],
            context.history_card,
            context.transcript,
            fixed_objective_observation=fixed_observation,
        )
        body = request_body(model, messages)
        request_receipt = custody_blob(run_root, row["attempt"], "REQUEST", body)
        raw_response = adapter(body, {"row": row, "context": context, "provider_authorized": provider_authorized})
        response_receipt = custody_blob(run_root, row["attempt"], "RESPONSE", raw_response)
        failure_codes: list[str] = []
        parsed = None
        try:
            parsed = parse_provider_response(raw_response, allowed_tools(context.channel, row["turn"]))
        except ParseFailure as exc:
            failure_codes.append(exc.code)
        tool_result = {"error": failure_codes[0]} if failure_codes else {}
        if parsed is not None:
            action = parsed["action"]
            if context.channel in ("BEHAVIOR", "ORDINARY_CONTROL"):
                tool_result = context.environment.execute(row["turn"], action)
            elif context.channel == "ACTION_SIBLING":
                tool_result = context.environment.execute(row["turn"], action)
            elif context.channel == "STRUCTURE":
                tool_result = {"accepted": True, "report": action["arguments"]}
            elif context.channel == "STRUCTURE_CRITERION":
                tool_result = {"accepted": True, "report": action["arguments"]}
            elif context.channel == "CANARY":
                tool_result = {"accepted": action["arguments"]["nonce"] == context.desc["truth"]["canary_nonce"]}
            context.transcript.append(
                {"assistant_content": parsed["assistant_content"], "tool_result": tool_result}
            )
        wal_row = append_wal(
            wal,
            {
                "event": "ATTEMPT_TERMINAL",
                "attempt": row["attempt"],
                "episode": key,
                "request": request_receipt,
                "response": response_receipt,
                "failure_codes": failure_codes,
            },
            wal_previous,
        )
        wal_previous = wal_row["event_sha256"]
        attempt_terminal += 1

        final_turn = row["turn"] == (6 if context.channel in ("BEHAVIOR", "ORDINARY_CONTROL") else 1)
        if final_turn and not context.endpoint_finalized:
            base = {
                "schema": "maofield.glm53.private_endpoint_row.v2",
                "episode_id": "::".join(map(str, key)),
                "channel": context.channel,
                "stratum": context.stratum,
                "superblock": context.superblock,
                "opaque_slot": context.opaque_slot,
                "assignment": context.assignment,
                "world_id": context.desc["world_id"],
            }
            if context.channel in ("BEHAVIOR", "ORDINARY_CONTROL"):
                left = scorer_a(context.root, context.desc)
                right = scorer_b(context.root, context.desc)
                result = build_behavior_endpoints(
                    context.desc,
                    context.environment.trajectory,
                    context.environment.submitted_route,
                    left,
                    right,
                    context.environment.failure_codes + failure_codes,
                )
            elif context.channel == "ACTION_SIBLING":
                left = scorer_a(context.root, context.desc)
                right = scorer_b(context.root, context.desc)
                result = action_sibling_endpoint(
                    context.desc, context.environment.submitted_route, left, right
                )
            elif context.channel == "STRUCTURE":
                report = tool_result.get("report", {})
                result = structure_endpoint(report, _structure_truth(context.history_card))
            elif context.channel == "STRUCTURE_CRITERION":
                report = tool_result.get("report", {})
                result = {
                    "status": "EVALUABLE",
                    "STRUCTURE_CRITERION": int(report == context.desc["truth"]),
                    "renderer": context.desc["public"]["renderer"],
                    "criterion_case": context.desc["public"]["criterion_case"],
                    "failure_codes": failure_codes,
                }
            else:
                result = {
                    "status": "EVALUABLE",
                    "CANARY": int(bool(tool_result.get("accepted"))),
                    "failure_codes": failure_codes,
                }
            write_endpoint({**base, **result})
            context.endpoint_finalized = True
            if context.channel == "BEHAVIOR" and context.stratum == "MAIN96":
                main_behavior_finalized.add(key)
    return {
        "schema": "maofield.glm53.state_machine_completion.v2",
        "attempt_started": attempt_started,
        "attempt_terminal": attempt_terminal,
        "endpoint_rows": endpoint_rows,
        "main96_freeze_present": (run_root / "MAIN96_FREEZE_RECEIPT.json").exists(),
        "provider_authorized": provider_authorized,
        "endpoint_files": {"main96": str(main_endpoints_path.name), "sealed32": str(sealed_endpoints_path.name), "auxiliary": str(auxiliary_endpoints_path.name)},
        "automatic_next_round": False,
    }
