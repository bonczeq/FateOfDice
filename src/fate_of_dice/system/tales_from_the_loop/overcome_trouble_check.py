from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from fate_of_dice.common.dice import Dice, DicesFilterType
from fate_of_dice.common.presentation import SymbolResolver
from fate_of_dice.resources.resource_handler import ResourceImageHandler
from fate_of_dice.system import DiceResult
from .argument_parser import OvercomeTroubleArguments, parse


def overcome_trouble_check(user: str, command_prefix: str, arguments: (str, ...)) -> 'OvercomeTroubleResult':
    return _OvercomeTroubleCheck(user, command_prefix, arguments).roll()


class OvercomeTroubleResultType(Enum):
    NONE = None, 0xffffff, None
    SUCCESS = "Success", 0x55e453, ResourceImageHandler.SUCCESS_IMAGE
    FAILURE = "Failure", 0xf35858, ResourceImageHandler.FAILURE_IMAGE

    def __init__(self, title: str, colour: int, icon: [str or Path]):
        self.title = title
        self.colour = colour
        self.icon = icon


@dataclass(frozen=True)
class OvercomeTroubleResult(DiceResult):
    type: OvercomeTroubleResultType = field(default=OvercomeTroubleResultType.NONE)
    success_amount: int = field(default=0)
    dices: [Dice] = field(default_factory=list)


class _OvercomeTroubleCheck:
    def __init__(self, user: str, command_prefix: str, arguments: (str, ...)):
        self.__user: str = user
        self.__arguments: OvercomeTroubleArguments = parse(command_prefix, arguments)

    def roll(self) -> OvercomeTroubleResult:
        dices = [Dice.roll(1, 6) for _ in range(0, self.__arguments.dice_amount)]

        successes = self.__filter_successes(dices)
        successes_amount = len(successes)

        result_type = self.__check_result_type(successes_amount, self.__arguments.success_requirement)
        description = self.__describe_roll(successes_amount, dices)

        return OvercomeTroubleResult(user=self.__user, descriptions=[description], type=result_type,
                                     success_amount=successes_amount, dices=dices, basic_arguments=self.__arguments)

    @staticmethod
    def __filter_successes(dices: [Dice]):
        return DicesFilterType.EQUAL.filter_dices(dices, 6)

    @staticmethod
    def __check_result_type(successes_amount: int, required_successes_amount: int) -> OvercomeTroubleResultType:
        if successes_amount >= required_successes_amount:
            result_type = OvercomeTroubleResultType.SUCCESS
        else:
            result_type = OvercomeTroubleResultType.FAILURE
        return result_type

    @staticmethod
    def __describe_roll(successes_amount: int, result_dices: [Dice]) -> str:
        rolls = f'[{", ".join([SymbolResolver.circled_number(dice, 6) for dice in result_dices])}]'
        success_description = f'{successes_amount} {"success" if successes_amount == 1 else "successes"}'
        return (
            f'Rolls: {rolls}\n'
            f'Result: {success_description}'
        )
