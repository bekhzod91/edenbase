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

def command_name_to_class_name(command_name):
    class_name_parts = []
    for command_name_part in command_name.split('_'):
        command_name_part_list = list(command_name_part)
        command_name_part_list[0] = command_name_part_list[0].upper()
        class_name_parts.append(''.join(command_name_part_list))
    return ''.join(class_name_parts)


def simple_command_search(command_args):
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


def short_command_search(command_args):
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


def full_command_search(command_args):
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

