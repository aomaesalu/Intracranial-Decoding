#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

# TODO: Add a parameter for ensuring that the data distribution within the test
# and training sets is the same.

from argparse import ArgumentParser
from random import sample
from lib.io import read_data, write_data


def run(input_path, train_path, test_path, train_size, is_even):

    # Read the data set
    data = read_data(input_path)

    # Find the number of images in the data set
    number_of_images = len(data['image_category'])

    # Find all image classes in the data set
    classes = sorted(set(data['image_category']))

    # Construct a list of indices of appropriate images for each image class
    index_lists = {}
    for image_class in classes:
        index_lists[image_class] = []
    for i in range(number_of_images):
        index_lists[data['image_category'][i]].append(i)

    # Generate the training set indices
    train_indices = []
    for image_class in classes:
        images_in_class = len(index_lists[image_class])
        train_indices += sample(index_lists[image_class], \
                                int(images_in_class * float(train_size) / 100))
    train_indices.sort()

    # Calculate the test set indices
    test_indices = sorted(list(set(range(number_of_images)) \
                               - set(train_indices)))

    # Partition data
    train_data = {
        'subjects': data['subjects'],
        'areas': data['areas'],
        'image_category': [data['image_category'][i] for i in train_indices],
        'neural_responses': [data['neural_responses'][i] for i in train_indices]
    }
    test_data = {
        'subjects': data['subjects'],
        'areas': data['areas'],
        'image_category': [data['image_category'][i] for i in test_indices],
        'neural_responses': [data['neural_responses'][i] for i in test_indices]
    }

    # Save data
    write_data(train_path, train_data)
    write_data(test_path, test_data)


if __name__ == '__main__':

    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('input_path', help='the pickled input data file ' +
                        'containing the neural responses data')
    PARSER.add_argument('train_path', help='the pickled output training data ' +
                        'file path')
    PARSER.add_argument('test_path', help='the pickled output testing data ' +
                        'file path')
    PARSER.add_argument('train_size', help='the size of the training data set')
    PARSER.add_argument('--even', help='ensure that the distribution of ' +
                        'classes in partitions is even', action='store_true')
    ARGUMENTS = PARSER.parse_args()

    # Run the data partition script
    run(ARGUMENTS.input_path, ARGUMENTS.train_path, ARGUMENTS.test_path,
        ARGUMENTS.train_size, ARGUMENTS.even)
