# Manifold RAID — Current Dynamic Admissible-Trajectory Model

**Status:** Current canonical architecture, 2026-08-22

## 1. Core change

Manifold RAID no longer treats a previously observed execution trajectory as the thing that must be preserved for later reconstruction.

The primary persistent artifact is an **invariant reconstruction record** describing:

- where execution may begin;
- what transforms are available;
- which transforms are admissible from each current state;
- how admissible branches are ranked or preserved;
- what terminal condition counts as a valid result.

The execution trajectory is generated dynamically when needed.

## 2. State and transform relation

Let:

- `SR_t = (s_t, D_t, C_t)` be the current state representation;
- `T_G` be the applicable transform family/vocabulary;
- `C_t` be the current constraint set;
- `M_C` be the constraint-mask function.

For each candidate transform `T`:

```text
SR_out = T(SR_t)
```

and:

```text
M_C(SR_t, T, SR_out) = 1
```

only when the transition is admissible.

The admissible transform set is:

```text
A_t = { T in T_G | M_C(SR_t, T, T(SR_t)) = 1 }
```

No transform outside `A_t` may be executed.

## 3. Dynamic generation loop

```text
INPUT: invariant reconstruction record R*

1. Reconstruct SR_0 from R*.
2. Load the declared transform vocabulary/family T_G.
3. Evaluate candidate transforms at SR_t.
4. Apply the constraint mask to obtain A_t.
5. If A_t is empty: FAIL CLOSED.
6. If one transform remains: apply it.
7. If multiple transforms remain:
   a. preserve the branch set, or
   b. rank using declared HDRP / OGSI / policy information, or
   c. apply an explicit deterministic tie-break rule.
8. Compute SR_{t+1} = T_t(SR_t).
9. Update present/previous state context.
10. Test exit/closure condition.
11. If not closed, repeat from step 3.
12. Verify the terminal behavioral-equivalence relation.
13. Accept only on successful verification.
```

## 4. HDRP role

HDRP supplies local direction/context rather than a saved historical path.

With:

```text
R_-1 = previous state register
R_0  = present state register
Delta_t = R_0 - R_-1
```

`Delta_t` can be used to rank candidate admissible transforms by trajectory coherence.

This means the generator can use momentum/state-transition information while still deriving the actual future trajectory dynamically.

## 5. OGSI / family role

Where a transform or trajectory family has been resolved, OGSI/family information can reduce the candidate set or rank admissible continuations.

The current model does not require that family membership force one unique path. If more than one continuation remains admissible, branch preservation is preferred over false certainty.

## 6. CIIU / QSON role

Each generated transition can emit a record such as:

```text
(SR_in, T, SR_out, M)
```

for runtime evidence.

A QSON or equivalent trace can therefore be produced for:

- audit;
- reproducibility;
- debugging;
- test evidence;
- provenance of the generated run.

But this trace is **not part of the minimum persistent reconstruction substrate**. It may be discarded after the run.

## 7. Historical trace vs generated trajectory

Historical architecture:

```text
historical trace -> compact seed -> regenerate historical/verified behavior
```

Current architecture:

```text
invariant state + admissible transform constraints
              -> dynamically generate tau_hat
              -> verify terminal behavior
```

The critical difference is that `tau_hat` does not have to equal the historical internal path unless exact path identity is itself part of the declared equivalence relation.

## 8. Closure reachability

Local admissibility is necessary but may not be sufficient. A locally valid transform can potentially lead to a later dead end.

Profiles may therefore add a closure-reachability rule:

```text
ReachableClosure(SR_out, R*) = true
```

or a bounded viability constraint that rejects transitions known to eliminate all valid terminal continuations.

This is a current research requirement, not something established by the original four-case benchmark.

## 9. Persistent record minimum

A current Manifold RAID record should identify at minimum:

- schema/version;
- invariant entry state or invariant projection;
- transform-set/family identity;
- constraint/admissibility policy identity;
- generation-selection policy identity;
- terminal exit condition;
- behavioral-equivalence relation;
- closure verification material.

The historical `tau_q_prefix` may be retained as optional profile-specific evidence or an initialization anchor. It is not a required universal field.

## 10. Acceptance rule

A generated trajectory is acceptable only if:

1. every executed transition was admissible under the active constraint set;
2. the trajectory terminates under the declared exit rule;
3. terminal verification satisfies the declared behavioral-equivalence relation;
4. required closure integrity checks pass.

This is the current Manifold RAID definition of successful procedural regeneration.
