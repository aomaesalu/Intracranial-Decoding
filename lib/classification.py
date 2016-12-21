#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from .string import pad
from .cross_validation import construct_data_sets
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier


class Result(object):

    def __init__(self):

        # Intialise the true and predicted value lists
        self.true_values = []
        self.predicted_values = []

        # Initialise the result confusion matrix and scores per each class
        self.classes = None
        self.confusion_matrix = None
        self.scores_per_class = None
        self.average_scores = None


    def add_values(self, true_values, predicted_values):

        # Append the new true and predicted values to the existing lists
        self.true_values += list(true_values)
        self.predicted_values += list(predicted_values)


    def calculate(self):

        # Find all classes in the results
        self.classes = sorted(set(self.true_values) | \
                              set(self.predicted_values))

        # Calculate the score matrix
        self.confusion_matrix = confusion_matrix(self.true_values,
                                                 self.predicted_values,
                                                 labels=self.classes)

        # Calculate the scores per each class
        self.scores_per_class = precision_recall_fscore_support(self.true_values, self.predicted_values)

        # Calculate the average score
        # We are using macro averaging because it doesn't take class
        # distribution inbalance into account. Each class is as important as
        # another.
        self.average_scores = precision_recall_fscore_support(self.true_values, self.predicted_values, labels=self.classes, average='macro')


    def class_precision(self, class_name):
        return self.scores_per_class[0][self.classes.index(class_name)]


    def class_recall(self, class_name):
        return self.scores_per_class[1][self.classes.index(class_name)]


    def class_f1(self, class_name):
        return self.scores_per_class[2][self.classes.index(class_name)]


    def class_support(self, class_name):
        return self.scores_per_class[3][self.classes.index(class_name)]


    def average_precision(self):
        return self.average_scores[0]


    def average_recall(self):
        return self.average_scores[1]


    def average_f1(self):
        return self.average_scores[2]


    def average_support(self):
        return self.average_scores[3]


    def confusion_matrix_output(self):

        # Add the the title of the output
        output = 'Confusion matrix:\n'

        # Add the header row
        output += pad('', 12)
        for class_label in self.classes:
            output += pad(class_label, 8)
        output += '\n'

        # Add the table itself
        for i in range(len(self.classes)):
            output += pad('', 4) + pad(self.classes[i], 8)
            for j in range(len(self.classes)):
                output += pad(self.confusion_matrix[i][j], 8)
            output += '\n'

        # Return the output string
        return output


    def scores_per_class_output(self):

        # Define scoring methods used
        methods = ['precision', 'recall', 'f1', 'support']

        # Add the title of the output
        output = 'Scores per class:\n'

        # Add the header row
        output += pad('', 15)
        for class_label in self.classes:
            output += pad(class_label, 16)
        output += '\n'

        # Add the table itself
        for i in range(len(methods)):
            output += pad('', 4) + pad(methods[i], 11)
            for j in range(len(self.classes)):
                output += pad(self.scores_per_class[i][j], 16)
            output += '\n'

        # Return the output string
        return output


    def average_scores_output(self):

        # Define scoring methods used
        methods = ['precision', 'recall', 'f1']

        # Add the title of the output
        output = 'Average scores:\n'

        # Add the table
        for i in range(len(methods)):
            output += pad('', 4) + pad(methods[i], 11) + \
                      pad(self.average_scores[i], 16) + '\n'

        # Return the output string
        return output


    def __str__(self):
        return self.confusion_matrix_output() + '\n' + \
               self.scores_per_class_output() + '\n' + \
               self.average_scores_output()


def classify(data, classifier):

    # Initialise the result of the classification
    result = Result()

    # Repeat cross-validation a set amount of times
    for iteration_data in data:

        # Iterate through all of the data sets, using each of them for test
        # data exactly once, and using all others as training data sets
        for test_index in range(len(iteration_data)):

            # Construct training and test data sets
            train_data, test_data = construct_data_sets(iteration_data,
                                                        test_index)

            # Classification
            classifier.fit(train_data['neural_responses'],
                           train_data['image_category'])

            # Prediction
            predicted_values = classifier.predict(test_data['neural_responses'])

            # Add the true and predicted values to the result
            result.add_values(test_data['image_category'], predicted_values)

    # Calculate the confusion matrix and the scores for each class
    result.calculate()

    # Return results
    return result


def get_true_values(data):

    # Initialise the true values list
    true_values = []

    # Repeat cross-validation a set amount of times
    for iteration_data in data:

        # Iterate through all of the data sets, using each of them for test data
        # exactly once, and using all others as training data sets
        for test_index in range(len(iteration_data)):

            # Construct training and test data sets
            train_data, test_data = construct_data_sets(iteration_data,
                                                        test_index)

            # Add the true values to the result list
            true_values += test_data['image_category']

    # Return the list of true values in the data set
    return true_values


classifierFromAlgorithm = {
    'svm': svm.SVC(),
    'random_forest': RandomForestClassifier(n_estimators=500)
}
