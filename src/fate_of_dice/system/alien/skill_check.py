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
    STRESS = "STRESS!", 0xf35858

    def __init__(self, title: str, colour: int = None):
        self.title = title
        self.colour = colour


@dataclass
class SkillCheckResult(BasicResult):
    type: SkillCheckResultType = field(default=SkillCheckResultType.NONE)
    success_amount: int = field(default=0)
    stress_amount: int = field(default=0)
    basic_dices: [Dice] = field(default_factory=lambda: [])
    stress_dices: [Dice] = field(default_factory=lambda: [])


class SkillCheck:
    def __init__(self, user: str, command_prefix: str, arguments: (str, ...)):
        self.__user: str = user
        self.__command_prefix: str = command_prefix
        self.__arguments: SkillCheckArguments = parse(command_prefix, arguments)

    def roll(self) -> SkillCheckResult:
        basic_dices = [Dice.roll(1, 6) for _ in range(0, self.__arguments.dice_amount)]
        stress_dices = [Dice.roll(1, 6) for _ in range(0, self.__arguments.stress_dice_amount)]

        successes = self.__filter_successes(basic_dices + stress_dices)
        successes_amount = len(successes)
        failures = self.__filter_failures(stress_dices)
        stress_amount = len(failures)

        result_type = self.__check_result_type(successes_amount, stress_amount)
        description = self.__describe_roll(successes_amount, stress_amount, basic_dices, stress_dices)

        result = SkillCheckResult(user=self.__user, descriptions=[description], type=result_type,
                                  success_amount=successes_amount, stress_amount=stress_amount,
                                  basic_dices=basic_dices, stress_dices=stress_dices)
        result.add_basic_arguments(self.__arguments)
        return result

    @staticmethod
    def __filter_successes(dices: [Dice]):
        return DicesFilterType.EQUAL.filter_dices(dices, 6)

    @staticmethod
    def __filter_failures(dices: [Dice]):
        return DicesFilterType.EQUAL.filter_dices(dices, 1)

    @staticmethod
    def __check_result_type(successes_amount: int, stress_amount: int) -> SkillCheckResultType:
        if stress_amount > 0:
            result_type = SkillCheckResultType.STRESS
        elif successes_amount > 0:
            result_type = SkillCheckResultType.SUCCESS
        else:
            result_type = SkillCheckResultType.FAILURE
        return result_type

    @staticmethod
    def __describe_roll(successes_amount: int, stress_amount: int, basic_dices: [Dice], stress_dices: [Dice]) -> str:
        description = f'Basic dices: [{", ".join([str(dice) for dice in basic_dices])}]\n'

        if stress_dices:
            description += f'Stress dices: [{", ".join([str(dice) for dice in stress_dices])}]\n'

        if stress_amount > 0:
            description += f'Result: {stress_amount} {"stress" if stress_amount == 1 else "stresses"}'
        else:
            description += f'Result: {successes_amount} {"success" if successes_amount == 1 else "successes"}'

        return description
