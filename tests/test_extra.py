import io
import unittest
from contextlib import redirect_stdout

import core


class TestEdgeCases(unittest.TestCase):
    def test_11_invalid_command_rejected(self):
        state = core.new_game()
        self.assertFalse(core._run_command(state, ["hack"]))
        self.assertFalse(core._run_command(state, ["mine", "V1"]))
        self.assertFalse(core._run_command(state, ["work", "abc"]))

    def test_12_empty_save_data_rejected(self):
        with self.assertRaises(ValueError):
            core.load_state("")
        with self.assertRaises(ValueError):
            core.load_state("   ")
        with self.assertRaises(ValueError):
            core.load_state("[1, 2]")

    def test_13_capacity_boundary(self):
        state = core.new_game()
        self.assertFalse(core.mine_vein(state, "V1", 101))
        self.assertTrue(core.mine_vein(state, "V1", 100))
        self.assertEqual(state["reserve"], 0)
        self.assertFalse(core.mine_vein(state, "V2", 1))
        self.assertFalse(core.blast(state, 21))
        self.assertTrue(core.blast(state, 20))
        self.assertEqual(state["explosive"], 0)
        core.cancel_blast(state, 50)
        self.assertEqual(state["explosive"], 20)

    def test_14_duplicate_and_negative_inputs(self):
        state = core.new_game()
        self.assertTrue(core.mine_vein(state, "V1", 10))
        self.assertFalse(core.mine_vein(state, "V1", 5))
        self.assertFalse(core.mine_vein(state, "", 5))
        self.assertFalse(core.mine_vein(state, "V2", -1))
        self.assertFalse(core.work(state, 0))
        self.assertFalse(core.work(state, -3))
        self.assertFalse(core.blast(state, -1))
        self.assertFalse(core.cancel_blast(state, 0))

    def test_15_no_negative_values(self):
        state = core.new_game()
        for _ in range(20):
            core.accident(state)
        self.assertEqual(state["safety"], 0)
        core.blast(state, 20)
        self.assertFalse(core.blast(state, 1))
        self.assertGreaterEqual(state["explosive"], 0)
        self.assertGreaterEqual(state["reserve"], 0)
        self.assertGreaterEqual(state["work_hours"], 0)

    def test_16_main_handles_bad_input(self):
        import core as m
        inputs = iter(["", "foo bar", "mine V1", "mine V1 10", "mine V1 10", "quit"])
        m.input = lambda prompt="": next(inputs)
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.main()
        out = buf.getvalue()
        self.assertIn("非法命令", out)
        self.assertEqual(out.count("ok"), 1)


if __name__ == "__main__":
    unittest.main()
