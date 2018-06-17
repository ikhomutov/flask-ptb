# coding: utf-8

import os
from dotenv import load_dotenv
from flask import Flask
from telegram.ext import MessageHandler
from telegram.ext import Filters

from flask_ptb import TelegramBot


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    print('loading dotenv')
    load_dotenv(dotenv_path)


class Config:
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    TELEGRAM_PROXY_URL = os.environ.get('TELEGRAM_PROXY_URL')
    TELEGRAM_PROXY_USERNAME = os.environ.get('TELEGRAM_PROXY_USERNAME')
    TELEGRAM_PROXY_PASSWORD = os.environ.get('TELEGRAM_PROXY_PASSWORD')


app = Flask(__name__)
app.config.from_object(Config)

ptb = TelegramBot()
ptb.init_app(app)


def echo(bot, update):
    update.message.reply_text(update.message.text)


ptb.add_handler(MessageHandler(Filters.text, echo))


if __name__ == '__main__':
    app.run()
