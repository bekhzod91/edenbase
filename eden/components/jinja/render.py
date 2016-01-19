__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"

from .environment import Environment


def render_to_string(template_name, context=None):
    if not context:
        context = {}

    env = Environment.instance.get()
    template = env.get_template(template_name)
    return template.render(**context)
