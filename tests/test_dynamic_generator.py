import unittest

from reference.dynamic_generator import (
    GenerationFailure,
    Transform,
    deterministic_id_selector,
    generate_trajectory,
)


class DynamicTrajectoryGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.transforms = (
            Transform("a_plus_two", lambda state: state + 2),
            Transform("b_plus_one", lambda state: state + 1),
            Transform("z_minus_one", lambda state: state - 1),
        )

    @staticmethod
    def forward_bounded_admissibility(state, _transform, output):
        # Reference constraint mask: remain in [0, 6] and make forward progress.
        return 0 <= output <= 6 and output > state

    @staticmethod
    def target_six(state):
        return state == 6

    def test_generates_path_without_historical_trace_input(self):
        result = generate_trajectory(
            initial_state=0,
            transforms=self.transforms,
            admissibility=self.forward_bounded_admissibility,
            closure=self.target_six,
            selector=deterministic_id_selector,
            max_steps=8,
        )

        self.assertEqual(result.states, (0, 2, 4, 6))
        self.assertEqual(
            tuple(item.transform_id for item in result.transitions),
            ("a_plus_two", "a_plus_two", "a_plus_two"),
        )
        self.assertEqual(result.terminal_state, 6)

    def test_generated_path_can_differ_from_reference_history(self):
        # This sequence represents a possible historical path only for comparison.
        # It is deliberately NOT supplied to generate_trajectory().
        historical_reference = (0, 1, 2, 3, 4, 5, 6)

        result = generate_trajectory(
            initial_state=0,
            transforms=self.transforms,
            admissibility=self.forward_bounded_admissibility,
            closure=self.target_six,
            selector=deterministic_id_selector,
            max_steps=8,
        )

        self.assertNotEqual(result.states, historical_reference)
        self.assertEqual(result.states[0], historical_reference[0])
        self.assertEqual(result.terminal_state, historical_reference[-1])

    def test_non_admissible_transforms_are_never_executed(self):
        result = generate_trajectory(
            initial_state=0,
            transforms=self.transforms,
            admissibility=self.forward_bounded_admissibility,
            closure=self.target_six,
            selector=deterministic_id_selector,
            max_steps=8,
        )

        self.assertNotIn("z_minus_one", [item.transform_id for item in result.transitions])
        for transition in result.transitions:
            self.assertGreater(transition.state_out, transition.state_in)
            self.assertLessEqual(transition.state_out, 6)

    def test_fails_closed_when_no_admissible_continuation_exists(self):
        with self.assertRaises(GenerationFailure):
            generate_trajectory(
                initial_state=5,
                transforms=(Transform("plus_two", lambda state: state + 2),),
                admissibility=lambda state, _transform, output: output <= 6 and output > state,
                closure=lambda state: state == 6,
                max_steps=4,
            )

    def test_step_bound_prevents_unbounded_generation(self):
        with self.assertRaises(GenerationFailure):
            generate_trajectory(
                initial_state=0,
                transforms=(Transform("plus_one", lambda state: state + 1),),
                admissibility=lambda _state, _transform, _output: True,
                closure=lambda state: state == 100,
                max_steps=3,
            )


if __name__ == "__main__":
    unittest.main()
