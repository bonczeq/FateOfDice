from fate_of_dice.common.resources_handler import get_property
from fate_of_dice.system.call_of_cthulhu import check_skill
from fate_of_dice.mapper import crate_embed
from fate_of_dice.common import log, DiceException

from typing import Final

from discord.ext import commands

FATE_OF_DICE_TOKEN: Final[str] = 'FATE_OF_DICE_TOKEN'
FATE_OF_DICE_PREFIX: Final[str] = 'FATE_OF_DICE_PREFIX'
FATE_OF_DICE_SIMPLE_RESULTS: Final[str] = 'FATE_OF_DICE_SIMPLE_PRESENTATION'

__bot_token: Final[str] = get_property(FATE_OF_DICE_TOKEN, None, 1)
__command_prefixes: [str] or str = get_property(FATE_OF_DICE_PREFIX, ['/', '\\', 'fateOfDice'])
__simple_presentation: bool = get_property(FATE_OF_DICE_SIMPLE_RESULTS, False) in [True, 'True']

if not __bot_token:
    raise Exception('Bot token has not be defined')
if not isinstance(__command_prefixes, list):
    __command_prefixes = __command_prefixes.strip('][').split(', ')

client = commands.Bot(case_insensitive=True, command_prefix=__command_prefixes)


@client.event
async def on_ready():
    log(f'Bot started')
    log(f'Bot token: {__bot_token}')
    log(f'Bot prefixes: {" or ".join(__command_prefixes)}')
    log(f'Simple presentation: {__simple_presentation}')


@client.command(aliases=['s'])
async def status(ctx: commands.Context) -> None:
    status_message: str = "Bot ready"
    log(status_message)
    await ctx.send(embed=crate_embed(status_message))


@client.command(aliases=['roll', 'r', '!'])
async def common_roll(ctx: commands.Context, dice: str = None) -> None:
    await ctx.send(embed=crate_embed("No implementation"))


@client.command(aliases=['CallOfCthulhu', 'c', '?', 't', 'test'])
async def call_of_cthulhu_test(ctx: commands.Context, *arguments: str) -> None:
    result = check_skill(ctx.author.name, arguments)
    await ctx.send(**crate_embed(ctx.message, result, __simple_presentation))


@client.event
async def on_command_error(ctx, error):
    original = error.original
    await ctx.send(**crate_embed(original))

    if not isinstance(original, DiceException):
        raise error


client.run(__bot_token)
