"""
    {{ docs }}
"""
__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"

from http.client import HTTPException
from eden.core.pattern.singleton import Singleton
from eden.core.config.api import config
from eden.components.werkzeug import exception
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request


ROUTE_PATH_LIST = 'werkzeug_route'
ROUTE_KEY_IN_CONFIG = 'routing'
ROUTE_CONFIG_URL_KEY = 'url'
ROUTE_CONFIG_VIEW_KEY = 'view'
ROUTE_CONFIG_NAME_KEY = 'name'

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


class Routing(Singleton):
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
                if not routing.get(ROUTE_CONFIG_URL_KEY):
                    raise exception.RouteUrlNotFoundException

                if not routing.get(ROUTE_CONFIG_VIEW_KEY):
                    raise exception.RouteViewNotFoundException

                if not routing.get(ROUTE_CONFIG_NAME_KEY):
                    raise exception.RouteNameNotFoundException

                # Check duplicate
                if routing[ROUTE_CONFIG_URL_KEY] in self.__urls:
                    raise exception.RouteUrlDuplicatedException

                if routing[ROUTE_CONFIG_NAME_KEY] in self.__names:
                    raise exception.RouteNameDuplicatedException

                self.__urls.append(routing[ROUTE_CONFIG_URL_KEY])
                self.__names.append(routing[ROUTE_CONFIG_NAME_KEY])

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


class Shortly(object):
    def dispatch_request(self, request):
        routes = Routing.instance.get_route()
        adapter = routes.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            print(endpoint)
            return getattr(self, 'on_' + endpoint)(request, **values)
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(with_static=True):
    app = Shortly()
    return app

@Request.application
def application(request):
    # urls = get_url_map()
    """
    urls = url_map.bind_to_environ(environ)
    try:
        endpoint, args = urls.match()
    except HTTPException as e:
        return e
    """
    return create_app()
