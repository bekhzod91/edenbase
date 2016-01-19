__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"

import json
from .base import BaseFormat


class JsonFormat(BaseFormat):
    @staticmethod
    def encode(obj):
        return json.dumps(obj)

    @staticmethod
    def decode(string):
        return json.loads(string)