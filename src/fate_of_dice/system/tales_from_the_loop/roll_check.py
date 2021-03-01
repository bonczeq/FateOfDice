from enum import Enum
from dataclasses import dataclass

from fate_of_dice.common.dice import Dice, DicesFilterType
from fate_of_dice.system import BasicResult

from .argument_parser import RollCheckArguments, parse


def roll_check(user: str, command_prefix: str, arguments: (str, ...)) -> 'RollCheckResult':
    return RollCheck(user, command_prefix, arguments).roll()


class RollCheckResultType(Enum):
    NONE = None, 0xffffff
    SUCCESS = "SUCCESS.", 0x55e453
    FAILURE = "Failure.", 0xf35858

    def __init__(self, title: str, colour: int = None):
        self.title = title
        self.colour = colour


@dataclass
class RollCheckResult(BasicResult):
    type: RollCheckResultType
    success_amount: int
    dices: [Dice]


class RollCheck:
    def __init__(self, user: str, command_prefix: str, arguments: (str, ...)):
        self.__user: str = user
        self.__command_prefix: str = command_prefix
        self.__arguments: RollCheckArguments = parse(command_prefix, arguments)

    def roll(self) -> RollCheckResult:
        dices = [Dice.roll(1, 6) for _ in range(0, self.__arguments.dice_amount)]

        successes = self.__filter_successes(dices)
        successes_amount = len(successes)

        result_type = self.__check_result_type(successes_amount, self.__arguments.success_requirement)
        description = self.__describe_roll(successes_amount, dices)

        return RollCheckResult(user=self.__user, priv_request=self.__arguments.priv_request,
                               descriptions=[description], type=result_type,
                               success_amount=successes_amount, dices=dices)

    @staticmethod
    def __filter_successes(dices: [Dice]):
        return DicesFilterType.EQUAL.filter_dices(dices, 6)

    @staticmethod
    def __check_result_type(successes_amount: int, required_successes_amount: int) -> RollCheckResultType:
        if successes_amount >= required_successes_amount:
            result_type = RollCheckResultType.SUCCESS
        else:
            result_type = RollCheckResultType.FAILURE
        return result_type

    @staticmethod
    def __describe_roll(successes_amount: int, result_dices: [Dice]) -> str:
        success_description = f'{successes_amount} {"success" if successes_amount == 1 else "successes"}'
        return f'[{", ".join([str(dice) for dice in result_dices])}] 🠖 {success_description}'
