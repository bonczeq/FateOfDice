import unittest
from unittest import mock

from fate_of_dice.common.dice import Dice


class TestDice(unittest.TestCase):

    def test_value(self):
        value: int = 20
        dice = Dice(value)

        self.assertEqual(dice.value, value)
        self.assertEqual(int(dice), value)
        self.assertEqual(str(dice), str(value))

    def test_operators(self):
        self.assertTrue(Dice(10) == 10)
        self.assertTrue(Dice(1) != Dice(10))

        self.assertFalse(Dice(10) < Dice(1))
        self.assertTrue(Dice(10) <= Dice(10))
        self.assertFalse(Dice(10) > Dice(100))
        self.assertTrue(Dice(10) >= Dice(1))

        self.assertTrue(Dice(10) + Dice(5) == Dice(15))
        self.assertTrue(Dice(10) - Dice(2) == Dice(8))

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_roll(self, randrange_mock):
        (result, min_value, max_value, step) = (7, 5, 10, 2)

        randrange_mock.return_value = result
        dice = Dice.roll(min_value, max_value, step)
        randrange_mock.assert_called_with(min_value, max_value + 1, step)

        self.assertEqual(dice.value, result)


if __name__ == '__main__':
    unittest.main()
