#!/bin/bash

# Descriptive analysis of the data set. This is not necessaryly a part of the
# pipeline, as the data set does not change, but it is still currently included
# for the purposes of clarity.
python2.7 ./descriptive_analysis.py data/stim_probe_category_ON_meangamma_bipolar_noscram_artif_brodmann_resppositive.pkl

# Set the number of different random partitions to use.
N=10

# Data partitioning. We partition the data 80-20 into training and testing sets,
# and create N different random partitions for analysis comparison.
for (( i=1; i<=N; i++ ))
do
    python2.7 ./partition_data.py data/stim_probe_category_ON_meangamma_bipolar_noscram_artif_brodmann_resppositive.pkl data/train-$i.pkl data/test-$i.pkl 80
done

# Analysis: SVM
# TODO
#for (( i=1; i<=N; i++ ))
#do
#  python2.7 ./svm.py data/train-1.pkl data/test-1.pkl
#done

# Analysis: Random forests
# TODO
#for (( i=1; i<=N; i++ ))
#do
#  python2.7 ./random_forest.py data/train-1.pkl data/test-1.pkl
#done
