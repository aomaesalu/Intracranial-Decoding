#!/bin/bash

# Define file paths
data_file='data/stim_probe_category_ON_meangamma_bipolar_noscram_artif_brodmann_resppositive.pkl'
partition_file='data/partition.pkl'

# Split file name and extension
partition_file_name=${partition_file%.*}
partition_file_extension=${partition_file##*.}

# Descriptive analysis of the data set. This is not necessaryly a part of the
# pipeline, as the data set does not change, but it is still currently included
# for the purposes of clarity.
printf '# Pipeline: Descriptive analysis\n'
python2.7 ./descriptive_analysis.py $data_file
printf '\n'

# Set how many times to perform cross-validation.
N=5

# Set how many equal parts to partition the data into.
k=10

# Data partitioning. We use stratified k-fold cross-validation N times.
for (( i=1; i<=N; i++ ))
do
    printf '# Pipeline: Partitioning data (%d)\n' $i
    python2.7 ./partition_data.py $data_file $partition_file_name'-'$i'.'$partition_file_extension $k --even
    printf '\n'
done

# Analysis: SVM
printf '# Pipeline: SVM\n'
python2.7 ./svm.py $partition_file $k $N
printf '\n'

# Analysis: SVM
printf '# Pipeline: Random forests\n'
python2.7 ./random_forest.py $partition_file $k $N
printf '\n'
