import re
from dataclasses import dataclass

from fate_of_dice.common.dice import Dice, DicesPresentation
from .exception import RollException
from .argument_parser import RollArguments, parse


def roll(user: str, command_prefix: str, arguments: (str, ...)) -> ['RollResult']:
    return Roller(user, command_prefix, arguments).roll()


@dataclass
class RollResult:
    description: str
    result_dices: [Dice]
    all_dices: [Dice]


@dataclass
class RollResults:
    user: str
    presentation: DicesPresentation
    results: [RollResult]


class Roller:
    __DICE_TYPE_PATTERN: re.Pattern = re.compile(r'^(\d+)?[dk]?(\d*)$')

    def __init__(self, user: str, command_prefix: str, arguments: (str, ...)):
        self.__user: str = user
        self.__command_prefix: str = command_prefix
        self.__arguments: RollArguments = parse(command_prefix, arguments)

    def roll(self) -> RollResults:
        results = [self.__calculate_result(dices_pattern) for dices_pattern in self.__arguments.dices]
        return RollResults(user=self.__user, presentation=self.__arguments.presentation, results=results)

    def __calculate_result(self, dices_pattern: str) -> RollResult:
        all_dices = self.__resolve_dices(dices_pattern)
        result_dices = self.__arguments.presentation.modify_dices(all_dices)
        description = self.__resolve_description(result_dices, all_dices)

        return RollResult(result_dices=result_dices, all_dices=all_dices, description=description)

    @classmethod
    def __resolve_dices(cls, dices_pattern: str) -> [Dice]:
        matches = cls.__DICE_TYPE_PATTERN.match(dices_pattern)
        if not matches:
            raise RollException(f'Unsupported dice type: {dices_pattern}')

        groups: [str] = matches.groups()
        dice_amount: int = int(groups[0]) if (groups[0] and groups[1]) else 1
        dice_range: int = int(groups[1]) if groups[1] else int(groups[0])

        if dice_amount < 1:
            raise RollException(f'Dice amount must be positive, but is: {dice_amount}')

        return [Dice.roll(1, dice_range) for _ in range(0, dice_amount)]

    @staticmethod
    def __resolve_description(result_dices: [Dice], all_dices: [Dice]) -> str:
        if len(all_dices) == 1:
            return str(result_dices[0])
        elif len(result_dices) == 1:
            return f'[{", ".join([str(dice) for dice in all_dices])}] 🠖 {str(result_dices[0])}'
        else:
            return f'[{", ".join([str(dice) for dice in result_dices])}]'
