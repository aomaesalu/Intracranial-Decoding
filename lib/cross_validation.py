#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i


def construct_data_sets(data, cv_amount, test_index):

    # Initialise the training data
    train_data = {
        'subjects': data[0]['subjects'],
        'areas': data[0]['areas'],
        'image_category': [],
        'neural_responses': []
    }

    # Iterate through all of the partitioned data sets to construct the training
    # data set
    for i in range(cv_amount):

        # If the current data set corresponds to the test data set index set,
        # skip that data set
        if i == test_index:
            continue

        # Add the corresponding image categories and neural responses from the
        # partitioned data set into the training data set
        for field in ['image_category', 'neural_responses']:
            train_data[field] += data[i][field]

    # Copy data into the test data set from the partitioned data set with the
    # specified index
    test_data = data[test_index]

    # Return the training and test data sets
    return train_data, test_data
