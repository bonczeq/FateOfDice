import unittest
from unittest import mock

from fate_of_dice.system.alien.skill_check import check_skill, SkillCheckResultType
from fate_of_dice.common.dice.dice_argument_parse import DiceArgumentParserException, DiceArgumentParserHelpException


class TestSkillCheck(unittest.TestCase):

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_default(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple([]))

        randrange_mock.side_effect = lambda *it: {
            (1, 6 + 1, 1): 5
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.FAILURE, result.type)
        self.assertEqual([5], result.basic_dices)
        self.assertEqual([], result.stress_dices)
        self.assertEqual(0, result.success_amount)
        self.assertEqual(0, result.stress_amount)

        expected_description = (
            "Basic dices: [5]\n"
            "Result: 0 successes"
        )
        self.assertEqual(expected_description, result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_failure(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['2']))

        randrange_mock.side_effect = [5, 1]

        result = check_skill(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1)
        ])

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.FAILURE, result.type)
        self.assertEqual([5, 1], result.basic_dices)
        self.assertEqual([], result.stress_dices)
        self.assertEqual(0, result.success_amount)
        self.assertEqual(0, result.stress_amount)

        expected_description = (
            "Basic dices: [5, 1]\n"
            "Result: 0 successes"
        )
        self.assertEqual(expected_description, result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_success(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3']))

        randrange_mock.side_effect = [5, 6, 1]

        result = check_skill(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
        ])

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.SUCCESS, result.type)
        self.assertEqual([5, 6, 1], result.basic_dices)
        self.assertEqual([], result.stress_dices)
        self.assertEqual(1, result.success_amount)
        self.assertEqual(0, result.stress_amount)

        expected_description = (
            "Basic dices: [5, 6, 1]\n"
            "Result: 1 success"
        )
        self.assertEqual(expected_description, result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_successes(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3']))

        randrange_mock.side_effect = [6, 6, 1]

        result = check_skill(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
        ])

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.SUCCESS, result.type)
        self.assertEqual([6, 6, 1], result.basic_dices)
        self.assertEqual([], result.stress_dices)
        self.assertEqual(2, result.success_amount)
        self.assertEqual(0, result.stress_amount)

        expected_description = (
            "Basic dices: [6, 6, 1]\n"
            "Result: 2 successes"
        )
        self.assertEqual(expected_description, result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_failure_with_stress(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3', '2']))

        randrange_mock.side_effect = [5, 5, 1, 4, 2]

        result = check_skill(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1)
        ])

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.FAILURE, result.type)
        self.assertEqual([5, 5, 1], result.basic_dices)
        self.assertEqual([4, 2], result.stress_dices)
        self.assertEqual(0, result.success_amount)
        self.assertEqual(0, result.stress_amount)

        expected_description = (
            "Basic dices: [5, 5, 1]\n"
            "Stress dices: [4, 2]\n"
            "Result: 0 successes"
        )
        self.assertEqual(expected_description, result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_success_with_stress(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3', '2']))

        randrange_mock.side_effect = [5, 5, 1, 6, 2]

        result = check_skill(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1)
        ])

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.SUCCESS, result.type)
        self.assertEqual([5, 5, 1], result.basic_dices)
        self.assertEqual([6, 2], result.stress_dices)
        self.assertEqual(1, result.success_amount)
        self.assertEqual(0, result.stress_amount)

        expected_description = (
            "Basic dices: [5, 5, 1]\n"
            "Stress dices: [6, 2]\n"
            "Result: 1 success"
        )
        self.assertEqual(expected_description, result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_successes_with_stress(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3', '2']))

        randrange_mock.side_effect = [5, 6, 1, 6, 2]

        result = check_skill(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1)
        ])

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.SUCCESS, result.type)
        self.assertEqual([5, 6, 1], result.basic_dices)
        self.assertEqual([6, 2], result.stress_dices)
        self.assertEqual(2, result.success_amount)
        self.assertEqual(0, result.stress_amount)

        expected_description = (
            "Basic dices: [5, 6, 1]\n"
            "Stress dices: [6, 2]\n"
            "Result: 2 successes"
        )
        self.assertEqual(expected_description, result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_stress_with_stress(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3', '2']))

        randrange_mock.side_effect = [5, 6, 1, 4, 1]

        result = check_skill(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1)
        ])

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.STRESS, result.type)
        self.assertEqual([5, 6, 1], result.basic_dices)
        self.assertEqual([4, 1], result.stress_dices)
        self.assertEqual(1, result.success_amount)
        self.assertEqual(1, result.stress_amount)

        expected_description = (
            "Basic dices: [5, 6, 1]\n"
            "Stress dices: [4, 1]\n"
            "Result: 1 stress"
        )
        self.assertEqual(expected_description, result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_stresses_with_stress(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3', '2']))

        randrange_mock.side_effect = [6, 6, 6, 1, 1]

        result = check_skill(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1)
        ])

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.STRESS, result.type)
        self.assertEqual([6, 6, 6], result.basic_dices)
        self.assertEqual([1, 1], result.stress_dices)
        self.assertEqual(3, result.success_amount)
        self.assertEqual(2, result.stress_amount)

        expected_description = (
            "Basic dices: [6, 6, 6]\n"
            "Stress dices: [1, 1]\n"
            "Result: 2 stresses"
        )
        self.assertEqual(expected_description, result.descriptions[0])

    def test_help(self):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['-h']))
        with self.assertRaises(DiceArgumentParserHelpException) as context:
            check_skill(user, prefix, arguments)

        self.assertRegex(str(context.exception), '.*usage:.*')

    def test_unsupported_arguments(self):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['Unsupported']))

        with self.assertRaises(DiceArgumentParserException):
            check_skill(user, prefix, arguments)


if __name__ == '__main__':
    unittest.main()
