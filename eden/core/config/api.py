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


CONFIG_FILE_FORMAT = '.yml'
DEFAULT_CONFIG = os.environ.get('EDEN_APP_CONFIG')

class Config(Singleton):
    __instance = None
    __config = {}
    __default_config = None

    def __get_config(self, obj):
        app_url = os.environ.get('EDEN_APP_DIR')
        directories = obj.split('.')
        config_url = os.path.join(*[app_url] + directories) + CONFIG_FILE_FORMAT

        content = open(config_url).read()

        return YamlFormat.decode(content)

    def get_value(self, key, obj=DEFAULT_CONFIG):
        try:
            return self.__config[obj][key]
        except KeyError:
            self.__config[obj] = self.__get_config(obj)
            return self.get_value(obj, key)



