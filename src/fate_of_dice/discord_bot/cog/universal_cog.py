from typing import Final, Iterable

from discord.ext.commands import Context, command
from discord_slash import cog_ext, SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

from fate_of_dice.discord_bot.cog.dice_cog import DiceCog, aliases_to_name, guild_ids
from fate_of_dice.discord_bot.environment import SIMPLE_PRESENTATION
from fate_of_dice.discord_bot.mapper import crate_embed
from fate_of_dice.system.universal import roll


class UniversalCog(DiceCog, name='Roll commands'):
    __UNIVERSAL_ROLL_ALIASES: Final[Iterable[str]] = ['r', '!', 'roll']

    @command(aliases=__UNIVERSAL_ROLL_ALIASES, name=aliases_to_name(__UNIVERSAL_ROLL_ALIASES),
             help='Roll the defined dices')
    async def universal_roll(self, ctx: Context, *arguments: str) -> None:
        command_prefix: str = self._get_command_prefix(ctx)
        roll_result = roll(ctx.author.name, command_prefix, arguments)
        discord_result = crate_embed(roll_result, ctx.author, SIMPLE_PRESENTATION)
        await self._send_message(ctx, discord_result, roll_result)

    @cog_ext.cog_slash(name='roll', description='Roll the defined dices', guild_ids=guild_ids,
                       options=[
                           create_option(name='options',  option_type=SlashCommandOptionType.STRING, required=False,
                                         description="[dices ...] "
                                                     "[-e value | --upper-than value | --lower-than value] "
                                                     "[-m | -x | -s | -r | --sum]")
                       ])
    async def universal_roll_slash(self, ctx: Context, options: str = None) -> None:
        await self.universal_roll(ctx, *(options or '').split())
