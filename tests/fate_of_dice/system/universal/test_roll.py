import unittest
from unittest import mock

from fate_of_dice.system.universal import roll
from fate_of_dice.common.dice import DicesPresentation
from fate_of_dice.system.universal.exception import RollException
from fate_of_dice.common.third_party_wrapper.argument_parse import ArgumentParserException


class TestRoll(unittest.TestCase):

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_default_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple([]))

        randrange_mock.side_effect = [55]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([mock.call(1, 100 + 1, 1)])

        self.assertEqual(user, dice_result.user)
        self.assertEqual(DicesPresentation.NONE, dice_result.presentation)
        self.assertEqual(len(dice_result.results), 1)

        result = dice_result.results[0]
        self.assertEqual([55], result.result_dices)
        self.assertEqual([55], result.all_dices)
        self.assertEqual('55', result.description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_default_dice_amount_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['d8']))

        randrange_mock.side_effect = [5]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([mock.call(1, 8 + 1, 1)])

        self.assertEqual(user, dice_result.user)
        self.assertEqual(DicesPresentation.NONE, dice_result.presentation)
        self.assertEqual(len(dice_result.results), 1)

        result = dice_result.results[0]
        self.assertEqual([5], result.result_dices)
        self.assertEqual([5], result.all_dices)
        self.assertEqual('5', result.description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_default_dice_amount_short_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['8']))

        randrange_mock.side_effect = [5]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([mock.call(1, 8 + 1, 1)])

        self.assertEqual(user, dice_result.user)
        self.assertEqual(DicesPresentation.NONE, dice_result.presentation)
        self.assertEqual(len(dice_result.results), 1)

        result = dice_result.results[0]
        self.assertEqual([5], result.result_dices)
        self.assertEqual([5], result.all_dices)
        self.assertEqual('5', result.description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_single_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3d8']))

        randrange_mock.side_effect = [5, 8, 1]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1)
        ])

        self.assertEqual(user, dice_result.user)
        self.assertEqual(DicesPresentation.NONE, dice_result.presentation)
        self.assertEqual(len(dice_result.results), 1)

        result = dice_result.results[0]
        self.assertEqual([5, 8, 1], result.result_dices)
        self.assertEqual([5, 8, 1], result.all_dices)
        self.assertEqual('[5, 8, 1]', result.description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_min_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3d8', '--min']))

        randrange_mock.side_effect = [5, 8, 1]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(user, dice_result.user)
        self.assertEqual(DicesPresentation.MIN, dice_result.presentation)
        self.assertEqual(len(dice_result.results), 1)

        result = dice_result.results[0]
        self.assertEqual([1], result.result_dices)
        self.assertEqual([5, 8, 1], result.all_dices)
        self.assertEqual('[5, 8, 1] 🠖 1', result.description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_max_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3d8', '--max']))

        randrange_mock.side_effect = [5, 8, 1]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(user, dice_result.user)
        self.assertEqual(DicesPresentation.MAX, dice_result.presentation)
        self.assertEqual(len(dice_result.results), 1)

        result = dice_result.results[0]
        self.assertEqual([8], result.result_dices)
        self.assertEqual([5, 8, 1], result.all_dices)
        self.assertEqual('[5, 8, 1] 🠖 8', result.description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_sorted_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3d8', '--sort']))

        randrange_mock.side_effect = [5, 8, 1]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(user, dice_result.user)
        self.assertEqual(DicesPresentation.SORTED, dice_result.presentation)
        self.assertEqual(len(dice_result.results), 1)

        result = dice_result.results[0]
        self.assertEqual([1, 5, 8], result.result_dices)
        self.assertEqual([5, 8, 1], result.all_dices)
        self.assertEqual('[1, 5, 8]', result.description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_reverse_sorted_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3d8', '--reverse']))

        randrange_mock.side_effect = [5, 8, 1]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(user, dice_result.user)
        self.assertEqual(DicesPresentation.REVERSE_SORTED, dice_result.presentation)
        self.assertEqual(len(dice_result.results), 1)

        result = dice_result.results[0]
        self.assertEqual([8, 5, 1], result.result_dices)
        self.assertEqual([5, 8, 1], result.all_dices)
        self.assertEqual('[8, 5, 1]', result.description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_sum_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3d8', '--sum']))

        randrange_mock.side_effect = [5, 8, 1]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(user, dice_result.user)
        self.assertEqual(DicesPresentation.SUM, dice_result.presentation)
        self.assertEqual(len(dice_result.results), 1)

        result = dice_result.results[0]
        self.assertEqual([14], result.result_dices)
        self.assertEqual([5, 8, 1], result.all_dices)
        self.assertEqual('[5, 8, 1] 🠖 14', result.description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_three_rolls(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['2d100', '3d2', '1d20', '-m']))

        randrange_mock.side_effect = lambda *it: {
            (1, 100 + 1, 1): 88,
            (1, 2 + 1, 1): 2,
            (1, 20 + 1, 1): 20
        }[it]

        dice_result = roll(user, prefix, tuple(arguments))

        self.assertEqual(user, dice_result.user)
        self.assertEqual(DicesPresentation.MIN, dice_result.presentation)
        self.assertEqual(len(dice_result.results), 3)

        result_0 = dice_result.results[0]
        self.assertEqual([88], result_0.result_dices)
        self.assertEqual([88, 88], result_0.all_dices)
        self.assertEqual('[88, 88] 🠖 88', result_0.description)

        result_1 = dice_result.results[1]
        self.assertEqual([2], result_1.result_dices)
        self.assertEqual([2, 2, 2], result_1.all_dices)
        self.assertEqual('[2, 2, 2] 🠖 2', result_1.description)

        result_2 = dice_result.results[2]
        self.assertEqual([20], result_2.result_dices)
        self.assertEqual([20], result_2.all_dices)
        self.assertEqual('20', result_2.description)

    def test_help(self):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['-h']))
        with self.assertRaises(ArgumentParserException) as context:
            roll(user, prefix, arguments)

        self.assertRegex(str(context.exception), '.*usage:.*')

    def test_unsupported_arguments(self):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['2h10']))
        with self.assertRaises(RollException) as context:
            roll(user, prefix, arguments)

        self.assertEqual('Unsupported dice type: 2h10', str(context.exception))

    def test_unsupported_dice_amount(self):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['0d10']))
        with self.assertRaises(RollException) as context:
            roll(user, prefix, arguments)

        self.assertEqual('Dice amount must be positive, but is: 0', str(context.exception))

    def test_unsupported_modifiers(self):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['1d10 -m -x']))
        with self.assertRaises(RollException) as context:
            roll(user, prefix, arguments)

        self.assertEqual('Unsupported dice type: 1d10 -m -x', str(context.exception))


if __name__ == '__main__':
    unittest.main()
