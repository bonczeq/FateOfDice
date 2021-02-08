import os
import traceback

from fate_of_dice.roll import RollResult
from fate_of_dice.test import TestResult
from fate_of_dice.mapper import *
from fate_of_dice.common import LazyDeveloperException

from discord.ext import commands

FATE_OF_DICE_TOKEN: str = 'FATE_OF_DICE_TOKEN'
FATE_OF_DICE_PREFIX: str = 'FATE_OF_DICE_PREFIX'

bot_token: str = os.getenv(FATE_OF_DICE_TOKEN)
command_prefix: str = os.getenv(FATE_OF_DICE_PREFIX, '/')

client = commands.Bot(case_insensitive=True, command_prefix=command_prefix)


@client.event
async def on_ready():
    print("Fate of Dice started")
    print(f'Bot token: {bot_token}')


@client.command(aliases=['s'])
async def status(ctx: commands.Context) -> None:
    status_message: str = "Bot ready"
    print(status_message)
    await ctx.send(status_message)


@client.command(aliases=['r', '!', '/'])
async def roll(ctx: commands.Context, dice: str = None) -> None:
    try:
        author: str = ctx.author.name
        result = RollResult(dice, author)
        await ctx.send("No implementation")
    except LazyDeveloperException as exp:
        await ctx.send(exp.message)
    except BaseException as exp:
        traceback.print_exc()
        await ctx.send(f'Exception: {exp}')


@client.command(aliases=['t', '?', 'check'])
async def test(ctx: commands.Context, threshold: int = None, extra_dices: str = None) -> None:
    try:
        author: str = ctx.author.name
        result = TestResult(threshold, extra_dices, author)
        await ctx.send(embed=test_result_to_discord_embed(result))
    except LazyDeveloperException as exp:
        await ctx.send(exp.message)
    except BaseException as exp:
        traceback.print_exc()
        await ctx.send(f'Exception: {exp}')


client.run(bot_token)
