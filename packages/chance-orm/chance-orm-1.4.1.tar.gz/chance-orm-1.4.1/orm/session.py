#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: orm/session.py
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 01.02.2018
"""Database Connection
"""
import logging


from orm.connections import (
    SQLConnection, RethinkdbConnection, InfluxdbConnection
)


LOGGER = logging.getLogger(__name__)


CONNECTION_TYPES = {
    'mysql': SQLConnection,
    'rethinkdb': RethinkdbConnection,
    'influxdb': InfluxdbConnection
}


class DBSessionMaker(object):
    """An instance of sessionmaker.
    """
    __values = ['user', 'password', 'host', 'port', 'database']
    _ConnectionMaker = None

    @classmethod
    def connect(cls, **kwargs):
        """Initialize connection with given arguments

        User, Password, Host, Port, Database is required, and KeyError raised
        if not in given arguments.
        """
        cls._ConnectionMaker = CONNECTION_TYPES[kwargs.get('backend', 'mysql')]
        cls._ConnectionMaker.values = {
            key: val for key, val in kwargs.items() if key in cls.__values
        }
        cls._ConnectionMaker.connect()

    @classmethod
    def create_all(cls):
        """Create all tables in metadata
        """
        cls._ConnectionMaker.create_all()

    @classmethod
    def drop_all(cls):
        """Drop all tables in metadata
        """
        cls._ConnectionMaker.drop_all()

    @classmethod
    def close(cls):
        """Close connection
        """
        cls._ConnectionMaker.close()

    @classmethod
    def with_session(cls, **kwargs):
        return cls._ConnectionMaker.with_session()
