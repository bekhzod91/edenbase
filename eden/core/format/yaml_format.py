__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"

import yaml
from .base import BaseFormat


class YamlFormat(BaseFormat):
    @staticmethod
    def encode(obj):
        return yaml.dump(obj)

    @staticmethod
    def decode(string):
        return yaml.load(string)
