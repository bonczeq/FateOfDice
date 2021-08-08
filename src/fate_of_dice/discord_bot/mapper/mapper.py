# pylint: disable=function-redefined
from discord import File, Member
from multipledispatch import dispatch

from fate_of_dice.system import DiceResult
from .dice_embed import DiceEmbed
from .dice_result_mapper import from_roll_result
from .exception_mapper import from_exception


@dispatch(str)
def crate_embed(description: str) -> {DiceEmbed}:
    return {'embed': DiceEmbed(colour=0xff00a2, description=description)}


@dispatch(BaseException)
def crate_embed(error: BaseException) -> {DiceEmbed, File}:
    return from_exception(error)


@dispatch(DiceResult, Member, bool)
def crate_embed(result, author: Member, simple: bool) -> {DiceEmbed, File}:
    return from_roll_result(result, author, simple)
