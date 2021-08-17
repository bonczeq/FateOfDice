import logging
from threading import Thread

from discord import Member, TextChannel, Intents
from discord.ext.commands import Bot
from discord_slash import SlashCommand

from fate_of_dice.common import DiceException
from fate_of_dice.common.presentation import SymbolResolver
from fate_of_dice.discord_bot.cog import BasicCog, UniversalCog, AlienCog, CallOfCthulhuCog, TalesFromTheLoopCog
from fate_of_dice.discord_bot.environment import BOT_TOKEN, COMMAND_PREFIXES, SIMPLE_PRESENTATION
from fate_of_dice.discord_bot.mapper import crate_embed
from fate_of_dice.resources.resource_handler import ResourceImageHandler
from fate_of_dice.system import DiceResult

intents = Intents.default()
intents.members = True

bot: Bot = Bot(case_insensitive=True, command_prefix=COMMAND_PREFIXES, intents=intents)
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
async def on_slash_command_error(ctx, error):
    original = error
    if hasattr(error, 'original'):
        original = error.original
    await ctx.send(**crate_embed(original))


@bot.event
async def on_command_error(ctx, error):
    original = error
    if hasattr(error, 'original'):
        original = error.original
    await ctx.send(**crate_embed(original))


class DiscordBot:

    def __init__(self) -> None:
        self.bot: Bot = bot

    def send_dice_result(self, channels: list[int], user_name: str, dice_result: DiceResult) -> None:
        if not self.bot.is_ready():
            raise Exception('Bot is not started')
        else:
            for channelId in channels:
                channel: TextChannel = self._get_channel(channelId)
                member: Member = self._get_member(channel, user_name)
                discord_result = crate_embed(dice_result, member, SIMPLE_PRESENTATION)

                self.bot.loop.create_task(channel.send(**discord_result))

                if dice_result.priv_request:
                    self.bot.loop.create_task(channel.send(**discord_result))

    def on_error(self, channels: list[int], error: DiceException) -> None:
        if not self.bot.is_ready():
            raise Exception('Bot is not started')
        else:
            for channelId in channels:
                channel: TextChannel = self._get_channel(channelId)
                discord_result = crate_embed(error)
                self.bot.loop.create_task(channel.send(**discord_result))

    def run(self, thread=False):
        if not BOT_TOKEN:
            raise Exception('Bot token has not be defined')
        elif thread:
            Thread(name='discord-bot', target=self.bot.run, daemon=True).start()
        else:
            self.bot.run(BOT_TOKEN)

    def _get_channel(self, channel_id: int) -> TextChannel:
        channel = self.bot.get_channel(channel_id)
        if not isinstance(channel, TextChannel):
            raise DiceException('Cannot find channel by given id')
        return channel

    @staticmethod
    def _get_member(channel: TextChannel, user_name: str) -> Member:
        members = [member for member in channel.members if str(member) == user_name]
        if len(members) == 0:
            raise DiceException('Cannot find user by given name')
        return members[0]


if __name__ == '__main__':
    DiscordBot().run()
