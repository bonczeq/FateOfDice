import unittest
from unittest import mock

from fate_of_dice.system.tales_from_the_loop.skill_check import check_skill, SkillCheckResultType
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
        self.assertEqual([5], result.dices)
        self.assertEqual(0, result.success_amount)
        self.assertEqual('[5] 🠖 0 successes', result.descriptions[0])

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
        self.assertEqual([5, 1], result.dices)
        self.assertEqual(0, result.success_amount)
        self.assertEqual('[5, 1] 🠖 0 successes', result.descriptions[0])

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
        self.assertEqual([5, 6, 1], result.dices)
        self.assertEqual(1, result.success_amount)
        self.assertEqual('[5, 6, 1] 🠖 1 success', result.descriptions[0])

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
        self.assertEqual([6, 6, 1], result.dices)
        self.assertEqual(2, result.success_amount)
        self.assertEqual('[6, 6, 1] 🠖 2 successes', result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_failure_with_required_amount(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3', '2']))

        randrange_mock.side_effect = [5, 6, 1]

        result = check_skill(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
        ])

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.FAILURE, result.type)
        self.assertEqual([5, 6, 1], result.dices)
        self.assertEqual(1, result.success_amount)
        self.assertEqual('[5, 6, 1] 🠖 1 success', result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_success_with_required_amount(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3', '2']))

        randrange_mock.side_effect = [6, 6, 1]

        result = check_skill(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
        ])

        self.assertEqual(user, result.user)
        self.assertEqual(SkillCheckResultType.SUCCESS, result.type)
        self.assertEqual([6, 6, 1], result.dices)
        self.assertEqual(2, result.success_amount)
        self.assertEqual('[6, 6, 1] 🠖 2 successes', result.descriptions[0])

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
