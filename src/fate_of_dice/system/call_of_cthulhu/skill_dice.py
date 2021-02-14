from enum import Enum
from fate_of_dice.common import Dice


class DiceType(Enum):
    MAIN = 1
    BONUS = 2
    PENALTY = 3


class OnesDice(Dice):
    def __init__(self, value: int):
        super().__init__(value)

    @classmethod
    def roll(cls, **kwargs) -> 'OnesDice':
        min_value = kwargs.get('min_value') or 0
        max_value = kwargs.get('max_value') or 9
        return Dice.roll(min_value=min_value, max_value=max_value, step=1)


class TensDice(Dice):
    def __init__(self, value: int, dice_type: DiceType = DiceType.MAIN):
        super().__init__(value)
        self.dice_type = dice_type

    @classmethod
    def roll(cls, dice_type: DiceType = DiceType.MAIN, **kwargs) -> 'TensDice':
        min_value = kwargs.get('min_value') or 0
        max_value = kwargs.get('max_value') or 90
        return Dice.roll(min_value=min_value, max_value=max_value, step=10)
