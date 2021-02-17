import unittest

from fate_of_dice.system.call_of_cthulhu.argument_parser import parse
from fate_of_dice.common.third_party_wrapper.argument_parse import ArgumentParserException


class TestDice(unittest.TestCase):

    def test_parse_help(self):
        with self.assertRaises(ArgumentParserException) as context:
            parse("unsupported value")

        self.assertRegexpMatches(str(context.exception), '.*usage:.*')

    def test_parse_unsupported(self):
        with self.assertRaises(ArgumentParserException):
            parse("unsupported value")


if __name__ == '__main__':
    unittest.main()
