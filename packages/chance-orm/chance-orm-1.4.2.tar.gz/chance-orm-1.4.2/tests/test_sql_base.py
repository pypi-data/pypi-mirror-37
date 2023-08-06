#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: tests/test_base.py
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 27.10.2017
import arrow
import logging

from collections import namedtuple
from decimal import Decimal
from nose import tools

from mock_logger import MockLoggingHandler
from orm.connections import SQLBase


HANDLER = MockLoggingHandler(level='DEBUG')


def setup_module():
    logger = logging.getLogger('orm.connections.sql_connection')
    logger.addHandler(HANDLER)


class TBase(SQLBase):
    test_decimal = Decimal(9.999)


class TestSQLBase(object):
    """Test class for ``SQLBase``
    """
    def setUp(self):
        HANDLER.reset()

        self.base = TBase

    def test_repr(self):
        """Check if ``SQLBase.__repr__`` works
        """
        base = self.base()
        base._sa_instance_state = namedtuple('temp', 'attrs')
        base._sa_instance_state.attrs = {'test_decimal': 'test'}
        assert "TBase: [('test_decimal'" in repr(base)
        assert ")]" in repr(base)

    def test_eq_with_non_dict(self):
        """Check if ``SQLBase.__eq__`` works with non-dict object
        """
        assert not self.base() == "test"
        tools.assert_equals(HANDLER.messages['info'], ['Value not dict'])

    def test_eq_key_not_in_object(self):
        """Check if ``SQLBase.__eq__`` works when key not in object
        """
        test_dict = {}
        test_dict["test"] = "test"
        assert not self.base() == test_dict
        tools.assert_equals(
            HANDLER.messages['info'], ['test not found in object']
        )

    def test_time(self):
        """Check if ``SQLBase._time`` works
        """
        expect_time = '00:04:55'
        tools.assert_equals(
            self.base()._time(arrow.get(expect_time, "HH:mm:ss").time()),
            expect_time
        )

    def test_date(self):
        """Check if ``SQLBase._date`` works
        """
        expect_date = '2017-08-09'
        tools.assert_equals(
            self.base()._date(arrow.get(expect_date, "YYYY-MM-DD").date()),
            expect_date
        )

    def test_datetime(self):
        """Check if ``SQLBase._datetime`` works
        """
        expect_date = '2017-08-09 04:09:34'
        tools.assert_equals(
            self.base()._datetime(
                arrow.get(expect_date).datetime
            ),
            expect_date
        )

    def test_decimal(self):
        """Check if ``SQLBase._decimal`` works
        """
        expect_data = '9.999'
        tools.assert_equals(
            self.base()._decimal(Decimal(expect_data)),
            expect_data
        )

    def test_eq_normal(self):
        """Check if ``SQLBase.__eq__`` works
        """
        test_dict = {}
        test_dict["test_decimal"] = '9.999'
        assert self.base() == test_dict

    def test_eq_not_equal(self):
        """Check if ``SQLBase.__eq__`` works when value not equal
        """
        test_dict = {}
        test_dict["test_decimal"] = '9.998'
        assert not self.base() == test_dict
        tools.assert_equals(
            HANDLER.messages['info'],
            ['Value not matched for test_decimal: 9.999 | 9.998']
        )
