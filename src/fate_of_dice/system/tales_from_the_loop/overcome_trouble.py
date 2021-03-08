from enum import Enum
from dataclasses import dataclass, field

from fate_of_dice.common.dice import Dice, DicesFilterType
from fate_of_dice.system import DiceResult

from .argument_parser import OvercomeTroubleArguments, parse


def overcome_trouble(user: str, command_prefix: str, arguments: (str, ...)) -> 'OvercomeTroubleResult':
    return OvercomeTrouble(user, command_prefix, arguments).roll()


class OvercomeTroubleResultType(Enum):
    NONE = None, 0xffffff
    SUCCESS = "SUCCESS.", 0x55e453
    FAILURE = "Failure.", 0xf35858

    def __init__(self, title: str, colour: int = None):
        self.title = title
        self.colour = colour


@dataclass
class OvercomeTroubleResult(DiceResult):
    type: OvercomeTroubleResultType = field(default=OvercomeTroubleResultType.NONE)
    success_amount: int = field(default=0)
    dices: [Dice] = field(default_factory=lambda: [])


class OvercomeTrouble:
    def __init__(self, user: str, command_prefix: str, arguments: (str, ...)):
        self.__user: str = user
        self.__command_prefix: str = command_prefix
        self.__arguments: OvercomeTroubleArguments = parse(command_prefix, arguments)

    def roll(self) -> OvercomeTroubleResult:
        dices = [Dice.roll(1, 6) for _ in range(0, self.__arguments.dice_amount)]

        successes = self.__filter_successes(dices)
        successes_amount = len(successes)

        result_type = self.__check_result_type(successes_amount, self.__arguments.success_requirement)
        description = self.__describe_roll(successes_amount, dices)

        return OvercomeTroubleResult(user=self.__user, descriptions=[description], type=result_type,
                                     success_amount=successes_amount, dices=dices)\
            .add_basic_arguments(self.__arguments)

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
        success_description = f'{successes_amount} {"success" if successes_amount == 1 else "successes"}'
        return f'[{", ".join([str(dice) for dice in result_dices])}] 🠖 {success_description}'
