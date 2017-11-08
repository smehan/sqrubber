# Copyright (C) 2001-2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# 
#
#  -*- coding: utf-8 -*-

# standard libs
import os

# 3rd party libs
import pytest

# application libs
import sqrubber as sq
import collisions as coll

#################
# Define fixtures
#################


@pytest.fixture()
def sqrub_min_sql():
    sqrub = sq.Sqrubber(min_sql_input())
    return sqrub


@pytest.fixture()
def sqrub_not_sql_input():
    sqrub = sq.Sqrubber(not_sql_input())
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
    path = os.path.join('tests', 'lorem.txt')
    return path


@pytest.fixture()
def sql_file_input():
    path = os.path.join('tests', 'example.sql')
    return path

###############
# Collisions
###############


@pytest.fixture()
def cs_sql():
    cs = coll.Collisions(infile='tests/multiple-example.sql')
    if cs.infile:
        cs.doc = cs.read_dump(cs.infile)
    return cs


@pytest.fixture()
def coll_sql_dump_name():
    cs = coll.Collisions(infile='multiple-example.sql')
    return cs


@pytest.fixture()
def min_sql_comment_with_meta():
    data = '''-- SQL Dump of DB_2.mdb
-- generated by MDB Viewer 2.2.7
-- optimized for PostgreSQL'''


@pytest.fixture()
def sqrub_not_sql_input():
    sqrub = sq.Sqrubber(not_sql_input())
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
    path = os.path.join('tests', 'lorem.txt')
    return path


@pytest.fixture()
def sql_file_input():
    path = os.path.join('tests', 'example.sql')
    return path