#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

'''
This module contains all I/O functionality necessary to perform the analysis.
All file I/O operations are carried out with pickled data.
'''

try:
    from cPickle import load, dump
except ImportError:
    from pickle import load, dump


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
    # Open the output file at the specified path
    with open(path, 'wb') as output_file:

        # Dump data into the output data file
        dump(data, output_file)
