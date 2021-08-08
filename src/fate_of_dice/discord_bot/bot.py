import logging

from discord.ext.commands import Bot
from discord_slash import SlashCommand

from fate_of_dice.common.presentation import SymbolResolver
from fate_of_dice.discord_bot.cog import BasicCog, UniversalCog, AlienCog, CallOfCthulhuCog, TalesFromTheLoopCog
from fate_of_dice.discord_bot.environment import BOT_TOKEN, COMMAND_PREFIXES, SIMPLE_PRESENTATION
from fate_of_dice.discord_bot.mapper import crate_embed
from fate_of_dice.resources.resource_handler import ResourceImageHandler

bot: Bot = Bot(case_insensitive=True, command_prefix=COMMAND_PREFIXES)
slash = SlashCommand(bot, sync_commands=True)

bot.add_cog(BasicCog(bot))
bot.add_cog(UniversalCog(bot))
bot.add_cog(AlienCog(bot))
bot.add_cog(CallOfCthulhuCog(bot))
bot.add_cog(TalesFromTheLoopCog(bot))


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
