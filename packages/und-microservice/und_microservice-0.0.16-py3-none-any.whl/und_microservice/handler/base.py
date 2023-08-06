# -*- coding: utf-8 -*-
"""
    Modulo und_microservice.handler.base
    Base para handler y collectiones
"""

import falcon
from und_microservice.handler.decorator.service import service_validator
from und_microservice.helper import url
from und_microservice.response.orbis import Response
from und_microservice.handler.exception import ServiceNotExistError


class BaseCollectionHandler:
    """ Colleccion de handler """

    service = None
    response = Response()

    @service_validator
    def on_get(self, req, resp: falcon.Response):
        """ Default method GET """
        if self.service is None:
            raise ServiceNotExistError()
        try:
            params = url.split_query_string(req.params.items())
            resp.media = self.response.success(self.service.find_all(params))
            resp.status = falcon.HTTP_200
        except Exception as exception:
            resp.media = self.response.error(exception.__str__())
            resp.status = falcon.HTTP_500

    @service_validator
    def on_post(self, req: falcon.Request, resp: falcon.Response):
        """ Default method POST """
        try:
            kwargs = req.media['metadata']
            resp.media = self.response.success(self.service.create(**kwargs))
            resp.status = falcon.HTTP_200
        except Exception as exception:
            resp.media = self.response.error(exception.__str__())
            resp.status = falcon.HTTP_500

    @service_validator
    def on_put(self, req: falcon.Request, resp: falcon.Response):
        """ Default method PUT """
        try:
            kwargs = req.media['metadata']
            params = url.split_query_string(req.params.items())
            resp.media = self.response.success(self.service.update_collection(params, **kwargs))
            resp.status = falcon.HTTP_200
        except (Exception, AttributeError) as exception:
            resp.media = self.response.error(exception.__str__())
            resp.status = falcon.HTTP_500


class BaseHandler:
    """ Handler Base """
    service = None
    response = Response()

    @service_validator
    def on_get(self, req, resp: falcon.Response, id_value):
        """ Default method GET """
        try:
            resp.media = self.response.success(self.service.find_by_id(id_value))
            resp.status = falcon.HTTP_200
        except Exception as exception:
            resp.media = self.response.error(exception.__str__())
            resp.status = falcon.HTTP_500

    @service_validator
    def on_put(self, req: falcon.Request, resp: falcon.Response, id):
        """ Default method PUP """
        try:
            id = int(id) if id.isdigit() else id
            kwargs = req.media['metadata']
            if 'id' in kwargs:
                kwargs.pop('id')
            resp.media = self.response.success(self.service.update(id, **kwargs))
            resp.status = falcon.HTTP_200
        except (Exception, AttributeError) as exception:
            resp.media = self.response.error(exception.__str__())
            resp.status = falcon.HTTP_500

    @service_validator
    def on_delete(self, req, resp: falcon.Response, id):
        """ Default method DELETE """
        try:
            resp.media = self.response.success(self.service.delete(id))
            resp.status = falcon.HTTP_200
        except Exception as exception:
            resp.media = self.response.error(exception.__str__())
            resp.status = falcon.HTTP_500

    @service_validator
    def on_post(self, req: falcon.Request, resp: falcon.Response, id):
        """ Default method POST """
        try:
            id = int(id) if id.isdigit() else id
            kwargs = req.media['metadata']
            resp.media = self.response.success(self.service.create(id, **kwargs))
            resp.status = falcon.HTTP_200
        except Exception as exception:
            resp.media = self.response.error(exception.__str__())
            resp.status = falcon.HTTP_500
