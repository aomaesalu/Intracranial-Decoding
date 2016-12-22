#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

'''
This module contains all I/O functionality necessary to perform the analysis.
All file I/O operations are carried out with pickled data.
'''

from os import makedirs
from os.path import isfile, isdir
from .string import add_suffix_to_path

try:
    from cPickle import load, dump
except ImportError:
    from pickle import load, dump


def ensure_file_existence(path, exists=False):

    # If the file is set to already exist, validate that the specified path
    # is actually a file.
    if exists:
        if not isfile(path):
            raise IOError('The file ' + str(path) + ' does not exist')

    # Otherwise, the file needs to be created. Check the existence of the
    # specified directories in the path, and create the file.
    else:

        # Create the directory path to the file.
        try:
            makedirs(path.rsplit('/', 1)[0])
        except OSError:
            if not isdir(path.rsplit('/', 1)[0]):
                raise

        # Create the new file.
        with open(path, 'w'):
            pass


def read_data(path):
    '''Reads a pickled data file at the specified path, and returns the data
    retrieved.

    Args:
        path:       A string containing the path to the pickled file.

    Returns:
        Data stored in the pickled file.
    '''
    # Initialise the data array as None
    data = None

    # Ensure file existence
    ensure_file_existence(path, True)

    # Open the pickled data file at the specified path
    with open(path, 'rb') as input_file:

        # Load data from the input data file
        data = load(input_file)

    # Return the retrieved data
    return data


def write_data(path, data):
    '''Writes the specified data set into a pickled data file at the specified
    path.

    Args:
        path:       A string containing the path to the pickled file to be
                    created.
        data:       The data to be stored in the pickled file.

    Returns:
        None
    '''
    # Ensure file existence
    ensure_file_existence(path)

    # Open the output file at the specified path
    with open(path, 'wb') as output_file:

        # Dump data into the output data file
        dump(data, output_file)


def read_partitioned_data(raw_path, iterations, partitions):

    # Initialise the partitioned data set list
    data = []

    for iteration in range(1, iterations + 1):
        iteration_data = []
        for partition in range(1, partitions + 1):
            file_path = add_suffix_to_path(raw_path, '-', iteration, partition)
            iteration_data.append(read_data(file_path))
        data.append(iteration_data)

    # Return partitioned data
    return data
