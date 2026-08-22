# Manifold RAID — Preliminary Bounded Results

## Status

These results document a prior controlled prototype exercise reconstructed from the July 8–10, 2026 Manifold RAID conversation/artifact line. They are retained as preliminary engineering evidence and must not be read as a universal proof of invariant-state reconstruction, generalized losslessness, or hardware performance.

## Benchmark table

| Benchmark | Raw trace bytes | Seed / ISR bytes | Representation ratio `C_r` | Reconstruction error | Result |
|---|---:|---:|---:|---:|---|
| `BINARY_SEARCH` | 949 | 279 | 3.40× | 0.000000 | PASS |
| `SIGNAL_TRAP / MXO` | 896 | 277 | 3.23× | 0.000000 | PASS |
| `RUNTIME_GUARD` | 880 | 284 | 3.10× | 0.000000 | PASS |
| `SIGNAL_TRAP variant` exemplar | 66 | 282 | 0.23× | 0.000000 | PASS |
| **Aggregate** | **2791** | **1122** | **2.49×** | **0.00** | **4 / 4 PASS** |

The small exemplar is intentionally retained. Its `0.23×` ratio means the representation was larger than its source trace, demonstrating that **Manifold RAID is not universally compressive**. The primary research target is representation sufficiency and verified regeneration, not compression ratio.

## Reported test outcome

The bounded prototype test reported:

| Measure | Result |
|---|---:|
| Round trips | 4 / 4 PASS |
| Byte-identical reconstructions | 4 / 4 |
| Measured drift | 0.000 |
| Aggregate representation ratio `C_r` | 2.49× |
| Larger-trace comparison | approximately 3.10–3.40× for the three larger tested traces |
| Test process | `test_manifold_raid.py` exit 0 |

Associated July artifacts also reported ISR fidelity at or above the declared tested threshold and behavioral-equivalence verification under the experiment's bounded relation. Those fidelity statements should remain tied to the preserved experiment definition rather than generalized outside the tested classes.

## Negative path

`bad_loop.g8son` was used as a rejection case.

The reported behavior was:

- trajectory fails the bounded acceptance path;
- no accepted Manifold seed block is created;
- failed paths are not silently coerced into reconstructable representations.

This negative test is as important as successful round trips because VERIFY/CLASSIFY must be capable of refusing unsupported trajectories.

## Encoder evidence

The recovered architecture records two hard acceptance stages:

1. `VERIFY` — `tau ∈ Omega(C)`;
2. `CLASSIFY` — unique trajectory family `T_G`.

Only accepted traces proceed to seed representation.

The historical seed block includes:

- `seed_coordinates` / `s0 ∈ R^8`;
- `tau_q_prefix`;
- `trajectory_family`;
- `container_radius R_c`;
- `rho`;
- margin / lock metadata;
- `closure_hash`.

## Decoder evidence

The recovered procedural decoder is described as an **HDRP Momentum Walk**:

- initialize `R-1` and `R0`;
- derive local momentum `m = R0 - R-1`;
- rank candidate continuation by coherence with the momentum/state relation;
- prune using bounded axioms/gates;
- terminate only on a valid exit plus closure match.

The July artifact preserves a significant correction:

> A2 container validity is evaluated at **orbit completion**, not as a naive per-step containment rule.

The per-step interpretation was identified as ill-posed because it could cause false pruning. This correction is retained as part of the engineering record.

## Software-integrity record

The historical test record reports SHA-256 before/after checks showing the protected core corpus unchanged across the pipeline. The poster names the following protected items:

- `citadel.db` snapshot;
- `restore.sh`;
- `ingest_router.py`;
- `behavior_injector.py`.

The purpose of this check was to show that Manifold RAID encoded/reconstructed around the protected source state rather than obtaining success by rewriting the source corpus during the test.

The repository does not currently contain the original full hash strings, so this document does not invent or reconstruct them from shortened poster text.

## Interpretation

A successful bounded closure test means the tested reconstruction satisfied the experiment's declared verification/equivalence condition. It does **not** imply that arbitrary programs, states, physical processes, or future implementations admit equivalent invariant representations.

The ratio `C_r` is a representation/resource observation. It is not a theorem and not the primary research objective.

## Required future validation

A stronger evaluation program should separately measure:

- minimum representation fidelity `F_min`;
- closure success/failure rates across larger computational classes;
- false-positive and false-negative acceptance at VERIFY/CLASSIFY boundaries;
- reconstruction error and drift across repeated cycles;
- ambiguity where multiple admissible trajectory families remain;
- resource overhead of ISR discovery, storage, verification, and regeneration;
- behavior under perturbation/adversarial state changes;
- failure cases where no sufficient ISR exists;
- whether representation savings survive when decoder/exemplar-bank costs are included.
