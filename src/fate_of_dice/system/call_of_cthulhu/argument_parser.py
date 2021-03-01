from dataclasses import dataclass

from fate_of_dice.common.dice import DiceArgumentParser, DicesBasicArguments

PARSER = DiceArgumentParser(description='Call of Cthulhu skill check.')

PARSER.add_argument('skill_value',
                    type=int,
                    nargs='?',
                    default=None,
                    help='keeper skill value (default: no result verification) ')
PARSER.add_argument('-b', '--bonus',
                    type=int,
                    nargs='?',
                    const='1',
                    dest='bonus_dice_amount',
                    help='amount of bonus dices')
PARSER.add_argument('-p', '--penalty',
                    type=int,
                    nargs='?',
                    const='1',
                    dest='penalty_dice_amount',
                    help='amount of penalty dices')
PARSER.add_comment_argument()
PARSER.add_priv_request()


@dataclass
class SkillCheckArguments(DicesBasicArguments):
    skill_value: int = None
    bonus_dice_amount: int = 0
    penalty_dice_amount: int = 0


def parse(command_prefix: str, arguments: (str, ...)) -> SkillCheckArguments:
    PARSER.prog = command_prefix
    return PARSER.parse_args(list(arguments), SkillCheckArguments())
