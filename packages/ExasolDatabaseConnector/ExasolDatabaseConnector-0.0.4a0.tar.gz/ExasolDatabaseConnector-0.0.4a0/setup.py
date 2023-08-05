#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='ExasolDatabaseConnector',
    version="0.0.4a",
    license="MIT",
    maintainer="Florian Reck",
    maintainer_email="support@exasol.com",
    description="Exasol database connector class written in python",
    long_description="Exasol database connector classes using ODBC or WebSockets",
    url='https://github.com/florian-reck/ExaDatabase',
    packages=[
        'ExasolDatabaseConnector',
        'ExasolDatabaseConnector.ExaDatabaseAbstract',
        'ExasolDatabaseConnector.ExaWebSockets',
        'ExasolDatabaseConnector.ExaOdbcDriver'
    ],
    install_requires=[
        'websocket_client',
        'rsa',
	'EXASOL-DB-API',
        'pyodbc'
    ]
)
