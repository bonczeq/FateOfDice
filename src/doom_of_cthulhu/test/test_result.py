from enum import Enum
from doom_of_cthulhu.common import Dice
from .test_dice import OnesDice, TensDice
from .extra_test_dices import ExtraTestDices


class TestResultColor(Enum):
    CRITICAL_SUCCESS: int = 0xf5e042
    EXTREMAL_SUCCESS: int = 0xb342f5
    HARD_SUCCESS: int = 0x264fad
    NORMAL_SUCCESS: int = 0x288f34
    NORMAL_FAILURE: int = 0xa81d1d
    CRITICAL_FAILURE: int = 0x45342d

    def __int__(self):
        return self.value


class TestResult:
    def __init__(self, threshold: int, extra_dices: str, author: str):
        (self.value, self.__ones_dice, self.__tens_dice, self.__all_tens_dice) = self.__roll(extra_dices)
        (self.test_result, self.test_result_colour) = self.__check_roll_result(self.value, threshold)
        self.description = self.__describe_roll(author)

    @staticmethod
    def __roll(extra_dices_str: str) -> (Dice, OnesDice, TensDice, [TensDice]):
        main_dice = TensDice()
        extra_dices = ExtraTestDices(extra_dices_str)

        tens_dice = extra_dices.chose_dice(main_dice)
        ones_dice = OnesDice()
        value = tens_dice + ones_dice

        return value, ones_dice, tens_dice, [main_dice] + extra_dices.dices

    @staticmethod
    def __check_roll_result(value: int, threshold: int) -> (str, TestResultColor):
        if value == 100 or (value >= 96 and threshold < 50):
            title = "CRITICAL FAILURE!"
            colour = TestResultColor.CRITICAL_FAILURE
        elif value == 1:
            title = "CRITICAL SUCCESS!"
            colour = TestResultColor.CRITICAL_SUCCESS
        elif value <= threshold / 5:
            title = "Extremal success!"
            colour = TestResultColor.EXTREMAL_SUCCESS
        elif value <= threshold / 2:
            title = "Hard success!"
            colour = TestResultColor.HARD_SUCCESS
        elif value <= threshold:
            title = "Normal success."
            colour = TestResultColor.NORMAL_SUCCESS
        else:
            title = "Normal failure."
            colour = TestResultColor.NORMAL_FAILURE

        return title, colour

    def __describe_roll(self, author: str) -> str:
        if len(self.__all_tens_dice) > 1:
            tens_dice_list = '/'.join([str(dice) for dice in self.__all_tens_dice])
            tens_dice_list = f'[{tens_dice_list}] '
        else:
            tens_dice_list = ''

        return f'User {author} roll:\n' \
               f'{self.__tens_dice} {tens_dice_list}+ {self.__ones_dice} = {self.value}'
