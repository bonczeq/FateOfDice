import unittest
from unittest import mock

from fate_of_dice.common.dice.dice_argument_parse import DiceArgumentParserException, DiceArgumentParserHelpException
from fate_of_dice.system.call_of_cthulhu.skill_check import check_skill, SkillCheckResultType


class TestSkillCheck(unittest.TestCase):

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_default(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple([]))

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 9, (0, 90 + 1, 10): 90
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.NONE)
        self.assertEqual(result.value, 99)
        self.assertEqual('90 + 9 = 99', result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_critical_failure(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['50']))

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 0, (0, 90 + 1, 10): 0
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.CRITICAL_FAILURE)
        self.assertEqual(result.value, 100)
        self.assertEqual('0 + 0 = 100', result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_critical_failure_when_98(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['49']))

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 8, (0, 90 + 1, 10): 90
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.CRITICAL_FAILURE)
        self.assertEqual(result.value, 98)
        self.assertEqual('90 + 8 = 98', result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_normal_failure(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['50']))

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 0, (0, 90 + 1, 10): 60
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.NORMAL_FAILURE)
        self.assertEqual(result.value, 60)
        self.assertEqual('60 + 0 = 60', result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_normal_failure_with_when_98(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['50']))

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 8, (0, 90 + 1, 10): 90
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.NORMAL_FAILURE)
        self.assertEqual(result.value, 98)
        self.assertEqual('90 + 8 = 98', result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_normal_success(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['50']))

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 1, (0, 90 + 1, 10): 30
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.NORMAL_SUCCESS)
        self.assertEqual(result.value, 31)
        self.assertEqual('30 + 1 = 31', result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_hard_success(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['50']))

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 5, (0, 90 + 1, 10): 20
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.HARD_SUCCESS)
        self.assertEqual(result.value, 25)
        self.assertEqual('20 + 5 = 25', result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_extremal_success(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['50']))

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 4, (0, 90 + 1, 10): 0
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.EXTREMAL_SUCCESS)
        self.assertEqual(result.value, 4)
        self.assertEqual('0 + 4 = 4', result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_critical_success(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['50']))

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 1, (0, 90 + 1, 10): 0
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.CRITICAL_SUCCESS)
        self.assertEqual(result.value, 1)
        self.assertEqual('0 + 1 = 1', result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_bonus_dices(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple('10 -b 2'.split()))

        randrange_mock.side_effect = [0, 0, 10, 90]

        result = check_skill(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(0, 9 + 1, 1),
            mock.call(0, 90 + 1, 10),
            mock.call(0, 90 + 1, 10),
            mock.call(0, 90 + 1, 10)
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.NORMAL_SUCCESS)
        self.assertEqual(result.value, 10)
        self.assertEqual('10 [0/10/90] + 0 = 10', result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_penalty_dices(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple('10 -p'.split()))

        randrange_mock.side_effect = [0, 0, 90]

        result = check_skill(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(0, 9 + 1, 1),
            mock.call(0, 90 + 1, 10),
            mock.call(0, 90 + 1, 10)
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.CRITICAL_FAILURE)
        self.assertEqual(result.value, 100)
        self.assertEqual('0 [0/90] + 0 = 100', result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_bonus_and_penalty_dices(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple('10 --bonus --penalty 2'.split()))

        randrange_mock.side_effect = [5, 10, 90]

        result = check_skill(user, prefix, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(0, 9 + 1, 1),
            mock.call(0, 90 + 1, 10),
            mock.call(0, 90 + 1, 10)
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.NORMAL_FAILURE)
        self.assertEqual(result.value, 95)
        self.assertEqual('90 [10/90] + 5 = 95', result.descriptions[0])

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
