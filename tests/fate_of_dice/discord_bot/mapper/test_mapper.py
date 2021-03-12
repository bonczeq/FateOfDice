import unittest

from fate_of_dice.discord_bot.mapper import crate_embed


class TestMapper(unittest.TestCase):

    def test_string(self):
        description: str = "testDescription"
        result = crate_embed(description)

        self.assertTrue('embed' in result)
        embed = result.get('embed')

        self.assertEqual(embed.colour.value, 0xff00a2)
        self.assertEqual(embed.description, description)


if __name__ == '__main__':
    unittest.main()
