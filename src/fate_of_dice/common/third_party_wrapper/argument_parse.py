import argparse

from fate_of_dice.common.exception import DiceException


class ArgumentParserException(DiceException):
    pass


class ArgumentParser(argparse.ArgumentParser):

    def print_help(self, file=None) -> None:
        raise ArgumentParserException(self.format_help())

    def error(self, message):
        raise ArgumentParserException(message + '\n\n' + self.format_help())
