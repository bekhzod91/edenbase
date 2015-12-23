"""
    {{ docs }}
"""
__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"

import importlib

from .help import Help, COMPONENTS, COMMAND_DIR
from .exception import DuplicateCommand, CommandClassNotFound
from .parser import (
    simple_command_search, short_command_search, full_command_search,
    command_name_to_class_name
)

from eden.core.config import config
from eden.core.config.handler import set_main_config

MAIN_COMMAND = 0


class CommandHandler(object):
    command_args = None

    def __init__(self, command_args):
        self.command_args = command_args

    def __handler(self, class_object, args, kwargs):
        command = class_object()
        command.handler(*args, **kwargs)

    def __find_command(self, main_command):
        command = None
        for module in config(COMPONENTS):
            import_module_name = module + '.' + \
                COMMAND_DIR + '.' + main_command

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
            console_command_helper = Help(
                message='Command %s not found!' % main_command)
            console_command_helper.show_helper()

        return command

    def execute(self):
        main_command = self.command_args[MAIN_COMMAND]
        execute_command = self.__find_command(main_command)

        if execute_command:
            simple_command = (simple_command_search(self.command_args))

            short_and_full_command = short_command_search(self.command_args)
            short_and_full_command.update(
                full_command_search(self.command_args))

            class_name = command_name_to_class_name(main_command)
            class_object = getattr(execute_command, class_name, None)
            if not class_object:
                raise CommandClassNotFound(
                    'You need create class %s for command %s in %s' %
                    (class_name, main_command, execute_command)
                )

            self.__handler(
                class_object, simple_command, short_and_full_command)


def execute(args, config_obj):
    arguments = args[1:]

    set_main_config(full_command_search(arguments), config_obj)

    if len(arguments) > 0:
        console_command_handler = CommandHandler(arguments)
        console_command_handler.execute()
    else:
        console_command_helper = Help(message='Please choice command!')
        console_command_helper.show_helper()
