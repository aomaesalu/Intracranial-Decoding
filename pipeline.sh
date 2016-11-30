#!/bin/bash

# Descriptive analysis of the data set. This is not necessaryly a part of the
# pipeline, as the data set does not change, but it is still currently included
# for the purposes of clarity.
printf '# Pipeline: Descriptive analysis\n'
python2.7 ./descriptive_analysis.py data/stim_probe_category_ON_meangamma_bipolar_noscram_artif_brodmann_resppositive.pkl
printf '\n'

# Set into how many equal parts to partition the data.
k=10

# Data partitioning. We use stratified k-fold cross-validation.
printf '# Pipeline: Partitioning data\n'
python2.7 ./partition_data.py data/stim_probe_category_ON_meangamma_bipolar_noscram_artif_brodmann_resppositive.pkl data/partition.pkl $k --even
printf '\n'

# Analysis: SVM
printf '# Pipeline: SVM\n'
python2.7 ./svm.py data/partition.pkl $k
printf '\n'

# Analysis: SVM
printf '# Pipeline: Random forests\n'
python2.7 ./random_forest.py data/partition.pkl $k
printf '\n'
