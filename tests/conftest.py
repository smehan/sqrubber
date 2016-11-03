# Copyright (C) 2001-2016 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# 
#
#  -*- coding: utf-8 -*-

# standard libs

# 3rd party libs
import pytest

# application libs
import sqrubber as sq

#################
# Define fixtures
#################


@pytest.fixture()
def sqrub():
    sqrub = sq.Sqrubber(test_sql_input())
    return sqrub


@pytest.fixture()
def test_sql_input():
    data = ['Here is some data']
    return data