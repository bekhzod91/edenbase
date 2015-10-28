"""
    {{ docs }}
"""
__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"

import os
from eden.core.format import YamlFormat
from eden.core.pattern.singleton import Singleton

from .exception import ConfigParamsNotFound
from .replace.base_url import BaseUrl


CONFIG_FILE_FORMAT = '.yml'
ENVIRONMENT_CONFIG = 'EDEN_APP_CONFIG'


def get_config_path(obj):
    app_url = os.environ.get('EDEN_APP_DIR')
    directories = obj.split('.')
    return os.path.join(*[app_url] + directories) + CONFIG_FILE_FORMAT


def set_main_config(command_args, config_obj):
    if command_args.get('config') and \
            os.path.isfile(get_config_path(command_args['config'])):
        os.environ.setdefault(ENVIRONMENT_CONFIG, command_args['config'])
    os.environ.setdefault(ENVIRONMENT_CONFIG, config_obj)


class Config(Singleton):
    __instance = None
    __config = {}
    __default_config = None

    def __get_config(self, obj):
        config_path = get_config_path(obj)
        content = open(config_path).read()

        # replace base_url
        base_url = BaseUrl()
        content = base_url.handler(content)

        return YamlFormat.decode(content)

    def get_value(self, key, config_file):
        try:
            return self.__config[config_file][key]
        except KeyError:
            self.__config[config_file] = self.__get_config(config_file)
            return self.get_value(key, config_file)



def config(key, config_file=None):
    config_file = config_file or os.environ.get('EDEN_APP_CONFIG')
    return Config.instance.get_value(key, config_file)
