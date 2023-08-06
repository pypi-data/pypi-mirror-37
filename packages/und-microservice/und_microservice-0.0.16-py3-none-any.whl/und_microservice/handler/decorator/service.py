# -*- coding: utf-8 -*-
"""Modulo und_microservice.handler.decorator.service"""

from functools import wraps
import falcon


def service_validator(method):
    """Validar si existe un servicio"""

    @wraps(method)
    def method_wrapper(*args, **kwargs):
        """Wraper de decorador"""
        if args[0].service is None:
            raise falcon.HTTPError('Application Services is Null')
        return method(*args, **kwargs)
    return method_wrapper
