#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: tests/test_rethinkdb_connection.py
# Author: Jimin Huang <huangjimin@whu.edu.cn> # Date: 22.10.2018
import rethinkdb as r

from nose.tools import assert_equals, assert_raises

from orm.connections import RethinkdbBase, RethinkdbConnection
from orm.session import DBSessionMaker


@RethinkdbBase.declared_attr
class Test(RethinkdbBase):
    pass


class TestRethinkdbConnection(object):
    """Test class for `orm.connections.RethinkdbConnection`
    """
    def test_raise_exceptions(self):
        """Check if `RethinkdbConnection.with_session` raise Exception
        """
        # Create integration class
        class TestTest(object):
            def setUp(self):
                # Create sql connection with arguments
                RethinkdbConnection.values = {
                    'host': 'rethinkdb', 'database': 'test',
                    'port': 28015,
                }

                # Build Connection
                RethinkdbConnection.connect()

                # Create table by metadata
                RethinkdbConnection.create_all()

            @RethinkdbConnection.with_session()
            def test_add(self, session):
                # Add new element
                Test.add({}, session)

                raise Exception()

            def tearDown(self):
                RethinkdbConnection.drop_all()

                # Close connection
                RethinkdbConnection.close()

        TestTest().setUp()

        # Run test function
        assert_raises(Exception, TestTest().test_add)

        session = RethinkdbConnection.session
        assert_equals(len(list(r.table('test').run(session))), 1)

        TestTest().tearDown()

    def test_normal(self):
        """Check if `RethinkdbConnection.with_session` works
        """
        # Create integration class
        class TestTest(object):
            def setUp(self):
                # Create sql connection with arguments
                RethinkdbConnection.values = {
                    'host': 'rethinkdb', 'database': 'test',
                    'port': 28015,
                }

                # Build Connection
                RethinkdbConnection.connect()

                # Create table by metadata
                RethinkdbConnection.create_all()

            @RethinkdbConnection.with_session()
            def test_add(self, session):
                # Add new element
                Test.add({'test': 'test'}, session)
                assert_equals(
                    len(list(r.table('test').run(session))), 1
                )

            @RethinkdbConnection.with_session()
            def test_batch_add(self, session):
                # Add new element
                Test.batch_add([{}, {}], session)
                assert_equals(
                    len(list(r.table('test').run(session))), 2
                )

            @RethinkdbConnection.with_session()
            def test_delete_all(self, session):
                # Add new element
                r.table('test').insert({}).run(session)
                assert_equals(
                    len(list(r.table('test').run(session))), 1
                )
                Test.delete_all(session)
                assert_equals(
                    len(list(r.table('test').run(session))), 0
                )

            @RethinkdbConnection.with_session()
            def test_query(self, session):
                assert_equals(Test.query(session), [])

                r.table('test').insert({}).run(session)
                result = Test.query(session)
                assert_equals(result, [{'id': result[0]['id']}])

            def tearDown(self):
                RethinkdbConnection.drop_all()

                # Close connection
                RethinkdbConnection.close()

        # Test add
        TestTest().setUp()
        TestTest().test_add()
        TestTest().tearDown()

        # Test batch add
        TestTest().setUp()
        TestTest().test_batch_add()
        TestTest().tearDown()

        # Test delete
        TestTest().setUp()
        TestTest().test_delete_all()
        TestTest().tearDown()

        # Test query
        TestTest().setUp()
        TestTest().test_query()
        TestTest().tearDown()

    def test_in_functional_tests(self):
        """Check if `RethinkdbConneciton.with_session` works in functional tests
        """
        # Create session maker with arguments
        DBSessionMaker.connect(
            host='rethinkdb', port=28015, database='test',
            backend='rethinkdb'
        )

        # Create table by metadata
        DBSessionMaker.create_all('rethinkdb')

        @DBSessionMaker.with_session(backend='rethinkdb')
        def create_fake_datum(session):
            # Create fake datum
            Test.batch_add([{}, {}], session)

        create_fake_datum()

        # Close
        DBSessionMaker.close('rethinkdb')

        # Create fake main function
        def main():
            # Create session maker with arguments
            DBSessionMaker.connect(
                host='rethinkdb', port=28015, database='test',
                backend='rethinkdb'
            )

            @DBSessionMaker.with_session(backend='rethinkdb')
            def run(session):
                Test.add({}, session)

            run()

            # Close connection
            DBSessionMaker.close('rethinkdb')

        # Call main method
        main()

        # Create functional class
        class TestFunctional(object):
            def fake_test_main(self):
                DBSessionMaker.connect(
                    host='rethinkdb', port=28015, database='test',
                    backend='rethinkdb'
                )

                session = DBSessionMaker.get_session('rethinkdb')

                # Query then
                assert_equals(
                    len(list(r.table('test').run(session))), 3
                )

                DBSessionMaker.drop_all('rethinkdb')

                DBSessionMaker.close('rethinkdb')

        # Run test function
        TestFunctional().fake_test_main()
