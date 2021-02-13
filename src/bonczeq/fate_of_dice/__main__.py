from bonczeq.fate_of_dice.common.util import get_property
from bonczeq.fate_of_dice.system.call_of_cthulhu import check_skill
from bonczeq.fate_of_dice.mapper import crate_embed
from bonczeq.fate_of_dice.common import log, DiceException

from discord.ext import commands

FATE_OF_DICE_TOKEN: str = 'FATE_OF_DICE_TOKEN'
FATE_OF_DICE_PREFIX: str = 'FATE_OF_DICE_PREFIX'

bot_token: str = get_property(FATE_OF_DICE_TOKEN, None, 1)
command_prefix: str = get_property(FATE_OF_DICE_PREFIX, '/', 2)

client = commands.Bot(case_insensitive=True, command_prefix=command_prefix)


@client.event
async def on_ready():
    log(f'Bot started with token: {bot_token}')


@client.command(aliases=['s'])
async def status(ctx: commands.Context) -> None:
    status_message: str = "Bot ready"
    log(status_message)
    await ctx.send(embed=crate_embed(status_message))


@client.command(aliases=['!', 'r', '/'])
async def roll(ctx: commands.Context, dice: str = None) -> None:
    await ctx.send(embed=crate_embed("No implementation"))


@client.command(aliases=['Call of Cthulhu', 'CoC', '?', 't', 'test'])
async def call_of_cthulhu_test(ctx: commands.Context, *arguments: str) -> None:
    result = check_skill(ctx.author.name, arguments)
    await ctx.send(embed=crate_embed(result))


@client.event
async def on_command_error(ctx, error):
    original = error.original
    await ctx.send(embed=crate_embed(original))

    if not isinstance(original, DiceException):
        raise error


client.run(bot_token)
