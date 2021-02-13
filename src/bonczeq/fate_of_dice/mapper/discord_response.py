from discord.embeds import Embed
from multipledispatch import dispatch

from bonczeq.fate_of_dice.common import DiceException
from bonczeq.fate_of_dice.system.call_of_cthulhu import SkillCheckResult


@dispatch(DiceException)
def crate_embed(error: DiceException) -> Embed:
    embed = Embed(
        title='Unhandled command',
        colour=0x000000
    )
    embed.add_field(name="Reason", value=str(error), inline=False)
    return embed


@dispatch(BaseException)
def crate_embed(error: BaseException) -> Embed:
    return Embed(
        description=str(error),
        title='Error:',
        colour=0x000000
    )


@dispatch(str)
def crate_embed(description: str) -> Embed:
    return Embed(description=description)


@dispatch(str, str, str)
def crate_embed(description: str, title: str, colour: int) -> Embed:
    return Embed(
        description=description,
        title=title,
        colour=colour
    )


@dispatch(SkillCheckResult)
def crate_embed(skill_check: SkillCheckResult) -> Embed:
    embed = Embed()
    embed.title = skill_check.title
    embed.colour = int(skill_check.colour)
    embed.add_field(name="User:", value=skill_check.user, inline=True)
    embed.add_field(name="Skill check result:", value=skill_check.description, inline=True)
    return embed
