# -*- coding: utf-8 -*-
"""Modulo Adaptador Sql basado en Alchemy"""

from abc import ABC
from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import sessionmaker, scoped_session


class SqlAlchemyAdapter(ABC):
    """Class Adaptador Sql basado en Alchemy"""
    session = None
    entity = None

    def __init__(self, config):
        self._options = config.get_key('db')
        self._session_maker()

    def create(self, data):
        """ Create query """
        try:
            self.session.add(data)
            self.commit()
            return data.id
        except Exception as exception:
            self.rollback()
            raise exception

    def update(self, primay_key, **kwargs):
        """ Create query """
        try:
            self.session.query(self.entity).filter_by(id=primay_key).update(kwargs)
            self.commit()
        except Exception as exception:
            self.rollback()
            raise exception

    def delete(self, primay_key):
        """ Delete query """
        try:
            self.session.query(self.entity).filter_by(
                id=primay_key).delete(synchronize_session=False)
            self.commit()
        except Exception as exception:
            self.rollback()
            raise exception

    def count(self):
        """ count query """
        try:
            return self.session.query(func.count('*')).select_from(self.entity).scalar()
        except Exception as exception:
            self.rollback()
            raise exception

    def delete_in(self, ids):
        """ Delete por id """
        try:
            self.session.query(self.entity).filter(
                self.entity.id.in_(ids)).delete(synchronize_session=False)
            self.commit()
        except Exception as exception:
            self.rollback()
            raise exception

    def find_all(self, params):
        """ Recuperar toda la lista """
        select_params = params['fields']
        where_params = params['filter']
        pagination_params = params['pagination']
        sort_params = params['sort']

        if select_params:
            columns = [getattr(self.entity, column) for column in select_params]
            query = self.session.query(*columns)
        else:
            query = self.session.query(self.entity)

        if 'filter_in' in params:
            for item_property, values in params['filter_in'].items():
                query = query.filter(getattr(self.entity, item_property).in_(tuple(values)))

        query = query.filter_by(**where_params)
        if sort_params:
            query = query.order_by(sort_params)

        if pagination_params:
            query = query.offset(pagination_params['offset']).limit(pagination_params['limit'])
        return query.all()

    def find_by_id(self, primary_key):
        """ Recuperar a partir de primary key """
        try:
            return self.session.query(self.entity).filter_by(id=primary_key).first()
        except Exception as exception:
            raise exception

    def statement(self, sql):
        """ Crear query customizada """
        result = self.session.query(self.entity).from_statement(text(sql))
        return result.all()

    def bulk_insert_entities(self, entities):
        """ Crear query entities """
        try:
            for entity in entities:
                self.session.add_all([entity])
                self.session.flush()
            self.session.commit()
        except Exception as exception:
            self.rollback()
            raise exception

    def bulk_insert(self, items):
        """ Crear query para insertar """
        try:
            self.session.add_all(items)
            self.commit()
        except Exception as exception:
            self.rollback()
            raise exception

    def delete_with_params(self, params):
        """ Eliminar aplicando where """
        return self.session.query(self.entity).filter(params).delete(synchronize_session=False)

    def commit(self):
        """ Crear un commit transaccional """
        self.session.commit()

    def rollback(self):
        """ Aplicar rollback """
        self.session.rollback()

    def _session_maker(self):
        try:
            driver = '%s://%s:%s@%s:%s/%s' % (
                self._options['connection'],
                self._options['user'],
                self._options['password'],
                self._options['host'],
                self._options['port'],
                self._options['database']
                )
            engine = create_engine(driver, echo=True, isolation_level="READ UNCOMMITTED")
            self.session = scoped_session(sessionmaker(bind=engine))
        except Exception as exception:
            raise exception
