# Exact saved-candidate Lean assembly and replay

## What is being replayed

Five saved files contain the same enclosing theorem and different visible `hclose` bodies. The study has six model requests, not six compilable candidates. `standard_1.lean` is **visible candidate 1, original STANDARD request 2**; `standard_2.lean` is **visible candidate 2, original STANDARD request 3**. STANDARD request 1 ended at the output limit with no visible body and was never compiled. The mapping is recomputed by matching each submission's `body.lean.txt` SHA-256 to the original request's `visible.utf8`; it is not inferred from ordinal filenames.

## Source identity and exact file layout

The preserved mathematical source originates from OpenAI `NavierStokesAndEuler`, commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`. The actual study project is the documented **modified research slice**, not an unmodified full repository. `SOURCE_NOTICE.md` and the Apache-2.0 `LICENSE` describe attribution and adaptations. Do not replace these files with the full completed original solution.

From `10_CURRENT_RUN/history/` the assembler merges:

- `workspace/`: preserved local Lean modules, `lakefile.toml`, `lake-manifest.json`, `lean-toolchain`, licence and source notice. The final `workspace/Branch/Direct.lean` is intentionally omitted from the common input because each saved candidate is inserted separately.
- `public/`: the original public modules, including `Checkpoint/NodeGoal.lean`, `GoalSpec.lean`, the two problem statements and periodic statement/support. Colliding paths must be byte-identical or assembly fails.
- `submissions/…/candidate.lean`: exact five candidate files copied to `saved_candidates/`; candidate text is never repaired.

The required resulting layout is:

```text
WORK/lean_project/
  lean-toolchain                 # leanprover/lean4:v4.34.0-rc2
  lakefile.toml
  lake-manifest.json
  LICENSE
  SOURCE_NOTICE.md
  Checkpoint/NodeGoal.lean       # actual supplied goal, not a new placeholder
  NavierStokes/…                 # original modified source slice
  GoalSpec.lean
  saved_candidates/history_1.lean
  saved_candidates/history_2.lean
  saved_candidates/history_3.lean
  saved_candidates/standard_1.lean  # original request 2
  saved_candidates/standard_2.lean  # original request 3
  candidate_manifest.json
  request_to_candidate.json
  ASSEMBLY_RECEIPT.json
```

`Checkpoint/NodeGoal.lean` SHA-256 must be `571a45c575a39523475c96b3789d331ba2c07a0c80e8fb477790a5d6e1b299d7`. Its first target represents the exact signature of `compact_chart_pair_bounds`; its second target is separately recorded. The former source signature came from `NavierStokes/PrimaryCovarianceBounds.lean`, SHA-256 `7417f840e9689a41504a1cc368acc04d565d2c5bac2cca3959675a9a86b97862`. These are preserved provenance identities, not a new check of the full NS theorem.

## 1. Offline assembly (executed in this revision)

From the package root:

```bash
python REPRODUCIBILITY/experiment/assemble_lean.py --out WORK/lean_project
python REPRODUCIBILITY/experiment/replay_lean.py \
  --probe --prepared-project WORK/lean_project --out WORK/lean_probe
```

The internal master defaults to `INTERNAL/RAW_HCLOSE`. The review-support archive defaults to its `REPRODUCIBILITY/experiment/raw` sharing tree. An explicit `--raw PATH` is also supported by the assembler. Output must be a fresh directory. All source hashes, public/workspace collision checks, local import paths, original request mappings and fixed package commits are recorded. `SOURCE_ASSEMBLED_NOT_COMPILED` is not Lean acceptance.

## 2. Obtain the historical toolchain in an isolated preparation environment

Preserved source identity:

- Lean release: `4.34.0-rc2`.
- Toolchain archive: `https://github.com/leanprover/lean4/releases/download/v4.34.0-rc2/lean-4.34.0-rc2-linux.tar.zst`.
- Expected archive SHA-256: `3d011041203acacf300d343a39673f7d233743397993797c941346ae9e5df1a8`.
- Recorded Lean source commit: `6a10ac8c22beadecabdbb0919c2b50214762f91d`.

These are historical dependency identifiers from the input archive; current retrievability was not established by this revision. In a separately reviewed preparation container, download only after explicitly approving network access, check the checksum before extracting, and verify `lean --version`. A different available version is not an identical replay. No automatic installer or historical machine endpoint is invoked by the default commands.

## 3. Prepare exact dependencies

The preserved `lake-manifest.json` is authoritative. Important pins include:

- Mathlib: `85e3a25e006c35636f0e53b0e9296caca2685bc0`.
- Comparator: `19e111e2141cf333c7daff0f64c5f24acc91dd2e`.
- Nine transitive packages, with repositories and commits in that same manifest.

All package source checkouts must match their exact recorded commits. Do not run `lake update` against an unpinned branch. In the isolated preparation environment, with the verified toolchain on PATH:

```bash
python REPRODUCIBILITY/experiment/prepare_dependencies.py \
  --project WORK/lean_project --allow-network --fetch
cd WORK/lean_project
lake exe cache get
```

The fetch command creates `.lake/packages/<name>` at the fixed commit and verifies `git rev-parse HEAD` for every lock entry. `lake exe cache get` is an explicitly online preparation step, not an experiment; retain its stdout/stderr. Mathlib cache retrieval is not guaranteed to provide every auxiliary package build. Where an exact package lacks `.lake/build`, build that package in the preparation environment, retaining output; the replay preflight stops rather than silently downloading or substituting a package. Preserve the original project lock and verify it remains byte-identical.

Create or select a local container image with this exact toolchain and a reviewed shell/git environment. Resolve its actual `sha256:…` image ID and record it; this package does not invent an available image. The historical image ID is provenance, not a downloadable public image.

## 4. Replay the five original candidates (NOT_RUN here)

```bash
python REPRODUCIBILITY/experiment/replay_lean.py \
  --execute --prepared-project WORK/lean_project \
  --package-cache WORK/lean_project/.lake/packages \
  --image sha256:REPLACE_WITH_ACTUAL_64_HEX_LOCAL_IMAGE_ID \
  --out WORK/saved_candidate_replay
```

Run `--execute` under a non-root account that owns the prepared project and output directory. A root caller is rejected rather than silently producing a root container. Ordinary candidate rejections are recorded as valid replay outcomes; infrastructure/unclassified failures return a nonzero process code. The placeholder image ID is an explicit required local input, not a claim that an image exists. The runner refuses tags and requires a pinned ID. For each candidate it creates a new project, copies the candidate unchanged to `Branch/Direct.lean`, and executes the historical command `lake build +Branch.Direct` in a network-disabled, non-root, read-only-root container. Only that candidate worktree and the dependency-ready, read-only cache are mounted. Never mount the complete internal evidence archive or host credentials. The same saved source is used for all five attempts; no failure is repaired.

Logs distinguish ordinary acceptance, a candidate rejection with a corresponding `Branch/Direct.lean` error, missing infrastructure, timeout and a nonzero result requiring review. Historical expected patterns (four candidate rejections and the third HISTORY acceptance) are comparison targets, not computed outcomes. The mapping retains raw original status strings separately where they differ from the observed compiler classification.

## 5. Independent kernel is a separate layer

An ordinary `lake build` is not independent certification. The original kernel/tool identifiers and full target obligations must be verified separately before an independent comparison is claimed. This package neither calls `nanoda` nor turns saved `#print axioms` output into a new independent acceptance. Current status: **NOT_RUN**.
