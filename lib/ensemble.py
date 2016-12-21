#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i


def select_best_classifiers(results, proportion):

    # Determine the amount of best classifiers to be returned
    amount = int(round(len(results) * proportion))
    if amount == 0:
        amount = 1

    # Return the list of best classifiers in the classification results list
    return sorted(results, key=lambda k: k['f1'], reverse=True)[:amount]


def construct_disagreement_matrix(results):

    pass # TODO

    # Return the disagreement matrix of the classification results list
    return None # TODO


def filter_most_disagreeing(results, disagreement):

    pass # TODO

    # Return the most disagreeing classifiers in the classification results list
    return None # TODO


def construct_ensemble(results, best_proportion, used_proportion):

    # Select best classifiers
    best_results = select_best_classifiers(results, best_proportion)

    # Measure pairwise disagreement
    disagreement = construct_disagreement_matrix(best_results)

    # Filter results that disagree with each other the most
    ensemble = filter_most_disagreeing(best_results, disagreement)

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
