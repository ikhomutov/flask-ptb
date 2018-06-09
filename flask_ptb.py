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

WEBHOOK = 'WEBHOOK'
POLLING = 'POLLING'

BOT_MODES = (WEBHOOK, POLLING)


def webhook():
    """Метод обрабатывающий обновления от Телеграма"""
    print('Load request data')
    data = request.get_json(force=True)
    print('Request data: ')
    print(data)
    try:
        print('Retrieving update object')
        update = Update.de_json(data, current_app.ptb.bot)
        print(update)
        current_app.ptb.dispatcher.process_update(update)
        print('Process update {}'.format(update))
    except TelegramError as error:
        print('TelegramError was raised while processing Update')
        current_app.ptb.dispatcher.dispatchError(update, error)
    return jsonify({})


class TelegramBot(object):
    """Основной класс бота, отвечающий за всю интеграцию с Flask"""

    def __init__(self, app=None):
        """Инициализация класса"""
        self.bot = None
        self.updater = None
        self.dispatcher = None

        self.logger = logging.getLogger(__name__)

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Настройка и запуск бота исходя из конфига в приложении Flask"""
        app.ptb = self
        token = app.config['TELEGRAM_TOKEN']
        if not token:
            self.logger.error('TOKEN for TelegramBot is not provided!')
            return
        bot_mode = app.config['TELEGRAM_BOT_MODE']
        if not bot_mode or bot_mode not in BOT_MODES:
            bot_mode = POLLING
            self.logger.warning(
                'TELEGRAM_BOT_MODE does not specified, or does not correct. '
                'Used POLLING by default')
        if bot_mode == WEBHOOK:
            site_url = app.config['SITE_URL']
            if not site_url:
                raise RuntimeError(
                    'You should provide proper SITE_URL to use WEBHOOK mode')
            webhook_prefix = app.config('TELEGRAM_WEBHOOK_PREFIX', '/webhook')
            webhook_url = u'{hook_url}{hook_prefix}'.format(
                hook_url=app.config['SITE_URL'],
                hook_prefix=webhook_prefix)

            # Регистрация адреса получения вэбхука
            app.add_url_rule(
                webhook_prefix, 'webhook', webhook, methods=['POST'])

            self.initialize_webhook_bot(token, webhook_url)
        else:
            if app.config['TELEGRAM_PROXY_URL']:
                request_kwargs = {
                    'proxy_url': app.config['TELEGRAM_PROXY_URL'],
                    'urllib3_proxy_kwargs': {
                        'username': app.config['TELEGRAM_PROXY_USERNAME'],
                        'password': app.config['TELEGRAM_PROXY_PASSWORD'],
                    },
                }
            else:
                request_kwargs = None

            self.initialize_polling_bot(token, request_kwargs)

    def initialize_webhook_bot(self, token, webhook_url):
        """Настройка бота, принимающие обновления через вэбхуки"""
        self.logger.info('Initializing TelegramBot...')
        self.logger.debug('Creating instance of telegram.Bot...')
        self.bot = Bot(token=token)
        self.logger.debug('Instance of telegram.Bot created')
        self.logger.debug('Creating instance of telegram.ext.Dispatcher...')
        self.dispatcher = Dispatcher(self.bot, None)
        self.logger.debug('Instance of telegram.ext.Dispatcher created')
        self.logger.debug('Setting webhook...')
        self.bot.setWebhook(webhook_url)
        self.logger.debug('Webhook setted')
        self.logger.info('TelegramBot initialized')

    def initialize_polling_bot(self, token, request_kwargs=None):
        """Настройка бота на опрос серверов для получения обновлений"""
        self.logger.info('Initializing Bot in POLLING mode')
        self.logger.debug('Initializing Updater...')
        self.updater = Updater(
            token=token,
            request_kwargs=request_kwargs,
        )
        self.logger.debug('Updater initialized')
        self.bot = self.updater.bot
        self.logger.debug('Deleting webhook...')
        self.bot.delete_webhook()
        self.logger.debug('Webhook deleted')
        self.logger.debug('Starting polling...')
        self.updater.start_polling()
        self.logger.debug('Pooling started')
        self.logger.info('Initializing complete')

    def add_handler(self, method, *args, **kwargs):
        """Регистрация хендлера с уведомлением"""
        self.dispatcher.add_handler(method, *args, **kwargs)
        print('Handler {} added'.format(repr(method)))
