from typing import Final, Iterable

from discord.ext.commands import Context, command
from discord_slash import cog_ext, SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

from fate_of_dice.discord_bot.cog.dice_cog import DiceCog, aliases_to_name, guild_ids
from fate_of_dice.discord_bot.environment import SIMPLE_PRESENTATION
from fate_of_dice.discord_bot.mapper import crate_embed
from fate_of_dice.system.alien import check_action


class AlienCog(DiceCog, name='Roll commands'):
    __ALIEN_ALIASES: Final[Iterable[str]] = ['a', 'Alien']

    @command(aliases=__ALIEN_ALIASES, name=aliases_to_name(__ALIEN_ALIASES),
             help='Check Alien RPG skill')
    async def alien_check(self, ctx: Context, *arguments: str) -> None:
        command_prefix: str = self._get_command_prefix(ctx)
        check_result = check_action(ctx.author.name, command_prefix, arguments)
        discord_result = crate_embed(check_result, ctx.author, SIMPLE_PRESENTATION)
        await self._send_message(ctx, discord_result, check_result)

    @cog_ext.cog_slash(name='alien', guild_ids=guild_ids,
                       description='Check Alien RPG skill',
                       options=[
                           create_option(name='options',  option_type=SlashCommandOptionType.STRING, required=False,
                                         description="[base dice amount] [stress dice amount] [--comment [text]]")
                       ])
    async def alien_check_slash(self, ctx: Context, options: str = None) -> None:
        await self.alien_check(ctx, *(options or '').split())
