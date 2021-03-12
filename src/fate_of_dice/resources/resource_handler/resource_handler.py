import configparser
import os
import sys
from pathlib import Path
from typing import Optional, Final

import fate_of_dice.resources

_IS_EXE: bool = getattr(sys, 'frozen', False)

_RESOURCES_PATH: Final[Path] = Path(fate_of_dice.resources.__file__).parent.absolute()

_DEFAULT_CONFIG_SECTION: Final[str] = 'FATE_OF_DICE'
_CONFIG_FILE: Final[Path] = (Path(sys.executable).parent.absolute()
                             if _IS_EXE else _RESOURCES_PATH).joinpath('config.ini')


def _get_resource_path(main_path: Path, sub_path: Optional[str] = None) -> Path:
    if sub_path:
        return main_path.joinpath(sub_path)
    else:
        return main_path


class ResourceHandler:
    _config = configparser.ConfigParser()
    _config.read(_CONFIG_FILE)

    @classmethod
    def get_resources_path(cls, sub_path: Optional[str] = None) -> Path:
        return _get_resource_path(_RESOURCES_PATH, sub_path)

    @classmethod
    def get_property(cls, property_name: str, default=None, section_name: str = _DEFAULT_CONFIG_SECTION):
        env_token: Optional[str] = os.getenv(property_name, None)
        if env_token:
            return env_token
        elif cls._config.has_option(section_name, property_name):
            return cls._config.get(section_name, property_name)
        else:
            return default
