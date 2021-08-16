from pathlib import Path
from typing import Optional, Final

import requests

from .resource_handler import ResourceHandler, _RESOURCES_PATH, _get_resource_path

_FATE_OF_DICE_URL_ICONS: Final[str] = 'FATE_OF_DICE_URL_ICONS'
_FATE_OF_DICE_URL_ICONS_URL: Final[str] = 'FATE_OF_DICE_URL_ICONS_URL'
_URL_ICONS: Final[bool or None] = {'true': True, 'false': False}.get(
    ResourceHandler.get_property(_FATE_OF_DICE_URL_ICONS, None), None)

_ICON_PATH: Final[Path] = _RESOURCES_PATH.joinpath('icons')

_DEFAULT_ICONS_URL = 'https://raw.githubusercontent.com/bonczeq/FateOfDice/master/src/fate_of_dice/resources/icons/'
_ICONS_URL_PREFIX: Final[str] = ResourceHandler.get_property(_FATE_OF_DICE_URL_ICONS_URL, _DEFAULT_ICONS_URL)


def _icon(url: Optional[str], path: Path):
    result = url or path
    if not _URL_ICONS and _URL_ICONS is str:
        result = path
    return result


def _get_image_url(icon_name: str) -> Optional[str]:
    url: str = _ICONS_URL_PREFIX + icon_name
    response = requests.get(url)
    return url if response.status_code == 200 else None


def _get_resources_path(sub_path: Optional[str] = None) -> Path:
    return _get_resource_path(_ICON_PATH, sub_path)


class ResourceImageHandler(ResourceHandler):
    URL_ICONS = _URL_ICONS

    @classmethod
    def get_resources_path(cls, sub_path: Optional[str] = None) -> Path:
        return _get_resources_path(sub_path)

    @classmethod
    def get_image_url(cls, icon_name: str) -> Optional[str]:
        return _get_image_url(icon_name)

    _FATE_OF_DICE_IMAGE_NAME: Final[str] = 'fate_of_dice.png'
    FATE_OF_DICE_IMAGE_PATH: Final[Path] = _get_resources_path(_FATE_OF_DICE_IMAGE_NAME)
    FATE_OF_DICE_IMAGE_URL: Final[str or None] = _get_image_url(_FATE_OF_DICE_IMAGE_NAME)
    FATE_OF_DICE_IMAGE: Final[str or Path] = _icon(FATE_OF_DICE_IMAGE_URL, FATE_OF_DICE_IMAGE_PATH)

    _CRITICAL_SUCCESS_IMAGE_NAME: Final[str] = 'critical_success.png'
    CRITICAL_SUCCESS_IMAGE_PATH: Final[Path] = _get_resources_path(_CRITICAL_SUCCESS_IMAGE_NAME)
    CRITICAL_SUCCESS_IMAGE_URL: Final[str or None] = _get_image_url(_CRITICAL_SUCCESS_IMAGE_NAME)
    CRITICAL_SUCCESS_IMAGE: Final[str or Path] = _icon(CRITICAL_SUCCESS_IMAGE_URL, CRITICAL_SUCCESS_IMAGE_PATH)

    _EXTREMAL_SUCCESS_IMAGE_NAME: Final[str] = 'extremal_success.png'
    EXTREMAL_SUCCESS_IMAGE_PATH: Final[Path] = _get_resources_path(_EXTREMAL_SUCCESS_IMAGE_NAME)
    EXTREMAL_SUCCESS_IMAGE_URL: Final[str or None] = _get_image_url(_EXTREMAL_SUCCESS_IMAGE_NAME)
    EXTREMAL_SUCCESS_IMAGE: Final[str or Path] = _icon(EXTREMAL_SUCCESS_IMAGE_URL, EXTREMAL_SUCCESS_IMAGE_PATH)

    _HARD_SUCCESS_IMAGE_NAME: Final[str] = 'hard_success.png'
    HARD_SUCCESS_IMAGE_PATH: Final[Path] = _get_resources_path(_HARD_SUCCESS_IMAGE_NAME)
    HARD_SUCCESS_IMAGE_URL: Final[str or None] = _get_image_url(_HARD_SUCCESS_IMAGE_NAME)
    HARD_SUCCESS_IMAGE: Final[str or Path] = _icon(HARD_SUCCESS_IMAGE_URL, HARD_SUCCESS_IMAGE_PATH)

    _SUCCESS_IMAGE_NAME: Final[str] = 'success.png'
    SUCCESS_IMAGE_PATH: Final[Path] = _get_resources_path(_SUCCESS_IMAGE_NAME)
    SUCCESS_IMAGE_URL: Final[str or None] = _get_image_url(_SUCCESS_IMAGE_NAME)
    SUCCESS_IMAGE: Final[str or Path] = _icon(SUCCESS_IMAGE_URL, SUCCESS_IMAGE_PATH)

    _NORMAL_FAILURE_IMAGE_NAME: Final[str] = 'failure.png'
    FAILURE_IMAGE_PATH: Final[Path] = _get_resources_path(_NORMAL_FAILURE_IMAGE_NAME)
    FAILURE_IMAGE_URL: Final[str or None] = _get_image_url(_NORMAL_FAILURE_IMAGE_NAME)
    FAILURE_IMAGE: Final[str or Path] = _icon(FAILURE_IMAGE_URL, FAILURE_IMAGE_PATH)

    _CRITICAL_FAILURE_IMAGE_NAME: Final[str] = 'critical_failure.png'
    CRITICAL_FAILURE_IMAGE_PATH: Final[Path] = _get_resources_path(_CRITICAL_FAILURE_IMAGE_NAME)
    CRITICAL_FAILURE_IMAGE_URL: Final[str or None] = _get_image_url(_CRITICAL_FAILURE_IMAGE_NAME)
    CRITICAL_FAILURE_IMAGE: Final[str or Path] = _icon(CRITICAL_FAILURE_IMAGE_URL, CRITICAL_FAILURE_IMAGE_PATH)

    _INNOVATION_IMAGE_NAME: Final[str] = 'innovation.png'
    INNOVATION_IMAGE_PATH: Final[Path] = _get_resources_path(_INNOVATION_IMAGE_NAME)
    INNOVATION_IMAGE_URL: Final[str or None] = _get_image_url(_INNOVATION_IMAGE_NAME)
    INNOVATION_IMAGE: Final[str or Path] = _icon(INNOVATION_IMAGE_URL, INNOVATION_IMAGE_PATH)

    _PROCESS_IMAGE_NAME: Final[str] = 'process.png'
    PROCESS_IMAGE_PATH: Final[Path] = _get_resources_path(_PROCESS_IMAGE_NAME)
    PROCESS_IMAGE_URL: Final[str or None] = _get_image_url(_PROCESS_IMAGE_NAME)
    PROCESS_IMAGE: Final[str or Path] = _icon(PROCESS_IMAGE_URL, PROCESS_IMAGE_PATH)
