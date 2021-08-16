import unittest
from unittest import mock

from fate_of_dice.common.dice.dice_argument_parse import DiceArgumentParserException, DiceArgumentParserHelpException
from fate_of_dice.system.alien.action_check import check_action, ActionCheckResultType


class TestActionCheck(unittest.TestCase):

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_default(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple([]))

        randrange_mock.side_effect = lambda *it: {
            (1, 6 + 1, 1): 5
        }[it]

        result = check_action(user, prefix, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, ActionCheckResultType.FAILURE)
        self.assertEqual(result.base_dices, [5])
        self.assertEqual(result.stress_dices, [])
        self.assertEqual(result.success_amount, 0)
        self.assertEqual(result.stress_amount, 0)
        self.assertEqual(result.panic_value, 0)

        expected_description = (
            "Base dices: [➄]"
        )
        self.assertEqual(result.descriptions[0], expected_description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_failure(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['2']))

        randrange_mock.side_effect = [5, 1]

        result = check_action(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1)
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, ActionCheckResultType.FAILURE)
        self.assertEqual([5, 1], result.base_dices)
        self.assertEqual(result.stress_dices, [])
        self.assertEqual(result.success_amount, 0)
        self.assertEqual(result.stress_amount, 0)
        self.assertEqual(result.panic_value, 0)

        expected_description = (
            "Base dices: [➄, ➀]"
        )
        self.assertEqual(result.descriptions[0], expected_description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_success(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3']))

        randrange_mock.side_effect = [5, 6, 1]

        result = check_action(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, ActionCheckResultType.SUCCESS)
        self.assertEqual([5, 6, 1], result.base_dices)
        self.assertEqual(result.stress_dices, [])
        self.assertEqual(result.success_amount, 1)
        self.assertEqual(result.stress_amount, 0)
        self.assertEqual(result.panic_value, 0)

        expected_description = (
            "Base dices: [➄, 🗹, ➀]\n"
            "Successes: 1"
        )
        self.assertEqual(result.descriptions[0], expected_description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_successes(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3']))

        randrange_mock.side_effect = [6, 6, 1]

        result = check_action(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, ActionCheckResultType.SUCCESS)
        self.assertEqual([6, 6, 1], result.base_dices)
        self.assertEqual(result.stress_dices, [])
        self.assertEqual(result.success_amount, 2)
        self.assertEqual(result.stress_amount, 0)
        self.assertEqual(result.panic_value, 0)

        expected_description = (
            "Base dices: [🗹, 🗹, ➀]\n"
            "Successes: 2"
        )
        self.assertEqual(result.descriptions[0], expected_description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_failure_with_stress(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3', '2']))

        randrange_mock.side_effect = [5, 5, 1, 4, 2]

        result = check_action(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1)
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, ActionCheckResultType.FAILURE)
        self.assertEqual([5, 5, 1], result.base_dices)
        self.assertEqual([4, 2], result.stress_dices)
        self.assertEqual(result.success_amount, 0)
        self.assertEqual(result.stress_amount, 0)
        self.assertEqual(result.panic_value, 0)

        expected_description = (
            "Base dices: [➄, ➄, ➀]\n"
            "Stress dices: [➃, ➁]"
        )
        self.assertEqual(result.descriptions[0], expected_description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_success_with_stress(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3', '2']))

        randrange_mock.side_effect = [5, 5, 1, 6, 2]

        result = check_action(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1)
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, ActionCheckResultType.SUCCESS)
        self.assertEqual([5, 5, 1], result.base_dices)
        self.assertEqual([6, 2], result.stress_dices)
        self.assertEqual(result.success_amount, 1)
        self.assertEqual(result.stress_amount, 0)
        self.assertEqual(result.panic_value, 0)

        expected_description = (
            "Base dices: [➄, ➄, ➀]\n"
            "Stress dices: [🗹, ➁]\n"
            "Successes: 1"
        )
        self.assertEqual(result.descriptions[0], expected_description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_successes_with_stress(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3', '2']))

        randrange_mock.side_effect = [5, 6, 1, 6, 2]

        result = check_action(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1)
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, ActionCheckResultType.SUCCESS)
        self.assertEqual([5, 6, 1], result.base_dices)
        self.assertEqual([6, 2], result.stress_dices)
        self.assertEqual(result.success_amount, 2)
        self.assertEqual(result.stress_amount, 0)
        self.assertEqual(result.panic_value, 0)

        expected_description = (
            "Base dices: [➄, 🗹, ➀]\n"
            "Stress dices: [🗹, ➁]\n"
            "Successes: 2"
        )
        self.assertEqual(result.descriptions[0], expected_description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_stress_with_stress(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3', '2']))

        randrange_mock.side_effect = [5, 5, 1, 4, 1, 3]

        result = check_action(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1)
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, ActionCheckResultType.STRESS)
        self.assertEqual([5, 5, 1], result.base_dices)
        self.assertEqual([4, 1], result.stress_dices)
        self.assertEqual(result.success_amount, 0)
        self.assertEqual(result.stress_amount, 1)
        self.assertEqual(result.panic_value, 4)

        expected_description = (
            "Base dices: [➄, ➄, ➀]\n"
            "Stress dices: [➃, 🞮]\n"
            "Panic value: 1 + 3 = 4"
        )
        self.assertEqual(result.descriptions[0], expected_description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_stresses_with_stress(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3', '2']))

        randrange_mock.side_effect = [6, 6, 6, 1, 1, 3]

        result = check_action(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1)
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, ActionCheckResultType.STRESS)
        self.assertEqual([6, 6, 6], result.base_dices)
        self.assertEqual([1, 1], result.stress_dices)
        self.assertEqual(result.success_amount, 3)
        self.assertEqual(result.stress_amount, 2)
        self.assertEqual(result.panic_value, 5)

        expected_description = (
            "Base dices: [🗹, 🗹, 🗹]\n"
            "Stress dices: [🞮, 🞮]\n"
            "Successes: 3\n"
            "Panic value: 2 + 3 = 5"
        )
        self.assertEqual(result.descriptions[0], expected_description)

    def test_help(self):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['-h']))
        with self.assertRaises(DiceArgumentParserHelpException) as context:
            check_action(user, prefix, arguments)

        self.assertRegex(str(context.exception), '.*usage:.*')

    def test_unsupported_arguments(self):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['Unsupported']))

        with self.assertRaises(DiceArgumentParserException):
            check_action(user, prefix, arguments)


if __name__ == '__main__':
    unittest.main()
