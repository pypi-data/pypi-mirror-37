#!/usr/bin/env python
#  -*- coding: utf-8 -*-
# File: test_influxdb_connection.py
# Author: MS Cai <i@unoiou.com>
# ---
# Last Modified: Monday, 22nd October 2018 4:05:04 pm
# Modified By: MS Cai <i@unoiou.com>
# ---
# Copyright 2018 All rights reserved, Chance Focus Co.,ltd.
from influxdb import InfluxDBClient
from nose.tools import assert_equals, assert_not_in

from orm.connections import InfluxdbBase, InfluxdbConnection
from orm.session import DBSessionMaker


@InfluxdbBase.declared_attr
class TestMeasurement(InfluxdbBase):
    pass


class TestInfluxdbConnectionNormal(object):
    """Test class for `InfluxdbConnection`
    """

    def setUp(self):
        InfluxdbConnection.values = {
            'host': 'influxdb', 'database': 'test', 'port': 8086
        }
        self.fake_obj = {
            'measurement': 'test_measurement',
            "tags": {
                "hos233t": "server01",
                "region": "us-west"
            },
            "time": "2009-11-10T23:00:00Z",
            "fields": {
                "Float_value": 0.64,
                "Int_value": 3,
                "String_value": "Text",
                "Bool_value": True
            }
        }
        self.expect_obj = {
            u'String_value': u'Text', u'region': u'us-west',
            u'time': u'2009-11-10T23:00:00Z', u'Bool_value': True,
            u'Float_value': 0.64, u'Int_value': 3, u'hos233t': u'server01'
        }
        self.client = InfluxDBClient(**InfluxdbConnection.values)
        self.query_str = 'select * from test_measurement'

        InfluxdbConnection.connect()
        InfluxdbConnection.create_all()

    def tearDown(self):
        InfluxdbConnection.drop_all()
        InfluxdbConnection.close()

    @InfluxdbConnection.with_session()
    def test_add(self, session):
        """Check if `InfluxdbBase.add` works.
        """
        TestMeasurement.add(self.fake_obj, session)
        result = list(self.client.query(self.query_str).get_points())

        assert_equals(len(result), 1)
        assert_equals(result[0], self.expect_obj)

    @InfluxdbConnection.with_session()
    def test_batch_add(self, session):
        """Check if `InfluxdbBase.batch_add` works.
        """
        # Here write 2 duplicate points, just 1 point inserted actually.
        TestMeasurement.batch_add([self.fake_obj, self.fake_obj], session)
        result = list(self.client.query(self.query_str).get_points())

        # 1 point inserted in fact.
        assert_equals(len(result), 1)
        assert_equals(result, [self.expect_obj])

    @InfluxdbConnection.with_session()
    def test_delete_all(self, session):
        """Check if `InfluxdbBase.delete_all` works.
        """
        self.client.write_points([self.fake_obj])
        assert_equals(
            len(list(self.client.query(self.query_str).get_points())),
            1
        )

        TestMeasurement.delete_all(session)
        assert_not_in(u'test_measurement', [
            measurement[u'name']
            for measurement in self.client.get_list_measurements()
        ])

    @InfluxdbConnection.with_session()
    def test_query(self, session):
        """Check if `InfluxdbBase.query` works.
        """
        assert_equals(
            len(list(self.client.query(self.query_str).get_points())),
            0
        )

        self.client.write_points([self.fake_obj])

        assert_equals(TestMeasurement.query(session), [self.expect_obj])

    def test_functional(self):
        """Check if `InfluxdbConnection.with_session` works in functional tests.
        """
        fake_config = {
            'host': 'influxdb', 'database': 'test', 'port': 8086,
            'backend': 'influxdb'
        }
        DBSessionMaker.connect(**fake_config)

        DBSessionMaker.create_all()

        @DBSessionMaker.with_session()
        def fake_insert_data_func(session):
            TestMeasurement.add(self.fake_obj, session)

        # Initialize database with 1 point
        fake_insert_data_func()

        DBSessionMaker.close()

        # Main function
        def fake_main_func():
            DBSessionMaker.connect(**fake_config)

            @DBSessionMaker.with_session()
            def run(session):
                # insert duplicate data, actually not inserted
                TestMeasurement.add(self.fake_obj, session)

            run()

            DBSessionMaker.close()

        fake_main_func()

        # Functional tests
        class TestFunctional(object):
            @staticmethod
            def fake_test_main():
                DBSessionMaker.connect(**fake_config)

                result = list(self.client.query(self.query_str).get_points())
                assert_equals(len(result), 1)
                assert_equals(result[0], self.expect_obj)

                DBSessionMaker.drop_all()
                DBSessionMaker.close()

        # Run test function
        TestFunctional().fake_test_main()
