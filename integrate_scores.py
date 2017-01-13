#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from lib.io import read_data, write_data


def run(raw_input_path, output_path_recall, output_path_precision,
        output_path_f1, time_windows, frequency_bands):

    # Convert time windows to integers
    time_windows = [int(time_window) for time_window in time_windows]

    # Initialise the integrated score data dictionaries
    integrated_recall = {}
    integrated_precision = {}
    integrated_f1 = {}
    for time_window in time_windows:
        integrated_recall[time_window] = {}
        integrated_precision[time_window] = {}
        integrated_f1[time_window] = {}
    for time_window in time_windows:
        for frequency_band in frequency_bands:
            integrated_recall[time_window][frequency_band] = None
            integrated_precision[time_window][frequency_band] = None
            integrated_f1[time_window][frequency_band] = None

    # Read F1-scores from the input files into the integrated data dictionary

    # Iterate through each time window and frequency band pair
    for time_window in time_windows:
        for frequency_band in frequency_bands:

            # Construct the input file path
            input_path = raw_input_path.replace('TIMEWINDOW', str(time_window))\
                .replace('FREQUENCYBAND', frequency_band)

            # Read the input file
            input_data = read_data(input_path)

            # Add the F1-score received from the data into the integrated data
            # dictionary
            integrated_recall[time_window][frequency_band] = input_data.average_recall()
            integrated_precision[time_window][frequency_band] = input_data.average_precision()
            integrated_f1[time_window][frequency_band] = input_data.average_f1()

    # Output the integrated scores into the specified files
    write_data(output_path_recall, integrated_recall)
    write_data(output_path_precision, integrated_precision)
    write_data(output_path_f1, integrated_f1)


if __name__ == '__main__':

    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('input_path', help='the pickled input data file path')
    PARSER.add_argument('output_path_recall', help='the pickled output ' +
                        'recall results data file path')
    PARSER.add_argument('output_path_precision', help='the pickled output ' +
                        'precision results data file path')
    PARSER.add_argument('output_path_f1', help='the pickled output f1-score ' +
                        'results data file path')
    PARSER.add_argument('time_windows', help='the list of time windows used')
    PARSER.add_argument('frequency_bands', help='the list of frequency bands ' +
                        'used')
    ARGUMENTS = PARSER.parse_args()

    # Run the score integration script
    run(ARGUMENTS.input_path, ARGUMENTS.output_path_recall,
        ARGUMENTS.output_path_precision, ARGUMENTS.output_path_f1,
        ARGUMENTS.time_windows.split(' '), ARGUMENTS.frequency_bands.split(' '))
