from dataclasses import dataclass, field

from fate_of_dice.common.dice import DiceArgumentParser, DicesBasicArguments

_PARSER = DiceArgumentParser(description='Tales from the Loop roll check.')

_PARSER.add_argument('dice_amount',
                     type=int,
                     choices=range(1, 50 + 1),
                     metavar='base dice amount',
                     nargs='?',
                     default=1,
                     help='number of dices to roll (default: 1) ')
_PARSER.add_argument('stress_dice_amount',
                     type=int,
                     choices=range(1, 50 + 1),
                     metavar='stress dice amount',
                     nargs='?',
                     default=0,
                     help='number of stress dices to roll (default: 0) ')
_PARSER.add_comment_argument()
_PARSER.add_priv_request()
_PARSER.add_simple_presentation()


@dataclass
class ActionCheckArguments(DicesBasicArguments):
    dice_amount: int = field(default=1)
    stress_dice_amount: int = field(default=0)


def parse(command_prefix: str, arguments: (str, ...)) -> ActionCheckArguments:
    _PARSER.prog = command_prefix
    return _PARSER.parse_args(list(arguments), ActionCheckArguments())
