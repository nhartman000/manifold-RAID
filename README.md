# Manifold RAID

**Manifold RAID — Redundant Array of Invariant Data**

Manifold RAID is an experimental architecture for **Invariant State Representation (ISR)** and **dynamic admissible-trajectory generation**. Its current design does **not** treat a saved execution trace as the primary computational artifact. Instead, it persists the invariant state, admissibility constraints, transform-family information, and closure/verification conditions needed to generate a valid execution trajectory when execution is required.

The central question is:

> Can a bounded computational system preserve a compact invariant representation of what states and transforms are admissible, then dynamically generate a behaviorally equivalent trajectory at runtime without retaining the historical execution trace?

## Current canonical principle

The persistent object is **not** the historical trajectory `tau_history`.

The persistent object is an invariant reconstruction record containing enough information to determine the admissible transform space from a current state and verify an acceptable terminal outcome.

At runtime, Manifold RAID generates:

```text
SR_t
  |
  v
candidate transforms
  |
  v
ADMISSIBILITY MASK / CONSTRAINT GATE
  |
  v
A_t = { T | (SR_t, T, T(SR_t)) satisfies C and family constraints }
  |
  v
HDRP / OGSI / policy ranking or branch preservation
  |
  v
select admissible T_t
  |
  v
SR_{t+1} = T_t(SR_t)
  |
  +---- repeat until declared exit / closure condition
```

The generated trajectory

`tau_hat = (SR_0, T_0, SR_1, T_1, ..., SR_n)`

is a **derived runtime artifact**. It may be emitted temporarily for verification/audit, but it is not required to be retained as the reconstruction substrate.

## What Manifold RAID persists

The current canonical record is centered on:

- invariant/seed state `SR_0` or invariant projection `Gamma(SR)`;
- state-domain and container constraints `C`;
- admissible transform vocabulary or transform-set identity;
- trajectory-family constraints `T_G` where a family has been resolved;
- transform admissibility policy / constraint mask;
- HDRP present/previous-register initialization where required;
- branch/tie-breaking policy where more than one continuation remains admissible;
- terminal exit condition;
- behavioral-equivalence relation;
- `closure_hash` or another machine-checkable closure condition;
- version/hash identities for the rules used to regenerate the path.

## What Manifold RAID does not need to persist

The current architecture does **not require persistence of**:

- the complete historical state sequence;
- the complete historical transform sequence;
- a QSON or equivalent execution log as an input to reconstruction;
- an exact replay of the original internal path;
- the original raw trace after a sufficient invariant representation has been established and independently verified.

A runtime execution trace can still be generated for evidence, debugging, audit, or CIIU/QSON interoperability. That trace is **output evidence**, not the source of future reconstruction.

## Dynamic admissible-transform formulation

For current state `SR_t`, constraint set `C`, and applicable transform family `T_G`, define the admissible continuation set:

```text
A(SR_t, C, T_G)
  = { T in T_G | (SR_t, T, T(SR_t)) satisfies C }
```

A constraint mask may further remove transforms that violate state, domain, policy, topology, resource, or closure-preservation requirements.

Then:

```text
T_t = Select(A_t, HDRP_delta, OGSI_family_information, generation_policy)
SR_{t+1} = T_t(SR_t)
```

where the HDRP local trajectory delta is based on present/previous state context:

`Delta_t = R_0 - R_-1`

Selection does not need to pretend that only one continuation always exists. If multiple transforms remain admissible, Manifold RAID may preserve the branch set until later state information resolves it. A deterministic replay claim is appropriate only where the record, selection policy, and tie-breaking rules actually determine a unique path.

## Relationship to the historical July prototype

The recovered concept line begins on **2026-04-25** with metadata-first/file-less persistence and on-demand reconstruction rather than conventional file storage.

By **2026-07-08**, the working prototype used:

```text
raw .g8son trace
    -> VERIFY
    -> CLASSIFY
    -> seed block / JSON sidecar
    -> HDRP Momentum Walk
    -> closure verification
```

That prototype proved an important intermediate step: a verified compact representation could support regeneration after the raw trace was removed in the bounded test line.

The **current architecture generalizes the idea one step further**:

> the seed is no longer conceptually a compressed history of the old path; it is a compact description of the invariant state and the admissible transform space from which a new valid path can be generated dynamically.

The historical `tau_q_prefix` remains part of the provenance record and may still be used as an optional anchor in a particular profile, but a saved historical prefix is **not a universal requirement of the current architecture**.

## Demonstrated bounded results

### Historical July prototype

Controlled prototype testing previously reported:

- raw execution traces were removed before regeneration in the tested workflow;
- **4 / 4** verification/round-trip passes;
- **0.000** measured reconstruction drift under the declared test relation;
- aggregate representation ratio **C_r = 2.49x**;
- three larger traces at approximately **3.10–3.40x** representation ratio;
- one small exemplar at **0.23x**, showing the method is not universally compressive;
- negative `bad_loop.g8son` rejection with **no accepted seed**;
- protected core artifacts remained byte-identical under SHA-256 checks;
- `test_manifold_raid.py` exited `0`.

### Current trace-independent reference model

The repository now includes `reference/dynamic_generator.py`. GitHub Actions compiles it under Python 3.12 and the current no-history suite passes **5 / 5 tests**.

The passing reference tests demonstrate, on bounded synthetic state spaces:

- trajectory generation without historical trace input;
- generation of `0 -> 2 -> 4 -> 6` while a different comparison history `0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6` is never supplied to the generator;
- non-admissible transforms are never executed;
- an empty admissible set fails closed;
- generation cannot exceed the declared step bound.

This is a tested software proof of the **current path-generation semantics**, not a general proof that arbitrary computational classes admit alternate behaviorally equivalent trajectories.

## Research framing

The current Manifold RAID hypothesis is more precise than “invariant compression”:

> For identifiable computational classes, persistent execution may be represented by invariant state plus admissible-transform constraints, allowing execution trajectories to be generated dynamically and verified when needed instead of preserving complete execution history.

The primary object of study is therefore **representation sufficiency + admissible trajectory generation + verification**.

Compression, storage reduction, energy reduction, and bandwidth reduction are possible consequences to measure, not axioms of the architecture.

## DARPA research baseline

On **2026-07-10**, the ISR/Manifold RAID research line was submitted to DARPA MXO under the Low Resource Computing RFI as:

**Invariant State Representations for Procedural Regeneration: A New Computational Abstraction for Low-Resource Autonomous Computing**

The current dynamic-trajectory formulation remains consistent with that premise: execution history becomes a derived artifact rather than the primary stored artifact.

## Repository status

This repository is the canonical Manifold RAID project/provenance line and remains intentionally **private**. It preserves the historical prototype separately from the current architectural formulation and does not incorporate unpublished third-party research, NDA material, or later cross-architecture synthesis.

## Documentation

The [bounded public reference summary](PUBLIC_RELEASE.md) describes the additional
persisted-record integer profile, the reproducible nine-test run, and its limits.
This research repository remains private; the public release package contains
only the selected reference files, example, tests, and summary.


- [`docs/CURRENT_DYNAMIC_TRAJECTORY_MODEL.md`](docs/CURRENT_DYNAMIC_TRAJECTORY_MODEL.md) — current canonical ISR + admissible-transform generation model
- [`docs/DEMONSTRATED_VS_HYPOTHESIS.md`](docs/DEMONSTRATED_VS_HYPOTHESIS.md) — historical evidence, current passing reference tests, and remaining hypotheses
- [`docs/CONVERSATION_CHRONOLOGY_2026.md`](docs/CONVERSATION_CHRONOLOGY_2026.md) — recovered concept chronology
- [`docs/RESEARCH_HYPOTHESIS.md`](docs/RESEARCH_HYPOTHESIS.md) — current research hypothesis and falsification criteria
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — current architecture and historical prototype mapping
- [`docs/EXPERIMENTAL_RESULTS.md`](docs/EXPERIMENTAL_RESULTS.md) — bounded historical benchmark and integrity record
- [`docs/DARPA_MXO_LOW_RESOURCE_RFI_2026-07-10.md`](docs/DARPA_MXO_LOW_RESOURCE_RFI_2026-07-10.md) — dated MXO research baseline
- [`docs/RELATIONSHIP_TO_TCTA_HDRP_MG8.md`](docs/RELATIONSHIP_TO_TCTA_HDRP_MG8.md) — relation to TCTA, HDRP, OGSI, and MG8
- [`docs/PROVENANCE.md`](docs/PROVENANCE.md) — evidence and IP/collaboration boundary
- [`spec/seed_block.schema.json`](spec/seed_block.schema.json) — current invariant reconstruction record schema
