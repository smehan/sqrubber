###########################################################
# Copyright (C) 2015-2016 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Functional test suite
###########################################################
#
#  -*- coding: utf-8 -*-

# standard libs

# 3rd party libs
import pytest

# application libs
import sqrubber as sq


#################
# Define functional tests
#################

# create a sqrubber to deal with our input file
def test_sq_up(sqrub):
    assert sqrub

# it reports if the input is not an SQL file and exits...
def test_not_sql_input(sqrub_not_sql_input):
    assert sqrub_not_sql_input.validate() is False

# it reports if we have a prefix defined for table names

# it tells us how many names fail to comply to the naming standard

# it fixes those bad names

# it returns the new SQL dump file ready for use
