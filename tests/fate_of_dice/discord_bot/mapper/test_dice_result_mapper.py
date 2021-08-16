# pylint: disable-all
import unittest

from discord import Member

from fate_of_dice.discord_bot.mapper import crate_embed
from fate_of_dice.system.alien import ActionCheckResult, ActionCheckResultType
from fate_of_dice.system.call_of_cthulhu import SkillCheckResult, SkillCheckResultType
from fate_of_dice.system.tales_from_the_loop import OvercomeTroubleResult, OvercomeTroubleResultType
from fate_of_dice.system.universal import RollResult


class MemberMock(Member):
    display_name = 'testName'
    avatar_url = 'testAvatarUrl'

    # noinspection PyMissingConstructor
    def __init__(self):
        pass


class TestDiceResultMapper(unittest.TestCase):

    def test_roll_result(self):
        descriptions = ["testDescription1", "testDescription2"]

        result = RollResult(descriptions=descriptions)
        author = MemberMock()

        result = crate_embed(result, author, False)

        self.assertTrue('embed' in result)
        embed = result.get('embed')

        self.assertEqual(embed.colour.value, 0x4dd5d3)

        for description, field in zip(descriptions, embed.fields):
            self.assertRegex(str(field), description)

    def test_skill_check_result(self):
        descriptions = ["testDescription1", "testDescription2"]
        result_type = SkillCheckResultType.NORMAL_FAILURE

        result = SkillCheckResult(descriptions=descriptions, type=result_type)
        author = MemberMock()

        result = crate_embed(result, author, False)

        self.assertTrue('embed' in result)
        embed = result.get('embed')

        self.assertEqual(embed.title, result_type.title)
        self.assertEqual(embed.colour.value, result_type.colour)

        for description, field in zip(descriptions, embed.fields):
            self.assertRegex(str(field), description)

    def test_overcome_trouble_result(self):
        descriptions = ["testDescription1", "testDescription2"]
        result_type = OvercomeTroubleResultType.SUCCESS

        result = OvercomeTroubleResult(descriptions=descriptions, type=result_type)
        author = MemberMock()

        result = crate_embed(result, author, False)

        self.assertTrue('embed' in result)
        embed = result.get('embed')

        self.assertEqual(embed.title, result_type.title)
        self.assertEqual(embed.colour.value, result_type.colour)

        for description, field in zip(descriptions, embed.fields):
            self.assertRegex(str(field), description)

    def test_action_check_result(self):
        descriptions = ["testDescription1", "testDescription2"]
        result_type = ActionCheckResultType.FAILURE

        result = ActionCheckResult(descriptions=descriptions, type=result_type)
        author = MemberMock()

        result = crate_embed(result, author, False)

        self.assertTrue('embed' in result)
        embed = result.get('embed')

        self.assertEqual(embed.title, result_type.title)
        self.assertEqual(embed.colour.value, result_type.colour)

        for description, field in zip(descriptions, embed.fields):
            self.assertRegex(str(field), description)


if __name__ == '__main__':
    unittest.main()
