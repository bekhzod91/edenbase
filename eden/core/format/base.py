__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"

import abc
import six


@six.add_metaclass(abc.ABCMeta)
class BaseFormat(object):
    @staticmethod
    @abc.abstractmethod
    def encode(obj):
        pass

    @staticmethod
    @abc.abstractmethod
    def decode(string):
        pass
