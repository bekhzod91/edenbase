__author__ = "Bekhzod Tillakhanov"
__copyright__ = "Copyright 2015, The Eden Project"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "bekhzod.tillakhanov@gmail.com"
__status__ = "Development"

import os
import six

from eden.core.pattern.singleton import Singleton
from eden.core.config import config
from eden.core.utils import import_string

from jinja2 import Environment as Env
from jinja2 import FileSystemLoader, FileSystemBytecodeCache
from .exception import JinjaTemplateUrlEmpty, JinjaTemplateUrlNotExist


class Environment(Singleton):
    env = None

    def get(self):
        if not self.env:
            self.env = Env(
                loader=FileSystemLoader(self.__check_urls()),
                bytecode_cache=self.__cache()
            )

        return self.env

    def __check_urls(self):
        jinja_template_urls = config('jinja_template_urls')
        if not jinja_template_urls:
            raise JinjaTemplateUrlEmpty('jinja_template_urls is empty')

        if isinstance(jinja_template_urls, six.string_types):
            if not os.path.isdir(jinja_template_urls):
                raise JinjaTemplateUrlNotExist(
                    '%s don\'t exists correct it!' % jinja_template_urls)
        else:
            for template_url in jinja_template_urls:
                if not os.path.isdir(template_url):
                    raise JinjaTemplateUrlNotExist(
                        '%s don\'t exists correct it!' % template_url)

        return jinja_template_urls

    def __cache(self):
        return None