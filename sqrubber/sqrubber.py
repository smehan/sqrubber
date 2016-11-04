###########################################################
# Copyright (C) 2015-2016 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# sqrubber will perform various transformations and verifications on an SQL dump file
###########################################################
#
#  -*- coding: utf-8 -*-

# Standard libs
import os
import re

# 3rd party libs

# application libs


def doubleit(x):
    """

    :param x:
    :return:
    """
    return x * 2


DDL_KEYWORDS = ['create table', 'create column', 'drop column', 'drop table', 'alter table']


def split_line(line):
    """
    tokenize the line into components for later use.
    :param line:
    :return:
    """
    pass

def remove_spaces(line):
    """
    Removes spaces and replaces them with underscores in a string.
    Assumes that DDL is present in the line. Use _token_in_line to check.
    :param line: the string to work on
    :return: transformed string
    """
    for tok in DDL_KEYWORDS:
        if tok in line.lower():
            print("{} is in line: {}".format(tok, line))
            pattern = re.compile(''.join(('^', tok, '([A-Za-z0-9 ])(.*)')))
            name = re.search(pattern).group(2)


def remove_caps(self, line):
    """
    Transforms uppercase names to lowercase in a string
    :param line: the string to work on
    :return: transformed string
    """
    pass


def add_prefix(self, name, prefix):
    """
    Adds a prefix to a column or table name
    :param name: the name to transform
    :param prefix: the prefix to prepend
    :return: the combined prefix_name
    """
    pass


class Sqrubber(object):
    """
    Sqrubber consumes an SQL dump and parses it, cleaning up and transforming the dump
    """

    def __init__(self, input=None):
        """Constructor for Sqrubber
        :param input: input file
        """
        if not input:
            print("Your Sqrubber has no input")
            exit()
        elif isinstance(input, list):
            self.doc = input
        elif os.path.isfile(input):
            self.doc = "FILE"
        else:
            print("Error")
            exit()

    def destroy(self):
        """Destructor for Sqrubber"""
        pass

    def validate(self):
        """
        Validates that the input contains a SQL DDL statement.
        Only meant as a high-level check before serious parsing begins.
        :return: True if DDL is found, False otherwise.
        """
        if not self.doc:
            return False
        for line in self.doc:
            if self._token_in_line(line):
                return True
        return False

    @staticmethod
    def _token_in_line(line):
        """
        checks for DDL token in the line
        :param line: line to check
        :return: True if present, False otherwise
        """
        if any(token in line.lower() for token in DDL_KEYWORDS):
            return True
        return False

    @staticmethod
    def read_dump(path):
        """
        Takes a path and reads in a dump file for processing
        :param path: the path to read from
        :return: a list of lines in file
        """
        data = []
        with open(path, 'r') as f:
            for line in f:
                data.append(line.strip())
        return data

    def write_dump(self):
        """
        Takes the content of sqrubber object and writes it to a file
        :param path: the path to write to
        :return:
        """
        pass



if __name__ == '__main__':
    sqrub = Sqrubber(["Drop Table employees"])
    if not sqrub.validate():
        print("Input is not DDL, please check input....")
        exit()
    sqrub.doc = sqrub.read_dump('../tests/example.sql')
    sqrub.validate()
    for line in sqrub.doc:
        sqrub.remove_spaces(line)





