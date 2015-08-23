"""
    {{ docs }}
"""
__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"


from eden.core.commands import CommandBase

class ClearCache(CommandBase):
    helper = 'run command clear jinja template cache'

    def handler(self, *args, **kwargs):
        pass
