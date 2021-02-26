from dataclasses import dataclass

from fate_of_dice.common.third_party_wrapper import ArgumentParser
from .roll_modifier import RollResultModifier

PARSER = ArgumentParser(description='Universal dice roll.')

PARSER.add_argument('dices',
                    type=str,
                    nargs='*',
                    default=['1d100'],
                    help='dices to roll')

GROUP = PARSER.add_argument_group('modifiers')
GROUP.add_argument('-m', '--min',
                   action='store_true',
                   dest='minimum',
                   help='show min dice')
GROUP.add_argument('-x', '--max',
                   action='store_true',
                   dest='maximum',
                   help='show max dice')
GROUP.add_argument('-s', '--sort',
                   action='store_true',
                   dest='sort',
                   help='show sorted dices')
GROUP.add_argument('-r', '--reverse-sort',
                   action='store_true',
                   dest='reverse_sort',
                   help='show reverse sorted dices')
GROUP.add_argument('-u', '--sum',
                   action='store_true',
                   dest='sum',
                   help='show added dices')
GROUP.add_argument('-c', '--comment',
                   nargs='+',
                   help='ignored comment')


@dataclass
class RollArguments:
    dices: [str] = "1d100"
    minimum: bool = False
    maximum: bool = False
    sort: bool = False
    reverse_sort: bool = False
    sum: bool = False

    __modifier: RollResultModifier = None

    @property
    def modifier(self):
        if not self.__modifier:
            self.__modifier = self.__resolve_modifier()
        return self.__modifier

    def __resolve_modifier(self):
        modifier_list: [bool] = [self.minimum, self.maximum, self.sort, self.reverse_sort, self.sum]
        if sum(modifier_list) > 1:
            raise Exception('Unsupported modifiers')

        if self.minimum:
            result = RollResultModifier.MIN
        elif self.maximum:
            result = RollResultModifier.MAX
        elif self.sort:
            result = RollResultModifier.SORTED
        elif self.reverse_sort:
            result = RollResultModifier.REVERSE_SORTED
        elif self.sum:
            result = RollResultModifier.SUM
        else:
            result = RollResultModifier.NONE
        return result


def parse(arguments: (str, ...)) -> RollArguments:
    arguments = PARSER.parse_args(list(arguments), RollArguments())
    return arguments
