import unittest

from fate_of_dice.common.exception import DiceException
from fate_of_dice.discord_bot.mapper import crate_embed


class TestExceptionMapper(unittest.TestCase):

    def test_dice_exception(self):
        error = DiceException("testDescription")
        result = crate_embed(error)

        self.assertTrue('embed' in result)
        embed = result.get('embed')

        self.assertEqual(embed.colour.value, 0xae6229)
        self.assertEqual(embed.description, str(error))

    def test_exception(self):
        error = Exception("testDescription")
        result = crate_embed(error)

        self.assertTrue('embed' in result)
        embed = result.get('embed')

        self.assertEqual(embed.title, 'Error')
        self.assertEqual(embed.description, str(error))


if __name__ == '__main__':
    unittest.main()
