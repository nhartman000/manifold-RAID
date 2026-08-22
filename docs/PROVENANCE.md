# Manifold RAID — Provenance Baseline

**Author / originator of the recovered Manifold RAID concept line:** Nicholas Hartman  
**Organization:** American Milestone Inc.  
**Repository:** `nhartman000/manifold-RAID`  
**Compilation/current-model date:** 2026-08-22

## Purpose

This document records the chronology and technical boundary of the Manifold RAID work represented in this repository. It is an engineering provenance record, not a legal determination of patentability, priority, inventorship, ownership, or claim scope.

## Earliest recovered concept in the six-month review window

The earliest recovered Manifold RAID discussion is dated **2026-04-25** and describes:

- metadata-first / metadata-only persistence;
- on-demand reconstruction likened to a MIDI-style live performance of stored parameters;
- RAID-style striping across storage and/or edge-compute resources;
- a file-less filesystem concept using dynamic addresses and compact vector/Fourier-like latent-space representations.

The later July ISR terminology was not retroactively assigned to the April wording in the chronology; it is recorded as a subsequent formalization of the same reconstruction-centered research direction.

## July implementation baseline

By **2026-07-08**, the recovered user-originated prototype line included:

- `manifold_raid_store/seed_blocks.json`;
- VERIFY then CLASSIFY gating;
- no seed creation after failed admissibility/classification;
- `seed_coordinates`;
- `tau_q_prefix`;
- `trajectory_family`;
- `container_radius` / `R_c`;
- `rho`, margin, and lock metadata;
- `closure_hash`;
- HDRP dual-register momentum walk `R0 - R-1`;
- A2/A3/A4 bounded pruning/termination logic;
- final verification;
- explicit negative-path testing with `bad_loop.g8son`;
- four reported successful bounded round trips with zero measured drift and aggregate `C_r = 2.49x`;
- byte-level integrity checks on protected files.

The associated ISR material records the architecture as replacing stored execution histories with compact invariant representations and procedural regeneration. The tested workflow reports raw traces removed before successful regeneration.

## July research formalization

During **2026-07-08 through 2026-07-10**, the work was formalized under the research abstraction **Invariant State Representation (ISR)** and the expanded name **Manifold RAID — Redundant Array of Invariant Data**.

The research emphasis became representation sufficiency and procedural regeneration under a defined verification relation, with representation efficiency treated as a measured consequence rather than a universal property.

The July research line also relates to the pre-existing TCTA concept of admissible trajectories/transforms within a constrained state space. Prior assistant formalization in that period explicitly described TCTA as discovering admissible trajectories within bounded problem space while ISR enables behaviorally equivalent execution without retaining prior traces. This is retained as conversation chronology, not misrepresented as a verbatim earlier user statement.

## External dated research disclosure

On **2026-07-10**, American Milestone Inc. submitted a response to DARPA-SN-26-97, MXO Low Resource Computing RFI titled:

**Invariant State Representations for Procedural Regeneration: A New Computational Abstraction for Low-Resource Autonomous Computing**

That submission presented the ISR hypothesis, Manifold RAID reference architecture, preliminary bounded results, admissible-manifold/verification framing, and falsification-oriented research questions.

## 2026-08-22 current architectural refinement

The current repository makes the relationship between the ISR and TCTA lines explicit:

> Manifold RAID persists invariant state plus the constraints/rules defining admissible transforms, then generates the execution trajectory dynamically at runtime rather than preserving the historical execution trajectory as the reconstruction substrate.

The current formulation defines, for current state `SR_t`:

```text
A_t = { T in T_G | (SR_t, T, T(SR_t)) satisfies C_t }
```

and generates:

```text
SR_t --T_t--> SR_{t+1}
```

only for `T_t in A_t`, repeating until the declared closure/equivalence condition is satisfied.

This explicit current formulation combines two already documented Hartman/AMI research lines:

1. **Manifold RAID / ISR:** execution history need not be the primary persistent artifact; and
2. **TCTA/HDRP/OGSI:** future continuation can be constrained to admissible transform/trajectory structure and informed by present/previous state and trajectory-family information.

The exact consolidated wording and current schema are dated **2026-08-22**. They should not be falsely backdated. Any earlier priority argument must rely on the actual content of the April/July records and external July 10 submission, not on this later wording.

## Demonstrated vs current extension

### Demonstrated bounded prototype behavior

The recovered test line supports:

- trace-to-invariant conversion;
- raw trace removal before successful regeneration in the tested workflow;
- 4 / 4 verified bounded round trips;
- zero measured drift under the declared relation;
- hard rejection/no-seed behavior for an invalid path;
- protected-file integrity checks;
- aggregate `C_r = 2.49x`.

### Current extension requiring further direct validation

The four-case prototype does not by itself prove:

- that a dynamically generated path different from the historical path will satisfy the same behavioral-equivalence relation;
- that local admissibility always preserves reachability of a valid closure;
- that all classes admit compact invariant reconstruction records;
- that admissible branch ambiguity can always be resolved without substantial history.

The repository labels those points as research hypotheses rather than proven results.

## Related pre-existing systems

Manifold RAID is related to but distinct from:

- **TCTA** — state representation, ordered transforms/trajectories, constraints, admissible transform/trajectory space, branch preservation;
- **HDRP** — present/previous registers and local trajectory-delta / momentum primitive;
- **OGSI** — trajectory/transform-family discrimination and structural reduction;
- **MG8 family** — bounded unit/gate/state/orchestration/trace interfaces;
- **NYCH** — symbolic/contextual representation work where used by related systems.

The relationship does not make these names interchangeable and does not imply that every feature in one repository is implemented by Manifold RAID.

## Assistant contribution boundary

Prior conversations included assistant-generated names, formalizations, explanatory analogies, DARPA-oriented wording, proposed abstractions, and analysis. The chronology explicitly labels those where recoverable.

The repository should not represent assistant-generated terminology as if it were verbatim earlier user wording. Conversely, later terminology does not erase the chronology of the earlier user-originated reconstruction/storage concept.

## Third-party / collaboration boundary

This baseline intentionally excludes:

- unpublished third-party research;
- private third-party correspondence;
- NDA text;
- confidential disclosures received from collaborators;
- third-party architectures not independently present in the recovered Manifold RAID/TCTA/HDRP/OGSI line.

Conceptual overlap with another architecture does not by itself establish derivation, inventorship, ownership, or joint development.

## Evidence hierarchy

Use evidence in the following order:

1. original source files and experiment outputs where preserved;
2. dated Git commits and repository files;
3. dated proposal/submission artifacts;
4. dated architecture diagrams/posters;
5. reconstructed conversation chronology;
6. later summaries/formalizations.

Where a later summary conflicts with a primary artifact, the primary artifact controls.
