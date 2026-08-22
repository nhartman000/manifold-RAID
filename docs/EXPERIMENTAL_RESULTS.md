# Manifold RAID — Preliminary Bounded Results

## Status

These results document a prior controlled prototype exercise. They are retained as preliminary engineering evidence and must not be read as a universal proof of invariant-state reconstruction, generalized losslessness, or hardware performance.

## Reported test outcome

The bounded prototype test reported:

| Measure | Result |
|---|---:|
| Round trips | 4 / 4 PASS |
| Byte-identical reconstructions | 4 / 4 |
| Measured drift | 0.000 |
| Aggregate representation ratio `C_r` | 2.49× |
| Full-trace comparison | approximately 3.10–3.40× |
| Test process | exit 0 |

The related controlled record also reported zero false negatives for the tested bounded cases and preserved SHA-256 integrity for the protected core files involved in the experiment.

## Integrity checks retained in the prior prototype record

The historical test record identified protected files/scripts whose SHA-256 state was checked across the experiment, including the backup/restore and routing/injection support path. The purpose of that check was to demonstrate that the Manifold RAID experiment operated around the protected corpus rather than silently mutating it as part of encoding/reconstruction.

## Interpretation

The ratio `C_r` is recorded as a representation/resource observation, not as the primary research objective. The relevant question is whether the stored invariant representation is sufficient to reconstruct the required behavior under the experiment's fidelity, admissibility, and closure constraints.

A successful bounded closure test means that the tested reconstruction satisfied the experiment's defined equivalence condition. It does not imply that arbitrary programs, states, or physical processes admit equivalent invariant representations.

## Required future validation

A stronger evaluation program should separately measure:

- minimum representation fidelity `F_min`;
- closure success/failure rates across larger classes;
- false-positive and false-negative acceptance at VERIFY/CLASSIFY boundaries;
- reconstruction error and drift across repeated cycles;
- resource overhead of ISR discovery, storage, verification, and regeneration;
- behavior under perturbation/adversarial state changes;
- failure cases where no sufficient ISR exists.
