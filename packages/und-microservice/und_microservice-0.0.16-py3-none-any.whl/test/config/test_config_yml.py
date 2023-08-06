# -*- coding: utf-8 -*-
"""Prueba del modulo conig"""

from und_microservice.config.config_yaml import ConfigYaml

def test_get_all():
    """Probando cargar todo los config"""
    config = ConfigYaml('test/resources/')
    espected_data = {
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
        }
    }
    all_data = config.get_all()
    assert espected_data == all_data

def test_get_key():
    """Test para recurar un valor grupo especifico"""
    config = ConfigYaml('test/resources/')
    espected_data = {
        'name': "x",
        'ip': "127.0.0.1",
        'user_name': "user"
    }
    service = config.get_key('service')
    assert service == espected_data
