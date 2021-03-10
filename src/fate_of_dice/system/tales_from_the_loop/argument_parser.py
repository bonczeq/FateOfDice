from dataclasses import dataclass, field

from fate_of_dice.common.dice import DiceArgumentParser, DicesBasicArguments

_PARSER = DiceArgumentParser(description='Tales from the Loop roll check.')

_PARSER.add_argument('dice_amount',
                     type=int,
                     choices=range(1, 50 + 1),
                     metavar='dice amount',
                     nargs='?',
                     default=1,
                     help='number of dices to roll (default: 1) ')
_PARSER.add_argument('success_requirement',
                     type=int,
                     choices=range(1, 50 + 1),
                     metavar='required number of successes',
                     nargs='?',
                     default=1,
                     help='number of dices to success (default: 1) ')
_PARSER.add_comment_argument()
_PARSER.add_priv_request()
_PARSER.add_simple_presentation()


@dataclass
class OvercomeTroubleArguments(DicesBasicArguments):
    dice_amount: int = field(default=1)
    success_requirement: int = field(default=1)


def parse(command_prefix: str, arguments: (str, ...)) -> OvercomeTroubleArguments:
    _PARSER.prog = command_prefix
    return _PARSER.parse_args(list(arguments), OvercomeTroubleArguments())
