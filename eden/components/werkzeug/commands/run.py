"""
    {{ docs }}
"""
__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"


import re

from eden.core.commands.base import CommandBase
from eden.core.config.api import config


class Run(CommandBase):
    helper = 'run command with argument run 0.0.0.0:8080'

    def handler(self, *args, **kwargs):
        debug = config('debug')
        host = self.get_host(args, kwargs) or 'localhost'
        port = self.get_port(args, kwargs) or 8080

        from werkzeug.serving import run_simple
        from werkzeug.wrappers import Response

        def application(environ, start_response):
            response = Response('Hello World!', mimetype='text/plain')
            return response(environ, start_response)

        run_simple(host, port, application, use_debugger=debug, use_reloader=debug)

    def get_host(self, simple_commands, short_and_full_commands):
        for command in simple_commands:
            host_regex = re.match('(.*)?:[0-9]{1,5}', command)
            if host_regex:
                return host_regex.group()[0]

        if short_and_full_commands.get('h'):
            return short_and_full_commands['h']

        if short_and_full_commands.get('host'):
            return short_and_full_commands['host']

        return None

    def get_port(self, simple_commands, short_and_full_commands):
        for command in simple_commands:
            port_regex = re.match('.*?:([0-9]{1,5})', command)
            if port_regex:
                return port_regex.group()[0]

        if short_and_full_commands.get('p'):
            return short_and_full_commands['p']

        if short_and_full_commands.get('port'):
            return short_and_full_commands['port']

        return None
