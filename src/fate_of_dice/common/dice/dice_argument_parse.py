import argparse
from abc import ABC
from typing import Callable
from dataclasses import dataclass, field

from fate_of_dice.common.exception import DiceException


class DiceArgumentParserException(DiceException):
    pass


class DiceArgumentParserHelpException(DiceArgumentParserException):
    pass


@dataclass
class DicesBasicArguments(ABC):
    simple_presentation: bool = field(default=False)
    priv_request: bool = field(default=False)

    def _validate_single_value_set(self, class_type: type) -> None:
        names = class_type.__annotations__.keys()
        values = [self.__getattribute__(name) for name in names if name]
        set_values = [value for value in values if value]

        if len(set_values) > 1:
            raise Exception('Only single value is supported')


class DiceArgumentParser(argparse.ArgumentParser):

    def print_help(self, file=None) -> None:
        raise DiceArgumentParserHelpException(self.format_help())

    def error(self, message) -> None:
        raise DiceArgumentParserException(message + '\n\n' + self.format_help())

    def add_arguments_with_function(self, argument_container, adding_function: Callable, *adding_arguments):
        if callable(argument_container):
            argument_container = argument_container(self)
        adding_function(argument_container.add_argument, *adding_arguments)

    def add_priv_request(self):
        return self.add_argument('--priv', action='store_true', dest='priv_request',
                                 help=argparse.SUPPRESS)

    def add_simple_presentation(self):
        return self.add_argument('--simple', action='store_true', dest='simple_presentation',
                                 help=argparse.SUPPRESS)

    def add_comment_argument(self):
        return self.add_argument('-c', '--comment', nargs='+',
                                 help='ignored comment')
