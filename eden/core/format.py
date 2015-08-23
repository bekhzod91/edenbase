"""
    {{ docs }}
"""
__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"

import yaml
import json
import abc


class BaseFormat(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def encode(obj):
        pass

    @staticmethod
    @abc.abstractmethod
    def decode(string):
        pass


class JsonFormat(BaseFormat):
    @staticmethod
    def encode(obj):
        return json.dumps(obj)

    @staticmethod
    def decode(string):
        return json.loads(string)


class YamlFormat(BaseFormat):
    @staticmethod
    def encode(obj):
        return yaml.dump(obj)

    @staticmethod
    def decode(string):
        return yaml.load(string)

