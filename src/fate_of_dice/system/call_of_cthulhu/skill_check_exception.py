from fate_of_dice.common import DiceException


class UnsupportedExtraDiceAmountException(DiceException):
    def __int__(self):
        super().__init__("It is forbidden to roll more than 2 bonus/penalty dices")
