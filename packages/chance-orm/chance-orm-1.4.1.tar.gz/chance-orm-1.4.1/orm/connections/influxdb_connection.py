#!/usr/bin/env python
#  -*- coding: utf-8 -*-
# File: influxdb_connection.py
# Author: MS Cai <i@unoiou.com>
# ---
# Last Modified: Monday, 22nd October 2018 10:19:54 am
# Modified By: MS Cai <i@unoiou.com>
# ---
# Copyright 2018 All rights reserved, Chance Focus Co.,ltd.
import logging

import influxdb as influx
from functools import wraps
from inflection import underscore

from .connection import Connection


LOGGER = logging.getLogger(__name__)


def serializer(func):
    """Serialize resultset to a list.
    """
    @wraps(func)
    def _decorator(*args, **kwargs):
        return list(func(*args, **kwargs).get_points())
    return _decorator


class InfluxdbConnection(Connection):
    """Class for Influxdb connection.
    """
    measurements = []

    @classmethod
    def connect(cls):
        """Initialize connection with given arguments

        User, Password, Host, Port, Database is required, and KeyError raised
        if not in given arguments.
        """
        try:
            cls.session = influx.InfluxDBClient(**cls.values)
        except Exception as e:
            LOGGER.exception(e)
        else:
            LOGGER.info('Successfully build influxdb connection!')

    @classmethod
    def create_all(cls):
        """Create all tables in metadata
        """
        if cls.values[u'database'] not in [
            item[u'name'] for item in cls.session.get_list_database()
        ]:
            cls.session.create_database(dbname=cls.values[u'database'])

    @classmethod
    def drop_all(cls):
        """Drop all tables in metadata
        """
        cls.session.drop_database(dbname=cls.values[u'database'])

    @classmethod
    def close(cls):
        """Close connection
        """
        cls.session.close()

    @classmethod
    def with_session(cls, *args, **kwargs):
        """Decorator for creating session context around function.
        """
        def _decorator(func):
            @wraps(func)
            def _wrapper(*args, **kwargs):
                session = kwargs.pop('session', cls.session)
                kwargs['session'] = session

                LOGGER.info('Connection start')

                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    LOGGER.exception(e)
                    raise e
                else:
                    LOGGER.info('Connection exit normally')
                return result

            return _wrapper
        return _decorator


class InfluxdbBase(object):
    """Persisted object for InfluxDB.
    """
    @classmethod
    def declared_attr(cls, new_cls):
        class WithTableClass(new_cls):
            __measurement__ = underscore(new_cls.__name__)
            # Append measurement name in connection
            InfluxdbConnection.measurements.append(__measurement__)
        return WithTableClass

    @classmethod
    def add(cls, obj, session):
        """Add object to database.

        Args:
            obj: a dict
            session: an instance of `InfluxDBClient`
        """
        obj['measurement'] = cls.__measurement__
        session.write_points([obj])

    @classmethod
    def batch_add(cls, obj, session):
        """Write points to measurements in current database

        Example:

        .. code block:: python

            obj = [
                {
                    'tags':{
                        'tag1': 'tag_value1'
                    },
                    'time': '2009-11-10T23:00:00Z',
                    'fields': {
                        'field_key1': 'field_value1',
                        'field_key2': 0.34
                    }
                }, ...
            ]

        Args:
            obj: a list of dict
            session: an instance of `InfluxDBClient`
        """
        for point in obj:
            point['measurement'] = cls.__measurement__
        session.write_points(obj)

    @classmethod
    @serializer
    def query(cls, session):
        """Query all result.

        Args:
            an influxdb resultset
            session: an instance of `InfluxDBClient`

        Return:
            a list
        """
        return session.query('select * from {}'.format(cls.__measurement__))

    @classmethod
    def delete_all(cls, session):
        """Drop a measurement.

        Args:
            session: an instance of `InfluxDBClient`
        """
        session.drop_measurement(measurement=cls.__measurement__)
