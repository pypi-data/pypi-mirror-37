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


class DBSessionMaker(object):
    """An instance of sessionmaker.
    """
    __values = ['user', 'password', 'host', 'port', 'database']
    _ConnectionMaker = {
        'mysql': SQLConnection, 'rethinkdb': RethinkdbConnection,
        'influxdb': InfluxdbConnection
    }

    @classmethod
    def connect(cls, **kwargs):
        """Initialize connection with given arguments

        User, Password, Host, Port, Database is required, and KeyError raised
        if not in given arguments.
        """
        backend = kwargs.get('backend', 'mysql')
        if cls._ConnectionMaker[backend].connected:
            return
        cls._ConnectionMaker[backend].values = {
            key: val for key, val in kwargs.items() if key in cls.__values
        }
        cls._ConnectionMaker[backend].connect()

    @classmethod
    def create_all(cls, backend='mysql'):
        """Create all tables in metadata
        """
        cls._ConnectionMaker[backend].create_all()

    @classmethod
    def drop_all(cls, backend='mysql'):
        """Drop all tables in metadata
        """
        cls._ConnectionMaker[backend].drop_all()

    @classmethod
    def close(cls, backend='mysql'):
        """Close connection
        """
        cls._ConnectionMaker[backend].close()

    @classmethod
    def with_session(cls, **kwargs):
        backend = kwargs.pop('backend', 'mysql')
        return cls._ConnectionMaker[backend].with_session(**kwargs)

    @classmethod
    def get_session(cls, backend='mysql'):
        return cls._ConnectionMaker[backend].get_session()
