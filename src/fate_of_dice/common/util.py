import sys
import os
import configparser
from typing import Final
from pathlib import Path

__CONFIG_FILE: Final = 'config.properties'
__RESOURCES_PATH: Final = Path(__file__).parent.parent.parent.parent.parent / 'resources/'


def get_resources_path(sub_path: str) -> Path:
    return __RESOURCES_PATH.joinpath(sub_path)


def get_property(property_name: str, default, sys_argv_number: int):
    if len(sys.argv) > sys_argv_number:
        return sys.argv[sys_argv_number]

    env_token: str = os.getenv(property_name)
    if env_token:
        return env_token

    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(__CONFIG_FILE)
    properties_token: str = config.defaults().get(property_name)
    if properties_token:
        return properties_token

    return default
