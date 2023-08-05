# -*- coding: utf-8 -*-

"""
Define locale code.
"""


class Locale(object):
    """
    Hardcoded locale code table.
    """
    en_US = "en-US"
    zh_CN = "zh-CN"
    zh_TW = "zh-TW"
    fr_FR = "fr_FR"
    de_DE = "de-DE"
    ja_JA = "ja-JA"
    es_ES = "es-ES"


locale_list = [
    value
    for key, value in Locale.__dict__.items()
    if not key.startswith("_")
]
