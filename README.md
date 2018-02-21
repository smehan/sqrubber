# sqrubber
Collection of python utilities for verifying and altering SQL dump files, including adding prefixes to table namespaces, changing table and column namespaces.
Currently expects python 3 (tested in 3.6.2)

[![Build Status](https://travis-ci.org/smehan/sqrubber.svg?branch=master)](https://travis-ci.org/smehan/sqrubber)

### Usage

sqrubber -[hpio] [-h help] [-p print-output-only] [--prefix=<prefix>] [--schema=schema_name][-i/--infile=<inputfile>] [-o/--outfile=<outputfile>]

$ python -m sqrubber

* print-output-only will echo changes only to output, not modifying any actual files.
* prefix=*string* will append a string to each table name in the modified schema.
* schema=*schema_name* will append a schema name to each table in the input file.
* infile=*name* is the SQL file to be parsed and transformed.
* output=*name* is the path and name of the output file into which to save the transformed SQL.
* help outputs help information on usage.

