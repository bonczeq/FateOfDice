import unittest
from unittest import mock

from fate_of_dice.system.call_of_cthulhu.skill_check import check_skill, SkillCheckResultType


class TestSkillCheck(unittest.TestCase):

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_critical_failure(self, randrange_mock):
        (user, arguments) = ('userTest', ['50'])

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 0, (0, 90 + 1, 10): 0
        }[it]

        result = check_skill(user, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.CRITICAL_FAILURE)
        self.assertEqual(result.value, 100)
        self.assertEqual(result.description, '0 + 0 = 0')

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_critical_failure_when_98(self, randrange_mock):
        (user, arguments) = ('userTest', ['49'])

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 8, (0, 90 + 1, 10): 90
        }[it]

        result = check_skill(user, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.CRITICAL_FAILURE)
        self.assertEqual(result.value, 98)
        self.assertEqual(result.description, '90 + 8 = 98')

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_normal_failure(self, randrange_mock):
        (user, arguments) = ('userTest', ['50'])

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 0, (0, 90 + 1, 10): 60
        }[it]

        result = check_skill(user, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.NORMAL_FAILURE)
        self.assertEqual(result.value, 60)
        self.assertEqual(result.description, '60 + 0 = 60')

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_normal_failure_with_when_98(self, randrange_mock):
        (user, arguments) = ('userTest', ['50'])

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 8, (0, 90 + 1, 10): 90
        }[it]

        result = check_skill(user, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.NORMAL_FAILURE)
        self.assertEqual(result.value, 98)
        self.assertEqual(result.description, '90 + 8 = 98')

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_normal_success(self, randrange_mock):
        (user, arguments) = ('userTest', ['50'])

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 1, (0, 90 + 1, 10): 30
        }[it]

        result = check_skill(user, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.NORMAL_SUCCESS)
        self.assertEqual(result.value, 31)
        self.assertEqual(result.description, '30 + 1 = 31')

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_hard_success(self, randrange_mock):
        (user, arguments) = ('userTest', ['50'])

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 5, (0, 90 + 1, 10): 20
        }[it]

        result = check_skill(user, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.HARD_SUCCESS)
        self.assertEqual(result.value, 25)
        self.assertEqual(result.description, '20 + 5 = 25')

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_extremal_success(self, randrange_mock):
        (user, arguments) = ('userTest', ['50'])

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 4, (0, 90 + 1, 10): 0
        }[it]

        result = check_skill(user, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.EXTREMAL_SUCCESS)
        self.assertEqual(result.value, 4)
        self.assertEqual(result.description, '0 + 4 = 4')

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_critical_success(self, randrange_mock):
        (user, arguments) = ('userTest', ['50'])

        randrange_mock.side_effect = lambda *it: {
            (0, 9 + 1, 1): 1, (0, 90 + 1, 10): 0
        }[it]

        result = check_skill(user, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.CRITICAL_SUCCESS)
        self.assertEqual(result.value, 1)
        self.assertEqual(result.description, '0 + 1 = 1')

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_bonus_dices(self, randrange_mock):
        (user, arguments) = ('userTest', '10 -b 2'.split())

        randrange_mock.side_effect = [0, 0, 10, 90]

        result = check_skill(user, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(0, 9 + 1, 1),
            mock.call(0, 90 + 1, 10),
            mock.call(0, 90 + 1, 10),
            mock.call(0, 90 + 1, 10)
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.NORMAL_SUCCESS)
        self.assertEqual(result.value, 10)
        self.assertEqual(result.description, '10 [0/10/90] + 0 = 10')

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_penalty_dices(self, randrange_mock):
        (user, arguments) = ('userTest', '10 -p'.split())

        randrange_mock.side_effect = [0, 0, 90]

        result = check_skill(user, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(0, 9 + 1, 1),
            mock.call(0, 90 + 1, 10),
            mock.call(0, 90 + 1, 10)
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.CRITICAL_FAILURE)
        self.assertEqual(result.value, 100)
        self.assertEqual(result.description, '0 [0/90] + 0 = 0')

    @mock.patch('fate_of_dice.common.dice.randrange')
    def test_bonus_and_penalty_dices(self, randrange_mock):
        (user, arguments) = ('userTest', '10 --bonus --penalty 2'.split())

        randrange_mock.side_effect = [5, 10, 90]

        result = check_skill(user, tuple(arguments))

        randrange_mock.assert_has_calls([
            mock.call(0, 9 + 1, 1),
            mock.call(0, 90 + 1, 10),
            mock.call(0, 90 + 1, 10)
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, SkillCheckResultType.NORMAL_FAILURE)
        self.assertEqual(result.value, 95)
        self.assertEqual(result.description, '90 [10/90] + 5 = 95')


if __name__ == '__main__':
    unittest.main()
