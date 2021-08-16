import re
from dataclasses import dataclass, field

from fate_of_dice.common import DiceException
from fate_of_dice.common.dice import Dice, DicesModifierType, DicesFilterType
from fate_of_dice.system import DiceResult
from .argument_parser import RollArguments, parse


def roll(user: str, command_prefix: str, arguments: (str, ...)) -> 'RollResult':
    return _Roller(user, command_prefix, arguments).roll()


@dataclass(frozen=True)
class RollResult(DiceResult):
    all_dices: [[Dice]] = field(default_factory=list)
    dices_modifier: DicesModifierType = field(default=DicesModifierType.NONE)
    dices_filter: DicesFilterType = field(default=DicesFilterType.NONE)
    result_dices: [[Dice]] = field(default_factory=list)


class _Roller:
    __DICE_TYPE_PATTERN: re.Pattern = re.compile(r'^(\d+)?[dk]?(\d*)$')

    def __init__(self, user: str, command_prefix: str, arguments: (str, ...)):
        self.__user: str = user
        self.__arguments: RollArguments = parse(command_prefix, arguments)

    def roll(self) -> RollResult:
        calculated_results = [self.__calculate_result(dices_pattern) for dices_pattern in self.__arguments.dices]

        result_dices = [calculated[0] for calculated in calculated_results]
        all_dices = [calculated[1] for calculated in calculated_results]
        descriptions = [calculated[2] for calculated in calculated_results]

        return RollResult(user=self.__user, result_dices=result_dices, descriptions=descriptions, all_dices=all_dices,
                          dices_modifier=self.__arguments.dices_modifier,
                          dices_filter=self.__arguments.dices_filter.type,
                          basic_arguments=self.__arguments)

    def __calculate_result(self, dices_pattern: str) -> ([Dice], [Dice], str):
        all_dices = self.__resolve_dices(dices_pattern)
        filtered_dices = self.__arguments.dices_filter.filter_dices(all_dices)
        result_dices = self.__arguments.dices_modifier.modify_dices(filtered_dices)
        description = self.__resolve_description(result_dices, all_dices)

        return result_dices, all_dices, description

    @classmethod
    def __resolve_dices(cls, dices_pattern: str) -> [Dice]:
        matches = cls.__DICE_TYPE_PATTERN.match(dices_pattern)
        if not matches:
            raise DiceException(f'Unsupported dice type: {dices_pattern}')

        groups: [str] = matches.groups()
        dice_amount: int = int(groups[0]) if (groups[0] and groups[1]) else 1
        dice_range: int = int(groups[1]) if groups[1] else int(groups[0])

        if dice_amount < 1:
            raise DiceException(f'Dice amount must be positive, but is: {dice_amount}')

        return [Dice.roll(1, dice_range) for _ in range(0, dice_amount)]

    @staticmethod
    def __resolve_description(result_dices: [Dice], all_dices: [Dice]) -> str:
        if len(all_dices) == 1:
            return str(result_dices[0])
        elif len(result_dices) == 1:
            return f'[{", ".join([str(dice) for dice in all_dices])}] 🠖 {str(result_dices[0])}'
        elif result_dices != all_dices:
            return f'[{", ".join([str(d) for d in all_dices])}] 🠖 [{", ".join([str(d) for d in result_dices])}]'
        else:
            return f'{", ".join([str(dice) for dice in result_dices])}'
