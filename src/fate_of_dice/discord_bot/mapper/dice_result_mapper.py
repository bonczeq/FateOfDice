# pylint: disable=function-redefined
from typing import Optional

from discord import Member, File
from multipledispatch import dispatch

from fate_of_dice.system.alien import ActionCheckResult
from fate_of_dice.system.call_of_cthulhu import SkillCheckResult
from fate_of_dice.system.tales_from_the_loop import OvercomeTroubleResult
from fate_of_dice.system.universal import RollResult
from .dice_embed import DiceEmbed


@dispatch(RollResult, Member, bool)
def from_roll_result(roll_result: RollResult, author: Member, simple: bool = False) -> {DiceEmbed}:
    embed = DiceEmbed.from_dice_result(roll_result, author, simple)
    embed.colour = 0x4dd5d3

    if not embed.simple_presentation:
        embed.add_fields(name="Roll:", values=roll_result.descriptions, inline=False)

    return {'embed': embed}


@dispatch(SkillCheckResult, Member, bool)
def from_roll_result(skill_check: SkillCheckResult,
                     author: Member, simple: bool = False) -> {DiceEmbed, Optional[File]}:
    embed = DiceEmbed.from_dice_result(skill_check, author, simple)
    embed.title = skill_check.type.title
    embed.colour = skill_check.type.colour

    if not embed.simple_presentation:
        embed.add_thumbnail(skill_check.type.icon)
        embed.add_fields(name="Skill check result:", values=skill_check.descriptions, inline=False)
        return {'embed': embed, 'file': embed.thumbnail_file()}
    else:
        return {'embed': embed}


@dispatch(OvercomeTroubleResult, Member, bool)
def from_roll_result(overcome_trouble: OvercomeTroubleResult,
                     author: Member, simple: bool = False) -> {DiceEmbed, Optional[File]}:
    embed = DiceEmbed.from_dice_result(overcome_trouble, author, simple)
    embed.title = overcome_trouble.type.title
    embed.colour = overcome_trouble.type.colour

    if not embed.simple_presentation:
        embed.add_thumbnail(overcome_trouble.type.icon)
        embed.add_fields(name="Roll result:", values=overcome_trouble.descriptions, inline=True)
        return {'embed': embed, 'file': embed.thumbnail_file()}
    else:
        return {'embed': embed}


@dispatch(ActionCheckResult, Member, bool)
def from_roll_result(action_check: ActionCheckResult,
                     author: Member, simple: bool = False) -> {DiceEmbed, Optional[File]}:
    embed = DiceEmbed.from_dice_result(action_check, author, simple)
    embed.title = action_check.type.title
    embed.colour = action_check.type.colour

    if not embed.simple_presentation:
        embed.add_thumbnail(action_check.type.icon)
        embed.add_fields(name="Roll result:", values=action_check.descriptions, inline=False)
        return {'embed': embed, 'file': embed.thumbnail_file()}
    else:
        return {'embed': embed}
