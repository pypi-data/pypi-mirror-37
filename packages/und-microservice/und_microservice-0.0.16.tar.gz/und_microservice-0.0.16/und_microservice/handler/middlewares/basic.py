# -*- coding: utf-8 -*-
"""Modulo und_microservice.handler.midelwares.basic"""

import falcon

class Basic:
    """Clase midelware basico"""

    def process_request(self, req: falcon.Request, resp: falcon.Response):
        """Midelware de ejemplo"""
        print(req)
        print(resp)
        print('Im a basic middleware')
        return resp
