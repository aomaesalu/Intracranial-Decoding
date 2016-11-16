#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from .lib.io import read_data


def run(input_path, train_path, test_path):

    # Read the data set
    data = read_data(input_path)

    # TODO: Partitioning


if __name__ == '__main__':

    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('input_path', help='the pickled input data file \
                                            containing the neural responses \
                                            data')
    PARSER.add_argument('train_path', help='the pickled output training data \
                                            file path')
    PARSER.add_argument('test_path', help='the pickled output testing data \
                                           file path')
    ARGUMENTS = PARSER.parse_args()

    # Run the data partition script
    run(ARGUMENTS.input_path, ARGUMENTS.train_path, ARGUMENTS.test_path)
