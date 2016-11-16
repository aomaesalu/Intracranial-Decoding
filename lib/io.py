#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from cPickle import load, dump


def read_data(path):
    # Initialise the data array as None
    data = None
    # Open the pickled data file at the specified path
    with open(path, 'rb') as input_file:
        # Load data from the input data file
        data = load(input_file)
    # Return the retrieved data
    return data


def write_data(path, data):
    # Open the output file at the specified path
    with open(path, 'wb') as output_file:
        # Dump data into the output data file
        dump(data, output_file)
