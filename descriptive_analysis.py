#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from collections import Counter
from lib.io import read_data


def output_frequencies(data_list):
    counter = Counter(data_list)
    for key, value in sorted(counter.items(), key=lambda x: (-x[1], x[0])):
        print('  ' + str(key) + ': ' + str(value))


def run(input_path):

    # Read the data set
    data = read_data(input_path)

    # Print header
    print('--------------------------------------------------')
    print('Descriptive analysis')
    print('--------------------------------------------------')

    # Analyse keys
    keys = sorted(data.keys())
    print('There are ' + str(len(keys)) + ' keys in total:')
    print('  ' + str(keys))
    print('')

    # Analyse subjects
    print('There are ' + str(len(set(data['subjects']))) + ' ' +
          'unique subjects tests were performed on.')
    print('Their frequencies within the data set are the following:')
    output_frequencies(data['subjects'])
    print('')

    # Analyse Brodmann areas
    print('There are ' + str(len(set(data['areas']))) + ' ' +
          'unique Brodmann areas used in the tests.')
    print('Their frequencies within the data set are the following:')
    output_frequencies(data['areas'])
    print('')

    # Analyse image categories
    print('There are ' + str(len(set(data['image_category']))) + ' unique ' +
          'image categories that the images have been classified into.')
    print('Their frequencies within the data set are the following:')
    output_frequencies(data['image_category'])
    print('')

    # Analyse tests
    print('In total, there were ' + str(len(data['subjects'])) + ' tests ' +
          'performed on each of the ' + str(len(data['image_category'])) + ' ' +
          'images. For each of these test and image pairs, there is an ' +
          'integer denoting the neural response in the specifed Brodmann ' +
          'area of the specified patient after showing them the specified ' +
          'image.')
    print('--------------------------------------------------')


if __name__ == '__main__':

    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('input_path', help='the pickled input data file \
                                            containing the neural responses \
                                            data')
    ARGUMENTS = PARSER.parse_args()

    # Run the descriptive analysis script
    run(ARGUMENTS.input_path)
