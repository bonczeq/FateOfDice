from random import randrange
import operator


class Dice:

    @classmethod
    def roll(cls, min_value: int, max_value: int, step: int = 1):
        dice_value = cls.__rand_value__(min_value, max_value, step)
        return cls(dice_value)

    def __init__(self, value: int):
        self.value: int = value

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return self.value

    def __add__(self, other):
        new_value = self.value + int(other)
        return Dice(new_value)

    def __sub__(self, other):
        new_value = self.value - int(other)
        return Dice(new_value)

    def __lt__(self, other):
        return operator.lt(self.value, other)

    def __le__(self, other):
        return operator.le(self.value, other)

    def __gt__(self, other):
        return operator.gt(self.value, other)

    def __ge__(self, other):
        return operator.ge(self.value, other)

    def __eq__(self, other):
        return operator.eq(self.value, other)

    def __ne__(self, other):
        return operator.ne(self.value, other)

    @staticmethod
    def __rand_value__(min_value: int, max_value: int, step: int):
        return randrange(min_value, max_value + 1, step)
