#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from lib.io import read_data
from sklearn import svm


def run(train_path, test_path):
    
    # Read input data
    train_data = read_data(train_path)
    test_data = read_data(test_path)

    print('Performing SVM classifier...')
    svcClassif = svm.SVC()
    print('Fitting training samples to create a training model...')

    #TODO not sure if this is the correct type of data that should be used for fitting, but this
    #should be the general sequence of the classification

    #first parameter: array of size [n_samples, n_features], second parameter: array of size [n_samples]
    svcClassif.fit(train_data['neural_responses'], train_data['image_category'])
    print('Performing classification on test samples...')
    results=svcClassif.predict(test_data['neural_responses'])
    print 'Resulting classifications: ', results
    print 'Actual classes: ', test_data['image_category']


if __name__ == '__main__':

    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('train_path', help='the pickled output training data \
                                            file path')
    PARSER.add_argument('test_path', help='the pickled output testing data \
                                           file path')
    ARGUMENTS = PARSER.parse_args()

    # Run the data partition script
    run(ARGUMENTS.train_path, ARGUMENTS.test_path)
