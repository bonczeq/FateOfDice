import unittest

from fate_of_dice.common.dice import Dice, DicesModifierType


class TestDicesModifier(unittest.TestCase):

    def test_none(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(5)]
        dices_modifier = DicesModifierType.NONE

        result = dices_modifier.modify_dices(dices)

        self.assertEqual(dices, result)

    def test_min(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_modifier = DicesModifierType.MIN

        result = dices_modifier.modify_dices(dices)

        self.assertEqual([0], result)

    def test_max(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_modifier = DicesModifierType.MAX

        result = dices_modifier.modify_dices(dices)

        self.assertEqual([9], result)

    def test_sorted(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_modifier = DicesModifierType.SORTED

        result = dices_modifier.modify_dices(dices)

        self.assertEqual([0, 4, 4, 9], result)

    def test_reverse_sorted(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_modifier = DicesModifierType.REVERSE_SORTED

        result = dices_modifier.modify_dices(dices)

        self.assertEqual([9, 4, 4, 0], result)

    def test_sum(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_modifier = DicesModifierType.SUM

        result = dices_modifier.modify_dices(dices)

        self.assertEqual([17], result)

    def test_average_floor(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_modifier = DicesModifierType.AVERAGE_FLOOR

        result = dices_modifier.modify_dices(dices)

        self.assertEqual([4], result)

    def test_average_ceil(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_modifier = DicesModifierType.AVERAGE_CEIL

        result = dices_modifier.modify_dices(dices)

        self.assertEqual([5], result)


if __name__ == '__main__':
    unittest.main()
