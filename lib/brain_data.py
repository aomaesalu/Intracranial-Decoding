#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i


def get_classes(data):

    # Initalise the classes set
    classes = set()

    # Iterate through each image category in the data set
    for image_category in data['image_category']:

        # If the current image category has not yet been added to the class set,
        # add it. Otherwise, do nothing.
        if image_category not in classes:
            classes.add(image_category)

    # Return a sorted list of all of the classes in the data set
    return sorted(classes)
