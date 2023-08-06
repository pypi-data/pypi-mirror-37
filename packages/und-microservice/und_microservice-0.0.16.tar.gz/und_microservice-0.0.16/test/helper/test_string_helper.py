# -*- coding: utf-8 -*-
"""Test helper para datos genericos"""

from und_microservice.helper.string import concat

def test_concat_helper():
    """Prueba de concatenacion de elementos de un array"""
    test_data = [
        'salu',
        'do',
        'hola'
    ]
    espected_string = 'salu_do_hola'
    result = concat(test_data, '_')
    assert espected_string == result
