import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_no_duplicate_vein(self):
        state = core.new_game()
        self.assertTrue(core.mine_vein(state, "V1", 10))
        self.assertFalse(core.mine_vein(state, "V1", 10))

    def test_02_no_work_when_collapsed(self):
        state = core.new_game()
        state["collapsed"] = True
        result = core.work(state, 5)
        self.assertFalse(result)

    def test_03_reserve_by_volume(self):
        state = core.new_game()
        core.mine_vein(state, "V1", 10)
        self.assertEqual(core.reserve_volume(state, "V1"), 10)

    def test_04_cancel_blast_refunds(self):
        state = core.new_game()
        core.blast(state, 5)
        core.cancel_blast(state, 5)
        self.assertEqual(state["explosive"], 20)

    def test_05_no_work_without_ventilation(self):
        state = core.new_game()
        state["ventilation"] = False
        result = core.work(state, 5)
        self.assertFalse(result)

    def test_06_accident_once(self):
        state = core.new_game()
        core.accident(state)
        self.assertEqual(state["safety"], 90)

    def test_07_no_work_without_support(self):
        state = core.new_game()
        state["supported"] = False
        result = core.support(state)
        self.assertFalse(result)

    def test_08_load_preserves_shift(self):
        state = core.new_game()
        state["shift_id"] = 3
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["shift_id"], 3)


if __name__ == "__main__":
    unittest.main()
