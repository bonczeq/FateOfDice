from enum import Enum
from typing import Optional, Callable
from statistics import mean
from math import floor, ceil

from fate_of_dice.common.dice import Dice
from .dice_argument_parse import DicesBasicArguments


class DicesModifier(Enum):
    NONE = None
    MIN = 'Minimum'
    MAX = 'Maximum'
    SORTED = 'Sorted'
    REVERSE_SORTED = 'Reverse sorted'
    SUM = 'Sum'
    AVERAGE_FLOOR = 'Average rounded down'
    AVERAGE_CEIL = 'Average rounded up'

    def modify_dices(self, dices: [Dice]) -> [Dice]:
        if self == self.MIN:
            result = [min(dices)]
        elif self == self.MAX:
            result = [max(dices)]
        elif self == self.SORTED:
            result = sorted(dices)
        elif self == self.REVERSE_SORTED:
            result = sorted(dices, reverse=True)
        elif self == self.SUM:
            result = [sum(dices)]
        elif self == self.AVERAGE_FLOOR:
            value = self.__average(dices)
            result = [Dice(floor(value))]
        elif self == self.AVERAGE_CEIL:
            value = self.__average(dices)
            result = [Dice(ceil(value))]
        elif self == self.NONE:
            result = dices
        else:
            raise Exception
        return result

    @staticmethod
    def __average(dices: [Dice]) -> float:
        return mean(map(int, dices))


class DicesModifierArguments(DicesBasicArguments):
    minimum: bool = False
    maximum: bool = False
    sort: bool = False
    reverse_sort: bool = False
    sum: bool = False
    average_floor = False
    average_ceil = False

    __dices_modifier: DicesModifier = None

    @property
    def dices_modifier(self) -> DicesModifier:
        return self.__resolve_modifier()

    def __resolve_modifier(self) -> Optional[DicesModifier]:
        self._validate_single_value_set(DicesModifierArguments)

        if self.minimum:
            result = DicesModifier.MIN
        elif self.maximum:
            result = DicesModifier.MAX
        elif self.sort:
            result = DicesModifier.SORTED
        elif self.reverse_sort:
            result = DicesModifier.REVERSE_SORTED
        elif self.sum:
            result = DicesModifier.SUM
        elif self.average_floor:
            result = DicesModifier.AVERAGE_FLOOR
        elif self.average_ceil:
            result = DicesModifier.AVERAGE_CEIL
        else:
            result = DicesModifier.NONE
        return result


def add_modifier_arguments(add_argument_callable: Callable, *modifiers: DicesModifier):
    if DicesModifier.MIN in modifiers:
        add_argument_callable('-m', '--min', action='store_true', dest='minimum',
                              help='show min dice')
    if DicesModifier.MAX in modifiers:
        add_argument_callable('-x', '--max', action='store_true', dest='maximum',
                              help='show max dice')
    if DicesModifier.SORTED in modifiers:
        add_argument_callable('-s', '--sort', action='store_true', dest='sort',
                              help='show sorted dices')
    if DicesModifier.REVERSE_SORTED in modifiers:
        add_argument_callable('-r', '--reverse-sort', action='store_true', dest='reverse_sort',
                              help='show reverse sorted dices')
    if DicesModifier.SUM in modifiers:
        add_argument_callable('--sum', action='store_true', dest='sum',
                              help='show sum of dices')
    if DicesModifier.AVERAGE_FLOOR in modifiers:
        add_argument_callable('--average-floor', action='store_true', dest='average_floor',
                              help='show dices average rounded down')
    if DicesModifier.AVERAGE_FLOOR in modifiers:
        add_argument_callable('--average-ceil', action='store_true', dest='average_ceil',
                              help='show dices average rounded up')
