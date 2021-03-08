from enum import Enum
from pathlib import Path
from dataclasses import dataclass, field

from fate_of_dice.common.dice import Dice
from fate_of_dice.common import ResourceImageHandler
from fate_of_dice.system import DiceResult

from .argument_parser import parse, SkillCheckArguments
from .skill_dice import OnesDice, TensDice, DiceType


def check_skill(user: str, command_prefix: str, arguments: (str, ...)) -> 'SkillCheckResult':
    return SkillCheck(user, command_prefix, arguments).roll()


class SkillCheckResultType(Enum):
    NONE = None, 0xffffff, None
    CRITICAL_SUCCESS = "CRITICAL SUCCESS!", 0xc547ff, ResourceImageHandler.CRITICAL_SUCCESS_IMAGE
    EXTREMAL_SUCCESS = "Extremal success!", 0xfcff4d, ResourceImageHandler.EXTREMAL_SUCCESS_IMAGE
    HARD_SUCCESS = "Hard success!", 0x7d7aff, ResourceImageHandler.HARD_SUCCESS_IMAGE
    NORMAL_SUCCESS = "Normal success.", 0x55e453, None
    NORMAL_FAILURE = "Normal failure.", 0xf35858, ResourceImageHandler.NORMAL_FAILURE_IMAGE
    CRITICAL_FAILURE = "CRITICAL FAILURE!", 0xff0000, ResourceImageHandler.CRITICAL_FAILURE_IMAGE

    def __init__(self, title: str, colour: int = None, icon_path: Path = None):
        self.title = title
        self.colour = colour
        self.icon_path = icon_path


@dataclass
class SkillCheckResult(DiceResult):
    value: Dice = field(default=None)
    type: SkillCheckResultType = field(default=SkillCheckResultType.NONE)


class SkillCheck:
    def __init__(self, user: str, command_prefix: str, arguments: (str, ...)):
        self.__user: str = user
        self.__command_prefix: str = command_prefix
        self.__arguments: SkillCheckArguments = parse(command_prefix, arguments)

    def roll(self) -> SkillCheckResult:
        ones_dice: OnesDice = OnesDice.roll()
        main_tens_dice: TensDice = TensDice.roll()

        (extra_dices_type, extra_dices) = self.__roll_extra_dices(self.__arguments)
        result_tens_dice = self.__chose_dice(ones_dice, main_tens_dice, extra_dices, extra_dices_type)

        result_dice = (result_tens_dice, ones_dice)
        all_dices = ([main_tens_dice] + extra_dices, [ones_dice])
        return self.__create_result(result_dice, all_dices, self.__arguments.skill_value)

    @classmethod
    def __chose_dice(cls, ones_dice: OnesDice, main_tens_dice: TensDice,
                     extra_dices: [TensDice], extra_dices_type: DiceType) -> Dice:
        if extra_dices_type == DiceType.PENALTY:
            return cls.__max_dice(ones_dice, main_tens_dice, extra_dices)
        elif extra_dices_type == DiceType.BONUS:
            return cls.__min_dice(ones_dice, main_tens_dice, extra_dices)
        else:
            return main_tens_dice

    @staticmethod
    def __max_dice(ones_dice: OnesDice, main_tens_dice: TensDice, extra_dices: [TensDice]) -> Dice:
        tens_dices: [TensDice] = [main_tens_dice] + extra_dices

        if ones_dice == 0 and any(it == 0 for it in tens_dices):
            return Dice(0)
        else:
            return max(tens_dices)

    @staticmethod
    def __min_dice(ones_dice: OnesDice, main_tens_dice: TensDice, extra_dices: [TensDice]) -> Dice:
        tens_dices: [TensDice] = [main_tens_dice] + extra_dices

        if ones_dice == 0:
            return min(filter(lambda it: it != 0, tens_dices))
        else:
            return min(tens_dices)

    @staticmethod
    def __roll_extra_dices(arguments: SkillCheckArguments) -> (DiceType, [TensDice]):
        amount = arguments.bonus_dice_amount - arguments.penalty_dice_amount

        if amount == 0:
            dice_type = None
        elif amount > 0:
            dice_type = DiceType.BONUS
        else:
            dice_type = DiceType.PENALTY

        return dice_type, [TensDice.roll(dice_type) for _ in range(abs(amount))]

    def __create_result(self, result_dice: (TensDice, OnesDice), all_dices: ([TensDice], [OnesDice]), threshold: int):
        (result_tens_dice, result_ones_dice) = result_dice
        result_dice = result_tens_dice + result_ones_dice
        result_dice = Dice(100) if result_dice == 0 else result_dice

        result_type = self.__skill_result_type(result_dice, threshold)
        description = self.__describe_roll(result_dice, result_tens_dice, result_ones_dice, all_dices)

        return SkillCheckResult(value=result_dice, type=result_type, descriptions=[description], user=self.__user) \
            .add_basic_arguments(self.__arguments)

    @staticmethod
    def __skill_result_type(value: int, threshold: int) -> SkillCheckResultType:
        if not threshold:
            result_type = SkillCheckResultType.NONE
        elif value == 100 or (value >= 96 and threshold < 50):
            result_type = SkillCheckResultType.CRITICAL_FAILURE
        elif value == 1:
            result_type = SkillCheckResultType.CRITICAL_SUCCESS
        elif value <= threshold / 5:
            result_type = SkillCheckResultType.EXTREMAL_SUCCESS
        elif value <= threshold / 2:
            result_type = SkillCheckResultType.HARD_SUCCESS
        elif value <= threshold:
            result_type = SkillCheckResultType.NORMAL_SUCCESS
        else:
            result_type = SkillCheckResultType.NORMAL_FAILURE

        return result_type

    @staticmethod
    def __describe_roll(result_dice: Dice, result_tens_dice: Dice, result_ones_dice: Dice,
                        all_dices: ([TensDice], [OnesDice])) -> str:
        (tens_dices, _) = all_dices

        tens_dice_str = None
        if len(tens_dices) > 1:
            tens_dice_str = f'[{"/".join([str(dice) for dice in tens_dices])}] '

        return f'{result_tens_dice} {tens_dice_str or ""}+ {result_ones_dice} = {result_dice}'
