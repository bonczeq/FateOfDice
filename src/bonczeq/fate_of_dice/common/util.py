import sys
import os
import configparser

__config_file: str = 'config.properties'


def get_property(property_name: str, default, sys_argv_number: int):
    if len(sys.argv) > sys_argv_number:
        return sys.argv[sys_argv_number]

    env_token: str = os.getenv(property_name)
    if env_token:
        return env_token

    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(__config_file)
    properties_token: str = config.defaults().get(property_name)
    if properties_token:
        return properties_token

    return default
