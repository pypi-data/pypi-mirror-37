# -*- coding: utf-8 -*-
""" Helpers herramientas para recursos de ambientes"""
from dotenv import load_dotenv

def load_env_file(env_file):
    """Carga de archivos .env"""
    load_dotenv(env_file)
