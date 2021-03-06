import unittest
from unittest import mock

from fate_of_dice.common.dice.dice_argument_parse import DiceArgumentParserException, DiceArgumentParserHelpException
from fate_of_dice.system.tales_from_the_loop.overcome_trouble_check import overcome_trouble_check, OvercomeTroubleResultType


class TestOvercomeTroubleCheck(unittest.TestCase):

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_default(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple([]))

        randrange_mock.side_effect = lambda *it: {
            (1, 6 + 1, 1): 5
        }[it]

        result = overcome_trouble_check(user, prefix, arguments)

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, OvercomeTroubleResultType.FAILURE)
        self.assertEqual(result.dices, [5])
        self.assertEqual(result.success_amount, 0)
        self.assertEqual('Rolls: [➄]\nResult: 0 successes', result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_failure(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['2']))

        randrange_mock.side_effect = [5, 1]

        result = overcome_trouble_check(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1)
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, OvercomeTroubleResultType.FAILURE)
        self.assertEqual([5, 1], result.dices)
        self.assertEqual(result.success_amount, 0)
        self.assertEqual('Rolls: [➄, ➀]\nResult: 0 successes', result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_success(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3']))

        randrange_mock.side_effect = [5, 6, 1]

        result = overcome_trouble_check(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, OvercomeTroubleResultType.SUCCESS)
        self.assertEqual([5, 6, 1], result.dices)
        self.assertEqual(result.success_amount, 1)
        self.assertEqual('Rolls: [➄, 🗹, ➀]\nResult: 1 success', result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_successes(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3']))

        randrange_mock.side_effect = [6, 6, 1]

        result = overcome_trouble_check(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, OvercomeTroubleResultType.SUCCESS)
        self.assertEqual([6, 6, 1], result.dices)
        self.assertEqual(result.success_amount, 2)
        self.assertEqual('Rolls: [🗹, 🗹, ➀]\nResult: 2 successes', result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_failure_with_required_amount(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3', '2']))

        randrange_mock.side_effect = [5, 6, 1]

        result = overcome_trouble_check(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, OvercomeTroubleResultType.FAILURE)
        self.assertEqual([5, 6, 1], result.dices)
        self.assertEqual(result.success_amount, 1)
        self.assertEqual('Rolls: [➄, 🗹, ➀]\nResult: 1 success', result.descriptions[0])

    @mock.patch('fate_of_dice.common.dice.dice.randrange')
    def test_success_with_required_amount(self, randrange_mock):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['3', '2']))

        randrange_mock.side_effect = [6, 6, 1]

        result = overcome_trouble_check(user, prefix, arguments)

        randrange_mock.assert_has_calls([
            mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1), mock.call(1, 6 + 1, 1),
        ])

        self.assertEqual(result.user, user)
        self.assertEqual(result.type, OvercomeTroubleResultType.SUCCESS)
        self.assertEqual([6, 6, 1], result.dices)
        self.assertEqual(result.success_amount, 2)
        self.assertEqual('Rolls: [🗹, 🗹, ➀]\nResult: 2 successes', result.descriptions[0])

    def test_help(self):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['-h']))
        with self.assertRaises(DiceArgumentParserHelpException) as context:
            overcome_trouble_check(user, prefix, arguments)

        self.assertRegex(str(context.exception), '.*usage:.*')

    def test_unsupported_arguments(self):
        (user, prefix, arguments) = ('userTest', 'prefix', tuple(['Unsupported']))

        with self.assertRaises(DiceArgumentParserException):
            overcome_trouble_check(user, prefix, arguments)


if __name__ == '__main__':
    unittest.main()
