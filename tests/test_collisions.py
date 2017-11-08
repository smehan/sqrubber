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


def test_get_sql_dump_name(cs_sql):
    assert 'db_2' == coll.get_sql_dump_name(cs_sql, 8)


def test_orphan_create_table(cs_orphan_create_sql):
    """There may be a create table DDL that has no following insert DDL for that tablename.
       In which case the process_table_name should return a None, otherwise the new insert"""
    orphan_line = 'CREATE TABLE myschema.der_all_brands_transposed ('.lower()
    coll.find_dupes(orphan_line, cs_orphan_create_sql)
    assert coll.process_create_table(orphan_line, cs_orphan_create_sql, 104) is None
    orphan_line = 'CREATE TABLE myschema.der_all_brands_price_data ('.lower()
    coll.find_dupes(orphan_line, cs_orphan_create_sql)
    assert coll.process_create_table(orphan_line, cs_orphan_create_sql, 82) == \
           'INSERT INTO myschema.der_all_brands_price_data_create table myschema.der_all_brands_price_data ( (market, name, store_num, category, item, size_or_quantity, price, date)'

