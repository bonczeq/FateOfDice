import unittest
from unittest import mock

from fate_of_dice.system.universal import roll, RollResultModifier
from fate_of_dice.system.universal.exception import RollException
from fate_of_dice.common.third_party_wrapper.argument_parse import ArgumentParserException


class TestSkillCheck(unittest.TestCase):

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_default_roll(self, randrange_mock):
        (user, arguments) = ('userTest', tuple([]))

        randrange_mock.side_effect = [55]

        results = roll(user, tuple(arguments))

        randrange_mock.assert_has_calls([mock.call(1, 100 + 1, 1)])

        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.user, user)
        self.assertEqual([55], result.result)
        self.assertEqual([55], result.all_results)
        self.assertEqual(RollResultModifier.NONE, result.modifier)
        self.assertEqual('55', result.description)

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_default_dice_amount_roll(self, randrange_mock):
        (user, arguments) = ('userTest', tuple(['d8']))

        randrange_mock.side_effect = [5]

        results = roll(user, tuple(arguments))

        randrange_mock.assert_has_calls([mock.call(1, 8 + 1, 1)])

        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.user, user)
        self.assertEqual([5], result.result)
        self.assertEqual([5], result.all_results)
        self.assertEqual(RollResultModifier.NONE, result.modifier)
        self.assertEqual('5', result.description)

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_default_dice_amount_short_roll(self, randrange_mock):
        (user, arguments) = ('userTest', tuple(['8']))

        randrange_mock.side_effect = [5]

        results = roll(user, tuple(arguments))

        randrange_mock.assert_has_calls([mock.call(1, 8 + 1, 1)])

        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(user, result.user)
        self.assertEqual([5], result.result)
        self.assertEqual([5], result.all_results)
        self.assertEqual(RollResultModifier.NONE, result.modifier)
        self.assertEqual('5', result.description)

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_single_roll(self, randrange_mock):
        (user, arguments) = ('userTest', tuple(['3d8']))

        randrange_mock.side_effect = [5, 8, 1]

        results = roll(user, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1)
        ])

        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(user, result.user)
        self.assertEqual([5, 8, 1], result.result)
        self.assertEqual([5, 8, 1], result.all_results)
        self.assertEqual(RollResultModifier.NONE, result.modifier)
        self.assertEqual('[5, 8, 1]', result.description)

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_min_roll(self, randrange_mock):
        (user, arguments) = ('userTest', tuple(['3d8', '--min']))

        randrange_mock.side_effect = [5, 8, 1]

        results = roll(user, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(user, result.user)
        self.assertEqual([1], result.result)
        self.assertEqual([5, 8, 1], result.all_results)
        self.assertEqual(RollResultModifier.MIN, result.modifier)
        self.assertEqual('[5, 8, 1] => 1', result.description)

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_max_roll(self, randrange_mock):
        (user, arguments) = ('userTest', tuple(['3d8', '--max']))

        randrange_mock.side_effect = [5, 8, 1]

        results = roll(user, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(user, result.user)
        self.assertEqual([8], result.result)
        self.assertEqual([5, 8, 1], result.all_results)
        self.assertEqual(RollResultModifier.MAX, result.modifier)
        self.assertEqual('[5, 8, 1] => 8', result.description)

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_sorted_roll(self, randrange_mock):
        (user, arguments) = ('userTest', tuple(['3d8', '--sort']))

        randrange_mock.side_effect = [5, 8, 1]

        results = roll(user, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(user, result.user)
        self.assertEqual([1, 5, 8], result.result)
        self.assertEqual([5, 8, 1], result.all_results)
        self.assertEqual(RollResultModifier.SORTED, result.modifier)
        self.assertEqual('[1, 5, 8]', result.description)

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_reverse_sorted_roll(self, randrange_mock):
        (user, arguments) = ('userTest', tuple(['3d8', '--reverse']))

        randrange_mock.side_effect = [5, 8, 1]

        results = roll(user, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(user, result.user)
        self.assertEqual([8, 5, 1], result.result)
        self.assertEqual([5, 8, 1], result.all_results)
        self.assertEqual(RollResultModifier.REVERSE_SORTED, result.modifier)
        self.assertEqual('[8, 5, 1]', result.description)

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_sum_roll(self, randrange_mock):
        (user, arguments) = ('userTest', tuple(['3d8', '--sum']))

        randrange_mock.side_effect = [5, 8, 1]

        results = roll(user, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1), mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(user, result.user)
        self.assertEqual([14], result.result)
        self.assertEqual([5, 8, 1], result.all_results)
        self.assertEqual(RollResultModifier.SUM, result.modifier)
        self.assertEqual('[5, 8, 1] => 14', result.description)

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_three_rolls(self, randrange_mock):
        (user, arguments) = ('userTest', tuple(['2d100', '3d2', '1d20', '-m']))

        randrange_mock.side_effect = lambda *it: {
            (1, 100 + 1, 1): 88,
            (1, 2 + 1, 1): 2,
            (1, 20 + 1, 1): 20
        }[it]

        results = roll(user, tuple(arguments))

        self.assertEqual(len(results), 3)

        result_0 = results[0]
        self.assertEqual(user, result_0.user)
        self.assertEqual([88], result_0.result)
        self.assertEqual([88, 88], result_0.all_results)
        self.assertEqual(RollResultModifier.MIN, result_0.modifier)
        self.assertEqual('[88, 88] => 88', result_0.description)

        result_1 = results[1]
        self.assertEqual(user, result_1.user)
        self.assertEqual([2], result_1.result)
        self.assertEqual([2, 2, 2], result_1.all_results)
        self.assertEqual(RollResultModifier.MIN, result_1.modifier)
        self.assertEqual('[2, 2, 2] => 2', result_1.description)

        result_2 = results[2]
        self.assertEqual(user, result_2.user)
        self.assertEqual([20], result_2.result)
        self.assertEqual([20], result_2.all_results)
        self.assertEqual(RollResultModifier.MIN, result_2.modifier)
        self.assertEqual('20', result_2.description)

    def test_help(self):
        (user, arguments) = ('userTest', tuple(['-h']))
        with self.assertRaises(ArgumentParserException) as context:
            roll(user, arguments)

        self.assertRegex(str(context.exception), '.*usage:.*')

    def test_unsupported_arguments(self):
        (user, arguments) = ('userTest', tuple(['2h10']))
        with self.assertRaises(RollException) as context:
            roll(user, arguments)

        self.assertEqual('Unsupported dice type: 2h10', str(context.exception))

    def test_unsupported_dice_amount(self):
        (user, arguments) = ('userTest', tuple(['0d10']))
        with self.assertRaises(RollException) as context:
            roll(user, arguments)

        self.assertEqual('Dice amount must be positive, but is: 0', str(context.exception))

    def test_unsupported_modifiers(self):
        (user, arguments) = ('userTest', tuple(['1d10 -m -x']))
        with self.assertRaises(RollException) as context:
            roll(user, arguments)

        self.assertEqual('Unsupported dice type: 1d10 -m -x', str(context.exception))


if __name__ == '__main__':
    unittest.main()
