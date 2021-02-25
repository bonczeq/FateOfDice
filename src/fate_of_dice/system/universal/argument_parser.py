from dataclasses import dataclass

from fate_of_dice.common.third_party_wrapper import ArgumentParser
from .roll_modifier import RollResultModifier

PARSER = ArgumentParser(description='Universal dice roll.')

PARSER.add_argument('dices',
                    type=str,
                    nargs='*',
                    default='1d100',
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
GROUP.add_argument('-c', '--comment',
                   nargs='+',
                   help='ignored comment')


@dataclass
class RollArguments:
    dices: str = '1d100'
    minimum: bool = False
    maximum: bool = False
    sort: bool = False
    reverse_sort: bool = False
    modifier: RollResultModifier = RollResultModifier.NONE

    def resolve_modifier(self) -> None:
        modifier_list: [bool] = [self.minimum, self.maximum, self.sort, self.reverse_sort]
        if sum(modifier_list) > 1:
            raise Exception('Unsupported modifiers')

        if self.minimum:
            self.modifier = RollResultModifier.MIN
        elif self.maximum:
            self.modifier = RollResultModifier.MAX
        elif self.sort:
            self.modifier = RollResultModifier.SORTED
        elif self.reverse_sort:
            self.modifier = RollResultModifier.REVERSE_SORTED


def parse(arguments: (str, ...)) -> RollArguments:
    arguments = PARSER.parse_args(list(arguments), RollArguments())
    arguments.resolve_modifier()
    return arguments
