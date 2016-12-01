#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from lib.io import read_data, write_data


def run(input_path, output_path, classes):

    # Read the input data set from the specified input path
    input_data = read_data(input_path)

    # Change the list of classes to a set
    classes = set(classes)

    # Construct the output data set, filtering to only have the selected classes
    output_data = {
        'subjects': input_data['subjects'],
        'areas': input_data['areas'],
        'image_category': [],
        'neural_responses': []
    }
    for i in range(len(input_data['image_category'])):
        if input_data['image_category'][i] in classes:
            for field in ['image_category', 'neural_responses']:
                output_data[field].append(input_data[field][i])

    # Write the output data set to the specified output path
    write_data(output_path, output_data)


if __name__ == '__main__':

    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('input_path', help='the pickled raw input data set ' +
                        'file path')
    PARSER.add_argument('output_path', help='the pickled filtered output ' +
                        'data set file path')
    PARSER.add_argument('classes', help='the list of classes that are kept ' +
                        'the data set', nargs='+', type=int)
    ARGUMENTS = PARSER.parse_args()

    # Run the data filtering script
    run(ARGUMENTS.input_path, ARGUMENTS.output_path, ARGUMENTS.classes)
