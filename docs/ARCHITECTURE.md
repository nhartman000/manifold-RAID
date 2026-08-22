# Manifold RAID Architecture

## 1. Purpose

Manifold RAID is a reference architecture for **Invariant State Representation (ISR)** plus **dynamic admissible-trajectory generation**.

The current architecture replaces full execution-history retention with a persistent invariant reconstruction record that defines:

- the starting/invariant state;
- the admissible state/transform constraints;
- the transform vocabulary or trajectory family;
- the generation/ranking policy;
- the behavioral-equivalence relation;
- the terminal closure condition.

A trajectory is then generated at runtime from admissible transforms. The generated path is a derived execution artifact, not the primary persistent artifact.

The architecture does **not** assume that every computational class admits a useful ISR or that every admissible state has a unique continuation.

---

## 2. Formal state-transition model

Let the runtime state be represented as:

`SR_t = (s_t, D_t, C_t)`

where `s_t` is the state vector, `D_t` is domain/context information, and `C_t` is the active constraint set.

Let `T_G` denote the applicable transform family or transform vocabulary.

For state `SR_t`, define the admissible transform set:

```text
A_t = A(SR_t, C_t, T_G)
    = { T in T_G | (SR_t, T, T(SR_t)) satisfies C_t }
```

Equivalently, a constraint mask `M_C` can be evaluated over candidate transforms:

```text
M_C(SR_t, T) = 1  -> admissible
M_C(SR_t, T) = 0  -> pruned
```

The runtime generator then selects or preserves one or more continuations from `A_t`.

When a unique continuation is selected:

```text
T_t = Select(A_t, Delta_t, Psi, P)
SR_{t+1} = T_t(SR_t)
```

where:

- `Delta_t` is the HDRP local trajectory delta from present/previous registers;
- `Psi` may provide OGSI/family-discrimination information;
- `P` is the declared generation/ranking/tie-breaking policy.

The generated path is:

```text
tau_hat = (SR_0, T_0, SR_1, T_1, ..., T_{n-1}, SR_n)
```

with every applied transform required to be admissible under the active constraints.

---

## 3. Persistent invariant reconstruction record

The current persistent object is not a full trace. It records the information required to regenerate an admissible path.

### 3.1 Required conceptual fields

- invariant/entry state `SR_0` or `Gamma(SR)`;
- state/container/domain constraints;
- transform-set identity or transform family `T_G`;
- admissibility/constraint-mask rules;
- closure/exit specification;
- declared equivalence relation;
- rule/version identities needed to make regeneration reproducible/auditable.

### 3.2 Optional profile fields

Depending on the computational class/profile, a record may also contain:

- HDRP register initialization or momentum seed;
- OGSI family identifier;
- resource budget;
- branch-resolution/tie-break policy;
- `rho`, margin, lock metadata;
- an optional short trajectory anchor/prefix if a particular profile requires one.

The historical July `tau_q_prefix` therefore remains a supported **profile-specific anchor**, not a universal requirement.

### 3.3 Explicit non-requirements

A valid current record does not inherently require:

- the original complete historical state sequence;
- the original complete historical transform sequence;
- the original raw `.g8son` trace;
- the previous QSON execution log;
- exact internal replay of the original path.

---

## 4. Dynamic trajectory generator

### 4.1 Initialization

Reconstruct `SR_0` from the invariant record and initialize any declared HDRP state:

```text
R_-1 <- prior/register seed if required
R_0  <- current/entry state
Delta_0 <- R_0 - R_-1
```

A profile that does not require a previous register may derive the initial delta from its own declared initialization rule.

### 4.2 Candidate generation

Enumerate or generate candidate transforms applicable to `SR_t`.

Candidate generation may come from:

- a finite transform vocabulary;
- a resolved transform family `T_G`;
- a bounded generator that proposes transforms satisfying a schema/domain contract.

Candidate generation alone does not authorize a transform.

### 4.3 Admissibility mask

Every candidate is evaluated against the declared constraint set.

A transform is admissible only if its transition record:

```text
(SR_in, T, SR_out, M)
```

satisfies the applicable constraints and preserves any required domain/container/closure-reachability conditions.

If `A_t` is empty, generation **fails closed**.

### 4.4 Branch preservation

If `|A_t| > 1`, Manifold RAID does not automatically pretend a unique trajectory exists.

The runtime may:

- preserve multiple admissible branches;
- rank branches using HDRP momentum coherence;
- use OGSI/family discrimination;
- apply a deterministic declared tie-break policy;
- defer resolution until later state information reduces the admissible set.

This branch-preservation rule is important to avoid pruning legitimate continuations merely to force determinism.

### 4.5 State transition

Once a transform is selected:

```text
SR_{t+1} = T_t(SR_t)
R_-1 <- R_0
R_0  <- SR_{t+1}
Delta_{t+1} <- R_0 - R_-1
```

The process repeats until the declared exit/closure condition is reached or a configured resource/failure boundary is hit.

---

## 5. Closure and verification

A generated trajectory is accepted only when its terminal state satisfies the declared verification relation.

Examples include:

- exact terminal state equality;
- exact observable output equality;
- declared behavioral equivalence;
- successful closure fingerprint/hash;
- another predeclared machine-checkable terminal relation.

Where a closure hash is used:

`closure_hash = SHA-256(terminal fingerprint)`

A closure mismatch is a failed generation.

Closure success verifies the declared bounded relation; it does not automatically prove broader semantic or universal correctness.

---

## 6. Runtime trace semantics

Manifold RAID may emit runtime evidence such as CIIU or QSON records:

```text
(SR_in, T, SR_out, M)
```

for each generated transition.

Those records are useful for:

- audit;
- debugging;
- experimental measurement;
- reproducibility checks;
- provenance of a particular run.

But the generated trace is **not required to become the next persistent reconstruction input**. It can be discarded after verification without invalidating the invariant record.

This is the architectural distinction between **execution evidence** and **persistent computational representation**.

---

## 7. Relationship to the historical July 2026 prototype

The historical prototype accepted an observed raw `.g8son` trace only after:

1. VERIFY — `tau in Omega(C)`;
2. CLASSIFY — unique trajectory family `T_G`;
3. creation of an invariant seed block;
4. HDRP-informed procedural regeneration;
5. terminal closure verification.

That implementation used fields including:

- `seed_coordinates`;
- `tau_q_prefix`;
- `trajectory_family`;
- `container_radius`;
- `rho` / margin / lock metadata;
- `closure_hash`.

The historical prototype is retained as evidence of **trace-to-invariant conversion and bounded regeneration**.

The current model extends the architecture by treating the saved trace/prefix as nonessential to the general case. The invariant record describes the **admissible transform space**, and the trajectory is generated forward from that representation.

---

## 8. Demonstrated bounded behavior

The recovered July prototype demonstrated, within its test scope:

- raw traces removed before successful regeneration in the tested workflow;
- 4 / 4 verified round trips;
- zero measured drift under the declared bounded relation;
- aggregate `C_r = 2.49x`;
- a negative `bad_loop.g8son` case rejected without an accepted seed;
- byte-identical protected files under SHA-256 integrity checks;
- successful test-process exit.

These are evidence for bounded **representation-based regeneration** and hard-gated rejection.

They do **not yet establish** that the current generalized dynamic generator can always discover an alternate admissible path, that all classes have sufficient ISRs, or that a unique path always exists.

---

## 9. Current research boundary

The central current claim under investigation is:

> For some identifiable computational classes, invariant state plus admissible-transform constraints can replace persisted execution history as the primary computational representation, with trajectories generated dynamically and verified at execution time.

The model is falsified for a target class if:

- no sufficient invariant record can be discovered;
- the admissible generator cannot reach an acceptable closure state;
- generated trajectories fail the declared equivalence relation;
- ambiguity cannot be resolved or safely preserved;
- storing/generating/verifying the representation eliminates the targeted resource advantage.
