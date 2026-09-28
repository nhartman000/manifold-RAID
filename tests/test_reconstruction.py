import json
import tempfile
import unittest
from pathlib import Path

from reference.dynamic_generator import GenerationFailure
from reference.reconstruction import ReconstructionRecord, reconstruct_file


EXAMPLE = Path(__file__).resolve().parents[1] / "examples/integer_record.json"


class ReconstructionTests(unittest.TestCase):
    def test_record_generates_verified_alternate_path_without_history(self):
        reconstruction = reconstruct_file(EXAMPLE)
        self.assertEqual(reconstruction.result.states, (0, 2, 4, 6))
        self.assertEqual(reconstruction.result.terminal_state, 6)
        self.assertEqual(reconstruction.candidate_evaluations, 6)
        self.assertGreater(reconstruction.record_bytes, 0)
        self.assertNotIn("history", EXAMPLE.read_text())

    def test_missing_rule_identity_rejected_before_execution(self):
        record = json.loads(EXAMPLE.read_text())
        record["mask_policy_id"] = "unknown"
        with self.assertRaises(ValueError):
            self._run(record)

    def test_historical_path_hidden_in_record_rejected(self):
        record = json.loads(EXAMPLE.read_text())
        record["historical_trace"] = [0, 1, 2, 3, 4, 5, 6]
        with self.assertRaises(ValueError):
            self._run(record)

    def test_budget_insufficient_fails_closed(self):
        record = json.loads(EXAMPLE.read_text())
        record["max_steps"] = 2
        with self.assertRaises(GenerationFailure):
            self._run(record)

    def _run(self, record):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            path.write_text(json.dumps(record))
            return reconstruct_file(path)


if __name__ == "__main__":
    unittest.main()
