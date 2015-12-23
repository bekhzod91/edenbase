__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"

# Eden project
from eden.core.config import config

# Werkzeug module
from werkzeug.wsgi import SharedDataMiddleware


WERKZEUG_STATIC_URL = 'werkzeug_static_url'
WERKZEUG_STATIC_ROOT = 'werkzeug_static_root'


class StaticFilesMiddleware(SharedDataMiddleware):
    def __init__(self, app):
        static_url = config(WERKZEUG_STATIC_URL)
        static_root = config(WERKZEUG_STATIC_ROOT)

        super(StaticFilesMiddleware, self)\
            .__init__(app, {static_url: static_root})
