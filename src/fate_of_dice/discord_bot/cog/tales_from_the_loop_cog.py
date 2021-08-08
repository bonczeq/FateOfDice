from typing import Final, Iterable

from discord.ext.commands import Context, command

from fate_of_dice.discord_bot.cog.dice_cog import DiceCog, aliases_to_name
from fate_of_dice.discord_bot.environment import SIMPLE_PRESENTATION
from fate_of_dice.discord_bot.mapper import crate_embed
from fate_of_dice.system.tales_from_the_loop import overcome_trouble_check


class TalesFromTheLoopCog(DiceCog, name='Roll commands'):
    __TALES_FROM_THE_LOOP_ALIASES: Final[Iterable[str]] = ['t', 'TftL', 'TalesFromTheLoop']

    @command(aliases=__TALES_FROM_THE_LOOP_ALIASES, name=aliases_to_name(__TALES_FROM_THE_LOOP_ALIASES),
             help='Check overcoming Tales From The Loop RPG troubles')
    async def tales_from_the_loop_check(self, ctx: Context, *arguments: str) -> None:
        command_prefix: str = ctx.prefix + ctx.invoked_with
        roll_result = overcome_trouble_check(ctx.author.name, command_prefix, arguments)
        discord_result = crate_embed(roll_result, ctx.author, SIMPLE_PRESENTATION)
        await self._send_message(ctx, discord_result, roll_result)
