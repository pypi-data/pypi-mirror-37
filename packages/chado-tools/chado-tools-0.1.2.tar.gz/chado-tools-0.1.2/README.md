# chado-tools

Python3 command line script providing various tools for accessing CHADO databases

[![Build Status](https://travis-ci.org/sanger-pathogens/chado-tools.svg?branch=master)](https://travis-ci.org/sanger-pathogens/chado-tools)

## Prerequisites

* Python 3.6 or higher
* PostgreSQL 9.6 or higher

## Installation from source

Download the latest release from this github repository, or clone the repository to obtain the most recent updates.

Modify the file with [default connection settings](pychado/data/defaultDatabase.yml) such that it contains the settings for an existing PostgreSQL database server to which you can connect.

Then run the tests:

    python3 setup.py test

If the tests all pass, install:

    python3 setup.py install

## Alternative installations

You can install the program from the *Python Package Index (PyPI)* using the command

    pip install chado-tools
    
The program is also available as *Bioconda* package. Install it with the command

    conda install -c bioconda chado-tools

Now change the default connection parameters by running `chado init`. You can always reset them to the original state by running `chado reset`.

## Usage

The installation will put a single script called `chado` in your PATH.
The usage is:

    chado <command> [options]

* To list the available commands and brief descriptions, just run `chado -h` or `chado --help`.
* To display the version of the program, type `chado -v` or `chado --version`.
* Use `chado <command> -h` or `chado <command> --help` to get a detailed description and the usage of that command.

## Available commands

------------------------------------------------------------------------------------------------
| Command               | Description                                                          |
|-----------------------|----------------------------------------------------------------------|
| init                  | set the default connection parameters                                |
| reset                 | reset the default connection parameters to factory settings          |
| connect               | connect to a CHADO database for an interactive session               |
| query                 | query a CHADO database and export the result into a text file        |
| extract               | run a pre-compiled query against the CHADO database                  |
| insert                | insert a new entity of a specified type into the CHADO database      |
| delete                | delete an entity of a specified type from the CHADO database         |
| import                | import entities of a specified type into the CHADO database          |
| admin                 | perform admin tasks, such as creating or dumping a CHADO database    |
------------------------------------------------------------------------------------------------

## Examples

Create a new CHADO database called `eukaryotes` according to the current GMOD schema:

    chado admin create eukaryotes
    chado admin setup -s gmod eukaryotes
    
Dump this database into an archive called `eukaryotes.dump`:

    chado admin dump eukaryotes eukaryotes.dump

List all organisms in the `eukaryotes` database:

    chado extract organisms eukaryotes

Query the database to check the meaning of a certain `cvterm_id`:

    chado query -q "SELECT name FROM cvterm WHERE cvterm_id = 25" eukaryotes


## Note

Unless explicitly specified by the flag `-c`, all commands employ the [default connection settings](pychado/data/defaultDatabase.yml).
You can change these by running `chado init`.
