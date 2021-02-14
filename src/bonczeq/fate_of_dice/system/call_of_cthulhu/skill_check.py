from enum import Enum
from typing import Final
from pathlib import Path

from bonczeq.fate_of_dice.common import get_resources_path, Dice

from .argument_parser import parse, SkillCheckArguments
from .skill_dice import OnesDice, TensDice, DiceType


def check_skill(user: str, arguments: (str, ...)) -> 'SkillCheckResult':
    skill_check = SkillCheck(user, arguments)
    return skill_check.roll()


class SkillCheckResultType(Enum):
    __CRITICAL_SUCCESS_IMAGE: Final = get_resources_path('icons/critical_success.png')
    __EXTREMAL_SUCCESS_IMAGE: Final = get_resources_path('icons/extremal_success.png')
    __HARD_SUCCESS_IMAGE: Final = get_resources_path('icons/hard_success.png')
    __NORMAL_FAILURE_IMAGE: Final = get_resources_path('icons/failed.png')
    __CRITICAL_FAILURE_IMAGE: Final = get_resources_path('icons/critical_failed.png')

    CRITICAL_SUCCESS: {str, int, Path} = "CRITICAL SUCCESS!", 0xf5e042, __CRITICAL_SUCCESS_IMAGE
    EXTREMAL_SUCCESS: {str, int, Path} = "Extremal success!", 0xb342f5, __EXTREMAL_SUCCESS_IMAGE
    HARD_SUCCESS: {str, int, Path} = "Hard success!", 0x264fad, __HARD_SUCCESS_IMAGE
    NORMAL_SUCCESS: {str, int, Path} = "Normal success.", 0x288f34, None
    NORMAL_FAILURE: {str, int, Path} = "Normal failure.", 0xff0000, __NORMAL_FAILURE_IMAGE
    CRITICAL_FAILURE: {str, int, Path} = "CRITICAL FAILURE!", 0x45342d, __CRITICAL_FAILURE_IMAGE

    def __init__(self, title: str, colour: int = None, icon_path: Path = None):
        self.title = title
        self.colour = colour
        self.icon_path = icon_path


class SkillCheckResult:
    def __init__(self, result_dice: (TensDice, OnesDice), all_dices: ([TensDice], [OnesDice]), threshold: int,
                 user: str):
        (result_tens_dice, result_ones_dice) = result_dice
        result_dice = result_tens_dice + result_ones_dice

        self.user = user
        self.value = 100 if result_dice == 0 else result_dice
        self.type = self.__skill_result_type(self.value, threshold)
        self.description = self.__describe_roll(result_dice, result_tens_dice, result_ones_dice, all_dices)

    @staticmethod
    def __skill_result_type(value: int, threshold: int) -> SkillCheckResultType:
        if value == 100 or (value >= 96 and threshold < 50):
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
            tens_dice_str = f'[{"/".join([str(dice) for dice in tens_dices])}]'

        return f'{result_tens_dice} {tens_dice_str or ""} + {result_ones_dice} = {result_dice}'


class SkillCheck:
    def __init__(self, user: str, arguments: (str, ...)):
        self.__user: str = user
        self.__arguments: SkillCheckArguments = parse(arguments)

    def roll(self) -> SkillCheckResult:
        ones_dice: OnesDice = OnesDice.roll()
        main_tens_dice: TensDice = TensDice.roll()
        (extra_dices_type, extra_dices) = self.__roll_extra_dices(self.__arguments)

        result_dice = self.__chose_dice(ones_dice, main_tens_dice, extra_dices, extra_dices_type)

        return SkillCheckResult((result_dice, ones_dice), ([main_tens_dice] + extra_dices, [ones_dice]),
                                self.__arguments.skill_value, self.__user)

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

        if ones_dice != 0:
            return min(tens_dices)
        else:
            return min(filter(lambda it: it != 0, tens_dices))

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
