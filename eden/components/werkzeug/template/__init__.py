__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"

import os

WERKZEUG_TEMPLATE_DIR = os.path.dirname(__file__)

def render_to_string(template_path, **kwargs):
    with open(template_path) as template:
        content = template.read() % kwargs

    return content

__all__ = [WERKZEUG_TEMPLATE_DIR]

