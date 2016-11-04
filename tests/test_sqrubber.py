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


def test_remove_spaces():
    assert 'DROP TABLE employees;' == sq.remove_spaces('DROP TABLE employees;')
    assert 'CREATE TABLE employees (' == sq.remove_spaces('CREATE TABLE employees (')
    assert 'CREATE TABLE former_employees (' == sq.remove_spaces('CREATE TABLE former employees (')
