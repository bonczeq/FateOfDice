import unittest

from fate_of_dice.common.dice import Dice, DicesPresentation


class TestDicesPresentation(unittest.TestCase):

    def test_none(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_presentation = DicesPresentation.NONE

        result = dices_presentation.modify_dices(dices)

        self.assertEqual(dices, result)

    def test_min(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_presentation = DicesPresentation.MIN

        result = dices_presentation.modify_dices(dices)

        self.assertEqual([0], result)

    def test_max(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_presentation = DicesPresentation.MAX

        result = dices_presentation.modify_dices(dices)

        self.assertEqual([9], result)

    def test_sorted(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_presentation = DicesPresentation.SORTED

        result = dices_presentation.modify_dices(dices)

        self.assertEqual([0, 4, 4, 9], result)

    def test_reverse_sorted(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_presentation = DicesPresentation.REVERSE_SORTED

        result = dices_presentation.modify_dices(dices)

        self.assertEqual([9, 4, 4, 0], result)

    def test_sum(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_presentation = DicesPresentation.SUM

        result = dices_presentation.modify_dices(dices)

        self.assertEqual([17], result)


if __name__ == '__main__':
    unittest.main()