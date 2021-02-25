from enum import Enum

from fate_of_dice.common import Dice


class RollResultModifier(Enum):
    NONE = 'None'
    MIN = 'Minimum'
    MAX = 'Maximum'
    SORTED = 'Sorted'
    REVERSE_SORTED = 'Reverse sorted'

    def modify_dices(self, dices: [Dice]) -> [Dice]:
        if self == self.MIN:
            result = [min(dices)]
        elif self == self.MAX:
            result = [max(dices)]
        elif self == self.SORTED:
            result = sorted(dices)
        elif self == self.REVERSE_SORTED:
            result = sorted(dices, reverse=True)
        else:
            result = dices
        return result
