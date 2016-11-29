#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from lib.io import read_data
from lib.brain_data import get_classes
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score


def run(train_path, test_path):

    # Read input data
    train_data = read_data(train_path)
    test_data = read_data(test_path)

    # Find all classes in test data
    classes = get_classes(test_data)

    # Classification
    model = RandomForestClassifier(n_estimators=1000)
    model.fit(train_data['neural_responses'], train_data['image_category'])

    # Prediction
    prediction = model.predict(test_data['neural_responses'])

    # Scoring
    # We are using macro averaging because it doesn't take class distribution
    # inbalance into account. Each class is as important as another.
    # In the future, we should also measure scores for each class separately.
    # Currently, sometimes it can happen that there are no positives for a class
    # and the measure is ruined.
    score = f1_score(test_data['image_category'], prediction,
                     average='macro')
    print('F1 score: ' + str(score))


if __name__ == '__main__':

    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('train_path', help='the pickled input training data \
                                            file path')
    PARSER.add_argument('test_path', help='the pickled input testing data \
                                           file path')
    ARGUMENTS = PARSER.parse_args()

    # Run the data classification script
    run(ARGUMENTS.train_path, ARGUMENTS.test_path)
