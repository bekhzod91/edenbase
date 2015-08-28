"""
    {{ docs }}
"""
__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class Singleton(object):
    _instance = None

    @classproperty
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
