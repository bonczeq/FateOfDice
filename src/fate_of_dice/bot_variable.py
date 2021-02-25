from typing import Final
from fate_of_dice.common.resources_handler import ResourcesHandler

FATE_OF_DICE_TOKEN: Final[str] = 'FATE_OF_DICE_TOKEN'
FATE_OF_DICE_PREFIX: Final[str] = 'FATE_OF_DICE_PREFIX'
FATE_OF_DICE_SIMPLE_RESULTS: Final[str] = 'FATE_OF_DICE_SIMPLE_PRESENTATION'


def __resolve_command_prefixes() -> [str] or str:
    property_value = ResourcesHandler.get_property(FATE_OF_DICE_PREFIX, ['/', '\\', 'fateOfDice'])
    if not isinstance(COMMAND_PREFIXES, list):
        property_value = property_value.strip('][').split(', ')
    return property_value


def __simple_presentation() -> bool:
    property_value = ResourcesHandler.get_property(FATE_OF_DICE_SIMPLE_RESULTS, False)
    return property_value in [True, 'True']


BOT_TOKEN: Final[str] = ResourcesHandler.get_property(FATE_OF_DICE_TOKEN, None)
COMMAND_PREFIXES: Final[[str] or str] = __resolve_command_prefixes()
SIMPLE_PRESENTATION: Final[bool] = __simple_presentation()
