from pathlib import Path
from typing import Final

from discord import File
from discord import Message
from discord.embeds import Embed
from multipledispatch import dispatch

from fate_of_dice.common import DiceException, get_resources_path
from fate_of_dice.system.call_of_cthulhu import SkillCheckResult

__PYTHON_IMAGE: Final = get_resources_path('icons/python.png')
__DISCORD_IMAGE: Final = get_resources_path('icons/discord.png')
__INNOVATION_IMAGE: Final = get_resources_path('icons/innovation.png')
__PROCESS_IMAGE: Final = get_resources_path('icons/process.png')


@dispatch(DiceException)
def crate_embed(error: DiceException) -> {list[File], Embed}:
    (user_file_name, user_file) = __create_discord_file(__DISCORD_IMAGE)
    (thumbnail_file_name, thumbnail_file) = __create_discord_file(__INNOVATION_IMAGE)

    embed = Embed()
    embed.colour = 0xff00a2
    embed.set_author(name='FateOfDice', icon_url=f"attachment://{user_file_name}")
    embed.set_thumbnail(url=f"attachment://{thumbnail_file_name}")
    embed.add_field(name="Unhandled message:", value=str(error), inline=False)

    return {'files': [user_file, thumbnail_file], 'embed': embed}


@dispatch(BaseException)
def crate_embed(error: BaseException) -> {list[File], Embed}:
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


@dispatch(Message, SkillCheckResult)
def crate_embed(message: Message, skill_check: SkillCheckResult) -> {File, Embed}:
    (thumbnail_file_name, thumbnail_file) = __create_discord_file(skill_check.type.icon_path)

    embed = Embed()
    embed.title = skill_check.type.title
    embed.colour = skill_check.type.colour
    embed.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
    embed.set_thumbnail(url=f"attachment://{thumbnail_file_name}")
    embed.add_field(name="Skill check result:", value=skill_check.description, inline=True)

    return {'file': thumbnail_file, 'embed': embed}


def __create_discord_file(file_path: Path or None) -> (str, File):
    if file_path:
        file_name = file_path.name
        return file_name, File(str(file_path), filename=file_name)
    else:
        return None, None
