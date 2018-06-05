# coding: utf-8

import logging

from flask import current_app
from flask import request

from telegram import Bot
from telegram.ext import Dispatcher
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import ConversationHandler

WEBHOOK = 'WEBHOOK'
POLLING = 'POLLING'

BOT_MODES = (WEBHOOK, POLLING)

def webhook():
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        print('Received invalid request:{}'.format(repr(request)))
        return jsonify({})
    try:
        update = Update.de_json(data, ptb.bot)
        current_app.telegram_dispatcher.process_update(update)
        print('Process update {}'.format(update))
    except TelegramError as te:
        print('TelegramError was raised while processing Update')
        current_app.telegram_dispatcher.dispathError(update, te)
    except Exception:
        print('An uncaught error was raised while processint Update')
    finally:
        return jsonify({})

class TelegramBot(object):
    bot = None
    dispatcher = None
    updater = None

    logger = logging.getLogger('TelegramBot')

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        token = app.config['TELEGRAM_TOKEN']
        if not token:
            self.logger.error('TOKEN for TelegramBot is not provided!')
            return
        bot_mode = app.config['TELEGRAM_BOT_MODE']
        if not bot_mode or bot_mode not in BOT_MODES:
            app.config['TELEGRAM_BOT_MODE'] = 'POLLING'
            self.logger.warning(
                'TELEGRAM_BOT_MODE does not specified, or does not correct. '
                'Used POLLING by default')
        if bot_mode == WEBHOOK:
            webhook_prefix = app.config['TELEGRAM_WEBHOOK_PREFIX']
            webhook_url = u'{hook_url}{hook_prefix}'.format(
                hook_url=app.config['TELEGRAM_WEBHOOK_URL'],
                hook_prefix=webhook_prefix)
            workers = app.config['TELEGRAM_WORKERS']

            # Регистрация адреса получения вэбхука
            app.add_url_rule(webhook_prefix, 'webhook', webhook)

            self.initialize_webhook_bot(app, token, webhook_url, workers)
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
            self.initialize_polling_bot(app, token, request_kwargs)

    def initialize_webhook_bot(self, app, token, webhook_url, workers):
        """Настройка бота, принимающие обновления через вэбхуки"""
        self.logger.info('Initializing TelegramBot...')
        self.logger.debug('Creating instance of telegram.Bot...')
        self.bot = Bot(token=token)
        self.logger.debug('Instance of telegram.Bot created')
        self.logger.debug('Creating instance of telegram.ext.Dispatcher...')
        self.dispatcher = Dispatcher(self.bot, None, workers=workers)
        app.telegram_dispatcher = self.dispatcher
        self.logger.debug('Instance of telegram.ext.Dispatcher created')
        self.logger.debug('Setting webhook...')
        self.bot.setWebhook(webhook_url)
        self.logger.debug('Webhook setted')
        self.logger.info('TelegramBot initialized')

    def initialize_polling_bot(self, app, token, request_kwargs=None):
        """Настройка бота на опрос серверов для получения обновлений"""
        print('Starting Updater...')
        self.updater = Updater(
            token=token,
            request_kwargs=request_kwargs,
        )
        print('Updater started')
        self.bot = self.updater.bot
        self.dispatcher = self.updater.dispatcher
        app.telegram_dispatcher = self.dispatcher
        self.bot.delete_webhook()
        print('Start polling...')
        self.updater.start_polling()
        print('Pooling')

    def add_handler(self, method, *args, **kwargs):
        """Регистрация хендлера с уведомлением"""
        self.dispatcher.add_handler(method, *args, **kwargs)
        print('Handler {} added'.format(repr(method)))
