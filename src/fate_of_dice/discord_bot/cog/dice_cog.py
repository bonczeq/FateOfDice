from discord.ext.commands import Cog, Context

from fate_of_dice.system import DiceResult

guild_ids = [762274941197352971]


def aliases_to_name(aliases: [str]) -> str:
    return " | ".join(aliases)


class DiceCog(Cog):
    @classmethod
    def _get_command_prefix(cls, ctx: Context) -> str:
        if hasattr(ctx, 'prefix'):
            return ctx.prefix + ctx.invoked_with
        else:
            return ctx.command + ctx.invoked_with

    @classmethod
    async def _send_message(cls, ctx: Context, discord_result, dice_result: DiceResult) -> None:
        await ctx.send(**discord_result)

        if dice_result.priv_request:
            await ctx.author.send(**discord_result)
