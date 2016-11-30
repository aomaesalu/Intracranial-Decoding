#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from random import shuffle
from lib.io import read_data, write_data


def partition_list(data, amount):

    # Shuffle the list
    shuffle(data)

    # Find the average partition size
    size = len(data) / float(amount)

    # Partition the list into k equal parts, and return each of them in a
    # sorted format
    return [sorted(data[int(round(size * i)) : int(round(size * (i + 1)))])
            for i in range(amount)]


def format_path(path, number):

    # Split the path by points to find the file extension
    path = path.split('.')

    # Add the number just before the file extension, and return the updated
    # file path
    return '.'.join(path[:-1]) + '-' + str(number) + '.' + path[-1]



def run(input_path, output_path, cv_amount, is_even):

    # Read the data set
    data = read_data(input_path)

    # Find the number of images in the data set
    number_of_images = len(data['image_category'])

    # Find all image classes in the data set
    classes = sorted(set(data['image_category']))

    # Construct a list of image indices corresponding to each image class
    indices = {}
    for image_class in classes:
        indices[image_class] = []
    for i in range(number_of_images):
        indices[data['image_category'][i]].append(i)

    # Randomly split each of these lists into k nearly equal parts, and merge
    # them by partitions
    partitioned_indices = [[] for i in range(cv_amount)]
    for image_class in classes:
        partitions = partition_list(indices[image_class], cv_amount)
        for i in range(cv_amount):
            partitioned_indices[i] += partitions[i]

    # Sort all of the partitions
    for partition in partitioned_indices:
        partition.sort()

    # Partition data
    for i in range(cv_amount):
        partitions.append({
            'subjects': data['subjects'],
            'areas': data['areas'],
            'image_category': [data['image_category'][j]
                               for j in partitioned_indices[i]],
           'neural_responses': [data['neural_responses'][j]
                                for j in partitioned_indices[i]]
        })

    # Save partitioned data
    for i in range(cv_amount):
        write_data(format_path(output_path, i + 1), partitions[i])


if __name__ == '__main__':

    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('input_path', help='the pickled input data file ' +
                        'path containing the neural responses data')
    PARSER.add_argument('output_path', help='the pickled output data file ' +
                        'path')
    PARSER.add_argument('cv_amount', help='how many equal sized data sets ' +
                        'are created', type=int)
    PARSER.add_argument('--even', help='ensure that the distribution of ' +
                        'classes in partitions is even', action='store_true')
    ARGUMENTS = PARSER.parse_args()

    # Run the data partition script
    run(ARGUMENTS.input_path, ARGUMENTS.output_path, ARGUMENTS.cv_amount,
        ARGUMENTS.even)
