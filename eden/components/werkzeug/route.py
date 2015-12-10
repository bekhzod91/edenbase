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
from werkzeug.wsgi import SharedDataMiddleware


ROUTE_CONFIG_NAME = 'werkzeug_route'


class EdenRouteToWerkzeug(Singleton):
    __routes = []

    def set_route(self, url, view, name):
        endpoint = '%s:%s' % (view, name)
        self.__routes.append(Rule(url, endpoint=endpoint))

    def get_route(self):
        return Map(self.__routes)


class Routing(Singleton):
    __routes = None
    __urls, __names = [], []

    def reading_project_route(self):
        for werkzeug_route in config(ROUTE_CONFIG_NAME):
            self.__reading_components_route(werkzeug_route)

        return EdenRouteToWerkzeug.instance.get_route()

    def __reading_components_route(self, werkzeug_route):
        for routing in config('routing', werkzeug_route):
            # Check exists
            if not routing.get('url'):
                raise exception.RouteUrlNotFoundException

            if not routing.get('view'):
                raise exception.RouteViewNotFoundException

            if not routing.get('name'):
                raise exception.RouteNameNotFoundException

            # Check duplicate
            if routing['url'] in self.__urls:
                raise exception.RouteUrlDuplicatedException

            if routing['name'] in self.__names:
                raise exception.RouteNameDuplicatedException

            self.__urls.append(routing['url'])
            self.__names.append(routing['name'])

            EdenRouteToWerkzeug.instance.set_route(
                routing['url'], routing['view'], routing['name'])

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
