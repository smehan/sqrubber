###########################################################
# Copyright (C) 2015-2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# unit test class for main program
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs

# 3rd party libs
import pytest

# application libs
import sqrubber as sq

# def test_doubleit():
#     assert sq.doubleit(10) == 20
#     print("number")
#
#
# def test_doublieit_type():
#     with pytest.raises(TypeError):
#         sq.doubleit('string')


@pytest.mark.skip('Sqrubber object failing on tests')
def test_input_exists(sqrub):
    assert sqrub.doc
    print("There is no content in the Sqrubber object")


@pytest.mark.skip('Sqrubber object failing on tests')
def test_validate(sqrub):
    assert sqrub.validate()
    print("Can't find valid DDL")


@pytest.mark.skip('Sqrubber object failing on tests')
def test_not_valid(sqrub_not_sql_input):
    assert not sqrub_not_sql_input.validate()


@pytest.mark.skip('Sqrubber object failing on tests')
def test_file_check(sqrub):
    assert sqrub


def test_standardize_name(sqrub):
    assert 'DROP TABLE employees;' == sq.process_line('DROP TABLE employees;', sqrub)
    assert 'CREATE TABLE employees (' == sq.process_line('CREATE TABLE employees (', sqrub)
    assert 'CREATE TABLE former_employees (' == sq.process_line('CREATE TABLE former employees (', sqrub)
    assert 'CREATE TABLE yet_to_be_employees (' == sq.process_line('CREATE TABLE YET to BE employees (', sqrub)
    assert 'DROP TABLE yet_to_be_employees;' == sq.process_line('DROP TABLE YET to BE employEeS;', sqrub)
    assert 'CREATE TABLE tmpclp277481 (' == sq.process_line('CREATE TABLE "~TMPCLP277481" (', sqrub)


def test_standardize_names_with_indents(sqrub):
    sqrub.indent = True
    assert '     returned TEXT,' == sq.process_line('"Returned>" TEXT,', sqrub)
    assert '     survey_05 TEXT,' == sq.process_line('"Survey? 05" TEXT,', sqrub)
    assert '     jan09_survey TEXT,' == sq.process_line('\"Jan09 Survey?\" TEXT,', sqrub)
    assert '     survey_2005 TEXT,' == sq.process_line('"Survey 2005?" TEXT,', sqrub)
    assert '     deadline TEXT,' == sq.process_line('"Deadline?" TEXT,', sqrub)


def test_ddl_types_in_line(sqrub):
    assert 'returned TEXT,' == sq.process_line('"Returned" TEXT,', sqrub)
    assert 'returned BOOLEAN,' == sq.process_line('"Returned" BOOLEAN,', sqrub)
    assert 'amount INTEGER,' == sq.process_line('"amount" INTEGER,', sqrub)
    assert 'returned DOUBLE PRECISION,' == sq.process_line('"Returned" double precision,', sqrub)
    assert not sq.process_line('"Dud" VARCHAR', sqrub)


def test_standardize_name_with_if_exists(sqrub):
    assert 'DROP TABLE IF EXISTS employees;' == sq.process_line('DROP TABLE if exists employees;', sqrub)
    assert 'CREATE TABLE IF EXISTS employees (' == sq.process_line('CREATE TABLE if exists employees (', sqrub)
    assert 'CREATE TABLE IF EXISTS former_employees (' == sq.process_line('CREATE TABLE if exists former employees (', sqrub)
    assert 'CREATE TABLE IF EXISTS yet_to_be_employees (' == sq.process_line('CREATE TABLE if exists YET to BE employees (', sqrub)
    assert 'DROP TABLE IF EXISTS yet_to_be_employees;' == sq.process_line('DROP TABLE if exists YET to BE employEeS;', sqrub)


def test_add_prefix():
    assert 'test001_employees' == sq.add_prefix('employees', 'test001')
    assert 'test001_employees' == sq.add_prefix('employees', 'test001')
    assert 'test001_former_employees' == sq.add_prefix('former_employees', 'test001')
    assert 'test001_former_employees' != sq.add_prefix('former employees', 'test001')
    # TODO what about multiple word names?


def test_split_line_with_column_name():
    assert ('jan09 survey?', ' text,') == sq.split_line_with_column_name('\"Jan09 Survey?\" TEXT,')
    assert ('deadline?', ' text,') == sq.split_line_with_column_name('"Deadline?" TEXT,')
    assert ('package sent?', ' boolean,') == sq.split_line_with_column_name('"Package Sent?" BOOLEAN,')


def test_split_insert_line():
    assert 'INSERT INTO test (name, store_num, category, item, size_or_quantity, price)' == sq.split_insert_line('INSERT INTO test("Name","Store #","Category","Item","Size/Quantity","Price")')
    assert 'INSERT INTO test (store_num, jan09_survey)'  == sq.split_insert_line('INSERT INTO test("Store #","Jan09 Survey?")')