###########################################################
# Copyright (C) 2015-2018 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
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

# 3rd party libs

# application libs

# These keywords are verbs and direct objects in initial DDL/DML statements.
DDL_KEYWORDS = ['create table', 'create column', 'drop column', 'drop table', 'alter table']
DDL_OTHER_KEYWORDS = ['set names']
DDL_TYPES = ['integer', 'text', 'double precision']
SPECIAL_CASES = {'#': 'num', '/': '-'}


def standardize_name(name):
    """
    replace spaces with underscores. remove special characters.
    :param name: the one or more column or table names to be processed, as a string
    :return: a new string with replaced chars
    """
    for k in SPECIAL_CASES:
        if k in name:
            name = name.replace(k, SPECIAL_CASES[k])
    name = name.replace(' ', '_')
    return name.lower()


def split_line_with_token(line, tok):
    """
    tokenize the line into components for later use.
    :param line: incoming line with DDL/DML token in line
    :return: three strings: DDL/DML token, name, remainder of line
    """
    pattern = re.compile(r''.join(('^\s?', tok, '\s+([A-Za-z0-9 _#/\'\"]+)(.*)')))
    match = re.search(pattern, line.lower())
    name = match.group(1).strip()
    remain = match.group(2)
    return name, remain


def split_line_with_column_name(line):
    """
    tokenize the into components for later use.
    :param line: incoming string with no DDL/DML token at beginning but
    rather a column declaration, e.g. "COLUMN NAME" TEXT,
    :return: two strings: name, remainder of line
    """
    pattern = re.compile(r'\s?[\'\"]?([A-Za-z0-9 _#/]+)[\'\"]?(.*,?)')
    match = re.search(pattern, line.lower())
    name = match.group(1).strip()
    remain = match.group(2)
    return name, remain


def split_insert_line(line):
    """
    tokenize an INSERT INTO line into components and standardize all table and column names in the line.
    :param line: incoming string with INSERT INTO at beginning
    :return: fully standardized line
    """
    new_columns = []
    table_name, columns = line.split('(')
    table_name = standardize_name(table_name.split('INTO ')[1])
    columns = columns.replace(')', '')
    for index, col in enumerate(columns.split(',')):
        new_columns.append(standardize_name(col))
    return ''.join(('INSERT INTO', ' ', table_name)) + \
           ' (' + \
           ', '.join((new_columns)) + \
           ')'


def process_line(line):
    """
    Processes a line of DDL/DML with potential column and table names.
    Removes spaces and replaces them with underscores in a string.
    Lower cases all elements of names.
    Upper cases all elements of DDL.
    Checks special case of [if exists] in DDL verbs.
    Assumes that DDL is present in the line. Use _token_in_line to check.
    :param line: the string to work on
    :return: transformed string
    """
    # remove noise lines from parse
    if re.search(r'^--', line) or line == '' or line == ');':
        return line
    # INSERT INTO CASE
    if re.search(r'^INSERT INTO', line.upper()):
        return split_insert_line(line)
    # VALUES or sub-line CASE
    if re.search(r'VALUES\s?\(E?\'', line.upper()) or re.search(r'\s?\(E?\'', line.upper()):
        return line
    # special DDL line with no name
    for tok in DDL_OTHER_KEYWORDS:
        if re.search(r''.join(tok), line.lower()):
            return line
    for tok in DDL_KEYWORDS:
        if tok in line.lower():
            if ' '.join((tok, 'if exists')) in line.lower():
                tok = ' '.join((tok, 'if exists'))
            name, remain = split_line_with_token(line, tok)
            name = standardize_name(name)
            return ''.join((tok.upper(), ' ', name, ' ', remain)).replace(' ;', ';')
    # no token at start of line - column declaration
    for tok in DDL_TYPES:
        if tok in line.lower():
            name, remain = split_line_with_column_name(line)
            name = standardize_name(name)
    return ' '.join((name, remain.upper()))


def add_prefix(line, prefix):
    """
    Adds a prefix to a column or table name
    :param name: the name to transform
    :param prefix: the prefix to prepend
    :return: the combined prefix_name
    """
    for tok in DDL_KEYWORDS:
        if tok in line.lower():
            name, remain = split_line_with_token(line, tok)
            name = '_'.join((prefix, name))
            return ''.join((tok.upper(), ' ', name, ' ', remain)).replace(' ;', ';')


class Sqrubber(object):
    """
    Sqrubber consumes an SQL dump and parses it, cleaning up and transforming the dump
    """

    def __init__(self, input=None, prefix=None):
        """Constructor for Sqrubber
        :param input: input file
        """
        if not input:
            print("Your Sqrubber has no input")
            try:
                sys.stdin.close()
            except SystemError:
                pass
            raise SystemExit()
        elif isinstance(input, list):
            self.infile = None
            self.doc = input
        # FIXME need to be able to test whether type is correct for this.
        elif os.path.isfile(input):
            self.infile = input
            self.doc = None
        else:
            print("General error...")
            try:
                sys.stdin.close()
            except SystemError:
                pass
            raise SystemExit()
        self.prefix = prefix

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

    def write_dump(self, path, output):
        """
        Takes the content of sqrubber object and writes it to a file
        :param output: the output to write out
        :param path: the path to write to
        :return:
        """
        if self.print:
            for line in output:
                print(line)
            return
        with open(path, 'w') as f:
            f.write("-- Sqrubber output generated on " + str(datetime.datetime.now()) + 3*"\n")
            for line in output:
                f.write(line + '\n')
            f.write("\n\n-- Sqrubber job finished")


def usage():
    """
    returns usage string
    :return:
    """
    output = ['usage: sqrubber -[hpio] [-h help] [-p print-output-only] ',
              '[-i/--infile=<inputfile>] [-o/--outfile=<outputfile>]']
    return ' '.join(output)


def main(argv):
    """
    drives a command line invocation of Sqrubber
    :param argv:
    :return:
    """
    print = None
    outfile = None
    try:
        options, remainder = getopt.gnu_getopt(argv, 'hpi:o:', ['print', 'infile=', 'outfile='])
    except getopt.GetoptError:
        print("Error", usage())
        sys.exit(2)
    for opt, arg in options:
        if opt == '-h':
            print("Proper usage is ", usage())
            sys.exit()
        elif opt in ['-i', '--infile']:
            sqrub = Sqrubber(arg)
        elif opt in ['-o', '--outfile']:
            outfile = arg
        elif opt in ['-p', '--print']:
            print = True
    sqrub.outfile = outfile
    sqrub.print = print
    if sqrub.infile:
        sqrub.doc = sqrub.read_dump(sqrub.infile)
    if not sqrub.validate():
        print("Input is not DDL, please check input....")
        exit()
    output = []
    for line in sqrub.doc:
        output.append(process_line(line))
    sqrub.write_dump(sqrub.outfile, output)
    sqrub.destroy()


if __name__ == '__main__':
    main(sys.argv[1:])





