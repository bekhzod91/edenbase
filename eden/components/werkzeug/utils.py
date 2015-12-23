__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"

import os


MAX_DEEP_FOLDER = 5

def find_config_files(file_ext):
    """This iterates over all project files with
    the exception of hidden files example .venv .idea etc.
    Exist restriction of deep folders
    """
    __main__ = __import__('__main__')
    dir_name = os.path.dirname(__main__.__file__)

    def find_files_list(dir_path, deep=0):
        if deep <= MAX_DEEP_FOLDER and not dir_name.startswith('.'):
            contents = os.listdir(dir_path)
            for content in contents:
                content_abspath = os.path.join(dir_path, content)

                if os.path.isdir(content_abspath):
                    for item in find_files_list(content_abspath, deep + 1):
                        yield item
                if os.path.isfile(content_abspath) and \
                        content_abspath.endswith(file_ext):
                    yield os.path.abspath(content_abspath)

    return [filename for filename in find_files_list(dir_name)]