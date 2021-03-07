from dataclasses import dataclass, field

from fate_of_dice.common.dice import DiceArgumentParser, DicesBasicArguments

PARSER = DiceArgumentParser(description='Tales from the Loop roll check.')

PARSER.add_argument('dice_amount',
                    type=int,
                    nargs='?',
                    default=1,
                    help='number of dices to roll (default: 1) ')
PARSER.add_argument('stress_dice_amount',
                    type=int,
                    nargs='?',
                    default=0,
                    help='number of stress dices to roll (default: 0) ')
PARSER.add_comment_argument()
PARSER.add_priv_request()
PARSER.add_simple_presentation()


@dataclass
class SkillCheckArguments(DicesBasicArguments):
    dice_amount: int = field(default=1)
    stress_dice_amount: int = field(default=0)


def parse(command_prefix: str, arguments: (str, ...)) -> SkillCheckArguments:
    PARSER.prog = command_prefix
    return PARSER.parse_args(list(arguments), SkillCheckArguments())
