# pylint: disable=function-redefined
from pathlib import Path
from typing import Optional

from discord import File
from discord import Message
from discord.embeds import Embed
from multipledispatch import dispatch

from fate_of_dice.common import DiceException, ResourceImageHandler
from fate_of_dice.system.alien import SkillCheckResult as SkillCheckResultAlien
from fate_of_dice.system.call_of_cthulhu import SkillCheckResult as SkillCheckResultCoC
from fate_of_dice.system.tales_from_the_loop import SkillCheckResult as SkillCheckResultTftL
from fate_of_dice.system.universal import RollResult


@dispatch(str)
def crate_embed(description: str) -> Embed:
    return Embed(colour=0xff00a2, description=description)


@dispatch(DiceException)
def crate_embed(error: DiceException) -> {list[File], Embed}:
    (user_file_name, user_file) = __create_discord_file(ResourceImageHandler.DISCORD_IMAGE)
    (thumbnail_file_name, thumbnail_file) = __create_discord_file(ResourceImageHandler.INNOVATION_IMAGE)

    embed = Embed()
    embed.colour = 0xae6229
    embed.set_author(name='FateOfDice', icon_url=f"attachment://{user_file_name}")
    embed.set_thumbnail(url=f"attachment://{thumbnail_file_name}")
    embed.add_field(name="Unhandled message:", value=str(error), inline=False)

    return {'files': [user_file, thumbnail_file], 'embed': embed}


@dispatch(BaseException)
def crate_embed(error: BaseException) -> {list[File], Embed}:
    (user_file_name, user_file) = __create_discord_file(ResourceImageHandler.PYTHON_IMAGE)
    (thumbnail_file_name, thumbnail_file) = __create_discord_file(ResourceImageHandler.PROCESS_IMAGE)

    embed = Embed()
    embed.colour = 0x000000
    embed.set_author(name='FateOfDice', icon_url=f"attachment://{user_file_name}")
    embed.set_thumbnail(url=f"attachment://{thumbnail_file_name}")
    embed.add_field(name="Exception:", value=str(error), inline=False)

    return {'files': [user_file, thumbnail_file], 'embed': embed}


@dispatch(Message, RollResult, bool)
def crate_embed(message: Message, roll_result: RollResult, simple: bool) -> {Embed}:
    embed = Embed()
    embed.colour = 0x4dd5d3

    if not simple:
        embed.description = message.content
        embed.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))

        if roll_result.dices_modifier.value:
            embed.add_field(name="Modifier:", value=str(roll_result.dices_modifier.value), inline=False)

        for description in roll_result.descriptions:
            embed.add_field(name="Roll:", value=description, inline=False)
        return {'embed': embed}
    else:
        embed.description = "\n".join([roll_result.descriptions])
        return {'embed': embed}


@dispatch(Message, SkillCheckResultCoC, bool)
def crate_embed(message: Message, skill_check: SkillCheckResultCoC, simple: bool) -> {Embed, Optional[File]}:
    embed = Embed()
    embed.title = skill_check.type.title
    embed.colour = skill_check.type.colour

    if not simple:
        (thumbnail_file_name, thumbnail_file) = __create_discord_file(skill_check.type.icon_path)

        embed.description = message.content
        embed.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
        embed.set_thumbnail(url=f"attachment://{thumbnail_file_name}")

        for description in skill_check.descriptions:
            embed.add_field(name="Skill check result:", value=description, inline=False)
        return {'embed': embed, 'file': thumbnail_file}
    else:
        embed.description = "\n".join(skill_check.descriptions)
        return {'embed': embed}


@dispatch(Message, SkillCheckResultTftL, bool)
def crate_embed(message: Message, roll_check: SkillCheckResultTftL, simple: bool) -> {Embed, Optional[File]}:
    embed = Embed()
    embed.title = roll_check.type.title
    embed.colour = roll_check.type.colour

    if not simple:
        embed.description = message.content
        embed.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))

        for description in roll_check.descriptions:
            embed.add_field(name="Roll result:", value=description, inline=False)
        return {'embed': embed}
    else:
        embed.description = "\n".join(roll_check.descriptions)
        return {'embed': embed}


@dispatch(Message, SkillCheckResultAlien, bool)
def crate_embed(message: Message, roll_check: SkillCheckResultAlien, simple: bool) -> {Embed, Optional[File]}:
    embed = Embed()
    embed.title = roll_check.type.title
    embed.colour = roll_check.type.colour

    if not simple:
        embed.description = message.content
        embed.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))

        for description in roll_check.descriptions:
            embed.add_field(name="Roll result:", value=description, inline=False)
        return {'embed': embed}
    else:
        embed.description = "\n".join(roll_check.descriptions)
        return {'embed': embed}


def __create_discord_file(file_path: Optional[Path]) -> (str, File):
    if file_path:
        file_name = file_path.name
        return file_name, File(str(file_path), filename=file_name)
    else:
        return None, None
