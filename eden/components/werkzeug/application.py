"""
    {{ docs }}
"""
__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"

# Eden project module
from eden.core.config import config
from eden.components.werkzeug.exception import MiddlewareNotFound
from eden.core.utils import import_string


WERKZEUG_MIDDLEWARE = 'werkzeug_middleware'


def application():
    app = None
    middleware_list = config(WERKZEUG_MIDDLEWARE)

    if not middleware_list:
        raise MiddlewareNotFound

    for middleware in middleware_list:
        if app:
            app = import_string(middleware)(app)
        else:
            app = import_string(middleware)()

    return app
