from __future__ import annotations
from pathlib import Path
import json
from .family_rules import resource_cost
from .scorer_a import score as score_a
from .scorer_b import score as score_b
from .worlds import apply_action, execute_probe


class Environment:
    def __init__(self, root: Path, desc: dict) -> None:
        self.root = root
        self.desc = desc
        self.trajectory: list[dict] = []
        self.submitted_route: str | None = None
        self.failure_codes: list[str] = []

    def execute(self, sequence: int, action: dict) -> dict:
        tool = action["tool"]
        arguments = action["arguments"]
        event = {"sequence": sequence, "tool": tool, "ok": False, "cost": 0}
        try:
            if tool == "list_files":
                result = {"files": sorted(path.name for path in self.root.iterdir())}
            elif tool == "read_file":
                result = {
                    "path": arguments["path"],
                    "content": (self.root / arguments["path"]).read_text(encoding="utf-8"),
                }
            elif tool == "run_probe":
                result = execute_probe(self.desc, arguments["probe_id"])
                event.update(
                    probe_semantic_private=result.pop("semantic_private"),
                    observation_sha256=result["observation_sha256"],
                    cost=1,
                )
            elif tool in ("apply_patch", "apply_patch_and_submit"):
                result = apply_action(self.root, self.desc, arguments["action_id"])
                event.update(route_private=result.pop("route_private"))
                solution = json.loads((self.root / "solution.json").read_text(encoding="utf-8"))
                event["cost"] = resource_cost(self.desc["family"], solution)
                if tool == "apply_patch_and_submit":
                    self.submitted_route = event["route_private"]
            elif tool == "run_visible_tests":
                left = score_a(self.root, self.desc)
                right = score_b(self.root, self.desc)
                if [x["pass"] for x in left["tests"]] != [x["pass"] for x in right["tests"]]:
                    raise RuntimeError("VISIBLE_SCORER_DISAGREEMENT")
                result = {"visible_tests": left["tests"][:2]}
            elif tool == "inspect_diff":
                result = {
                    "solution": json.loads(
                        (self.root / "solution.json").read_text(encoding="utf-8")
                    )
                }
            elif tool == "submit":
                route = self.desc["action_alias_private"].get(arguments["action_id"])
                if route is None:
                    raise ValueError("ACTION_NOT_IN_CATALOGUE")
                self.submitted_route = route
                result = {"submitted": True}
            else:
                raise ValueError("TOOL_UNKNOWN")
            event["ok"] = True
            event["result"] = result
        except Exception as exc:
            code = str(exc).split(":", 1)[0]
            self.failure_codes.append(code)
            event["failure_code"] = code
            result = {"error": code}
        self.trajectory.append(event)
        return result
