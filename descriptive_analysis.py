#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from lib.io import read_data


def run(input_path):

    # Read the data set
    data = read_data(input_path)

    # TODO: Analysis


if __name__ == '__main__':

    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('input_path', help='the pickled input data file \
                                            containing the neural responses \
                                            data')
    ARGUMENTS = PARSER.parse_args()

    # Run the descriptive analysis script
    run(ARGUMENTS.input_path)