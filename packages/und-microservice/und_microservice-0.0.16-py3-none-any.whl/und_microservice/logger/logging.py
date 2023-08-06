# -*- coding: utf-8 -*-
"""Logger por consola"""

import logging


class ConsoleLogger(object):
    """Clase logger para trabajar por consola"""

    def __init__(self):
        try:
            self.output = logging
            self.output.basicConfig(
                format='%(asctime)s [%(levelname)s] - %(name)s - %(message)s',
                datefmt='[%Y/%m/%d %I:%M:%S %p]'
            )
        except Exception as exception:
            raise exception
