# -*- coding: utf-8 -*-
""" Comportamiento base para administrador de configuraciones"""

from abc import ABC
from und_microservice.config.exception.config import NotConfigException
from und_microservice.config.exception.config import NotValueConfigException

class  BaseConfig(ABC):
    """ Clase de configuracion base """
    _config = None

    def get_all(self):
        """ Permite recuperar la todas las configuraciones """
        if self._config == '':
            raise NotConfigException
        return self._config

    def get_key(self, key):
        """ Permite recuperar un grupo de configuraciones """
        if self._config == '':
            raise NotValueConfigException
        return self._config[key]
