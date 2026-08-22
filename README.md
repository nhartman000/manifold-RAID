# Manifold RAID

**Manifold RAID — Redundant Array of Invariant Data**

Manifold RAID is an experimental architecture for **invariant state representation (ISR)** and deterministic procedural reconstruction. Its purpose is not conventional compression and not archival replay of execution history. The research question is whether a bounded system can preserve a compact representation sufficient to reconstruct behaviorally equivalent state while maintaining explicit admissibility and closure checks.

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

## Decoder

The procedural reconstruction line uses the Hartman Dual-Register Predictor (HDRP) concept as a momentum/state-transition primitive, including prior/current state context and bounded procedural traversal.

The historical reference implementation also used A2/A3/A4 traversal stages during reconstruction.

## Preliminary bounded results

Controlled prototype testing previously reported:

- **4 / 4** byte-identical round trips
- **0.000** measured drift on the bounded test set
- aggregate representation ratio **C_r = 2.49×**
- full-trace comparison approximately **3.10–3.40×**
- unchanged SHA-256 integrity for protected core files during the test sequence
- test process exit status `0`

These are **preliminary bounded prototype results**, not a general proof of ISR sufficiency, universal losslessness, or hardware performance.

## Research framing

The contribution under investigation is **representation sufficiency and invariant reconstruction**, not compression as an objective. A useful falsification condition is failure to discover a representation that reconstructs the required behavior within the defined fidelity/admissibility constraints, or resource overhead that eliminates the claimed operational advantage.

## Repository status

This repository is the canonical Manifold RAID project/provenance line. It is intentionally private at this stage. The repository does not incorporate unpublished third-party research, NDA material, or later cross-architecture synthesis.

See:

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/EXPERIMENTAL_RESULTS.md`](docs/EXPERIMENTAL_RESULTS.md)
- [`docs/PROVENANCE.md`](docs/PROVENANCE.md)
- [`spec/seed_block.schema.json`](spec/seed_block.schema.json)
