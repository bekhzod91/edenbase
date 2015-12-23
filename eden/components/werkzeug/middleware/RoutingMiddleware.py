__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"

# Eden module
from eden.core.pattern.singleton import Singleton
from eden.core.config import config
from eden.core.utils import import_string
from eden.components.werkzeug import exception

# Werkzeug module
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException


ROUTE_PATH_LIST = 'werkzeug_route'
ROUTE_KEY_IN_CONFIG = 'routing'
URL_KEY_IN_ROUTE_CONFIG = 'url'
VIEW_KEY_IN_ROUTE_CONFIG = 'view'
NAME_KEY_ROUTE_CONFIG = 'name'


class EdenRouteToWerkzeug(Singleton):
    """
        Translate eden route to werkzeug route
        reading ROUTE_CONFIG_NAME is global config for routing list
    """
    __routes = []

    def set_route(self, url, view, name):
        """
            Keyword arguments:
            url -- the simple werkzeug url
            view -- the handler this route
            name -- the unique name for this route
        """
        endpoint = '%s:%s' % (view, name)
        self.__routes.append(Rule(url, endpoint=endpoint))

    def get_route(self):
        """Return werkzeug Map object instance"""
        return Map(self.__routes)


class RoutingParser(Singleton):
    __routes = None
    __urls, __names = [], []

    def reading_project_route(self):
        for route_path in config(ROUTE_PATH_LIST):
            for route_params in self.__get_valid_routes(route_path):
                url, view, name = route_params
                EdenRouteToWerkzeug.instance.set_route(url, view, name)

        return EdenRouteToWerkzeug.instance.get_route()

    def __get_valid_routes(self, werkzeug_route):
        """
            Get correct routes or throw exception
        """
        try:
            for routing in config(ROUTE_KEY_IN_CONFIG, werkzeug_route):
                # Check exists
                if not routing.get(URL_KEY_IN_ROUTE_CONFIG):
                    raise exception.RouteUrlNotFoundException

                if not routing.get(VIEW_KEY_IN_ROUTE_CONFIG):
                    raise exception.RouteViewNotFoundException

                if not routing.get(NAME_KEY_ROUTE_CONFIG):
                    raise exception.RouteNameNotFoundException

                # Check duplicate
                if routing[URL_KEY_IN_ROUTE_CONFIG] in self.__urls:
                    raise exception.RouteUrlDuplicatedException

                if routing[NAME_KEY_ROUTE_CONFIG] in self.__names:
                    raise exception.RouteNameDuplicatedException

                self.__urls.append(routing[URL_KEY_IN_ROUTE_CONFIG])
                self.__names.append(routing[NAME_KEY_ROUTE_CONFIG])

                yield routing['url'], routing['view'], routing['name']
        except exception.RoutingException as route_exception:
            # Protected shadow exceptions
            self.__urls, self.__names = [], []
            raise route_exception

    def get_route(self):
        if self.__routes:
            return self.__routes
        self.__routes = self.reading_project_route()
        return self.__routes


class RoutingMiddleware(object):
    def dispatch_request(self, request):
        routes = RoutingParser.instance.get_route()
        adapter = routes.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            view, name = endpoint.split(':')

            view_handler = import_string(view)

            return view_handler(request, **values)

        except HTTPException as http_exception:
            return Response(http_exception.description, http_exception.code)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
