# -*- coding: utf-8 -*-
""" Excepcion base"""

class NotConfigException(Exception):
    """ Excepcion no existe configuraciones  """
    def __init__(self):
        super().__init__('Data not found ')

class NotValueConfigException(Exception):
    """ Excepcion no existe configuraciones  """
    def __init__(self, value):
        super().__init__('That key: ' + value + 'not found in config')
