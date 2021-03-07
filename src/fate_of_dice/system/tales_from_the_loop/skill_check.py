from enum import Enum
from dataclasses import dataclass, field

from fate_of_dice.common.dice import Dice, DicesFilterType
from fate_of_dice.system import BasicResult

from .argument_parser import SkillCheckArguments, parse


def check_skill(user: str, command_prefix: str, arguments: (str, ...)) -> 'SkillCheckResult':
    return SkillCheck(user, command_prefix, arguments).roll()


class SkillCheckResultType(Enum):
    NONE = None, 0xffffff
    SUCCESS = "SUCCESS.", 0x55e453
    FAILURE = "Failure.", 0xf35858

    def __init__(self, title: str, colour: int = None):
        self.title = title
        self.colour = colour


@dataclass
class SkillCheckResult(BasicResult):
    type: SkillCheckResultType = field(default=SkillCheckResultType.NONE)
    success_amount: int = field(default=0)
    dices: [Dice] = field(default_factory=lambda: [])


class SkillCheck:
    def __init__(self, user: str, command_prefix: str, arguments: (str, ...)):
        self.__user: str = user
        self.__command_prefix: str = command_prefix
        self.__arguments: SkillCheckArguments = parse(command_prefix, arguments)

    def roll(self) -> SkillCheckResult:
        dices = [Dice.roll(1, 6) for _ in range(0, self.__arguments.dice_amount)]

        successes = self.__filter_successes(dices)
        successes_amount = len(successes)

        result_type = self.__check_result_type(successes_amount, self.__arguments.success_requirement)
        description = self.__describe_roll(successes_amount, dices)

        return SkillCheckResult(user=self.__user, descriptions=[description], type=result_type,
                                success_amount=successes_amount, dices=dices)\
            .add_basic_arguments(self.__arguments)

    @staticmethod
    def __filter_successes(dices: [Dice]):
        return DicesFilterType.EQUAL.filter_dices(dices, 6)

    @staticmethod
    def __check_result_type(successes_amount: int, required_successes_amount: int) -> SkillCheckResultType:
        if successes_amount >= required_successes_amount:
            result_type = SkillCheckResultType.SUCCESS
        else:
            result_type = SkillCheckResultType.FAILURE
        return result_type

    @staticmethod
    def __describe_roll(successes_amount: int, result_dices: [Dice]) -> str:
        success_description = f'{successes_amount} {"success" if successes_amount == 1 else "successes"}'
        return f'[{", ".join([str(dice) for dice in result_dices])}] 🠖 {success_description}'
