from dataclasses import dataclass, field

from fate_of_dice.common.dice import DiceArgumentParser
from fate_of_dice.common.dice import DicesFilterArguments, DicesFilterType, add_filter_arguments
from fate_of_dice.common.dice import DicesModifierArguments, DicesModifierType, add_modifier_arguments

_PARSER = DiceArgumentParser(description='Universal dice roll.')

_PARSER.add_argument('dices',
                     type=str,
                     nargs='*',
                     default=['1d100'],
                     help='rolls description (default: 1d100)')
_PARSER.add_arguments_with_function(lambda parser: parser.add_mutually_exclusive_group(),
                                    add_filter_arguments, DicesFilterType.UPPER_THAN, DicesFilterType.LOWER_THAN)
_PARSER.add_arguments_with_function(lambda parser: parser.add_mutually_exclusive_group(),
                                    add_modifier_arguments,
                                    DicesModifierType.MIN, DicesModifierType.MAX, DicesModifierType.SORTED,
                                    DicesModifierType.REVERSE_SORTED,
                                    DicesModifierType.SUM, DicesModifierType.AVERAGE_FLOOR,
                                    DicesModifierType.AVERAGE_CEIL)
_PARSER.add_comment_argument()
_PARSER.add_priv_request()
_PARSER.add_simple_presentation()


@dataclass
class RollArguments(DicesModifierArguments, DicesFilterArguments):
    dices: [str] = field(default="1d100")


def parse(command_prefix: str, arguments: (str, ...)) -> RollArguments:
    _PARSER.prog = command_prefix
    return _PARSER.parse_args(list(arguments), RollArguments())
