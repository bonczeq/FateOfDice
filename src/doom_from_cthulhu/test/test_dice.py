from enum import Enum
from doom_from_cthulhu.common import Dice


class DiceType(Enum):
    NONE = 0
    NORMAL = 1
    BONUS = 2
    PENALTY = 3


class OnesDice(Dice):
    def __init__(self):
        super(OnesDice, self).__init__(1, 10)


class TensDice(Dice):
    def __init__(self, dice_type: DiceType = DiceType.NORMAL):
        super(TensDice, self).__init__(0, 9)
        self.value *= 10
        self.dice_type = dice_type
