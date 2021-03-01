import sys
import os
import configparser
from typing import Optional, Final
from pathlib import Path

import fate_of_dice.resources


class ResourceHandler:
    _IS_EXE: bool = getattr(sys, 'frozen', False)

    _RESOURCES_PATH: Final[Path] = Path(fate_of_dice.resources.__file__).parent.absolute()

    _CONFIG_FILE: Final[Path] = (Path(sys.executable).parent.absolute()
                                 if _IS_EXE else _RESOURCES_PATH).joinpath('config.ini')

    _DEFAULT_CONFIG_SECTION: Final[str] = 'FATE_OF_DICE'

    _config = configparser.ConfigParser()
    _config.read(_CONFIG_FILE)

    @classmethod
    def get_resources_path(cls, sub_path: Optional[str] = None) -> Path:
        return cls._get_resource_path(cls._RESOURCES_PATH, sub_path)

    @classmethod
    def get_property(cls, property_name: str, default, section_name: str = _DEFAULT_CONFIG_SECTION):
        env_token: Optional[str] = os.getenv(property_name, None)
        if env_token:
            return env_token
        elif cls._config.has_option(section_name, property_name):
            return cls._config.get(section_name, property_name)
        else:
            return default

    @staticmethod
    def _get_resource_path(main_path: Path, sub_path: Optional[str] = None) -> Path:
        if sub_path:
            return main_path.joinpath(sub_path)
        else:
            return main_path


class ResourceImageHandler(ResourceHandler):
    __ICONS_DIR: Final[str] = 'icons'
    __ICON_PATH: Final[Path] = ResourceHandler._RESOURCES_PATH.joinpath(__ICONS_DIR)

    @classmethod
    def get_resources_path(cls, sub_path: Optional[str] = None) -> Path:
        return cls._get_resource_path(cls.__ICON_PATH, sub_path)

    PYTHON_IMAGE: Final[Path] = __ICON_PATH.joinpath('python.png')
    DISCORD_IMAGE: Final[Path] = __ICON_PATH.joinpath('discord.png')

    CRITICAL_SUCCESS_IMAGE: Final = __ICON_PATH.joinpath('critical_success.png')
    EXTREMAL_SUCCESS_IMAGE: Final = __ICON_PATH.joinpath('extremal_success.png')
    HARD_SUCCESS_IMAGE: Final = __ICON_PATH.joinpath('hard_success.png')
    NORMAL_FAILURE_IMAGE: Final = __ICON_PATH.joinpath('failed.png')
    CRITICAL_FAILURE_IMAGE: Final = __ICON_PATH.joinpath('critical_failed.png')

    INNOVATION_IMAGE: Final[Path] = __ICON_PATH.joinpath('innovation.png')
    PROCESS_IMAGE: Final[Path] = __ICON_PATH.joinpath('process.png')
