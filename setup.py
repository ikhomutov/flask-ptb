#!/usr/bin/env python
"""
Flask-PythonTelegramBot
-----------------------

Flask-PythonTelegramBot long description

Links
`````
* `development version <https://github.com/iskhomutov/flask-ptb>`_
* `documentation <https://flask-ptb.readthedocs.io/en/stable/`_
"""
from setuptools import setup

setup(
    name='Flask-PythonTelegramBot',
    version='0.0.2',
    url='https://github.com/iskhomutov/flask-ptb',
    download_url=(
        'https://github.com/iskhomutov/flask-ptb/archive/0.0.2.tar.gz'),
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
