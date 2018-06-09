#!/usr/bin/env python
"""
Flask-PythonTelegramBot
-----------------------

Flask-PythonTelegramBot long description

Links
`````
* `development version <https://github.com/iskhomutov/flask-ptb>`_
"""
from setuptools import setup

setup(
    name='Flask-PythonTelegramBot',
    version='0.0.1',
    url='https://github.com/iskhomutov/flask-ptb',
    download_url=(
        'https://github.com/iskhomutov/flask-ptb/archive/0.0.1.tar.gz'),
    license='MIT',
    author='Ivan Khomutov',
    author_email='iskhomutov@gmail.com',
    description='python-telegram-bot integration with Flask',
    long_description=__doc__,
    py_modules=['flask_ptb'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.10',
        'python-telegram-bot==10.1.0'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
