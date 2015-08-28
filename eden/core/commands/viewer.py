"""
    {{ docs }}
"""
__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"

from eden.core.pattern.singleton import Singleton

# Command color state
class BgColor(Singleton):
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
