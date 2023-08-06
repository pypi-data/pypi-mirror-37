#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: orm/connections/rethinkdb_connection.py
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 19.10.2018
import logging
import rethinkdb as r

from functools import wraps
from inflection import underscore

from .connection import Connection


LOGGER = logging.getLogger(__name__)


class RethinkdbConnection(Connection):
    """A class for rethinkdb connection
    """
    tables = []

    @classmethod
    def connect(cls):
        """Initialize connection with given arguments

        Host, Port is required, and KeyError raised if not in given arguments.
        """
        try:
            database = cls.values.pop('database', 'test')
            cls.values['db'] = database
            cls.session = r.connect(**cls.values)
        except Exception, e:
            LOGGER.exception(e)
            cls.connected = False
        else:
            LOGGER.info("Successfully Build Connection")
            cls.connected = True

    @classmethod
    def create_all(cls):
        """Create all tables in metadata
        """
        if cls.session.db not in r.db_list().run(cls.session):
            r.db_create(cls.session.db).run(cls.session)
        for table in cls.tables:
            if table in r.db(cls.session.db).table_list().run(cls.session):
                continue
            r.db(cls.session.db).table_create(table).run(cls.session)

    @classmethod
    def drop_all(cls):
        """Drop all tables in metadata
        """
        r.db_drop(cls.session.db).run(cls.session)

    @classmethod
    def close(cls):
        """Close connection
        """
        cls.session.close()
        cls.connected = False

    @classmethod
    def get_session(cls):
        return cls.session

    @classmethod
    def with_session(cls, **kwgs):
        """Decorator for creating connection context around function.

        Wrap the function with a connection.

        Example:

        .. code-block:: python

            @with_session
            def A(some_arguments, session):
                pass

        Notice that only in keywords can you pass your own session rather than
        the created session, or a TypeError will raise for multiple arguments
        of session passed into the same function. In other works, following
        code will raise a TypeError:

        .. code-block:: python

            @with_session
            def A(some_arguments, session):
                pass

            A('test', your_own_session) # Raise TypeError
            A('test', session=your_own_session) # Safe

        Return:
            a wrapped func
        """
        def decorator(func):

            @wraps(func)
            def wrapper(*args, **kwargs):
                session = kwargs.pop('session', cls.session)
                kwargs['session'] = session

                LOGGER.info('Connection start')

                try:
                    result = func(*args, **kwargs)
                except Exception, e:
                    LOGGER.exception(e)
                    raise e
                else:
                    LOGGER.info('Connection exit in normal')

                return result

            return wrapper
        return decorator


class RethinkdbBase(object):
    """Persisted object base class
    """
    @classmethod
    def declared_attr(cls, new_cls):
        class WithTableClass(new_cls):
            __table_name = underscore(new_cls.__name__)
            # Set class attribute for table in rethinkdb
            table = r.table(__table_name)
            # Append table name in connection
            RethinkdbConnection.tables.append(__table_name)
        return WithTableClass

    @classmethod
    def add(cls, obj, session):
        """Add new obj with given connection

        Args:
            obj: (dict)
            session: (rethinkdb.Connection)

        """
        cls.table.insert(obj).run(session)

    @classmethod
    def batch_add(cls, objs, session):
        """Batch add objects with given connection

        Args:
            objs: ([dict,])
            session: (rethinkdb.Connection)
        """
        cls.table.insert(objs).run(session)

    @classmethod
    def delete_all(cls, session):
        """Delete all objects with given connection

        Args:
            session: (rethinkdb.Connection)
        """
        cls.table.delete().run(session)

    @classmethod
    def query(cls, session):
        """Query all results

        Args:
            session: (rethinkdb.Connection)

        Return:
            [dict,]
        """
        return list(cls.table.run(session))
