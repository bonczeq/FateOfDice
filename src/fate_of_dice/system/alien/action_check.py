from enum import Enum
from dataclasses import dataclass, field

from fate_of_dice.common.dice import Dice, DicesFilterType
from fate_of_dice.system import DiceResult

from .argument_parser import ActionCheckArguments, parse


def check_action(user: str, command_prefix: str, arguments: (str, ...)) -> 'ActionCheckResult':
    return ActionCheck(user, command_prefix, arguments).roll()


class SkillCheckResultType(Enum):
    NONE = None, 0xffffff
    SUCCESS = "SUCCESS.", 0x55e453
    FAILURE = "Failure.", 0xf35858
    STRESS = "PANIC.", 0xff0000

    def __init__(self, title: str, colour: int = None):
        self.title = title
        self.colour = colour


@dataclass
class ActionCheckResult(DiceResult):
    type: SkillCheckResultType = field(default=SkillCheckResultType.NONE)
    success_amount: int = field(default=0)
    stress_amount: int = field(default=0)
    panic_value: int = field(default=0)
    base_dices: [Dice] = field(default_factory=lambda: [])
    stress_dices: [Dice] = field(default_factory=lambda: [])


class ActionCheck:
    def __init__(self, user: str, command_prefix: str, arguments: (str, ...)):
        self.__user: str = user
        self.__command_prefix: str = command_prefix
        self.__arguments: ActionCheckArguments = parse(command_prefix, arguments)

    def roll(self) -> ActionCheckResult:
        base_dices = [self.__roll_dice() for _ in range(0, self.__arguments.dice_amount)]
        stress_dices = [self.__roll_dice() for _ in range(0, self.__arguments.stress_dice_amount)]

        successes = self.__filter_successes(base_dices + stress_dices)
        successes_amount = len(successes)
        stresses = self.__filter_failures(stress_dices)
        stress_amount = len(stresses)

        panic_value = self.__calculate_panic(stress_amount)

        result_type = self.__check_result_type(successes_amount, stress_amount)
        description = self.__describe_roll(successes_amount, stress_amount, panic_value, base_dices, stress_dices)

        result = ActionCheckResult(user=self.__user, descriptions=[description], type=result_type,
                                   success_amount=successes_amount, stress_amount=stress_amount,
                                   panic_value=panic_value, base_dices=base_dices, stress_dices=stress_dices)
        result.add_basic_arguments(self.__arguments)
        return result

    @staticmethod
    def __roll_dice() -> Dice:
        return Dice.roll(1, 6)

    @staticmethod
    def __filter_successes(dices: [Dice]) -> [Dice]:
        return DicesFilterType.EQUAL.filter_dices(dices, 6)

    @staticmethod
    def __filter_failures(dices: [Dice]) -> [Dice]:
        return DicesFilterType.EQUAL.filter_dices(dices, 1)

    @classmethod
    def __calculate_panic(cls, stress_amount: int) -> int:
        if not stress_amount:
            return 0
        else:
            return stress_amount + cls.__roll_dice()

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
    def __describe_roll(successes_amount: int, stress_amount: int, panic_value: int,
                        base_dices: [Dice], stress_dices: [Dice]) -> str:

        description = f'Base dices: [{", ".join([str(dice) for dice in base_dices])}]'

        if stress_dices:
            description += f'\nStress dices: [{", ".join([str(dice) for dice in stress_dices])}]'

        if successes_amount:
            description += f'\nSuccesses amount: {successes_amount}'
        if panic_value:
            description += f'\nPanic value: {stress_amount} + {panic_value-stress_amount} = {panic_value}'

        return description
