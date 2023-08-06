# -*- coding: utf-8 -*-
""" Comportamiento base para administrador de configuraciones"""

import glob
from und_microservice.config.base import BaseConfig
from und_microservice.commons.file import File
from und_microservice.helper.data import dict_merge


class ConfigYaml(BaseConfig):
    """ Manejador de config en yml """

    def __init__(self, path='config/'):
        self._config = {}
        yaml_file = File()
        paths = glob.glob(path + '*yml')
        for path in paths:
            config = yaml_file.read_yml(path)
            dict_merge(self._config, config)
