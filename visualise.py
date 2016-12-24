#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from lib.io import read_data


def run(input_path, output_path):

    # Read the integrated score results
    scores = read_data(input_path)

    # Visualise the scores as a heatmap
    pass # TODO

    # Save the heatmap to the specified destination
    pass # TODO


if __name__ == '__main__':

    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('input_path', help='the pickled input data file path ' +
                        'containing all of the integrated scores')
    PARSER.add_argument('output_path', help='the heatmap output path')
    ARGUMENTS = PARSER.parse_args()

    # Run the results visualisation script
    run(ARGUMENTS.input_path, ARGUMENTS.output_path)
