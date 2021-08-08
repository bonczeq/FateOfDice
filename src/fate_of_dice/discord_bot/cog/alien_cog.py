from typing import Final, Iterable

from discord.ext.commands import Context, command

from fate_of_dice.discord_bot.cog.dice_cog import DiceCog, aliases_to_name
from fate_of_dice.discord_bot.environment import SIMPLE_PRESENTATION
from fate_of_dice.discord_bot.mapper import crate_embed
from fate_of_dice.system.alien import check_action


class AlienCog(DiceCog, name='Roll commands'):
    __ALIEN_ALIASES: Final[Iterable[str]] = ['a', 'Alien']

    @command(aliases=__ALIEN_ALIASES, name=aliases_to_name(__ALIEN_ALIASES),
             help='Check Alien RPG skill')
    async def alien_check(self, ctx: Context, *arguments: str) -> None:
        command_prefix: str = ctx.prefix + ctx.invoked_with
        check_result = check_action(ctx.message.author.name, command_prefix, arguments)
        discord_result = crate_embed(check_result, ctx.author, SIMPLE_PRESENTATION)
        await self._send_message(ctx, discord_result, check_result)
