from dataclasses import dataclass

from fate_of_dice.common.third_party_wrapper import ArgumentParser
from fate_of_dice.common.dice.dices_presentation import DiceArguments

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
class RollArguments(DiceArguments):
    dices: [str] = "1d100"


def parse(command_prefix: str, arguments: (str, ...)) -> RollArguments:
    PARSER.prog = command_prefix
    return PARSER.parse_args(list(arguments), RollArguments())
