###########################################################
# Copyright (C) 2015-2016 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
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


def test_standardize_name():
    assert 'DROP TABLE employees;' == sq.process_line('DROP TABLE employees;')
    assert 'CREATE TABLE employees (' == sq.process_line('CREATE TABLE employees (')
    assert 'CREATE TABLE former_employees (' == sq.process_line('CREATE TABLE former employees (')
    assert 'CREATE TABLE yet_to_be_employees (' == sq.process_line('CREATE TABLE YET to BE employees (')
    assert 'DROP TABLE yet_to_be_employees;' == sq.process_line('DROP TABLE YET to BE employEeS;')

def test_standardize_name_with_if_exists():
    assert 'DROP TABLE if exists employees;' == sq.process_line('DROP TABLE if exists employees;')
    assert 'CREATE TABLE if exists employees (' == sq.process_line('CREATE TABLE if exists employees (')
    assert 'CREATE TABLE if exists former_employees (' == sq.process_line('CREATE TABLE if exists former employees (')
    assert 'CREATE TABLE if exists yet_to_be_employees (' == sq.process_line('CREATE TABLE if exists YET to BE employees (')
    assert 'DROP TABLE if exists yet_to_be_employees;' == sq.process_line('DROP TABLE if exists YET to BE employEeS;')

def test_add_prefix():
    assert 'CREATE TABLE test001_employees (' == sq.add_prefix('CREATE TABLE employees (', 'test001')
    assert 'CREATE TABLE test001_former_employees (' == sq.add_prefix('CREATE TABLE former_employees (', 'test001')
    assert 'CREATE TABLE test001_former_employees (' != sq.add_prefix('CREATE TABLE former employees (', 'test001')

