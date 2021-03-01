from dataclasses import dataclass

from fate_of_dice.common.dice import DiceArgumentParser, DicesBasicArguments

PARSER = DiceArgumentParser(description='Tales from the Loop roll check.')

PARSER.add_argument('dice_amount',
                    type=int,
                    nargs='?',
                    default=1,
                    help='number of dice to roll (default: 1) ')
PARSER.add_argument('success_requirement',
                    type=int,
                    nargs='?',
                    default=1,
                    help='number of dice to success (default: 1) ')
PARSER.add_comment_argument()
PARSER.add_priv_request()


@dataclass
class RollCheckArguments(DicesBasicArguments):
    dice_amount: int = 1
    success_requirement: int = 1


def parse(command_prefix: str, arguments: (str, ...)) -> RollCheckArguments:
    PARSER.prog = command_prefix
    return PARSER.parse_args(list(arguments), RollCheckArguments())
