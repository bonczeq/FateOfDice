from abc import ABC, abstractmethod

from fate_of_dice.common import DiceException
from fate_of_dice.system import DiceResult


class RestRollStrategy(ABC):
    REST_ROLL_STRATEGY_PROPERTY_NAME: str = 'RestRollStrategyProperty'

    @abstractmethod
    def execute(self, request_dict: dict, dice_result: DiceResult):
        pass

    @abstractmethod
    def on_error(self, request_dict: dict, error: DiceException):
        pass
