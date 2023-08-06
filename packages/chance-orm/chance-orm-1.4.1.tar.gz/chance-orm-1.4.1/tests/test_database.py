#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 02.02.2017
"""Tests of database base class.
"""
import logging

from mock import Mock, patch
from nose import tools

from mock_logger import MockLoggingHandler
from orm import database
from orm.database import DBSession, DBSessionMaker


HANDLER = MockLoggingHandler(level='DEBUG')


def setup_module():
    logger = logging.getLogger('orm.database')
    logger.addHandler(HANDLER)


class TestDBSessionMaker(object):
    """Test class for ``database.DBSessionMaker``
    """
    def setUp(self):
        """Setup mock object
        """
        HANDLER.reset()
        self.fake_arguments = {
            'user': 'test', 'password': 'test', 'host': 'test', 'port': 'test',
            'database': 'test'
        }

    @patch.object(database, 'sessionmaker')
    @patch.object(database, 'MetaData')
    @patch.object(database, 'create_engine')
    def test_connect(self, mock_create, mock_meta, mock_maker):
        """Check if ``DBSessionMaker.__init__`` works

        Args:
            mock_create: the mock object of ``create_engine``
            mock_meta: the mock object of ``MetaData``
            mock_maker: the mock object of ``sessionmaker``
        """
        session_maker = DBSessionMaker(**self.fake_arguments)

        session_maker.connect()

        mock_create.assert_called_with(
            'mysql+mysqldb://test:test@test:test/test?charset=utf8',
            pool_recycle=3600,
            encoding='utf8',
        )
        tools.assert_equals(
            HANDLER.messages['info'], ['Successfully Build Connection']
        )

        mock_meta.assert_called_with(bind=mock_create.return_value)
        tools.assert_equals(mock_meta.return_value, session_maker.metadata)

        mock_create.return_value.connect.assert_called_with()
        tools.assert_equals(
            mock_create.return_value.connect.return_value,
            session_maker.connection
        )

        session_maker.connection.begin.assert_called_with()
        tools.assert_equals(
            session_maker.connection.begin.return_value,
            session_maker.trans
        )

        mock_maker.assert_called_with(bind=session_maker.connection)
        tools.assert_equals(
            session_maker.session_maker, mock_maker.return_value
        )

    @patch.object(database, 'create_engine')
    def test_connect_with_exception(self, mock_create):
        """Check if ``DBSessionMaker.connect`` works when exception raised

        Args:
            mock_create: the mock object of ``create_engine``
        """
        mock_create.side_effect = Exception('test')
        session_maker = DBSessionMaker(**self.fake_arguments)
        session_maker.connect()

        mock_create.assert_called_with(
            'mysql+mysqldb://test:test@test:test/test?charset=utf8',
            pool_recycle=3600,
            encoding='utf8',
        )

        tools.assert_equals(HANDLER.messages['error'], ['test'])

    def test_close(self):
        """Check if ``DBSessionMaker.close`` works
        """
        session_maker = DBSessionMaker(**self.fake_arguments)

        # Mock connection and transaction of the class
        mock_conn, mock_trans = [Mock()] * 2
        session_maker.connection = mock_conn
        session_maker.trans = mock_trans

        session_maker.save()

        mock_trans.commit.assert_called_with()
        mock_conn.close.assert_called_with()

    def test_rollback(self):
        """Check if ``DBSessionMaker.rollback`` works
        """
        session_maker = DBSessionMaker(**self.fake_arguments)

        # Mock connection and transaction of the class
        mock_conn, mock_trans = [Mock()] * 2
        session_maker.connection = mock_conn
        session_maker.trans = mock_trans

        session_maker.rollback()

        mock_trans.rollback.assert_called_with()
        mock_conn.close.assert_called_with()

    @patch.object(DBSessionMaker, 'save')
    @patch.object(DBSessionMaker, 'connect')
    def test_enter_and_exit_normal(self, mock_connect, mock_save):
        """Check if ``DBSessionMaker`` works

        Args:
            mock_connect: the mock object for ``DBSessionMaker.connect``
            mock_save: the mock object for ``DBSessionMaker.save``
        """
        with DBSessionMaker(**self.fake_arguments):
            mock_connect.assert_called_with()
        tools.assert_equals(
            HANDLER.messages['debug'], ['Connection exit in normal']
        )

        mock_save.assert_called_with()

    @patch.object(DBSessionMaker, 'rollback')
    @patch.object(DBSessionMaker, 'connect')
    def test_enter_and_exit_in_rollback(self, mock_connect, mock_rollback):
        """Check if ``DBSessionMaker`` works in rollback

        Args:
            mock_connect: the mock object for ``DBSessionMaker.connect``
            mock_rollback: the mock object for ``DBSessionMaker.rollback``
        """
        self.fake_arguments['rollback'] = True
        with DBSessionMaker(**self.fake_arguments):
            mock_connect.assert_called_with()
        tools.assert_equals(
            HANDLER.messages['debug'], ['Connection rollback']
        )

        mock_rollback.assert_called_with()

    @patch.object(DBSessionMaker, 'rollback')
    @patch.object(DBSessionMaker, 'connect')
    def test_enter_and_exit_in_exception(self, mock_connect, mock_rollback):
        """Check if ``DBSessionMaker`` works in rollback

        Args:
            mock_connect: the mock object for ``DBSessionMaker.connect``
            mock_rollback: the mock object for ``DBSessionMaker.rollback``
        """
        def _nested_func():
            with DBSessionMaker(**self.fake_arguments):
                mock_connect.assert_called_with()
                raise Exception('test')
        tools.assert_raises(Exception, _nested_func)
        tools.assert_equals(
            HANDLER.messages['error'], ['test']
        )

        mock_rollback.assert_called_with()


class TestDBSession(object):
    """Test class for ``database.DBSession``
    """
    def setUp(self):
        """Setup mock object
        """
        HANDLER.reset()

        self.mock_session = Mock()
        self.mock_maker = Mock()
        self.mock_session.commit.return_value = None
        self.mock_session.rollback.return_value = None
        self.mock_session.close.return_value = None
        self.mock_maker.return_value = self.mock_session

    def test_DBSession_normal(self):
        """Check if ``database.DBSession`` works
        """
        with DBSession(self.mock_maker) as session:
            tools.assert_equal(session, self.mock_session)
            self.mock_maker.assert_called_with()
        self.mock_session.commit.assert_called_with()
        self.mock_session.close.assert_called_with()
        tools.assert_equals(
            HANDLER.messages['debug'], ['Session exit in normal']
        )

    def test_DBSession_exception_raised(self):
        """Check if ``database.DBSession`` works when exception raised
        """
        def _nested_func():
            with DBSession(self.mock_maker):
                raise Exception('test')
        tools.assert_raises(Exception, _nested_func)
        self.mock_session.rollback.assert_called_with()
        self.mock_session.close.assert_called_with()

        tools.assert_equals(
            HANDLER.messages['error'], ['Session exit with exception!', 'test']
        )
