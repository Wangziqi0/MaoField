# Reproduction layers

The supported packaged entry point is `./reproduce.sh` from the repository root; see the root README for platform prerequisites and environment assets. The complete route has been executed from freshly unpacked public Python/Lean assets. It checks exact algebra, mapped and full original records, successor export equivalence, source assembly, and five offline ordinary Lean compilations. New experimental model calls: zero. Independent-kernel checks: NOT_RUN.

For an existing Python 3.12 environment, `python REPRODUCIBILITY/reproduce.py --out WORK/analysis` runs deterministic mapped-record checks. Install `environment/requirements-analysis.txt`; `environment/requirements-complete.txt` pins the packaged analysis dependency closure. The older `REPRODUCIBILITY/requirements-lock.txt` additionally lists optional figure/document authoring packages, which are not required by the default reproduction and are not bundled. This analysis-only command does not compile Lean.

`experiment/replay_bwrap.py` is the tested offline Linux candidate replay path. Historical Docker-based `replay_lean.py` remains available as an alternative implementation, not the default and not claimed tested here. `assemble_lean.py` mechanically assembles original sources and candidates. `audit_hclose.py` checks all 859 unmodified payload identities; `audit_shareable.py` checks the explicitly mapped reviewer copy. `successor/audit_successor.py --raw-root ...` exports and independently recalculates from the full archive.

STANDARD request 1 was truncated without a candidate. The filenames `standard_1.lean` and `standard_2.lean` therefore correspond to original requests 2 and 3. Rejected candidates are expected outcomes and remain unchanged.
