from abc import ABC
from dataclasses import dataclass, field
from typing import Optional

from fate_of_dice.common.dice import DicesBasicArguments


@dataclass
class DiceResult(ABC):
    descriptions: [str] = field(default_factory=lambda: [])
    user: Optional[str] = field(default=None)
    simple_presentation: bool = field(default=False)
    priv_request: bool = field(default=False)

    def add_basic_arguments(self, basic_arguments: DicesBasicArguments) -> 'DiceResult':
        self.simple_presentation = basic_arguments.simple_presentation
        self.priv_request = basic_arguments.priv_request
        return self
