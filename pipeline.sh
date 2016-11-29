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
    printf '# Pipeline: Partitioning data (%d)\n' $i
    python2.7 ./partition_data.py data/stim_probe_category_ON_meangamma_bipolar_noscram_artif_brodmann_resppositive.pkl data/train-$i.pkl data/test-$i.pkl 80
    printf '\n'
done

# Analysis: SVM
for (( i=1; i<=N; i++ ))
do
    printf '# Pipeline: SVM (%d)\n' $i
    python2.7 ./svm.py data/train-$i.pkl data/test-$i.pkl
    printf '\n'
done

# Analysis: Random forests
for (( i=1; i<=N; i++ ))
do
    printf '# Pipeline: Random forests (%d)\n' $i
    python2.7 ./random_forest.py data/train-$i.pkl data/test-$i.pkl
    printf '\n'
done
