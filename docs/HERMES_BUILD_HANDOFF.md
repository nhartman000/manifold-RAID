# Manifold RAID: technical explanation and fast build handoff

**Prepared:** 2026-10-21  
**Repository:** `nhartman000/manifold-RAID` (`main`)  
**Purpose:** single, model-readable handoff for Hermes, Claude, or a human engineer implementing the current Manifold RAID design.

## 1. What Manifold RAID is

Manifold RAID means **Redundant Array of Invariant Data**. It is an experimental architecture for **Invariant State Representation (ISR)** and **dynamic admissible-trajectory generation**.

The core idea is to preserve a compact, verified description of the state and the rules that constrain valid future transformations. When a result is needed, the system generates an admissible trajectory from that description and checks the result against declared closure/equivalence conditions. The full past execution path is evidence of one run; it is not automatically the data structure that must be stored to generate a future valid run.

In plain terms: preserve the state and the rules that shape valid behavior; construct the needed execution or artifact when asked; verify it; retain only what the profile explicitly requires.

The phrase “RAID” is an architectural analogy to redundancy/striping and reconstruction. It does not, by itself, mean that the current Python reference implementation already has distributed storage, hardware redundancy, fault tolerance, or production-grade storage striping. Those are separate implementation/research claims and require separate tests.

## 2. The current canonical model

Represent the current system state as:

```text
SR_t = (s_t, D_t, C_t)
```

where `s_t` is the state vector or state payload, `D_t` is domain/context information, and `C_t` is the active constraint set. `T_G` identifies the applicable transform vocabulary, family, or bounded transform generator.

For every candidate transform `T`, compute `SR_out = T(SR_t)`, then evaluate the declared admissibility mask. The admissible set is:

```text
A_t = { T in T_G | M_C(SR_t, T, T(SR_t)) = 1 }
```

Only members of `A_t` may be executed. If the set is empty, generation fails closed. If several candidates remain, preserve the branch set, rank it with a declared policy, or apply a declared deterministic tie-break. Do not silently treat ambiguity as certainty.

The runtime path is:

```text
invariant record
  -> reconstruct entry state SR_0
  -> generate candidates from T_G
  -> apply constraints/admissibility mask
  -> preserve or select an admissible branch
  -> apply transform and update state
  -> repeat until exit/closure
  -> verify declared behavioral equivalence and closure
```

The generated trajectory can be represented as:

```text
tau_hat = (SR_0, T_0, SR_1, T_1, ..., T_(n-1), SR_n)
```

It is a derived runtime artifact. It may be held in memory, emitted as evidence, returned to a caller, serialized to a string, or materialized as a file on request. It is not required to become the reconstruction record for the next run.

## 3. Persistent reconstruction record versus runtime trace

These objects must stay distinct in code, schemas, names, and documentation.

| Object | Suggested type/name | Role | Persist by default? |
|---|---|---|---|
| Invariant reconstruction record | `InvariantReconstructionRecord` / current `seed_block` | Entry/invariant state, transform-space identity, admissibility rules, generation policy, closure and verification contract, provenance/version identities | Yes, when accepted and stored |
| Generated trajectory | `GeneratedTrajectory` / `tau_hat` | States and transitions created during one runtime generation | No; run-local |
| Generated evidence | `TransitionEvidence` / CIIU-like or QSON-compatible records | Auditable account of what the generator did in a particular run | Optional; output evidence, not reconstruction input |
| In-memory string result | **`StringTraceInstance`** (proposed canonical name) | Complete textual output for one generated run, held as a runtime object without creating a filesystem file | No; return to caller, discard unless requested |
| Materialized output file | `MaterializedArtifact` | File bytes derived from a verified generated result and written only when a caller requests file output | Only by explicit output request/profile |

### Terminology decision for the “non-file” object

Use **`StringTraceInstance`** for the in-memory textual result and **`GeneratedTrajectory`** for the abstract state/transition sequence. `StringTraceInstance` is a proposed implementation name, not an existing canonical schema name yet. Keep `TraceStringInstance` as a possible alias only if an existing code convention demands it; do not use both names for different things.

“String” means a runtime text value, not a hidden file and not persistent history. A run can create a `StringTraceInstance` from generated trajectory/evidence, return it directly, and exit without creating directories or writing bytes to disk. The object may contain the complete requested textual artifact, while the persistent reconstruction record remains compact and independent of that output.

If the requested output is binary, do not claim arbitrary bytes are a text string. Use an in-memory `bytes` payload or a documented base64 text envelope. The simplest first vertical slice should support UTF-8 text, with binary formats deferred unless already required by an existing use case.

Suggested initial shape:

```python
@dataclass(frozen=True)
class StringTraceInstance:
    trace_id: str
    record_id: str
    content: str                 # complete generated UTF-8 text
    media_type: str              # e.g. text/plain; charset=utf-8
    generated_steps: int
    terminal_state: object
    closure_hash: str | None
    verifier_id: str | None
    verified: bool
    content_sha256: str
    provenance: dict[str, object]
```

This is an implementation proposal. Adapt the types to the repository’s conventions, but preserve the semantics and fields needed to bind the string to its generation record and verifier. Do not serialize arbitrary Python callables into the instance. Store versioned identifiers/hashes for transform sets, constraint policies, selectors, and verifiers.

## 4. Dynamic file generation

File output is a materialization adapter around generation, not the definition of Manifold RAID.

```text
InvariantReconstructionRecord
  -> dynamic generator
  -> GeneratedTrajectory
  -> declared verifier
  -> serializer / output adapter
       ├── string mode: return StringTraceInstance; no filesystem write
       ├── file mode: write verified content and return MaterializedArtifact
       └── both mode: return the string instance and materialize the same bytes
```

Recommended public call shape for a first implementation:

```python
result = generate_artifact(
    record=record,
    output_mode="string",        # "string" | "file" | "both"
    output_root=None,             # required for file/both, ignored in string mode
    relative_path=None,
)
```

If the repository chooses another API, retain these externally observable guarantees:

1. **String mode:** returns the complete string instance; no open/write/mkdir/rename/unlink calls and no file creation.
2. **File mode:** requires an explicit output root and relative path or a safe generated filename; refuses traversal and refuses to escape the output root.
3. **Both mode:** writes exactly the UTF-8 bytes represented by the string instance; the file’s SHA-256 equals `content_sha256`.
4. **Verification first:** do not materialize an output from a failed/unverified trajectory unless an explicit diagnostic mode is separately designed. Diagnostic mode must label partial output and must never report it as accepted.
5. **Atomic write:** write a temporary file in the target directory, flush/close it, then atomically replace the destination after checks succeed. Avoid leaving a partial artifact on failure.
6. **Bounded output:** enforce declared maximum steps and output bytes. Return a structured failure rather than hanging or writing partial success.
7. **Stable identity:** include a run/trace ID and record/version IDs in metadata; do not encode uncontrolled user text into a path.
8. **No reconstruction-history dependency:** the generated file/string must be produced from the invariant record, transform space, constraints, and declared policy—not by secretly reading the historical trace or cached finished output.

Filesystem-specific protections should be implemented in the output adapter: normalize the requested relative path, reject absolute paths and `..`, resolve the destination and verify it remains under `output_root`, use exclusive/atomic creation policy, and document overwrite behavior. Tests should use a temporary directory. Do not let “dynamic file generation” turn into unbounded or silent writes across the host filesystem.

## 5. Persistent record fields and earlier prototype compatibility

The current repository’s JSON Schema is `spec/seed_block.schema.json`, record version `0.2`. Its required top-level fields are:

- `record_version` (`"0.2"`);
- `invariant_state` (requires `seed_coordinates`; may include domain, invariant projection, container radius, HDRP prior/present registers);
- `transform_space` (requires `transform_set_id`; may identify trajectory family, family hash, or generator contract);
- `admissibility` (requires `constraint_set_id` and `mask_policy_id`; may define non-identity, closure reachability, resource budget);
- `generation_policy` (requires `branch_policy`: `preserve`, `rank`, `deterministic_tiebreak`, or `profile_defined`);
- `closure` (requires `equivalence_relation` and `exit_condition`; may include SHA-256 `closure_hash` and verifier ID).

Optional provenance is source/evidence metadata, not execution history. The `historical_profile` compatibility object can include `trace_id`, `tau_q_prefix`, `rho`, `margin`, and `lock`; these are not required by the current generalized architecture.

The earlier July 2026 prototype remains important and should be preserved as a historical profile, not merged into the current minimum schema. Its sequence was:

```text
raw .g8son trace -> VERIFY -> CLASSIFY -> JSON sidecar seed block
                 -> HDRP Momentum Walk -> closure verification
```

Historical seed details included `s0 ∈ R^8`, `tau_q_prefix`, trajectory family `T_G`, `R_c = max_r * 1.15 + 1.0`, `rho`/margin/lock, and `closure_hash`. The encoder required VERIFY then CLASSIFY before persistence (`tau ∈ Ω(C)` and a unique class/family under that prototype’s rule). The decoder initialized `R_-1`/`R_0`, derived momentum `m = R_0 - R_-1`, pruned by gates, and stopped only at a valid exit plus closure match. The historical correction says A2 container validity is evaluated at orbit completion, not as a naive per-step containment rule.

Historical JSON sidecar path: `manifold_raid_store/seed_blocks.json`. Locate the original implementation/test assets before moving or deleting anything; remembered paths include `test_manifold_raid.py`, `bad_loop.g8son`, and `manifold_raid_store/seed_blocks.json`. Some prior repository artifacts may have since moved.

## 6. Existing repository and confirmed baseline

The repository is `nhartman000/manifold-RAID`, default branch `main`, currently private. The current `main` snapshot contains:

- `README.md` — current overview and status;
- `docs/CURRENT_DYNAMIC_TRAJECTORY_MODEL.md` — canonical current model;
- `docs/ARCHITECTURE.md` — expanded architecture and historical mapping;
- `docs/DEMONSTRATED_VS_HYPOTHESIS.md` — evidence boundaries;
- `docs/EXPERIMENTAL_RESULTS.md` — historical bounded test results;
- `docs/RESEARCH_HYPOTHESIS.md` — hypothesis and falsification framing;
- `docs/RELATIONSHIP_TO_TCTA_HDRP_MG8.md` — subsystem roles;
- `docs/PROVENANCE.md`, `docs/ARTIFACT_INDEX.md`, `docs/CONVERSATION_CHRONOLOGY_2026.md`;
- `spec/seed_block.schema.json` — v0.2 reconstruction-record schema;
- `reference/dynamic_generator.py` — current no-history generic reference generator;
- `tests/test_dynamic_generator.py` — five tests for no-history path generation, alternate path, admissibility, fail-closed, and step bound.

The current reference example generates `0 -> 2 -> 4 -> 6` without receiving the comparison history `0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6`. The reference generator accepts initial state, transforms, admissibility predicate, closure predicate, selector, and max step count. It returns states and `TransitionEvidence`; it does not yet expose the proposed `StringTraceInstance` or dynamic filesystem adapter. The repository README reports the current no-history suite as 5/5. Re-run tests on the actual local checkout before modifying or relying on that result.

The workspace in which this handoff was prepared had no local project files mounted, so no local checkout status or working-tree changes were inspected. Before coding, Hermes must identify the user’s actual checkout and compare it with GitHub `main`; never overwrite uncommitted local work.

## 7. Results and evidence boundaries

Reported historical controlled prototype results:

- 4/4 round trips passed;
- 0.000 measured drift under the declared test relation;
- aggregate representation ratio `C_r = 2.49x`;
- three larger traces approximately 3.10x–3.40x;
- one small exemplar `0.23x` (larger representation than trace), explicitly showing compression is not universal;
- `bad_loop.g8son` rejected without an accepted seed;
- protected `citadel.db`, `restore.sh`, `ingest_router.py`, and `behavior_injector.py` were reported byte-identical by SHA-256 checks;
- historical test process `test_manifold_raid.py` exited 0.

The current generalized reference path generator separately has five bounded synthetic tests. These are not the same experiment as the July prototype. Do not merge their claims.

What is established: bounded examples show trace-independent admissible path generation in the current reference code, and historical controlled results report trace-to-seed regeneration and rejection behavior.

What remains a hypothesis: discovering sufficient invariant representations for broader computational classes; resource advantage after including encoding, generation, and verification; robust closure reachability; production-scale dynamic file generation; generalized semantic equivalence; distributed/hardware fault tolerance; unique path recovery where several valid continuations exist.

Compression, latency, energy savings, and resilience are measurements to earn, not architectural axioms. Report both successful and unfavorable cases, including the `0.23x` example.

## 8. Relationship to adjacent systems

- **TCTA:** defines admissible state transformations and transform algebra.
- **HDRP:** supplies local present/previous state direction or momentum for ranking candidate continuations; it does not provide a saved historical path.
- **OGSI:** supplies trajectory-family discrimination or structural reduction where that capability is available.
- **Manifold RAID:** defines what invariant reconstruction information must persist and dynamically generates/validates an admissible path or requested artifact.
- **MG8 / QSON / CIIU:** can provide bounded representation/orchestration and optional evidence formats. Runtime traces can be exported for audit but are not inherently the reconstruction substrate.
- **NYCH:** when a profile uses NYCH rules, those rules define authoritative symbolic constraints and must be verified at the relevant boundary. Do not imply that the current generic Python example already implements the entire NYCH pipeline.

Earlier explorations also described parallel semantic/manifold representations, role/action manifolds, adaptive trust, RAID-5-style quantized XOR, and noisy parity. Keep them in a **legacy/research history** section. They are not the current canonical file-less dynamic-trajectory model and must not silently re-enter its core runtime.

## 9. Fastest safe implementation plan

The target is one vertical slice: create a record, generate an admissible trajectory without historical input, verify closure, return the complete text in memory, and optionally materialize the exact same text to a file.

### Phase 0 — protect and baseline

1. In the actual local `manifold-RAID` checkout, inspect `pwd`, `git status --short --branch`, remotes, and latest commit. Preserve all uncommitted changes.
2. Read the README, architecture docs, schema, generator, tests, and workflow from that checkout.
3. Run the existing suite before edits; record the command, output, and commit SHA.
4. Find historical encoder/decoder assets and tests (`test_manifold_raid.py`, `bad_loop.g8son`, sidecar JSON). Do not replace them with the reference model.

### Phase 1 — define output contract

1. Add a small module, likely `reference/artifacts.py` or a package-equivalent matching the repository layout.
2. Define `StringTraceInstance` plus a `MaterializedArtifact` result and explicit `output_mode` enum.
3. Serialize generated trajectory/evidence deterministically to UTF-8 text. Specify newline convention, canonical JSON settings if JSON is chosen, and content hashing.
4. Bind each result to `record_id`, transform-set ID, constraint/mask policy IDs, selection-policy ID, verifier ID, run/trace ID, terminal state, and closure result.
5. Keep historical trace as an optional provenance input only when a historical profile explicitly requests it. The current generator itself must not accept or inspect it.

### Phase 2 — implement and test string-only path first

1. Generate an admissible trajectory through the existing `generate_trajectory` reference API.
2. Verify every transition, step limit, terminal closure, and declared behavioral equivalence.
3. Build and return `StringTraceInstance` only after verification succeeds.
4. Prove string mode has no filesystem side effects by patching/intercepting file operations or by testing with a controlled temp root and asserting it remains empty.
5. Test deterministic serialization and SHA-256 across identical runs under a deterministic profile.

### Phase 3 — add optional file materialization

1. Add a separate output adapter that receives a verified `StringTraceInstance`.
2. Require explicit output root/path for file mode, enforce path confinement, and use atomic writes.
3. Return path, byte count, and SHA-256; verify they match the source string instance.
4. Support `both` by returning the same instance plus materialization metadata.
5. Add tests for exact byte equality, file content, no partial output on error, path traversal rejection, missing output-root rejection, collision/overwrite policy, and max output bytes.

### Phase 4 — integrate record validation and CLI/API

1. Validate input records against `spec/seed_block.schema.json` before generation.
2. Verify referenced transform, constraint, selector, and verifier identities resolve to installed/versioned implementations.
3. Add one small CLI or callable example that accepts a record and asks for `string`, `file`, or `both`; avoid building a service/UI until this vertical slice passes.
4. Keep generation, verification, serialization, and file writing as separate modules/functions so each boundary can be tested.

### Phase 5 — CI and provenance

1. Ensure CI runs the existing tests and all new output-mode tests on the repository’s supported Python version.
2. Add a synthetic fixture that generates an alternate valid path with no historical trace supplied.
3. Add invalid-record, no-admissible-candidate, no-closure, wrong-hash, and attempted-history-injection tests.
4. Preserve protected repository/source bytes in any legacy benchmark and record SHA-256 evidence.
5. Update docs only with actually run commands, exact pass counts, platform/runtime, fixture scope, and limitations.

## 10. Acceptance checklist

The first implementation is done when all are true:

- [ ] Existing tests pass unchanged or behavior changes are documented and justified.
- [ ] A valid invariant record can produce a valid path with no historical trace argument.
- [ ] Every executed transform was in the current admissible set.
- [ ] Empty admissible set and step exhaustion fail closed.
- [ ] Branches are preserved or resolved only by the declared policy.
- [ ] Acceptance requires closure/equivalence verification.
- [ ] `StringTraceInstance` contains the complete requested text and has a reproducible content hash.
- [ ] String mode creates no files or directories.
- [ ] File mode writes the exact same UTF-8 content, within the caller’s output root, atomically.
- [ ] Failed verification does not produce an accepted artifact.
- [ ] Historical benchmarks and current synthetic tests remain clearly separated.
- [ ] Docs do not claim universal compression, universal determinism, hardware resilience, or broad semantic equivalence from bounded examples.

## 11. Direct task prompt for Hermes or Claude

> Work in the existing `nhartman000/manifold-RAID` repository and first inspect the local checkout, its git status, branch, remotes, and commit. Do not overwrite or discard uncommitted work. Read the current README, `docs/CURRENT_DYNAMIC_TRAJECTORY_MODEL.md`, `docs/ARCHITECTURE.md`, `docs/EXPERIMENTAL_RESULTS.md`, `docs/DEMONSTRATED_VS_HYPOTHESIS.md`, `docs/RELATIONSHIP_TO_TCTA_HDRP_MG8.md`, `spec/seed_block.schema.json`, `reference/dynamic_generator.py`, and all current tests. Run the baseline suite before editing.
>
> Implement the smallest complete vertical slice for Manifold RAID: a validated v0.2 invariant reconstruction record drives the existing no-history admissible trajectory generator; a verifier checks admissibility and closure; the result can be returned as an in-memory `StringTraceInstance` containing the complete UTF-8 output without creating any file; and an optional explicit `file`/`both` output mode materializes exactly those bytes safely and atomically under a caller-specified root. Keep `GeneratedTrajectory`, evidence, `StringTraceInstance`, persistent reconstruction record, and file materialization as separate concepts. Do not make a historical trace a required generator input. Preserve the July prototype as a legacy profile and do not merge its trace prefix into the current minimum record. Fail closed on invalid records, empty admissible sets, failed closure, max-step exhaustion, unsafe paths, and byte-limit violations. Add focused tests for the acceptance checklist above, run the full suite and CI-equivalent checks, and report exact changed paths, commands, results, and remaining limitations. Do not claim performance, universal compression, production resilience, or general semantic equivalence without measurements that support those claims.

## 12. Source-of-truth files

Use repository source files as the code baseline; this handoff is a build guide, not a replacement for the schema or existing tests.

- `README.md`
- `docs/CURRENT_DYNAMIC_TRAJECTORY_MODEL.md`
- `docs/ARCHITECTURE.md`
- `docs/DEMONSTRATED_VS_HYPOTHESIS.md`
- `docs/EXPERIMENTAL_RESULTS.md`
- `docs/RESEARCH_HYPOTHESIS.md`
- `docs/RELATIONSHIP_TO_TCTA_HDRP_MG8.md`
- `docs/PROVENANCE.md`
- `spec/seed_block.schema.json`
- `reference/dynamic_generator.py`
- `tests/test_dynamic_generator.py`

If the local checkout differs from GitHub `main`, identify the divergence first and preserve the newer/user-authored work. Resolve discrepancies explicitly in the implementation notes.
