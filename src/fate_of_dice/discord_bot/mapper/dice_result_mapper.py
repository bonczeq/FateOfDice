# pylint: disable=function-redefined
from typing import Optional

from discord import Message, File
from multipledispatch import dispatch

from fate_of_dice.system.alien import ActionCheckResult
from fate_of_dice.system.call_of_cthulhu import SkillCheckResult
from fate_of_dice.system.tales_from_the_loop import OvercomeTroubleResult
from fate_of_dice.system.universal import RollResult
from .dice_embed import DiceEmbed


@dispatch(RollResult, Message, bool)
def from_roll_result(roll_result: RollResult, message: Message, simple: bool = False) -> {DiceEmbed}:
    embed = DiceEmbed.from_dice_result(roll_result, message, simple)
    embed.colour = 0x4dd5d3

    if not embed.simple_presentation:
        embed.add_fields(name="Roll:", values=roll_result.descriptions, inline=False)

    return {'embed': embed}


@dispatch(SkillCheckResult, Message, bool)
def from_roll_result(skill_check: SkillCheckResult,
                     message: Message, simple: bool = False) -> {DiceEmbed, Optional[File]}:
    embed = DiceEmbed.from_dice_result(skill_check, message, simple)
    embed.title = skill_check.type.title
    embed.colour = skill_check.type.colour

    if not embed.simple_presentation:
        embed.add_thumbnail(skill_check.type.icon)
        embed.add_fields(name="Skill check result:", values=skill_check.descriptions, inline=False)
        return {'embed': embed, 'file': embed.thumbnail_file()}
    else:
        return {'embed': embed}


@dispatch(OvercomeTroubleResult, Message, bool)
def from_roll_result(overcome_trouble: OvercomeTroubleResult,
                     message: Message, simple: bool = False) -> {DiceEmbed, Optional[File]}:
    embed = DiceEmbed.from_dice_result(overcome_trouble, message, simple)
    embed.title = overcome_trouble.type.title
    embed.colour = overcome_trouble.type.colour

    if not embed.simple_presentation:
        embed.add_thumbnail(overcome_trouble.type.icon)
        embed.add_fields(name="Overcome a trouble result:", values=overcome_trouble.descriptions, inline=True)
        return {'embed': embed, 'file': embed.thumbnail_file()}
    else:
        return {'embed': embed}


@dispatch(ActionCheckResult, Message, bool)
def from_roll_result(action_check: ActionCheckResult,
                     message: Message, simple: bool = False) -> {DiceEmbed, Optional[File]}:
    embed = DiceEmbed.from_dice_result(action_check, message, simple)
    embed.title = action_check.type.title
    embed.colour = action_check.type.colour

    if not embed.simple_presentation:
        embed.add_thumbnail(action_check.type.icon)
        embed.add_fields(name="Roll result:", values=action_check.descriptions, inline=False)
        return {'embed': embed, 'file': embed.thumbnail_file()}
    else:
        return {'embed': embed}
