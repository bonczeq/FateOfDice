import unittest

from fate_of_dice.mapper import *
from fate_of_dice.common import DiceException


class TestCreateEmbed(unittest.TestCase):

    def test_crate_embed_from_message(self):
        message = "TestTestTest"
        result = from_str(str(message))

        self.assertEqual(result.description, message)

    def test_crate_embed_from_dice_exception(self):
        message = "TestDiceException"
        result = from_exception(DiceException(message))

        field = result['embed'].fields[0]
        self.assertEqual(field.name, 'Unhandled message:')
        self.assertEqual(field.value, message)

    def test_crate_embed_from_base_exception(self):
        message = "TestBaseExceptionMessage"
        result = from_exception(BaseException(message))

        field = result['embed'].fields[0]
        self.assertEqual(field.name, 'Exception:')
        self.assertEqual(field.value, message)

    if __name__ == '__main__':
        unittest.main()
