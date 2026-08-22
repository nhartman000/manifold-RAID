# Manifold RAID — Demonstrated vs Current Hypothesis

## Purpose

This document prevents the historical bounded prototype results from being overstated as proof of the current generalized architecture.

## A. Demonstrated in the recovered bounded prototype

The July 2026 Manifold RAID test/artifact line reports the following as observed behavior within the tested cases:

### Representation and regeneration

- the workflow produced compact invariant/seed records from accepted source traces;
- raw execution traces were removed before regeneration in the tested workflow;
- regeneration succeeded in all four accepted bounded cases;
- verification passed 4 / 4 cases;
- measured reconstruction drift was 0.000 under the declared test relation.

### Representation sizes

| Benchmark | Raw bytes | ISR/seed bytes | `C_r` |
|---|---:|---:|---:|
| BINARY_SEARCH | 949 | 279 | 3.40x |
| SIGNAL_TRAP / MXO | 896 | 277 | 3.23x |
| RUNTIME_GUARD | 880 | 284 | 3.10x |
| SIGNAL_TRAP variant | 66 | 282 | 0.23x |
| **Aggregate** | **2791** | **1122** | **2.49x** |

The 0.23x small case is evidence that the architecture is not universally compressive.

### Gate/rejection behavior

- VERIFY and CLASSIFY were hard acceptance boundaries;
- `bad_loop.g8son` was rejected;
- the rejected case produced no accepted seed.

### Integrity behavior

- the recovered test record reports protected source artifacts unchanged under SHA-256 before/after checks;
- `test_manifold_raid.py` exited successfully.

## B. Supported architectural inference

The demonstrated results support this narrower inference:

> For the tested bounded cases, a verified compact representation retained enough information to regenerate the required result after the raw trace was removed.

They also support the operational distinction between:

- source/history used to discover or validate a representation; and
- the representation used later for regeneration.

## C. Current architecture extension

The current Manifold RAID model generalizes that demonstrated behavior to:

> persist invariant state plus admissible-transform structure, then generate a valid trajectory dynamically rather than replay or store historical execution history.

This extension is structurally consistent with the ISR premise and TCTA admissible-transform framework, but the original four-case benchmark did not by itself prove every part of this generalized model.

## D. Not yet generally demonstrated

The following remain research hypotheses or future validation targets:

- generating a trajectory that is materially different from the historical path while preserving the declared behavioral-equivalence relation;
- proving closure reachability from local admissibility constraints alone;
- discovering minimal sufficient invariant records automatically across broad computational classes;
- proving that all admissible branch ambiguity can be resolved without retaining significant history;
- proving that all useful computational classes admit compact ISRs;
- universal deterministic path uniqueness;
- universal storage/compression advantage;
- universal energy or bandwidth savings;
- hardware fault tolerance/resilience as an established property;
- global optimality of HDRP/OGSI transform selection.

## E. Current test that would materially strengthen the claim

A direct test of the new architecture should:

1. define a transform vocabulary `T_G` and constraint set `C`;
2. persist only the current invariant reconstruction record—not a historical path;
3. delete/exclude the historical execution trace from the generator;
4. generate candidate transforms dynamically at each state;
5. prune all non-admissible transforms;
6. preserve or resolve legitimate branches under a declared policy;
7. reach terminal closure;
8. verify behavioral equivalence;
9. compare generated `tau_hat` against historical `tau_history` to determine whether a different path can satisfy the same terminal relation;
10. measure representation size plus generation/verification resource cost.

A successful alternate-path case would directly demonstrate the distinction between **historical replay** and **admissible dynamic trajectory generation**.
