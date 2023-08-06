# -*- coding: utf-8 -*-
"""Helpers para manipulacion de data"""

import collections
import decimal

def get_object_dict(data_object, params=None):
    """Convertir un objeto en diccionarios"""
    if params is not None and params['fields']:
        fields = params['fields']
    else:
        fields = [attr for attr in data_object.__dict__.keys() if not attr.startswith('_')]
    result = {}
    for field in fields:
        value = getattr(data_object, field)
        if field.startswith('date') and value is not None:
            result.update({field: value.strftime('%Y-%m-%d %H:%M:%S')})
        else:
            result.update({field: parse_value(value)})
    return result


def parse_value(value):
    """Convertir un valor a decimal"""
    return float(value) if isinstance(value, decimal.Decimal) else value


def get_multi_objects_dict(*args, params=None):
    """Convertir un array de objetos en diccionarios"""
    object_group = []
    result = {}
    for data_object in args:
        if params is not None and params['fields']:
            fields = params['fields']
        else:
            fields = [attr for attr in data_object.__dict__.keys() if not attr.startswith('_')]
        row = {}
        for field in fields:
            value = getattr(data_object, field)
            if field.startswith('date') and value is not None:
                row.update({field: value.strftime('%Y-%m-%d %H:%M:%S')})
            else:
                row.update({field: parse_value(value)})
        object_group.append(row)

    for data_object in object_group:
        result.update(**data_object)

    return result

def dict_merge(dct, merge_dct):
    """Mescla diccionarios"""
    for index, item in merge_dct.items():
        if (index in dct and isinstance(dct[index], dict)
                and isinstance(item, collections.Mapping)):
            dict_merge(dct[index], item)
        else:
            dct[index] = item
