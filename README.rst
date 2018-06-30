Flask-PythonTelegramBot
=======================

Make it easy to integrate python-telegram-bot library with Flask-based project

.. image:: https://travis-ci.org/iskhomutov/flask-ptb.svg?branch=master
    :target: https://travis-ci.org/iskhomutov/flask-ptb

.. image:: https://coveralls.io/repos/github/iskhomutov/flask-ptb/badge.svg?branch=master
    :target: https://coveralls.io/github/iskhomutov/flask-ptb?branch=master

.. image:: https://readthedocs.org/projects/flask-ptb/badge/?version=latest
    :target: https://flask-ptb.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/License-MIT-green.svg
    :target: https://opensource.org/licenses/MIT


Instalation
-----------

``pip install Flask-PythonTelegramBot``

Usage
-----

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

Name it **server.py** and run with ``python server.py``


Compatibility
-------------
- Python 3.4, 3.5, 3.6
- Flask >= 0.10

Author
------
Created by Ivan Khomutov <iskhomutov@gmail.com> in 2018
