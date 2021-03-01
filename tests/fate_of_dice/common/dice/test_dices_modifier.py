import unittest

from fate_of_dice.common.dice import Dice, DicesModifier


class TestDicesModifier(unittest.TestCase):

    def test_none(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(5)]
        dices_modifier = DicesModifier.NONE

        result = dices_modifier.modify_dices(dices)

        self.assertEqual(dices, result)

    def test_min(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_modifier = DicesModifier.MIN

        result = dices_modifier.modify_dices(dices)

        self.assertEqual([0], result)

    def test_max(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_modifier = DicesModifier.MAX

        result = dices_modifier.modify_dices(dices)

        self.assertEqual([9], result)

    def test_sorted(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_modifier = DicesModifier.SORTED

        result = dices_modifier.modify_dices(dices)

        self.assertEqual([0, 4, 4, 9], result)

    def test_reverse_sorted(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_modifier = DicesModifier.REVERSE_SORTED

        result = dices_modifier.modify_dices(dices)

        self.assertEqual([9, 4, 4, 0], result)

    def test_sum(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_modifier = DicesModifier.SUM

        result = dices_modifier.modify_dices(dices)

        self.assertEqual([17], result)

    def test_average_floor(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_modifier = DicesModifier.AVERAGE_FLOOR

        result = dices_modifier.modify_dices(dices)

        self.assertEqual([4], result)

    def test_average_ceil(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_modifier = DicesModifier.AVERAGE_CEIL

        result = dices_modifier.modify_dices(dices)

        self.assertEqual([5], result)


if __name__ == '__main__':
    unittest.main()
