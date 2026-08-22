"""Manifold RAID reference dynamic admissible-trajectory generator.

This module intentionally does not accept a historical execution trace as input.
It generates a trajectory from an initial invariant state, a transform vocabulary,
an admissibility predicate, a selector, and a terminal closure predicate.

It is a small reference model for the current architecture, not a claim that
arbitrary computational classes admit compact invariant reconstruction records.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Iterable, Sequence, TypeVar

State = TypeVar("State")


class GenerationFailure(RuntimeError):
    """Raised when no admissible trajectory reaches closure within the bound."""


@dataclass(frozen=True)
class Transform(Generic[State]):
    """A named state transform."""

    transform_id: str
    apply: Callable[[State], State]


@dataclass(frozen=True)
class Candidate(Generic[State]):
    """One admissible next-state candidate."""

    transform: Transform[State]
    output_state: State


@dataclass(frozen=True)
class TransitionEvidence(Generic[State]):
    """CIIU-like runtime evidence emitted by a generated transition."""

    step: int
    state_in: State
    transform_id: str
    state_out: State
    admissible: bool = True


@dataclass(frozen=True)
class GenerationResult(Generic[State]):
    """Result of one dynamically generated run.

    `states` and `transitions` are generated evidence. They are not required to
    be fed back as the persistent reconstruction substrate for a future run.
    """

    states: tuple[State, ...]
    transitions: tuple[TransitionEvidence[State], ...]

    @property
    def terminal_state(self) -> State:
        return self.states[-1]


Admissibility = Callable[[State, Transform[State], State], bool]
Closure = Callable[[State], bool]
Selector = Callable[[State | None, State, Sequence[Candidate[State]]], Candidate[State]]


def admissible_candidates(
    state: State,
    transforms: Iterable[Transform[State]],
    admissibility: Admissibility[State],
) -> tuple[Candidate[State], ...]:
    """Evaluate the constraint mask and return every admissible continuation."""

    candidates: list[Candidate[State]] = []
    for transform in transforms:
        output = transform.apply(state)
        if admissibility(state, transform, output):
            candidates.append(Candidate(transform=transform, output_state=output))
    return tuple(candidates)


def deterministic_id_selector(
    _previous: State | None,
    _current: State,
    candidates: Sequence[Candidate[State]],
) -> Candidate[State]:
    """Select by transform identity for profiles that declare this tie-break."""

    if not candidates:
        raise GenerationFailure("selector received no admissible candidates")
    return min(candidates, key=lambda candidate: candidate.transform.transform_id)


def numeric_momentum_selector(
    previous: float | int | None,
    current: float | int,
    candidates: Sequence[Candidate[float | int]],
) -> Candidate[float | int]:
    """Minimal HDRP-style numeric momentum ranking reference.

    When a prior state is available, prefer the admissible candidate whose local
    delta most closely matches the current `R0 - R_-1` delta. Stable transform
    identity is used only as the final tie-break.
    """

    if not candidates:
        raise GenerationFailure("selector received no admissible candidates")
    if previous is None:
        return min(candidates, key=lambda candidate: candidate.transform.transform_id)

    momentum = current - previous
    return min(
        candidates,
        key=lambda candidate: (
            abs((candidate.output_state - current) - momentum),
            candidate.transform.transform_id,
        ),
    )


def generate_trajectory(
    *,
    initial_state: State,
    transforms: Iterable[Transform[State]],
    admissibility: Admissibility[State],
    closure: Closure[State],
    selector: Selector[State] = deterministic_id_selector,
    max_steps: int = 128,
) -> GenerationResult[State]:
    """Generate an admissible trajectory without a stored historical trace.

    Invariants:
    - every executed transform came from the current admissible set;
    - an empty admissible set fails closed;
    - a selector cannot inject a transform that was not admitted;
    - acceptance requires the declared closure predicate;
    - the step bound prevents unbounded generation.
    """

    if max_steps < 0:
        raise ValueError("max_steps must be non-negative")

    transform_set = tuple(transforms)
    current = initial_state
    previous: State | None = None
    states: list[State] = [current]
    evidence: list[TransitionEvidence[State]] = []

    if closure(current):
        return GenerationResult(states=tuple(states), transitions=tuple(evidence))

    for step in range(max_steps):
        candidates = admissible_candidates(current, transform_set, admissibility)
        if not candidates:
            raise GenerationFailure(
                f"no admissible transforms from state at generated step {step}"
            )

        selected = selector(previous, current, candidates)
        if selected not in candidates:
            raise GenerationFailure("selector attempted a non-admissible continuation")

        next_state = selected.output_state
        evidence.append(
            TransitionEvidence(
                step=step,
                state_in=current,
                transform_id=selected.transform.transform_id,
                state_out=next_state,
            )
        )
        states.append(next_state)

        previous, current = current, next_state
        if closure(current):
            return GenerationResult(states=tuple(states), transitions=tuple(evidence))

    raise GenerationFailure(
        f"closure not reached within max_steps={max_steps}"
    )
