import logging

from discord.ext.commands import Context, command
from discord_slash import cog_ext

from fate_of_dice.discord_bot.cog.dice_cog import DiceCog, guild_ids
from fate_of_dice.discord_bot.mapper import crate_embed


class BasicCog(DiceCog, name='Basic commands'):

    @command(help='Information about bot')
    async def info(self, ctx: Context) -> None:
        logging.info('Received info command')
        message: str = (
            'Author: **bonczeq**\n'
            'Please check [GitHub project page](https://github.com/bonczeq/FateOfDice/blob/master/README.md)'
        )
        discord_result = crate_embed(message)
        await ctx.send(**discord_result)

    @cog_ext.cog_slash(name='info', description='Information about bot', guild_ids=guild_ids)
    async def info_slash(self, ctx: Context) -> None:
        await self.info(ctx)
