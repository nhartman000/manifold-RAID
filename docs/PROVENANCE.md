# Manifold RAID — Provenance Baseline

**Author / originator of the recovered Manifold RAID concept line:** Nicholas Hartman  
**Organization:** American Milestone Inc.  
**Repository:** `nhartman000/manifold-RAID`  
**Compilation date:** 2026-08-22

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

## July research formalization

During July 8–10 the work was formalized under the research abstraction **Invariant State Representation (ISR)** and the expanded name **Manifold RAID — Redundant Array of Invariant Data**.

The research emphasis became representation sufficiency and deterministic procedural regeneration under a defined verification relation, with representation efficiency treated as a measured consequence rather than a universal property.

## External dated research disclosure

On **2026-07-10**, American Milestone Inc. submitted a response to DARPA-SN-26-97, MXO Low Resource Computing RFI titled:

**Invariant State Representations for Procedural Regeneration: A New Computational Abstraction for Low-Resource Autonomous Computing**

That submission presented the ISR hypothesis, Manifold RAID reference architecture, preliminary bounded results, and falsification-oriented research framing.

## Related pre-existing systems

Manifold RAID is related to but distinct from:

- **TCTA** — state representation, ordered trajectories, constraints, admissible trajectory space, trajectory-family reasoning;
- **HDRP** — present/previous registers and local trajectory-delta / momentum primitive;
- **MG8 family** — bounded unit/gate/state/trace interfaces and orchestration concepts;
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
- later cross-architecture synthesis not present in the recovered pre-existing Manifold RAID line.

Conceptual overlap with another architecture does not by itself establish derivation, inventorship, ownership, or joint development.

## Evidence hierarchy

Use evidence in the following order:

1. original source files and experiment outputs where preserved;
2. dated Git commits and repository files;
3. dated proposal/submission artifacts;
4. dated architecture diagrams/posters;
5. reconstructed conversation chronology;
6. later summaries.

Where a later summary conflicts with a primary artifact, the primary artifact controls.
