# -*- coding: utf-8 -*-
""" Init Bootstrap """

import codecs
import json
import yaml


class File:
    """ Clase para leer archivos """

    @staticmethod
    def read(file):
        """ Leer texto plano """
        return codecs.open(file, 'r', 'utf-8')

    @staticmethod
    def read_yml(file):
        """ Leer archivos yml """
        file_object = open(file, 'r', encoding='utf-8')
        return yaml.load(file_object)

    @staticmethod
    def read_json(file):
        """ Leer archivos json """
        file_object = open(file, 'r')
        return json.load(file_object)
