from dataclasses import dataclass

from fate_of_dice.common.third_party_wrapper import ArgumentParser

PARSER = ArgumentParser(description='Call of Cthulhu skill check.')

PARSER.add_argument('skill_value',
                    type=int,
                    nargs='?',
                    default=None,
                    help='keeper skill value')
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
PARSER.add_argument('-c', '--comment',
                    nargs='+',
                    help='ignored comment')


@dataclass
class SkillCheckArguments:
    skill_value: int = None
    bonus_dice_amount: int = 0
    penalty_dice_amount: int = 0


def parse(arguments: (str, ...)) -> SkillCheckArguments:
    return PARSER.parse_args(list(arguments), SkillCheckArguments())
