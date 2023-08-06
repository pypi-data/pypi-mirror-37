# -*- coding: utf-8 -*-
"""Test helper para datos genericos"""

from und_microservice.helper.data import dict_merge

def test_dict_merge():
    """Test para probar metodo para mesclar diccionarios"""
    dict_a = {
        'service': {
            'name': "x",
            'ip': "127.0.0.1",
            'user_name': "user"
        }
    }

    dict_b = {
        'db': {
            'connection': "mysql",
            'host': "localhost",
            'user': "root",
            'password': "password",
            'port': "3307",
            'database': "db",
            'lifetime': 180
        }
    }
    espected_dic = {
        'service': {
            'name': "x",
            'ip': "127.0.0.1",
            'user_name': "user"
        },
        'db': {
            'connection': "mysql",
            'host': "localhost",
            'user': "root",
            'password': "password",
            'port': "3307",
            'database': "db",
            'lifetime': 180
        },
    }

    dict_merge(dict_a, dict_b)
    assert dict_a == espected_dic
