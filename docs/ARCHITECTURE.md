# Manifold RAID Architecture

## 1. Purpose

Manifold RAID is a reference architecture for preserving **invariant state representations (ISR)** sufficient for bounded procedural reconstruction. It replaces full execution-history retention with a compact seed representation only when the source trajectory satisfies explicit admissibility and classification constraints.

The architecture does **not** assume that every computational process admits a useful ISR. Discoverability, sufficiency, reconstruction fidelity, and resource advantage are empirical questions.

## 2. Encoder path

### 2.1 VERIFY gate

The encoder first evaluates whether the observed trajectory is admissible under the applicable constraint set:

`tau ∈ Omega(C)`

If this gate fails, no seed is committed.

### 2.2 CLASSIFY gate

The verified trace is then assigned to a uniquely resolved trajectory family `T_G`.

If family resolution is ambiguous or otherwise fails the bounded classification requirement, no seed is committed.

### 2.3 Invariant seed

An accepted seed captures the minimum reconstruction state currently represented by:

- `seed_coordinates` (`s0`, historically represented as an 8-dimensional starting vector in the reference prototype)
- `tau_q_prefix`
- `trajectory_family`
- `container_radius` (`R_c`)
- optional verification metadata such as `rho`, margin, and lock state
- `closure_hash`

The JSON sidecar used by the historical prototype stored these invariant seed blocks in a bounded seed store.

## 3. Procedural decoder

The decoder reconstructs state procedurally rather than replaying a stored execution history.

The reference reconstruction line uses:

1. seed-coordinate initialization;
2. HDRP dual-register state/momentum context;
3. bounded A2/A3/A4 traversal stages from the historical prototype;
4. trajectory-family constraints;
5. terminal closure verification.

HDRP contributes present/previous-state context and local trajectory delta information to the reconstruction procedure. Manifold RAID does not require the decoder to reproduce the original internal execution path byte-for-byte unless a test specifically defines that as its equivalence criterion; the research target is representation-sufficient reconstruction under the stated fidelity constraints.

## 4. Closure

After reconstruction, the terminal result is fingerprinted and compared to the stored closure condition.

`closure_hash = SHA-256(terminal fingerprint)`

A closure mismatch is a failed round trip. Closure success does not by itself prove global correctness; it verifies the bounded closure condition defined by the experiment.

## 5. Data path

```text
Input state / bounded trace
        |
        v
VERIFY admissibility
        |
      fail -> reject / no seed
        |
        v
CLASSIFY trajectory family
        |
      fail -> reject / no seed
        |
        v
Invariant seed block
        |
        v
Invariant store / JSON sidecar
        |
        v
HDRP-informed procedural decoder
        |
        v
Reconstructed state / execution
        |
        v
Closure fingerprint + hash comparison
```

## 6. Integrity boundary

The historical test line preserved protected core files unchanged while the Manifold RAID store and reconstruction pipeline operated around them. The architecture therefore treats invariant-state storage and reconstruction as a separate layer rather than rewriting the protected source corpus as a side effect of encoding.

## 7. Research boundary

The central research claim is **not** "compression works." It is:

> For some bounded computational classes, there may exist invariant state representations substantially smaller than full execution histories that are sufficient for verified reconstruction of the required behavior.

The hypothesis is falsified for a target class if no representation meeting the minimum fidelity/admissibility constraints can be found, if verification cannot establish the required equivalence, or if representation/reconstruction overhead eliminates the operational advantage.
