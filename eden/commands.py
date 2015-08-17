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
import importlib
from abc import ABCMeta, abstractmethod

COMMAND_DIR = 'commands'
MAIN_COMMAND = 0

modules = [
    'eden.core.managements',
    'eden.core.validators'
]


# Exception
class DuplicateCommand(Exception):
    pass


# Exception
class CommandHelper(object):
    def __init__(self, message):
        print(message)


class CommandBase(object):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def help(self):
        pass

    @abstractmethod
    def handler(self, *args, **kwargs):
        pass


class ConsoleCommandHandler(object):
    command_args = None
    module = None

    def __init__(self, command_args):
        self.command_args = command_args

    def __handler(self, *args, **kwargs):
        print(args)
        print(kwargs)

    def __simple_command(self):
        """
        Console simple command example("manage.py simple_command ")
        :return: dict
        """
        simple_command = []
        before_command_is_not_simple = False
        for command_arg in self.command_args[1:]:
            if not before_command_is_not_simple and '-' != command_arg[:1]:
                simple_command.append(command_arg)
            else:
                before_command_is_not_simple = not before_command_is_not_simple

        return simple_command

    def __short_command(self):
        """
        Console short command example("manage.py command -short /var/www/")
        :return: dict
        """
        short_command = {}
        # Without first command
        command_args = self.command_args[1:]

        is_short_command = False
        for index, command_arg in enumerate(command_args):
            if not is_short_command and \
                    re.match(r'^-[A-Za-z0-9]*$', command_arg):
                keyword = command_arg[1:]
                try:
                    short_command[keyword] = command_args[index + 1]
                except IndexError:
                    short_command[keyword] = None

                is_short_command = True
            else:
                is_short_command = False

        return short_command

    def __full_command(self):
        """
        Console full command example("manage.py command --full=/var/www/")
        :return: dict
        """
        full_command = {}
        # Without first command
        command_args = self.command_args[1:]

        for command_arg in command_args:
            key_value = re.match(r'--([A-Za-z0-9]*)=(.*)', command_arg)
            if key_value:
                key, value = key_value.groups()
                full_command[key] = value

        return full_command

    def __find_command(self, main_command):
        for module in modules:
            import_module_name = module + '.' + COMMAND_DIR + '.' + main_command
            try:
                module = importlib.import_module(import_module_name)
                if not self.module and module:
                    self.module = module
                else:
                    raise DuplicateCommand(
                        'Duplicate command %s please correct it!' % main_command
                    )
            except ImportError:
                pass

        if not self.module:
            CommandHelper('Command %s not found!' % main_command)

    def execute(self):
        main_command = self.command_args[MAIN_COMMAND]
        self.__find_command(main_command)

        if self.module:
            simple_command = (self.__simple_command())
            short_and_full_command = self.__short_command()
            short_and_full_command.update(self.__full_command())

            self.__handler(*simple_command, **short_and_full_command)

def execute(*args):
    arguments = args[0][1:]
    if len(arguments) > 0:
        console_command_handler = ConsoleCommandHandler(args[0][1:])
        console_command_handler.execute()
