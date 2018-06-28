# coding: utf-8
"""Модуль для интеграции библиотеки python-telegram-bot с Flask"""

import logging

from flask import current_app
from flask import jsonify
from flask import request
from telegram import Bot
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import Dispatcher
from telegram.ext import Updater
from telegram.utils.request import Request
from telegram.vendor.ptb_urllib3.urllib3.util.url import parse_url

WEBHOOK = 'WEBHOOK'
POLLING = 'POLLING'

BOT_MODES = (WEBHOOK, POLLING)


class PTBConfigException(Exception):
    """Исключение выбрасываемое если переданы неправильные параметры конфига"""
    pass


def webhook():
    """Метод обрабатывающий обновления от Телеграма"""
    ptb = current_app.ptb
    data = request.get_json(force=True)
    try:
        ptb.logger.debug('Retrieving update object')
        update = Update.de_json(data, current_app.ptb.bot)
        ptb.logger.debug(update)
        ptb.dispatcher.process_update(update)
        ptb.logger.debug('Process update %', update)
    except TelegramError as error:
        ptb.logger.error('TelegramError was raised while processing Update')
        ptb.dispatcher.dispatchError(update, error)
    return jsonify({})


class TelegramBot(object):
    """Основной класс бота, отвечающий за всю интеграцию с Flask"""

    def __init__(self, app=None):
        """Инициализация класса"""
        self.bot = None
        self.dispatcher = None
        self.config = None

        self.logger = logging.getLogger(__name__)

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Настройка и запуск бота"""
        self.config = app.config

        self.init_bot()

        # Определяем режим работы бота - либо с вебхуками, либо опросами
        bot_mode = self.config.get('TELEGRAM_BOT_MODE')
        if not bot_mode or bot_mode not in BOT_MODES:
            bot_mode = POLLING
            self.logger.warning(
                'TELEGRAM_BOT_MODE does not specified, or does not correct. '
                'Used POLLING by default')
        if bot_mode == WEBHOOK:
            self.dispatcher = Dispatcher(self.bot, None)
            site_domain = self.config.get('TELEGRAM_WEBHOOK_DOMAIN')
            if not site_domain:
                raise PTBConfigException
                # raise Exception('You should provide proper '
                #                 'TELEGRAM_WEBHOOK_URL to use WEBHOOK mode')
            hook_route = self.config.get(
                'TELEGRAM_WEBHOOK_ROUTE', '/webhook')
            webhook_url = u'{hook_domain}{hook_route}'.format(
                hook_domain=site_domain,
                hook_route=hook_route)
            self.bot.setWebhook(webhook_url)

            # Регистрация адреса получения вэбхука
            app.add_url_rule(
                hook_route, 'webhook', webhook, methods=['POST'])

        else:
            self.start_polling()

        # Привязываем текущего бота к приложению для корректной обработки
        # принятого через вэбхук обновления
        app.ptb = self

    def init_bot(self):
        token = self.config.get('TELEGRAM_TOKEN')
        if not token:
            raise PTBConfigException

        # Настраиваем класс Request для бота
        proxy_url = None
        urllib3_proxy_kwargs = None
        if self.config.get('TELEGRAM_PROXY_URL'):
            proxy_url = self.config.get('TELEGRAM_PROXY_URL')
            urllib3_proxy_kwargs = {
                'username': self.config.get('TELEGRAM_PROXY_USERNAME'),
                'password': self.config.get('TELEGRAM_PROXY_PASSWORD'),
            }
            # Проверяем не прописаны ли в самом адресе юзер и пароль
            auth_part = parse_url(proxy_url).auth
            if auth_part and len(auth_part) == 2:
                username, password = auth_part
                # Перезаписываем, только если данные не были прописаны явно
                urllib3_proxy_kwargs.setdefault('username', username)
                urllib3_proxy_kwargs.setdefault('password', password)
        _request = Request(
            proxy_url=proxy_url, urllib3_proxy_kwargs=urllib3_proxy_kwargs)
        self.bot = Bot(token=token, request=_request)

    def start_polling(self):
        """Настройка бота на опрос серверов для получения обновлений"""
        self.logger.debug('Initializing Updater...')
        updater = Updater(bot=self.bot)
        self.logger.debug('Updater initialized')
        self.dispatcher = updater.dispatcher
        self.logger.debug('Starting polling...')
        updater.start_polling()
        self.logger.debug('Pooling started')

    def add_handler(self, method, *args, **kwargs):
        """Регистрация хендлера с логированием"""
        self.dispatcher.add_handler(method, *args, **kwargs)
        self.logger.info('Handler % added', repr(method))
