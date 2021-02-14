from fate_of_dice.common import ArgumentParser

parser = ArgumentParser(description='Call of Cthulhu skill check.')

parser.add_argument('skill_value',
                    type=int,
                    help='keeper current skill value')
parser.add_argument('-b', '--bonus',
                    type=int,
                    nargs='?',
                    const='1',
                    dest='bonus_dice_amount',
                    help='amount of bonus dices')
parser.add_argument('-p', '--penalty',
                    type=int,
                    nargs='?',
                    const='1',
                    dest='penalty_dice_amount',
                    help='amount of penalty dices')
parser.add_argument('-c', '--comment',
                    nargs='+',
                    help='ignored comment')


class SkillCheckArguments:
    def __init__(self):
        self.skill_value: int = 0
        self.bonus_dice_amount: int = 0
        self.penalty_dice_amount: int = 0


def parse(arguments: (str, ...)) -> SkillCheckArguments:
    return parser.parse_args(list(arguments), SkillCheckArguments())
