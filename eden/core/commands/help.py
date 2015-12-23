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
import os
import importlib

from .parser import command_name_to_class_name
from .viewer import BgColor, correct_space_length

from eden.core.config import config


COMMAND_DIR = 'commands'
COMPONENTS = 'components'
PYTHON_INIT_FILE = '__init__.py'

# MESSAGE
MESSAGE_USAGE = 'Usage: use.py subcommand [options] [args]'
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


class Help(object):
    message = None

    def __init__(self, **kwargs):
        self.message = kwargs.get('message')

    def show_helper(self):
        BgColor.instance.white(MESSAGE_USAGE)
        BgColor.instance.info(MESSAGE_PROJECT_NAME_ART_TAG)
        print(MESSAGE_AVAILABLE_SUB_COMMAND)
        for module in self.__find_modules():
            BgColor.instance.success(MESSAGE_MODULE % module['name'])
            for command in module['commands']:
                command_instance = command['object']()
                helper = getattr(
                    command_instance, 'helper', MESSAGE_COMMAND_EMPTY)

                # Add spaces for showing beautiful
                spaces = correct_space_length(command['name'], 30)
                BgColor.instance.white(MESSAGE_COMMAND % (
                    command['name'] + spaces, helper))

        BgColor.instance.fail('\n' + self.message)

    def __find_modules(self):
            modules_list = []
            for module in config(COMPONENTS):
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
