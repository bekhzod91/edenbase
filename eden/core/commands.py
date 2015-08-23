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
import re
import abc
import importlib
from eden.core.config import Config

COMMAND_DIR = 'commands'
MAIN_COMMAND = 0

# MESSAGE
MESSAGE_USAGE = 'Usage: command.py subcommand [options] [args]'
MESSAGE_AVAILABLE_SUB_COMMAND = 'Available subcommands:\n'
MESSAGE_MODULE = '[%s]'
MESSAGE_COMMAND = '  %s%s'
MESSAGE_COMMAND_EMPTY = 'Document not ready'
MESSAGE_PROJECT_NAME_ART_TAG = '''
                                  dddddddd
EEEEEEEEEEEEEEEEEEEEEE            d::::::d
E::::::::::::::::::::E            d::::::d
E::::::::::::::::::::E            d::::::d
EE::::::EEEEEEEEE::::E            d:::::d
  E:::::E       EEEEEE    ddddddddd:::::d     eeeeeeeeeeee    nnnn  nnnnnnnn
  E:::::E               dd::::::::::::::d   ee::::::::::::ee  n:::nn::::::::nn
  E::::::EEEEEEEEEE    d::::::::::::::::d  e::::::eeeee:::::een::::::::::::::nn
  E:::::::::::::::E   d:::::::ddddd:::::d e::::::e     e:::::enn:::::::::::::::n
  E:::::::::::::::E   d::::::d    d:::::d e:::::::eeeee::::::e  n:::::nnnn:::::n
  E::::::EEEEEEEEEE   d:::::d     d:::::d e:::::::::::::::::e   n::::n    n::::n
  E:::::E             d:::::d     d:::::d e::::::eeeeeeeeeee    n::::n    n::::n
  E:::::E       EEEEEEd:::::d     d:::::d e:::::::e             n::::n    n::::n
EE::::::EEEEEEEE:::::Ed::::::ddddd::::::dde::::::::e            n::::n    n::::n
E::::::::::::::::::::E d:::::::::::::::::d e::::::::eeeeeeee    n::::n    n::::n
E::::::::::::::::::::E  d:::::::::ddd::::d  ee:::::::::::::e    n::::n    n::::n
EEEEEEEEEEEEEEEEEEEEEE   ddddddddd   ddddd    eeeeeeeeeeeeee    nnnnnn    nnnnnn
'''

PYTHON_INIT_FILE = '__init__.py'
MODULES = Config.get_instance().get_value('app.config.config', 'components')

# Exception
class DuplicateCommand(Exception):
    pass

# Command color state
class BgColor(object):
    __instance = None

    HEADER = '\033[95m'
    WHITE = '\033[01m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(BgColor, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    @staticmethod
    def get_instance():
        return BgColor()

    def warning(self, message):
        print(self.WARNING + message + self.END)

    def fail(self, message):
        print(self.FAIL + message + self.END)

    def info(self, message):
        print(self.BLUE + message + self.END)

    def success(self, message):
        print(self.GREEN + message + self.END)

    def white(self, message):
        print(self.WHITE + message + self.END)

    def bold(self, message):
        print(self.BOLD + message + self.END)

    def underline(self, message):
        print(self.UNDERLINE + message + self.END)


def correct_space_length(text, space_length):
    return ' ' * (space_length - len(text))


def command_name_to_class_name(command_name):
    class_name_parts = []
    for command_name_part in command_name.split('_'):
        command_name_part_list = list(command_name_part)
        command_name_part_list[0] = command_name_part_list[0].upper()
        class_name_parts.append(''.join(command_name_part_list))
    return ''.join(class_name_parts)


class ConsoleCommandHelper(object):
    message = None

    def __init__(self, **kwargs):
        self.message = kwargs.get('message')

    def __find_commands(self, file, import_module_name):
        commands = []
        file_match = re.match('^([A-Za-z0-9_]*?)\.py$', file)
        if file_match and PYTHON_INIT_FILE != file:
            command_name = file_match.groups()[0]
            try:
                class_name = \
                    command_name_to_class_name(command_name)
                command_file = \
                    importlib.import_module(
                        import_module_name + '.' +
                        command_name)
                class_object = getattr(command_file, class_name)
                commands.append({
                    'name': command_name,
                    'object': class_object,
                })
            except (AttributeError, ImportError):
                pass

        return commands

    def __find_modules(self):
        modules_list = []
        for module in MODULES:
            import_module_name = module + '.' + COMMAND_DIR
            try:
                module_import = importlib.import_module(import_module_name)
                command_dir_path = os.path.dirname(module_import.__file__)
                for file in os.listdir(command_dir_path):
                    commands = self.__find_commands(file, import_module_name)
                    if commands:
                        modules_list.append({
                            'name': module,
                            'commands': commands
                        })
            except ImportError:
                pass

        return modules_list

    def show_helper(self):
        BgColor.get_instance().white(MESSAGE_USAGE)
        BgColor.get_instance().info(MESSAGE_PROJECT_NAME_ART_TAG)
        print(MESSAGE_AVAILABLE_SUB_COMMAND)
        for module in self.__find_modules():
            BgColor.get_instance().success(MESSAGE_MODULE % module['name'])
            for command in module['commands']:
                command_instance = command['object']()
                helper = getattr(
                    command_instance, 'helper', MESSAGE_COMMAND_EMPTY)

                # Add spaces for showing beautiful
                spaces = correct_space_length(command['name'], 30)
                BgColor.get_instance().white(MESSAGE_COMMAND % (
                    command['name'] + spaces, helper))

        BgColor.get_instance().fail('\n' + self.message)


class CommandBase(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def helper(self):
        pass

    @abc.abstractmethod
    def handler(self, *args, **kwargs):
        pass


class ConsoleCommandHandler(object):
    command_args = None

    def __init__(self, command_args):
        self.command_args = command_args

    def __handler(self, *args, **kwargs):
        print(args)
        print(kwargs)

    def __simple_command(self, command_args):
        """
        Console simple command example("command.py simple_command ")
        :return: dict
        """
        simple_command = []
        # Without first command
        command_args = command_args[1:]
        before_command_is_not_simple = False

        for command_arg in command_args:
            if not before_command_is_not_simple and '-' != command_arg[:1]:
                simple_command.append(command_arg)
            else:
                # As this command is not simple
                # next command is current command value, so skip this command
                before_command_is_not_simple = not before_command_is_not_simple

        return simple_command

    def __short_command(self, command_args):
        """
        Console short command example("command.py command -short /var/www/")
        :return: dict
        """
        short_command = {}
        # Without first command
        command_args = command_args[1:]

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

    def __full_command(self, command_args):
        """
        Console full command example("manage.py command --full=/var/www/")
        :return: dict
        """
        full_command = {}
        # Without first command
        command_args = command_args[1:]

        for command_arg in command_args:
            key_value = re.match(r'--([A-Za-z0-9]*)=(.*)', command_arg)
            if key_value:
                key, value = key_value.groups()
                full_command[key] = value

        return full_command

    def __find_command(self, main_command):
        Config.get_instance().get_value('app.config.config', 'components')
        command = None
        for module in MODULES:
            import_module_name = module + '.' + COMMAND_DIR + '.' + main_command
            try:
                module = importlib.import_module(import_module_name)
                if not command and module:
                    command = module
                else:
                    raise DuplicateCommand(
                        'Duplicate command %s please correct it!' % main_command
                    )
            except ImportError:
                pass

        if not command:
            console_command_helper = ConsoleCommandHelper(
                message='Command %s not found!' % main_command)
            console_command_helper.show_helper()

        return command

    def execute(self):
        main_command = self.command_args[MAIN_COMMAND]
        execute_command = self.__find_command(main_command)

        if execute_command:
            simple_command = (self.__simple_command(self.command_args))
            short_and_full_command = self.__short_command(self.command_args)
            short_and_full_command.update(
                self.__full_command(self.command_args))

            self.__handler(*simple_command, **short_and_full_command)

def execute(*args):
    arguments = args[0][1:]
    if len(arguments) > 0:
        console_command_handler = ConsoleCommandHandler(args[0][1:])
        console_command_handler.execute()
    else:
        console_command_helper = ConsoleCommandHelper(
            message='Please choice command!')
        console_command_helper.show_helper()
