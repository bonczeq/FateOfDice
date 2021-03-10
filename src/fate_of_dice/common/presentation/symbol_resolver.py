from typing import Final

from fate_of_dice.common.resource_handler import ResourceHandler


class SymbolResolver:
    _FATE_OF_DICE_PURELY_ASCII: str = 'FATE_OF_DICE_PURELY_ASCII'
    PURELY_ASCII: Final[bool] = {'true': True, 'false': False}.get(
        ResourceHandler.get_property(_FATE_OF_DICE_PURELY_ASCII, False), False)

    @classmethod
    def arrow_character(cls) -> str:
        if cls.PURELY_ASCII:
            return '->'
        else:
            return '🠖'

    @classmethod
    def circled_number(cls, number: int, success: int = None, failure: int = None) -> str:
        result = number
        if cls.PURELY_ASCII:
            result = number
        elif success and number == success:
            result = '🗹'
        elif failure and number == failure:
            result = '🞮'
        elif number in range(1, 10 + 1):
            result = chr(0x2780 + number - 1)
        return result

    @classmethod
    def dice(cls, number: int) -> str:
        result = number
        if number in range(1, 6 + 1) and not cls.PURELY_ASCII:
            result = chr(0x2680 + number - 1)
        return result
