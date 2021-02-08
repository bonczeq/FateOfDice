from fate_of_dice.test import TestResult
from discord.embeds import Embed


def test_result_to_discord_embed(test_result: TestResult) -> Embed:
    embed = Embed()
    embed.title = test_result.test_result
    embed.colour = int(test_result.test_result_colour)
    embed.description = test_result.description
    return embed
