import logging
from typing import Final, Iterable

from discord.ext.commands import Cog, Bot, Context, command

from fate_of_dice.common.presentation import SymbolResolver
from fate_of_dice.discord_bot.environment import BOT_TOKEN, COMMAND_PREFIXES, SIMPLE_PRESENTATION
from fate_of_dice.discord_bot.mapper import crate_embed
from fate_of_dice.resources.resource_handler import ResourceImageHandler
from fate_of_dice.system import DiceResult
from fate_of_dice.system.alien import check_action
from fate_of_dice.system.call_of_cthulhu import check_skill
from fate_of_dice.system.tales_from_the_loop import overcome_trouble_check
from fate_of_dice.system.universal import roll


class _Basic(Cog, name='Basic commands'):

    @command(help='Information about bot')
    async def info(self, ctx: Context) -> None:
        logging.info('Received info command')
        message: str = (
            'Author: **bonczeq**\n'
            'Please check [GitHub project page](https://github.com/bonczeq/FateOfDice/blob/master/README.md)'
        )
        discord_result = crate_embed(message)
        await ctx.send(**discord_result)


def _aliases_to_name(aliases: [str]) -> str:
    return " | ".join(aliases)


class _Rolls(Cog, name='Roll commands'):
    __UNIVERSAL_ROLL_ALIASES: Final[Iterable[str]] = ['r', '!', 'roll']
    __CALL_OF_CTHULHU_ALIASES: Final[Iterable[str]] = ['c', '?', 'CoC', 'CallOfCthulhu']
    __TALES_FROM_THE_LOOP_ALIASES: Final[Iterable[str]] = ['t', 'TftL', 'TalesFromTheLoop']
    __ALIEN_ALIASES: Final[Iterable[str]] = ['a', 'Alien']

    @command(aliases=__UNIVERSAL_ROLL_ALIASES, name=_aliases_to_name(__UNIVERSAL_ROLL_ALIASES),
             help='Roll the defined dices')
    async def universal_roll(self, ctx: Context, *arguments: str) -> None:
        command_prefix: str = ctx.prefix + ctx.invoked_with
        roll_result = roll(ctx.message.author.display_name, command_prefix, arguments)
        discord_result = crate_embed(roll_result, ctx.message, SIMPLE_PRESENTATION)
        await self._send_message(ctx, discord_result, roll_result)

    @command(aliases=__CALL_OF_CTHULHU_ALIASES, name=_aliases_to_name(__CALL_OF_CTHULHU_ALIASES),
             help='Check Call of Cthulhu RPG skill')
    async def call_of_cthulhu_check(self, ctx: Context, *arguments: str) -> None:
        command_prefix: str = ctx.prefix + ctx.invoked_with
        skill_result = check_skill(ctx.message.author.display_name, command_prefix, arguments)
        discord_result = crate_embed(skill_result, ctx.message, SIMPLE_PRESENTATION)
        await self._send_message(ctx, discord_result, skill_result)

    @command(aliases=__TALES_FROM_THE_LOOP_ALIASES, name=_aliases_to_name(__TALES_FROM_THE_LOOP_ALIASES),
             help='Check overcoming Tales From The Loop RPG troubles')
    async def tales_from_the_loop_check(self, ctx: Context, *arguments: str) -> None:
        command_prefix: str = ctx.prefix + ctx.invoked_with
        roll_result = overcome_trouble_check(ctx.message.author.display_name, command_prefix, arguments)
        discord_result = crate_embed(roll_result, ctx.message, SIMPLE_PRESENTATION)
        await self._send_message(ctx, discord_result, roll_result)

    @command(aliases=__ALIEN_ALIASES, name=_aliases_to_name(__ALIEN_ALIASES),
             help='Check Alien RPG skill')
    async def alien_check(self, ctx: Context, *arguments: str) -> None:
        command_prefix: str = ctx.prefix + ctx.invoked_with
        check_result = check_action(ctx.message.author.display_name, command_prefix, arguments)
        discord_result = crate_embed(check_result, ctx.message, SIMPLE_PRESENTATION)
        await self._send_message(ctx, discord_result, check_result)

    @classmethod
    async def _send_message(cls, ctx: Context, discord_result, dice_result: DiceResult) -> None:
        await ctx.send(**discord_result)

        if dice_result.priv_request:
            await ctx.author.send(**discord_result)


bot: Bot = Bot(case_insensitive=True, command_prefix=COMMAND_PREFIXES)
bot.add_cog(_Basic())
bot.add_cog(_Rolls())


@bot.event
async def on_ready():
    logging.info('Bot ready')
    logging.info('Bot token: %s', BOT_TOKEN)
    logging.info('Bot prefixes: %s', ' or '.join(COMMAND_PREFIXES))
    logging.info('Simple presentation: %s', SIMPLE_PRESENTATION)
    logging.info('Purely ascii descriptions: %s', SymbolResolver.PURELY_ASCII)
    logging.info('Icons from url: %s', ResourceImageHandler.URL_ICONS or 'Default')


@bot.event
async def on_command_error(ctx, error):
    original = error
    if hasattr(error, 'original'):
        original = error.original
    await ctx.send(**crate_embed(original))


def run_bot():
    if BOT_TOKEN:
        bot.run(BOT_TOKEN)
    else:
        raise Exception('Bot token has not be defined')
