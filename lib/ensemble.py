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

    pass # TODO

    # Return the classification results of the ensemble based on a popularity
    # vote
    return None
