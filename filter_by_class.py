#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from lib.io import read_data


def run(input_path, output_path, classes):

    pass


if __name__ == '__main__':

    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('input_path', help='the pickled raw input data set ' +
                        'file path')
    PARSER.add_argument('output_path', help='the pickled filtered output ' +
                        'data set file path')
    PARSER.add_argument('classes', help='the list of classes that are kept ' +
                        'the data set')
    ARGUMENTS = PARSER.parse_args()

    # Run the data filtering script
    run(ARGUMENTS.input_path, ARGUMENTS.output_path, ARGUMENTS.classes)
