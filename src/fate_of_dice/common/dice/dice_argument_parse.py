import argparse
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, tzinfo
from dateutil import tz
from typing import Callable, Optional, Any

from fate_of_dice.common.exception import DiceException


class DiceArgumentParserException(DiceException):
    pass


class DiceArgumentParserHelpException(DiceArgumentParserException):
    pass


@dataclass
class DicesBasicArguments(ABC):
    time_zone: Optional[tzinfo] = field(default=None)
    time: str = field(default=datetime.now().strftime("%H:%M:%S"))
    comment: Optional[str] = field(default=None)
    simple_presentation: bool = field(default=False)
    priv_request: bool = field(default=False)

    def fill_from_directory(self, directory: dict[str, Any]) -> 'DicesBasicArguments':
        self.time_zone = tz.gettz(directory.get('timeZone'))
        self.time = datetime.fromtimestamp(directory.get('time', self.time), self.time_zone).strftime("%H:%M:%S")
        self.comment = directory.get('comment', self.comment)
        self.simple_presentation = directory.get('simplePresentation', self.simple_presentation)
        self.priv_request = directory.get('privRequest', self.priv_request)
        return self

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
        return self.add_argument('--priv', '--private', action='store_true', dest='priv_request',
                                 help=argparse.SUPPRESS)

    def add_simple_presentation(self):
        return self.add_argument('--simple', action='store_true', dest='simple_presentation',
                                 help=argparse.SUPPRESS)

    def add_comment_argument(self):
        return self.add_argument('--comment', type=str, nargs='?', metavar='text', dest='comment',
                                 help='ignored comment')
