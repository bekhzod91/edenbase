__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"

from eden.components.werkzeug.status import HTTP_200_OK
from eden.components.jinja.render import render_to_string
from werkzeug.wrappers import Response


def render_to_response(
        template_name, context=None,
        status=HTTP_200_OK, content_type='text/html'):
    return Response(
        render_to_string(template_name, context),
        status=status, content_type=content_type
    )
