from abc import ABC
from dataclasses import dataclass, field, InitVar
from datetime import datetime
from typing import Optional

from fate_of_dice.common.dice import DicesBasicArguments


@dataclass(frozen=True)
class DiceResult(ABC):
    comment: Optional[str] = field(default=None)
    time: str = field(default=datetime.now().strftime("%H:%M:%S"))
    descriptions: [str] = field(default_factory=list)
    user: Optional[str] = field(default=None)
    simple_presentation: bool = field(default=False)
    priv_request: bool = field(default=False)
    basic_arguments: InitVar[DicesBasicArguments] = None

    def to_directory(self) -> dict:
        return {
            'comment': self.comment,
            'time': self.time,
            'user': self.user,
            'descriptions': self.descriptions,
            'simplePresentation': self.simple_presentation,
            'privRequest': self.priv_request
        }

    def __post_init__(self, basic_arguments):
        if basic_arguments:
            object.__setattr__(self, 'comment', basic_arguments.comment)
            object.__setattr__(self, 'time', basic_arguments.time)
            object.__setattr__(self, 'simple_presentation', basic_arguments.simple_presentation)
            object.__setattr__(self, 'priv_request', basic_arguments.priv_request)
