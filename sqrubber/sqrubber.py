###########################################################
# Copyright (C) 2015-2016 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# sqrubber will perform various transformations and verifications on an SQL dump file
###########################################################
#
#  -*- coding: utf-8 -*-

# Standard libs

# 3rd party libs

# application libs


def doubleit(x):
    """

    :param x:
    :return:
    """
    return x * 2


class Sqrubber(object):
    """
    Sqrubber consumes an SQL dump and parses it, cleaning up and transforming the dump
    """

    def __init__(self, input=None):
        """Constructor for Sqrubber
        :param input: input file
        """
        if input:
            self.doc = input
            print("New Sqrubber created")
        else:
            print("Your Sqrubber has no input")


    def destroy(self):
        """Destructor for Sqrubber"""
        pass

    def read_dump(self, path):
        """
        Takes a path and reads in a dump file for processing
        :param path: the path to read from
        :return:
        """
        pass

    def write_dump(self):
        """
        Takes the content of sqrubber object and writes it to a file
        :param path: the path to write to
        :return:
        """

    def remove_spaces(self, line):
        """
        Removes spaces and replaces them with underscores in a string
        :param line: the string to work on
        :return: transformed string
        """
        pass

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


if __name__ == '__main__':
    print("Hello, World")
    sqrub = Sqrubber()

