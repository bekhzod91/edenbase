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


class BaseUrl(object):
    identifier = '%base_url%'

    def handler(self, content):
        base_url = os.environ.get('EDEN_APP_DIR')
        return content.replace(self.identifier, base_url)
