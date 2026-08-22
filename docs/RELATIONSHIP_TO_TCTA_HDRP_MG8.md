# Manifold RAID Relationship to TCTA, HDRP, and MG8

## Purpose

Manifold RAID shares concepts and interfaces with several Hartman / American Milestone systems, but it should remain a distinct architecture.

## TCTA

Trajectory-Constrained Transform Algebra provides the strongest formal vocabulary for Manifold RAID's verification layer:

- state representation `SR = (s, D, C)`;
- ordered transform trajectories `tau`;
- admissible trajectory space `Omega(C)`;
- trajectory-family resolution;
- constraint-mask/admissible-space truncation;
- branch preservation where multiple admissible continuations remain;
- trace / transform records.

In Manifold RAID, the recovered VERIFY gate is represented as:

`tau ∈ Omega(C)`

and the CLASSIFY stage resolves a trajectory family `T_G` before a seed is accepted.

TCTA therefore supplies formal admissibility/trajectory language, while Manifold RAID asks whether a compact invariant representation of the accepted trajectory/state relation is sufficient for reconstruction.

## HDRP

The Hartman Dual-Register Predictor contributes the local reconstruction primitive:

- present state register `R0`;
- previous state register `R-1`;
- local trajectory delta / momentum `m = R0 - R-1`;
- bounded forward continuation under constraints.

The July Manifold RAID prototype described the decoder as an **HDRP Momentum Walk**. HDRP is therefore a decoder primitive, not the Manifold RAID storage abstraction itself.

## MG8 family

MG8-related formats/runtime concepts provide useful software representation boundaries:

- `.mg8` — bounded unit/container manifest role;
- `.gst` — state/context representation;
- `.g8son` — bounded gate/policy representation;
- `.qson` — execution/audit trace;
- `.ork` — orchestration role;
- `.mg8pk` — package role.

The historical Manifold RAID prototype specifically used raw `.g8son` traces as source material and emitted/stored JSON seed blocks in a sidecar. It should not be rewritten to imply that the current canonical MG8 file family was already fully formalized at the same date.

## Architectural separation

```text
TCTA
  formal state / trajectory / admissibility layer
        |
        v
Manifold RAID encoder
  VERIFY -> CLASSIFY -> ISR seed
        |
        v
HDRP
  procedural local reconstruction primitive
        |
        v
Manifold RAID verifier
  closure / declared equivalence relation

MG8 family
  software representation, gating, orchestration, and trace interfaces
  that may host or interoperate with these layers
```

## Shared overarching principle

A later July discussion grouped these systems around a broader theme:

> computation emerges from constrained state representations evolving through geometry.

That is a useful research umbrella, but it does not erase the distinct technical roles of TCTA, HDRP, Manifold RAID, and MG8.
