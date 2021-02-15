import sys
import os
import configparser
from typing import Final
from pathlib import Path

__MAIN_PATH: Final = Path(__file__).parent.parent.parent.parent
__RESOURCES_PATH: Final = Path(__file__).parent.parent.parent.parent / 'resources/'

__CONFIG_FILE_NAME: Final = 'config.ini'
__CONFIG_FILE: Final =\
    (Path(sys.executable).parent if getattr(sys, 'frozen', False) else __RESOURCES_PATH).joinpath(__CONFIG_FILE_NAME)
__REQUIRED_SECTION = 'FATE_OF_DICE'


def get_resources_path(sub_path: str) -> Path:
    return __RESOURCES_PATH.joinpath(sub_path)


def get_property(property_name: str, default, sys_argv_number: int):
    if len(sys.argv) > sys_argv_number:
        return sys.argv[sys_argv_number]

    env_token: str = os.getenv(property_name)
    if env_token:
        return env_token

    config = configparser.ConfigParser()
    config.read(__CONFIG_FILE)
    if config.has_option(__REQUIRED_SECTION, property_name):
        return config.get(__REQUIRED_SECTION, property_name)

    return default
