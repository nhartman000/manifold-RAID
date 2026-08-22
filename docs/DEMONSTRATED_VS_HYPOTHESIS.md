# Manifold RAID — Demonstrated vs Current Hypothesis

## Purpose

This document separates three evidence tiers:

1. the recovered July 2026 bounded Manifold RAID prototype;
2. the current August 22 trace-independent reference implementation and CI tests;
3. broader research hypotheses that remain unproven.

## A. Demonstrated in the recovered bounded prototype

The July 2026 Manifold RAID test/artifact line reports the following as observed behavior within the tested cases.

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

## B. Supported inference from the historical prototype

The recovered results support this narrower inference:

> For the tested bounded cases, a verified compact representation retained enough information to regenerate the required result after the raw trace was removed.

They also support the operational distinction between:

- source/history used to discover or validate a representation; and
- the representation used later for regeneration.

## C. Current August 22 reference implementation — tested

The repository now contains `reference/dynamic_generator.py`, a trace-independent generator whose API accepts:

- `initial_state`;
- a transform vocabulary;
- an admissibility predicate / constraint mask;
- a branch/selection function;
- a terminal closure predicate;
- a maximum generation bound.

It **does not accept historical execution history as an input**.

GitHub Actions run `32564358980` compiled the reference model under Python 3.12 and executed the no-history test suite successfully.

**Result: 5 / 5 tests passed.**

The passing tests establish the behavior of this reference implementation for its synthetic bounded cases:

1. `test_generates_path_without_historical_trace_input` — generates `0 -> 2 -> 4 -> 6` from state, transforms, constraints, selector, and closure only;
2. `test_generated_path_can_differ_from_reference_history` — the generated `0 -> 2 -> 4 -> 6` path reaches the same terminal state as a comparison history `0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6`, while that history is never supplied to the generator;
3. `test_non_admissible_transforms_are_never_executed` — constraint-masked transforms are excluded from the generated path;
4. `test_fails_closed_when_no_admissible_continuation_exists` — generation rejects a state with no valid continuation;
5. `test_step_bound_prevents_unbounded_generation` — generation fails when closure cannot be reached within the declared bound.

This is now a **tested software proof-of-architecture** for the distinction between historical replay and dynamic admissible-path generation.

It is not a general proof about arbitrary real computational classes.

## D. Current architecture extension

The current Manifold RAID model is:

> persist invariant state plus admissible-transform structure, then dynamically generate and verify an execution trajectory rather than persist historical execution as the reconstruction substrate.

For current state `SR_t`:

```text
A_t = { T in T_G | (SR_t, T, T(SR_t)) satisfies C_t }
```

and only `T in A_t` may be executed.

The current reference implementation demonstrates this mechanism on bounded synthetic state spaces. The historical prototype separately demonstrates trace removal plus verified regeneration on the recovered four-case benchmark.

Together these are stronger evidence than either alone, but they still do not establish universality.

## E. Not yet generally demonstrated

The following remain research hypotheses or future validation targets:

- dynamically generating materially different admissible trajectories across non-synthetic computational workloads while preserving the declared behavioral-equivalence relation;
- proving closure reachability from local admissibility constraints alone;
- discovering minimal sufficient invariant records automatically across broad computational classes;
- proving that all admissible branch ambiguity can be resolved without retaining significant history;
- proving that all useful computational classes admit compact ISRs;
- universal deterministic path uniqueness;
- universal storage/compression advantage;
- universal energy or bandwidth savings;
- hardware fault tolerance/resilience as an established property;
- global optimality of HDRP/OGSI transform selection.

## F. Next empirical validation

The next stronger experiment should apply the current no-history generator semantics to a non-synthetic bounded workload:

1. define a real transform vocabulary `T_G` and constraint set `C`;
2. persist only the current invariant reconstruction record—not a historical path;
3. delete/exclude the historical execution trace from generation;
4. generate candidate transforms dynamically at each state;
5. prune all non-admissible transforms;
6. preserve or resolve legitimate branches under a declared policy;
7. reach terminal closure;
8. verify behavioral equivalence;
9. compare generated `tau_hat` against `tau_history` only after the run;
10. measure representation size plus discovery/generation/verification resource cost.

A successful non-synthetic alternate-path case would materially strengthen the claim that **admissible dynamic trajectory generation**, rather than trace replay, is sufficient for a useful computational class.
