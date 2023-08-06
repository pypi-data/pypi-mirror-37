#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: orm/connections/sql_connection.py
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 19.10.2018
import arrow
import logging

from datetime import datetime, date, time
from decimal import Decimal
from functools import wraps
from inflection import underscore
from sqlalchemy import create_engine, BIGINT, Column
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declared_attr, as_declarative
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import func

from .connection import Connection


LOGGER = logging.getLogger(__name__)
BASE_VALUE_TYPE = {
    datetime: "_datetime",
    time: "_time",
    date: "_date",
    Decimal: "_decimal"
}

TIME_FORMAT = '%H:%M:%S'
DATE_FORMAT = 'YYYY-MM-DD'
DATETIME_FORMAT = 'YYYY-MM-DD HH:mm:ss'


@as_declarative()
class SQLBase(object):
    """Persisted object base class
    """
    @declared_attr
    def __tablename__(cls):
        return underscore(cls.__name__)

    id = Column('id', BIGINT, primary_key=True)
    gmt_create = Column('gmt_create', DATETIME(fsp=6), default=func.now(6))
    gmt_modified = Column(
        'gmt_modified', DATETIME(fsp=6), default=func.now(6),
        onupdate=func.now(6)
    )

    @classmethod
    def add(cls, obj, session):
        """Add new obj with given session

        Args:
            obj: (dict)
            session: ``DBSession`` instance
        """
        session.add(cls(**obj))

    @classmethod
    def batch_add(cls, objs, session):
        """Batch add objects with given session

        Args:
            objs: a list of dicts
            session: ``DBSession`` instance
        """
        session.bulk_insert_mappings(cls, objs)

    @classmethod
    def delete_all(cls, session):
        """Delete all objects with given session

        Args:
            session: ``DBSession`` instance
        """
        session.query(cls).delete()

    @classmethod
    def query(cls, session):
        """Query all results

        Args:
            session: ``DBSession`` instance

        Return:
            [dict,]
        """
        return [val.__dict__ for val in session.query(cls).all()]

    def get_items(self):
        """Get columns and values from ``_sa_instance_state.attr.items()``
        """
        return self._sa_instance_state.attrs.items()

    def __repr__(self):
        """Return str format of the class

        Return:
            a str
        """
        return '{0}: {1}'.format(
            self.__class__.__name__,
            [(key, getattr(self, key)) for key, _ in self.get_items()]
        )

    def __eq__(self, other):
        """Overlap the eq method to compare object to dict.

        If key not in self, then return False, or get the value in self. If the
        type of the value in ``value_type_dict``, namely that the value need a
        transform before compare, call corresponding method in
        ``value_type_dict``. Finally, return if the value is equal to self
        value.

        Args:
            other: a dict with all key-value pairs to be compared.
        """
        if not isinstance(other, dict):
            LOGGER.info("Value not dict")
            return False

        for key, value in other.iteritems():
            try:
                self_value = getattr(self, key)
            except AttributeError:
                LOGGER.info("{0} not found in object".format(key))
                return False

            try:
                method = BASE_VALUE_TYPE[type(self_value)]
                self_value = getattr(self, method)(self_value)
            except KeyError:
                pass

            if self_value == value:
                continue
            LOGGER.info(
                "Value not matched for {0}: {1} | {2}".format(
                    key, self_value, value
                )
            )
            return False
        return True

    def _time(self, self_value):
        """Method to transform ``time``.

        Args:
            self_value: ``time`` instance

        Return:
            a str
        """
        return self_value.strftime(TIME_FORMAT)

    def _date(self, self_value):
        """Method to transform ``date``.

        Args:
            self_value: ``date`` instance

        Return:
            a str
        """
        return arrow.get(self_value).format(DATE_FORMAT)

    def _datetime(self, self_value):
        """Method to transform ``datetime``.

        Args:
            self_value: ``datetime`` instance

        Return:
            a str
        """
        return arrow.get(self_value).format(DATETIME_FORMAT)

    def _decimal(self, decimal):
        """Method to transform ``decimal.Decimal()``

        Args:
            self_value: ``Decimal`` instance

        Return:
            a str
        """
        return '{0:.3f}'.format(decimal)


class SQLConnection(Connection):
    """An instance of sessionmaker.
    """
    __session_maker = None
    base = SQLBase

    @classmethod
    def connect(cls):
        """Initialize connection with given arguments

        User, Password, Host, Port, Database is required, and KeyError raised
        if not in given arguments.
        """
        try:
            cls.__engine = create_engine(
                (
                    u'mysql+mysqldb://{user}:{password}@{host}:{port}/'
                    u'{database}?charset=utf8'
                ).format(**cls.values), pool_recycle=3600, encoding="utf8",
            )
        except Exception, e:
            LOGGER.exception(e)
            cls.connected = False
        else:
            LOGGER.info("Successfully Build Connection")
            cls.Session = scoped_session(sessionmaker(bind=cls.__engine))
            cls.connected = True

    @classmethod
    def create_all(cls):
        """Create all tables in metadata
        """
        LOGGER.info(cls.base.metadata.sorted_tables)
        cls.base.metadata.create_all(cls.__engine)
        cls.Session.close()

    @classmethod
    def drop_all(cls):
        """Drop all tables in metadata
        """
        cls.Session.close()
        cls.base.metadata.drop_all(cls.__engine)

    @classmethod
    def close(cls):
        """Close connection
        """
        cls.Session.close()
        cls.__engine.dispose()
        cls.connected = False

    @classmethod
    def get_session(cls):
        return cls.Session()

    @classmethod
    def with_session(cls, rollback=False, nested=False):
        """Decorator for creating session context around function.

        Wrap the function with a session created from scoped session. If
        subtransaction is True, a savepoint is created in this context to
        ensure that rollback only to this point.

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

        Args:
            rollback: a boolean controls whether rollback in the end.
            nested: a boolean controls whether the transaction is nested.

        Return:
            a wrapped func
        """
        def decorator(func):

            @wraps(func)
            def wrapper(*args, **kwargs):
                session = kwargs.pop('session', cls.Session())
                kwargs['session'] = session

                exit_action = session.rollback if rollback else session.commit

                if nested:
                    session.begin_nested()
                    LOGGER.info('Sub session start')
                LOGGER.info('Session start')

                try:
                    result = func(*args, **kwargs)
                except Exception, e:
                    LOGGER.exception(e)
                    session.rollback()
                    raise e
                else:
                    exit_action()
                    LOGGER.info('Session exit in normal')
                finally:
                    session.close()

                return result

            return wrapper
        return decorator
