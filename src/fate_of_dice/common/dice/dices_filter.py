from enum import Enum
from dataclasses import dataclass
from typing import Optional, Callable

from fate_of_dice.common.dice import Dice, DicesBasicArguments


class DicesFilterType(Enum):
    NONE = None
    EQUAL = 'Equal to value'
    UPPER_THAN = 'Upper than value'
    LOWER_THAN = 'Lower than value'

    def filter_dices(self, dices: [Dice], value: Optional[int]) -> [Dice]:
        if self == self.EQUAL:
            result = [dice for dice in dices if value is None or value == dice]
        elif self == self.UPPER_THAN:
            result = [dice for dice in dices if value is None or value < dice]
        elif self == self.LOWER_THAN:
            result = [dice for dice in dices if value is None or value > dice]
        elif self == self.NONE:
            result = dices
        else:
            raise Exception
        return result


@dataclass
class DicesFilter:
    type: DicesFilterType
    value: Optional[int]

    def filter_dices(self, dices: [Dice]) -> [Dice]:
        return self.type.filter_dices(dices, self.value)


class DicesFilterArguments(DicesBasicArguments):
    equal: int = None
    upper_than: int = None
    lower_than: int = None

    @property
    def dices_filter(self) -> DicesFilter:
        self._validate_single_value_set(DicesFilterArguments)

        if self.equal:
            result = DicesFilter(DicesFilterType.EQUAL, self.equal)
        elif self.upper_than:
            result = DicesFilter(DicesFilterType.UPPER_THAN, self.upper_than)
        elif self.lower_than:
            result = DicesFilter(DicesFilterType.LOWER_THAN, self.lower_than)
        else:
            result = DicesFilter(DicesFilterType.NONE, None)
        return result


def add_filter_arguments(add_argument_callable: Callable, *filters: DicesFilterType):
    if DicesFilterType.UPPER_THAN in filters:
        add_argument_callable('-e', '--equal', type=int, choices=range(0, 1000), dest='equal',
                              metavar='value', help='show dices equal to given value')
    if DicesFilterType.UPPER_THAN in filters:
        add_argument_callable('--upper-than', type=int, choices=range(0, 1000), dest='upper_than',
                              metavar='value', help='show dices upper than given value')
    if DicesFilterType.LOWER_THAN in filters:
        add_argument_callable('--lower-than', type=int, choices=range(0, 1000), dest='lower_than',
                              metavar='value', help='show dices lower than given value')
