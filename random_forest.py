#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from lib.io import read_data
from lib.score import ConfusionMatrix, Score
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier

from collections import Counter
import numpy as np


def run(train_path, test_path):

    # Read input data
    train_data = read_data(train_path)
    test_data = read_data(test_path)

    # counter = Counter(train_data['areas'])
    # removed_areas = set()
    # for key, value in counter.items():
    #     if value < 10:
    #         removed_areas.add(key)
    # print('Removed areas:')
    # print(removed_areas)
    #
    # removed_indices = []
    # for i in range(len(train_data['areas'])):
    #     if train_data['areas'][i] in removed_areas:
    #         removed_indices.append(i)
    # print('Removed indices')
    # print(removed_indices)
    #
    # train_data['neural_responses'] = np.delete(train_data['neural_responses'], removed_indices, 1)
    # test_data['neural_responses'] = np.delete(test_data['neural_responses'], removed_indices, 1)
    #
    # print(len(train_data['neural_responses'][0]))
    #
    # counter = Counter(train_data['subjects'])
    # removed_subjects = set()
    # for key, value in counter.items():
    #     if value < 5:
    #         removed_subjects.add(key)
    # print('Removed subjects:')
    # print(removed_subjects)
    #
    # removed_indices = []
    # for i in range(len(train_data['subjects'])):
    #     if train_data['subjects'][i] in removed_subjects:
    #         removed_indices.append(i)
    # print('Removed indices')
    # print(removed_indices)
    #
    # train_data['neural_responses'] = np.delete(train_data['neural_responses'], removed_indices, 1)
    # test_data['neural_responses'] = np.delete(test_data['neural_responses'], removed_indices, 1)
    #
    # print(len(train_data['neural_responses'][0]))

    # Classification
    model = ExtraTreesClassifier(n_estimators=1000, max_features=1)
    model.fit(train_data['neural_responses'], train_data['image_category'])

    # Prediction
    prediction = model.predict(test_data['neural_responses'])

    # Scoring
    confusion_matrix = ConfusionMatrix(test_data['image_category'], prediction)
    print(confusion_matrix)
    score = Score(test_data['image_category'], prediction)
    print(score)

if __name__ == '__main__':

    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('train_path', help='the pickled input training data ' +
                                           'file path')
    PARSER.add_argument('test_path', help='the pickled input testing data ' +
                                          'file path')
    ARGUMENTS = PARSER.parse_args()

    # Run the data classification script
    run(ARGUMENTS.train_path, ARGUMENTS.test_path)
