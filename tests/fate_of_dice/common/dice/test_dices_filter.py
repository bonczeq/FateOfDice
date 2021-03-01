import unittest

from fate_of_dice.common.dice import Dice, DicesFilterType


class TestDicesFilter(unittest.TestCase):

    def test_none(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(5)]
        dices_filter = DicesFilterType.NONE

        result = dices_filter.filter_dices(dices, None)

        self.assertEqual(dices, result)

    def test_equal(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_filter = DicesFilterType.EQUAL

        result = dices_filter.filter_dices(dices, None)

        self.assertEqual(dices, result)

    def test_equal_to_value(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(4)]
        dices_filter = DicesFilterType.EQUAL

        result = dices_filter.filter_dices(dices, 4)

        self.assertEqual([4, 4], result)

    def test_upper_than(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(5)]
        dices_filter = DicesFilterType.UPPER_THAN

        result = dices_filter.filter_dices(dices, None)

        self.assertEqual(dices, result)

    def test_upper_than_limit(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(5)]
        dices_filter = DicesFilterType.UPPER_THAN

        result = dices_filter.filter_dices(dices, 4)

        self.assertEqual([9, 5], result)

    def test_lower_than(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(5)]
        dices_filter = DicesFilterType.LOWER_THAN

        result = dices_filter.filter_dices(dices, None)

        self.assertEqual(dices, result)

    def test_lower_than_limit(self):
        dices = [Dice(4), Dice(9), Dice(0), Dice(5)]
        dices_filter = DicesFilterType.LOWER_THAN

        result = dices_filter.filter_dices(dices, 5)

        self.assertEqual([4, 0], result)


if __name__ == '__main__':
    unittest.main()
