from os import environ
from subprocess import getstatusoutput
from typing import TypeVar, Optional, Final

from fate_of_dice.common.resources_handler import ResourcesHandler

PrefixType = TypeVar('PrefixType', list[str], str)

FATE_OF_DICE_TOKEN: Final[str] = 'FATE_OF_DICE_TOKEN'
FATE_OF_DICE_PREFIX: Final[str] = 'FATE_OF_DICE_PREFIX'
FATE_OF_DICE_SIMPLE_RESULTS: Final[str] = 'FATE_OF_DICE_SIMPLE_PRESENTATION'


def __resolve_command_prefixes() -> [str] or str:
    property_value = ResourcesHandler.get_property(FATE_OF_DICE_PREFIX, ['/', '\\', 'fateOfDice'])
    if not isinstance(property_value, list):
        property_value = property_value.strip('][').split(', ')
    return property_value


def __simple_presentation() -> bool:
    property_value = ResourcesHandler.get_property(FATE_OF_DICE_SIMPLE_RESULTS, False)
    return property_value in [True, 'True']


BOT_TOKEN: Final[str] = ResourcesHandler.get_property(FATE_OF_DICE_TOKEN, None)
COMMAND_PREFIXES: Final[PrefixType] = __resolve_command_prefixes()
SIMPLE_PRESENTATION: Final[bool] = __simple_presentation()


def get_heroku_status() -> Optional[str]:
    if 'DYNO' in environ:
        (status, result) = getstatusoutput("heroku ps -a fate-of-dice")
        return str(result) if status == 0 else None
