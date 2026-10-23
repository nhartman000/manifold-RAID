"""Print a reproducible bounded reconstruction and its measured operation count."""

import json
from pathlib import Path

from reference.reconstruction import reconstruct_file


def main() -> None:
    source = Path(__file__).resolve().parents[1] / "examples/integer_record.json"
    run = reconstruct_file(source)
    print(json.dumps({
        "states": run.result.states,
        "transform_ids": [step.transform_id for step in run.result.transitions],
        "verified_terminal_state": run.result.terminal_state,
        "candidate_evaluations": run.candidate_evaluations,
        "record_bytes": run.record_bytes,
    }, indent=2))


if __name__ == "__main__":
    main()
