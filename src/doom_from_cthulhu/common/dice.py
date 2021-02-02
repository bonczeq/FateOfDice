from random import randint
import operator
import copy


class Dice:
    def __init__(self, min_value: int, max_value: int):
        self.value: int = randint(min_value, max_value)

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return self.value

    def __add__(self, other):
        new_dice = copy.copy(self)
        new_dice.value = self.value + other.value
        return new_dice

    def __sub__(self, other):
        new_dice = copy.copy(self)
        new_dice.value = self.value - other.value
        return new_dice

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
