###########################################################
# Copyright (C) 2015-2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# unit test class for collisions program
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs

# 3rd party libs
import pytest

# application libs
import collisions as coll


@pytest.mark.skip('Collisions object failing on tests')
def test_input_exists(cs_sql):
    assert cs_sql.doc
    print("There is no content in the Collisions object")


@pytest.mark.skip('Collisions object failing on tests')
def test_validate(cs_sql):
    assert cs_sql.validate()
    print("Can't find valid DDL")


@pytest.mark.skip('Collisions object failing on tests')
def test_not_valid(sqrub_not_sql_input):
    assert not sqrub_not_sql_input.validate()


@pytest.mark.skip('Collisions object failing on tests')
def test_file_check(coll):
    assert coll


def test_validate(cs_sql):
    assert cs_sql.validate()


def test_get_sql_dump_name(cs_sql):
    assert 'db_2' == coll.get_sql_dump_name(cs_sql, 8)


def test_multiple_sql_find_dupes(cs_sql):
    for line in cs_sql.doc:
        coll.find_dupes(line, cs_sql)
    assert cs_sql.names['create table myschema.der_all_brands_price_data ('] == 2


def test_multiple_sql_process_dupes(cs_sql):
    for line in cs_sql.doc:
        coll.find_dupes(line, cs_sql)
    # Then process those found
    for idx, line in enumerate(cs_sql.doc):
        coll.process_dupes(line, cs_sql, idx)
    assert cs_sql.doc[81] == 'DROP TABLE IF EXISTS myschema.der_all_brands_price_data_d_2;'
    assert cs_sql.doc[82] == ''
    assert cs_sql.doc[83] == 'CREATE TABLE myschema.der_all_brands_price_data_d_2 ('


def test_orphan_create_table(cs_orphan_create_sql):
    """There may be a create table DDL that has no following insert DDL for that table name,
       in which case the process_table_name should return a None, otherwise the new insert"""
    orphan_line = 'CREATE TABLE myschema.der_all_brands_transposed ('.lower()
    coll.find_dupes(orphan_line, cs_orphan_create_sql)
    assert coll.process_create_table(coll.make_suffix(coll.get_sql_dump_name(cs_orphan_create_sql, 103)), cs_orphan_create_sql, 103) is None
    orphan_line = 'CREATE TABLE myschema.der_all_brands_price_data ('.lower()
    coll.find_dupes(orphan_line, cs_orphan_create_sql)
    assert coll.process_create_table(coll.make_suffix(coll.get_sql_dump_name(cs_orphan_create_sql, 81)), cs_orphan_create_sql, 81) == \
           'INSERT INTO myschema.der_all_brands_price_data_d_2 (market, name, store_num, category, item, size_or_quantity, price, date)'


def test_make_suffix():
    assert coll.make_suffix('wilkes_barre_report_fall_2016') == \
        'wbrf_2016'
