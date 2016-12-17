#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from .io import read_data
from .string import pad, add_suffix_to_path
from .cross_validation import construct_data_sets
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support


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


def classify(data_path, partitions, iterations, model):

    # Initialise the result of the classification
    result = Result()

    # Repeat cross-validation a set amount of times
    for iteration in range(iterations):

        # Read input data
        data = []
        for partition in range(partitions):
            file_path = add_suffix_to_path(data_path, '-', iteration + 1,
                                           partition + 1)
            data.append(read_data(file_path))

        # Iterate through all of the data sets, using each of them for test data
        # exactly once, and using all others as training data sets at the same
        for test_index in range(partitions):

            # Construct training and test data sets
            train_data, test_data = construct_data_sets(data, partitions,
                                                        test_index)

            # Classification
            model.fit(train_data['neural_responses'],
                      train_data['image_category'])

            # Prediction
            predicted_values = model.predict(test_data['neural_responses'])

            # Add the true and predicted values to the result
            result.add_values(test_data['image_category'], predicted_values)

    # Calculate the confusion matrix and the scores for each class
    result.calculate()

    # Return results
    return result
