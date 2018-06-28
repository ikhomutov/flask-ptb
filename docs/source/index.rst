.. flask-ptb documentation master file, created by
   sphinx-quickstart on Sat Jun 30 07:08:21 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Flask-PythonTelegramBot
=======================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

The **Flask-PythonTelegramBot** extension integrates the `python-telegram-bot`_ library with `Flask`_.

Installation
------------

Install with **pip**::

    pip install Flask-PythonTelegramBot

or download the latest version from version control::

    git clone https://github.com/iskhomutov/flask-ptb.git
    cd flask-ptb
    python setup.py dev

If you are using **virtualenv**, it is assumed that you are installing 
**Flask-PythonTelegramBot** in the same virtualenv as your Flask application.


Quick start
-----------

.. code:: python

    from flask import Flask
    from flask-ptb import TelegramBot
    from telegram.ext import MessageHandler
    from telegram.ext import Filters

    app = Flask(__name__)
    app.config['TELEGRAM_TOKEN'] = '1234:abcd'
    ptb = TelegramBot()
    ptb.init_app(app)

    def echo(bot, update):
        update.message.reply_text(update.message.text)


    ptb.add_handler(MessageHandler(Filters.text, echo))


    if __name__ == '__main__':
        app.run()

Configuration
-------------

**Flask-PythonTelegramBot** uses the following application-level configuration
variables:

* ``TELEGRAM_TOKEN`` - Telegram Bot API token you received from `@BotFather`

* ``TELEGRAM_BOT_MODE`` - method will used for receiving new updates.

  Possible choices: 
  
  - *POLLING*
  - *WEBHOOK*

  **Default**: *POLLING*

* ``TELEGRAM_WEBHOOK_DOMAIN``
* ``TELEGRAM_WEBHOOK_ROUTE``

  **Default**: */webhook*

* ``TELEGRAM_PROXY_URL``
* ``TELEGRAM_PROXY_USERNAME``
* ``TELEGRAM_PROXY_PASSWORD``

.. _Flask: http://flask.pocoo.org
.. _python-telegram-bot: https://python-telegram-bot.org
