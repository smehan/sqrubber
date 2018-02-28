###########################################################
# Copyright (C) 2015-2018 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
# Collisions finds duplicate table names in a SQL dump file
# and makes them unique from metadata found in the sqrubber metadata comments.
###########################################################
#
#  -*- coding: utf-8 -*-

# Standard libs
import os
import sys
import getopt
import datetime
import pathlib
from collections import Counter

# 3rd party libs

# application libs


# These keywords are verbs and direct objects in initial DDL/DML statements.
DDL_KEYWORDS = ['create table', 'drop table']
MAX_LENGTH = 63

VERSION = '0.5.0'


def make_suffix(dump_name: str)-> str:
    """ Makes a suffix which is a contraction of extracted sql dump name.
        Is acronym of first letters in words plus _DATE """
    suffix = ''
    for p in dump_name.split('_'):
        p = p.strip('_')
        if len(p) == 0:
            continue
        if p[0].isalpha():
            suffix += p[0]
        elif p[0].isdigit():
            suffix += '_'
            suffix += p
    return suffix


def insert_suffix(old_string, suffix, table_type='drop'):
    """Inserts a suffix at appropriate position in a specific DDL statement"""
    if table_type == 'drop':
        pos = -1
    elif table_type == 'create':
        pos = -2
    elif table_type == 'insert':
        pos = old_string.index(' (')
    return old_string[:pos] + '_' + suffix + old_string[pos:]


def is_processable(line: str):
    """Tests whether the line has processable DDL"""
    if 'drop table' in line.lower() or 'create table' in line.lower():
        return True
    return False


def find_dupes(line: str, body):
    """Find and collect all the duplicate tablenames in the document"""
    for word in DDL_KEYWORDS:
        if word in line.lower():
            body.names.update([line.lower()])


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
        self.print_only = None
        self.outfile = None
        self.version = VERSION
        self.names = Counter()
        self.suffixes = {}

    def __repr__(self):
        """ REPR for Collisions"""
        return f'< Collisions ver {self.version} >'

    @staticmethod
    def destroy():
        """Destructor for Collisions"""
        print("Collisions is finished....")

    def validate(self):
        """
        Validates that the input contains a SQL DDL statement.
        Only meant as a high-level sanity check before serious parsing begins.
        :return: True if any valid DDL is found, False otherwise.
        """
        if not self.doc:
            return False
        for line in self.doc:
            if not self._token_in_line(line):
                return True
        return False

    def get_sql_dump_name(self, idx: int):
        """ Extracts sql dump file name from sqrubber generated comment block which is the
        dump file name for the current SQL line"""
        SQL_DUMP_LINE = '-- SQL Dump of '.lower()
        while SQL_DUMP_LINE not in self.doc[idx].lower():
            idx -= 1
        try:
            return self.doc[idx].lower().rsplit(' ', 1)[1].split('.')[0].lower()
        except IndexError:
            return None

    def make_sql_dump_suffixes(self):
        """Pass through SQL file and create unique suffixes for all SQL
        dump names encountered in file. Store for subsequent use in writing
        appropriate suffix to updated SQL lines."""
        for name in self.get_all_sql_dump_names():
            if name not in self.suffixes.keys():
                span = 1
                while make_suffix_2(name, span) in self.suffixes.values():
                    span += 1
                self.suffixes[name] = make_suffix_2(name, span)
                print(make_suffix_2(name, span))
                print(self.suffixes)

    def get_all_sql_dump_names(self):
        """Find and report all sql dump file names from sqrubber generated comment blocks"""
        SQL_DUMP_LINE = '-- SQL Dump of '.lower()
        out = []
        for line in self.doc:
            if SQL_DUMP_LINE in line.lower():
                out.append(line.rsplit(' ', 1)[1].split('.')[0].lower())
        return out

    def process_drop_table(self, suffix: str, idx: int):
        self.doc[idx] = insert_suffix(self.doc[idx], suffix, 'drop')

    def process_create_table(self, suffix: str, idx: int, recurse=False):
        if not recurse:
            self.doc[idx] = insert_suffix(self.doc[idx], suffix, 'create')
        while 'insert into' not in self.doc[idx].lower() and idx < len(self.doc) - 1:
            idx += 1
            if is_processable(self.doc[idx]):
                return
        # guard against end of doc overrun
        if idx == len(self.doc) - 1:
            return
        self.doc[idx] = insert_suffix(self.doc[idx], suffix, 'insert')
        # recurse for multiple inserts
        self.process_create_table(suffix, idx + 1, recurse=True)
        return self.doc[idx]

    def process_table_name(self, line: str, idx: int):
        """Splits the processing into two branches based on drop or create table in DDL line"""
        if not is_processable(line):
            return
        # table_suffix = make_suffix(get_sql_dump_name(self.doc, idx))
        table_suffix = self.suffixes[self.get_sql_dump_name(idx)]
        if 'drop table' in line:
            self.process_drop_table(table_suffix, idx)
        elif 'create table' in line:
            self.process_create_table(table_suffix, idx)
        new_table_name = self.make_table_name(idx, table_suffix)

    def make_table_name(self, idx: int, suffix: str):
        # "drop table if exists ingest.db033_grocery_convenience_data_entry_chicago_data_entry_spring_2016;"
        # 'drop table if exists' = 21
        line = self.doc[idx].lower()
        if 'drop table if exists ' in line:
            start = 21
            end = line.index(';')
        # create table ingest.db033_sub_category_sort (
        elif 'create table ' in line:
            start = 13
            end = line.index(' (')
        # INSERT INTO ingest.db008_all_data_2015_may (market,  category, item, price, register_ring___beverages, qc_notes)
        elif 'insert into ' in line:
            start = 12
            end = line.index(' (')
        # fn is the full identifier, including schema components
        fn = line[start:end]
        # tn is the table name with no schema
        tn = fn.split('.')[1]
        if len(tn) > MAX_LENGTH:
            print(f'Length: {len(tn)} - {tn}')
        return fn

    def process_dupes(self, line: str, idx: int):
        """Given a list of duplicate table names, make them unique.
        These lines are contextualized by DDL keyword, e.g., DROP tablename is
        different to CREATE tablename and so the test of > 1 is measuring by context.
        :param line: the current line of the doc being processed
        :param body: the collisions object formed from the file being processed
        :param idx: the index of the line"""
        if self.names[line.lower()] > 1:
            self.process_table_name(line.lower(), idx)
        return

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
        Takes the content of Collisions object and writes it to a file
        :return:
        """
        #self.print_only = True
        if self.print_only:
            # FIXME this should probably turn into a cmd line flag and even break out from a conf file....
            print(f"-- Collisions version {self.version}\n")
            print("-- Collisions output generated on " + str(datetime.datetime.now()) + 3 * "\n")
            for line in self.doc:
                print(line)
            return
        path = self.outfile
        with open(path, 'w') as f:
            f.write(f"-- Collisions version {self.version}\n")
            f.write("-- Collisions output generated on " + str(datetime.datetime.now()) + 3 * "\n")
            for line in self.doc:
                f.write(f"{line}\n")


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
    print_only = False
    outfile = None
    try:
        options, remainder = getopt.gnu_getopt(argv, 'hpi:', ['print', 'infile=', 'overwrite'])
    except getopt.GetoptError:
        print(f"Error. Proper usage is {usage()}")
        sys.exit(2)
    if len(options) == 0:
        print(f"Error. Proper usage is {usage()}")
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
        collisions.outfile = collisions.infile + '.cleaned'
    else:
        collisions.outfile = outfile
    collisions.print_only = print_only
    if collisions.infile:
        collisions.doc = collisions.read_dump(collisions.infile)
    # Check if there is any valid DDL in the document
    if not collisions.validate():
        print("Input has no valid DDL, please check input....")
        exit()
    # Find all the sql dump names and print them out.
    collisions.make_sql_dump_suffixes()
    # First find the duplicates
    for line in collisions.doc:
        find_dupes(line, collisions)
    # Then process those found
    for idx, line in enumerate(collisions.doc):
        collisions.process_dupes(line, idx)
    collisions.write_dump()
    collisions.destroy()


if __name__ == '__main__':
    main(sys.argv[1:])





