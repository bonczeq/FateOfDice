import sys
import os
import configparser
from typing import Optional, Final
from pathlib import Path

import fate_of_dice.resources


class ResourcesHandler:
    __IS_EXE: bool = getattr(sys, 'frozen', False)

    __RESOURCES_PATH: Final[Path] = Path(fate_of_dice.resources.__file__).parent.absolute()

    __CONFIG_FILE: Final[Path] = (Path(sys.executable).parent.absolute()
                                  if __IS_EXE else __RESOURCES_PATH).joinpath('config.ini')

    __DEFAULT_CONFIG_SECTION: Final[str] = 'FATE_OF_DICE'

    __config = configparser.ConfigParser()
    __config.read(__CONFIG_FILE)

    @classmethod
    def get_resources_path(cls, sub_path: Optional[str] = None) -> Path:
        if sub_path:
            return cls.__RESOURCES_PATH.joinpath(sub_path)
        else:
            return cls.__RESOURCES_PATH

    @classmethod
    def get_property(cls, property_name: str, default, section_name: str = __DEFAULT_CONFIG_SECTION):
        env_token: Optional[str] = os.getenv(property_name, None)
        if env_token:
            return env_token
        elif cls.__config.has_option(section_name, property_name):
            return cls.__config.get(section_name, property_name)
        else:
            return default
