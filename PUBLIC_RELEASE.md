# Manifold RAID: bounded public reference, September 2026

**Nicholas Hartman / American Milestone Inc.**

Manifold RAID studies whether a bounded computational class can retain an invariant reconstruction record and rules rather than retaining its historical execution path. A later execution generates admissible transitions and accepts a terminal result only after checking declared closure. Exact replay is a different requirement.

## Reproduce the current result

From the repository root with Python 3.10 or newer:

```sh
python -m unittest discover -s tests -v
python -m reference.run_example
```

The nine tests cover the original generator and an end-to-end record-driven integer profile. The example record has an initial state of 0, a target of 6, versioned rule identifiers and an eight-step bound. It generates `0 → 2 → 4 → 6` and verifies the transition chain and terminal state. A comparison path `0 → 1 → 2 → 3 → 4 → 5 → 6` is never passed to the generator. The run evaluates six candidates. The JSON record is 253 bytes in this checkout; that number can change with formatting.

The rules themselves reside in `reference/reconstruction.py`. Their source and runtime costs must be included in any storage or compute comparison. This example does **not** establish compression or a performance benefit: the generated state list is too small to support such a claim. A malicious or incomplete mask can accept wrong paths; the verifier checks against the declared rules, not against an external truth oracle. Future application profiles require independently specified behavior and adversarial tests.

The older July report states 4/4 bounded round trips and an aggregate 2.49× representation ratio, including a 0.23× case that expanded storage. The underlying historical prototype and complete reproducibility inputs are not part of this public reference package; those numbers remain reported historical observations, not independently reproduced here.

## Scope

This public release contains only the bounded reference implementation, example record, tests and this research statement. It omits private chronology, proposal material, third-party correspondence and historical artifacts. Public access grants no software license; copyright remains with Nicholas Hartman / American Milestone Inc. until a license is chosen explicitly.
