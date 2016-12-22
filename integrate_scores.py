#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from lib.io import read_data, write_data


def run(raw_input_path, output_path, time_windows, frequency_bands):

    # Convert time windows to integers
    time_windows = [int(time_window) for time_window in time_windows]

    # Initialise the integrated data dictionary
    integrated = {}
    for time_window in time_windows:
        integrated[time_window] = {}
    for time_window in time_windows:
        for frequency_band in frequency_bands:
            integrated[time_window][frequency_band] = None

    # Read F1-scores from the input files into the integrated data dictionary

    # Iterate through each time window and frequency band pair
    for time_window in time_windows:
        for frequency_band in frequency_bands:

            # Construct the input file path
            input_path = raw_input_path.replace('TIMEWINDOW', str(time_window))\
                .replace('FREQUENCYBAND', frequency_band)

            # Read the input file
            input_data = read_data(input_path)

            print(input_data)

            # Add the F1-score received from the data into the integrated data
            # dictionary
            integrated[time_window][frequency_band] = input_data.average_f1()

    print(integrated)

    # Output the integrated scores into the specified file
    write_data(output_path, integrated)


if __name__ == '__main__':

    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('input_path', help='the pickled input data file path')
    PARSER.add_argument('output_path', help='the pickled output data file ' +
                        'path')
    PARSER.add_argument('time_windows', help='the list of time windows used')
    PARSER.add_argument('frequency_bands', help='the list of frequency bands ' +
                        'used')
    ARGUMENTS = PARSER.parse_args()

    # Run the score integration script
    run(ARGUMENTS.input_path, ARGUMENTS.output_path,
        ARGUMENTS.time_windows.split(' '), ARGUMENTS.frequency_bands.split(' '))
