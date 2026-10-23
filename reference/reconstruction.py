"""Executable, bounded Manifold RAID profile using a persisted reconstruction record.

This is a deliberately small integer-state example. Rule identifiers resolve to
versioned code here; the record contains no historical execution sequence.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from reference.dynamic_generator import (
    GenerationFailure,
    GenerationResult,
    Transform,
    generate_trajectory,
)


@dataclass(frozen=True)
class ReconstructionRecord:
    version: str
    initial_state: int
    target_state: int
    transform_set_id: str
    mask_policy_id: str
    selector_id: str
    closure_id: str
    max_steps: int

    @classmethod
    def load(cls, path: str | Path) -> "ReconstructionRecord":
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(raw, dict) or set(raw) != set(cls.__dataclass_fields__):
            raise ValueError("record fields do not match the bounded profile")
        if type(raw["initial_state"]) is not int or type(raw["target_state"]) is not int:
            raise ValueError("states must be integers")
        if type(raw["max_steps"]) is not int or not 0 <= raw["max_steps"] <= 1000:
            raise ValueError("max_steps must be an integer in [0, 1000]")
        if raw["version"] != "bounded-integer-v1":
            raise ValueError("unsupported record version")
        if (raw["transform_set_id"], raw["mask_policy_id"], raw["selector_id"], raw["closure_id"]) != (
            "integer-steps-v1", "forward-bounded-v1", "id-order-v1", "target-equality-v1"
        ):
            raise ValueError("unknown or mismatched rule identity")
        if not 0 <= raw["initial_state"] <= raw["target_state"]:
            raise ValueError("invalid entry or target state")
        return cls(**raw)


@dataclass(frozen=True)
class Reconstruction:
    result: GenerationResult[int]
    candidate_evaluations: int
    record_bytes: int


def reconstruct(record: ReconstructionRecord, record_bytes: int = 0) -> Reconstruction:
    """Generate from declared rules; verify every transition independently.

    No history is accepted as an argument. Closure verifies the terminal value,
    while the independent pass verifies path continuity and policy adherence.
    """
    transforms = (
        Transform("a_plus_two", lambda state: state + 2),
        Transform("b_plus_one", lambda state: state + 1),
    )
    evaluations = 0

    def mask(state: int, _transform: Transform[int], output: int) -> bool:
        nonlocal evaluations
        evaluations += 1
        return state < output <= record.target_state

    result = generate_trajectory(
        initial_state=record.initial_state,
        transforms=transforms,
        admissibility=mask,
        closure=lambda state: state == record.target_state,
        max_steps=record.max_steps,
    )
    by_id = {transform.transform_id: transform for transform in transforms}
    if result.states[0] != record.initial_state or result.terminal_state != record.target_state:
        raise GenerationFailure("closure verification failed")
    for idx, item in enumerate(result.transitions):
        if item.state_in != result.states[idx] or item.state_out != result.states[idx + 1]:
            raise GenerationFailure("discontinuous evidence")
        if by_id[item.transform_id].apply(item.state_in) != item.state_out:
            raise GenerationFailure("transform verification failed")
        if not item.state_in < item.state_out <= record.target_state:
            raise GenerationFailure("admissibility verification failed")
    return Reconstruction(result, evaluations, record_bytes)


def reconstruct_file(path: str | Path) -> Reconstruction:
    source = Path(path)
    return reconstruct(ReconstructionRecord.load(source), source.stat().st_size)
