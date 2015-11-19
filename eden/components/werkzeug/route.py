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
from werkzeug.routing import Map, Rule


class Routing(Singleton):
    __routes = []

    def set_route(self, url, endpoint):
        self.__routes.append(Rule(url, endpoint=endpoint))

    def get_route(self):
        return Map(self.__routes)


def route(url):
    def func(url_name):
        print(url_name)
        return url_name

    return func


def application(environ, start_response):
    urls = url_map.bind_to_environ(environ)
    try:
        endpoint, args = urls.match()
    except HTTPException as e:
        return e
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['Rule points to %r with arguments %r' % (endpoint, args)]
