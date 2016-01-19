"""
    {{ docs }}
"""
__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"

from eden.components.werkzeug.jinja import render_to_response


def hello(request, **kwargs):
    return render_to_response(
        'mytemplate.html', {'hello': [1, 2, 3, 4, 5, 6]}
    )
