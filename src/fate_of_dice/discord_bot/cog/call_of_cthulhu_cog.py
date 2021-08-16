from typing import Final, Iterable

from discord.ext.commands import Context, command
from discord_slash import cog_ext, SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

from fate_of_dice.discord_bot.cog.dice_cog import DiceCog, aliases_to_name, guild_ids
from fate_of_dice.discord_bot.environment import SIMPLE_PRESENTATION
from fate_of_dice.discord_bot.mapper import crate_embed
from fate_of_dice.system.call_of_cthulhu import check_skill


class CallOfCthulhuCog(DiceCog, name='Roll commands'):
    __CALL_OF_CTHULHU_ALIASES: Final[Iterable[str]] = ['c', '?', 'CoC', 'CallOfCthulhu']

    @command(aliases=__CALL_OF_CTHULHU_ALIASES, name=aliases_to_name(__CALL_OF_CTHULHU_ALIASES),
             help='Check Call of Cthulhu RPG skill')
    async def call_of_cthulhu_check(self, ctx: Context, *arguments: str) -> None:
        command_prefix: str = self._get_command_prefix(ctx)
        skill_result = check_skill(ctx.author.name, command_prefix, arguments)
        discord_result = crate_embed(skill_result, ctx.author, SIMPLE_PRESENTATION)
        await self._send_message(ctx, discord_result, skill_result)

    @cog_ext.cog_slash(name='cthulhu', guild_ids=guild_ids, description='Roll commands',
                       options=[
                           create_option(name='options',  option_type=SlashCommandOptionType.STRING, required=False,
                                         description='[skill value] [-b [amount]] [-p [amount]] [--comment [text]]')
                       ])
    async def call_of_cthulhu_check_slash(self, ctx: Context, options: str = None) -> None:
        await self.call_of_cthulhu_check(ctx, *(options or '').split())
