__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"

from werkzeug.exceptions import HTTPException


class RoutingException(HTTPException):
    pass


class RouteUrlNotFoundException(RoutingException):
    code = 500
    description = (
        "In werkzeug_route not found <b>url</b> keywords"
    )

    def get_description(self, env=None):
        return self.get_description

class RouteViewNotFoundException(RoutingException):
    code = 500
    description = (
        "In werkzeug_route not found <b>view</b> keywords"
    )

class RouteNameNotFoundException(RoutingException):
    code = 500
    description = (
        "In werkzeug_route not found <b>name</b> keywords"
    )



class RouteNameDuplicatedException(RoutingException):
    pass

class RouteUrlDuplicatedException(RoutingException):
    pass
