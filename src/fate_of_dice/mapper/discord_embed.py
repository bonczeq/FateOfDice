# pylint: disable=function-redefined

from pathlib import Path
from typing import Final, Optional

from discord import File
from discord import Message
from discord.embeds import Embed
from multipledispatch import dispatch

from fate_of_dice.common import DiceException, ResourcesHandler
from fate_of_dice.system.call_of_cthulhu import SkillCheckResult
from fate_of_dice.system.universal import RollResult

__PYTHON_IMAGE: Final[Path] = ResourcesHandler.get_resources_path('icons/python.png')
__DISCORD_IMAGE: Final[Path] = ResourcesHandler.get_resources_path('icons/discord.png')
__INNOVATION_IMAGE: Final[Path] = ResourcesHandler.get_resources_path('icons/innovation.png')
__PROCESS_IMAGE: Final[Path] = ResourcesHandler.get_resources_path('icons/process.png')


@dispatch(DiceException)
def crate_embed(error: DiceException) -> {[File], Embed}:
    (user_file_name, user_file) = __create_discord_file(__DISCORD_IMAGE)
    (thumbnail_file_name, thumbnail_file) = __create_discord_file(__INNOVATION_IMAGE)

    embed = Embed()
    embed.colour = 0xff00a2
    embed.set_author(name='FateOfDice', icon_url=f"attachment://{user_file_name}")
    embed.set_thumbnail(url=f"attachment://{thumbnail_file_name}")
    embed.add_field(name="Unhandled message:", value=str(error), inline=False)

    return {'files': [user_file, thumbnail_file], 'embed': embed}


@dispatch(BaseException)
def crate_embed(error: BaseException) -> {[File], Embed}:
    (user_file_name, user_file) = __create_discord_file(__PYTHON_IMAGE)
    (thumbnail_file_name, thumbnail_file) = __create_discord_file(__PROCESS_IMAGE)

    embed = Embed()
    embed.colour = 0x712828
    embed.set_author(name='FateOfDice', icon_url=f"attachment://{user_file_name}")
    embed.set_thumbnail(url=f"attachment://{thumbnail_file_name}")
    embed.add_field(name="Exception:", value=str(error), inline=False)

    return {'files': [user_file, thumbnail_file], 'embed': embed}


@dispatch(str)
def crate_embed(description: str) -> Embed:
    return Embed(description=description)


@dispatch(Message, [RollResult], bool)
def crate_embed(message: Message, roll_results: [RollResult], simple: bool) -> {Embed}:
    embed = Embed()
    embed.colour = 0x8feb34

    if not simple:
        embed.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
        for result in roll_results:
            embed.add_field(name="Modifier:", value=str(result.modifier), inline=True)
            embed.add_field(name="Roll:", value=result.description, inline=False)
        return {'embed': embed}
    else:
        embed.description = "\n".join([result.description for result in roll_results])
        return {'embed': embed}


@dispatch(Message, SkillCheckResult, bool)
def crate_embed(message: Message, skill_check: SkillCheckResult, simple: bool) -> {Embed, Optional[File]}:
    embed = Embed()
    embed.title = skill_check.type.title
    embed.colour = skill_check.type.colour

    if not simple:
        (thumbnail_file_name, thumbnail_file) = __create_discord_file(skill_check.type.icon_path)
        embed.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
        embed.set_image(url=f"attachment://{thumbnail_file_name}")
        embed.description = message.content
        embed.add_field(name="Skill check result:", value=skill_check.description, inline=True)
        return {'embed': embed, 'file': thumbnail_file}
    else:
        embed.description = skill_check.description
        return {'embed': embed}


def __create_discord_file(file_path: Optional[Path]) -> Optional[(str, File)]:
    if file_path:
        file_name = file_path.name
        return file_name, File(str(file_path), filename=file_name)
    else:
        return None
