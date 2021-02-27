from enum import Enum
from abc import ABC

from fate_of_dice.common.dice import Dice


class DicesPresentation(Enum):
    NONE = None
    MIN = 'Minimum'
    MAX = 'Maximum'
    SORTED = 'Sorted'
    REVERSE_SORTED = 'Reverse sorted'
    SUM = 'Sum'

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
        else:
            result = dices
        return result


class DiceArguments(ABC):
    minimum: bool = False
    maximum: bool = False
    sort: bool = False
    reverse_sort: bool = False
    sum: bool = False

    __presentation: DicesPresentation = None

    @property
    def presentation(self):
        if not self.__presentation:
            self.__presentation = self.__resolve_presentation()
        return self.__presentation

    def __resolve_presentation(self):
        presentation_list: [bool] = [self.minimum, self.maximum, self.sort, self.reverse_sort, self.sum]
        if sum(presentation_list) > 1:
            raise Exception('Unsupported presentation request')

        if self.minimum:
            result = DicesPresentation.MIN
        elif self.maximum:
            result = DicesPresentation.MAX
        elif self.sort:
            result = DicesPresentation.SORTED
        elif self.reverse_sort:
            result = DicesPresentation.REVERSE_SORTED
        elif self.sum:
            result = DicesPresentation.SUM
        else:
            result = DicesPresentation.NONE
        return result
