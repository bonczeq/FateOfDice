import re
from dataclasses import dataclass

from fate_of_dice.common import Dice
from .exception import RollException
from .argument_parser import RollArguments, parse
from .roll_modifier import RollResultModifier


def roll(user: str, arguments: (str, ...)) -> ['RollResult']:
    return Roller(user, arguments).roll()


@dataclass
class RollResult:
    user: str
    description: str
    result: [Dice]
    all_results: [Dice]
    modifier: RollResultModifier


class Roller:
    __DICE_TYPE_PATTERN: re.Pattern = re.compile(r'^(\d+)?[dk]?(\d*)$')

    def __init__(self, user: str, arguments: (str, ...)):
        self.__user: str = user
        self.__arguments: RollArguments = parse(arguments)

    def roll(self) -> [RollResult]:
        results: [RollResult] = []

        for dices_pattern in self.__arguments.dices:
            modifier = self.__arguments.modifier
            all_dices = self.__resolve_dices(dices_pattern)
            modified_dices = modifier.modify_dices(all_dices)
            description = self.__resolve_description(modified_dices, all_dices)

            roll_result = RollResult(result=modified_dices, description=description,
                                     modifier=modifier, all_results=all_dices, user=self.__user)
            results.append(roll_result)

        return results

    @classmethod
    def __resolve_dices(cls, dices_pattern: str) -> [Dice]:
        matches = cls.__DICE_TYPE_PATTERN.match(dices_pattern)
        if not matches:
            raise RollException(f'Unsupported dice type: {dices_pattern}')

        groups: [str] = matches.groups()
        dice_amount: int = int(groups[0]) if groups[0] else 1
        dice_range: int = int(groups[1])

        if dice_amount < 1:
            raise RollException(f'Dice amount must be positive, but is: {dice_amount}')

        return [Dice.roll(1, dice_range) for _ in range(0, dice_amount)]

    @classmethod
    def __resolve_description(cls, modified_dices: [Dice], all_dices: [Dice]) -> str:
        if len(modified_dices) > 1:
            return f'[{", ".join([str(dice) for dice in modified_dices])}]'
        else:
            return f'[{", ".join([str(dice) for dice in all_dices])}] => {str(modified_dices[0])}'
