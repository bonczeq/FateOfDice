from typing import Final

from discord.ext import commands

from fate_of_dice.common.resources_handler import ResourcesHandler
from fate_of_dice.system.call_of_cthulhu import check_skill
from fate_of_dice.mapper import crate_embed
from fate_of_dice.common import log, DiceException

FATE_OF_DICE_TOKEN: Final[str] = 'FATE_OF_DICE_TOKEN'
FATE_OF_DICE_PREFIX: Final[str] = 'FATE_OF_DICE_PREFIX'
FATE_OF_DICE_SIMPLE_RESULTS: Final[str] = 'FATE_OF_DICE_SIMPLE_PRESENTATION'

__BOT_TOKEN: Final[str] = ResourcesHandler.get_property(FATE_OF_DICE_TOKEN, None)
__COMMAND_PREFIXES: [str] or str = ResourcesHandler.get_property(FATE_OF_DICE_PREFIX, ['/', '\\', 'fateOfDice'])
__SIMPLE_PRESENTATION: bool = ResourcesHandler.get_property(FATE_OF_DICE_SIMPLE_RESULTS, False) in [True, 'True']

if not __BOT_TOKEN:
    raise Exception('Bot token has not be defined')
if not isinstance(__COMMAND_PREFIXES, list):
    __COMMAND_PREFIXES = __COMMAND_PREFIXES.strip('][').split(', ')

client = commands.Bot(case_insensitive=True, command_prefix=__COMMAND_PREFIXES)


@client.event
async def on_ready():
    log('Bot started')
    log(f'Bot token: {__BOT_TOKEN}')
    log(f'Bot prefixes: {" or ".join(__COMMAND_PREFIXES)}')
    log(f'Simple presentation: {__SIMPLE_PRESENTATION}')


@client.command(aliases=['s'])
async def status(ctx: commands.Context) -> None:
    status_message: str = "Bot ready"
    log(status_message)
    await ctx.send(embed=crate_embed(status_message))


@client.command(aliases=['roll', 'r', '!'])
async def common_roll(ctx: commands.Context) -> None:
    await ctx.send(embed=crate_embed("No implementation"))


@client.command(aliases=['CallOfCthulhu', 'c', '?', 't', 'test'])
async def call_of_cthulhu_test(ctx: commands.Context, *arguments: str) -> None:
    skill_result = check_skill(ctx.author.name, arguments)
    discord_result = crate_embed(ctx.message, skill_result, __SIMPLE_PRESENTATION)
    await ctx.send(**discord_result)


@client.event
async def on_command_error(ctx, error):
    original = error.original
    await ctx.send(**crate_embed(original))

    if not isinstance(original, DiceException):
        raise error


client.run(__BOT_TOKEN)
