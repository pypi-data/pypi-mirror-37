#!/usr/bin/env python
"""setup.py

setup.py for cbpro2 python package.
"""
from setuptools import find_packages
from setuptools import setup

INSTALL_REQUIRES = [
    'pymongo>=3.5.1',
    'python-dateutil',
    'requests>=2.13.0',
    'six>=1.10.0',
    'sortedcontainers>=1.5.9',
    'websocket-client>=0.40.0',
]

TESTS_REQUIRE = [
    'pytest',
    'coverage',
]

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name='cbpro2',
    version='1.0.1',
    author='Daniel Paquin',
    author_email='dpaq34@gmail.com',
    license='MIT',
    url='https://github.com/yiwensong/coinbasepro-python',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    description='The unofficial Python client for the Coinbase Pro API',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    keywords=[
        'gdax',
        'gdax-api',
        'orderbook',
        'trade',
        'bitcoin',
        'ethereum',
        'BTC',
        'ETH',
        'client',
        'api',
        'wrapper',
        'exchange',
        'crypto',
        'currency',
        'trading',
        'trading-api',
        'coinbase',
        'pro',
        'prime',
        'coinbasepro',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
