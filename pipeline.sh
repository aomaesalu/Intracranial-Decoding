#!/bin/bash

# Define file paths
raw_data_file='data/stim_probe_category_ON_meangamma_bipolar_noscram_artif_brodmann_resppositive.pkl'
filtered_data_file='data/filtered.pkl'
partition_file='data/partition.pkl'

# Split file name and extension
partition_file_name=${partition_file%.*}
partition_file_extension=${partition_file##*.}

# Filter the raw data by classes
printf '# Pipeline: Filtering data by classes'
python ./filter_by_class.py $raw_data_file $filtered_data_file 10 20 30 40 50
printf '\n\n'

# Descriptive analysis of the data set. This is not necessaryly a part of the
# pipeline, as the data set does not change, but it is still currently included
# for the purposes of clarity.
printf '# Pipeline: Descriptive analysis\n'
python ./descriptive_analysis.py $filtered_data_file
printf '\n'

# Set how many equal parts to partition the data into.
k=10

# Set how many times to perform cross-validation.
N=5

# Data partitioning. We use stratified k-fold cross-validation N times.
printf '# Pipeline: Partitioning data %d times into %d equal sets\n' $N $k
for (( i=1; i<=N; i++ ))
do
    python ./partition_data.py $filtered_data_file $partition_file_name'-'$i'.'$partition_file_extension $k --even
done
printf '\n'

# Analysis: SVM
printf '# Pipeline: SVM\n'
python ./svm.py $partition_file $k $N
printf '\n'

# Analysis: SVM
printf '# Pipeline: Random forests\n'
python ./random_forest.py $partition_file $k $N
printf '\n'
