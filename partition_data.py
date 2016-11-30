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



def run(input_path, output_path, cv_amount, use_even_distribution):

    # Read the data set
    data = read_data(input_path)

    # Find the number of images in the data set
    number_of_images = len(data['image_category'])

    # Find all image classes in the data set
    classes = sorted(set(data['image_category']))

    # Initialise the list of partitioned indices
    partitioned_indices = [[] for i in range(cv_amount)]

    # If even distribution is set to be used, partition data within each class
    # separately and merge the resulting partitions into the partitioned
    # indices list, so the image class distribution in each partition would be
    # roughly the same.
    if use_even_distribution:

        # Construct a list of image indices corresponding to each image class
        indices = {}
        for image_class in classes:
            indices[image_class] = []
        for i in range(number_of_images):
            indices[data['image_category'][i]].append(i)

        # Randomly split each of these lists into k nearly equal parts, and
        # merge them by partitions
        for image_class in classes:

            # Partition the indices list for the current image class into k
            # nearly equal parts
            partitions_list = partition_list(indices[image_class], cv_amount)

            # Shuffle the partition list to ensure that cumulative partitions
            # after merging by partitions are roughly of equal size
            shuffle(partitions_list)

            # Merge the partitioned indices list for the current image class
            # into the general partitioned indices list by partitions
            for i in range(cv_amount):
                partitioned_indices[i] += partitions_list[i]

    # If even distribution is not set to be used, partition data randomly.
    else:

        # Partition the indices list into k nearly equal parts
        partitioned_indices = partition_list(range(number_of_images), cv_amount)

    # Sort all of the partitions
    for partition in partitioned_indices:
        partition.sort()

    # Partition data
    partitions = []
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
    PARSER.add_argument('cv_amount', help='the amount of equal sized data ' +
                        'sets created upon partitioning the data', type=int)
    PARSER.add_argument('--even', help='ensure that the distribution of ' +
                        'classes in partitions is even', action='store_true')
    ARGUMENTS = PARSER.parse_args()

    # Run the data partition script
    run(ARGUMENTS.input_path, ARGUMENTS.output_path, ARGUMENTS.cv_amount,
        ARGUMENTS.even)
