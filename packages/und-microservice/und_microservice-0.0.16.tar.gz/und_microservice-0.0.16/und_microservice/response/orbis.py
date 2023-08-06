# -*- coding: utf-8 -*-
"""Modulo response"""

class Response(object):
    """Clase response generico"""

    PROCESS_SUCCESS_CODE = 2000
    PROCESS_SUCCESS_MESSAGE = 'SUCCESS'
    PROCESS_ERROR_CODE = 4000
    PROCESS_ERROR_MESSAGE = 'ERROR'

    def success(self, data):
        """Respuesta afirmativa"""
        try:
            return self._schema(False,
                                self.PROCESS_SUCCESS_CODE,
                                self.PROCESS_SUCCESS_MESSAGE,
                                data if data is not None else [])
        except Exception as exception:
            raise exception

    def error(self, message):
        """Respuesta con error"""
        try:
            return self._schema(True,
                                self.PROCESS_ERROR_CODE,
                                self.PROCESS_ERROR_MESSAGE if message is None else message,
                                [])
        except Exception as exception:
            raise exception

    @staticmethod
    def _schema(error, code, message, data):
        return {
            'error': error,
            'code': code,
            'message': message,
            'data': data
        }
