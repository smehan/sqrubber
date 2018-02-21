# Copyright (C) 2001-2018 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# 
#
#  -*- coding: utf-8 -*-

# standard libs
import os

# 3rd party libs
import pytest

# application libs
import sqrubber as sq

#################
# Define fixtures
#################


@pytest.fixture()
def sqrub_min_sql():
    sqrub = sq.Sqrubber(min_sql_input())
    return sqrub


@pytest.fixture()
def sqrub_not_sql_input():
    sqrub = sq.Sqrubber(not_sql_input)
    return sqrub


@pytest.fixture()
def sqrub():
    sqrub = sq.Sqrubber(sql_file_input())
    return sqrub


@pytest.fixture()
def min_sql_input():
    data = ['DROP TABLE employees']
    return data


@pytest.fixture()
def not_sql_input():
    with open('lorem.txt', 'r') as fh:
        data = fh.readlines()
    return data


@pytest.fixture()
def sql_file_input():
    path = os.path.dirname('example.sql')
    return path
