from typing import Final, Iterable

from discord.ext.commands import Context, command
from discord_slash import cog_ext, SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

from fate_of_dice.discord_bot.cog.dice_cog import DiceCog, aliases_to_name, guild_ids
from fate_of_dice.discord_bot.environment import SIMPLE_PRESENTATION
from fate_of_dice.discord_bot.mapper import crate_embed
from fate_of_dice.system.tales_from_the_loop import overcome_trouble_check


class TalesFromTheLoopCog(DiceCog, name='Roll commands'):
    __TALES_FROM_THE_LOOP_ALIASES: Final[Iterable[str]] = ['t', 'TftL', 'TalesFromTheLoop']

    @command(aliases=__TALES_FROM_THE_LOOP_ALIASES, name=aliases_to_name(__TALES_FROM_THE_LOOP_ALIASES),
             help='Check overcoming Tales From The Loop RPG troubles')
    async def tales_from_the_loop_check(self, ctx: Context, *arguments: str) -> None:
        command_prefix: str = self._get_command_prefix(ctx)
        roll_result = overcome_trouble_check(ctx.author.name, command_prefix, arguments)
        discord_result = crate_embed(roll_result, ctx.author, SIMPLE_PRESENTATION)
        await self._send_message(ctx, discord_result, roll_result)

    @cog_ext.cog_slash(name='tales', guild_ids=guild_ids,
                       description='Check overcoming Tales From The Loop RPG troubles',
                       options=[
                           create_option(name='options',  option_type=SlashCommandOptionType.STRING, required=False,
                                         description="[dice amount] [required number of successes] [--comment [text]]")
                       ])
    async def tales_from_the_loop_check_slash(self, ctx: Context, options: str = None) -> None:
        await self.tales_from_the_loop_check(ctx, *(options or '').split())
