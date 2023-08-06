# -*- coding: utf-8 -*-
"""Test helper para url"""

from und_microservice.helper.url import get_filter_in

def test_split_query_string():
    """Test convertir querystring en array"""
    pass

def test_get_fileter_in():
    """Test para recuperar los filtros de una lista"""
    test_filters = {
        'index': [
            'i',
            'j'
        ],
        'index_b': 'name'
    }
    espected_list = {
        'index': [
            'i',
            'j'
        ]
    }
    result = get_filter_in(test_filters)
    assert espected_list == result

def test_join_query_string():
    """Union de query string"""
    pass
