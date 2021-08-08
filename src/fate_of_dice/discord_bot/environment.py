from typing import TypeVar, Iterable, Final

from fate_of_dice.resources.resource_handler import ResourceHandler

PrefixType = TypeVar('PrefixType', Iterable[str], str)

FATE_OF_DICE_TOKEN: Final[str] = 'FATE_OF_DICE_TOKEN'
FATE_OF_DICE_PREFIX: Final[str] = 'FATE_OF_DICE_PREFIX'
FATE_OF_DICE_SIMPLE_RESULTS: Final[str] = 'FATE_OF_DICE_SIMPLE_PRESENTATION'


def __resolve_command_prefixes() -> [str] or str:
    property_value = ResourceHandler.get_property(FATE_OF_DICE_PREFIX, ['!', '\\', 'fateOfDice'])
    if not isinstance(property_value, list):
        property_value = property_value.strip('][').split(', ')
    return property_value


def __simple_presentation() -> bool:
    property_value = ResourceHandler.get_property(FATE_OF_DICE_SIMPLE_RESULTS, False)
    return property_value in [True, 'True']


BOT_TOKEN: Final[str] = ResourceHandler.get_property(FATE_OF_DICE_TOKEN, None)
COMMAND_PREFIXES: Final[PrefixType] = __resolve_command_prefixes()
SIMPLE_PRESENTATION: Final[bool] = __simple_presentation()
