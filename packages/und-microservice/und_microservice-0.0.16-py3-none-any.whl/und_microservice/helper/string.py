# -*- coding: utf-8 -*-
"""Helpers para manejo de strings"""

def concat(item_list, separator="-"):
    """Concatena un array de string con un separador"""
    return separator.join(str(item) for item in item_list)
