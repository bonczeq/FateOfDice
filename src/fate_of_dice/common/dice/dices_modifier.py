from enum import Enum
from math import floor, ceil
from statistics import mean
from typing import Optional, Callable

from fate_of_dice.common.dice import Dice
from .dice_argument_parse import DicesBasicArguments


class DicesModifierType(Enum):
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
            raise Exception('Unsupported DicesModifier')
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

    @property
    def dices_modifier(self) -> DicesModifierType:
        return self.__resolve_modifier()

    def __resolve_modifier(self) -> Optional[DicesModifierType]:
        self._validate_single_value_set(DicesModifierArguments)

        if self.minimum:
            result = DicesModifierType.MIN
        elif self.maximum:
            result = DicesModifierType.MAX
        elif self.sort:
            result = DicesModifierType.SORTED
        elif self.reverse_sort:
            result = DicesModifierType.REVERSE_SORTED
        elif self.sum:
            result = DicesModifierType.SUM
        elif self.average_floor:
            result = DicesModifierType.AVERAGE_FLOOR
        elif self.average_ceil:
            result = DicesModifierType.AVERAGE_CEIL
        else:
            result = DicesModifierType.NONE
        return result


def add_modifier_arguments(add_argument_callable: Callable, *modifiers: DicesModifierType):
    if DicesModifierType.MIN in modifiers:
        add_argument_callable('-m', '--min', action='store_true', dest='minimum',
                              help='show min dice')
    if DicesModifierType.MAX in modifiers:
        add_argument_callable('-x', '--max', action='store_true', dest='maximum',
                              help='show max dice')
    if DicesModifierType.SORTED in modifiers:
        add_argument_callable('-s', '--sort', action='store_true', dest='sort',
                              help='show sorted dices')
    if DicesModifierType.REVERSE_SORTED in modifiers:
        add_argument_callable('-r', '--reverse-sort', action='store_true', dest='reverse_sort',
                              help='show reverse sorted dices')
    if DicesModifierType.SUM in modifiers:
        add_argument_callable('--sum', action='store_true', dest='sum',
                              help='show sum of dices')
    if DicesModifierType.AVERAGE_FLOOR in modifiers:
        add_argument_callable('--average-floor', action='store_true', dest='average_floor',
                              help='show dices average rounded down')
    if DicesModifierType.AVERAGE_FLOOR in modifiers:
        add_argument_callable('--average-ceil', action='store_true', dest='average_ceil',
                              help='show dices average rounded up')
