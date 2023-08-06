#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: orm/connections/connection.py
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 19.10.2018
from abc import ABCMeta


class Connection(object):
    """Class for database connection
    """
    __metaclass__ = ABCMeta
    connected = False

    @classmethod
    def connect(cls):
        """Initialize connection with given arguments

        User, Password, Host, Port, Database is required, and KeyError raised
        if not in given arguments.
        """
        pass

    @classmethod
    def create_all(cls):
        """Create all tables in metadata
        """
        pass

    @classmethod
    def drop_all(cls):
        """Drop all tables in metadata
        """
        pass

    @classmethod
    def close(cls):
        """Close connection
        """
        pass

    @classmethod
    def with_session(cls):
        """Decorator for creating session context around function.
        """
        pass

    @classmethod
    def get_session(cls):
        """Get present session
        """
        pass
