# Manifold RAID

**Manifold RAID — Redundant Array of Invariant Data**

Manifold RAID is an experimental architecture for **invariant state representation (ISR)** and deterministic procedural reconstruction. Its purpose is not conventional compression and not archival replay of execution history. The research question is whether a bounded system can preserve a compact representation sufficient to reconstruct behaviorally equivalent state while maintaining explicit admissibility and closure checks.

## Concept lineage

The recovered six-month research history begins on **2026-04-25** with a metadata-first / file-less persistence concept: retain compact reconstructive metadata and geometry, distribute it using RAID-like redundancy/striping, and regenerate the conventional artifact on demand rather than treating the complete file as the primary stored object.

By **2026-07-08**, that direction had become a bounded encoder/decoder prototype with hard VERIFY/CLASSIFY gates, JSON seed blocks, HDRP-informed procedural reconstruction, A2/A3/A4 constraints, closure verification, negative-path rejection, and measured round-trip results.

During **2026-07-08 through 2026-07-10**, the work was formalized as an **Invariant State Representation** research program and Manifold RAID was expanded as **Redundant Array of Invariant Data**. The later ISR terminology sharpens the earlier reconstruction concept; it does not replace its chronology.

## Core thesis

Instead of storing a complete execution history, Manifold RAID stores a compact invariant representation of the state needed for reconstruction. The representation is accepted only when the source trajectory passes hard verification and classification gates.

The reference architecture is:

```text
source state / trajectory
        |
        v
  VERIFY: tau ∈ Omega(C)
        |
        v
  CLASSIFY: unique trajectory family T_G
        |
        v
 invariant seed representation
        |
        v
 JSON sidecar / invariant store
        |
        v
 HDRP dual-register momentum + procedural decoder
        |
        v
 reconstructed execution/state
        |
        v
 closure verification / closure_hash
```

Failed verification or ambiguous trajectory-family classification produces **no accepted invariant seed**.

## Canonical seed fields

The current reference representation includes:

- `seed_coordinates` / initial state vector `s0`
- `tau_q_prefix` — bounded trajectory prefix
- `trajectory_family` — resolved family `T_G`
- `container_radius` / `R_c`
- verification metadata such as `rho`, margin, and lock state where applicable
- `closure_hash` — SHA-256 of the terminal reconstruction fingerprint

The historical July prototype stored these in:

`manifold_raid_store/seed_blocks.json`

## Decoder

The procedural reconstruction line uses the Hartman Dual-Register Predictor (HDRP) concept as a momentum/state-transition primitive, including prior/current state context and bounded procedural traversal.

The historical reference implementation used an **HDRP Momentum Walk** and A2/A3/A4 verification stages. The recovered engineering record preserves the correction that A2 container validity is evaluated at **orbit completion**, not as naive per-step containment.

## Preliminary bounded results

Controlled prototype testing previously reported:

- **4 / 4** byte-identical round trips
- **0.000** measured drift on the bounded test set
- aggregate representation ratio **C_r = 2.49×**
- three larger trace ratios of approximately **3.10–3.40×**
- a small exemplar ratio of **0.23×**, demonstrating that Manifold RAID is not universally compressive
- negative `bad_loop.g8son` rejection with no accepted seed
- unchanged SHA-256 integrity for protected core files during the test sequence
- `test_manifold_raid.py` exit status `0`

These are **preliminary bounded prototype results**, not a general proof of ISR sufficiency, universal losslessness, or hardware performance.

## Research framing

The contribution under investigation is **representation sufficiency and invariant reconstruction**, not compression as an objective. The formal research line asks which computational classes admit discoverable ISRs, what minimum fidelity `F_min` is required, which classes do not admit useful ISRs, and whether discovery/regeneration/verification overhead preserves a resource advantage.

On **2026-07-10**, this research line was submitted to DARPA MXO under the Low Resource Computing RFI as:

**Invariant State Representations for Procedural Regeneration: A New Computational Abstraction for Low-Resource Autonomous Computing**

## Repository status

This repository is the canonical Manifold RAID project/provenance line. It is intentionally **private** at this stage. It documents development chronology without creating a new public-disclosure event through this repository.

The repository does not incorporate unpublished third-party research, NDA material, or later cross-architecture synthesis.

## Documentation

- [`docs/CONVERSATION_CHRONOLOGY_2026.md`](docs/CONVERSATION_CHRONOLOGY_2026.md) — recovered six-month concept chronology with user/assistant distinction
- [`docs/RESEARCH_HYPOTHESIS.md`](docs/RESEARCH_HYPOTHESIS.md) — formal ISR hypothesis, research questions, and falsification criteria
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — encoder/store/decoder/closure architecture
- [`docs/EXPERIMENTAL_RESULTS.md`](docs/EXPERIMENTAL_RESULTS.md) — bounded benchmark and integrity record
- [`docs/DARPA_MXO_LOW_RESOURCE_RFI_2026-07-10.md`](docs/DARPA_MXO_LOW_RESOURCE_RFI_2026-07-10.md) — dated MXO research baseline
- [`docs/RELATIONSHIP_TO_TCTA_HDRP_MG8.md`](docs/RELATIONSHIP_TO_TCTA_HDRP_MG8.md) — architectural relationship without collapsing distinct systems
- [`docs/PROVENANCE.md`](docs/PROVENANCE.md) — chronology, evidence hierarchy, and IP/collaboration boundary
- [`docs/ARTIFACT_INDEX.md`](docs/ARTIFACT_INDEX.md) — recovered poster/proposal artifact index
- [`spec/seed_block.schema.json`](spec/seed_block.schema.json) — reference seed-block schema
