#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from lib.io import read_data
from sklearn import svm

def run(train_path, test_path):
	 train_data = read_data(train_path)
	 test_data = read_data(test_path)
	 
	 #TODO fit data into arrays that can be used by svc
	 
	 svcClassif = svm.SVC()
	 #svcClassif.fit(trainSamples, trainFeatures)
	 #svcClassif.predict(testSamples)
	

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
