from enum import Enum
from fate_of_dice.common import Dice


class DiceType(Enum):
    MAIN = 1
    BONUS = 2
    PENALTY = 3


class OnesDice(Dice):
    @classmethod
    def roll(cls, **kwargs) -> 'OnesDice':
        min_value = kwargs.get('min_value') or 0
        max_value = kwargs.get('max_value') or 9
        step = kwargs.get('step') or 1

        dice_value = cls.__rand_value__(min_value=min_value, max_value=max_value, step=step)
        return OnesDice(dice_value)


class TensDice(Dice):
    def __init__(self, value: int, dice_type: DiceType = DiceType.MAIN):
        super().__init__(value)
        self.dice_type = dice_type

    @classmethod
    def roll(cls, dice_type: DiceType = DiceType.MAIN, **kwargs) -> 'TensDice':
        min_value = kwargs.get('min_value') or 0
        max_value = kwargs.get('max_value') or 90
        step = kwargs.get('step') or 10

        dice_value = cls.__rand_value__(min_value=min_value, max_value=max_value, step=step)
        return TensDice(dice_value, dice_type)
