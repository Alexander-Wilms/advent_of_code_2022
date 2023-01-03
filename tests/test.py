import importlib
import unittest


class TestAdventOfCode(unittest.TestCase):

    def test(self):
        test_cases = {
            1: ['calorie_counting', (70116, 206582)],
            2: ['rock_paper_scissors', (12586, 13193)],
            3: ['rucksack_reorganization', (7889, 2825)],
            4: ['camp_cleanup', (453, 919)],
            5: ['supply_stacks', ('WCZTHTMPS', 'BLSGJSDTS')],
            6: ['tuning_trouble', (1042, 2980)],
            7: ['no_space_left_on_device', (1350966, 6296435)],
            8: ['treetop_tree_house', (1647, 392080)],
            9: ['rope_bridge', (5878, None)],
            10: ['cathode_ray_tube', (14560, 'EKRHEPUZ')],
            11: ['monkey_in_the_middle', (90294, 18170818354)],
            # 12: ['hill_climbing_algorithm', (None, None)],
            13: ['distress_signal', (6568, 19493)],
            14: ['regolith_reservoir', (964, 32041)],
            # 15: ['beacon_exclusion_zone', (None, None)],
            # 16: ['proboscidea_volcanium', (None, None)],
            # 17: ['pyroclastic_flow', (None, None)],
            18: ['boiling_boulders', (4300, None)],
            # 19: ['not_enough_minerals', (None, None)],
            # 20: ['grove_positioning_system', (None, None)],
            21: ['monkey_math', (194058098264286, 3592056845086)],
            # 22: ['monkey_map', (None, None)],
            # 23: ['unstable_diffusion', (None, None)],
            # 24: ['blizzard_basin', (None, None)],
            # 25: ['full_of_hot_air', (None, None)]
        }
        input_file = 'input.txt'
        for day, test_case in test_cases.items():
            with self.subTest(msg=f"day_{day}"):
                futures = importlib.import_module(f"day_{day}.{test_case[0]}")
                get_solutions = getattr(futures, 'get_solutions')
                self.assertEqual(get_solutions(input_file), test_case[1], f"testing day {day}")


if __name__ == '__main__':
    unittest.main()
