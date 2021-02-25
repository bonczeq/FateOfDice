import unittest
from unittest import mock

from fate_of_dice.system.universal import roll, RollResultModifier
from fate_of_dice.system.universal.exception import RollException
from fate_of_dice.common.third_party_wrapper.argument_parse import ArgumentParserException


class TestSkillCheck(unittest.TestCase):

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_single_roll(self, randrange_mock):
        (user, arguments) = ('userTest', tuple(['3d8']))

        randrange_mock.side_effect = [5, 8, 1]

        results = roll(user, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(1, 8 + 1, 1),
            mock.call(1, 8 + 1, 1),
            mock.call(1, 8 + 1, 1),
        ])

        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result.user, user)
        self.assertEqual(result.result, [5, 8, 1])
        self.assertEqual(result.all_results, [5, 8, 1])
        self.assertEqual(result.modifier, RollResultModifier.NONE)
        self.assertEqual(result.description, '[5, 8, 1]')

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_three_rolls(self, randrange_mock):
        (user, arguments) = ('userTest', tuple(['1d100', '3d2', '1d20', '-m']))

        randrange_mock.side_effect = lambda *it: {
            (1, 100 + 1, 1): 88,
            (1, 2 + 1, 1): 2,
            (1, 20 + 1, 1): 20
        }[it]

        results = roll(user, tuple(arguments))

        self.assertEqual(len(results), 3)

        result_0 = results[0]
        self.assertEqual(result_0.user, user)
        self.assertEqual(result_0.result, [88])
        self.assertEqual(result_0.all_results, [88])
        self.assertEqual(result_0.modifier, RollResultModifier.MIN)
        self.assertEqual(result_0.description, '[88] => 88')

        result_1 = results[1]
        self.assertEqual(result_1.user, user)
        self.assertEqual(result_1.result, [2])
        self.assertEqual(result_1.all_results, [2, 2, 2])
        self.assertEqual(result_1.modifier, RollResultModifier.MIN)
        self.assertEqual(result_1.description, '[2, 2, 2] => 2')

        result_2 = results[2]
        self.assertEqual(result_2.user, user)
        self.assertEqual(result_2.result, [20])
        self.assertEqual(result_2.all_results, [20])
        self.assertEqual(result_2.modifier, RollResultModifier.MIN)
        self.assertEqual(result_2.description, '[20] => 20')

    def test_help(self):
        (user, arguments) = ('userTest', tuple(['-h']))
        with self.assertRaises(ArgumentParserException) as context:
            roll(user, arguments)

        self.assertRegex(str(context.exception), '.*usage:.*')

    def test_unsupported_arguments(self):
        (user, arguments) = ('userTest', tuple(['2h10']))
        with self.assertRaises(RollException) as context:
            roll(user, arguments)

        self.assertEqual(str(context.exception), 'Unsupported dice type: 2h10')

    def test_unsupported_dice_amount(self):
        (user, arguments) = ('userTest', tuple(['0d10']))
        with self.assertRaises(RollException) as context:
            roll(user, arguments)

        self.assertEqual(str(context.exception), 'Dice amount must be positive, but is: 0')


if __name__ == '__main__':
    unittest.main()
