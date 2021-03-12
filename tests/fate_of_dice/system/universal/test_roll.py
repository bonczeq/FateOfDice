import unittest
from unittest import mock

from fate_of_dice.common import DiceException
from fate_of_dice.common.dice import DicesModifierType, DicesFilterType
from fate_of_dice.common.dice.dice_argument_parse import DiceArgumentParserException
from fate_of_dice.system.universal import roll


class TestRoll(unittest.TestCase):

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_default_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple([]))

        randrange_mock.side_effect = [55]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([mock.call(1, 100 + 1, 1)])

        self.assertEqual(dice_result.user, user)
        self.assertEqual(dice_result.dices_modifier, DicesModifierType.NONE)
        self.assertEqual(dice_result.dices_filter, DicesFilterType.NONE)

        self.assertEqual(1, len(dice_result.descriptions))
        self.assertEqual(dice_result.descriptions[0], '55')
        self.assertEqual(dice_result.result_dices[0], [55])
        self.assertEqual(dice_result.all_dices[0], [55])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_default_dice_amount_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['d8']))

        randrange_mock.side_effect = [5]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([mock.call(1, 8 + 1, 1)])

        self.assertEqual(dice_result.user, user)
        self.assertEqual(dice_result.dices_modifier, DicesModifierType.NONE)
        self.assertEqual(dice_result.dices_filter, DicesFilterType.NONE)

        self.assertEqual(1, len(dice_result.descriptions))
        self.assertEqual(dice_result.descriptions[0], '5')
        self.assertEqual(dice_result.result_dices[0], [5])
        self.assertEqual(dice_result.all_dices[0], [5])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_default_dice_amount_short_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['8']))

        randrange_mock.side_effect = [5]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([mock.call(1, 8 + 1, 1)])

        self.assertEqual(dice_result.user, user)
        self.assertEqual(dice_result.dices_modifier, DicesModifierType.NONE)
        self.assertEqual(dice_result.dices_filter, DicesFilterType.NONE)

        self.assertEqual(1, len(dice_result.descriptions))
        self.assertEqual(dice_result.descriptions[0], '5')
        self.assertEqual(dice_result.result_dices[0], [5])
        self.assertEqual(dice_result.all_dices[0], [5])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_single_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3d8']))

        randrange_mock.side_effect = [5, 8, 1]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1)
        ])

        self.assertEqual(dice_result.user, user)
        self.assertEqual(dice_result.dices_modifier, DicesModifierType.NONE)
        self.assertEqual(dice_result.dices_filter, DicesFilterType.NONE)

        self.assertEqual(1, len(dice_result.descriptions))
        self.assertEqual('5, 8, 1', dice_result.descriptions[0])
        self.assertEqual([5, 8, 1], dice_result.result_dices[0])
        self.assertEqual([5, 8, 1], dice_result.all_dices[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_min_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3d8', '--min']))

        randrange_mock.side_effect = [5, 8, 1]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(dice_result.user, user)
        self.assertEqual(dice_result.dices_modifier, DicesModifierType.MIN)
        self.assertEqual(dice_result.dices_filter, DicesFilterType.NONE)

        self.assertEqual(1, len(dice_result.descriptions))
        self.assertEqual('[5, 8, 1] 🠖 1', dice_result.descriptions[0])
        self.assertEqual(dice_result.result_dices[0], [1])
        self.assertEqual([5, 8, 1], dice_result.all_dices[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_max_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3d8', '--max']))

        randrange_mock.side_effect = [5, 8, 1]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(dice_result.user, user)
        self.assertEqual(dice_result.dices_modifier, DicesModifierType.MAX)
        self.assertEqual(dice_result.dices_filter, DicesFilterType.NONE)

        self.assertEqual(1, len(dice_result.descriptions))
        self.assertEqual('[5, 8, 1] 🠖 8', dice_result.descriptions[0])
        self.assertEqual(dice_result.result_dices[0], [8])
        self.assertEqual([5, 8, 1], dice_result.all_dices[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_sorted_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3d8', '--sort']))

        randrange_mock.side_effect = [5, 8, 1]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(dice_result.user, user)
        self.assertEqual(dice_result.dices_modifier, DicesModifierType.SORTED)
        self.assertEqual(dice_result.dices_filter, DicesFilterType.NONE)

        self.assertEqual(1, len(dice_result.descriptions))
        self.assertEqual('[5, 8, 1] 🠖 [1, 5, 8]', dice_result.descriptions[0])
        self.assertEqual([1, 5, 8], dice_result.result_dices[0])
        self.assertEqual([5, 8, 1], dice_result.all_dices[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_reverse_sorted_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3d8', '--reverse']))

        randrange_mock.side_effect = [5, 8, 1]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(dice_result.user, user)
        self.assertEqual(dice_result.dices_modifier, DicesModifierType.REVERSE_SORTED)
        self.assertEqual(dice_result.dices_filter, DicesFilterType.NONE)

        self.assertEqual(1, len(dice_result.descriptions))
        self.assertEqual('[5, 8, 1] 🠖 [8, 5, 1]', dice_result.descriptions[0])
        self.assertEqual([8, 5, 1], dice_result.result_dices[0])
        self.assertEqual([5, 8, 1], dice_result.all_dices[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_sum_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3d8', '--sum']))

        randrange_mock.side_effect = [5, 8, 1]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(dice_result.user, user)
        self.assertEqual(dice_result.dices_modifier, DicesModifierType.SUM)
        self.assertEqual(dice_result.dices_filter, DicesFilterType.NONE)

        self.assertEqual(1, len(dice_result.descriptions))
        self.assertEqual('[5, 8, 1] 🠖 14', dice_result.descriptions[0])
        self.assertEqual(dice_result.result_dices[0], [14])
        self.assertEqual([5, 8, 1], dice_result.all_dices[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_average_floor_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3d8', '--average-floor']))

        randrange_mock.side_effect = [5, 8, 1]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(dice_result.user, user)
        self.assertEqual(dice_result.dices_modifier, DicesModifierType.AVERAGE_FLOOR)
        self.assertEqual(dice_result.dices_filter, DicesFilterType.NONE)

        self.assertEqual(1, len(dice_result.descriptions))
        self.assertEqual('[5, 8, 1] 🠖 4', dice_result.descriptions[0])
        self.assertEqual(dice_result.result_dices[0], [4])
        self.assertEqual([5, 8, 1], dice_result.all_dices[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_average_ceil_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3d8', '--average-ceil']))

        randrange_mock.side_effect = [5, 8, 1]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(dice_result.user, user)
        self.assertEqual(dice_result.dices_modifier, DicesModifierType.AVERAGE_CEIL)
        self.assertEqual(dice_result.dices_filter, DicesFilterType.NONE)
        self.assertEqual(1, len(dice_result.descriptions))
        self.assertEqual('[5, 8, 1] 🠖 5', dice_result.descriptions[0])
        self.assertEqual(dice_result.result_dices[0], [5])
        self.assertEqual([5, 8, 1], dice_result.all_dices[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_lower_than_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3d8', '--lower-than', '6']))

        randrange_mock.side_effect = [5, 8, 1]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(dice_result.user, user)
        self.assertEqual(dice_result.dices_modifier, DicesModifierType.NONE)
        self.assertEqual(dice_result.dices_filter, DicesFilterType.LOWER_THAN)

        self.assertEqual(1, len(dice_result.descriptions))
        self.assertEqual('[5, 8, 1] 🠖 [5, 1]', dice_result.descriptions[0])
        self.assertEqual([5, 1], dice_result.result_dices[0])
        self.assertEqual([5, 8, 1], dice_result.all_dices[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_upper_than_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3d8', '--upper-than', '4']))

        randrange_mock.side_effect = [5, 8, 1]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(dice_result.user, user)
        self.assertEqual(dice_result.dices_modifier, DicesModifierType.NONE)
        self.assertEqual(dice_result.dices_filter, DicesFilterType.UPPER_THAN)

        self.assertEqual(1, len(dice_result.descriptions))
        self.assertEqual('[5, 8, 1] 🠖 [5, 8]', dice_result.descriptions[0])
        self.assertEqual([5, 8], dice_result.result_dices[0])
        self.assertEqual([5, 8, 1], dice_result.all_dices[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_equal_roll(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3d8', '--equal', '8']))

        randrange_mock.side_effect = [5, 8, 8]

        dice_result = roll(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(dice_result.user, user)
        self.assertEqual(dice_result.dices_modifier, DicesModifierType.NONE)
        self.assertEqual(dice_result.dices_filter, DicesFilterType.EQUAL)

        self.assertEqual(1, len(dice_result.descriptions))
        self.assertEqual('[5, 8, 8] 🠖 [8, 8]', dice_result.descriptions[0])
        self.assertEqual([8, 8], dice_result.result_dices[0])
        self.assertEqual([5, 8, 8], dice_result.all_dices[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_three_rolls(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['2d100', '3d2', '1d20', '-m']))

        randrange_mock.side_effect = lambda *it: {
            (1, 100 + 1, 1): 88,
            (1, 2 + 1, 1): 2,
            (1, 20 + 1, 1): 20
        }[it]

        dice_result = roll(user, prefix, tuple(arguments))

        self.assertEqual(dice_result.user, user)
        self.assertEqual(dice_result.dices_modifier, DicesModifierType.MIN)
        self.assertEqual(dice_result.dices_filter, DicesFilterType.NONE)
        self.assertEqual(3, len(dice_result.descriptions))

        self.assertEqual('[88, 88] 🠖 88', dice_result.descriptions[0])
        self.assertEqual(dice_result.result_dices[0], [88])
        self.assertEqual([88, 88], dice_result.all_dices[0])

        self.assertEqual('[2, 2, 2] 🠖 2', dice_result.descriptions[1])
        self.assertEqual(dice_result.result_dices[1], [2])
        self.assertEqual([2, 2, 2], dice_result.all_dices[1])

        self.assertEqual(dice_result.descriptions[2], '20')
        self.assertEqual(dice_result.result_dices[2], [20])
        self.assertEqual(dice_result.all_dices[2], [20])

    def test_help(self):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['-h']))
        with self.assertRaises(DiceArgumentParserException) as context:
            roll(user, prefix, arguments)

        self.assertRegex(str(context.exception), '.*usage:.*')

    def test_unsupported_arguments(self):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['2h10']))
        with self.assertRaises(DiceException) as context:
            roll(user, prefix, arguments)

        self.assertEqual('Unsupported dice type: 2h10', str(context.exception))

    def test_unsupported_dice_amount(self):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['0d10']))
        with self.assertRaises(DiceException) as context:
            roll(user, prefix, arguments)

        self.assertEqual('Dice amount must be positive, but is: 0', str(context.exception))

    def test_unsupported_modifiers(self):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['1d10 -m -x']))
        with self.assertRaises(DiceException) as context:
            roll(user, prefix, arguments)

        self.assertEqual('Unsupported dice type: 1d10 -m -x', str(context.exception))


if __name__ == '__main__':
    unittest.main()
