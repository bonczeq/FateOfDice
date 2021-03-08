from dataclasses import dataclass, field

from fate_of_dice.common.dice import DiceArgumentParser
from fate_of_dice.common.dice import DicesModifierArguments, DicesModifier, add_modifier_arguments
from fate_of_dice.common.dice import DicesFilterArguments, DicesFilterType, add_filter_arguments

PARSER = DiceArgumentParser(description='Universal dice roll.')

PARSER.add_argument('dices',
                    type=str,
                    nargs='*',
                    default=['1d100'],
                    help='rolls description (default: 1d100)')
PARSER.add_arguments_with_function(lambda parser: parser.add_mutually_exclusive_group(),
                                   add_filter_arguments, DicesFilterType.UPPER_THAN, DicesFilterType.LOWER_THAN)
PARSER.add_arguments_with_function(lambda parser: parser.add_mutually_exclusive_group(),
                                   add_modifier_arguments,
                                   DicesModifier.MIN, DicesModifier.MAX, DicesModifier.SORTED,
                                   DicesModifier.REVERSE_SORTED,
                                   DicesModifier.SUM, DicesModifier.AVERAGE_FLOOR, DicesModifier.AVERAGE_CEIL)
PARSER.add_comment_argument()
PARSER.add_priv_request()
PARSER.add_simple_presentation()


@dataclass
class RollArguments(DicesModifierArguments, DicesFilterArguments):
    dices: [str] = field(default="1d100")


def parse(command_prefix: str, arguments: (str, ...)) -> RollArguments:
    PARSER.prog = command_prefix
    return PARSER.parse_args(list(arguments), RollArguments())
