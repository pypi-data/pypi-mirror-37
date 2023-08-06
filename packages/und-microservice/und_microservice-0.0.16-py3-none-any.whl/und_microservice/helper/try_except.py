# -*- coding: utf-8 -*-
""" Helpers Para manejo de excepciones"""

from functools import wraps
from und_microservice.logger.logging import ConsoleLogger

def handler_except(method):
    """Helper para excepcion de los handlers"""
    @wraps(method)
    def method_wrapper(*args, **kwargs):
        """Metodo para los wrappers"""
        try:
            return method(*args, **kwargs)
        except AttributeError as attribute_error:
            raise attribute_error
        except (Exception, ValueError) as exception:
            logger = ConsoleLogger()
            logger.output.error('=== Handler exception ===')
            logger.output.error(exception)
            logger.output.error('=' * 25)
            return exception
    return method_wrapper
