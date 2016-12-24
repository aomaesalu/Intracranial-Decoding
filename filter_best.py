#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from lib.io import read_data, write_data


def run(input_path, output_path):

    # Read the results as input data
    results = read_data(input_path)

    # Retrieve the best result
    best_result = sorted(results, key=lambda k: k.average_f1(), reverse=True)[0]

    # Output the score into the specified file
    write_data(output_path, best_result)


if __name__ == '__main__':

    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('input_path', help='the pickled data input file ' +
                        'containing all of the classification results')
    PARSER.add_argument('output_path', help='the pickled data output file to ' +
                        'contain only the best result')
    ARGUMENTS = PARSER.parse_args()

    # Run the best score filtering script
    run(ARGUMENTS.input_path, ARGUMENTS.output_path)
