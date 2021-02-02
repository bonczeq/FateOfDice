import re
from .test_dice import TensDice, DiceType
from doom_from_cthulhu.common.dice import Dice
from doom_from_cthulhu.common.lazy_developer_exception import LazyDeveloperException


class ExtraTestDices:
    def __init__(self, extra_dices_pattern: str):
        self.dices: [Dice] = []
        self.dices_type: DiceType = DiceType.NONE

        if not extra_dices_pattern:
            return

        (self.dices_type, self.dices) = self.__parse_extra_dices(extra_dices_pattern)

    def chose_dice(self, main_dice: TensDice) -> TensDice:
        if main_dice.dice_type != DiceType.NORMAL:
            raise LazyDeveloperException

        if self.dices_type == DiceType.PENALTY:
            return max([main_dice] + self.dices)
        elif self.dices_type == DiceType.BONUS:
            return min([main_dice] + self.dices)
        else:
            return main_dice

    def __parse_extra_dices(self, extra_dices_pattern: str) -> (DiceType, [TensDice]):
        extra_dices_part = re.search(r'^(\d*[bpk])(\d*[bpk])?$', extra_dices_pattern)
        if not extra_dices_part:
            raise LazyDeveloperException.of_incorrect_format(extra_dices_pattern)

        bonus_dice_amount = 0
        penalty_dice_amount = 0

        groups = [group for group in extra_dices_part.groups() if group]
        for extra_dice_part in groups:
            (dice_type, dice_amount) = self.__parse_extra_dices_part(extra_dice_part)
            if dice_type == DiceType.BONUS:
                bonus_dice_amount = dice_amount
            elif dice_type == DiceType.PENALTY:
                penalty_dice_amount = dice_amount

        return self.__roll_dices(bonus_dice_amount, penalty_dice_amount)

    def __parse_extra_dices_part(self, extra_dices_part_pattern: str) -> (DiceType, int):
        extra_dices_part = re.search(r'^(\d*)([bpk])$', extra_dices_part_pattern)
        if not extra_dices_part:
            raise LazyDeveloperException.of_incorrect_format(extra_dices_part_pattern)

        groups = extra_dices_part.groups()
        dice_amount = int(groups[0]) if groups[0].isdigit() else 1
        dice_type = self.__parse_dice_type(groups[1])
        return dice_type, dice_amount

    @staticmethod
    def __parse_dice_type(dice_type_pattern: str):
        if dice_type_pattern == 'b':
            return DiceType.BONUS
        elif dice_type_pattern == 'p' or 'k':
            return DiceType.PENALTY
        else:
            raise LazyDeveloperException('Unknown type of extra dice')

    @staticmethod
    def __roll_dices(bonus_dices_amount: int, penalty_dices_amount: int) -> (DiceType, [TensDice]):
        amount = bonus_dices_amount - penalty_dices_amount

        if amount == 0:
            dice_type = DiceType.NONE
        elif amount > 0:
            dice_type = DiceType.BONUS
        else:
            dice_type = DiceType.PENALTY

        return dice_type, [TensDice(dice_type) for _ in range(abs(amount))]
