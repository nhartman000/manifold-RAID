# Manifold RAID Relationship to TCTA, HDRP, OGSI, and MG8

## Purpose

Manifold RAID shares concepts and interfaces with several Hartman / American Milestone systems, but each has a distinct technical role.

The current Manifold RAID architecture uses those roles together to replace persisted execution history with **invariant state + admissible-transform generation**.

## TCTA — admissibility and transform-space semantics

Trajectory-Constrained Transform Algebra provides the formal vocabulary for the current generation layer:

- state representation `SR = (s, D, C)`;
- transforms `T : SR_in -> SR_out`;
- ordered trajectories `tau`;
- admissible trajectory/transform space `Omega(C)`;
- constraint-mask / admissible-space truncation;
- trajectory-family resolution;
- branch preservation where multiple continuations remain valid;
- CIIU transition records `(SR_in, T, SR_out, M)`.

The historical July Manifold RAID prototype used a whole-trace acceptance relation:

`tau in Omega(C)`

before accepting a seed.

The current architecture applies the same logic **incrementally to generation**.

For current state `SR_t`:

```text
A_t = { T in T_G | (SR_t, T, T(SR_t)) satisfies C_t }
```

Only transforms in `A_t` are eligible for execution.

This is the key current relationship:

> TCTA defines the admissible transform geometry; Manifold RAID persists enough invariant information to regenerate execution by traversing only that admissible geometry.

## HDRP — local trajectory direction

The Hartman Dual-Register Predictor contributes present/previous-state context:

- present state register `R0`;
- previous state register `R-1`;
- local trajectory delta / momentum `Delta_t = R0 - R-1`;
- bounded forward projection/ranking information.

HDRP does **not** supply a stored historical trajectory. It supplies local directional information that can help rank currently admissible continuations.

This makes HDRP naturally compatible with dynamic path generation:

```text
admissible transforms A_t
        +
HDRP local delta Delta_t
        -> rank/preserve/select continuation
```

The July prototype's **HDRP Momentum Walk** is retained as the demonstrated historical decoder profile.

## OGSI — family discrimination

Orthogonal Gestalt Symmetry Identification (OGSI) contributes trajectory/transform-family discrimination.

Where OGSI resolves or scores family structure, it can:

- reduce candidate transforms to a compatible family;
- help distinguish admissible continuations;
- preserve branch points where more than one family/continuation remains supported.

OGSI information therefore helps constrain the dynamic generator without requiring the original execution path to be stored.

OGSI family discrimination should not be represented as a guarantee of unique continuation unless the actual constraints resolve one unique transform.

## Manifold RAID — persistence and regeneration abstraction

Manifold RAID's distinct job is to persist the minimum sufficient **reconstruction structure** rather than the historical execution sequence.

The current persistent record identifies:

- invariant/entry state;
- applicable transform space/family;
- admissibility constraints and constraint-mask identity;
- generation/branch policy;
- closure/equivalence conditions;
- optional HDRP/OGSI initialization metadata.

At runtime it generates `tau_hat` by repeated admissible transforms and verifies the terminal relation.

## MG8 family — representation and runtime interfaces

MG8-related formats/runtime concepts provide software boundaries that can host the Manifold RAID model:

- `.mg8` — bounded unit/container manifest;
- `.gst` — state/context representation;
- `.g8son` — gate/admissibility/policy representation;
- `.qson` — generated execution/audit evidence;
- `.ork` — orchestration role;
- `.mg8pk` — package role.

A useful current mapping is:

```text
.gst     -> invariant/current state and constraints
.g8son   -> admissibility / gate / transform conditions
.mg8     -> bounded reconstruction-unit manifest
.ork     -> generation/orchestration profile
.qson    -> optional generated run evidence, NOT required historical input
.mg8pk   -> package/distribution boundary
```

The historical July Manifold RAID prototype used raw `.g8son` traces and a JSON seed sidecar before the current MG8 family was fully canonicalized. That chronology remains explicit.

## Current architectural separation

```text
                 TCTA
     state + admissible transform algebra
                  |
                  v
             constraint mask
                  |
                  v
Invariant record -> Manifold RAID dynamic generator
                  |             |
                  |             +--> OGSI family discrimination
                  |             +--> HDRP local trajectory delta
                  v
         generated admissible tau_hat
                  |
                  v
       closure/equivalence verifier
                  |
                  +--> optional QSON/CIIU evidence

MG8 family provides bounded software representation/orchestration interfaces
around the state, constraints, generator, and evidence layers.
```

## Shared overarching principle

The systems share a broader research principle:

> computation can be represented as constrained state transformation, with admissible future trajectories generated from invariant structure rather than requiring archival preservation of every historical execution step.

That shared principle does not make TCTA, HDRP, OGSI, Manifold RAID, and MG8 interchangeable. Their roles are complementary:

- **TCTA:** what transformations are admissible;
- **HDRP:** local state-transition direction/context;
- **OGSI:** family discrimination and structural reduction;
- **Manifold RAID:** what invariant reconstruction information must persist and how a valid trajectory is regenerated;
- **MG8:** bounded software representation/orchestration/trace interfaces.
