import unittest
from unittest import mock

from fate_of_dice.system.call_of_cthulhu.skill_check import check_skill, SkillCheckResultType
from fate_of_dice.common.third_party_wrapper.argument_parse import ArgumentParserException


class TestSkillCheck(unittest.TestCase):

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_default(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple([]))

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 9, (0, 90 + 1, 10): 90
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.NONE, result.type)
        self.assertEqual(99, result.value)
        self.assertEqual('90 + 9 = 99', result.description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_critical_failure(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['50']))

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 0, (0, 90 + 1, 10): 0
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.CRITICAL_FAILURE, result.type)
        self.assertEqual(100, result.value)
        self.assertEqual('0 + 0 = 100', result.description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_critical_failure_when_98(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['49']))

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 8, (0, 90 + 1, 10): 90
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.CRITICAL_FAILURE, result.type)
        self.assertEqual(98, result.value)
        self.assertEqual('90 + 8 = 98', result.description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_normal_failure(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['50']))

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 0, (0, 90 + 1, 10): 60
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.NORMAL_FAILURE, result.type)
        self.assertEqual(60, result.value)
        self.assertEqual('60 + 0 = 60', result.description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_normal_failure_with_when_98(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['50']))

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 8, (0, 90 + 1, 10): 90
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.NORMAL_FAILURE, result.type)
        self.assertEqual(98, result.value)
        self.assertEqual('90 + 8 = 98', result.description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_normal_success(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['50']))

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 1, (0, 90 + 1, 10): 30
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.NORMAL_SUCCESS, result.type)
        self.assertEqual(31, result.value)
        self.assertEqual('30 + 1 = 31', result.description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_hard_success(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['50']))

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 5, (0, 90 + 1, 10): 20
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.HARD_SUCCESS, result.type)
        self.assertEqual(25, result.value)
        self.assertEqual('20 + 5 = 25', result.description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_extremal_success(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['50']))

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 4, (0, 90 + 1, 10): 0
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.EXTREMAL_SUCCESS, result.type)
        self.assertEqual(4, result.value)
        self.assertEqual('0 + 4 = 4', result.description)

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_critical_success(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['50']))

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 1, (0, 90 + 1, 10): 0
        }[it]

        result = check_skill(user, prefix, arguments)

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.CRITICAL_SUCCESS, result.type)
        self.assertEqual(1, result.value)
        self.assertEqual('0 + 1 = 1', result.description)

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

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.NORMAL_SUCCESS, result.type)
        self.assertEqual(10, result.value)
        self.assertEqual('10 [0/10/90] + 0 = 10', result.description)

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

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.CRITICAL_FAILURE, result.type)
        self.assertEqual(100, result.value)
        self.assertEqual('0 [0/90] + 0 = 100', result.description)

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

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.NORMAL_FAILURE, result.type)
        self.assertEqual(95, result.value)
        self.assertEqual('90 [10/90] + 5 = 95', result.description)

    def test_help(self):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['-h']))
        with self.assertRaises(ArgumentParserException) as context:
            check_skill(user, prefix, arguments)

        self.assertRegex(str(context.exception), '.*usage:.*')

    def test_unsupported_arguments(self):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['Unsupported']))

        with self.assertRaises(ArgumentParserException):
            check_skill(user, prefix, arguments)


if __name__ == '__main__':
    unittest.main()
