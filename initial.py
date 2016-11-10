# imports
import numpy as np
import cPickle

# load data
with open('stim_probe_category_ON_meangamma_bipolar_noscram_artif_brodmann_resppositive.pkl', 'rb') as infile:
    dataset = cPickle.load(infile)

# get to know the dataset structure
print(dataset.keys())
print(dataset['neural_responses'].shape)
print(len(dataset['subjects']))
print(dataset['image_category'].shape)
print(dataset['areas'].shape)
print('')
print(len(set(dataset['areas'])))
