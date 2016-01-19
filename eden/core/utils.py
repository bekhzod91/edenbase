__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"


import importlib

class ImportStringError(Exception):
    pass


def import_string(string):
    try:
        import_module = importlib.import_module(
            '.'.join(string.split('.')[:-1]))
        return getattr(import_module, string.split('.')[-1:][0])
    except (ImportError, AttributeError):
        raise ImportStringError(
            'Module %s can\'t find please check correct path' % string)


class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
