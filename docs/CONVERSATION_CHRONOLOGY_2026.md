# Manifold RAID — Conversation-Derived Research Chronology

**Coverage window:** 2026-02-22 through 2026-08-22  
**Repository compilation date:** 2026-08-22

## Purpose

This document reconstructs the Manifold RAID concept line from prior technical conversations and associated artifacts. It intentionally distinguishes:

- **User-originated concept/result** — a concept, requirement, observation, or test result stated by Nicholas Hartman in prior discussions;
- **Assistant formulation** — terminology or formalization introduced while helping organize the user's concept;
- **Artifact-confirmed** — later files/posters/proposal material that independently preserve the technical formulation.

The distinction matters because conversation assistance can sharpen language without changing the chronology of the underlying user-originated idea.

No unpublished third-party/NDA material is incorporated here.

---

## 2026-04-25 — Original Manifold RAID storage concept

### User-originated concept

The earliest recovered Manifold RAID discussion in the six-month window described a **separate metadata-only storage technology for an IDE**.

Core points stated by the user:

- preserve metadata/reconstruction information rather than conventional complete file payloads;
- recreate data on demand, compared to a **MIDI-like live performance** in which parameters/instructions generate the output when needed;
- use **RAID-style striping** across storage and/or edge-compute media;
- move toward a **file-less filesystem** in which dynamic addresses and compact metadata strings represent reconstructable content;
- describe those compact representations as vector/Fourier-like impressions of a coherent latent-space geometry.

This April formulation predates the later ISR terminology. The central idea was already present: **persistence by reconstruction from compact structural metadata rather than by preserving the entire conventional artifact**.

### Assistant formulation at the time

The concept was organized as:

- “Metadata-Striped Generative Reconstruction Storage”;
- reconstruction instructions, model/context, deterministic seed, constraints, hashes/fidelity target;
- RAID-like striping/parity/mirroring/rebuild/checksum analogues;
- content-addressable reconstruction objects;
- a possible “Vector Addressable Reconstruction Filesystem” abstraction.

These names were organizational proposals, not evidence that the April user statements originally used the later ISR vocabulary.

---

## 2026-07-08 — Concrete encoder/decoder prototype

### User-originated implementation/result

By July 8, Manifold RAID had moved from a storage metaphor into an implemented bounded reconstruction architecture.

The recovered prototype context specifies:

```text
raw .g8son trace
    -> VERIFY
    -> CLASSIFY
    -> seed block JSON sidecar
    -> HDRP momentum decoder
    -> final verification / closure
```

The sidecar path was:

`manifold_raid_store/seed_blocks.json`

Required seed fields included:

- `seed_coordinates`
- `tau_q_prefix`
- `trajectory_family`
- `container_radius`
- `rho`
- `margin`
- lock metadata
- `closure_hash`

The encoder used two hard gates:

1. **VERIFY** — trajectory admissibility, represented as `tau ∈ Omega(C)`;
2. **CLASSIFY** — unique trajectory-family resolution `T_G`.

A failed gate produced **no accepted seed**.

The decoder used:

- HDRP dual-register momentum, `m = R0 - R-1`;
- procedural state traversal;
- A2/A3/A4 constraints;
- terminal closure matching;
- final verification.

The recovered test names include:

- `BINARY_SEARCH`
- `SIGNAL_TRAP / MXO`
- `RUNTIME_GUARD`
- `SIGNAL_TRAP variant` exemplar
- `bad_loop.g8son` rejection case

The prototype test process `test_manifold_raid.py` reported exit status `0`.

### Artifact-confirmed implementation detail

The July architecture artifact records:

- `seed_coordinates` as an entry vector in `R^8`;
- `container_radius R_c`;
- A3 non-identity (`Delta S != 0`);
- A2 container validation at **completed orbit**, rather than per-step containment;
- A4 terminating exit plus `closure_hash` match;
- the explicit warning that per-step A2 containment was ill-posed and caused false pruning before correction.

This correction is part of the technical history and should be retained because it demonstrates refinement of the verification semantics rather than a static post-hoc specification.

---

## 2026-07-08 to 2026-07-10 — Bounded round-trip results

### User-originated reported results

The bounded Manifold RAID prototype reported:

- 4 / 4 successful round trips;
- zero measured reconstruction drift;
- aggregate representation ratio `C_r = 2.49x`;
- negative `bad_loop.g8son` trajectory rejected with zero seed creation;
- SHA-256 non-destructive checks showing protected core artifacts unchanged across the test sequence.

### Artifact-confirmed benchmark table

| Benchmark | Raw trace bytes | Seed bytes | Representation ratio | Reconstruction error |
|---|---:|---:|---:|---:|
| BINARY_SEARCH | 949 | 279 | 3.40x | 0.000000 |
| SIGNAL_TRAP / MXO | 896 | 277 | 3.23x | 0.000000 |
| RUNTIME_GUARD | 880 | 284 | 3.10x | 0.000000 |
| SIGNAL_TRAP variant (exemplar) | 66 | 282 | 0.23x | 0.000000 |
| **Aggregate** | **2791** | **1122** | **2.49x** | **0.00** |

The exemplar is important because it demonstrates that the representation can be larger than the source for small traces. Manifold RAID therefore should not be characterized as universally compressive.

The research target is **representation sufficiency**, with representation efficiency treated as a possible emergent property.

---

## 2026-07-08 — ISR reframing and DARPA research direction

### Assistant formulation

During the July 8 discussion, the architecture was formalized as an **Invariant State Representation (ISR)** research program and expanded into DARPA MXO Low Resource Computing language.

The later retained name became:

**Manifold RAID — Redundant Array of Invariant Data**

The core reframing was:

> Replace preservation of complete execution history with a compact invariant computational representation from which behaviorally equivalent executable state can be procedurally regenerated and independently verified.

This terminology sharpened the existing April/July implementation line; it should not be confused with the date of origin of the underlying metadata/reconstruction concept.

---

## 2026-07-08 — DAXDA / lazy reconstruction discussion

### User-originated architectural relationship

A later July 8 discussion treated Manifold RAID as **metadata-first**:

- inspect/analyze invariant representations first;
- invoke HDRP procedural synthesis only when execution-level detail is needed;
- invoke MG8 VERIFY/CLASSIFY when the reconstruction path requires execution-level verification.

This strengthens the architectural distinction between persistent representation and regenerated execution.

---

## 2026-07-09 to 2026-07-10 — Research hypothesis formalization

Associated research artifacts state the hypothesis in a more disciplined form:

> Identifiable computational classes may admit discoverable Invariant State Representations with a minimum representation fidelity sufficient to reconstruct behaviorally equivalent executable states without preserving the original execution history.

The associated research questions became:

1. Can ISRs be algorithmically discovered for identifiable classes of computation?
2. What minimum representation fidelity `F_min` is required for behaviorally equivalent reconstruction?
3. Under what mathematical conditions is deterministic procedural regeneration possible?
4. Which computational classes admit sufficient ISRs, and which fundamentally do not?
5. What formal guarantees can be established for reconstructed executable state?

The proposal line deliberately changed the framing from “invariant compression” to **representation-centric computing**, because compression ratio is not the research claim.

---

## 2026-07-10 — DARPA-SN-26-97 Low Resource Computing RFI

### User-originated submission fact

American Milestone Inc. submitted a response to **DARPA-SN-26-97, MXO Low Resource Computing RFI** on July 10, 2026.

The submission title was:

**Invariant State Representations for Procedural Regeneration: A New Computational Abstraction for Low-Resource Autonomous Computing**

The submission presented:

- ISR as the research hypothesis;
- Manifold RAID as the experimental/reference architecture;
- compact invariant representation rather than preserved full execution history;
- hard-gated verification;
- bounded preliminary empirical results;
- falsification criteria;
- low-resource relevance in memory, energy, and bandwidth-constrained settings.

The submission was framed as a research hypothesis and experimental vehicle, not a finished universal technology.

---

## 2026-07-10 — Session-gated memory / remote reconstruction line

### User-originated implementation/result

A July 10 discussion extended the reconstruction idea into a session-gated memory system:

- Manifold seed JSON stores invariant geometry/state descriptors including Gamma, `tau_q`, `R_c`, `T_G`, and `closure_hash`;
- the local sidecar was reported at approximately 280 bytes for the referenced case;
- `restore` regenerated the tested trajectory byte-identically;
- VERIFY completed successfully;
- remote ship/recall behavior was designed to **fail closed**.

This is a useful architectural extension because it applies the same representation/reconstruction principle to memory transport and recall rather than only local trace replacement.

---

## 2026-07-10 — TCTA reduction-harness relationship

### Assistant-reported analysis requiring source verification

A July 10 assistant analysis reported additional harness results relating ISR/TCTA admissible-space reduction to:

- `SORTED_SEARCH` — reported reduction from 343 candidate paths to 4, with `R = 85.8x`, fidelity 1.000, mean 3.2 steps;
- `PREFIX_ACCUMULATION` — reported reduction from 36 to 1, with `R = 36x`, fidelity 1.000;
- degradation under H2 ablations.

These values are preserved here because they appeared in the Manifold RAID conversation line, but they are **not promoted to canonical Manifold RAID benchmark claims unless the underlying harness/output artifact is independently located and verified**.

---

## 2026-07-17 — Broader constrained-state computing relationship

### User-accepted thematic relationship

The Manifold RAID/ISR work was later grouped with TCTA, HDRP, MG8, waveform/physical-compute concepts, and related work under the broader theme:

> computation emerges from constrained state representations evolving through geometry.

Proposed umbrella terminology included “Geometric State Computing,” “Geometric Information Processing,” and “Constraint-Based Physical Computation.”

For Manifold RAID specifically, the useful relationship is:

- **TCTA** — formal state/trajectory/admissibility language;
- **HDRP** — present/previous register and trajectory-delta reconstruction primitive;
- **Manifold RAID / ISR** — compact representation + procedural regeneration + closure verification;
- **MG8 family** — bounded representation, gating, orchestration, and trace interfaces.

These are related layers, not interchangeable names.

---

## 2026-07-28 — Later proposal reuse of Manifold RAID evidence

A later MXO Pitch Day proposal referenced Manifold RAID as prior work involving:

- deterministic round-trip reconstruction tests;
- constraint metadata;
- closure hashes;
- zero-drift validation on bounded examples.

The proposal explicitly did **not** treat those software results as proof of unrelated optical-hardware claims. That distinction remains part of the evidence discipline for this repository.

---

## Current canonical interpretation

Across the recovered six-month history, the stable concept is:

1. **April:** persist reconstructive metadata/geometry rather than complete files; regenerate on demand; distribute/stripe representations.
2. **July prototype:** enforce admissibility/classification before accepting a seed; reconstruct procedurally using bounded state/trajectory information; verify terminal closure.
3. **July research framing:** define the object as an Invariant State Representation and ask which computational classes admit sufficient representations.
4. **Low-resource implication:** if a sufficient representation is smaller/cheaper to preserve than full state/history, memory/bandwidth/energy savings may emerge—but efficiency is an empirical consequence, not an axiom.

The repository should preserve all four stages rather than collapsing the origin story into the final terminology.
