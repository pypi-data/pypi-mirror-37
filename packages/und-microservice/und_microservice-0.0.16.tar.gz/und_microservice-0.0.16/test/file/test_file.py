# -*- coding: utf-8 -*-
"""Test module file"""

from und_microservice.commons.file import File

def test_yml_file():
    """Test read yml file"""
    espected_data = {
        'service': {
            'name': "x",
            'ip': "127.0.0.1",
            'user_name': "user"
        }
    }
    read_data = File.read_yml('test/resources/test_other_file.yml')
    assert espected_data == read_data

def test_json_file():
    """Test read json file"""
    espected_data = {
        "value": 1,
        "name": "example",
        "version": "1.0.1"
    }
    read_data = File.read_json('test/resources/test_file.json')
    assert espected_data == read_data

def test_txt_file():
    """Test read txt file"""
    espected_data = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sem dolor'

    read_data = File.read_yml('test/resources/test_file.txt')
    assert espected_data == read_data
