from discord.ext.commands import Cog, Context

from fate_of_dice.system import DiceResult
from fate_of_dice.discord_bot.environment import FORWARD_CHANNELS

guild_ids = []


def aliases_to_name(aliases: [str]) -> str:
    return " | ".join(aliases)


class DiceCog(Cog):
    @classmethod
    def _get_command_prefix(cls, ctx: Context) -> str:
        if hasattr(ctx, 'prefix'):
            return ctx.prefix + ctx.invoked_with
        else:
            return ctx.invoked_with

    @classmethod
    async def _send_message(cls, ctx: Context, discord_result, dice_result: DiceResult) -> None:
        await ctx.send(**discord_result)

        forward_channels: list = FORWARD_CHANNELS.get(str(ctx.channel.id))
        if forward_channels:
            await cls.__forward_messages(ctx, forward_channels, discord_result)
        if dice_result.priv_request:
            await ctx.author.send(**discord_result)

    @classmethod
    async def __forward_messages(cls, ctx: Context, forward_channels: list, discord_result) -> None:
        for channelId in forward_channels:
            channel = ctx.guild.get_channel(int(channelId))
            await channel.send(**discord_result)
