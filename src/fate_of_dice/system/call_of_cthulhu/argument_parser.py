from dataclasses import dataclass, field

from fate_of_dice.common.dice import DiceArgumentParser, DicesBasicArguments

_PARSER = DiceArgumentParser(description='Call of Cthulhu skill check.')

_PARSER.add_argument('skill_value',
                     type=int,
                     choices=range(1, 100 + 1),
                     metavar='skill value',
                     nargs='?',
                     help='keeper skill value (default: no result verification) ')
_PARSER.add_argument('-b', '--bonus',
                     type=int,
                     choices=range(1, 10 + 1),
                     metavar='amount',
                     nargs='?',
                     const='1',
                     dest='bonus_dice_amount',
                     help='amount of bonus dices')
_PARSER.add_argument('-p', '--penalty',
                     type=int,
                     choices=range(1, 10 + 1),
                     metavar='amount',
                     nargs='?',
                     const='1',
                     dest='penalty_dice_amount',
                     help='amount of penalty dices')
_PARSER.add_comment_argument()
_PARSER.add_priv_request()
_PARSER.add_simple_presentation()


@dataclass
class SkillCheckArguments(DicesBasicArguments):
    skill_value: int = field(default=None)
    bonus_dice_amount: int = field(default=0)
    penalty_dice_amount: int = field(default=0)


def parse(command_prefix: str, arguments: (str, ...)) -> SkillCheckArguments:
    _PARSER.prog = command_prefix
    return _PARSER.parse_args(list(arguments), SkillCheckArguments())
