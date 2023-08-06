#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: tests/test_session.py
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 01.02.2018
import logging

from nose.tools import assert_equals, assert_raises

from orm.connections import SQLBase, SQLConnection
from orm.session import DBSessionMaker


logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
logging.getLogger('sqlalchemy.orm').setLevel(logging.DEBUG)


class Test(SQLBase):
    __tablename__ = 'test'


class TestSQLConnection(object):
    """Test class for SQLConnection
    """
    def test_rollback_in_exceptions(self):
        """Check if `session` rollback in exceptions
        """
        # Create integration class
        class TestTest(object):
            def setUp(self):
                # Create sql connection with arguments
                SQLConnection.values = {
                    'user': 'root', 'password': 'test', 'host': 'mysql',
                    'port': 3306, 'database': 'test',
                }

                # Build Connection
                SQLConnection.connect()

                # Create table by metadata
                SQLConnection.create_all()

            @SQLConnection.with_session()
            def test_add(self, session):
                # Add new element
                Test.add({}, session)

                raise Exception()

            def tearDown(self):
                SQLConnection.drop_all()

                # Close connection
                SQLConnection.close()

        TestTest().setUp()

        # Run test function
        assert_raises(Exception, TestTest().test_add)

        session = SQLConnection.Session()
        assert_equals(len(session.query(Test).all()), 0)

        TestTest().tearDown()

    def test_rollback_in_integration_tests(self):
        """Check if `session` works in integration tests
        """
        # Create integration class
        class TestTest(object):
            def setUp(self):
                # Create session maker with arguments
                SQLConnection.values = {
                    'user': 'root', 'password': 'test', 'host': 'mysql',
                    'port': 3306, 'database': 'test',
                }
                SQLConnection.connect()

                # Create table by metadata
                SQLConnection.create_all()

            @SQLConnection.with_session(rollback=True)
            def test_add(self, session):
                # Add new element
                Test.add({}, session)

                # Query then
                assert_equals(len(session.query(Test).all()), 1)

            def tearDown(self):
                SQLConnection.drop_all()

                # Close connection
                SQLConnection.close()

        TestTest().setUp()

        # Run test function
        TestTest().test_add()

        TestTest().tearDown()

    def test_in_functional_tests(self):
        """Check if `session` works in functional tests
        """
        # Create session maker with arguments
        DBSessionMaker.connect(
            user='root', password='test', host='mysql', port=3306,
            database='test',
        )

        # Create table by metadata
        DBSessionMaker.create_all()

        @DBSessionMaker.with_session()
        def create_fake_datum(session):
            # Create fake datum
            Test.batch_add([{}, {}], session)

        create_fake_datum()

        # Close
        DBSessionMaker.close()

        # Create fake main function
        def main():
            # Create session maker with arguments
            DBSessionMaker.connect(
                user='root', password='test', host='mysql', port=3306,
                database='test',
            )

            @DBSessionMaker.with_session()
            def run(session):
                Test.add({}, session)

            run()

            # Close connection
            DBSessionMaker.close()

        # Call main method
        main()

        # Create functional class
        class TestFunctional(object):
            def fake_test_main(self):
                DBSessionMaker.connect(
                    user='root', password='test', host='mysql', port=3306,
                    database='test',
                )

                session = DBSessionMaker.get_session()

                # Query then
                assert_equals(len(session.query(Test).all()), 3)

                DBSessionMaker.drop_all()

                DBSessionMaker.close()

        # Run test function
        TestFunctional().fake_test_main()
