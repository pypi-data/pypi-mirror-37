#!/usr/bin/env python
from setuptools import setup

setup(
    name='Block_Fund_Trading',
    version='1.0',
    packages=['BinanceAPI', 'Scrappers', 'Keys', 'OrderManager', 'AccountManager', 'Database', 'Symbols' , 'db'],
    description='ICO-python-trading',
    url='',
    author='Maarten Elgar',
    author_email='maartenelgar12@gmail.com',
    install_requires=['requests', 'six', 'Twisted', 'pyOpenSSL', 'autobahn', 'service-identity', 'dateparser', 'urllib3', 'chardet', 'certifi', 'cryptography', 'pandas', 'numpy', 'os' ],
    keywords='',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
