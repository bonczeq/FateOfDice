# pylint: disable=function-redefined
from discord import File
from multipledispatch import dispatch

from fate_of_dice.common import DiceException
from fate_of_dice.resources.resource_handler import ResourceImageHandler
from .dice_embed import DiceEmbed


@dispatch(DiceException)
def from_exception(error: DiceException) -> {DiceEmbed, File}:
    embed = DiceEmbed(description=str(error), colour=0xae6229)
    embed.add_thumbnail(ResourceImageHandler.INNOVATION_IMAGE)
    return {'embed': embed, 'file': embed.thumbnail_file()}


@dispatch(BaseException)
def from_exception(error: BaseException) -> {DiceEmbed, File}:
    embed = DiceEmbed(description=str(error), title="Error", colour=0x000000)
    embed.add_thumbnail(ResourceImageHandler.PROCESS_IMAGE)
    return {'embed': embed, 'file': embed.thumbnail_file()}
