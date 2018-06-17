# coding: utf-8
"""Модуль с тестами для библиотеки"""

import pytest
from flask import Flask

from flask_ptb import PTBConfigException
from flask_ptb import TelegramBot


class TestConfig(object):
    TELEGRAM_TOKEN = '123:abcd'


def test_empty_constructor():
    """Тест конструктора без параметров"""
    ptb = TelegramBot()
    assert ptb.bot is None
    assert ptb.dispatcher is None


def test_wrong_config():
    """Тест неверной конфигурации"""
    app = Flask(__name__)
    ptb = TelegramBot()
    with pytest.raises(PTBConfigException):
        ptb.init_app(app)


def test_init_bot():
    app = Flask(__name__)
    app.config.from_object(TestConfig)
    ptb = TelegramBot()
    ptb.config = app.config
    ptb.init_bot()
    assert ptb.bot is not None
    assert ptb.bot.token == TestConfig.TELEGRAM_TOKEN
