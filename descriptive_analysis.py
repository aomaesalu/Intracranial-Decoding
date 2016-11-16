#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from lib.io import read_data


def run(input_path):

    # Read the data set
    data = read_data(input_path)

    print('--------------------------------------------------')
    print('Descriptive analysis')
    print('--------------------------------------------------')

    # Analyse keys
    keys = sorted(data.keys())
    print('There are ' + str(len(keys)) + ' keys in total:')
    print('  ' + str(keys))
    print('')

    # Analyse subjects
    subjects = sorted(list(set(data['subjects'])))
    print('There are ' + str(len(subjects)) + ' unique subjects tests were ' +
          'performed on:')
    print('  ' + str(subjects))
    print('Their frequencies within the data set are the following:')
    # TODO
    print('')

    # Analyse Brodmann areas
    areas = sorted(list(set(data['areas'])))
    print('There are ' + str(len(areas)) + ' unique Brodmann areas used in ' +
          'the tests:')
    print('  ' + str(areas))
    print('Their frequencies within the data set are the following:')
    # TODO
    print('')

    # Analyse image categories
    image_categories = sorted(list(set(data['image_category'])))
    print('There are ' + str(len(image_categories)) + ' unique image ' +
          'categories that the images have been classified into:')
    print('  ' + str(image_categories))
    print('Their frequencies within the data set are the following:')
    # TODO
    print('')

    # Analyse tests
    print('In total, there were ' + str(len(data['subjects'])) + ' tests ' +
          'performed on each of the ' + str(len(data['image_category'])) + ' ' +
          'images. For each of these test and image pairs, there is an ' +
          'integer denoting the neural response in the specifed Brodmann ' +
          'area of the specified patient after showing them the specified ' +
          'image.')


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
