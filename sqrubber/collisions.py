###########################################################
# Copyright (C) 2015-2017 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# sqrubber will perform various transformations and verifications on an SQL dump file
###########################################################
#
#  -*- coding: utf-8 -*-

# Standard libs
import os
import sys
import getopt
import re
import datetime
import pathlib
from collections import OrderedDict, Counter

# 3rd party libs

# application libs


# These keywords are verbs and direct objects in initial DDL/DML statements.
DDL_KEYWORDS = ['create table', 'drop table']
INDENT = ' '*4

VERSION = '0.3.0'


def get_sql_dump_name(body, idx: int):
    """ Extracts sql dump file name from sqrubber generated comment block"""
    SQL_DUMP_LINE = '-- SQL Dump of '.lower()
    while SQL_DUMP_LINE not in body.doc[idx].lower():
        idx -= 1
    try:
        return body.doc[idx].lower().rsplit(' ', 1)[1].split('.')[0].lower()
    except IndexError:
        return None


def insert_suffix(old_string, suffix, table_type='drop'):
    if table_type == 'drop':
        pos = -1
    elif table_type == 'create':
        pos = -2
    elif table_type == 'insert':
        pos = old_string.index(' (')
    return old_string[:pos] + '_' + suffix + old_string[pos:]


def process_drop_table(suffix: str, body, idx: int):
    body.doc[idx] = insert_suffix(body.doc[idx], suffix, 'drop')
    return body.doc[idx]


def process_create_table(suffix: str, body, idx: int):
    body.doc[idx] = insert_suffix(body.doc[idx], suffix, 'create')
    while 'insert into' not in body.doc[idx].lower():
        idx += 1
    body.doc[idx] = insert_suffix(body.doc[idx], suffix, 'insert')


def process_table_name(line: str, body, idx: int):
    table_suffix = get_sql_dump_name(body, idx)
    if 'drop table' in line:
        process_drop_table(table_suffix, body, idx)
    elif 'create table' in line:
        process_create_table(table_suffix, body, idx)


def process_dupes(line: str, body, idx: int):
    if body.names[line.lower()] > 1:
        process_table_name(line.lower(), body, idx)
    return


def find_dupes(line: str, body, idx: int):
    for word in DDL_KEYWORDS:
        if word in line.lower():
            body.names.update([line.lower()])
    process_dupes(line, body, idx)
    return


class Collisions(object):
    """
    Collisions consumes a sqrubbed SQL dump and parses it,
    checking for table name collisions from combined schema.
    """

    def __init__(self, infile=None, prefix=None, schema=None):
        """Constructor for Collisions
        :param infile: input file containing a sqrubbed SQL dump to be processed.
        """
        if not infile:
            print("Warning! Collisions check needs an input file.")
            try:
                sys.stdin.close()
            except SystemError as e:
                print(e)
            raise SystemExit()
        elif isinstance(infile, list):
            self.infile = None
            self.doc = infile
        # FIXME need to be able to test whether type is correct for this.
        elif os.path.isfile(infile):
            self.infile = infile
            self.doc = None
        else:
            print("General error ...")
            try:
                sys.stdin.close()
            except ValueError as e:
                print(e)
            raise SystemExit()
        self.version = VERSION
        self.names = Counter()

    def __repr__(self):
        """

        :return:
        """
        return '< Collisions ver {version}:'\
                .format(version=self.version)

    @staticmethod
    def destroy():
        """Destructor for Collisions"""
        print("Collisions is finished....")

    def set_schema(self):
        """
        Writes out a comment in output SQL to remind user of schema assumptions in dump.
        :return:
        """
        return '\n\n--\n-- Sqrubber is assuming the existence of schema {}\n--\n\n'.format(self.schema)

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

    def write_dump(self, path):
        """
        Takes the content of Collisions object and writes it to a file
        :param path: the path to write to
        :return:
        """
        self.print_only = True
        if self.print_only:
            # FIXME this should probably turn into a cmd line flag and even break out from a conf file....
            print("-- Collsions version {version}\n".format(version=self.version))
            print("-- Collisions output generated on " + str(datetime.datetime.now()) + 3 * "\n")
            for line in self.doc:
                print(line)
            return
        # with open(path, 'w') as f:
        #     f.write("-- Sqrubber version {version}\n".format(version=self.version))
        #     f.write("-- Sqrubber output generated on " + str(datetime.datetime.now()) + 3*"\n")
        #     for line in output:
        #         f.write(line + '\n')
        #     f.write("\n\n-- Sqrubber job finished")


def usage():
    """
    returns usage string
    """
    output = 'usage: collsions -[hpi] [-h help] [-p print-output-only] ' \
             '[--overwrite]' \
             '[-i/--infile=<inputfile>]'
    return output


def main(argv):
    """
    drives a command line invocation of collision check
    :param argv:
    :return:
    """
    print_only = None
    outfile = None
    try:
        options, remainder = getopt.gnu_getopt(argv, 'hpi:', ['print', 'infile=', 'overwrite'])
    except getopt.GetoptError:
        print("Error. Proper usage is " + usage())
        sys.exit(2)
    if len(options) == 0:
        print("Error. Proper usage is " + usage())
        sys.exit(2)
    for opt, arg in options:
        if opt == '-h':
            print(f"Proper usage is {usage()}")
            sys.exit()
        elif opt in ['-i', '--infile']:
            collisions = Collisions(arg)
        elif opt in ['--overwrite']:
            outfile = collisions.infile
        elif opt in ['-p', '--print']:
            print_only = True
        elif opt in ['--prefix']:
            prefix = arg
        elif opt in ['--schema']:
            schema = arg
    if outfile is None:
        outfile = collisions.infile + '.cleaned'
    collisions.outfile = outfile
    collisions.print_only = print_only
    if collisions.infile:
        collisions.doc = collisions.read_dump(collisions.infile)
    if not collisions.validate():
        print("Input is not DDL, please check input....")
        exit()
    output = []
    # if schema:
    #     sqrub.schema = schema
    #     output.append(sqrub.set_schema())
    # if prefix:
    #     sqrub.prefix = prefix
    for idx, line in enumerate(collisions.doc):
        # if idx == 0:
        #     sqrub.indent = False
        find_dupes(line, collisions, idx)
        # output.append(process_line(line, sqrub, sqrub.prefix, sqrub.schema))
    collisions.write_dump(None)
    collisions.destroy()


if __name__ == '__main__':
    main(sys.argv[1:])





