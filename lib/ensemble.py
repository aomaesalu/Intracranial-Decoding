#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i


def select_best_classifiers(results, proportion):

    # Determine the amount of best classifiers to be returned
    amount = int(round(len(results) * proportion))
    if amount == 0:
        amount = 1

    # Return the list of best classifiers in the classification results list
    return sorted(results, key=lambda k: k['f1'], reverse=True)[:amount]


def calculate_disagreement(values_1, values_2):

    # Initialise the disagreement metric
    disagreement = 0

    # Iterate through all values in both lists
    for i in range(len(values_1)):

        # If the values do not match, increment the disagreement metric by 1
        if values_1[i] != values_2[i]:
            disagreement += 1

    # Return the disagreement metric
    return disagreement


def construct_disagreement_matrix(results):

    # Initialise the disagreement matrix
    matrix = [[[]] * len(results)] * len(results)

    # Iterate through all result pairs
    for i in range(len(results)):
        for j in range(i + 1, len(results)):

            # Calculate the disagreement of these two results
            values_1 = results[i]['predicted_values']
            values_2 = results[j]['predicted_values']
            disagreement = calculate_disagreement(values_1, values_2)

            # Add the disagreement to the disagreement matrix
            matrix[i][j] = disagreement
            matrix[j][i] = disagreement

    # Return the disagreement matrix of the classification results list
    return disagreement


def calculate_sums(matrix):

    # Calculate the row and column sums
    row_sums = [[0]] * len(matrix)
    column_sums = [[0]] * len(matrix[0])
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            row_sums[i] += matrix[i][j]
            column_sums[j] += matrix[i][j]

    # Return the row and column sums in the matrix
    return row_sums, column_sums


def filter_most_disagreeing(results, proportion):

    # Determine the amount of classifiers to be included in the ensemble
    amount = int(round(len(results) * proportion))
    if amount == 0:
        amount = 1

    # Measure pairwise disagreement
    disagreement = construct_disagreement_matrix(best_results)

    # Calculate the row and column sums of the disagreement matrix
    row_sums, column_sums = calculate_sums(disagreement)

    # Iterate the removal of results until only the specified amount is left.
    # Note that as the disagreement matrix is symmetric, we only use the column
    # sums in the calculation.
    for i in range(len(results) - amount):

        # Find the index of the result that disagrees with others the least
        index = column_sums.index(min(column_sums))

        # Remove that result's values from the column sums
        for j in range(len(column_sums)):
            column_sums[j] -= disagreement[index][j]

        # Remove that result's index from the column sums
        del column_sums[index]

        # Remove that result's row from the disagreement matrix
        del disagreement[index]

        # Remove that result's index from the results list
        del results[index]

    # Return the most disagreeing classifiers in the classification results list
    return results


def construct_ensemble(results, best_proportion, used_proportion):

    # Select best classifiers
    best_results = select_best_classifiers(results, best_proportion)

    # Filter results that disagree with each other the most
    ensemble = filter_most_disagreeing(best_results, used_proportion)

    # Return the ensemble constructed in the process
    return ensemble


def ensemble_vote(results):

    # Initialise the list of predicted values
    predicted_values = []

    # Iterate through each value to be predicted
    for i in range(len(results[0])):

        # Initialise the frequency dictionary
        frequency = {}

        # Iterate through all results
        for result in results:

            # Retrieve the current predicted value of the current result
            value = result['predicted_values'][i]

            # If the value does not exist in the frequency dictionary, add it
            # with an initial count of 1 (the current result value). If it does
            # exist, increment the corresponding value by 1.
            if value not in frequency:
                frequency[value] = 1
            else:
                frequency[value] += 1

        # Append the most popular value to the list of predicted values
        predicted_values.append(max(frequency, key=frequency.get))

    # Return the classified predicted values of the ensemble based on a
    # popularity vote
    return predicted_values
