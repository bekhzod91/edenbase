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
import sys


if __name__ == '__main__':
    os.environ.setdefault('EDEN_PROJECT_DIR', os.path.dirname(__file__))
    os.environ.setdefault('EDEN_PROJECT_CONFIG', 'app.config.config.yml')

    from eden.commands import execute
    execute(sys.argv)
