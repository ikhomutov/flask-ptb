# coding: utf-8
"""Модуль с тестами для библиотеки"""

import pytest
from flask import Flask

from flask_ptb import PTBConfigException
from flask_ptb import TelegramBot


def test_empty_constructor():
    """Тест конструктора без параметров"""
    ptb = TelegramBot()
    assert ptb.bot is None
    assert ptb.dispatcher is None
    assert ptb.updater is None


def test_wrong_config():
    """Тест неверной конфигурации"""
    app = Flask(__name__)
    ptb = TelegramBot()
    with pytest.raises(PTBConfigException):
        ptb.init_app(app)
