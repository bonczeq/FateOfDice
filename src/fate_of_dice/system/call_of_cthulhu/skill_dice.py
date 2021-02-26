from enum import Enum
from fate_of_dice.common import Dice


class DiceType(Enum):
    MAIN = 1
    BONUS = 2
    PENALTY = 3


class OnesDice(Dice):
    @classmethod
    def roll(cls, min_value: int = 0, max_value: int = 9, step: int = 1) -> 'OnesDice':
        dice_value = cls.__rand_value__(min_value=min_value, max_value=max_value, step=step)
        return OnesDice(dice_value)


class TensDice(Dice):
    def __init__(self, value: int, dice_type: DiceType = DiceType.MAIN):
        super().__init__(value)
        self.dice_type = dice_type

    @classmethod
    def roll(cls, dice_type: DiceType = DiceType.MAIN,
             min_value: int = 0, max_value: int = 90, step: int = 10) -> 'TensDice':
        dice_value = cls.__rand_value__(min_value=min_value, max_value=max_value, step=step)
        return TensDice(dice_value, dice_type)
